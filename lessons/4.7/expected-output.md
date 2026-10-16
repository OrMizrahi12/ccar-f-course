# Expected output: Lesson 4.7, Provenance and conflicting sources

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. Long lines are wrapped by the terminal, so they're shown here unwrapped. `...` marks lines left out to keep this page short.

**What will differ on yours:** the run's timings, the searchers' queries, which documents each agent reads, the report's wording, which topics end up contested, the costs, and your commit ID. Claude's answers vary from run to run. Each section says what should match.

## Step 1: Render and check

```text
(.venv) $ git status --short
(.venv) $ code research/provenance.py
```

`git status --short` prints nothing: a clean tree after Lesson 4.6. Then type `research/provenance.py` (68 lines) and save it.

## Step 2: The report's shape

```text
(.venv) $ code research/agents.py
(.venv) $ code research/coordinator.py
```

Change both files as in README.md, step 2, and save them. Nothing is printed.

## Step 3: Provenance, tested

```text
(.venv) $ clear; python -m pytest -q tests/test_provenance.py
....                                                                     [100%]
4 passed in 0.01s
(.venv) $ python -m pytest -q
.............................................................................. [ 75%]
..........................                                                     [100%]
104 passed in 2.08s
```

**Should match:** `4 passed` and `104 passed` (the 100 tests from Lesson 4.6, plus these four). These tests call no model, so they pass the same way every time.

## Step 4: One run

```text
(.venv) $ clear; python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs/research.log
  3.9s -> searcher 1: Research question: What does processing e-commerce product r...
  4.7s -> searcher 2: Research question: How do online shoppers react when retaile...
  4.9s    [searcher 1] search_web cost of product returns retailers study
  5.1s    [searcher 1] search_web online returns rate ecommerce percentage
...
  5.8s -> searcher 3: Research question: What return shipping fee policies do onli...
  6.6s -> searcher 4: Research question: Find Harborline's own internal documents ...
...
 12.7s <- searcher 1 done (8.9s)
 13.7s <- searcher 4 done (7.1s)
 14.2s <- searcher 2 done (9.6s)
 16.4s <- searcher 3 done (10.6s)
 20.5s -> analyst 1: Read these web sources with load_document and return finding...
 21.9s    [analyst 1] load_document https://retail-signals.example/2026/05/charging-for-returns
 22.0s -> analyst 2: Read these Harborline internal documents with load_document ...
 22.1s    [analyst 1] load_document https://homeretaildaily.example/2026/08/pinecrest-return-fee
 22.2s    [analyst 1] load_document https://meridian-institute.example/reports/returns-benchmark-2025
 22.4s    [analyst 1] load_document https://retail-signals.example/2026/03/return-rates-new-high
 22.6s    [analyst 1] load_document https://parcelpostreview.example/2026/07/box-free-returns
 22.8s    [analyst 1] load_document https://lakeshore-business.example/papers/return-leniency-clv
 23.0s    [analyst 1] load_document https://consumerpulse.example/insights/bracketing-2025
 23.3s    [analyst 2] load_document harborline://internal/finance-memo-free-returns
 23.5s    [analyst 2] load_document harborline://internal/q2-2026-returns-report
 23.7s    [analyst 2] load_document harborline://internal/customer-survey-aug-2026
 23.8s    [analyst 2] load_document harborline://internal/warehouse-returns-note
 53.4s <- analyst 1 done (33.0s)
 57.4s <- analyst 2 done (35.4s)
 61.8s -> searcher 5: Gap search: find web pages that state a named online retaile...
...
 72.4s <- searcher 5 done (10.6s)
 84.8s -> synthesizer 1: Question from Harborline managers: Should Harborline charge ...
...
 89.9s    [synthesizer 1] verify_fact Return rate was 17.6% of units across 1,214 merchants (about 48M orders, Jan–Sep 2025); apparel/footwear 26.4%, home goods 11.9%, electronics 9.8%, beauty 5.1%; order-value rates are usually several points higher than unit rates. https://meridian-institute.example/reports/returns-benchmark-2025
...
 90.7s    [synthesizer 1] verify_fact 2025 return rate was 24.0% of order value, up from 21.3%; processing one online return costs $9–$14 including shipping, handling, and unsellable items; 71% of surveyed retailers offer free return shipping on every order. https://retail-signals.example/2026/03/return-rates-new-high
...
 92.1s    [synthesizer 1] verify_fact Apr–Jun 2026 return rate 19.2% by order value and 13.1% by units; cost per return $11.40 average = $7.10 shipping + $2.60 handling/inspection + $1.70 written off; changed my mind 38% of reasons. harborline://internal/q2-2026-returns-report
...
112.3s    [synthesizer 1] verify_fact 41% of US adults bracketed online purchases (34% clothing, 12% home goods) in a July 2025 survey of 2,050 adults with a margin of about plus or minus 2 points. https://consumerpulse.example/insights/bracketing-2025
136.2s <- synthesizer 1 done (51.4s)

## Answer
Harborline should test a return fee before rolling it out: limit it to 'changed my mind' returns, keep damaged or wrong items and Plus members free, and start in one category, as Finance proposes. The Finance model's $0.6M-$0.8M annual saving excludes lost repeat purchases; by my arithmetic from the memo's own figures (a 2% repeat drop is about $0.5M), the saving is gone if repeat purchases fall roughly 2.4%-3.2%, and the external panel reports a 6% repeat drop at fee retailers (observational data).

## Established
- Among 40 retailers that added a $3.95-$5.95 return fee in 2025, return volume fell a median 18% six months later, and repeat purchase fell 6% vs 1% for matched retailers that kept returns free (self-selected panel, no retailer names, loyalty effects still being measured). (Retail Signals Weekly, 2026-05-19)
- Harborline return shipping cost $1.61M in FY2025 and is forecast at $1.94M for FY2026; the modeled $4.95 fee on changed-my-mind returns saves $0.6M-$0.8M a year if volume falls 15%, but the model excludes lost repeat purchases (a 2% repeat drop is about $0.5M gross margin). (Harborline Finance, 2026-08-14)
- In Apr-Jun 2026 Harborline's average cost per return was $11.40 ($7.10 shipping, $2.60 handling and inspection, $1.70 written off), and 'changed my mind' was 38% of return reasons; return rate was 19.2% by order value and 13.1% by units. (Harborline Operations, 2026-07-20)
- Pinecrest Home began a $5.95 return shipping fee on 2026-09-15, waived for loyalty members, damaged or defective items, and partner drop-off returns; this is trade-press reporting and is not confirmed on Pinecrest's own site. (Home Retail Daily, 2026-08-27)
- 71% of 312 surveyed retail executives offer free return shipping on every order, and the survey estimates one online return costs $9-$14 including shipping, handling and unsellable items (self-reported, unaudited). (Retail Signals Weekly, 2026-03-12)
- In H1 2026, drop-off returns cost retailers an average of $5.70 per parcel vs $8.20 for a prepaid label and box (shipping cost only; drop-off is thin in rural areas and items reach the warehouse about 2 days sooner). (Parcel & Post Review, 2026-07-08)

## Contested
**Return rate level**: The figures use different measures (share of units vs share of order value), samples (transaction data from 1,214 merchants vs a survey of 312 executives vs Harborline's own orders) and periods. Meridian notes value-based rates are usually several points higher than unit rates, so the figures should not be compared directly.

| Figure | Source | Method |
|---|---|---|
| 17.6% of units (Jan-Sep 2025 average) | Meridian Commerce Institute, 2025-11-04 | Anonymized transaction data from 1,214 merchants, about 48M orders |
| 24.0% of order value (2025) | Retail Signals Weekly, 2026-03-12 | Survey of 312 retail executives, self-reported |
| 19.2% of order value; 13.1% of units (Apr-Jun 2026, Harborline) | Harborline Operations, 2026-07-20 | Harborline internal order and return records for one quarter |

**Effect of free returns on customer value and repeat purchase**: The two studies measure different outcomes (6-month repeat purchase after a fee is introduced vs 3-year customer lifetime value of customers acquired under free returns), cover different categories, and use observational designs. Neither is randomized, so they cannot settle the direction of the effect.

| Figure | Source | Method |
|---|---|---|
| Repeat purchase fell 6% at fee retailers vs 1% at comparison retailers, six months after the change | Retail Signals Weekly, 2026-05-19 | Self-selected panel of 40 fee retailers vs 40 matched free-returns retailers; observational |
| Customers acquired under free returns had 8% higher 3-year CLV than paid-returns customers (home goods only; smaller for items under $40; not significant for electronics) | Lakeshore University School of Business (working paper), 2025-04-15 | Observational study of 23 online retailers, 2019-2024, controlling for first-order size and channel; working paper, not peer reviewed |

**Stated vs observed response to a return fee**: Harborline's survey and Consumer Pulse measure what customers say they would do; the external panel measures what retailers observed after a fee. Stated intentions are not observed behavior, and Harborline's survey does not report its response rate or weighting and does not limit the fee to changed-my-mind returns.

| Figure | Source | Method |
|---|---|---|
| 27% would shop less often and 9% would stop shopping at a $4.95 return fee; Plus members 35% vs 24% of other customers | Harborline Customer Insights, 2026-09-05 | Email survey of 1,148 recent Harborline customers; response rate, weighting, margin of error and full question wording not stated |
| 58% would be very or somewhat likely to abandon their cart at a hypothetical $5 return fee; 23% would buy only one version; 19% no difference | Consumer Pulse Panel, 2025-09-02 | Online survey of 2,050 US adults, July 2025, margin of error about 2 points; hypothetical question |

## Not covered
Competitor policies: no policy was found for Wayfair, IKEA, Target, Walmart, Amazon, Williams-Sonoma or Crate & Barrel, so the only named competitor is Pinecrest Home, which is reported in trade press and not confirmed on its own site (the source is a .example URL). The 40-retailer panel does not name its retailers. Not covered: carrier per-parcel costs by retailer; Harborline's actual return counts and refund dollar totals, so the $11.40 per-return cost and the $1.94M forecast cannot be combined into a volume-based estimate; whether the $1.61M FY2025 figure is actual or estimated (not stated); fee-deduction-from-refund policies; randomized experiments on fee effects; NRF return totals (not confirmed). Not verified and not used: the 41% bracketing total (only the 34% clothing and 12% home goods figures were confirmed); the Northgate 9.4% fraud estimate (searcher snippet only); the Meridian 2023 rate of 16.5% (not read); Harborline's warehouse note (22% of returns not resellable, 6.5-day refund lag) was not analysed for fee cost. The Plus subgroup sample size in the Harborline survey is not stated. The requested output keys (recommendation, cost_of_returns, etc.) were replaced by this report's required schema, so the recommendation is in the answer and the cost, customer, competitor and data content is in the established and contested sections.

provenance: ok

subagents: searcher 1, searcher 2, searcher 3, searcher 4, analyst 1, analyst 2, searcher 5, synthesizer 1
subagents worked 167s in 112s of clock time: running together saved 55s
147s in all · 9 turns · $0.0363
```

**Should match:**

- The report comes out in this order: `## Answer`, `## Established`, `## Contested`, `## Not covered` (only when something isn't covered).
- Every established line ends with its source and date, in parentheses: `(Publisher, YYYY-MM-DD)`.
- Every contested topic has a bold name, a line on why the figures differ, and a `| Figure | Source | Method |` table with at least two rows.
- The last report line is `provenance: ok`, or a list of what `check()` found.

Your topics, figures and wording will differ. In the lesson's run, Meridian's 2023 figure wasn't read, and the report says so under `## Not covered`; in a practice run before filming it was read, and the report listed 2023 and 2025 under established as a change over time. If a source with no stated method is used, its citation ends with `(no method stated)`. The run takes two to three minutes.

## Step 5: Commit

```text
(.venv) $ clear; git status --short
 M research/agents.py
 M research/coordinator.py
?? research/provenance.py
?? tests/test_provenance.py
(.venv) $ git add research tests
(.venv) $ git commit -m "Lesson 4.7: a report that keeps every claim with its source, and shows conflicting figures side by side"
[main c1d9e00] Lesson 4.7: a report that keeps every claim with its source, and shows conflicting figures side by side
 4 files changed, 136 insertions(+), 8 deletions(-)
 create mode 100644 research/provenance.py
 create mode 100644 tests/test_provenance.py
(.venv) $ git push
...
   fe332ab..c1d9e00  main -> main
```

**Should match:** `4 files changed, 136 insertions(+), 8 deletions(-)` if your files match the kit's. Your commit IDs will differ.
