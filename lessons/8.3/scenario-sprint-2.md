# Scenario sprint 2 on one page: Scenarios 2, 4 and 5

CCAR-F · Section 8: Exam Readiness · Lesson 8.3 · Scenario 2 (Code Generation with Claude Code), Scenario 4 (Developer Productivity with Claude) and Scenario 5 (Claude Code for Continuous Integration) · Domain 3 (20%) through all three · checked against the Claude docs and the exam guide on 2026-10-17

**Scenario 2:** slash commands, CLAUDE.md, and plan mode or direct execution. Adds Domain 5 (15%).

**Scenario 4:** an Agent SDK agent that explores codebases with the built-in tools (Read, Write, Bash, Grep, Glob) and MCP servers. Adds Domains 2 (18%) and 1 (27%).

**Scenario 5:** Claude Code in CI: automated reviews and tests, actionable feedback, few false positives. Adds Domain 4 (20%).

| # | Rule the exam rewards | Trap that sounds right |
|---|---|---|
| 1 | **The CLAUDE.md hierarchy** (TS 3.1): team rules in the project's CLAUDE.md, checked into git; personal ones in your home folder; a package's rules in its own subdirectory, or in an import; `/memory` shows what loaded. | Team rules in your own user file, where nobody else gets them. |
| 2 | **Path rules** (TS 3.3): for a convention spread across the tree, like every test file, a rule file in `.claude/rules` with a `paths` glob, loaded only when Claude touches a matching file. | A CLAUDE.md in every directory. |
| 3 | **Commands and skills** (TS 3.2): a skill holds a procedure that runs on demand, and it can fork its own context and limit its tools; CLAUDE.md holds the rules that always apply. | A skill for a rule that must always hold. |
| 4 | **Plan mode** (TS 3.4): plan for a change across many files, an architecture choice, or several valid approaches; go direct for a clear, contained fix. | Plan mode for a one-line fix, or straight to code for a 30-file migration. |
| 5 | **Iterative refinement** (TS 3.5): two or three input and output examples; tests first, then iterate on the failures; or let Claude interview you about the edge cases. | Describe the transformation with more adjectives. |
| 6 | **Large codebases** (TS 5.4): keep a findings file, compact with a focus, send verbose discovery to subagents, and summarize one phase before the next. | Keep one session open until the context degrades. |
| 7 | **MCP and the built-in tools** (TS 2.4, 2.5): a project's `.mcp.json`, with each secret as an environment variable; Grep for content, Glob for paths, Edit with a unique anchor; MCP descriptions strong enough that Claude picks them over Grep. | Secrets in the file, or reading every file to find a symbol. |
| 8 | **Claude Code in CI** (TS 3.6): run `claude -p`, never an invented flag, with `--output-format json` and a JSON schema, so a script can read the result; in a plain `-p` run, CLAUDE.md still loads, and a re-run gets the earlier findings. | A headless variable that doesn't exist, or parsing the prose. |
| 9 | **Explicit criteria** (TS 4.1): list what to report and what to skip, define each severity with an example, and add a switch that turns a noisy category off. | Tell the reviewer to be conservative. |
| 10 | **Few-shot examples** (TS 4.2): two to four examples, each with the plausible alternative and why it's wrong; one root cause is one finding; one example where the answer is none. | Ask the model to be consistent. |
| 11 | **Multi-pass review** (TS 4.6): an independent instance reviews the change, with a pass per file plus a cross-file pass, and a verification pass that gives each finding a confidence. | The session that wrote the code reviews itself, or one bigger context window. |

**Reading a stem:** find the deciding constraint (the one requirement that rules options out), then strike every option that relies on a trap. In CI, nobody is watching: permissions set up front, a schema for the output, and criteria instead of adjectives.

Sources: the CCAR-F exam guide (sections 4 and 5); code.claude.com/docs (How Claude remembers your project, Extend Claude with skills, Best practices for Claude Code, Run Claude Code programmatically); platform.claude.com/docs (Prompting best practices). Models and tools change: confirm details in the official docs.
