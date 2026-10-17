# Expected output: Lesson 6.3, Explicit criteria beat "be conservative"

What each step showed in the lesson (Claude Code headless with Haiku 5.5 on the API, Python 3.12, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. The reviewer's wording, its findings and its costs change from run to run; compare the behavior, not the exact text. Long lines are shown unwrapped.

## The teammate's branch

`git status --short` prints nothing (the tree is clean), and `source .env` prints nothing either.

```text
$ git fetch -q && git log --oneline main..origin/refund-totals
8eb2fdd (origin/refund-totals) Refund totals per customer for the weekly report
```

Your commit hash will differ. `git --no-pager diff main...origin/refund-totals` shows one new file, `scripts/refund_totals.py` (21 lines). Line 17:

```text
+    print("total", round(sum(t.values())))
```

## Step 1: criteria in a file

`mkdir` prints nothing. `review.md`, `review_config.json` and the `review.py` edits are typed and saved; nothing runs yet.

## Step 2: measure the vague version

Run 1:

```text
$ python ci/review.py --local main...origin/refund-totals
scripts/refund_totals.py:17 medium bug: The grand total is rounded to whole dollars with round(sum(...)), so the printed total drops the cents. The per-customer lines use %.2f, and docs/conventions/money.md says amounts round to cents only at the end.
1 findings; 3 turns, $0.0033
```

Run 2, with nothing changed:

```text
$ python ci/review.py --local main...origin/refund-totals
scripts/refund_totals.py:17 medium bug: The total line calls round(sum(...)), which rounds the total to whole dollars. The per-customer lines show cents, and docs/conventions/money.md says amounts round to cents only at the end. A total such as $412.50 prints as 412 or 413.
1 findings; 3 turns, $0.0026
```

The run prints nothing while it works (10 to 20 seconds), then everything at once. Here the two runs happened to agree. In our practice runs of the same prompt, they didn't: the same line was filed once as a convention break and once as a bug, and a speculative extra finding came and went.

## Step 3: switch off a noisy category

With `{"disabled_categories": ["style"]}`:

```text
$ python ci/review.py --local main...origin/refund-totals
scripts/refund_totals.py:17 medium bug: The grand total is rounded to whole dollars with round(sum(...)), so it prints e.g. "total 14" for $13.90. The per-customer lines use cents and docs/conventions/money.md says amounts are rounded to cents only at the end.
scripts/refund_totals.py:14 low bug: The script is named refund_totals and labels its output as totals, but it sums shipping fees owed from the seed data via late_orders. scripts/late_deliveries.py's docstring warns that the seed file does not record refunds already issued through the Harborline tools, so these totals can count orders that were already paid.
2 findings; 3 turns, $0.0033
```

No finding in these runs was filed as style, so the switch hid nothing here. The line-14 finding is a guess about the data, not a problem in the diff.

## Step 4: explicit criteria

Run 1:

```text
$ python ci/review.py --local main...origin/refund-totals
scripts/refund_totals.py:17 high bug: The grand total is rounded to whole dollars with round(sum(t.values())) instead of to cents, so the printed total is wrong (e.g. 18.90 prints as 19) and does not match the per-customer lines, which show cents.
1 findings; 5 turns, $0.0035
```

Run 2:

```text
$ python ci/review.py --local main...origin/refund-totals
scripts/refund_totals.py:17 high bug: The grand total is rounded with round(), which rounds to whole dollars, not cents. Any total with cents is wrong: e.g. fees 6.95 + 6.95 print as "total 14" instead of 13.90. The per-customer lines use %.2f, so the printed total disagrees with them.
scripts/refund_totals.py:14 medium bug: totals() sums the fee for every late order in data/orders.json, but late_deliveries.py's docstring says that seed file does not record refunds already issued through the Harborline tools. The totals can therefore count fees that were already paid, overstating refunds owed in the report.
2 findings; 3 turns, $0.0016
```

The point to check: line 17 is **high** in both runs (wrong money in a report is the high example), and no naming, formatting or style comment appears. The seed-data guess can still come back; Lesson 6.4's examples address that. The category may also move between `bug` and `convention` for the same line.

## Commit and push

```text
$ git status --short
 M ci/review.py
?? ci/prompts/
?? ci/review_config.json
$ git add ci
$ git commit -m "Lesson 6.3: explicit review criteria in ci/prompts/review.md, and a switch for noisy categories"
[main ccc4dec] Lesson 6.3: explicit review criteria in ci/prompts/review.md, and a switch for noisy categories
 3 files changed, 42 insertions(+), 6 deletions(-)
 create mode 100644 ci/prompts/review.md
 create mode 100644 ci/review_config.json
```

`git push` ends with `main -> main`. Your hashes will differ.
