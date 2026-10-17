# Student kit: Lesson 6.3, Explicit criteria beat "be conservative"

Claude Certified Architect – Foundations (CCAR-F) · Module 6: Claude Code in CI/CD · Lesson 6.3

This kit holds everything you need to repeat the lesson on your own computer: every command in order, the files the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Replace "be conservative" with report/skip rules
2. Anchor severity with real code examples
3. Switch off a noisy category while you fix it

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `review-v1.md` | The vague version of the criteria you start with in step 1 (one line: "thoroughly, but be conservative") |
| `harborline/ci/prompts/review.md` | The explicit version you write in step 4: what to report, what to skip, and severity with examples |
| `harborline/ci/review_config.json` | The category switch, as the lesson ends it: `{"disabled_categories": ["style"]}` |
| `harborline/ci/review.py` | The reviewer from Lesson 6.2 after this lesson's edits: the criteria file, the config filter, and a `--local` mode |
| `harborline/ci/findings.schema.json` | The findings schema from Lesson 6.2, unchanged (for reference) |
| `harborline/scripts/refund_totals.py` | The teammate's file on the `refund-totals` branch: the diff the lesson reviews |

You type `review.md` (both versions), `review_config.json` and the `review.py` edits yourself, as in the lesson, or paste them from the kit.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The code and the steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 6.2 done**: your own `harborline` repository in `~/projects/harborline` at the Lesson 6.2 commit, with `ci/review.py` and `ci/findings.schema.json` from Lesson 6.2, its `.venv`, `pytest` passing, Claude Code installed (the `claude` command), and `origin` pointing at your own private `harborline` repository.
- **Your Anthropic API key in `.env`** (Lesson 0.4): `ANTHROPIC_API_KEY=...`. `.env` is in `.gitignore`, so it is never committed.
- About 20 minutes. **This lesson makes API calls**: each local review runs `claude -p` on your API key. In the lesson, each run cost between $0.0016 and $0.0035 (seven runs, about two cents in all).

## Before you start: a teammate's branch

The lesson reviews a teammate's branch, `refund-totals`, with one new file: `scripts/refund_totals.py`. It prints refund totals per customer, in deliberately loose style (one-letter names, no docstrings), with one real problem on line 17: `round(sum(...))` rounds the total to whole dollars, so the cents are gone. Make the branch once, from the kit's copy:

```bash
git switch -c refund-totals
cp <kit>/harborline/scripts/refund_totals.py scripts/refund_totals.py
git add scripts/refund_totals.py
git commit -m "Refund totals per customer for the weekly report"
git push -u origin refund-totals
git switch main
```

Replace `<kit>` with the folder where you unpacked this kit.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### The teammate's branch

```bash
git status --short
set -a; source .env; set +a
git fetch -q && git log --oneline main..origin/refund-totals
git --no-pager diff main...origin/refund-totals
```

The tree is clean; `source .env` exports your API key for `claude -p`; the log shows one commit, and the diff adds `scripts/refund_totals.py`.

### 1. Criteria in a file

```bash
mkdir -p ci/prompts
code ci/prompts/review.md
```

Type the vague version from `review-v1.md` (one line) and save. It's where many teams start: "Review this pull request's diff thoroughly, but be conservative: report only issues you are confident about."

```bash
code ci/review_config.json
```

Type `{"disabled_categories": []}` on three lines and save: a list of categories to switch off, empty for now.

```bash
code ci/review.py
```

Edit Lesson 6.2's reviewer so the criteria live in the file, not in the code (the kit's `ci/review.py` is the result):

- At the top, two loads: `CRITERIA` reads `ci/prompts/review.md`; `CONFIG` reads `ci/review_config.json`.
- `PROMPT` loses its old built-in first line, and `review()` builds the prompt as `CRITERIA + PROMPT.format(...)`.
- `review()` drops every finding whose category is in `CONFIG["disabled_categories"]`, and returns them in `result["findings"]`; `main()` reads `result["findings"]`.
- A local mode: `python ci/review.py --local <git range>` runs the same review on `git diff <git range>`, prints each finding as `path:line severity category: issue`, then one line with the findings, the turns and the cost. It posts nothing.

### 2. Measure the vague version

```bash
python ci/review.py --local main...origin/refund-totals
python ci/review.py --local main...origin/refund-totals
```

Run it twice on the same diff, with nothing changed. In the lesson, both runs happened to agree: one finding, line 17, a medium bug. In our practice runs of the same prompt, they didn't: the same line came back as a bug in one run and a convention break in another, with an extra, speculative finding some of the time. Your runs may differ again. That is the point of measuring.

### 3. Switch off a noisy category

Change `ci/review_config.json` to `{"disabled_categories": ["style"]}`, save, and run once more:

```bash
python ci/review.py --local main...origin/refund-totals
```

Nothing in the lesson's runs was filed as style, so the switch had nothing to hide there. It's a stopgap: ready the day style comments start costing trust, and it never touches the bugs. In the lesson this third run found two things: line 17, medium, and a new one on line 14, at low (the seed data may not record refunds already paid). That second one is a guess about data, not a problem in this diff.

### 4. Explicit criteria

Replace `ci/prompts/review.md` with the explicit version from the kit:

- **Report** only these, each defined: a bug (crashes, or a wrong result, on data this project really has), a convention break (a rule in `CLAUDE.md` or `docs/conventions/`), a security problem (a secret in the code, or outside input that reaches a shell, a file path or a refund).
- **Skip**, even when noticed: naming, formatting, docstrings, comments and code style; refactors, performance ideas and "consider" suggestions; anything you can't tie to one line of the diff.
- **Severity**, with examples from this codebase: high (wrong money or wrong dates reach a customer or a report, like a refund computed by hand instead of with `policy.check_refund`), medium (a crash on real data), low (wrong only on rare inputs, and no customer sees it).

Then run it twice:

```bash
python ci/review.py --local main...origin/refund-totals
python ci/review.py --local main...origin/refund-totals
```

In the lesson, line 17 came back as a **high** bug in both runs: wrong money in a report is exactly the high example. The second run also brought the seed-data guess back, at medium. The criteria fixed what is reported as high, not every judgment call; examples of what a finding looks like, and of when to report nothing, come in Lesson 6.4.

### Commit and push

```bash
git status --short
git add ci
git commit -m "Lesson 6.3: explicit review criteria in ci/prompts/review.md, and a switch for noisy categories"
git push
```

The commit has 3 files: `ci/review.py` changed, `ci/prompts/review.md` and `ci/review_config.json` new.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Load the key from `.env` | `set -a; source .env; set +a` | PowerShell: `Get-Content .env \| ForEach-Object { $k, $v = $_ -split '=', 2; Set-Item "env:$k" $v }` |
| Make the folder | `mkdir -p ci/prompts` | PowerShell: `mkdir ci\prompts` |
| Copy the teammate's file | `cp <kit>/harborline/scripts/refund_totals.py scripts/` | PowerShell: `Copy-Item <kit>\harborline\scripts\refund_totals.py scripts\` |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

`git diff main...origin/refund-totals` (three dots) is the same everywhere: the changes on the branch since it left `main`. **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save).

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git log --oneline main..origin/refund-totals` | one commit, `8eb2fdd Refund totals per customer for the weekly report` |
| The vague version, run 1 | 1 finding: `scripts/refund_totals.py:17 medium bug`; 3 turns, $0.0033 |
| The vague version, run 2 | the same single finding, medium bug; 3 turns, $0.0026 |
| With `["style"]` switched off | 2 findings: line 17 medium bug; line 14 low bug (the seed data); 3 turns, $0.0033 |
| The explicit version, run 1 | 1 finding: line 17 **high** bug; 5 turns, $0.0035 |
| The explicit version, run 2 | 2 findings: line 17 **high** bug; line 14 medium bug (the seed data); 3 turns, $0.0016 |
| The commit | `ccc4dec`, 3 files changed, 42 insertions, 6 deletions |

See `expected-output.md` for the exact lines. Model output changes from run to run: compare the behavior, not the wording.

## Troubleshooting

- **`claude: command not found`**: Claude Code isn't installed or isn't on your `PATH` (Lesson 0.3). `claude --version` must work in this terminal.
- **An authentication error, or `Invalid API key`**: the key isn't exported in this terminal. Run `set -a; source .env; set +a` again, and check `ANTHROPIC_API_KEY` in `.env` (Lesson 0.4).
- **`fatal: ambiguous argument 'main...origin/refund-totals'`**: the branch isn't on your remote yet. Make it (see "Before you start"), then `git fetch`.
- **`FileNotFoundError: ... ci/prompts/review.md` or `review_config.json`**: `review.py` now loads both at the top. Create them first (step 1), from the `harborline` folder.
- **`KeyError: 'disabled_categories'`**: the config must be a JSON object with that exact key: `{"disabled_categories": []}`.
- **More or different findings than the lesson**: expected. Runs vary; that is what step 2 measures. With the explicit criteria, the line-17 rounding finding should come back as high, and naming or style comments should be gone.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Vague instruction:** an adjective ("conservative", "important") the model has to interpret.
- **Categorical criteria:** a list of what to report and what to skip.
- **Severity anchor:** a code example that defines what a level, like high, means here.
- **False positive:** a finding that isn't a real problem; each one costs trust.
- **Category switch:** config that turns one category off while its rules are fixed.

Claude Code changes often. If an option or a message doesn't match what you see, follow the official pages: Run Claude Code programmatically (https://code.claude.com/docs/en/headless) and the prompting best practices (https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).
