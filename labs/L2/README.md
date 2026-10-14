# Lab 2: harborline-mcp, hardened and measured

Claude Certified Architect – Foundations (CCAR-F) · Module 2: Tool Design & MCP Integration · the module checkpoint

In Lessons 2.5 and 2.6 you built harborline-mcp: four tools, two resources and a prompt, started by Claude Code with a token from the environment. In this lab you finish it the way a production server needs. You close a validation gap in the refund tool, publish one more catalog as a resource, and prove two things: every error comes back with a category, and Claude still picks the right tool when the tool list comes from the server.

You pass the lab when the self-check tests pass and one real routing run gets at least 90% of the held-out requests right.

## What you start from

`starter/` is the `harborline` project exactly as it stands after Lesson 2.7: the Module 1 loop, the tools and descriptions from Lessons 2.1 to 2.4, `mcp_server/server.py` (2.5, with the token check from 2.6), `.mcp.json` (2.6) and the experiments from both modules. If your own project is there too, keep working in it. If not, copy `starter/` to `~/projects/harborline`, create the virtual environment, install `requirements.txt`, and add your `.env` with `ANTHROPIC_API_KEY` and `HARBORLINE_API_TOKEN` (Lessons 0.4, 0.6 and 2.6 show how).

`solution/` is a finished version to compare with when you're done. `tests/` holds the self-check.

## What you change

- `harborline/backend.py`: one check in `process_refund`.
- `mcp_server/server.py`: one new resource.
- `experiments/m2/mcp_routing.py`: a new file.
- `tests/test_mcp_server.py`: one line, because the server now has three resources.

Keep the four tools, their names and their descriptions as they are. The routing run measures the descriptions you wrote in Lessons 2.1 and 2.2, now served over MCP.

## Steps

### 1. Find the bug first (Lesson 2.4)
Start a Python shell in the project and ask the backend for a refund that should never happen:

```python
from harborline import backend
backend.process_refund("HL-10163", -20.0, "damaged", sku="SKU-1102")
```

It comes back with `"status": "processed"`. So does an amount of `0.0`. The policy check only asks whether the amount is too large, so a negative or zero amount slips through. Call `backend.reset()` afterwards to clear the refunds you made.

### 2. Reject an amount of $0 or less (Lesson 2.4)
At the top of `process_refund`, before it looks anything up, raise `InvalidRequest("A refund amount must be more than $0.")` when `amount <= 0`. `InvalidRequest` is already imported. It is a validation error, so the structured body from Lesson 2.4 marks it `"errorCategory": "validation"` and `"isRetryable": false`. Claude reads that as "fix the input", not "try again".

You don't touch `server.py` for this. Its `call()` helper already turns every `BackendError` into an error result with `is_error` set. The check sits in the backend, so the loop from Module 1 gets the fix too.

### 3. Publish the status codes as a resource (Lesson 2.5)
Orders from the old warehouse system carry numeric status codes, and the names live in `legacy/warehouse/codes.py` as `STATUS_NAMES` (you met it in Lesson 2.7). Add a resource next to the other two:

- URI `harborline://catalog/statuses`
- MIME type `application/json`
- a one-line description that says what the codes are
- content: `json.dumps(STATUS_NAMES, indent=1)`

A resource is read by the app and handed to Claude, with no tool call. It fits reference data that changes rarely and that Claude would otherwise have to ask for. JSON turns the integer keys into strings (`"3": "shipped"`); that's expected.

Then update the resource set in `tests/test_mcp_server.py` so it lists all three URIs.

### 4. Measure routing through the server (Lessons 2.1 and 2.5)
Write `experiments/m2/mcp_routing.py`. It does what `routing_eval.py` does, with one difference: the tools come from the server.

1. Open an in-memory `Client(app)`, the same client the tests use, and call `list_tools()`.
2. Turn each MCP tool into a Messages API tool: `name`, `description`, and `input_schema` from the tool's `input_schema`. Put that in a function, `as_api_tool(tool)`.
3. Keep only the cases whose expected tool the server publishes. The server has no `escalate_to_human`, so two labeled requests and two held-out requests drop out. That leaves 14 labeled and 6 held-out. Put that in `cases_for(names)`, returning `(labeled, held_out)`. You can import `HELD_OUT`, `TRIES` and `correct` from `routing_eval.py`.
4. Ask each request 3 times, scored as in Lesson 2.1. When Claude calls a lookup on the way to another tool, run it through the MCP client with `call_tool` and send the result back. Two rounds at most.
5. Print a score per case, the labeled and held-out totals, the cost, and whether the held-out score reaches 90%.

Every response goes through `log_usage`, as in every lesson since 1.2.

## Check your work

1. Copy `labs/L2/tests/test_lab2.py` into your project's `tests/` and run the whole suite:
   ```bash
   python -m pytest -q
   ```
   Our solution: `71 passed` (the starter's 57 tests plus the lab's 14). Before your changes, 4 of the lab's tests fail: the two refund amounts, the three resources and the routing helpers. The other 10 already pass. They guard what Lessons 2.4 to 2.6 built, so a change in this lab can't quietly break it. The tests use the in-memory MCP client, cost nothing and need no key. They cover:
   - exactly four tools, with `lookup_order` and `list_orders` naming each other in their descriptions
   - one error of each category, with its `isRetryable` flag: validation (`12345`), not found (`HL-99999`), transient (`HL-10211`, once after a reset), business (the final-sale item in `HL-10159`) and permission (`HL-10088`, whose customer is on review hold)
   - the business error's `customerReason`
   - a refund of `-20.0` and of `0.0`: validation, not retryable, nothing refunded
   - a valid refund that still goes through
   - an empty order list for `C-1058` as a success, not an error
   - the three resources: the statuses equal `STATUS_NAMES`, 40 products, and a policy that says 30 days
   - the server started with no `HARBORLINE_API_TOKEN`: it exits with an error, says why on stderr, and prints nothing on stdout, because stdout belongs to the protocol
   - `as_api_tool` and `cases_for`
2. Run the routing measurement once (about $0.02):
   ```bash
   python -m experiments.m2.mcp_routing
   ```
   Our run: held-out 18/18, labeled 36/42, PASS, 75 requests and $0.0153 in `runs/usage.jsonl`. The six labeled misses were R06 and R12, 0/3 each. Claude answered without calling `process_refund`, and the scoring counts that as a miss. These are the two requests Lesson 2.1 showed are mislabeled. Claude looked up the real orders and declined: there's no kettle on HL-10112, and HL-10089 was delivered a day early. So the miss is in the label, not in the tool, and the frozen dataset stays as it is. Your numbers will differ a little. If a held-out case misses, read the request, then the tool descriptions, before you change anything.

## Compare with the solution

`solution/harborline/backend.py`, `solution/mcp_server/server.py` and `solution/experiments/m2/mcp_routing.py` are one way to do it. `solution/tests/test_lab2.py` is the self-check. Other designs pass too. For example, you might run the three tries one after another instead of side by side, or keep one MCP client per try.

## Commit

```bash
git add harborline/backend.py mcp_server/server.py experiments/m2/mcp_routing.py tests/test_mcp_server.py tests/test_lab2.py
git commit -m "Lab 2: reject refunds of \$0 or less, status codes resource, MCP routing check"
git push
```
