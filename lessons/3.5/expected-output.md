# Expected output: Lesson 3.5, Escalation and ambiguity

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. The replies under each ticket line are wrapped by the script itself (84 columns, at most two rows; `[...]` marks a cut).

**What will differ on yours:** the replies' wording, and possibly a decision (Claude's choices vary from run to run), and your commit IDs. Each section says what should match.

## Step 1: Measure

```text
(.venv) $ git status --short
(.venv) $ code support/escalation_check.py
(.venv) $ clear; python -m support.escalation_check 2> runs/escalation_check.log
T-005  want escalate  got escalate  get_customer, lookup_order, escalate_to_human
  Thank you, Mr. Varga.
T-022  want escalate  got escalate  get_customer, lookup_order, escalate_to_human
  Sorry for the frustration, Wesley. Order HL-10205 has shipped with Parcelway
  (tracking PW9177579633) and is estimated to arrive October 18, 2026, ahead [...]
T-023  want escalate  got escalate  get_customer, lookup_order, escalate_to_human
  I've confirmed your account and order HL-10188 (Stand Mixer, $329), but I can't
  refund a price drop that happened after your purchase, since our refund [...]
T-017  want resolve   got resolve   get_customer, lookup_order, process_refund
  I'm sorry the sheets didn't match what you saw online. I've processed a refund of
  $98.00 for the Percale Sheet Set (Queen) on order HL-10182 (refund ID RF-0001).
T-015  want ask       got ask       get_customer
  Hi Jordan, I found more than one account under that name, so I need to confirm
  which one is yours before I can look at any order. Could you send the email [...]

right call 5/5 · asked for a person, handed over at once 0/2
```

**Should match:** five ticket lines in this order, then the two scores. In practice runs before filming, the agent as Lesson 3.4 left it made the right call on all five every time, and looked the order up before handing over both person requests (`0/2`) every time. Your replies will be worded differently.

## Step 2: The criteria

```text
(.venv) $ clear; mkdir support/prompts
(.venv) $ code support/prompts/system.md
(.venv) $ code support/agent.py
```

Nothing else prints. `support/prompts/system.md` is 44 lines; the changes in `support/agent.py` are listed in `README.md`, step 2.

## Step 3: Measure again

```text
(.venv) $ clear; python -m support.escalation_check 2> runs/escalation_check.log
T-005  want escalate  got escalate  get_customer, escalate_to_human
  Hi Marcus, I've confirmed your account and passed your request to our support
  leads team, so a person will take over from here. Your escalation ID is [...]
T-022  want escalate  got escalate  get_customer, escalate_to_human
  I understand how frustrating it is not knowing where order HL-10205 is. I've
  verified your account and passed your request to our support team as [...]
T-023  want escalate  got escalate  get_customer, lookup_order, escalate_to_human
  Thanks, Rowan. I checked order HL-10188 for the stand mixer ($329, delivered
  October 10).
T-017  want resolve   got resolve   get_customer, lookup_order, process_refund
  I understand your frustration, Theo, and I'm sorry the sheets didn't match what
  you saw online. I've processed a full refund of $98.00 for the Percale Sheet [...]
T-015  want ask       got ask       get_customer
  Hi Jordan, I can help with the water bottle return. We have two accounts under the
  name Jordan Lee, so I need to confirm which one is yours.

right call 5/5 · asked for a person, handed over at once 2/2
```

**Should match:** T-005 and T-022 now show `get_customer, escalate_to_human`, with no `lookup_order` in between. T-023 still looks the order up (a price drop isn't a request for a person). In practice runs with the same files, `5/5 · 2/2` four times out of four. If a run differs, read that ticket's reply: the check exists to catch exactly that.

## Step 4: Commit

```text
(.venv) $ clear; git status --short
 M support/agent.py
?? support/escalation_check.py
?? support/prompts/
(.venv) $ git add support
(.venv) $ git commit -m "Lesson 3.5: escalation criteria and examples, in a prompt file"
[main ff1c087] Lesson 3.5: escalation criteria and examples, in a prompt file
 3 files changed, 105 insertions(+), 8 deletions(-)
 create mode 100644 support/escalation_check.py
 create mode 100644 support/prompts/system.md
(.venv) $ git push
...
   6e328fc..ff1c087  main -> main
```

**Should match:** the file list and the counts. Your commit IDs will differ, and the push goes to your own `harborline`.
