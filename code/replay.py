"""
Cross-model replay.

For each curated intent-gap conversation, replay the first user turn through
each frontier model and record the response for grading.

Usage:
    python replay.py --input ../data/intent_gap_corpus.jsonl \
                     --output ../data/replays.jsonl \
                     --models claude,gpt,gemini,llama

Each model is wrapped behind a thin function so providers can be swapped without
touching the pipeline. Versions are pinned at run-time and recorded with each row.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable

# ---------- Pinned model versions (record what was used) ----------

MODEL_VERSIONS = {
    "claude":  "claude-opus-4-6",         # update at run-time
    "gpt":     "gpt-X.X",
    "gemini":  "gemini-X.X",
    "llama":   "llama-X.X-instruct",
}


# ---------- Provider stubs ----------

def call_claude(prompt: str) -> str:
    raise NotImplementedError("Wire up Anthropic client.")


def call_gpt(prompt: str) -> str:
    raise NotImplementedError("Wire up OpenAI client.")


def call_gemini(prompt: str) -> str:
    raise NotImplementedError("Wire up Google client.")


def call_llama(prompt: str) -> str:
    raise NotImplementedError("Wire up Together / Groq / vLLM endpoint.")


PROVIDERS: dict[str, Callable[[str], str]] = {
    "claude": call_claude,
    "gpt":    call_gpt,
    "gemini": call_gemini,
    "llama":  call_llama,
}


# ---------- Replay ----------

@dataclass
class Replay:
    conv_id: str
    source: str
    user_prompt: str
    inferred_intent: str
    model: str
    model_version: str
    response: str
    elapsed_ms: int


def replay_one(conv: dict, model_key: str) -> Replay:
    fn = PROVIDERS[model_key]
    t0 = time.time()
    response = fn(conv["user_prompt"])
    elapsed_ms = int((time.time() - t0) * 1000)
    return Replay(
        conv_id=conv["conv_id"],
        source=conv["source"],
        user_prompt=conv["user_prompt"],
        inferred_intent=conv.get("inferred_intent", conv.get("user_repair", "")),
        model=model_key,
        model_version=MODEL_VERSIONS[model_key],
        response=response,
        elapsed_ms=elapsed_ms,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--models", default="claude,gpt,gemini,llama")
    ap.add_argument("--sleep", type=float, default=0.5, help="Seconds between calls.")
    args = ap.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    written = 0
    with open(args.input, "r", encoding="utf-8") as inf, out.open("w", encoding="utf-8") as outf:
        for line in inf:
            conv = json.loads(line)
            for m in models:
                r = replay_one(conv, m)
                outf.write(json.dumps(asdict(r), ensure_ascii=False) + "\n")
                written += 1
                time.sleep(args.sleep)
    print(f"Wrote {written} replays to {out}")


if __name__ == "__main__":
    main()
