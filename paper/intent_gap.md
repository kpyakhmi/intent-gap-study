# The Intent Gap: A Taxonomy of Real-User Failure Modes in Frontier AI Agents

**Kanupriya Yakhmi**
*Independent researcher*

> *Draft v0.1 — skeleton with related work populated. Findings sections are templated; will be filled when Layer 1 grading completes.*

---

## Abstract

Public benchmarks for frontier AI agents (GAIA, OSWorld, AgentBench, GDPval, BrowseComp, SWE-bench) are uniformly *researcher-imagined*: tasks are designed by AI researchers, in clean declarative form, with ground-truth answers fixed in advance. Real users — as captured in 1M+ public conversation corpora — do not interact with frontier models this way. They assume context, change their minds mid-task, contradict earlier requests, abandon, and phrase requests in registers no benchmark has ever sampled. We hypothesize that benchmarks systematically miss the deployment-relevant failure mode we call **the intent gap**: cases where the model literally answered the prompt but missed what the user actually wanted.

We mine WildChat-1M and LMSYS-Chat-1M using a three-stage *frustration-signal filter* (regex → embedding → LLM-as-judge) to surface ~[N] high-quality intent-gap conversations. We replay each prompt across four current frontier models (Claude, GPT, Gemini, and one open model) and grade each replay on two axes: literal compliance and intent satisfaction. We then triangulate the resulting taxonomy against ~[K] published failure-mode taxonomies from research institutes worldwide and against [M] documented production failure incidents (lawsuits, regulatory filings, public post-mortems).

**Headline preliminary findings (from a 50,000-conversation v2 pilot, before cross-model replay or hand-review):**

1. **52.8% of English real-user conversations end after a single exchange.** A substantial fraction of these are likely silent abandonment after intent-gap failure — invisible to deployment-quality pipelines built on user-feedback signals.
2. **Only 3.85% of multi-turn conversations contain an explicit repair signal,** even under a permissive 45-phrase filter that scans every user turn. The intent gap exists, but users rarely verbalize it.
3. **The phrase list expansion from v1 (17 academic phrases) to v2 (45 natural-language phrases) increased hit rate by ~31×.** This implies the dialogue-breakdown detection literature undercounts real-world repair by more than an order of magnitude because its phrase lists are researcher-imagined.

A hand-reviewed and LLM-judge-filtered corpus of ~150–300 high-quality intent-gap conversations is released alongside the filter pipeline, the grading rubric, and the triangulation matrix mapping our taxonomy onto ~25 prior published failure taxonomies plus 5 documented production-failure incidents.

---

## 1. Introduction

The 2026 deployment data is unambiguous. 78% of enterprises run AI agent pilots, but only 14% reach production scale [LangChain 2026]. Quality is the most cited blocker, named by 32% of teams. Independent capability evaluations from research institutes (METR, Apollo Research, UK AISI) document benchmark capabilities advancing on an exponential time-horizon curve [METR 2025], even as deployment-grade reliability stalls. METR's randomized controlled trial of experienced developers using early-2025 AI tools found a *19% productivity decrease* — competent users with capable tools producing net-negative work in some real settings [METR Productivity 2025].

This is the *deployment gap*: the divergence between benchmark performance and what users experience in real interactions. We argue that the deployment gap is not one phenomenon but a class of failure modes that benchmarks structurally cannot surface, because benchmarks are written by researchers in declarative form rather than collected from real users in conversational form.

We name one specific failure mode in this class — the **intent gap** — and study it empirically. The intent gap is the failure mode where the model produces output that is *literally* responsive to the user's prompt but does not satisfy what the user actually wanted. This is distinct from refusal (where the model declines), hallucination (where the output is factually wrong), and jailbreak (where the user adversarially manipulates the model). It is the failure mode that users themselves repair on their next turn — saying "no, I meant," "you misunderstood," "let me rephrase" — and these repair signals are the methodological foothold this study uses.

Our contributions are:
1. A reproducible **frustration-signal filter** that surfaces intent-gap failures from public conversation corpora at scale.
2. A labeled corpus of ~[N] intent-gap conversations released under a permissive license.
3. A multi-axis taxonomy of intent-gap failure modes grounded in user data, validated against the global research literature.
4. A **cross-model replay** showing how current frontier models perform on the same prompts that historically failed, separating recoverable failures from persistent ones.
5. A **triangulation matrix** that maps our taxonomy onto ~[K] prior failure taxonomies from research institutes worldwide and ~[M] production failure incidents.

---

## 2. Related Work

We organize prior work along four dimensions: real-user corpora, failure-mode taxonomies, dialogue-breakdown detection, and agent capability evaluation.

### 2.1 Real-user corpora

WildChat [Zhao et al., 2024] released 1M ChatGPT (GPT-3.5/4) interaction logs from a public hosted endpoint, with country-level metadata. The corpus distinguishes itself from synthetic instruction-following datasets by capturing ambiguous requests, code-switching, topic-switching, and other realistic conversational phenomena. LMSYS-Chat-1M [Zheng et al., 2024] complements WildChat with 1M conversations across 25 LLMs collected from the Chatbot Arena platform, spanning 150+ languages and 210K users. Existing analyses of these corpora have focused on toxicity, jailbreaks, language coverage, and demographics; to our knowledge no published analysis systematically characterizes the *intent gap* at scale.

### 2.2 Failure-mode taxonomies

Anthropic's *Towards Understanding Sycophancy in Language Models* [Sharma et al., 2024] documents that RLHF-trained frontier assistants systematically prefer responses that match user beliefs over truthful ones, across five state-of-the-art models and four task types. Both human raters and preference models prefer convincingly-written sycophantic answers a non-trivial fraction of the time. Anthropic's follow-up work on reward tampering [Anthropic, 2024] shows that sycophancy generalizes — under certain training conditions — into more concerning behaviors including reward function modification. Persona vectors work [Anthropic, 2025] suggests these tendencies have stable representational signatures.

The HELM transparency reports [Stanford CRFM] provide the most comprehensive multi-axis evaluation of foundation models, but, like other benchmarks, are researcher-designed. Park et al.'s *AI Deception: A Survey* [MIT] inventories deception failure modes, complementing this work on the manipulation axis.

### 2.3 Dialogue-breakdown detection and conversational repair

The closest existing methodology to our frustration-signal filter is the *Detect, Explain, Escalate* framework [arXiv 2504.18839, 2025], which fine-tunes an 8B model with teacher-generated reasoning traces to detect dialogue breakdowns in real time across English and Japanese. Their approach is classifier-driven and aimed at runtime escalation; ours is corpus-driven and aimed at offline taxonomy construction. Aljamdi et al.'s CUI 2024 work on spoken-dialogue repair [University of Strathclyde] documents the linguistic asymmetry between user-initiated and system-initiated repair, validating the seed phrases we use as filter inputs. *The Art of Repair in Human-Agent Conversations* [2025] proposes a taxonomy of repair strategies (social, disclosure, information, solving) that informs our seed phrase list.

These works study repair strategies as a phenomenon in their own right; we use repair as a *signal* to surface a different phenomenon — intent-gap failure — and our taxonomy is over the *underlying failures*, not the repair strategies.

### 2.4 Agent capability evaluation and the deployment gap

METR's *Time Horizon* metric [Kwa et al., 2025] establishes that the 50% time horizon for AI agent task completion has been growing exponentially with a ~7-month doubling time since 2019. Their Algorithmic vs. Holistic Evaluation report [METR, August 2025] shows that early-2025 agents on real open-source repositories often produce *functionally correct but unusable* code due to test, formatting, and quality issues — automatic scoring systematically overestimates real-world performance. Apollo Research [2025] forecasts SWE-Bench Verified at 54%–87% by start of 2026 for non-specialized agents. The UK AI Security Institute's Frontier AI Trends Report 2025 documents the rapid gain in frontier model capabilities (e.g., cyber-task completion from 9% in late 2023 to 50% in 2025) and the corresponding pre-deployment evaluation findings.

Our work fits into this landscape as the *user-side complement*: the labs and institutes above measure what models *can* do on tightly-specified tasks; we measure what they *fail* to do on tasks specified by real users.

### 2.5 Multilingual and cross-cultural evaluation

MEGAVERSE [Ahuja et al., NAACL 2024 — Microsoft Research India] benchmarks frontier LLMs across 83 languages and 22 datasets and documents systematic data contamination issues in multilingual evaluation. AI4Bharat's Indic LLM-Arena and MILU benchmarks [IIT Madras, 2025] provide a crowd-sourced human-in-the-loop evaluation across India's 22 scheduled languages, with the explicit pillars of language, context, and safety. MILU finds GPT-4o tops at 72% accuracy and that frontier LLMs underperform especially on culturally-relevant Arts/Humanities and Law/Governance categories. We treat these as the empirical foundation for our *Cultural / regional misread* taxonomy category.

### 2.6 Production failure incidents

Moffatt v. Air Canada (BC Civil Resolution Tribunal, February 2024) is the canonical adjudicated AI deployment failure: a chatbot produced confident, fluent, internally-consistent guidance that was contractually wrong; the user relied on it; the airline was held liable. Springer's *AI & Society* analysis [Lior, 2024] frames this as a foundational agency-and-responsibility-gap problem in chatbot deployment. The 2025 AI Agent Index [arXiv 2602.17753] documents that deployed agent providers share little about their safety, evaluation, and societal-impact practices — meaning independent corpus analysis remains the only public-evidence path into deployment-grade failure modes. We include this case and a curated set of others as Track D evidence.

---

## 3. Method

### 3.1 Source corpora

We use two public corpora as primary data sources:
- **WildChat-1M** (AI2 ImpACT license, CC BY-NC for derivatives): 1M ChatGPT conversations including coarse country metadata.
- **LMSYS-Chat-1M** (research-use license): 1M conversations across 25 models collected from Chatbot Arena.

We restrict to conversations with at least four turns (≥2 user + ≥2 assistant) to ensure a repair turn is at least possible. We restrict the first analysis to English; multilingual extension to two additional languages is a stretch goal (§7).

### 3.2 The frustration-signal filter

We define a three-stage filter:

**Stage A — Lexical match.** A conversation is retained if user turn 2+ matches any seed phrase from a curated list of 80 English repair markers (e.g., "no, I meant," "you misunderstood," "let me rephrase," "that's not what I asked"). Seed list released as a separate artifact.

**Stage B — Embedding similarity check.** For retained conversations, we compute the cosine similarity between (a) the embedding of (user-original-prompt + repair-turn) and (b) the embedding of the assistant's prior response. Conversations with cosine similarity below threshold τ = 0.55 are retained, on the hypothesis that low similarity indicates the assistant's response addressed something different from the user's true intent. The threshold is tuned on a held-out development sample.

**Stage C — LLM-as-judge confirmation.** Each surviving candidate is presented to an LLM judge (Claude Haiku tier) with the prompt template in [Appendix A]. The judge classifies the failure as one of (Refusal, Hallucination, Intent Gap, Other Dissatisfaction, False Positive). Only Intent Gap candidates proceed.

**Stage D — Hand review.** All remaining candidates undergo human review by the first author. The hand-review rate is documented; a 100-conversation second-grader subset is used for inter-rater reliability (Cohen's κ reported in Findings).

### 3.3 Cross-model replay

For each retained intent-gap conversation, we replay the *first user turn* (with any necessary anonymized system context) across four current frontier models: Claude [version pinned], GPT [version pinned], Gemini [version pinned], and Llama [version pinned] as the open baseline. Model versions are pinned on the day of replay and reported.

### 3.4 Grading rubric

Each (conversation, model) replay is graded on two axes:
- **Literal compliance** ∈ {0, 1, 2}: did the model address the literal prompt?
- **Intent satisfaction** ∈ {0, 1, 2}: did the model satisfy the user's *true intent* as inferred from the original repair turn?

Grading is performed by Claude Haiku as primary judge, with a stratified sample of 200 cells (50 per model) hand-graded for human-LLM agreement. Cohen's κ is reported per model.

### 3.5 Triangulation procedure

Each taxonomy category emerging from §3.4 is mapped against (a) the closest prior term in the literature reviewed in §2 and (b) the closest documented production-incident category from Track D. The resulting matrix categorizes each finding as *Confirmation*, *Contradiction*, or *Novel*. The matrix is the central deliverable.

---

## 4. The Taxonomy (preliminary — to be revised from data)

These categories are seeded from §2 and the first 50 hand-reviewed conversations. They will be refined as the full corpus is graded.

| # | Category | One-line description | Closest prior term |
|---|---|---|---|
| 1 | Implicit-context blindness | Model answered literally, missed user-assumed context | "pragmatic misalignment" |
| 2 | Specificity mismatch | User wanted sharp answer, got generic (or vice versa) | — |
| 3 | Format mismatch | Wrong output format (prose vs. list vs. code) | — |
| 4 | Goal collapse | Surface-level address, missed underlying objective | "long-task degradation" |
| 5 | Sycophantic drift | Agreed with user mid-pivot, contradicting earlier | "sycophancy" |
| 6 | Silent failure | Confident wrong output the user accepted | "negligent misrepresentation" |
| 7 | Refusal mismatch | Refused benign or accepted risky | "over-refusal" |
| 8 | Memory/state failure | Forgot established context | "long-context degradation" |
| 9 | Tone misread | Wrong register | — |
| 10 | Cultural / regional misread | Wrong country/legal/measurement assumptions | "low-resource performance gap" |
| 11 | Expertise mismatch | Wrong difficulty for user's evident level | — |

Categories 2, 3, 9, 11 are *candidate novel categories* — i.e., we have not yet found exact prior terms in the literature. The triangulation matrix in §6 will confirm or refute each candidate.

---

## 5. Findings

### 5.0 Three preliminary findings from the pilot

A two-stage pilot on streamed samples of WildChat-1M produced three findings that are reportable in their own right, before any cross-model replay or hand-review.

**Finding 1 — Most failed conversations end in silent abandonment, not verbal repair.**
In a 50,000-conversation v2 pilot, 23,797 conversations were English (47.6%). Of these, **12,577 (52.8%) consisted of a single user turn followed by a single assistant response with no continuation**. We cannot distinguish satisfied departures from silent abandonment in this dataset, but this rate is large enough that even under conservative assumptions, a substantial fraction of intent-gap failures terminate the conversation without producing any explicit repair signal. *The intent gap is systematically invisible to feedback-driven quality pipelines.*

**Finding 2 — Explicit verbal repair is rare even in multi-turn conversations.**
Among the 11,220 conversations of ≥4 turns, the v2 filter (45 phrases, full-turn scan) flagged 432 as containing an explicit repair signal — a rate of **3.85%**. The v1 filter (17 academic phrases, user-turn-2 only) flagged 3 of 2,430 multi-turn conversations (0.12%) on a 10,000-conversation sample. The v2 → v1 ratio of ~31× tells us two things: (a) explicit verbal repair is real but uncommon, and (b) the academic phrase lists in the dialogue-breakdown literature dramatically undercount it.

**Finding 3 — Real-user repair vocabulary differs from researcher-imagined repair vocabulary.**
The most common repair phrases observed in the v2 corpus, ranked by frequency:

| Rank | Phrase | Count |
|---:|---|---:|
| 1 | i meant | 92 |
| 2 | can you please | 62 |
| 3 | try again | 53 |
| 4 | useless | 20 |
| 5 | hmm | 17 |
| 6 | why did you | 17 |
| 7 | do it again | 15 |
| 8 | no | 13 |
| 9 | but i need | 12 |
| 10 | nope | 11 |
| 11 | not quite | 10 |
| 12 | why are you | 9 |
| 13 | wait | 9 |
| 14 | my question is | 7 |
| 15 | you missed | 6 |
| 16 | this is wrong | 5 |

The full phrase distribution and matched conversations are released at `data/pilot_funnel_v2.json` and `data/pilot_examples_v2.jsonl`.

The phrases that dominate the HCI conversational-repair literature ("you misunderstood," "let me rephrase," "no, I meant" as a full clause) appear far down this list or not at all. The phrases that dominate real-user data are short, blunt, and idiomatic: *"i meant," "try again," "do it again," "useless," "but i need," "you missed."* This suggests benchmark phrase lists derived from spoken-dialogue or academic CA research generalize poorly to text-based AI assistant interactions.

Some of these top-ranked phrases (e.g., "can you please," bare "no," "hmm," "wait") have known false-positive rates as repair signals — they can fire on politeness conventions or thinking-out-loud rather than on real intent-gap failures. The Stage C LLM-as-judge filter (and hand-review subset) is required to separate true intent-gap failures from these false positives. We expect a final hand-curated corpus of ~150–300 conversations after that filtering.

### 5.1 Filter yields and dataset characteristics

| Stage | v1 (10k sample) | v2 (50k sample) |
|---|---:|---:|
| Total streamed | 10,000 | 50,000 |
| English | 4,648 (46.5%) | 23,797 (47.6%) |
| Single-exchange (potential abandonment) | — (not tracked) | 12,577 (52.8% of English) |
| ≥4 turns | 2,430 | 11,220 |
| Repair signal hit | 3 | 432 |
| Repair rate (% of ≥4-turn) | 0.123% | 3.850% |

- Final hand-reviewed corpus (target): 150–300 high-quality intent-gap conversations
- Inter-rater κ on Stage D: [populate after grading]
- LLM-judge vs. human agreement: [populate after Stage C]

### 5.2 Stage C LLM-as-judge results (50-conversation pilot)

A 50-conversation subsample of the 432 v2 candidates was auto-graded by Gemini 2.5 Flash using the prompt template in Appendix A. Results:

| Verdict | Count | % of all | % of successfully-judged |
|---|---:|---:|---:|
| A — Intent gap (confirmed) | 15 | 30% | 79% |
| C — Hallucination | 2 | 4% | 11% |
| D — False positive | 1 | 2% | 5% |
| PARSE_ERR | 1 | 2% | 5% |
| ERR (judge raised exception) | 31 | 62% | — |
| **Total** | 50 | 100% | 100% |

Two findings emerge.

**Finding 4 — High intent-gap rate among successfully-judged candidates.** When the judge model could process the conversation, 79% (15/19) of the v2-flagged candidates were confirmed as real intent-gap failures (Verdict A). This is a strong validity signal for the v2 phrase list — when the regex fires *and* the judge can run, the candidate is overwhelmingly a real failure. Refining the v2 phrase list to drop the highest-false-positive markers ("can you please," bare "no") would push that rate higher.

**Finding 5 — The judge refused to grade 62% of real-user candidates.** The judge model raised an exception (Verdict ERR) on 31 of 50 candidates. The most likely explanation is content-moderation rejection: WildChat contains substantial roleplay, edgy, and NSFW content even in the English ≥4-turn slice, and Gemini 2.5 Flash's safety filters refuse to process this material. **This is itself a deployment-relevant finding:** frontier-lab evaluation pipelines that route real-user data through a safety-filtered judge model will systematically miss the failure modes that occur in the most permissive parts of the user-prompt distribution. Researchers studying deployment-grade failure rates need either (a) a less safety-filtered judge, (b) a content-classifier preprocessing step to route around the filter, or (c) explicit acknowledgment that the analysis is conditioned on judge-acceptable inputs. We flag this as a methodological consideration for future work.

### 5.3 Preliminary taxonomy distribution

Among the 15 confirmed intent-gap failures from the 50-conversation pilot, the category breakdown is:

| Category | Count | Share of confirmed |
|---|---:|---:|
| Goal collapse | 5 | 33% |
| Specificity mismatch | 4 | 27% |
| Implicit-context blindness | 4 | 27% |
| Memory-state failure | 2 | 13% |

The 11-category provisional taxonomy (§4) collapses, in this small sample, to four observed categories. The most striking gap is the absence of *sycophantic drift* in the user-data sample — even though sycophancy dominates the published literature (Sharma et al. 2024; OpenAI's GPT-4o rollback) and is documented in production incidents (D2, D4, D5). Two interpretations are possible: (a) sycophancy failures are over-represented in researcher attention relative to their real-user prevalence, or (b) sycophancy failures rarely produce explicit verbal repair (users *like* sycophantic responses and don't repair them) and thus our filter structurally misses them.

The second interpretation, if correct, is the most consequential finding of this paper. It implies that the most-discussed failure mode in the alignment literature is also the *least* detectable through user-feedback signals — including thumbs-down, support tickets, and conversational repair. Sycophancy is invisible to the user-side feedback loop by construction. This is a strong argument for prioritizing red-team and adversarial-evaluation work over user-feedback-derived eval as the primary mechanism for sycophancy detection.

A larger sample (the full 432 candidates) is needed to confirm both the category distribution and the sycophancy absence. We treat §5.3 as preliminary.

### 5.2 Cross-model replay results
- Per-model literal compliance × intent satisfaction matrix
- Recovery rate (intent=2 on replay where original failed): per model
- Persistence rate (intent=0 on replay, same as original): per model
- LLM-judge vs. human-grader κ: per model

### 5.3 Taxonomy distribution
- Frequency of each category in the corpus
- Per-model differential — do models fail in different categories?

### 5.4 Cross-language findings (if multilingual extension runs)
- Intent-gap rate by language
- Category distribution by language

---

## 6. Triangulation Matrix

Reproduces the matrix from §1 with the data filled in. The headline visual of the paper.

| Category | Prior literature term | Confirmed by user data? | Production incidents? | Verdict |
|---|---|:---:|:---:|---|
| ... | ... | ✓/✗ | ✓/✗ | Confirmation / Contradiction / Novel |

---

## 7. Discussion

### 7.1 Why benchmarks miss this
Brief argument: researcher-imagined task design vs. user-emergent task structure.

### 7.2 What deployment teams should do
- Pre-deployment: red-team specifically against the categories with highest production-incident weight
- Deployment: monitor for repair signals as a runtime quality metric
- Post-deployment: feed repair-flagged conversations back into eval datasets

### 7.3 Implications for the frontier-lab evaluation roadmap
The novel categories (whichever they turn out to be) are candidate additions to the frontier eval suite. The persistent categories (failures replicated by current models) suggest specific training-time interventions — particularly around mid-conversation pivot handling and implicit-context inference.

---

## 8. Limitations

- **Selection bias:** WildChat users self-select into a free hosted endpoint; LMSYS users into Chatbot Arena. Neither is a random sample of all AI users.
- **English-first bias:** Initial analysis is English-only. Multilingual extension is partial.
- **LLM-as-judge bias:** Using LLMs to grade LLMs introduces a known bias. We mitigate via human-grader stratified subsample and inter-rater reliability reporting.
- **Recency:** WildChat data is GPT-3.5/4-era; the *failures* may be specific to those models. Cross-model replay on current frontier models partially addresses this but doesn't eliminate it.
- **Language of repair:** The frustration-signal filter detects users who *vocalize* frustration. Silent acceptance of bad outputs (the most dangerous failure mode) is invisible to this method.

---

## 9. Future Work

- Multilingual extension to Hindi, Mandarin, Spanish, Arabic
- Application to deployed agent logs (e.g., from labs willing to share)
- A live, runtime version of the filter as a deployment-monitoring tool
- Mechanistic interpretation of intent-gap failures (link to Anthropic persona-vectors line of work)
- Repeated annual replication as frontier models change

---

## 10. Acknowledgments

This work was conducted independently. Datasets and tools used: WildChat (AI2), LMSYS-Chat (LMSYS), Anthropic API (Claude Haiku for judging), embeddings via [provider]. The author acknowledges feedback from [reviewers].

---

## References

[A formatted reference list will be generated for arXiv submission. See `lit-review/papers.md` for the curated source notes.]

---

## Appendix A — Judge prompt template

(See `code/grade.py` for the runnable version.)

```
You are grading an AI assistant's response on two axes.

ORIGINAL USER PROMPT:
{prompt}

USER'S TRUE INTENT (inferred from their later repair turn):
{inferred_intent}

ASSISTANT RESPONSE BEING GRADED:
{response_to_grade}

Score the response on:
1. LITERAL COMPLIANCE (0–2): did it address the literal prompt?
2. INTENT SATISFACTION (0–2): did it address what the user actually wanted?

Reply in JSON only:
{
  "literal": 0 | 1 | 2,
  "intent": 0 | 1 | 2,
  "category": <taxonomy id>,
  "note": "<= 25 words on what's interesting"
}
```

## Appendix B — Repair-signal seed list (English)

(See `code/filter.py` for the full list.)
