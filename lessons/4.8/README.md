# Student kit: Lesson 4.8, State, crash recovery and context budgets

Claude Certified Architect – Foundations (CCAR-F) · Module 4: Multi-Agent Systems: the Research Pipeline · Lesson 4.8

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Save each agent's work as it lands
2. Resume a crashed run from its manifest
3. Pass facts, not reasoning, downstream

## What's in the kit

| File | What it is |
|---|---|
| `research/state.py` | New (49 lines): each run's state on disk. `start(question)` makes a run (its ID is the start time, `YYYYMMDD-HHMMSS`), its folder `research/runs/<run_id>/` and an empty `manifest.json`; `manifest(run_id)` reads it; `write()` saves it atomically (a temporary file, then `replace`); `save(run_id, name, prompt, report, **more)` writes one subagent's report to its own JSON file, then adds a line to the manifest (plus `more`: anything else the run needs to continue); `done(run_id)` returns every saved report in the order they finished |
| `research/agents.py` | Changed: the analyst's prompt asks for one more key per finding, `relevance` (0 to 1: how much it bears on the question), and ends with "Only what sources say; no reasoning." |
| `research/coordinator.py` | Changed: every subagent report is saved the moment it arrives, with `found` (the URLs searches returned); `--resume <run_id>` loads the manifest and the saved reports, puts the saved URLs back into `FOUND`, numbers new subagents after the saved ones, and tells the coordinator to use the saved reports and not repeat their work; `CRASH_AFTER` simulates a crash after that many saved reports; the system prompt passes the synthesizer only findings with relevance 0.5 or more |
| `tests/test_state.py` | New (30 lines): three tests of the run state, without calling Claude, each in a temporary folder: reports come back in the order they were saved; the manifest keeps what the run needs to continue; a new run starts with nothing done |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `research` and `tests` folders into your `harborline` folder (they replace `agents.py` and `coordinator.py`, and add `research/state.py` and `tests/test_state.py`).

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except a few lines, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 4.1 to 4.7 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, the research pipeline (`research/tools.py`, `agents.py`, `coordinator.py`, `provenance.py`) committed, and `origin` pointing at your own private `harborline` on GitHub.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 25 minutes, most of it typing. **API spend:** the crashed run in step 4 cost about one cent (it stops before the cost line prints) and the resumed run in step 5 just under three cents (`$0.0287`), all on Haiku 5.5. The tests in step 3 call no model and cost nothing.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, **Ctrl+G** jumps to a line, and **Ctrl+L** selects the whole line.

### 1. State on disk

```bash
git status --short                       # prints nothing: a clean tree after Lesson 4.7
code research/state.py                   # type the file (or copy it from the kit), save
```

The design, in one folder per run:

```text
research/runs/20261016-045244/
    manifest.json        {"question": ..., "reports": [{"name": "searcher 2", "file": "searcher-2.json"}, ...], "found": [...]}
    searcher-2.json      {"name": ..., "prompt": ..., "report": ...}
    searcher-1.json
    analyst-2.json
```

- **One file per report**, written the moment the subagent reports.
- **The manifest** lists the question and every saved report, in the order they finished. It is read first on resume, so it is written atomically: to `manifest.tmp`, then `replace` swaps it in. A crash leaves the old manifest or the new one, never half a file.
- **`more`** keeps anything else the run needs to continue. Here: `found`, the URLs searches returned. Since Lesson 4.5, `load_document` only loads those; if they lived only in memory, a resumed analyst would be refused.

`research/runs/` is never committed: the `runs/` line in `.gitignore` covers it.

### 2. Save, resume, crash

```bash
code research/agents.py                  # change it in place, save
code research/coordinator.py             # change it in place, save
```

In `agents.py` (line 29), the analyst's prompt: each finding keeps `claim`, `evidence`, `url`, `publisher`, `published` and `method` (copied from the source's details), and gets `relevance` (0 to 1: how much it bears on the question); "Only what sources say; no reasoning."

In `coordinator.py`, top to bottom:

1. The docstring: `python -m research.coordinator --resume <run_id>`; each subagent's report is saved as it arrives.
2. `import os`, `from research import state`, and `FOUND` from `research.tools`.
3. The system prompt: "Give it the findings with relevance 0.5 or more, whole, as JSON."
4. A helper, `text_of(content)`: a result's text, whether it came as one string or in parts. `failure()` now uses it.
5. `main(run_id)` instead of `main(question)`: `prompts` keeps each subagent's brief; the prompt starts as the manifest's question; the saved reports (`earlier`) set the counters, so new subagents are numbered after them; when there are saved reports it prints `resuming <run_id>: N reports already saved`, puts the manifest's `found` back into `FOUND`, and adds to the prompt: "This run is resuming after a crash. These subagents already reported. Use their reports, and don't repeat their work:" followed by the reports; otherwise it prints `run <run_id>`. `CRASH_AFTER` comes from the environment (0: no crash).
6. The query gets that prompt; each subagent's brief is kept under its call's ID.
7. When a subagent's result arrives: `state.save(run_id, name, brief, text, found=sorted(FOUND))`, then, if the number of saved reports equals `CRASH_AFTER`, print `simulated crash` and stop.
8. `__main__`: `--resume <run_id>` resumes that run; a question starts a new one with `state.start()`.

### 3. State, tested

```bash
code tests/test_state.py                 # type the file (or copy it from the kit), save
clear; python -m pytest -q tests/test_state.py
python -m pytest -q
```

The fixture points `state.RUNS` at pytest's temporary folder, so the tests never touch your real runs.

### 4. A crash

```bash
clear; CRASH_AFTER=3 python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs/research.log
ls research/runs/*/
clear; cat research/runs/*/manifest.json
```

- **`CRASH_AFTER=3`** stops the run right after the third saved report, the way a restart or a killed process would. The traceback goes to `runs/research.log`.
- **Work in flight is lost.** In the lesson, analyst 1 was still reading when the run stopped; it has no report file.
- **`ls`** shows the manifest and one file per saved report. **`cat`** shows the question, the reports in the order they finished, and `found`.

### 5. Resume

```bash
clear; python -m research.coordinator --resume $(ls research/runs) 2> runs/research.log
```

`$(ls research/runs)` names the run's folder, which works because there is exactly one. If you have more than one run folder, type the run ID instead (the folder's name, for example `20261016-045244`).

**In the lesson:** `resuming 20261016-045244: 3 reports already saved`; one new analyst, `analyst 3` (numbered after the saved `analyst 2`), loaded the web sources analyst 1 never finished, and `load_document` allowed them because `found` came back from the manifest; no searcher ran again; `synthesizer 1` checked 14 figures with `verify_fact`; the report ended `provenance: ok`, `subagents: analyst 3, synthesizer 1`, `149s in all · 3 turns · $0.0287`.

### 6. Commit

```bash
clear; git status --short
git add research tests
git commit -m "Lesson 4.8: each report saved to a run manifest as it arrives, and a crashed run resumed from it"
git push
```

`git status --short` shows `agents.py` and `coordinator.py` changed, `state.py` and `tests/test_state.py` new. The commit has `4 files changed, 125 insertions(+), 11 deletions(-)`. Your commit ID will differ from the lesson's.

## Compact hand-overs

| Upstream sends | Why |
|---|---|
| `claim`, `evidence` (the source's exact words) | the fact, and the words behind it |
| `url`, `publisher`, `published`, `method` | metadata: where it comes from, when, and how it was measured, so the synthesis can weigh it |
| `relevance` (0 to 1) | the coordinator passes on only findings with 0.5 or more, so the synthesizer's context holds what matters |
| no reasoning | the reasoning stays with the analyst; it would only fill the next agent's context budget |

The 0.5 filter is a sentence in the coordinator's prompt, not code: the coordinator follows it when it briefs the synthesizer.

## Windows, macOS and Linux

`git`, `code` and `python -m ...` are the same on every system (run them with the environment active). These lines differ:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m ...` | the same line | `cls`, then the `python -m ...` command on its own line (and `runs\research.log`) |
| The crash (step 4) | `CRASH_AFTER=3 python -m ...` | `$env:CRASH_AFTER=3; python -m ...`, then `Remove-Item Env:CRASH_AFTER` before step 5 | `set CRASH_AFTER=3`, the command, then `set CRASH_AFTER=` before step 5 |
| The run ID (step 5) | `--resume $(ls research/runs)` | `--resume (Get-ChildItem research/runs -Name)` | `--resume 20261016-045244` (type your folder's name) |
| `ls` / `cat` (step 4) | `ls research/runs/*/`, `cat research/runs/*/manifest.json` | `ls research/runs/*`, `cat research/runs/*/manifest.json` | `dir research\runs\<run_id>`, `type research\runs\<run_id>\manifest.json` |

- On Linux and macOS, `CRASH_AFTER=3 python ...` sets the variable for that one command only, so the resume in step 5 runs without a crash. On Windows, clear it before step 5, or the resumed run will stop after its first new report.
- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `pytest -q tests/test_state.py` | `3 passed in 0.03s` |
| `pytest -q` (the whole suite) | `107 passed in 5.43s` |
| the crash | run `20261016-045244`: searcher 2, searcher 1 and analyst 2 saved, then `62.9s simulated crash`; analyst 1 lost |
| the run folder | `analyst-2.json  manifest.json  searcher-1.json  searcher-2.json` |
| the manifest's `found` | 12 URLs: 4 of Harborline's documents, 8 web pages |
| the resume | `resuming 20261016-045244: 3 reports already saved`; new subagents only: `analyst 3, synthesizer 1` |
| the resumed run | `149s in all · 3 turns · $0.0287` |
| `git commit` | `4 files changed, 125 insertions(+), 11 deletions(-)` |

In the practice runs before filming: in the first crash, searchers 1, 2 and 4 were saved and searcher 3 was lost. That first version didn't keep `found` in the manifest, so on resume `load_document` refused the analysts (the URLs weren't returned "in this run"), and the coordinator had to send another searcher to find the same sources again. With `found` in the manifest, the second resume ran analysts and the synthesizer only, and no searcher was repeated.

## Troubleshooting

- **The resumed analysts get `... wasn't returned by search_web in this run`**: the manifest has no `found`, or the coordinator doesn't load it. Check `found=sorted(FOUND)` in the `state.save(...)` call and `FOUND.update(state.manifest(run_id)["found"])` in `main`. A manifest saved before that change has no `found`: start a new run.
- **The resume prints `run <run_id>` instead of `resuming ...`**: no report was saved before the crash, so there is nothing to resume from; the run starts its work from the beginning, in the same folder.
- **The resumed run stops after one report with `simulated crash`**: `CRASH_AFTER` is still set (Windows). Clear it and resume again.
- **`ls research/runs` names two folders**: `$(ls research/runs)` expects exactly one. Type the run ID, or move older run folders out of `research/runs/`.
- **`FileExistsError` from `start()`**: two runs started within the same second. Wait a second and run again.
- **`ModuleNotFoundError: No module named 'research'`**: run from the `harborline` folder with `python -m ...`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Manifest:** a small file listing a run's question and every saved report, read first on resume.
- **Atomic write:** write to a temporary file, then rename it, so a crash never leaves half a manifest.
- **Resume:** start again from the manifest: hand the saved reports to the coordinator and skip finished work.
- **Relevance score:** each finding's 0–1 weight for the question, so only the findings that matter go downstream.
- **Context budget:** what each agent's prompt can afford; compact, structured hand-overs keep it small.

## Sources (checked 2026-10-15)

- Anthropic Engineering, *How we built our multi-agent research system*: agents are stateful and errors compound; rather than restart from the beginning, they built systems that "resume from where the agent was when the errors occurred"; agents "store essential information in external memory" before moving on; subagents store their work in external systems, then "pass lightweight references back to the coordinator": https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 5.4 (structured state persistence for crash recovery: each agent exports its state to a known location, and the coordinator loads a manifest on resume and injects it into agent prompts) and Task Statement 5.1 (upstream agents return structured data, such as key facts, citations and relevance scores, instead of verbose content and reasoning when downstream agents have limited context budgets; subagents include metadata such as dates, source locations and methodological context). Scenario 3: Multi-Agent Research System.

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 4.9: the traps of Module 4 and a recap, before Lab 4.
