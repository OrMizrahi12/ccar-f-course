# Expected output: Lesson 4.2, Subagents in the Agent SDK

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. Prompts are wrapped by the script itself (78 columns); the answer's long lines are wrapped by the terminal, so they're shown here unwrapped.

**What will differ on yours:** the wording of every prompt the coordinator writes, the searches, the URLs it picks, the number of findings, the answer, the cost, and your commit IDs. Claude's choices vary from run to run. Each section says what should match.

## Step 1: Three definitions

```text
(.venv) $ git status --short
(.venv) $ code research/agents.py
```

`git status --short` prints nothing: a clean tree after Lesson 4.1. Then type `research/agents.py` (41 lines) and save it.

## Step 2: The coordinator uses them

```text
(.venv) $ code research/coordinator.py
```

No output: you change the file in the editor (README.md, step 2) and save it. It ends up 115 lines long.

## Step 3: Findings handed over whole

```text
(.venv) $ clear; python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs/research.log
coordinator tools: Task, mcp__research__fetch_url, mcp__research__search_web

-> searcher gets only this prompt:
   Research question: Should an online home-goods retailer (Harborline) charge
   customers a fee for return shipping? Find sources worth reading on: the
   effect of return shipping fees on customer conversion, sales, and
   retention; customer reactions and trust; return rates; and fee-free return
   policies versus fee policies in retail. Run several short keyword searches,
   one topic per search. Return the URLs worth reading, with publisher and
   date for each. Prefer recent, credible sources (retailer research, industry
   studies, consumer surveys, reputable business press).
   [searcher] search_web {'query': 'return shipping fee effect on online conversion and sales'}
   [searcher] search_web {'query': 'return shipping fees customer retention study'}
   [searcher] search_web {'query': 'paid returns customer reaction trust survey'}
   [searcher] search_web {'query': 'free returns impact on return rates ecommerce'}
   [searcher] search_web {'query': 'free returns vs return fee retailer policy comparison'}

-> analyst gets only this prompt:
   Question: Should Harborline, an online home-goods store, charge customers a
   fee for return shipping? Read each URL below with fetch_url and return
   findings as JSON: each claim with its evidence (quoted or closely
   paraphrased), the figures and sample sizes, and the source's publisher,
   date, and URL. Flag anything that is only a snippet-level claim, a
   vendor/trade-group estimate, or not supported by the page. Do not add
   outside knowledge.

   URLs:
   1. https://retail-signals.example/2026/05/charging-for-returns
   2. https://homeretaildaily.example/2026/08/pinecrest-return-fee
   3. https://lakeshore-business.example/papers/return-leniency-clv
   4. https://meridian-institute.example/reports/returns-benchmark-2025
   5. https://consumerpulse.example/insights/bracketing-2025
   6. https://northgate-lpc.example/research/return-fraud-2025
   7. https://retail-signals.example/2026/03/return-rates-new-high
   [analyst] fetch_url {'url': 'https://retail-signals.example/2026/05/charging-for-returns'}
   [analyst] fetch_url {'url': 'https://homeretaildaily.example/2026/08/pinecrest-return-fee'}
   [analyst] fetch_url {'url': 'https://lakeshore-business.example/papers/return-leniency-clv'}
   [analyst] fetch_url {'url': 'https://meridian-institute.example/reports/returns-benchmark-2025'}
   [analyst] fetch_url {'url': 'https://consumerpulse.example/insights/bracketing-2025'}
   [analyst] fetch_url {'url': 'https://northgate-lpc.example/research/return-fraud-2025'}
   [analyst] fetch_url {'url': 'https://retail-signals.example/2026/03/return-rates-new-high'}

-> synthesizer gets only this prompt:
   Question: Should Harborline, an online home-goods store, charge customers a
   fee for return shipping?

   Write the answer using only the findings below. Do not add outside
   knowledge. Give a clear recommendation (yes, no, or conditional), state the
   main evidence and its limits (observational, self-reported, small samples,
   unit vs. value bases), and name what Harborline should check before
   deciding, including its own internal customer survey
   (harborline://internal/customer-survey-aug-2026, 2026-09-05), which was not
   read. Keep the answer to at most eight lines.

   Findings (analyst output, complete and unchanged):
   [ 21 findings as JSON, keys: claim, evidence, url, publisher, published, method ]

**Recommendation: conditional. Don't add a blanket return fee on the current evidence.** If Harborline does add one, exempt damaged or wrong items and loyalty members, and test it before rolling it out fully.

- **Fee effects:** One panel of 40 fee-charging retailers vs. 40 matched peers (Retail Signals Weekly, May 2026) found a median 18% drop in returns, but a 6% drop in repeat purchases vs. 1% for peers, and about a quarter more service contacts. The comparison is not randomized and the sample is small.
- **Free returns and lifetime value:** A working paper (Lakeshore University, April 2025) links free returns to 8% higher three-year customer lifetime value. It is observational, not peer reviewed, and the effect was smaller for items under $40 and not significant for electronics.
- **Conflicting signals:** Meridian (November 2025) found free-return merchants had 3.4 points higher return rates, controlling for category only. Northgate (December 2025) found 57% of loss-prevention managers at free-return retailers reported rising abuse vs. 39% at fee retailers; these are manager perceptions.
- **Customer intent:** In a survey (Consumer Pulse, September 2025), 58% said a hypothetical $5 fee would likely make them abandon a cart, and 41% of shoppers report bracketing. These are stated intentions, not observed behavior.
- **Peer case:** Pinecrest Home announced a $5.95 fee with loyalty waivers (August 2026), but there are no outcome data yet.
- **Before deciding:** Harborline's own August 2026 customer survey was not read, and this is the most relevant evidence. Also pull Harborline's return rates by category on both unit and value bases, its share of returns that are damaged items or from loyalty members, and the effect of a pilot fee on repeat purchase.

subagents: searcher, analyst, synthesizer · 4 turns · $0.0147
```

**Should match:**

- The first line lists `Task` with the two research tools. `Task` is the Agent tool's name in the init list; in tool calls it's `Agent`.
- Three subagents run in order, each under `-> <name> gets only this prompt:`: the searcher (searches only), the analyst (fetches only) and the synthesizer (no tool calls at all).
- The synthesizer's prompt ends with one line in place of the findings: `[ N findings as JSON, keys: claim, evidence, url, publisher, published, method ]`. The keys come from the analyst's definition, even when the coordinator's brief to the analyst asks for a different shape (as it did in the lesson). Only the printout is one line: the synthesizer gets the whole list.
- The answer names a publisher and a date for its claims, and the last line reads `subagents: searcher, analyst, synthesizer`.

In the three practice runs before filming, every run used the searcher, the analyst and the synthesizer, with 17 to 21 findings. The run takes about a minute and a half; most of it is the analyst reading the pages.

## Step 4: Commit

```text
(.venv) $ clear; git status --short
 M research/coordinator.py
?? research/agents.py
(.venv) $ git add research
(.venv) $ git commit -m "Lesson 4.2: subagent definitions in one file, and findings handed over as JSON"
[main 39b822d] Lesson 4.2: subagent definitions in one file, and findings handed over as JSON
 2 files changed, 75 insertions(+), 29 deletions(-)
 create mode 100644 research/agents.py
(.venv) $ git push
...
   1bffb08..39b822d  main -> main
```

**Should match:** `2 files changed, 75 insertions(+), 29 deletions(-)` if your files match the kit's. Your commit IDs will differ.
