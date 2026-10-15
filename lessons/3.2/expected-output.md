# Expected output: Lesson 3.2, The support agent: tools, loop and a target

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. The terminal wrapped long lines; they're shown unwrapped here.

**What will differ on yours:** Claude's wording (its replies are written fresh each time), the costs in the last digit, the session ID, sometimes a ticket's verdict or its number of turns, and your commit IDs. Each section says what should match.

## Step 1: Four tools

```text
(.venv) $ git status --short
(.venv) $ code support/tools.py
```

Nothing else prints: `support/tools.py` is edited and saved. Compare your file with the kit's. The last three lines:

```python
TOOLS = [get_customer, lookup_order, process_refund, escalate_to_human]
server = create_sdk_mcp_server("harborline", version="1.0.0", tools=TOOLS)
NAMES = [f"mcp__harborline__{t.name}" for t in TOOLS]  # for allowed_tools
```

## Step 2: One ticket

```text
(.venv) $ code support/agent.py
(.venv) $ clear; python -m support.agent T-003
⚠ claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set and takes precedence over your claude.ai login · Unset it to load your organization's connectors
tools: get_customer, lookup_order, process_refund
reply: Hi Amara, I've processed a refund of $74.00 for the Ceramic Table Lamp on order HL-10163 (refund ID RF-0001), returned to your card ending in 1817. The $6.95 shipping fee was not included in the refund.
success: 4 turns, $0.0008, session e6480a2b-0630-44ca-b522-929f472cce74
```

What should match: the three tools in that order, a $74.00 refund on HL-10163, and `success`. The first line appears only if your computer is signed in to Claude Code (Lesson 3.1). Your session ID is different every run.

## Step 3: The number

```text
(.venv) $ code support/evaluate.py
(.venv) $ clear; python -m support.evaluate 2> runs/evaluate.log
T-001  resolved                   4 turns  $0.0011  get_customer, lookup_order, process_refund
T-002  wrong refund               4 turns  $0.0006  get_customer, lookup_order, process_refund
T-003  resolved                   4 turns  $0.0006  get_customer, lookup_order, process_refund
T-004  resolved                   5 turns  $0.0009  get_customer, lookup_order, lookup_order, process_refund
T-005  escalated                  4 turns  $0.0008  get_customer, lookup_order, escalate_to_human
T-006  resolved                   4 turns  $0.0007  get_customer, lookup_order, process_refund
T-007  resolved                   5 turns  $0.0009  get_customer, lookup_order, lookup_order, process_refund
T-008  resolved                   3 turns  $0.0005  get_customer, lookup_order
T-009  resolved                   4 turns  $0.0007  get_customer, lookup_order, process_refund
T-010  resolved                   4 turns  $0.0007  get_customer, lookup_order, process_refund
T-011  resolved                   4 turns  $0.0007  get_customer, lookup_order, process_refund
T-012  resolved                   4 turns  $0.0007  get_customer, lookup_order, process_refund
T-013  resolved                   4 turns  $0.0007  get_customer, lookup_order, process_refund
T-014  resolved                   4 turns  $0.0006  get_customer, lookup_order, process_refund
T-015  refund missing             1 turns  $0.0003
T-016  resolved                   5 turns  $0.0009  get_customer, lookup_order, lookup_order, process_refund
T-017  resolved                   4 turns  $0.0009  get_customer, lookup_order, process_refund
T-018  resolved                   4 turns  $0.0007  get_customer, lookup_order, process_refund
T-022  escalated                  4 turns  $0.0008  get_customer, lookup_order, escalate_to_human
T-023  escalated                  4 turns  $0.0008  get_customer, lookup_order, escalate_to_human

FCR 15/20 (75%) · escalation recall 3/3 · wrong refunds 1 · $0.0146
```

How to read it:

- **T-001, T-010, T-011, T-012**: `process_refund` was called and the refund policy refused it (a closed return window, or a final-sale item), so nothing was paid, which is what the label expects.
- **T-002, `wrong refund`**: an opened e-reader, past its 15-day window. `process_refund` has no input for "opened", so the policy never saw it and paid $129.
- **T-015, `refund missing`**: the message is signed Jordan Lee with no email, and two customers have that name. Claude asked which one, in one turn with no tools. That's the right move, but it needs a second message, so it isn't a first-contact resolution.
- **T-005, T-022, T-023, `escalated`**: two customers who asked for a person, and a price-drop refund the policy says nothing about.

What should match: 20 lines, escalation recall near 3/3, and a summary in the same form. Every run ends with subtype `success`; the verdicts come from the backend's ledgers, not from the replies. `runs/evaluate.log` holds the connectors notice, once per ticket.

## Step 4: Commit

```text
(.venv) $ clear; git status --short
 M support/tools.py
?? support/agent.py
?? support/evaluate.py
(.venv) $ git add support
(.venv) $ git commit -m "Lesson 3.2: the support agent with four tools, and an FCR baseline"
[main d180d01] Lesson 3.2: the support agent with four tools, and an FCR baseline
 3 files changed, 148 insertions(+), 2 deletions(-)
 create mode 100644 support/agent.py
 create mode 100644 support/evaluate.py
(.venv) $ git push
…
To https://github.com/YOUR-USERNAME/harborline.git
   b0148e9..d180d01  main -> main
```

What should match: three files, 148 insertions and 2 deletions (if you typed the files exactly), and `main -> main`. Your commit IDs differ.
