# Expected output: Lesson 1.3, Tool use from first principles

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12.3 and Claude Haiku 5.5 (`claude-haiku-5-5`), from the `harborline` folder with `.venv` active. The terminal wrapped long lines; they're shown unwrapped here.

**Your numbers and replies will differ from these, run to run.** Claude decides each time whether to think, whether to write a sentence before it calls a tool, and whether to ask for both tools in one response; its wording and the token counts change too. The four-character ids at the end of each `[tool_use]` and `[tool_result]` line are random. Each section says what should match.

## Step 1: Define

```text
(.venv) $ git status --short
(.venv) $ mkdir loop
(.venv) $ code loop/tools.py
```

`git status --short` prints nothing: the tree is clean after Lesson 1.2. `loop/tools.py` prints nothing either: it is data and one function. You type lines 1-40 here (the docstring, the imports, `GET_CUSTOMER`, `LOOKUP_ORDER`, `TOOLS` and `HANDLERS`), and `run_tool` (lines 43-54) at the start of step 2.

What should match: VS Code shows `loop/tools.py` in the Explorer, and after you save, no red squiggles under `from harborline import backend`.

## Step 2: Round trip

```text
(.venv) $ code experiments/m1/manual_tool_call.py
(.venv) $ clear; python -m experiments.m1.manual_tool_call
--- tool_use, 604 tokens in
[thinking]
[tool_use] get_customer {'email': 'elijah.petrov@example.com'} id wWyB
[tool_use] lookup_order {'order_id': 'HL-10196'} id Ayn3
[tool_result] id wWyB is_error=False {"verified": true, "customer": {"customer_id"
[tool_result] id Ayn3 is_error=False {"order_id": "HL-10196", "customer_id": "C-10
--- end_turn, 1,168 tokens in
[thinking]
[text] Hi Elijah, order HL-10196 has shipped with Parcelway (tracking number PW4974187387) and is estimated to arrive by October 16, 2026. You can track it on the Parcelway website using that number, and I'm sorry the shipping email hasn't reached you yet.
```

How to read it:

| Line | What it means |
|---|---|
| `--- tool_use, 604 tokens in` | The first response stopped with `stop_reason` `tool_use`: Claude is asking for tools, not answering. The request was 604 input tokens: the system prompt, the two tool definitions (plus the tool prompt the API adds) and the ticket |
| `[thinking]` | A thinking block. Claude Haiku 5.5 thinks when it decides to and doesn't return the thinking text, so nothing follows the label |
| `[tool_use] get_customer {...} id wWyB` | Claude's first request: run `get_customer` with this input. `id` shows the last four characters of the block's `id` |
| `[tool_use] lookup_order {...} id Ayn3` | Its second request, in the same response: two independent lookups, asked for together |
| `[tool_result] id wWyB is_error=False ...` | Your code ran the call and built its `tool_result`, tied to the call by `tool_use_id` (same last four characters). The script prints only the first 45 characters of the content |
| `[tool_result] id Ayn3 is_error=False ...` | The order, from Harborline's backend. Both results go back together, in one user turn |
| `--- end_turn, 1,168 tokens in` | The second response finished on its own. It cost more input: the tools again, Claude's previous turn and both results |
| `[text] Hi Elijah, ...` | The answer, written from the data your code sent back |

What should match: a first response with `--- tool_use`, `[tool_use]` lines for `get_customer` (the email `elijah.petrov@example.com`) and `lookup_order` (`HL-10196`), one `[tool_result]` line per call with `is_error=False`, then `--- end_turn` and an answer saying the order has shipped with Parcelway. In other runs of the same request the first request was 604 tokens every time and the second 1,131 to 1,170. What may differ: the `[thinking]` lines (present or not), the ids, the token counts a little, and the wording of the answer. If Claude calls one tool per response instead of two, see the README's troubleshooting.

## Step 3: Report a failure

```text
(.venv) $ clear; python -m experiments.m1.manual_tool_call bad
--- tool_use, 592 tokens in
[tool_use] get_customer {'email': 'elijah.petrov@example.com'} id aeMD
[tool_use] lookup_order {'order_id': '12345'} id YZeF
[tool_result] id aeMD is_error=False {"verified": true, "customer": {"customer_id"
[tool_result] id YZeF is_error=True '12345' is not an order ID. Order IDs look li
--- end_turn, 900 tokens in
[thinking]
[text] Thanks, Elijah, your account is verified. Order 12345 isn't in our system because Harborline order IDs look like HL-10234, so could you send the ID from your confirmation email (it should start with "HL-")?
```

How to read it:

| Line | What it means |
|---|---|
| `[tool_use] lookup_order {'order_id': '12345'}` | Claude passed the order number exactly as the customer wrote it. The schema says so; checking IDs is your code's job |
| `[tool_result] id YZeF is_error=True '12345' is not ...` | The backend raised a `BackendError`; `run_tool` turned it into a `tool_result` with `is_error: true` and the backend's message. The preview stops at 45 characters; the full message is `'12345' is not an order ID. Order IDs look like HL-10234.` |
| `--- end_turn, 900 tokens in` | Claude read both results in its next turn and answered. Nothing crashed |
| `[text] Thanks, Elijah, ...` | The failure became information: Claude asks the customer for the right ID |

What should match: `lookup_order` called with `'12345'`, its `[tool_result]` line with `is_error=True`, the other result with `is_error=False`, and a reply that asks for the order ID. What may differ: Claude may call `lookup_order` with `'HL-12345'` instead; the backend then says `Order HL-12345 does not exist.`, still with `is_error=True`. Or the second response may be another `--- tool_use` with a corrected call: Claude retrying from your error message. The script stops after the second response, so that call isn't run; answering again and again is the loop of Lesson 1.4.

Then commit and push:

```text
(.venv) $ git status --short
?? experiments/m1/manual_tool_call.py
?? loop/
(.venv) $ git add loop experiments/m1/manual_tool_call.py
(.venv) $ git commit -m "Lesson 1.3: tool definitions and a tool round trip by hand"
[main 2f5b6f5] Lesson 1.3: tool definitions and a tool round trip by hand
 2 files changed, 120 insertions(+)
 create mode 100644 experiments/m1/manual_tool_call.py
 create mode 100644 loop/tools.py
(.venv) $ git push
Enumerating objects: 10, done.
Counting objects: 100% (10/10), done.
Delta compression using up to 24 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (7/7), 2.15 KiB | 2.15 MiB/s, done.
Total 7 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/YOUR-USERNAME/harborline.git
   aee226e..2f5b6f5  main -> main
```

What should match: `git status --short` lists the two new paths and not `runs/` (it's ignored, and it holds the usage log from Lesson 1.2, which now has this lesson's calls too); `2 files changed, 120 insertions(+)` (54 + 66 lines); `main -> main` to your own `harborline`. What differs: the commit ids, the thread count and the transfer numbers.
