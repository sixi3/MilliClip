# MilliClip — Staged Implementation Backlog

Phases map to the plan: A (cloud build/test) → B (validate selection/render/private
uploads) → C (reproducible Mac package) → D (deploy on home HW) → E (tune on GTA 6).

## Phase A — Cloud build & test on owned footage  *(no Mac; in progress)*
- [x] Repo scaffold, docs, config schema, `.gitignore` (no secrets).
- [x] Job store: SQLite, content-hash dedup, retry/backoff, idempotent posts.
- [x] Detection: audio loudness, scene cuts, optional Whisper, ranker.
- [x] Selection: dedup/repetition, lead-in/out, min-gap, caps.
- [x] Editing: 9:16 reframe, ASS subtitles + burn-in, platform encode.
- [x] Metadata: Claude structured title/description/hashtags grounded in transcript.
- [x] Publishing clients: YouTube + Instagram, dry-run default, safety gates.
- [x] Capture abstraction + ffmpeg segmenter (bounded ring buffer).
- [x] Health monitor: disk watermarks, pluggable alerts.
- [x] CLI orchestrator + `doctor`.
- [x] Tests on synthetic media (detection, selection, render, dedup, retry, disk, restart).
- [ ] CI workflow (GitHub Actions) running the suite with ffmpeg installed.

## Phase B — Validate on real sample gameplay  *(no Mac)*
- [ ] Run full pipeline on user-provided sample MP4s; eyeball highlight quality.
- [ ] Tune default weights/thresholds on samples.
- [ ] Exercise YouTube private upload + Instagram test/sandbox where supported.
- [ ] Measure throughput & storage on real footage; record in `docs/COSTS.md`.

## Phase C — Reproducible Mac package  *(no Mac to build; needs Mac to run)*
- [ ] `scripts/install_mac.sh` (Homebrew ffmpeg, venv, deps, launch agent plist).
- [ ] `milliclip doctor` environment/permission/credential checks.
- [ ] Source-specific setup docs (card vs chiaki-ng vs broadcast).
- [ ] First-run OAuth flows + token storage.

## Phase D — Deploy & test on home hardware  *(requires Mac + capture + accounts)*
- [ ] Capture real PS5 output unattended; confirm no TV interference for chosen source.
- [ ] 24–48h soak: bounded storage, alerts, zero duplicate posts, induced outage recovery.
- [ ] First real private→public post per platform after audits pass.

## Phase E — Tune on GTA 6  *(after release)*
- [ ] Threshold tuning on real GTA 6 footage.
- [ ] Music/Content-ID handling validated against actual radio audio.
- [ ] Confidence gate & daily limits tuned to observed quality.

## Known risks / open questions (tracked)
- Remote Play TV-interference: unresolved until hardware test (Phase D).
- YouTube audit + quota reality: verify in Console before volume planning.
- Instagram app review timeline + Reels duration cap: verify against live docs.
- GTA 6 streaming/UGC + music policy: not yet published; verify at launch.
