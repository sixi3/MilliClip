# YouTube Shorts — Short-Form Gameplay View & Engagement Strategy (2026)

> Scope: Organic/authentic tactics to maximize views + watch-time for gameplay clips (GTA / open-world / action) on YouTube Shorts, for a US audience, to encode into an automated clipping pipeline. ToS-compliant only; risk flags called out.
>
> **Sourcing caveat (important):** In this session `WebFetch` was network-blocked for every external host attempted, including `support.google.com`, `vidiq.com`, `dev.to`, and `fluxnote.io` (DNS `ENOTFOUND` — those hosts must be allow-listed in the session's network settings to fetch full pages). All findings below therefore come from `WebSearch` result summaries, which quote the underlying pages. I could NOT open YouTube's own Help pages directly to copy exact policy wording; where primary-source wording matters, that is flagged as a Gap. Most non-YouTube sources are creator-economy/vendor blogs — directional, not authoritative — and are flagged as such.

---

## Optimal Shorts length for gameplay, and how length interacts with loop/replay signals

### Takeaway
No official YouTube "optimal length" exists; the hard cap is 3 minutes (since Oct 2024). For gameplay clips the practical consensus is short and tight — roughly 15-40s, with the clip ending immediately after the payoff so it reads in one or two seconds and invites a replay/loop. Retention % matters more than raw duration.

### Cited Findings
- Shorts max length was extended to **3 minutes in October 2024** (previously 60s) — [Piktochart](https://piktochart.com/blog/how-long-youtube-shorts/); [1of10](https://1of10.com/blog/how-long-can-youtube-shorts-be/).
- YouTube publishes **no official recommended/optimal length** — any "sweet spot" is strategy, not platform guidance — [Piktochart](https://piktochart.com/blog/how-long-youtube-shorts/).
- Suggested ranges vary by source: 15-40s, 30-60s, and one 2026 guide says the sweet spot has moved *longer* than the 20-25s it was in 2024 — [Piktochart](https://piktochart.com/blog/how-long-youtube-shorts/).
- Algorithm favors **retention over length**; aim for ~80%+ completion; a tight 25s clip beats a padded 60s one — [Piktochart](https://piktochart.com/blog/how-long-youtube-shorts/).
- Gaming Shorts have **high replay value** — "viewers rewatch impressive plays" — cited alongside 10M+ view examples (BGMI/Free Fire/Valorant); vendor source — [ClipSpeed GTA6](https://clipspeed.ai/gta6/turn-gta-6-gameplay-into-viral-shorts.html).
- Viral GTA clips "spread because a stranger gets the situation in a second or two and the clip **ends right after the payoff**" — a clean stop/loop point matters more than a long build-up — [Eklipse](https://blog.eklipse.gg/basic-knowledge/best-games-to-stream-for-viral-clips.html).
- A clip should "resolve cleanly, so viewers don't need a replay to understand it" (payoff should not *require* replay to parse) — [Nerdbot](https://nerdbot.com/2026/01/26/what-makes-a-game-streamable-in-10-seconds-designing-moments-that-work-for-shorts-and-reels/).

### Inferences
- For an automated pipeline, target **~12-30s** per gameplay clip as the default band: long enough to establish context + deliver the payoff, short enough that a viewer who likes it re-watches (boosting the re-watch/loop signal). Allow longer (up to ~45-60s) only when the moment genuinely needs setup.
- "End right after the payoff" + "high replay value" are complementary: trimming the tail so the last frame is the climax maximizes the odds the Short loops back to frame 1, inflating average-%-watched and re-watch signals. Encode a rule: cut the out-point within ~0.5-1s of the detected climax, not after a slow decay.
- A near-seamless visual loop (last frame compositionally similar to first) is plausibly beneficial but is NOT directly sourced (see Gaps).

### Gaps
- No source gives a gameplay-specific optimal-length *dataset* with retention curves; ranges are generalized creator-blog estimates.
- "Seamless loop" (matching first/last frame to force continuous replay) was not directly confirmed by any source — only the adjacent "replay value" and "clean ending" points.

---

## Hook tactics for the first 1-3 seconds

### Takeaway
The opening ~1-3 seconds decide retention. For gameplay the dominant tactic is a cold-open on the peak of the action (reverse-order editing: show the result first), a first-frame text hook, and avoiding any slow chronological build-up. Curiosity-gap / "wait for it" / question hooks are common but the gameplay-specific winner is "payoff-forward."

### Cited Findings
- Consensus hook window is **first 1-3 seconds**; some put it at 1s (vidIQ cited), others stretch effective window to ~5-6s — [Opus.pro hooks](https://www.opus.pro/blog/youtube-shorts-hook-formulas); [GoFaceless 2-second rule](https://www.gofaceless.ai/en/blog/mastering-first-impressions-two-second-rule).
- Gaming guide: Shorts with a clear hook **within the first ~1.5s consistently outperformed** slower builds (no methodology given) — [FluxNote gaming](https://fluxnote.io/blog/youtube-shorts-strategy-for-gaming-creators-in-2026).
- Recommended gameplay edit: **reverse-order** (show the result/outcome first) + a **caption on the first frame**; warns chronological "fight starts → buildup → final kill" structure "gets almost everyone scrolling away" — [FluxNote gaming](https://fluxnote.io/blog/youtube-shorts-strategy-for-gaming-creators-in-2026).
- Open on the **peak of the action**, keep subject centered in a 9:16 crop; avoid slow ramp-ups and "lazy crops" that chop the action — [ClipSpeed GTA6](https://clipspeed.ai/gta6/turn-gta-6-gameplay-into-viral-shorts.html).
- Common hook types: curiosity gaps, pattern interrupts, bold claims; one blog's own dataset claims curiosity-gap hooks averaged a 68% first-3s retention rate (single-creator sample) — [dev.to hook engineering](https://dev.to/bulkdl/hook-engineering-the-science-of-the-first-3-seconds-in-short-form-video-2026-2jp9).
- Retention targets cited for the first 3s range widely (~60% to ~80%); all unverified vendor figures — [Opus.pro hooks](https://www.opus.pro/blog/youtube-shorts-hook-formulas).

### Inferences
- Pipeline rule: detect the climax, then **reorder** so a 0.3-0.8s flash of the payoff (or a text hook teasing it) precedes the setup; or simply cold-open as close to the action as possible. Never start on menus, loading, or a slow approach.
- Burn a short **first-frame text hook** (question or claim) tied to the clip's moment (e.g. "He didn't see this coming…", "Wait for the landing").

### Gaps
- Retention-percentage thresholds for the first 3s are vendor estimates with no YouTube confirmation; treat as directional.

---

## What the Shorts algorithm ranks on in 2026 (confirmed vs unconfirmed signals)

### Takeaway
2026 consensus: the algorithm weighs **viewer satisfaction + retention/completion + re-watches/loops** alongside engagement-per-view (likes/comments/shares), tested first on a small audience. The only semi-confirmed shift (attributed to YouTube creator liaison Rene Ritchie) is "satisfaction over raw watch time." Exact signal weights are unpublished; sources conflict on whether swipe-away rate or watch-time-per-impression dominates.

### Cited Findings
- Reported shift from raw watch time toward **viewer satisfaction** as the dominant signal, attributed to statements from YouTube creator liaison **Rene Ritchie**; satisfaction inferred from post-watch surveys + whether viewers keep browsing after (session continuation) + repeat viewing + likes — [SocialBee](https://socialbee.com/blog/youtube-algorithm/); [vidIQ Shorts algorithm](https://vidiq.com/blog/post/youtube-shorts-algorithm/).
- Shorts are **tested on a small audience first**, then promoted based on swipe-through rate, watch completion, likes, shares, comments — [SocialPilot](https://www.socialpilot.co/de/youtube-marketing/youtube-algorithm).
- Sources **conflict** on the top Shorts signal: some say Shorts moved from swipe-rate to **watch-time-per-impression**; one guide still puts **swipe-away rate in the first 2s** at the top — [SocialBee](https://socialbee.com/blog/youtube-algorithm/); [quso.ai](https://quso.ai/blog/youtube-shorts-algorithm).
- Completion + loops commonly cited; one guide claims Shorts <30s with >85% completion get strong boosts (threshold has no visible source) — [vidIQ Shorts algorithm](https://vidiq.com/blog/post/youtube-shorts-algorithm/).
- Multiple sources explicitly note **exact signal weights are not published** by YouTube — treat any % breakdown as estimate — [SocialBee](https://socialbee.com/blog/youtube-algorithm/).

### Inferences
- Practical ranking model to encode: maximize (a) **% watched / completion**, (b) **re-watches/loops**, (c) **swipe-vs-view** (did they stay vs flick away in first 2s), (d) **engagement-per-view** (like/comment/share rate), and (e) **session continuation** (did the viewer keep watching Shorts after). These are the levers every source agrees on even while disagreeing on their relative weights.
- Because distribution starts with a small test cohort, the **first-2s hook and completion** disproportionately gate whether a clip ever scales. Optimize those first.

### Gaps
- No primary YouTube/Creator Insider document was directly retrievable (fetch blocked). The Rene Ritchie "satisfaction > watch time" framing is reported secondhand; treat the specific weighting as unconfirmed.

---

## Captions/subtitles (burned-in), on-screen text, auto vs styled

### Takeaway
Burned-in captions are strongly recommended for retention (silent autoplay / sound-off viewers), and are treated as better than YouTube's native auto-captions for retention (native = accessibility). Claimed lift is 15-25% retention / ~18% watch-time, but these are vendor figures. Keep text clear of the Shorts UI and the subject; word-level (karaoke) captions may hold attention better; text should add info, not just repeat audio.

### Cited Findings
- On-screen text claimed to raise watch-time ~**18%** (cites "Instavar 2026 production research"); burned-in captions claimed to correlate with **15-25% higher retention** — both vendor sources, no primary study found — [Opus.pro captions](https://www.opus.pro/blog/youtube-shorts-caption-subtitle-best-practices).
- Burned-in text favored over native captions **for retention**; YouTube auto-captions "may be sufficient for accessibility, but for retention they are not" — [Opus.pro captions](https://www.opus.pro/blog/youtube-shorts-caption-subtitle-best-practices).
- Placement guidance **conflicts**: one warns against the bottom third (Shorts UI covers it) and recommends center; another says lower third to avoid blocking faces. Agreement: keep text off the UI and off the subject/face — [Opus.pro captions](https://www.opus.pro/blog/youtube-shorts-caption-subtitle-best-practices); [OverseerOS](https://www.overseeros.com/blog/how-long-should-on-screen-text-stay-youtube).
- On-screen text dwell time ~1.5-3s per line; one source suggests min font ~60px at 1080x1920 (unconfirmed) — [OverseerOS](https://www.overseeros.com/blog/how-long-should-on-screen-text-stay-youtube).
- **Word-level (karaoke-style) captions** argued to hold attention better by forcing the eye to track at speech speed; text should add to narration, not repeat it — [alcheclip word-level](https://alcheclip.vercel.app/guides/word-level-vs-line-level-captions).

### Inferences
- Pipeline rule: always **burn in** styled captions (not rely on YouTube auto-captions), positioned in the safe zone (roughly vertical center / upper-middle, clear of the bottom ~15-20% reserved for the Shorts UI and the right-side action rail). For gameplay with little speech, use short punchy on-screen text/labels rather than full transcripts.
- Styled word-level captions are a reasonable default over static line blocks.

### Gaps
- All retention-lift percentages are vendor marketing numbers; no independent/YouTube study found. UI safe-zone pixel margins not authoritatively specified.

---

## Hashtags, titles, descriptions for Shorts gameplay (incl. #shorts)

### Takeaway
Title is the single biggest SEO lever; put the main keyword there. Use ~3-5 total hashtags (hard cap 15 combined across title+description — exceed it and YouTube ignores ALL of them). #shorts usage is debated and increasingly treated as minor/optional. YouTube also analyzes the actual audio/visual content for relevance, so on-screen/spoken keywords matter.

### Cited Findings
- **Title = single most important SEO element you control**; put most important keyword in the first ~25 words of the description too — [vidIQ SEO](https://www.vidiq.com/blog/post/youtube-seo/); [metadatareactor](https://metadatareactor.com/blog/youtube-shorts-seo-guide/).
- Hashtag count: most recommend **3-5**; hard cap is **15 total combined across title+description** — exceeding it causes YouTube to **ignore all** hashtags — [hashtagtools](https://hashtagtools.io/blog/youtube-shorts-character-limits-title-description-hashtags-2026).
- Placement conflicts: some say description-end (first 3 shown above title), some say title-end only for Shorts; top-3 hashtags display above the title on the Shorts player — [hashtagtools](https://hashtagtools.io/blog/youtube-shorts-character-limits-title-description-hashtags-2026); [YT hashtags guide](https://ytthumbnail-2va.pages.dev/blog/youtube-hashtags-guide).
- Hashtags characterized as a **minor discovery tool**; they "no longer reliably boost algorithmic distribution" — title/keyword optimization matters more — [vidIQ SEO](https://www.vidiq.com/blog/post/youtube-seo/).
- YouTube can **analyze what is said and shown** in a Short for relevance (content itself is an SEO input, not just metadata) — [miraflow SEO](https://miraflow.ai/blog/youtube-shorts-seo-2026-how-to-rank-shorts-in-search).

### Inferences
- Pipeline metadata rule: a keyword-forward **title** naming the game + the moment (e.g. "GTA 6 — insane police chase escape"), 1 optional hashtag in title (e.g. #GTA6), 2-3 more in description (e.g. #gaming #shorts #gta), total ≤5. Keep main keyword in the first sentence of the description.
- `#shorts` is low-value in 2026 but low-risk; include it once at most. Do NOT keyword-stuff hashtags (risk: all ignored past 15; also reads as spam).
- Because content is analyzed, accurate burned-in text / spoken keywords reinforce ranking — align captions with the target keyword.

### Gaps
- Sources contradict each other on title-vs-description hashtag placement; no YouTube primary doc retrievable to settle it. Whether `#shorts` still influences Shorts-shelf eligibility in 2026 is unconfirmed (historically it was never strictly required).

---

## Posting cadence and best times (US audience)

### Takeaway
For a US audience, default to Eastern Time windows (covers the largest population + aligns Central). Common slots: morning 7-9am ET, lunch 12-2pm ET, evening 7-10pm ET. Cadence: ~3-5/week minimum, up to 1+/day for growth; one large study found ~3x/week channels grew views faster than <monthly posters. Consistency reportedly matters more than exact timing. All figures are vendor/blog-level, not YouTube-official.

### Cited Findings
- Optimize for **Eastern Time** for a US audience (largest population center, ~aligns Central) — [HopperHQ](https://www.hopperhq.com/blog/best-time-to-post-youtube-shorts/); [SocialPilot times](https://www.socialpilot.co/insights/best-time-to-post-on-youtube).
- Time windows cited: **7-9am ET** (morning), **12-2pm ET** (lunch); another gives 12-3pm + 7-10pm; one source cites a Friday 3-4pm Shorts slot (single source) — [SocialPilot times](https://www.socialpilot.co/insights/best-time-to-post-on-youtube); [BloggingWizard](https://bloggingwizard.com/best-time-post-youtube-shorts/).
- Cadence: **3-5 posts/week** for brands, **daily** for growth-focused creators — [CoSchedule](https://coschedule.com/social-media-marketing/best-times-to-post-on-youtube-shorts).
- A **vidIQ study of ~5.08M channels** (cited secondhand) found channels posting **~3x/week grew views faster** than those posting less than monthly — [SocialPilot times](https://www.socialpilot.co/insights/best-time-to-post-on-youtube).
- **Consistency > exact timing** for Shorts; check YouTube Studio audience report for your own peak windows — [HopperHQ](https://www.hopperhq.com/blog/best-time-to-post-youtube-shorts/).

### Inferences
- Pipeline scheduling default: publish 1-3 Shorts/day staggered across US peak windows (late morning + lunch + evening ET), front-loading evening for gaming (gamer audiences skew evening). Avoid dumping multiple Shorts in one hour.
- Since consistency dominates, a steady daily cadence is likely better than bursty batches — but watch for self-cannibalization / reused-content risk if clips are too similar (see policy section).

### Gaps
- No 2026 US-specific, gameplay-specific posting dataset; windows are generalized. No evidence on an upper frequency limit before reach degrades (diminishing returns/cannibalization unquantified).

---

## Does YouTube allow/monetize "gameplay-as-background B-roll under unrelated content" (subway-surfers style)?

### Takeaway
High demonetization risk. A plain gameplay background with no original commentary, editing, or educational/transformative value is exactly the pattern YouTube's **reused content** and **inauthentic/mass-produced content** policies target. These policies apply **channel-wide** (can demonetize the whole channel), are separate from copyright, and were tightened/clarified on **July 15, 2025** ("repetitious" → "inauthentic"). Gameplay itself is fine; the subway-surfers overlay-under-unrelated-content format specifically is the risky case. FLAG: this format risks losing YPP monetization for the entire channel.

### Cited Findings
- YouTube's reused-content definition (as quoted): "videos that contain content from other sources repurposed **without original commentary or educational value**"; a plain background clip with no added commentary is the kind of thing that can be flagged — [TunePocket](https://www.tunepocket.com/reused-content-youtube-guide/).
- The overlay trend — creators "plac[ing] Subway Surfers gameplay footage as a background or overlay... to boost engagement on short-form platforms like TikTok and YouTube Shorts" — is "the pattern most likely to draw reused content flags unless the creator adds original commentary or a clear transformation" — [TunePocket](https://www.tunepocket.com/reused-content-youtube-guide/); [Quizzly overlay trend](https://quizzly.ai/play/subway-surfers-overlay-trend).
- The **inauthentic content** policy (renamed from "repetitious content" on **July 15, 2025**) targets mass-produced/repetitive material: content "made with a template with little to no variation across videos" or "easily replicable at scale"; **monetization may be removed from your entire channel** — [support.google.com/youtube (via search summary)](https://support.google.com/youtube/answer/1311392?hl=en); [PlagiarismToday](https://www.plagiarismtoday.com/2025/07/08/youtube-targets-inauthentic-content/); [NetInfluencer](https://www.netinfluencer.com/youtube-clarifies-july-15-policy-update-repetitious-content-rebranded-as-inauthentic-content/).
- Reused-content policy applies **channel-level**, not per-video; a channel-level notice does not identify a specific Short — [vidIQ reused content](https://vidiq.com/blog/post/youtube-reused-content-policy-guide/).
- Policy is **separate from copyright** — "not based on copyright, permission, or fair use"; applies even with the original creator's permission — [vidIQ reused content](https://vidiq.com/blog/post/youtube-reused-content-policy-guide/).
- Commentary, clips, compilations, and reactions **can still qualify** if they add original value; re-uploads with no added commentary/editing are the problem; YouTube says content is treated the same whether shot, animated, or AI-generated — [vidIQ reused content](https://vidiq.com/blog/post/youtube-reused-content-policy-guide/).
- Gameplay is monetizable "depending on the commercial use rights granted... by licenses of video game publishers" — [vidIQ gaming monetization (via yttalk)](https://vidiq.com/blog/post/get-full-youtube-monetization-gaming-videos/).

### Inferences
- **For a compliant automated pipeline:** each clip must be transformed/add original value — e.g. original commentary/voiceover, editorial selection + captions/analysis, or a distinctive edit — NOT raw gameplay as silent wallpaper under unrelated repurposed text/audio. Avoid templated, near-identical outputs at scale (that trips "inauthentic/mass-produced").
- The channel-wide scope makes this existential, not per-video: one batch of templated subway-surfers-style Shorts can demonetize the whole channel. Encode a "variation + added value" requirement and avoid mass-producing cookie-cutter clips.
- Note: policy affects **monetization eligibility**, not necessarily whether the videos get views/distribution — such content can still farm views while being non-monetizable, but also risks broader "spam/inauthentic" enforcement.

### Gaps
- Exact current (2026) policy wording could not be fetched from support.google.com directly (fetch blocked); wording above is via search summaries dated to the July 2025 update. Confirm against the live Help page.
- No source precisely quantifies how much transformation is "enough," or whether gameplay-background-under-original-voiceover is safe vs gameplay-background-under-reused-audio. YouTube publishes no exhaustive list.

---

## Copyright / Content ID behavior for licensed in-game music on Shorts

### Takeaway
A Content ID music claim on a Short typically does NOT block it — the common outcome is the **rights holder monetizes** (ad revenue diverted to them), or the creator can **mute/trim** the claimed audio. Blocking is less common for music. Using YouTube's Shorts audio library / Audio Library avoids claims. In-game licensed music (e.g. radio stations in GTA) can trigger Content ID and divert/limit revenue. Shorts-specific mute mechanics are less clearly documented than long-form.

### Cited Findings
- On a Content ID audio claim, the creator can **mute the claimed song or trim the segment**; if in YPP, you "may be able to **share revenue** with the music publisher." Rights holders set **monetize / track / block** policies, and **"Monetize" is the most common** policy on music claims — [support.google.com Content ID (via search summary)](https://support.google.com/youtube/answer/6013276).
- Rights holder "typically collects the ad revenue on a claimed Short," and **blocking is less common for music in Shorts** — [search summary of foximusic / dynamoi](https://www.foximusic.com/blog/youtube-shorts-copyright-music-library-guide/).
- Music from **YouTube's Shorts audio library** is licensed for Shorts and generally avoids claims (one vendor claims it still creates an undisputable claim — unconfirmed); **YouTube Audio Library royalty-free music won't get a Content ID claim** — [search summary](https://www.foximusic.com/blog/youtube-shorts-copyright-music-library-guide/).
- Rights holders can set **Shorts-specific licenses** — a track cleared for Shorts may not be cleared for long-form (and vice versa); rights holders can also manage Shorts specifically — [support.google.com Manage Shorts as a rights holder (via search)](https://support.google.com/youtube/answer/13053317).
- Revenue-impact estimates conflict: one says YouTube routes part of revenue to music rights holders first (cost shared across the creator pool); another claims a 20-40% per-view reduction (**no methodology — treat as unreliable**) — [search summary](https://www.foximusic.com/blog/youtube-shorts-copyright-music-library-guide/).
- Broader 2026 context: YouTube has at times **muted copyrighted music** on uploads amid licensing disputes — [HotHardware](https://hothardware.com/news/youtube-begins-muting-copyrighted-music-); [TechCrunch](https://techcrunch.com/?p=65555).

### Inferences
- For gameplay with in-game licensed music (GTA radio, sports-game soundtracks, etc.): expect a Content ID claim that **diverts monetization to the rights holder rather than blocking the video** in most cases — so the Short still gets views but the creator may earn little/nothing on it. Occasionally a track is set to **block** in some regions.
- Safest pipeline rule: where possible, **mute in-game licensed music and overlay YouTube-Shorts-audio-library / royalty-free tracks** (or keep raw SFX only) to avoid claims and revenue diversion. This also sidesteps region-blocks.
- Content ID music claims are a **revenue/availability** issue, generally NOT a copyright strike (strikes come from removal requests, not Content ID matches) — important distinction for channel safety.

### Gaps
- Could not fetch the live support.google.com Content ID / "Manage Shorts as a rights holder" pages to confirm exact 2026 Shorts mute/block/monetize mechanics (fetch blocked). Shorts-specific behavior is described as less documented than long-form.
- No reliable figure for the actual revenue share diverted on a claimed Short (the 20-40% figure is unsourced).

---

## Cross-cutting notes for the clipping pipeline (synthesis)

### Takeaway
The repeatable, ToS-safe formula that every strand of evidence supports.

### Inferences (encode as pipeline rules)
- **Length:** default ~12-30s; hard-cut the out-point within ~1s of the climax; never exceed ~45-60s without a reason.
- **Hook:** cold-open on/near peak action or lead with a payoff flash (reverse-order); first-frame burned-in text hook; no menus/loading/slow approach; subject centered in 9:16 (no lazy crops).
- **Retention/loop:** end right after the payoff so the moment reads instantly and invites re-watch/loop; optimize for completion % and re-watches (the signals all sources agree on).
- **Captions:** always burn in styled captions (word-level preferred), in the UI-safe zone (clear of bottom ~15-20% and the subject/face); align caption keywords with the title keyword.
- **Metadata:** keyword-forward title (game + moment); ≤5 hashtags total (≤15 hard cap or all are ignored); main keyword in first sentence of description; `#shorts` optional/low-value.
- **Cadence/timing:** 1-3/day, staggered across US ET peak windows (late-morning, lunch, evening — favor evening for gaming); consistency over exact timing.
- **Policy safety (critical):** every clip must add original value / variation — NO raw gameplay-as-silent-wallpaper under unrelated repurposed content, and NO templated near-identical mass output (channel-wide demonetization risk under reused + inauthentic/mass-produced policies).
- **Music safety:** prefer muting in-game licensed music and using Shorts-audio-library/royalty-free tracks to avoid Content ID revenue diversion and region blocks; understand Content ID claims divert revenue, they don't strike.

### Gaps (what the report writer should caveat)
- Primary YouTube Help/Creator Insider pages could not be fetched in-session (network-blocked); exact 2026 policy wording should be verified against live support.google.com pages.
- Nearly all engagement/retention percentages come from vendor/creator blogs, not YouTube or independent studies — directional only.
- No gameplay-specific, US-specific 2026 dataset on length, posting time, or retention was found; recommendations are synthesized from generalized guides + GTA-clip vendor guidance.
