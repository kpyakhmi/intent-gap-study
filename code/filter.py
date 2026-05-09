"""
Frustration-signal filter for surfacing intent-gap failures in conversation corpora.

Three stages:
  Stage A  Lexical match on user-turn-2+ for repair phrases.
  Stage B  Embedding similarity check between (user prompt + repair) and assistant response.
  Stage C  LLM-as-judge confirms classification as 'intent gap' (not refusal/hallucination/jailbreak).

Usage:
    python filter.py --dataset wildchat --output ../data/candidates.jsonl
    python filter.py --dataset lmsys --output ../data/lmsys_candidates.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Iterator, Optional

# ---------- Stage A: Lexical repair signals ----------

REPAIR_PHRASES = [
    # explicit repair (high precision)
    r"no,?\s+i\s+meant",
    r"that(?:'s|\s+is)\s+not\s+what\s+i\s+(?:asked|wanted|meant)",
    r"you\s+misunderstood",
    r"you\s+missed\s+the\s+point",
    r"let\s+me\s+rephrase",
    r"let\s+me\s+clarify",
    r"i\s+think\s+you\s+misunderstood",
    r"to\s+be\s+clear,?\s+i\s+(?:want|meant|need)",
    r"actually,?\s+i\s+(?:want|meant|need)",
    r"not\s+quite\s*[—-]\s*i\s+(?:want|meant|need)",
    r"what\s+i\s+actually\s+(?:need|want|meant)",
    r"the\s+question\s+was",
    r"re-?read\s+my\s+(?:question|prompt)",
    r"that\s+wasn'?t\s+the\s+question",
    r"you\s+didn'?t\s+answer\s+my\s+question",
    r"read\s+the\s+prompt\s+again",
    r"i\s+don'?t\s+think\s+you\s+understood",

    # explicit dissatisfaction (medium precision)
    r"this\s+is\s+(?:wrong|incorrect|not\s+what\s+i'?m\s+looking\s+for)",
    r"this\s+isn'?t\s+right",
    r"this\s+doesn'?t\s+help",
    r"that(?:'s|\s+is)\s+(?:incorrect|not\s+accurate)",
    r"you\s+got\s+it\s+wrong",
    r"(?:not\s+useful|useless|unhelpful)",
    r"wrong\s+answer",
]

REPAIR_RE = re.compile("|".join(f"({p})" for p in REPAIR_PHRASES), flags=re.IGNORECASE)


def has_repair_signal(text: str) -> bool:
    """Stage A — keyword/regex match for repair phrases."""
    return bool(REPAIR_RE.search(text or ""))


# ---------- Stage B: Embedding similarity ----------

EMBED_THRESHOLD = 0.55  # tuned on dev set


def embed(text: str):
    """Embed text using the configured embedding provider.

    Provider is configured via env var EMBED_PROVIDER ∈ {'openai', 'voyage', 'local'}.
    Implementations omitted here for brevity — drop-in any embedding API.
    """
    raise NotImplementedError("Wire up an embedding provider in this function.")


def cosine(a, b) -> float:
    import numpy as np
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


def low_intent_match(prompt: str, response: str, repair: str) -> bool:
    """Stage B — embedding similarity below threshold suggests intent gap."""
    target = embed(f"{prompt}\n\n{repair}")  # what the user actually wanted
    actual = embed(response)
    return cosine(target, actual) < EMBED_THRESHOLD


# ---------- Stage C: LLM-as-judge ----------

JUDGE_PROMPT = """You are an expert evaluator deciding whether an AI assistant exchange exhibits a particular failure mode.

ORIGINAL USER PROMPT:
{prompt}

ASSISTANT RESPONSE:
{response}

USER FOLLOW-UP:
{repair}

Pick exactly one classification:

A. REFUSAL — assistant declined or said it could not help.
B. HALLUCINATION — assistant gave a factually wrong answer.
C. INTENT GAP — assistant addressed the literal prompt but missed what the user actually wanted.
D. OTHER DISSATISFACTION — user is unhappy for some other specific reason.
E. FALSE POSITIVE — user follow-up is not actually a repair turn.

Reply on a single line in this exact format:
LETTER | <one-sentence justification>

Examples of valid replies:
C | The user asked about hotel options near a specific address; assistant gave a generic city overview.
A | Assistant refused on policy grounds; the follow-up is the user pushing back on the refusal.
"""


def llm_judge(prompt: str, response: str, repair: str) -> tuple[str, str]:
    """Stage C — LLM judge call. Returns (letter, justification)."""
    raise NotImplementedError(
        "Wire up an LLM client (Anthropic / OpenAI / etc.) and call with JUDGE_PROMPT."
    )


def is_intent_gap(prompt: str, response: str, repair: str) -> bool:
    letter, _ = llm_judge(prompt, response, repair)
    return letter.strip().upper().startswith("C")


# ---------- Pipeline ----------

@dataclass
class Conversation:
    """Minimal in-memory representation of a multi-turn conversation."""
    conv_id: str
    source: str            # 'wildchat' | 'lmsys' | 'oasst' | ...
    language: Optional[str]
    turns: list[dict]      # [{role: 'user'|'assistant', content: str}, ...]


@dataclass
class Candidate:
    """A conversation that passed all three filter stages."""
    conv_id: str
    source: str
    user_prompt: str
    assistant_response: str
    user_repair: str
    judge_letter: str
    judge_note: str


def iter_conversations(dataset_name: str) -> Iterator[Conversation]:
    """Load conversations from the given dataset.

    For WildChat / LMSYS the 'datasets' library handles streaming; loaders not shown here.
    """
    raise NotImplementedError("Implement dataset loader (e.g., HuggingFace `datasets`).")


def filter_pipeline(dataset: str) -> Iterable[Candidate]:
    n_total = n_a = n_b = n_c = 0

    for conv in iter_conversations(dataset):
        n_total += 1
        if len(conv.turns) < 4:
            continue
        # Pull first prompt / response / repair
        try:
            user_t1 = conv.turns[0]["content"]
            asst_t1 = conv.turns[1]["content"]
            user_t2 = conv.turns[2]["content"]
        except (IndexError, KeyError):
            continue

        # Stage A
        if not has_repair_signal(user_t2):
            continue
        n_a += 1

        # Stage B
        try:
            if not low_intent_match(user_t1, asst_t1, user_t2):
                continue
        except NotImplementedError:
            # If embeddings not wired, skip Stage B for now and rely on Stages A + C.
            pass
        n_b += 1

        # Stage C
        try:
            letter, note = llm_judge(user_t1, asst_t1, user_t2)
        except NotImplementedError:
            letter, note = "C", "(judge not wired; Stage A pass only)"
        if not letter.upper().startswith("C"):
            continue
        n_c += 1

        yield Candidate(
            conv_id=conv.conv_id,
            source=conv.source,
            user_prompt=user_t1,
            assistant_response=asst_t1,
            user_repair=user_t2,
            judge_letter=letter,
            judge_note=note,
        )

    # Funnel summary printed at end of run
    print(f"Funnel: total={n_total} stageA={n_a} stageB={n_b} stageC={n_c}")


# ---------- CLI ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["wildchat", "lmsys", "oasst"])
    ap.add_argument("--output", required=True, help="Path to write JSONL of candidates.")
    args = ap.parse_args()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with out.open("w", encoding="utf-8") as f:
        for c in filter_pipeline(args.dataset):
            f.write(json.dumps(asdict(c), ensure_ascii=False) + "\n")
            written += 1
    print(f"Wrote {written} candidates to {out}")


if __name__ == "__main__":
    main()
