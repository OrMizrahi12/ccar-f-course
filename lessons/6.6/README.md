# Student kit: Lesson 6.6, Test generation that adds value

Claude Certified Architect – Foundations (CCAR-F) · Module 6: Claude Code in CI/CD · Lesson 6.6

This kit holds everything you need to repeat the lesson on your own computer: every command in order, the files the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Put testing standards where CI reads them
2. Give existing tests so new ones add coverage
3. Learn from dismissed findings by pattern

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/CLAUDE.md` | The project instructions as the lesson ends them: the new `## Testing` section (5 lines) below `## Conventions` |
| `harborline/ci/testgen.py` | The test generator (56 lines): existing tests in the prompt, a `why_new` per test, the never-overwrite guard, then pytest |
| `harborline/tests/test_normalize_generated.py` | The five tests generated in the lesson (yours will differ) |
| `harborline/ci/findings.schema.json` | The findings schema with `detected_pattern` added to the properties and to `required` |
| `harborline/ci/review.py` | Lesson 6.5's reviewer with three changes: `log()`, the call in `local()`, and the `detected_pattern` prompt line |
| `harborline/ci/review_log.py` | The review log tool (38 lines): list, `dismiss <n>...`, `report` |

You type the new files yourself, as in the lesson, or copy them from the kit. The generated tests are there to compare with yours; generate your own.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The code and the steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 6.5 done**: your own `harborline` repository in `~/projects/harborline` at the Lesson 6.5 commit, with `ci/review.py --local` (a pass per file, a cross-file pass and the independent check from Lesson 6.5), `ci/findings.schema.json`, `ci/review_config.json` and `ci/prompts/review.md`, its `.venv` with pytest, Claude Code installed (the `claude` command), and `origin` pointing at your own private `harborline` repository.
- **The three teammate branches**: `late-refunds` (Lesson 6.1), `refund-totals` (Lesson 6.3) and `weekly-fees` (Lesson 6.5), pushed to your `origin`. If one is missing, make it from that lesson's kit.
- **Your Anthropic API key in `.env`** (Lesson 0.4): `ANTHROPIC_API_KEY=...`. `.env` is in `.gitignore`, so it is never committed.
- About 30 minutes. **This lesson makes API calls**: `ci/testgen.py` and each local review run `claude -p` on your API key. In the lesson, the generation cost $0.0070 and the three reviews $0.0094, $0.0044 and $0.0143 (about four cents in all).

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### The starting point

```bash
git status --short
grep -l normalize tests/*.py
```

The tree is clean. The lesson's target is `harborline/normalize.py`, and one test file mentions it: `tests/test_partner_dates.py`. Those are the existing tests the generator will hand to Claude.

### 1. Standards and a generator

```bash
code CLAUDE.md
```

Below `## Conventions`, add a `## Testing` section: where each module's tests go, how to name a test (one behavior, the exact expected value), how to build fixtures (small dicts inside the test, never the data files), what's worth a test and what isn't. Keep it short: Claude reads `CLAUDE.md` on every run, CI runs included. A path-scoped rule would load only when Claude touches a matching file, and a personal file never reaches the CI machine.

```bash
code ci/testgen.py
```

Type the generator (the kit's `ci/testgen.py`). The parts that matter:

- **`SCHEMA`**: the imports and a list of tests, each with a `name`, the `code` and a `why_new`, the field that makes every test justify itself.
- **`PROMPT`**: follow the Testing section of `CLAUDE.md`; the existing tests are below; don't test what they already test, and say in `why_new` which behavior none of them covers; at most five.
- **`existing_tests()`**: every test file that mentions the module, pasted in under its path.
- **`main()`**: the guard first (if the generated file already exists, stop: review it and commit or remove it). Then `claude -p` with the prompt, JSON output, the schema and read-only tools (`Read,Grep,Glob`); `check=True`, so a failed call raises and CI sees it. It prints each test's `why_new`, writes the file, prints the count and the cost, and runs pytest on the new file.

### 2. Five new tests

```bash
set -a; source .env; set +a
python ci/testgen.py harborline/normalize.py
code tests/test_normalize_generated.py
python -m pytest -q
```

In the lesson: five tests, each with a reason the existing tests don't cover (Unix seconds as an int, a float with a fraction, an ISO date with a -04:00 offset, a numeric status code, the caller's dict left unchanged), $0.0070, and `5 passed`. Then the whole suite: `139 passed`. Read each `why_new` against `tests/test_partner_dates.py` before you commit: it is a claim you can check.

### 3. What developers dismiss

```bash
code ci/findings.schema.json
code ci/review.py
code ci/review_log.py
```

- **The schema**: add `"detected_pattern": {"type": "string"},` to the finding's properties, and `"detected_pattern"` to its `required` list.
- **`ci/review.py`**, from the bottom of the file up: `log(result["findings"])` in `local()`, right after the review; a `log()` function that appends each finding as one JSON line to `runs/review_log.jsonl`; and one prompt line: name the kind of problem in `detected_pattern`, in a few words joined by hyphens, such as `refund-by-hand`.
- **`ci/review_log.py`** (the kit's file): with no arguments it lists the logged findings, numbered; `dismiss 3 5` marks findings as dismissed; `report` counts each pattern's findings and its dismissed ones, most common first.

Then three real reviews, each one logged:

```bash
set -a; source .env; set +a
python ci/review.py --local main...<your late-refunds commit>
python ci/review.py --local main...origin/refund-totals
python ci/review.py --local main...origin/weekly-fees
python ci/review_log.py
```

In the lesson: two findings, one, and two; five in the log, each with its pattern. Two of them (`raw-date-parse` and `raw-order-dates-read`) are the same kind of problem under two names: free text drifts. For counts that hold over weeks, list the team's pattern names in the prompt and show them in examples, as in Lesson 6.4.

### As the developer: dismiss, then the report

```bash
python ci/review_log.py dismiss 4
python ci/review_log.py
python ci/review_log.py report
```

In the lesson, finding 4 (`harborline/fees.py:9`, raw orders handed to `check_refund`) is the one rejected: the repo's own `scripts/late_deliveries.py` does the same, `policy.as_date` parses both stored date formats, and at 0.70 it was below the 0.8 `inline_confidence`, so in CI it would have gone to a person. Your list may be numbered differently: dismiss the finding you judge wrong. In CI, a dismissal would come from the pull request (a comment resolved as won't fix); here the log stays on your machine.

### Commit and push

```bash
git status --short
git add CLAUDE.md ci tests/test_normalize_generated.py
git commit -m "Lesson 6.6: test generation with existing tests as context, and detected_pattern for dismissals"
git push
```

Six files changed, 137 insertions, 1 deletion. The review log itself stays local: `runs/` is in `.gitignore`.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Load the key from `.env` | `set -a; source .env; set +a` | PowerShell: `Get-Content .env \| ForEach-Object { $k, $v = $_ -split '=', 2; Set-Item "env:$k" $v }` |
| Find the test files that mention a module | `grep -l normalize tests/*.py` | PowerShell: `Select-String -List -Path tests\*.py -Pattern normalize \| ForEach-Object Path` |
| Find the first late-refunds commit | `git log --oneline --reverse main..origin/late-refunds \| head -1` | PowerShell: `git log --oneline --reverse main..origin/late-refunds \| Select-Object -First 1` |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

`ci/testgen.py` and `ci/review_log.py` use only the Python standard library and run the same everywhere. **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save).

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `grep -l normalize tests/*.py` | `tests/test_partner_dates.py` |
| `python ci/testgen.py harborline/normalize.py` | 5 tests, each with a `why_new`; $0.0070; `5 passed in 0.01s` |
| `python -m pytest -q` | `139 passed in 2.42s` |
| Review of the late-refunds commit | 2 findings (17 high convention, 7 medium convention); 9 turns, $0.0094 |
| Review of `refund-totals` | 1 finding (17 high convention, confirmed 0.93); 5 turns, $0.0044 |
| Review of `weekly-fees` | 2 findings (fees.py:9 medium convention, confirmed 0.70; weekly_fees.py:12 high bug, found by the cross-file pass); 19 turns, $0.0143 |
| `python ci/review_log.py report` after `dismiss 4` | `raw-order-dates-read` 1 of 1 dismissed; every other pattern 0 of 1 |
| The commit | `f47c25d`, 6 files changed, 137 insertions, 1 deletion |

See `expected-output.md` for the exact lines. Model output changes from run to run: compare the shape, not the wording.

## Troubleshooting

- **`claude: command not found`**: Claude Code isn't installed or isn't on your `PATH` (Lesson 0.3). `claude --version` must work in this terminal.
- **An authentication error, or `Invalid API key`**: the key isn't exported in this terminal. Run `set -a; source .env; set +a` again, and check `ANTHROPIC_API_KEY` in `.env` (Lesson 0.4).
- **`subprocess.CalledProcessError` from `ci/testgen.py`**: the `claude -p` call failed, and `check=True` raised on purpose. Run the same `claude -p "hello"` by hand to see the error (often the key, or an old Claude Code without `--json-schema`).
- **`tests/test_normalize_generated.py exists: review it and commit or remove it first`**: that's the guard. Review the file; commit it, or remove it if you don't want those tests, then run again.
- **A generated test fails**: read it before you fix anything. A test can be wrong, or it can have found a real bug; either way, don't commit a failing test. Remove the file and generate again, or fix the test by hand.
- **A `why_new` claims something an existing test already covers**: that's what the field is for. Delete that test before you commit.
- **`KeyError: 'detected_pattern'` in `ci/review_log.py`**: the log has findings from before the schema change. Remove `runs/review_log.jsonl` and run the reviews again.
- **`fatal: ambiguous argument`**: the commit hash or the branch isn't known here. Run `git fetch`, then find the hash again; `refund-totals` and `weekly-fees` must be pushed (Lessons 6.3 and 6.5).
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Testing standards:** the team's rules for tests, in the project's `CLAUDE.md`.
- **Fixture:** the small data a test builds for itself.
- **Existing-test context:** the module's current tests in the prompt, so new ones cover something else.
- **detected_pattern:** a short name for the kind of problem a finding reports.
- **Dismissal rate:** the share of a pattern's findings that developers rejected.

Claude Code changes often. If an option or a message doesn't match what you see, follow the official pages: Claude Code GitHub Actions (https://code.claude.com/docs/en/github-actions), Run Claude Code programmatically (https://code.claude.com/docs/en/headless) and Manage Claude's memory (https://code.claude.com/docs/en/memory).
