# Expected output: Lesson 6.2, A pull-request review pipeline

What each step showed in the lesson (the GitHub CLI in the VS Code terminal on Ubuntu 24.04; the reviews ran in GitHub Actions with Claude Code's default model), and what will differ on yours. The findings, their wording, the run times and the costs change from run to run; compare the shape of the output (how many findings, which lines, new or still open, what the summary counts), not the exact text. Long lines are shown unwrapped. Where the lesson shows its account, yours shows your own.

## The starting point

`git status --short` prints nothing (the tree is clean).

## Step 1 and step 2: the workflow and the script

Nothing prints while you type. Then:

```text
$ git status --short
 M ci/findings.schema.json
?? .github/
?? ci/review.py
$ git add .github ci
$ git commit -m "Lesson 6.2: review every pull request with Claude Code in GitHub Actions"
[main c8fb8c6] Lesson 6.2: review every pull request with Claude Code in GitHub Actions
 3 files changed, 115 insertions(+), 1 deletion(-)
 create mode 100644 .github/workflows/pr-review.yml
 create mode 100644 ci/review.py
```

Your commit hash will differ. `git push` ends with a line like `8c583fc..c8fb8c6  main -> main`.

## Step 3: open the pull request

```text
$ gh repo set-default <your-account>/harborline
✓ Set <your-account>/harborline as the default repository for the current directory
$ gh secret list -R <your-account>/harborline
NAME               UPDATED
ANTHROPIC_API_KEY  about 16 minutes ago
$ gh pr create --base main --head late-refunds --title "Late-delivery refund estimates" --body "Refund estimates for the weekly report."

Creating pull request for late-refunds into main in <your-account>/harborline

https://github.com/<your-account>/harborline/pull/4
$ N=$(gh pr view late-refunds --json number -q .number); echo $N
4
```

The lesson's base was `lesson-6.2`; yours is `main`. Your pull request's number will differ.

```text
$ sleep 10; gh run watch --exit-status "$(gh run list -w pr-review.yml -L 1 --json databaseId -q '.[0].databaseId')"
✓ late-refunds PR review <your-account>/harborline#4 · 39094000789
Triggered via pull_request less than a minute ago

JOBS
✓ review in 32s (ID 117576500597)
  ✓ Set up job
  ✓ Run actions/checkout@v6
  ✓ Run npm install -g @anthropic-ai/claude-code
  ✓ Run python3 ci/review.py 4
  ✓ Post Run actions/checkout@v6
  ✓ Complete job

✓ Run PR review (39094000789) completed with 'success'
```

While the run is in progress the same view refreshes, with a spinner on the running step. GitHub may add an `ANNOTATIONS` block about its runner images; it doesn't affect the review. The `Run python3 ci/review.py` step's log (on GitHub, the run's page) ends with the script's own line:

```text
0 earlier: 0 fixed, 0 still open; 3 new (3 inline); 4 turns, $0.0832
```

The inline comments:

```text
$ gh api repos/{owner}/{repo}/pulls/$N/comments --jq '.[] | "\(.path):\(.line)\n\(.body)\n"'
harborline/late_refunds.py:7
**high · convention**: days_late parses the raw promised_by/delivered_at fields with datetime.fromisoformat, which breaks the dates convention: read orders through harborline.normalize, never parse raw date fields. This causes real crashes. Warehouse orders store Unix seconds (int), so fromisoformat raises TypeError. Partner dates like '10/08/2026 2:30 PM ET' raise ValueError. A plain date such as '2026-10-08' paired with an offset timestamp such as '2026-10-10T14:00:00Z' gives one naive and one aware datetime, so the subtraction on line 9 raises TypeError. An undelivered order (delivered_at None) also raises.

Fix: Pass the order through harborline.normalize.order() first. Better still, drop days_late and let policy.check_refund handle it, because it already reduces both fields to dates with as_date and handles a missing delivered_at.
<!-- harborline-review -->

harborline/late_refunds.py:17
**high · convention**: late_refund works out the refund amount by hand, which breaks the money convention: refund amounts come from policy.check_refund. Its rule also contradicts the real policy. check_refund('late_delivery') refunds only the shipping fee, and only when the delivery is more than 5 days late (LATE_DELIVERY_DAYS). This code pays 10% of the order total for every day late, up to the full total. Example: a $200 order delivered 3 days late shows $60 here, but policy allows $0. At 10 days late this shows $200, but policy allows only the shipping fee. The weekly report would overstate refunds.

Fix: Return policy.check_refund(normalize.order(order), 'late_delivery')['refund']. If the business really wants a new per-day rule, add it to policy.py and data/refund_policy.md rather than this module.
<!-- harborline-review -->

harborline/late_refunds.py:9
**low · bug**: timedelta.days floors the difference. A delivery 23 hours late counts as 0 days late, and one 1 hour early counts as -1. The result depends on time-of-day, not on calendar days, so it won't match policy, which compares dates.

Fix: Compare calendar dates, e.g. policy.as_date on normalized values, or use check_refund, which already does.
<!-- harborline-review -->
```

`gh api` fills in `{owner}` and `{repo}` from the default repository. The mark at the end of each comment is the HTML comment the script adds; on GitHub's site it's hidden. Your findings will differ in number and wording; the two high convention findings (raw dates on line 7, the refund by hand on line 17) are the ones the late-refunds code is built to show.

```text
$ gh pr view $N --comments
Late-delivery refund estimates <your-account>/harborline#4
Open • <you> wants to merge 1 commit into main from late-refunds • about 2 minutes ago
+17 -0 • ✓ Checks passing
Reviewers: github-actions (Commented)

  Refund estimates for the weekly report.

github-actions commented • 1m • Newest comment

  Claude review: 3 new, 0 still open, 0 fixed.

View this pull request on GitHub: https://github.com/<your-account>/harborline/pull/4
```

## Step 4: push a fix, review again

```text
$ N=$(gh pr view late-refunds --json number -q .number); git switch late-refunds && git pull -q
Switched to branch 'late-refunds'
Your branch is up to date with 'origin/late-refunds'.
$ git commit -am "Use the refund policy for late deliveries" && git push -q
[late-refunds 01b4580] Use the refund policy for late deliveries
 1 file changed, 4 insertions(+), 12 deletions(-)
```

The watch shows a second run, triggered by the push (`synchronize`); in the lesson `review in 22s`, every step passed. Its log line:

```text
3 earlier: 3 fixed, 0 still open; 0 new (0 inline); 4 turns, $0.1247
```

```text
$ gh pr view $N --comments
Late-delivery refund estimates <your-account>/harborline#4
Open • <you> wants to merge 2 commits into main from late-refunds • about 6 minutes ago
+9 -0 • ✓ Checks passing
Reviewers: github-actions (Commented)

  Refund estimates for the weekly report.

github-actions commented • 5m

  Claude review: 3 new, 0 still open, 0 fixed.

github-actions commented • 0m • Newest comment

  Claude review: 0 new, 0 still open, 3 fixed.

View this pull request on GitHub: https://github.com/<your-account>/harborline/pull/4
```

If your second review reports something still open, or a new finding, read it against the diff: that's the reviewer's judgment, and the summary lists it so nothing is posted twice. `git switch main` takes you back.
