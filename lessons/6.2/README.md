# Student kit: Lesson 6.2, A pull-request review pipeline

Claude Certified Architect – Foundations (CCAR-F) · Module 6: Claude Code in CI/CD · Lesson 6.2

This kit holds everything you need to repeat the lesson on your own computer: every command in order, the files the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Run a review on every pull request
2. Post findings as inline comments
3. Re-review without repeating yourself

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/.github/workflows/pr-review.yml` | The workflow (18 lines): on `opened` and `synchronize`, `contents: read` and `pull-requests: write`, installs Claude Code and runs `ci/review.py` with the API key from the repository's secrets and the job's own token |
| `harborline/ci/review.py` | The review script (95 lines): the diff, the earlier findings, `claude -p` with JSON output and the schema, then one review with inline comments and a summary |
| `harborline/ci/findings.schema.json` | The findings schema with the new `status` field (`new` or `still_open`), required |
| `harborline/harborline/late_refunds.py` | The teammate's fix (9 lines), pushed in step 4 |

You type the new files yourself, as in the lesson, or copy them from the kit.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The code and the steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 6.1 done**: your own `harborline` repository in `~/projects/harborline` at the Lesson 6.1 commit, with `ci/findings.schema.json` (Lesson 6.1), Claude Code installed (the `claude` command), and `origin` pointing at your own `harborline` repository on GitHub.
- **The teammate's branch** `late-refunds` (Lesson 6.1), pushed to your `origin`. If it's missing, make it from Lesson 6.1's kit.
- **The GitHub CLI** (`gh`), signed in to your account: `gh auth status` must show it. Install it from https://cli.github.com and run `gh auth login` once.
- **Your Anthropic API key** (Lesson 0.4). In this lesson it goes into the repository's Actions secrets, never into a file in the repository.
- About 30 minutes. **This lesson makes API calls**, from GitHub Actions: each review run is one `claude -p` call on your key. In the lesson the two runs cost $0.0832 and $0.1247. The workflow passes no `--model`, so Claude Code's default model ran; add `"--model", "haiku"` to the `claude` command in `review()` if you want each run to cost a fraction of that.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### The starting point

```bash
git status --short
```

The tree is clean, on `main`, at the Lesson 6.1 commit.

### 1. The workflow

```bash
mkdir -p .github/workflows
code .github/workflows/pr-review.yml
```

Type the workflow (the kit's file). The parts that matter:

- **The trigger**: `pull_request` with `types: [opened, synchronize]`. `opened` runs it when a pull request is created; `synchronize` runs it on every later push to its branch. The docs' own example also lists `ready_for_review` and `reopened`; this pipeline needs the two.
- **The permissions**: `contents: read` to check out the code, `pull-requests: write` to post the review. Nothing more.
- **The steps**: check out the code, install Claude Code with npm, run `python3 ci/review.py` with the pull request's number.
- **The environment**: `ANTHROPIC_API_KEY` from `${{ secrets.ANTHROPIC_API_KEY }}`, never written in the code; `GH_TOKEN` from `${{ github.token }}`, the job's own token, which the `gh` commands in the script use.

### 2. The review script

```bash
code ci/review.py
code ci/findings.schema.json
```

Type the script (the kit's file). From the top:

- **`MARK`**: a hidden HTML comment, `<!-- harborline-review -->`, added to every comment the review posts, so the next run can find its own findings.
- **`PROMPT`**: review the diff for bugs and convention breaks, with the file and the line in the new version; the earlier findings are listed below it; report one that is still in the code again with status `still_open`, leave fixed ones out, give everything else status `new`.
- **`prior_findings()`**: the pull request's review comments that carry the mark, as `path:line: text`.
- **`review()`**: `claude -p` with the prompt, `--output-format json`, `--json-schema`, `--permission-mode dontAsk` and read-only tools (`Read,Grep,Glob`); the diff goes in on standard input. `check=True`, so a failed call fails the job.
- **`diff_lines()`**: the lines of each file the diff shows. GitHub accepts an inline comment only on those lines.
- **`post()`**: one review: each new finding on a line the diff shows becomes an inline comment; the rest, and every still-open finding, go into the summary, which starts with `Claude review: N new, N still open, N fixed.`
- **`main()`**: the diff, the earlier findings, the review, then the post. "Fixed" is the earlier count minus the still-open ones: the model decides what's still open, and you can check that on the diff.

In the schema, add `"status": {"type": "string", "enum": ["new", "still_open"]},` to the finding's properties and `"status"` to its `required` list. Then commit and push to `main`:

```bash
git status --short
git add .github ci
git commit -m "Lesson 6.2: review every pull request with Claude Code in GitHub Actions"
git push
```

### 3. Open the pull request

Once, before the first run, store your API key as a repository secret (the lesson did this off camera):

```bash
gh secret set ANTHROPIC_API_KEY -R <your-account>/harborline
```

`gh` asks for the value: paste your key and press Enter. GitHub never shows a secret's value again, only its name and when it was updated. Then:

```bash
gh repo set-default <your-account>/harborline
gh secret list -R <your-account>/harborline
gh pr create --base main --head late-refunds --title "Late-delivery refund estimates" --body "Refund estimates for the weekly report."
N=$(gh pr view late-refunds --json number -q .number); echo $N
sleep 10; gh run watch --exit-status "$(gh run list -w pr-review.yml -L 1 --json databaseId -q '.[0].databaseId')"
gh api repos/{owner}/{repo}/pulls/$N/comments --jq '.[] | "\(.path):\(.line)\n\(.body)\n"'
gh pr view $N --comments
```

The lesson's base was a branch named `lesson-6.2` (this lesson's commit), because the course repository's `main` has moved on; on your own repository the base is `main`. `sleep 10` gives GitHub a moment to start the run; `gh run watch` follows it to the end. In the lesson: every step passed (`review in 32s`), three inline comments (line 7 high convention, line 17 high convention, line 9 low bug), each with its fix and the hidden mark, and the summary `Claude review: 3 new, 0 still open, 0 fixed.` On GitHub's site the comments sit on their lines in the pull request's **Files changed** tab.

### 4. Push a fix, review again

You play the teammate:

```bash
N=$(gh pr view late-refunds --json number -q .number); git switch late-refunds && git pull -q
code harborline/late_refunds.py
```

Replace the file with the kit's version: it reads the order through `normalize.order()` and lets `check_refund(..., "late_delivery")` decide the refund. Then:

```bash
git commit -am "Use the refund policy for late deliveries" && git push -q
sleep 10; gh run watch --exit-status "$(gh run list -w pr-review.yml -L 1 --json databaseId -q '.[0].databaseId')"
gh pr view $N --comments
git switch main
```

The push is a `synchronize` event, so the review runs again, this time with the three earlier findings in its prompt. In the lesson: `Claude review: 0 new, 0 still open, 3 fixed.` No comment was posted twice.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Make the workflow folder | `mkdir -p .github/workflows` | PowerShell: `New-Item -ItemType Directory -Force .github\workflows` |
| Keep the pull request's number | `N=$(gh pr view late-refunds --json number -q .number)` | PowerShell: `$N = gh pr view late-refunds --json number -q .number`, then use `$N` the same way |
| Wait, then watch the run | `sleep 10; gh run watch ...` | PowerShell: `Start-Sleep 10; gh run watch --exit-status (gh run list -w pr-review.yml -L 1 --json databaseId -q '.[0].databaseId')` |
| The comments command | as in `commands.txt` | Run it in Git Bash or WSL; PowerShell's quoting changes the `--jq` filter |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

The workflow itself always runs on GitHub's Ubuntu runner, whatever your computer is. **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save).

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `gh secret list` | `ANTHROPIC_API_KEY` and when it was updated; never the value |
| `gh pr create` | the pull request's address (number 4 in the lesson; yours will differ) |
| The first run | every step passed, `review in 32s`; its log: `0 earlier: 0 fixed, 0 still open; 3 new (3 inline); 4 turns, $0.0832` |
| The inline comments | `harborline/late_refunds.py:7` high convention, `:17` high convention, `:9` low bug |
| The fix | `[late-refunds 01b4580]`, 1 file changed, 4 insertions, 12 deletions |
| The second run | `review in 22s`; its log: `3 earlier: 3 fixed, 0 still open; 0 new (0 inline); 4 turns, $0.1247` |
| `gh pr view $N --comments` | `Claude review: 3 new, 0 still open, 0 fixed.` then `Claude review: 0 new, 0 still open, 3 fixed.` |

See `expected-output.md` for the exact lines. Model output changes from run to run: compare the shape, not the wording.

## Troubleshooting

- **`gh: command not found`, or `gh` asks you to log in**: install the GitHub CLI and run `gh auth login` once.
- **`gh secret list` asks which repository**: your folder has more than one remote. Pass `-R <your-account>/harborline`, as the lesson does.
- **The run fails at `python3 ci/review.py` with an authentication error**: the secret is missing or wrong. `gh secret list` must show `ANTHROPIC_API_KEY`; set it again with `gh secret set ANTHROPIC_API_KEY -R <your-account>/harborline`.
- **`Resource not accessible by integration`**: the job's token can't post the review. The workflow needs `pull-requests: write` in its `permissions`.
- **No run starts after a push**: check that the workflow is on the pull request's base branch (`main`) and that `types` lists `synchronize`. `gh run list -w pr-review.yml` shows the runs.
- **`gh run watch` shows an older run**: GitHub hadn't started the new one yet. Wait a few seconds and run the watch command again.
- **A finding isn't an inline comment**: its line isn't in the diff, and GitHub accepts comments only on lines the diff shows. It's listed in the summary instead.
- **The second run reports a finding as still open**: read it against the diff; the model judged the code still has it. Fix it and push again, or answer it on the pull request.
- **Each run costs more than you expected**: no `--model` is passed, so Claude Code's default model runs. Add `"--model", "haiku"` to the `claude` command in `review()`.

## Key terms

- **Workflow trigger:** the events that start the job; here `opened` and `synchronize`.
- **Repository secret:** a value stored with the repository and read as `secrets.NAME`, never written in the code.
- **Inline comment:** a review comment on one line of the diff.
- **Prior findings:** what the review already posted, passed back so it isn't repeated.
- **`still_open`:** an earlier finding that the new code still has.

Claude Code and GitHub change often. If an option or a message doesn't match what you see, follow the official pages: Claude Code GitHub Actions (https://code.claude.com/docs/en/github-actions), Run Claude Code programmatically (https://code.claude.com/docs/en/headless) and the GitHub CLI manual (https://cli.github.com/manual/).
