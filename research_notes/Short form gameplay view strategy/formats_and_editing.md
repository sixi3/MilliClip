# Cross-Platform Content Formats & Editing Craft for Viral Short-Form Gameplay (2026)

> Scope note: This research was conducted via WebSearch only. In this session WebFetch and direct `curl` were both blocked (DNS failures / proxy 403), so full-page retrieval of primary sources was not possible — findings rely on WebSearch's synthesized result summaries plus their cited caveats. Hosts confirmed blocked for fetch: `www.opus.pro`, `blitzcutai.com`, `www.medeo.app`, `techcrunch.com`, `crayo.ai` (and by extension all fetch targets). These would need network allow-listing to retrieve verbatim. Treat vendor/marketing statistics as unverified unless flagged otherwise; platform-policy facts are better corroborated.

---

## Key Question 1: Catalog the dominant short-form formats and when each performs best

### Takeaway
Six formats dominate. The two highest-leverage for an automated pipeline are (a) the raw highlight clip (works when the gameplay moment itself is the payoff — stunts, clutches, sandbox chaos) and (b) the "gameplay-as-background / brainrot" split where unrelated narration or text rides over satisfying gameplay (works when the *overlaid* content is the payoff and the gameplay only supplies motion). The brainrot/background format is the most scalable but also the most actively suppressed by platforms (see KQ2).

### Cited Findings
- **(b) Gameplay-as-background / "brainrot" split** — defining features are split-screen or layered visuals, typically Subway Surfers or Minecraft parkour gameplay running underneath/alongside the main content, an AI voiceover narrating something unrelated on top, and captions + sound effects timed to the voiceover (captions flashing in sync, SFX on each punchline). — [WebSearch synthesis of brainrot how-to vendor guides](https://www.medeo.app/blog/how-to-make-brainrot-videos)
- The top-half / bottom-half layout (e.g. Reddit story text or second video on top, gameplay on bottom) is pitched as an attention device: "one screen gets boring quickly and the other supplies new stimulation." — [vendor guide via WebSearch](https://inflowave.netlify.app/resources/minecraft-parkour-brainrot-page-playbook-2026)
- **Format lineage:** Reddit/Subway-Surfers videos evolved from split-screen clips of Family Guy scenes + mobile gaming; creators adopted the split specifically to dodge copyright (put borrowed footage on top, gameplay on bottom). — [Studybreaks via WebSearch](https://studybreaks.com/tvfilm/subway-surfers-new-storytelling-method)
- **(a) Raw highlight clip / (d) facecam overlay (GTA-specific):** The default for GTA stream clips is a stacked vertical split — facecam in the top third, gameplay below — because "for GTA streams the streamer's face is often the payoff." GTA 5 stream clips "usually need the streamer's reaction, because the gameplay alone looks like any other chase," whereas sandbox/stunt clips can stand alone. — [cut.pro blog via WebSearch](https://cut.pro/en/blog/cortar-gameplay-clipe-vertical-2026)
- A clip spreads when "a stranger gets the situation in a second or two and the clip ends right after the payoff." — [cut.pro via WebSearch](https://cut.pro/en/blog/cortar-gameplay-clipe-vertical-2026)
- **(c) Split-screen stacked two-video** and **(e) text-hook/story over gameplay** are variants of the same background mechanic; the standard pipeline for the story variant is: scrape post → TTS narration → subtitles → silent gameplay background → upload. — [free.ai tool pages via WebSearch](https://free.ai/video/reddit/)
- Unverified performance claims for the background format: one creator's Reddit/Subway-Surfers videos reportedly hit up to 10M views; "many such creators reported making $1,000/month"; vendor pages claim ~89% completion rates for gaming-background Reddit-story videos (no sourcing). — [Studybreaks + hooked.so/free.ai via WebSearch](https://studybreaks.com/tvfilm/subway-surfers-new-storytelling-method)

### Inferences
- For an automated GTA/open-world pipeline, the two cleanest templates to codify are: **full-frame raw highlight** (reframe 16:9→9:16 keeping the action centered) for self-explanatory stunt/chase/chaos moments, and **background-B-roll** (gameplay fills frame; narration + karaoke captions on top) for story/fact/hot-take overlays. The facecam-stacked split is only relevant if source footage includes a facecam.
- "Ends right after the payoff" is a concrete, implementable edit rule: trim clip-out to ~0.3–0.5s after the detected peak event rather than letting it run.

### Gaps
- No independent (non-vendor) measurement of which format wins on reach for GTA/action specifically. Completion-rate and revenue figures are all anecdotal/marketing.
- "(f) satisfying loops" as a standalone format had little dedicated coverage beyond the looping mechanics in KQ5; no GTA-specific satisfying-loop case studies found.

---

## Key Question 2: Gameplay-as-background — what goes on top, performance, and platform risk

### Takeaway
What farms views on top: AITA/Reddit stories via TTS, scary stories, fun facts, life tips/hacks, and hot takes. BUT this is the single most platform-endangered format in 2026 — YouTube, Meta/Facebook, Instagram, and TikTok all rolled out "inauthentic / unoriginal / reused content" demonetization-and-reach penalties across 2025–2026 that directly target mass-produced, repetitive, reposted, and generic-AI content. An automated pipeline must treat this format as high-risk for demonetization and reach-throttling.

### Cited Findings — what goes on top
- Overlay content that farms views: AI-voiced Reddit stories (AITA), scary stories, fun facts, life tips, hot takes — narration with synced captions + SFX over silent satisfying gameplay. — [brainrot/Reddit-story vendor guides via WebSearch](https://www.medeo.app/blog/how-to-make-brainrot-videos)
- The copyright-avoidance rationale (gameplay on bottom lets you use borrowed/narrated top content) is a *marketing* assertion, not a legal finding; "Reddit narration + royalty-free gameplay = no claims" is unverified. — [WebSearch brainrot synthesis](https://inflowave.netlify.app/resources/minecraft-parkour-brainrot-page-playbook-2026)

### Cited Findings — platform crackdowns (best-corroborated facts in this report)
- **YouTube (effective July 15, 2025):** YPP update reworded "repetitious content" → "inauthentic content" to stress that creators (even AI-using ones) must add effort/creativity. Framed by YouTube's Rene Ritchie as a "minor update"/clarification — mass-produced and repetitive content was already monetization-ineligible. It is NOT a blanket AI ban: AI used to *improve* content stays eligible, and legitimate reaction/clip content is explicitly unaffected. — [TechCrunch / Engadget / Windows Central coverage via WebSearch](https://techcrunch.com/2025/07/09/youtube-prepares-crackdown-on-mass-produced-and-repetitive-videos-as-concern-over-ai-slop-grows)
- **Meta / Facebook (blog post July 14, 2025):** Defined unoriginal content as repeatedly reusing another creator's work without credit; repeat reposters face **reduced reach + lost monetization**; creators who add commentary/reactions are not penalized. Meta said it removed ~10M profiles impersonating creators and ~500K spam accounts; rollout gradual over several months. — [Lindsey Gamble / Medianama / InfluencerMarketingHub via WebSearch](https://www.lindseygamble.com/blog/facebook-will-limit-reach-and-monetization-of-unoriginal-content)
- **Instagram (announced ~April 30, 2026):** Extended the reposted-content rules from Reels to photos/carousels. Aggregator accounts lose **Discovery/recommendation reach** (non-followers), though existing followers still see posts. Mosseri acknowledged aggregators but said they must adapt. — [PetaPixel / WebProNews via WebSearch](https://petapixel.com/2026-04-30/new-instagram-policies-target-reposted-content/)
- **TikTok (enforcement step-up from Sept 15, 2025):** Stricter enforcement against Unoriginal Content; watermarked/logo-heavy/reposted video is downranked and ineligible for Creator Rewards. Third-party (unverified) claims: Creator Rewards pays only on original videos >1 minute; repeated violations (often cited as 3) can mean permanent monetization loss. May 2026 reports: some creators say *original* videos were wrongly flagged, with no public TikTok response. — [BigSeller / SocialBoost / BallerAlert via WebSearch](https://www.bigseller.pro/blog/articleDetails/3778/tiktok-unoriginal-content.htm)
- An AI-generated fake "GTA 6 gameplay" clip reportedly reached ~8M views before the creator admitted it was fake — illustrates both the virality and the inauthenticity risk of synthetic gameplay. — [Eklipse via WebSearch](https://eklipse.gg/?p=19598)

### Inferences
- The common denominator platforms penalize is **repetition + lack of transformative effort + reposting**, not AI per se. An automated pipeline mass-producing near-identical background-gameplay videos sits squarely in the highest-risk bucket; the facecam/reaction and genuinely transformative highlight formats are explicitly lower-risk.
- Practical mitigations implied by the policies: add genuine transformation (commentary, editing, unique captions), vary templates, avoid watermarks/reposting others' clips, and prefer the account's *own* captured gameplay over scraped footage.

### Gaps
- No official platform text retrieved (fetch blocked); category lists (YouTube's "three specific AI content types") and exact thresholds unconfirmed. The "3-strike" TikTok monetization-loss number is anecdotal.
- No data on current (late-2026) *enforcement intensity* against gameplay-background specifically vs. other slop.

---

## Key Question 3: Concrete editing specs that boost retention

### Takeaway
Consensus implementable specs: 1080×1920 master; keep text/faces in a ~900×1400 center safe zone clear of bottom (~250–370px) and right (~120–164px) UI; bold word-by-word karaoke captions ~60–75px with high-contrast highlight and no background box, placed above the bottom UI; frequent zoom punch-ins and jump cuts for pacing; SFX stingers on beats. Most specific numbers are vendor-sourced and conflict at the margins, so treat them as starting ranges to A/B test.

### Cited Findings — 9:16 framing & safe zones
- Master canvas is **1080×1920 (9:16)** on TikTok, Reels, and Shorts; safe zones/crops differ by platform. — [WebSearch safe-zone synthesis](https://reap.video/blog/short-form-video-safe-zones)
- Official safe-zone specs are published mainly for **ads**, not organic posts — don't treat them as permanent organic pixel rules. — [reap.video via WebSearch](https://reap.video/blog/short-form-video-safe-zones)
- Conflicting UI-margin figures (keep captions/faces out of these):
  - Top ~120–200px, bottom ~250–370px, right ~120–164px, left ~50–60px; Shorts has the most aggressive bottom UI. — [WebSearch synthesis](https://www.houseofmarketers.com/guide-to-safe-zones-tiktok-facebook-instagram-stories)
  - Universal center safe zone ~**900×1400px**; TikTok top blocked ~108px, central zone ~900×1492px. — [WebSearch synthesis](https://www.upload-post.com/tools/safe-zone-checker/)
  - Reels bottom UI ~250px, TikTok bottom UI ~350px. — [WebSearch synthesis](https://reap.video/blog/short-form-video-safe-zones)
  - Design-system guide: 48px side margins → 984px-wide graphic-safe area. — [WebSearch synthesis](https://reap.video/blog/short-form-video-safe-zones)
- **Reframing gameplay 16:9→9:16:** a lazy crop "chops off half the action"; the player and the car must stay centered throughout. Hand-keyframing the crop for fast chases is the tedious core problem these tools automate. — [cut.pro via WebSearch](https://cut.pro/en/blog/cortar-gameplay-clipe-vertical-2026)

### Cited Findings — subtitles / captions
- Word-by-word (karaoke) captions are credited with better retention; "bold statement" presets work better for hook-driven clips, word-by-word for educational/narration. — [WebSearch caption synthesis](https://openclip.app/learn/caption-styling)
- Font size (conflicting; use as ranges on a 1080×1920 frame): BlitzCut puts Reels at **60–75px**; a Shorts guide recommends **7–10% of frame height (~54–70pt)**; Mosaic's API default is **108px** (range 20–120). — [WebSearch synthesis](https://blitzcutai.com/blog/best-caption-size-instagram-reels-2026)
- Weight: **bold 700–900** at 60–75px is more readable than thin weight at 90px. — [WebSearch synthesis](https://blitzcutai.com/blog/best-caption-style-instagram-reels-2026)
- Position: avoid the bottom ~20% (UI-covered); center-bottom placement sits above the Shorts UI overlay zone. — [WebSearch synthesis](https://blitzcutai.com/blog/best-caption-style-youtube-shorts-2026)
- Styling: high-contrast highlight on the active word, **no background box**, sentence case for body; ALL CAPS only for short hooks (caps slows reading of full sentences). — [WebSearch synthesis](https://openclip.app/learn/caption-styling)
- Single-source claim: clips with **2–3 caption updates in the first 3 seconds** outperform one static/no caption. — [dev.to hook-engineering via WebSearch](https://dev.to/bulkdl/hook-engineering-the-science-of-the-first-3-seconds-in-short-form-video-2026-2jp9)
- ~68% of TikTok / ~54% of Reels short-form views reportedly start sound-off or very low volume (2025 study, uncorroborated) — reinforces captions as mandatory. — [WebSearch synthesis; study not located](https://dev.to/bulkdl/hook-engineering-the-science-of-the-first-3-seconds-in-short-form-video-2026-2jp9)

### Cited Findings — zoom / jump cuts / pacing / SFX / progress bars
- **Zoom punch-in (ffmpeg `zoompan`):** zoom value is evaluated per-frame; official docs give a pattern that zooms 2x into center "only for the first second" via `if(between(in_time,...))`. A "zoom punch" = instant stepped tighter crop at a timestamp for emphasis on a word/beat; a gradual "push-in" is the slower variant. — [FFmpeg docs + Gooseworks skill via WebSearch](https://creatomate.com/blog/how-to-zoom-images-and-videos-using-ffmpeg)
- Example punch pattern (flagged by the source as unverified synthesis, test before use): `zoompan=z='if(between(in_time,2,2.2),1.15,1)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':fps=30:s=1920x1080`. Known old caveat: a 2014 trac ticket reported zoompan stops at 2s when overlaid (may not apply to current builds). — [WebSearch ffmpeg synthesis](https://creatomate.com/blog/how-to-zoom-images-and-videos-using-ffmpeg)
- Pacing heuristic: a visual change every **2–3 seconds** (low-authority source). — [WebSearch synthesis](https://www.socialync.io/blog/retention-techniques-keep-viewers-watching-2026)
- **Progress bars:** Vendor tools sell a "dummy progress bar" to make viewers feel a video is near its end (pitched for sales VSLs, not short-form). YouTube hides the Shorts seek bar until hover. No study found that a fake progress bar improves short-form retention, and showing false info may conflict with platform rules — use with caution. — [Panda Video / Previews via WebSearch](https://www.pandavideo.com/features/dummy-progress-bar)
- No source confirmed an ffmpeg approach for SFX stingers; mixing a delayed sound clip via `-filter_complex` (audio `adelay`/`amix`) is the implied method but uncorroborated. — [WebSearch ffmpeg synthesis](https://creatomate.com/blog/how-to-zoom-images-and-videos-using-ffmpeg)

### Inferences
- Safe-zone build target: render captions/overlays inside a centered **~900×1400** box; keep nothing load-bearing in the bottom ~320px or right ~160px. Validate per-platform by previewing.
- Caption default to codify: bold sans (700–900), ~64–72px, active-word highlight, outline/stroke for contrast (sources imply outline over box), 1–3 words visible at a time, positioned ~mid-lower frame above the UI band.
- Pacing engine: schedule a zoom punch or jump cut roughly every 2–3s and align SFX stingers to detected beats/punchlines.

### Gaps
- Exact stroke/outline width in px: not specified by sources (they say "outline/contrast, no box" qualitatively). Pick ~6–10px black stroke and test.
- No authoritative organic (non-ad) safe-zone pixel spec exists; numbers conflict by up to ~100px.
- No verified ffmpeg recipe for SFX timing or beat-synced effects.

---

## Key Question 4: Role of TTS / AI voiceover — tools and platform tolerance

### Takeaway
TTS/AI voiceover is the backbone of the background-story format. ElevenLabs is the most consistently recommended for realism; TikTok's built-in TTS and CapCut are the quick in-workflow options. Platform tolerance hinges on licensing (commercial-use rights) and on the "inauthentic content" rules from KQ2 — AI voice is tolerated when the video is transformative, risky when it powers mass-produced slop.

### Cited Findings
- **ElevenLabs** is put first for voice realism by nearly every source ("strongest when quality matters more than speed"); free tier ~10 min/month. — [Stork / ElevenLabs / DIYAI via WebSearch](https://www.stork.ai/blog/best-ai-voice-youtube-tiktok-2026)
- **TikTok built-in TTS:** good for quick native posts; limited editing/export control; not ideal for longer narration. — [WebSearch synthesis](https://diyai.io/ai-tools/audio-generation/tiktok-voice-generator/)
- **CapCut:** all-in-one voiceover + captions + editing; voice quality depends on selected style. — [WebSearch synthesis](https://www.stork.ai/blog/best-ai-voice-youtube-tiktok-2026)
- **Murf AI** (polished explainer narration) and **Speechify** (quick clean narration) are secondary picks. — [WebSearch synthesis](https://www.stork.ai/blog/best-ai-voice-youtube-tiktok-2026)
- Reddit-sourced picks: start with ElevenLabs free tier; Adobe Podcast has a free TTS feature. Warning (Jan 2026 Reddit analysis): some free tools may not grant **commercial licenses** — matters for monetization. — [WebSearch synthesis of Reddit threads](https://voxbooster.com/blog/ai-voice-generator-reddit-story-narration)
- Standard story pipeline uses TTS as step 2: scrape post → **TTS narration** → subtitles → silent gameplay background → upload. — [free.ai via WebSearch](https://free.ai/video/reddit/)

### Inferences
- For automation, ElevenLabs API is the realism default; the generated TTS also provides word-level timestamps that can directly drive karaoke-caption timing and SFX/zoom beat alignment (a key integration point for the pipeline).
- Platform "tolerance" of AI voice is really tolerance of the *overall* video's originality (KQ2); the voice itself is not what gets flagged.

### Gaps
- No explicit platform statement that AI *voice* alone triggers demonetization (it's bundled under inauthentic/mass-produced rules).
- Current (late-2026) ElevenLabs pricing/licensing terms not retrieved (fetch blocked) — verify commercial-use tier before monetizing.

---

## Key Question 5: What makes a clip LOOP, and why loops farm watch-time

### Takeaway
A loop works when the last frame visually/motion-wise flows into the first frame, so the viewer doesn't perceive the restart and watches past 100%, inflating average watch time and completion/replay signals that TikTok weights. Core techniques: plan the loop first, match motion across the seam, and use crossfade/masking/time-remap to hide the cut. Watch-time gains are real in principle but the headline "+40%" stat is poorly sourced.

### Cited Findings
- A seamless loop raises watch time by prompting replays; one widely-repeated figure is "**up to 40% higher watch time**," but it traces to secondary blogs, not TikTok data — do not rely on it. One extra pass can materially raise average watch time vs. duration. — [WebSearch looping synthesis](https://crayo.ai/blog/how-to-make-looping-content-for-tiktok)
- TikTok weights **completion rate and replays** (and Reels leans on shares/saves) — the mechanism loops exploit. — [WebSearch brainrot synthesis](https://inflowave.netlify.app/resources/minecraft-parkour-brainrot-page-playbook-2026)
- Editing approach: plan the loop before filming ("never shoot your beginning first"); the ending should flow perfectly back into the beginning. Four core techniques: **crossfades, matching action, masking, time remapping**. — [WebSearch looping synthesis](https://crayo.ai/blog/how-to-make-looping-content-for-tiktok)
- Testing: scrub the boundary frame-by-frame AND watch at full speed — a mathematically imperfect cut can feel seamless if motion carries the eye across it. — [WebSearch synthesis](https://faceless.so/blog/how-to-make-loop-videos-for-tiktok-reels-shorts)
- Measuring: aim for average watch time > video length; split-test different loop lengths/actions. Caveat: the second viewing should *add* something; avoid loops that feel merely repetitive. — [WebSearch synthesis](https://thesocialcat.com/glossary/video-loop-short-form-content)

### Inferences
- Implementable loop-seam rules for the pipeline: (1) choose clip in/out points where camera motion and on-screen composition are similar; (2) optionally apply a short crossfade (e.g. ffmpeg `xfade`) across the seam; (3) for background gameplay (Subway Surfers/driving), pick a segment with near-constant motion so the restart is imperceptible. Background endless-runner gameplay is intrinsically loop-friendly — a reason it's favored.
- Loops pair naturally with the background format: narration can end on a cliffhanger/open loop while the gameplay seam is visually continuous.

### Gaps
- No primary TikTok/platform data quantifying loop watch-time lift; the +40% number is unsourced.
- No GTA/driving-specific loop-seam case study; applicability inferred from endless-runner examples.

---

## Key Question 6: Hooks — first-frame patterns that work for gameplay

### Takeaway
Most drop-off is in the first 2–3 seconds, so the opening frame must show motion/action/face and the hook must front-load the payoff or a bold promise. Gameplay-specific guidance is thinner than general hook advice, but the recurring rule is: open on motion/action (not a logo or slow cut-in), and for stream clips make the situation legible within 1–2 seconds.

### Cited Findings
- Most videos lose **60–80% of audience in the first 3 seconds**; creators target **40%+ retention at 3s**, then hold **25%+** through the full video. — [WebSearch hook synthesis](https://dev.to/bulkdl/hook-engineering-the-science-of-the-first-3-seconds-in-short-form-video-2026-2jp9)
- Vendor claim (unconfirmed in primary platform sources): TikTok/YouTube have said first-3-to-5-second retention is the dominant ranking signal. — [WebSearch synthesis](https://www.capcut.com/create/short-form-video-hooks-first-3-second-patterns)
- Hook structures: open with the problem, the result, a surprising insight, or a bold claim rather than saving the payoff; sequence = hook (0–3s) → promise (3–5s) → main content → short CTA. — [WebSearch synthesis](https://jellymarketing.ca/blog/stop-the-scroll-in-3-seconds-secrets-to-high-performing-short-form-video-hooks/)
- Visual hook cues: first frame should have **motion, a face, or action**; avoid logos and slow cut-ins. — [WebSearch synthesis](https://dev.to/bulkdl/hook-engineering-the-science-of-the-first-3-seconds-in-short-form-video-2026-2jp9)
- Gameplay-specific: a clip works when "a stranger gets the situation in a second or two and the clip ends right after the payoff"; for GTA, the streamer's reaction/face is often the hook. — [cut.pro via WebSearch](https://cut.pro/en/blog/cortar-gameplay-clipe-vertical-2026)
- Suspect single-source stat: 0.84 correlation between 3-second retention and total views (from one person's 120-video test — not established). — [WebSearch synthesis](https://autoclip.dev/blog/viral-clip-anatomy-3-second-hook-data)

### Inferences
- For an auto-clipper on GTA/action: start the clip ~0.5–1s *before* the peak action so the first frame already has motion and the situation reads instantly; overlay a bold text hook (the promise/claim) in the first second; for background-story videos, the first spoken line + first caption is the hook and should state the stakes immediately.
- Captions-as-hook: 2–3 caption updates in the first 3s (KQ3) doubles as a hook tactic.

### Gaps
- No reliable gameplay-specific data on whether a clear objective on-screen, a near-fail, or a clutch moment makes the strongest first frame — sources recommend testing your own retention curves in Studio/analytics.

---

## Key Question 7: Tools and the specific features to replicate in ffmpeg

### Takeaway
CapCut = manual/all-in-one and cheap; Opus Clip = long→short repurposing with virality scoring and auto-reframe; Submagic = caption + auto-edit specialist (kinetic captions, auto-zooms, keyword B-roll, SFX). The pipeline-relevant features to replicate in ffmpeg are: speaker/action-tracking reframe, word-level karaoke captions, auto zoom punch-ins, keyword-triggered B-roll, silence/filler removal, and SFX/emoji stingers.

### Cited Findings
- **Submagic:**
  - Auto-zoom = dynamic zoom in one click, **6 zoom styles** (vendor lists fast, crash, smooth, expo, linear); zooms can be attached to a specific subtitle line. — [Submagic via WebSearch](https://submagic.co/features/auto-zooms)
  - **B-roll** = keyword-matched stock footage pulled from the transcript (Pro+ adds premium B-roll + movie clips). — [Submagic via WebSearch](https://submagic.co/features/b-rolls)
  - Animated emojis/colors/GIFs in captions; emoji transitions can animate with sound; sound effects + background music + AI audio cleanup; removes silences/filler words; "Magic Clips" highlight extraction; caption translation. — [Submagic via WebSearch](https://submagic.co/features/add-sound-effects-to-video)
  - Vendor claim: 98.9% subtitle accuracy (vs. Opus Clip 97%). — [Submagic via WebSearch](https://www.submagic.co/alternatives/opus-clip)
- **Opus Clip:**
  - **Auto-reframe** on every plan (detects speakers/moving objects; object tracking Pro+). — [Castmagic/thecmo via WebSearch](https://www.castmagic.io/software-reviews/opus-clip)
  - **AI B-roll** insertion Pro-only; auto **hook** overlay on top clips (free tier); AI intro titles higher-tier; clip titles/descriptions/hashtags from Starter. — [WebSearch synthesis](https://thecmo.com/tools/opusclip-review/)
  - **Virality score** (sources disagree: 0–99 or 0–100) from hook strength, flow/pacing, value, emotional peaks, and trending signals; most useful for short formats where opening seconds matter. — [Castmagic via WebSearch](https://www.castmagic.io/software-reviews/opus-clip)
  - Pricing (conflicting): Starter ~$15/mo, Pro ~$29/mo. — [WebSearch synthesis](https://thecmo.com/tools/opusclip-review/)
- **CapCut:** the free/manual option; adjust every caption by hand (desktop/mobile); matching the animated look takes more work; some auto-caption functions are Pro-only. — [WebSearch synthesis](https://hackceleration.com/labs/switch/submagic)
- **Eklipse / StreamLadder / ClipSpeedAI / Cut.Pro / AutoClip:** gaming-specific auto-clippers that detect highlights (heists, stunts, clutches) and auto-reframe to vertical — marketed for GTA; claims are vendor marketing, not independently tested. — [Eklipse/cut.pro via WebSearch](https://eklipse.gg/use-case/grand-theft-auto-v-highlights)

### Inferences — ffmpeg replication map
- **Auto-reframe (16:9→9:16):** detect subject (player/car/face) bounding box per segment, then `crop`+`scale` with a smoothed center-x track (replicates Opus/Submagic object-tracking reframe). This is the hardest-to-replicate, highest-value feature for GTA action.
- **Karaoke captions:** generate from TTS/ASR word timestamps → render active-word highlight via `drawtext` per-word (or burn an ASS/SSA subtitle with `\k` karaoke tags via the `subtitles` filter) — replicates Submagic/CapCut word-by-word.
- **Auto zoom punch-ins:** `zoompan` stepped crop at caption/beat timestamps (KQ3) — replicates Submagic auto-zooms.
- **Keyword B-roll:** map transcript keywords → stock clips → `overlay`/concat at those timestamps — replicates Submagic/Opus B-roll.
- **Silence/filler removal:** `silenceremove` audio filter + matching video cuts — replicates Submagic's "remove silences."
- **SFX/emoji stingers:** `amix`/`adelay` for audio stingers and `overlay` of emoji PNGs at beats (uncorroborated ffmpeg path — test).

### Gaps
- Current exact pricing/tiers for all three tools are inconsistent across sources (fetch blocked) — verify on vendor sites.
- No source gave the internal parameters of auto-reframe tracking (smoothing, detection model), so ffmpeg replication must be reverse-engineered empirically.
- No confirmed ffmpeg recipe for beat-synced SFX or the exact Submagic zoom-style curves (fast/crash/expo/etc.).
