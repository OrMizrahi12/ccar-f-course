# Student kit: Lesson 6.5, Independent and multi-pass review

Claude Certified Architect – Foundations (CCAR-F) · Module 6: Claude Code in CI/CD · Lesson 6.5

This kit holds everything you need to repeat the lesson on your own computer: every command in order, the files the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Review with a fresh, independent instance
2. Split a big change: per-file and cross-file passes
3. Verify findings and route them by confidence

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/ci/review.py` | The reviewer as the lesson ends it: a pass per file, a cross-file pass, an independent check with a verdict and a confidence, and routing by confidence |
| `harborline/ci/verify.schema.json` | The schema of the check's answer (new in this lesson) |
| `harborline/ci/review_config.json` | The config as the lesson ends it: Lesson 6.3's switch, plus `"inline_confidence": 0.8` |
| `harborline/harborline/fees.py` | The teammate's first file on the `weekly-fees` branch: shipping fees owed per customer, in integer cents |
| `harborline/scripts/weekly_fees.py` | The teammate's second file: the weekly report, which prints those cents as dollars |

You type the `review.py` edits, `verify.schema.json` and the config line yourself, as in the lesson, or paste them from the kit.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The code and the steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 6.4 done**: your own `harborline` repository in `~/projects/harborline` at the Lesson 6.4 commit, with `ci/review.py --local`, `ci/prompts/review.md` (Lesson 6.3's criteria and Lesson 6.4's examples), `ci/review_config.json` and `ci/findings.schema.json`, its `.venv`, Claude Code installed (the `claude` command), and `origin` pointing at your own private `harborline` repository.
- **Your Anthropic API key in `.env`** (Lesson 0.4): `ANTHROPIC_API_KEY=...`. `.env` is in `.gitignore`, so it is never committed.
- About 25 minutes. **This lesson makes API calls**: the multi-pass review runs `claude -p` four times on your API key (two per-file passes, a cross-file pass and the check). In the lesson, the run took 28 turns, about two minutes, and cost $0.0244.

## Before you start: a teammate's branch

The lesson reviews a teammate's branch, `weekly-fees`, with two new files. `harborline/fees.py` returns the shipping fees owed per customer **in integer cents**, so totals never drift. `scripts/weekly_fees.py` prints them **as dollars**, with a dollar sign and no division by 100, so a $6.95 fee prints as `$695.00`. Each file is reasonable on its own; the bug lives between them. Make the branch once, from the kit's copies:

```bash
git switch -c weekly-fees
cp <kit>/harborline/harborline/fees.py harborline/fees.py
cp <kit>/harborline/scripts/weekly_fees.py scripts/weekly_fees.py
git add harborline/fees.py scripts/weekly_fees.py
git commit -m "Weekly report of shipping fees owed, per customer"
git push -u origin weekly-fees
git switch main
```

Replace `<kit>` with the folder where you unpacked this kit.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### 1. Passes and a checker

```bash
git status --short
code ci/review.py
```

The tree is clean. In `ci/review.py` (the kit's copy is the result), from the bottom up:

- **The local print**: each finding now shows `found by <pass>` and the checker's verdict and confidence, and the last line says how many passes ran: `N findings from N passes; N turns, $…`.
- **Routing in `post()`**: a new finding becomes an inline comment only when its `confidence` reaches `CONFIG["inline_confidence"]`; every other one goes in the summary comment as `For a person to check (0.xx)`.
- **`review()`**: one pass per file (the criteria and that file's part of the diff); when the change has more than one file, one cross-file pass (the whole diff, plus the `CROSS` instruction); every finding tagged `found_by`; then, if anything was found, one check call: the findings as a numbered list, the whole diff, the `CHECK` prompt and `verify.schema.json`. Each check sets `verdict` and `confidence`; findings with verdict `rejected` are dropped.
- **Two helpers**: `files(diff)` splits the diff at each `diff --git` header, keyed by path; `claude(prompt, text, schema)` now takes the schema as a parameter.
- **The prompts**: `CROSS` (each file was already reviewed on its own; report only problems that span files), `VERIFY` (loads the new schema) and `CHECK` (you are checking findings another reviewer wrote; read the code each one points to; give an index, a verdict and a confidence).

Save, then:

```bash
code ci/verify.schema.json
```

Type the schema (the kit's copy): `checks`, a list of objects with `index` (integer), `verdict` (`confirmed`, `rejected` or `unsure`) and `confidence` (0 to 1). Save.

```bash
code ci/review_config.json
```

Add `"inline_confidence": 0.8` after `disabled_categories` (mind the comma) and save.

### 2. The bug, for real

```bash
clear
set -a; source .env; set +a
git fetch -q && git log --oneline main..origin/weekly-fees
git --no-pager diff main...origin/weekly-fees --stat
git switch -q --detach origin/weekly-fees && python -m scripts.weekly_fees; git switch -q main
```

One commit, two files. The report prints `$695.00` per customer and a total of `$1,390.00`: each fee is really $6.95. The last line runs the script on the branch without leaving `main` checked out afterwards.

### 3. Multi-pass review

```bash
clear
python ci/review.py --local main...origin/weekly-fees
```

It prints nothing for about two minutes (four calls in a row), then the findings. In the lesson: four findings from four passes. The cents bug (`scripts/weekly_fees.py:12`, high) was found by the cross-file pass and confirmed at 0.97. A rounding convention finding was confirmed at only 0.60: below the threshold, so in CI it would go to the summary, for a person to check. And the raw-orders finding on `fees.py:9` came twice, from two passes: a duplicate.

### Commit and push

```bash
clear
git status --short
git add ci
git commit -m "Lesson 6.5: a pass per file, a cross-file pass and an independent check with confidence"
git push
```

Three files changed, 68 insertions, 13 deletions.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Load the key from `.env` | `set -a; source .env; set +a` | PowerShell: `Get-Content .env \| ForEach-Object { $k, $v = $_ -split '=', 2; Set-Item "env:$k" $v }` |
| Run the script on the branch | `git switch -q --detach origin/weekly-fees && python -m scripts.weekly_fees; git switch -q main` | PowerShell: `git switch -q --detach origin/weekly-fees; python -m scripts.weekly_fees; git switch -q main` |
| Copy the kit's files | `cp <kit>/... ...` | PowerShell: `Copy-Item <kit>\... ...` |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

`git diff main...origin/weekly-fees` (three dots) is the same everywhere: the changes on the branch since it left `main`. **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save).

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git log --oneline main..origin/weekly-fees` | one commit, `b6e1856` |
| `--stat` | `harborline/fees.py` 14, `scripts/weekly_fees.py` 17; 2 files changed, 31 insertions |
| The script on the branch | `C-1043  $695.00`, `C-1008  $695.00`, `total  $1,390.00` |
| The multi-pass review | 4 findings from 4 passes; 28 turns, $0.0244 |
| `scripts/weekly_fees.py:12` | high bug, found by cross-file; confirmed 0.97 |
| `harborline/fees.py:9` | low convention, found by `harborline/fees.py`; confirmed 0.85; and again as medium, found by cross-file; confirmed 0.75 |
| `harborline/fees.py:12` | low convention, found by `harborline/fees.py`; confirmed 0.60 (below 0.8: a person checks it) |
| The commit | `40d212f`, 3 files changed, 68 insertions, 13 deletions |

See `expected-output.md` for the exact lines. Model output changes from run to run: compare the behavior, not the wording.

## Troubleshooting

- **`claude: command not found`**: Claude Code isn't installed or isn't on your `PATH` (Lesson 0.3). `claude --version` must work in this terminal.
- **An authentication error, or `Invalid API key`**: the key isn't exported in this terminal. Run `set -a; source .env; set +a` again, and check `ANTHROPIC_API_KEY` in `.env` (Lesson 0.4).
- **`KeyError: 'inline_confidence'`**: the config line is missing or the file wasn't saved. `ci/review_config.json` must match the kit's copy.
- **`FileNotFoundError` for `verify.schema.json`**: the schema must be saved as `ci/verify.schema.json`, next to `review.py`.
- **`fatal: ambiguous argument 'main...origin/weekly-fees'`**: the branch isn't pushed or fetched. Make it as in [Before you start](#before-you-start-a-teammates-branch), then `git fetch`.
- **The run seems stuck**: four calls in a row take one to three minutes, and the local mode prints nothing until the end. Wait for the prompt.
- **The cents bug is found by a different pass, or by two**: that's normal. In our practice runs the per-file pass for `weekly_fees.py`, which can read `fees.py` with its tools, sometimes caught it too. What matters is that the bug is found and confirmed.
- **Two findings point at the same line**: overlapping passes can report the same problem twice, and the checker confirms both when both are true. Merging duplicates is a separate step.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Self-review bias:** the author's context and assumptions make its own mistakes harder to see.
- **Independent instance:** a new session with no memory of writing the code.
- **Per-file pass:** one file's diff reviewed alone.
- **Cross-file pass:** the whole change, looking only at what spans files.
- **Confidence routing:** confident findings become comments; uncertain ones go to a person.

Claude Code changes often. If an option or a message doesn't match what you see, follow the official pages: Best practices for Claude Code (https://code.claude.com/docs/en/best-practices) and Run Claude Code programmatically (https://code.claude.com/docs/en/headless).
