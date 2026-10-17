# Expected output: Lesson 6.4, Few-shot for consistent output

What each step showed in the lesson (Claude Code headless with Haiku 5.5 on the API, Python 3.12, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. The reviewer's wording, its findings and its costs change from run to run; compare the shape of the output (how many findings, which lines, which categories and severities), not the exact text. Long lines are shown unwrapped.

## The starting point

`git status --short` prints nothing (the tree is clean), and `source .env` prints nothing either.

```text
$ git log --oneline -1 b065274
b065274 (origin/late-refunds, late-refunds) Late-delivery refund estimates for the weekly report
```

Your hash will differ. The commit adds `harborline/late_refunds.py` (17 lines): raw date parsing on lines 7 and 8, a subtraction on line 9, and a refund computed by hand on line 17.

## Step 1: measure the drift

Run 1, with Lesson 6.3's criteria:

```text
$ python ci/review.py --local main...b065274
harborline/late_refunds.py:17 high convention: late_refund computes the refund by hand (10% per day, capped at total, rounded) instead of using policy.check_refund, which docs/conventions/money.md requires. The weekly report gets money figures that bypass the policy.
harborline/late_refunds.py:7 medium convention: days_late parses promised_by and delivered_at directly with datetime.fromisoformat. docs/conventions/dates.md says to read orders through harborline.normalize and never parse raw date fields. Some orders store Unix seconds, so fromisoformat raises on real data.
harborline/late_refunds.py:9 medium bug: Subtracting a naive datetime (plain date such as 2026-10-01) from an offset-aware one (ISO 8601 with offset) raises TypeError. Orders mix both formats, so this crashes on real data.
3 findings; 4 turns, $0.0032
```

Run 2, with nothing changed:

```text
$ python ci/review.py --local main...b065274
harborline/late_refunds.py:17 high convention: late_refund computes the refund by hand (10% of total per day late, capped at total). docs/conventions/money.md says refund amounts come from policy.check_refund and must never be computed by hand. This figure goes into the weekly report.
harborline/late_refunds.py:7 medium convention: days_late parses order["promised_by"] with datetime.fromisoformat. docs/conventions/dates.md says orders mix Unix seconds, ISO 8601 with offsets and plain dates, and that raw date fields must never be parsed; read them through harborline.normalize. Line 8 does the same for delivered_at.
harborline/late_refunds.py:7 medium bug: fromisoformat raises ValueError on orders whose promised_by (or delivered_at, line 8) is Unix seconds, which the dates doc says real orders contain. The late-refund report crashes on those orders.
harborline/late_refunds.py:9 medium bug: The subtraction raises TypeError when one date is a plain date or naive ISO string and the other has an offset, because naive and aware datetimes cannot be subtracted. The dates doc says orders mix these formats.
4 findings; 2 turns, $0.0023
```

Three findings, then four: the raw-date problem came back as two findings in run 1 (line 7 convention, line 9 bug) and as three in run 2 (line 7 twice, once as a convention break and once as a bug, and line 9). Your runs may drift differently, or happen to agree; run it a third time if they do.

## Step 2: add four examples

Nothing runs. `review.md` gains 18 lines below the criteria: the rule line, the format line, the `Examples` header and four examples (two with a finding, two answered `None.`).

## Step 3: same diff, same findings

Run A:

```text
$ python ci/review.py --local main...b065274
harborline/late_refunds.py:17 high convention: Computes the late refund by hand (10% of total per day), which docs/conventions/money.md forbids: refund amounts must come from policy.check_refund.
harborline/late_refunds.py:7 medium convention: Parses the raw promised_by and delivered_at fields with fromisoformat, which docs/conventions/dates.md forbids; it crashes on Unix-second dates and fails when offset-aware and naive values are subtracted.
2 findings; 3 turns, $0.0032
```

Run B, with nothing changed:

```text
$ python ci/review.py --local main...b065274
harborline/late_refunds.py:17 high convention: Computes the late refund by hand (10% of total per day late), which docs/conventions/money.md forbids. Refund amounts must come from policy.check_refund, so this figure can reach the weekly report wrong.
harborline/late_refunds.py:7 medium convention: Parses the raw promised_by and delivered_at fields, which docs/conventions/dates.md forbids. datetime.fromisoformat also crashes on orders whose dates are Unix seconds or plain dates.
2 findings; 2 turns, $0.0022
```

The point to check: the same two findings in both runs, on the same lines, with the same categories and severities, and the crash folded into the line-7 convention finding instead of filed beside it. The issue now names the rule file ("which docs/conventions/... forbids"), as the examples show. The wording still differs. Two runs that agree are a measurement, not a proof.

A diff the examples have never seen:

```text
$ python ci/review.py --local main...origin/refund-totals
scripts/refund_totals.py:14 high convention: Reads raw orders from data.orders() and passes them to late_orders, skipping normalize. docs/conventions/dates.md requires reading orders through harborline.normalize; 71 delivered_at values in the seed data carry a -05:00 offset, so as_date can shift an evening delivery to the wrong day and flip the >5-day late rule.
scripts/refund_totals.py:17 high convention: round(sum(...)) rounds the printed total to whole dollars, but docs/conventions/money.md says amounts are rounded to cents only at the end.
2 findings; 7 turns, $0.0066
```

The lines that print cents with `%.2f` are not flagged. The line-14 finding is what this run reported; in other runs the second finding was different (for example, a note about the seed data), so read it as one run's judgment.

`--local` prints the issue, not the fix. The examples still pin the fix's shape for the pull-request comments that `ci/review.py` posts from Lesson 6.2.

## Commit and push

```text
$ git status --short
 M ci/prompts/review.md
$ git add ci/prompts/review.md
$ git commit -m "Lesson 6.4: few-shot examples for one finding per root cause and a fixed format"
[main 69c2202] Lesson 6.4: few-shot examples for one finding per root cause and a fixed format
 1 file changed, 18 insertions(+)
```

`git push` ends with `main -> main`. Your hashes will differ.
