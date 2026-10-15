# Expected output: Lesson 3.6, Multi-concern requests and handoffs

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. The `next:` lines are wrapped by the script itself (84 columns, at most two rows; `[...]` marks a cut).

**What will differ on yours:** the `next:` wording, which tool calls land in one turn, possibly a score (Claude's replies vary from run to run), and your commit IDs. Each section says what should match.

## Step 1: Measure

```text
(.venv) $ git status --short
(.venv) $ code support/case_check.py
(.venv) $ clear; python -m support.case_check 2> runs/case_check.log
T-004  answered 2/3  get_customer + lookup_order + lookup_order | process_refund
T-007  answered 3/3  get_customer + lookup_order + lookup_order | process_refund
T-016  answered 2/3  get_customer + lookup_order + lookup_order | process_refund
T-005  hand-off  missing: order_id, amount, recommended_action
  next: None
T-022  hand-off  missing: order_id, amount, recommended_action
  next: None
T-023  hand-off  missing: order_id, amount, recommended_action
  next: None

requests answered 7/9 · hand-offs complete 0/3
```

**Should match:** every hand-off missing `order_id, amount, recommended_action`, because the old `escalate_to_human` tool only takes a customer ID, a reason and a summary. The agent as Lesson 3.5 left it usually looks both orders up in one turn already (a `+` between calls). The question that only the refund policy answers (T-004: how long refunds take) is usually missed: the agent hasn't seen the policy. In practice runs before filming, `7/9 · 0/3` three times out of three.

## Step 2: The hand-off

```text
(.venv) $ code support/handoff.py
(.venv) $ code support/tools.py
```

Nothing else prints. `support/handoff.py` is 32 lines; the changes in `support/tools.py` are listed in `README.md`, step 2.

## Step 3: The policy

```text
(.venv) $ code support/prompts/system.md
(.venv) $ code support/agent.py
```

Nothing else prints. The new lines in `support/prompts/system.md` and `support/agent.py` are listed in `README.md`, step 3.

## Step 4: Measure again

```text
(.venv) $ clear; python -m support.case_check 2> runs/case_check.log
T-004  answered 3/3  get_customer | lookup_order + lookup_order | process_refund
T-007  answered 3/3  get_customer + lookup_order + lookup_order | process_refund
T-016  answered 3/3  get_customer + lookup_order + lookup_order | process_refund
T-005  hand-off  missing: -
  next: Contact Marcus Varga (verified account C-1035, marcus.varga@example.com,
  +1-555-0128) and speak with him directly about the chipped stoneware vase on [...]
T-022  hand-off  missing: -
  next: Contact the customer (Wesley Marchetti, wesley.marchetti@example.com,
  +1-555-0162). Check the shipping status of HL-10205 and give an update on [...]
T-023  hand-off  missing: -
  next: Decide whether a goodwill price adjustment of $50 is allowed. If it is, it
  would be paid as store credit, because the order was paid by gift card. [...]

requests answered 9/9 · hand-offs complete 3/3
```

**Should match:** `missing: -` on all three hand-offs, and a real next step under each. The two orders still come in one turn (here T-004 verified first, then looked both orders up together). The check counts a question as answered when the reply contains the policy's words ("5 business days", "not refunded", the email on file); a correct answer worded another way counts as a miss, so a run with `8/9` can still be right: read that ticket's reply. In practice runs with the same files, `9/9 · 3/3` twice out of twice; an earlier draft of the check, which counted fewer wordings, scored the same agent `8/9` three times.

## Step 5: Commit

```text
(.venv) $ clear; git status --short
 M support/agent.py
 M support/prompts/system.md
 M support/tools.py
?? support/case_check.py
?? support/handoff.py
(.venv) $ git add support
(.venv) $ git commit -m "Lesson 3.6: a structured hand-off, and the policy as shared context"
[main 5c357e0] Lesson 3.6: a structured hand-off, and the policy as shared context
 5 files changed, 127 insertions(+), 5 deletions(-)
 create mode 100644 support/case_check.py
 create mode 100644 support/handoff.py
(.venv) $ git push
...
To https://github.com/YOUR-USERNAME/harborline.git
   ff1c087..5c357e0  main -> main
```

**Should match:** the five files and the line counts, if you typed the kit's files exactly. Your commit IDs will differ. `runs/` and `.env` must not appear in `git status`.
