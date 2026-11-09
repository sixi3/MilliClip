# MilliClip — Experimentation Plan

Status: planning document, 9 Nov 2026. No pipeline code is implied. Companion to
`reports/Short form gameplay view strategy revised.md` (evidence discipline, measurement) and
`reports/India regional gameplay content strategy.md` (Hinglish-first, duo vs highlights, gates).

## 0. Premise and evidence labels

Automation makes *production* nearly free. *Learning* is not free, because it is bounded by:

1. **Publishing slots.** Roughly 1–2 clips/day/platform (project default budget, not a platform limit).
   No near-duplicate variants of one clip (YouTube's inauthentic-content wording names
   "superficial differences" **[Policy — recheck live]**), and no extra test accounts or channels.
2. **Noisy, heavy-tailed view counts.** One post can out-view twenty others.

So the goal is **maximum learning per post**: test big differences, use low-noise proxy metrics,
randomize and block carefully, and let cheap offline layers (§1) prune ideas before they cost a slot.

Labels used throughout: **[Platform]** confirmed in first-party docs (recheck before relying),
**[Observational]** data that shows association only, **[Vendor]** vendor/creator claim,
**[Assumption]** our own modelling choice or project default.

Slot arithmetic **[Assumption]**: 1 distinct clip/day posted to both YouTube and Instagram ≈ 7 clips/week
≈ 55 clips over 8 weeks. Cross-posting *the same* clip to both platforms is one unit, not two (§3).
This 55-clip budget is the binding constraint for the whole roadmap in §8.

## 1. Three learning layers

| Layer | What | Cost in publishing slots | Evidential status |
|---|---|---|---|
| **A. Outside-in outlier mining** | Competitor/niche outlier videos (views far above that channel's own median) mined by the research tool being built separately in `milliclip/research/`. Output: hypotheses about topics, hooks, lengths, formats. | 0 | **[Observational]**, correlational, survivorship-biased. A hypothesis generator only; never a result. |
| **B. Pre-publish filters** | Hard gates (rights, suitability, factual grounding, duplicate, render QA, caption golden tests) and an optional LLM ranker over candidate clips. | 0 | Gates are compliance, not learning. LLM rank is a **filter to drop weak candidates**, never audience evidence; do not report it as "predicted retention" unless validated (§5.5). |
| **C. Live experiments** | Randomized, interleaved treatments on real posts (§3). | 1 per clip | The only layer that yields causal-ish evidence about *our* audience. |

Flow: A proposes → B screens candidates and checks production feasibility → C tests the survivors.
Every hypothesis in the registry (§10) records its `source` (`outlier_mining`, `owner_idea`, `prior_result`).

**LLM-rank validation (cheap, worthwhile):** log the LLM score for every published clip, then
after ≥40 posts compute rank correlation with the 7-day primary proxy. If |ρ| < ~0.2, keep the LLM
only as a coarse reject filter. **[Assumption]** threshold.

## 2. Metrics

### 2.1 Tiers

| Tier | YouTube Shorts | Instagram Reels | Role |
|---|---|---|---|
| **Primary (low-noise proxies)** | Viewed vs swiped away ("chose to watch"); average % viewed; average view duration | Average watch time; shares/sends per reach; saves per reach | Decision metrics. Bounded or light-tailed, so far fewer posts needed (§4). |
| **Secondary** | Engaged views; subs gained per 1K views; likes per view | Follows per reach; likes per reach; plays/reach | Reported, used for gates in the strategy report, but not alone enough to declare a win. |
| **Operational** | Reject rate, duplicate rate, publish failures, processing latency, cost per accepted clip | same | Pipeline health, not content learning. |

Why proxies first: raw view counts depend heavily on shelf luck (which test audience the system
happened to sample), which the log-sd in §4 captures. Ratios like % viewed and shares/reach are less
heavy-tailed per post. Caveat: a higher % viewed is mechanically easier on shorter clips — always
compare *within a length band* **[Platform guidance says to compare similar videos; band cut-offs are an Assumption]**.

### 2.2 Fixed measurement ages

Snapshot every post at **24h, 72h, 7d** after publish (using publish timestamp, not scheduled time).
Primary decision age: **7d** (72h as early-stop age only for bandit arms, §6). Store every snapshot;
never overwrite. Mark values as `null` (unavailable/not yet exposed) vs genuine `0`.

### 2.3 YouTube March 2025 view-count change — never pool

YouTube changed Shorts view counting in March 2025 to count starts and replays, with "engaged views"
reported separately **[Platform: support thread cited in the revised report — recheck]**.
Rules: store `view_definition` per snapshot (`engaged_views` vs `starts_replays`); all of our posts
post-date the change, but historical competitor data from the outlier miner may not. **Never pool
or compare pre- and post-change counts, nor YouTube and Instagram counts, in one analysis.**

### 2.4 Metric access inventory

Status for every row is **UNVERIFIED — confirm against live docs.** A metric visible in the phone app
may not be exposed through the API, may be delayed, or may be unavailable for Shorts specifically.
Verification task: with the real authorized accounts, call each endpoint on one published test video and record
(available / delayed by N h / absent / per-Short vs per-channel only).

| Metric | Platform | Candidate API surface | Status |
|---|---|---|---|
| Viewed vs swiped away ("chose to watch") | YouTube | YouTube Analytics API (possible dimension/metric); else Studio UI only | UNVERIFIED — confirm against live docs |
| Average view duration | YouTube | YouTube Analytics API (`averageViewDuration`-style metric) | UNVERIFIED — confirm against live docs |
| Average % viewed | YouTube | YouTube Analytics API (`averageViewPercentage`-style metric) | UNVERIFIED — confirm against live docs |
| Views / engaged views (distinct) | YouTube | YouTube Analytics API; Data API `statistics.viewCount` | UNVERIFIED — confirm against live docs |
| Likes, comments, shares | YouTube | YouTube Analytics API / Data API | UNVERIFIED — confirm against live docs |
| Subscribers gained from a video | YouTube | YouTube Analytics API | UNVERIFIED — confirm against live docs |
| Traffic/geography/language split | YouTube | YouTube Analytics API dimensions | UNVERIFIED — confirm against live docs |
| Reach, plays/views | Instagram | Instagram Graph API media insights | UNVERIFIED — confirm against live docs |
| Average watch time / total watch time | Instagram | Instagram Graph API Reels insights | UNVERIFIED — confirm against live docs |
| Shares (sends), saves, likes, comments | Instagram | Instagram Graph API media insights | UNVERIFIED — confirm against live docs |
| Follows attributed to a Reel | Instagram | Graph API (if exposed) | UNVERIFIED — confirm against live docs |
| Trial Reel performance vs main-feed Reel | Instagram | Unknown | UNVERIFIED — confirm against live docs |
| Insight retention window / backfill limits | Both | Docs | UNVERIFIED — confirm against live docs |

Rule: **an experiment's primary metric may only be one marked "verified available" in this table.** If a
preferred proxy is UI-only, either collect it by a documented manual export step or demote it to secondary.

## 3. Experimental design

- **Unit of randomization: one distinct clip/event.** A clip is posted once per platform; its treatment label
  is shared across platforms (one unit, two measurements). Platform is a stratum/covariate, not extra units.
- **Randomize per clip, interleave in time.** When a clip passes the §1B filters, it enters the next slot and its arm is
  drawn by seeded RNG (stored in the registry). **Never A-block-then-B-block**: that confounds with launch-hype
  decay, channel growth, weekday and festivals.
- **Blocked randomization:** within each stratum, randomize in blocks of 2–4 so arms stay balanced even if the test stops early.
- **One major question at a time** (a single factor). Other production choices are fixed at defaults for the test period.
  Pre-agreed minor factors may vary only if assigned independently (factorial), but don't count them as separate evidence.
- **Stratify by:** event/topic type (e.g. stunt, chase, glitch, explainer-topic), length band (≤20s, 21–35s, 36–60s —
  **[Assumption]** bands), platform. Analyze with stratum as a covariate or via within-stratum comparisons.
- **Distinctness requirement:** every treatment posts a *different* clip/event. If only one clip exists for an event, it
  gets one treatment (chosen by RNG); do not render it twice and post both.
- **Fixed-effects hygiene:** same posting-time window policy during the test (unless time *is* the factor), same title style,
  same account, same hashtag policy.

### 3.1 Pre-registration (before the first post of each test)

Written to the registry (§10) and frozen (hash stored). Required fields:

1. Hypothesis and expected direction, with source layer (A/B/C).
2. Arms and exact operational definitions (what differs; what is held fixed).
3. Primary metric and measurement age (default 7d), plus ≤2 secondary metrics.
4. Minimum meaningful effect (MDE) — smallest difference worth acting on, in metric units.
5. Decision rule (e.g. "ship B if P(B > A by ≥MDE) ≥ 0.90 and the guardrail holds"; "inconclusive otherwise → keep default A").
6. Stratification variables and block size.
7. Max duration / max posts per arm. Exceeding it ends the test as "inconclusive."
8. Exclusions defined up front (rights/suitability rejections are removed *before* arm assignment; platform outages; a post pulled for policy).

Anything not pre-registered is exploratory: label it so, and treat it as a new hypothesis.

## 4. Sample size

**All numbers below are illustrative and assumption-driven; they come from `scripts/sample_size_sim.py`
(numpy, seed 7, 3,000 replications per cell). They are not measurements from any real channel.**

Assumptions: two arms, equal allocation, one unit = one clip, two-sided α = 0.05, 80% power; critical
values are calibrated by simulating the null at each n. Views ~ log-normal with log-sd σ; arm B's *median* is r× arm A's.
The "naive" test is a Welch t-test on raw views (what you'd get comparing mean views). The proxy is average % viewed ~ Beta
with mean 0.55 (our guess) and a clip-to-clip sd stated below.

### 4.1 Raw views — posts needed **per arm**

| Log-sd σ (assumed) | 1.5× median, log-scale test | 1.5×, naive raw-mean test | 2× median, log-scale test | 2×, naive raw-mean test |
|---|---|---|---|---|
| 0.8 (mild spread) | 66 | 85 | 23 | 28 |
| 1.2 (plausible) | 143 | 277 | 49 | 90 |
| 1.6 (heavy tail) | 258 | 947 | 85 | 269 |

### 4.2 Lower-variance proxy (average % viewed) — posts needed **per arm**

| Beta concentration κ → clip-to-clip sd | +5 points (e.g. 55→60%) | +10 points |
|---|---|---|
| κ=10 → ~15 pts | 145 | 36 |
| κ=20 → ~11 pts | 77 | 19 |
| κ=40 → ~8 pts | 39 | 11 |

### 4.3 False positives with small samples

A/A simulation (no true difference), 20 posts/arm, σ = 1.6: a rule "B wins if mean views are ≥20% higher" fires
**~40%** of the time; the median-of-logs analogue fires ~39% (one-sided). Declaring winners off raw views at ~20 posts/arm is mostly noise.

### 4.4 What this means for the plan **[Assumption-driven]**

- With ~55 clips in 8 weeks (§0), a 2-arm test has ~27 clips/arm if it uses everything. That can detect roughly a **2× difference in
  median views only if σ ≲ 0.9**, or a **~+10-point shift in a proxy** when clip sd ≲ 11 points. It cannot detect 1.5× in views.
- Hence: **decision metrics are proxies; views are a secondary report.** Pick treatments with *large* expected effects (concept, format),
  not cosmetic ones.
- The India report's gate ("≥20% margin on engaged views per Short and shares per reach at 7 days, ≥20 posts/arm") is a **project default**.
  At 20 posts/arm it is underpowered for a 20% views difference (needs hundreds/arm) — treat 20 posts/arm as the *earliest look*, evaluate with the
  Bayesian rule in §5 on proxies, and let the gate return "inconclusive: continue to the max-duration cap" rather than a forced verdict.
- **Re-run the simulation with real σ and proxy sd after ~30–50 posts.** Replace the assumed spreads in this section with channel estimates.
- Variance reduction (free): within-stratum comparisons, adjusting for length band and platform, and using proxies not counts.

## 5. Analysis

1. **Transform.** Views and watch-time totals: analyze `log(views + 1)`; or rank-based (Mann–Whitney / Hodges–Lehmann shift on logs).
   Ratio-bounded proxies: analyze as-is (or logit for rates). Report effects as **ratio of medians** (views) and **point differences** (proxies),
   with 80% and 95% intervals.
2. **Bayesian primary read.** Model per-arm log-metric as Normal with unknown mean/sd (weakly informative priors **[Assumption]**: mean
   from channel history or competitor miner, wide sd); report **P(B > A)** and **P(B > A by ≥ MDE)** from posterior samples. A pre-registered rule
   like "act at P(≥MDE) ≥ 0.90" replaces repeated p-value peeking. Use stratum as a covariate (hierarchical term if ≥3 strata).
3. **Outlier discipline.** Always show the arm distributions (dot plot of per-clip values). Re-run with the top-1 post per arm removed
   (and with trimming at 5%). **A result that changes sign or drops below the decision threshold when one post is removed is not a win.**
   A viral outlier is logged as a *lead for new hypotheses* (new test), not as proof for its arm.
4. **Multiple looks.** Planned looks at 20 and 40 posts/arm and the max-duration cap; the decision threshold at each look is stricter
   than the final (**[Assumption]**: 0.95 early vs 0.90 final). No unplanned looks decide a test.
5. **Predictions are claims.** Any pre-publish score (LLM rank, "retention confidence") is a hypothesis to be validated against 7d proxies (§1), never a result.

### 5.1 Confounders

| Confounder | Why it bites | Handling |
|---|---|---|
| GTA 6 launch hype decaying | All topic-linked views fall over weeks, penalizing whichever arm ran later | Interleave; include `days_since_launch` / week index as a covariate; never sequential A→B |
| Channel growth / audience shifts | New subscribers change the test audience; later posts see a bigger base | Interleave; stratify by week; prefer rate proxies over counts |
| Seasonality / festivals (Diwali, IPL, exam periods, weekends) | Demand swings unrelated to content | Calendar table of known dates; flag posts within ±2 days; exclude or covariate |
| Platform changes (view definition, UI, algorithm) | Breaks comparability | Log `platform_change` events in the registry; never pool across them (§2.3); restart baseline |
| Shelf / test-audience luck | Early exposure varies wildly | Use 7d proxies; heavy-tail handling (§5.3) |
| Cross-contamination (viewers see both arms) | Spillover lowers effect size | Accept; note as bias toward null for brand/format tests |
| Event difficulty (some clips just better) | Dominates treatment | Randomize per clip; stratify by event type; pre-filter quality (§1B) |

## 6. Adaptive allocation (bandits)

Fixed 50/50 A/B is the default for two-arm structural questions (format, concept). Switch to a **Thompson-sampling bandit**
only when **all** of these hold:

- ≥3 arms (e.g. 3–5 hook styles) or many candidate templates;
- a **verified proxy metric** (§2.4) with ≥24h–72h availability, used as the reward;
- treatments are cheap and *distinct* (never near-duplicates of the same clip);
- ≥8–10 posts already collected per arm (warm start) and arms were randomized up to then;
- no strong time trend left uncontrolled (or reward is detrended within week).

Design **[Assumption]**:

- Reward = z-scored 72h primary proxy within stratum (e.g. chose-to-watch rate, avg % viewed), clipped at ±3 sd.
- Posterior: Normal-Normal per arm; sample, pull the arm with the highest draw.
- **Exploration floor:** every arm keeps ≥10–15% of allocation (≥1 post per 10).
- **Guardrails:** a **hard stop** and reversion to the default arm if an arm's rolling 72h proxy falls below the default by more than a pre-set margin
  with ≥0.95 posterior probability; no arm may exceed 70% of allocation; reset posteriors after any platform change event.
- Report the bandit's *decision*, not "winner": bandit-collected data is biased toward the leading arm, so for formal claims, use the
  analysis in §5 with the logged allocation probabilities (inverse-probability weights) or finish with a short fixed-allocation confirmation.
- Revert to fixed A/B for any *structural* question or whenever the reward metric is views counts.

## 7. Platform-native test tools

| Tool | What it offers | Status |
|---|---|---|
| **Instagram Trial Reels** | Share a Reel with non-followers first, before showing it to followers; a way to test content on cold audience **[Vendor/Platform announcement — recheck]** | **UNVERIFIED — confirm against live docs.** Whether the Graph API can publish trial Reels, and whether trial insights are exposed, is unknown. If UI-only, use manually only as a pre-screen, and don't auto-count it. |
| **YouTube Test & Compare** | Native thumbnail/title (and possibly other) A/B testing in Studio | **UNVERIFIED — confirm against live docs.** Support for Shorts specifically and API access are both unknown. Likely long-form-only; do not assume. |

Policy: use them as *extra* precision on caption/title/thumbnail questions **if** available; they never replace our clip-level design.
They test packaging on one video — not differences in underlying clip content — so there's no conflict with the "distinct clip" rule, but confirm the
tool's own terms. Where results come from a native tool, record `source=native_tool` in the registry and do not pool them with our own arms.

## 8. Prioritized roadmap (first ~8 weeks)

Order = expected effect size × decision value ÷ posts needed: **concept > format > hook > length > caption > time.**
Big levers first; small levers wait until channel-specific σ is known. Budget **[Assumption]** ≈ 55 clips/8 weeks (§0). Timing inside the India
report's Phase 2 ("first ~60 posts, 6–8 weeks").

| Weeks | Question | Arms | Primary metric (7d) | MDE (default) | Posts | Notes |
|---|---|---|---|---|---|---|
| 0 | Baseline setup | — | — | — | 0 | Verify metric access (§2.4); estimate σ from a few unpublished/early posts; fix defaults |
| 1–8 (continuous) | **Q1 Topic/concept** | Rotate 3–5 topic/event categories (e.g. stunts, police chase, glitches, explainer-topics from outlier mining) *inside both formats* | chose-to-watch / avg % viewed; shares per reach | Descriptive: rank concepts; flag top vs bottom | all posts | Stratify, don't hard-test: learn which concepts to over-sample; categories are weakly randomized by event availability |
| 2–8 | **Q2 Format: duo vs highlights** | A = original two-character Hinglish duo explainer; B = coherent highlight + Hinglish hook (control) | avg % viewed + shares/reach (YouTube: engaged views as secondary) | India gate default: **≥20% relative** on the primary proxy(ies), plus not worse on guardrail | **≥20/arm minimum; stretch to 27+** | Randomized per clip within concept strata; project-default margin, not evidence-based. Decide with §5 Bayesian rule; "inconclusive" → highlights primary, duo as a series |
| 5–8 (after Q2 early read) | **Q3 Hook style** | 2–3 hooks (e.g. payoff-first, question, context-first) on the winning format | chose-to-watch | +5 pts chose-to-watch **[Assumption]** | 10–15/arm; bandit if 3+ arms (§6) | Only after format is clear to avoid interaction confusion |
| 7–8+ | **Q4 Length** | Length bands (≤20 / 21–35 / 36–60 s) | avg view duration (not % viewed alone) | — | observational by stratum | Mechanical % viewed advantage for short clips; use per-band comparison and duration metrics. Randomize cuts only where the event allows |
| 8+ | **Q5 Caption style** | Subtitles/emphasis vs minimal; Roman vs Devanagari Hinglish caption (India report) | avg % viewed | — | 15+/arm | Low expected effect — defer; use native tool (§7) if available |
| 8+ | **Q6 Posting time** | Windows (e.g. 5–7 PM IST vs others) | 24h reach proxy | — | 15+/arm | Lowest priority: vendor guidance only **[Vendor]**; confounded by audience composition. Use Insights data first |

Re-evaluate at weeks 4 and 8 and at each India-report gate (≥20 posts/arm, 90-day pace). Gate outputs feed back into the registry as decisions with dates.

## 9. Guardrails

- **Daily caps** per platform (default 1–2) from the pipeline; the experiment scheduler may reorder arms but never raise the cap.
- **Every test post is a genuinely distinct video** (different event/footage). No re-renders of the same moment as separate arms; no
  superficial differences (color, crop nudge, music swap) used as treatments.
- **No test-account farms,** no secondary accounts or channels for experimentation. Experiments run on the single real channel/account per platform.
- **Existing gates always apply first:** rights/provenance, content suitability and advertiser suitability, factual grounding, privacy,
  licensed audio, AI-disclosure flags. A treatment never relaxes a gate; ineligible clips are excluded before randomization.
- **Stop rules** (any one halts a test and logs `stopped`): policy warning/strike, Content ID claim pattern, spike in negative feedback or
  complaints, monetization/limited-ads notice, platform metric-definition change (§2.3), posting circuit breaker from ARCHITECTURE §6, arm proxy falling
  ≥ pre-set margin below baseline with posterior ≥ 0.95 (§6), max-duration reached.
- **No data peeking decisions** outside pre-registered looks; no HARKing; changed hypotheses get new IDs.
- **Human override:** owner can pause the whole experiment system; paused tests resume or close as `inconclusive`.

## 10. Experiment registry schema

SQLite DDL (a YAML mirror of the same keys is acceptable for review). Pre-registration fields are frozen once `status` leaves `draft`.

```sql
CREATE TABLE experiment (
  id               TEXT PRIMARY KEY,            -- e.g. 'EXP-2026-004'
  title            TEXT NOT NULL,
  hypothesis       TEXT NOT NULL,
  source           TEXT,                        -- outlier_mining | owner_idea | prior_result
  question_tier    TEXT,                        -- concept | format | hook | length | caption | time
  arms             TEXT NOT NULL,               -- JSON: [{"name":"A","definition":"..."},...]
  unit             TEXT NOT NULL DEFAULT 'clip',-- distinct clip/event
  strata           TEXT,                        -- JSON: ["event_type","length_band","platform"]
  block_size       INTEGER,
  allocation       TEXT NOT NULL DEFAULT 'fixed',-- fixed | thompson
  explore_floor    REAL,                        -- e.g. 0.10 for bandits
  primary_metric   TEXT NOT NULL,               -- must be 'verified' in metric inventory
  secondary_metrics TEXT,                       -- JSON
  measure_age      TEXT NOT NULL DEFAULT '7d',  -- 24h | 72h | 7d
  mde              REAL NOT NULL,               -- in metric units or relative; see mde_unit
  mde_unit         TEXT NOT NULL,               -- ratio | points | relative_pct
  decision_rule    TEXT NOT NULL,
  looks            TEXT,                        -- JSON: [{"posts_per_arm":20,"threshold":0.95}, ...]
  max_posts_per_arm INTEGER,
  max_duration_days INTEGER,
  assumptions      TEXT,                        -- sigma / sd used for sample size
  prereg_hash      TEXT,                        -- hash of frozen fields
  start_date       TEXT,
  end_date         TEXT,
  status           TEXT NOT NULL DEFAULT 'draft',-- draft | running | stopped | completed | inconclusive
  result           TEXT,                        -- JSON: effect, interval, P(B>A), P(>=MDE), outlier check
  decision         TEXT,                        -- adopt_A | adopt_B | keep_default | follow_up
  notes            TEXT
);

CREATE TABLE experiment_assignment (
  experiment_id    TEXT REFERENCES experiment(id),
  clip_id          TEXT NOT NULL,               -- the unit; one row per clip
  arm              TEXT NOT NULL,
  stratum          TEXT,
  rng_seed         TEXT,
  alloc_prob       REAL,                        -- needed for bandit weighting
  assigned_at      TEXT,
  excluded         INTEGER DEFAULT 0,           -- exclusions defined in prereg only
  exclusion_reason TEXT,
  PRIMARY KEY (experiment_id, clip_id)
);

CREATE TABLE metric_snapshot (
  post_id          TEXT NOT NULL,               -- platform post
  platform         TEXT NOT NULL,
  age              TEXT NOT NULL,               -- 24h | 72h | 7d
  metric           TEXT NOT NULL,
  value            REAL,                        -- NULL = unavailable, 0 = genuine zero
  view_definition  TEXT,                        -- starts_replays | engaged | n/a (never pool)
  fetched_at       TEXT,
  PRIMARY KEY (post_id, age, metric)
);
```

## 11. Open verification items

1. Metric access inventory (§2.4) — every row.
2. Instagram Trial Reels and YouTube Test & Compare: Shorts support, API/insights exposure (§7).
3. Current YouTube wording on inauthentic/repetitive content and what counts as "superficial differences."
4. Per-platform posting caps actually in force on the real accounts.
5. Re-run `scripts/sample_size_sim.py` with measured σ/proxy sd after 30–50 posts.
