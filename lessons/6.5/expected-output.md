# Expected output: Lesson 6.5, Independent and multi-pass review

What each step showed in the lesson (Claude Code headless with Haiku 5.5 on the API, Python 3.12, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. The reviewer's wording, its findings, which pass finds what, the confidences and the costs change from run to run; compare the behavior, not the exact text. Long lines are shown unwrapped.

## Step 1: passes and a checker

`git status --short` prints nothing (the tree is clean). `review.py`, `verify.schema.json` and `review_config.json` are edited and saved; nothing runs yet.

## Step 2: the bug, for real

`source .env` prints nothing.

```text
$ git fetch -q && git log --oneline main..origin/weekly-fees
b6e1856 (origin/weekly-fees) Weekly report of shipping fees owed, per customer
$ git --no-pager diff main...origin/weekly-fees --stat
 harborline/fees.py     | 14 ++++++++++++++
 scripts/weekly_fees.py | 17 +++++++++++++++++
 2 files changed, 31 insertions(+)
$ git switch -q --detach origin/weekly-fees && python -m scripts.weekly_fees; git switch -q main
C-1043  $695.00
C-1008  $695.00
total  $1,390.00
```

Your commit hash will differ. Each fee is really $6.95: `fees.py` returns integer cents (695), and `weekly_fees.py` prints them with a dollar sign and no division by 100.

## Step 3: multi-pass review

```text
$ python ci/review.py --local main...origin/weekly-fees
harborline/fees.py:9 low convention (found by harborline/fees.py; confirmed 0.85): Reads the raw orders from data.orders(), not through normalize, which docs/conventions/dates.md requires. It works on today's Unix-second and ISO dates only because policy.as_date handles both; a partner-format date such as '10/08/2026' would crash fromisoformat.
harborline/fees.py:12 low convention (found by harborline/fees.py; confirmed 0.60): Rounds each order to cents before summing, but docs/conventions/money.md says amounts are rounded to cents only at the end. Each refund is already rounded to 2 places by policy, so no cents drift shows on current data.
scripts/weekly_fees.py:12 high bug (found by cross-file; confirmed 0.97): owed_by_customer returns integer cents (harborline/fees.py line 13), but this prints them with a dollar sign and no division by 100, so every amount and the total show 100 times too large.
harborline/fees.py:9 medium convention (found by cross-file; confirmed 0.75): Reads raw orders from data.orders() instead of through harborline.normalize, which docs/conventions/dates.md forbids. Offset dates such as '...-05:00' are cut to their local day by policy.as_date but converted to UTC by normalize.to_utc, so a late-delivery check near midnight can land on the other side of the 5-day rule.
4 findings from 4 passes; 28 turns, $0.0244
```

The run prints nothing while it works (about two minutes here), then everything at once. The points to check:

- **The cents bug is found and confirmed.** Here only the cross-file pass caught it; in our practice runs the per-file pass for `scripts/weekly_fees.py` (which can read `fees.py` with its tools) sometimes caught it too, so it may appear twice, with two `found by` labels.
- **The routing.** The 0.60 finding is below `inline_confidence` (0.8): in CI it goes to the summary comment as "For a person to check (0.60)", not inline.
- **Duplicates.** `fees.py:9` appears twice, from two passes. The checker confirms both when both are true; merging duplicates is a separate step.
- A finding the checker rejects is dropped and never printed, so you may see fewer findings than the passes reported.

## Commit and push

```text
$ git status --short
 M ci/review.py
 M ci/review_config.json
?? ci/verify.schema.json
$ git add ci
$ git commit -m "Lesson 6.5: a pass per file, a cross-file pass and an independent check with confidence"
[main 40d212f] Lesson 6.5: a pass per file, a cross-file pass and an independent check with confidence
 3 files changed, 68 insertions(+), 13 deletions(-)
 create mode 100644 ci/verify.schema.json
```

`git push` ends with `main -> main`. Your hashes will differ.
