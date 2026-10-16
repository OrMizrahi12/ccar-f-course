# Expected output: Lesson 3.7, Long conversations without losing facts

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. The summary and the reply are wrapped by the script itself (84 columns; the reply shows at most four rows, and `[...]` marks a cut).

**What will differ on yours:** the summary, the reply's wording, which tools each turn calls, possibly the score (Claude's replies and summaries vary from run to run), and your commit IDs. Each section says what should match.

## Step 1: Measure

```text
(.venv) $ git status --short
(.venv) $ code support/long_check.py
(.venv) $ clear; python -m support.long_check 2> runs/long_check.log
1  get_customer, lookup_order, process_refund
2  lookup_order, get_customer, process_refund
3  get_customer, lookup_order, process_refund
4  -
5  -
6  -
7  -
8  -

summary: Sofia: RF-0001 mirror $129, RF-0002 blanket $119, RF-0003 garden $67. 5
business days. Shipping refunded if damaged, wrong, or 5+ days late. Free shipping
$75+.

> I can put together that list, but first I need to verify your account. Please send
  the email address on your Harborline account or the order number for one of the
  refunds. Once I've confirmed your account, I'll look up each order and list the
  amount, order number and refund reference for every refund.

$129  HL-10158  RF-0001        0/3 in the last reply
$119  HL-10131  RF-0002        0/3 in the last reply
$67  HL-10193  RF-0003         0/3 in the last reply

facts kept 0/9
```

**Should match:** three refunds in turns 1 to 3 (the three ledger lines at the bottom: `$129 HL-10158 RF-0001`, `$119 HL-10131 RF-0002`, `$67 HL-10193 RF-0003`), and no tools in turns 4 to 7 (the policy questions). The summary is 25 words or fewer and loses something: here the order numbers and the verification. The score varies: in practice runs before filming, 0/9, 3/9, 6/9 and 0/9.

## Step 2: Case facts and the trim

```text
(.venv) $ code support/case_facts.py
(.venv) $ clear; python -m support.case_facts HL-10187
full     12 fields  484 characters
trimmed   8 fields  292 characters
{"order_id": "HL-10187", "status": "delivered", "promised_by": "2026-10-11", "delivered_at": "2026-10-10T12:04:23Z", "items": [{"sku": "SKU-1105", "name": "Stoneware Vase", "category": "home", "unit_price": 32.0, "final_sale": false}], "shipping_fee": 6.95, "total": 38.95, "payment": "card"}
```

**Should match:** exactly (the seed data is the same for everyone).

## Step 3: Wire it in

```text
(.venv) $ code support/hooks.py
(.venv) $ code support/long_check.py
```

Nothing else prints. The edits are listed in `README.md`, step 3.

## Step 4: Measure again

```text
(.venv) $ clear; python -m support.long_check 2> runs/long_check.log
1  get_customer, lookup_order, process_refund
2  lookup_order, process_refund
3  get_customer, lookup_order, process_refund
4  -
5  -
6  -
7  -
8  get_customer, lookup_order, lookup_order, lookup_order

summary: Refunds RF-0001 ($129), RF-0002 ($119), RF-0003 ($67) processed; arrive by
Oct 20, 2026. Shipping refunds: damaged, wrong, late, pre-shipment cancellations
only. Orders $75+ ship free.

> Here are your refunds on record, all on your account (C-1009):  1. RF-0001:
  $129.00 on order HL-10158 (Round Wall Mirror) 2. RF-0002: $119.00 on order
  HL-10131 (Weighted Blanket) 3. RF-0003: $67.00 on order HL-10193 (Garden Tool Set)
  Total refunded: $315.00.

$129  HL-10158  RF-0001        3/3 in the last reply
$119  HL-10131  RF-0002        3/3 in the last reply
$67  HL-10193  RF-0003         3/3 in the last reply

facts kept 9/9
```

**Should match:** `facts kept 9/9` (or very close). The summary is still short and still loses the order numbers; the reply reads them from the case facts. Turn 8 may or may not call tools: in the lesson the agent confirmed the facts with `get_customer` and the three lookups before answering. In practice runs before filming, 9/9 in four runs out of four.

## Step 5: Commit

```text
(.venv) $ clear; git status --short
 M support/hooks.py
?? support/case_facts.py
?? support/long_check.py
(.venv) $ git add support
(.venv) $ git commit -m "Lesson 3.7: case facts outside the summary, and trimmed order lookups"
[main e5c3ff5] Lesson 3.7: case facts outside the summary, and trimmed order lookups
 3 files changed, 171 insertions(+), 3 deletions(-)
 create mode 100644 support/case_facts.py
 create mode 100644 support/long_check.py
(.venv) $ git push
...
   5c357e0..e5c3ff5  main -> main
```

**Should match:** the file list and the counts. Your commit IDs will differ.
