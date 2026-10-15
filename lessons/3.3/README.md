# Student kit: Lesson 3.3, Enforcement, not instructions

Claude Certified Architect – Foundations (CCAR-F) · Module 3: Agents with the Claude Agent SDK: the Support Resolution Agent · Lesson 3.3

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Explain why a prompt rule can fail
2. Build a prerequisite gate for the order tools
3. Prove it on skipped verification

## What's in the kit

| File | What it is |
|---|---|
| `support/gates.py` | New: the prerequisite gate. `start_case()`, `get_customer()` (the backend call, and it remembers a verified customer ID), `check(order_id)` (no verified customer, or someone else's order: blocked with a permission error, or counted as served when `ENFORCE` is off), and the gated `lookup_order()` and `process_refund()` |
| `support/tools.py` | Changed: one import, and three tools now call `gates.` instead of `backend.` (`get_customer`, `lookup_order`, `process_refund`) |
| `support/agent.py` | Changed: one import; `handle(ticket_id, prompt=None)` starts a case with `gates.start_case()`, and takes an optional prompt |
| `support/gate_check.py` | New: five "skipped verification" tickets, run with the prompt rule alone, then with the gate |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `support` folder into your `harborline` folder (it replaces `tools.py` and `agent.py`; the other files stay).

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 3.2 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, `support/tools.py` (four tools), `support/agent.py` and `support/evaluate.py` committed, and `origin` pointing at your own private `harborline` on GitHub.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 25 minutes, most of it typing. **API spend:** the gate check makes 10 short agent runs on Haiku 5.5, well under a cent.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, and **Ctrl+G** jumps to a line.

### 1. The gate

```bash
git status --short                 # prints nothing: a clean tree after Lesson 3.2
code support/gates.py              # type the file (or copy it from the kit), save
```

- **The docstring** says what the gate does, and why it lives in code: a prompt can be skipped, this check can't.
- **`ENFORCE = True`** is a switch, only for the comparison in step 3. **`case`** holds the verified customer ID for the current ticket, and two counters: `served` and `blocked`.
- **`start_case()`** empties the case for a new ticket: nobody is verified yet.
- **`get_customer(**arguments)`** calls the backend, and when the result says `verified`, keeps that customer's ID. It's the only way a customer becomes verified.
- **`check(order_id)`** finds the order's owner in `data.orders()`. Two problems: no verified customer yet, or a verified customer asking about someone else's order. With `ENFORCE` on, the call is counted as blocked and refused with `PermissionDenied`; with it off, it goes through and is counted as served.
- **`lookup_order()` and `process_refund()`** call `check()` first, then the backend, exactly as before.

`PermissionDenied` is one of Harborline's `BackendError`s, so the tool's `reply()` turns it into Lesson 2.4's structured error with `is_error`, and Claude reads the message: "No verified customer yet: call get_customer first." or "That order belongs to a different customer."

### 2. Wire it in

```bash
code support/tools.py              # line 16 + three lines, save
code support/agent.py              # line 16 + handle(), save
```

**`support/tools.py`**: after line 15 add `from support import gates`. Then three lines change from `backend.` to `gates.` (in the lesson: **Ctrl+G** to the line, **End**, **Shift+Home**, and type the new line):

| Line | Now |
|---|---|
| 34 | `return reply(gates.get_customer, email=args.get("email"),` |
| 41 | `return reply(gates.lookup_order, order_id=args["order_id"])` |
| 47 | `return reply(gates.process_refund, order_id=args["order_id"],` |

The tools keep their names, descriptions and schemas. `escalate_to_human` doesn't change.

**`support/agent.py`**: after line 15 add `from support import gates`. Then `handle()`:

```python
async def handle(ticket_id, prompt=None):
    """One ticket: the tools Claude called, its reply, the result."""
    gates.start_case()
    prompt = prompt or first_message(ticket_id)["content"]
```

`gates.start_case()` makes sure one customer's verification never carries over to the next ticket. The optional `prompt` lets a test pass a message that isn't in the ticket file.

### 3. Prove it

```bash
code support/gate_check.py         # type the file (or copy it from the kit), save
clear; python -m support.gate_check 2> runs/gate_check.log
```

- **`TICKETS`**: five senders and messages. Three come from addresses that match no account (`elijah.p.work@example.org`, `leila.k@mail.example`, `w.iwasaki@work.example`), signed with a customer's name. Two come from verified customers (`lena.moreau@example.com`, `theo.ndiaye@example.com`) asking about an order that belongs to someone else. The addresses use reserved example domains.
- **`main()`** runs the five tickets with `gates.ENFORCE = False` (the prompt rule alone: Lesson 3.2's system prompt already says "Verify the sender with get_customer first"), then with `True`. Before each ticket, `backend.reset()`. One line per ticket: `served`, `blocked`, `refunds`, and the tools Claude called.
- **`2> runs/gate_check.log`** keeps Claude Code's connectors notice (once per run) out of the table. `runs/` is git-ignored.

**In the lesson:** prompt rule only: `served 1  blocked 0  refunds 0` on all five tickets (Claude looked up the order every time). Gate on: `served 0  blocked 1  refunds 0` on all five. Your first half may differ (that's the point: a prompt rule's failure rate isn't zero, and it varies); the gate's half should always say `served 0`.

### 4. Commit

```bash
clear; git status --short
git add support
git commit -m "Lesson 3.3: a verification gate for the order tools"
git push
```

`git status --short` shows ` M support/agent.py`, ` M support/tools.py`, `?? support/gate_check.py` and `?? support/gates.py`. The commit has four files (`4 files changed, 106 insertions(+), 5 deletions(-)`). Your commit ID will differ from the lesson's.

## Windows, macOS and Linux

`git`, `code` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m support.gate_check 2> runs/gate_check.log` | the same line | `cls`, then `python -m support.gate_check 2> runs\gate_check.log` on its own line |

The same goes for `clear; git status --short`.

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `python -m support.gate_check`, prompt rule only | `served 1  blocked 0  refunds 0` on all five tickets |
| `python -m support.gate_check`, gate on | `served 0  blocked 1  refunds 0` on all five tickets |
| `git commit` | `4 files changed, 106 insertions(+), 5 deletions(-)` |
| `git push` | `main -> main` to your own `harborline` |

In practice runs before filming: with the prompt rule alone, two or three of the five tickets were served (it varies); after a block, Claude asked the customer for the email on their account, or explained that the order wasn't theirs; and `python -m support.evaluate` with the gate on still scored FCR 15/20 on the dev tickets, as in Lesson 3.2.

See `expected-output.md` for the exact lines and what should match.

## Troubleshooting

- **`ImportError: cannot import name 'gates'`** or **`ModuleNotFoundError: No module named 'support.gates'`**: `support/gates.py` isn't saved, or it's in another folder.
- **`AttributeError: module 'support.gates' has no attribute ...`**: a name in `tools.py` doesn't match `gates.py` (`get_customer`, `lookup_order`, `process_refund`). Compare with the kit's files.
- **`TypeError: handle() takes 1 positional argument but 2 were given`**: `agent.py`'s `handle()` still has the old signature. It needs `prompt=None`.
- **The gate half shows `served 1`**: a tool in `tools.py` still calls `backend.` instead of `gates.`, or `ENFORCE` was left `False` in `gates.py`.
- **Every ticket says `served 0  blocked 0`**: Claude didn't call an order tool at all on your run (it asked for verification straight away). That's a good outcome for the first half; the counters only count order calls.
- **Real tickets now fail with "No verified customer yet"**: `gates.start_case()` must run at the start of `handle()`, and `get_customer` in `tools.py` must call `gates.get_customer`, or no verification is ever recorded.
- **`ModuleNotFoundError: No module named 'support'`**: run from the `harborline` folder with `python -m support.gate_check`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Prompt-based guidance:** rules in the system prompt or a tool description; the model follows them most of the time.
- **Programmatic enforcement:** a check in code that runs on every call, whatever the model decides.
- **Prerequisite gate:** code that blocks a tool until an earlier step has completed, here a verified customer.
- **Skipped verification:** an order read or a refund before the sender is verified, or on someone else's order.
- **Non-zero failure rate:** "almost always" isn't "always"; over many tickets, a rule that usually holds still fails.

## Sources (checked 2026-10-15)

- Claude Code docs, *Use Claude Code features in the SDK*: if instructions conflict, the outcome depends on how Claude interprets them; deterministic logic on tool calls (audit, block, transform) belongs in hooks: https://code.claude.com/docs/en/agent-sdk/claude-code-features
- Claude Code docs, *Give Claude custom tools*, Handle errors: a handler error doesn't stop the agent loop; a composed error message can say what to try instead: https://code.claude.com/docs/en/agent-sdk/custom-tools
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.4 (Domain 1): programmatic enforcement vs prompt-based guidance; prompt instructions alone have a non-zero failure rate where compliance must be deterministic; programmatic prerequisites that block `process_refund` until `get_customer` has returned a verified customer ID. Scenario 1: Customer Support Resolution Agent.

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 3.4: hooks, which see every tool call, stop a refund above $500, and clean up what the tools return.
