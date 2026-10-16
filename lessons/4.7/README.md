# Student kit: Lesson 4.7, Provenance and conflicting sources

Claude Certified Architect – Foundations (CCAR-F) · Module 4: Multi-Agent Systems: the Research Pipeline · Lesson 4.7

This kit holds everything you need to repeat the lesson on your own computer: the files written and changed in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Keep every claim with its source
2. Show conflicting figures side by side
3. Structure the report to be read

## What's in the kit

| File | What it is |
|---|---|
| `research/provenance.py` | New (68 lines). `SHAPE`: the JSON the synthesizer must return (an answer of two or three sentences; established claims, each with its `url` and `published` date; contested topics, each with `why` the figures differ and every figure's `value`, `url`, `published` and `method`; `not_covered`; at most six established claims and three contested topics). `parse()` takes the JSON object out of a reply, whatever surrounds it. `sources()` maps each URL to its source in Harborline's research index. `cite()` writes the publisher and the date, and adds "(no method stated)" for a source with no stated method. `render()` builds the report in a fixed order: `## Answer`, `## Established`, `## Contested` (a `Figure \| Source \| Method` table per topic), `## Not covered`. `check()` lists what breaks provenance: an unknown source, a missing date, a contested topic with only one figure |
| `research/agents.py` | Changed (54 lines): imports `SHAPE`; the synthesizer's prompt asks for the report in that shape: gaps under `not_covered` with why, every claim keeps its URL and date, disagreeing figures all under `contested` with their sources and why they differ (another measure, sample or method), figures from different years under `established` with their dates (a change over time, not a conflict), and a source with no stated method can't settle a conflict on its own |
| `research/coordinator.py` | Changed (158 lines): imports `check`, `parse` and `render`; the coordinator's prompt ends "Reply with the synthesizer's JSON report only, unchanged, with nothing before or after it."; at the end the reply is parsed and rendered, then `provenance: ok` or the problems `check()` found. A reply that isn't JSON is printed as it came |
| `tests/test_provenance.py` | New (48 lines): four tests on a hand-written report, without calling Claude |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

`research/tools.py` doesn't change in this lesson: keep the one from Lesson 4.6.

The files are exactly the ones in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `research` and `tests` files over yours.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 4.6 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, and `research/tools.py`, `research/agents.py` and `research/coordinator.py` as Lesson 4.6 left them, with `origin` pointing at your own private `harborline` on GitHub. The research index (`data/research/`) has been in the repository since you set it up.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 25 minutes, most of it typing. **API spend:** the run in step 4 cost under four cents in the lesson ($0.0363: the coordinator and eight subagents, all on Haiku 5.5). The tests in step 3 call no model.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, **Ctrl+G** jumps to a line, and **Ctrl+L** selects the whole line (press it again to add the next line).

### 1. Render and check

```bash
git status --short                       # prints nothing: a clean tree after Lesson 4.6
code research/provenance.py              # type the file (or copy it from the kit), save
```

The report travels as data. The synthesizer returns JSON in `SHAPE`; code renders it, so no model can reorder it, and code checks it, so a broken citation is listed before anyone reads the report.

### 2. The report's shape

```bash
code research/agents.py                  # change it in place, save
code research/coordinator.py             # change it in place, save
```

Starting from Lesson 4.6's files, the lesson makes these changes:

1. `agents.py`, near the top: `from research.provenance import SHAPE`.
2. `agents.py`, the synthesizer's prompt: its last lines (the "Not covered:" line, "Keep each claim with its publisher and date", "Where findings disagree, show both", at most eight lines) are replaced by the report's rules: `not_covered` with why; every claim keeps its URL and date; disagreeing figures all under `contested` with their sources and why they differ; figures from different years under `established` with their dates; a source with no stated method can't settle a conflict on its own; then `+ SHAPE`.
3. `coordinator.py`, the imports: `from research.provenance import check, parse, render`.
4. `coordinator.py`, the end of the coordinator's prompt: "Give it findings whole, as JSON. Reply with the synthesizer's JSON report only, unchanged, with nothing before or after it." (it used to ask for at most ten lines).
5. `coordinator.py`, the result: `parse(reply)`; if that raises `ValueError` (not JSON), the reply is printed as it came; otherwise the rendered report, then `provenance:` and the problems from `check()`, or `ok`.

Why both the prompt and `parse()`: in the first practice run, the coordinator wrapped the report in its own prose and a code fence. The prompt now asks for the JSON only, and `parse()` finds the object wherever it sits.

### 3. Provenance, tested

```bash
code tests/test_provenance.py            # type the file (or copy it from the kit), save
clear; python -m pytest -q tests/test_provenance.py
python -m pytest -q
```

The tests use three real sources from the index: Retail Signals Weekly's article (`S01`), Meridian's benchmark (`S02`) and a personal blog with no stated method (`S13`). The report has one established claim from the blog and one contested topic, the return rate: 24.0% of order value and 17.6% of units.

1. Both figures keep their sources and dates in the rendered table, one row each.
2. The blog has no stated method, so the report flags it: `(no method stated)`.
3. `check()` finds nothing wrong with the report; with a made-up URL and a contested topic holding one figure, it lists both.
4. `parse()` finds the report inside other text, even inside a code fence.

`4 passed`, then the whole suite: `104 passed` (the 100 tests from Lesson 4.6, plus these four).

### 4. One run

```bash
clear; python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs/research.log
```

The run's lines first (searchers, analysts, any gap round, the synthesizer's `verify_fact` checks), then the rendered report: `## Answer`, `## Established`, `## Contested` with a table per topic, `## Not covered`, and `provenance: ok`. Scroll up to read it all. **`2> runs/research.log`** keeps Claude Code's connectors notice out of the output.

### 5. Commit

```bash
clear; git status --short
git add research tests
git commit -m "Lesson 4.7: a report that keeps every claim with its source, and shows conflicting figures side by side"
git push
```

`git status --short` shows `M research/agents.py`, `M research/coordinator.py`, `?? research/provenance.py` and `?? tests/test_provenance.py`. The commit has `4 files changed, 136 insertions(+), 8 deletions(-)`. Your commit ID will differ from the lesson's.

## Established, contested, or a change over time

| The figures | Where they go | Why |
|---|---|---|
| Sources agree, or one source states a fact | **Established**, each claim with its source and date | The reader can trace every claim |
| Credible sources disagree (24.0% of order value from a survey of retail executives; 17.6% of units from merchant transaction data) | **Contested**: all the figures in a table, each with its source, date and method, plus why they differ | Picking one hides a real disagreement; averaging gives a number nobody measured |
| The same measure from different years (Meridian: 16.5% of units in 2023, 17.6% in 2025) | **Established**, with both dates | A change over time, not a conflict |
| A source with no stated method (a blog's "half of everything") | Kept, flagged "(no method stated)" | It can't settle a conflict on its own; the reader sees what it's worth |

The report puts the answer first, then the sections under headers, tables for figures and prose for the rest: readers find the key findings before anything gets lost in the middle.

## Windows, macOS and Linux

`git`, `code` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs/research.log` | the same line | `cls`, then `python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs\research.log` on its own line |

The same goes for `clear; python -m pytest -q tests/test_provenance.py` and `clear; git status --short`.

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel, **Ctrl+G** jumps to a line).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `pytest tests/test_provenance.py` | `4 passed in 0.01s` |
| `pytest` (the whole suite) | `104 passed in 2.08s` |
| the run | searchers 1–4 together, analysts 1–2, a gap round (`searcher 5`), `synthesizer 1` with its `verify_fact` checks; a report with six established claims and three contested topics; `provenance: ok`; `subagents worked 167s in 112s of clock time: running together saved 55s`; `147s in all · 9 turns · $0.0363` |
| `git commit` | `4 files changed, 136 insertions(+), 8 deletions(-)` |

In the lesson's run, the contested topics were the return rate (Meridian's 17.6% of units, Retail Signals Weekly's 24.0% of order value, and Harborline's own 19.2% by value and 13.1% by units), the effect of free returns on repeat purchase and customer value (two observational studies, neither randomized), and stated versus observed customer reactions to a fee. Meridian's 2023 rate wasn't read in that run, and the report said so under `## Not covered`; in a practice run before filming, it was read, and the report put 2023 and 2025 under established as a change over time. The blog didn't come up in the filmed run, so the "(no method stated)" flag is shown by the test in step 3. Your run will differ: Claude's searches, findings and wording vary from run to run.

## Troubleshooting

- **The report prints as plain prose, with no `provenance:` line**: the coordinator's reply wasn't JSON. Check the end of its prompt ("Reply with the synthesizer's JSON report only, ...") and that the synthesizer's prompt ends with `+ SHAPE`. The prose is printed as it came, so nothing is lost; run it again.
- **`provenance: unknown source: ...`**: a claim's URL isn't in the research index, often a URL without `https://`. That's the check doing its job: the claim can't be traced as written.
- **`provenance: contested with one figure: ...`**: the synthesizer put a single figure under contested. A conflict needs at least two figures; move it to established or find the other source.
- **`KeyError: 'established'` or `'contested'`**: the JSON is missing a section. Check `SHAPE` in `research/provenance.py` against the kit's file.
- **`ModuleNotFoundError: No module named 'research.provenance'`**: run from the `harborline` folder, and check the file is `research/provenance.py`.
- **Fewer than 104 tests pass**: run `python -m pytest -q tests/test_provenance.py` first; its four tests call no model, so a failure there points at `provenance.py`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Provenance:** where a claim comes from: the source's URL, publisher, date and method, kept with the claim through every step.
- **Contested:** figures that disagree, kept together with their sources and the reason they differ.
- **Change over time:** figures from different years; dated, not a conflict.
- **Established:** what the sources agree on, each claim with its source.
- **Provenance check:** code that lists claims with unknown sources, missing dates, or a "conflict" with only one figure.

## Sources (checked 2026-10-15)

- Anthropic, *How we built our multi-agent research system*: after the research loop, a CitationAgent processes the documents and the report "to identify specific locations for citations"; the LLM judge's rubric includes citation accuracy, "do the cited sources match the claims?": https://www.anthropic.com/engineering/multi-agent-research-system
- Claude docs, *Prompting best practices*, Long context prompting: "Structure document content and metadata with XML tags" (each document with its content and its source), and "Ground responses in quotes": https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 5.6 (claim-source mappings preserved through synthesis; conflicting statistics annotated with their sources; dates so time differences aren't read as contradictions; established versus contested sections; data as tables, news as prose) and Task Statement 5.1 (key findings first, section headers).

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 4.8: state, crash recovery and context budgets.
