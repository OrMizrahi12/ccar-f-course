# Student kit: Lesson 4.4, Choosing a decomposition strategy

Claude Certified Architect – Foundations (CCAR-F) · Module 4: Multi-Agent Systems: the Research Pipeline · Lesson 4.4

This kit holds everything you need to repeat the lesson on your own computer: the file written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Chain fixed steps in code
2. Review per file, then across files
3. Map first, then adapt the plan

## What's in the kit

| File | What it is |
|---|---|
| `experiments/m4/decompose.py` | New (106 lines): two ways to split work on Harborline's old `legacy/warehouse` package. `chain` is a fixed review chain written in code: one Messages API call per file (the per-file prompt), then one call across the files with all the code and the per-file notes (the cross-file prompt); it prints the number of calls and the cost. `explore` is an open-ended task on the Agent SDK: plan unit tests for the package, most important first; the agent has only `Read`, `Grep` and `Glob`, maps the package first, says what it will do before each step and when a finding changes the plan, and ends with the plan |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The file is exactly the one written in the lesson. Typing it yourself is the best way to learn it. If you'd rather not, copy the kit's `experiments/m4` folder into your `harborline/experiments` folder.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 4.3 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv` (including `anthropic` and `claude-agent-sdk`), and `origin` pointing at your own private `harborline` on GitHub. The `legacy/warehouse` package (five short files) has been in the repository since you set it up.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 25 minutes, most of it typing. **API spend:** both runs together cost under one cent in the lesson (the chain $0.0032, the explorer $0.0048, all on Haiku 5.5).

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while the file is open.

### 1. Two modes in one file

```bash
git status --short                       # prints nothing: a clean tree after Lesson 4.3
mkdir -p experiments/m4
code experiments/m4/decompose.py         # type the file (or copy it from the kit), save
```

What the file holds, top to bottom:

- **`PACKAGE`**: the package under review, `legacy/warehouse`.
- **`ROOM = 4096`**: `max_tokens` for one reply. Haiku 5.5's reply includes its thinking, and the limit covers the thinking too: in the first practice run, with 1024, the cross-file pass came back empty because the thinking used the whole reply.
- **`FILE_PASS`**: the per-file prompt. One Python file on its own, at most three problems, one line each, starting with the line number.
- **`CROSS_PASS`**: the cross-file prompt. It gets the files and the per-file notes, and lists only problems that show across files (one function under two names, two files that disagree), without repeating the per-file notes.
- **`TASK`**: the open-ended task for the explorer: plan unit tests for `legacy/warehouse`, most important first; map the package first (files, public names, importers), look closer where it matters, say when a finding changes the plan, one line before each step, change no files, end with a plan of at most eight lines.
- **`ask()`**: one Messages API call; it adds the call's cost to a list and returns the reply's text blocks (the first block of Haiku 5.5's reply is its thinking).
- **`chain()`**: the fixed steps. Step 1, one pass per file (sorted by name); step 2, one pass across the files. It prints each note, then the number of calls and their cost.
- **`explore()`**: the Agent SDK with `tools=["Read", "Grep", "Glob"]` (it can look, not change), `permission_mode="dontAsk"`, no settings from disk, the project as its working folder, at most 25 turns and a $0.10 budget. It prints each tool call with its arguments (paths shown from the project) and each text block, then the tool calls, turns and cost.

### 2. The chain

```bash
clear; python -m experiments.m4.decompose chain 2> runs/decompose.log
```

Six calls, the same six every run: five per-file passes (`__init__.py`, `codes.py`, `compat.py`, `records.py`, `shipping.py`), then one across the files. A per-file pass sees only its file: in the lesson, the pass on `compat.py` said so itself ("I can't see `codes.py`"). The cross-file pass found what no single file shows, such as one status returned in two casings under two exported names.

### 3. The open-ended plan

```bash
clear; python -m experiments.m4.decompose explore 2> runs/decompose.log
```

Nothing in the code says which file to read or in what order. In the lesson the agent mapped the package (Glob, then Grep for the public names and the importers), read the five files and the existing `tests/test_legacy.py`, said what changed its picture, followed the leads (the data in `data/orders.json`, a duplicate time conversion in `harborline/normalize.py`), and ended with an eight-line plan, most important first: 14 tool calls, chosen during the run.

**`2> runs/decompose.log`** keeps Claude Code's connectors notice out of the output.

### 4. Commit

```bash
clear; git status --short
git add experiments
git commit -m "Lesson 4.4: a fixed review chain, file by file and then across files, and an open-ended plan that adapts"
git push
```

`git status --short` shows the new `experiments/m4/` folder. The commit has `1 file changed, 106 insertions(+)`. Your commit ID will differ from the lesson's.

## Choosing: a chain or dynamic decomposition

| The work | The shape | Why |
|---|---|---|
| Predictable, with known aspects (a review against fixed checks, a fixed sequence of transformations) | **Prompt chaining**: the steps written in code | Each call gets one easier job, every output in between can be inspected or checked by a gate, and every run makes the same calls |
| A large review | **Per-file passes, then a cross-file pass** | One pass per file gives each file full attention; a separate pass across the files, with the per-file notes as input, finds problems between files |
| Open-ended investigation (the next step depends on the last finding) | **Dynamic decomposition**: map, prioritize, adapt | The steps can't be listed in advance; the agent maps the ground, ranks what matters, and changes the plan as it learns |

An honest caveat from the lesson: `legacy/warehouse` is five short files, small enough for one call. The split pays off on a real review with dozens of files, where one pass over everything spreads its attention thin. There, the cross-file pass would get the files' interfaces and the per-file notes rather than all the code.

## Windows, macOS and Linux

`git`, `code`, `mkdir -p` (PowerShell accepts `mkdir experiments/m4`) and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m experiments.m4.decompose chain 2> runs/decompose.log` | the same line | `cls`, then `python -m experiments.m4.decompose chain 2> runs\decompose.log` on its own line |

In cmd.exe, make the folder with `mkdir experiments\m4`.

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| the chain | 5 per-file passes, then `--- across the files` with four cross-file points; `6 calls, fixed before the run · $0.0032` |
| the explorer | Glob, Grep, Read × 6, then "Two things changed the picture."; 14 steps in all; an eight-line plan; `14 tool calls, chosen during the run · 15 turns · $0.0048` |
| `git commit` | `1 file changed, 106 insertions(+)` |

In the practice runs before filming, the chain made the same six calls in every run, and the explorer took 13 or 14 tool calls and changed its plan for different reasons (no float timestamps in the data; production code doesn't call `read_record`). Your explorer run will differ too: its steps depend on what it finds.

## Troubleshooting

- **The `--- across the files` block is empty**: the reply's thinking used the whole `max_tokens`. Check `ROOM = 4096` and that `ask()` passes `max_tokens=ROOM`.
- **An error about a block with no `text`, or a note that's only part of the reply**: `ask()` must join only the text blocks (`if b.type == "text"`); the first block of the reply is the thinking.
- **The explorer stops early with `error_max_turns` or a budget error**: check `max_turns=25` and `max_budget_usd=0.10`; a run in the lesson used 15 turns and under half a cent.
- **The explorer edits a file**: it can't with `tools=["Read", "Grep", "Glob"]`. Check that `tools` and `allowed_tools` list only those three.
- **`ModuleNotFoundError: No module named 'experiments.m4'`**: run from the `harborline` folder with `python -m experiments.m4.decompose`.
- **`IndexError: list index out of range`**: add the mode after the module name: `chain` or `explore`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Prompt chaining:** a fixed sequence of calls written in code, each call working on the previous one's output.
- **Per-file pass:** one call that reviews one file on its own, for problems inside that file.
- **Cross-file pass:** a separate call that looks only at how the files work together (one function under two names, files that disagree).
- **Dynamic decomposition:** the agent decides the next subtask from what it has found so far.
- **Map, prioritize, adapt:** for an open-ended task, map the ground first, rank what matters, and say when a finding changes the plan.

## Sources (checked 2026-10-15)

- Anthropic, *Building effective agents*: prompt chaining is ideal when a task can be cleanly decomposed into fixed subtasks, "making each LLM call an easier task", with a programmatic gate between steps; orchestrator-workers suits "complex tasks where you can't predict the subtasks needed": https://www.anthropic.com/engineering/building-effective-agents
- Claude docs, *Prompting best practices*, Chain complex prompts: Claude handles most multistep reasoning internally, and explicit prompt chaining is still useful "when you need to inspect intermediate outputs or enforce a specific pipeline structure"; each step is a separate call you can log, evaluate or branch: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.6 (fixed sequential pipelines, prompt chaining, versus dynamic adaptive decomposition; per-file local passes plus a separate cross-file integration pass; mapping structure, finding high-impact areas, and a prioritized plan that adapts).

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 4.5: distributing tools across agents.
