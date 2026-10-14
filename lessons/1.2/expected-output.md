# Expected output: Lesson 1.2, Reading the response

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12.3 and Claude Haiku 5.5 (`claude-haiku-5-5`), from the `harborline` folder with `.venv` active. The terminal wrapped long lines; they're shown unwrapped here.

**Your replies, numbers and IDs will differ from these, run to run.** Claude's replies, whether it thinks, its thinking tokens and its output tokens change every time you send a request, and every message ID, request ID and tool-use ID is new. Each section says what should match.

## Step 1: Log every call

```text
(.venv) $ git status --short
(.venv) $ code harborline/usage.py
```

`git status --short` prints nothing: the tree is clean after Lesson 1.1. `usage.py` is typed and saved; nothing runs yet.

## Step 2: Read a reply

### The `plain` case

```text
(.venv) $ clear; python -m experiments.m1.read_response plain
[thinking] 0 characters, signature 980 characters
[text] I can't look up order HL-10196 from here, so I don't have its shipping status. Please check your order confirmation email for tracking details, or contact Harborline support with your order number for an update.
usage: {"cache_creation":{"ephemeral_1h_input_tokens":0,"ephemeral_5m_input_tokens":0},"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"inference_geo":"global","input_tokens":68,"output_tokens":104,"output_tokens_details":{"thinking_tokens":44},"service_tier":"standard"}
stop_reason: end_turn
message id: msg_011Cg1WLi1ZzxU3kbnym9ras
request id: req_011Cg1WLgoeEBEtr3KXK9Wvy
next step: done: use the text
logged: runs/usage.jsonl, about $0.000059
```

How to read it:

| Line | What it means |
|---|---|
| `[thinking] 0 characters, signature 980 characters` | A thinking content block came first. Claude Haiku 5.5 doesn't return the thinking text by default, so the text is empty; the signature is what you send back unchanged in a later turn. Its tokens are billed as output |
| `[text] I can't look up order HL-10196…` | The answer, a text block. Without a tool, Claude can't look anything up, so it points to the confirmation email or support. That's a correct `end_turn`, and a sign the system needs a tool |
| `usage: {…}` | The `usage` object exactly as returned, on one line |
| `"input_tokens":68` | The prompt tokens that weren't read from or written to the cache. Here nothing is cached (`cache_creation_input_tokens` and `cache_read_input_tokens` are 0), so 68 is the whole prompt |
| `"output_tokens":104` … `"thinking_tokens":44` | 104 output tokens, 44 of them thinking: the output includes the thinking |
| `stop_reason: end_turn` | Claude finished on its own |
| `message id: msg_…` | The message's own ID: it names the message, not the call |
| `request id: req_…` | The request ID, from the `request-id` response header: it names this one API call. Support asks for it |
| `next step: done: use the text` | `next_step()` decided from `stop_reason` |
| `about $0.000059` | 68 × $0.10 + 104 × $0.50, per million tokens, on Claude Haiku 5.5 |

What should match: a short `[text]` reply saying it can't look up the order, `stop_reason: end_turn`, `next step: done: use the text`, both cache fields 0, `input_tokens` close to 68, and two different IDs (`msg_…` and `req_…`). What may differ: the reply's wording, the output and thinking tokens, the IDs, and the `[thinking]` line itself: Claude Haiku 5.5 decides per request whether to think, so on some runs there is no `[thinking]` line and `thinking_tokens` is 0.

### The `tool` case

```text
(.venv) $ clear; python -m experiments.m1.read_response tool
[tool_use] lookup_order {'order_id': 'HL-10196'} id=toolu_01PCHXshTNqCKvvvRFTf77U5
usage: {"cache_creation":{"ephemeral_1h_input_tokens":0,"ephemeral_5m_input_tokens":0},"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"inference_geo":"global","input_tokens":443,"output_tokens":55,"output_tokens_details":{"thinking_tokens":0},"service_tier":"standard"}
stop_reason: tool_use
message id: msg_011Cg1WNvN2rfG9nbMF81Pvd
request id: req_011Cg1WNv2CCxztMRaSx1W9P
next step: run the tool, then send its result back (Lesson 1.3)
logged: runs/usage.jsonl, about $0.000072
```

How to read it:

| Line | What it means |
|---|---|
| `[tool_use] lookup_order {'order_id': 'HL-10196'} id=toolu_…` | No thinking, no text: one `tool_use` block. Claude asks us to run `lookup_order` with this input. Nothing is executed here |
| `"input_tokens":443` | Up from 68: the tool definition, plus the tool-use system prompt the API adds when tools are present (286 tokens on Claude Haiku 5.5) |
| `stop_reason: tool_use` | The reply isn't an answer: it's a request to act |
| `next step: run the tool…` | Code that only looked for text would have sent the customer nothing |

What should match: a `[tool_use] lookup_order` line with `'order_id': 'HL-10196'`, `stop_reason: tool_use`, and an input several hundred tokens higher than the `plain` case. What may differ: a short `[text]` line (such as "I'll look that up") or a `[thinking]` line before the tool call, the output tokens and the IDs.

### The `next_step()` code and the log

In the editor, `next_step()` starts at line 47 of `read_response.py`: a `match` on `response.stop_reason` with a branch for `end_turn`, `tool_use`, `max_tokens`, `pause_turn` and `refusal`, and a catch-all.

```text
(.venv) $ code runs/usage.jsonl
```

```json
{"time": "2026-10-14T04:34:39+00:00", "label": "1.2 plain", "request_id": "req_011Cg1WLgoeEBEtr3KXK9Wvy", "model": "claude-haiku-5-5", "stop_reason": "end_turn", "input_tokens": 68, "cache_read_tokens": 0, "cache_write_tokens": 0, "output_tokens": 104, "thinking_tokens": 44, "cost_usd": 5.88e-05}
{"time": "2026-10-14T04:35:09+00:00", "label": "1.2 tool", "request_id": "req_011Cg1WNv2CCxztMRaSx1W9P", "model": "claude-haiku-5-5", "stop_reason": "tool_use", "input_tokens": 443, "cache_read_tokens": 0, "cache_write_tokens": 0, "output_tokens": 55, "thinking_tokens": 0, "cost_usd": 7.18e-05}
```

One line per call. `cost_usd` is in dollars; small values print in e-notation (`5.88e-05` = $0.0000588). What should match: one line per run you made, each with a `req_…` request ID and the same fields in the same order. If you ran the cases more than once, you have more lines: the log only grows. In the Explorer, the `runs` folder is dimmed: git ignores it.

## Step 3: Chat, turn by turn

```text
(.venv) $ code experiments/m1/conversation.py
(.venv) $ clear; python -m experiments.m1.conversation

You: Hi, I'm Elijah. Can I cancel order HL-10196 before it ships?
Claude: Yes, Elijah. An order that hasn't shipped yet can be cancelled for a full refund, shipping included. Once it has shipped, it can't be cancelled, but you can return it when it arrives.
  [end_turn] 676 in, 68 out (0 thinking), 2 messages kept

You: And if it already shipped?
Claude: If it has already shipped, it can't be cancelled, but you can return it once it arrives. Returns for changed minds cover most items within 30 days of delivery, and the original shipping fee isn't refunded in that case. If the item arrives damaged, defective, or not what you ordered, let us know within 30 days of delivery and we'll refund the item price and the shipping fee.
  [end_turn] 754 in, 120 out (0 thinking), 4 messages kept

You: How long will the refund take?
Claude: Refunds go back to the original payment method within 5 business days. If the order was paid with a Harborline gift card, the refund is issued as store credit instead.
  [end_turn] 884 in, 50 out (0 thinking), 6 messages kept

You: quit
History: user, assistant, user, assistant, user, assistant
```

How to read it:

| Turn | Messages sent | Input tokens | What it shows |
|---|---|---|---|
| 1 | 1 (the question) | 676 | The system prompt with the whole refund policy, plus the question |
| 2 | 3 (question, reply, new question) | 754 | Only answerable because turn 1 is in the history. 754 − 676 = turn 1's 68-token reply plus the new question |
| 3 | 5 | 884 | The input grows again: every turn re-sends everything before it |

`2 / 4 / 6 messages kept` counts the list after the reply is appended. `History:` prints the roles in order: user and assistant, alternating, only ever appended to.

What should match: three `end_turn` answers that follow the refund policy (cancel before shipping for a full refund; return within 30 days once shipped; refunds within 5 business days), `2 / 4 / 6 messages kept`, an input that grows every turn, and the alternating history. What may differ: the wording and length of each answer, the token counts, and thinking: no turn thought in the lesson's run, but yours may. If a turn thinks, its thinking block is stored with the reply and counts as input on every later turn too.

## Step 4: Commit

```text
(.venv) $ git status --short
?? experiments/m1/conversation.py
?? experiments/m1/read_response.py
?? harborline/usage.py
(.venv) $ git add harborline/usage.py experiments/m1/read_response.py experiments/m1/conversation.py
(.venv) $ git commit -m "Lesson 1.2: read responses, handle stop reasons, log usage"
[main aee226e] Lesson 1.2: read responses, handle stop reasons, log usage
 3 files changed, 158 insertions(+)
 create mode 100644 experiments/m1/conversation.py
 create mode 100644 experiments/m1/read_response.py
 create mode 100644 harborline/usage.py
(.venv) $ git push
...
To https://github.com/YOUR-USERNAME/harborline.git
   fec1387..aee226e  main -> main
```

What should match: three `??` lines and no `runs/` (it's ignored), `3 files changed, 158 insertions(+)` (39 + 82 + 37 lines), and `main -> main` to your own `harborline`. What differs: the commit ids, your username, and the push's object counts.
