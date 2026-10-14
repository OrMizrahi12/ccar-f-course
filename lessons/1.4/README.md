# Student kit: Lesson 1.4, The agentic loop

Claude Certified Architect – Foundations (CCAR-F) · Module 1: Claude API Foundations for Architects · Lesson 1.4

This kit holds everything you need to repeat the lesson on your own computer: the two Python files written in the lesson, every command in order, what each run printed in the lesson, the one command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Loop on `stop_reason`: continue on `tool_use`, stop on `end_turn`
2. Feed every tool result back so Claude reasons on it
3. Spot the three stop-rule anti-patterns

## What's in the kit

| File | What it is |
|---|---|
| `loop/agent.py` | Steps 1 and 2: Harborline's agentic loop. `SYSTEM` (the support agent's instructions plus the refund policy), `MAX_TURNS` (a safety net), `LoopStopped` (an ending that isn't an answer), `first_message()` (a ticket as the customer's first message), `show()` (each turn, block by block) and `run(client, messages)`, which calls Claude until it ends its turn and returns every response. Run on its own, it prints each turn and then the history |
| `experiments/m1/antipatterns.py` | Step 3: four ways to decide the loop is done. It runs the real loop once, then asks each stop rule where it would have ended that same run, and what the customer would have received |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each run printed in the lesson, line by line, and what will differ on yours |

The two files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them; if you'd rather not, copy the kit's `loop` and `experiments` folders into your `harborline` folder, so that you have `harborline/loop/agent.py` and `harborline/experiments/m1/antipatterns.py`. Lesson 1.3's `loop/tools.py` stays exactly as it is.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 1.3 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv` (`anthropic` 1.13.0, `python-dotenv` 1.2.4, `pytest` 9.1.1), `pytest` passing, `origin` pointing at your own private `harborline` on GitHub, Lesson 1.2's usage logger (`harborline/usage.py`) and Lesson 1.3's tools (`loop/tools.py` with `TOOLS` and `run_tool`). `agent.py` imports both.
- **Your API key in Harborline's `.env`** (Lesson 0.6, step 3). `python -m scripts.check_setup` should say `ANTHROPIC_API_KEY is set`. The scripts load the key from `.env` and never print it.
- About 25 minutes, most of it typing. The lesson's API spend was **a fraction of a cent** on Claude Haiku 5.5: three runs of two or three short requests each.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder: the scripts are run as modules (`python -m loop.agent`), so they can import Harborline's shared code and each other.

### 1. Write the loop

```bash
git status --short          # prints nothing: a clean tree after Lesson 1.3
code loop/tools.py          # a quick look at Lesson 1.3's file: TOOLS and run_tool
code loop/agent.py          # type the file (or copy it from the kit), save
```

In the lesson, **Ctrl+J** hides the terminal panel while the file is typed, so the editor gets the full height, and **Ctrl+`** brings the terminal back. What `loop/agent.py` holds, top to bottom:

- **`SYSTEM`** (lines 16-23): Harborline's support agent, with Harborline's fixed "today" (so "30 days after delivery" means something). Verify the sender with `get_customer` first; only then look up their orders. Before each tool call, say in a few words what you're checking. No refunds yet: say what the policy allows. Four sentences or fewer, plain text. Then the refund policy.
- **`MAX_TURNS = 10`** (line 24): a safety net for runaway loops, not how the loop stops.
- **`LoopStopped`**: an ending that isn't an answer becomes an exception, never a reply to a customer.
- **`first_message(ticket_id)`**: finds the ticket and turns it into the customer's first message, with the sender's email on a `From:` line, because `get_customer` needs it.
- **`show(turn, response)`**: prints the turn number and its stop reason, then every block by type, never by position: text, tool calls, and anything else (such as thinking) by its type name.
- **`run(client, messages)`** (lines 52-75), the heart. Each turn makes one request with the model, the system prompt, the tools and the **whole** message list, logs the usage (Lesson 1.2), keeps the response and shows it. Then:
  - any stop reason other than `tool_use` or `end_turn` raises `LoopStopped` (`max_tokens`, `refusal`: none of those is an answer);
  - Claude's turn joins the history **exactly as returned**, thinking blocks included;
  - on `end_turn`, it returns every response;
  - otherwise it runs **every** `tool_use` block with `run_tool`, prints the start of each result, and appends them all in **one** user turn, then goes round again;
  - if the `for` loop runs out, that's a failure too: `LoopStopped("no end_turn after 10 turns")`.
- **The `__main__` block** (lines 78-90): loads `.env`, builds the first message from the ticket id on the command line, and runs. The guard is there because `antipatterns.py` imports `run`. Then it prints the history: each message's role and the types of its blocks.

The code never says how many turns a ticket takes. Claude decides; the loop listens to `stop_reason`.

### 2. Run it on two tickets

```bash
clear; python -m loop.agent T-003
clear; python -m loop.agent T-016
```

**T-003**: Amara changed her mind about a ceramic table lamp, order HL-10163. In the lesson the run took three turns: turn 1 checked who was writing (`get_customer`, verified, customer `C-1031`), turn 2 looked up the order (`lookup_order`), and turn 3 ended the turn with the answer: delivered October 3, inside the 30 days, $74.00 back to her card ending 1817, shipping not refunded. None of that was in her message: it came from the tool results, and the History block shows they were in the list Claude saw. Three turns, and the code never said three.

**T-016**: Callum wants to return a pillow, asks where his desk chair is, and whether shipping gets refunded. In the lesson turn 1 verified Callum, and turn 2 asked for **two** `lookup_order` calls in one response; both results went back in one user turn. Then turn 3 stopped on **`max_tokens`**: thinking plus a long answer filled the response budget, and the text stopped mid-sentence. The loop raised `LoopStopped: stopped on max_tokens`, so the cut-off reply never reached Callum. That wasn't planned, but it's the loop's rule at work. Lab 1 handles each stop reason properly. Your run may finish with `end_turn` and a full answer instead; see `expected-output.md`.

### 3. Three stop rules that fail

```bash
code experiments/m1/antipatterns.py               # type the file (or copy it), save
clear; python -m experiments.m1.antipatterns T-003
```

What `antipatterns.py` holds: `text_of()` joins a response's text blocks into one string. Then four stop rules:

1. **`done_words`**: search the reply for "done", "resolved" or "all set".
2. **`fixed_cap`**: stop at turn 2, because "most tickets need two calls".
3. **`any_text`**: any text means finished.
- **`stop_reason`**: `end_turn`, the rule that works.

`where_it_stops()` walks the responses and returns the first turn where a rule says stop. The trick: until a rule says stop, all four loops send exactly the same requests. So the script runs the real loop **once**, and asks each rule where it would have ended: the same evidence for all four, for the price of one run.

In the lesson: `stop_reason` turn 3, `end_turn`, OK, and the customer gets the real answer. `done_words` never stops: Claude finished without the magic words, so that loop would keep calling, and paying. `fixed_cap` turn 2, `tool_use`, WRONG: the customer gets "The account is verified and active. Next I'm looking up...", a promise, not an answer. `any_text` turn 1, WRONG: the customer gets "I'm checking the sender's account...": text and a tool call arrive in the same response. Only `stop_reason` knows.

### 4. Commit

```bash
git status --short          # ?? experiments/m1/antipatterns.py   ?? loop/agent.py
git add loop/agent.py experiments/m1/antipatterns.py
git commit -m "Lesson 1.4: the agentic loop and three stop-rule anti-patterns"
git push
```

The commit adds the two files (`2 files changed, 149 insertions(+)`), and `git push` sends it to `origin`, your own private `harborline`. Your commit id will differ from the lesson's. `runs/` doesn't show up in `git status`: it's ignored, and its usage log now holds this lesson's calls too. This is the loop the coming lessons build on.

## Windows, macOS and Linux

`git`, `code` and the `python -m ...` commands are the same on every system (run them with the environment active). Only one line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m loop.agent T-003` | the same line | `cls`, then `python -m loop.agent T-003` on its own line |

The same goes for the T-016 run and for `python -m experiments.m1.antipatterns T-003`.

- **Windows:** `code loop/agent.py` works with forward slashes in PowerShell. If your venv's `python` isn't found, activate the environment first (`.venv\Scripts\Activate.ps1`, Lesson 0.6).
- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, and **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal, in your WSL home folder.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `python -m loop.agent T-003` | `turn 1: tool_use` (`get_customer`, `C-1031`), `turn 2: tool_use` (`lookup_order` `HL-10163`), `turn 3: end_turn`: delivered October 3, $74.00 to the card ending 1817, $6.95 shipping not refunded; History of 6 messages |
| `python -m loop.agent T-016` | `turn 1: tool_use` (`C-1038`), `turn 2: tool_use` with two `lookup_order` calls (`HL-10168`, `HL-10202`) and two results in one turn, `turn 3: max_tokens`, then `LoopStopped: stopped on max_tokens` |
| `python -m experiments.m1.antipatterns T-003` | A fresh three-turn run; `stop_reason` OK at turn 3; `done_words` never stops; `fixed_cap` WRONG at turn 2; `any_text` WRONG at turn 1 |
| `git commit` | `2 files changed, 149 insertions(+)` |
| `git push` | `main -> main` to your own `harborline` |
| API spend | A fraction of a cent on Claude Haiku 5.5 |

Your wording, turns and verdicts can differ from these, run to run. See `expected-output.md` for what should match.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'loop'`** or **`'harborline'`**: you ran a file directly (`python loop/agent.py`), or you're not in the `harborline` folder. `cd ~/projects/harborline` and run it as a module: `python -m loop.agent T-003`.
- **`ImportError: cannot import name 'run_tool'`** (or `TOOLS`) **from `loop.tools`**: Lesson 1.3's `loop/tools.py` is missing or different. Do Lesson 1.3 first, or copy its kit's `loop/tools.py`.
- **`ModuleNotFoundError: No module named 'harborline.usage'`**: Lesson 1.2's `harborline/usage.py` is missing. Do Lesson 1.2 first: it writes that file.
- **`IndexError: list index out of range`**: you left out the ticket id. Run `python -m loop.agent T-003`.
- **`No ticket T-03`**: the ticket id is misspelled. Harborline's tickets are `T-001` to `T-050`, with three digits.
- **`ModuleNotFoundError: No module named 'anthropic'`** or **`python: command not found`**: the environment isn't active in this terminal. Activate it (Lesson 0.6); the prompt should start with `(.venv)`.
- **An error about the API key, or `401` `authentication_error`**: `.env` is missing, empty or not saved, or the key is incomplete or disabled. Run `python -m scripts.check_setup`: it says which. Create a new key in the Console if you need one (Lesson 0.4).
- **`LoopStopped: stopped on max_tokens`**: the response hit its output budget before Claude finished, as in the lesson's T-016 run. The loop is right to refuse it. Run it again, or wait for Lab 1, which handles each stop reason properly. Don't "fix" it by sending the cut-off text.
- **`LoopStopped: no end_turn after 10 turns`**: the safety net caught a loop that never finished. Check that `run()` appends Claude's turn and then the results every time round; a loop that sends the same history again gets the same answer again.
- **`400` `invalid_request_error` on turn 2 or 3**: the history isn't what the API expects. Append `response.content` exactly as it came back (thinking blocks included, never rebuilt), and send one `tool_result` for every `tool_use` block, all of them in one user turn right after Claude's turn.
- **Claude repeats a lookup, or answers "I can't see your order"**: the results aren't reaching it. Check that `results` holds the dicts `run_tool` returns and that they're appended as `{"role": "user", "content": results}`.
- **A verdict in step 3 comes out right for a wrong rule** (for example `done_words` stops because the answer says "you're all set"): that rule got lucky on this wording. Run it again, and keep the reason in mind: it reads the words, not the signal.
- **`[tool_result]` lines or answers wrap in your terminal**: harmless. The loop prints only the first 60 characters of each result.
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them. `git add loop/agent.py experiments/m1/antipatterns.py` adds only the two new files.
- **Never paste your API key into code or into a chat.** If a key leaks, disable it in the Console first, then create a new one (Lesson 0.4).

## Key terms

- **Agentic loop:** your code's loop that calls Claude, runs the tools it asks for, sends the results back, and repeats until Claude ends its turn.
- **Agent:** a model that chooses its own next step (which tool, and when it's done) from the results it gets back. Lesson 1.5 sets it against fixed workflows.
- **Turn** (in our code): one pass through the loop, one request and its response. A ticket takes as many turns as Claude needs. (The Agent SDK's `max_turns` counts only tool-use round trips.)
- **Safety cap:** a hard limit on turns (`MAX_TURNS` here, the Agent SDK's `max_turns`, the Tool Runner's `max_iterations`) that catches runaway loops. Hitting it is a failure, never the normal way to stop.
- **Anti-pattern:** a common solution that looks reasonable but fails in a predictable way.

## Sources (checked 2026-10-14)

- How tool use works, the agentic loop (client tools): the canonical shape is a `while` loop keyed on `stop_reason`; the loop exits on any other stop reason; "if you're writing a regex to extract a decision from model output, that decision should have been a tool call": https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works
- Tutorial: build a tool-using agent, Ring 2 (the agentic loop; keep a running list and append to it; "Your code no longer needs to know in advance.") and Ring 3 (send back all results together in one user message): https://platform.claude.com/docs/en/agents-and-tools/tool-use/build-a-tool-using-agent
- How the agent loop works (Agent SDK), turns and budget (max turns: maximum tool-use round trips, default no limit) and the `error_max_turns` result subtype: https://code.claude.com/docs/en/agent-sdk/agent-loop
- Handling stop reasons (`end_turn`, `tool_use`, `max_tokens`, `refusal`, `pause_turn`): https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
- Handle tool calls (`tool_result` blocks right after their `tool_use` blocks): https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
- Parallel tool use (every result in a single user message): https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use
- Thinking with tool use (pass thinking blocks back complete and unmodified): https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows
- Claude Haiku 5.5 migration guide (keep conversations append-only; pass thinking blocks back with tool results): https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide
- Tool Runner (the SDK helper runs this same loop; `max_iterations` is optional): https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner
- Anthropic, *Building effective agents* (agents are "LLMs using tools based on environmental feedback in a loop"; stopping conditions such as a maximum number of iterations "to maintain control"): https://www.anthropic.com/engineering/building-effective-agents
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.1 (Domain 1: Agentic Architecture & Orchestration) and Scenario 1: Customer Support Resolution Agent

Models and APIs change. If a number or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 1.5 we set this loop against a fixed workflow.
