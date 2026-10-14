# Expected output: Lesson 1.5, Who decides: model-driven agents vs fixed workflows

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12.3 and Claude Haiku 5.5 (`claude-haiku-5-5`), from the `harborline` folder with `.venv` active. The terminal wrapped long lines; they're shown unwrapped here.

**Your runs will differ from these.** The numbers vary run to run: Claude words each reply differently, the token counts and costs change with every call, and a route can change too (most of all on a ticket that fits no route, like T-006). The agent may also take a different number of turns. Each section says what should match.

## Step 1: Fix the path

```text
(.venv) $ git status --short
(.venv) $ code loop/agent.py
(.venv) $ code loop/workflow.py
```

`git status --short` prints nothing: the tree is clean after Lesson 1.4. `loop/agent.py` is Lesson 1.4's file, opened for a look and not changed: in `run()`, every request carries `tools=TOOLS`, and each turn Claude picks the next step. `loop/workflow.py` prints nothing when you save it.

What should match: after you save, no red squiggles under `from loop.agent import first_message` or `from harborline.usage import log_usage`.

### T-008: where is my order?

```text
(.venv) $ clear; python -m loop.workflow T-008
route: status  orders checked: ['HL-10196']  calls: 2
Your order HL-10196 has shipped with Parcelway (tracking number PW4974187387), and it's on its way to you in Tucson. The carrier estimates delivery for tomorrow, October 16, one day after the originally promised date of today, October 15. You can follow the package with the tracking number above on Parcelway's website.
```

How to read it:

| Part | What it means |
|---|---|
| `route: status` | Step 1: the forced `route_ticket` call's input. Claude filled in the label; our code decided the call would happen |
| `orders checked: ['HL-10196']` | Step 2: our code ran `get_customer`, then `lookup_order` on the first order ID in the ticket. Claude chose no tool |
| `calls: 2` | Two model calls, always: one to label, one to write |
| The reply | Step 3: one call with no tools, written from `ROLE`, the status task and the facts our code fetched |

What should match: `route: status`, `orders checked: ['HL-10196']`, `calls: 2`, and a reply that says the order shipped with Parcelway and gives the carrier's estimate (October 16, a day after the promised October 15). What may differ: the wording.

## Step 2: Where the path ends

```text
(.venv) $ clear; python -m loop.workflow T-004
route: refund  orders checked: ['HL-10164']  calls: 2
Your LED desk lamp from order HL-10164 is eligible for a change-of-mind return, since it was delivered on October 3 and you're within the 30-day window. The refund would be the $48 item price, and the card ending in 8423 would be refunded within 5 business days. I can't see order HL-10203 in the information I have, so please check its tracking details or send me the tracking number, and I can't issue the refund myself.
```

How to read it:

| Part | What it means |
|---|---|
| `route: refund` | One label for a ticket with three requests (return the lamp, where is HL-10203, how long do refunds take) |
| `orders checked: ['HL-10164']` | The regex in `handle()` takes the first order ID only, so the fixed path looked up one order of two |
| "I can't see order HL-10203" | Not Claude's fault: our code never looked it up. The fixed path has room for one request |

What should match: `route: refund`, `orders checked: ['HL-10164']`, `calls: 2`, and a reply about the lamp (delivered October 3, inside the 30 days, the $48 item price to the card ending 8423) that cannot say where HL-10203 is. What may differ: the wording, and whether the reply mentions the refund timing. If the router answers `other`, you'll see `route: other  orders checked: []  calls: 1` and `(sent to the human queue)`: the gate's designed path.

## Step 3: Measure, then decide

```text
(.venv) $ code experiments/m1/who_decides.py
(.venv) $ clear; python -m experiments.m1.who_decides
T-008  workflow  calls 2  orders 1/1  route: status
T-008  agent     calls 3  orders 1/1  tool calls: 2
T-003  workflow  calls 2  orders 1/1  route: refund
T-003  agent     calls 3  orders 1/1  tool calls: 2
T-014  workflow  calls 2  orders 1/1  route: refund
T-014  agent     calls 3  orders 1/1  tool calls: 2
T-006  workflow  calls 2  orders 1/1  route: status
T-006  agent     calls 3  orders 1/1  tool calls: 2
T-004  workflow  calls 2  orders 1/2  route: refund
T-004  agent     calls 3  orders 2/2  tool calls: 3

workflow  calls 10  tokens 10,553  $0.0024  orders 5/6
agent     calls 15  tokens 26,465  $0.0039  orders 6/6
```

The rows print as each ticket finishes (about 50 seconds in all in the lesson). The agent's turn-by-turn printout is silenced on purpose: only its totals count here.

How to read it:

| Part | What it means |
|---|---|
| `calls 2` / `calls 3` | Model calls per ticket. The workflow labels and writes; the agent verifies, looks up and answers, a turn each |
| `orders 1/1` | How many of the ticket's real order IDs (from Harborline's labels) the design looked up. A rough coverage check, not a quality score |
| `route: status` on T-006 | T-006 is a billing question about a shipping fee. There's no billing route, so the router picked the closest label |
| `tool calls: 2` / `3` | The `tool_use` blocks in the agent's responses: what Claude chose to call |
| T-004 `orders 1/2` vs `2/2` | The fixed path checked one order of two; Claude chose to look up both |
| The totals | Tokens are input plus output from each response's `usage`; the cost is `estimate_cost` (Lesson 0.6) on the same numbers. The workflow used about 40% of the agent's tokens |

What should match: the workflow at 2 calls per routed ticket and the agent at more; both designs looking up the order on the single-order tickets; the workflow at 1/2 on T-004; the workflow's total tokens well below the agent's. What may differ: every token count and cost; T-006's route (`status`, `refund` or `other`; with `other` its row reads `calls 1  orders 0/1  route: other`); the agent's number of calls; and whether it looks up both T-004 orders. If the agent stops on `max_tokens`, its row reads `calls 0  orders 0/N  stopped on max_tokens`, and that ticket's agent tokens are left out of the total.

## Step 4: Commit

```text
(.venv) $ git status --short
?? experiments/m1/who_decides.py
?? loop/workflow.py
(.venv) $ git add loop/workflow.py experiments/m1/who_decides.py
(.venv) $ git commit -m "Lesson 1.5: a fixed routing workflow next to the agent"
[main 1690112] Lesson 1.5: a fixed routing workflow next to the agent
 2 files changed, 154 insertions(+)
 create mode 100644 experiments/m1/who_decides.py
 create mode 100644 loop/workflow.py
(.venv) $ git push
Enumerating objects: 11, done.
Counting objects: 100% (11/11), done.
Delta compression using up to 24 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (7/7), 2.88 KiB | 2.88 MiB/s, done.
Total 7 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/YOUR-USERNAME/harborline.git
   a925cba..1690112  main -> main
```

What should match: the two `??` lines (and no `runs/` or `.env`), `2 files changed, 154 insertions(+)`, and `main -> main` to your own `harborline`. What will differ: the commit ids (yours are your own), the thread count and the sizes, and `YOUR-USERNAME`.
