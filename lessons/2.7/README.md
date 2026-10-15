# Student kit: Lesson 2.7, Built-in tools: Read, Write, Edit, Bash, Grep, Glob

Claude Certified Architect – Foundations (CCAR-F) · Module 2: Tool Design & MCP Integration · Lesson 2.7

This kit holds everything you need to repeat the lesson on your own computer: the one file changed in the lesson, every command and prompt in order, what each step printed in the lesson, what differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Pick Grep for content and Glob for file names
2. Edit with a unique anchor, or fall back to Read + Write
3. Explore step by step: search, read, follow the names

## What's in the kit

| File | What it is |
|---|---|
| `legacy/warehouse/records.py` | The file after the lesson's one Edit: inside `read_record`, the local variable `record` is now `order` (six lines). Nothing else in the file changed |
| `commands.txt` | Every command and prompt typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

In this lesson you don't type code: you ask Claude Code, and Claude makes the change. Use the kit's `records.py` to compare with yours afterwards. If Claude's edit went wrong, you can copy it over yours.

The video is filmed on Ubuntu 24.04. The commands are the same on Windows, macOS and Linux except `clear`; one thing about the tools themselves differs on Windows: see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 2.6 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, the `legacy/warehouse` package from the starter, `pytest` passing, and `origin` pointing at your own private `harborline` on GitHub.
- **Claude Code** (Lesson 0.5), signed in, with the `harborline` folder trusted (Lesson 2.6).
- About 20 minutes. **No API calls: Claude Code runs on your Claude sign-in.** Each prompt counts toward your Claude Code usage like any other.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Start every session from the `harborline` folder.

### 1. The default tool set

```bash
clear; claude
```

Ask:

```text
Where does the name getStatus come from? Trace it to the function that actually runs, file by file.
```

Watch the first move. In the lesson it was `Bash(git grep -n "getStatus" …)`: on macOS, Linux and WSL, today's Claude Code leaves Grep and Glob out of its default tools and searches with `grep` and `find` through Bash. Then `Read 1 file`, and the answer walked the chain:

- `legacy/warehouse/codes.py` defines the real function, `status_name(code)`.
- `legacy/warehouse/compat.py` binds it to a second name: `getStatus = status_name`. A plain assignment: the same function.
- `legacy/warehouse/__init__.py` imports `getStatus` from `compat` and lists it in `__all__`: a re-export.
- `tests/test_legacy.py` calls `warehouse.getStatus(3)`, which runs `status_name(3)` and returns `"shipped"`.

**Ctrl+O** shows the detailed transcript; **Ctrl+O** again hides it. Then `/exit`.

### 2. Grep and Glob as tools

```bash
clear; claude --allowedTools Grep Glob
```

Naming either tool when you start a session brings both back. Ask the same question again, word for word:

```text
Where does the name getStatus come from? Trace it to the function that actually runs, file by file.
```

In the lesson: `Searched for 1 pattern, read 3 files`, then one more search, `"status_name|STATUS_NAMES"`, for the function `getStatus` points to. Search, read, follow the name. The same chain as before; "A repo-wide search found only those four hits." This time the search was a tool call, which Claude Code can show, permit and limit like any other tool.

Then a question about names, not contents:

```text
Find every Python test file in this repo, names like test_*.py, at any depth.
```

Claude reaches for Glob with `**/test_*.py`: nine files, all in `tests/`. In the lesson it added that the search also matched about 25 files under `.venv/`, test files of installed packages, and left them out: Glob doesn't respect `.gitignore` by default (Grep does).

### 3. One Edit, one anchor

In the same session, ask:

```text
In legacy/warehouse/records.py, rename the local variable record to order inside read_record.
```

Claude reads the file first, then makes **one** Edit. The word `record` appears many times inside `read_record`, and once more inside the name `read_record` itself, so a one-word `old_string` isn't unique, and `replace_all` would rename the function too. The Edit's anchor is the function's body: lines that match one place only. In the lesson, Claude then ran the legacy tests on its own (`3 passed in 0.03s`) and summed up: all four uses changed (the copy, the loop body, the status line and the return), same behavior.

**Ctrl+O** shows the whole diff. Then:

```text
Run the legacy tests.
```

`pytest tests/test_legacy.py -v`: all three pass: `test_status_codes_and_old_names`, `test_reading_a_legacy_record`, `test_the_old_shipping_rule`. Then `/exit`.

The lesson's Claude Code ran in auto mode, where it checks each tool call and runs the safe ones without asking ("Allowed by auto mode classifier"). If yours asks first, read the call and approve it: the searches and reads, the one Edit to `records.py`, and `pytest`.

### 4. Commit

```bash
clear; git diff --stat
git diff
git add legacy/warehouse/records.py
git commit -m "Lesson 2.7: rename a local variable with one Edit (a unique anchor)"
git push
```

`git diff --stat`: `legacy/warehouse/records.py | 12 ++++++------`, `1 file changed, 6 insertions(+), 6 deletions(-)`. `git diff` shows only the variable's name changing, nothing else in the file. Compare your `records.py` with the kit's.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Clear, then run | `clear; claude` | PowerShell: the same line. cmd.exe: `cls`, then `claude` on its own line |
| Grep and Glob in a plain `claude` session | not in the default tools: Claude searches with `grep` and `find` through Bash | in the default tools |
| `claude --allowedTools Grep Glob` | brings Grep and Glob back | Grep and Glob, as by default |

On Windows, step 1 will likely show the Grep tool where the lesson showed Bash: that's the difference the lesson talks about. The answer and the lesson's point stay the same: search contents one way, find names another. **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl**; in Claude Code, **Ctrl+O** is still Ctrl.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| Default session, the getStatus question | `Bash(git grep -n "getStatus" …)`, `Read 1 file`; the chain: `codes.py` → `compat.py` (`getStatus = status_name`) → `__init__.py` (re-export) → `tests/test_legacy.py` |
| `claude --allowedTools Grep Glob`, the same question | `Searched for 1 pattern, read 3 files`, then `"status_name|STATUS_NAMES"`; the same chain; four hits in the repo |
| The test-file question | Glob `**/test_*.py`: nine files in `tests/`; about 25 more under `.venv/`, left out |
| The rename | `Reading 1 file`, one Edit (the body of `read_record`), Claude's own test run: `3 passed in 0.03s` |
| `Run the legacy tests.` | `pytest … -v`: all 3 legacy tests pass |
| `git diff --stat` | `1 file changed, 6 insertions(+), 6 deletions(-)` |
| `git commit` | `Lesson 2.7: rename a local variable with one Edit (a unique anchor)` |
| API spend | $0: Claude Code on the subscription, no API calls |

See `expected-output.md` for the exact lines and what should match.

## Troubleshooting

- **No `legacy/warehouse` folder**: it comes with the starter repository (Lesson 0.6). Check `git log --oneline` and that you're in your own `harborline`.
- **Claude uses the Grep tool in a plain session**: you're on native Windows, or your Claude Code's settings already allow Grep and Glob. That's fine: compare with step 2.
- **`--allowedTools` isn't recognized**: update Claude Code (Lesson 0.5), then check `claude --help` for the flag.
- **Claude read every file instead of searching**: ask again with the lesson's exact words. Answers vary from run to run; the moves are what to watch.
- **The rename touched `read_record`'s name, or `records` elsewhere**: undo it with `git checkout legacy/warehouse/records.py` and ask again, or copy the kit's file.
- **Claude asks before each tool call**: your Claude Code isn't in auto mode. Approve the calls listed in step 3, or press **Shift+Tab** to cycle the permission mode.
- **The legacy tests fail after the rename**: compare your `records.py` with the kit's; a missed `record` inside the function is the usual cause.
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Grep**: searches file contents for a pattern, like a function name, an error message or an import.
- **Glob**: finds files by name pattern, such as `**/test_*.py`; it doesn't respect `.gitignore` by default.
- **Edit**: exact string replacement; the old string must appear exactly once in the file (or use `replace_all` when every copy should change).
- **Unique anchor**: enough of the surrounding text that the string to replace matches one place only.
- **Re-export**: a module making a name available under another name (`getStatus = status_name`), traced one name at a time.

## Sources (all checked 2026-10-15)

- **Claude Code docs, Tools reference.** https://code.claude.com/docs/en/tools-reference : Glob tool behavior (left out of the default tool set on macOS, Linux and WSL; naming either tool restores both; Grep finds lines inside files; Glob and gitignored files), Edit tool behavior (exact string replacement; must appear exactly once; a longer string or replace_all), Read (contents with line numbers), Write (creates or overwrites a whole file; Edit for partial changes).
- **Claude Code docs, How Claude Code works.** https://code.claude.com/docs/en/how-claude-code-works : gather context, take action, verify results; the five categories of built-in tools; search: find files by pattern, search content with regex.
- **Anthropic, *Claude Certified Architect – Foundations Exam Guide*.** Version 1.0, effective July 2026: Task Statement 2.5 (Domain 2), Scenario 4: Developer Productivity with Claude and Scenario 2: Code Generation with Claude Code.

Claude Code changes often. If a tool, a message or a screen doesn't match what you see, follow the official page.

## What's next

Lesson 2.8 brings Module 2 together: its traps and a recap.
