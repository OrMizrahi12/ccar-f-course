# Expected output: Lesson 3.8, Sessions: resume, fork, or start fresh

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. Replies are wrapped by the script itself (84 columns).

**What will differ on yours:** the wording of every reply (Claude's answers vary from run to run), every session ID, and your commit IDs. Each section says what should match.

## Step 1: A named session

```text
(.venv) $ git status --short
(.venv) $ code support/sessions.py
(.venv) $ clear; python -m support.sessions new review "Read support/hooks.py. One line per hook: when it runs, and what it does." 2> runs/sessions.log
tools: Read hooks.py
- **refund_limit** (PreToolUse, `process_refund`): denies refunds over $500 and
  tells Claude to call `escalate_to_human` instead of retrying. Refunds at or under
  $500 pass through.
- **normalize_order** (PostToolUse, `lookup_order`): if the result is an order
  record, trims it to the relevant fields in one format and replaces Claude's view
  of the output. Error or non-JSON results are left alone.
- **case_facts.record** (PostToolUse, all `mcp__harborline__.*` tools): runs after
  every Harborline tool call. I haven't read `support/case_facts.py`, so I can't say
  what it records.

session review: 551546b1-89e9-4065-897f-e7181e6edd43
```

**Should match:** one `Read` of `hooks.py`, three hooks, and a line `session review: <an ID>`. `runs/sessions.json` now holds that ID under the name `review`.

## Step 2: Resume

```text
(.venv) $ clear; python -m support.sessions resume review "Which of these hooks protects money, and how?" 2> runs/sessions.log
tools: -
The `refund_limit` hook protects money. It runs before every `process_refund` call
  and denies any amount over $500 (`REFUND_LIMIT`), telling Claude to escalate to a
  human instead of retrying.

Gaps I can see in the code:
- If `amount` is missing, it defaults to 0 and the refund passes.
- If `amount` arrives as a string, the comparison with a float raises an error
  rather than denying.

session review: 551546b1-89e9-4065-897f-e7181e6edd43
```

**Should match:** `tools: -` (the answer comes from the session, not from reading the file again) and the same session ID as step 1. The gaps it lists may differ.

## Step 3: Fork

```text
(.venv) $ clear; python -m support.sessions fork review tests-direct "Plan three unit tests that call these hooks directly, without the agent. One line each." 2> runs/sessions.log
tools: -
1. `refund_limit({"tool_input": {"amount": 500}}, None, None)` returns `{}`, and
  `amount: 500.01` returns a deny with the escalation reason.
2. `refund_limit` with `amount` missing or passed as a string, to pin down the
  current behaviour (missing passes, string raises) before deciding whether to fix
  it.
3. `normalize_order` given an error payload (no `order_id`) returns `{}` unchanged,
  and given a valid order returns `updatedToolOutput` with trimmed JSON.

session tests-direct: 01c27dcc-2ec5-48ee-a71b-7a337048e54a
(.venv) $ clear; python -m support.sessions fork review tests-agent "Plan three checks that run the whole agent instead. One line each." 2> runs/sessions.log
tools: -
1. **Over-limit refund:** run the full agent with a request for more than $500 and
  confirm it never calls `process_refund` and ends by escalating to a human.
2. **Missing or string amount:** run the agent with a refund request whose amount is
  absent or formatted as text, and check whether the refund goes through or the call
  errors.
3. **Normal refund:** run the agent with a refund at or under $500 and confirm it
  completes, and that `normalize_order` and `case_facts.record` still fire on the
  related lookups.

session tests-agent: f2d13d48-84a9-4f73-b0a4-a9701d5c0c8d
(.venv) $ clear; python -m support.sessions resume review "Have we planned any tests in this conversation?" 2> runs/sessions.log
tools: -
No. We haven't planned or written any tests in this conversation; we've only read
  `support/hooks.py` and discussed it. I can write tests for the `refund_limit` gaps
  (missing `amount`, string `amount`) if you want them.

session review: 551546b1-89e9-4065-897f-e7181e6edd43
(.venv) $ cat runs/sessions.json
{
 "review": "551546b1-89e9-4065-897f-e7181e6edd43",
 "tests-direct": "01c27dcc-2ec5-48ee-a71b-7a337048e54a",
 "tests-agent": "f2d13d48-84a9-4f73-b0a4-a9701d5c0c8d"
}(.venv) $
```

**Should match:** `tools: -` on all three runs; each fork gets a new ID; the original `review` keeps its ID and knows nothing of the forks' plans. The file has no final newline, so the prompt follows the `}`.

## Step 4: Tell it what changed

```text
(.venv) $ code support/hooks.py
(.venv) $ clear; python -m support.sessions resume review "I changed one line in support/hooks.py: refund_limit now reads the amount with float(). Re-read only that function. Does a text amount like 600 still get past it?" 2> runs/sessions.log
tools: Read hooks.py
Yes, it now gets denied. `float("600")` is 600.0, which is above 500, so the hook
  returns a deny.

Two cases still behave differently: a non-numeric string like `"abc"` makes
  `float()` raise an error instead of denying, and a missing `amount` still defaults
  to 0 and passes.

session review: 551546b1-89e9-4065-897f-e7181e6edd43
```

**Should match:** exactly one `Read`, of `hooks.py`, and the same `review` ID. In the lesson the reply starts with "Yes" but means the opposite: a text amount is now denied.

## Step 5: Commit

```text
(.venv) $ clear; git status --short
 M support/hooks.py
?? support/sessions.py
(.venv) $ git add support
(.venv) $ git commit -m "Lesson 3.8: named sessions to resume and fork, and a refund amount read as a number"
[main 9bcefb7] Lesson 3.8: named sessions to resume and fork, and a refund amount read as a number
 2 files changed, 79 insertions(+), 1 deletion(-)
 create mode 100644 support/sessions.py
(.venv) $ git push
...
   e5c3ff5..9bcefb7  main -> main
```

**Should match:** the file list and the counts. `runs/sessions.json` is not listed: `runs/` is git-ignored. Your commit IDs will differ.
