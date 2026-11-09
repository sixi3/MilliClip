# MilliClip — Feasibility Assessment

_Last updated: 2026-11-09. Written from an iPhone-only context; the Mac mini is not
reachable from any coding workspace (no remote access configured)._

## 1. Verdict

A **tested software prototype** of the full pipeline (capture → detect → select →
edit → publish) is **buildable and testable now** in a cloud workspace using sample
footage, with no access to the Mac. A **verified unattended home system** is **not**
fully testable before physical access to the Mac, because capture hardware, macOS
permissions, and live publishing authorization all require someone at the machine.

This split is the single most important thing to understand: see the Definition of
Done (`docs/ARCHITECTURE.md` §Definition of Done).

## 2. Hard blockers (must be resolved by a person at the Mac)

| Blocker | Why it blocks | Needs physical Mac? |
|---|---|---|
| Capture input | No capture card confirmed; no card-free route avoids the Mac visit | **Yes** |
| macOS Screen Recording permission | OBS/ffmpeg screen capture is gated by TCC; cannot be granted remotely | **Yes** |
| Remote access not configured | iPhone + same Apple ID does **not** grant Mac control | **Yes** (one-time) |
| PSN login for Remote Play | chiaki-ng needs an interactive PSN registration (PIN) | **Yes** |
| YouTube/Instagram OAuth consent | First-run OAuth needs a browser click-through | **Yes** (one-time) |
| Platform app review | YouTube audit & Meta app review gate public posting | No (submission is remote, but needs real accounts) |

**There is no supported way to reach the powered-on Mac from the iPhone with no remote
access set up.** Shared Apple ID gives Find My, iCloud Drive sync, and Handoff-class
features — none of which run commands or control the screen. Back to My Mac was removed
in 2018. Enabling Remote Login / Screen Sharing / Tailscale can only be done _at_ the
Mac. This is a ~10-minute one-time task; instructions are in `docs/MAC_SETUP.md`.

## 3. Capture options (card vs. card-free)

| Option | TV interference | Quality | Unattended | GTA6 block risk | Mac visit |
|---|---|---|---|---|---|
| **Capture card** (Elgato HD60 X / 4K X) | None | True 4K/60 | Yes | None | Once |
| Remote Play (chiaki-ng → OBS) | **Likely** (unconfirmed — test on HW) | 1080p, compressed | Yes (auto-reconnect) | Low | Once |
| PS5 broadcast → unlisted YouTube → record | None | Limited, compressed | **No** (manual start) | **Possible** | Once |

- **Recommended:** capture card. Most reliable, no TV interference, true quality,
  fully unattended. ~$180 (HD60 X) and the same single Mac visit every option needs.
- The capture **source is a swappable module** (`milliclip/capture/`), so the entire
  downstream pipeline is identical regardless of source and can be built/tested now.
- HDCP must be disabled on the PS5 for a capture card (Settings → System → HDMI). This
  disables Netflix/Disney+/etc. on the console while active — a known trade-off.
- **Open question to settle on hardware:** does Remote Play blank/replace the TV output?
  Sources suggest the PS5 allows only one active session; this must be tested, not assumed.

## 4. Publishing eligibility (verify against live docs before relying on numbers)

These figures come from third-party sources; the official Google/Meta developer pages
were **not reachable** from this workspace (`developers.google.com` and
`developers.facebook.com` are outside the allowed network). **Re-verify at setup.**

- **YouTube Data API v3** — `videos.insert`. Projects created after 2020-07-28 that are
  **unverified** upload videos **locked to private**, regardless of requested privacy,
  until a **compliance audit** passes. Quota reporting is inconsistent across sources
  (historically 1600 units/call out of 10,000/day ≈ 6 uploads/day; later reports claim a
  move to a per-call bucket of ~100 uploads/day). **Verify the current quota and audit
  requirement in the Cloud Console before planning volume.**
- **Instagram** — Content Publishing API requires an **Instagram Business account**
  (Creator reportedly unsupported), a linked Facebook Page, and
  `instagram_content_publish` permission (app review needed for production/other users).
  Video is supplied via a **public HTTPS URL** or resumable upload; the working
  rate-limit figure is **~100 published posts / 24h**, queryable at
  `GET /<IG_ID>/content_publishing_limit`. Reels duration limits are reported
  inconsistently (90s vs 15min) — **verify against the current Reels reference.**
- **Do not** use unsupported scraping or browser automation for posting. The code uses
  only official APIs and defaults to **private/unlisted dry-run** until audits pass.

## 5. Copyright / licensed music

GTA radio stations contain **licensed music** that platform Content ID can detect,
risking claims, muting, or blocked Shorts. Mitigations the pipeline supports:
- Prefer clips where **radio/music is low or absent** (the audio analyzer already
  measures loudness; a music-presence penalty can bias selection away from music-heavy
  moments).
- Optionally **duck or replace** in-game music on export (configurable; off by default).
- Treat any Content ID claim as an **alert**, not an auto-appeal. No claim-bypassing.
Rockstar's policy for GTA 6 UGC/streaming is **not yet published**; verify at launch.

## 6. What can be done now from the phone vs. at the Mac

See `docs/MAC_SETUP.md` for the full checklists. Summary:
- **Now (phone/cloud):** all code, all unit/integration tests on sample footage, private
  "dry-run" render validation, API client code, OAuth app *registration* prep, audit
  submission drafting, repo + CI.
- **At the Mac (one visit):** plug in capture card, grant Screen Recording, install the
  package, run first-run OAuth, enable remote access + Tailscale, set power/sleep.
- **After release:** tune detection thresholds against real GTA 6 footage.

## 7. Reliability limits (candid)

- Card-free capture (Remote Play) can drop sessions and depends on PSN staying logged in.
- Unattended 24/7 operation on a consumer Mac is subject to OS updates, sleep, and
  network blips; the health monitor mitigates but cannot eliminate these.
- Platform APIs change quotas and review rules; the system must degrade safely (skip,
  pause, alert) rather than retry blindly.
- **The complete home system cannot be fully verified until hardware is in hand.**
