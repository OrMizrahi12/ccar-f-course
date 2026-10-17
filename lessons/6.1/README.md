# Student kit: Lesson 6.1, Claude Code without a human

Claude Certified Architect – Foundations (CCAR-F) · Module 6: Claude Code in CI/CD and Review Prompts · Lesson 6.1

This kit holds everything you need to repeat the lesson on your own computer: every command in order, the schema the lesson ends with, the teammate's branch it reviews, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Run Claude Code headless with `-p`
2. Get findings as schema-checked JSON
3. Give a CI run the project's rules

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the lesson, in order (copy the long ones from here) |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/ci/findings.schema.json` | The findings schema as committed at the end of the lesson |
| `harborline/harborline/late_refunds.py` | The teammate's change the lesson reviews (the only file on the `late-refunds` branch) |

## What you need

- **Module 5 done**: your own `harborline` repository in `~/projects/harborline`, on `main`, clean, with its `.venv`, and `origin` pointing at your own private `harborline` repository. Its `CLAUDE.md` has the Conventions section that imports `docs/conventions/money.md` and `docs/conventions/dates.md`.
- **Your API key in `.env`** (Lesson 0.6): `ANTHROPIC_API_KEY=...`. A CI runner has a key, not a sign-in, so the lesson's headless runs use it. Never print it: no `cat .env`, no `echo $ANTHROPIC_API_KEY`.
- **Claude Code** (Lesson 0.5).
- **jq**, a small command-line JSON tool (install it below if `jq --version` fails).
- About 15 minutes, and a few cents at most: in the lesson the review cost $0.0045 and each context question under $0.002, on Haiku 5.5.

## Before you start: the teammate's branch

The lesson reviews a teammate's branch, `late-refunds`, that was pushed before the lesson. Make yours once: copy `harborline/late_refunds.py` from this kit into your repository's `harborline/` folder, then:

```bash
git switch -c late-refunds
git add harborline/late_refunds.py
git commit -m "Late-delivery refund estimates for the weekly report"
git push -u origin late-refunds
git switch main
```

The file is meant to be imperfect: it parses raw dates and computes a refund by hand, which breaks two of Harborline's conventions. That's what the review should find. The same branch is the pull request of Lesson 6.2, so keep it.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)`.

### 1. Headless

```bash
git status --short
set -a; source .env; set +a
```

`git status --short` prints nothing. `set -a; source .env; set +a` exports every variable in `.env` into this shell, so `claude` finds `ANTHROPIC_API_KEY`; it prints nothing.

```bash
git fetch -q && git log --oneline main..origin/late-refunds
git diff main...origin/late-refunds --stat
git diff main...origin/late-refunds | claude -p "In one sentence, what does this change do?"; echo "exit code $?"
```

`-p` (print) runs one prompt, reads the piped diff, prints the answer and exits. No session opens and nothing waits for you. `$?` is the exit code: 0 on success, non-zero when the run fails. That's what a CI job branches on.

A yellow warning that claude.ai connectors are disabled because `ANTHROPIC_API_KEY` takes precedence is expected: the key wins over your sign-in. In the lesson the answer also added an unasked second paragraph about two broken project conventions: plain `-p` loads `CLAUDE.md`, as an interactive session does.

### 2. A findings schema

```bash
mkdir -p ci
code ci/findings.schema.json
```

Type (or paste) the schema from `harborline/ci/findings.schema.json` and save. One field, `findings`, an array; each finding has `path`, `line`, `category` (bug, convention, security or style), `severity` (high, medium or low), `issue` and `fix`, all required.

### 3. The review as JSON

```bash
clear
git diff main...origin/late-refunds | claude -p "Review this diff for bugs and for breaks of this project's conventions. Report each finding with its file and line." --output-format json --json-schema "$(cat ci/findings.schema.json)" > /tmp/review.json; echo "exit code $?"
jq .structured_output /tmp/review.json
```

The output goes to a file, so the screen stays still while it runs (about 15 seconds in the lesson). `--output-format json` wraps the answer with metadata; with `--json-schema`, the findings arrive in the `structured_output` field, in your schema's shape. In the lesson: exit code 0 and four findings (two convention breaks naming `docs/conventions/money.md` and `docs/conventions/dates.md`, a high bug on Unix-second dates, a low bug on partial days). Yours will differ in number and wording.

```bash
clear
jq '{turns: .num_turns, cost: .total_cost_usd, session: .session_id}' /tmp/review.json
```

The run's metadata: in the lesson, 3 turns, a cost of 0.0045 dollars, and the session ID. A schema guarantees the shape of the findings, not that each one is right: a reviewer still decides.

### 4. Where the rules come from

```bash
clear
Q="Without reading any files: quote the conventions you were given for this repository, or say there are none. Nothing else."
claude -p "$Q"
claude --bare -p "$Q"
claude --bare -p "$Q" --append-system-prompt-file CLAUDE.md
```

- Plain `claude -p` quotes both convention files: it loaded `CLAUDE.md` and its `@` imports.
- `claude --bare -p` answers that there are none. Bare mode skips `CLAUDE.md`, hooks, skills, plugins, MCP servers, auto memory and the sign-in (it needs `ANTHROPIC_API_KEY`), so every machine starts the same.
- `--append-system-prompt-file CLAUDE.md` passes the file's text, but its `@` lines aren't expanded: in the lesson only the two import lines arrived. In bare mode, pass the rules themselves (for example the convention files), not a file that only points to them.

```bash
clear
git status --short
git add ci/findings.schema.json
git commit -m "Lesson 6.1: ci/findings.schema.json for headless reviews"
git push
```

`git status --short` shows `?? ci/`. The commit has 1 file and 21 insertions.

## Windows, macOS and Linux

| | Linux and WSL (the lesson) | macOS | Windows (native PowerShell) |
|---|---|---|---|
| Install jq | `sudo apt install jq` | `brew install jq` | `winget install jqlang.jq` |
| Load `.env` into the shell | `set -a; source .env; set +a` | the same | use **WSL** or **Git Bash** for this lesson; PowerShell has no `source` for `.env` files |
| The exit code | `echo "exit code $?"` | the same | in PowerShell: `echo "exit code $LASTEXITCODE"` |
| `$(cat ci/findings.schema.json)` | as shown | the same | in PowerShell: `(Get-Content ci/findings.schema.json -Raw)` |
| `/tmp/review.json` | as shown | the same | use a path in your project, for example `review.json` (and don't commit it) |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal). Without jq, `python -m json.tool /tmp/review.json` pretty-prints the whole file.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` at the start | nothing: the tree is clean |
| The teammate's branch | one commit, "Late-delivery refund estimates for the weekly report"; 1 file, 17 insertions |
| One sentence with `-p` | a 10%-per-day refund capped at the total; an unasked paragraph on two broken conventions; `exit code 0` |
| The review as JSON | `exit code 0`; four findings in `structured_output` (lines 7, 8, 9, 12) |
| The metadata | 3 turns, cost 0.004519065, a session ID |
| Plain `-p` | both convention files quoted word for word |
| `--bare -p` | "There are none." |
| `--bare` + `--append-system-prompt-file CLAUDE.md` | only the two `@docs/conventions/...` lines, unexpanded |
| The commit | 1 file changed, 21 insertions |
| API spend | the review: 0.0045 dollars, read from its own JSON |

See `expected-output.md` for the exact lines.

## Troubleshooting

- **`claude -p` asks you to sign in, or fails with an authentication error**: `ANTHROPIC_API_KEY` isn't in this shell. Run `set -a; source .env; set +a` again in the same terminal. Check `.env` has the variable without quotes or spaces around `=` (open it in the editor; never print it).
- **`exit code` is not 0**: read the output. When a failure happens inside the run, Claude Code prints it as the result; a bad flag is reported on stderr before the run starts.
- **`jq: command not found`**: install jq (table above), or use `python -m json.tool /tmp/review.json`.
- **`structured_output` is `null`**: check that `--output-format json` and `--json-schema` are both on the command, and that `ci/findings.schema.json` is valid JSON (`jq . ci/findings.schema.json`).
- **`git log main..origin/late-refunds` prints nothing**: the branch isn't pushed. Do "Before you start" again, then `git fetch`.
- **Plain `-p` also says there are no conventions**: run it from the repository's root, where `CLAUDE.md` is, and check that the Conventions section imports both files.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline`.

## Key terms

- **Headless (`-p`):** one prompt in, one answer out, then exit; nobody to ask.
- **Exit code:** 0 on success, non-zero on failure: what CI branches on.
- **`--output-format json`:** the answer plus session ID, turns and cost.
- **`--json-schema`:** output that follows your schema, in `structured_output`.
- **`--bare`:** skips CLAUDE.md, hooks, skills, MCP and the sign-in: the same start on every machine.

Claude Code changes often. If a flag or a message doesn't match what you see, follow the official page, Run Claude Code programmatically (https://code.claude.com/docs/en/headless).
