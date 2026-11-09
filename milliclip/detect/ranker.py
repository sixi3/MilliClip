"""Combine detection signals into ranked candidate highlight windows.

Approach: build a per-second weighted "excitement" curve by splatting each signal (with a
small Gaussian-ish spread) onto a timeline, then find local maxima and grow a window
around each peak while the curve stays above a fraction of the peak. Windows are clamped
to configured min/max duration. Each window gets a normalized 0..1 score and a coarse
signature (downsampled curve) used later for dedup.
"""
from __future__ import annotations

import math
from typing import List

from ..config import DetectConfig
from ..models import Candidate, Signal


def _splat(curve: List[float], t: float, strength: float, weight: float,
           spread: float, hz: float) -> None:
    center = int(round(t * hz))
    radius = int(math.ceil(spread * hz))
    for i in range(center - radius, center + radius + 1):
        if 0 <= i < len(curve):
            d = (i - center) / hz
            falloff = math.exp(-(d * d) / (2 * (spread / 2) ** 2 or 1e-6))
            curve[i] += strength * weight * falloff


def build_curve(signals: List[Signal], duration: float, cfg: DetectConfig,
                hz: float = 4.0) -> List[float]:
    n = max(1, int(math.ceil(duration * hz)))
    curve = [0.0] * n
    weights = {
        "loudness": cfg.weight_loudness,
        "scene": cfg.weight_scene,
        "speech": cfg.weight_speech,
    }
    for s in signals:
        w = weights.get(s.kind, 0.5)
        _splat(curve, s.start, s.strength, w, spread=1.5, hz=hz)
    return curve


def _signature(curve: List[float], start_i: int, end_i: int, bins: int = 16) -> List[float]:
    seg = curve[start_i:end_i] or [0.0]
    out = []
    step = max(1, len(seg) // bins)
    for b in range(bins):
        chunk = seg[b * step:(b + 1) * step] or [0.0]
        out.append(sum(chunk) / len(chunk))
    mx = max(out) or 1.0
    return [v / mx for v in out]


def rank_highlights(signals: List[Signal], duration: float, cfg: DetectConfig,
                    has_music: bool = False, hz: float = 4.0) -> List[Candidate]:
    if duration <= 0 or not signals:
        return []
    curve = build_curve(signals, duration, cfg, hz=hz)
    peak = max(curve) if curve else 0.0
    if peak <= 0:
        return []

    grow_floor = 0.35 * peak          # grow window while above this
    peak_floor = 0.45 * peak          # only consider peaks above this
    min_len = int(cfg.min_highlight_seconds * hz)
    max_len = int(cfg.max_highlight_seconds * hz)

    candidates: List[Candidate] = []
    used = [False] * len(curve)

    # Iterate peaks high-to-low so stronger moments claim their window first.
    order = sorted(range(len(curve)), key=lambda i: curve[i], reverse=True)
    for i in order:
        if curve[i] < peak_floor or used[i]:
            continue
        lo = hi = i
        while lo > 0 and curve[lo - 1] >= grow_floor and (hi - lo) < max_len:
            lo -= 1
        while hi < len(curve) - 1 and curve[hi + 1] >= grow_floor and (hi - lo) < max_len:
            hi += 1
        # Enforce minimum length by padding symmetrically.
        while (hi - lo) < min_len:
            if lo > 0:
                lo -= 1
            elif hi < len(curve) - 1:
                hi += 1
            else:
                break
        if any(used[lo:hi + 1]):
            # overlaps an already-claimed window; skip
            continue
        for k in range(lo, hi + 1):
            used[k] = True

        window = curve[lo:hi + 1]
        strength = sum(window) / (len(window) or 1)
        score = max(0.0, min(1.0, strength / peak))
        if has_music:
            score *= (1.0 - cfg.music_penalty)

        reasons = []
        kinds = {s.kind for s in signals if lo / hz <= s.start <= hi / hz}
        if "loudness" in kinds:
            reasons.append("loud moment")
        if "scene" in kinds:
            reasons.append("scene change")
        if "speech" in kinds:
            reasons.append("reaction")
        if has_music:
            reasons.append("music present (penalized)")

        candidates.append(Candidate(
            start=lo / hz, end=hi / hz, score=round(score, 4),
            reasons=reasons, has_music=has_music,
            signature=_signature(curve, lo, hi + 1),
        ))

    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates
