# Student kit: Lesson 7.7, Module 7 exam traps and recap

Claude Certified Architect – Foundations (CCAR-F) · Module 7: Structured Data Extraction · Lesson 7.7

This lesson adds no code. It goes back over Module 7 using the module's own runs. By the end of it you can:

1. Spot Module 7's eight classic traps
2. Ask what makes each value trustworthy
3. Hold Module 7 on one page

## What's in the kit

| File | What it is |
|---|---|
| `module-7.md` | The Module 7 cheat sheet: one row per lesson, plus the eight traps and why each one is wrong |

## The question that settles most of them

**What makes this value trustworthy, and who finds out when it isn't?**

Not a stronger word in the prompt, but a mechanism: a forced tool (`tool_choice` `any` or by name), a field that can say "not stated" (nullable, `other`, `unclear`), a validator (checks in code), a retry with the errors (capped, then a person), an example (one per layout), a `custom_id` (results matched, not ordered), a resubmitted failure (each with its fix), and a measured slice (accuracy by layout and field, plus random samples).

## The eight traps

| Trap | It sounds like | The fix it hides |
|---|---|---|
| Ask for JSON | "Reply in JSON." "Parse the reply with a regex." "Offer the tool with tool_choice auto and hope." | The record is a tool's input schema; force the call (`any`, or the tool by name); classify first with a forced metadata call. |
| Fill every field | "Make every field required." "Default the missing values to 0." | Nullable fields, null when not stated; `other` + detail and `unclear` in enums. Required only for what every document states. |
| Strict means right | "Strict mode checks the output, so the values are correct." | Strict guarantees the shape. Validators check the values: totals, dates, a calculated total beside the stated one. |
| Retry until it works | "Raise the retry limit." "Retry at a higher temperature." "Retry until the total appears." | Retry with the document, the failed output and the exact errors, up to a cap, then a person. Never retry what isn't in the source. |
| More rules | "Add the rule in capital letters." "List every informal quantity." | A few examples, one per layout, each with the exact output; then re-run the dev set and count. |
| Batch the blocking work | "Batch the pre-merge check." "The results come back in order." "One batch a day for a 36-hour deadline." | Batch only what nobody waits on; match by `custom_id`; submit often enough that the wait + 24 hours meets the deadline. |
| Resubmit everything | "Re-run the whole batch." "Raise max_tokens everywhere." "Drop what failed." | Resubmit only the failed `custom_id`s, each with its fix: in parts, with its errors, or as it was. |
| Trust the average | "97% overall, skip the review." "Review only what the model calls unsure." "Spot-check the first 20." | Accuracy by layout and field on a labeled set; route by measured confidence and conflicts; random samples from every layout, every run. |

## Where the runs come from

Every run in the lesson was recorded in an earlier lesson. To repeat one, use that lesson's kit:

- **Lesson 7.1** (traps 1 and 3): with `tool_choice` `any`, the pro-forma came back as `record_invoice`; metadata first, it was skipped as `"doc_type": "other"`. With every tool strict, Ironleaf's invoice was valid with `"quantity": 1` for 1 gross, and its lines added up to 3,603.96 against 3,594.96 stated.
- **Lesson 7.2** (trap 2): every field required gave `"<UNKNOWN>"` for a missing due date and order number, and `"stated_total": -1` for an illegible total; nullable fields gave `"stated_total": null`.
- **Lesson 7.3** (trap 4): the retry with the exact error fixed the 144 x 6.84 line on attempt 2; the same reading three times went to review; the missing total went to review without a retry.
- **Lesson 7.4** (trap 5): `9 of 12 documents exact; 7 wrong values` before the examples, `12 of 12 documents exact; 0 wrong values` after.
- **Lesson 7.5** (traps 6 and 7): the docstring's deadline math (36 hours, up to 24, a batch every 8 hours); two invoices stopped at `max_tokens` and went back in parts, 38 requests, one joined from 19 parts; the whole run: 85 ok, 9 for review, 6 skipped, $0.0486.
- **Lesson 7.6** (trap 8): overall 98.8%, `supplier_name` 61.7%; 42 records to a person; 4 random samples, different on every run.

Each result comes from one run on the day it was recorded, so yours will differ. This lesson made no API calls and cost nothing.

## Next

1. **Lab 7: the extraction pipeline, finished**, in the course materials under `labs/L7/`: confidence that Claude reports and you calibrate, a log of what each retry fixed, the deadline math and a fallback for long documents, and one more example, for names printed in capitals, checked by the self-check tests.
2. **The Module 7 quiz**: 14 questions, three of them from earlier modules. This lesson has no quick check, because the quiz takes its place.

## Sources (checked 2026-10-17)

- Define tools: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- Strict tool use: https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use
- Reduce hallucinations: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- Handle tool calls: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Batch processing: https://platform.claude.com/docs/en/build-with-claude/batch-processing
- Define success criteria and build evaluations: https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- Claude Certified Architect – Foundations Exam Guide: Domains 4 and 5, Task Statements 4.2, 4.3, 4.4, 4.5 and 5.5, Scenario 6

Models and tools change. Always confirm current details in the official docs.
