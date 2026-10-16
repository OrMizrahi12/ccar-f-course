# Student kit: Lesson 4.3, Parallel subagents, scope and refinement

Claude Certified Architect – Foundations (CCAR-F) · Module 4: Multi-Agent Systems: the Research Pipeline · Lesson 4.3

This kit holds everything you need to repeat the lesson on your own computer: the file changed in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Run independent subagents together
2. Split the work without overlap
3. Check the answer against the goal

## What's in the kit

| File | What it is |
|---|---|
| `research/coordinator.py` | Changed: the system prompt states the goal and what a good answer looks like (not a list of steps), asks for work split so no two subagents cover the same ground (by part of the goal or by source type), for independent subagents to start together in one response, and for the answer to be checked against the goal, with a subagent sent after any missing part. Built-in agents are off, so only our three subagents exist. Every printed line starts with the seconds since the run began; each subagent's start and finish are printed, and the last lines compare the subagents' working time with the clock time |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

`research/agents.py` and `research/tools.py` don't change in this lesson: keep the ones from Lesson 4.2.

The file is exactly the one written in the lesson. Typing the changes yourself is the best way to learn them. If you'd rather not, copy the kit's `research/coordinator.py` over yours.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 4.2 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, and `research/tools.py`, `research/agents.py` and `research/coordinator.py` committed, with `origin` pointing at your own private `harborline` on GitHub.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 20 minutes, most of it typing. **API spend:** the run in step 2 cost about two cents in the lesson (the coordinator and six subagents, all on Haiku 5.5).

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, **Ctrl+G** jumps to a line, and **Ctrl+L** selects the whole line (press it again to add the next line).

### 1. A goal, a split, and subagents that start together

```bash
git status --short                       # prints nothing: a clean tree after Lesson 4.2
code research/coordinator.py             # change it in place, save
```

Starting from Lesson 4.2's `coordinator.py` (115 lines), the lesson makes these changes, top to bottom (the kit's file is the result, 129 lines):

1. The docstring: the coordinator gets a goal and what a good answer looks like, splits the work, starts independent subagents together, checks the answer against the goal; each printed line starts with the seconds since the run began.
2. `import json` out; `import textwrap` becomes `import time`.
3. The SDK import: `SystemMessage` out, `UserMessage` in. A subagent's report comes back to the coordinator inside a `UserMessage`, as a tool result.
4. The system prompt: the setting (a saved copy of the web, Harborline's own documents under `harborline://internal/`, the three subagents); the **goal** (an answer Harborline's managers can act on) and the **criteria** (it covers the cost of returns, how customers react to a fee, what competitors do and Harborline's own data; every claim keeps its source; it shows where sources disagree); the **split** (no two subagents cover the same ground, by part of the goal or by source type; subagents that don't depend on each other start together, in one response); the **check** (compare the synthesizer's answer with the goal; send a subagent after a missing part only; have the synthesizer write again with all the findings).
5. `env`: `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS` set to `"1"`, so the coordinator has only our three subagents (in a practice run, it used the SDK's built-in Explore agent instead of our searcher).
6. `findings()` and `show()` (18 lines) are replaced by `covered(spans)`: the seconds when at least one subagent was running, each second counted once.
7. In `main()`: `names`, `started`, `counts`, `spans` and `start = time.monotonic()`; the init print goes; every message gets `now`, the seconds since the run began.
8. Each `Agent` call: counted per kind (`searcher 1`, `searcher 2`, ...), its start time noted, and one line printed: the time, `->`, its name and the first 60 characters of its prompt.
9. Any other tool call: the time, who made it, the tool and its inputs. A call from outside every subagent is the coordinator's own, denied by the Lesson 4.1 hook, and labeled `coordinator, denied`.
10. A new branch for `UserMessage`: when a tool result matches a started subagent, save its span and print the time, `<-`, its name, `done` and how long it took.
11. At the end: the answer, the subagents, `subagents worked ...s in ...s of clock time: running together saved ...s`, then the total time, the turns and the cost.

Nothing in the code starts subagents at the same time. The coordinator does that when it puts several `Agent` calls in one response; the SDK runs them concurrently and waits for all of their reports.

### 2. One run, timed

```bash
clear; python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs/research.log
```

- **`6.9s -> searcher 1: ...`**: each subagent's start, with the seconds since the run began. Starts within a second or two of each other came from one response.
- **`[searcher 2] search_web ...`**: lines from different subagents interleave while they work at the same time.
- **`15.7s <- searcher 2 done (8.1s)`**: a subagent's report is back, with how long it worked.
- **The last lines**: `subagents worked` is the sum of every subagent's own time (what running them one after another would take); `of clock time` is the time when at least one was running. The difference is what running together saved in this run. It's a measurement of one run, not a benchmark.
- **`2> runs/research.log`** keeps Claude Code's connectors notice out of the output.

**In the lesson:** three searchers started together, split by part of the goal (how shoppers react to a fee, what returns cost, competitors' return policies); then two analysts together, split by source type (the web pages, and Harborline's own documents); then the synthesizer. `subagents worked 98s in 57s of clock time: running together saved 41s` · `84s in all · 7 turns · $0.0195`. No gap round in this run: the coordinator answered right after the synthesizer. In practice runs before filming, running together saved 12 to 37 seconds, and in some of them the coordinator sent an extra searcher after a missing part (Harborline's own documents, or competitors) before the synthesizer wrote.

### 3. Commit

```bash
clear; git status --short
git add research
git commit -m "Lesson 4.3: subagents split by scope and run together, and the answer checked against the goal"
git push
```

`git status --short` shows `coordinator.py` changed. The commit has `1 file changed, 61 insertions(+), 47 deletions(-)`. Your commit ID will differ from the lesson's.

## Steps or a goal: the coordinator's prompt

| The prompt says | What the coordinator can do |
|---|---|
| Fixed steps: search, then read, then write | Follow them, even when a question needs more subagents, a different split, or one more round |
| The goal and what a good answer covers | Decide how many subagents to start, split the work so nothing overlaps, start independent ones together, and check the answer for gaps before it's final |

A split that's too narrow fails quietly: every finding can be accurate and well sourced, and the answer still covers only part of the question. The criteria in the prompt are what the coordinator checks the answer against.

## Windows, macOS and Linux

`git`, `code` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m research.coordinator "..." 2> runs/research.log` | the same line | `cls`, then `python -m research.coordinator "..." 2> runs\research.log` on its own line |

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| the starts | `6.9s -> searcher 1`, `7.6s -> searcher 2`, `8.4s -> searcher 3`; `20.9s -> analyst 1`, `22.2s -> analyst 2` |
| the split | searchers by part of the goal; analysts by source type (web pages / `harborline://internal/`) |
| subagents used | `searcher 1, searcher 2, searcher 3, analyst 1, analyst 2, synthesizer 1` |
| the gain | `subagents worked 98s in 57s of clock time: running together saved 41s` |
| the run | `84s in all · 7 turns · $0.0195` |
| `git commit` | `1 file changed, 61 insertions(+), 47 deletions(-)` |

## Troubleshooting

- **Each subagent starts only after the previous one is done**: the coordinator put one `Agent` call in each response. Check the sentence "Subagents that don't depend on each other start together, in one response." The analysts depend on the searchers' URLs, so they start after them; that's expected.
- **`-> Explore ...` or a subagent name you didn't define**: check `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS` in `env`.
- **`[coordinator, denied]` lines**: the coordinator tried to search or read by itself, and the Lesson 4.1 hook denied it. It then delegates; nothing to fix.
- **`running together saved 0s`**: no two subagents overlapped in that run. Run it again, or check the prompt's sentence about starting together.
- **`ImportError: cannot import name 'UserMessage'`**: check the SDK import (Lesson 4.2's environment has it).
- **`ModuleNotFoundError: No module named 'research'`**: run from the `harborline` folder with `python -m research.coordinator`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Parallel subagents:** several Agent calls in one response; they run at the same time, and the coordinator waits for all of them.
- **Scope partition:** giving each subagent a distinct part of the question or a distinct source type, so no two cover the same ground.
- **Too-narrow decomposition:** subtasks that together cover only part of a broad question; every finding can be right and the answer still incomplete.
- **Refinement loop:** check the synthesis against the goal, re-delegate only the gaps, synthesize again.
- **Goal and criteria:** a prompt that says what the answer must achieve and how it will be judged, instead of fixed steps.

## Sources (checked 2026-10-15)

- Agent SDK docs, *Subagents in the SDK*: Parallelization, multiple subagents can run concurrently, so independent subtasks "finish in the time of the slowest one" rather than the sum; "Claude decides on its own when to spawn" a subagent and how many; the limits table (depth 3 layers by default; concurrency 20 "subagents running at once", `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`): https://code.claude.com/docs/en/agent-sdk/subagents
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.2 (overly narrow decomposition; partitioning research scope by subtopic or source type; iterative refinement loops) and Task Statement 1.3 (parallel subagents with multiple Task tool calls in one coordinator response; coordinator prompts with research goals and quality criteria). Scenario 3: Multi-Agent Research System.

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 4.4: fixed chains of steps, and decompositions that adapt as they go.
