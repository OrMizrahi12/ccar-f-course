# Student kit: Lesson 5.9, Module 5 exam traps and recap

Claude Certified Architect – Foundations (CCAR-F) · Module 5: Configuring Claude Code for a Team · Lesson 5.9

This lesson adds no code. It goes back over Module 5 using the module's own sessions. By the end of it you can:

1. Spot Module 5's eight classic traps
2. Ask who needs it, and when
3. Hold Module 5 on one page

## What's in the kit

| File | What it is |
|---|---|
| `module-5.md` | The Module 5 cheat sheet: one row per lesson, plus the eight traps and why each one is wrong |

## The question that settles most of them

**Who needs this, and when?**

- **Who:** the whole team, so it's committed with the repository (the project `CLAUDE.md`, `.claude/rules/`, `.claude/skills/`, `.mcp.json`), or just me, so it stays out of git (`~/.claude/...`, `CLAUDE.local.md`, a user-scope MCP server).
- **When:** every session (`CLAUDE.md`, rules without `paths`), only for some files (rules with `paths`), or on demand (a skill or a command).

## The eight traps

| Trap | It sounds like | The fix it hides |
|---|---|---|
| Keep it personal | "Put it in ~/.claude." "Each developer adds it to their own settings." "Add the server at user scope." | Team rules in the project `CLAUDE.md`, `.claude/rules/` or `.claude/skills/`; team servers in `.mcp.json`, each developer's token as `${VAR}`; all committed. Keep your home folder for your own preferences. To block a command, use a deny rule: an instruction is not enforcement. |
| Invent a config file | ".claude/config.json." "Coding standards inside settings.json." "An instructions field in .mcp.json." | Instructions come from `CLAUDE.md` files and their `@` imports, `.claude/rules/` and skills. Settings hold permissions and options; `.mcp.json` holds servers. |
| Wrong home for the knowledge | "A skill for always-on rules." "Paste the 300-line checklist into CLAUDE.md." "A command for the coding style." | `CLAUDE.md` and rules without `paths` load every session; a skill's body loads only when it's used. Always-needed rules in `CLAUDE.md` or a rule; an occasional procedure in a skill, forked when its output is long; a personal variant under its own name. |
| A CLAUDE.md in every folder | "Copy the testing rules into every folder's CLAUDE.md." | One `.claude/rules/` file with `paths:` globs, loaded when Claude reads or edits a matching file. A folder with rules of its own can still have its own `CLAUDE.md`. |
| One way of working | "Always use plan mode to be safe." "Skip planning, review the diff afterwards." "Bypass permissions to go faster." | Direct for a diff you can describe in one sentence; plan mode, with Explore for the discovery, for many files, open designs or risk. The permission mode by risk, deny rules for what must never run. |
| Say it louder | "Describe the format in more detail." "Tell Claude it's still wrong." "Raise the effort level." | Let Claude interview you, give 2 or 3 input → output examples, write the tests first and share the failing output. Interacting issues together, independent ones one at a time. |
| One long conversation | "Keep going in the same session." "Ask Claude to be more specific." "/clear and ask again." | Explore subagents per area, findings in a scratchpad file, `/compact <focus>`, the next phase from a summary. `/clear` is for switching to an unrelated task. |
| Force the tool | "Remove Grep so the agent must use the MCP tool." "Tell it to prefer MCP tools in general." "bypassPermissions so it can run anything." | Tool descriptions that say what the tool returns and when to use it instead of Grep; `allowed_tools` with the exact test command under `dontAsk`; check the agent's claims yourself. |

## Where the sessions come from

Every session in the lesson was recorded in an earlier lesson. To repeat one, use that lesson's kit:

- **Lesson 5.2** (trap 1): a teammate's fresh clone answered "I wasn't given any rules specific to this repository" before anything was committed; after the commit and push, the same question quoted the project `CLAUDE.md` and both `@docs/conventions/...` imports. Reading `support/agent.py` printed `Loaded support/CLAUDE.md` (trap 4).
- **Lessons 5.2 and 5.3** (trap 2): the project `CLAUDE.md` with its two imports; `.claude/rules/testing.md` with `paths: "tests/**/*.py"`.
- **Lesson 5.4** (trap 3): typing `/rev` listed the project skill `/review-tool-descriptions` and the personal `/my-tool-review` marked `(user)`; the forked review answered one line per tool and said "No files were changed."
- **Lesson 5.3** (trap 4): reading `harborline/costs.py` loaded no rules; reading a test file printed `Loaded .claude/rules/testing.md`; reading `mcp_server/server.py` printed `Loaded .claude/rules/tools.md`.
- **Lesson 5.5** (trap 5): the free-shipping fix went direct (`>` to `>=`, the test file and the whole suite passed); retiring `legacy/warehouse/compat.py` went through plan mode, an Explore agent and an approved plan.
- **Lesson 5.6** (trap 6): Claude's interview asked nine questions, one of them about naive ISO strings; the tests written first gave 5 failed, 1 passed (that one for the wrong reason, as Claude said); then 6 of 6 and the full suite passed.
- **Lesson 5.7** (trap 7): three Explore agents mapped the refund path, their findings went into `notes/exploration.md`, then `/compact` with a focus, and phase 2 started from the file.
- **Lesson 5.8** (trap 8): the explorer called `trace_export` first and answered in 3 turns without Grep. In the boilerplate run, `dontAsk` refused a chained shell command, the agent said it couldn't run the tests, and the developer's own `.venv/bin/python -m pytest -q` gave 129 passed.

Each result comes from one session on the day it was recorded, so yours will differ. This lesson made no API calls and cost nothing.

## Next

1. **Lab 5: the repository, set up for a team**, in the course materials under `labs/L5/`: share the `codemap` server in `.mcp.json`, add a rule that loads only for `devtools/`, write a forked, read-only skill, decide plan or direct for three tasks, and check it all with the self-check tests.
2. **The Module 5 quiz**: 14 questions, three of them from Modules 2 to 4. This lesson has no quick check, because the quiz takes its place.

## Sources (checked 2026-10-17)

- Best practices for Claude Code: https://code.claude.com/docs/en/best-practices
- Choose a permission mode: https://code.claude.com/docs/en/permission-modes
- How Claude remembers your project: https://code.claude.com/docs/en/memory
- Extend Claude with skills: https://code.claude.com/docs/en/skills
- Connect Claude Code to tools via MCP: https://code.claude.com/docs/en/mcp
- Agent SDK, Configure permissions: https://code.claude.com/docs/en/agent-sdk/permissions
- Claude Certified Architect – Foundations Exam Guide: Domain 3, Task Statements 3.1 to 3.5, 2.4, 2.5 and 5.4, Scenarios 2 and 4

Models and tools change. Always confirm current details in the official docs.
