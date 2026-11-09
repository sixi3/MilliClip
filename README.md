# MilliClip

Automated gameplay clipping & publishing pipeline: capture PS5 gameplay → detect & rank
highlights → cut vertical clips with subtitles → generate titles/descriptions/hashtags →
publish to YouTube Shorts and Instagram Reels, unattended, with safety controls.

> **Status: Phase A (cloud build & test).** The software pipeline is being built and
> tested against sample footage with no access to the home Mac. A *verified unattended
> home system* requires a one-time physical Mac setup — see `docs/MAC_SETUP.md`. Read
> `docs/FEASIBILITY.md` first for what is and isn't possible before hardware is in hand.

## Why a capture source is swappable
The capture **source** (capture card / PS Remote Play / PS5 broadcast) sits behind one
interface; everything downstream is identical and testable now. Recommended source for the
live system is a **capture card** (no TV interference, true quality, fully unattended).

## Quick start (development / dry run)
```bash
pip install -r requirements.txt           # ffmpeg must also be installed (brew install ffmpeg)
cp config/config.example.yaml config/config.yaml
cp .env.example .env                       # fill in secrets (git-ignored)

# Run the pipeline on a sample file you own, dry-run (no uploads):
python -m milliclip run --input samples/your_clip.mp4 --dry-run

# Environment / permission / credential checks:
python -m milliclip doctor
```

## Layout
```
milliclip/
  capture/   source abstraction + ffmpeg segmenter (bounded ring buffer)
  detect/    audio loudness, scene cuts, optional Whisper speech, ranker
  select/    dedup, lead-in/out, min-gap, caps
  edit/      9:16 reframe, ASS subtitles + burn-in, platform encode
  publish/   Claude metadata, YouTube + Instagram clients, safety gates
  jobs/      SQLite store: dedup, retry, idempotent posts
  health/    disk watermarks + alerts
  cli.py     orchestrator
docs/        FEASIBILITY, ARCHITECTURE, MAC_SETUP, BACKLOG
config/      config.example.yaml
tests/       run on synthetic media (no footage required)
```

## Safety & policy
- Secrets never in source control (`.env`, token files, keychain).
- Publishing defaults to **off / dry-run**; confidence + daily-limit gates; circuit
  breaker pauses after repeated failures; content-hash dedup prevents duplicate uploads.
- Official APIs only — no scraping or browser automation for posting.
- Licensed in-game music is treated as a copyright risk (selection penalty + alerts), not
  bypassed.

See `docs/` for the full design, costs, and test plan.
