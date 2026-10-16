# Student kit: Lesson 5.2, The CLAUDE.md hierarchy

Claude Certified Architect – Foundations (CCAR-F) · Module 5: Configuring Claude Code for a Team · Lesson 5.2

This kit holds everything you need to repeat the lesson on your own computer: the instruction files written in the lesson, every command and prompt in order, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Put each instruction at the right level
2. Keep CLAUDE.md short with imports
3. Check what loaded, and fix what didn't

## What's in the kit

| File | What it is |
|---|---|
| `harborline/CLAUDE.md` | The project instructions (14 lines), at the root of the repo, committed: what Harborline is, the test commands, two imports (`@docs/conventions/money.md`, `@docs/conventions/dates.md`) and the commit rule |
| `harborline/docs/conventions/money.md` | Imported by `CLAUDE.md` (4 lines): amounts are US dollars, rounded to cents only at the end; refund amounts come from `policy.check_refund`, never computed by hand |
| `harborline/docs/conventions/dates.md` | Imported by `CLAUDE.md` (4 lines): orders mix Unix seconds, ISO 8601 with offsets and plain dates; read them through `harborline.normalize`, never parse the raw fields |
| `harborline/support/CLAUDE.md` | The support folder's own rules (4 lines): a refund above $500 goes to a team lead; gates and hooks are the rules. It loads only when Claude works with a file in `support/` |
| `user-level/CLAUDE.md` | Your user file at the end of the lesson (`~/.claude/CLAUDE.md`, 3 lines): only the personal preference "Keep answers short." It is not part of the repo |
| `commands.txt` | Every command, prompt and key in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |

The four `harborline/` files are exactly the ones committed in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `harborline/CLAUDE.md`, `docs/` and `support/CLAUDE.md` into your `harborline` folder.

The video is filmed on Ubuntu 24.04, in the VS Code terminal. Claude Code behaves the same on Windows, macOS and Linux; a few shell commands differ, see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 5.1 done**: your own `harborline` repository in `~/projects/harborline` at the Lesson 5.1 commit, pushed, with `origin` pointing at your own private `harborline` repository.
- **Claude Code** (Lesson 0.5), signed in, with the `harborline` folder trusted.
- No `~/.claude/CLAUDE.md` yet (if you have one, see [Troubleshooting](#troubleshooting)).
- About 20 minutes. **No API calls: Claude Code runs on your Claude sign-in.** Each `claude -p` counts toward your Claude Code usage like any other prompt.

## Where instructions live (the lesson's table)

| Level | File | Who gets it |
|---|---|---|
| User | `~/.claude/CLAUDE.md` | only you, in every project |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | everyone who clones the repo (it's committed) |
| Local | `./CLAUDE.local.md` | only you, in this project (add it to `.gitignore`) |
| Subdirectory | `<folder>/CLAUDE.md` | everyone; it loads when Claude works with a file in that folder |
| Managed policy | a system path your organization manages | everyone on that machine |

At launch Claude Code loads the CLAUDE.md files in the folder you start in and in every folder above it, and concatenates them (nothing overrides anything). Subdirectory files load on demand. `@path` imports load at launch with the file that imports them.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). **Ctrl+J** hides and shows the terminal panel; the lesson hides it while typing a file.

### 1. The rules nobody else gets

```bash
git status --short
code ~/.claude/CLAUDE.md
```

`git status --short` prints nothing: the tree is clean. `code` opens a new, empty file in the `.claude` folder of your home directory: your **user file**. Type the team's rules the way one person might keep them for themselves, plus one personal line, and save (**Ctrl+S**):

```markdown
# My notes for Claude

- Run the tests with: .venv/bin/python -m pytest -q
- Money: take refund amounts from policy.check_refund, never compute them by hand.
- Dates: read orders through harborline.normalize, never parse the raw date fields.
- Commit messages: one line that says what changed.
- Keep answers short.
```

Then ask Claude, in one shot:

```bash
clear
claude -p "Without reading any files: quote the rules you were given for working in this repository, or say there are none. Nothing else."
```

In the lesson it answered `Rules from your global notes (~/.claude/CLAUDE.md), which apply to all projects:` and quoted all five lines. It works on your machine; nobody else has that file.

### 2. A project CLAUDE.md with imports

```bash
code CLAUDE.md
```

Type the kit's `harborline/CLAUDE.md` (14 lines) and save. The two `@` lines are imports: each pulls a file into the context at launch. A relative path resolves from the file that contains the import (here, the repo root).

```bash
mkdir -p docs/conventions
code docs/conventions/money.md
code docs/conventions/dates.md
```

Type the kit's `money.md` and `dates.md` (4 lines each), saving each one.

### 3. A folder's own rules

```bash
code support/CLAUDE.md
```

Type the kit's `harborline/support/CLAUDE.md` and save. Then trim your user file to what's really yours:

```bash
code ~/.claude/CLAUDE.md
```

Delete the four team lines (lines 3 to 6 in the lesson: **Ctrl+G** `3` **Enter**, then **Ctrl+L** four times selects them, **Delete**) and save. Only `- Keep answers short.` is left (the kit's `user-level/CLAUDE.md`).

### 4. Check and share

**A teammate's view.** To play a new teammate, make a fresh clone of your repo **outside your home folder** (off camera in the lesson; do it once). Outside your home folder matters: Claude Code also reads instruction files in the folders above the one you start in, and your `~/.claude` folder is in your home folder.

```bash
git clone <your harborline repository URL> /tmp/teammate
```

Then run the teammate's check, with only project and local settings, so no user-level files load:

```bash
cd /tmp/teammate && git pull -q && claude -p --setting-sources project,local "Without reading any files: quote the rules you were given for working in this repository, or say there are none. Nothing else."
cd ~/projects/harborline
```

In the lesson: `I wasn't given any rules specific to this repository. No CLAUDE.md or other project instructions were loaded into my context.` Your user file never left your machine, and the new project files aren't committed yet.

**What loaded in your session:**

```bash
clear
claude
```

```text
/memory
```

It lists `User instructions  Saved in ~/.claude/CLAUDE.md`, `Project instructions  Checked in at ./CLAUDE.md`, and under it `docs/conventions/money.md` and `docs/conventions/dates.md`, each `@-imported`. Selecting one opens it in your editor; **Esc** closes the list.

```text
/context
```

Scroll to the top of the report: the tokens in use out of the context window, and `Memory files` (295 tokens in the lesson). Further down, the `Memory files · /memory` list shows each file with its tokens: `~/.claude/CLAUDE.md` 25, `CLAUDE.md` 140, `docs/conventions/money.md` 61, `docs/conventions/dates.md` 69. `support/CLAUDE.md` is not there: it hasn't loaded yet.

```text
Read support/agent.py and tell me in two lines what it does.
```

Under `Read 1 file`, Claude Code prints `Loaded support/CLAUDE.md`: the folder's file loaded on demand, the moment Claude touched a file in `support/`. Then the two-line answer.

```text
/exit
```

**Commit and push** (your user file is not part of the repo):

```bash
clear
git add CLAUDE.md docs support/CLAUDE.md
git commit -m "Lesson 5.2: team rules in CLAUDE.md with imports, and support/CLAUDE.md for the support agent"
git push
```

**The teammate's check again:**

```bash
clear
cd /tmp/teammate && git pull -q && claude -p --setting-sources project,local "Without reading any files: quote the rules you were given for working in this repository, or say there are none. Nothing else."
cd ~/projects/harborline
```

This time Claude quotes `CLAUDE.md`, `docs/conventions/money.md` and `docs/conventions/dates.md` word for word. `Keep answers short.` isn't there (it's yours), and neither are the support rules (they load when someone works in `support/`).

## Windows, macOS and Linux

| | Linux and macOS (the lesson) | Windows (PowerShell) |
|---|---|---|
| Your user file | `~/.claude/CLAUDE.md` | `$HOME\.claude\CLAUDE.md` (`%USERPROFILE%\.claude\CLAUDE.md`) |
| Open it in VS Code | `code ~/.claude/CLAUDE.md` | `code $HOME\.claude\CLAUDE.md` |
| Make the folder | `mkdir -p docs/conventions` | `mkdir docs\conventions` |
| The teammate's clone (outside your home folder) | `/tmp/teammate` | `C:\teammate` (not `%TEMP%`, which sits inside your user folder) |
| Run two commands in a row | `cd /tmp/teammate && git pull -q && claude -p ...` | PowerShell 7: the same with `&&`. Windows PowerShell 5.1: `cd C:\teammate; git pull -q; claude -p ...` |
| Clear the terminal | `clear` | `clear` or `cls` |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save, Cmd+J for the panel; Ctrl+G still goes to a line). `/tmp` works the same way. **WSL** follows the Linux column.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `claude -p` with the team rules in my user file | quoted from `~/.claude/CLAUDE.md` ("your global notes"), all five lines |
| The teammate's check before the commit | `I wasn't given any rules specific to this repository.` |
| `/memory` | User instructions (`~/.claude/CLAUDE.md`), Project instructions (`./CLAUDE.md`), money.md and dates.md `@-imported` |
| `/context` | 31.2k/1m tokens (3%); Memory files 295 tokens (25 + 140 + 61 + 69) |
| Reading `support/agent.py` | `Loaded support/CLAUDE.md` under `Read 1 file` |
| The commit | `[main 242274d] Lesson 5.2: …`, 4 files changed, 26 insertions(+) |
| The teammate's check after the push | `CLAUDE.md`, `money.md` and `dates.md` quoted word for word |
| API spend | $0: Claude Code on the subscription, no API calls |

See `expected-output.md` for the exact lines.

## Troubleshooting

- **You already have a `~/.claude/CLAUDE.md`**: keep it. Add the lesson's lines at the end in step 1, and remove only those lines in step 3. Every check still works; your own lines will show up in the first answer.
- **The teammate's clone still quotes your user file**: the clone is inside your home folder, so Claude Code reads `~/.claude/CLAUDE.md` as an instruction file of a folder above it. Clone to a folder outside your home folder (`/tmp/teammate` or `C:\teammate`).
- **The teammate's answer lists other instructions** (for example how Claude Code attributes commits, or an MCP server's instructions): those come from Claude Code itself or from the project's settings, not from your CLAUDE.md files. The check is about which CLAUDE.md files it quotes.
- **`/memory` doesn't show the imports**: check the `@` lines in `CLAUDE.md`: an `@path` inside backticks or a code block isn't imported, and a path with spaces needs a backslash before each space. The path is relative to `CLAUDE.md`.
- **`Loaded support/CLAUDE.md` doesn't appear**: Claude must read, write or edit a file inside `support/` (a file outside it won't trigger the load). Ask it again to read `support/agent.py`.
- **`/context` numbers differ**: they depend on your account's skills and connectors. What matters is that your files appear under `Memory files`.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **User CLAUDE.md**: `~/.claude/CLAUDE.md`: your preferences, for every project, only on your machine.
- **Project CLAUDE.md**: `./CLAUDE.md` (or `./.claude/CLAUDE.md`): the team's instructions, shared through git.
- **Subdirectory CLAUDE.md**: a folder's own rules; they load when Claude works with files in that folder.
- **`@path` import**: pulls another file into a CLAUDE.md at launch; a relative path resolves from the importing file.
- **`/memory`**: lists the instruction files for this session and opens them in your editor.

## Sources (all checked 2026-10-16)

- **Claude Code docs, How Claude remembers your project.** https://code.claude.com/docs/en/memory : the table of locations (managed policy, user, project, local) and who each is shared with; "Files in subdirectories load on demand"; how CLAUDE.md files load (the working directory and every directory above it, concatenated rather than overriding); imports ("expanded and loaded into context at launch", relative to the importing file, four hops); `/memory`; checking the list under Memory files with `/context`; the `Loaded` line for a subdirectory file; files under 200 lines; context, not enforced configuration.
- **Anthropic, *Claude Certified Architect – Foundations Exam Guide*.** Version 1.0, effective July 2026: Task Statement 3.1 (Domain 3) and Scenario 2: Code Generation with Claude Code.

Claude Code changes often. If a screen or a message doesn't match what you see, follow the official page.

## What's next

Lesson 5.3: rules and path-scoped conventions, for instructions that should load only for the files they're about.
