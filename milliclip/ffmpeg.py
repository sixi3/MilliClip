"""Thin wrappers around ffmpeg / ffprobe.

All external-binary interaction is centralized here so the rest of the code stays testable
and so a missing ffmpeg surfaces as one clear error.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Optional


class FfmpegError(RuntimeError):
    pass


def ensure_available() -> None:
    for binary in ("ffmpeg", "ffprobe"):
        if shutil.which(binary) is None:
            raise FfmpegError(
                f"'{binary}' not found on PATH. Install ffmpeg (e.g. `brew install ffmpeg`)."
            )


def run(args: List[str], capture: bool = True, timeout: Optional[float] = None) -> subprocess.CompletedProcess:
    """Run an ffmpeg/ffprobe command. `args` excludes the binary name's -hide_banner."""
    try:
        return subprocess.run(
            args,
            check=True,
            capture_output=capture,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise FfmpegError(str(exc)) from exc
    except subprocess.CalledProcessError as exc:
        raise FfmpegError(
            f"command failed ({exc.returncode}): {' '.join(args)}\n{exc.stderr or ''}"
        ) from exc


@dataclass
class MediaInfo:
    duration: float
    width: int
    height: int
    has_audio: bool
    fps: float


def probe(path: str) -> MediaInfo:
    """Return basic media info via ffprobe."""
    proc = run([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", path,
    ])
    data = json.loads(proc.stdout)
    duration = float(data.get("format", {}).get("duration", 0.0) or 0.0)
    width = height = 0
    fps = 0.0
    has_audio = False
    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video" and width == 0:
            width = int(stream.get("width", 0) or 0)
            height = int(stream.get("height", 0) or 0)
            rate = stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "0/1"
            try:
                num, den = rate.split("/")
                fps = float(num) / float(den) if float(den) else 0.0
            except (ValueError, ZeroDivisionError):
                fps = 0.0
        elif stream.get("codec_type") == "audio":
            has_audio = True
    return MediaInfo(duration=duration, width=width, height=height, has_audio=has_audio, fps=fps)
