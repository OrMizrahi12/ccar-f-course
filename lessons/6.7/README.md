# Student kit: Lesson 6.7, Module 6 exam traps and recap

Claude Certified Architect – Foundations (CCAR-F) · Module 6: Claude Code in CI/CD · Lesson 6.7

This lesson adds no code. It goes back over Module 6 using the module's own runs. By the end of it you can:

1. Spot Module 6's eight classic traps
2. Ask what makes the pipeline sure
3. Hold Module 6 on one page

## What's in the kit

| File | What it is |
|---|---|
| `module-6.md` | The Module 6 cheat sheet: one row per lesson, plus the eight traps and why each one is wrong |

## The question that settles most of them

**What does the pipeline need to be sure of, and what makes it sure?**

Not a stronger word in the prompt, but a mechanism: a flag that exists (`claude -p`), a schema (`--json-schema`, `structured_output`), the earlier findings (`new` / `still_open`), explicit criteria (report, skip, severity by example), examples (one root cause, one finding), a separate pass (per file, then cross-file), an independent check (verdict and confidence), and the tests you already have (`why_new`).

## The eight traps

| Trap | It sounds like | The fix it hides |
|---|---|---|
| Invent a flag | "Set CLAUDE_HEADLESS=true." "Add --batch." "Use --non-interactive." | `claude -p` (`--print`), with `--allowedTools` and `dontAsk` set up front. The Message Batches API is for a big job that can wait up to a day. |
| Assume the context | "CI ignores CLAUDE.md." "--bare is just a faster -p." | Plain `-p` loads `CLAUDE.md` and its imports; `--bare` loads none of it. Under `--bare`, pass the context in. |
| Parse the prose | "Grep the review for 'bug'." "Ask for a table and split the rows." | `--output-format json` + `--json-schema`; read `structured_output`. |
| Say it all again | "Re-run the full review on every push." "Review only when the PR opens." "Delete the old comments first." | Pass the earlier findings; mark each `new` or `still_open`; post only the new. |
| Just be careful | "Be conservative." "Only high-confidence issues." "Be thorough." | Categories to report and to skip, severity defined by examples, a switch for a noisy category. |
| Ask for consistency | "Be consistent." "Temperature down." "Merge nearby findings in a script." | Two to four examples: the exact finding, one root cause = one finding, cases where the answer is None. |
| One bigger pass | "A bigger context window." "A consensus of three runs." "The author reviews its own change." | A pass per file, one cross-file pass, and an independent check of every finding, with a confidence for routing. |
| More tests | "More tests per module." "Delete the failing generated tests." "Conventions in ~/.claude." | Standards in the project `CLAUDE.md`, the existing tests in the prompt, `why_new` for each test, run what you generate, log dismissals by pattern. |

## Where the runs come from

Every run in the lesson was recorded in an earlier lesson. To repeat one, use that lesson's kit:

- **Lesson 6.1** (traps 1 to 3): the diff piped into `claude -p` answered, then `exit code 0`; plain `-p` quoted the money and dates conventions, `--bare` said "There are none.", and `--bare` with `--append-system-prompt-file CLAUDE.md` got only the two `@docs/conventions/...` lines; the review with `--json-schema` returned four findings in `structured_output`, and `jq` showed 3 turns and a cost under half a cent.
- **Lesson 6.2** (trap 4): `ci/review.py`'s prompt lists the earlier findings (still in the code: `still_open`; fixed: left out; the rest: `new`), and `ci/findings.schema.json` makes `status` required, with `"enum": ["new", "still_open"]`.
- **Lesson 6.3** (trap 5): with "be conservative", `scripts/refund_totals.py:17` was a medium bug, and a third run added a low finding guessing about the seed data; with explicit criteria, line 17 came back high (and the guess returned once, at medium).
- **Lesson 6.4** (trap 6): the same diff and criteria gave 3 findings, then 4; with four examples, 2 findings, then the same 2.
- **Lesson 6.5** (trap 7): `4 findings from 4 passes`; `scripts/weekly_fees.py:12 high bug (found by cross-file; confirmed 0.97)`; `harborline/fees.py:12 low convention (... confirmed 0.60)`, under the 0.8 threshold.
- **Lesson 6.6** (trap 8): `ci/testgen.py` wrote five tests, each with a `why_new` line, `5 passed`; the full suite `139 passed`; `ci/review_log.py report`: `raw-order-dates-read  1 of 1 dismissed`.

Each result comes from one run on the day it was recorded, so yours will differ. This lesson made no API calls and cost nothing.

## Next

1. **Lab 6: the CI review, hardened**, in the course materials under `labs/L6/`: a payload you can test without posting, a safety net for findings marked still open, a switch for the patterns developers dismiss, and tests generated for one more module that you keep only after reading them, checked by the self-check tests.
2. **The Module 6 quiz**: 14 questions, three of them from earlier modules. This lesson has no quick check, because the quiz takes its place.

## Sources (checked 2026-10-17)

- Run Claude Code programmatically: https://code.claude.com/docs/en/headless
- Claude Code GitHub Actions: https://code.claude.com/docs/en/github-actions
- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Best practices for Claude Code: https://code.claude.com/docs/en/best-practices
- Claude Certified Architect – Foundations Exam Guide: Domains 3 and 4, Task Statements 3.6, 4.1, 4.2, 4.4, 4.6 and 1.6, Scenario 5

Models and tools change. Always confirm current details in the official docs.
