# TikTok Short-Form Gameplay View Strategy (2026)

> Scope: what maximizes views + completion for short-form GAMEPLAY clips (GTA / open-world / action, plus gameplay-as-B-roll split-screen) on TikTok, for encoding into an automated clipping pipeline. US audience default. Authentic/organic only; ToS-compliant.
>
> **Source-quality caveat (applies throughout):** TikTok does not publish its ranking weights or completion benchmarks. Almost all quantitative figures below come from third-party marketing/analyst blogs or vendor tools, many of which repeat each other and sell the strategies they describe. Treat specific percentages as directional estimates, not platform-confirmed facts. Primary TikTok sources (developers.tiktok.com, business help center, buffer.com, ttcalculator.net) were **blocked by this session's network allowlist** and could not be fetched directly — see Gaps. Flagged inline where a claim is anecdotal/unverified.

---

## US availability / regulatory status of TikTok in 2026 (priority gate)

### Takeaway
TikTok is operating normally in the US in 2026 under a new US-controlled joint venture that resolved the divestiture/ban threat. The app is live and targetable; no ban or shutdown is in effect. The main forward risk is algorithm behavior changing as the recommendation engine is retrained for US users.

### Cited Findings
- A US joint venture (**TikTok USDS Joint Venture LLC**) was formally established **January 22, 2026**, serving a stated 200M+ US users and 7.5M businesses — [chinadaily.com.cn](https://mobile.chinadaily.com.cn/html5/2026-01/24/content_001_6973ec0aed50ccabe1520f2c.htm); [Variety](https://au.variety.com/2025/digital/global/tiktok-us-joint-venture-deal-close-date-oracle-silver-lake-31293/)
- Ownership: **Oracle, MGX (UAE), and Silver Lake each ~15%**; **ByteDance retains 19.9%**; other investors include Dell Family Office, Susquehanna affiliates, General Atlantic. Seven-member majority-American board incl. CEO Shou Chew; Adam Presser named JV CEO — [chinadaily.com.cn](https://mobile.chinadaily.com.cn/html5/2026-01/24/content_001_6973ec0aed50ccabe1520f2c.htm); [abc30/ABC News](https://abc30.com/post/tiktok-finalizes-deal-keep-operating-us/18451438/)
- The JV **retains decision-making over trust & safety and content moderation for US users**, and will **retrain/test/update the recommendation algorithm for US users, secured in Oracle Cloud** — [chinadaily.com.cn](https://mobile.chinadaily.com.cn/html5/2026-01/24/content_001_6973ec0aed50ccabe1520f2c.htm)
- JV also covers other ByteDance apps incl. **CapCut and Lemon8** (relevant: CapCut is a primary editing tool) — [BGR](https://www.bgr.com/2083488/tiktok-us-owned-changes-coming/)
- "American users won't notice major differences right away, though some content may start to look different over coming weeks/months as the algorithm is retrained and data is stored" — [chinadaily.com.cn](https://mobile.chinadaily.com.cn/html5/2026-01/24/content_001_6973ec0aed50ccabe1520f2c.htm)

### Inferences
- **Verdict: TikTok is a valid/priority target for a US-audience gameplay pipeline in 2026.** No ban or divestiture-driven shutdown is active; the app operates normally.
- The **algorithm is being retrained on US infrastructure during 2026**, so ranking behavior may shift. Build the pipeline to A/B test and re-measure its own completion/retention rather than hard-coding assumed weights.
- CapCut being inside the same US JV means the editing toolchain is unlikely to be disrupted alongside TikTok.

### Gaps
- No post-January 2026 operational reporting found confirming day-to-day stability (search results were all the January announcement). Monitor for later news.
- Unknown whether retraining changes creator-facing ranking signals materially.

---

## Optimal length in 2026 + completion-rate vs length (does >1 min gameplay work?)

### Takeaway
No official 2026 benchmark exists. Modeled/third-party data consistently shows completion rate falls sharply with length, so **short clips (~7–21s) maximize completion**, while **longer clips (>60s) compete on total watch time, not completion** and only work if retention holds. Practical default for gameplay: keep clips short unless the clip has a genuine payoff arc.

### Cited Findings
- Modeled completion-rate-by-length estimates (vendor calculator, **explicitly "representative benchmark estimates, not a proprietary study"**): ~**89% @ 7s, 73% @ 15s, 55% @ 30s, 38% @ 60s, 28% @ 90s** — [ttcalculator.net](https://ttcalculator.net/learn/completion-rate-by-video-length/) (host blocked for direct fetch; figures via search summary)
- Same source's completion bands: **80%+ excellent, 60–80% good, 40–60% average, <40% weak** — [ttcalculator.net](https://ttcalculator.net/data/engagement/completion-rate-by-video-length/)
- FanPageKarma analysis of **~32,000 TikToks**: **0–10s videos achieve the highest completion rate by far**; conclusion "there is no universally optimal video length" — [FanPageKarma](https://www.fanpagekarma.com/insights/optimal-tiktok-video-length/)
- One widely-cited framing puts the practical answer at **~41 seconds** for general content — [Opus.pro](https://www.opus.pro/blog/how-long-should-a-tiktok-be-2026)
- Length-vs-signal split (consistent across sources): **short videos compete mainly on completion rate; longer (1–3 min) videos compete on total watch time and are only rewarded if completion holds up** — [SocialBu](https://socialbu.com/blog/ideal-length-of-tiktok-videos); [stackinfluence](https://stackinfluence.com/blog/best-tiktok-video-lengths-for-creators-in-2026)
- Suggested content-type sweet spots (vendor opinion): entertainment/trends **15–30s**; talking-head/educational/opinion **30–90s** — [SocialBu](https://socialbu.com/blog/ideal-length-of-tiktok-videos)

### Inferences
- For raw gameplay highlight clips (GTA stunts, kills, chaos), **target ~7–21s** to ride the high-completion band; this is where the modeled data is strongest.
- For narrated/story-stacked gameplay (see two-video stack below), **30–60s is defensible** because the talking track supplies a retention arc, but only if the hook + payoff structure holds completion up — otherwise longer actively hurts distribution.
- **Do not assume longer = more reach.** Longer only helps when watch-time gains outweigh the completion drop; make clip length a tunable parameter driven by measured per-length completion, not a fixed rule.

### Gaps
- No TikTok-published completion numbers; all figures are modeled or third-party. The 89/73/55/38/28 curve should be treated as a hypothesis to validate against the pipeline's own analytics.
- No gameplay-specific completion dataset found.

---

## What the FYP algorithm ranks on in 2026

### Takeaway
Across sources the consistent core is **watch time + completion rate (watch-through rate) as the dominant signals**, well above any single like/comment, with shares/saves/comments and re-watches as strong secondary signals. Exact weights are **not published by TikTok**; any percentage weighting seen online is an estimate.

### Cited Findings
- Most sources rank **total watch time and completion (watch-through) rate as the top signals**, "far more important than any single like or comment" — [SocialChamp](https://www.socialchamp.com/blog/tiktok-algorithm/); [Metricool](https://metricool.com/de/der-tiktok-algorithmus/)
- One vendor claims **re-watch rate has become a top signal** (and may have displaced completion rate) — **unconfirmed by other sources** — [tlinky](https://tlinky.com/tiktok-algorithm/)
- Commonly cited distribution target: **~70% average completion** ranks far higher than ~25%; but sources also note **TikTok does not publish how much each signal counts**, so weighting percentages (e.g., 40–50%) are guesses — [socialchamp](https://www.socialchamp.com/blog/tiktok-algorithm/); [virlo.ai](https://virlo.ai/blog/how-the-tiktok-algorithm-works)
- Secondary signals consistently listed: **shares, saves, comments**; less consistently: TikTok Shop activity, search keywords, on-screen text — [Sendible](https://www.sendible.com/insights/how-does-tiktok-algorithm-work); [darkroomagency](https://www.darkroomagency.com/observatory/tiktok-algorithm-guide-2026)
- TikTok's documented logic is framed by multiple sources as **"watch-time percentage as primary ranking signal"** — [nestscale](https://nestscale.com/blog/tiktok-engagement-metrics.html)

### Inferences
- Pipeline optimization order of priority: **(1) completion / watch-through rate, (2) re-watch/loop-ability, (3) shares, (4) saves/comments.** Likes are near-noise.
- **Design clips to loop** (seamless end→start) to lift re-watches and completion simultaneously — cheap to do in editing, high expected value given the re-watch claims.
- Prompting **shares** (shareable moment / "send this to…") and **saves** (useful/"wait for it" payoff) matters more than chasing likes.

### Gaps
- No TikTok-confirmed ranking weights; re-watch-as-top-signal is single-source. Treat weight ordering as directional.

---

## Hooks / first-second retention + the "two-video stack" (gameplay-as-B-roll) format

### Takeaway
The opening ~1–3 seconds decide most retention; lead with the payoff and an immediate visual/text hook. The **two-video stack** (talking-head/story or captioned text on top, looping low-stakes gameplay — Subway Surfers, GTA driving, Minecraft parkour — on the bottom) is deliberate **"retention bait"**: the gameplay strip holds idle attention and suppresses the swipe-away while the top track delivers the narrative, boosting completion.

### Cited Findings
- Hook window disputed but short: variously **first 1–1.5s**, **first 2s ("decide over 70% of retention")**, or **3-second mark** as where platforms measure hook rate — [virlo.ai](https://virlo.ai/blog/why-the-first-few-seconds-matter); [dev.to/bulkdl](https://dev.to/bulkdl/hook-engineering-the-science-of-the-first-3-seconds-in-short-form-video-2026-2jp9)
- Tactics with broad agreement: **start with the payoff not the setup; use open-loop / curiosity-gap hooks; clear text overlay + physical motion in first 2s** (claimed up to **+50% lift in 3-second retention** vs static openings — *vendor claim*) — [nestscale](https://nestscale.com/blog/tiktok-engagement-metrics.html); [viralnation](https://www.viralnation.com/blog/the-formula-for-going-viral-4-things-every-tiktok-hit-has-in-common-and-none-of-them-is-luck)
- Two-video stack is described by a journalist/editor as **"retention bait"** — the gameplay strip exists because "TikTok incentivizes users to swipe away the second they get bored," so a second stimulus keeps them — [Kotaku](https://kotaku.com/subway-surfers-tiktok-corecore-video-collage-psychology-1850061976)
- Split-screen format "keeps attention by overstimulating" the viewer; gameplay footage argued to "increase auditory/visual attention" — [Trill Magazine](https://www.trillmag.com/life/social-media/is-the-tiktok-split-screen-destroying-modern-movie-watching/); [Studybreaks](https://studybreaks.com/tvfilm/subway-surfers-new-storytelling-method)
- Vendor claim: **split-screen videos average "72% higher watch time" vs single-frame** — **no methodology given, treat as unverified marketing** — [Ghostshorts](https://ghostshorts.com/blog/how-to-make-split-screen-videos-for-tiktok-2026)
- Subway Surfers' enduring dominance as the background game is tied directly to this TikTok trend (billions of downloads attributed partly to it) — [Bloomberg](https://www.bloomberg.com/news/newsletters/2023-02-03/tiktok-subway-surfers-family-guy-videos-are-terrible-for-attention-span)

### Inferences
- For a gameplay pipeline, two viable templates: **(A) pure gameplay highlight** (hook = the action spike in frame 1; cut straight to the most intense moment, no intro) and **(B) stacked B-roll** (narration/text top + looping calm gameplay bottom). GTA/open-world works for both; high-chaos clips suit (A), driving/cruising/parkour suits (B).
- **Put the most visually arresting gameplay frame first** (explosion, crash, kill, near-miss). Cold-open on the climax, then optionally rewind — standard "start with the payoff."
- Bottom-strip gameplay should be **low-cognitive-load and looping** so it never competes with the top track for comprehension (the vendor warning that high-energy bottom + calm top is "jarring" is unsourced but directionally plausible).
- Burn a **text hook overlay into the first frame** — serves both the retention lift and the keyword/SEO indexing (below).

### Gaps
- No peer-reviewed or platform data isolating the retention effect of the gameplay strip; the strongest evidence is qualitative/journalistic. The 72% and 50% figures are unverified vendor numbers.

---

## Captions / subtitles / on-screen text + TikTok's own tools

### Takeaway
On-screen captions are effectively mandatory (sound-off viewing + they feed search indexing). Use TikTok's built-in auto-captions as a baseline but review for errors; keep text in the safe zone (center-to-upper-third), sans-serif, short, and clear of the UI chrome.

### Cited Findings
- TikTok has a built-in **Auto Captions** feature that transcribes spoken audio into on-screen subtitles before publishing; control over fonts/animations/branding is **minimal** — [Opus.pro](https://www.opus.pro/blog/tiktok-caption-subtitle-best-practices); [Kapwing](https://www.kapwing.com/resources/a-complete-guide-to-tiktok-subtitles/)
- Auto-caption accuracy drops with accents, background noise, rapid speech, or multiple speakers — **review and correct** — [Notta](https://notta.ai/en/blog/how-to-add-captions-on-tiktok)
- **Placement:** keep captions out of the bottom (covered by description) and clear of username/sound credit/engagement buttons; safe zone ≈ center-middle to upper-middle third — [3Play Media](https://www.3playmedia.com/blog/best-practices-tiktok-accessibility/); [Kapwing](https://www.kapwing.com/resources/a-complete-guide-to-tiktok-subtitles/)
- **Style:** sans-serif (Helvetica/Arial/Montserrat) stays legible small; keep text concise, break long sentences — [Opus.pro](https://www.opus.pro/blog/tiktok-caption-subtitle-best-practices)
- **TikTok's search indexes caption text**, so keywords in subtitles improve discoverability — *secondary/lower-quality source, verify* — [Opus.pro](https://www.opus.pro/blog/tiktok-caption-subtitle-best-practices)

### Inferences
- Pipeline should **auto-generate + spell-check captions**, render them in a sans-serif font, and position them in the **upper-middle safe zone** (also avoids collision with a bottom gameplay strip in the two-video stack — the strip takes the bottom, captions take the top/middle).
- Seed target keywords into the burned-in text and the native caption field for dual SEO benefit.

### Gaps
- No TikTok-official doc fetched on caption safe-zone pixel bounds; placement advice is third-party. Confirm current UI-element safe margins empirically.

---

## Audio: trending sounds vs original audio + Commercial Music Library / in-game music conflict

### Takeaway
There's a real conflict for gameplay clips: trending-sound strategy maximizes reach but **trending/mainstream audio is largely unavailable to Business accounts** (which are restricted to the Commercial Music Library), and **in-game licensed music (e.g., GTA radio stations) risks copyright muting/takedowns**. Safest automated path: strip/duck in-game licensed music and use CML or cleared original audio; trending sounds only on non-Business accounts and even then with copyright risk.

### Cited Findings
- TikTok created a separate **Commercial Music Library (CML)** of pre-cleared tracks for verified businesses; Business accounts are **generally limited to CML** in the in-app editor (one vendor: **1M+ tracks**) — [Soundstripe](https://www.soundstripe.com/blogs/tiktok-music-licensing-rules); [stackinfluence](https://stackinfluence.com/blog/find-royalty-free-commercial-music-for-tiktok)
- **Business accounts cannot use mainstream trending sounds** — TikTok announced (May 2020) business accounts could no longer use trending sounds from the mainstream library; the standard library disappears when you switch to a business account — [Stinson](https://www.stinson.com/newsroom-publications-music-licensing-in-the-age-of-tiktok); [slip.stream](https://blog.slip.stream/commercial-music-2022-guide-for-tiktok-business-accounts-music-licenses-and-royalty-free-options/)
- **CML is not a total safe harbor:** Stinson notes CML use "should not" draw DMCA notices for most, but **"even this approach is not a total safe harbor,"** and some commercial users reported **copyright claims despite using CML** — [Stinson](https://www.stinson.com/newsroom-publications-music-licensing-in-the-age-of-tiktok)
- Independently-licensed music is allowed **only if** the license covers commercial use on TikTok **and** you complete TikTok's **Music Usage Confirmation** at upload — [Gelato](https://www.gelato.com/blog/tiktok-music-usage-confirmation); [Soundstripe](https://www.soundstripe.com/blogs/tiktok-music-licensing-rules)

### Inferences
- **In-game music is a liability.** GTA/open-world titles stream licensed commercial tracks (radio); keeping that audio invites copyright muting/takedown and complicates monetization. Pipeline should **mute or heavily duck the game-music bed** and overlay cleared audio (SFX + CML/original), preserving gameplay SFX where possible.
- **Account-type tradeoff:** Personal/Creator accounts can use trending sounds (reach upside) but still bear copyright risk on in-game audio; Business accounts lose trending sounds but gain CML clearance. For an automated pipeline, **Business account + CML (or original/cleared audio)** is the lower-risk default; add a trending-sound track only when legally cleared.
- Favor **original audio / gameplay SFX + a cleared music bed** so the clip isn't dependent on a trending-sound window and avoids the Business-account restriction entirely.

### Gaps
- No source found on gameplay/esports-specific audio handling. Whether muting the in-game radio fully avoids claims is unconfirmed. Current exact CML availability by account type should be re-checked in TikTok's Business Help Center (not fetchable this session).

---

## Hashtags & caption SEO / discovery (TikTok Search) in 2026

### Takeaway
Hashtags in 2026 function mainly as **search/categorization signals, not reach boosters**. Discovery is increasingly search-driven: captions, on-screen text, and spoken words (transcribed) are indexed, so keyword/SEO phrasing matters more than tag volume. Mix niche + content-type + 1–2 broad tags; skip generic #fyp/#viral.

### Cited Findings
- Hashtags still work but mainly as **search + categorization**, not reach boosters; TikTok shows both videos and hashtag pages for a search term — [SproutSocial](https://sproutsocial.com/insights/tiktok-hashtags/); [Metricool](https://metricool.com/tiktok-seo/)
- **Captions are among TikTok's strongest SEO signals**; use **long-tail phrasing** ("skincare tips for oily skin" > "skincare tips") — [NewTarget](https://www.newtarget.com/web-insights-blog/5-tiktok-seo-best-practices/); [Metricool](https://metricool.com/tiktok-seo/)
- Recommended mix: **niche-specific + content-type (#tutorial/#storytime) + 1–2 broad tags**, prioritizing relevance over size — [SproutSocial](https://sproutsocial.com/insights/tiktok-hashtags/)
- **Avoid generic #fyp / #viral** ("do nothing") — [appinstitute](https://appinstitute.com/tiktok-seo-for-mobile-apps/)
- Use **TikTok Creative Center** for trending tags by category/region; A/B test hashtag sets against Analytics — [SproutSocial](https://sproutsocial.com/insights/tiktok-hashtags/)

### Inferences
- For gameplay: lead with **game-title + mechanic keywords** in caption and burned-in text (e.g., "GTA 6 best heist moment," "open world free roam," "insane clutch"), not just #gaming. Long-tail game + moment phrasing captures search.
- Build a per-game **hashtag template**: 1–2 game-specific tags (#gta6, #minecraft), 1 content-type tag (#gamingclips/#gameplay), 1 broad relevant tag — relevance-weighted, auto-generated per clip, avoiding #fyp.
- Treat the **caption as primary SEO real estate**; the hashtag field is secondary.

### Gaps
- No TikTok-official doc on how search ranks hashtags vs captions vs transcription; ranking details are third-party.

---

## Posting cadence + best times (US audience) + frequency vs reach

### Takeaway
No single best time; studies disagree, but US **evenings (late afternoon–8pm) and midweek** cluster as strongest. **Consistency and frequency (≈1+/day) matter more than hitting an exact minute.** Test slots against own analytics.

### Cited Findings
- **Buffer** (2026, 1M+ TikTok videos): late-afternoon/evening; **Sunday 8pm highest**, then **Tuesday 4pm, Wednesday 2–5pm** — [Buffer](https://buffer.com/library/best-time-to-post-on-tiktok) (host blocked for direct fetch; via search summary)
- **Sprout Social** (2026, business accounts): **Tue–Thu 2–6pm local** — [sproutsocial via summary]; **Hootsuite** differs again — methodology differences explain the gaps (each uses its own customer sample) — [NealSchaffer](https://nealschaffer.com/best-time-to-post-on-tiktok/); [HopperHQ](https://www.hopperhq.com/blog/best-time-to-post-on-tiktok/)
- **Frequency:** posting consistently at good times beats posting once at the "perfect" time; **~1 post/day cited as a minimum**; frequency "moves the needle more visibly than shaving minutes off timing" — *vendor blogs* — [HopperHQ](https://www.hopperhq.com/blog/best-time-to-post-on-tiktok/); [iqfluence](https://iqfluence.io/public/blog/best-time-to-post-on-tiktok)

### Inferences
- Pipeline default US posting windows: **weekday afternoons ~2–6pm ET and evenings to ~8–9pm ET, plus Sunday evening**; schedule ≥1/day, ideally 1–3/day for a clipping volume account.
- **Spread posts** across windows rather than clustering; let per-slot analytics reallocate over 30–60 days. Over-posting low-quality clips risks the unoriginal-content flag (below), so cadence must be paired with per-clip originality.

### Gaps
- No primary cadence guidance from Buffer/Hootsuite found; "1/day minimum" is vendor opinion. Times are sample-dependent and should be validated per account.

---

## Content rules relevant to us: reposted/low-effort, watermarks, automated posting via API

### Takeaway
Two hard constraints for an automated clipping pipeline: (1) **TikTok suppresses unoriginal/reused content and content carrying another app's watermark** (enforcement tightened Sept 15, 2025) — so clips need genuine creative transformation and must not carry other-platform watermarks; (2) **automated posting via the official Content Posting API is permitted but gated** — apps must pass audit, and **unaudited clients can only post private videos**, with spam limits on rapid posting. Scheduling your own content via the official API is allowed; bot likes/follows/DMs are not.

### Cited Findings
**Unoriginal content / watermarks:**
- TikTok Community Guidelines (quoted): content is **ineligible for the For You feed** if it's **reused/unoriginal without anything new**, example given: **"clips that show someone else's watermark or logo"** — [BigSeller quoting TikTok CG](https://www.bigseller.pro/blog/articleDetails/3778/tiktok-unoriginal-content.htm)
- Enforcement **stepped up from 15 September 2025**; flagged content can **lose recommendations, search ranking, or organic reach** — [BigSeller](https://www.bigseller.pro/blog/articleDetails/3778/tiktok-unoriginal-content.htm)
- A logo/watermark added to copied content **does not make it original**; flag triggers on reused clips, other-app watermarks, or lack of original creative input — [influenceflow](https://influenceflow.io/resources/why-is-my-tiktok-unoriginal-content-flag-appearing-and-how-to-fix-it/); [openclip](https://openclip.app/guides/tiktok-slideshow-unoriginal-content-flag)
- Specific reach-reduction figures (e.g., "40% for visible competitor branding") come from unnamed analysts — **unverified** — [budindia](https://www.budindia.com/blog/why-reposted-content-is-killing-your-social-media-reach-in-2026.php)

**Content Posting API (all via vendor blogs; developers.tiktok.com blocked this session):**
- Two modes: **Direct Post** (publishes straight to account) and **Upload/inbox** (sends to creator's inbox as a draft to post manually). Automation needs **Direct Post** — [vorplabs](https://vorplabs.com/agent-tools/tiktok-content-posting-api); [postproxy](https://postproxy.dev/blog/how-to-post-to-tiktok-via-api/)
- **Unaudited apps: posts restricted to private viewing** until the app passes TikTok's audit/review — [vorplabs](https://vorplabs.com/agent-tools/tiktok-content-posting-api)
- Audit timeline cited as **2–6 weeks** — **unverified** — [rapidevelopers](https://www.rapidevelopers.com/md/api-automations/how-to-automate-tiktok-video-posting-using-the-api)
- **Rate limits depend on approval level**; sandbox apps lower; one vendor cites **~15 posts/day/account** — **unverified** — [socialrails](https://socialrails.com/documentation/tiktok-api-integration)
- **Rapid automated posting can trigger spam detection/restrictions** — [postpeer](https://www.postpeer.dev/errors/tiktok)
- **Scheduling your own content via official API = allowed; automated DMs / comment bots = prohibited** — [brandghost](https://blog.brandghost.ai/posts/tiktok-automation-scheduling/)

### Inferences
- **Each published clip must be genuinely transformed** (new cut, captions/overlays, reframe, commentary, audio change) — raw re-uploads or clips bearing another creator's/platform's watermark will be FYP-ineligible. The pipeline must **detect and crop/avoid foreign watermarks** and ensure every output has original editorial input.
- **Do NOT upload clips carrying a TikTok/CapCut/other-app watermark** from a prior export; render clean.
- To post automatically at reach-visible (public) scale, the app **must pass TikTok's Content Posting API audit** — budget 2–6 weeks (unverified) and build for Direct Post. Until audited, outputs are private-only (useless for views).
- **Throttle posting** to avoid spam flags (keep well under any ~15/day figure; space posts out); this reinforces the cadence section's "spread, don't cluster."
- Stay within official API only — no engagement bots. Authentic engagement constraint satisfied.

### Gaps
- All Content Posting API specifics are from vendor blogs; **developers.tiktok.com was blocked and must be verified directly** for current audit requirements, exact rate limits, Direct Post eligibility, and watermark/branding rules. The ~15 posts/day and 2–6 week audit figures are unverified.
- Unclear whether TikTok's own "AI-generated content" and automation disclosure rules impose added labeling requirements on API-posted clips — not covered by sources found.

---

## Blocked sources (could not fetch directly this session — flagged for the writer)
These hosts failed DNS/network allowlist and were only available via WebSearch summaries; verify directly if possible:
- **developers.tiktok.com** (Content Posting API — authoritative rules/limits/audit)
- **buffer.com** (best-time study)
- **ttcalculator.net** (completion-by-length data)
- **getlate.dev** (API posting guide)
