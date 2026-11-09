# Posting Cadence, Timing, Cross-Posting & ToS-Safe Automated Publishing (YouTube Shorts / Instagram Reels / TikTok, 2026)

> Scope: US audience default, short-form gameplay content, automated pipeline using **official publishing APIs only**. Authentic engagement only — no bots, no fake views, no engagement pods.
>
> **Source-quality warning for the report-writer:** The timing/frequency/shadowban space is dominated by vendor blogs (schedulers, "warm-up" sellers, clip tools) with a commercial stake. Below, confirmed platform statements are flagged **[PLATFORM]**, data studies **[STUDY]**, and creator folklore / vendor marketing **[FOLKLORE]**. Treat specific hours, percentages, and "banned hashtag" lists as heuristics, not rules.
>
> **Network caveat (collection limitation):** In this session, several primary hosts failed DNS resolution and could NOT be fetched directly: `buffer.com`, `sproutsocial.com`, `metricool.com` (reachable only via press-release mirrors/coverage), `www.socialmediatoday.com`, `support.google.com` (YouTube Help), and `developers.tiktok.com`. Findings sourced to those publishers below rely on search-engine summaries of their pages and secondary coverage, not full-text fetches. They should be re-verified against the live primary pages before encoding as hard defaults. Flagged inline as **[UNVERIFIED-PRIMARY]** where relevant.

---

## Q1. Best posting times (by platform, US, day/hour) — and does timing matter vs watch-time?

### Takeaway
Timing is a **weak, secondary signal** for short-form in 2026 — all three platforms distribute on a delay via personalized recommendation feeds, not a chronological follower feed, so the publish hour mostly affects the *first* small test audience, not ceiling reach. Watch-time / retention (especially "viewed vs swiped") is the dominant ranking signal. Benchmark "best times" disagree across studies; use them only as a tie-breaker and override with the account's own analytics once data exists.

### Cited Findings
- Sprout Social (≈2B engagements, 307k profiles): overall best windows are **Tue–Wed, 11 a.m.–6 p.m. local**, with **Sunday weakest** — [Sprout Social](https://sproutsocial.com/insights/best-times-to-post-on-social-media/) **[UNVERIFIED-PRIMARY]**
- Buffer 2026 (millions of posts) says there is **no universal best time**; its platform-specific picks were **Instagram ~3 p.m. Friday, TikTok ~8 p.m. Sunday** — [Buffer](https://buffer.com/best-time-to-post) **[UNVERIFIED-PRIMARY]**
- Vendor-blog consensus windows (US Eastern, treat as rough): **TikTok** weekday evenings ~7–9 p.m., plus Tue/Thu/Fri 9 a.m.–12 p.m. & 5–7 p.m.; **Reels** ~Tue 4 p.m., 11 a.m.–1 p.m. & 7–9 p.m.; **Shorts** Thu–Sat 6–9 p.m. (sources conflict most on Shorts) — [ClipSpeed](https://clipspeed.ai/blog/best-posting-times-social-media.html); [Socialync](https://www.socialync.io/blog/best-time-to-post-tiktok-instagram-youtube) **[FOLKLORE]**
- Distribution-window differences: **TikTok** most distribution in first ~48h; **YouTube Shorts** have a long tail (views accrue for weeks); **Instagram** personalizes home feed so Reels can surface hours/days later — meaning exact publish hour matters least on Shorts/Reels — [Socialync](https://www.socialync.io/blog/best-time-to-post-tiktok-instagram-youtube) **[FOLKLORE]**
- Retention is the core signal: "content that holds attention gets shown to more people… high retention [is] a quality signal" across all three platforms — [Shortimize](https://www.shortimize.com/blog/compare-watch-time-tiktok-vs-reels-vs-shorts) **[FOLKLORE citing platform behavior]**
- For Shorts the key metric is **viewed-vs-swiped**; YouTube's own guidance is that **relative watch time matters more for short videos**, absolute watch time more for long videos — [Shortimize](https://www.shortimize.com/blog/compare-watch-time-tiktok-vs-reels-vs-shorts) **[FOLKLORE citing [PLATFORM]]**
- One analysis argues short-form algos now prioritize **format, sound, hook, retention over publish hour** — [Conbersa](https://www.conbersa.ai/blog/why-posting-time-matters-less-than-content-format) **[FOLKLORE]**

### Inferences
- For a pipeline, **do not over-engineer timing.** Pick one sensible default slot per platform (e.g., weekday late-afternoon/evening US Eastern) and keep it consistent; spend optimization effort on hook/retention and thumbnail/first-frame instead.
- Because DST shifts US clocks (flagged for March 2026), store schedule times in a timezone-aware form (America/New_York) rather than fixed UTC offsets.
- Staggering publish times across platforms is cheap and harmless; it is NOT primarily a timing-optimization move (see Q3 — it's about watermark/first-mover and spreading API calls).

### Gaps
- Buffer/Sprout exact 2026 per-platform tables couldn't be fetched (hosts blocked); numbers above are search summaries. Re-verify before hard-coding.
- No platform has published an official "best time" — all timing data is third-party.

---

## Q2. Optimal posting frequency & diminishing-returns / over-posting evidence

### Takeaway
Rough safe defaults: **~1 post/day per platform (3–5/week minimum, up to ~1–2/day)** is the widely-cited sweet spot; consistency beats volume. The strongest *data* finding is a YouTube **over-posting ceiling**: Metricool's 2026 study found channels posting **≥35 Shorts/month** saw long-form performance collapse back to the level of channels posting *no* Shorts — evidence of real diminishing/negative returns at high volume on YouTube specifically.

### Cited Findings
- **Metricool 2026 YouTube Study** (799,718 videos, 71,177 accounts; Feb 2025–Feb 2026) **[STUDY]**:
  - Channels posting **≥35 Shorts/month** → long-form views fall to roughly the "zero Shorts" level — [Metricool press release](https://metricool.com/press-release-youtube-study-2026/); [Tubefilter](https://www.tubefilter.com/2026/08/03/youtube-shorts-long-form-study-metricool/)
  - Channels with **no Shorts** averaged **4,364 views/long-form video**; **~5 Shorts/month** peaked at **8,789**; global avg **5,985** — [Metricool](https://metricool.com/youtube-trends/)
  - **No clear ceiling for Shorts' own view totals** — monthly Short views keep rising with volume (more discovery surface) — [NetInfluencer](https://www.netinfluencer.com/youtube-views-are-rising-but-watch-time-and-ad-revenue-are-falling-study-finds/)
  - Best long-form cadence: **2–4 uploads/week** — [NetInfluencer](https://www.netinfluencer.com/youtube-views-are-rising-but-watch-time-and-ad-revenue-are-falling-study-finds/)
  - Context: views up (long-form +76%, Shorts +127%) but **watch-time per Short falling** for every account size; engagement down 45% — "everyone is posting more" — [Metricool newsletter](https://newsletter.metricool.com/p/still-trying-to-figure-out-youtube)
- Vendor-blog frequency consensus **[FOLKLORE]**: TikTok 3–5×/week (some say 1–3/day), Reels 3–5/week, Shorts 3–5/week; aggressive planners push 7–14/week — [Outfy](https://www.outfy.com/blog/how-often-should-you-post-on-social-media/); [ClipSpeed](https://www.clipspeed.ai/blog/content-calendar-short-form-creators.html)
- TikTok's own help/creator guidance is commonly cited as **1–4 posts/day** as the sustainable range; sudden spikes in posting flagged as potential spam — [Socialcrawl](https://www.socialcrawl.dev/blog/how-often-should-you-post-on-tiktok.md) **[FOLKLORE citing [PLATFORM]]**
- Repeated theme: "posting daily increases reach but risks quality drops; consistency matters more than volume" — multiple vendor guides **[FOLKLORE]**

### Inferences
- **Encode an over-posting guard, not just a floor.** For a YouTube-Shorts-heavy gameplay pipeline, cap Shorts well under 35/month if the same channel also hosts (or may host) long-form — i.e. **≤ ~1 Short/day (~30/month)** per channel is the data-backed safe ceiling; a Shorts-only channel can go higher but watch per-Short dilution.
- The Metricool ceiling is a **correlation** (methodology for the 35 cutoff not published); treat as a caution threshold, not a hard law.
- TikTok/Reels have no comparable published over-posting study — default to ~1/day/platform and scale up only if retention holds.

### Gaps
- No published Shorts-specific frequency *study* beyond Metricool's cross-sectional view counts; no causal proof the 35-Shorts drop is caused by volume vs. correlated low quality.
- No TikTok/Instagram equivalent of the Metricool over-posting finding.

---

## Q3. Cross-posting one identical clip to all three — does it hurt reach? Watermarks. Clean exports.

### Takeaway
Posting the **same video file across different platforms** (TikTok + Reels + Shorts) is **not** penalized by any confirmed platform policy — the "duplicate content" penalty is **within-platform** (same/near-identical clip reposted on one platform or across multiple accounts you control). The one **confirmed** cross-platform suppressor is **visible competitor watermarks/logos** — Instagram explicitly down-ranks Reels carrying other apps' logos (notably the TikTok logo). Fix = always publish from a clean master export, never the TikTok "Save video" download.

### Cited Findings
- **[PLATFORM]** Instagram head **Adam Mosseri**: Instagram tries **not to recommend Reels containing other apps' logos**; a creator's **own** logo is fine — [Social Media Today](https://www.socialmediatoday.com/news/instagram-clarifies-including-your-own-logo-on-a-reel-is-ok/730852/) **[UNVERIFIED-PRIMARY — host blocked, via search summary]**
- Instagram has applied a **discovery penalty for TikTok-watermarked Reels since 2021**: reposts still reach *followers* but are kept out of Explore/recommendations — [Social Media Today](https://www.socialmediatoday.com/news/instagram-clarifies-including-your-own-logo-on-a-reel-is-ok/730852/); [Tubefilter](https://www.tubefilter.com/) **[UNVERIFIED-PRIMARY]**
- Cross-posting (different platforms) is **not** algorithmically penalized per several analyses; duplicate penalty is within-platform — [Post-Bridge](https://www.post-bridge.com/blog/does-cross-posting-hurt-engagement); [Socialync](https://www.socialync.io/blog/avoid-content-duplication-penalties-cross-posting-2026) **[FOLKLORE]**
- **Within-platform duplication IS the clearly-penalized case**: same clip to multiple accounts you control on one platform → reduced reach; TikTok community guidelines discourage identical content across accounts — [Post-Bridge](https://www.post-bridge.com/blog/does-cross-posting-hurt-engagement) **[FOLKLORE citing [PLATFORM] guidelines]**
- Watermark mechanics: TikTok stamps logo + username only when **TikTok renders the download** (in-app "Save video"). **Exporting a master from an external editor and uploading separately avoids the stamp.** YouTube Shorts and Instagram do **not** add a watermark to the downloadable file in the same way — [SocialK.it](https://socialk.it/en/blog/tiktok-watermark-reach-guide); [PostEverywhere](https://posteverywhere.ai/blog/how-to-remove-tiktok-watermark-before-posting) **[FOLKLORE]**
- Claim that watermarked Reels lose "~90% of reach" vs clean — vendor marketing, **no methodology, treat as unverified** — [SocialK.it](https://socialk.it/en/blog/tiktok-watermark-reach-guide) **[FOLKLORE]**
- Reddit anecdote: identical cross-post underperformed on TikTok (23% full-video-watched, 7.8s avg, 1,400 views) — single anecdote, no established cause — [Reddit snapshot](https://reddit.sentinel-team.org/posts/1pj4w3n/snapshots/2025-12-11T00%3A00%3A45.448964Z) **[FOLKLORE/anecdotal]**

### Inferences / Pipeline rules
- **Render ONE clean master** (no platform UI, no TikTok/CapCut logo, no username sticker) and upload that same file to all three via API. This is safe and standard.
- **CapCut watermark**: CapCut's default export and templates can add a logo/end-card; disable it or export logo-free. Same risk class as the TikTok logo for Reels recommendation. **[FOLKLORE — not platform-confirmed for CapCut specifically, but same mechanism as confirmed TikTok-logo case]**
- "Export platform-clean versions" ≈ per-platform **aspect/safe-zone** tweak (keep action out of the right-edge UI rail and bottom caption zone), not a content difference needed for dedup. A single 9:16 clean master works; per-platform cropping is a polish, not a reach requirement.
- The only *forced* difference across platforms should be **caption/description + hashtags** (see Q5 — identical captions are a mild duplicate signal), not the video bytes.

### Gaps
- No platform has quantified the watermark penalty; the "90%" and "Shorts demotes watermarks" claims are vendor-only and unconfirmed by YouTube.
- Whether YouTube Shorts actively *detects* a TikTok watermark (vs just not caring) is unconfirmed — no YouTube primary statement found.

---

## Q4. Does automated/scheduled posting via OFFICIAL APIs reduce reach vs manual?

### Takeaway
Evidence says **no** — posting through official publishing APIs/schedulers does **not** inherently suppress reach. Instagram leadership has publicly stated scheduled posts enter ranking identically to manual ones. The myth persists from older tests on deprecated tools and from confusing *correlation* (scheduled posts often lack native features / optimal timing) with *causation*. Risk comes from **unofficial/unsanctioned** automation, not the sanctioned APIs.

### Cited Findings
- **[PLATFORM]** Mosseri (via Planoly) and an Aug 2026 Q&A (via Kontentino): **scheduled posts do not affect reach**; scheduled & manual Reels "enter ranking the same way, no difference in reach" — [Planoly](https://www.planoly.com/blog/does-scheduling-your-posts-affect-your-post-reach.md); [Kontentino](https://www.kontentino.com/q-and-a/does-scheduling-instagram-posts-affect-reach/) **[UNVERIFIED-PRIMARY — host summaries]**
- Instagram Graph API docs describe third-party publishing with **no mention of any algorithmic penalty** — [Hootsuite](https://blog.hootsuite.com/experiment-third-party-scheduling-instagram/)
- Hootsuite experiment: scheduled posts had **higher** engagement (8.19% vs 6.44% native) and higher reach — small sample — [Hootsuite](https://blog.hootsuite.com/experiment-third-party-scheduling-instagram/) **[STUDY, small-n]**
- Counter-data: a 2019 Agorapulse test (Facebook Creator Studio) found slightly *lower* reach for scheduled on some accounts — older, different tool — [Agorapulse](https://agorapulse.com/social-media-lab/instagram-3rd-party-tools) **[STUDY, dated]**
- Metricool's methodological point: a scheduled post doing worse **doesn't mean the tool caused it** — usually timing/content/missing native features; also verify queued posts actually published (API limits / expired tokens silently drop them) — [Metricool](https://metricool.com/does-scheduling-social-media-posts-affect-reach/) **[UNVERIFIED-PRIMARY]**

### Inferences
- **Using the three official APIs is reach-neutral.** The pipeline's reach risk is content quality + watermark + warm-up/velocity, not the fact of automation.
- Practical automation failure mode to guard against: **silent publish failures** (expired OAuth, rate-limit 429, TikTok unaudited→private). Build verification that each post actually went public, plus token-refresh and retry/backoff.
- Prefer native platform features when the API exposes them (captions, cover frame, hashtags) so scheduled posts aren't disadvantaged by missing metadata.

### Gaps
- No controlled 2026 study isolating API-vs-manual on TikTok or YouTube Shorts specifically; Instagram is best-documented.

---

## Q5. Shadowban / reach-suppression causes in 2026 and how to avoid

### Takeaway
"Shadowban" is contested (platforms deny a secret toggle; much reported suppression is normal distribution variance). But there are **recurring, avoidable triggers**: visible competitor watermarks, banned/spam-associated hashtags, posting-velocity spikes, reported/guideline-violating content, near-duplicate content on one platform, and non-organic engagement spikes (bots/pods). Avoid all of these by design.

### Cited Findings
- Commonly cited suppression triggers (vendor consensus) **[FOLKLORE]**:
  - **Duplicate/near-duplicate content** repeated across pages/accounts on the same platform — [Kontentino](https://www.kontentino.com/blog/shadow-ban-what-it-is-and-how-to-prevent-fix-it/)
  - **Banned/restricted hashtags** (spam/policy-associated) reduce reach even on clean content; example list floated (#followforfollow, #snapchat, etc.) **unverified against Instagram** — [Ayrshare](https://www.ayrshare.com/blog/avoid-using-these-instagram-banned-hashtags.md)
  - **Posting too fast / spikes**: TikTok "flags accounts that show sudden spikes in posting activity as potentially spam"; keep ~1–4/day sustainable — [Stackinfluence](https://stackinfluence.com/blog/shadow-banning-on-tiktok-and-instagram); [Socialcrawl](https://www.socialcrawl.dev/blog/how-often-should-you-post-on-tiktok.md)
  - **Non-organic engagement** (bought/bot/pod activity creating unnatural spikes) — [Stackinfluence](https://stackinfluence.com/blog/shadow-banning-on-tiktok-and-instagram)
  - **Mass deletions** of posts can itself trip spam flags — [SSemble](https://www.ssemble.com/blog/account-warmup-guide-2026)
- **[PLATFORM]-adjacent**: Instagram officially *denies* a "shadowban" exists but acknowledges reach can be limited by guideline violations, spammy behavior, broken hashtags, or reported content — [SocialChamp](https://www.socialchamp.com/blog/instagram-shadowban/) **[FOLKLORE citing [PLATFORM]]**
- Contrarian/epistemic check: "shadowban as secret reach penalty is backed by no platform primary source; most drops are ordinary distribution variance" — [Post-Bridge](https://www.post-bridge.com/blog/does-cross-posting-hurt-engagement); [blckalpaca](https://blckalpaca.at/en/knowledge-base/social-media/social-media-algorithms-distribution/what-is-a-shadowban-myths-and-evidence) **[FOLKLORE, skeptical]**
- **Identical captions across platforms** are cited as a mild duplicate signal; vary caption/hashtags per platform — implied by within-platform duplicate guidance — [Socialync](https://www.socialync.io/blog/avoid-content-duplication-penalties-cross-posting-2026) **[FOLKLORE]**
- TikTok 3rd-party "spam error" when posting via tools is a known failure — tie to velocity + unaudited-client state — [Postly](https://blog.postly.ai/how-to-fix-tiktoks-spam-error-when-posting-via-postly-or-other-third-party-tools) **[FOLKLORE]**

### Inferences / Pipeline guardrails
- **Hashtag hygiene:** maintain a periodically-reviewed denylist; avoid generic spam-magnet tags; keep hashtag counts modest and topical (gameplay/game-title tags) rather than reach-bait.
- **Velocity governor:** cap posts/account/day (see Q8), enforce minimum spacing between posts, never burst-publish a backlog.
- **Per-platform caption variation:** auto-generate platform-specific captions/hashtags rather than echoing one string to all three.
- **No bots/pods** (already a hard constraint) — these are among the clearest real suppression/ban triggers.
- Treat sudden reach drops as **variance first**; don't react by deleting content (deletion itself is a flag).

### Gaps
- No authoritative 2026 "banned hashtag" list from Instagram/TikTok; lists are vendor-maintained and drift.
- Exact velocity thresholds that trip spam detection are undisclosed by all platforms.

---

## Q6. Account warm-up — how a brand-new posting account should ramp

### Takeaway
Consensus (vendor, not platform-confirmed): a **new account should not post heavily on day one**; do a short period of **human-like passive activity**, then ramp posting **gradually from ~1/day**. Instagram is treated as strictest. All numbers are heuristics — no official platform warm-up guidance exists.

### Cited Findings (all **[FOLKLORE]** — vendor blogs, commercial stake)
- Warm-up length estimates vary: **3 days minimum**, **7 days**, up to **14–21 days (TikTok)** — [SuperScale](https://superscale.ai/learn/the-right-way-to-warm-up-new-tiktok-instagram-accounts/); [Post-Bridge](https://post-bridge.com/growth-guide/account-warmup); [InfluencerMarketingHub](https://influencermarketinghub.com/tiktok-)
- Instagram stricter: new accounts that "post on day one get suppressed for weeks, sometimes permanently" (claim) — [SSemble](https://www.ssemble.com/blog/account-warmup-guide-2026)
- During warm-up: **passive, human-paced use** — watch/scroll/like/follow target-niche content, **zero promotion/posting** — [SuperScale](https://superscale.ai/learn/the-right-way-to-warm-up-new-tiktok-instagram-accounts/)
- Ramp: **start ~1 post/day, increase gradually**; keep spacing (Instagram ~3h+, TikTok ~2h+ between posts) — [picmim](https://blog.picmim.com/blog/warm-up-new-social-media-account-30-day-strategy); [airbridge](https://www.airbridge.io/en/resources/handbook/ugc/06-account-setup-and-posting-rhythm)
- **Post manually for ~1 week (or until views climb) before enabling schedulers/automation** — [SSemble](https://help.ssemble.com/docs/publish-clips/social-media-account-warm-up)
- Other flags during warm-up: inconsistent device/network/IP, TikTok/3rd-party watermarks, mass deletions — [SSemble](https://www.ssemble.com/blog/account-warmup-guide-2026)

### Inferences / Pipeline ramp schedule (conservative default)
- **Week 0 (pre-launch):** complete profile (pic, bio, links); do manual human-like browsing/engagement; **no automated posting.**
- **Week 1:** manual or 1 post/day/platform max; verify posts publish & reach followers; observe for suppression before scaling.
- **Weeks 2–3:** ramp to the normal cap (~1/day, up to 2/day only if retention healthy).
- **Stable state:** apply Q8 caps.
- Keep **consistent device/IP/OAuth identity** per account; don't rotate.
- Enable the scheduler/API posting only **after** the manual warm-up week.

### Gaps
- Zero official platform documentation on warm-up; every figure is vendor heuristic. The "permanent suppression on day-one posting" claim is unverified and likely overstated.

---

## Q7. Confidence / quality gating — does posting only high-quality clips affect channel-level reach?

### Takeaway
YouTube's **official** position: recommendations lean on **video- and audience-level signals**, and the platform does **not** judge a whole channel off a few videos — so one weak Short won't tank a channel. BUT a **sustained pattern** of weak videos does matter (viewers stop watching when recommended), and Metricool's data shows high-volume low-quality Shorts correlate with worse long-form outcomes. Net: **quality-gating (confidence threshold) to suppress weak clips is well-justified** on YouTube; TikTok/Reels evidence is weaker but directionally the same (retention-driven).

### Cited Findings
- **[PLATFORM]** YouTube Help: "Our systems rely more on video and audience-level signals… A decline in overall channel views [comes] when viewers stop watching most of your videos when they're recommended." — [YouTube Help](https://support.google.com/youtube/answer/141805) **[UNVERIFIED-PRIMARY — host blocked; via search summary + SEJ]**
- **[PLATFORM]** "YouTube doesn't make assessments about a channel as a whole based on the performance of a few videos." — via [Search Engine Journal](https://www.searchenginejournal.com/youtube-recommendation-algorithm/387030/)
- Individual videos judged more on **video-level than channel-level** signals (vidIQ summary of YT guidance) — [vidIQ/rosetta](https://rosetta.to/u/vidiq/youtube-algorithm-2021-facts-confirmed-and-myths-debunked) **[FOLKLORE citing [PLATFORM]]**
- **Pattern risk**: commentators describe a "death spiral" from multiple poor videos — **anecdotal, not official** — [overseeros](https://www.overseeros.com/blog/does-one-bad-youtube-video-hurt-your-channel) **[FOLKLORE]**
- **[STUDY]** Metricool: ≥35 Shorts/mo → long-form reverts to "no Shorts" level; ~5 Shorts/mo was the *peak* long-form view bucket — i.e. **a few good Shorts help, flooding hurts** — [Metricool](https://metricool.com/youtube-trends/)
- Shorts vs long-form "operate independently" officially, but creator anecdotes report spillover — [tabzgm](https://tabzgm.blogspot.com/2025/12/do-poor-performing-shorts-hurt-channels.html) **[FOLKLORE]**

### Inferences
- **Encode a confidence/quality gate**: only publish clips above a retention/quality score threshold rather than maximizing raw volume. This aligns with YouTube's "~5 good Shorts/mo beat 35 mediocre" data and with retention being the universal ranking signal.
- Volume ≠ growth once quality drops; the pipeline's clip-selection confidence score should be the throttle, not a fixed daily quota.
- One weak clip is low-risk (video-level judging) — so the gate can be moderately permissive — but **avoid sustained low-quality streaks**.

### Gaps
- No TikTok/Instagram official statement on channel-wide quality carryover; inference from retention-centrality only.
- Metricool link is correlational; can't prove low-quality Shorts *cause* long-form decline.

---

## Q8. Practical daily-limit recommendations (within platform norms AND API quotas)

### Takeaway
Keep well under both the behavioral spam thresholds and the API quotas. Safe pipeline defaults: **~1 post/day/platform/account (hard cap ~2/day), minimum 2–3h spacing, ≤~30 Shorts/month/channel.** API quotas are far above these behavioral limits except TikTok's unaudited-client trap.

### Cited Findings — API quotas
- **TikTok Content Posting API [PLATFORM]**: **Unaudited clients** → up to **5 users** can post per 24h **and all posts forced to PRIVATE** until the app passes a ToS audit. Per-app creator cap is set from the audit form's usage estimate. Errors: `reached_active_user_cap`, and `429 rate_limit_exceeded`. — [TikTok developer docs via search summary](https://developers.tiktok.com/doc/content-posting-api-reference-direct-post) **[UNVERIFIED-PRIMARY — host blocked]**
  - Third-party (conflicting, unverified): ~**6 requests/min/user**, daily cap **~15–25 videos/account**; MP4 ≤1GB — [getphyllo](https://www.getphyllo.com/post/tiktok-api-rate-limits-in-2026-quotas-errors-workarounds); [adaptlypost](https://adaptlypost.com/blog/tiktok-post-limit-per-day) **[FOLKLORE, conflicting]**
- **Instagram Content Publishing API (Graph API) [PLATFORM]**: current docs cap **50 API-published posts / rolling 24h** per IG account (older docs & many tools still cite **25**); **carousels count as 1**. Query live limit via `GET /{ig-user-id}/content_publishing_limit`. — [Meta docs](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/content-publishing); [Ayrshare](https://www.ayrshare.com/solutions/instagram-graph-api-error-9-the-25-post-daily-limit-how-to-fix-it/) (Error 9 = daily limit)
- **YouTube Data API v3 [PLATFORM]**: default project quota **10,000 units/day**; a **video insert costs ~1,600 units** → **~6 uploads/day per project** before needing a quota increase. (Standard uploads to your own channel need no app review.) — characterized by [getphyllo](https://www.getphyllo.com/post/using-apis-to-automate-content-upload-on-youtube-instagram-tiktok) **[FOLKLORE for the 1,600/6-per-day figure; the 10k default is [PLATFORM] standard — verify current cost table]**

### Cited Findings — behavioral norms
- Sustainable behavioral range ~**1–4 posts/day** (TikTok); spikes flagged as spam — [Socialcrawl](https://www.socialcrawl.dev/blog/how-often-should-you-post-on-tiktok.md) **[FOLKLORE]**
- Minimum spacing between posts: Instagram **~3h+**, TikTok **~2h+** — [airbridge](https://www.airbridge.io/en/resources/handbook/ugc/06-account-setup-and-posting-rhythm) **[FOLKLORE]**
- YouTube over-posting ceiling **≤35 Shorts/mo** (Q2) — [Metricool](https://metricool.com/youtube-trends/) **[STUDY]**

### Inferences / Recommended encoded defaults
| Platform | Default/day | Hard cap/day | Min spacing | Monthly guard | Binding constraint |
|---|---|---|---|---|---|
| YouTube Shorts | 1 | 2 | 3h | ≤30/mo (stay under 35 ceiling) | API: ~6 uploads/day/project (1,600 units) |
| Instagram Reels | 1 | 2 | 3h | — | API: 50/24h (safe) |
| TikTok | 1 | 2 | 2–3h | — | **Audit required**: unaudited = private + 5-user cap |
- **TikTok gotcha**: the Content Posting API **must pass the audit** or every post is private — this is the single biggest automated-pipeline blocker; budget 2–6 weeks for the audit before launch.
- Behavioral caps (~1–2/day) are far below API quotas → quotas won't bind except TikTok's audit gate and YouTube's per-project upload-unit budget (request a quota increase or use multiple projects if scaling channels).
- Implement a **token bucket per account** (daily cap + min-spacing) and **exponential backoff on 429**; don't hard-code TikTok daily numbers (no quota-query endpoint — handle `reached_active_user_cap`/`429` reactively).

### Gaps
- TikTok's exact per-creator daily post cap is audit-dependent and not publicly fixed; third-party 15–25 figures conflict.
- YouTube upload unit cost (1,600) and IG 50-vs-25 need live re-verification (hosts blocked this session).

---

## Q9. Legal / ToS — automated posting rules & which official APIs are sanctioned

### Takeaway
All three platforms **sanction automated publishing ONLY through their official first-party APIs** and prohibit scraping, credential-sharing automation, and unofficial/reverse-engineered posting. Sanctioned stack: **YouTube Data API v3**, **Instagram Graph API — Content Publishing** (Business/Creator accounts only), **TikTok Content Posting API** (requires app audit for public posts). Compliance = use these APIs, proper OAuth, respect rate limits, and avoid bulk-duplicate/spam patterns.

### Cited Findings
- **Sanctioned APIs** (the three official publishing endpoints) — [getphyllo](https://www.getphyllo.com/post/using-apis-to-automate-content-upload-on-youtube-instagram-tiktok):
  - **YouTube Data API v3** — OAuth upload scope; standard publishing to your own channel, **no app review** required for basic upload — [getphyllo](https://www.getphyllo.com/post/using-apis-to-automate-content-upload-on-youtube-instagram-tiktok) **[FOLKLORE characterization; API itself [PLATFORM]]**
  - **Instagram Graph API / Content Publishing** — requires **Professional (Business/Creator) account** + `instagram_business_content_publish` permission; two-step container→publish model — [Meta](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/content-publishing) **[PLATFORM]**
  - **TikTok Content Posting API (Direct Post)** — **app audit required** to lift private-only restriction; see TikTok **Content Sharing Guidelines** — [TikTok dev](https://developers.tiktok.com/doc/content-sharing-guidelines) **[UNVERIFIED-PRIMARY — host blocked]**
- Prohibited-automation patterns summarized across platforms: **bulk duplicate posting / spam-pattern automation**, **scraping / automated mass actions** — [website-apn](https://website-apn.pages.dev/blog/social-media-api-for-publishing-developer-guide) **[FOLKLORE summary — verify each platform's dev ToS directly]**
- TikTok 3rd-party tools that post via unofficial routes trigger spam errors / risk — favors official API — [Postly](https://blog.postly.ai/how-to-fix-tiktoks-spam-error-when-posting-via-postly-or-other-third-party-tools) **[FOLKLORE]**
- Instagram Content Publishing API launched Jan 2021 (originally 25 posts/24h), expanding management APIs since — [Meta blog](https://developers.facebook.com/blog/post/2021/01/26/introducing-instagram-content-publishing-api/) **[PLATFORM]**

### Inferences
- **Build exclusively on the three first-party APIs.** Any "unofficial API" / browser-automation / credential-based poster is a ToS violation and ban risk — exclude entirely.
- **Account types**: Instagram publishing requires Business/Creator (not personal) accounts — provision accordingly. TikTok requires completing developer app registration + audit.
- Respect each platform's **rate limits and content/community guidelines**; the APIs are reach-neutral (Q4) so there's no ToS-vs-reach tradeoff when using them correctly.
- Keep OAuth tokens healthy (refresh, scope minimization) and log publish confirmations for auditability.

### Gaps
- Full current developer-ToS text for each platform (TikTok Content Sharing Guidelines, Meta Platform Terms, YouTube API Services Terms) wasn't fetchable this session (hosts blocked) — the exact prohibited-automation clauses should be read directly from the primary dev-terms pages before launch.
- Whether TikTok's audit permits a backlog-publishing/scheduling pattern at the pipeline's intended volume needs confirmation in the audit application.
