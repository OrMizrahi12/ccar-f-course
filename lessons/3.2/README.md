# Student kit: Lesson 3.2, The support agent: tools, loop and a target

Claude Certified Architect – Foundations (CCAR-F) · Module 3: Agents with the Claude Agent SDK: the Support Resolution Agent · Lesson 3.2

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Wire the support agent's four tools, two that read and two that act
2. Read the message stream and the result message
3. Measure first-contact resolution on labeled tickets

## What's in the kit

| File | What it is |
|---|---|
| `support/tools.py` | Changed: Lesson 3.1's file plus `process_refund` and `escalate_to_human` (Lab 1's descriptions and schemas), one `TOOLS` list, the in-process server built from it, and `NAMES`, the full tool names for `allowed_tools` |
| `support/agent.py` | New: the support agent. `SYSTEM`, `OPTIONS`, `handle(ticket_id)` (one ticket: the tools Claude called, its reply, the `ResultMessage`) and a `main()` that prints them |
| `support/evaluate.py` | New: `grade()` and a `main()` that runs the 20 labeled dev tickets and prints first-contact resolution (FCR), escalation recall, wrong refunds and the cost |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `support` folder into your `harborline` folder (it replaces `support/tools.py`; `support/hello_agent.py` from Lesson 3.1 stays as it is).

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 3.1 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, `claude-agent-sdk==0.2.165` installed, `support/tools.py` and `support/hello_agent.py` committed, and `origin` pointing at your own private `harborline` on GitHub.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 35 minutes, most of it typing. **API spend in the lesson: about $0.016** (one ticket, $0.0008, then 20 tickets, $0.0146, on Haiku 5.5). The cost figures are the SDK's client-side estimates, not billing data.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, so the editor gets the full height.

### 1. Four tools: two that read, two that act

```bash
git status --short                 # prints nothing: a clean tree after Lesson 3.1
code support/tools.py              # one import line, then replace the server line (or copy the file from the kit), save
```

- **Line 15**, a new import: `from loop.tools import ESCALATE_TO_HUMAN, PROCESS_REFUND`. Lab 1's tool definitions already hold their descriptions and input schemas.
- **From the old `server = create_sdk_mcp_server(...)` line to the end**, select and type over it (in the lesson: **Ctrl+G** 43, then **Ctrl+Shift+End**):
  - `@tool("process_refund", ...)`: calls `backend.process_refund` with the order ID, the amount, the reason and the SKU. The backend checks the refund policy itself and refuses what it doesn't allow, whatever the model asks for.
  - `@tool("escalate_to_human", ...)`: calls `backend.escalate_to_human` with the customer ID, the reason and a summary for the person who takes the case.
  - `TOOLS = [get_customer, lookup_order, process_refund, escalate_to_human]`, the server built from that list, and `NAMES = [f"mcp__harborline__{t.name}" for t in TOOLS]`. One list feeds both, so a new tool can't be served but forgotten in `allowed_tools`.

### 2. One ticket, and what the run tells us

```bash
code support/agent.py              # type the file (or copy it from the kit), save
clear; python -m support.agent T-003
```

- **`SYSTEM`**: verify the sender with `get_customer` first, then look up the order; refund what the policy allows (`process_refund` checks it); hand the case to a person when the customer asks for one, when a refund is above $500, or when the policy doesn't cover the request; four sentences or fewer.
- **`OPTIONS`**: Lesson 3.1's locked-down options (`tools=[]`, `permission_mode="dontAsk"`, `setting_sources=[]`) with `allowed_tools=NAMES`, and two safety nets: `max_turns=10`, `max_budget_usd=0.10`.
- **`handle(ticket_id)`** sends the ticket as the prompt and reads the stream. From each `AssistantMessage` it keeps the tool calls (`ToolUseBlock`, by their short names) and the latest text (`TextBlock`, Claude's reply). It keeps the `ResultMessage` and returns all three. Claude chooses each next tool; the SDK decides when the loop ends.
- **`main()`** prints the tools, the reply, and from the `ResultMessage`: `subtype`, `num_turns`, `total_cost_usd` and `session_id`.

**In the lesson** (T-003, a customer who changed their mind about a lamp): the connectors notice (see Lesson 3.1), `tools: get_customer, lookup_order, process_refund`, a reply with a $74.00 refund for the Ceramic Table Lamp (refund ID RF-0001, shipping not included), and `success: 4 turns, $0.0008, session …`.

### 3. The number: first-contact resolution on labeled tickets

```bash
code support/evaluate.py           # type the file (or copy it from the kit), save
clear; python -m support.evaluate 2> runs/evaluate.log
```

- **What we measure** (the docstring): **FCR** = solved with no person involved and exactly the refunds the label expects; **escalation recall** = of the tickets that need a person, how many got one; **wrong refunds** = money paid that the label doesn't expect.
- **`grade(label, refunds, escalations)`** looks at what the agent did, never at what it said: the refunds in the backend's ledger against the label's expected refunds (by order and amount), and whether a case reached a person.
- **`main()`** takes the 20 dev tickets. For each: `backend.reset()` (empty refund and escalation ledgers), `handle()`, `grade()`, one line (verdict, turns, cost, tools). Then the summary line. The 30 test tickets are kept for the lab, so you don't tune the agent on the tickets that measure it.
- **`2> runs/evaluate.log`** sends standard error to a log file: that's where Claude Code prints its connectors notice, once per ticket. `runs/` is git-ignored.

**In the lesson:** `FCR 15/20 (75%) · escalation recall 3/3 · wrong refunds 1 · $0.0146`. Every run ended with subtype `success`, and five tickets still weren't resolved. Scenario 1's target is 80%. With three of the 20 needing a person, the most this set allows is 17/20 (85%).

### 4. Commit

```bash
clear; git status --short
git add support
git commit -m "Lesson 3.2: the support agent with four tools, and an FCR baseline"
git push
```

`git status --short` shows ` M support/tools.py`, `?? support/agent.py` and `?? support/evaluate.py`. The commit has three files (`3 files changed, 148 insertions(+), 2 deletions(-)`). Your commit ID will differ from the lesson's.

## Windows, macOS and Linux

`git`, `code` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m support.evaluate 2> runs/evaluate.log` | the same line | `cls`, then `python -m support.evaluate 2> runs\evaluate.log` on its own line |

The same goes for `clear; python -m support.agent T-003` and `clear; git status --short`.

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `python -m support.agent T-003` | `tools: get_customer, lookup_order, process_refund`; a $74.00 refund; `success: 4 turns, $0.0008` |
| `python -m support.evaluate` | `FCR 15/20 (75%) · escalation recall 3/3 · wrong refunds 1 · $0.0146` |
| The two failures | T-002 `wrong refund` (an opened e-reader: `process_refund` has no input for "opened", so the policy never saw it); T-015 `refund missing` (a name and no email, two customers with that name: Claude asked which one, which needs a second message) |
| `git commit` | `3 files changed, 148 insertions(+), 2 deletions(-)` |
| `git push` | `main -> main` to your own `harborline` |
| API spend | about $0.016 |

See `expected-output.md` for the exact lines and what should match.

## Troubleshooting

- **`ImportError: cannot import name 'NAMES'`** (or `'server'`): `support/tools.py` isn't saved, or its last three lines differ from the kit's.
- **`ImportError: cannot import name 'PROCESS_REFUND'`**: Lab 1's `loop/tools.py` is missing or different. Compare with Lab 1's solution.
- **`ModuleNotFoundError: No module named 'support'`**, **`'loop'`** or **`'harborline'`**: you're not in the `harborline` folder, or you ran the file directly. `cd ~/projects/harborline` and use `python -m support.agent T-003`.
- **An authentication error**: `ANTHROPIC_API_KEY` isn't in your `.env`. Check with `python scripts/check_setup.py` (Lesson 0.6); it says whether the key is set without printing it.
- **A tool call is denied**: its full name isn't in `allowed_tools`. Print `NAMES`: each one is `mcp__harborline__` + the tool's name.
- **`error_max_turns` or `error_max_budget_usd`**: a safety net stopped the run. Check the system prompt and the tools against the kit's files.
- **`No such file or directory: runs/evaluate.log`**: create the folder first with `mkdir runs`.
- **Your FCR differs from 15/20**: Claude's choices vary between runs. In the lesson's rehearsals the dev set scored 15/20 each time, but a ticket or two can change. What should match: escalation recall near 3/3, and T-002 and T-015 as the likely failures.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **First-contact resolution (FCR):** the share of tickets solved in the first exchange, with no person involved and exactly the right actions.
- **Result message (`ResultMessage`):** the last message of every run: subtype, number of turns, cost, usage and session ID.
- **Subtype:** how the loop ended (`success`, or a limit such as `error_max_turns`), not whether the work was right.
- **Labeled tickets:** tickets with the right outcome and the exact expected refunds written down in advance.
- **Escalation recall:** of the tickets that need a person, the share that reached one.

## Sources (checked 2026-10-15)

- Claude Code docs, *How the agent loop works*: Claude calls tools until it produces a response with no tool calls; the result message carries the final text, usage, cost and session ID; the subtype is the primary way to check termination state; all result subtypes carry the cost, usage, turns and session ID: https://code.claude.com/docs/en/agent-sdk/agent-loop
- Claude Code docs, *Track cost and usage*: `total_cost_usd` is a client-side estimate, not authoritative billing data: https://code.claude.com/docs/en/agent-sdk/cost-tracking
- Claude Code docs, *Agent SDK reference: Python*: `query()`, `ClaudeAgentOptions`, `AssistantMessage`, `ToolUseBlock`, `TextBlock`, `ResultMessage`: https://code.claude.com/docs/en/agent-sdk/python
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.1 (Domain 1), Scenario 1: Customer Support Resolution Agent (80%+ first-contact resolution while knowing when to escalate)

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 3.3: enforcement, not instructions, with a gate the agent can't skip.
