# Expected output: Lesson 4.1, Coordinators and subagents

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. The prompts the coordinator writes are wrapped by the script itself (78 columns); long tool-call lines and the answer are wrapped by the terminal, and are shown here unwrapped.

**What will differ on yours:** the wording of every prompt the coordinator writes, the searches the searcher runs, the URLs it picks, every answer (Claude's replies vary from run to run), the costs, and your commit IDs. Each section says what should match.

## Step 1: The research tools

```text
(.venv) $ git status --short
(.venv) $ mkdir research
(.venv) $ code research/tools.py
(.venv) $ clear; python -m research.tools "return fee"
2025-11-04 Meridian Commerce Institute https://meridian-institute.example/reports/returns-benchmark-2025
2026-05-19 Retail Signals Weekly https://retail-signals.example/2026/05/charging-for-returns
2025-09-02 Consumer Pulse Panel https://consumerpulse.example/insights/bracketing-2025
2025-12-10 Northgate Loss Prevention Council https://northgate-lpc.example/research/return-fraud-2025
2026-09-05 Harborline Customer Insights harborline://internal/customer-survey-aug-2026
```

**Should match exactly:** the search is plain Python over a fixed folder, so the same query prints the same five lines on every machine, and it makes no API call.

## Step 3: One question, two subagents

```text
(.venv) $ clear; python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs/research.log

-> searcher gets only this prompt:
   Research question: Should an online home-goods retailer charge customers a
   fee for return shipping? Find sources (publisher, date, URL) on: (1) survey
   or study data on how return shipping fees affect customer purchase,
   conversion, or loyalty; (2) retailer case studies or industry benchmarks on
   paid vs free returns; (3) any US or EU regulatory rules on charging for
   returns (e.g., FTC or EU consumer rules). Use short keyword queries, one
   topic per search. Return the URLs worth reading, most relevant first.
   Nothing is ruled out yet.
   [searcher] search_web {'query': 'return shipping fee effect on online purchase conversion study'}
   [searcher] search_web {'query': 'paid returns survey consumers abandon purchase'}
   [searcher] search_web {'query': 'free returns vs paid returns retailer case study'}
   [searcher] search_web {'query': 'online returns fees industry benchmark 2025'}
   [searcher] search_web {'query': 'EU Consumer Rights Directive return costs trader pays'}
   [searcher] search_web {'query': 'FTC rule returns refunds junk fees'}
   [searcher] search_web {'query': 'Consumer Rights Directive 2011/83/EU article 14 return costs'}
   [searcher] search_web {'query': 'FTC mail order rule refunds return shipping cost disclosure'}
   [searcher] search_web {'query': 'Pinecrest Home return fee announcement'}

-> analyst gets only this prompt:
   Question: Should an online home-goods retailer (Harborline) charge
   customers for return shipping? Fetch each URL below and report, per URL:
   whether it loaded, the publisher and date shown on the page, and the
   specific facts relevant to the question (fees, return rates, customer
   behavior or sales impact, with figures). Quote numbers exactly. Flag any
   page that fails to load or does not match the description given. Do not add
   facts from outside these pages.
   URLs:
   1. https://retail-signals.example/2026/05/charging-for-returns
   2. https://homeretaildaily.example/2026/08/pinecrest-return-fee
   3. https://consumerpulse.example/insights/bracketing-2025
   4. https://meridian-institute.example/reports/returns-benchmark-2025
   5. https://lakeshore-business.example/papers/return-leniency-clv
   6. https://eur-lex.europa.eu/eli/dir/2011/83/oj (only the sections on
   withdrawal costs / who pays return costs)
   Keep the report short.
   [analyst] fetch_url {'url': 'https://retail-signals.example/2026/05/charging-for-returns'}
   [analyst] fetch_url {'url': 'https://homeretaildaily.example/2026/08/pinecrest-return-fee'}
   [analyst] fetch_url {'url': 'https://consumerpulse.example/insights/bracketing-2025'}
   [analyst] fetch_url {'url': 'https://meridian-institute.example/reports/returns-benchmark-2025'}
   [analyst] fetch_url {'url': 'https://lakeshore-business.example/papers/return-leniency-clv'}
   [analyst] fetch_url {'url': 'https://eur-lex.europa.eu/eli/dir/2011/83/oj'}

Recommendation: a paid return fee is defensible if it's narrow, but the evidence I gathered shows a real sales cost, so I'd test it before rolling it out to everyone.

- A fee cut returns by a median 18%, but repeat purchases fell 6% vs. 1% at matched free-return retailers, and return-related service contacts rose about 25% ([Retail Signals Weekly, 2026-05-19](https://retail-signals.example/2026/05/charging-for-returns)).
- Most fee-charging retailers waived the fee for damaged or wrong items (38 of 40) and about half for loyalty members (22 of 40) (same source).
- Shoppers say a $5 fee would make them abandon carts (58%), but these are stated intentions, not observed behavior ([Consumer Pulse Panel, 2025-09-02](https://consumerpulse.example/insights/bracketing-2025)).
- A home-goods peer, Pinecrest Home, announced a $5.95 fee with waivers for members and damaged items, but the page has no outcome data ([Home Retail Daily, 2026-08-27](https://homeretaildaily.example/2026/08/pinecrest-return-fee)).
- Free returns were linked to 8% higher three-year customer lifetime value in home goods, but the paper is unreviewed and not randomized ([Lakeshore working paper, 2025-04-15](https://lakeshore-business.example/papers/return-leniency-clv)).
- Caveat: every source domain ends in `.example`, a reserved placeholder TLD, so these may not be real publishers. Verify them before any decision.
- I found no usable regulatory sources; the EUR-Lex directive page did not load, so check local return-cost rules yourself.
- Harborline's own Q2 2026 Returns Report was not reviewed and should be checked against these figures.

subagents: searcher, analyst · 3 turns · $0.0057
```

**Should match:** the shape. An `-> searcher` prompt and `[searcher] search_web` lines, then an `-> analyst` prompt that lists URLs and `[analyst] fetch_url` lines, then an answer that cites URLs, and `subagents: searcher, analyst`. No `[coordinator]` line: the hook keeps the research tools in the subagents. The analyst never sees the searcher's work; the URLs reach it only because the coordinator wrote them into its prompt. A URL that isn't in `data/research/` (here, the EU law page) comes back as an error, and the answer should say so. The searches, the URLs, the facts chosen, the turn count and the cost will differ (the practice runs cost $0.0045 to $0.0071).

## Step 4: Only what the question needs

```text
(.venv) $ clear; python -m research.coordinator "What return rate does https://meridian-institute.example/reports/returns-benchmark-2025 report?" 2> runs/research.log

-> analyst gets only this prompt:
   Question: What return rate does the report at https://meridian-
   institute.example/reports/returns-benchmark-2025 report?

   Fetch that URL and extract every return-rate figure it states (value, what
   it measures, such as overall, by category, or by year, and the exact
   sentence or table row it comes from). If the page fails to load or contains
   no return-rate figure, say so plainly and quote what the page does say
   about returns, if anything. Report the page URL as the source for each
   fact. Do not use outside knowledge.
   [analyst] fetch_url {'url': 'https://meridian-institute.example/reports/returns-benchmark-2025'}

The headline figure is 17.6%: the average online return rate for January to September 2025, measured as a share of units sold.
Source: https://meridian-institute.example/reports/returns-benchmark-2025
By category (share of units returned), from the same page:
- Apparel and footwear: 26.4%
- Home goods: 11.9%
- Consumer electronics: 9.8%
- Beauty: 5.1%
The page also says free-return-shipping merchants had a return rate 3.4 points higher than fee-charging merchants, after controlling for category, but it does not give the two underlying rates.

subagents: analyst · 2 turns · $0.0012
(.venv) $ clear; python -m research.coordinator "Which sources cover return fraud? Just list them." 2> runs/research.log

-> searcher gets only this prompt:
   Research question: Which sources cover return fraud (retail merchandise
   return fraud, e.g. fraudulent returns, return abuse, refund fraud, receipt
   fraud, returns policy abuse)? Today is 2026-10-15. Use short keyword
   searches, one topic per search. Run several searches with different
   phrasings (e.g. "retail return fraud", "return fraud statistics", "return
   fraud prevention ecommerce", "merchandise return abuse report"). Return
   only the URLs worth reading, each with publisher and date published. Prefer
   reputable sources: industry reports (e.g. NRF, Appriss Retail, Forrester),
   major retailers' or consultancies' publications, news outlets, and academic
   or government sources. No summaries of content are needed beyond a one-line
   description per source.
   [searcher] search_web {'query': 'retail return fraud report'}
   [searcher] search_web {'query': 'return fraud statistics'}
   [searcher] search_web {'query': 'return fraud prevention ecommerce'}
   [searcher] search_web {'query': 'merchandise return abuse report'}
   [searcher] search_web {'query': 'NRF Appriss Retail returns fraud'}
   [searcher] search_web {'query': 'refund fraud receipt fraud retailers'}

Candidate sources reported by the searcher (not independently verified):
1. Northgate Loss Prevention Council, 2025-12-10, on return fraud and policy abuse: https://northgate-lpc.example/research/return-fraud-2025
2. Meridian Commerce Institute, 2025-11-04, e-commerce returns benchmark: https://meridian-institute.example/reports/returns-benchmark-2025
3. Meridian Commerce Institute, 2024-01-22, earlier returns benchmark: https://meridian-institute.example/reports/returns-benchmark-2023
4. Retail Signals Weekly, 2026-05-19, return shipping fees vs. free returns: https://retail-signals.example/2026/05/charging-for-returns
5. Home Retail Daily, 2026-08-27, single-retailer return fee story: https://homeretaildaily.example/2026/08/pinecrest-return-fee

Caution: every URL uses a `.example` domain, which is a reserved placeholder, so these may not be real pages. The searcher found no NRF, Appriss Retail, Forrester, government, or academic sources. Only the first source is clearly about return fraud. Please verify the URLs before citing them.

subagents: searcher · 2 turns · $0.0024
```

**Should match:** the question that names its page goes to the analyst alone (one `fetch_url`, no searcher), and the figure is 17.6% (it's on the page). The list question goes to the searcher alone (no `fetch_url`). In every practice run, the coordinator chose the same subagents for these two questions; the wording and the searches differed.

## Step 5: Commit

```text
(.venv) $ clear; git status --short
?? research/
(.venv) $ git add research
(.venv) $ git commit -m "Lesson 4.1: a research coordinator with two subagents"
[main 1bffb08] Lesson 4.1: a research coordinator with two subagents
 2 files changed, 187 insertions(+)
 create mode 100644 research/coordinator.py
 create mode 100644 research/tools.py
(.venv) $ git push
...
   1e0bbd4..1bffb08  main -> main
```

**Should match:** the file list and the counts. `runs/research.log` is not listed: `runs/` is git-ignored. Your commit IDs will differ.
