# Expected output: Lesson 2.1, Tool descriptions that route correctly

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12.3 and Claude Haiku 5.5 (`claude-haiku-5-5`), from the `harborline` folder with `.venv` active. The terminal wrapped and scrolled long output; it's shown unwrapped and complete here.

**Your runs will differ from these.** Each request runs three times, and Claude doesn't pick the same way every time: a row can read 2/3 on your run where the lesson's read 3/3, token counts and costs change with every call, and a request that's close to a boundary (like R13) moves the most. Each section says what should match.

## Step 1: Measure the first drafts

```text
(.venv) $ git status --short
(.venv) $ code loop/tools.py
(.venv) $ mkdir -p experiments/m2
(.venv) $ code experiments/m2/routing_eval.py
```

`git status --short` prints nothing: the tree is clean after Lab 1. The two `code` commands open the files in the editor; saving prints nothing.

What should match: after you save, no red squiggles under `from loop.tools import TOOLS, run_tool` or `from harborline.backend import ORDER_ID_PATTERN`.

### The before run

```text
(.venv) $ clear; python -m experiments.m2.routing_eval before
-- labeled
R01  lookup_order      lookup_order         3/3
R02  list_orders       list_orders          3/3
R03  list_orders       list_orders          3/3
R04  lookup_order      lookup_order         3/3
R05  get_customer      get_customer         3/3
R06  process_refund    (end_turn)           0/3
     The kettle in order HL-10112 arrived cracked. I [...]
R07  escalate_to_human escalate_to_human    3/3
R08  list_orders       list_orders          3/3
R09  lookup_order      lookup_order         3/3
R10  get_customer      get_customer         3/3
R11  list_orders       list_orders          3/3
R12  process_refund    (end_turn)           0/3
     Order HL-10089 came a week late. Please refund [...]
R13  escalate_to_human (end_turn)           0/3
     I need a supervisor to sign off on a refund over $500.
R14  list_orders       list_orders          3/3
R15  lookup_order      lookup_order         3/3
R16  get_customer      get_customer         3/3
-- held-out
H1  lookup_order      lookup_order 10190   0/3
     Has order 10190 shipped?
H2  lookup_order      lookup_order 10199   0/3
     Where is my order #10199?
H3  lookup_order      lookup_order hl 1020 0/3
     Can you track hl 10203?
H4  lookup_order      lookup_order 10164   0/3
     What came in order 10164?
H5  escalate_to_human process_refund       0/3
     My espresso machine from HL-10192 arrived [...]
H6  escalate_to_human process_refund       0/3
     The desk from HL-10177 came damaged. Refund it.
H7  process_refund    process_refund       3/3
H8  process_refund    process_refund       3/3

before: labeled 39/48  held-out 6/24  97,383 in  $0.0157
```

How to read a row:

| Part | What it means |
|---|---|
| `R06` | The request's ID. R01 to R16 are Harborline's labeled routing requests; H1 to H8 are the held-out set in `routing_eval.py` |
| `process_refund` (first column) | The label: the tool this request should get |
| `(end_turn)` (second column) | The most common miss across the three tries: the tool Claude called instead, the input it passed when the tool was right (`lookup_order 10190`), or, in brackets, why it stopped without a tool (`end_turn`: it answered in text) |
| `0/3` | Tries that were correct: the right tool, an order ID in `HL-` form, the signed-in customer, and the input the label asks for |
| The indented line | The request itself, shortened, printed under every miss |

The summary line: correct tries out of 48 on the labeled set (16 requests × 3) and out of 24 on the held-out set (8 × 3), the input tokens of every call in the run, and their cost. The run takes about a minute: the three tries of each request run side by side. It saves its scores to `runs/routing-before.json`, which the after run reads.

What should match: H1 to H4 miss with `lookup_order` and the number as the customer typed it (`10190`, `#10199`, `hl 10203`): right tool, wrong input. H5 and H6 go to `process_refund` for refunds above $500. H7, H8 and most labeled rows are 3/3. What may differ: the exact scores (R06, R12 and R13 are the ones that move), tokens and cost.

## Step 2: Write descriptions that route

```text
(.venv) $ code loop/tools.py
```

Only description strings change: the five tool descriptions and `lookup_order`'s `order_id` line. Saving prints nothing. Compare your file with the kit's `loop/tools.py`.

## Step 3: Measure again

```text
(.venv) $ clear; python -m experiments.m2.routing_eval after
-- labeled
R01  lookup_order      lookup_order         3/3
R02  list_orders       list_orders          3/3
R03  list_orders       list_orders          3/3
R04  lookup_order      lookup_order         3/3
R05  get_customer      get_customer         3/3
R06  process_refund    (end_turn)           0/3
     The kettle in order HL-10112 arrived cracked. I [...]
R07  escalate_to_human escalate_to_human    3/3
R08  list_orders       list_orders          3/3
R09  lookup_order      lookup_order         3/3
R10  get_customer      get_customer         3/3
R11  list_orders       list_orders          3/3
R12  process_refund    (end_turn)           0/3
     Order HL-10089 came a week late. Please refund [...]
R13  escalate_to_human (end_turn)           1/3  was 0/3
     I need a supervisor to sign off on a refund over $500.
R14  list_orders       list_orders          3/3
R15  lookup_order      lookup_order         3/3
R16  get_customer      get_customer         3/3
-- held-out
H1  lookup_order      lookup_order         3/3  was 0/3
H2  lookup_order      lookup_order         3/3  was 0/3
H3  lookup_order      lookup_order         3/3  was 0/3
H4  lookup_order      lookup_order         3/3  was 0/3
H5  escalate_to_human process_refund       2/3  was 0/3
     My espresso machine from HL-10192 arrived [...]
H6  escalate_to_human escalate_to_human    3/3  was 0/3
H7  process_refund    process_refund       3/3
H8  process_refund    process_refund       3/3

before: labeled 39/48  held-out 6/24  97,383 in  $0.0157
after:  labeled 40/48  held-out 23/24  145,177 in  $0.0203
```

`was 0/3` appears only where a score moved. The run reads the before scores from `runs/routing-before.json`, so run `before` first.

What should match: H1 to H4 now pass the ID as `HL-` plus five digits (3/3 or close); H6 goes to `escalate_to_human`; H7 and H8 stay refunds; the held-out score rises far more than the labeled one; the after run costs more input tokens than the before run (about half again in the lesson), because every description is sent with every request. What may differ: H5 (in the lesson, one try of three still went to `process_refund`), R13 (Claude often asks which order, how much and why before escalating), the exact numbers.

About R06 and R12: in the lesson they stayed 0/3 in both runs, and Claude was right. Order HL-10112 holds a rug, not a kettle, and HL-10089 arrived a day early, not a week late: Claude looked up the orders and declined. The labels were wrong, not the routing. Read your misses before you trust a score.

## Step 4: Commit

```text
(.venv) $ git status --short
 M loop/tools.py
?? experiments/m2/
(.venv) $ git add loop/tools.py experiments/m2/routing_eval.py
(.venv) $ git commit -m "Lesson 2.1: tool descriptions that route, measured before and after"
[main 5087233] Lesson 2.1: tool descriptions that route, measured before and after
 2 files changed, 212 insertions(+), 9 deletions(-)
 create mode 100644 experiments/m2/routing_eval.py
(.venv) $ git push
...
To https://github.com/YOUR-USERNAME/harborline.git
   6f977a7..5087233  main -> main
```

What should match: `2 files changed, 212 insertions(+), 9 deletions(-)` if you typed the files exactly as the kit has them, and `main -> main` to your own repository. What differs: the commit IDs (yours are your own), the push's object counts, and the URL (your GitHub account). `runs/` isn't listed by `git status`: it's ignored.
