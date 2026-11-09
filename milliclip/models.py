"""Shared data models passed between pipeline stages."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Signal(BaseModel):
    """A time-localized detection signal within a source video."""
    kind: str                      # "loudness" | "scene" | "speech"
    start: float                   # seconds
    end: float                     # seconds
    strength: float                # 0..1 normalized
    note: str = ""


class Candidate(BaseModel):
    """A candidate highlight window before selection."""
    start: float
    end: float
    score: float                   # 0..1
    reasons: List[str] = Field(default_factory=list)
    has_music: bool = False
    signature: List[float] = Field(default_factory=list)  # coarse fingerprint for dedup

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)


class Clip(BaseModel):
    """A selected clip with padding applied, ready for editing."""
    source: str                    # path to source video
    start: float
    end: float
    score: float
    reasons: List[str] = Field(default_factory=list)
    transcript: str = ""
    words: List[dict] = Field(default_factory=list)  # [{word,start,end}]

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)


class RenderResult(BaseModel):
    clip: Clip
    path: str                      # rendered vertical mp4
    width: int
    height: int


class Metadata(BaseModel):
    title: str
    description: str
    hashtags: List[str] = Field(default_factory=list)


class PublishResult(BaseModel):
    platform: str
    success: bool
    dry_run: bool
    external_id: Optional[str] = None
    error: Optional[str] = None
    skipped_reason: Optional[str] = None
