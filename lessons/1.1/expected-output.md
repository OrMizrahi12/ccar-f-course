# Expected output: Lesson 1.1, How Claude reads a request

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12.3 and Claude Haiku 5.5 (`claude-haiku-5-5`), from the `harborline` folder with `.venv` active. The terminal wrapped long lines; they're shown unwrapped here.

**Your numbers and replies will differ from these, run to run.** Token counts are estimates and can change when the tokenizer changes; Claude's replies, its thinking tokens and its output tokens change every time you run a request. Each section says what should match.

## Step 1: Count

```text
(.venv) $ git status --short
(.venv) $ mkdir -p experiments/m1
(.venv) $ code experiments/m1/budget.py
(.venv) $ python -m experiments.m1.budget
claude-haiku-5-5: window 1,000,000, max output 128,000
role                          59 tokens   0.01%
role + policy                664 tokens   0.07%
role + policy + orders    73,323 tokens   7.33%
```

`git status --short` prints nothing: the tree is clean after Lesson 0.6.

How to read it:

| Line | What it means |
|---|---|
| `window 1,000,000` | The model's context window, from the Models API (`max_input_tokens`): 1M tokens on Claude Haiku 5.5 |
| `max output 128,000` | The largest `max_tokens` one request may ask for (the Models API's `max_tokens`) |
| `role  59 tokens  0.01%` | The one-sentence role as the system prompt, plus the customer's ticket as the user turn: 59 input tokens, 0.01% of the window |
| `role + policy  664 tokens` | The same request with Harborline's refund policy added to the system prompt |
| `role + policy + orders  73,323 tokens  7.33%` | The same request with all 213 orders added too |

What should match: the window (1,000,000) and the max output (128,000), unless Anthropic changes the model's limits; three lines in that order, each bigger than the one before, with the third around 7% of the window. What may differ: the token counts, slightly (the count is an estimate). The counts are free and don't run the model.

On Claude Haiku 5.5 ($0.10 per million input tokens), sending the third version once costs about $0.0073 in input; the second, about $0.00007. Same question, about 110 times the price, on every request.

## Step 2: Send

### With `MAX_TOKENS = 1024`

```text
(.venv) $ code experiments/m1/first_request.py
(.venv) $ python -m experiments.m1.first_request
[thinking]
[text] You can return the ceramic table lamp for a refund of the item price within 30 days of delivery, as long as it isn't marked Final Sale, but the original shipping fee won't be refunded. Once the return is approved, the refund goes to your original payment method within 5 business days.
stop_reason: end_turn
output 179 of 1024 (thinking 91), input 677
```

How to read it:

| Line | What it means |
|---|---|
| `[thinking]` | A thinking content block. Claude Haiku 5.5 thinks by default and doesn't return the thinking text, so nothing follows the label, but its tokens are billed as output |
| `[text] You can return…` | The answer, a text content block: two sentences, because the system prompt says "Answer in two sentences or fewer." |
| `stop_reason: end_turn` | Claude finished on its own |
| `output 179 of 1024 (thinking 91)` | 179 output tokens against a ceiling of 1,024; 91 of them were thinking |
| `input 677` | The system prompt (role, rule, refund policy) plus the ticket |

What should match: a `[text]` reply of at most two sentences about returning the lamp, `stop_reason: end_turn`, output far below 1024, and input close to 677. What may differ: the wording of the reply, the output and thinking tokens (in other runs of the same request the thinking ranged from 91 to 146 tokens), and the `[thinking]` line itself: on some runs Claude may not think at all.

### With `MAX_TOKENS = 40`

Line 8 changed to `MAX_TOKENS = 40  # the ceiling for this reply, thinking included`, saved, and run again:

```text
(.venv) $ python -m experiments.m1.first_request
[thinking]
stop_reason: max_tokens
output 40 of 40 (thinking 40), input 677
```

No `[text]` line at all: thinking used the whole 40-token budget, and the reply stopped before any answer. `stop_reason: max_tokens` says it was cut off, not finished.

What should match: `stop_reason: max_tokens` and `output 40 of 40`. What may differ: if that run thinks for fewer than 40 tokens, you see a `[text]` line cut off mid-sentence instead, and the thinking count is below 40. Either way, the cap stopped the reply; it didn't make it shorter.

Then line 8 back to `MAX_TOKENS = 1024`, and save.

## Step 3: Converse

```text
(.venv) $ code experiments/m1/stateless.py
(.venv) $ python -m experiments.m1.stateless
--- first request: messages=1, input_tokens=66
I'm sorry, I don't have access to your order details or Harborline's return policy here, so I can't confirm refund eligibility for HL-10163. Please check the returns section of your order confirmation email or the Harborline website, or contact our support team with your order number so they can walk you through the return and refund process.

--- new request, no history: messages=1, input_tokens=38
I don't see an order number or any order details in our conversation so far. If you share your order number, or the item name and approximate purchase date, I'll help you look into it.

--- new request, full history: messages=3, input_tokens=255
You mentioned order HL-10163, for the ceramic table lamp. Please include that number when you contact our support team so they can locate it quickly.
```

How to read it:

| Request | What was sent | What came back |
|---|---|---|
| `first request` | The system prompt and the ticket: 1 message, 66 input tokens | A reply to the ticket. This system prompt is only "You are Harborline's support assistant. Reply in two sentences.", with no refund policy, so Claude says it can't confirm eligibility |
| `new request, no history` | Only "Which order did I mention?": 1 message, 38 input tokens | Claude has no order number: nothing from the first request was kept |
| `new request, full history` | The ticket, Claude's first reply exactly as it came back, and the question: 3 messages, 255 input tokens | Claude names HL-10163, the order from the ticket |

What should match: `messages=1`, `messages=1`, `messages=3`; the no-history reply has no order number; the full-history reply names **HL-10163**; and the third request's input tokens are several times the second's. What may differ: every reply's wording, and the input tokens of the third request (they include Claude's first reply, which changes from run to run; in other runs they ranged from about 195 to 255). The first two input counts should be at or near 66 and 38.

## Saving your work

```text
(.venv) $ git add experiments
(.venv) $ git commit -m "Lesson 1.1: count, send and converse experiments"
[main fec1387] Lesson 1.1: count, send and converse experiments
 3 files changed, 103 insertions(+)
 create mode 100644 experiments/m1/budget.py
 create mode 100644 experiments/m1/first_request.py
 create mode 100644 experiments/m1/stateless.py
(.venv) $ git push
Enumerating objects: 8, done.
Counting objects: 100% (8/8), done.
Delta compression using up to 24 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (7/7), 2.06 KiB | 351.00 KiB/s, done.
Total 7 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/YOUR-USERNAME/harborline.git
   81d60e9..fec1387  main -> main
```

What should match: `3 files changed, 103 insertions(+)` (if you typed the files exactly as in the kit), the three `create mode` lines, and `main -> main` to your own `harborline`. What will differ: the commit ids (`fec1387`, and `81d60e9` before it, are the lesson's), your GitHub username, the thread count and the speed.

## What to compare with yours

- `budget.py` prints a 1,000,000-token window and three growing counts, the last one around 7% of the window.
- `first_request.py` at 1024 ends with `end_turn` and a short reply; at 40 it ends with `max_tokens`.
- `stateless.py` can't name the order without the history, and names HL-10163 with it.
- `MAX_TOKENS` is back at 1024 before you commit.
- `git push` sends the commit to your own `harborline`, never to the starter.
