# Lab 5: the repository, set up for a team

Claude Certified Architect – Foundations (CCAR-F) · Module 5: Configuring Claude Code for a Team · the module checkpoint

In Module 5 you set Harborline up so that Claude Code works the same way for everyone who clones it. The project CLAUDE.md is short and imports its conventions. Rules in `.claude/rules/` load only for the files they name. A command and a skill run the team's routines on demand. You chose plan mode or direct execution per task, refined a change test-first, explored the code in phases, and built `devtools/`: an Agent SDK explorer and the `codemap` MCP server.

In this lab you finish that setup for the new `devtools/` folder and check it in code. Everything a teammate needs comes with `git clone`; nothing personal or secret goes into git.

You pass the lab when the self-check tests pass and `/map-module legacy.warehouse` answers from a forked, read-only skill.

## What you start from

`starter/` is the `harborline` project exactly as it stands after Lesson 5.8: everything from Modules 1 to 4, the Module 5 configuration (`CLAUDE.md` with its imports, `.claude/rules/`, `.claude/commands/run-tests.md`, `.claude/skills/review-tool-descriptions/`), and `devtools/` from Lesson 5.8. If your own project is there too, keep working in it. If not, copy `starter/` to `~/projects/harborline`, create the virtual environment, install `requirements.txt`, and add your `.env` with `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6 show how).

`solution/` is a finished version to compare with when you're done. `tests/` holds the self-check.

## What you change

- `.mcp.json`: add the `codemap` server next to `harborline`.
- `.claude/rules/devtools.md`: new. A rule that loads only for `devtools/`.
- `.claude/skills/map-module/SKILL.md`: new. A forked, read-only skill.
- `notes/plan-or-direct.md`: new. Three tasks, one choice each.

## Steps

### 1. Share the codemap server (Lessons 2.6 and 5.8)
Lesson 5.8's explorer starts `codemap` itself. Claude Code doesn't know about it yet. Add it to the project's `.mcp.json`, next to `harborline`: `type` stdio, `command` `.venv/bin/python`, `args` `["-m", "devtools.codemap_server"]`. `codemap` needs no secret. Leave the `harborline` entry as it is: its token is `${HARBORLINE_API_TOKEN}`, which each developer sets in their own environment.

Then see the other scope once. Add a personal copy under another name, list the servers, and remove it:
```bash
claude mcp add --scope user codemap-mine -- "$PWD/.venv/bin/python" "$PWD/devtools/codemap_server.py"
claude mcp list
claude mcp remove --scope user codemap-mine
```

In our practice run, `claude mcp add` wrote `codemap-mine` to the user config (`~/.claude.json`), which no teammate ever sees. `claude mcp list` showed it connected, and listed `harborline` and `codemap` from the project's `.mcp.json` as pending approval: Claude Code asks once before it starts a server that came with the repository. It also warned that `HARBORLINE_API_TOKEN` was missing in that shell. That warning is the expansion working: the file names the variable, and the value lives only on your machine.

### 2. A rule for devtools/ (Lessons 5.3 and 5.8)
Create `.claude/rules/devtools.md` with `paths: ["devtools/**"]` in its frontmatter, and three short rules from Lesson 5.8: agents here load no Claude Code settings (`setting_sources=[]`); each agent gets an explicit tools list, `allowed_tools`, `permission_mode="dontAsk"` and a `max_budget_usd`; MCP tool descriptions say what the tool returns and when to use it instead of Grep. It loads only when Claude reads or edits a file under `devtools/`, so the rest of the repository never pays for it.

### 3. A forked, read-only skill (Lesson 5.4)
Create `.claude/skills/map-module/SKILL.md`. In its frontmatter:
- a `description` that says what it maps and when to use it, and `argument-hint: [module]`
- `context: fork` and `agent: Explore`, so the mapping runs in its own context
- `allowed-tools` with `mcp__codemap__list_public_names`, `mcp__codemap__trace_export` and `Read`
- `disallowed-tools: Write Edit Bash`, so it can't change anything

In the body, tell it to list the package's public names, trace each re-exported one to its real definition, and answer with one table: name, defined in (file:line), original name if it was renamed. Use `$ARGUMENTS` for the module.

Then run it in Claude Code: `/map-module legacy.warehouse`. In our practice run, it called `list_public_names` once and `trace_export` for each of the four names `legacy.warehouse` exports now (Lesson 5.5 retired the old `compat.py` names). Its table showed `load_record` at `legacy/warehouse/records.py:15`, originally `read_record`, and `shipping_quote` at `shipping.py:7`, originally `quote`. It also tried one Bash command, which the skill's `disallowed-tools` refused, and it said "I made no file changes." The run cost under half a cent.

### 4. Plan or direct (Lesson 5.5)
Decide how you'd start each of these tasks, and write the decision to `notes/plan-or-direct.md`, one line each, in the form `A: direct. <why>` or `A: plan. <why>`:

- **A.** `trace_export` in `devtools/codemap_server.py` gives up after 10 re-exports. Raise the limit to 20.
- **B.** Give every Agent SDK agent in `support/`, `research/` and `devtools/` a budget limit read from one setting in `harborline/config.py`, instead of the numbers each one sets now.
- **C.** Make `codemap` remember files it has already parsed, so repeated questions are faster.

Don't make the changes. The lab checks the decisions.

## Check your work

1. Copy `labs/L5/tests/test_lab5.py` into your project's `tests/`, and run the whole suite:
   ```bash
   .venv/bin/python -m pytest -q
   ```
   Our solution: `134 passed` (the starter's 129 tests plus the lab's 5). On the starter, four of the five lab tests fail; the `CLAUDE.md` imports test already passes, since Lesson 5.2 set them up. It needs no key and costs nothing. It covers:
   - `.mcp.json` lists `harborline` and `codemap`, the token is `${HARBORLINE_API_TOKEN}`, and no key or token is written in the file
   - every `@` import in `CLAUDE.md` points to a file that exists
   - every rule in `.claude/rules/` has `paths`, `devtools.md` is one of them, and each pattern matches at least one file
   - `map-module` has a description and an argument hint, runs forked in Explore, can call `trace_export`, and can't use Write, Edit or Bash
   - the three plan-or-direct decisions
2. Run `/map-module legacy.warehouse` once (step 3) and check that the table names where `load_record` really comes from.

## Compare with the solution

`solution/` holds one way to do it. Other wordings pass too: the tests check the structure, not the exact text of your rules, your skill's instructions or your reasons in `notes/plan-or-direct.md`.
