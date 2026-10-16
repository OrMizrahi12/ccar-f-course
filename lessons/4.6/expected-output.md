# Expected output: Lesson 4.6, Errors across agents

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. Long lines are wrapped by the terminal, so they're shown here unwrapped.

**What will differ on yours:** every time, how the coordinator splits the work, the prompts it writes, the searches (and so which of them time out), the retries, the pages read, the answer and its gap line, the time saved, the cost, and your commit IDs. Claude's choices vary from run to run. Each section says what should match.

## Step 1: A timeout with context

```text
(.venv) $ git status --short
(.venv) $ code research/tools.py
```

`git status --short` prints nothing: a clean tree after Lesson 4.5. Then change `research/tools.py` in the editor (README.md, step 1) and save it. It ends up 135 lines long.

## Step 2: Recover, report, carry on

```text
(.venv) $ code research/agents.py
(.venv) $ code research/coordinator.py
```

Change both files in the editor (README.md, step 2) and save them. `agents.py` ends up 49 lines long, `coordinator.py` 151.

## Step 3: Failure versus empty, tested

```text
(.venv) $ code tests/test_research_tools.py
(.venv) $ clear; python -m pytest -q tests/test_research_tools.py
......                                                                          [100%]
6 passed in 1.17s
(.venv) $ python -m pytest -q
............................................................................... [ 79%]
.....................                                                           [100%]
100 passed in 3.87s
```

**Should match:** `6 passed` (Lesson 4.5's four tests and the two new ones) and `100 passed` for the whole suite. The times will differ.

## Step 4: One run

The lesson shows the run's lines in the terminal; some of the answer scrolled past and isn't shown here.

```text
(.venv) $ clear; python -m research.coordinator "Should Harborline charge customers a fee for return shipping, and would a fee cut return fraud?" 2> runs/research.log
  6.0s -> searcher 1: Find web sources (saved copy, URLs end in .example) on how c...
  6.9s -> searcher 2: Find web sources (saved copy, URLs end in .example) on (a) c...
  7.3s    [searcher 1] search_web return shipping fee effect on conversion rate
  7.5s    [searcher 1] search_web return fee customer churn study
  7.7s    [searcher 1] search_web return policy strictness return rates study
  7.9s    [searcher 1] search_web wardrobing return fraud prevention
  7.9s  ! [searcher 1] search_web failed: timeout
  8.0s -> searcher 3: Find Harborline's own internal documents (URLs start with ha...
  8.0s    [searcher 1] search_web serial returners return fees abuse
  8.0s  ! [searcher 1] search_web failed: timeout
  8.4s    [searcher 2] search_web online retailer return shipping fee policy home goods
  8.6s    [searcher 2] search_web ecommerce paid returns policy survey
  8.8s    [searcher 2] search_web average cost of product return retailers
  9.0s    [searcher 2] search_web online return rate percent of orders returned
  9.0s    [searcher 3] search_web harborline returns
  9.2s    [searcher 3] search_web harborline return fee
  9.2s    [searcher 1] search_web wardrobing return fraud prevention
  9.2s  ! [searcher 1] search_web failed: timeout
  9.3s    [searcher 1] search_web serial returners return fees abuse
  9.3s  ! [searcher 1] search_web failed: timeout
  9.3s    [searcher 3] search_web harborline return rate
  9.4s    [searcher 3] search_web harborline refunds
 11.1s    [searcher 3] search_web harborline return fraud
 11.2s  ! [searcher 3] search_web failed: timeout
 11.2s    [searcher 3] search_web harborline return shipping cost
 11.3s    [searcher 2] search_web cost to process a return per item
 11.3s    [searcher 3] search_web harborline customer feedback returns
 12.4s    [searcher 3] search_web harborline return fraud
 12.4s  ! [searcher 3] search_web failed: timeout
 16.3s <- searcher 1 done (10.3s)
 16.5s <- searcher 2 done (9.6s)
 17.8s <- searcher 3 done (9.8s)
 21.5s -> analyst 1: Read these sources with load_document and return findings as...
 22.8s    [analyst 1] load_document harborline://internal/finance-memo-free-returns
 22.9s    [analyst 1] load_document harborline://internal/q2-2026-returns-report
 23.1s    [analyst 1] load_document harborline://internal/customer-survey-aug-2026
 23.3s    [analyst 1] load_document https://retail-signals.example/2026/05/charging-for-returns
 23.5s    [analyst 1] load_document https://homeretaildaily.example/2026/08/pinecrest-return-fee
 23.7s    [analyst 1] load_document https://northgate-lpc.example/research/return-fraud-2025
 23.9s    [analyst 1] load_document https://meridian-institute.example/reports/returns-benchmark-2025
 24.0s    [analyst 1] load_document https://retail-signals.example/2026/03/return-rates-new-high
 24.2s    [analyst 1] load_document https://lakeshore-business.example/papers/return-leniency-clv
 24.4s    [analyst 1] load_document https://consumerpulse.example/insights/bracketing-2025
 64.0s <- analyst 1 done (42.4s)
 77.1s -> synthesizer 1: Question from Harborline managers: Should Harborline charge ...
 79.7s    [synthesizer 1] verify_fact Cost per return: $11.40 on average, including $7.10 return shipping, $2.60 handling and inspection, and $1.70 items written off. harborline://internal/q2-2026-returns-report
 79.9s    [synthesizer 1] verify_fact Q2 2026 return rate was 19.2% by order value and 13.1% by units. harborline://internal/q2-2026-returns-report
 80.4s    [synthesizer 1] verify_fact Return volume fell a median 18% over six months after retailers added a return fee, compared with matched non-fee retailers. https://retail-signals.example/2026/05/charging-for-returns
 80.7s    [synthesizer 1] verify_fact With a $4.95 return fee, 27% of customers would shop less often and 9% would stop shopping. harborline://internal/customer-survey-aug-2026
 81.1s    [synthesizer 1] verify_fact Loss-prevention managers estimate 9.4% of online returns in 2025 involved fraud or policy abuse, up from 8.1% in 2024. https://northgate-lpc.example/research/return-fraud-2025
 81.5s    [synthesizer 1] verify_fact Merchants with free return shipping on every order had a return rate 3.4 points higher than fee-charging merchants after controlling for category. https://meridian-institute.example/reports/returns-benchmark-2025
 81.8s    [synthesizer 1] verify_fact Harborline Finance modeled a $4.95 fee on 'changed my mind' returns; if volume falls 15%, fee plus lower volume save $0.6M to $0.8M a year. harborline://internal/finance-memo-free-returns
 95.1s <- synthesizer 1 done (18.0s)

**Short answer:** Harborline can reasonably test a fee on "changed my mind" returns, but the evidence doesn't show a fee would cut return fraud. Treat the fee as a revenue and return-volume question, not a fraud fix.

- **Cost of returns:** Harborline's average cost per return in Q2 2026 was $11.40, of which $7.10 is return shipping, $2.60 handling and inspection, and $1.70 items written off (Q2 2026 Returns Report, harborline://internal/q2-2026-returns-report). ...
- **Harborline's proposed fee:** Finance modeled $4.95 on "changed my mind" returns, which is below the $7.10 shipping cost. ...
- **Customer reaction:** In Harborline's August 2026 email survey (1,148 customers), 27% said a $4.95 fee would make them shop less and 9% said they would stop. ...
- **Competitors:** 40 retailers that added $3.95 to $5.95 fees saw a median 18% drop in return volume over six months, against matched non-fee retailers. ...
- **Fraud:** No source tests whether fees reduce fraud or serial returns. Loss-prevention managers estimate 9.4% of 2025 online returns involved fraud or abuse, up from 8.1%. ... This is perception only (Northgate, 2025-12-10, https://northgate-lpc.example/research/return-fraud-2025).
- **Where sources disagree:**
  - Return rates aren't comparable. ...
  - The fee effect differs. ...
- **Gaps:** Searches for wardrobing and serial-returner evidence and for Harborline return-fraud documents timed out, so Harborline's own fraud rate is unknown. Harborline has no data on actual churn or conversion after a fee.

**Recommendation:** Run a one-category test of a fee on "changed my mind" returns, with damaged and wrong items exempt. Measure return volume, repeat purchases, and fraud indicators against a control group, and track the repeat-purchase loss the model leaves out. ...

subagents: searcher 1, searcher 2, searcher 3, analyst 1, synthesizer 1
subagents worked 90s in 72s of clock time: running together saved 18s
102s in all · 6 turns · $0.0219
```

**Should match:**

- Every search whose query contains "fraud" or "abuse" fails with a `!` line: `! [searcher N] search_web failed: timeout`. Every other search works.
- A failed query usually comes back a moment later (the searcher following the error's first alternative, retry once), and fails again: the timeout is simulated, so retries never help. A searcher may also reword the query and search the rest of the question.
- The run doesn't stop: the searchers finish (`<- searcher N done`), and the analyst and the synthesizer still do their work.
- The answer says what isn't covered, and why, in a line that starts "Not covered:" (or, as in the lesson, under another heading such as "Gaps:"). It never says that no evidence on fraud exists because a search returned nothing.

**May differ:** how many searchers there are and which one gets the fraud question, how many queries hit the slow topic, whether a reworded query finds more, which sources the analyst reads, and what the gap line says. In a practice run before filming, the fraud searcher found the loss-prevention survey with a reworded query ("wardrobing retail returns"), and the answer's line started "Not covered:".

## Step 5: Commit

```text
(.venv) $ clear; git status --short
 M research/agents.py
 M research/coordinator.py
 M research/tools.py
 M tests/test_research_tools.py
(.venv) $ git add research tests
(.venv) $ git commit -m "Lesson 4.6: a timeout that says what failed and what came back, recovery in the searcher, and the gap in the answer"
[main fe332ab] Lesson 4.6: a timeout that says what failed and what came back, recovery in the searcher, and the gap in the answer
 4 files changed, 63 insertions(+), 7 deletions(-)
(.venv) $ git push
...
   be0c870..fe332ab  main -> main
```

**Should match:** `4 files changed, 63 insertions(+), 7 deletions(-)` if your files match the kit's. Your commit IDs will differ.
