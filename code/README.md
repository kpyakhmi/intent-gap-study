# Code

Three scripts compose the pipeline:

1. `filter.py` — surfaces intent-gap candidates from a public corpus.
2. `replay.py` — runs each candidate's first user turn through 4 frontier models.
3. `grade.py` — LLM-as-judge scores each replay on literal × intent axes.

## Setup

```bash
pip install -r requirements.txt

# Set up API keys
cp ../.env.template .env  # then edit
export ANTHROPIC_API_KEY=...
export OPENAI_API_KEY=...
export GOOGLE_API_KEY=...
export TOGETHER_API_KEY=...   # or whichever provider hosts the open model
```

## End-to-end run

```bash
# Stage 1: mine candidates from WildChat (assumes you've downloaded the HF dataset locally)
python filter.py --dataset wildchat --output ../data/wildchat_candidates.jsonl

# Stage 2: replay across models
python replay.py \
    --input ../data/intent_gap_corpus.jsonl \
    --output ../data/replays.jsonl \
    --models claude,gpt,gemini,llama

# Stage 3: grade
python grade.py --input ../data/replays.jsonl --output ../data/graded.jsonl
```

## Provider stubs

Each `call_*` function in the scripts raises `NotImplementedError` until wired
to your provider client of choice. Replace with a few lines per provider; the
shapes are intentionally minimal so the pipeline doesn't depend on a particular
SDK.

## Notes

- Pin `MODEL_VERSIONS` at run-time and report them in the paper.
- Embedding provider in `filter.py` is configured via `EMBED_PROVIDER` env var.
- All scripts emit JSONL for easy diff and partial reruns.
- Cost: full pipeline (500 candidates × 4 models × ~1k tokens) ~ $15-30.
