# X / Twitter thread — draft

> 10–12 tweets. Rule: each tweet works as a standalone if reposted. The thread
> is a story, not a list.

---

**1/**
Every public benchmark for AI agents is *researcher-imagined*. GAIA, OSWorld, AgentBench, GDPval, BrowseComp, SWE-bench — all of them. Tasks are written in clean declarative form by AI researchers, in a room.

Real users don't behave that way. So I went looking.

**2/**
I mined 1M+ public real-user conversations (WildChat, LMSYS-Chat-1M) for one specific failure mode that benchmarks systematically miss:

The model literally answered the prompt — but missed what the user actually wanted.

Call it the **intent gap**.

**3/**
You can find it cleanly because users *repair* themselves. They say "no, I meant," "you misunderstood," "let me rephrase." Those phrases are a label-free signal that the prior assistant turn whiffed.

I built a 3-stage filter (regex → embedding → LLM-as-judge) on those signals.

**4/**
After ~[N] surviving conversations, the failures cluster into [K] categories. Some have prior names in the literature:
- Sycophantic drift (Anthropic)
- Cultural misread (AI4Bharat MILU; MEGAVERSE)
- Long-context degradation (METR Time Horizon)

[M] don't. Those are the contribution.

**5/**
The killer move: I replayed the *same* prompts on current frontier models — Claude, GPT, Gemini, and one open model.

Recovery rate: [X]%. Persistence rate: [Y]%.

The persistent ones tell you what to fix. They tell you a year of training has not closed certain specific gaps.

**6/**
[Chart 1: stacked bar of categories per model — show the picture]

**7/**
Triangulation against ~25 papers from research institutes worldwide (US, UK, EU, India, China, MENA) shows: the literature has named [A]/[K] categories. [B] are confirmed; [C] are partially confirmed; [M] are new.

The new ones are where the work is.

**8/**
Production data tells the same story. Air Canada lost a tribunal case in 2024 because its chatbot confidently misrepresented bereavement-fare policy. Classic *silent failure* + *implicit-context blindness* — categories the chatbot benchmarks of 2023 didn't measure.

**9/**
LangChain's 2026 survey: 78% of enterprises pilot agents, 14% reach production. Quality is the #1 blocker.

The intent-gap rate is not an academic abstraction. It is the gating variable for whether your agent ever ships.

**10/**
Filter code, labeled dataset, grading rubric, full paper, triangulation matrix — all open on GitHub.

[link]

If you build agents and want to know which *specific* failures are eating your retention, this is for you.

**11/**
Built independently in 30 days as a non-engineer with Claude as the engine. The methodology is the moat: anyone can re-run the filter on a new corpus, in a new language, on a new model.

If you want to extend it, open an issue. If you're hiring, my email is in the repo.

**12/**
Next: multilingual extension (Hindi, Mandarin, Spanish, Arabic), then a runtime version of the filter as a deployment-monitoring tool.

If you work on agent eval at a frontier lab — pls steal this freely. That's the point.
