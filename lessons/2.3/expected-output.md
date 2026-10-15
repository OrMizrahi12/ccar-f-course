# Expected output: Lesson 2.3, How many tools, and tool_choice

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12.3, from the `harborline` folder with `.venv` active. Every run is on Claude Haiku 5.5 (`claude-haiku-5-5`) except the second `tool_choice` run, which is on Claude Sonnet 5.5 (`claude-sonnet-5-5`). The terminal wrapped long lines; they're shown unwrapped here.

**Your runs will differ from these.** Claude doesn't answer the same way every time: a row can read 3/3 where the lesson's read 2/3, a text reply can become a question or a tool call, and token counts and costs change with every call. Each section says what should match.

## Step 1: Eighteen tools or six

```text
(.venv) $ git status --short
(.venv) $ code experiments/m2/routing_eval.py
(.venv) $ code experiments/m2/tool_count.py
```

`git status --short` prints nothing: the tree is clean after Lesson 2.2. Saving prints nothing. Line 21 of `routing_eval.py` now reads:

```python
LOOKUPS = ["get_customer", "lookup_order", "list_orders", "check_refund"]
```

```text
(.venv) $ clear; python -m experiments.m2.tool_count
R10  get_customer       3/3  2/3  (end_turn)
24/24 requests

                 6 tools   18 tools
labeled            39/48      38/48
held-out           24/24      24/24
extra picked           0          0
text replies           9         10
in per call        1,996      3,143
cost             $0.0273    $0.0400
```

While it runs, one line counts the requests as they finish (`8/24 requests`, then `9/24` and so on, on the same line). A row prints above it only where the two tool sets scored differently.

How to read it:

| Part | What it means |
|---|---|
| `R10  get_customer  3/3  2/3` | A request where the two sets disagreed: its ID, the tool it should get, then the score with 6 tools and with 18 (tries out of three that picked the right tool with the right input) |
| `(end_turn)` | What Claude did instead on the miss: here it answered in text. An extra tool's name would mean it picked one of the twelve |
| `labeled` / `held-out` | The 16 labeled requests and the 8 held-out ones from Lesson 2.1, three tries each |
| `extra picked` | How many tries picked one of the twelve extra tools |
| `text replies` | How many tries answered in text instead of calling a tool |
| `in per call` | Input tokens per call, the follow-up lookups included |
| `cost` | What each set's calls cost |

What should match: `in per call` is clearly higher with 18 tools (in the lesson, 3,143 against 1,996: about 57% more on every call), and every request finishes (`24/24`). What may differ: the scores, the rows that print, and the text replies. In the lesson, selection held: one try apart on the labeled requests, inside the "two tries or fewer is noise" line decided before the run, and no extra tool was ever picked. If your 18-tool column drops by more than that, you've measured the other half of the story; both results are worth keeping.

## Step 2: Scope tools to a role

```text
(.venv) $ code loop/agent.py
(.venv) $ pytest -q
......................................................                   [100%]
54 passed in 1.21s
```

Saving prints nothing. Lab 1's tests still pass: the loop didn't change, only what it offers. Your time will differ.

```text
(.venv) $ clear; python -m loop.agent T-003
turn 1: tool_use
  [thinking]
  [text] I'm verifying your account by email before looking at your order.
  [tool_use] get_customer {'email': 'amara.pemberton@example.com'}
  [tool_result] {"verified": true, "customer": {"customer_id": "C-1031", "na
turn 2: tool_use
  [text] Your account is verified. Next I'm pulling up order HL-10163 to check its delivery date and eligibility.
  [tool_use] lookup_order {'order_id': 'HL-10163'}
  [tool_result] {"order_id": "HL-10163", "customer_id": "C-1031", "source":
turn 3: tool_use
  [tool_use] check_refund {'order_id': 'HL-10163', 'reason': 'changed_mind', 'sku': 'SKU-1102'}
  [tool_result] {"allowed": true, "refund": 74.0, "rule": "returned within 3
turn 4: end_turn
  [text] Your return is eligible: the ceramic table lamp was delivered on October 3, within the 30-day window, and it isn't Final Sale. Under our policy, you can get a refund of $74.00 for the item price. The $6.95 shipping fee is not refunded for a change of mind. I can't issue the refund from here, but a support agent can process it, and it would go back to your card ending in 1817 within 5 business days.

History:
  user      text
  assistant thinking, text, tool_use
  user      tool_result
  assistant text, tool_use
  user      tool_result
  assistant tool_use
  user      tool_result
  assistant text
```

The agent shortens each tool result to its first characters, as in Lab 1. All the customers, orders and cards are made up.

What should match: every tool it calls is one of the five in `ROLE_TOOLS`, never `process_refund`, and it ends with `end_turn` and an answer that says what the policy allows ($74.00 for the lamp, not the shipping fee). What may differ: the number of turns, the wording, and whether it calls `check_refund` or answers from the policy text in its system prompt.

## Step 3: Who decides: tool_choice

```text
(.venv) $ code experiments/m2/tool_choice.py
(.venv) $ clear; python -m experiments.m2.tool_choice
claude-haiku-5-5

auto   end_turn  1,871 in  thinking, text
       I can help with that. Before I send it to a [...]
any    tool_use  1,991 in  tool_use
       escalate_to_human {'customer_id': 'C-1046', [...]
tool   tool_use  2,000 in  tool_use
       escalate_to_human {'customer_id': 'C-1046', [...]
none   end_turn  1,871 in  thinking, text
       I can send this to a supervisor. First I need [...]
asked  tool_use  1,944 in  thinking, tool_use
       escalate_to_human {'customer_id': 'C-1046', [...]

$0.0019
```

How to read a row: the setting, the stop reason, the input tokens, then the types of the blocks that came back, in order. Under it, each block: a text shortened to one line, or a tool call with its input. Nothing is executed.

What should match on Haiku 5.5: `any` and `tool` come back as `tool_use` with **only** a `tool_use` block (no thinking, no text before the call), and their input tokens are about 120 higher than `auto` and `none` (the docs' tool prompt for forced use: 406 tokens instead of 286); `tool` calls `escalate_to_human`, the tool it names; `none` answers in text. What may differ: `auto` may call a tool instead of asking first (that's what auto means: Claude decides); `any` may pick another tool; `asked` usually calls `escalate_to_human` and may or may not write a sentence first.

```text
(.venv) $ python -m experiments.m2.tool_choice claude-sonnet-5-5
claude-sonnet-5-5

auto   end_turn  1,871 in  thinking, text
       I can pass this to a person. First I need a [...]
any    400  tool_choice: type "tool" and "any" are not
            supported for this model.
tool   400  tool_choice: type "tool" and "any" are not
            supported for this model.
none   end_turn  1,871 in  thinking, text
       I can send this to a supervisor. I need two [...]
asked  tool_use  1,944 in  thinking, tool_use, tool_use
       get_customer {}
       list_orders {'customer_id': 'C-1046'}

$0.0193
```

What should match on Sonnet 5.5 today: `any` and `tool` print `400` with exactly that message. The request is rejected before anything runs: no response comes back, so nothing is logged and the cost line counts only the other three rows. What may differ: `asked` may call `escalate_to_human`, as it did on Haiku, or, as in the lesson, two lookups in parallel instead of the tool it names. Asking steers; it doesn't guarantee. That's why code should check for the `tool_use` block, and its name, before relying on it.

If `any` and `tool` are accepted on Sonnet 5.5 when you run this, the API has changed since the lesson: check the forced tool use table on the Define tools page.

## Step 4: Commit

```text
(.venv) $ git status --short
 M experiments/m2/routing_eval.py
 M loop/agent.py
?? experiments/m2/tool_choice.py
?? experiments/m2/tool_count.py
(.venv) $ git add experiments/m2 loop/agent.py
(.venv) $ git commit -m "Lesson 2.3: tool count, a role tool list, tool_choice settings"
[main a68247e] Lesson 2.3: tool count, a role tool list, tool_choice settings
 4 files changed, 163 insertions(+), 3 deletions(-)
 create mode 100644 experiments/m2/tool_choice.py
 create mode 100644 experiments/m2/tool_count.py
(.venv) $ git push
...
To https://github.com/YOUR-USERNAME/harborline.git
   7f2daa1..a68247e  main -> main
```

What should match: `4 files changed, 163 insertions(+), 3 deletions(-)` if you typed the files exactly as the kit has them, and `main -> main` to your own repository. What differs: the commit IDs, the push's object counts, and the URL (your GitHub account). `runs/` and `__pycache__/` aren't listed: they're ignored.
