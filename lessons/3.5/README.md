# Student kit: Lesson 3.5, Escalation and ambiguity

Claude Certified Architect – Foundations (CCAR-F) · Module 3: Agents with the Claude Agent SDK: the Support Resolution Agent · Lesson 3.5

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Name the real escalation triggers
2. Explain why sentiment is a poor trigger
3. Write criteria with few-shot examples

## What's in the kit

| File | What it is |
|---|---|
| `support/escalation_check.py` | New: five dev tickets, the right call for each (escalate, resolve or ask), and the call the agent makes. Prints one line per ticket and two scores: the right call, out of 5, and requests for a person handed over at once, out of 2 |
| `support/prompts/system.md` | New: the system prompt as a Markdown file. Every ticket; when to hand a case to a person, with the reason; what isn't a reason on its own; two customers with one name; four examples in `<example>` tags |
| `support/agent.py` | Changed: `from pathlib import Path`, and the system prompt read from `prompts/system.md` instead of a string |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `support` folder into your `harborline` folder (it replaces `agent.py`; the other files stay).

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 3.4 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, the support agent (`support/tools.py`, `support/agent.py`), the gate (`support/gates.py`) and the hooks (`support/hooks.py`) committed, and `origin` pointing at your own private `harborline` on GitHub.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 25 minutes, most of it typing. **API spend:** each check makes 5 short agent runs on Haiku 5.5, well under a cent.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, and **Ctrl+G** jumps to a line.

### 1. Measure

```bash
git status --short                       # prints nothing: a clean tree after Lesson 3.4
code support/escalation_check.py         # type the file (or copy it from the kit), save
clear; python -m support.escalation_check 2> runs/escalation_check.log
```

- **`TICKETS`** maps five dev tickets to the right call: `T-005` and `T-022` ask for a person (escalate); `T-023` wants money back for a price drop, which the refund policy doesn't cover (escalate); `T-017` is annoyed, but its refund is in scope (resolve); `T-015` is signed with a name two customers share (ask for an identifier).
- **`ASKED_FOR_PERSON`**: the two tickets where the customer asked for a person.
- **`outcome(calls)`** turns what happened into one word: an escalation in the backend's ledger is `escalate`; a `lookup_order` call or a refund is `resolve`; neither is `ask`.
- **`main()`** runs each ticket on a fresh backend (`backend.reset()`), compares the outcome with the right call, and, for the two person requests, checks whether `lookup_order` came before `escalate_to_human` (then the hand-over wasn't at once). One line per ticket, then the first two sentences of the reply, then the two scores.
- **`2> runs/escalation_check.log`** keeps Claude Code's connectors notice (once per agent run) out of the output. `runs/` is git-ignored.

**In the lesson:** `right call 5/5 · asked for a person, handed over at once 0/2`. The agent already made the right call on every ticket, but on both person requests it looked the order up first.

### 2. The criteria

```bash
clear; mkdir support/prompts
code support/prompts/system.md           # type the file (or copy it from the kit), save
code support/agent.py                    # the import and the two SYSTEM lines, save
```

- **`## Every ticket`**: what the old prompt said: verify with `get_customer`, look up the order, refund what the policy allows, four sentences or fewer. `{date}` is a placeholder the agent fills in.
- **`## When to hand a case to a person`** starts with the reason (a person is slower and costs more), then the triggers: the customer asks for a person (verify, then escalate at once, without looking anything up or trying to solve it); the policy doesn't cover the request; no progress; a refund above $500.
- **Not a reason on its own:** frustration (if the request is in scope, say you understand and fix it; escalate only if they then ask for a person), and how sure the model feels.
- **Two customers match a name:** ask for the email or an order number; never pick one.
- **`## Examples`**: four, in `<examples>` / `<example>` tags: an annoyed customer whose refund is in scope; "I want a human, not a bot"; a request the policy has no exception for; two accounts with one name. None of them is one of the five test tickets.

**`support/agent.py`**: after `import sys`, add `from pathlib import Path`. Then select the whole `SYSTEM = (...)` block (8 lines) and type in its place:

```python
PROMPT = Path(__file__).parent / "prompts" / "system.md"
SYSTEM = PROMPT.read_text().replace("{date}", str(BUSINESS_DATE))
```

The tools, the hooks and `OPTIONS` don't change. If the prompt file is missing, the agent stops at start-up with `FileNotFoundError` instead of running with no rules.

### 3. Measure again

```bash
clear; python -m support.escalation_check 2> runs/escalation_check.log
```

**In the lesson:** `right call 5/5 · asked for a person, handed over at once 2/2`. `T-005` and `T-022`: `get_customer, escalate_to_human`, nothing in between. `T-023` still looks the order up first, which is right: it isn't a request for a person.

### 4. Commit

```bash
clear; git status --short
git add support
git commit -m "Lesson 3.5: escalation criteria and examples, in a prompt file"
git push
```

`git status --short` shows ` M support/agent.py`, `?? support/escalation_check.py` and `?? support/prompts/`. The commit has three files (`3 files changed, 105 insertions(+), 8 deletions(-)`). Your commit ID will differ from the lesson's.

## Windows, macOS and Linux

`git`, `code`, `mkdir` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m support.escalation_check 2> runs/escalation_check.log` | the same line | `cls`, then `python -m support.escalation_check 2> runs\escalation_check.log` on its own line |

The same goes for `clear; mkdir support/prompts` (cmd.exe: `mkdir support\prompts`) and `clear; git status --short`.

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `escalation_check`, before | `right call 5/5 · asked for a person, handed over at once 0/2` |
| `escalation_check`, after | `right call 5/5 · asked for a person, handed over at once 2/2` |
| `git commit` | `3 files changed, 105 insertions(+), 8 deletions(-)` |
| `git push` | `main -> main` to your own `harborline` |

In practice runs before filming: before the change, `5/5 · 0/2` three times out of three; after it, `5/5 · 2/2` four times out of four. One extra prompt line, "Escalate to a person whenever the customer is upset or angry", sent all three annoyed customers with in-scope refunds (T-017, T-035, T-038) to a person in 6 of 6 runs: sentiment is a poor trigger.

See `expected-output.md` for the exact lines and what should match.

## Troubleshooting

- **`FileNotFoundError: ... support/prompts/system.md`**: the folder or the file is missing, or it's named differently. It must be `support/prompts/system.md`, next to `agent.py`'s folder.
- **`NameError: name 'Path' is not defined`**: the `from pathlib import Path` line is missing in `agent.py`.
- **The reply says "Today is {date}"** or the date is wrong: the `.replace("{date}", str(BUSINESS_DATE))` part is missing, or the placeholder in `system.md` is spelled differently.
- **`0/2` again after the change**: check that `agent.py` really reads the file (print `SYSTEM[:80]` once in a Python shell), and that the person rule says to escalate at once, without looking anything up. Then run the check again: one run can differ.
- **`ModuleNotFoundError: No module named 'support'`**: run from the `harborline` folder with `python -m support.escalation_check`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Escalation criteria:** the written rules for when the agent hands a case to a person.
- **Policy gap:** a request the policy doesn't cover, or covers ambiguously.
- **Sentiment-based escalation:** handing over because the customer sounds upset; a poor proxy for how hard the case is.
- **Few-shot examples:** a few worked cases in the prompt that show the decision.
- **Multiple matches:** a lookup that returns more than one customer: ask for an identifier, never pick one.

## Sources (checked 2026-10-15)

- Anthropic docs, *Prompting best practices*: Use examples effectively (few-shot or multishot prompting; relevant, diverse, in `<example>` tags; "Include 3–5 examples for best results"); Add context to improve performance ("explaining to Claude why such behavior is important"): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 5.2 (escalation triggers; explicit requests versus straightforward issues; sentiment and self-reported confidence as unreliable proxies; multiple customer matches); Task Statement 4.2 (few-shot examples). Scenario 1: Customer Support Resolution Agent.

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 3.6: multi-concern requests and handoffs, when one message asks for several things, and a person takes over a case without reading the transcript.
