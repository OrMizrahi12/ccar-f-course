# Expected output: Lesson 4.3, Parallel subagents, scope and refinement

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. Long lines are wrapped by the terminal, so they're shown here unwrapped.

**What will differ on yours:** every time, how the coordinator splits the work, the prompts it writes, the searches, the pages read, the answer, the time saved, the cost, and your commit IDs. Claude's choices vary from run to run. Each section says what should match.

## Step 1: A goal, a split, and subagents that start together

```text
(.venv) $ git status --short
(.venv) $ code research/coordinator.py
```

`git status --short` prints nothing: a clean tree after Lesson 4.2. Then change `research/coordinator.py` in the editor (README.md, step 1) and save it. It ends up 129 lines long.

## Step 2: One run, timed

The lesson shows the run's lines in the terminal; the middle of the answer scrolled past and isn't shown here.

```text
(.venv) $ clear; python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs/research.log
  6.9s -> searcher 1: Research question: How do online shoppers react when retaile...
  7.6s -> searcher 2: Research question: What does it cost retailers to process ec...
  8.4s -> searcher 3: Research question: What return shipping fee policies do majo...
  8.6s    [searcher 1] search_web return shipping fee consumer survey online shoppers abandonment
  8.8s    [searcher 1] search_web paid returns A/B test conversion study retailer
  9.0s    [searcher 1] search_web return shipping charge purchase behavior study journal
  9.3s    [searcher 1] search_web Baymard return shipping fee survey
  9.3s    [searcher 2] search_web cost of ecommerce returns per parcel retailers
  9.4s    [searcher 3] search_web free returns policy home goods retailer
  9.5s    [searcher 2] search_web online return rate home goods retail
  9.5s    [searcher 1] search_web paid return shipping fees online retail empirical study
  9.5s    [searcher 3] search_web return shipping fee policy 2026
  9.5s    [searcher 2] search_web return shipping cost restocking cost retailers study
  9.7s    [searcher 3] search_web Target return policy shipping label fee
  9.9s    [searcher 3] search_web Williams Sonoma return policy
 10.0s    [searcher 3] search_web Wayfair returns policy
 12.3s    [searcher 3] search_web Pinecrest Home returns policy
 12.4s    [searcher 3] search_web Crate and Barrel returns
 12.6s    [searcher 3] search_web Amazon returns policy label fee
 15.7s <- searcher 2 done (8.1s)
 16.7s <- searcher 1 done (9.8s)
 17.9s <- searcher 3 done (9.5s)
 20.9s -> analyst 1: Read these pages and return findings as JSON: each claim wit...
 22.2s -> analyst 2: Read these Harborline internal documents and return findings...
 22.5s    [analyst 1] fetch_url https://retail-signals.example/2026/05/charging-for-returns
 22.7s    [analyst 1] fetch_url https://homeretaildaily.example/2026/08/pinecrest-return-fee
 23.0s    [analyst 1] fetch_url https://consumerpulse.example/insights/bracketing-2025
 23.4s    [analyst 1] fetch_url https://meridian-institute.example/reports/returns-benchmark-2025
 23.8s    [analyst 1] fetch_url https://parcelpostreview.example/2026/07/box-free-returns
 24.1s    [analyst 2] fetch_url harborline://internal/customer-survey-aug-2026
 24.1s    [analyst 2] fetch_url harborline://internal/finance-memo-free-returns
 24.2s    [analyst 2] fetch_url harborline://internal/q2-2026-returns-report
 46.9s <- analyst 2 done (24.7s)
 55.3s <- analyst 1 done (34.4s)
 66.8s -> synthesizer 1: Question from Harborline managers: Should Harborline charge ...
 78.1s <- synthesizer 1 done (11.3s)

**Short answer: don't add a blanket return fee yet. If you want to test one, limit it to "changed my mind" returns and keep damaged and wrong-item returns free.**

- **Cost of returns:** In Q2 2026 each Harborline return cost $11.40: $7.10 shipping, $2.60 handling, $1.70 write-offs. Return rate was 19.2% by order value and 13.1% by units, with undefined denominators. Finance forecasts $1.94M in FY2026 return shipping, up from $1.61M. (harborline://internal/q2-2026-returns-report, 2026-07-20; ...
...
- **Sources disagree:** Meridian's transaction data (1,214 merchants) shows free-returns merchants with return rates 3.4 points higher, which cuts against the fee-driven drop above. (meridian-institute.example/reports/returns-benchmark-2025, 2025-11-04) Harborline's 19.2% and Meridian's 17.6% use different metrics, and Retail Signals' 24.0% is a third basis, so don't average them.
- **Recommendation:** Run a test: charge on "changed my mind" returns only, in one category, against a holdout group. Keep damaged, wrong-item, and Plus waivers. Judge it on repeat purchases as well as return volume, since the repeat-purchase loss could cancel the savings.
- **Caveats:** Every web source uses a .example domain and may be a placeholder, so verify before citing. No source measured cart abandonment after a fee, and the 15% and 2% inputs are unverified.

subagents: searcher 1, searcher 2, searcher 3, analyst 1, analyst 2, synthesizer 1
subagents worked 98s in 57s of clock time: running together saved 41s
84s in all · 7 turns · $0.0195
```

**Should match:**

- Every line starts with the seconds since the run began.
- Subagents that don't depend on each other start within a second or two of each other (`->` lines close together), and their tool calls interleave while they work. Subagents that need earlier results (the analysts need the searchers' URLs; the synthesizer needs the findings) start after them.
- Each subagent is numbered within its kind (`searcher 1`, `searcher 2`, ...) and reports back with a `<- ... done (N.Ns)` line.
- The work is split without overlap: by part of the goal (in the lesson, the searchers) or by source type (in the lesson, the analysts: web pages and `harborline://internal/` documents).
- The last lines: the list of subagents, `subagents worked ...s in ...s of clock time: running together saved ...s`, and the total time, turns and cost.

**May differ:** the number of subagents and how the coordinator splits the work. Sometimes the coordinator checks the findings or the answer against the goal and sends a subagent after a missing part before the synthesizer writes (again); in the lesson's run it didn't. In practice runs before filming, running together saved 12 to 37 seconds and each run cost $0.015 to $0.020. If you see `[coordinator, denied]` lines, the coordinator tried to search by itself and the Lesson 4.1 hook stopped it.

## Step 3: Commit

```text
(.venv) $ clear; git status --short
 M research/coordinator.py
(.venv) $ git add research
(.venv) $ git commit -m "Lesson 4.3: subagents split by scope and run together, and the answer checked against the goal"
[main eea31f2] Lesson 4.3: subagents split by scope and run together, and the answer checked against the goal
 1 file changed, 61 insertions(+), 47 deletions(-)
(.venv) $ git push
...
   39b822d..eea31f2  main -> main
```

**Should match:** `1 file changed, 61 insertions(+), 47 deletions(-)` if your file matches the kit's. Your commit IDs will differ.
