# Student kit: Lesson 3.8, Sessions: resume, fork, or start fresh

Claude Certified Architect – Foundations (CCAR-F) · Module 3: Agents with the Claude Agent SDK: the Support Resolution Agent · Lesson 3.8

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Resume a named session
2. Fork to compare two approaches
3. Choose resume or a fresh start

## What's in the kit

| File | What it is |
|---|---|
| `support/sessions.py` | New: a small code reviewer built with the Agent SDK (Read, Grep and Glob only; Haiku 5.5; answers in at most five lines) with three commands: `new <name> "<prompt>"`, `resume <name> "<prompt>"` and `fork <name> <branch> "<prompt>"`. `runs/sessions.json` keeps a name for each session ID. Each run prints the tools it used, the reply, and the session's name and ID |
| `support/hooks.py` | Changed: line 20, `refund_limit` reads the amount with `float()`, so an amount sent as text is compared as a number |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `support` folder into your `harborline` folder (it replaces `hooks.py`; the other files stay). To see step 4 as the lesson shows it, make the `hooks.py` change after steps 1 to 3.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 3.7 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, the support agent with its hooks and case facts committed, and `origin` pointing at your own private `harborline` on GitHub.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 20 minutes, most of it typing. **API spend:** each run is one short reviewer call on Haiku 5.5, about a tenth of a cent; the whole lesson is about one cent.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, **Ctrl+G** jumps to a line, and **Ctrl+L** selects the whole line.

### 1. A named session

```bash
git status --short                       # prints nothing: a clean tree after Lesson 3.7
code support/sessions.py                 # type the file (or copy it from the kit), save
clear; python -m support.sessions new review "Read support/hooks.py. One line per hook: when it runs, and what it does." 2> runs/sessions.log
```

- **`NAMES`** is `runs/sessions.json`: one short name for each session ID (session IDs are long). `runs/` is git-ignored.
- **`REVIEW`**: the reviewer's options: a short system prompt, Haiku (`MODEL`), the built-in tools `Read`, `Grep` and `Glob` (`tools=` makes them available, `allowed_tools=` lets them run without asking), no settings files, at most 10 turns, a budget of $0.10.
- **`ask(prompt, **session)`** runs the reviewer once. `session` holds the extra options: nothing for a new session, `resume=<ID>` to continue one, `resume=<ID>, fork_session=True` to branch one. `dataclasses.replace` copies `REVIEW` with them added. It returns the session ID from the `ResultMessage`, the tools used (with the file name) and the last text.
- **`main(command, name, *words)`**: `new` runs the prompt alone; `resume` passes the ID saved under the name; `fork` passes the same ID with `fork_session=True` and saves the new ID under the branch's name. Then it saves the names and prints the tools, the reply and `session <name>: <ID>`.
- **`2> runs/sessions.log`** keeps Claude Code's connectors notice out of the output.

**In the lesson:** `tools: Read hooks.py`, one line for each of the three hooks, and `session review: 551546b1-...`.

### 2. Resume

```bash
clear; python -m support.sessions resume review "Which of these hooks protects money, and how?" 2> runs/sessions.log
```

A new process, the same session. **In the lesson:** `tools: -` (no file read again: the answer came from the session), `refund_limit`, two gaps (a missing amount counts as 0; an amount sent as text breaks the comparison), and the same ID.

### 3. Fork

```bash
clear; python -m support.sessions fork review tests-direct "Plan three unit tests that call these hooks directly, without the agent. One line each." 2> runs/sessions.log
clear; python -m support.sessions fork review tests-agent "Plan three checks that run the whole agent instead. One line each." 2> runs/sessions.log
clear; python -m support.sessions resume review "Have we planned any tests in this conversation?" 2> runs/sessions.log
cat runs/sessions.json
```

Two approaches to testing the hooks, each in its own fork of the same review. **In the lesson:** `tools: -` on all three runs; two new IDs (`tests-direct`, `tests-agent`); the original answered "No. We haven't planned or written any tests in this conversation", because forks don't change it; three names in `runs/sessions.json`.

### 4. Tell it what changed

```bash
code support/hooks.py                    # line 20, save
clear; python -m support.sessions resume review "I changed one line in support/hooks.py: refund_limit now reads the amount with float(). Re-read only that function. Does a text amount like 600 still get past it?" 2> runs/sessions.log
```

Line 20 of `support/hooks.py` becomes:

```python
    amount = float(input_data["tool_input"].get("amount", 0))
```

The review's copy of `hooks.py` is now stale, so the prompt names the change and asks for one re-read. **In the lesson:** `tools: Read hooks.py`, once; the text amount is now denied (the reply starts with "Yes" but means the opposite); and it names what's left: text that isn't a number makes `float()` raise, and a missing amount still counts as 0.

### 5. Commit

```bash
clear; git status --short
git add support
git commit -m "Lesson 3.8: named sessions to resume and fork, and a refund amount read as a number"
git push
```

`git status --short` shows `hooks.py` changed and `sessions.py` new. The commit has `2 files changed, 79 insertions(+), 1 deletion(-)`. Your commit ID will differ from the lesson's.

## Resume, fork, or start fresh

| Situation | What to do |
|---|---|
| Continue yesterday's work, nothing changed | Resume the session (SDK `resume=<ID>`; Claude Code `claude --resume <name>`) |
| A few files changed since | Resume, and say exactly which files or functions changed, so it re-reads only those |
| Most of what it read is out of date | Start a new session with a short, structured summary of the conclusions to keep and what to re-check |
| Two approaches to compare | Fork the session once per approach (SDK `fork_session=True`; Claude Code `--fork-session` or `/branch`) |

In Claude Code you name a session with `claude -n <name>` (or `/rename` inside it) and come back with `claude --resume <name>`; `claude --continue` reopens the most recent session in the folder. Sessions are saved on the machine that ran them (under `~/.claude/projects/`); a fork copies the conversation, not your files.

## Windows, macOS and Linux

`git`, `code`, `cat` and `python -m ...` are the same on every system (run them with the environment active; on Windows cmd.exe use `type runs\sessions.json` instead of `cat`). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m support.sessions resume review "..." 2> runs/sessions.log` | the same line | `cls`, then `python -m support.sessions resume review "..." 2> runs\sessions.log` on its own line |

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `new review` | `tools: Read hooks.py`, three hooks, `session review: 551546b1-...` |
| `resume review` | `tools: -`, the same ID |
| two forks | `tools: -`, two new IDs; the original unchanged |
| after the change, `resume review` | `tools: Read hooks.py` (one file), the same ID |
| `git commit` | `2 files changed, 79 insertions(+), 1 deletion(-)` |

In two practice runs before filming, the flow had the same shape: one `Read` on `new`, no tools on resume and on the forks, one `Read` after the change.

## Troubleshooting

- **`KeyError: 'review'`**: you resumed or forked a name that isn't in `runs/sessions.json` yet. Run `new review ...` first, from the same folder.
- **`No conversation found with session ID`** (in `runs/sessions.log`): the session was created on another machine or in a container that's gone. Sessions are stored on the machine that ran them.
- **`tools:` shows a Read on resume**: the reviewer chose to check the file again. That's allowed; the point is that it doesn't have to.
- **`ModuleNotFoundError: No module named 'support'`**: run from the `harborline` folder with `python -m support.sessions`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Session:** the whole conversation (prompts, tool calls, results, replies), saved on disk under an ID.
- **Resume:** continue a saved session, with everything it already read and decided.
- **Fork:** a new session that starts from a copy of another's history; the original stays as it was.
- **Stale tool results:** results in the history that describe files or data as they were, not as they are.
- **Fresh start with a summary:** a new session that gets a short, structured summary instead of the old history.

## Sources (checked 2026-10-15)

- Claude Code docs, *CLI reference*: `--resume`, "Resume a specific session by ID or name"; `--fork-session`, "When resuming, create a new session ID instead of reusing the original"; `--name` / `-n`: https://code.claude.com/docs/en/cli-reference
- Claude Code docs, *Manage sessions* (naming, resuming by name, branching): https://code.claude.com/docs/en/sessions
- Agent SDK docs, *Work with sessions*: `resume`, `fork_session` ("starts with a copy of the original's history"; "Forking branches the conversation history, not the filesystem"); passing captured results into a fresh session's prompt is "often more robust": https://code.claude.com/docs/en/agent-sdk/sessions
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.7 (named session resumption; `fork_session` for divergent approaches; informing a resumed session about changed files; a new session with a structured summary when tool results are stale). Scenario 4: Developer Productivity with Claude.

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 3.9: the exam traps of Module 3, and a recap of the whole module.
