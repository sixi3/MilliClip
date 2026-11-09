"""Scene-change signals via ffmpeg's `scdet` filter.

Rapid scene cuts often mark action: camera swings, deaths, cutscene transitions, mission
changes. Each detected cut becomes a short 'scene' signal.
"""
from __future__ import annotations

import re
from typing import List

from ..ffmpeg import run
from ..models import Signal

_SCORE_RE = re.compile(r"lavfi\.scd\.score[=:]\s*([0-9.]+)")
_TIME_RE = re.compile(r"lavfi\.scd\.time[=:]\s*([0-9.]+)")
# scdet prints lines like: "[scdet @ ...] lavfi.scd.score: 12.34, lavfi.scd.time: 5.00"


def detect_scene_changes(path: str, threshold: float = 10.0) -> List[Signal]:
    """Return 'scene' signals at detected scene-change timestamps.

    `threshold` is scdet's sensitivity (0..100; lower = more cuts).
    """
    proc = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", path,
        "-filter:v", f"scdet=threshold={threshold}", "-f", "null", "-",
    ])
    signals: List[Signal] = []
    for line in proc.stderr.splitlines():
        if "scd.time" not in line:
            continue
        t_match = _TIME_RE.search(line)
        s_match = _SCORE_RE.search(line)
        if not t_match:
            continue
        t = float(t_match.group(1))
        raw = float(s_match.group(1)) if s_match else threshold
        strength = max(0.0, min(1.0, raw / 100.0))
        signals.append(Signal(kind="scene", start=t, end=t, strength=strength,
                              note=f"scd {raw:.1f}"))
    return signals
