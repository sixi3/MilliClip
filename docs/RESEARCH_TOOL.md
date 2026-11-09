# Competitor outlier-mining tool (`milliclip.research`)

Learns from **public** YouTube statistics which topics, hooks, lengths and languages over-perform for
comparable channels, before we publish our own Shorts/Reels. Official YouTube Data API v3 only — no
scraping, no browser automation. It is independent of the clipping pipeline.

## Setup

1. In Google Cloud Console create (or pick) a project → **APIs & Services → Library → "YouTube Data API v3" → Enable**.
2. **APIs & Services → Credentials → Create credentials → API key.** Restrict it to the YouTube Data API v3.
3. `export YOUTUBE_API_KEY=...` — the key is read **only** from this env var, sent in a request header
   (never in URLs), and never logged or written to outputs. Don't put it in files that get committed.
4. `cp research/channels.example.yaml research/channels.yaml` and replace the placeholders with
   channel IDs (`UC...`) or `@handles`, tagged with `language` / `niche`. Entries containing `PLACEHOLDER`
   are skipped. The example contains no verified real channels.

## Quota costs (default 10,000 units/day)

| Call | Units | Used for |
|---|---|---|
| channels.list | 1 | resolve ID/`forHandle`, get uploads playlist |
| playlistItems.list | 1 per 50 items | last N uploads |
| videos.list | 1 per 50 videos | snippet, duration, statistics |
| search.list | **100** | discovery only; off unless `--allow-search` |

A 100-upload channel costs ≈ 1 + 2 + 2 = 5 units. The tool prints estimated units (successful calls only)
and enforces `max_quota_units` (default 2000) per run.

## Usage

```bash
pip install -r requirements.txt
python -m milliclip.research --config research/channels.yaml      # or: milliclip-research ...
python -m milliclip.research --config research/channels.yaml --uploads 50 --out work/research
# discovery (costs 100 units per call; prints candidates, does not add them):
python -m milliclip.research --allow-search --discover "GTA 6 gameplay hindi" --region IN
```

Outputs (default `data/research/`, git-ignored; `work/` also works): `videos.csv` (all videos, features,
scores) and `summary.md` (top outliers per channel; top-10% vs rest feature comparison).

## Method

- **Shorts** = duration ≤ `shorts_max_seconds` (180). **Heuristic**: the API has no Shorts flag; short
  horizontal clips count, and Shorts over the limit don't.
- **Outlier score** = `metric / median(metric of same-channel, same-class peers)`. `metric` is
  `views_per_day` (views ÷ age in days; default, age-adjusted) or raw `views`. Videos younger than
  `min_age_days` (3) aren't scored. Peers = eligible videos of that channel and class published in the last
  `baseline_window_days` (180), excluding the video itself (`exclude_self`); if fewer than `min_peers`, all
  of the channel's same-class videos are used; if still fewer, no score. Settings are in the YAML
  (`settings.outlier`). Note views/day is still crude: view curves are front-loaded, so very recent
  videos tend to score high.
- **Features**: duration bucket, title length, title script (Devanagari/Bengali/Malayalam/Latin/mixed),
  language guess (script-based; romanized Hindi via a small wordlist — **heuristic**, Devanagari is
  reported as "hindi" but may be Marathi etc.), hashtag count (title + description), question/number/emoji
  in title, publish hour and weekday in IST.
- **Topic tagging**: pluggable `TopicTagger` (`milliclip/research/llm.py`), **off by default**; nothing calls an LLM.

## Interpretation caveats

Results are **correlational and survivorship-biased**: only seeded, still-public channels/videos are
seen; luck, trends, thumbnails and promotion are invisible; small samples are noisy; language and Shorts
labels are heuristics. Use findings as hypotheses to test on our own content.

## Tests

`pytest` — all API behaviour is tested against fake JSON fixtures with a mocked HTTP layer (no network).
No live API run has been performed for this tool.
