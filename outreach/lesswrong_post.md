# LessWrong / Alignment Forum crosspost — draft

> Long-form, discussion-bait framing. ~1500 words. The thread on X drives traffic;
> the LessWrong post is where the conversation happens.

---

# The Intent Gap: A Failure Mode That Frontier Benchmarks Systematically Miss

**TL;DR.** I mined 1M+ public real-user AI conversations for cases where the
model literally answered the prompt but missed what the user actually wanted —
a failure mode I'm calling the *intent gap*. Used a three-stage filter
(regex → embedding → LLM-as-judge) keyed on conversational repair signals
("no, I meant," "you misunderstood"). Built a taxonomy from the surviving
~[N] conversations, replayed each across four current frontier models, and
triangulated the result against ~25 papers from research institutes worldwide
plus ~15 documented production-failure incidents. Filter code, labeled corpus,
grading rubric, paper draft all open on GitHub. Looking for feedback before
arXiv submission.

---

## Why I think this is worth your time

There's been a steady drumbeat of independent capability evaluation work over
the past two years — METR's Time Horizon, Apollo's forecasting, UK AISI's
Frontier AI Trends — all of which document benchmark capability rising on an
exponential curve. Meanwhile LangChain's 2026 industry survey reports that 78%
of enterprises run agent pilots and only 14% reach production scale. Quality is
the #1 cited barrier.

There's a gap somewhere between "benchmark says it's smart" and "users say it's
not useful enough to ship."

This post is about *one specific shape* of that gap, called out by a *specific
filter* that operates on *publicly available data*. I think the methodology
generalizes.

## The filter

A user who's been mis-served by an AI assistant repairs themselves on the next
turn. They say "no, I meant," "you misunderstood," "actually I wanted X." These
are *conversational repair signals* in HCI/CA terms (cf. Schegloff 1977,
Aljamdi et al. CUI 2024).

I curated 80 English repair phrases as Stage A. Stage B is a cosine-similarity
check between (user prompt + repair turn) and the assistant's response —
similarity below 0.55 suggests the response addressed something different from
the user's true intent. Stage C is an LLM judge that classifies the failure
into one of {refusal, hallucination, intent gap, other dissatisfaction, false
positive} — only "intent gap" candidates survive.

Stage D is hand review by me, with a 100-conversation second-grader subset for
inter-rater reliability. Cohen's κ reported in the paper.

Funnel from a 1M-conversation source corpus: ~30k Stage A → ~3k Stage C →
~500 hand-reviewed.

## What's in the corpus

After grading the cross-model replays, the failures cluster into eleven
preliminary categories. Roughly:

1. **Implicit-context blindness** — model answered literally, missed user-assumed context
2. **Specificity mismatch** — generic where user wanted sharp, or vice versa
3. **Format mismatch** — wrong output shape
4. **Goal collapse** — addressed surface request, missed underlying objective
5. **Sycophantic drift** — agreed with mid-conversation user pivot, contradicting earlier instructions
6. **Silent failure** — confident wrong output the user accepted
7. **Refusal mismatch** — refused benign or accepted risky
8. **Memory/state failures** — forgot established context
9. **Tone misread** — wrong register
10. **Cultural / regional misread** — wrong country/legal/measurement assumptions
11. **Expertise mismatch** — wrong difficulty for user's evident level

Some have prior names in the literature; some don't. The triangulation matrix
in the paper places each category against the closest published term and marks
it as Confirmation / Partial Confirmation / Novel.

## The cross-model replay

For each curated conversation, I replayed the first user turn through Claude,
GPT, Gemini, and an open model (Llama). Two-axis grading: *literal compliance*
and *intent satisfaction*, both 0–2.

The interesting cells are (literal=2, intent=0) — where the model did the
prompt, but not the user.

The headline numbers will be in the paper. I'll preview here that **persistent
intent-gap categories exist** across all four models — i.e., a year of training
has not closed certain specific gaps. Some categories have improved
considerably. The pattern of which improved and which didn't is, I think, the
most interesting finding.

## Triangulation

Layer 1: user data (this study).
Layer 2: institutional research literature — ~25 papers across Anthropic
(sycophancy), AI2 (WildChat itself), AI4Bharat (cultural eval), MEGAVERSE
(multilingual contamination), METR (long-task degradation), Apollo Research
(forecasting), UK AISI (pre-deployment), DeepMind / OpenAI / FAIR / MSR /
Tsinghua / Shanghai AI Lab / MBZUAI.

Layer 3: documented production-failure incidents (Moffatt v. Air Canada being
the canonical adjudicated case; others in the repo).

Findings live in three buckets — Confirmation, Contradiction, Novel. The Novel
bucket is the contribution.

## Limitations I want to flag

- **Selection bias.** WildChat users self-select into a free hosted GPT mirror;
  LMSYS users into Chatbot Arena. Neither is a random sample.
- **Recency.** WildChat is GPT-3.5/4-era; the original failures may be specific
  to those models. Cross-model replay partially controls for this.
- **Silent acceptance.** The filter sees users who *vocalize* their
  frustration. Users who silently accept bad outputs are invisible — and that's
  arguably the most dangerous category.
- **LLM-as-judge bias.** Using LLMs to grade LLMs has well-known issues. I
  mitigate via a stratified human-graded subset and report human-LLM agreement.
- **English-first.** Multilingual extension is partial in this draft.

## What I'm asking for

1. **Methodology critique.** Does the filter make sense? What's a category I'm
   missing? Where would you tighten the definition of "intent gap"?
2. **Pointers to prior work I missed.** I deliberately read across global
   institutes and weighted non-US work, but I'm sure I'm missing relevant
   threads. Especially curious about non-English HCI/dialogue work.
3. **Operational interest.** If you work on deployment / eval / safety at a
   frontier lab, what would make this dataset more useful to you? I'll tune the
   v1 release for what you'd actually consume.

GitHub: [link]
arXiv submission target: [date]

— Kanupriya
