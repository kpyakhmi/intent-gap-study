# Curated Literature Review

> ~20 papers across global research institutes documenting LLM failure modes, real-user evaluation, conversational repair, and deployment gaps. Each entry includes citation, region, two-line takeaway, and how it maps to our taxonomy.

---

## A. Real-user conversation corpora (the data foundation)

### A1. WildChat: 1M ChatGPT Interaction Logs in the Wild
- **Authors / Institute:** Zhao, Ren, Tao, Chiang, Choi, et al. — Allen Institute for AI (AI2), University of Washington — US
- **Venue / Year:** ICLR 2024 (Spotlight)
- **Link:** https://arxiv.org/abs/2405.01470
- **Takeaway:** 1M ChatGPT (GPT-3.5/4) conversations with 2.5M turns from public hosted endpoint. Unique features vs. prior corpora: ambiguous user requests, code-switching, topic-switching, political/toxic content. Includes country-level metadata.
- **Maps to our work:** Primary data source. We use the non-toxic subset and filter for repair signals.
- **Limitation we inherit:** Users self-select into using a free hosted ChatGPT mirror; not a random sample of all AI users.

### A2. LMSYS-Chat-1M: A Large-Scale Real-World LLM Conversation Dataset
- **Authors / Institute:** Zheng, Chiang, Sheng, Li, Zhuang, et al. — UC Berkeley, LMSYS — US
- **Venue / Year:** ICLR 2024
- **Link:** https://arxiv.org/abs/2309.11998
- **Takeaway:** 1M conversations across 25 LLMs, 210K users, 150+ languages, collected from Chatbot Arena (Apr–Aug 2023).
- **Maps to our work:** Secondary data source. Lets us check if intent-gap failures are model-specific or general across the model frontier circa 2023.

---

## B. Failure-mode taxonomies and surveys

### B1. Towards Understanding Sycophancy in Language Models
- **Authors / Institute:** Sharma, Tong, Korbak, Duvenaud, et al. — Anthropic — US
- **Venue / Year:** ICLR 2024 (May 2025 update)
- **Link:** https://arxiv.org/abs/2310.13548
- **Takeaway:** RLHF-trained models systematically prefer responses that match user beliefs over truthful ones across five frontier assistants and four task types. Both human raters and preference models prefer convincingly-written sycophantic answers a non-trivial fraction of the time.
- **Maps to our work:** Direct feed into the *Sycophantic drift* category. Predicts that mid-conversation user-pivot scenarios should produce systematic intent-gap failures.

### B2. Sycophancy to Subterfuge: Investigating Reward-Tampering in Frontier Language Models
- **Authors / Institute:** Anthropic Alignment Team — US
- **Link:** https://www.anthropic.com/research/reward-tampering
- **Takeaway:** Sycophancy generalizes to checklist alteration and reward-function modification under the right training conditions. Sycophancy is a *gateway* failure mode, not a terminal one.
- **Maps to our work:** Strengthens the case that the *Sycophantic drift* and *Goal collapse* categories aren't isolated quirks but signs of a deeper alignment gap.

### B3. Persona Vectors: Monitoring and Controlling Character Traits in Language Models
- **Authors / Institute:** Anthropic — US
- **Link:** https://www.anthropic.com/research/persona-vectors
- **Takeaway:** Latent persona vectors can be extracted that correspond to traits like sycophancy. Suggests the failure has a stable representational signature, not just a behavioral one.
- **Maps to our work:** Future-work hook — could mechanistically explain why intent-gap failures cluster.

---

## C. Conversational repair / dialogue breakdown

### C1. Detect, Explain, Escalate: Sustainable Dialogue Breakdown Management for LLM Agents
- **Authors / Institute:** [authors per arXiv listing] — 2025
- **Link:** https://arxiv.org/abs/2504.18839
- **Takeaway:** Fine-tunes an 8B model with teacher-generated reasoning traces as a real-time breakdown detector across English and Japanese dialogues. Monitor-escalate pipeline reduces inference cost 54% while maintaining classification quality.
- **Maps to our work:** Their breakdown-detection task is the closest existing work to our frustration-signal filter. We differ in (a) using public corpora rather than crowd-sourced dialogues, (b) labeling intent-gap specifically rather than general breakdowns, and (c) producing a typed taxonomy rather than a binary classifier.

### C2. The Art of Repair in Human-Agent Conversations: A Taxonomy of Repair Strategies
- **Authors / Institute:** [as per ResearchGate listing] — 2025
- **Link:** https://www.researchgate.net/publication/395190410
- **Takeaway:** Builds a taxonomy of repair strategies used by both users and LLM-based agents. Distinguishes social, disclosure, information, and solving strategies, and asks (repeating questions, requesting rephrasing, soliciting details).
- **Maps to our work:** Provides the linguistic vocabulary for repair signals. We borrow some of their categories for our seed-phrase list.

### C3. System and User Strategies to Repair Conversational Breakdowns of Spoken Dialogue
- **Authors / Institute:** Aljamdi et al. — University of Strathclyde — UK
- **Venue / Year:** CUI 2024
- **Link:** https://strathprints.strath.ac.uk/89541/
- **Takeaway:** Field study of repair strategies in spoken dialogue systems. Identifies asymmetries: users repair more than systems do; users default to repetition and rephrasing.
- **Maps to our work:** Validates that the repair signals we filter on are real linguistic phenomena, not artifacts of specific dataset.

---

## D. Multilingual and cross-cultural evaluation

### D1. MEGAVERSE: Benchmarking LLMs Across Languages, Modalities, Models and Tasks
- **Authors / Institute:** Ahuja, Aggarwal, et al. — Microsoft Research India — India
- **Venue / Year:** NAACL 2024
- **Link:** https://arxiv.org/abs/2311.07463
- **Takeaway:** 22 datasets across 83 languages including low-resource African languages. Larger models outperform smaller models on low-resource languages, but data contamination is widespread. GPT-4 is the cross-lingual frontier (as of mid-2024) but multilingual eval is contaminated.
- **Maps to our work:** Anchors any multilingual extension we run. Implies that intent-gap rate is likely worse in low-resource languages.

### D2. Indic LLM-Arena and MILU
- **Authors / Institute:** AI4Bharat — IIT Madras — India
- **Year:** 2025
- **Link:** https://ai4bharat.iitm.ac.in/areas/llm
- **Takeaway:** Crowd-sourced human-in-the-loop benchmark for Indian languages, code-mixing (Hinglish, Tanglish), cultural context, and safety. MILU benchmark spans 11 Indic languages, 8 domains, 42 subjects. GPT-4o tops at 72% accuracy; current LLMs struggle most on culturally-relevant Arts/Humanities and Law/Governance.
- **Maps to our work:** Documents the cultural-misread failure category empirically; supports our *Cultural / regional misread* taxonomy item.

---

## E. Agent capability evaluation and deployment gap

### E1. Measuring AI Ability to Complete Long Tasks (Time Horizon)
- **Authors / Institute:** METR — US
- **Year:** 2025
- **Link:** https://arxiv.org/html/2503.14499v1 (METR research)
- **Takeaway:** Proposes "task length" as a unifying metric. The 50% time horizon for AI agents has been growing exponentially since 2019 with ~7-month doubling time.
- **Maps to our work:** Predicts that intent-gap failures will manifest most in *long* multi-turn tasks. Our filter uses 2-turn windows; a stretch finding is to compare intent-gap rates by conversation length.

### E2. Algorithmic vs. Holistic Evaluation
- **Authors / Institute:** METR — US
- **Year:** August 2025
- **Link:** https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/
- **Takeaway:** Early-2025 agents on real open-source repos often produce *functionally correct* code that is *not usable as-is* due to test coverage, formatting, lint, or quality issues. Automatic scoring overestimates real-world performance.
- **Maps to our work:** Direct precedent for our central thesis — benchmark scores systematically overestimate deployment readiness. We extend this from code to general user tasks.

### E3. METR Developer Productivity RCT
- **Authors / Institute:** METR — US
- **Year:** 2025
- **Takeaway:** Randomized controlled trial showing experienced open-source developers using early-2025 AI tools take *19% longer* than without. Even competent users + capable tools = net negative productivity in some real settings.
- **Maps to our work:** Empirical evidence that the intent gap costs measurable time in expert hands. Our taxonomy provides candidate mechanisms.

### E4. Forecasting Frontier Language Model Agent Capabilities
- **Authors / Institute:** Apollo Research — UK/Germany
- **Year:** 2025
- **Link:** https://www.apolloresearch.ai/science/forecasting-frontier-language-model-agent-capabilities/
- **Takeaway:** Forecasts SWE-Bench Verified at 54% (low elicitation) to 87% (SOTA) by start of 2026 for non-specialized agents. The gap between benchmark performance and deployment performance is forecast to *widen* even as benchmark performance saturates.
- **Maps to our work:** Provides the timing case — intent-gap research becomes *more* important as benchmark performance saturates.

### E5. AISI Frontier AI Trends Report 2025
- **Authors / Institute:** UK AI Security Institute (AISI) — UK
- **Year:** 2025
- **Link:** https://www.aisi.gov.uk/research/aisi-frontier-ai-trends-report-2025
- **Takeaway:** Cyber capability went from 9% (apprentice tasks, late 2023) → 50% (2025); first model passed expert-level cyber tasks in 2025. Documents specific deployment-stage findings frontier labs ship to AISI pre-release.
- **Maps to our work:** Government-backed validation that pre-deployment evaluation surfaces failure modes that public benchmarks don't catch. Strong precedent for the institutional value of our work.

---

## F. Production deployment incidents (Track D)

### F1. Moffatt v. Air Canada (2024 BCCRT 149)
- **Forum / Date:** British Columbia Civil Resolution Tribunal, February 14, 2024
- **Authors of analysis:** McCarthy Tétrault, UBC Allard School of Law Review, Springer AI & Society
- **Links:**
  - https://www.mccarthy.ca/en/insights/blogs/techlex/moffatt-v-air-canada-misrepresentation-ai-chatbot
  - https://link.springer.com/article/10.1007/s00146-024-02096-7
- **Facts:** Air Canada's chatbot told a customer he could apply for a bereavement-fare refund retroactively; the airline's actual policy required pre-application. Tribunal found Air Canada liable for $812 CAD; rejected the argument that the chatbot was a "separate entity."
- **Maps to our work:** Canonical real-world example of *implicit-context blindness* + *silent failure* — model produced confident, fluent, internally-consistent advice that was wrong. User accepted it. Damage was contractual.

### F2. LangChain State of AI Agents 2026
- **Authors / Institute:** LangChain — US
- **Year:** 2026
- **Link:** https://www.langchain.com/state-of-agent-engineering
- **Findings:** 57% of orgs have agents in production; 78% pilot but only 14% reach production scale; quality is the #1 barrier (32%); observability and evals are the lowest-rated parts of the stack.
- **Maps to our work:** Frames the market context — quality (i.e., the kinds of failures we taxonomize) is the gating issue, and the existing eval/observability stack is the bottleneck.

### F3. AI Agent Production Failure Analyses (DigitalApplied 2026)
- **Year:** 2026
- **Link:** https://www.digitalapplied.com/blog/88-percent-ai-agents-never-reach-production-failure-framework
- **Findings:** 88% of AI agents never reach production. Five most-cited root causes: integration complexity, inconsistent output quality at volume, absence of monitoring tooling, unclear organizational ownership, insufficient domain training data.
- **Maps to our work:** Output-quality-at-volume is exactly what intent-gap rate measures. We provide the missing taxonomy that tells deployment teams *which* quality issues to fix first.

### F4. The 2025 AI Agent Index
- **Authors / Institute:** [academic consortium] — 2026
- **Link:** https://arxiv.org/html/2602.17753v1
- **Takeaway:** Documents technical and safety features of deployed agentic AI systems. Most developers share little information about safety, evaluations, and societal impacts.
- **Maps to our work:** Validates the public-data approach — labs aren't disclosing internal data, so independent corpora analysis is the only way to study deployment-grade failures at scale.

---

## G. Curated reservoir (papers to read if Track B has more time)

These don't make the core 20 but are worth scanning:

- Stanford CRFM HELM transparency reports (US) — holistic benchmarking framework
- BIG-bench (Google + collaborators) — 200+ task benchmark
- Park et al. — *AI Deception: A Survey* (MIT)
- Liao et al. — HCI work on conversational AI breakdowns
- Luger & Sellen 2016 — *"Like having a really bad PA"*: foundational HCI critique
- DBDC (Dialogue Breakdown Detection Challenge) series — older benchmark family
- C-Eval, AGIEval (Tsinghua / Shanghai AI Lab) — Chinese evaluation
- MBZUAI publications on Arabic LLM evaluation
- AISI (US) reports — once published
- OpenAI o3 / o4-mini system cards — official failure-mode disclosures

---

## Comparison matrix (template — to be populated by Day 7)

| Our taxonomy category | Closest prior term | Source(s) | Confirmation / Contradiction / Novel |
|---|---|---|---|
| Implicit-context blindness | "pragmatic misalignment" | Detect/Explain/Escalate (C1) | Confirmation |
| Specificity mismatch | — | — | Novel (candidate) |
| Format mismatch | — | — | Novel (candidate) |
| Goal collapse | "long-task degradation" | METR Time Horizon (E1) | Partial confirmation |
| Sycophantic drift | "sycophancy" | Anthropic (B1, B2) | Confirmation |
| Silent failure | "negligent misrepresentation" | Moffatt v. Air Canada (F1) | Confirmation in deployment |
| Refusal mismatch | "over-refusal" / "compliance gap" | UK AISI (E5) | Confirmation |
| Memory/state failures | "long-context degradation" | various | Partial confirmation |
| Tone misread | — | HCI work (Luger & Sellen) | Partial confirmation |
| Cultural / regional misread | "low-resource performance gap" | MEGAVERSE (D1), AI4Bharat (D2) | Confirmation |
| Expertise mismatch | — | — | Novel (candidate) |

(Filled in after Layer 1 grading; this matrix is the visual centerpiece of the paper.)
