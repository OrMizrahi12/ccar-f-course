# Expected output: Lesson 6.1, Claude Code without a human

What each step showed in the lesson (Claude Code 2.1.301, Haiku 5.5, the API key from `.env`, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. Claude's wording changes from run to run; compare the behavior, not the exact text. Long lines are shown unwrapped.

## Step 1: headless

`git status --short` and `set -a; source .env; set +a` print nothing.

```text
$ git fetch -q && git log --oneline main..origin/late-refunds
b065274 (origin/late-refunds, late-refunds) Late-delivery refund estimates for the weekly report
$ git diff main...origin/late-refunds --stat
 harborline/late_refunds.py | 17 +++++++++++++++++
 1 file changed, 17 insertions(+)
```

Your commit hash differs. The one-sentence question:

```text
$ git diff main...origin/late-refunds | claude -p "In one sentence, what does this change do?"; echo "exit code $?"
⚠ claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set and takes precedence over your claude.ai login · Unset it to load your organization's connectors
It adds `harborline/late_refunds.py`, which estimates a late-delivery refund as 10% of the order total per day past `promised_by`, capped at the total, zero if on time, and rounded to cents.

It also breaks two project conventions: it parses raw date fields instead of going through `harborline.normalize`, and it computes the refund by hand instead of using `policy.check_refund`.
exit code 0
```

The warning appears when you are also signed in to Claude Code; without a sign-in it may not appear. The second paragraph is unasked: it comes from `CLAUDE.md`, which plain `-p` loads. Yours may or may not add it.

## Step 2: a findings schema

`mkdir -p ci` prints nothing; `code ci/findings.schema.json` opens an empty file. The saved file is `harborline/ci/findings.schema.json` in this kit (21 lines).

## Step 3: the review as JSON

The review command prints the warning, then nothing while it runs (the output goes to `/tmp/review.json`), then `exit code 0`. `jq .structured_output /tmp/review.json` printed four findings in the lesson:

```json
{
  "findings": [
    {
      "path": "harborline/late_refunds.py",
      "line": 7,
      "category": "convention",
      "severity": "medium",
      "issue": "days_late parses raw promised_by and delivered_at with datetime.fromisoformat. docs/conventions/dates.md says to read orders through harborline.normalize and never parse raw date fields.",
      "fix": "Get both dates from harborline.normalize instead of parsing the raw fields."
    },
    {
      "path": "harborline/late_refunds.py",
      "line": 8,
      "category": "bug",
      "severity": "high",
      "issue": "Orders mix Unix seconds, ISO 8601 with offsets, and plain dates. fromisoformat raises TypeError on an integer Unix timestamp, and subtracting a naive plain date from an offset-aware datetime also raises TypeError.",
      "fix": "Use harborline.normalize so every date is parsed the same way before subtraction."
    },
    {
      "path": "harborline/late_refunds.py",
      "line": 12,
      "category": "convention",
      "severity": "high",
      "issue": "late_refund computes the refund by hand with a hardcoded 10% rate and cap. docs/conventions/money.md says refund amounts must come from policy.check_refund and never be computed by hand.",
      "fix": "Call policy.check_refund for the late-delivery refund amount and move the 10% rate and cap into the policy."
    },
    {
      "path": "harborline/late_refunds.py",
      "line": 9,
      "category": "bug",
      "severity": "low",
      "issue": "timedelta.days floors partial days, so an order 1 day 23 hours late counts as 1 day. This changes the refund amount and is not documented.",
      "fix": "Confirm the policy's definition of a late day and implement that rule explicitly, or document the truncation."
    }
  ]
}
```

Your findings will differ in number, order and wording. What stays the same: every finding has the six fields of your schema, `category` and `severity` use only the listed values, and the two convention breaks usually name `docs/conventions/money.md` and `docs/conventions/dates.md`. A schema checks the shape, not the truth: read each finding before you act on it.

```text
$ jq '{turns: .num_turns, cost: .total_cost_usd, session: .session_id}' /tmp/review.json
{
  "turns": 3,
  "cost": 0.004519065,
  "session": "e5fd94a7-119c-4a58-8f6e-e7fb3e6677ed"
}
```

Your turns, cost and session ID differ.

## Step 4: where the rules come from

```text
$ claude -p "$Q"
⚠ claude.ai connectors are disabled because ... (as in step 1)
**Money** (`docs/conventions/money.md`):
- "Amounts are US dollars, rounded to cents only at the end."
- "Refund amounts come from policy.check_refund. Never compute them by hand."

**Dates** (`docs/conventions/dates.md`):
- "Orders mix Unix seconds, ISO 8601 with offsets and plain dates."
- "Read orders through harborline.normalize. Never parse the raw date fields."
$ claude --bare -p "$Q"
There are none. I was given only the working directory (/home/<you>/projects/harborline) and the date.
$ claude --bare -p "$Q" --append-system-prompt-file CLAUDE.md
- `@docs/conventions/money.md`
- `@docs/conventions/dates.md`
```

The bare runs print no connectors warning: bare mode never reads your sign-in. The last answer shows only the two import lines: the file's text arrived, but the `@` imports weren't expanded, so the rules themselves didn't.

```text
$ git status --short
?? ci/
$ git add ci/findings.schema.json
$ git commit -m "Lesson 6.1: ci/findings.schema.json for headless reviews"
[main 8c583fc] Lesson 6.1: ci/findings.schema.json for headless reviews
 1 file changed, 21 insertions(+)
 create mode 100644 ci/findings.schema.json
$ git push
...
   768220a..8c583fc  main -> main
```

Your hashes differ.
