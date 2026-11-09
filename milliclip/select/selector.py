"""Turn ranked candidates into a final, coherent set of clips.

Rules:
- Add lead-in and tail padding so a clip has context and a clean ending.
- Enforce a minimum gap between chosen clips (no two clips from the same beat).
- Drop near-duplicate / repetitive moments via signature cosine similarity.
- Clamp to source bounds and cap the number of clips per run.
Candidates are assumed pre-sorted by score (highest first); we greedily accept.
"""
from __future__ import annotations

from typing import List

from ..config import SelectConfig
from ..models import Candidate, Clip


def cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _overlaps(a_start: float, a_end: float, b_start: float, b_end: float,
              min_gap: float) -> bool:
    # True if windows are closer than min_gap (treating gap as required spacing).
    return not (a_end + min_gap <= b_start or b_end + min_gap <= a_start)


def select_clips(candidates: List[Candidate], source: str, source_duration: float,
                 cfg: SelectConfig) -> List[Clip]:
    chosen: List[Clip] = []
    chosen_cands: List[Candidate] = []

    ordered = sorted(candidates, key=lambda c: c.score, reverse=True)
    for cand in ordered:
        if len(chosen) >= cfg.max_clips_per_run:
            break

        start = max(0.0, cand.start - cfg.lead_in_seconds)
        end = min(source_duration, cand.end + cfg.tail_seconds)
        if end <= start:
            continue

        # Spacing / overlap check against already-chosen clips.
        too_close = any(
            _overlaps(start, end, c.start, c.end, cfg.min_gap_seconds)
            for c in chosen
        )
        if too_close:
            continue

        # Repetition check via signature similarity.
        is_dup = any(
            cosine_similarity(cand.signature, prev.signature) >= cfg.dedup_similarity
            for prev in chosen_cands
            if prev.signature and cand.signature
        )
        if is_dup:
            continue

        chosen.append(Clip(
            source=source, start=round(start, 3), end=round(end, 3),
            score=cand.score, reasons=list(cand.reasons),
        ))
        chosen_cands.append(cand)

    return chosen
