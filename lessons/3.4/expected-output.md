# Expected output: Lesson 3.4, Hooks: intercept and normalize

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. The replies under each agent line are wrapped by the script itself (84 columns, at most three rows).

**What will differ on yours:** the agent's half of the hook check (Claude's choices and wording vary from run to run), and your commit IDs. Each section says what should match.

## Step 1: Normalize

```text
(.venv) $ git status --short
(.venv) $ code harborline/normalize.py
```

Nothing else prints: `harborline/normalize.py` is typed and saved (34 lines). Compare your file with the kit's.

## Step 2: The hooks

```text
(.venv) $ code support/hooks.py
(.venv) $ code support/agent.py
```

Nothing prints. `support/hooks.py` is 54 lines; the two new lines in `support/agent.py` are listed in `README.md`, step 2.

## Step 3: Prove it

```text
(.venv) $ clear; python -m support.hook_check 2> runs/hook_check.log
called directly
  HL-10023  status 7 -> returned  delivered_at 1781891209 -> 2026-06-19T17:46:49Z
  refund $42.00: allow
  refund $649.00: deny
    Refunds above $500 need a support lead. Call escalate_to_human instead; don't
    retry.

through the agent
  kettle hooks off  refunds 0  get_customer, lookup_order, process_refund
    Thanks, Mateo. Order HL-10023 was delivered on June 19, 2026, and it includes
    the Pour-Over Coffee Kettle ($42.00) and the Hand-Woven Rug ($219.00).
  kettle hooks on   refunds 0  get_customer, lookup_order
    Thanks, Mateo. Order HL-10023 (delivered June 19, 2026) is already marked as
    returned in our system, and it includes the Pour-Over Coffee Kettle ($42.00) and
    the Hand-Woven Rug ($219.00).
  desk   hooks on   refunds 0  get_customer, lookup_order, escalate_to_human
    Thanks, Grace. I've confirmed your account and order HL-10177 (Oak Standing
    Desk, $649.00, delivered October 8), but I can't refund $649 myself because it's
    above my $500 limit.
```

How to read it: **called directly** runs each hook with no model, so it prints the same thing every time: the normalizer turns the old warehouse's status `7` into `returned` and its Unix seconds into a UTC date, and the refund limit allows $42.00 and denies $649.00 with its reason. **Through the agent**, each line shows the refunds actually paid and the tools Claude called, in order, then the first two sentences of its reply. In the lesson, with the hooks off, Claude called `process_refund` on the kettle even though the order was already returned (the backend's policy check refused it, so `refunds 0`); with the hooks on, it read "returned" and didn't try. On the desk, Claude escalated on its own, so the refund hook never had to fire.

What should match: the whole **called directly** block, word for word. `refunds 0` on all three agent lines, and `escalate_to_human` on the desk line. The kettle lines vary: in practice runs before filming, with the hooks off Claude tried a refund on 5 of 6 runs; with the hooks on it said "returned" 6 of 6. `runs/hook_check.log` holds the connectors notice, once per agent run (3 lines).

## Step 4: Commit

```text
(.venv) $ clear; git status --short
 M support/agent.py
?? harborline/normalize.py
?? support/hook_check.py
?? support/hooks.py
(.venv) $ git add harborline support
(.venv) $ git commit -m "Lesson 3.4: a refund-limit hook and normalized orders"
[main 6e328fc] Lesson 3.4: a refund-limit hook and normalized orders
 4 files changed, 156 insertions(+)
 create mode 100644 harborline/normalize.py
 create mode 100644 support/hook_check.py
 create mode 100644 support/hooks.py
(.venv) $ git push
…
To https://github.com/YOUR-USERNAME/harborline.git
   bb0a5f8..6e328fc  main -> main
```

What should match: four files and 156 insertions (if you typed the files exactly), and `main -> main`. Your commit IDs differ.
