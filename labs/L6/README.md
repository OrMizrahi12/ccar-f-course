# Lab 6: the CI review, hardened

Claude Certified Architect – Foundations (CCAR-F) · Module 6: Claude Code in CI/CD and Review Prompts · the module checkpoint

In Module 6 you put Claude Code into Harborline's CI. `ci/review.py` runs `claude -p` with a JSON schema, so the findings come back as data. A workflow runs it on every pull request and posts inline comments. Explicit criteria and few-shot examples keep the findings precise and consistent. A pass per file, a cross-file pass and an independent check with confidence decide what gets posted. `ci/testgen.py` writes tests that its existing tests don't cover, and `ci/review_log.py` shows which patterns developers dismiss.

In this lab you harden the review where a production pipeline needs it: the review you post becomes a pure function you can test without GitHub, a safety net stops a finding the model wrongly calls "still open" from slipping out of the comments, the dismissal report turns into a switch, and you generate tests for one more module and keep only the ones you've read.

You pass the lab when the self-check tests pass.

## What you start from

`starter/` is the `harborline` project exactly as it stands after Lesson 6.6: everything from Modules 1 to 5, `.github/workflows/pr-review.yml`, and `ci/` with `review.py`, `findings.schema.json`, `verify.schema.json`, `prompts/review.md`, `review_config.json`, `testgen.py` and `review_log.py`. If your own project is there too, keep working in it. If not, copy `starter/` to `~/projects/harborline`, create the virtual environment, install `requirements.txt`, and add your `.env` with `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6 show how).

`solution/` is a finished version to compare with when you're done. `tests/` holds the self-check.

## What you change

- `ci/review.py`: `payload()`, `matches()` and `reconcile()`; `prior_findings()` returns records; `comment()` names the pattern; `skip_patterns` honored.
- `ci/review_config.json`: a `skip_patterns` list.
- `tests/test_policy_generated.py`: new, written by `ci/testgen.py` and reviewed by you.

## Steps

### 1. A payload you can test (Lesson 6.2)
`post()` builds the review and sends it in one go, so the only way to see what it would post is to post it. Move the building into `payload(new, still, fixed, lines)`, which returns the review as a dictionary: new findings Claude is sure of (`inline_confidence`) and that sit on a line the diff shows become inline comments; a sure finding off the diff, an unsure one, and every still-open one are listed in the body; the first line counts new, still open and fixed. `post()` calls `payload()` and sends the result.

While you're there, put the finding's `detected_pattern` into each comment, for example ``**high · bug** `refund-by-hand`: …``. Step 2 reads it back.

### 2. A safety net for "still open" (Lesson 6.2)
On a second push, the prompt lists the earlier findings and Claude marks each one `new` or `still_open`. A model can be wrong about that, and a finding wrongly marked `still_open` is never posted again. Check it in code:
- `prior_findings()` returns `{path, line, text}` records instead of lines of text (format them for the prompt where it's built).
- `matches(finding, earlier)`: same file, and either the line is within 3 of the earlier one (the code moved a little) or the earlier comment names the same pattern.
- `reconcile(findings, prior)`: a `still_open` finding that matches no earlier comment becomes `new`. Call it in `main()` before the findings are split.

### 3. Turn dismissals into a switch (Lesson 6.6)
Run `python ci/review_log.py report` on your own log. A pattern developers dismiss every time is noise. Add `"skip_patterns": []` to `ci/review_config.json`, and drop any finding whose `detected_pattern` is listed there, before the check pass, so the check doesn't spend money on it. Like the `disabled_categories` switch from Lesson 6.3, it's a list in the config, not a rewrite of the prompt: easy to add, easy to take back once the prompt is fixed.

In our Lesson 6.6 run, the report showed `raw-order-dates-read 1 of 1 dismissed`. One dismissal isn't enough to switch a pattern off; look for patterns dismissed again and again across several pull requests.

### 4. Tests for one more module (Lesson 6.6)
Generate tests for the refund policy:
```bash
set -a; source .env; set +a
python ci/testgen.py harborline/policy.py
```
Read every test and its `why_new`. Keep the ones that test behavior the existing tests in `tests/test_policy.py` don't, and delete the rest from the file (or regenerate). Then run the whole suite.

In our practice run (Claude Haiku 5.5, 2026-10-16), testgen wrote 5 tests for $0.0086, and all 5 passed: an unknown reason refused and named, a cancelled order refusing a change-of-mind refund, a SKU that isn't on the order, a damaged item reported after 30 days, and a delivery exactly 5 days late (the rule is "more than 5"). Each `why_new` named the gap in the existing tests, and we kept all five. Your tests will differ; what to check is the same: does each one test something new, and does it test the rule, not the implementation?

### 5. Optional: a real pull request (Lesson 6.2)
To watch the workflow review a real pull request, your GitHub repository needs the `ANTHROPIC_API_KEY` secret. Set it yourself, from your own terminal (it asks for the key; it never shows it):
```bash
gh secret set ANTHROPIC_API_KEY -R YOUR-USERNAME/harborline
```
Then push a branch with a small change and open a pull request. Push a second commit and check the summary: earlier findings are counted as fixed or listed as still open, and nothing is posted twice.

## Check your work

1. Copy `labs/L6/tests/test_lab6.py` into your project's `tests/`, and run the whole suite:
   ```bash
   .venv/bin/python -m pytest -q
   ```
   Our solution: `148 passed` (the starter's 139 tests, the lab's 4, and the 5 generated tests we kept). On the starter, all four lab tests fail. It needs no key and costs nothing: fake findings, fake comments and a fake Claude stand in. It covers:
   - `payload()`: a sure finding on a diff line goes inline with the mark and its pattern; the others are listed; the counts line
   - `reconcile()`: still open within 3 lines, still open by pattern after the code moved, an unknown "still open" turned new
   - `skip_patterns`: a listed pattern is dropped before the check pass ever sees it
   - `tests/test_policy_generated.py` exists and has tests
2. Read your generated tests once more before you commit them.

## Compare with the solution

`solution/` holds one way to do it. Other designs pass too: a different matching rule, or the pattern stored outside the comment text. The tests check behavior through `payload()`, `reconcile()` and `review()`.
