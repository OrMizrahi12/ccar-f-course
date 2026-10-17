# Scenario sprint 3 on one page: Scenario 6 and Domain 5

CCAR-F · Section 8: Exam Readiness · Lesson 8.4 · Scenario 6 (Structured Data Extraction) · Domain 4 (20%) and Domain 5 (15%), which is also a primary domain of Scenarios 1, 2 and 3 · checked against the Claude docs and the exam guide on 2026-10-17

**Scenario 6:** a system that pulls information out of unstructured documents, validates it against JSON schemas, keeps accuracy high, handles edge cases gracefully, and feeds the systems downstream. Primary domains: Domain 4, Prompt Engineering & Structured Output (20%), and Domain 5, Context Management & Reliability (15%).

**Domain 5 everywhere:** it's a primary domain of Scenarios 1, 2, 3 and 6, so rules 7 to 11 can appear on almost any exam.

| # | Rule the exam rewards | Trap that sounds right |
|---|---|---|
| 1 | **Structured output** (TS 4.3): make the record a tool's input schema and force the call, with `any` or the tool by name; classify first with a forced metadata call; strict for the shape. | Ask for JSON in the prompt. |
| 2 | **Schemas** (TS 4.3): nullable where the source may be silent; `other` with a detail field, and `unclear`; the format rules next to the schema. | Make every field required. |
| 3 | **Validation and retry** (TS 4.4): validators in code for what the schema can't say, like a calculated total next to the stated one; retry with the document, the failed output and the exact errors, up to a cap; never retry what isn't in the source. | Retry until it passes. |
| 4 | **Few-shot for documents** (TS 4.2): an example from each layout, with the exact output and the wrong reading it replaces, and the plain case too; then measure on a labeled dev set. | More rules, in capital letters. |
| 5 | **Batches** (TS 4.5): half the price, up to 24 hours, no promise of order, so match each result by its `custom_id`; batch only work nobody waits on; submit often enough that the wait plus 24 hours meets the deadline; resubmit only the failures, each with its fix. | Batch the pre-merge check, or resubmit everything. |
| 6 | **Human review** (TS 5.5): accuracy by document type and field; confidence calibrated on labeled data; low confidence and conflicts go to people; keep sampling trusted records at random. | Trust a 97% average. |
| 7 | **Long conversations** (TS 5.1): case facts outside the summary; tool results trimmed to the fields that matter. | A running summary trusted with the amounts. |
| 8 | **Escalation** (TS 5.2): hand over on an explicit request for a person, a policy that's silent or unclear, or no progress. | Sentiment, or the model's own confidence, as the trigger. |
| 9 | **Errors across agents** (TS 5.3): return structured error context, recover transient failures locally, pass up partial results with a note on what isn't covered. | An empty success, or killing the whole run. |
| 10 | **Large codebases** (TS 5.4): a findings file, `/compact` with a focus, and subagents for verbose discovery. | One session that keeps growing until it forgets. |
| 11 | **Provenance** (TS 5.6): every claim keeps its source; conflicting figures stay side by side, each with its date. | Pick one figure, and drop the other. |

**Reading a stem:** find the deciding constraint (the one requirement that rules options out), then strike every option that relies on a trap. In extraction, a value the source never gave is never a number: let the field say so, and let a person see it. An empty success is the most expensive error there is.

Sources: the CCAR-F exam guide (sections 4 and 5); platform.claude.com/docs (Strict tool use, Structured outputs, Reduce hallucinations, Handle tool calls, Batch processing, Define success criteria and build evaluations). Models and tools change: confirm details in the official docs.
