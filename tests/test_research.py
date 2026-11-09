import csv
import re
from datetime import datetime, timedelta, timezone

import pytest
import requests

from milliclip.research import report
from milliclip.research.cli import run
from milliclip.research.config import ChannelSeed, ResearchConfig, load_config
from milliclip.research.features import (detect_language, detect_script, duration_bucket,
                                         extract_features)
from milliclip.research.fetch import fetch_all
from milliclip.research.llm import NullTagger, get_tagger
from milliclip.research.scoring import score_videos
from milliclip.research.youtube import (ApiKeyError, QuotaBudgetError, QuotaExceededError,
                                        SearchDisabledError, YouTubeAPIError, YouTubeClient,
                                        get_api_key, parse_duration)
from conftest import FakeResponse, FakeSession, load

NOW = datetime(2026, 11, 9, tzinfo=timezone.utc)


def client(session, **kw):
    kw.setdefault("sleep", lambda s: None)
    return YouTubeClient("SECRETKEY", session, **kw)


# ---- API layer ---------------------------------------------------------
def test_api_key_env_only():
    assert get_api_key({"YOUTUBE_API_KEY": " abc "}) == "abc"
    with pytest.raises(ApiKeyError):
        get_api_key({})


def test_parse_duration():
    assert parse_duration("PT45S") == 45
    assert parse_duration("PT1H2M3S") == 3723
    assert parse_duration("PT3M") == 180
    assert parse_duration("P1DT1H") == 90000
    assert parse_duration("P0D") == 0
    assert parse_duration("garbage") is None and parse_duration(None) is None


def test_key_sent_in_header_not_url_and_not_in_repr():
    s = FakeSession([FakeResponse(200, load("channels_handle.json"))])
    c = client(s)
    c.channels_list(handle="fakehandle")
    call = s.calls[0]
    assert call["params"]["forHandle"] == "@fakehandle"
    assert "SECRETKEY" not in str(call["params"]) and "SECRETKEY" not in call["url"]
    assert call["headers"]["X-Goog-Api-Key"] == "SECRETKEY"
    assert "SECRETKEY" not in repr(c)
    assert c.quota_used == 1


def test_pagination_follows_tokens_and_limits():
    s = FakeSession([FakeResponse(200, load("playlist_page1.json")),
                     FakeResponse(200, load("playlist_page2.json"))])
    c = client(s)
    assert c.playlist_video_ids("UU1", 100) == ["v1", "v2", "v3", "v4", "v5"]
    assert s.calls[1]["params"]["pageToken"] == "PAGE2"
    assert c.quota_used == 2
    # limit smaller than a page
    s = FakeSession([FakeResponse(200, load("playlist_page1.json"))])
    assert client(s).playlist_video_ids("UU1", 2) == ["v1", "v2"]
    assert len(s.calls) == 1 and s.calls[0]["params"]["maxResults"] == 2


def test_pagination_max_pages_guard():
    page = {"nextPageToken": "X", "items": [{"contentDetails": {"videoId": "a"}}]}
    s = FakeSession(handler=lambda u, p: FakeResponse(200, page))
    client(s).playlist_video_ids("UU1", 1000, max_pages=3)
    assert len(s.calls) == 3


def test_videos_batched_by_50():
    ids = [f"id{i}" for i in range(120)]
    s = FakeSession(handler=lambda u, p: FakeResponse(200, {"items": []}))
    c = client(s)
    c.videos_list(ids)
    sizes = [len(x["params"]["id"].split(",")) for x in s.calls]
    assert sizes == [50, 50, 20] and c.quota_used == 3


def test_retry_backoff_on_429_and_5xx():
    sleeps = []
    s = FakeSession([FakeResponse(429), FakeResponse(503), FakeResponse(200, {"items": []})])
    c = client(s, sleep=sleeps.append, backoff_base=1.0)
    c.videos_list(["a"])
    assert sleeps == [1.0, 2.0] and len(s.calls) == 3


def test_retry_on_network_error_and_exhaustion():
    def boom(u, p):
        raise requests.ConnectionError("https://x?key=SECRETKEY")
    s = FakeSession(handler=boom)
    with pytest.raises(YouTubeAPIError) as e:
        client(s, max_retries=2).videos_list(["a"])
    assert len(s.calls) == 3 and "SECRETKEY" not in str(e.value)


def _err(code, reason, msg="m"):
    return FakeResponse(code, {"error": {"code": code, "message": msg, "errors": [{"reason": reason}]}})


def test_403_quota_clear_error_no_retry():
    s = FakeSession([_err(403, "quotaExceeded")])
    with pytest.raises(QuotaExceededError, match="quota"):
        client(s).videos_list(["a"])
    assert len(s.calls) == 1


def test_bad_key_error():
    s = FakeSession([_err(400, "badRequest", "API key not valid. Please pass a valid API key.")])
    with pytest.raises(ApiKeyError):
        client(s).videos_list(["a"])


def test_other_4xx_not_retried():
    s = FakeSession([_err(404, "notFound")])
    with pytest.raises(YouTubeAPIError):
        client(s).videos_list(["a"])
    assert len(s.calls) == 1


def test_search_gated_and_costed():
    with pytest.raises(SearchDisabledError):
        client(FakeSession()).search_channels("gta")
    body = {"items": [{"id": {"channelId": "UCx"}, "snippet": {"channelId": "UCx", "title": "T"}}]}
    c = client(FakeSession([FakeResponse(200, body)]), allow_search=True)
    assert c.search_channels("gta", "IN") == [{"channel_id": "UCx", "title": "T"}]
    assert c.quota_used == 100


def test_quota_budget_guard():
    c = client(FakeSession(), max_quota_units=0)
    with pytest.raises(QuotaBudgetError):
        c.videos_list(["a"])


# ---- fetch -------------------------------------------------------------
def fake_api_session():
    def handler(url, params):
        if url.endswith("/channels"):
            return FakeResponse(200, load("channels_handle.json"))
        if url.endswith("/playlistItems"):
            return FakeResponse(200, load("playlist_page2.json" if params.get("pageToken") else "playlist_page1.json"))
        return FakeResponse(200, load("videos_batch.json"))
    return FakeSession(handler=handler)


def test_fetch_all_skips_placeholders_and_tags():
    cfg = ResearchConfig(channels=[ChannelSeed(id="UC_PLACEHOLDER_1"),
                                   ChannelSeed(handle="@fake", language="hinglish", niche="gta")])
    s = fake_api_session()
    c = client(s)
    channels, videos = fetch_all(c, cfg)
    assert len(channels) == 1 and len(videos) == 5
    assert videos[0]["tag_language"] == "hinglish"
    assert c.quota_used == 4  # channels + 2 playlist pages + 1 videos batch
    assert len(s.calls) == 4


def test_load_example_config():
    cfg = load_config("research/channels.example.yaml")
    assert cfg.uploads_per_channel == 100 and cfg.metric == "views_per_day"
    assert all(ch.is_placeholder for ch in cfg.channels)


# ---- features ----------------------------------------------------------
def test_shorts_heuristic_boundary():
    base = {"title": "x", "published_at": NOW}
    assert extract_features({**base, "duration_s": 180})["is_short_heuristic"] is True
    assert extract_features({**base, "duration_s": 181})["is_short_heuristic"] is False
    assert extract_features({**base, "duration_s": 0})["is_short_heuristic"] is False
    assert extract_features({**base, "duration_s": None})["is_short_heuristic"] is False


def test_duration_buckets():
    assert [duration_bucket(x) for x in (10, 30, 59, 120, 400, 5000, None)] == [
        "0-15s", "16-30s", "46-60s", "61-180s", "181-600s", "601s+", "unknown"]


def test_script_and_language_detection():
    assert detect_script("जीटीए में क्या है") == "devanagari"
    assert detect_script("জিটিএ কী") == "bengali"
    assert detect_script("ജിടിഎ എന്താണ്") == "malayalam"
    assert detect_script("GTA 6 trailer") == "latin"
    assert detect_script("123 !!!") == "none"
    assert detect_script("GTA जीटीए") == "mixed"
    assert detect_language("जीटीए में क्या है") == "hindi"
    assert detect_language("GTA 6 mein kya hai bhai") == "hinglish"
    assert detect_language("This is the best GTA moment ever") == "english"
    assert detect_language("সেরা GTA মুহূর্ত") == "mixed"


def test_title_features_and_ist():
    v = {"title": "Top 5 tricks? 🔥", "description": "#a #b", "duration_s": 40,
         "published_at": datetime(2026, 10, 1, 18, 30, tzinfo=timezone.utc)}
    f = extract_features(v)
    assert f["title_has_question"] and f["title_has_number"] and f["title_has_emoji"]
    assert f["hashtag_count"] == 2 and f["title_length"] == len(v["title"])
    assert f["publish_hour_ist"] == 0 and f["publish_weekday_ist"] == "Fri"  # 18:30Z = 00:00 IST next day
    f2 = extract_features({**v, "title": "plain title", "description": ""})
    assert not (f2["title_has_question"] or f2["title_has_number"] or f2["title_has_emoji"])


# ---- scoring -----------------------------------------------------------
def mk(i, views, age, dur=30, ch="C1"):
    return {"video_id": f"v{i}", "channel_id": ch, "views": views, "duration_s": dur,
            "published_at": NOW - timedelta(days=age), "live_broadcast": "none"}


def cfg(**kw):
    return ResearchConfig(**{"min_peers": 2, **kw})


def test_age_adjustment_and_min_age():
    vs = [mk(1, 1000, 10), mk(2, 1000, 2), mk(3, 3000, 10), mk(4, 2000, 10)]
    score_videos(vs, cfg(min_age_days=3), NOW)
    assert vs[1]["eligible"] is False and vs[1]["outlier_score"] is None
    assert vs[0]["metric"] == pytest.approx(100.0)  # views/day
    # same views, younger video => higher views/day
    a, b = mk(5, 1000, 4), mk(6, 1000, 40)
    score_videos([a, b], cfg(), NOW)
    assert a["metric"] > b["metric"]


def test_outlier_score_formula_and_exclude_self():
    vs = [mk(i, v * 10, 10) for i, v in enumerate([100, 100, 100, 100, 500])]  # vpd 100x4, 500
    score_videos(vs, cfg(min_peers=3), NOW)
    assert [round(v["outlier_score"], 2) for v in vs] == [1.0, 1.0, 1.0, 1.0, 5.0]
    assert vs[4]["baseline"] == 100 and vs[4]["peer_count"] == 4
    vs2 = [mk(i, v * 10, 10) for i, v in enumerate([100, 100, 100, 100, 500])]
    score_videos(vs2, cfg(min_peers=3, exclude_self=False), NOW)
    assert vs2[4]["baseline"] == 100  # median incl. self still 100 here
    assert vs2[4]["peer_count"] == 5


def test_scores_separate_by_class_and_channel_and_min_peers():
    vs = [mk(1, 1000, 10, 30), mk(2, 1000, 10, 30), mk(3, 9000, 10, 30),
          mk(4, 50000, 10, 900), mk(5, 70000, 10, 900),  # long-form class
          mk(6, 5, 10, 30, ch="C2")]                      # lone video in other channel
    score_videos(vs, cfg(), NOW)
    assert vs[2]["outlier_score"] == pytest.approx(9.0)  # vs median of two shorts at 100/day
    assert vs[3]["video_class"] == "long" and vs[3]["outlier_score"] is None  # only 1 peer
    assert vs[5]["outlier_score"] is None


def test_window_and_fallback():
    old = [mk(i, 100, 400) for i in range(3)]          # outside 180d window
    new = [mk(10 + i, 1000, 10) for i in range(3)]
    score_videos(old + new, cfg(baseline_window_days=180, min_peers=2), NOW)
    assert new[0]["baseline"] == pytest.approx(100.0)  # old videos ignored (2 recent peers suffice)
    solo = [mk(20, 1000, 10)] + [mk(21 + i, 100, 400) for i in range(3)]
    score_videos(solo, cfg(baseline_window_days=180, min_peers=2), NOW)
    assert solo[0]["peer_count"] == 3  # fell back to all same-class videos


def test_missing_views_and_live_ineligible():
    a = mk(1, None, 10)
    b = {**mk(2, 100, 10), "live_broadcast": "upcoming"}
    score_videos([a, b], cfg(), NOW)
    assert not a["eligible"] and not b["eligible"]


def test_raw_views_metric():
    v = mk(1, 1234, 10)
    score_videos([v], cfg(metric="views"), NOW)
    assert v["metric"] == 1234.0


# ---- report / end to end ----------------------------------------------
def test_end_to_end_csv_and_summary(tmp_path):
    c = client(fake_api_session())
    config = ResearchConfig(channels=[ChannelSeed(handle="@fake", language="hinglish", niche="gta")],
                            min_peers=1, top_n_per_channel=3)
    csv_path, md_path = run(config, c, get_tagger("none"), tmp_path, now=NOW)
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    assert len(rows) == 5
    by = {r["video_id"]: r for r in rows}
    assert by["v1"]["is_short_heuristic"] == "True" and by["v2"]["is_short_heuristic"] == "False"
    assert by["v5"]["title_script"] == "devanagari" and by["v5"]["is_short_heuristic"] == "True"  # 180s
    assert by["v3"]["eligible"] == "False" and by["v4"]["eligible"] == "False"
    assert by["v1"]["title_language_heuristic"] == "hinglish" and by["v1"]["topic"] == ""
    assert sum(r["is_top_outlier"] == "True" for r in rows) == 1
    md = md_path.read_text(encoding="utf-8")
    assert "correlational" in md and "survivorship" in md and "heuristic" in md
    assert "Top outliers per channel" in md and "Fake GTA Hinglish" in md
    assert "Median duration" in md and "Estimated API quota used: 4 units" in md
    assert not re.search("SECRETKEY", md)


def test_mark_top_outliers_fraction():
    vs = [{"outlier_score": float(i)} for i in range(20)] + [{"outlier_score": None}]
    assert report.mark_top_outliers(vs, 0.10) == 2
    assert sum(v["is_top_outlier"] for v in vs) == 2
    assert vs[19]["is_top_outlier"] and not vs[20]["is_top_outlier"]


def test_summary_without_scores():
    c = ResearchConfig()
    md = report.build_summary([], [{"channel_id": "C", "channel_title": "T"}], c)
    assert "No scorable videos" in md and "Not enough scored videos" in md


def test_null_tagger_default_and_unknown():
    assert NullTagger().tag({}) is None and isinstance(get_tagger(), NullTagger)
    with pytest.raises(ValueError):
        get_tagger("nope")
