"""Audio-based highlight signals.

Uses ffmpeg's `ebur128` filter to get momentary loudness over time, then flags windows
that are loud relative to the rest of the clip (gunfights, explosions, shouting, hype).
Also provides a coarse music/sustained-tone detector used for the copyright penalty.
"""
from __future__ import annotations

import re
from typing import List, Tuple

from ..ffmpeg import run
from ..models import Signal

_TIME_RE = re.compile(r"pts_time:([0-9.]+)")
_M_RE = re.compile(r"lavfi\.r128\.M=(-?[0-9.]+)")


def _parse_ametadata(stdout: str) -> List[Tuple[float, float]]:
    """Return list of (time_seconds, momentary_LUFS) from ametadata print output.

    The `ametadata=mode=print` filter emits, per frame, a `pts_time:T` header line
    followed by `lavfi.r128.M=<LUFS>` (momentary loudness).
    """
    out: List[Tuple[float, float]] = []
    cur_t: float | None = None
    for line in stdout.splitlines():
        tm = _TIME_RE.search(line)
        if tm:
            cur_t = float(tm.group(1))
            continue
        mm = _M_RE.search(line)
        if mm and cur_t is not None:
            lufs = float(mm.group(1))
            if lufs <= -120:  # ffmpeg uses ~-120 for silence
                lufs = -70.0
            out.append((cur_t, lufs))
            cur_t = None
    return out


def loudness_series(path: str) -> List[Tuple[float, float]]:
    """Momentary loudness (LUFS) sampled over the file. Empty if no audio."""
    proc = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", path,
        "-map", "a:0?", "-af", "ebur128=metadata=1,ametadata=mode=print:file=-",
        "-f", "null", "-",
    ])
    # ametadata print writes to stdout
    return _parse_ametadata(proc.stdout)


def _percentile(values: List[float], pct: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    k = (len(s) - 1) * (pct / 100.0)
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    frac = k - lo
    return s[lo] * (1 - frac) + s[hi] * frac


def analyze_loudness(path: str, percentile: float = 90.0,
                     min_gap: float = 1.0) -> List[Signal]:
    """Emit 'loudness' signals at moments above the given loudness percentile.

    strength is normalized 0..1 within the clip's dynamic range.
    """
    series = loudness_series(path)
    if len(series) < 2:
        return []
    times = [t for t, _ in series]
    lufs = [v for _, v in series]
    lo = min(lufs)
    hi = max(lufs)
    span = (hi - lo) or 1.0
    threshold = _percentile(lufs, percentile)

    signals: List[Signal] = []
    last_t = -1e9
    for t, v in zip(times, lufs):
        if v >= threshold and (t - last_t) >= min_gap:
            strength = max(0.0, min(1.0, (v - lo) / span))
            signals.append(Signal(kind="loudness", start=t, end=t, strength=strength,
                                   note=f"{v:.1f} LUFS"))
            last_t = t
    return signals


def detect_music(path: str, flatness_threshold: float = 0.4) -> bool:
    """Very coarse heuristic for sustained music presence.

    Music tends to keep a fuller, steadier spectrum than sparse game SFX/speech. We use
    the standard deviation of RMS level: sustained music has a relatively *stable* high
    RMS, whereas action SFX is spiky and speech is gappy. This is a cheap bias signal, not
    a music classifier — the true copyright handling is Content-ID + alerts at publish.
    """
    series = loudness_series(path)
    if len(series) < 8:
        return False
    vals = [v for _, v in series if v > -70]
    if len(vals) < 8:
        return False
    mean = sum(vals) / len(vals)
    var = sum((v - mean) ** 2 for v in vals) / len(vals)
    std = var ** 0.5
    # Low variance + reasonably high mean loudness ⇒ likely sustained music bed.
    return std < (flatness_threshold * abs(mean) if mean else flatness_threshold) and mean > -30
