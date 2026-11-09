"""CLI: python -m milliclip.research --config research/channels.example.yaml  (or `milliclip-research`)."""
from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import report
from .config import load_config
from .features import extract_features
from .fetch import fetch_all
from .llm import get_tagger
from .scoring import score_videos
from .youtube import YouTubeAPIError, YouTubeClient, get_api_key


def run(cfg, client, tagger, out_dir: Path, now: datetime | None = None) -> tuple[Path, Path]:
    now = now or datetime.now(timezone.utc)
    channels, videos = fetch_all(client, cfg)
    score_videos(videos, cfg, now)
    for v in videos:
        v.update(extract_features(v, cfg.shorts_max_seconds))
        v["topic"] = tagger.tag(v)
    report.mark_top_outliers(videos, cfg.top_fraction)
    csv_path, md_path = out_dir / "videos.csv", out_dir / "summary.md"
    report.write_csv(videos, csv_path)
    report.write_summary(
        report.build_summary(videos, channels, cfg, quota=client.quota_used, generated=now), md_path)
    return csv_path, md_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="milliclip-research", description=__doc__)
    p.add_argument("--config", default="research/channels.example.yaml")
    p.add_argument("--out", help="output dir (default: config output_dir, git-ignored data/research)")
    p.add_argument("--uploads", type=int, help="override uploads_per_channel")
    p.add_argument("--tagger", default="none", help="topic tagger (default none: no API calls)")
    p.add_argument("--allow-search", action="store_true",
                   help="enable search.list (100 quota units/call); needed for --discover")
    p.add_argument("--discover", metavar="QUERY", help="print candidate channels for QUERY (needs --allow-search)")
    p.add_argument("--region", help="regionCode for --discover, e.g. IN")
    args = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    try:
        cfg = load_config(args.config)
        if args.uploads:
            cfg.uploads_per_channel = args.uploads
        client = YouTubeClient(get_api_key(), max_quota_units=cfg.max_quota_units,
                               allow_search=args.allow_search)
        if args.discover:
            for c in client.search_channels(args.discover, args.region):
                print(f"{c['channel_id']}\t{c['title']}")
            print(f"Estimated quota used: {client.quota_used} units", file=sys.stderr)
            return 0
        csv_path, md_path = run(cfg, client, get_tagger(args.tagger), Path(args.out or cfg.output_dir))
    except (YouTubeAPIError, ValueError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"Wrote {csv_path} and {md_path}")
    print(f"Estimated quota used: {client.quota_used} units {dict(client.quota_breakdown)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
