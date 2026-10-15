# Student kit: Lesson 2.8, Module 2 exam traps and recap

Claude Certified Architect – Foundations (CCAR-F) · Module 2: Tool Design & MCP Integration · Lesson 2.8

This lesson adds no code. It goes back over Module 2 using the module's own runs. By the end of it you can:

1. Spot Module 2's six classic traps
2. Know the fix each one hides
3. Hold Module 2 on one page

## What's in the kit

| File | What it is |
|---|---|
| `module-2.md` | The Module 2 cheat sheet: one row per lesson, plus the six traps and why each one is wrong |

## The six traps

Each wrong option on the exam is usually a real move, made too soon or in the wrong place.

| Trap | It sounds like | The fix it hides |
|---|---|---|
| Say it in the prompt | "Add few-shot examples first." "Add a keyword rule." "Ask Claude to take extra care." | Claude picks a tool by reading the tool definitions. Fix the description first, and reword a prompt line that names a tool by situation, or delete it. Examples are real, just not the first fix. |
| Add a layer | "A routing classifier in front of the agent." "A step that picks the tool for each request." | Fix the tool itself, then measure it on requests it wasn't written around. A router can be the right design later, not the first step. |
| One tool for everything | "Merge the tools, so nothing is left to choose." "A mode switch and one free-text query." | Same contract: merge (related operations behind an `action` parameter are fine). Different contracts: split, each tool with its own inputs and results. |
| Give it everything | "Every tool, just to be safe." "Read every file." | Give each agent the tools its role needs, search before you read, and put a catalog that rarely changes in a resource. |
| Hide the failure | "'Operation failed' for everything." "An empty list when access fails." "Blind retries on the server." | Flag the failure, name its category, say whether a retry can help, and add a readable message. An empty result is a success; a failed lookup is not. |
| Right idea, wrong place | "A token in the shared `.mcp.json`." "A personal server in project scope." "The team's server in your user scope." | A variable reference (`${VAR}`) in the shared file, team servers in project scope, your own in user scope, a private one-repo setup in local scope. |

## Where the runs come from

Every run in the lesson was recorded in an earlier lesson. To run one again, use that lesson's kit:

- **Lesson 2.1**, `python -m experiments.m2.routing_eval before` and `after`: only the description strings changed, no router and no new layer. Held-out requests went from 6/24 to 23/24, the labeled set from 39/48 to 40/48; input tokens from 97,383 to 145,177.
- **Lesson 2.2**, `python -m experiments.m2.prompt_override` (run 2): no prompt line 45/48; the keyword line "When a customer mentions shipping or delivery, call list_orders first." 39/48 (R12, a request to refund a shipping fee, went to `list_orders`: 0/3); the same intent keyed to the situation 46/48. Also in Lesson 2.2: the generic `query_backend` (a `kind` and one free-text `query`: "An email, an ID or a question") was never Claude's first pick in three practice runs, 0 of 48 each, and the split gave `check_refund` its own contract: an order and a reason in; allowed, refund and rule out.
- **Lesson 2.3**, `python -m experiments.m2.tool_count`: six tools against eighteen. Selection held (39/48 against 38/48, held-out 24/24 both), but input per call went from 1,996 to 3,143 tokens, about 57% more on every call. Then `loop/agent.py` got `ROLE_TOOLS`, five tools: it answers, checks the policy, and hands off; `process_refund` isn't one of its options.
- **Lesson 2.4**, `python -m experiments.m2.error_replies`: the same five cases with three kinds of error reply. Permission: 0/3 with the generic "Operation failed.", 3/3 with a sentence, 2/3 with the structured body; with the generic string Claude sent a refund again after the account hold refused it. Then `list_orders('C-1058')` returned `[]` (a success), and `python -m loop.agent T-040` got a transient, retryable error, ran the same lookup again, and answered.
- **Lesson 2.6**, `.mcp.json` holds `"HARBORLINE_API_TOKEN": "${HARBORLINE_API_TOKEN}"`, the variable's name, never its value. With the variable unset, `claude mcp list` shows `MCP config diagnostics`: `Missing environment variables: HARBORLINE_API_TOKEN`.
- **Lesson 2.7**, Claude Code with Grep and Glob: "Searched for 1 pattern, read 3 files", one more search, and the answer; it never read the whole repo.

Each number comes from one run on the day it was recorded, so yours will differ. This lesson made no API calls and cost nothing.

## Next

1. **Lab 2: harborline-mcp, hardened and measured**, in the course materials under `labs/L2/`: close a validation gap in the refund tool, publish one more catalog as a resource, and measure tool selection when the tool list comes from the server (at least 90% of the held-out requests right).
2. **The Module 2 quiz**: 12 questions, two of them from Module 1. This lesson has no quick check, because the quiz takes its place.

## Sources (checked 2026-10-15)

- Define tools: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- How tool use works: https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works
- Handle tool calls: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
- Tool search tool: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool
- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Writing effective tools for agents (Anthropic engineering): https://www.anthropic.com/engineering/writing-tools-for-agents
- MCP, Understanding MCP servers: https://modelcontextprotocol.io/docs/learn/server-concepts
- Connect Claude Code to tools via MCP: https://code.claude.com/docs/en/mcp
- Claude Code tools reference: https://code.claude.com/docs/en/tools-reference
- Claude Certified Architect – Foundations Exam Guide: Domain 2, Task Statements 2.1 to 2.5, Scenario 1

Models and tools change. Always confirm current details in the official docs.
