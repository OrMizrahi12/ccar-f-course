# Expected output: Lesson 6.6, Test generation that adds value

What each step showed in the lesson (Claude Code headless with Haiku 5.5 on the API, Python 3.12, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. The generated tests, the review findings, their wording and their costs change from run to run; compare the shape of the output (how many tests, what each `why_new` claims, which lines and patterns the findings name), not the exact text. Long lines are shown unwrapped.

## The starting point

`git status --short` prints nothing (the tree is clean).

```text
$ grep -l normalize tests/*.py
tests/test_partner_dates.py
```

One file mentions the module: those are the existing tests that `ci/testgen.py` hands to Claude.

## Step 1: standards and a generator

Nothing prints. `CLAUDE.md` gets a `## Testing` section of five lines below `## Conventions`, and `ci/testgen.py` is new (56 lines). Both are in this kit.

## Step 2: five new tests

`source .env` prints nothing. The run takes about half a minute and prints nothing while it works.

```text
$ python ci/testgen.py harborline/normalize.py
test_unix_seconds_become_utc_iso_string: No existing test passes a number to to_utc. This covers the Unix-seconds input shape (int), which takes the fromtimestamp branch.
test_unix_seconds_with_a_fraction_drop_the_fraction: No existing test passes a float. This covers the edge where a fractional second is cut off rather than rounded up, which the output format cannot show.
test_iso_datetime_with_offset_becomes_utc: Existing tests cover only the partner format. The ISO 8601 branch (the string contains 'T' and no '/') is not tested at all. This checks that a -04:00 offset is converted to UTC.
test_order_maps_numeric_status_code_to_its_name: The existing order test uses only a string status, so the int branch of order() that calls status_name is not covered.
test_order_leaves_the_input_record_unchanged: The existing order test checks only the returned copy. It does not check that the caller's dict keeps its raw dates and numeric status after order() runs.
5 tests in tests/test_normalize_generated.py; $0.0070
.....                                                                    [100%]
5 passed in 0.01s
```

Your tests and their names will differ. The point to check: each `why_new` names a behavior that `tests/test_partner_dates.py` doesn't test, and you can check that claim against the file. The generated file in the lesson is `harborline/tests/test_normalize_generated.py` in this kit (five tests, each a small input built inside the test and one exact expected value).

Run it a second time and it refuses, until you commit or remove the generated file:

```text
$ python ci/testgen.py harborline/normalize.py
tests/test_normalize_generated.py exists: review it and commit or remove it first
```

(Not run in the lesson; this is the guard in `main()`.)

```text
$ python -m pytest -q
................................................................................ [ 56%]
...........................................................                      [100%]
139 passed in 2.42s
```

Your count depends on the tests your repository has: 134 before this lesson, plus five.

## Step 3: what developers dismiss

Nothing prints while you edit the schema, `ci/review.py` and `ci/review_log.py`. Each review now appends its findings to `runs/review_log.jsonl`.

```text
$ python ci/review.py --local main...b065274
harborline/late_refunds.py:17 high convention (found by harborline/late_refunds.py; confirmed 0.97): Computes the late refund by hand (10% per day, capped at the total), which docs/conventions/money.md forbids. Refund amounts must come from policy.check_refund.
harborline/late_refunds.py:7 medium convention (found by harborline/late_refunds.py; confirmed 0.95): Parses the raw promised_by and delivered_at fields with fromisoformat, which docs/conventions/dates.md forbids. It crashes on Unix-second dates and raises TypeError when one date is naive and the other has an offset.
2 findings from 2 passes; 9 turns, $0.0094
```

```text
$ python ci/review.py --local main...origin/refund-totals
scripts/refund_totals.py:17 high convention (found by scripts/refund_totals.py; confirmed 0.93): The total line rounds the sum to whole dollars with round(), so a $13.90 total prints as 14 while the per-customer lines show cents. docs/conventions/money.md says amounts are rounded to cents only at the end.
1 findings from 2 passes; 5 turns, $0.0044
```

```text
$ python ci/review.py --local main...origin/weekly-fees
harborline/fees.py:9 medium convention (found by harborline/fees.py; confirmed 0.70): Reads orders straight from data.orders() and passes them to policy.check_refund, which parses the raw date fields; docs/conventions/dates.md says orders must be read through harborline.normalize. Raw partner-format or non-ISO dates would make as_date raise and crash the fee total.
scripts/weekly_fees.py:12 high bug (found by cross-file; confirmed 0.95): owed_by_customer() returns amounts in cents (harborline/fees.py multiplies the dollar refund by 100), but this line formats them with a $ sign as if they were dollars, so every customer's fee and the total on line 13 are 100 times too large.
2 findings from 4 passes; 19 turns, $0.0143
```

```text
$ python ci/review_log.py
 1. refund-by-hand                 harborline/late_refunds.py:17 high
 2. raw-date-parse                 harborline/late_refunds.py:7 medium
 3. money-rounded-to-dollars       scripts/refund_totals.py:17 high
 4. raw-order-dates-read           harborline/fees.py:9 medium
 5. cents-printed-as-dollars       scripts/weekly_fees.py:12 high
```

Look at 2 and 4: the same kind of problem (raw dates read without `normalize`) under two names. Free-text pattern names drift. Your names will differ, and they may drift in other places.

## As the developer: dismiss a finding, then the report

Finding 4 is the one the lesson rejects: the repo's own `scripts/late_deliveries.py` hands `data.orders()` to `policy.check_refund` the same way, `policy.as_date` parses both stored date formats, and at 0.70 it was below the 0.8 `inline_confidence` in `ci/review_config.json`, so in CI it would have gone to a person.

```text
$ python ci/review_log.py dismiss 4
$ python ci/review_log.py
 1. refund-by-hand                 harborline/late_refunds.py:17 high
 2. raw-date-parse                 harborline/late_refunds.py:7 medium
 3. money-rounded-to-dollars       scripts/refund_totals.py:17 high
 4. raw-order-dates-read           harborline/fees.py:9 medium  (dismissed)
 5. cents-printed-as-dollars       scripts/weekly_fees.py:12 high
$ python ci/review_log.py report
refund-by-hand                   0 of 1 dismissed
raw-date-parse                   0 of 1 dismissed
money-rounded-to-dollars         0 of 1 dismissed
raw-order-dates-read             1 of 1 dismissed
cents-printed-as-dollars         0 of 1 dismissed
```

One dismissal shows the mechanism, not a statistic. On a team the log runs over weeks of pull requests, and a pattern that keeps getting dismissed is where you tune the prompt.

## Commit and push

```text
$ git status --short
 M CLAUDE.md
 M ci/findings.schema.json
 M ci/review.py
?? ci/review_log.py
?? ci/testgen.py
?? tests/test_normalize_generated.py
$ git add CLAUDE.md ci tests/test_normalize_generated.py
$ git commit -m "Lesson 6.6: test generation with existing tests as context, and detected_pattern for dismissals"
[main f47c25d] Lesson 6.6: test generation with existing tests as context, and detected_pattern for dismissals
 6 files changed, 137 insertions(+), 1 deletion(-)
 create mode 100644 ci/review_log.py
 create mode 100644 ci/testgen.py
 create mode 100644 tests/test_normalize_generated.py
```

`git push` ends with `main -> main`. `runs/review_log.jsonl` is not listed: `runs/` is in `.gitignore`. Your hashes will differ.
