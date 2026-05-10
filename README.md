# The Intent Gap

**A taxonomy of real-user failure modes in frontier AI agents, mined from 1M+ public conversations and triangulated against the global research literature.**

---

## TL;DR

Every public benchmark for AI agents — GAIA, OSWorld, AgentBench, GDPval, BrowseComp, SWE-bench — is **researcher-imagined**. Tasks are written in clean declarative form by AI researchers, in a room, with ground-truth answers fixed in advance.

Real users don't behave that way. They assume context, change their minds, contradict themselves, abandon, and phrase requests in ways no benchmark prompt has ever been written. Benchmarks systematically miss the most common deployment-relevant failure mode: **the intent gap** — cases where the model literally answered the prompt but missed what the user actually wanted.

This project mines public real-user corpora (WildChat-1M, LMSYS-Chat-1M), surfaces ~300–500 high-quality intent-gap conversations using a reproducible **frustration-signal filter**, replays them across four current frontier models, and triangulates the resulting taxonomy against ~20–30 published failure taxonomies from research institutes worldwide (US, UK, EU, Asia, MENA).

**The contribution is the labeled subset, the taxonomy, the filter pipeline, and the triangulation matrix — not a leaderboard.**

---

## Headline preliminary findings

From a 50,000-conversation v2 pilot on WildChat-1M, plus a 50-candidate Stage C grading subsample with Gemini 2.5 Flash:

> **52.8%** of English real-user AI conversations end after a single exchange — likely silent abandonment after intent-gap failure, invisible to feedback-driven quality pipelines.
>
> **3.85%** of multi-turn conversations contain an explicit verbal repair signal under a 45-phrase filter. The intent gap exists, but most users do not verbalize it.
>
> **~31× hit-rate gap** between v1 (17 academic phrases, 0.12%) and v2 (45 natural-language phrases, 3.85%). The dialogue-breakdown literature undercounts real-world repair by more than an order of magnitude because its phrase lists are researcher-imagined.
>
> **79% of successfully-judged candidates** were confirmed real intent-gap failures, with a four-category distribution: *goal collapse* (33%), *specificity mismatch* (27%), *implicit-context blindness* (27%), *memory-state failure* (13%).
>
> **Sycophantic drift was absent** from the user-data sample, despite dominating the alignment literature and the production-incident record. Two interpretations are possible; the consequential one is that **sycophancy is structurally invisible to user-feedback signals** because users *like* sycophantic responses and don't repair them. If true, this is an argument for prioritizing red-team work over user-feedback-derived evaluation for sycophancy detection.
>
> **62% judge-refusal rate.** Gemini 2.5 Flash's safety filters refused to grade 31 of 50 real-user candidates — most likely a moderation rejection on WildChat's edgy/NSFW content. *Frontier-lab eval pipelines that route real-user data through safety-filtered judges systematically miss failure modes in the most permissive parts of the user-prompt distribution.*

These are preliminary on a 50-conversation subsample. Full 432-candidate grading, hand-spot-check, and cross-model replay are next.

---

## Why this matters for AI labs

The 2026 deployment data is unambiguous: 78% of enterprises run AI agent pilots, only 14% reach production scale ([LangChain State of AI Agents 2026](https://www.langchain.com/state-of-agent-engineering)). Quality is the top barrier cited by 32% of teams. Frontier labs need to know *which specific failure modes* are blocking deployment — not aggregate benchmark scores.

This work names those modes, grounds them in real user data, and validates them against the published research. It's intended for deployment, applied research, evaluation, and safety teams at frontier labs.

---

## Repo structure

```
intent-gap-study/
├── README.md                  ← you are here
├── paper/                     ← the writeup
│   └── intent_gap.md
├── code/                      ← runnable filter + replay pipeline
│   ├── filter.py
│   ├── replay.py
│   ├── grade.py
│   └── requirements.txt
├── data/                      ← curated intent-gap dataset (released after paper publishes)
│   ├── schema.md
│   └── README.md
├── lit-review/                ← curated 20–30 papers across global institutes
│   ├── papers.md
│   └── taxonomy_matrix.md
├── incidents/                 ← production failure incidents corpus (Track D)
│   └── README.md
└── outreach/                  ← X thread, LessWrong post, hiring-manager target list
    ├── x_thread.md
    ├── lesswrong_post.md
    └── outreach_targets.md
```

---

## Methodology in one paragraph

We extract conversations from WildChat-1M and LMSYS-Chat-1M where the user's second turn contains a *conversational repair signal* — phrases like "no, I meant," "you misunderstood," "let me rephrase." We pass each candidate through an embedding similarity check (low match between user's true intent and the assistant's prior response) and an LLM-as-judge confirmation that the failure is an intent gap rather than a refusal, hallucination, or jailbreak. We hand-review the surviving subset, label with a multi-axis taxonomy, replay the original prompt across Claude, GPT, Gemini, and one open model, and grade each replay on two axes: literal compliance and intent satisfaction. Inter-rater reliability (Cohen's kappa) is reported. The full filter pipeline, judge prompt, grading rubric, and labeled dataset are released here under permissive licenses.

See [`paper/intent_gap.md`](paper/intent_gap.md) for the full method and findings.

---

## Three-layer design

The contribution lives in the cross-validation between three layers:

1. **Layer 1 — User behavior.** What users actually do, mined from WildChat and LMSYS.
2. **Layer 2 — Institutional research.** What ~20–30 papers across global research institutes have already documented about LLM failures.
3. **Layer 3 — Production incidents.** Real-world AI failures that have caused documented business consequences (lawsuits, regulator filings, public post-mortems).

Findings live in three buckets: **confirmations** (user data validates the literature), **contradictions** (literature predicts something user data doesn't show, or vice versa), and **novel gaps** (failures the user data shows that no institutional paper has named yet). The novel-gaps bucket is the contribution.

---

## Status

| Component | Status |
|---|:---:|
| Research scope | ✅ locked |
| Filter pipeline (code) | 🟡 draft |
| Lit review | 🟡 in progress |
| Production incidents corpus | 🟡 in progress |
| Data mining + grading | ⬜ not started |
| Cross-model replay | ⬜ not started |
| Paper draft | 🟡 skeleton |
| Publication | ⬜ pending |

---

## Reproducing this work

```bash
git clone https://github.com/<USER>/intent-gap-study
cd intent-gap-study
pip install -r code/requirements.txt
python code/filter.py --dataset wildchat --output data/candidates.jsonl
python code/replay.py --input data/intent_gap_corpus.jsonl --models claude,gpt,gemini,llama
python code/grade.py --input data/replays.jsonl --output data/graded.jsonl
```

Full instructions in [`code/README.md`](code/README.md).

---

## Citations

If this work is useful to you, please cite:

```bibtex
@misc{yakhmi2026intentgap,
  author = {Yakhmi, Kanupriya},
  title = {The Intent Gap: A Taxonomy of Real-User Failure Modes in Frontier AI Agents},
  year = {2026},
  note = {arXiv preprint},
}
```

---

## Licenses

- **Code:** MIT
- **Dataset:** CC BY-NC 4.0 (consistent with WildChat / LMSYS source licenses)
- **Paper:** CC BY 4.0

---

## Contact

Kanupriya Yakhmi — [LinkedIn](https://www.linkedin.com/in/kanupriyayakhmi/)

Issues and PRs welcome. Especially interested in: (a) extensions to additional languages, (b) replications on other public corpora, (c) pointers to relevant research from non-Western institutes.
