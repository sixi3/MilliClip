from __future__ import annotations

import csv
import math
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import median

from .config import ResearchConfig

CSV_COLUMNS = [
    "channel_id", "channel_title", "tag_language", "tag_niche", "video_id", "url", "title",
    "published_at", "age_days", "duration_s", "is_short_heuristic", "video_class", "duration_bucket",
    "views", "likes", "comments", "eligible", "metric", "baseline", "peer_count", "outlier_score",
    "is_top_outlier", "title_length", "title_script", "title_language_heuristic", "hashtag_count",
    "title_has_question", "title_has_number", "title_has_emoji", "publish_hour_ist",
    "publish_weekday_ist", "topic",
]

CAVEAT = (
    "**Caveat — read before acting on this.** These results are *correlational* and "
    "*survivorship-biased*: they cover only channels we chose to seed and videos that still exist "
    "and are public, so channels/videos that flopped or were deleted are largely invisible. "
    "Outlier status can come from the algorithm, trending events, thumbnails, collabs, paid "
    "promotion or luck — not the title/length features compared here. Shorts classification "
    "(duration ≤ threshold) and language/script detection (Hinglish especially) are heuristics. "
    "Treat findings as hypotheses to test with our own content, not as rules."
)


def mark_top_outliers(videos: list[dict], top_fraction: float) -> int:
    scored = sorted((v for v in videos if v.get("outlier_score") is not None),
                    key=lambda v: v["outlier_score"], reverse=True)
    n_top = max(1, math.ceil(top_fraction * len(scored))) if scored else 0
    top = {id(v) for v in scored[:n_top]}
    for v in videos:
        v["is_top_outlier"] = id(v) in top
    return n_top


def write_csv(videos: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        w.writeheader()
        for v in videos:
            row = dict(v)
            row["url"] = f"https://www.youtube.com/watch?v={v['video_id']}"
            row["published_at"] = v["published_at"].isoformat()
            for k in ("metric", "baseline", "outlier_score"):
                if row.get(k) is not None:
                    row[k] = round(row[k], 4)
            w.writerow(row)


def _fmt(x) -> str:
    if x is None:
        return "n/a"
    return f"{x:.1f}" if isinstance(x, float) else str(x)


def _med(vals):
    vals = [x for x in vals if x is not None]
    return median(vals) if vals else None


def _share(group: list[dict], pred) -> str:
    return f"{100 * sum(1 for v in group if pred(v)) / len(group):.0f}%" if group else "n/a"


def _mix(group: list[dict], key: str, top: int = 4) -> str:
    if not group:
        return "n/a"
    c = Counter(v[key] for v in group)
    return ", ".join(f"{k} {100 * n / len(group):.0f}%" for k, n in c.most_common(top))


def _mode(group, key):
    c = Counter(v[key] for v in group)
    return c.most_common(1)[0][0] if c else None


def _esc(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def build_summary(videos: list[dict], channels: list[dict], cfg: ResearchConfig, *,
                  quota: int | None = None, generated: datetime | None = None) -> str:
    scored = [v for v in videos if v.get("outlier_score") is not None]
    top = [v for v in scored if v.get("is_top_outlier")]
    rest = [v for v in scored if not v.get("is_top_outlier")]
    L = ["# MilliClip competitor outlier summary", ""]
    L += [CAVEAT, ""]
    if generated:
        L.append(f"- Generated: {generated.isoformat(timespec='minutes')}")
    L += [f"- Channels: {len(channels)} · videos fetched: {len(videos)} · scored: {len(scored)}",
          f"- Metric: `{cfg.metric}` (min age {cfg.min_age_days}d; baseline = median of same-channel, "
          f"same-class peers in last {cfg.baseline_window_days:g}d, min {cfg.min_peers} peers)",
          f"- Shorts = duration ≤ {cfg.shorts_max_seconds}s (**heuristic**; the API has no Shorts flag)"]
    if quota is not None:
        L.append(f"- Estimated API quota used: {quota} units")
    L.append("")

    L += ["## Top outliers per channel", ""]
    for ch in channels:
        vids = sorted((v for v in scored if v["channel_id"] == ch["channel_id"]),
                      key=lambda v: v["outlier_score"], reverse=True)[: cfg.top_n_per_channel]
        L.append(f"### {_esc(ch['channel_title'] or ch['channel_id'])} "
                 f"({ch.get('language') or '?'}/{ch.get('niche') or '?'})")
        if not vids:
            L += ["_No scorable videos (too few peers or too new)._", ""]
            continue
        L += ["| Score | Class | Views | Dur | Title | Link |", "|---|---|---|---|---|---|"]
        for v in vids:
            L.append(f"| {v['outlier_score']:.2f}× | {v['video_class']} | {v['views']:,} | "
                     f"{v['duration_s']}s | {_esc(v['title'])} | "
                     f"[{v['video_id']}](https://www.youtube.com/watch?v={v['video_id']}) |")
        L.append("")

    L += [f"## Top {cfg.top_fraction:.0%} outliers vs the rest", ""]
    if not top:
        L += ["_Not enough scored videos for a comparison._", ""]
    else:
        L += [f"Top group n={len(top)}, rest n={len(rest)} (pooled across channels; scores are "
              "already normalised per channel and class).", "",
              "| Feature | Top outliers | Rest |", "|---|---|---|"]
        rows = [
            ("Median duration (s)", lambda g: _fmt(_med(v["duration_s"] for v in g))),
            ("Median title length", lambda g: _fmt(_med(v["title_length"] for v in g))),
            ("Median hashtag count", lambda g: _fmt(_med(v["hashtag_count"] for v in g))),
            ("Shorts share (heuristic)", lambda g: _share(g, lambda v: v["is_short_heuristic"])),
            ("Title has question", lambda g: _share(g, lambda v: v["title_has_question"])),
            ("Title has number", lambda g: _share(g, lambda v: v["title_has_number"])),
            ("Title has emoji", lambda g: _share(g, lambda v: v["title_has_emoji"])),
            ("Script mix", lambda g: _mix(g, "title_script")),
            ("Language mix (heuristic)", lambda g: _mix(g, "title_language_heuristic")),
            ("Duration bucket mix", lambda g: _mix(g, "duration_bucket", 3)),
            ("Most common publish hour (IST)", lambda g: _fmt(_mode(g, "publish_hour_ist"))),
            ("Most common weekday (IST)", lambda g: _fmt(_mode(g, "publish_weekday_ist"))),
        ]
        for name, fn in rows:
            L.append(f"| {name} | {fn(top)} | {fn(rest)} |")
        L.append("")
    L += ["## Notes", "",
          "- Small samples make every row above noisy; differences of a few points mean nothing.",
          "- Topic tagging is off by default (no LLM calls).", ""]
    return "\n".join(L)


def write_summary(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
