# Expected output: Lesson 2.2, Rename, split, constrain

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12.3 and Claude Haiku 5.5 (`claude-haiku-5-5`), from the `harborline` folder with `.venv` active. The terminal wrapped and scrolled long output; it's shown unwrapped and complete here.

**Your runs will differ from these.** Each request runs three times per column, and Claude doesn't pick the same way every time: a row can read 2/3 where the lesson's read 3/3, token counts and costs change with every call, and a request near a word the line keys on (like R15, "Track ...") can move on one run and stay on the next. Each section says what should match.

## Step 1: One tool for everything

```text
(.venv) $ git status --short
(.venv) $ code loop/tools.py
(.venv) $ code experiments/m2/prompt_override.py
```

`git status --short` prints nothing: the tree is clean after Lesson 2.1. Saving prints nothing.

The lesson doesn't run the script with `query_backend` in the set. Run off camera three times, Claude never picked `query_backend` first: 0 of 48 tries in every run. If you run it (`clear; python -m experiments.m2.prompt_override`, one column), you'll most likely see the same. That doesn't make the generic tool safe: two right answers for one request is a risk you don't control, and its loose input and changing result shape stay.

## Step 2: Split it by purpose

```text
(.venv) $ code loop/tools.py
```

Saving prints nothing. Compare your file with the kit's `loop/tools.py`: `QUERY_BACKEND` and `query_backend()` are gone, `CHECK_REFUND` and `check_refund()` stand in their place, and `process_refund`'s description ends with "Only asking what the policy allows? Use check_refund."

## Step 3: One line in the system prompt

```text
(.venv) $ clear; python -m experiments.m2.prompt_override "When a customer mentions shipping or delivery, call list_orders first." "If a customer asks about an order but has no order ID, use list_orders to find it."
1: (none)
2: When a customer mentions shipping or delivery, [...]
3: If a customer asks about an order but has no [...]

R01  lookup_order       3/3  0/3  3/3
     Has order HL-10190 shipped yet?
     2: list_orders {'customer_id': 'C-1046'}
R02  list_orders        3/3  3/3  3/3
R03  list_orders        3/3  3/3  3/3
R04  lookup_order       3/3  3/3  3/3
R05  get_customer       3/3  3/3  3/3
R06  process_refund     3/3  3/3  3/3
R07  escalate_to_human  3/3  3/3  3/3
R08  list_orders        3/3  3/3  3/3
R09  lookup_order       3/3  2/3  3/3
     When was HL-10072 delivered?
     2: list_orders {'customer_id': 'C-1046'}
R10  get_customer       3/3  3/3  3/3
R11  list_orders        3/3  3/3  3/3
R12  process_refund     3/3  0/3  3/3
     Order HL-10089 came a week late. Please refund [...]
     2: list_orders {'customer_id': 'C-1046'}
R13  escalate_to_human  0/3  1/3  1/3
     I need a supervisor to sign off on a refund over $500.
     1: (end_turn)
     2: (end_turn)
     3: (end_turn)
R14  list_orders        3/3  3/3  3/3
R15  lookup_order       3/3  3/3  3/3
R16  get_customer       3/3  3/3  3/3

1: 45/48 as labeled
2: 39/48 as labeled
3: 46/48 as labeled
271,371 tokens in  $0.0356
```

How to read it:

| Part | What it means |
|---|---|
| `1:`, `2:`, `3:` at the top | The columns. 1 sends no system prompt; 2 and 3 send the line you passed as the whole system prompt (shortened here) |
| `R01  lookup_order` | The request's ID and the tool it should get first |
| `3/3  0/3  3/3` | Tries out of three whose first tool call was the right one, per column. For a refund request, a first call to `lookup_order` or `check_refund` also counts (`ALSO_OK`) |
| The indented lines | Under a row with misses: the request, shortened, then per column the most common wrong first call and the input Claude sent; `(end_turn)` means it answered in text |
| `N/48 as labeled` | Each column's total: 16 requests × 3 tries |
| The last line | Input tokens of all 144 calls, and their cost |

What should match: column 2 (the keyword line) loses requests that contain its words ("shipped", "delivered", "shipping fee"), and they go to `list_orders` with the signed-in customer's ID, although each one names an order; column 3 (the same intent, written for the situation) stays close to column 1; column 1 sends nothing outside refund requests to `check_refund`. What may differ: which keyword rows move and by how much, R13 (Claude often asks for details before escalating), and the totals.

```text
(.venv) $ code loop/agent.py
```

A look only. Its system prompt still says the agent can't issue refunds, while it's handed every tool in `TOOLS`, `process_refund` included. Choosing which tools each agent gets is the next lesson's topic.

## Step 4: Commit

```text
(.venv) $ git status --short
 M loop/tools.py
?? experiments/m2/prompt_override.py
(.venv) $ git add loop/tools.py experiments/m2/prompt_override.py
(.venv) $ git commit -m "Lesson 2.2: split a generic tool, test system-prompt lines"
[main 7f2daa1] Lesson 2.2: split a generic tool, test system-prompt lines
 2 files changed, 120 insertions(+), 2 deletions(-)
 create mode 100644 experiments/m2/prompt_override.py
(.venv) $ git push
...
To https://github.com/YOUR-USERNAME/harborline.git
   5087233..7f2daa1  main -> main
```

What should match: `2 files changed, 120 insertions(+), 2 deletions(-)` if you typed the files exactly as the kit has them, and `main -> main` to your own repository. What differs: the commit IDs, the push's object counts, and the URL (your GitHub account). `runs/` isn't listed: it's ignored.
