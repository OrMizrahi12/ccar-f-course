# Expected output: Lesson 4.8, State, crash recovery and context budgets

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. The terminal wraps long lines; they're shown here unwrapped.

**What will differ on yours:** the run ID (the time you start the run), the searches, which reports are saved before the crash and which subagent is lost, the URLs, the claims the synthesizer checks, the report, the timings, the cost, and your commit IDs. Claude's choices vary from run to run. Each section says what should match.

## Step 1: State on disk

```text
(.venv) $ git status --short
(.venv) $ code research/state.py
```

`git status --short` prints nothing: a clean tree after Lesson 4.7. Then type `research/state.py` in the editor and save it: 49 lines.

## Step 2: Save, resume, crash

```text
(.venv) $ code research/agents.py
(.venv) $ code research/coordinator.py
```

No output: you change both files in the editor (README.md, step 2) and save them. `agents.py` ends up 55 lines long, `coordinator.py` 192.

## Step 3: State, tested

```text
(.venv) $ code tests/test_state.py
(.venv) $ clear; python -m pytest -q tests/test_state.py
...                                                                      [100%]
3 passed in 0.03s
(.venv) $ python -m pytest -q
........ ... ........                                                    [ 73%]
........ ...                                                             [100%]
107 passed in 5.43s
```

(The rows of dots, one per test, are abridged here.)

**Should match:** `3 passed`. The whole suite's count is the lesson's (107: the 104 from Lesson 4.7 plus these 3) if your repository matches the lesson's; the timings differ.

## Step 4: A crash

```text
(.venv) $ clear; CRASH_AFTER=3 python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs/research.log
run 20261016-045244
 11.2s -> searcher 1: Research question: Should an online home-goods retailer char...
 12.2s -> searcher 2: Research question: Should Harborline (an online home-goods s...
 12.6s    [searcher 1] search_web cost of product returns to retailers
 12.8s    [searcher 1] search_web customer reaction return shipping fees
 12.9s    [searcher 1] search_web home goods retailer return shipping policy
 13.6s    [searcher 2] search_web harborline://internal return rates
 13.7s    [searcher 2] search_web harborline://internal return volumes
 13.9s    [searcher 2] search_web harborline://internal return shipping costs
 14.0s    [searcher 2] search_web harborline://internal refund policy
 14.2s    [searcher 2] search_web harborline://internal return complaints feedback
 14.3s    [searcher 2] search_web harborline://internal return fee experiment
 14.5s    [searcher 1] search_web online retailers charging return shipping fee 2026
 14.6s    [searcher 1] search_web furniture retailer return fee policy
 19.1s <- searcher 2 done (6.9s)
 21.8s <- searcher 1 done (10.6s)
 25.0s -> analyst 1: Question: Should an online home-goods retailer charge custom...
 26.2s    [analyst 1] load_document https://retail-signals.example/2026/05/charging-for-returns
 26.2s -> analyst 2: Question: Should Harborline (online home-goods store) charge...
 26.4s    [analyst 1] load_document https://retail-signals.example/2026/03/return-rates-new-high
 26.6s    [analyst 1] load_document https://meridian-institute.example/reports/returns-benchmark-2025
 26.7s    [analyst 1] load_document https://northgate-lpc.example/research/return-fraud-2025
 26.9s    [analyst 1] load_document https://parcelpostreview.example/2026/07/box-free-returns
 27.1s    [analyst 1] load_document https://homeretaildaily.example/2026/08/pinecrest-return-fee
 27.6s    [analyst 2] load_document harborline://internal/finance-memo-free-returns
 27.8s    [analyst 2] load_document harborline://internal/q2-2026-returns-report
 28.0s    [analyst 2] load_document harborline://internal/customer-survey-aug-2026
 28.1s    [analyst 2] load_document harborline://internal/warehouse-returns-note
 62.9s <- analyst 2 done (36.7s)
 62.9s simulated crash
(.venv) $ ls research/runs/*/
analyst-2.json  manifest.json  searcher-1.json  searcher-2.json
(.venv) $ clear; cat research/runs/*/manifest.json
{
 "question": "Should Harborline charge customers a fee for return shipping?",
 "reports": [
  {
   "name": "searcher 2",
   "file": "searcher-2.json"
  },
  {
   "name": "searcher 1",
   "file": "searcher-1.json"
  },
  {
   "name": "analyst 2",
   "file": "analyst-2.json"
  }
 ],
 "found": [
  "harborline://internal/customer-survey-aug-2026",
  "harborline://internal/finance-memo-free-returns",
  "harborline://internal/q2-2026-returns-report",
  "harborline://internal/warehouse-returns-note",
  "https://consumerpulse.example/insights/bracketing-2025",
  "https://homeretaildaily.example/2026/08/pinecrest-return-fee",
  "https://meridian-institute.example/reports/returns-benchmark-2023",
  "https://meridian-institute.example/reports/returns-benchmark-2025",
  "https://northgate-lpc.example/research/return-fraud-2025",
  "https://parcelpostreview.example/2026/07/box-free-returns",
  "https://retail-signals.example/2026/03/return-rates-new-high",
  "https://retail-signals.example/2026/05/charging-for-returns"
 ]
}
```

**Should match:** `run <run_id>` at the top; the run stops with `simulated crash` right after the third `done` line; the run folder holds `manifest.json` and one file per saved report; the manifest lists the question, the saved reports in the order they finished, and `found`. Which subagent was still working at the crash (here, analyst 1) differs from run to run: it has no report file. No cost line prints: the process stops before the end.

## Step 5: Resume

```text
(.venv) $ clear; python -m research.coordinator --resume $(ls research/runs) 2> runs/research.log
resuming 20261016-045244: 3 reports already saved
  6.4s -> analyst 3: Question: Should Harborline (online home-goods store) charge...
  7.6s    [analyst 3] load_document https://retail-signals.example/2026/03/return-rates-new-high
  7.8s    [analyst 3] load_document https://meridian-institute.example/reports/returns-benchmark-2025
  8.0s    [analyst 3] load_document https://meridian-institute.example/reports/returns-benchmark-2023
  8.1s    [analyst 3] load_document https://northgate-lpc.example/research/return-fraud-2025
  8.3s    [analyst 3] load_document https://parcelpostreview.example/2026/07/box-free-returns
  8.5s    [analyst 3] load_document https://retail-signals.example/2026/05/charging-for-returns
  8.7s    [analyst 3] load_document https://homeretaildaily.example/2026/08/pinecrest-return-fee
 31.9s    [analyst 3] load_document https://retail-signals.example/2026/03/return-rates-new-high
 50.2s <- analyst 3 done (43.8s)
 78.2s -> synthesizer 1: Question: Should Harborline (online home-goods store) charge...
 81.5s    [synthesizer 1] verify_fact Return shipping is forecast to cost Harborline $1.94 million in fiscal year 2026, up from $1.61 million in FY2025. harborline://internal/finance-memo-free-returns
 81.9s    [synthesizer 1] verify_fact We modeled a $4.95 return fee on "changed my mind" returns, waived for damaged, defective or wrong items and for Plus members. harborline://internal/finance-memo-free-returns
 82.2s    [synthesizer 1] verify_fact The return rate for April to June 2026 was 19.2% by order value and 13.1% by units. harborline://internal/q2-2026-returns-report
 82.5s    [synthesizer 1] verify_fact Cost per return: $11.40 on average; Return shipping: $7.10. harborline://internal/q2-2026-returns-report
 82.9s    [synthesizer 1] verify_fact If we added a $4.95 return shipping fee, 27% said they would shop with us less often. 9% said they would stop shopping with us. harborline://internal/customer-survey-aug-2026
 83.3s    [synthesizer 1] verify_fact Return volume fell by a median of 18% at the retailers that added a fee, and the repeat purchase rate fell 6% against 1% for the comparison group. https://retail-signals.example/2026/05/charging-for-returns
 83.7s    [synthesizer 1] verify_fact the average online return rate in the first nine months of 2025 was 17.6% of units sold. https://meridian-institute.example/reports/returns-benchmark-2025
 84.0s    [synthesizer 1] verify_fact the average online return rate reached 24.0% of order value, up from 21.3% the year before. https://retail-signals.example/2026/03/return-rates-new-high
 84.4s    [synthesizer 1] verify_fact merchants offering free return shipping on every order had a return rate 3.4 points higher than merchants that charged a fee, after controlling for category. https://meridian-institute.example/reports/returns-benchmark-2025
 84.7s    [synthesizer 1] verify_fact Pinecrest Home will charge a $5.95 fee for return shipping from September 15. https://homeretaildaily.example/2026/08/pinecrest-return-fee
 85.1s    [synthesizer 1] verify_fact retailers using box-free drop-off networks paid an average of $5.70 to bring back one parcel in the first half of 2026, compared with $8.20 for a prepaid label and a box. https://parcelpostreview.example/2026/07/box-free-returns
 89.4s    [synthesizer 1] verify_fact home goods retailers reported a 15.2% return rate, and 71% of the retailers in the survey now offer free return shipping on every order. https://retail-signals.example/2026/03/return-rates-new-high
 89.7s    [synthesizer 1] verify_fact processing one online return costs between $9 and $14 once shipping, handling and items that can't be resold are counted. https://retail-signals.example/2026/03/return-rates-new-high
 90.1s    [synthesizer 1] verify_fact Managers at retailers with free returns were more likely to report rising abuse (57%) than those at retailers that charge a fee (39%); 9.4% of online returns in 2025 involved fraud or policy abuse. https://northgate-lpc.example/research/return-fraud-2025
137.7s <- synthesizer 1 done (59.5s)

## Answer
Harborline should not add a blanket return fee yet. It should first test a fee on one category, as its Finance memo recommends, with damaged and wrong items kept free (harborline://internal/finance-memo-free-returns, 2026-08-14). The memo's $0.6M to $0.8M annual saving depends on an unsourced 15% volume drop and leaves out lost repeat purchases. By our linear extrapolation from the memo's own 2% case ($0.5M), the saving is gone if repeat purchases fall about 2.4% to 3.2%, and a fee-charging retailer panel saw repeat purchases fall 6% (https://retail-signals.example/2026/05/charging-for-returns, 2026-05-19). The fee is worth keeping only if the test measures actual return volume and repeat purchases and shows repeat losses below that break-even, because the Harborline survey measures stated intent, not behavior.

(The rest of the rendered report, as in Lesson 4.7: the established findings, each with its source and date; the
contested figures, such as the online return rate by order value and by units, in Figure | Source | Method tables;
and what isn't covered. Abridged here.)

provenance: ok

subagents: analyst 3, synthesizer 1
subagents worked 103s in 103s of clock time: running together saved 0s
149s in all · 3 turns · $0.0287
```

**Should match:** the first line, `resuming <run_id>: N reports already saved`, with N the number of report files in the run folder; no subagent whose report was saved runs again, and new subagents are numbered after the saved ones (here `analyst 3`, after the saved `analyst 2`); no `load_document` refusal, because `found` came back from the manifest; the report ends with a `provenance:` line. Only the subagents of this resumed run are listed under `subagents:`.

## Step 6: Commit

```text
(.venv) $ clear; git status --short
 M research/agents.py
 M research/coordinator.py
?? research/state.py
?? tests/test_state.py
(.venv) $ git add research tests
(.venv) $ git commit -m "Lesson 4.8: each report saved to a run manifest as it arrives, and a crashed run resumed from it"
[main 4678fc8] Lesson 4.8: each report saved to a run manifest as it arrives, and a crashed run resumed from it
 4 files changed, 125 insertions(+), 11 deletions(-)
 create mode 100644 research/state.py
 create mode 100644 tests/test_state.py
(.venv) $ git push
...
   c1d9e00..4678fc8  main -> main
```

**Should match:** `4 files changed, 125 insertions(+), 11 deletions(-)` if your files match the kit's. `research/runs/` doesn't appear: the `runs/` line in `.gitignore` covers it. Your commit IDs differ.
