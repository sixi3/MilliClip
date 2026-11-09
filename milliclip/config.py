"""Configuration schema and loader.

Config comes from a YAML file (non-secret settings). Secrets come only from environment
variables / token files referenced by name — never stored in the YAML or in source.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import BaseModel, Field


class Paths(BaseModel):
    recordings: str = "recordings"
    renders: str = "renders"
    work: str = "work"
    db: str = "data/milliclip.db"


class CaptureConfig(BaseModel):
    source: Literal["card", "remote_play", "broadcast"] = "card"
    segment_seconds: int = 60
    resolution: str = "1920x1080"
    fps: int = 60
    device: str = ""


class StorageConfig(BaseModel):
    max_recordings_gb: float = 50.0
    keep_renders: int = 50
    min_free_gb: float = 10.0


class SpeechConfig(BaseModel):
    enabled: bool = False
    model: str = "base"
    language: str = "en"


class DetectConfig(BaseModel):
    weight_loudness: float = 1.0
    weight_scene: float = 0.6
    weight_speech: float = 0.8
    loudness_percentile: float = 90.0
    min_highlight_seconds: float = 4.0
    max_highlight_seconds: float = 45.0
    music_penalty: float = 0.3
    speech: SpeechConfig = Field(default_factory=SpeechConfig)


class SelectConfig(BaseModel):
    lead_in_seconds: float = 2.0
    tail_seconds: float = 1.5
    min_gap_seconds: float = 30.0
    max_clips_per_run: int = 10
    dedup_similarity: float = 0.85


class SubtitleStyle(BaseModel):
    font: str = "Arial"
    fontsize: int = 18
    primary_color: str = "&H00FFFFFF"
    outline: int = 2
    margin_v: int = 120


class EncodeConfig(BaseModel):
    video_bitrate: str = "8M"
    audio_bitrate: str = "160k"
    preset: str = "medium"


class EditConfig(BaseModel):
    target_resolution: str = "1080x1920"
    reframe: Literal["center", "track"] = "center"
    subtitles: bool = True
    subtitle_style: SubtitleStyle = Field(default_factory=SubtitleStyle)
    encode: EncodeConfig = Field(default_factory=EncodeConfig)


class MetadataConfig(BaseModel):
    model: str = "claude-opus-5-5"
    max_title_chars: int = 90
    max_hashtags: int = 12
    tone: str = "energetic, concise, gaming"
    game: str = "GTA 6"


class YouTubePublish(BaseModel):
    enabled: bool = False
    daily_limit: int = 5
    privacy: Literal["private", "unlisted", "public"] = "private"
    category_id: str = "20"


class InstagramPublish(BaseModel):
    enabled: bool = False
    daily_limit: int = 5
    public_media_base_url: str = ""


class PublishConfig(BaseModel):
    enabled: bool = False
    min_confidence: float = 0.55
    max_consecutive_failures: int = 3
    youtube: YouTubePublish = Field(default_factory=YouTubePublish)
    instagram: InstagramPublish = Field(default_factory=InstagramPublish)


class AlertConfig(BaseModel):
    method: Literal["none", "file", "webhook"] = "none"
    webhook_url_env: str = "MILLICLIP_ALERT_WEBHOOK"
    file: str = "data/alerts.log"


class HealthConfig(BaseModel):
    alert: AlertConfig = Field(default_factory=AlertConfig)


class Config(BaseModel):
    paths: Paths = Field(default_factory=Paths)
    capture: CaptureConfig = Field(default_factory=CaptureConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    detect: DetectConfig = Field(default_factory=DetectConfig)
    select: SelectConfig = Field(default_factory=SelectConfig)
    edit: EditConfig = Field(default_factory=EditConfig)
    metadata: MetadataConfig = Field(default_factory=MetadataConfig)
    publish: PublishConfig = Field(default_factory=PublishConfig)
    health: HealthConfig = Field(default_factory=HealthConfig)

    @classmethod
    def load(cls, path: Optional[str] = None) -> "Config":
        """Load config from YAML; fall back to defaults if no file given/found."""
        if path is None:
            for candidate in ("config/config.yaml", "config/config.example.yaml"):
                if Path(candidate).exists():
                    path = candidate
                    break
        if path and Path(path).exists():
            with open(path, "r") as fh:
                data = yaml.safe_load(fh) or {}
            return cls.model_validate(data)
        return cls()


def env(name: str, default: str = "") -> str:
    """Read a secret/config value from the environment by name."""
    return os.environ.get(name, default)
