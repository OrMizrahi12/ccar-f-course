# Student kit: Lesson 3.4, Hooks: intercept and normalize

Claude Certified Architect – Foundations (CCAR-F) · Module 3: Agents with the Claude Agent SDK: the Support Resolution Agent · Lesson 3.4

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Block a refund above $500 with a hook
2. Normalize what the tools return
3. Choose a hook over a prompt rule

## What's in the kit

| File | What it is |
|---|---|
| `harborline/normalize.py` | New: one format for order dates and statuses. `to_utc()` turns Unix seconds or an ISO 8601 timestamp into UTC ISO 8601 (a plain date stays as it is); `order()` returns a copy of an order with UTC dates and the status name from the old warehouse's own codes |
| `support/hooks.py` | New: the two hooks. `refund_limit()` (PreToolUse: above `REFUND_LIMIT`, $500, deny the call with a reason that sends Claude to `escalate_to_human`), `normalize_order()` (PostToolUse: replace `lookup_order`'s result with the normalized order through `updatedToolOutput`), and `HOOKS`, the two matchers |
| `support/agent.py` | Changed: one import, and `hooks=HOOKS,` in `OPTIONS` |
| `support/hook_check.py` | New: both hooks called directly, then the agent on two messages with the hooks off and on |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `harborline/normalize.py` into your `harborline/harborline` folder, and the kit's `support` files into your `harborline/support` folder (it replaces `agent.py`; the other files stay).

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 3.3 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, the support agent (`support/tools.py`, `support/agent.py`) and the verification gate (`support/gates.py`) committed, and `origin` pointing at your own private `harborline` on GitHub.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 25 minutes, most of it typing. **API spend:** the hook check makes 3 short agent runs on Haiku 5.5, well under a cent.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, and **Ctrl+G** jumps to a line.

### 1. Normalize

```bash
git status --short                 # prints nothing: a clean tree after Lesson 3.3
code harborline/normalize.py       # type the file (or copy it from the kit), save
```

- **The docstring** names the problem: web orders use ISO 8601 with an offset; orders from the old warehouse use Unix seconds and numeric status codes.
- **`status_name`** comes from `legacy.warehouse.codes`, the warehouse's own table (`4` delivered, `7` returned, and so on). **`DATE_FIELDS`** lists the three date fields.
- **`to_utc(value)`**: a number is Unix seconds; a string with a `T` is an ISO 8601 timestamp, converted to UTC; anything else (a plain date like `"2026-10-08"`, or `None`) stays. Every timestamp comes out as `YYYY-MM-DDTHH:MM:SSZ`.
- **`order(record)`** copies the order, so the original is never changed, converts each date field it has, and turns a numeric status into its name.

### 2. The hooks

```bash
code support/hooks.py              # type the file (or copy it from the kit), save
code support/agent.py              # line 17 + line 39, save
```

- **`REFUND_LIMIT = 500.00`**: above this, a support lead approves (the refund policy, section 6).
- **`refund_limit(input_data, tool_use_id, context)`** is a hook callback: the SDK calls it with the tool call's input. At or below the limit it returns `{}`, and the call goes on. Above it, it returns a PreToolUse decision: `"permissionDecision": "deny"` and a `permissionDecisionReason` that Claude reads in place of the tool's result: "Refunds above $500 need a support lead. Call escalate_to_human instead; don't retry."
- **`normalize_order(...)`** is a PostToolUse callback. `input_data["tool_response"]` is the tool's result as a list of content blocks; the hook reads the first block's text as JSON. If it isn't the JSON we expect, or it's an error rather than an order (no `order_id`), it returns `{}` and leaves the result alone. Otherwise it returns `updatedToolOutput`: a text block with the normalized order. Claude only ever reads that one.
- **`HOOKS`** maps each event to its `HookMatcher`s: PreToolUse on `mcp__harborline__process_refund` (the tool's full MCP name) with `refund_limit`, PostToolUse on `mcp__harborline__lookup_order` with `normalize_order`.

**`support/agent.py`**: after line 16 (`from support import gates`) add `from support.hooks import HOOKS`. In `OPTIONS`, after `max_budget_usd=0.10,` add:

```python
    hooks=HOOKS,
```

Every `query()` the agent runs now goes through both hooks. The gate from Lesson 3.3 is still inside the tools; a refund the hook denies never reaches the gate or the backend.

### 3. Prove it

```bash
code support/hook_check.py         # type the file (or copy it from the kit), save
clear; python -m support.hook_check 2> runs/hook_check.log
```

- **`KETTLE`** and **`DESK`**: two messages with a `From:` line, like real tickets. Mateo asks about order `HL-10023` (from the old warehouse: status `7`, returned, but it also has a delivery date) and wants to return the kettle. Grace's $649 desk (`HL-10177`) arrived with a cracked leg.
- **`direct()`** calls both hooks with no model: the normalizer on `HL-10023`, raw from the backend, and `refund_limit` with $42.00 and $649.00 (the input shape the SDK sends; the hook only reads the amount).
- **`run()`** sets `agent.OPTIONS.hooks` to the hooks or to `None`, resets the backend, and handles the message. One line per run: refunds paid and the tools Claude called, then the first two sentences of the reply. Switching the hooks off is only for this comparison.
- **`main()`**: the direct calls, then the kettle with the hooks off, the kettle with them on, and the desk with them on.
- **`2> runs/hook_check.log`** keeps Claude Code's connectors notice (once per agent run) out of the output. `runs/` is git-ignored.

**In the lesson:** called directly: `status 7 -> returned`, the Unix delivery date as `2026-06-19T17:46:49Z`, `refund $42.00: allow`, `refund $649.00: deny` with the reason. Through the agent: the kettle with the hooks off called `process_refund` on the returned order (the backend's policy check refused it, `refunds 0`); with the hooks on, Claude said the order is "already marked as returned" and didn't try; the desk was handed to `escalate_to_human`. Your agent lines may differ (see `expected-output.md`); the direct calls won't.

### 4. Commit

```bash
clear; git status --short
git add harborline support
git commit -m "Lesson 3.4: a refund-limit hook and normalized orders"
git push
```

`git status --short` shows ` M support/agent.py`, `?? harborline/normalize.py`, `?? support/hook_check.py` and `?? support/hooks.py`. The commit has four files (`4 files changed, 156 insertions(+)`). Your commit ID will differ from the lesson's.

## Windows, macOS and Linux

`git`, `code` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m support.hook_check 2> runs/hook_check.log` | the same line | `cls`, then `python -m support.hook_check 2> runs\hook_check.log` on its own line |

The same goes for `clear; git status --short`.

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `python -m support.hook_check`, called directly | `status 7 -> returned`; `refund $42.00: allow`; `refund $649.00: deny` + the reason |
| kettle, hooks off | `refunds 0  get_customer, lookup_order, process_refund` (a refund tried on a returned order; refused by the backend) |
| kettle, hooks on | `refunds 0  get_customer, lookup_order`; the reply says "already marked as returned" |
| desk, hooks on | `refunds 0  get_customer, lookup_order, escalate_to_human` |
| `git commit` | `4 files changed, 156 insertions(+)` |
| `git push` | `main -> main` to your own `harborline` |

In practice runs before filming: the $649 desk, in 31 runs with four different messages (and with the $500 sentence taken out of the system prompt), never got a `process_refund` call: the rule is also in two tool descriptions, and Claude followed it. The hook is there for the run where it wouldn't. The returned kettle: with the hooks off, a refund was tried on 5 of 6 runs and Claude never called the order returned; with the hooks on, "returned" 6 of 6, no refund call.

See `expected-output.md` for the exact lines and what should match.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'harborline.normalize'`** or **`... 'support.hooks'`**: the file isn't saved, or it's in another folder (`normalize.py` goes in `harborline/harborline/`, next to `backend.py`; `hooks.py` in `harborline/support/`).
- **The kettle line with the hooks on still says "delivered", not "returned"**: check that `HOOKS` uses the full MCP names, `mcp__harborline__lookup_order` and `mcp__harborline__process_refund`, as in the kit, and that `agent.py` passes `hooks=HOOKS`.
- **`refund $649.00: allow`** in the direct calls: `REFUND_LIMIT` or the comparison in `refund_limit()` differs from the kit's (`amount <= REFUND_LIMIT` returns `{}`).
- **`KeyError: 'tool_response'`** or a crash inside `normalize_order`: the hook is registered under `PreToolUse` instead of `PostToolUse`. PreToolUse inputs have no result yet.
- **`TypeError` about `handle()`**: `agent.py` must still have Lesson 3.3's `handle(ticket_id, prompt=None)`; the hook check passes its own message.
- **`ModuleNotFoundError: No module named 'support'`**: run from the `harborline` folder with `python -m support.hook_check`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Hook:** your code that runs at a fixed point in the agent loop, on every matching event.
- **PreToolUse:** runs before a tool call; can deny it, with a reason Claude reads, or change its input.
- **PostToolUse:** runs after a tool returns, before Claude reads the result; can replace the result.
- **Matcher:** the pattern that picks which tool calls a hook sees (`mcp__harborline__process_refund`).
- **Deterministic guarantee:** a rule that holds on every call, because code checks it, not the model.

## Sources (checked 2026-10-15)

- Claude Code docs, *Intercept and control agent behavior with hooks*: PreToolUse and PostToolUse, matchers, `permissionDecision` / `permissionDecisionReason` ("tells the model why, so it avoids retrying"), `updatedToolOutput` ("To replace the tool's output before Claude sees it"): https://code.claude.com/docs/en/agent-sdk/hooks
- Claude Code docs, *Configure permissions*: hooks run first; "a hook deny applies even in `bypassPermissions` mode": https://code.claude.com/docs/en/agent-sdk/permissions
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.5 (Domain 1): hooks that intercept tool results for transformation and outgoing tool calls for compliance (blocking refunds above a threshold, redirecting to human escalation); normalizing Unix timestamps, ISO 8601 and numeric status codes; hooks for deterministic guarantees versus prompt instructions for probabilistic compliance. Scenario 1: Customer Support Resolution Agent.

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 3.5: escalation and ambiguity, when the agent should hand a case to a person, and when it shouldn't.
