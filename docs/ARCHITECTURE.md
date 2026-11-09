# MilliClip — Architecture & Data Flow

## 1. Design principles

- **Modular, swappable stages.** Capture, detect, select, edit, publish are independent
  packages communicating through files on disk + a SQLite job store. Any stage can be run
  and tested in isolation.
- **Source-agnostic.** The capture source (card / Remote Play / broadcast) is behind one
  interface. Everything downstream is identical.
- **Fail safe, not fail loud.** Uncertain or failed clips are skipped; repeated errors
  pause publishing; nothing is deleted without bounded-storage rules; no duplicate posts.
- **Secrets never in source.** Credentials live in `.env` / OS keychain / token files that
  are git-ignored. Code reads them at runtime.
- **Supported APIs only.** No scraping, no browser automation for posting.

## 2. Data flow

```
          ┌─────────────┐
   PS5 ──►│  CAPTURE     │  source: card | remote_play | broadcast
          │  (segmenter) │  → recordings/seg_YYYYmmdd_HHMMSS.mp4  (bounded ring buffer)
          └──────┬───────┘
                 │ new segment event
          ┌──────▼───────┐
          │  DETECT      │  audio loudness (ebur128), scene cuts (scdet),
          │              │  optional speech (Whisper) → signals per segment
          │  RANK        │  weighted score → candidate highlight windows
          └──────┬───────┘
                 │ candidates (start, end, score, reasons)
          ┌──────▼───────┐
          │  SELECT      │  dedup / repetition filter, lead-in & ending,
          │              │  min-gap, per-run caps → chosen clips
          └──────┬───────┘
                 │ clip specs
          ┌──────▼───────┐
          │  EDIT        │  cut (stream-copy where possible), 9:16 reframe,
          │              │  Whisper word timings → ASS subtitles → burn-in,
          │              │  platform encode (YT Shorts / IG Reels) → renders/
          └──────┬───────┘
                 │ rendered vertical mp4 + sidecar json
          ┌──────▼───────┐
          │  PUBLISH     │  Claude: title/description/hashtags (grounded in transcript),
          │              │  confidence + daily-limit gates, dry-run default,
          │              │  YouTube + Instagram official APIs, idempotent
          └──────┬───────┘
                 │ post records
          ┌──────▼───────┐
          │  JOB STORE   │  SQLite: segments, clips, posts; content-hash dedup;
          │  + HEALTH    │  retry with backoff; disk watermarks; alerts
          └──────────────┘
```

## 3. Components (→ code)

| Stage | Package | Key external tool |
|---|---|---|
| Capture | `milliclip/capture/` | ffmpeg (segment muxer), OBS/chiaki-ng (source-dependent) |
| Detect | `milliclip/detect/` | ffmpeg `ebur128`/`astats`/`scdet`, faster-whisper (optional) |
| Select | `milliclip/select/` | — (pure Python) |
| Edit | `milliclip/edit/` | ffmpeg (crop/scale/subtitles=ASS/libx264) |
| Publish | `milliclip/publish/` | anthropic SDK, google-api-python-client, Instagram Graph API |
| Jobs | `milliclip/jobs/` | sqlite3 (stdlib) |
| Health | `milliclip/health/` | — (disk stat, pluggable alerters) |
| Orchestrate | `milliclip/cli.py` | — |

## 4. Storage model (bounded)

- `recordings/` is a **ring buffer**: segments are deleted oldest-first once total size
  exceeds `storage.max_recordings_gb`, but a segment is **never deleted while referenced**
  by an un-rendered clip. The health monitor enforces a hard floor of free disk.
- `renders/` keeps the last N published clips (`storage.keep_renders`) for re-use/audit.
- The SQLite store is the source of truth for what exists, what's been posted, and what
  must not be posted again.

## 5. Idempotency & dedup

- Every segment and clip gets a **content hash** (sha256 of the file, or of the
  normalized clip spec). The job store has a `UNIQUE` constraint on
  `(platform, content_hash)` for posts — a second attempt to publish the same content is a
  no-op, which prevents duplicate uploads across restarts.
- Highlight **repetition** is handled in selection: perceptual similarity (audio/scene
  signature) within a sliding window drops near-duplicate moments.

## 6. Safety gates (publishing)

1. `publish.enabled` master switch (default **false** → dry-run only).
2. `publish.min_confidence` — clips below threshold are skipped.
3. `publish.daily_limit` per platform — enforced against the job store.
4. **Circuit breaker:** after `publish.max_consecutive_failures`, publishing pauses and an
   alert fires; it stays paused until manually resumed.
5. Content-ID / music risk: a music-presence penalty biases selection; claims surface as
   alerts, never auto-appealed or bypassed.

## 7. Definition of Done

**Tested software prototype (achievable now, phone-only):**
- All stages implemented and unit/integration-tested on synthetic + sample footage.
- End-to-end dry run: sample MP4 → detected highlights → selected clips → vertical
  rendered files with burned subtitles → metadata generated → **private/dry-run** publish
  path exercised with mocked/sandbox API calls.
- Recovery tests pass: restart mid-run, disk-limit eviction, retry/backoff, dedup.

**Verified unattended home system (requires the Mac + hardware + live accounts):**
- Capture card (or chosen source) captures real PS5 output on the Mac unattended.
- macOS permissions granted; power/sleep configured; survives reboot.
- Real OAuth completed; YouTube audit + Meta review passed; at least one real
  private→public post per platform verified end-to-end.
- 24–48h soak test: continuous capture, bounded storage holds, alerts delivered,
  zero duplicate posts, graceful handling of an induced network outage.
