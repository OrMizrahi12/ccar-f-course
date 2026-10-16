# Lab 4: the research pipeline, checked on a hard question

Claude Certified Architect – Foundations (CCAR-F) · Module 4: Multi-Agent Systems: the Research Pipeline · the module checkpoint

In Module 4 you built Harborline's research pipeline with the Agent SDK. A coordinator sends searchers, analysts and a synthesizer out, several at once. Each subagent gets only its role's tools and everything it needs in its prompt. A failed search says what failed instead of coming back empty. The report keeps every claim with its source and shows conflicting figures side by side. Each report is saved as it lands, so a crashed run can resume.

In this lab you run the whole pipeline on a question that hits every one of those cases at once, and you check the report in code instead of by eye. The question asks about return fraud. Searches about fraud and abuse time out in this project (Lesson 4.6's simulated timeout), and the return-rate sources disagree (Lesson 4.7).

You pass the lab when the self-check tests pass and one full run's report passes all four checks:

1. both return-rate figures (Retail Signals Weekly's 24.0% of order value and Meridian's 17.6% of units) are kept, each with its source
2. every claim comes from a known source with a date
3. Meridian's 2023 and 2025 figures aren't filed as a conflict: they're a change over time
4. when tool calls failed during the run, the report says what isn't covered

## What you start from

`starter/` is the `harborline` project exactly as it stands after Lesson 4.8: the Module 1 loop, harborline-mcp from Module 2, the support agent from Module 3, and `research/` from Lessons 4.1 to 4.8 (the coordinator and its subagents, the research tools, provenance, and the run state). If your own project is there too, keep working in it. If not, copy `starter/` to `~/projects/harborline`, create the virtual environment, install `requirements.txt`, and add your `.env` with `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6 show how).

`solution/` is a finished version to compare with when you're done. `tests/` holds the self-check.

## What you change

- `research/coordinator.py`: keep a list of the tool calls that failed, save it with the run, and save the final report.
- `research/state.py`: `finish()` and `report()`, for the final report.
- `research/checker.py`: new. The four checks, run on a saved run.

Keep the subagents' prompts and tools as they are. The run measures what you built in Module 4.

## Steps

### 1. Keep the failures with the run (Lessons 4.6 and 4.8)
Lesson 4.6's coordinator prints a `!` line for every tool call that failed, then forgets it. Keep them. In `main()`, start a `failures` list, and append `"<who> <tool> failed: <failure type>"` each time a result has `is_error`: the line you already print. Pass `failures=failures` to `state.save()` next to `found`, so the manifest holds them.

On resume, start the list from the manifest (`state.manifest(run_id).get("failures", [])`), not from an empty list. Otherwise a resumed run forgets the failures that happened before the crash, and check 4 can't see them.

### 2. Save the final report (Lesson 4.8)
The subagents' reports are saved as they land, but the synthesizer's final report only goes to the screen. In `research/state.py`, add `finish(run_id, report)`, which writes `report.json` next to the manifest, and `report(run_id)`, which reads it back. In the coordinator, call `state.finish()` after `render()` and print where the report went.

### 3. Write the checker (Lessons 4.6 and 4.7)
Create `research/checker.py`:

- `results(report, failures)`: one `(name, passed)` pair per check above. Check 1 looks for a contested topic whose figures include both return-rate URLs. Check 2 is Lesson 4.7's `check(report)` returning no problems. Check 3 fails if any contested topic holds both Meridian URLs (2023 and 2025). Check 4 passes when nothing failed, or when `not_covered` isn't empty.
- `python -m research.checker <run_id>`: read the run's report and its failures, print `PASS` or `FAIL` for each check, how many tool calls failed, and `PASS` or `FAIL` overall.

Keep the source URLs in constants at the top (`S01`, `S02`, `S03` from `data/research/sources.json`), so a test can use them too.

### 4. Run it on the hard question
```bash
python -m research.coordinator "Should Harborline charge customers a fee for return shipping, and would a fee cut return fraud?" 2> runs/research.log
python -m research.checker $(ls research/runs | tail -1)
```

The run takes two to four minutes and costs about $0.03 to $0.05.

In our run, five subagents worked (`searcher 1, searcher 2, analyst 1, searcher 3, synthesizer 1`), seven search calls about fraud timed out and were reported with `!` lines, and the searchers went on with the rest. The report kept three contested topics: the return rate (24.0% of order value from Retail Signals Weekly, 17.6% of units from Meridian, and Harborline's own 19.2% by value and 13.1% by units), the effect of a fee on repeat purchases, and how customers react to a fee. Its `## Not covered` section began with no measured before-and-after study showing that a fee cuts fraud. `provenance: ok`, then all four checks `PASS`, 143 s, $0.0281. Your run will take a different path. If a check fails, read `report.json` and the `!` lines before you change a prompt.

### 5. Crash it on purpose (Lesson 4.8)
Run the same question with `CRASH_AFTER=3` in front of the command, then resume it with `--resume` and the run's ID, and run the checker on that run. The checker should still see the failures from before the crash.

In our practice run, searchers 1 to 3 reported and the run stopped at 18.4 s with five failed searches saved in the manifest. The resumed run started `analyst 1`, `searcher 4` and two synthesizer rounds without repeating the saved searchers. The checker counted 10 failed tool calls, five from before the crash, and all four checks passed (the resumed part: 209 s, $0.0420).

## Check your work

1. Copy `labs/L4/tests/test_lab4.py` into your project's `tests/`, and run the whole suite:
   ```bash
   python -m pytest -q
   ```
   Our solution: `112 passed` (the starter's 107 tests plus the lab's 5). Before your changes, `test_lab4.py` can't even import until `research/checker.py` exists. It needs no key and costs nothing. It covers:
   - a report with both return rates, each with its source, passes every check
   - one return rate alone fails check 1 only
   - Meridian's two years filed as a conflict fail check 3
   - a failed search with no `not_covered` fails check 4, and passes once the gap is named
   - the report and the failures are saved with the run and read back
2. Run the full pipeline once (step 4) and check the checker's last line says `PASS`.

## Compare with the solution

`solution/research/coordinator.py`, `solution/research/state.py` and `solution/research/checker.py` are one way to do it. Other designs pass too. For example, you could save each failure as its own file next to the reports, or have the checker read the failures from the reports themselves.

## Commit

```bash
git add research tests
git commit -m "Lab 4: failures kept with the run, the final report saved, and a checker for the report"
git push
```
