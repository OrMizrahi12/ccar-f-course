# Student kit: Lesson 3.6, Multi-concern requests and handoffs

Claude Certified Architect – Foundations (CCAR-F) · Module 3: Agents with the Claude Agent SDK: the Support Resolution Agent · Lesson 3.6

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Answer every request in one reply
2. Write a structured hand-off
3. Design it for a person without the transcript

## What's in the kit

| File | What it is |
|---|---|
| `support/case_check.py` | New: three dev tickets with three requests each (T-004, T-007, T-016) and three hand-off tickets (T-005, T-022, T-023). Prints, per ticket, how many requests the reply answered and the tools called in each turn; per hand-off, the fields left empty and the recommended next step; then two scores |
| `support/handoff.py` | New: the hand-off tool definition, `HANDOFF`: customer_id, order_id, root_cause, amount, recommended_action, summary, all required, each described for a person who never sees the conversation |
| `support/tools.py` | Changed: `escalate_to_human` uses `HANDOFF` and passes the new fields to the backend |
| `support/prompts/system.md` | Changed: a "Several requests in one message" section, a hand-off paragraph, and the refund policy at the end (`{policy}`) |
| `support/agent.py` | Changed: `from harborline import data`, and `{policy}` filled with the refund policy |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `support` folder into your `harborline` folder (it replaces `tools.py`, `agent.py` and `prompts/system.md`; the other files stay).

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 3.5 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, the support agent with its gate and hooks, and `support/prompts/system.md` committed, and `origin` pointing at your own private `harborline` on GitHub.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 25 minutes, most of it typing. **API spend:** each check makes 6 short agent runs on Haiku 5.5, about half a cent.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, and **Ctrl+G** jumps to a line.

### 1. Measure

```bash
git status --short                       # prints nothing: a clean tree after Lesson 3.5
code support/case_check.py               # type the file (or copy it from the kit), save
clear; python -m support.case_check 2> runs/case_check.log
```

- **`MULTI`** maps each multi-request ticket to the other order the reply should name, and the words that answer its question: T-004 asks how long refunds take ("5 business days"), T-007 asks for the email on file, T-016 asks whether shipping is refunded on a return (it isn't, so "not refunded", "n't refunded" and "don't refund" all count).
- **`HANDOFF`** and **`FIELDS`**: the three tickets that should go to a person, and the fields a hand-off needs.
- **`run(ticket_id)`** runs one ticket with the agent's own `OPTIONS`. It reads the stream itself, because it needs one thing `handle()` doesn't keep: which tool calls came in the same turn. Calls in one assistant message (one `message_id`) were made together.
- **`main()`** scores each multi ticket on a fresh backend: a refund in the backend's ledger, the other order named in the reply, the question answered. It prints the turns with ` + ` between calls in one turn and ` | ` between turns. For each hand-off ticket it reads the escalation the backend recorded, lists the empty fields, and prints the recommended next step as a person in the queue would read it.
- **`2> runs/case_check.log`** keeps Claude Code's connectors notice (once per agent run) out of the output. `runs/` is git-ignored.

**In the lesson:** `requests answered 7/9 · hand-offs complete 0/3`. The agent already looked both orders up in one turn, but missed the question only the policy answers, and every hand-off was missing `order_id`, `amount` and `recommended_action`.

### 2. The hand-off

```bash
code support/handoff.py                  # type the file (or copy it from the kit), save
code support/tools.py                    # four small edits, save
```

- **`support/handoff.py`**: a docstring that says who reads a hand-off, and `HANDOFF`, the tool's description and input schema. The description tells Claude the person reads only this hand-off. All six fields are required, so a hand-off can't leave one out.
- **`support/tools.py`**: line 15 becomes `from loop.tools import PROCESS_REFUND` (the old definition isn't imported any more); after `from support import gates` add `from support.handoff import HANDOFF`; the decorator becomes `@tool("escalate_to_human", HANDOFF["description"],` / `      HANDOFF["input_schema"])`; and the backend call's last line becomes four:

```python
                 order_id=args["order_id"], reason=args["root_cause"],
                 amount=args["amount"],
                 recommended_action=args["recommended_action"],
                 summary=args["summary"])
```

The backend already stores `order_id`, `amount` and `recommended_action`; the old tool never asked for them.

### 3. The policy

```bash
code support/prompts/system.md           # three additions, save
code support/agent.py                    # two edits, save
```

- **`support/prompts/system.md`**: after the "Every ticket" section, a new section:

```markdown
## Several requests in one message
- Split the message into its separate requests.
- Look up every order you need at once, in the same turn.
- Answer every request in one reply, in the order they were asked.
  The refund policy below answers most questions.
```

  after the "Not a reason on its own" list, a paragraph:

```markdown
When you hand a case over, the person never sees this conversation:
the hand-off needs the customer, the order, the root cause, the
amount and the next step.
```

  and at the very end:

```markdown
## The refund policy
{policy}
```

- **`support/agent.py`**: before `from harborline.config import ...` add `from harborline import data`, and the `SYSTEM` line becomes:

```python
SYSTEM = (PROMPT.read_text().replace("{date}", str(BUSINESS_DATE))
          .replace("{policy}", data.refund_policy()))
```

The policy text is `data/refund_policy.md`, the same file customers read: one source, the shared context for every part of every reply.

### 4. Measure again

```bash
clear; python -m support.case_check 2> runs/case_check.log
```

**In the lesson:** `requests answered 9/9 · hand-offs complete 3/3`, with a real next step under each hand-off.

### 5. Commit

```bash
clear; git status --short
git add support
git commit -m "Lesson 3.6: a structured hand-off, and the policy as shared context"
git push
```

`git status --short` shows three changed files (`agent.py`, `prompts/system.md`, `tools.py`) and two new ones (`case_check.py`, `handoff.py`). The commit has `5 files changed, 127 insertions(+), 5 deletions(-)`. Your commit ID will differ from the lesson's.

## Windows, macOS and Linux

`git`, `code` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m support.case_check 2> runs/case_check.log` | the same line | `cls`, then `python -m support.case_check 2> runs\case_check.log` on its own line |

The same goes for `clear; git status --short`.

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `case_check`, before | `requests answered 7/9 · hand-offs complete 0/3` |
| `case_check`, after | `requests answered 9/9 · hand-offs complete 3/3` |
| `git commit` | `5 files changed, 127 insertions(+), 5 deletions(-)` |
| `git push` | `main -> main` to your own `harborline` |

In practice runs before filming, the agent as Lesson 3.5 left it put `get_customer` and both `lookup_order` calls in one turn on all three multi tickets, every time; it missed the questions only the policy answers ("I don't have a standard timeline"); and its hand-offs were good prose with `order_id`, `amount` and `recommended_action` empty, every time.

See `expected-output.md` for the exact lines and what should match.

## Troubleshooting

- **`KeyError: 'root_cause'`** (or another field) in `tools.py`: the tool still uses the old definition. Check that the decorator reads `HANDOFF["description"]` and `HANDOFF["input_schema"]`.
- **`ImportError: cannot import name 'HANDOFF'`**: `support/handoff.py` is missing, or the variable is named differently.
- **`NameError: name 'data' is not defined`**: the `from harborline import data` line is missing in `agent.py`.
- **The reply says "{policy}"** or the agent still doesn't know the refund time: the `.replace("{policy}", ...)` part is missing, or the placeholder in `system.md` is spelled differently.
- **`8/9` after the change**: read that ticket's reply. The check counts words, not meaning: a correct answer worded another way counts as a miss. Run the check again; one run can differ.
- **`ModuleNotFoundError: No module named 'support'`**: run from the `harborline` folder with `python -m support.case_check`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Multi-concern request:** one message that asks for several separate things.
- **Parallel tool calls:** several tool calls in one turn, for lookups that don't depend on each other.
- **Shared context:** what every part of the answer draws on; here, the refund policy in the prompt.
- **Structured hand-off:** the fields a person needs to take over: customer, order, root cause, amount, next step.
- **Recommended action:** the next step the agent proposes, so the person starts from a decision, not from zero.

## Sources (checked 2026-10-15)

- Anthropic docs, *Parallel tool use*: Claude 4 and later models make parallel tool calls by default; "Only batch tool calls that are independent of each other.": https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use
- Anthropic docs, *Define tools*: "Provide extremely detailed descriptions", including what each parameter means: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.4 (multi-concern requests: decompose, investigate in parallel with shared context, one resolution; structured hand-off summaries for people without the transcript). Scenario 1: Customer Support Resolution Agent.

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 3.7: long conversations without losing facts, when amounts, dates and promises blur as a conversation grows.
