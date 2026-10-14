# Expected output: Lesson 1.4, The agentic loop

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12.3 and Claude Haiku 5.5 (`claude-haiku-5-5`), from the `harborline` folder with `.venv` active. The terminal wrapped long lines; they're shown unwrapped here. Long paths in the traceback are shortened to `.../harborline/`.

**Your runs will differ from these.** Claude decides each time whether to think, how it words its progress lines and its answer, and whether it asks for two lookups in one response or one at a time, so the number of turns can change too. That is the point of the lesson: the code doesn't need to know any of it in advance. Each section says what should match.

## Step 1: Write the loop

```text
(.venv) $ git status --short
(.venv) $ code loop/tools.py
(.venv) $ code loop/agent.py
```

`git status --short` prints nothing: the tree is clean after Lesson 1.3. `loop/tools.py` is Lesson 1.3's file, opened for a look and not changed: `TOOLS` is the list of tool definitions, and `run_tool(call)` takes one `tool_use` block and returns its `tool_result` block. `loop/agent.py` prints nothing when you save it; it runs in step 2.

What should match: after you save, no red squiggles under `from loop.tools import TOOLS, run_tool` or `from harborline.usage import log_usage`.

## Step 2: Run it on two tickets

### T-003: a refund question

```text
(.venv) $ clear; python -m loop.agent T-003
turn 1: tool_use
  [thinking]
  [text] I'll start by checking the sender's account against the email address.
  [tool_use] get_customer {'email': 'amara.pemberton@example.com'}
  [tool_result] {"verified": true, "customer": {"customer_id": "C-1031", "na
turn 2: tool_use
  [text] The account is verified. Next I'll look up order HL-10163 to check its delivery date and item.
  [tool_use] lookup_order {'order_id': 'HL-10163'}
  [tool_result] {"order_id": "HL-10163", "customer_id": "C-1031", "source":
turn 3: end_turn
  [thinking]
  [text] Thanks, Amara. Your ceramic table lamp (order HL-10163) was delivered on October 3, which is within the 30-day return window, and it isn't Final Sale, so you're eligible for a change-of-mind return. The policy refunds the item price of $74.00 to your card ending in 1817 within 5 business days of approval, but the $6.95 shipping fee is not refunded for a change of mind. I can't issue the refund myself, so I'm unable to process it from here; a support team member will need to take the return request forward.

History:
  user      text
  assistant thinking, text, tool_use
  user      tool_result
  assistant text, tool_use
  user      tool_result
  assistant thinking, text
```

How to read it:

| Line | What it means |
|---|---|
| `turn 1: tool_use` | One pass through the loop: one request, one response. `stop_reason` is `tool_use`, so Claude is waiting for a tool result and the loop goes round again |
| `[thinking]` | A thinking block. Claude Haiku 5.5 thinks when it decides to and doesn't return the thinking text, so nothing follows the label |
| `[text] I'll start by checking...` | The progress line the system prompt asks for ("Before each tool call, say in a few words what you are checking") |
| `[tool_use] get_customer {...}` | Claude verifies the sender first, as the system prompt says, with the email from the ticket's `From:` line |
| `[tool_result] {"verified": true, ...` | Your code ran the call. The script prints only the first 60 characters of each result; Claude gets all of it |
| `turn 2: tool_use` ... `lookup_order` | With the customer verified, Claude asks for the order |
| `turn 3: end_turn` | Claude ended its turn: the answer. The loop returns |
| `History:` | Every message in the list, by role and block types: the ticket, then Claude's turns exactly as returned, each followed by a user turn of tool results |

What should match: `get_customer` with `amara.pemberton@example.com` (customer `C-1031`), then `lookup_order` with `HL-10163`, then `end_turn` with an answer that says the lamp was delivered on October 3, the $74.00 item price can go back to the card ending in 1817, the $6.95 shipping fee isn't refunded for a change of mind, and the agent can't issue the refund itself. None of those facts is in Amara's message: they come from the tool results. What may differ: `[thinking]` lines, the wording, and the number of turns (if Claude asks for both tools at once, it can finish in two).

### T-016: three questions in one ticket

```text
(.venv) $ clear; python -m loop.agent T-016
turn 1: tool_use
  [thinking]
  [text] I'm checking the account for callum.fairbanks@example.com first.
  [tool_use] get_customer {'email': 'callum.fairbanks@example.com'}
  [tool_result] {"verified": true, "customer": {"customer_id": "C-1038", "na
turn 2: tool_use
  [text] Your account is verified. Next I'm looking up order HL-10168 for the pillow return.
  [tool_use] lookup_order {'order_id': 'HL-10168'}
  [tool_use] lookup_order {'order_id': 'HL-10202'}
  [tool_result] {"order_id": "HL-10168", "customer_id": "C-1038", "source":
  [tool_result] {"order_id": "HL-10202", "customer_id": "C-1038", "source":
turn 3: max_tokens
  [thinking]
  [text] Your pillow from HL-10168 was delivered October 4, so it's within the 30-day return window, and the policy allows a refund of its $39.00 item price to your card ending 8734 within 5 business days after the return is processed. I can't issue that refund myself, so it will need to go through the return process. Order HL-10202 (the desk chair) has shipped with Parcelway tracking number PW9340569446 and is estimated to arrive October 18, one day after the promised date, so it's not late enough for a shipping refund. It can't be cancelled now, but you can return it when it arrives. For a change-of-mind return like the pillow, the $6.95 shipping fee is not refunded;
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File ".../harborline/loop/agent.py", line 81, in <module>
    run(anthropic.Anthropic(), messages)
  File ".../harborline/loop/agent.py", line 64, in run
    raise LoopStopped(f"stopped on {response.stop_reason}")
LoopStopped: stopped on max_tokens
```

How to read it:

| Line | What it means |
|---|---|
| turn 2's two `[tool_use]` lines | Two independent lookups asked for in one response. Your code ran both and sent both results back in **one** user turn |
| `turn 3: max_tokens` | The response hit its output budget (`MAX_TOKENS`, 1,024 tokens in Harborline's `config.py`): thinking plus a long answer used it up, and the text stops mid-sentence at "is not refunded;" |
| `LoopStopped: stopped on max_tokens` | `run()` raised instead of returning: a cut-off reply is not an answer, so it never reaches the customer. This is the lesson's rule working, not a crash to fix here. Handling each stop reason properly (for example, continuing a `max_tokens` reply) is Lab 1 |

Because the loop raised, the script stops before it prints the History block.

What should match: `get_customer` with `callum.fairbanks@example.com` (customer `C-1038`), then `lookup_order` for `HL-10168` and `HL-10202`. What may differ: Claude may ask for the two lookups in two separate turns; and on your run turn 3 may well end with `end_turn` and a complete answer (the pillow's $39.00 can come back, HL-10202 has shipped with Parcelway and is estimated for October 18, and the shipping fee isn't refunded for a change of mind), followed by the History block with `user tool_result, tool_result` in one turn. If it stops on `max_tokens` like the lesson's run, you see the traceback above.

## Step 3: Three stop rules that fail

```text
(.venv) $ code experiments/m1/antipatterns.py
(.venv) $ clear; python -m experiments.m1.antipatterns T-003
turn 1: tool_use
  [thinking]
  [text] I'm checking the sender's account against amara.pemberton@example.com.
  [tool_use] get_customer {'email': 'amara.pemberton@example.com'}
  [tool_result] {"verified": true, "customer": {"customer_id": "C-1031", "na
turn 2: tool_use
  [text] The account is verified and active. Next I'm looking up order HL-10163 to check its delivery date and whether the lamp is electronics or Final Sale.
  [tool_use] lookup_order {'order_id': 'HL-10163'}
  [tool_result] {"order_id": "HL-10163", "customer_id": "C-1031", "source":
turn 3: end_turn
  [thinking]
  [text] Your ceramic table lamp (order HL-10163) was delivered on October 3, so it is within the 30-day window for a change-of-mind return. Under our policy, you would receive a refund of the $74.00 item price, but the $6.95 shipping fee is not refunded. Approved refunds go to your card ending in 1817 within 5 business days. I can't issue the refund myself, so I'd be glad to pass your return request along, or you can ask to speak with a person at any time.

stop_reason turn 3, end_turn: OK
            customer gets: 'Your ceramic table lamp (order HL-10163) was deliv'
done_words  never stops: it missed the end_turn
fixed_cap   turn 2, tool_use: WRONG
            customer gets: "The account is verified and active. Next I'm looki"
any_text    turn 1, tool_use: WRONG
            customer gets: "I'm checking the sender's account against amara.pe"
```

The script runs the real loop once (the turns print as in step 2, in Claude's own words this time), then asks each stop rule where it would have ended that same run. Until a rule says "stop", every one of those loops sends exactly the same requests, so one run is fair evidence for all four.

| Verdict | What it means |
|---|---|
| `stop_reason turn 3, end_turn: OK` | The rule that works: stop when Claude ends its turn. The customer gets the real answer |
| `done_words never stops` | Claude finished without saying "done", "resolved" or "all set", so this loop would keep calling, and paying, with nothing new to send. On another wording it could fire early instead |
| `fixed_cap turn 2, tool_use: WRONG` | Stopping after two turns cuts this ticket off while Claude is still waiting for a tool result: the customer gets a promise, not an answer. Raising the number only moves the cliff |
| `any_text turn 1, tool_use: WRONG` | The progress line and the tool call arrived in the same response. Text is not the end |

What should match: `stop_reason` OK on the `end_turn` turn, and `fixed_cap` and `any_text` WRONG whenever the run takes three turns and Claude writes a progress line before its first call. What may differ: if Claude's answer happens to say "you're all set", `done_words` lands right this time (it got lucky on the wording); if the run takes two turns, `fixed_cap` lands right; if Claude writes no progress line on turn 1, `any_text` does. A rule that only works on lucky runs is still the wrong rule.

## Step 4: Commit

```text
(.venv) $ git status --short
?? experiments/m1/antipatterns.py
?? loop/agent.py
(.venv) $ git add loop/agent.py experiments/m1/antipatterns.py
(.venv) $ git commit -m "Lesson 1.4: the agentic loop and three stop-rule anti-patterns"
[main a925cba] Lesson 1.4: the agentic loop and three stop-rule anti-patterns
 2 files changed, 149 insertions(+)
 create mode 100644 experiments/m1/antipatterns.py
 create mode 100644 loop/agent.py
(.venv) $ git push
Enumerating objects: 11, done.
Counting objects: 100% (11/11), done.
Delta compression using up to 24 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (7/7), 2.57 KiB | 2.57 MiB/s, done.
Total 7 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/YOUR-USERNAME/harborline.git
   2f5b6f5..a925cba  main -> main
```

What should match: `git status --short` lists the two new files and not `runs/` (it's ignored; its usage log now holds this lesson's calls too); `2 files changed, 149 insertions(+)` (90 + 59 lines); `main -> main` to your own `harborline`. What differs: the commit ids, the thread count and the transfer numbers.
