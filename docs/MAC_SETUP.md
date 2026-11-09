# MilliClip — Mac Setup & Access Checklists

Two lists: what can be done **now from the phone/cloud** (no Mac), and what **requires
someone physically at the Mac**. The second list is the critical path and cannot be
avoided or done remotely until remote access is itself enabled (which is on the list).

---

## A. Can be completed NOW (phone / cloud workspace, no Mac)

- [ ] Build & test all pipeline code on sample footage (this repo).
- [ ] Validate highlight detection, selection, vertical rendering, subtitles — dry run.
- [ ] Write API client code (YouTube, Instagram) and test against mocks/sandbox.
- [ ] Create a Google Cloud project; enable **YouTube Data API v3**; create OAuth client
      (Desktop app). *(Account/browser steps; no Mac needed.)*
- [ ] Draft the **YouTube API compliance audit** submission (needed to un-private uploads).
- [ ] Convert Instagram account to **Business**, link a Facebook Page, create a Meta app,
      request `instagram_content_publish`; draft **app review** materials.
- [ ] Decide capture source (default: capture card) and order hardware if card chosen.
- [ ] Prepare the reproducible install package (`scripts/install_mac.sh`, launch agent).

## B. Requires someone PHYSICALLY at the Mac (one visit, ~30–45 min)

Do these in order. Steps 1–3 unlock all future remote work.

1. **Enable remote access (unlocks everything else):**
   - System Settings → General → Sharing → **Remote Login** (SSH) = On.
   - System Settings → General → Sharing → **Screen Sharing** = On.
   - Install **Tailscale**, sign in (create the account from the phone first), note the
     Mac's Tailscale IP. This gives secure access without router port-forwarding.
2. **Power / sleep (so it runs unattended):**
   - Settings → Displays → … or `pmset`: prevent system sleep on power adapter.
   - Energy: **Start up automatically after a power failure** = On.
   - Disable automatic macOS updates that force reboots (or schedule them).
3. **Install the pipeline:** run `scripts/install_mac.sh` (installs Homebrew ffmpeg,
   Python deps, the MilliClip service + launch agent).
4. **Capture hardware (cannot be done remotely):**
   - *Capture card:* plug Elgato between PS5 and TV (PS5 → card IN, card OUT → TV, card
     USB → Mac). On PS5 disable HDCP (Settings → System → HDMI). Confirm passthrough to TV.
   - *Remote Play (card-free):* install chiaki-ng, register PS5 with PIN, **test whether
     the TV still shows the game** while streaming (the open feasibility question).
   - *Broadcast (card-free):* link YouTube in PS5 settings; note it needs manual start.
5. **macOS permissions (TCC — cannot be granted remotely/headless):**
   - Grant **Screen Recording** to OBS and/or the terminal running capture.
   - Grant **Microphone**/**Camera** only if used.
6. **First-run OAuth (needs a browser click-through):**
   - Run `milliclip auth youtube` and `milliclip auth instagram`; complete consent in the
     browser. Tokens are written to git-ignored token files.
7. **Verify:** run `milliclip doctor` (checks ffmpeg, disk, permissions, credentials,
     capture device) and one `--dry-run` end-to-end pass.

## C. After GTA 6 release

- [ ] Tune detection thresholds (`config.detect.*`) against real GTA 6 footage.
- [ ] Confirm Rockstar's streaming/UGC policy and music-handling settings for GTA 6.
- [ ] Flip `publish.enabled` to true only after audits pass and a manual review of the
      first batch of generated clips.

---

### Why the iPhone can't do section B remotely

Same Apple ID provides Find My, iCloud Drive sync, Handoff — **none run commands or
control the screen**. Back to My Mac was removed in 2018. Remote Login / Screen Sharing /
Tailscale are all **off by default and can only be turned on at the Mac**. macOS Screen
Recording permission (TCC) cannot be granted headlessly. There is no supported remote path
until step 1 is done in person.
