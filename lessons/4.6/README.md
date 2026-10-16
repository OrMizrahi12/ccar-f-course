# Student kit: Lesson 4.6, Errors across agents

Claude Certified Architect – Foundations (CCAR-F) · Module 4: Multi-Agent Systems: the Research Pipeline · Lesson 4.6

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Return errors with context
2. Recover locally, report the rest
3. Say what the answer doesn't cover

## What's in the kit

| File | What it is |
|---|---|
| `research/tools.py` | Changed: `SLOW = {"fraud", "abuse"}`. A `search_web` query with either word times out on purpose (our saved web never fails by itself), and returns a structured error flagged with `is_error`: `failure_type` (`"timeout"`), `retryable` (`true`), the `query`, `partial_results` (up to two hits for the rest of the query, none on the slow topic) and `alternatives` (retry once; search the rest and report the topic as not covered). A search that works and finds nothing still returns an empty list, with no error flag |
| `research/agents.py` | Changed: the searcher's prompt (if a search fails, follow its alternatives; if it still fails, say what failed, the query and any partial results; never report a failed search as finding nothing); the synthesizer's prompt (if its prompt says part of the question isn't covered, end with a line starting "Not covered:" that says what and why) |
| `research/coordinator.py` | Changed: the docstring (a `!` marks a tool call that failed); `import json`; the system prompt (if a subagent reports a search it couldn't complete, carry on with the rest and tell the synthesizer which part isn't covered); `failure()` (a failed tool's `failure_type`, or the start of its message); `calls` (who made each tool call, and which tool); a `!` line for every result flagged as an error |
| `tests/test_research_tools.py` | Changed: `import asyncio` and two new tests, without calling Claude: a search on "return fraud" times out with its failure type, query, partial results and alternatives (a failure, not an empty success); a search for "zeppelin" finds nothing and is a valid empty result |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing the changes yourself is the best way to learn them. If you'd rather not, copy the kit's `research` and `tests` folders into your `harborline` folder (they replace `tools.py`, `agents.py`, `coordinator.py` and `tests/test_research_tools.py`).

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 4.1 to 4.5 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, the research pipeline (`research/tools.py`, `research/agents.py`, `research/coordinator.py`) and `tests/test_research_tools.py` committed, and `origin` pointing at your own private `harborline` on GitHub.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 25 minutes, most of it typing. **API spend:** the run in step 4 cost about two cents in the lesson (the coordinator and five subagents, all on Haiku 5.5). The tests in step 3 call no model and cost nothing.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, **Ctrl+G** jumps to a line, and **Ctrl+L** selects the whole line.

### 1. A timeout with context

```bash
git status --short                       # prints nothing: a clean tree after Lesson 4.5
code research/tools.py                   # change it in place, save
```

Starting from Lesson 4.5's `tools.py` (119 lines), the lesson makes these changes (the kit's file is the result, 135 lines):

1. Two docstring lines: searches on fraud or abuse time out, as a real search sometimes does; the error says what failed, what came back, and what to try instead.
2. `SLOW = {"fraud", "abuse"}`, with a comment: searches on these words time out (simulated).
3. In `search_web`: if the query contains a slow word, search the rest of the query, keep up to two hits whose titles aren't on the slow topic (what came back before it stopped), and return the error as JSON with `error=True`: `failure_type`, `retryable`, `query`, `partial_results`, `alternatives`. Every other query runs as before.

The timeout is simulated, on purpose: the saved web is local, so the tool fails for one topic. What matters is the shape of the error and what each agent does with it.

### 2. Recover, report, carry on

```bash
code research/agents.py                  # change it in place, save
code research/coordinator.py             # change it in place, save
```

In `agents.py`: the searcher's prompt gets "If a search fails, follow its alternatives. If it still fails, say so: what failed, the query, and any partial results. Never report a failed search as finding nothing."; the synthesizer's prompt gets "If your prompt says part of the question isn't covered, end with a line starting "Not covered:" that says what and why."

In `coordinator.py`: the docstring (a `!` marks a tool call that failed); `import json`; the system prompt ("If a subagent reports a search it couldn't complete, carry on with the rest and tell the synthesizer which part isn't covered, so the answer says so."); `failure(content)`, which returns a failed tool's `failure_type`, or the first 60 characters of its message when the content isn't our JSON (for example a call denied by Lesson 4.1's hook); `calls`, filled at every tool call with who made it and which tool; and, for every result flagged with `is_error`, a line with the time, `!`, who called which tool, `failed:` and the failure type.

### 3. Failure versus empty, tested

```bash
code tests/test_research_tools.py        # change it in place, save
clear; python -m pytest -q tests/test_research_tools.py
python -m pytest -q
```

The first new test proves a timeout is a failure with context, not an empty success. The second proves that a search with no matches is a valid empty result: no `is_error`, and `[]`. Together they keep one fix from creating the opposite bug, where every empty result looks like a failure.

### 4. One run

```bash
clear; python -m research.coordinator "Should Harborline charge customers a fee for return shipping, and would a fee cut return fraud?" 2> runs/research.log
```

- **`! [searcher 1] search_web failed: timeout`**: a tool call that failed, with who made it and the failure type.
- **The same query again, a moment later**: the searcher following the error's first alternative, retry once.
- **The run carries on**: the other searches, the analyst and the synthesizer still do their work.
- **The answer's gap line**: what isn't covered, and why.
- **`2> runs/research.log`** keeps Claude Code's connectors notice out of the output.

**In the lesson:** three searchers started together; "wardrobing return fraud prevention" and "serial returners return fees abuse" timed out, were each retried once, and timed out again; "harborline return fraud" timed out, was retried, and timed out again. All three searchers finished; one analyst read ten sources (Harborline's three internal documents and seven web pages, among them a loss-prevention survey on return fraud that a search without a slow word had found); the synthesizer checked seven claims. The answer: Harborline can test a fee on "changed my mind" returns, but the evidence doesn't show a fee would cut return fraud. Its gap line was headed **"Gaps:"**, not "Not covered:" (the prompt's wording isn't always followed word for word): "Searches for wardrobing and serial-returner evidence and for Harborline return-fraud documents timed out, so Harborline's own fraud rate is unknown." `subagents: searcher 1, searcher 2, searcher 3, analyst 1, synthesizer 1` · `subagents worked 90s in 72s of clock time: running together saved 18s` · `102s in all · 6 turns · $0.0219`.

### 5. Commit

```bash
clear; git status --short
git add research tests
git commit -m "Lesson 4.6: a timeout that says what failed and what came back, recovery in the searcher, and the gap in the answer"
git push
```

`git status --short` shows the four files changed. The commit has `4 files changed, 63 insertions(+), 7 deletions(-)`. Your commit ID will differ from the lesson's.

## One failure, at every level

| Level | What it does with the failure |
|---|---|
| The tool | Says what failed (`failure_type`), whether a retry may help (`retryable`), the `query`, what came back (`partial_results`) and what to try instead (`alternatives`), flagged with `is_error` |
| The searcher | Retries once, tries an alternative, and reports only what it couldn't fix, with the query and any partial results; never "found nothing" |
| The coordinator | Carries on with everything else, and tells the synthesizer which part isn't covered |
| The answer | States the gap: what's missing, and why |

Two anti-patterns to avoid: a failure returned as an empty list (the report then says nothing exists, when nobody looked), and a run that stops on the first failure (everything already found is lost).

## Windows, macOS and Linux

`git`, `code` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m ...` | the same line | `cls`, then the `python -m ...` command on its own line (and `runs\research.log` in step 4) |

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `pytest -q tests/test_research_tools.py` | `6 passed in 1.17s` |
| `pytest -q` (the whole suite) | `100 passed in 3.87s` |
| failed calls | 6 `! ... search_web failed: timeout` lines: three queries, each tried twice |
| subagents used | `searcher 1, searcher 2, searcher 3, analyst 1, synthesizer 1` |
| the gap in the answer | `**Gaps:** Searches for wardrobing and serial-returner evidence and for Harborline return-fraud documents timed out, ...` |
| the run | `subagents worked 90s in 72s of clock time: running together saved 18s` · `102s in all · 6 turns · $0.0219` |
| `git commit` | `4 files changed, 63 insertions(+), 7 deletions(-)` |

What stays missing differs from run to run. In a practice run before filming, the fraud searcher retried each failed query once and then found the loss-prevention survey with a reworded query ("wardrobing retail returns"), and the answer's line started "Not covered:"; in the filmed run, no rewording was tried and the line was headed "Gaps:".

## Troubleshooting

- **No `!` lines at all**: check `SLOW` and the `if words(query) & SLOW:` branch in `tools.py`, and that the question mentions fraud. The searchers decide their own queries; if none contains "fraud" or "abuse", nothing fails.
- **`! [coordinator] ... failed: ...` with a sentence instead of `timeout`**: a call denied by Lesson 4.1's hook. `failure()` prints the start of its message. Nothing to fix.
- **The answer says nothing exists on return fraud**: a failed search was reported as finding nothing. Check the searcher's prompt sentence "Never report a failed search as finding nothing." and the synthesizer's "Not covered:" sentence.
- **`test_a_search_with_no_matches_is_a_valid_empty_result` fails**: your `search_web` returns an error for an empty result. Only queries with a slow word should time out.
- **`json.decoder.JSONDecodeError` in the timeout test**: check `json.dumps({...}, indent=1)` in the error branch.
- **`ModuleNotFoundError: No module named 'research'`**: run from the `harborline` folder with `python -m ...`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Structured error:** failure type, the query, partial results and alternatives, so the next agent can decide.
- **Valid empty result:** the search worked and found nothing; not an error.
- **Local recovery:** the subagent retries a transient failure or tries an alternative before it reports.
- **Propagate:** pass up only what the subagent couldn't fix, with what it tried and what it got.
- **Coverage gap:** the part of the question the answer couldn't cover, stated in the answer with the reason.

## Sources (checked 2026-10-15)

- Anthropic Engineering, *How we built our multi-agent research system*, Production reliability and engineering challenges: "Agents are stateful and errors compound"; telling the agent "when a tool is failing" and letting it adapt works surprisingly well; "deterministic safeguards like retry logic and regular checkpoints": https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 5.3 (structured error context with failure type, attempted query, partial results and alternatives; access failures vs valid empty results; generic statuses hide context; silent empty success and ending the whole run are both anti-patterns; local recovery for transient failures; coverage annotations in the synthesis) and Task Statement 2.2 (the isError flag; retryable and non-retryable errors; local recovery in subagents). Scenario 3: Multi-Agent Research System.

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 4.7: provenance, and what to do when sources conflict.
