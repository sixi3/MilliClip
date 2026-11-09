from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class ChannelSeed:
    id: str | None = None
    handle: str | None = None
    language: str = ""
    niche: str = ""
    note: str = ""

    @property
    def ref(self) -> str:
        return self.id or self.handle or "?"

    @property
    def is_placeholder(self) -> bool:
        return "PLACEHOLDER" in self.ref.upper()


@dataclass
class ResearchConfig:
    channels: list[ChannelSeed] = field(default_factory=list)
    uploads_per_channel: int = 100
    min_age_days: float = 3.0
    shorts_max_seconds: int = 180
    metric: str = "views_per_day"          # views_per_day | views
    baseline_window_days: float = 180.0
    min_peers: int = 5
    exclude_self: bool = True
    top_fraction: float = 0.10
    top_n_per_channel: int = 5
    max_quota_units: int | None = 2000
    output_dir: str = "data/research"


def load_config(path: str | Path) -> ResearchConfig:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    s = raw.get("settings", {}) or {}
    o = s.get("outlier", {}) or {}
    cfg = ResearchConfig()
    for name in ("uploads_per_channel", "min_age_days", "shorts_max_seconds", "max_quota_units",
                 "top_n_per_channel", "output_dir"):
        if name in s:
            setattr(cfg, name, s[name])
    for name in ("metric", "baseline_window_days", "min_peers", "exclude_self", "top_fraction"):
        if name in o:
            setattr(cfg, name, o[name])
    if cfg.metric not in ("views_per_day", "views"):
        raise ValueError(f"unknown outlier.metric {cfg.metric!r}")
    if not 0 < cfg.top_fraction <= 1:
        raise ValueError("outlier.top_fraction must be in (0, 1]")
    for c in raw.get("channels", []) or []:
        tags = c.get("tags", {}) or {}
        seed = ChannelSeed(id=c.get("id"), handle=c.get("handle"),
                           language=tags.get("language", ""), niche=tags.get("niche", ""),
                           note=c.get("note", ""))
        if not (seed.id or seed.handle):
            raise ValueError(f"channel entry needs id or handle: {c}")
        cfg.channels.append(seed)
    return cfg
