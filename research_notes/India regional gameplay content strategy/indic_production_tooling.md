# Indic-language automated video production tooling (2025-2026): ASR, TTS, LLM scripting, caption rendering, metadata, human review

Scope: English, Hinglish (code-mixed Hindi-English), Hindi, Bengali, Malayalam for an automated short-form gameplay pipeline (M4 Mac mini target). Voice cloning of real people is excluded.

**Method note (read first):** WebFetch was network-blocked in this session. Fetches of `docs.sarvam.ai` and `elevenlabs.io` failed with DNS resolution errors (the hosts are outside the session's allowed network domains). Every finding below therefore comes from WebSearch result summaries, not from full pages I read. Vendor pricing and language lists must be checked against the live vendor pages before anything is hard-coded. Where a summary quoted a third-party blog or reseller instead of the vendor, I say so. Retrieval date for all items: 2026-11-09.

---

## 1. Speech recognition (gameplay audio transcription, caption generation)

### Takeaway
Hindi and Bengali ASR is usable with Indic-specific models: IndicConformer scored roughly 8-10% WER on read speech in a small community test, and Sarvam claims about 8-12% on code-mixed speech. Malayalam is clearly harder: about 31% WER for IndicConformer in the same small test, and it is flagged as one of the hardest languages in Vistaar. Base Whisper large-v3 is the weakest option for Indic languages and code-mixing. It also writes words over silence and music, which matters for gameplay audio. For this pipeline ASR is mostly a fallback, because the scripts are LLM-generated and the exact caption text is already known.

### Cited Findings
**Benchmarks and WER**
- Vistaar (AI4Bharat, Interspeech 2023) is the main multi-benchmark suite for Indian-language ASR. Fine-tuned IndicWhisper had the lowest WER on 6 of 7 Hindi benchmarks, and Malayalam is listed among the hardest languages. Vistaar predates IndicConformer and does not evaluate it — [Vistaar arXiv](https://arxiv.org/pdf/2305.15386); [Interspeech PDF](https://www.isca-archive.org/interspeech_2023/bhogale23_interspeech.pdf)
- A community benchmark of IndicConformer on Kathbath (only 100 samples per language) found Hindi at about 7.65% WER, Bengali at about 9.68%, and Malayalam at about 31.50%. The author calls it an initial benchmark, not a definitive evaluation — [Mohanaspiringcoder/indicconformer-asr-benchmark](https://github.com/Mohanaspiringcoder/indicconformer-asr-benchmark)
- Whisper large-v3 had a WER of 34.1 on code-switched Hindi tokens in the Vaani Hindi benchmark. The overall Hindi WER was not in the snippet — [Vaani Benchmark V1.0, arXiv 2606.21408](https://arxiv.org/pdf/2606.21408)
- A 2026 health-conversation challenge (DISPLACE-M) used both Whisper large-v3 and IndicConformer as baselines. Their WERs were not in the search snippet — [DISPLACE-M arXiv 2603.02813](https://arxiv.org/pdf/2603.02813)
- A 2026 paper reports that commercial and open-source systems fail on entity-dense Indic audio, and that synthetic TTS audio closes the gap. This is relevant because gameplay contains many proper nouns (game names, places, weapons) — [TTS-STT Flywheel, arXiv 2605.03073](https://arxiv.org/pdf/2605.03073)
- Bengali Whisper fine-tunes report numbers that cannot be compared with each other:
  - A community fine-tune reports 44.5% WER on its FLEURS evaluation set — [KhushiDS/whisper-large-v3-Bengali](https://huggingface.co/KhushiDS/whisper-large-v3-Bengali)
  - Mozilla's fine-tune self-reports 9.65% WER on Common Voice Bengali — [mozilla-ai/whisper-large-v3-bn](https://huggingface.co/mozilla-ai/whisper-large-v3-bn)
- On Common Voice 24, Whisper large-v3 had a 9.62% insertion rate on Indian-accented English. The cause was repetition loops, and the effect was specific to Indian accents, not US or Canadian ones — [Do LLM Decoders Listen Fairly?, arXiv 2604.21276](https://arxiv.org/pdf/2604.21276)
- In a 2026 preprint, base Whisper large-v3 wrote words over silence 61.9% of the time and over music 99.0% of the time. A fine-tune cut those rates to 0.0% and 1.3%. The tuning targeted Malay, not Indic languages — [How to Reduce Whisper Hallucination, arXiv 2609.32560](https://arxiv.org/html/2609.32560v1)

**Sarvam speech-to-text (Saaras)**
- Sarvam released Saaras V4 (September 2026), covering all 22 scheduled Indian languages plus English, and describes it as handling code-mixed speech — [MarkTechPost](https://www.marktechpost.com/2026/09/26/sarvam-ai-releases-saaras-v4-a-speech-to-text-model-for-all-22-indian-languages-and-global-english/)
- Sarvam claims Saaras V4's error rate on noisy audio is under half that of Deepgram Nova-3 and GPT-4o Transcribe. This is a vendor claim — [mindcat.ai summary](https://mindcat.ai/blog/sarvam-saaras-v4-speech-to-text); [aiintoai report](https://aiintoai.vercel.app/article/sarvam-ai-saaras-v4-speech-to-text-deep-report)
- Hinglish WER figures come from resellers or blogs and are not independent:
  - Saaras v3 is listed at under 12% code-mixed WER by a reseller — [CallMissed Saaras v3](https://www.callmissed.com/models/saaras-v3)
  - Blogs report Saaras v2 at 8.4% on Hinglish and 9.2% on 8 kHz telephony audio, with no clear method, and the two disagree — [autointerviewai](https://www.autointerviewai.com/blog/best-stt-models-indian-accents-hinglish-2026); [agent-rush](https://agent-rush.com/blog/speech-to-text-indian-languages-comparison-2026)
- Pricing: Sarvam's pricing page (as reported around 28 September 2026) lists STT at ₹30 per audio hour, or ₹45 per hour with diarisation, for real-time, streaming and batch — [aiproducts.in](https://aiproducts.in/blog/sarvam-ai-2026-what-indian-businesses-can-use/); [Sarvam API pricing](https://www.sarvam.ai/api-pricing) (not fetched). A reseller lists Saaras V4 at $0.3125 per audio hour — [CallMissed Saaras V4](https://www.callmissed.com/models/saaras-v4)

**Google Chirp 3 (STT)**
- Word-level timestamps in Chirp 3 transcription are available only in `Recognize` and `BatchRecognize`, not in `StreamingRecognize` — [Google Cloud Chirp 3 STT docs](https://docs.cloud.google.com/speech-to-text/docs/models/chirp-3)

**ElevenLabs STT and forced alignment**
- ElevenLabs STT reportedly supports 90+ languages, including Hindi, Bengali and Malayalam (third-party summary) — [telenow.ai](https://telenow.ai/blog/elevenlabs-speech-to-text-models-benchmarks-pricing-and-when-to-use-it/)
- ElevenLabs launched a Forced Alignment API, trained on over 150 languages. It takes audio plus a transcript and returns word- and character-level timestamps — [ElevenLabsDevs on X](https://x.com/ElevenLabsDevs/status/1909234711546708030)

**Licensing and Apple Silicon**
- IndicConformer is MIT-licensed according to the AI4Bharat GitHub repo and the Government of India AIKosh catalog. The Hugging Face model page is gated, so you must agree to share contact information to download it — [AI4Bharat/IndicConformerASR](https://github.com/AI4Bharat/IndicConformerASR); [AIKosh listing](https://aikosh.indiaai.gov.in/home/models/details/aibharat_indicconformer_600m_multi.html); [HF model](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual)
- There are community repackages of IndicConformer-600M for local inference: a CoreML RNNT build (Apple Silicon) and ONNX/sherpa-onnx builds. These are community ports, not AI4Bharat releases — [phequals CoreML](https://huggingface.co/phequals/indic-conformer-600m-multilingual-coreml-rnnt); [VEXYL-STT self-hosted server (Medium)](https://medium.com/@anilmathewm/vexyl-stt-free-self-hosted-indian-language-speech-to-text-server-f2909003aaf6)

### Inferences
- **Per-language ASR verdict:**
  - English: Whisper is fine.
  - Hindi: IndicConformer or Saaras is good.
  - Hinglish: Saaras is the best-documented option, but with vendor-only numbers.
  - Bengali: workable.
  - Malayalam: unreliable for verbatim captions. A WER near 30% means about one word in three is wrong.
- The pipeline generates its own scripts and TTS. Karaoke captions should therefore come from the known script text plus TTS timestamps or forced alignment, not from ASR. ASR is only needed to transcribe the owner's gameplay voice or chat, if that is ever used.
- If ASR runs over gameplay audio, put voice-activity detection in front of it. Whisper's reported 61.9% and 99.0% rates of writing words over silence and music would otherwise produce fake captions over game music.
- Apple Silicon options:
  - Whisper and faster-whisper run well (both MIT, from general knowledge; not verified this session), but they are weak on Indic languages.
  - IndicConformer via the community CoreML or ONNX ports is the best local option for Indic languages.
  - Sarvam is cheap enough in the cloud: ₹30 per hour is about ₹0.5 per minute, which is negligible.

### Gaps
- I found no same-test-set, head-to-head WER table for Whisper large-v3/turbo vs IndicConformer vs Saaras vs Chirp 3 for Hindi, Bengali and Malayalam. The Vistaar leaderboard page was not reachable.
- No Malayalam WER for Whisper large-v3 or turbo was found. I also found no Hinglish (Roman-script output) WER for any open model.
- I did not confirm the IndicWhisper license, or whether Saaras returns word timestamps.
- I did not confirm the license for Whisper or faster-whisper this session (I believe both are MIT; verify on GitHub).
- I found no mlx-whisper Indic benchmark.

---

## 2. Text-to-speech for original character voices

### Takeaway
The two realistic commercial choices are ElevenLabs v3/v4, which wins blind listener preference overall and has character-level timestamps, and Sarvam Bulbul v3/v4, which covers 11 languages including Bengali and Malayalam, has explicit commercial output rights, very low INR pricing and better Indic pronunciation accuracy by vendor claims. Google Chirp 3 HD covers bn-IN and ml-IN but appears to lack timing marks. AI4Bharat's open models are reported as MIT or Apache, but their training-data provenance is unclear, which makes commercial use legally uncertain.

### Cited Findings
**Sarvam Bulbul**
- Bulbul v3 pricing:
  - ₹3.00 per 1,000 characters pay-as-you-go, with tiers at ₹2.85 (Pro), ₹2.70 (Growth) and ₹2.60 (Business), for real-time and streaming — [Sarvam API pricing](https://www.sarvam.ai/api-pricing); [Sarvam docs pricing](https://docs.sarvam.ai/api-reference-docs/pricing) (both via search summary)
  - One aggregator says v3 is flagged as beta pricing — [usagepricing.com](https://www.usagepricing.com/blueprint/sarvam-ai)
- Bulbul v3 languages: English (India) plus 10 Indic languages, including Hindi, Bengali and Malayalam. Assamese is not supported — [invideo blog](https://invideo.io/blog/sarvam-bulbul-indian-tts/); [Bolna integration](https://www.bolna.ai/integrations/sarvam-tts)
- Bulbul commercial licensing: Sarvam's commercial-licensing page says Bulbul v3 audio is licensed for commercial shipment when it is generated on your account with credits consumed. The rights fall under the Production License in Sarvam's EULA, and plan tiers affect only rate limits and credits — [Sarvam commercial licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing)
- Bulbul V4 has launched, marketed as emotional voice for 11 Indian languages — [AlphaSignal](https://alphasignal.ai/news/sarvam-ai-ships-bulbul-v4-to-bring-emotional-voice-to-11-indian-languages). A summary also mentioned a "Bulbul V4 Flash" promotional price of ₹10 per 10,000 characters through 12 November. That figure came from a search summary and is unverified.

**ElevenLabs**
- ElevenLabs API pricing lists v3 at $0.08 per 1,000 characters ($0.04 for Flash/Turbo or v3 Conversational). A third-party guide says $0.10 per 1,000 characters for v3 and Multilingual v2, which may be outdated — [ElevenLabs API pricing](https://elevenlabs.io/pricing/api) (via summary); [felloai](https://felloai.com/elevenlabs-pricing/)
- ElevenLabs says one minute of audio is about 1,000 characters, so v3 works out to roughly $0.08 per minute — [cartesia.ai on ElevenLabs pricing](https://www.cartesia.ai/learn/elevenlabs-pricing)
- Language support:
  - ElevenLabs says v3 covers 70+ languages, and Hindi is named in a third-party list — [ElevenLabs TTS product guide](https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech); [fal.ai](https://fal.ai/models/fal-ai/elevenlabs/tts/eleven-v3)
  - Multilingual v2's 29 languages include Hindi and Tamil, but not Bengali or Malayalam — [ElevenLabs TTS capabilities](https://elevenlabs.io/docs/overview/capabilities/text-to-speech)
  - The guide now recommends moving to Eleven v4 — [same product guide](https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech)
- Timestamps: `/v1/text-to-speech/{voice_id}/with-timestamps` returns character start and end times plus a normalized alignment. A streaming variant returns alignment per chunk — [ElevenLabs TTS capabilities](https://elevenlabs.io/docs/overview/capabilities/text-to-speech); [withone.ai](https://www.withone.ai/knowledge/elevenlabs/conn_mod_def::GJ2bFj8_rS8::BXsw7r6ZSByt2nXzYiRhGw). Third-party hosts also offer an "Eleven v3 Timing" endpoint — [WaveSpeedAI](https://wavespeed.ai/docs/docs-api/elevenlabs/elevenlabs-eleven-v3-timing)

**Head-to-head quality**
- Josh Talks ran a blind comparison on mostly Hindi data with some code-mixing. ElevenLabs v3 was preferred overall, 62.11% to 37.89% for Bulbul v3. Bulbul won only the "Announcements" category, 65.6% to 34.4% — [Josh Talks evals](https://evals.ai.joshtalks.com/blog/category-wise-tts-evaluation)
- An arXiv study ran large-scale pairwise preference tests across Indian languages. ElevenLabs v3 ranked 2nd (57% win rate) and Bulbul V3 Beta ranked 4th (52%) of 7 systems — [Preferences of a Voice-First Nation, arXiv 2604.21481](https://arxiv.org/pdf/2604.21481)
- Sarvam claims Bulbul v3 has the lowest character error rate (CER) in every Indian-domain category, including code-mixing and Romanized text — [Sarvam TTS page](https://www.sarvam.ai/text-to-speech). A blog puts Bulbul v3 under 5% CER versus about 10-15% for ElevenLabs v3 Alpha and Cartesia Sonic-3, with no source given — [latestai.me](https://www.latestai.me/2026/02/bulbul-v3-unpacked-sarvam-ais-llm.html)

**Google Cloud**
- Chirp 3 HD lists bn-IN and ml-IN among its languages — [Google Chirp 3 HD (via translate proxy)](https://translate.google.com/translate?client=srp&hl=es&sl=en&tl=es&u=https%3A%2F%2Fcloud.google.com%2Ftext-to-speech%2Fdocs%2Fchirp3-hd)
- Google's supported-voices page says Chirp 3 HD does not support SSML input or the speaking-rate and pitch audio parameters — [Google supported voices](https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types)
- Custom pronunciations work in every locale except some, including bn-IN. ml-IN is not on the excluded list — [Google TTS release notes](https://docs.cloud.google.com/text-to-speech/docs/release-notes)

**Azure**
- Azure neural TTS is about $15 per million characters for standard neural voices and about $22 for Neural HD (East US). Another source lists $30 for HD — [beri.net](https://www.beri.net/article/elevenlabs-vs-cartesia-vs-azure-tts-latency-pricing-voice-cloning-2026); [LiteLLM docs](https://docs.litellm.ai/docs/providers/azure_ai_speech)

**Open-source (AI4Bharat and derivatives)**
- Indic Parler-TTS licensing is inconsistent:
  - Listed as Apache 2.0 by tts.ai and as MIT by AIKosh. It is gated, and one aggregator advises confirming commercial terms with AI4Bharat — [tts.ai](https://tts.ai/voices/indic-parler/?lang=ig); [AIKosh](https://aikosh.indiaai.gov.in/home/models/details/ai4bharat_indic_parler_tts_text_to_speech_model.html); [dev.co](https://dev.co/ai/llms/indic-parler-tts)
  - It supports Bengali and Malayalam.
- IndicF5 licensing and provenance:
  - Listed as MIT on AIKosh, with 11 languages including Bengali and Malayalam — [AIKosh IndicF5](https://aikosh.indiaai.gov.in/home/models/details/aibharat_indicf5.html)
  - The community fine-tune dhee-indic-f5 is CC-BY-NC-4.0. It says it inherits non-commercial restrictions from its lineage: the F5-TTS Emilia training data and IIT-Madras Indic TTS data — [dheeyantra/dhee-indic-f5](https://huggingface.co/dheeyantra/dhee-indic-f5)

### Inferences
- **Recommended default:** ElevenLabs v3/v4 for English, Hinglish and Hindi, chosen for expressiveness and native char-level timestamps. Sarvam Bulbul v3/v4 for Bengali and Malayalam, chosen for confirmed language support and explicit commercial rights, and as a cheap A/B option for Hindi and Hinglish.
- **Cost:** roughly 1,000 characters per minute, at ₹3 (about $0.035) per minute on Bulbul and about $0.08 per minute on ElevenLabs v3. TTS cost is trivial either way for 30-60 s Shorts.
- **Karaoke timestamps:**
  - ElevenLabs returns them natively (character-level, which is easy to group into words).
  - For Bulbul and Chirp 3 HD, no timestamp output was found. Plan a forced-alignment step: ElevenLabs Forced Alignment API, or ASR word timestamps run against the known script, for example Chirp 3 batch, IndicConformer or Whisper with alignment.
  - Forced alignment on clean TTS audio with known text should be far more robust than open transcription, even in Malayalam.
- **Two-character comedic banter:**
  - No benchmark measures comedic timing. ElevenLabs v3's audio-tag and emotional-range positioning, and its preference wins, make it the best bet. Bulbul V4 markets emotion and should be tested.
  - Generate each character's lines separately with distinct original voices, then assemble them with programmed pauses. Do not rely on a single multi-speaker pass.
- **Open-source TTS:** treat AI4Bharat models as "license-unclear for commercial output" until the HF/GitHub LICENSE files and training-data terms are checked. The CC-BY-NC lineage note on an IndicF5 derivative is a red flag.
- **Original voices:** use vendor-designed or stock voices, or text-described voice design (Indic Parler-TTS style prompts or ElevenLabs Voice Design). Do not use reference-audio cloning of any real person. IndicF5 and F5-style models are reference-audio cloners by design, which is another reason to avoid them here.

### Gaps
- I could not confirm from ElevenLabs docs whether v3/v4 TTS supports Bengali and Malayalam. The full language list page was not fetchable. Test before relying on it.
- No word or phrase timestamps were found for Bulbul v3/v4 or Google Chirp 3 HD TTS. I also did not confirm Azure WordBoundary events or bn-IN/ml-IN voice availability.
- I did not verify Google Chirp 3 HD per-character pricing.
- I did not verify ElevenLabs commercial terms by plan (from general knowledge, paid plans grant commercial rights and the free tier requires attribution; verify).
- I found no Bengali- or Malayalam-specific TTS quality evaluations, and no comedic or expressive evaluations. The available preference studies are mostly Hindi.

---

## 3. LLM script generation and translation (Bengali, Malayalam vs Hindi/English; Hinglish)

### Takeaway
Benchmarks consistently show LLMs perform worse in Indic languages than in English, and worse at generating text than at understanding it. Frontier models (Claude, GPT, Gemini) now score in the high 80s to low 90s on MILU, according to unverified leaderboards. That measures comprehension, not natural colloquial generation. Expect Bengali and especially Malayalam scripts to need native review for idiom, register and naturalness. Hinglish is a register choice: generate it directly in Roman script with explicit style examples.

### Cited Findings
- MILU (AI4Bharat, NAACL 2025) covers 11 Indic languages, 8 domains and 41 subjects.
  - Across more than 42 models, GPT-4o had the highest average accuracy at about 74%. In the paper's table, Gemini 1.5 Pro scored about 67.7, Gemini 1.5 Flash about 61.6 and GPT-4o-mini about 57.2.
  - Models do better in high-resource languages than in low-resource ones — [MILU arXiv](https://arxiv.org/pdf/2411.02538); [ACL Anthology](https://aclanthology.org/2025.naacl-long.507.pdf)
- The MILU dataset has 6,638 Bengali questions and 4,321 Malayalam questions — [HF dataset card](https://huggingface.co/datasets/ai4bharat/MILU/blob/main/README.md)
- Third-party leaderboards report MILU scores of 93.1% for Claude Opus 5.5, 91.6% for Claude Sonnet 5.5 and 87.6% for Claude Haiku 5.5. Another ranks Gemini 3.1 Pro Preview first at 93.6%. The method is unverified and the sites disagree — [llm-stats MILU](https://llm-stats.com/benchmarks/milu); [benchmarklist MILU](https://benchmarklist.com/benchmarks/milu/)
- IndicGenBench (Google, ACL 2024) covers 29 Indic languages and 13 scripts. Its tasks are FLORES-IN translation in both directions, cross-lingual summarization, multilingual QA and cross-lingual QA.
  - It found a significant performance gap against English in all languages.
  - It notes that "higher-resource" Hindi and Bengali are still mid-to-low web-resource compared with English.
  - It does not cover long-form generation — [IndicGenBench arXiv](https://www.arxiv.org/pdf/2404.16816); [GitHub](https://github.com/google-research-datasets/indic-gen-bench/)
- A secondary review summarizes IndicGenBench as showing that LLMs understand low-resource languages better than they generate fluent text in them — [themoonlight.io review](https://www.themoonlight.io/review/indicgenbench-a-multilingual-benchmark-to-evaluate-generation-capabilities-of-llms-on-indic-languages)
- IndicTrans2 (AI4Bharat) is an open MT model for all 22 scheduled languages and an alternative translation step — [IndicTrans2 arXiv](https://arxiv.org/pdf/2305.16307). Its license was not verified this session.
- About 93% of native Hindi speakers' code-mixed social media posts were in Roman script versus about 3% in Devanagari (2014 analysis, cited in a 2025 paper). The same paper builds Romanized Hindi and Bengali datasets for LLMs — [Modeling Romanized Hindi and Bengali, arXiv 2511.22769](https://arxiv.org/pdf/2511.22769)

### Inferences
- "Write in English, then adapt": this is likely better for factual and structural control. The plot, gag structure and gameplay facts are fixed in English, which is the LLM's strongest language. A second "transcreate, don't translate" pass then rewrites it into colloquial Bengali or Malayalam. I found no direct study comparing this with native generation for short-form comedy; that would need an A/B test with native raters.
- Expected risks for Bengali and Malayalam:
  - Overly formal or "textbook" register, because sadhu bhasha-like forms and formal Malayalam dominate web text.
  - Literal idiom translation.
  - Wrong game-term handling (whether to transliterate English game terms or translate them).
  - Script mixing, such as stray Devanagari or Latin text in Bengali output.
  - Hallucinated "facts" about games.
- A cheap automated guard is a Unicode-block check that rejects output containing characters outside the target script plus Latin.
- Hinglish: prompt for Roman-script output with a style guide (spelling conventions such as "nahi", "kya", "bhai") and few-shot examples. Normalize spelling consistently, because TTS pronunciation of Romanized Hindi depends on spelling. Sarvam claims Bulbul handles Romanized text, which supports feeding Roman Hinglish straight to TTS.
- The Indic LLMs (Sarvam-M and others, Krutrim) were not benchmarked in my sources. Frontier models are the default. An Indic LLM is worth testing only as a "naturalness rewriter."

### Gaps
- I found no per-language Bengali or Malayalam scores from MILU or IndicGenBench for current frontier models.
- I found no benchmarks for Sarvam's or Krutrim's LLMs.
- I found no evidence on comedic or colloquial generation quality.
- I found no study comparing "translate then adapt" with native generation.

---

## 4. Caption rendering (burned-in Bengali/Malayalam)

### Takeaway
Correct Bengali and Malayalam rendering requires libass built with HarfBuzz (the "COMPLEX" shaper). Without it, Indic scripts render incorrectly, with broken conjuncts and misplaced vowel signs. Even with HarfBuzz, one open FFmpeg/libass ticket reports a Bengali vowel-sign error. Noto Sans Bengali and Noto Sans Malayalam are SIL OFL 1.1, so burning them into commercial video is fine.

### Cited Findings
- FFmpeg closed a 2020 ticket about the subtitle filter failing to render Indic languages as invalid: the libass build lacked HarfBuzz, which FFmpeg cannot fix on its side — [FFmpeg-trac #8738](https://ffmpeg.org/pipermail/ffmpeg-trac/2020-June/054649.html)
- Arch Linux (2013) noted that libass without HarfBuzz renders many writing systems incorrectly, including all Indic languages — [Arch FS#38249](https://bugs.archlinux.org/task/38249)
- In libass logs, a correct build shows a line like "Shaper: FriBidi 1.0.13 (SIMPLE) HarfBuzz-ng 7.3.0 (COMPLEX)". A ticket from about a year ago reports Bengali "সো" rendering as "স" even with HarfBuzz present, linked to libass issue #682. It is still listed as new — [FFmpeg trac #10384](https://trac.ffmpeg.org/ticket/10384)
- HarfBuzz's own shaping tests show residual failures for Malayalam and Bengali in historical test runs (for example, 463 failing out of about 354k Bengali tests). This is general regression history, not a libass result — [HarfBuzz list, Malayalam](https://lists.freedesktop.org/archives/harfbuzz/2012-August/002332.html)
- Malayalam has a known split between traditional and reformed orthography, plus chillu characters, which HarfBuzz and SMC have worked on — [SMC GSoC 2013 archive](https://google-melange.com/archive/gsoc/2013/orgs/smc/projects/nandaja.html)
- Noto Sans Bengali and Noto Sans Malayalam are licensed under SIL Open Font License 1.1, which permits commercial use and embedding. The main restrictions are that fonts cannot be sold on their own and modified versions keep the license — [notofonts/noto-sans-bengali](https://github.com/notofonts/noto-sans-bengali); [Fontsource Noto Sans Malayalam](https://fontsource.org/fonts/noto-sans-malayalam/about); [SIL OFL (Wikipedia mirror)](https://en.wikipedia-on-ipfs.org/wiki/SIL_Open_Font_License)
- A Devanagari conjunct (श्री) breaking into श् री in a renderer without shaping (ReportLab) shows the same class of failure — [reportlab-users](https://groups.google.com/g/reportlab-users/c/QaVk8ZiscRg)

### Inferences
- Build and test requirements:
  - Check at startup that `ffmpeg -filters` and libass logs show HarfBuzz. Homebrew ffmpeg on macOS normally links libass with HarfBuzz, but verify on the M4.
  - Render a golden test card per language containing hard conjuncts and vowel signs (for example Bengali ক্ষ, সো, ত্র; Malayalam chillus ൻ ർ ൽ and conjuncts ക്ക, ന്ത), and compare it pixel-wise against `hb-view` output.
- Karaoke pitfall: per-word or per-syllable highlighting with ASS `\k` tags, or by splitting text into separately styled runs, can break shaping across the split, because a conjunct or vowel sign can be separated from its base consonant. Highlight whole words (split on spaces only) and never split inside a grapheme cluster. Use a grapheme-cluster-aware segmenter (ICU or Python `regex` `\X`), not code-point slicing.
- Alternative path: render caption frames with a HarfBuzz-backed library (Pillow with libraqm, Skia or Pango) and overlay them as images. This gives full control and avoids libass edge cases like #10384.
- Fonts: Noto Sans Bengali, Noto Sans Malayalam and Noto Sans Devanagari, plus Noto Sans for Latin text, all OFL. Use a bold or heavy weight with a stroke for Shorts readability. Indic glyphs need more line height for upper and lower vowel signs.

### Gaps
- I did not confirm whether libass #682 is fixed in current releases.
- I did not test the specific Homebrew build.
- I found no Malayalam-specific libass bug reports.

---

## 5. Platform metadata: native script vs romanized titles/hashtags

### Takeaway
I found no platform documentation or rigorous study on whether YouTube or Instagram treat native-script and romanized titles differently. The available evidence is behavioral: Indians type code-mixed Hindi overwhelmingly in Roman script. Creator guidance says the choice of script follows the audience and recommends bilingual or mixed metadata. Script choice for Bengali and Malayalam titles is an experiment to run, not a known answer.

### Cited Findings
- About 93% of native Hindi speakers' code-mixed posts were in Roman script versus about 3% in Devanagari (2014 analysis) — [arXiv 2511.22769](https://arxiv.org/pdf/2511.22769)
- Romanized Hindi persists because of keyboard friction and the dominance of English in education — [HindiPod101](https://www.hindipod101.com/lesson/hindi-teachers-answer-your-questions-5-what-types-of-hindi-romanization-are-there)
- A 15-person neuroimaging study found reading Romanized Hindi harder than reading English or Devanagari Hindi — [Nature India](https://www.nature.com/articles/nindia.2013.23)
- Creator and vendor guides make three points:
  - Roman Hinglish suits young bilingual Shorts and Reels viewers, while Devanagari suits Hindi-first or regional audiences. Creators often split channels by script.
  - Roman spelling is ambiguous: "kal" can be कल or काल.
  - They recommend adding English keywords to metadata — [themomentra](https://themomentra.com/guides/hinglish-vs-devanagari-captions); [videocaptions.ai](https://www.videocaptions.ai/blog/hindi-vs-hinglish-captions); [capsai](https://capsai.co/blogs/best-practices-for-subtitling-youtube-shorts-in-hindi-and-hinglish)
- YouTube uses title and description text to understand context and match queries. #Shorts is no longer required for Short classification but still acts as a discovery tag. These claims come from creator blogs — [miraflow](https://miraflow.ai/blog/youtube-shorts-titles-descriptions-2026-templates); [Alan Spicer](https://alanspicer.com/youtube-shorts-optimization-titles-hashtags-descriptions/)
- Bollywood film titles mostly use Latin script as a neutral choice — [Wikipedia Roman Urdu](https://en.wikipedia.org/wiki/Roman_Urdu)

### Inferences
- Pragmatic default:
  - Hinglish: Roman-script title, plus English game-name keywords.
  - Hindi: Devanagari title with the English game name, plus a Roman Hinglish phrase in the description.
  - Bengali and Malayalam: native-script hook plus the English game name ("GTA 5") in the title, with romanized and English keywords in the description and hashtags (for example #GTA5 #MalayalamGaming #BanglaGaming).
- This hedges across both search behaviors (romanized typing and native-script audience signal). It needs A/B measurement per channel.
- Set the YouTube video language and audio language fields correctly for each language. That is an explicit signal, independent of title script. This comes from general knowledge of YouTube Studio fields and was not sourced this session.

### Gaps
- I found no first-party YouTube or Instagram statement on script or transliteration handling in search or recommendations.
- I found no data on Bengali or Malayalam hashtag or title performance.
- I found no study on whether YouTube search matches romanized queries to native-script titles (transliteration matching).

---

## 6. Human-in-the-loop: which languages need native review

### Takeaway
English can run unattended with automated checks. Hinglish and Hindi can run mostly automated, with sampled review at the start. Bengali, and especially Malayalam, need native-speaker review before publishing, at least until quality is established. The weak points are LLM generation naturalness, TTS pronunciation of game terms, ASR (Malayalam about 31% WER) and script-rendering edge cases.

### Cited Findings
- Malayalam is among the hardest Vistaar ASR languages, and IndicConformer Malayalam WER was about 31.5% versus about 8-10% for Hindi and Bengali in a small test — [Vistaar](https://arxiv.org/pdf/2305.15386); [community benchmark](https://github.com/Mohanaspiringcoder/indicconformer-asr-benchmark)
- LLM generation lags English in all Indic languages — [IndicGenBench](https://www.arxiv.org/pdf/2404.16816); [MILU](https://arxiv.org/pdf/2411.02538)
- TTS preference studies are largely Hindi-based. Bulbul and ElevenLabs trade wins depending on category — [Josh Talks](https://evals.ai.joshtalks.com/blog/category-wise-tts-evaluation); [arXiv 2604.21481](https://arxiv.org/pdf/2604.21481)
- Bengali rendering bugs can persist even with HarfBuzz — [FFmpeg #10384](https://trac.ffmpeg.org/ticket/10384)
- Entity-dense audio breaks Indic ASR, and game names are dense in entities — [arXiv 2605.03073](https://arxiv.org/pdf/2605.03073)

### Inferences
- **Per-language automation tier:**

| Language | Script/LLM | TTS | Captions (known-text alignment) | Review recommendation |
|---|---|---|---|---|
| English | High | High | High | Automated QA only; spot-check |
| Hinglish | Medium-High (spelling consistency) | Medium-High | High (Roman) | First ~20 clips reviewed, then 10-20% sampling |
| Hindi | Medium-High | High | High (needs HarfBuzz) | First ~20 clips reviewed, then sampling |
| Bengali | Medium (register risk) | Medium (Bulbul; ElevenLabs unconfirmed) | Medium (known libass bug) | Pre-publish native review |
| Malayalam | Medium-Low | Medium (Bulbul) | Medium (only if forced alignment, not ASR) | Pre-publish native review, mandatory |

- **Lightweight review workflow:**
  1. The pipeline renders a draft MP4 and a one-page review sheet: the script in native script plus an English back-translation, a list of flagged terms, and LLM-judge naturalness scores.
  2. It pushes these to a reviewer queue (Telegram/WhatsApp bot, or a simple web page).
  3. The reviewer replies approve, reject or edit-line, typically in 1-2 minutes per 30-60 s Short. Edits re-trigger TTS for that line only.
  4. Keep a per-language pronunciation lexicon of game terms (respellings fed to TTS) and a "banned phrasing" list built from reviewer edits.
  5. Track the reviewer reject rate. Relax to sampling when it is consistently low.
- **Automated pre-checks for every language:**
  - Unicode script-purity check.
  - Back-translation consistency, as an LLM judge comparing back-translated meaning to the English master.
  - TTS round-trip: run ASR on the generated audio and compare it with the script. High CER flags mispronunciation or skipped words. Use a lenient threshold for Malayalam because the ASR itself is weak.
  - Caption glyph-rendering golden test.
  - Duration and timing sanity checks.
- **Cost of review:** freelance native reviewers would cost the most in this pipeline. Model and API costs are a few rupees per clip; that is an estimate from the pricing above, and I did not source reviewer rates.

### Gaps
- I found no sourced data on reviewer rates or on how often LLM-generated Bengali or Malayalam short-form scripts are rejected.
- I found no evaluation of LLM-as-judge reliability for Bengali or Malayalam naturalness.
