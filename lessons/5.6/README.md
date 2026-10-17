# Student kit: Lesson 5.6, Iterative refinement

Claude Certified Architect – Foundations (CCAR-F) · Module 5: Configuring Claude Code for a Team · Lesson 5.6

This kit holds everything you need to repeat the lesson on your own computer: every prompt and command in order, the two files the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Let Claude interview you first
2. Pin the change with examples and tests
3. Iterate on failures, bundled or one by one

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command and prompt in the lesson, in order (copy the prompts from here) |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/tests/test_partner_dates.py` | The tests as committed at the end of the lesson: 7 tests, written before the code (the midnight one added in step 4) |
| `harborline/harborline/normalize.py` | `normalize.py` as committed at the end of the lesson: `PARTNER_SHAPE`, `PARTNER_ZONE` and `partner_to_utc`, called from `to_utc` |

Use the two code files to compare with yours, or to recover if your run went somewhere else. Claude writes its own version on your machine, so yours will differ in the details.

The video is filmed on Ubuntu 24.04 in the VS Code terminal. The prompts and the Claude Code steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 5.5 done**: your own `harborline` repository in `~/projects/harborline` at the Lesson 5.5 commit, its `.venv`, `pytest` passing, and `origin` pointing at your own private `harborline` repository. Lesson 5.3's `.claude/rules/` are in place (the testing rule loads when Claude writes the tests).
- **Claude Code** (Lesson 0.5), signed in, with the `harborline` folder trusted.
- About 20 minutes. **No API calls: Claude Code runs on your Claude sign-in.** Each message counts toward your Claude Code usage like any other prompt.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### 1. The interview

```bash
git status --short
claude
```

`git status --short` prints nothing: the tree is clean. In Claude Code, send the interview request (from `commands.txt`):

```text
Some new orders come from a marketplace partner whose dates look like 10/08/2026 2:30 PM ET. I want harborline/normalize.py to handle them. Before you write anything, interview me: ask the questions you need answered, all in one message.
```

Claude reads `normalize.py` and answers with questions only: in the lesson, nine of them (day or month first, the time zone and daylight saving, the output format, other shapes, date-only values, how to detect the partner format, which fields, naive ISO strings, tests and commit). Read them before you answer: one of them is usually something you hadn't considered.

### 2. Examples and failing tests

Send one answer, with three examples, and ask for the tests first (the full text is in `commands.txt`). It's **one message** because these answers interact: the day order, the zone and the output format all shape the same conversion.

| Input | Expected output |
|---|---|
| `10/08/2026 2:30 PM ET` | `2026-10-08T18:30:00Z` (October: daylight time, UTC−4) |
| `01/02/2026 9:05 AM ET` | `2026-01-02T14:05:00Z` (January: standard time, UTC−5) |
| `10/08/2026` | `2026-10-08` (a date alone stays a date) |

Claude writes `tests/test_partner_dates.py`, runs it, and shows you the failures without touching `normalize.py`. In the lesson, 5 of the 6 new tests failed, and one passed **for the wrong reason**: the old code sent every value with a `T` (and `ET` has one) to the ISO parser, which raised an error that happened to contain the value. That's why you watch new tests fail before you write the code.

The lesson's answer doesn't answer question 8 (naive ISO strings). Claude said so and left it out of scope, instead of guessing.

### 3. Make them pass

```text
Now change normalize.py so these tests pass, then run the whole suite.
```

Claude adds `partner_to_utc` (a value with a `/` must match the exact shape; the time is read in `America/New_York`, then converted to UTC; a date alone stays a date; anything else raises a `ValueError` that shows the value) and runs both: 6 of 6, and the whole suite with 0 failed.

### 4. One more example, then commit

The midnight case is **independent** of the rest, so it goes on its own:

```text
One more example for the tests: 10/08/2026 12:00 AM ET gives 2026-10-08T04:00:00Z. Add it and run the test file.
```

Claude adds the test and runs the file: 7 passed. Then:

```text
/exit
```

```bash
clear
git status --short
git add harborline/normalize.py tests/test_partner_dates.py
git commit -m "Lesson 5.6: partner dates in normalize.py, test-first from three examples"
git push
```

`git status --short` shows ` M harborline/normalize.py` and `?? tests/test_partner_dates.py`. The commit has 2 files, 67 insertions and 1 deletion.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| The tests Claude runs | `.venv/bin/python -m pytest` | `.venv\Scripts\python -m pytest` (Claude picks the right one from your project) |
| The time zone data | built in | `zoneinfo` needs the `tzdata` package on Windows: `.venv\Scripts\python -m pip install tzdata` if a test fails with `ZoneInfoNotFoundError` |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal).

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` at the start | nothing: the tree is clean |
| The interview request | nine questions, no code; question 8 about naive ISO strings |
| Tests first | `tests/test_partner_dates.py`, 40 lines; 5 of the 6 new tests fail; one passes for the wrong reason |
| The unanswered question | "You didn't answer question 8, so I've left it out of scope." |
| Make them pass | `normalize.py`: 23 lines added, 1 removed; 6 of 6; full suite 124 passed, 0 failed |
| One more example | the midnight test; 7 passed |
| The commit | 2 files changed, 67 insertions, 1 deletion |
| API spend | $0: Claude Code on the subscription, no API calls |

See `expected-output.md` for the exact lines.

## Troubleshooting

- **Claude starts writing code instead of asking**: say so in one line ("Stop: questions first, no code yet") and send the interview request again. Press **Esc** to stop it mid-action.
- **Your questions differ from the lesson's**: that's expected. Answer what it asks; keep the three examples exactly as in the table, because the tests are built from them.
- **No test fails in step 2**: check that `normalize.py` is unchanged (`git status --short` shows only the new test file). If Claude already changed it, ask it to revert `normalize.py` and run the tests again.
- **A time is off by one hour**: the conversion used a fixed offset instead of the `America/New_York` zone. Point Claude at the failing test and its output, not just "it's wrong".
- **`ZoneInfoNotFoundError` on Windows**: install `tzdata` in the project's environment (see the table above).
- **The full suite has failures that aren't about dates**: something else changed since Lesson 5.5. Fix that first, or commit only the two files, as in the lesson.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Interview pattern:** ask Claude to question you before it writes anything.
- **Input/output examples:** concrete input → expected output pairs that define a transformation.
- **Test-first:** write the tests, watch them fail, then write the code.
- **Red, then green:** failing tests, then passing ones.
- **Interacting issues:** problems whose fixes affect each other; send them together. Independent ones go one at a time.

Claude Code changes often. If a message or a step doesn't match what you see, follow the official page, Best practices for Claude Code (https://code.claude.com/docs/en/best-practices).
