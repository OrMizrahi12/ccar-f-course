# Six scenarios, one retailer

The exam frames its questions with scenarios: each exam presents four of the six below, picked at random. So the course builds all six, in one repository, for one fictional online retailer: Harborline. It sells home, kitchen, bedding, electronics, outdoor and office goods to customers in the United States and Canada. Its world is synthetic and fixed: 60 customers, 213 orders, 50 labeled support tickets, 112 supplier invoices and 14 research sources, and "today" is always 2026-10-15.

| Module | What Harborline gains | Folder | Exam scenario |
|---|---|---|---|
| 1 | A tool-using agent loop on the Messages API | `loop/` | Foundations for every scenario |
| 2 | `harborline-mcp`: an MCP server for customers, orders and refunds | `mcp_server/` | Tools for Scenarios 1 and 4 |
| 3 | The support resolution agent, with gates, hooks and escalation | `support/` | **Scenario 1:** Customer Support Resolution Agent |
| 4 | A coordinator and research subagents that write a cited report | `research/` | **Scenario 3:** Multi-Agent Research System |
| 5 | Claude Code set up for a team, and a codebase explorer agent | `.claude/`, `devtools/` | **Scenarios 2 and 4:** Code Generation with Claude Code; Developer Productivity with Claude |
| 6 | A pull-request review pipeline in GitHub Actions | `.github/`, `ci/` | **Scenario 5:** Claude Code for Continuous Integration |
| 7 | A supplier-invoice extraction pipeline | `extraction/` | **Scenario 6:** Structured Data Extraction |

## The six scenarios, by the systems that answer them

| Scenario | Where you build it |
|---|---|
| 1. Customer Support Resolution Agent | Module 3, on the tools of Module 2 and the loop of Module 1 |
| 2. Code Generation with Claude Code | Module 5 |
| 3. Multi-Agent Research System | Module 4 |
| 4. Developer Productivity with Claude | Module 5, with the MCP server of Module 2 |
| 5. Claude Code for Continuous Integration | Module 6, on your own GitHub repository |
| 6. Structured Data Extraction | Module 7 |

## The three cost habits

1. **The model:** start with Claude Haiku 5.5 ($0.10 per million input tokens, $0.50 per million output). Sonnet 5.5 is $2 / $10 and Opus 5.5 is $4 / $20. Step up only when a test shows you need to.
2. **`max_tokens`:** keep it small, but leave room for thinking, which counts toward it on Claude Haiku 5.5. Harborline's default is 1024.
3. **Input size:** count tokens before a big request (counting is free), send one ticket, not the whole folder, and use the Message Batches API at half price when you have volume and can wait.

Source: Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0, §5 Exam Scenarios. The module plan is this course's own; the starter's README has the same table.
