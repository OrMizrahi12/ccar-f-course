# Student kit: Lesson 8.2, Scenario sprint 1

Claude Certified Architect – Foundations (CCAR-F) · Section 8: Exam Readiness · Lesson 8.2

This lesson adds no code. It recalls the rules behind Scenarios 1 and 3 using earlier lessons' runs. By the end of it you can:

1. Recall the rules behind Scenarios 1 and 3
2. Spot the traps that sound right
3. Apply them to a stem from either scenario

## What's in the kit

| File | What it is |
|---|---|
| `scenario-sprint-1.md` | The sprint on one page: the two scenarios, the eleven rules with their task statements, and the trap each one rules out |

## Where the runs come from

Every run in the lesson was recorded in an earlier lesson. To repeat one, use that lesson's kit:

- **Lesson 3.3** (rule 2): the prompt rule alone still served order data to unverified senders; the gate in code blocked every lookup.
- **Lesson 3.4** (rule 3): the hooks called directly: status 7 → `returned`, a timestamp → a date, a $42.00 refund allowed and $649.00 denied, with the reason.
- **Lesson 3.5** (rule 4): both customers who asked for a person were handed over at once, 2/2.
- **Lesson 3.6** (rule 2): hand-offs complete 3/3, requests answered 9/9.
- **Lesson 3.7** (rule 5): facts kept 0/9 with a running summary only; 9/9 with case facts.
- **Lesson 3.8** (rule 6): the original session never saw the forks; the resumed one was told what changed.
- **Lessons 4.2 and 4.3** (rule 7): each subagent got only its prompt; running together saved 41 s.
- **Lesson 4.6** (rule 10): two searches timed out, and the answer names the gap.
- **Lesson 4.7** (rule 11): two sources side by side, with their publishers and dates, under Contested.
- **Lesson 2.4** (rule 10): `is_error`, `transient`, `isRetryable: true`, then a retry and the answer.

Each result comes from one run on the day it was recorded, so yours will differ. This lesson made no API calls and cost nothing.

## Next

1. **This lesson's quick check:** three short questions.
2. **Lesson 8.3: scenario sprint 2,** for Scenarios 2, 4 and 5.

## Sources (checked 2026-10-17)

- Claude Certified Architect – Foundations Exam Guide: sections 4 and 5 (Scenarios 1 and 3; Domains 1, 2 and 5)
- Agent SDK, hooks: https://code.claude.com/docs/en/agent-sdk/hooks
- Agent SDK, Configure permissions: https://code.claude.com/docs/en/agent-sdk/permissions
- Subagents in the SDK: https://code.claude.com/docs/en/agent-sdk/subagents
- MCP specification, Tools: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- Define tools: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools

Models and tools change. Always confirm current details in the official docs.
