# Student kit: Lesson 5.3, Rules and path-scoped conventions

Claude Certified Architect – Foundations (CCAR-F) · Module 5: Configuring Claude Code for a Team · Lesson 5.3

This kit holds everything you need to repeat the lesson on your own computer: the two rule files written in the lesson, every command and prompt in order, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Split instructions into rule files
2. Scope a rule to the files it governs
3. Choose a path rule or a folder's CLAUDE.md

## What's in the kit

| File | What it is |
|---|---|
| `harborline/.claude/rules/testing.md` | The testing rule (10 lines). Its frontmatter scopes it to `tests/**/*.py`, every Python file under `tests/`; three testing conventions follow |
| `harborline/.claude/rules/tools.md` | The tool-definitions rule (11 lines). Its frontmatter lists three paths: `loop/tools.py`, `mcp_server/**` and `support/tools.py`; two conventions for tool descriptions and tool errors follow |
| `commands.txt` | Every command, prompt and key in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |

The two rule files are exactly the ones committed in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `harborline/.claude/rules/` folder into your `harborline` folder (the folder name starts with a dot, so your file manager may hide it).

The video is filmed on Ubuntu 24.04, in the VS Code terminal. Claude Code behaves the same on Windows, macOS and Linux; a few shell commands differ, see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 5.2 done**: your own `harborline` repository in `~/projects/harborline` at the Lesson 5.2 commit (the project `CLAUDE.md` with its two imports, and `support/CLAUDE.md`), pushed, with `origin` pointing at your own private `harborline` repository.
- **Claude Code** (Lesson 0.5), signed in, with the `harborline` folder trusted.
- About 15 minutes. **No API calls: Claude Code runs on your Claude sign-in.** Each prompt counts toward your Claude Code usage like any other.

## How rules load (the lesson's summary)

| A file in `.claude/rules/` | When it loads |
|---|---|
| No frontmatter (an unconditional rule) | At launch, in every session, with the same priority as `CLAUDE.md` |
| A `paths:` list of globs in its frontmatter | On demand: when Claude uses the Read, Write or Edit tool on a matching file, or views one with a Bash command such as `cat` or `head` |
| Frontmatter whose YAML doesn't parse | Claude Code ignores the frontmatter and loads the rule as if it had no `paths` |

A glob is a file pattern: `tests/**/*.py` matches every Python file under `tests/`, in any subfolder; `**/*.ts` matches every TypeScript file in any folder; a plain path such as `loop/tools.py` matches that one file.

**A path rule or a folder's CLAUDE.md?** Ask what the convention follows. One folder: a `CLAUDE.md` in that folder is enough (it loads when Claude works with files there, like `support/CLAUDE.md` from Lesson 5.2). A kind of file spread across the tree (tests, tool definitions in three folders): one path rule, one list of globs, nothing to copy into every folder.

Rules are context, not enforcement: when something must hold every time, use a hook (Lesson 3.4) or a test.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). **Ctrl+J** hides and shows the terminal panel; the lesson hides it while typing a file.

### 1. Two scoped rules

```bash
git status --short
mkdir -p .claude/rules
code .claude/rules/testing.md
```

`git status --short` prints nothing: the tree is clean. `code` opens a new, empty file. Type the kit's `testing.md` and save (**Ctrl+S**):

```markdown
---
paths:
  - "tests/**/*.py"
---

# Tests

- Name each test for the behavior it checks.
- Build small order dicts inside the test. Never edit data/*.json for a test.
- Run the one test file first, then the whole suite.
```

The block between the two `---` lines is the frontmatter. Both `---` lines start at the very beginning of their line, and `paths:` holds a YAML list.

Back in the terminal (**Ctrl+`**):

```bash
code .claude/rules/tools.md
```

Type the kit's `tools.md` and save:

```markdown
---
paths:
  - "loop/tools.py"
  - "mcp_server/**"
  - "support/tools.py"
---

# Tool definitions

- A description says what the tool returns, and when to use it instead of a similar tool.
- Errors go through harborline/tool_errors.py: errorCategory, isRetryable and a message.
```

Harborline defines tools in three places (the agent loop, the MCP server folder, the support agent), so this rule lists three paths. Then `clear` the terminal.

### 2. Watch them load

```bash
claude
```

Keep `tools.md` open in the editor, as in the lesson: the prompt shows a chip `In tools.md` (the editor tells Claude which file is open). Then ask three times, one file each:

```text
Read harborline/costs.py. Then quote any rules from .claude/rules that you were given, or say there are none.
```

```text
Read tests/test_policy.py. Then quote any rules from .claude/rules that you were given, or say there are none.
```

```text
Read mcp_server/server.py. Then quote any rules from .claude/rules that you were given, or say there are none.
```

- `harborline/costs.py` matches no rule: `Read 1 file, listed 1 directory`, and no `Loaded` line. Claude says no rules from `.claude/rules` were given, even though `tools.md` is open in the editor: an open tab isn't a read.
- `tests/test_policy.py` matches `tests/**/*.py`: under `Read 1 file`, Claude Code prints `Loaded .claude/rules/testing.md`, and Claude quotes the three testing rules.
- `mcp_server/server.py` matches `mcp_server/**`: `Loaded .claude/rules/tools.md`, and Claude quotes both tool rules.

In the lesson, the second and third answers also said the previous answer was "wrong". It wasn't: each rule loaded only with its first matching read.

Scroll back up to compare the three reads. Then:

```text
/context
```

Scroll up to the grid. `Memory files` counts what loaded at launch (295 tokens in the lesson: your user file, `CLAUDE.md` and its two imports, as at the end of Lesson 5.2). The two rules aren't counted there: they loaded on demand, later, with the reads.

```text
/exit
```

### 3. Commit and share

```bash
clear
git status --short
git add .claude/rules
git commit -m "Lesson 5.3: path-scoped rules for tests and for tool definitions"
git push
```

`git status --short` shows `?? .claude/` (the new folder is untracked). `git add .claude/rules` adds the rules folder only. Every teammate who pulls gets both rules, and they load for them the same way.

## Windows, macOS and Linux

| | Linux and macOS (the lesson) | Windows (PowerShell) |
|---|---|---|
| Make the folder | `mkdir -p .claude/rules` | `mkdir .claude\rules` (PowerShell creates the parent folder too) |
| Open a rule file in VS Code | `code .claude/rules/testing.md` | `code .claude\rules\testing.md` |
| Inside the rule files | the globs use forward slashes: `tests/**/*.py` | the same: write the globs with forward slashes, as in the docs' examples |
| Clear the terminal | `clear` | `clear` or `cls` |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save, Cmd+J for the panel). Finder hides folders whose names start with a dot; **Cmd+Shift+.** shows them. **WSL** follows the Linux column.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| Claude Code | v2.1.301, Haiku 5.5, signed in with a subscription |
| Reading `harborline/costs.py` | `Read 1 file, listed 1 directory`; no `Loaded` line; "No rules from .claude/rules were given to me in this conversation." |
| Reading `tests/test_policy.py` | `Read 1 file` + `Loaded .claude/rules/testing.md`; the three testing rules quoted |
| Reading `mcp_server/server.py` | `Loaded .claude/rules/tools.md`; both tool rules quoted |
| `/context` | Memory files 295 tokens; Messages 19k tokens |
| The commit | `[main b46b623] Lesson 5.3: …`, 2 files changed, 21 insertions(+) |
| API spend | $0: Claude Code on the subscription, no API calls |

See `expected-output.md` for the exact lines.

## Troubleshooting

- **A path rule loads in every session** (or `/context` counts it at launch): the frontmatter doesn't parse, so Claude Code treats the rule as if it had no `paths`. Check that the first line is exactly `---`, that the closing `---` starts at the beginning of its line, and that each list item is `  - "pattern"` under `paths:`. VS Code may keep the previous line's indent when you press Enter in a Markdown file: delete the extra spaces. `claude --debug` shows the parse error.
- **No `Loaded` line when Claude reads a test file**: the path must match the glob from the repo root (`tests/test_policy.py` matches `tests/**/*.py`). Claude must read, write or edit the file; having it open in the editor doesn't count.
- **The rule files don't load at all**: they must sit in `.claude/rules/` at the project root (with the dot) and end in `.md`. Rules are skipped when you start Claude Code with `--setting-sources` without `project`.
- **Claude's wording differs**: its answers depend on the model and the session. What should match: which reads print a `Loaded` line, and which rules get quoted.
- **`/context` numbers differ**: they depend on your account's skills and connectors and on your own `~/.claude/CLAUDE.md`.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **`.claude/rules/`**: a folder of topic rule files, committed with the project.
- **`paths:` frontmatter**: glob patterns that scope a rule to matching files.
- **Glob**: a file pattern: `tests/**/*.py` = every Python file under `tests/`.
- **Unconditional rule**: a rule with no `paths`; it loads at launch, like CLAUDE.md.
- **On-demand load**: a scoped rule enters the context when Claude reads, writes or edits a matching file.

## Sources (all checked 2026-10-17)

- **Claude Code docs, How Claude remembers your project.** https://code.claude.com/docs/en/memory : "Organize rules with `.claude/rules/`" (one topic per file, discovered recursively, committed for the team); rules without `paths` frontmatter load at launch with the same priority as `.claude/CLAUDE.md`; "Path-specific rules" (a path-scoped rule loads when Claude uses the Read, Write, or Edit tool on a matching file, or a Bash command that counts as a read); the glob pattern table; the rule frontmatter reference (`paths` is the only field; frontmatter that doesn't parse is ignored); CLAUDE.md files under 200 lines; subdirectory CLAUDE.md files load on demand; `/context` shows the CLAUDE.md and rules files loaded at launch; context, not enforced configuration.
- **Anthropic, *Claude Certified Architect – Foundations Exam Guide*.** Version 1.0, effective July 2026: Task Statements 3.3 and 3.1 (Domain 3) and Scenario 2: Code Generation with Claude Code.

Claude Code changes often. If a screen or a message doesn't match what you see, follow the official page.

## What's next

Lesson 5.4: slash commands and skills, for procedures you load only when you need them.
