"""Minimal, quota-aware YouTube Data API v3 client (official API, API-key auth only).

The key is read only from the YOUTUBE_API_KEY env var and sent in the
``X-Goog-Api-Key`` header (never in the URL), so it cannot leak through request
URLs in exceptions or logs.
"""
from __future__ import annotations

import os
import re
import time
from datetime import datetime
from typing import Any, Callable

import requests

API_BASE = "https://www.googleapis.com/youtube/v3"
ENV_VAR = "YOUTUBE_API_KEY"

# Documented quota cost per call (units). search.list is deliberately expensive.
QUOTA_COSTS = {"channels.list": 1, "playlistItems.list": 1, "videos.list": 1, "search.list": 100}

RETRY_STATUS = {429, 500, 502, 503, 504}
QUOTA_REASONS = {"quotaExceeded", "dailyLimitExceeded"}
RATE_REASONS = {"rateLimitExceeded", "userRateLimitExceeded"}
KEY_REASONS = {"keyInvalid", "keyExpired", "ipRefererBlocked", "accessNotConfigured", "API_KEY_INVALID"}


class YouTubeAPIError(RuntimeError):
    pass


class ApiKeyError(YouTubeAPIError):
    pass


class QuotaExceededError(YouTubeAPIError):
    pass


class QuotaBudgetError(YouTubeAPIError):
    """Our own configured max_quota_units budget would be exceeded."""


class SearchDisabledError(YouTubeAPIError):
    pass


def get_api_key(env: dict | None = None) -> str:
    key = (env if env is not None else os.environ).get(ENV_VAR, "").strip()
    if not key:
        raise ApiKeyError(
            f"{ENV_VAR} is not set. Create a YouTube Data API v3 key in Google Cloud and "
            f"export {ENV_VAR}=... (see docs/RESEARCH_TOOL.md). The key is never read from files."
        )
    return key


_DUR = re.compile(r"^P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?$")


def parse_duration(iso: str | None) -> int | None:
    """ISO-8601 duration (PT1M5S, PT1H, P1DT2H) -> seconds. None if unparseable."""
    if not iso:
        return None
    m = _DUR.match(iso)
    if not m:
        return None
    d, h, mi, s = (int(x) if x else 0 for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _int(v: Any) -> int | None:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def normalize_video(item: dict) -> dict:
    sn, cd, st = item.get("snippet", {}), item.get("contentDetails", {}), item.get("statistics", {})
    return {
        "video_id": item["id"],
        "channel_id": sn.get("channelId"),
        "channel_title": sn.get("channelTitle"),
        "title": sn.get("title", ""),
        "description": sn.get("description", ""),
        "published_at": parse_ts(sn["publishedAt"]),
        "duration_s": parse_duration(cd.get("duration")),
        "views": _int(st.get("viewCount")),  # None if hidden
        "likes": _int(st.get("likeCount")),
        "comments": _int(st.get("commentCount")),
        "live_broadcast": sn.get("liveBroadcastContent", "none"),
    }


class YouTubeClient:
    def __init__(
        self,
        api_key: str,
        session: Any = None,
        *,
        max_retries: int = 5,
        backoff_base: float = 1.0,
        sleep: Callable[[float], None] = time.sleep,
        max_quota_units: int | None = None,
        allow_search: bool = False,
        timeout: float = 30.0,
    ):
        self._key = api_key
        self.session = session or requests.Session()
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self._sleep = sleep
        self.max_quota_units = max_quota_units
        self.allow_search = allow_search
        self.timeout = timeout
        self.quota_used = 0
        self.quota_breakdown: dict[str, int] = {}

    def __repr__(self) -> str:  # never expose the key
        return f"YouTubeClient(quota_used={self.quota_used})"

    # -- low level ---------------------------------------------------------
    def _charge(self, method: str) -> None:
        cost = QUOTA_COSTS[method]
        self.quota_used += cost
        self.quota_breakdown[method] = self.quota_breakdown.get(method, 0) + cost

    @staticmethod
    def _error_info(resp: Any) -> tuple[str, str]:
        try:
            err = resp.json().get("error", {})
        except Exception:
            return "", ""
        reasons = [e.get("reason", "") for e in err.get("errors", [])]
        status = err.get("status", "")
        return (reasons[0] if reasons else status), err.get("message", "")

    def _request(self, method: str, params: dict) -> dict:
        cost = QUOTA_COSTS[method]
        if self.max_quota_units is not None and self.quota_used + cost > self.max_quota_units:
            raise QuotaBudgetError(
                f"Configured quota budget {self.max_quota_units} would be exceeded "
                f"(used {self.quota_used}, next call {method} costs {cost})."
            )
        url = f"{API_BASE}/{method.split('.')[0]}"
        headers = {"X-Goog-Api-Key": self._key, "Accept": "application/json"}
        last = ""
        for attempt in range(self.max_retries + 1):
            try:
                resp = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
            except (requests.ConnectionError, requests.Timeout) as e:
                last = type(e).__name__  # not str(e): keep URLs out of messages
            else:
                code = resp.status_code
                if code == 200:
                    self._charge(method)
                    return resp.json()
                reason, msg = self._error_info(resp)
                if code == 403 and reason in QUOTA_REASONS:
                    raise QuotaExceededError(
                        f"YouTube API quota exhausted ({reason}). Daily quota resets at midnight "
                        f"Pacific time; lower uploads_per_channel or request more quota."
                    )
                if code in (400, 403) and (reason in KEY_REASONS or "API key" in msg):
                    raise ApiKeyError(f"API key rejected ({reason or code}): {msg}")
                if code in RETRY_STATUS or (code == 403 and reason in RATE_REASONS):
                    last = f"HTTP {code} {reason}".strip()
                else:
                    raise YouTubeAPIError(f"{method} failed: HTTP {code} {reason}: {msg}")
            if attempt < self.max_retries:
                self._sleep(self.backoff_base * (2 ** attempt))
        raise YouTubeAPIError(f"{method} failed after {self.max_retries} retries ({last})")

    # -- endpoints ---------------------------------------------------------
    def channels_list(self, *, channel_id: str | None = None, handle: str | None = None) -> list[dict]:
        params: dict[str, Any] = {"part": "snippet,contentDetails,statistics", "maxResults": 1}
        if channel_id:
            params["id"] = channel_id
        elif handle:
            params["forHandle"] = handle if handle.startswith("@") else "@" + handle
        else:
            raise ValueError("channel_id or handle required")
        return self._request("channels.list", params).get("items", [])

    def playlist_video_ids(self, playlist_id: str, limit: int, max_pages: int | None = None) -> list[str]:
        """Most recent `limit` video IDs of a playlist (uploads playlists are newest-first)."""
        ids: list[str] = []
        token = None
        pages = 0
        max_pages = max_pages or (limit + 49) // 50 + 1
        while len(ids) < limit and pages < max_pages:
            params = {"part": "contentDetails", "playlistId": playlist_id,
                      "maxResults": min(50, limit - len(ids))}
            if token:
                params["pageToken"] = token
            data = self._request("playlistItems.list", params)
            pages += 1
            for it in data.get("items", []):
                vid = it.get("contentDetails", {}).get("videoId")
                if vid and vid not in ids:
                    ids.append(vid)
            token = data.get("nextPageToken")
            if not token:
                break
        return ids[:limit]

    def videos_list(self, video_ids: list[str]) -> list[dict]:
        out: list[dict] = []
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i + 50]
            data = self._request("videos.list", {
                "part": "snippet,contentDetails,statistics", "id": ",".join(batch),
                "maxResults": 50})
            out.extend(normalize_video(it) for it in data.get("items", []))
        return out

    def search_channels(self, query: str, region: str | None = None) -> list[dict]:
        """Discovery only. 100 quota units per call; gated behind allow_search."""
        if not self.allow_search:
            raise SearchDisabledError("search.list costs 100 units/call; pass --allow-search to enable.")
        params = {"part": "snippet", "type": "channel", "q": query, "maxResults": 25}
        if region:
            params["regionCode"] = region
        items = self._request("search.list", params).get("items", [])
        return [{"channel_id": it["snippet"].get("channelId") or it["id"].get("channelId"),
                 "title": it["snippet"].get("title", "")} for it in items]
