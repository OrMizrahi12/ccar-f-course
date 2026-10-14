# Student kit: Lesson 1.6, Module 1 exam traps and recap

Claude Certified Architect – Foundations (CCAR-F) · Module 1: Claude API Foundations for Architects · Lesson 1.6

This lesson adds no code. It goes back over Module 1 using the module's own runs. By the end of it you can:

1. Spot Module 1's five classic traps
2. Know the fix each one hides
3. Hold Module 1 on one page

## What's in the kit

| File | What it is |
|---|---|
| [`cheatsheets/module-1.md`](../../cheatsheets/module-1.md) | The Module 1 cheat sheet (in this repository's `cheatsheets/` folder): one row per lesson, plus the five traps and why each one is wrong |

## The five traps

| Trap | It sounds like | The fix it hides |
|---|---|---|
| Make it bigger | "Use a larger model." "Move to a bigger context window." "Raise `max_tokens`." | Read the evidence first. Size fixes only a size problem: give it room when `stop_reason` says `max_tokens`. If it says anything else, size isn't the cause. |
| Say it in the prompt | "Tell Claude to remember the order number." "Add a rule: finish within three tool calls." | The API is stateless, so send the whole conversation every time. A rule that has to hold belongs in your code. |
| Read the words | "Stop when the reply says done." "Any text is the answer." "Parse the decision with a regex." "Stop after three turns." | Loop on `stop_reason`: continue on `tool_use`, finish on `end_turn`, and treat anything else as not an answer. A turn cap is only a safety net, and a decision you'd parse out of text should be a tool call. |
| Retry it | "Retry the failed lookup." "Claude refused, so send it again." | Retry only failures that can pass on their own: a dropped connection, a rate limit, a 5xx error (the SDK already retries those). Fix the cause of anything else, or report it: send the failure back as a `tool_result` with `is_error` set. |
| More machinery | "Make it an agent." "Add an orchestrator." "Add more agents." Or the mirror image: "A decision tree with a branch for every case." | Start with the simplest design that meets the requirement, a single call if that's enough. Add steps only when a measurement shows they pay. |

## Where the runs come from

Every run in the lesson was recorded in an earlier lesson. To run one again, use that lesson's kit:

- **Lesson 1.1**, `experiments/m1/budget.py`: a 1,000,000-token window; the role alone 59 tokens, role and policy 664, every order added 73,323 (7.33% of the window). The window was never the limit; the bill was. Also `experiments/m1/first_request.py` at `MAX_TOKENS = 40`: `stop_reason: max_tokens`, 40 of 40 output tokens, all of them thinking, no text. And `experiments/m1/stateless.py`: a new request with no history, 38 input tokens, and Claude doesn't see an order number; all three messages, 255 tokens, and it names HL-10163.
- **Lesson 1.2**, `experiments/m1/read_response.py` (the tool case): one `tool_use` block (`lookup_order`, HL-10196), no text, `stop_reason: tool_use`.
- **Lesson 1.3**, `experiments/m1/manual_tool_call.py` (the bad run): `lookup_order` on `12345` comes back with `is_error=True` ("not an order ID"); nothing is retried, and Claude asks Elijah for the right number.
- **Lesson 1.4**, `experiments/m1/antipatterns.py T-003`: four stop rules judged on one real run. `stop_reason`: turn 3, `end_turn`, OK. `done_words`: never stops. `fixed_cap`: stops at turn 2 while Claude still waited for a tool. `any_text`: stops at turn 1, on a progress line. Lesson 1.4's `loop/agent.py` also printed the History: every assistant turn kept as returned, with each `tool_use` followed by its `tool_result`.
- **Lesson 1.5**, `python -m loop.workflow T-004`: `route: refund  orders checked: ['HL-10164']  calls: 2`, so the fixed path checked one order of two. Then `experiments/m1/who_decides.py` on five tickets: the workflow used 10 calls and 10,553 tokens ($0.0024) and checked 5 of 6 orders; the agent used 15 calls and 26,465 tokens ($0.0039) and checked 6 of 6.

Each number comes from one run on the day it was recorded, so yours will differ. This lesson made no API calls and cost nothing.

## Next

1. **Lab 1**, in the course materials under `labs/L1/`: give every stop reason its own handling, and prove each branch with tests that need no API key.
2. **The Module 1 quiz**: 10 questions. This lesson has no quick check, because the quiz takes its place.

## Sources (checked 2026-10-14)

- Context windows: https://platform.claude.com/docs/en/build-with-claude/context-windows
- Using the Messages API: https://platform.claude.com/docs/en/build-with-claude/working-with-messages
- How tool use works: https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works
- Refusals and fallback: https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback
- Handle tool calls: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
- Errors: https://platform.claude.com/docs/en/api/errors
- Python SDK, retries: https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python
- Building effective agents (Anthropic engineering): https://www.anthropic.com/engineering/building-effective-agents
- Claude Certified Architect – Foundations Exam Guide: Task Statements 1.1 and 5.1, Scenario 1

API details change. Always confirm current details in the official docs.
