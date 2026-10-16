# Lab 3: the support agent, measured on every ticket

Claude Certified Architect – Foundations (CCAR-F) · Module 3: Agents with the Claude Agent SDK: the Support Resolution Agent · the module checkpoint

In Module 3 you built Harborline's support agent with the Agent SDK. It verifies the customer before it touches an order, sends refunds above $500 to a person, hands over a structured case, and keeps the case facts outside the summary. In Lesson 3.2 you measured it on the 20 dev tickets. In this lab you measure it on all 50 labeled tickets, including the customer's follow-up answers. Then you fix what that run finds, and run the Module 1 loop against harborline-mcp, so you see the same rules hold when you write the loop yourself.

You pass the lab when the self-check tests pass and one full run reaches the target: **first-contact resolution of at least 80% (40 of 50), escalation recall 100% (8 of 8), and no wrong refunds.**

## What you start from

`starter/` is the `harborline` project exactly as it stands after Lesson 3.8: the Module 1 loop, harborline-mcp from Module 2, and `support/` from Lessons 3.1 to 3.8 (agent, evaluation, gates, hooks, hand-off, case facts, sessions). If your own project is there too, keep working in it. If not, copy `starter/` to `~/projects/harborline`, create the virtual environment, install `requirements.txt`, and add your `.env` with `ANTHROPIC_API_KEY` and `HARBORLINE_API_TOKEN` (Lessons 0.4, 0.6 and 2.6 show how).

`solution/` is a finished version to compare with when you're done. `tests/` holds the self-check, in two files.

## What you change

- `support/agent.py`: `handle()` can continue a session.
- `support/evaluate.py`: every split, each follow-up in the same session, totals per split, and the target.
- `harborline/policy.py`, `harborline/backend.py`, `loop/tools.py`: the refund fixes the full run asks for.
- `support/gates.py`, `support/tools.py`: `list_orders`, behind the gate.
- `loop/mcp_agent.py`: new. The Module 1 loop, with its tools from harborline-mcp over stdio.

Keep the system prompt and the hooks as they are. The run measures what you built in Module 3.

## Steps

### 1. Send the follow-ups (Lesson 3.8)
Some tickets need a second message. T-015 and T-037 come from a "Jordan Lee", and two customers have that name. The agent is right to ask for an email, and the ticket's `follow_ups` list holds the answer. Lesson 3.2's `evaluate.py` never sends it, so those tickets can't be solved.

Give `handle()` a `resume=None` parameter. When it has a session ID, copy `OPTIONS` with `dataclasses.replace(OPTIONS, resume=resume)` and don't call `gates.start_case()`: it's the same conversation, so the customer verified in the first message stays verified. In `evaluate.py`, write `conversation(ticket)`. It handles the first message, then sends each follow-up with `resume=` the session ID from the last `ResultMessage`. It returns the tools called and the total cost.

### 2. Measure every ticket (Lesson 3.2)
Add `--split dev|test|all` with `argparse` (default `dev`, so Lesson 3.2's command still works). Collect one row per ticket (split, label outcome, verdict, wrong refunds, cost), and add:

- `totals(rows)`: tickets, resolved, how many needed a person, how many got one, wrong refunds, cost.
- `meets(totals)`: FCR at least 80%, escalation recall 100%, no wrong refunds. Keep the numbers in one `TARGET` dict.
- A line per split, then the whole run, then `PASS` or `FAIL`.

Keep `grade()` as it is. Then run it once (about $0.04):

```bash
python -m support.evaluate --split all
```

Our run before any fix: `all FCR 38/50 (76%) · escalation recall 8/8 · wrong refunds 2 · $0.0378`, **FAIL**. Dev was 16/20 and test 22/30. The escalations were all right. Four tickets missed: T-015 and T-037 (`refund missing`), and T-032 and T-039 (`escalated, could resolve`, with a wrong refund each).

FCR counts every ticket, including the 8 that need a person, so the most it can reach is 42/50 (84%).

### 3. Read the misses before you change anything (Lesson 3.2)
Run one of them alone and read what the tools returned:

```bash
python -m support.agent T-032
```

In our runs on T-032, a smashed mixing bowl, Claude called `process_refund` for the full $44.95 without a SKU. The error said `item None is not on this order`. It tried again with the SKU but only for the item ($38.00), and that went through. A second call for the $6.95 shipping fee, again without a SKU, failed, and it escalated the rest. The policy allows one refund of item plus shipping. The agent paid a partial refund, and a person had to finish the case.

T-015 and T-037 fail for a different reason. With the email the agent verifies Jordan Lee, then asks for an order number, because it has no tool that lists a customer's orders.

### 4. Make the refund errors say what to fix (Lesson 2.4)
- `harborline/policy.py`, in `check_refund`: before looking up the item, when `sku` is `None` for an item reason, return the rule `a refund for an item needs its SKU: get it from lookup_order`. An error should say what's wrong and how to fix it. `item None` does neither.
- `loop/tools.py`, `PROCESS_REFUND`'s description: add that a damaged, defective or wrong item is **one** refund, the item price plus the order's shipping fee, with the item's SKU.
- `harborline/backend.py`, in `process_refund`: refunds on one order must never add up to more than the order cost. Sum the refunds already made on the order. If this one would go past the total, raise `PolicyViolation` and say how much is left. Each call already checks the policy's maximum. This one checks across calls, because a retried or split refund passes every per-call check.

### 5. Give the agent `list_orders`, behind the gate (Lesson 3.3)
`LIST_ORDERS` exists in `loop/tools.py`, and harborline-mcp serves it, but the Module 3 agent never got it. In `support/gates.py`, add `list_orders(customer_id)`: refuse with `PermissionDenied` until a customer is verified, and refuse any other customer's ID. Then add the tool in `support/tools.py` with `LIST_ORDERS`'s description and schema, calling the gate, and put it in `TOOLS`. `NAMES` follows by itself.

Run the full evaluation again. Our run: `dev 17/20`, `test 25/30`, `all FCR 42/50 (84%) · escalation recall 8/8 · wrong refunds 0 · $0.0376`, **PASS**. T-032 and T-039 now take one `process_refund` each. T-015 and T-037 go `get_customer`, then `list_orders`, `lookup_order` and `process_refund` after the email arrives.

### 6. The same rules in your own loop (Lessons 1.4, 2.5, 3.3 and 3.4)
The Agent SDK runs the loop for you. Write it once more by hand, the way Lesson 1.4 did, with the tools coming from harborline-mcp, a separate process over stdio. Create `loop/mcp_agent.py`:

1. `server()`: a `StdioServerParameters` that runs `python -m mcp_server.server` from the project folder. Its environment is `get_default_environment()` plus `HARBORLINE_API_TOKEN` only. The server never needs your Anthropic key, so don't pass it.
2. The tools: the server's four, each through Lab 2's `as_api_tool`, plus `escalate_to_human` with Lesson 3.6's `HANDOFF` schema. The hand-off runs in your process, not on the server.
3. `guard(call, case)`: the rules that run before a call reaches the server, whatever Claude decided. No order tool until `get_customer` has verified someone. No `process_refund` above `REFUND_LIMIT`: return an error that sends Claude to `escalate_to_human`. These are Lesson 3.3's gate and Lesson 3.4's hook, written in your own loop.
4. `run_call(session, call, case)`: the guard first, then the call through `session.call_tool`. When the result is an error with `"isRetryable": true` (Lesson 2.4), try once more. Remember the verified customer from `get_customer`.
5. `run(client, session, tools, messages, case)`: Lesson 1.4's loop, made async, with a branch for every stop reason. Use the Module 3 system prompt (`support.agent.SYSTEM`).

Then run it on a ticket that needs a person, and on one with two requests:

```bash
python -m loop.mcp_agent T-046
python -m loop.mcp_agent T-016
```

In our runs: T-046 (a $549.00 espresso machine, damaged) went `get_customer` and `lookup_order`, then `escalate_to_human` with every hand-off field filled, then `end_turn`. T-016 verified, looked up both orders in one turn, refunded $39.00 for the pillow, and answered both questions. The rehearsal runs of this step (four tickets) cost $0.0067 in all.

## Check your work

1. Copy `labs/L3/tests/test_lab3.py` and `labs/L3/tests/test_lab3_loop.py` into your project's `tests/`, and run the whole suite:
   ```bash
   python -m pytest -q
   ```
   Our solution: `94 passed` (the starter's 71 tests plus the lab's 23). Before your changes, 7 of the 17 tests in `test_lab3.py` fail, and `test_lab3_loop.py` can't even import until `loop/mcp_agent.py` exists. The other 10 already pass: they guard the gate, the refund-limit hook and `grade()` from Lessons 3.2 to 3.4, so nothing in this lab can quietly break them. Neither file needs a key, and neither costs anything. They cover:
   - the missing-SKU message, the one-refund line in the tool description, and a second refund that would go past the order total
   - `list_orders` behind the gate: nobody verified, someone else's orders, then the right two orders for C-1042
   - the refund-limit hook called directly: `600`, `"600"` and `500.01` denied with a pointer to `escalate_to_human`; `500` and `44.95` allowed
   - follow-ups sent with `resume=` and the same session ID, and a resumed session keeping the verified customer
   - `grade()` and the target: recall below 100% fails, and so does one wrong refund
   - the loop, with a fake Claude and the real server in memory: an order lookup before verification never runs; $549 is redirected and nothing is paid; HL-10211's one timeout gets a second try and succeeds; the hand-off is recorded; an unknown stop reason raises `LoopStopped`
2. Run the full evaluation once (about $0.04) and check the last line says `PASS`. Your numbers will differ a little from ours. If a ticket misses, run it alone with `python -m support.agent <ticket>` and read the tool results before you change the prompt.

## Compare with the solution

`solution/support/evaluate.py`, `solution/support/agent.py`, `solution/support/gates.py`, `solution/support/tools.py`, `solution/harborline/policy.py`, `solution/harborline/backend.py`, `solution/loop/tools.py` and `solution/loop/mcp_agent.py` are one way to do it. Other designs pass too. For example, you could keep the follow-ups in `handle()` itself, or cap refunds per item instead of per order.

## Commit

```bash
git add support harborline loop tests
git commit -m "Lab 3: every ticket with its follow-ups, one refund per damaged item, list_orders behind the gate, the loop over harborline-mcp"
git push
```
