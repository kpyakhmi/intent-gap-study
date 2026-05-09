# Taxonomy Triangulation Matrix

> The headline visual of the paper. Maps each user-data taxonomy category against
> (a) the closest prior literature term and (b) the closest documented production
> incident. Each cell tagged Confirmation / Partial / Novel.

| # | Our category | One-line description | Closest literature term | Source(s) | Production incident | Verdict |
|---|---|---|---|---|---|---|
| 1 | Implicit-context blindness | Model answered literally, missed user-assumed context | "pragmatic misalignment" | C1 (Detect/Explain/Escalate, 2025) | Moffatt v. Air Canada (D1) | **Confirmation** |
| 2 | Specificity mismatch | Generic where user wanted sharp, or vice versa | — | — | — | **Novel (candidate)** |
| 3 | Format mismatch | Wrong output shape (prose vs list vs code) | — | — | — | **Novel (candidate)** |
| 4 | Goal collapse | Surface-level address, missed underlying objective | "long-task degradation" | E1 (METR Time Horizon) | LangChain 2026 quality block | **Partial confirmation** |
| 5 | Sycophantic drift | Agreed with mid-pivot, contradicting earlier instructions | "sycophancy" | B1 (Anthropic), B2 (Reward Tampering) | — | **Confirmation** |
| 6 | Silent failure | Confident wrong output the user accepted | "negligent misrepresentation" | E2 (METR Algo vs Holistic) | Moffatt v. Air Canada (D1) | **Confirmation** |
| 7 | Refusal mismatch | Refused benign or accepted risky | "over-refusal" / "compliance gap" | E5 (UK AISI 2025) | — | **Confirmation** |
| 8 | Memory/state failure | Forgot established context | "long-context degradation" | various | — | **Partial confirmation** |
| 9 | Tone misread | Wrong register | — | HCI work (Luger & Sellen 2016) | DPD swearing chatbot (UK 2024) | **Partial confirmation** |
| 10 | Cultural / regional misread | Wrong country/legal/measurement assumptions | "low-resource performance gap" | D1 (MEGAVERSE), D2 (AI4Bharat MILU) | — | **Confirmation** |
| 11 | Expertise mismatch | Wrong difficulty for user's evident level | — | — | — | **Novel (candidate)** |

---

## How to read this

- **Confirmation:** the user-data finding agrees with what published research has named.
  The contribution here is *quantifying the rate at scale* with a reproducible filter.
- **Partial confirmation:** the literature names something nearby but not the same thing.
  The contribution here is *sharpening the term* and providing labeled examples.
- **Novel (candidate):** no published institutional taxonomy has named this category.
  These are the most interesting findings — but they need the most defense in the paper
  (arguing convincingly that no prior term covers them).

---

## Headline numerical claim (template)

> Of N taxonomy categories, K are confirmed by prior institutional research,
> P are partially confirmed, and M are novel candidates. Of M novel candidates,
> Q are validated by at least one documented production incident from Track D,
> giving Q "high-confidence novel" categories.

Replace once Layer 1 grading completes.
