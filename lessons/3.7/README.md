# Student kit: Lesson 3.7, Long conversations without losing facts

Claude Certified Architect – Foundations (CCAR-F) · Module 3: Agents with the Claude Agent SDK: the Support Resolution Agent · Lesson 3.7

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Explain how summaries blur the facts
2. Keep a case-facts block outside the summary
3. Trim tool results to the fields that matter

## What's in the kit

| File | What it is |
|---|---|
| `support/long_check.py` | New: one customer, eight messages. Each turn is one agent call whose prompt holds the case facts, a running summary of the older exchanges (25 words or fewer, folded by a separate Claude call) and the last two exchanges word for word. The last message asks for every refund; the check scores the last reply against the backend's refund ledger (`facts kept N/9`). This is the version **after** step 3 |
| `support/case_facts.py` | New: the case facts. `trim()` keeps the order fields refunds and status need; `record()` is a PostToolUse hook that keeps the verified customer and one entry per order (items, delivery, total, refunds) from the tool results; `block()` turns them into JSON for the top of every prompt; `python -m support.case_facts HL-10187` prints an order full and trimmed |
| `support/hooks.py` | Changed: the lookup hook also trims, and a second PostToolUse matcher sends every Harborline tool's result to `case_facts.record` |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `support` folder into your `harborline` folder (it replaces `hooks.py`; the other files stay). To see the "before" measurement, leave out the three lines listed in step 3 when you first type `long_check.py`.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 3.6 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, the support agent with its gate, hooks, hand-off and refund policy committed, and `origin` pointing at your own private `harborline` on GitHub.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 25 minutes, most of it typing. **API spend:** each check makes 8 short agent calls and 6 short summary calls on Haiku 5.5, a few cents per run.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, **Ctrl+G** jumps to a line, and **Ctrl+L** selects the whole line.

### 1. Measure

```bash
git status --short                       # prints nothing: a clean tree after Lesson 3.6
code support/long_check.py               # type the file without the three step-3 lines, save
clear; python -m support.long_check 2> runs/long_check.log
```

- **`TURNS`**: Sofia Fairbanks (a seed customer) asks for three refunds on three orders (HL-10158 a cracked mirror, HL-10131 a blanket she changed her mind about, HL-10193 a garden tool set with a broken handle), then four questions the refund policy answers, then: "list every refund, with the amount, the order and the refund reference."
- **`SUMMARIZER`**: a separate Claude call with no tools and one turn. **`fold()`** asks it to update the running summary with the oldest exchange, in 25 words or fewer: deliberately tight, a stand-in for a long chat with a small budget. A real chat would fold only when it runs out of room; this one folds on every turn from the third, so the effect shows in eight messages.
- **`main()`**: each prompt has the summary so far, the last two exchanges word for word, and the new message. Each turn prints its number and the tools it called. At the end: the final summary, the last reply (up to four rows), and the score. The truth is `backend.refunds()`, the ledger: a fact counts when its exact text (amount, order number, refund reference) is in the last reply. `$129.00` and `$129` count the same.
- **`2> runs/long_check.log`** keeps Claude Code's connectors notice (once per call) out of the output. `runs/` is git-ignored.

**In the lesson:** `facts kept 0/9`. The summary kept the references and amounts but not the order numbers, and not that Sofia was verified; on turn 8 the agent asked her to verify her account again before listing anything.

### 2. Case facts and the trim

```bash
code support/case_facts.py               # type the file (or copy it from the kit), save
clear; python -m support.case_facts HL-10187
```

- **`KEEP`** and **`ITEM`**: the order fields a refund or a status question needs (8 of the order's 12), and the fields kept per item.
- **`trim(order)`**: only those fields, with just the payment method.
- **`record(...)`**: a PostToolUse hook. `get_customer` → the customer's ID, name, email and `verified: true`; `process_refund` → the refund's ID and amount under its order; `lookup_order` → the item names, delivery time and total under its order. One entry per order: the per-issue layer, filled from the tools, never from the chat.
- **`block()`**: the facts as JSON under `## Case facts (exact, from the tools)`, for the top of every prompt.

**In the lesson:** `full 12 fields 484 characters`, `trimmed 8 fields 292 characters`, then the trimmed order.

### 3. Wire it in

```bash
code support/hooks.py                    # four edits, save
code support/long_check.py               # three edits, save
```

- **`support/hooks.py`**: after `from harborline import normalize` add `from support import case_facts`; the `normalize_order` docstring becomes `"""Give Claude one format, and only the fields that matter."""`; its `clean = ...` line becomes `clean = case_facts.trim(normalize.order(record))`; and `PostToolUse` gets a second matcher:

```python
    "PostToolUse": [HookMatcher(
        matcher="mcp__harborline__lookup_order",
        hooks=[normalize_order]),
        HookMatcher(matcher="mcp__harborline__.*",
                    hooks=[case_facts.record])],
```

- **`support/long_check.py`**: `from support import gates` becomes `from support import case_facts, gates`; after `gates.start_case()` add `case_facts.start_case()`; and the prompt starts with the block:

```python
        prompt = (case_facts.block() + "\n\n"
                  f"## The conversation so far (summary)\n{summary or '-'}"
```

Nothing old is edited: the summary and the last two exchanges are the same as before; the facts are a separate block, rebuilt from the tools and sent with every turn.

### 4. Measure again

```bash
clear; python -m support.long_check 2> runs/long_check.log
```

**In the lesson:** `facts kept 9/9`. The summary still had no order numbers, but the last reply listed all three refunds with the reference, the amount and the order.

### 5. Commit

```bash
clear; git status --short
git add support
git commit -m "Lesson 3.7: case facts outside the summary, and trimmed order lookups"
git push
```

`git status --short` shows one changed file (`hooks.py`) and two new ones (`case_facts.py`, `long_check.py`). The commit has `3 files changed, 171 insertions(+), 3 deletions(-)`. Your commit ID will differ from the lesson's.

## Windows, macOS and Linux

`git`, `code` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m support.long_check 2> runs/long_check.log` | the same line | `cls`, then `python -m support.long_check 2> runs\long_check.log` on its own line |

The same goes for `clear; python -m support.case_facts HL-10187` and `clear; git status --short`.

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `long_check`, before | `facts kept 0/9` |
| `case_facts HL-10187` | `full 12 fields 484 characters` · `trimmed 8 fields 292 characters` |
| `long_check`, after | `facts kept 9/9` |
| `git commit` | `3 files changed, 171 insertions(+), 3 deletions(-)` |
| `git push` | `main -> main` to your own `harborline` |

In practice runs before filming, the check without the case facts kept 0, 3, 6 and 0 of the nine facts (both 0/9 runs: the agent asked the customer to verify again); with the case facts and the trim, 9/9 in four runs out of four.

See `expected-output.md` for the exact lines and what should match.

## Troubleshooting

- **`ImportError: cannot import name 'case_facts'`**: `support/case_facts.py` is missing, or it's saved under another name.
- **`AttributeError: module 'support.case_facts' has no attribute 'record'`** (or `trim`, `block`): a function is missing or misspelled in `case_facts.py`.
- **`facts kept 9/9` before the change**: the summary happened to keep everything. Summaries vary from run to run; run the check again, or read the summary line to see what it kept.
- **`facts kept 6/9` or less after the change**: read the last reply. If it names the facts in another form (for example "$129.00 USD" or "order 10158"), the check counts words, not meaning. If the reply asks the customer to verify, check that the second `HookMatcher` is in `hooks.py` and that the prompt starts with `case_facts.block()`.
- **`ModuleNotFoundError: No module named 'support'`**: run from the `harborline` folder with `python -m support.long_check`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Progressive summarization:** folding older messages into a shorter and shorter running summary as a conversation grows.
- **Case facts:** the exact facts of a case (amounts, orders, references, dates), kept apart and sent with every turn.
- **Per-issue layer:** the facts kept one entry per issue, here one per order.
- **Tool result trimming:** keeping only the fields that matter from a tool's output, before it enters the context.
- **Context window:** everything the model sees on one call; tool results pile up in it.

## Sources (checked 2026-10-15)

- Anthropic docs, *Manage tool context*: "Tool definitions and accumulated `tool_result` blocks consume your context window.": https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context
- Anthropic docs, *Prompting best practices*, state management: "Use structured formats for state data" (JSON for structured information): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 5.1 (progressive summarization risks; a persistent case-facts block outside summarized history; a separate layer for multi-issue sessions; trimming verbose tool outputs before they accumulate). Scenario 1: Customer Support Resolution Agent.

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 3.8: sessions. When to resume a conversation, when to fork it, and when to start fresh.
