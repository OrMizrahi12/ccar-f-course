# Expected output: Lesson 5.6, Iterative refinement

What each step showed in the lesson (Claude Code v2.1.301, Haiku 5.5, auto mode, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. Claude's wording changes from run to run; compare the behavior, not the exact text.

## Step 1: the interview

`git status --short` prints nothing (the tree is clean). After the interview request, Claude listed the folder, read `harborline/normalize.py`, and answered with questions only, no code:

```text
● Before I write anything, I read harborline/normalize.py. Its to_utc only parses values that contain a T,
  so 10/08/2026 2:30 PM ET would pass through unchanged. These are the questions I need answered:

  1. Day/month order: Is 10/08/2026 October 8 (MM/DD) or August 10 (DD/MM)? ...
  2. Eastern time: Should I convert with the America/New_York zone so EDT and EST are handled automatically? ...
  3. Output format: Keep the current UTC form 2026-10-08T18:30:00Z for all sources? I'd recommend yes.
  4. Other shapes: ... 24-hour times, seconds, a date with no time, or a time with no date?
  5. Date-only values: If a partner value has no time (10/08/2026), should it stay a plain date ...?
  6. Detection: Should I detect the partner format by its pattern, or does the record carry a source or partner field ...?
  7. Fields: Which of placed_at, promised_by and delivered_at does the partner send?
  8. Naive ISO strings: The existing ISO branch treats a string with no offset as the machine's local time.
     Should I fix that too, or leave it out of scope?
  9. Tests and commit: Add tests under tests/ for the new format? Should I commit when done, with the one-line
     message your CLAUDE.md asks for?
```

Your questions will differ in number and wording. Answer the ones you get; the lesson's answer (in `commands.txt`) covers the usual ones and, on purpose, not question 8.

## Step 2: examples and failing tests

Claude wrote `tests/test_partner_dates.py` (40 lines; the rules file `.claude/rules/testing.md` from Lesson 5.3 loaded with it), ran it and the whole suite, and did not touch `normalize.py`:

```text
● I wrote tests/test_partner_dates.py and ran it, and normalize.py is unchanged.
  Result: 5 of the 6 new tests fail, as expected. ...
  - test_partner_date_without_time_stays_a_plain_date: fails because it is not yet handled.
  - test_partner_day_is_never_read_as_month: fails the same way.
  - test_order_converts_partner_dates_in_all_three_fields: fails the same way.
  - test_partner_value_that_does_not_parse_raises_with_the_value: passes, but for the wrong reason.
    Every partner value contains "ET", and the current code treats any string with a "T" as ISO, so it raises
    an error that happens to contain the value. ...
  Two things to decide:
  - The passing error test: Should I tighten it now ...?
  - Naive ISO strings: You didn't answer question 8, so I've left it out of scope.
```

## Step 3: make them pass

```text
● Update(harborline/normalize.py)
  ⎿  Added 23 lines, removed 1 line
● Bash(.venv/bin/python -m pytest -q tests/test_partner_dates.py ...; .venv/bin/python -m pytest -q ...)
  ⎿  6 passed in 0.02s
● I changed harborline/normalize.py so partner dates convert correctly, and all tests pass.
  - New partner tests: tests/test_partner_dates.py passes, 6 of 6.
  - Full suite: 124 passed, 0 failed.
  Partner values are now detected by their / and checked against the exact shape, so anything else raises a
  ValueError that shows the value. The ISO branch is unchanged.
```

Your suite count depends on what you have from earlier lessons; what matters is 0 failed. The code Claude wrote in the lesson is in this kit (`harborline/harborline/normalize.py`, the `PARTNER_SHAPE`, `PARTNER_ZONE` and `partner_to_utc` lines).

## Step 4: one more example, then commit

```text
● Update(tests/test_partner_dates.py)   (test_partner_midnight_in_daylight_time_becomes_utc)
● Bash(.venv/bin/python -m pytest -q tests/test_partner_dates.py 2>&1 | tail -5)
  ⎿  7 passed in 0.01s
● I added the midnight test (10/08/2026 12:00 AM ET → 2026-10-08T04:00:00Z) to tests/test_partner_dates.py.
  The file now has 7 tests, and all pass.
```

Then, after `/exit`:

```text
$ git status --short
 M harborline/normalize.py
?? tests/test_partner_dates.py
$ git add harborline/normalize.py tests/test_partner_dates.py
$ git commit -m "Lesson 5.6: partner dates in normalize.py, test-first from three examples"
[main 0810f6b] Lesson 5.6: partner dates in normalize.py, test-first from three examples
 2 files changed, 67 insertions(+), 1 deletion(-)
 create mode 100644 tests/test_partner_dates.py
$ git push
   3e0ebe2..0810f6b  main -> main
```

Your commit hashes will differ.
