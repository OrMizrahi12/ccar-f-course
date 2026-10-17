# Student kit: Lesson 8.4, Scenario sprint 3

Claude Certified Architect – Foundations (CCAR-F) · Section 8: Exam Readiness · Lesson 8.4

This lesson adds no code. It recalls the rules behind Scenario 6 and Domain 5 using earlier lessons' runs. By the end of it you can:

1. Recall the rules behind Scenario 6
2. Recall Domain 5 across every scenario
3. Apply them to a mixed stem

## What's in the kit

| File | What it is |
|---|---|
| `scenario-sprint-3.md` | The sprint on one page: Scenario 6 and Domain 5, the eleven rules with their task statements, and the trap each one rules out |

## Where the runs come from

Every run in the lesson was recorded in an earlier lesson. To repeat one, use that lesson's kit:

- **Lesson 7.1** (rule 1): under `tool_choice` `any`, a pro-forma filed as an invoice; a forced metadata call first skips it as `other`.
- **Lesson 7.2** (rule 2): every field required gives `<UNKNOWN>` placeholders; nullable fields give `null`.
- **Lesson 7.3** (rule 3): a retry that carries the exact error passes on attempt 2; the cap sends a repeat failure to review.
- **Lesson 7.4** (rule 4): rules alone, 9 of 12 exact; an example for each layout, 12 of 12.
- **Lesson 7.5** (rule 5): 100 requests, 94 succeeded; only the two `max_tokens` failures resubmitted, in parts.
- **Lesson 7.6** (rule 6): 98.8% of values right overall, `supplier_name` right only 61.7% of the time.
- **Lesson 3.7** (rule 7): a running summary keeps none of the nine facts; case facts outside it keep nine of nine.
- **Lesson 3.5** (rule 8): both customers who asked for a person handed over at once.
- **Lesson 4.6** (rule 9): two searches timed out, and the answer says what isn't covered.
- **Lesson 5.7** (rule 10): a findings file, `/compact` with a focus, and the notes read back.
- **Lesson 4.7** (rule 11): two sources that disagree, kept side by side with their dates.

Each result comes from one run on the day it was recorded, so yours will differ. This lesson made no API calls and cost nothing.

## Next

1. **This lesson's quick check:** three short questions.
2. **Lesson 8.5: exam strategy,** for the day itself.

## Sources (checked 2026-10-17)

- Claude Certified Architect – Foundations Exam Guide: sections 4 and 5 (Scenario 6; Domains 4 and 5)
- Strict tool use: https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use
- Structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Reduce hallucinations: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- Handle tool calls: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
- Batch processing: https://platform.claude.com/docs/en/build-with-claude/batch-processing
- Define success criteria and build evaluations: https://platform.claude.com/docs/en/test-and-evaluate/develop-tests

Models and tools change. Always confirm current details in the official docs.
