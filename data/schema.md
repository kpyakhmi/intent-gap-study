# Dataset Schema

The released artifact is a single JSONL file: `intent_gap_corpus.jsonl`.

Each line is one curated intent-gap conversation.

## Fields

| Field | Type | Description |
|---|---|---|
| `conv_id` | string | Stable ID (preserves source dataset's ID where available) |
| `source` | string | `wildchat` \| `lmsys` \| `oasst` |
| `language` | string | ISO 639-1 code, or `und` if not detectable |
| `domain` | string | Coarse: `code`, `creative`, `factual`, `personal`, `work`, `other` |
| `user_prompt` | string | Anonymized first user turn |
| `assistant_response` | string | Anonymized first assistant response |
| `user_repair` | string | Anonymized user follow-up containing repair signal |
| `inferred_intent` | string | One-line summary of what the user actually wanted |
| `repair_signal_matched` | string | The exact phrase that triggered Stage A |
| `taxonomy_label` | string | Primary category from the §5 taxonomy |
| `taxonomy_label_secondary` | string \| null | Secondary category if applicable |
| `judge_letter` | string | Stage C judge's classification |
| `judge_note` | string | Stage C judge's one-line note |
| `human_reviewer_id` | string | Hash of who hand-reviewed (e.g., `KY` or `R2`) |
| `human_reviewer_note` | string | Free-text note from review |
| `replay` | object | `{model: {response, literal, intent, category}, ...}` populated after Stages 2-3 |

## Anonymization

All free-text fields have been processed to remove:
- Names (NER + regex)
- Email addresses
- Phone numbers
- Specific street addresses
- Employer / company names mentioned in text
- URLs containing identifiers
- Account numbers, case numbers

Replacements use bracketed tokens: `[NAME]`, `[EMAIL]`, `[EMPLOYER]`, etc.

If a conversation could not be anonymized without destroying its meaning, it
was dropped from the corpus rather than included.

## License

CC BY-NC 4.0, consistent with WildChat and LMSYS-Chat-1M source licenses.

## Versions

- v0.1: scaffolded schema only — no rows yet
- v1.0: target ~300-500 rows, English-only
- v1.1 (stretch): multilingual extension to 2 additional languages
