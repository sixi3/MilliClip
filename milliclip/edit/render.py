"""Render a selected clip into a platform-ready vertical video.

Pipeline per clip:
1. Trim the window from the source (accurate seek).
2. Reframe to vertical (center crop or padded fit) at the target resolution.
3. Optionally burn in ASS subtitles.
4. Encode with platform-friendly settings (H.264 high, yuv420p, AAC, +faststart).

The gameplay-as-background / split-screen "B-roll on top" formats are intentionally left
as a separate future layer (`edit/layouts.py`); this module handles the core single-feed
vertical render that every format builds on.
"""
from __future__ import annotations

import os
import tempfile
from typing import List, Optional

from ..config import EditConfig
from ..ffmpeg import probe, run
from ..models import Clip, RenderResult
from .subtitles import build_ass, words_in_window


def _parse_res(res: str) -> tuple[int, int]:
    w, h = res.lower().split("x")
    return int(w), int(h)


def _reframe_filter(src_w: int, src_h: int, out_w: int, out_h: int, mode: str) -> str:
    """Build a filter that converts the source into out_w x out_h vertical.

    center: scale so height fills, then center-crop width (zooms in, no bars).
    """
    if mode == "center":
        # Scale to cover the target, then crop to exact size.
        return (
            f"scale={out_w}:{out_h}:force_original_aspect_ratio=increase,"
            f"crop={out_w}:{out_h}"
        )
    # padded fit (letterbox/pillarbox) fallback
    return (
        f"scale={out_w}:{out_h}:force_original_aspect_ratio=decrease,"
        f"pad={out_w}:{out_h}:(ow-iw)/2:(oh-ih)/2:color=black"
    )


def _escape_ass_path(path: str) -> str:
    # ffmpeg filtergraph escaping for the subtitles filter path.
    return path.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def render_clip(clip: Clip, out_path: str, cfg: EditConfig,
                words: Optional[List[dict]] = None) -> RenderResult:
    """Render one clip to `out_path`. Returns RenderResult. Raises FfmpegError on failure."""
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    info = probe(clip.source)
    out_w, out_h = _parse_res(cfg.target_resolution)
    vf_parts = [_reframe_filter(info.width or 1920, info.height or 1080, out_w, out_h,
                                cfg.reframe)]

    ass_file: Optional[str] = None
    if cfg.subtitles and words:
        win_words = words_in_window(words, clip.start, clip.end)
        if win_words:
            ass_text = build_ass(win_words, cfg.subtitle_style, out_w, out_h)
            fd, ass_file = tempfile.mkstemp(suffix=".ass")
            with os.fdopen(fd, "w") as fh:
                fh.write(ass_text)
            vf_parts.append(f"subtitles='{_escape_ass_path(ass_file)}'")

    vf = ",".join(vf_parts)
    duration = max(0.1, clip.end - clip.start)

    try:
        run([
            "ffmpeg", "-hide_banner", "-nostats", "-y",
            "-ss", f"{clip.start:.3f}", "-i", clip.source, "-t", f"{duration:.3f}",
            "-vf", vf,
            "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-preset", cfg.encode.preset, "-b:v", cfg.encode.video_bitrate,
            "-c:a", "aac", "-b:a", cfg.encode.audio_bitrate,
            "-movflags", "+faststart",
            out_path,
        ])
    finally:
        if ass_file and os.path.exists(ass_file):
            os.unlink(ass_file)

    return RenderResult(clip=clip, path=out_path, width=out_w, height=out_h)
