# Expected output: Lesson 5.1, Working with Claude Code

What each step showed in the lesson, copied from the screen. Claude's wording, the order of its tool calls and its file contents will differ on your machine, and so will times, token counts and commit ids. What should match: the modes in the status bar, the two late orders and the $13.90 total, the tests passing, `/clear` forgetting and `/resume` remembering, and the shape of the git output. Long passages are shortened with `…`.

## 1. Explore and plan

```text
$ git status --short
$ claude
 Claude Code v2.1.301
 Haiku 5.5 · Claude Max
 ~/projects/harborline
…
⏵⏵ auto mode on (shift+tab to cycle) · ← for agents
```

The status bar after each **Shift+Tab**:

```text
⏸ manual mode on · ? for shortcuts · ← for agents
⏵⏵ accept edits on (shift+tab to cycle) · ← for agents
⏸ plan mode on (shift+tab to cycle) · ← for agents
```

The explore question, in plan mode:

```text
● I'll load the Harborline order tools and look for the refund policy in the repo.

  Read 3 files, listed 2 directories (ctrl+o to expand)

● Bash(python3 -I - <<'EOF'
      import json,collections…)
  ⎿  <class 'list'> 213
     …
  ⎿  Allowed by auto mode classifier
```

Claude Code asks before the MCP tool (once per order in the lesson; each answered `1`):

```text
Tool use
harborline – Lookup Order Tool: (MCP)
order_id: "HL-10147"
…
Do you want to proceed?
❯ 1. Yes
  2. Yes, and don't ask again for harborline – Lookup Order commands in ~/pro…
  3. No
```

The answer (its parts, top to bottom; the table's borders simplified):

```text
● Two orders qualify, and the policy owes each customer the shipping fee back. I
  haven't issued any refund.

  Late orders (delivered more than 5 days after the promised date)

  | Order    | Customer | Promised   | Delivered  | Days late | Shipping fee owed |
  | HL-10147 | C-1043   | 2026-09-28 | 2026-10-06 | 8         | $6.95             |
  | HL-10148 | C-1008   | 2026-09-29 | 2026-10-07 | 8         | $6.95             |

  What the policy says we owe
  - Section 4 of data/refund_policy.md says a delivery that arrives more than 5 days
    after the promised date gets the shipping fee refunded. harborline/policy.py
    implements this as check_refund(..., "late_delivery").
  - That is $6.95 per order, $13.90 in total. The item price isn't covered by this
    rule.
  …
  How the dates are stored
  - Three formats: Orders from before July 15 use Unix seconds. Newer orders use ISO
    text, either …Z or with a -04:00 offset. promised_by on the newer orders is a bare
    date like 2026-09-28.
  …
  - Effect on this answer: I counted lateness two ways: calendar dates as stored, and
    everything converted to UTC. Both give the same two orders at 8 days. …
  - Not delivered: I left out the 23 orders with no delivery date. …

  Two caveats on the data. I read the lateness from data/orders.json, because there's
  no tool to list every order. I then confirmed both orders through lookup_order. …

  If you want these refunded, say so and I'll check each through process_refund first.
```

The plan request, then the plan (shortened) and the menu:

```text
● Bash(ls scripts tests && sed -n 1,40p scripts/count_tokens.py && sed -n 1,40p
      harborline/data.py && cat pytest.ini && sed -n 1,30p tests/test_backend.py)
  ⎿  Allowed by auto mode classifier

● Updated plan
  ⎿  /plan to preview

 Ready to code?

 Here is Claude's plan:
 Plan: scripts/late_deliveries.py + tests/test_late_deliveries.py
 Context
 …
 - harborline.policy.LATE_DELIVERY_DAYS (5) and check_refund(order, "late_delivery"):
   the single source of truth for "late" and for the amount … The script calls it
   rather than re-implementing the rule, so it cannot drift from the policy.
 scripts/late_deliveries.py
 - late_orders(orders): for each order with a non-null delivered_at, call
   check_refund(order, "late_delivery"); keep those with allowed. …
 - main(): print a table sorted by order id, then Total owed: $X.XX and the count. …
 - Read-only: it never calls process_refund.
 tests/test_late_deliveries.py
 Style like tests/test_policy.py: plain pytest functions, small synthetic order dicts
 built in the test.
 …
 Verification
 - python -m pytest tests/test_late_deliveries.py -q, then the full python -m pytest
   -q to confirm nothing else moved.
 - python -m scripts.late_deliveries shows two rows and a total of $13.90, matching
   the manual lookup_order results.

 Claude has written up a plan and is ready to execute. Would you like to proceed?

 ❯ 1. Yes, and use auto mode
   2. Yes, manually approve edits
   3. Tell Claude what to change
      shift+tab to approve with this feedback

 ctrl+g to edit in VS Code · ~/.claude/plans/<a generated name>.md
```

## 2. Code and test

```text
● Plan approved. I'll write the script and its test now, touching only those two files.

● Write(scripts/late_deliveries.py)
  ⎿  Wrote 54 lines to scripts/late_deliveries.py
● Write(tests/test_late_deliveries.py)
  ⎿  Wrote 71 lines to tests/test_late_deliveries.py

● Bash(python -m pytest tests/test_late_deliveries.py -q 2>&1 | tail -20 && python -m
      scripts.late_deliveries && git status --short)
  ⎿  ......                                                                  [100%]
     6 passed in 0.02s
  ⎿  Allowed by auto mode classifier

● The new tests pass. The plan also called for the full suite, so I'll run it.

● Bash(python -m pytest -q 2>&1 | tail -15)
  ⎿  Allowed by auto mode classifier

● I added scripts/late_deliveries.py and tests/test_late_deliveries.py, and nothing
  else changed. Running python -m scripts.late_deliveries lists HL-10147 and HL-10148
  with the fee owed for each, $6.95, and a total of $13.90. The new tests pass (6), and
  so does the full suite (118).
  …
  Nothing is committed. Both files are untracked in the working tree.

✻ Worked for 42s
```

The script's own output, with the kit's files (`python -m scripts.late_deliveries`):

```text
order      customer   promised    delivered    late      fee
HL-10147   C-1043     2026-09-28  2026-10-06      8     6.95
HL-10148   C-1008     2026-09-29  2026-10-07      8     6.95

2 orders. Total shipping fees owed: $13.90
```

## 3. Context

`/context`, scrolled up to the grid (the category lines; your numbers depend on your account's skills and connectors):

```text
Haiku 5.5
claude-haiku-5-5
67.1k/1m tokens (7%)

Estimated usage by category
System prompt: 2.9k tokens (0.3%)
System tools: 20.1k tokens (2.0%)
MCP tools: 246 tokens (0.0%)
MCP server instructions: 1.2k tokens (0.1%)
Skills: 6.6k tokens (0.7%)
Messages: 36.1k tokens (3.6%)
Free space: 899.9k (90.0%)
Autocompact buffer: 33k tokens (3.3%)

MCP tools · /mcp (loaded on-demand)
Loaded
└ mcp__harborline__lookup_order: 246 tokens
```

```text
❯ /compact Keep the late-delivery script, its test and the policy rule
  ⎿  Compacted (ctrl+o to see full summary)
  ⎿  Read tests/test_late_deliveries.py (72 lines)
  ⎿  Read scripts/late_deliveries.py (55 lines)
  ⎿  Read harborline/policy.py (117 lines)
  ⎿  Read data/refund_policy.md (33 lines)
  ⎿  Read data/README.md (24 lines)
  ⎿  Plan file referenced (~/.claude/plans/<a generated name>.md)
```

`/context` again, scrolled up to the new grid:

```text
59k/1m tokens (6%)
…
Messages: 28.9k tokens (2.9%)
Free space: 908k (90.8%)
```

## 4. Commit, clear, resume

```text
❯ Commit the script and its test with a descriptive message.

● You're on main, so I'll commit on a new branch.

● Bash(git switch -c late-delivery-report && git add scripts/late_deliveries.py
      tests/test_late_deliveries.py && git commit -q -m "Add late-delivery report: list
      order…)
  ⎿  Switched to a new branch 'late-delivery-report'
     cf8ab59 Add late-delivery report: list orders the refund policy covers, with
     the shipping fee owed

● I committed the script and its test as cf8ab59 on a new branch, late-delivery-report,
  because main was the current branch. The working tree is clean.
  … Nothing was pushed, and main is unchanged.
```

```text
❯ /clear
❯ What did I ask you to plan earlier in this conversation?
● The conversation was just cleared with /clear, so I have no record of any earlier
  planning request. The only thing I can see is the git state: …
```

```text
❯ /resume
 Resume session (1 of 5)
 ❯ add-late-deliveries-script
   52 seconds ago · late-delivery-report · 1.3MB
   …
```

```text
❯ What did I ask you to plan earlier in this conversation?
● You asked me to plan scripts/late_deliveries.py, a script that lists the orders
  delivered more than 5 days after the promised date, with the shipping fee owed for
  each and the total, plus a test for it. You asked that the change touch only those
  two files.
  I wrote the plan to …/.claude/plans/<a generated name>.md, and you approved it. …
  Later you asked me to keep the script, its test, and the policy rule. I committed
  both files on late-delivery-report as cf8ab59.

❯ /exit
Resume this session with:
claude --resume <your session id>
```

```text
$ git log --oneline -1
cf8ab59 (HEAD -> late-delivery-report) Add late-delivery report: list orders the refund policy covers, with the shipping fee owed
$ git push
fatal: The current branch late-delivery-report has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin late-delivery-report
…
```

```text
$ git switch main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
$ git merge --ff-only late-delivery-report
Updating a543410..cf8ab59
Fast-forward
 scripts/late_deliveries.py    | 54 ++++++++++++++++
 tests/test_late_deliveries.py | 71 ++++++++++++++++++++++
 2 files changed, 125 insertions(+)
 create mode 100644 scripts/late_deliveries.py
 create mode 100644 tests/test_late_deliveries.py
$ git push
…
To https://github.com/YOUR-USERNAME/harborline.git
   a543410..cf8ab59  main -> main
$ git branch -d late-delivery-report
Deleted branch late-delivery-report (was cf8ab59).
$ git log --oneline -2
cf8ab59 (HEAD -> main, origin/main) Add late-delivery report: list orders the refund policy covers, with the shipping fee owed
a543410 Lab 4: …
```

```text
$ claude --continue
```

The most recent conversation comes back, ending where you left it.
