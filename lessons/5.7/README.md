# Student kit: Lesson 5.7, Exploring a large codebase

Claude Certified Architect – Foundations (CCAR-F) · Module 5: Configuring Claude Code for a Team · Lesson 5.7

This kit holds everything you need to repeat the lesson on your own computer: the notes file the lesson ends with, every command and prompt in order, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Spot context degradation
2. Split exploration across subagents
3. Carry findings through a scratchpad, phase by phase

## What's in the kit

| File | What it is |
|---|---|
| `harborline/notes/exploration.md` | The scratchpad as it was committed in the lesson: the refund path through `support/`, `mcp_server/` and `loop/`, the shared core, a convention check, and seven open questions, with phase 2's answer under question 1. Claude wrote it; yours will differ |
| `commands.txt` | Every command and prompt in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |

The video is filmed on Ubuntu 24.04 in the VS Code terminal. The prompts and the Claude Code commands are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 5.6 done**: your own `harborline` repository in `~/projects/harborline` at the Lesson 5.6 commit, its `.venv`, and `origin` pointing at your own private `harborline` repository.
- **Claude Code** (Lesson 0.5), signed in, with the `harborline` folder trusted. A recent version: the lesson uses the built-in **Explore** subagent and background agents.
- About 15 minutes. **No API calls: Claude Code runs on your Claude sign-in.** The subagents count toward your Claude Code usage like any other work.

## The habits, in one place

- **Know the signs of context degradation.** Answers turn generic ("typically", "usually") instead of naming the files and functions found; earlier findings are forgotten or read again; new answers contradict old ones. A better prompt won't fix it: the context is the problem.
- **Send the reading to subagents.** Explore is a built-in, read-only subagent. It searches and reads in its own context, and only its summary comes back to your conversation. For a big question, send one per area, in parallel.
- **Keep a scratchpad file.** A plain notes file in the repo, written by Claude: paths with line numbers, function names, open questions. Specific notes keep their value after the context is gone.
- **Compact on purpose.** `/compact <focus>` replaces the conversation with a summary that keeps what you name. `/clear` drops everything, for a new, unrelated task.
- **Work in phases.** End each phase with a short summary in the file, and start the next phase from the file, with subagents aimed at the open questions.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### 1. Phase 1: three Explore subagents

```bash
git status --short
claude
```

`git status --short` prints nothing: the tree is clean. In Claude Code, send the phase 1 prompt (from `commands.txt`): one question, one Explore subagent each for `support/`, `mcp_server/` and `loop/`, wait for all three, then write the files, the functions on the path and the open questions to `notes/exploration.md`, under 40 lines.

Three background agents launch. The panel under the prompt lists them as Explore agents, each with its own token count (tens of thousands of tokens each in the lesson). That reading stays in their contexts; the main session waits, then writes the notes file.

### 2. The scratchpad

Read the answer: in the lesson, refunds reach the backend through two paths (the support agent after its hooks and gates, and the MCP server's tool), and the open questions start with a per-call limit gap (the $500 hook checks each call, but only the backend checks the running total). Treat them as findings to check, not verified bugs.

Scroll up to the `Write(notes/exploration.md)` line. In the lesson the summary said the file was over the 40-line limit, while the Write line said **39 lines**. When a summary and the tool's own record disagree, trust the record.

### 3. Compact, with a focus

```text
/compact Keep the phase 1 summary; the details are in notes/exploration.md
```

The conversation is compacted. In the lesson, the notes file was then read back in, along with the two convention files that the project's `CLAUDE.md` imports.

### 4. Phase 2, from the file

Send the phase 2 prompt (from `commands.txt`): read the notes file first, send one Explore subagent at its first open question, wait, and add the answer under that question.

In the lesson, one Explore agent ("Answer open question 1 (per-call refund limit)") reported after 27 seconds, and Claude added one line to the file. The answer: the second $400 refund is blocked by the backend's running-total check (`harborline/backend.py:126`), but $450 then $199 on the same $649 order passes every check, and no test covers a split above $500. Claude separated what it read itself from what the subagent reported, and said it ran no tests. Then:

```text
/exit
```

### 5. The notes file, then share it

```bash
clear
code notes/exploration.md
```

Read the file: each path step by step, with file, line and function. Then, back in the terminal (**Ctrl+`**):

```bash
clear
git add notes/exploration.md
git commit -m "Lesson 5.7: notes/exploration.md, the refund path mapped in two phases"
git push
```

The commit has 1 file and 40 insertions in the lesson. The findings are in the repo now, for the next session or the next teammate.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| The prompts and `/compact` | as in `commands.txt` | the same; Claude Code accepts `/` paths on Windows too |
| Open the notes file | `code notes/exploration.md` | `code notes\exploration.md` (or the same `/` path) |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal).

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` at the start | nothing: the tree is clean |
| Phase 1 | 3 background Explore agents (support/, mcp_server/, loop/), finished after 21, 24 and 25 seconds; `Wrote 39 lines to notes/exploration.md`; two paths; three open questions in the answer |
| `/compact` with a focus | `Compacted`; the notes file read back in, plus `docs/conventions/dates.md` and `money.md` |
| Phase 2 | 1 Explore agent, finished after 27 seconds; `Update(notes/exploration.md)`, 1 line added under question 1 |
| The commit | 1 file changed, 40 insertions |
| API spend | $0: Claude Code on the subscription, no API calls |

See `expected-output.md` for the exact lines.

## Troubleshooting

- **Claude reads the folders itself instead of sending subagents**: say it plainly in the prompt ("Send one Explore subagent each to …") and ask it to wait for all of them. A turn that ends while background agents still run ends before the notes are written.
- **The answer is different from the lesson's**: it will be. Claude's findings and wording change from run to run; the refund path and the per-call limit question come from the course code, so you should see something close.
- **The notes file is long or vague**: ask for specifics (paths with line numbers, function names, open questions) and a line limit, and check the Write line for the real length.
- **`/compact` doesn't read the notes file back**: that's fine; the phase 2 prompt tells Claude to read it first.
- **`git status` shows other files**: something else changed since Lesson 5.6. Commit only `notes/exploration.md`, as in the lesson.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Context degradation:** answers grow generic and earlier findings slip as the context fills.
- **Scratchpad file:** a notes file Claude writes findings to and reads back later.
- **Phase summary:** a short, specific write-up that ends one phase and seeds the next.
- **Explore subagent:** a built-in, read-only subagent that searches and reads in its own context and returns a summary.
- **`/compact <focus>`:** replaces the conversation with a summary that keeps what you name.

Claude Code changes often. If a command, a menu or a message doesn't match what you see, follow the official pages: Best practices for Claude Code (https://code.claude.com/docs/en/best-practices) and Create custom subagents (https://code.claude.com/docs/en/sub-agents).
