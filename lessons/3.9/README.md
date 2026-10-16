# Student kit: Lesson 3.9, Module 3 exam traps and recap

Claude Certified Architect – Foundations (CCAR-F) · Module 3: Agents with the Claude Agent SDK: the Support Resolution Agent · Lesson 3.9

This lesson adds no code. It goes back over Module 3 using the module's own runs. By the end of it you can:

1. Spot Module 3's six classic traps
2. Know the fix each one hides
3. Hold Module 3 on one page

## What's in the kit

| File | What it is |
|---|---|
| `module-3.md` | The Module 3 cheat sheet: one row per lesson, plus the six traps and why each one is wrong |

## The six traps

Each wrong option on the exam usually sounds careful. It's a real move, used where it can't do the job.

| Trap | It sounds like | The fix it hides |
|---|---|---|
| Say it louder | "Write the rule in capitals, at the top." "Add sample chats." "A prompt line to use only these tools." | A rule that must hold every time goes in code that runs on every call: a gate in the tool's handler, or a `PreToolUse` hook that denies with a reason. The prompt is the right lever for judgment, the wrong one for a rule. |
| Trust a proxy | "Escalate when sentiment turns negative." "Escalate below a confidence of 7/10." | Explicit escalation criteria with examples: the customer asks for a person, the policy is silent or ambiguous, no progress. Acknowledge frustration and offer the fix; ask for another identifier when several accounts match. |
| Count the wrong thing | "Count every `success` subtype as resolved." "The reply says it's resolved." "Raise `max_turns`." | Grade each run against its label, from what the agent did (the refunds in the ledger), and count escalations apart. |
| Ship the transcript | "Attach the whole chat." "Ask for longer summaries." "The customer can explain it again." | A structured hand-off with required fields: customer ID, order, root cause, amount, recommended action, each described for the person who reads it. |
| Summarize harder | "Double the summary limit." "A bigger context window." "Tell it to double-check the numbers." | Case facts from the tool results, outside the summary, one entry per issue, in every prompt; trim tool results before they pile up. |
| Resume blindly | "Resume as it is." "Start a blank session and re-read everything." "Fork to see which one notices." | Mostly still valid: resume and name the files that changed. Mostly stale: a fresh session with a structured summary. Forks compare approaches; they don't detect changes. |

## Where the runs come from

Every run in the lesson was recorded in an earlier lesson. To run one again, use that lesson's kit:

- **Lesson 3.3**, `python -m support.gate_check`: five tickets (three senders no account matches, two customers asking about someone else's order), the same system prompt, which already says to verify the sender first. Prompt rule only: `served 1` on all five tickets. Gate on: `served 0`, `blocked 1` on all five. In a practice run after a block, Claude asked for the email on the account.
- **Lesson 3.4**, `python -m support.hook_check`: called directly, `refund $42.00: allow` and `refund $649.00: deny` with the reason "Refunds above $500 need a support lead. Call escalate_to_human instead; don't retry." Through the agent, the $649 desk went `get_customer`, `lookup_order`, `escalate_to_human`, with no refund paid.
- **Lesson 3.5**, `python -m support.escalation_check`: before the criteria, both customers who asked for a person were escalated only after an order lookup: `handed over at once 0/2`. With explicit criteria and examples in `support/prompts/system.md`: `get_customer, escalate_to_human`, `2/2`; the frustrated customer on T-017 was acknowledged and refunded $98.00.
- **Lesson 3.2**, `python -m support.evaluate`: every one of the 20 runs ended with subtype `success`; graded against the labels, T-002 was a `wrong refund` and T-015 a `refund missing`: `FCR 15/20 (75%) · escalation recall 3/3 · wrong refunds 1`.
- **Lesson 3.6**, `python -m support.case_check`: before, every hand-off was missing `order_id`, `amount` and `recommended_action` (`hand-offs complete 0/3`); with the structured hand-off, nothing missing and a next step for each case (`3/3`).
- **Lesson 3.7**, `python -m support.long_check`: with a summary only, the summary kept the amounts but lost the order numbers and that the customer was verified, and the last reply asked her to verify again: `facts kept 0/9`. With case facts outside the summary: `facts kept 9/9`. `python -m support.case_facts HL-10187`: 12 fields, 484 characters, trimmed to 8 fields, 292 characters.
- **Lesson 3.8**, `python -m support.sessions`: after two forks planned tests, the resumed original answered that no tests had been planned in its conversation. After one line of `support/hooks.py` changed, a resume that named the change made one `Read` of that file and answered about the new code.

Each number comes from one run on the day it was recorded, so yours will differ. This lesson made no API calls and cost nothing.

## Next

1. **Lab 3: the support agent, measured on every ticket**, in the course materials under `labs/L3/`: measure the agent on all 50 labeled tickets, with the customers' follow-up answers, fix what that run finds, and reach the target (first-contact resolution of at least 80%, every escalation, no wrong refunds). Then the same rules in a loop you write yourself, with its tools from harborline-mcp.
2. **The Module 3 quiz**: 14 questions, three of them from Modules 1 and 2. This lesson has no quick check, because the quiz takes its place.

## Sources (checked 2026-10-16)

- Use Claude Code features in the SDK: https://code.claude.com/docs/en/agent-sdk/claude-code-features
- Configure permissions: https://code.claude.com/docs/en/agent-sdk/permissions
- Intercept and control agent behavior with hooks: https://code.claude.com/docs/en/agent-sdk/hooks
- How the agent loop works: https://code.claude.com/docs/en/agent-sdk/agent-loop
- Work with sessions: https://code.claude.com/docs/en/agent-sdk/sessions
- CLI reference: https://code.claude.com/docs/en/cli-reference
- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Define tools: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- Manage tool context: https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context
- Claude Certified Architect – Foundations Exam Guide: Domains 1 and 5, Task Statements 1.1, 1.4, 1.5, 1.7, 5.1 and 5.2, Scenario 1

Models and tools change. Always confirm current details in the official docs.
