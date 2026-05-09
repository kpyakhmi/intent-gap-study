"""
LLM-as-judge grading on the literal × intent axes.

Usage:
    python grade.py --input ../data/replays.jsonl \
                    --output ../data/graded.jsonl \
                    --judge claude-haiku
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path

GRADE_PROMPT = """You are grading an AI assistant's response on two independent axes.

ORIGINAL USER PROMPT:
{prompt}

USER'S TRUE INTENT (inferred from a later repair turn):
{inferred_intent}

ASSISTANT RESPONSE BEING GRADED:
{response}

Score the assistant response on:
1. LITERAL COMPLIANCE (0-2): did it address the literal prompt?
   0 = did not address the prompt at all
   1 = partially addressed
   2 = fully addressed
2. INTENT SATISFACTION (0-2): did it satisfy the user's true intent?
   0 = missed the true intent
   1 = partial
   2 = correctly understood and satisfied

Also pick the BEST taxonomy category from this list (or "other"):
- implicit-context-blindness
- specificity-mismatch
- format-mismatch
- goal-collapse
- sycophantic-drift
- silent-failure
- refusal-mismatch
- memory-state-failure
- tone-misread
- cultural-misread
- expertise-mismatch
- other

Reply in JSON only, no prose:
{{"literal": <0|1|2>, "intent": <0|1|2>, "category": "<id>", "note": "<<= 25 words"}}
"""

JSON_RE = re.compile(r"\{[^}]*\}", flags=re.DOTALL)


def call_judge(prompt: str) -> str:
    raise NotImplementedError("Wire up LLM client (e.g., Anthropic Haiku).")


@dataclass
class Grade:
    conv_id: str
    model: str
    model_version: str
    literal: int
    intent: int
    category: str
    note: str
    raw_judge: str


def grade_one(replay: dict) -> Grade:
    judge_prompt = GRADE_PROMPT.format(
        prompt=replay["user_prompt"],
        inferred_intent=replay["inferred_intent"],
        response=replay["response"],
    )
    raw = call_judge(judge_prompt)
    m = JSON_RE.search(raw)
    if not m:
        return Grade(replay["conv_id"], replay["model"], replay["model_version"],
                     -1, -1, "parse-error", "judge returned non-JSON", raw)
    try:
        parsed = json.loads(m.group(0))
    except Exception:
        return Grade(replay["conv_id"], replay["model"], replay["model_version"],
                     -1, -1, "parse-error", "json decode failed", raw)
    return Grade(
        conv_id=replay["conv_id"],
        model=replay["model"],
        model_version=replay["model_version"],
        literal=int(parsed.get("literal", -1)),
        intent=int(parsed.get("intent", -1)),
        category=str(parsed.get("category", "other")),
        note=str(parsed.get("note", "")),
        raw_judge=raw,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(args.input, "r", encoding="utf-8") as inf, out.open("w", encoding="utf-8") as outf:
        for line in inf:
            replay = json.loads(line)
            g = grade_one(replay)
            outf.write(json.dumps(asdict(g), ensure_ascii=False) + "\n")
            n += 1
    print(f"Wrote {n} grades to {out}")


if __name__ == "__main__":
    main()
