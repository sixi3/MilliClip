"""Quota-efficient collection: channels.list -> uploads playlist -> videos.list."""
from __future__ import annotations

import logging

from .config import ChannelSeed, ResearchConfig
from .youtube import YouTubeClient

log = logging.getLogger(__name__)


def fetch_channel(client: YouTubeClient, seed: ChannelSeed, uploads: int) -> tuple[dict | None, list[dict]]:
    items = client.channels_list(
        channel_id=seed.id if seed.id else None, handle=None if seed.id else seed.handle)
    if not items:
        log.warning("channel not found: %s", seed.ref)
        return None, []
    ch = items[0]
    uploads_pl = ch.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
    info = {"channel_id": ch["id"], "channel_title": ch.get("snippet", {}).get("title", ""),
            "subscribers": ch.get("statistics", {}).get("subscriberCount"),
            "language": seed.language, "niche": seed.niche}
    if not uploads_pl:
        return info, []
    ids = client.playlist_video_ids(uploads_pl, uploads)
    videos = client.videos_list(ids)
    for v in videos:
        v["channel_id"] = v["channel_id"] or info["channel_id"]
        v["tag_language"], v["tag_niche"] = seed.language, seed.niche
    return info, videos


def fetch_all(client: YouTubeClient, cfg: ResearchConfig) -> tuple[list[dict], list[dict]]:
    channels, videos = [], []
    for seed in cfg.channels:
        if seed.is_placeholder:
            log.warning("skipping placeholder channel %s (replace it in your config)", seed.ref)
            continue
        info, vids = fetch_channel(client, seed, cfg.uploads_per_channel)
        if info:
            channels.append(info)
            videos.extend(vids)
    return channels, videos
