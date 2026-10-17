# Scenario sprint 1 on one page: Scenarios 1 and 3

CCAR-F · Section 8: Exam Readiness · Lesson 8.2 · Scenario 1 (Customer Support Resolution Agent) and Scenario 3 (Multi-Agent Research System) · Domains 1 (27%), 2 (18%) and 5 (15%) · checked against the Claude docs and the exam guide on 2026-10-17

**Scenario 1:** an agent built on the Agent SDK, with `get_customer`, `lookup_order`, `process_refund` and `escalate_to_human`; target: 80% first-contact resolution.

**Scenario 3:** a coordinator, with subagents that search, analyze, synthesize and report.

| # | Rule the exam rewards | Trap that sounds right |
|---|---|---|
| 1 | **Agentic loop** (TS 1.1): loop while `stop_reason` is `tool_use`; every tool result goes back into the history; stop on `end_turn`. | Read the text for the word "done"; an iteration cap as the main way to stop. |
| 2 | **Enforcement and hand-offs** (TS 1.4): a business rule that must hold, like no order data before the customer is verified, is a gate in code; a hand-off carries the customer, the root cause, the amount and the next action. | A stronger sentence in the system prompt. |
| 3 | **Hooks** (TS 1.5): a `PreToolUse` hook blocks or redirects a call before it runs (a refund over $500 goes to escalation); a `PostToolUse` hook normalizes a result before Claude sees it (timestamps, status codes). | Ask the model to convert formats as it reasons. |
| 4 | **Escalation** (TS 5.2): hand over when the customer asks for a person, when the policy is silent or unclear, or when there's no progress. | Sentiment, or the model's own confidence, as the trigger. |
| 5 | **Long conversations** (TS 5.1): keep the case facts (amounts, orders, dates) outside the summary; trim tool results to the fields that matter. | Trust a running summary to keep the numbers. |
| 6 | **Sessions** (TS 1.7): resume when the context is still valid, and say what changed; start fresh, with a summary, when tool results are stale; fork to compare two approaches from the same point. | Resume a stale session as it is. |
| 7 | **Coordinators and subagents** (TS 1.2, 1.3): the coordinator owns routing and errors; a subagent inherits nothing, so pass it complete findings as structured data; start parallel subagents in one response. | Assume a subagent sees the coordinator's history. |
| 8 | **Decomposition** (TS 1.6): a fixed chain for predictable work; a pass per file plus a cross-file pass for a big review; a plan that adapts for open-ended research. | One pass over everything. |
| 9 | **Tools** (TS 2.1, 2.3): descriptions route: what the tool does, its inputs, its edge cases, and when to use another tool instead; four or five tools per role; `tool_choice` when you need a guarantee. | One tool that does everything, or every tool for every agent. |
| 10 | **Errors** (TS 2.2, 5.3): structured errors with a category, whether it's retryable, and a message; recover transient errors locally; pass the rest up with the partial results. | An empty "success" that hides the failure, or killing the whole run. |
| 11 | **Provenance** (TS 5.6): every claim keeps its source (URL, excerpt, date) through every summary; conflicting figures stay side by side, each with its source. | Pick one number, and drop the other. |

**Reading a stem:** find the deciding constraint (the one requirement that rules options out), then strike every option that relies on a trap. A rule that must hold every time needs a control (code that enforces it), not a better sentence.

Sources: the CCAR-F exam guide (sections 4 and 5); code.claude.com/docs (Agent SDK hooks, Configure permissions, Subagents in the SDK); the MCP specification (Tools, error handling); platform.claude.com/docs (Define tools). Models and tools change: confirm details in the official docs.
