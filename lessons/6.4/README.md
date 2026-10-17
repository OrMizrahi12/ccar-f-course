# Student kit: Lesson 6.4, Few-shot for consistent output

Claude Certified Architect – Foundations (CCAR-F) · Module 6: Claude Code in CI/CD · Lesson 6.4

This kit holds everything you need to repeat the lesson on your own computer: every command in order, the file the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Show the choice, not just the rule
2. Pin the format with examples
3. Put acceptable code next to real issues

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/ci/prompts/review.md` | The review criteria as the lesson ends them: Lesson 6.3's criteria, then the rule line, the format line and the four examples (the last 18 lines) |
| `harborline/harborline/late_refunds.py` | The teammate's file on the `late-refunds` branch (Lesson 6.1): the diff the lesson measures |

You type the 18 new lines yourself, as in the lesson, or paste them from the kit.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The code and the steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 6.3 done**: your own `harborline` repository in `~/projects/harborline` at the Lesson 6.3 commit, with `ci/review.py --local`, `ci/prompts/review.md` (the explicit criteria) and `ci/review_config.json` from Lesson 6.3, its `.venv`, Claude Code installed (the `claude` command), and `origin` pointing at your own private `harborline` repository.
- **The two teammate branches**: `late-refunds` (Lesson 6.1) and `refund-totals` (Lesson 6.3), pushed to your `origin`. If one is missing, make it from that lesson's kit.
- **Your Anthropic API key in `.env`** (Lesson 0.4): `ANTHROPIC_API_KEY=...`. `.env` is in `.gitignore`, so it is never committed.
- About 20 minutes. **This lesson makes API calls**: each local review runs `claude -p` on your API key. In the lesson, each run cost between $0.0022 and $0.0066 (five runs, about two cents in all).

## The test diff

The lesson measures the first commit of the `late-refunds` branch: `harborline/late_refunds.py`, 17 lines that parse raw dates (lines 7 and 8), subtract them (line 9) and compute a refund by hand (line 17). In the lesson that commit is `b065274`. Find yours once:

```bash
git log --oneline --reverse main..origin/late-refunds | head -1
```

and use its hash wherever the lesson shows `b065274`. Using the commit, not the branch name, keeps the test diff the same even if the branch gets more commits later.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### The starting point

```bash
git status --short
set -a; source .env; set +a
git log --oneline -1 <your late-refunds commit>
```

The tree is clean; `source .env` exports your API key for `claude -p`; the log shows the teammate's commit.

### 1. Measure the drift

```bash
python ci/review.py --local main...<your late-refunds commit>
python ci/review.py --local main...<your late-refunds commit>
```

Run it twice on the same diff, with Lesson 6.3's criteria and nothing changed. In the lesson: three findings, then four. The raw-date problem came back as two findings in the first run (a convention break on line 7 and a bug on line 9) and as three in the second (line 7 twice, as a convention break and as a bug, plus line 9). The criteria said what to report, not how many findings one mistake is, or what shape a finding takes.

### 2. Add four examples

```bash
code ci/prompts/review.md
```

Below the criteria, add (the kit's `review.md` is the result):

- **One rule line**: one root cause is one finding; a convention break is filed as convention, even when it also crashes.
- **The format, in words**: the issue in at most two sentences, naming the rule file for a convention; the fix as one concrete change.
- **Four examples**, each a diff line and the finding it should get:
  - a line that parses the raw `placed_at` field: `convention, medium`, with the issue and the fix, and the reason it is not a second bug finding for the crash (the same root cause);
  - a loop that skips the first item: `bug, high`;
  - `print(f"{customer_id}: {fee:.2f}")`: `None.` Rounding to cents when printing is what the money convention asks for;
  - `t = {}`: `None.` A short name is style, and style is skipped.

None of the four examples is a line from either test diff: the point is that the model generalizes, not that it copies.

### 3. Same diff, same findings

```bash
python ci/review.py --local main...<your late-refunds commit>
python ci/review.py --local main...<your late-refunds commit>
python ci/review.py --local main...origin/refund-totals
```

In the lesson, both runs gave the same two findings: line 17 high convention, and line 7 medium convention with the crash folded in. The wording still differed. Then a diff the examples have never seen: two high convention findings on `refund_totals.py` (line 17, the rounding to whole dollars; line 14, raw orders read without `normalize`), and the lines that print cents were not flagged.

### Commit and push

```bash
git status --short
git add ci/prompts/review.md
git commit -m "Lesson 6.4: few-shot examples for one finding per root cause and a fixed format"
git push
```

One file changed, 18 insertions.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Load the key from `.env` | `set -a; source .env; set +a` | PowerShell: `Get-Content .env \| ForEach-Object { $k, $v = $_ -split '=', 2; Set-Item "env:$k" $v }` |
| Find the first late-refunds commit | `git log --oneline --reverse main..origin/late-refunds \| head -1` | PowerShell: `git log --oneline --reverse main..origin/late-refunds \| Select-Object -First 1` |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

`git diff main...<commit>` (three dots) is the same everywhere: the changes since that commit left `main`. **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save).

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| Lesson 6.3's criteria, run 1 | 3 findings: 17 high convention; 7 medium convention; 9 medium bug; 4 turns, $0.0032 |
| Lesson 6.3's criteria, run 2 | 4 findings: 17 high convention; 7 medium convention; 7 medium bug; 9 medium bug; 2 turns, $0.0023 |
| With the examples, run A | 2 findings: 17 high convention; 7 medium convention; 3 turns, $0.0032 |
| With the examples, run B | the same 2 findings; 2 turns, $0.0022 |
| `main...origin/refund-totals` | 2 findings: 14 high convention; 17 high convention; 7 turns, $0.0066 |
| The commit | `69c2202`, 1 file changed, 18 insertions |

See `expected-output.md` for the exact lines. Model output changes from run to run: compare the shape, not the wording.

## Troubleshooting

- **`claude: command not found`**: Claude Code isn't installed or isn't on your `PATH` (Lesson 0.3). `claude --version` must work in this terminal.
- **An authentication error, or `Invalid API key`**: the key isn't exported in this terminal. Run `set -a; source .env; set +a` again, and check `ANTHROPIC_API_KEY` in `.env` (Lesson 0.4).
- **`fatal: ambiguous argument`**: the commit hash or the branch isn't known here. Run `git fetch`, then find the hash again; `refund-totals` must be pushed (Lesson 6.3).
- **Your first two runs already agree**: drift is a tendency, not a guarantee. Run once or twice more; in our practice run, as in the lesson, one pair gave three findings and then four.
- **The runs with examples still differ**: compare the shape first (lines, categories, severities). If a root cause is still split, check that the rule line and the first example (the "not a second bug finding" line) were saved.
- **A finding quotes one of the example lines**: the examples are being read as part of the diff. Keep the `Examples (diff line, then the finding, or none):` header above them, as in the kit.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Few-shot examples:** a handful of worked input → output pairs in the prompt.
- **Plausible alternative:** the other answer a reasonable reviewer might give; the example says why not.
- **Root cause:** the one underlying mistake behind several symptoms; one finding.
- **Acceptable pattern:** code that looks suspicious but is fine here; an example answered "None", with the reason.
- **Format drift:** the same finding shaped differently from run to run.

Claude Code changes often. If an option or a message doesn't match what you see, follow the official pages: Run Claude Code programmatically (https://code.claude.com/docs/en/headless) and the prompting best practices (https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).
