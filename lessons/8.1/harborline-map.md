# The Harborline map: six systems, six scenarios, two foundations

Claude Certified Architect – Foundations (CCAR-F) · Lesson 8.1

Every exam question sits inside one of the guide's six scenarios (section 5), and you get four of them. Each scenario describes a whole system. This course built one of each in a single repository, Harborline. Use this page to place a question before you read its options: which system is it, and which control, schema or context is it missing?

## The two foundations

| Foundation | Folder | Built in | What it gives every later system |
|---|---|---|---|
| The raw loop | `loop/` | Module 1 | Send, read `stop_reason`, run the tools, repeat; one branch each for `max_tokens`, `refusal` and `pause_turn` |
| harborline-mcp | `mcp_server/`, `.mcp.json` | Module 2 | The tools every later system calls, with descriptions that route and errors that say what went wrong |

## The six systems

| Scenario (guide §5) | Primary domains (guide §5) | Harborline system | Folder | Built in | Look for |
|---|---|---|---|---|---|
| 1. Customer Support Resolution Agent | 1, 2, 5 | The support agent, on the Agent SDK | `support/` | Module 3 | The verification gate, the refund-limit hook, escalation, case facts, sessions |
| 2. Code Generation with Claude Code | 3, 5 | The team's Claude Code setup | `CLAUDE.md`, `.claude/` | Module 5 | `CLAUDE.md` and its imports, path-scoped rules, a command and two skills, plan mode or direct |
| 3. Multi-Agent Research System | 1, 2, 5 | A coordinator and its subagents | `research/` | Module 4 | Each subagent's definition and its role's tools, errors that carry context, provenance |
| 4. Developer Productivity with Claude | 2, 3, 1 | The codebase explorer: an Agent SDK agent with the built-in tools and its own MCP server | `devtools/` | Lesson 5.8 | A scoped tool (codemap) instead of reading the whole codebase |
| 5. Claude Code for Continuous Integration | 3, 4 | The review on every pull request | `.github/workflows/`, `ci/` | Module 6 | Claude Code with `-p`, explicit criteria, examples, a findings schema, a separate cross-file pass |
| 6. Structured Data Extraction | 4, 5 | The extraction pipeline | `extraction/` | Module 7 | A schema with nullable fields, validation with retries, batches, review routed by measured confidence |

The domains: 1 Agentic Architecture & Orchestration (27%), 2 Tool Design & MCP Integration (18%), 3 Claude Code Configuration & Workflows (20%), 4 Prompt Engineering & Structured Output (20%), 5 Context Management & Reliability (15%).

## Three questions to ask of any scenario item

1. **Which system is this?** Place it on the map first.
2. **Is a rule only an instruction?** When money moves or a step must always happen, the exam wants a control in code: a gate, a hook, a schema, a validator.
3. **What is the model missing?** A schema field it can leave empty, the earlier findings, the subagent's context, a better tool description.
