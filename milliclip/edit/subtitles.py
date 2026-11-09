"""Generate ASS subtitles from word-level timings.

We group words into short caption lines (a few words each) with timings relative to the
clip start, then emit an ASS file that ffmpeg's `subtitles`/`ass` filter burns in. Styling
comes from config so captions stay readable on vertical video.
"""
from __future__ import annotations

from typing import List

from ..config import SubtitleStyle


def words_in_window(words: List[dict], start: float, end: float) -> List[dict]:
    """Return words overlapping [start,end], retimed relative to `start`."""
    out = []
    for w in words:
        ws, we = float(w["start"]), float(w["end"])
        if we <= start or ws >= end:
            continue
        out.append({
            "word": w["word"],
            "start": max(0.0, ws - start),
            "end": max(0.0, min(we, end) - start),
        })
    return out


def _fmt_ts(t: float) -> str:
    if t < 0:
        t = 0.0
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    cs = int(round((t - int(t)) * 100))
    if cs == 100:
        cs = 99
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def _group(words: List[dict], max_words: int = 4, max_dur: float = 2.5) -> List[dict]:
    lines: List[dict] = []
    cur: List[dict] = []
    for w in words:
        if not cur:
            cur = [w]
            continue
        span = w["end"] - cur[0]["start"]
        if len(cur) >= max_words or span > max_dur:
            lines.append({"text": " ".join(x["word"] for x in cur),
                          "start": cur[0]["start"], "end": cur[-1]["end"]})
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append({"text": " ".join(x["word"] for x in cur),
                      "start": cur[0]["start"], "end": cur[-1]["end"]})
    return lines


def build_ass(words: List[dict], style: SubtitleStyle, play_res_x: int = 1080,
              play_res_y: int = 1920) -> str:
    """Return a complete ASS subtitle document as a string."""
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {play_res_x}
PlayResY: {play_res_y}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{style.font},{style.fontsize},{style.primary_color},&H00000000,&H64000000,1,0,1,{style.outline},1,2,40,40,{style.margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = _group(words)
    body = []
    for ln in lines:
        text = ln["text"].replace("\n", " ").strip()
        if not text:
            continue
        body.append(
            f"Dialogue: 0,{_fmt_ts(ln['start'])},{_fmt_ts(ln['end'])},Default,,0,0,0,,{text}"
        )
    return header + "\n".join(body) + "\n"
