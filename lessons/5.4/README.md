# Student kit: Lesson 5.4, Slash commands and skills

Claude Certified Architect – Foundations (CCAR-F) · Module 5: Configuring Claude Code for a Team · Lesson 5.4

This kit holds everything you need to repeat the lesson on your own computer: the three files you write in the lesson, every command and prompt in order, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Turn a workflow into a slash command
2. Write a forked skill with its own tools
3. Pick skill, CLAUDE.md, project or personal

## What's in the kit

| File | What it is |
|---|---|
| `harborline/.claude/commands/run-tests.md` | The project command `/run-tests`: runs one test file, then the whole suite, and reports the counts. `argument-hint: [test-file]`; `allowed-tools` pre-approves only the project's own pytest command |
| `harborline/.claude/skills/review-tool-descriptions/SKILL.md` | The project skill `/review-tool-descriptions`: reviews every tool description in a file against three checks from Lesson 5.3's tools rule. `context: fork` with `agent: Explore` and `background: false`; `allowed-tools: Read Grep Glob`; changes no files |
| `user-level/skills/my-tool-review/SKILL.md` | The personal variant `/my-tool-review`: the same kind of review, plus a full replacement description for each gap. It goes in `~/.claude/skills/my-tool-review/`, in your home folder, never in the repo |
| `commands.txt` | Every command, file and prompt in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |

The `harborline/.claude/` folder starts with a dot, so your file manager may hide it. Show hidden files (Ctrl+H in most Linux file managers, Cmd+Shift+. in the macOS Finder), or open the kit in VS Code.

The video is filmed on Ubuntu 24.04 in the VS Code terminal. The files and the Claude Code commands are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 5.3 done**: your own `harborline` repository in `~/projects/harborline` at the Lesson 5.3 commit (with `.claude/rules/`), its `.venv`, `pytest` passing, and `origin` pointing at your own private `harborline` repository.
- **Claude Code** (Lesson 0.5), signed in, with the `harborline` folder trusted. A recent version: `context: fork`, `agent` and `background` in a skill's front matter need a current Claude Code.
- About 20 minutes. **No API calls: Claude Code runs on your Claude sign-in.** Each command counts toward your Claude Code usage like any other prompt.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### 1. A project command

```bash
git status --short
mkdir -p .claude/commands .claude/skills/review-tool-descriptions
code .claude/commands/run-tests.md
```

`git status --short` prints nothing: the tree is clean. Type the command file (or copy the kit's `harborline/.claude/commands/run-tests.md`), then save with **Ctrl+S**:

```markdown
---
description: Run one test file, then the whole suite, and summarize the result
argument-hint: [test-file]
allowed-tools: Bash(.venv/bin/python -m pytest *)
---

Run .venv/bin/python -m pytest -q $ARGUMENTS, then the whole suite with .venv/bin/python -m pytest -q.
Report the pass and fail counts of each run. For a failure, name the test and the line that failed.
```

- The **file name** becomes the command: `run-tests.md` is `/run-tests`.
- The **front matter**, between the two `---` lines, configures it. `description` says what it does (Claude also reads it to decide when to load a skill). `argument-hint` is shown in the menu as you type. `allowed-tools` lets Claude run the listed tools without asking during the turn that runs the command; here only `.venv/bin/python -m pytest` with any arguments.
- The **body** is the prompt. Whatever you type after the command name replaces `$ARGUMENTS`.

### 2. A forked skill

```bash
code .claude/skills/review-tool-descriptions/SKILL.md
```

Type the skill (or copy the kit's file), then save:

```markdown
---
description: Review the tool descriptions in a file against the team's tool rules. Use when tool definitions change.
argument-hint: [file]
context: fork
agent: Explore
background: false
allowed-tools: Read Grep Glob
---

Review every tool description in $ARGUMENTS. For each tool, check that it:
1. says what the tool returns,
2. says when to use it instead of a similar tool,
3. reports errors through harborline/tool_errors.py.

Answer with one line per tool: its name, then OK or the gap and a suggested fix.
Change no files.
```

- A skill is a **folder** with a `SKILL.md`; the folder name is the command, `/review-tool-descriptions`.
- `context: fork` runs it in a **subagent with a fresh context of its own**; `agent: Explore` picks a read-only subagent type; `background: false` makes you wait for the result in the same turn. The subagent never sees your conversation, so the skill's text has to stand on its own. Only its result comes back into your conversation.

### 3. A personal variant

```bash
mkdir -p ~/.claude/skills/my-tool-review
code ~/.claude/skills/my-tool-review/SKILL.md
```

Type it (or copy the kit's `user-level/skills/my-tool-review/SKILL.md`) and save, then `clear` the terminal:

```markdown
---
description: My quick tool check, with a rewrite I can paste.
argument-hint: [file]
context: fork
agent: Explore
background: false
---

Review the tool descriptions in $ARGUMENTS against the team's rules,
and for each gap write a full replacement description I can paste.
Change no files.
```

It lives in your **home folder**, so it follows you into every project and nobody else gets it. It has a **different name** on purpose: if a personal skill and a project skill share a name, the personal one runs, and you'd quietly shadow the team's version.

### 4. Run them and share

```bash
claude
```

Type `/rev` without pressing Enter. The menu lists the team's `/review-tool-descriptions` with its description, your `/my-tool-review` marked `(user)`, and built-in commands that match, like `/security-review`. Delete the text with Backspace, then run:

```text
/run-tests tests/test_policy.py
```

Claude runs that file (`9 passed`), then the whole suite, and neither run stops for a permission prompt: that's what `allowed-tools` is for. The answer in the lesson: `tests/test_policy.py: 9 passed, 0 failed` and `Full suite: 118 passed, 0 failed`.

```text
/review-tool-descriptions loop/tools.py
```

The work runs nested under the command: the forked subagent reads the tool file and `harborline/tool_errors.py`, searches the backend, and its tool uses fold away. Your conversation only gets the answer: one line per tool. In the lesson five tools passed, and `process_refund` had a gap: its description never says what it returns; the suggested fix adds that it returns the refund record (id, amount, reason, SKU and status). It also noted that Rule 3 is met in code, with two paths that skip it, and that no files were changed.

Then share the two project files:

```text
/exit
```

```bash
clear
git status --short
git add .claude/commands .claude/skills
git commit -m "Lesson 5.4: a /run-tests command and a forked review-tool-descriptions skill"
git push
```

`git status --short` shows two new folders, `?? .claude/commands/` and `?? .claude/skills/`. The commit has 2 files and 24 insertions. Your personal skill isn't in it: it lives in your home folder, not in the repo. Your team gets both project files the next time they pull.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Your personal skills folder | `~/.claude/skills/` | `%USERPROFILE%\.claude\skills\` |
| Make the folders | `mkdir -p …` | PowerShell: `New-Item -ItemType Directory -Force -Path .claude\commands, .claude\skills\review-tool-descriptions` and `New-Item -ItemType Directory -Force -Path $HOME\.claude\skills\my-tool-review` |
| The pytest command in `run-tests.md` | `.venv/bin/python -m pytest` | `.venv\Scripts\python -m pytest`: change it in both the body and `allowed-tools` |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+S to save, Cmd+` for the terminal).

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` at the start | nothing: the tree is clean |
| `/rev` in Claude Code | `/review-tool-descriptions` with its description; `/my-tool-review … (user)`; built-ins such as `/security-review` |
| `/run-tests tests/test_policy.py` | two Bash runs, no permission prompt; `9 passed, 0 failed`; full suite `118 passed, 0 failed` |
| `/review-tool-descriptions loop/tools.py` | runs nested (forked Explore subagent); one line per tool; five OK; `process_refund` never says what it returns; "No files were changed." |
| `git status --short` after | `?? .claude/commands/` and `?? .claude/skills/` |
| The commit | 2 files changed, 24 insertions; the personal skill not included |
| API spend | $0: Claude Code on the subscription, no API calls |

See `expected-output.md` for the exact lines.

## Troubleshooting

- **`/run-tests` doesn't appear in the menu**: check the path (`.claude/commands/run-tests.md`, in the folder where you started `claude`) and that the file starts with `---`. Restart Claude Code if you created the folder during a session.
- **`/run-tests` asks for permission anyway**: the command Claude runs must match the `allowed-tools` pattern exactly (`.venv/bin/python -m pytest …`). On Windows, use the `Scripts` path in both places.
- **The skill doesn't run in a subagent**: check `context: fork` in the front matter and update Claude Code (Lesson 0.5); older versions ignore fields they don't know.
- **`/my-tool-review` is missing or not marked `(user)`**: the file must be at `~/.claude/skills/my-tool-review/SKILL.md`, in your home folder, not in the repo.
- **The review finds different gaps**: Claude's wording changes from run to run. The `process_refund` gap is a fact of the course code; if your review misses it, run it again.
- **`git status` shows other files**: something else changed since Lesson 5.3. Commit only the two folders, as in the lesson.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Slash command:** a Markdown prompt you run as `/name`; project (`.claude/commands/`) or personal (`~/.claude/commands/`). Commands are now merged into skills.
- **Skill:** a folder with a `SKILL.md`; it runs as `/name`, and Claude can also load it when its description fits the task.
- **`$ARGUMENTS`:** whatever you type after the command name.
- **`allowed-tools`:** tools Claude can use without asking during the turn that runs the skill; `disallowed-tools` removes tools.
- **`context: fork`:** runs the skill in a subagent with its own context; it doesn't see your conversation.

Claude Code changes often. If a field, a menu or a message doesn't match what you see, follow the official page, Extend Claude with skills (https://code.claude.com/docs/en/skills).
