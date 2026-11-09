"""Age-adjusted outlier scoring.

For each video v (age measured at `now`):
  eligible(v)  = views known, duration known, live_broadcast == none, age_days >= min_age_days
  metric(v)    = views_per_day = views / age_days      (default)
                 or raw views                          (metric: views; NOT age-adjusted)
  class(v)     = "short" if duration <= shorts_max_seconds else "long"   (heuristic)
  peers(v)     = eligible videos of the same channel and same class published within the
                 last `baseline_window_days` of `now` (excluding v itself if exclude_self);
                 if fewer than min_peers, fall back to all eligible same-class videos of the channel.
  baseline(v)  = median(metric over peers)
  outlier_score(v) = metric(v) / baseline(v)      (None if ineligible, < min_peers peers, or baseline <= 0)
"""
from __future__ import annotations

from datetime import datetime, timezone
from statistics import median

from .config import ResearchConfig


def age_days(published_at: datetime, now: datetime) -> float:
    return (now - published_at).total_seconds() / 86400.0


def video_class(duration_s: int | None, shorts_max_seconds: int) -> str:
    if duration_s is None:
        return "unknown"
    return "short" if 0 < duration_s <= shorts_max_seconds else "long"


def compute_metric(views: int, age: float, metric: str) -> float:
    return views / age if metric == "views_per_day" else float(views)


def score_videos(videos: list[dict], cfg: ResearchConfig, now: datetime | None = None) -> list[dict]:
    """Adds age_days, video_class, metric, eligible, baseline, peer_count, outlier_score to each dict."""
    now = now or datetime.now(timezone.utc)
    for v in videos:
        v["age_days"] = round(age_days(v["published_at"], now), 3)
        v["video_class"] = video_class(v.get("duration_s"), cfg.shorts_max_seconds)
        v["eligible"] = (v.get("views") is not None and v.get("duration_s") is not None
                         and v.get("live_broadcast", "none") == "none"
                         and v["age_days"] >= cfg.min_age_days)
        v["metric"] = compute_metric(v["views"], v["age_days"], cfg.metric) if v["eligible"] else None
        v["baseline"] = v["peer_count"] = v["outlier_score"] = None

    groups: dict[tuple, list[dict]] = {}
    for v in videos:
        if v["eligible"]:
            groups.setdefault((v["channel_id"], v["video_class"]), []).append(v)

    for group in groups.values():
        for v in group:
            def peers(pool):
                return [p["metric"] for p in pool if not (cfg.exclude_self and p is v)]
            windowed = peers([p for p in group if p["age_days"] <= cfg.baseline_window_days])
            vals = windowed if len(windowed) >= cfg.min_peers else peers(group)
            v["peer_count"] = len(vals)
            if len(vals) < cfg.min_peers:
                continue
            base = median(vals)
            v["baseline"] = base
            if base > 0:
                v["outlier_score"] = v["metric"] / base
    return videos
