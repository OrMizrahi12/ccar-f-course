# Student kit: Lesson 2.3, How many tools, and tool_choice

Claude Certified Architect – Foundations (CCAR-F) · Module 2: Tool Design & MCP Integration · Lesson 2.3

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each run printed in the lesson, the one command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Explain why fewer tools select better, and scope tools to a role
2. Choose auto, any, a named tool or none for a requirement
3. Handle models that reject forced tool use

## What's in the kit

| File | What it is |
|---|---|
| `experiments/m2/routing_eval.py` | Lesson 2.1's measuring stick with one line changed: `check_refund` joins `LOOKUPS`, because it only reads, and lookups Claude makes on the way run for real |
| `experiments/m2/tool_count.py` | Step 1: the same 24 requests, three tries each, with Harborline's six tools and with eighteen (twelve realistic extras that never run). Prints a row only where the two sets disagree, then a table: scores, extra picks, text replies, input tokens per call and cost |
| `loop/agent.py` | Step 2: Lab 1's agent with its own tool list. `ROLE_TOOLS` holds the five tools its job needs; `process_refund` isn't one of them. The system prompt is unchanged |
| `experiments/m2/tool_choice.py` | Step 3: one request, five `tool_choice` settings (`auto`, `any`, a named tool, `none`, and `asked`: auto with the tool named in the request and every tool strict). Takes an optional model name |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each run printed in the lesson, and what will differ on yours |

The files are exactly the ones the lesson committed. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `experiments` and `loop` folders into `harborline` (the two existing files are replaced by the lesson's versions).

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 2.2 and Lab 1 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv` (`anthropic` 1.13.0, `python-dotenv` 1.2.4, `pytest` 9.1.1), `pytest` passing (54 tests), `origin` pointing at your own private `harborline` on GitHub, Lesson 1.2's usage logger (`harborline/usage.py`), Lab 1's agent (`loop/agent.py`), Lesson 2.1's `experiments/m2/routing_eval.py` and Lesson 2.2's `loop/tools.py` (six tools, `check_refund` included).
- **Your API key in Harborline's `.env`** (Lesson 0.6, step 3). `python -m scripts.check_setup` should say `ANTHROPIC_API_KEY is set`. The scripts load the key from `.env` and never print it.
- About 45 minutes, most of it typing. The lesson's API spend was **about nine cents**: almost seven cents for the tool-count run (Claude Haiku 5.5), a fifth of a cent each for the agent and the Haiku `tool_choice` run, and about two cents for the one short run on Claude Sonnet 5.5.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder: the scripts are run as modules (`python -m experiments.m2.tool_count`), so they can import Harborline's shared code, the tools and Lesson 2.1's eval.

### 1. Eighteen tools or six

```bash
git status --short                       # prints nothing: a clean tree after Lesson 2.2
code experiments/m2/routing_eval.py      # line 21: add , "check_refund" to LOOKUPS, save
code experiments/m2/tool_count.py        # type the file (or copy it from the kit), save
```

In the lesson, **Ctrl+J** hides the terminal panel while a file is typed, so the editor gets the full height.

Harborline has six tools now, and real support teams keep adding more. What does that do to Claude's choices? First, one fix: Lesson 2.1's rule is that lookups Claude makes on the way run for real, and `check_refund` only reads, so it joins `LOOKUPS`.

What `experiments/m2/tool_count.py` holds:

- **The imports**: Lesson 2.1's measuring stick, not retyped: `decide`, `correct`, the held-out requests (`HELD_OUT`) and `TRIES`.
- **`EXTRA`**: twelve more tools a support team might really add: cancel an order; change a delivery address, an email or a phone number; reset a password; a return label; store credit (which is not a refund); a coupon; product details; a delivery estimate (before anything is bought); a note on the case; loyalty points. Each gets one short sentence, to keep the file small; real tools would get Lesson 2.1's full treatment, and cost even more. None of them is the right answer to any of the 24 requests: that would be overlap, Lesson 2.2's problem. Some are near neighbors on purpose: `update_phone` beside `get_customer`, store credit beside `process_refund`. And none of them ever runs: `decide()` only runs lookups.
- **`MORE`**: the six tools plus the twelve, eighteen in all. Each extra is built from its name, its description and its inputs, all strings.
- **`show()`**: prints one row of the final table.
- **The main block**: one client and a pool of six threads, so both sets run side by side. The 16 labeled requests, signed in as C-1046, plus the 8 held out. For each request, three tries with 6 tools and three with 18, all submitted at once. As they come back, it counts the calls, input tokens and cost, whether Claude picked one of the twelve extras, and whether it replied in text instead of calling anything. `correct()` is Lesson 2.1's own scoring: the right tool, with the right input. A row prints only where the two sets disagree, with the wrong pick next to it; a progress line counts the requests as they finish; at the end, the table, one column per set.

Decide before you run it what counts as noise. The lesson's line: a gap of two tries or fewer, out of 72, is noise.

```bash
clear; python -m experiments.m2.tool_count
```

That's 144 first decisions, plus any lookups Claude makes on the way, six calls at a time.

**In the lesson:** one row differed: R10 (`get_customer`), 3/3 with six tools and 2/3 with eighteen, and the miss wasn't an extra tool but `end_turn`, a text reply. One try out of 72: noise, by the line drawn in advance. The table: labeled 39/48 with six tools against 38/48 with eighteen; held-out 24/24 both; extras picked 0 and 0; text replies 9 and 10. Selection held. What changed is the bill: 1,996 input tokens per call against 3,143, about 57% more on every call, for twelve tools this agent never touched. Every tool definition goes into the prompt on every request, the lookups on the way included.

### 2. Scope tools to a role

```bash
code loop/agent.py                       # the import, ROLE_TOOLS, tools=ROLE_TOOLS; save
```

Lab 1's system prompt says: "You can't issue refunds yet: say what the policy allows." But `run()` sends `TOOLS`: all six, `process_refund` included. A prompt line is a request; the tool list is what's possible. Three edits:

- **The import**: instead of `TOOLS`, import the five tools this agent needs by name (`CHECK_REFUND`, `ESCALATE_TO_HUMAN`, `GET_CUSTOMER`, `LIST_ORDERS`, `LOOKUP_ORDER`), plus `run_tool`.
- **After `SYSTEM`**: a two-line comment that says why (it answers, checks what the policy allows and hands off to a person; it never pays refunds, so it isn't given `process_refund`), then `ROLE_TOOLS = [GET_CUSTOMER, LOOKUP_ORDER, LIST_ORDERS, CHECK_REFUND, ESCALATE_TO_HUMAN]`. Five, inside the exam's "four or five".
- **In `run()`**: `tools=ROLE_TOOLS`.

The system prompt didn't change, and it no longer fights the tool list.

```bash
pytest -q
clear; python -m loop.agent T-003
```

**In the lesson:** `54 passed`: the loop is the same; only what it offers changed. Then ticket T-003, a lamp and a changed mind: turn 1 `get_customer`, turn 2 `lookup_order`, turn 3 `check_refund` with the order, the reason and the lamp's SKU (allowed, $74), turn 4 `end_turn`: eligible, $74.00, and "I can't issue the refund from here, but a support agent can process it." It checked instead of paying, and `process_refund` isn't one of its options any more. (The shared `run_tool` would still run any handler it's asked to; what changed is what the agent is offered.)

### 3. Who decides: tool_choice

```bash
code experiments/m2/tool_choice.py       # type the file (or copy it from the kit), save
```

What it holds:

- **`REQUEST`**: Lesson 2.1's R13, signed in as C-1046: "I need a supervisor to sign off on a refund over $500." On `auto`, Claude usually answers it in text first. **`ASK`** adds one sentence: "Use the escalate_to_human tool."
- **`STRICT`**: the same tools, each marked `"strict": True` with `additionalProperties: False`, so Claude's inputs always match the schema. Strict doesn't make Claude call anything (Lesson 7.1 teaches it).
- **`CHOICES`**: five rows. `auto`, the default (Claude decides: a tool or a text reply). `any` (it must call a tool, and picks which). `tool`, naming `escalate_to_human` (this tool, now). `none` (text only, though the tools stay defined). And `asked`: `auto`, strict tools, and the tool named in the request.
- **The main block**: the model comes from the command line, Haiku 5.5 by default. Each row is one call: same model, same `MAX_TOKENS`, same request; only the `tool_choice`, the tools and that added sentence change. A 400 is caught and its message printed, wrapped to fit: nothing ran, so there's no usage to log. Otherwise it logs the usage, adds up the cost, and prints the stop reason, the input tokens and the types of the blocks that came back; then each block, found by type, never by position: text, shortened, or a tool call with its input. Nothing is ever executed.

```bash
clear; python -m experiments.m2.tool_choice
python -m experiments.m2.tool_choice claude-sonnet-5-5
```

**In the lesson, on Haiku 5.5:** `auto`: `end_turn`, thinking and text (Claude chose to reply first). `any`: only a `tool_use` block, no thinking, no text, straight to `escalate_to_human`, its own pick. `tool`: exactly the named call, nothing before it. Both forced rows used about 120 more input tokens than `auto` (1,991 and 2,000 against 1,871): the docs' tool prompt for forced use is 406 tokens instead of 286. `none`: text, with the tools still defined. `asked`: thinking, then `escalate_to_human`. Five calls: $0.0019.

**On Sonnet 5.5** (its input costs 20 times Haiku's, so it's one short run): `auto`: `end_turn`, thinking and text. `any` and `tool`: `400`, `tool_choice: type "tool" and "any" are not supported for this model.` Rejected before anything ran: no response, no usage, nothing in the log. `none`: thinking and text. `asked`: `tool_use`, but two calls in parallel, `get_customer` and `list_orders`: not the tool it named. So asking steers; it doesn't guarantee. Check for the `tool_use` block, and its name, in code. For a fixed JSON answer, use structured outputs (Lesson 7.1). Three billed calls: $0.0193.

On the exam, answer the guide's way: `any`, or a named tool, is how you guarantee a call. In production, check the model's row in the docs' forced tool use table first.

### 4. Commit

```bash
git status --short          # M experiments/m2/routing_eval.py  M loop/agent.py  ?? tool_choice.py  ?? tool_count.py
git add experiments/m2 loop/agent.py
git commit -m "Lesson 2.3: tool count, a role tool list, tool_choice settings"
git push
```

The commit has the four files (`4 files changed, 163 insertions(+), 3 deletions(-)`), and `git push` sends it to `origin`, your own private `harborline`. Your commit ID will differ from the lesson's. `runs/` doesn't show up in `git status`: it's ignored, and its usage log now holds this lesson's calls too. The tool-count calls go through Lesson 2.1's `decide()`, so they're labelled `2.1 routing 6 tools` and `2.1 routing 18 tools`; the agent's are `lab 1 agent`, and the rest `2.3 tool_choice <row>`.

## Windows, macOS and Linux

`git`, `code`, `pytest` and the `python -m ...` commands are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m experiments.m2.tool_count` (and the same for `loop.agent T-003` and `experiments.m2.tool_choice`) | the same line | `cls`, then the `python -m ...` command on its own line |

- **Windows:** `code loop/agent.py` works with forward slashes in PowerShell. If your venv's `python` isn't found, activate the environment first (`.venv\Scripts\Activate.ps1`, Lesson 0.6).
- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, and **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal, in your WSL home folder.
- **The progress line** in step 1 rewrites itself in place (`8/24 requests`, `9/24 requests`, ...). If your terminal prints each update on a new line instead, nothing is wrong: the rows and the table are the same.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `python -m experiments.m2.tool_count` | One differing row: R10 `get_customer` 3/3 vs 2/3 (`end_turn`). Labeled 39/48 vs 38/48; held-out 24/24 vs 24/24; extras picked 0 vs 0; text replies 9 vs 10; input tokens per call 1,996 vs 3,143 (about 57% more); $0.0273 vs $0.0400 |
| `pytest -q` | `54 passed in 1.21s` |
| `python -m loop.agent T-003` | `get_customer` → `lookup_order` → `check_refund` (allowed, $74) → `end_turn`: eligible for $74.00, "I can't issue the refund from here" |
| `python -m experiments.m2.tool_choice` (Haiku 5.5) | auto `end_turn` 1,871 in, thinking, text · any `tool_use` 1,991 in, tool_use only · tool `tool_use` 2,000 in, tool_use only · none `end_turn` 1,871 in, thinking, text · asked `tool_use` 1,944 in, thinking, tool_use (`escalate_to_human`) · $0.0019 |
| `... tool_choice claude-sonnet-5-5` | auto `end_turn` 1,871 in, thinking, text · any and tool `400` "not supported for this model" · none `end_turn` 1,871 in, thinking, text · asked `tool_use` 1,944 in, thinking and two tool calls (`get_customer`, `list_orders`) · $0.0193 |
| `git commit` | `4 files changed, 163 insertions(+), 3 deletions(-)` |
| `git push` | `main -> main` to your own `harborline` |
| API spend | About nine cents |

Your scores, token counts and costs can differ from these, run to run. See `expected-output.md` for what should match.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'experiments'`**, **`'loop'`** or **`'harborline'`**: you ran a file directly (`python experiments/m2/tool_count.py`), or you're not in the `harborline` folder. `cd ~/projects/harborline` and run it as a module.
- **`ImportError: cannot import name 'HELD_OUT'`** (or `decide`, `correct`, `TRIES`) **from 'experiments.m2.routing_eval'**: Lesson 2.1's file is missing or differs. Compare it with the kit's copy.
- **`ImportError: cannot import name 'CHECK_REFUND' from 'loop.tools'`**: Lesson 2.2's `loop/tools.py` (with `check_refund`) isn't in place. Do Lesson 2.2 first, or copy its kit's `loop/tools.py`.
- **`NameError: name 'TOOLS' is not defined`** in `loop/agent.py`: the import no longer brings in `TOOLS`, so the `tools=` line must say `ROLE_TOOLS`.
- **`pytest` fails after step 2**: compare your `loop/agent.py` with the kit's. Only the import, the comment, `ROLE_TOOLS` and the `tools=` line change.
- **A `SyntaxError` or `IndentationError`** in a typed file: often a missing comma, bracket or quote in `EXTRA`, `MORE` or `CHOICES`. Compare your file with the kit's.
- **`any` or `tool` print a 400 on Haiku 5.5 too**: check that the model in `harborline/config.py` is `claude-haiku-5-5`, and that extended thinking isn't switched on: manual extended thinking blocks forced tool use on every model.
- **`any` and `tool` don't print a 400 on Sonnet 5.5**: the API has changed since the lesson. Check the forced tool use table on the Define tools page, and follow it.
- **The `asked` row prints a 400 about the schema**: a strict schema hit a limit. Mark only `escalate_to_human` as strict (the structured outputs page suggests marking only critical tools as strict), and run it again.
- **`ModuleNotFoundError: No module named 'harborline.usage'`**: Lesson 1.2's `harborline/usage.py` is missing. Do Lesson 1.2 first.
- **`ModuleNotFoundError: No module named 'anthropic'`** or **`python: command not found`**: the environment isn't active in this terminal. Activate it (Lesson 0.6); the prompt should start with `(.venv)`.
- **An error about the API key, or `401` `authentication_error`**: `.env` is missing, empty or not saved, or the key is incomplete or disabled. Run `python -m scripts.check_setup`: it says which. Create a new key in the Console if you need one (Lesson 0.4).
- **`429` `rate_limit_error`**: the tool-count run sends six calls at once. Wait a minute and run it again; the SDK already retries a few times on its own.
- **Your numbers differ from the lesson's**: expected. Look for the shape: more input tokens per call with eighteen tools; forced rows with only a `tool_use` block on Haiku; a 400 for `any` and `tool` on Sonnet 5.5.
- **The tool-count run seems stuck**: 144 decisions plus lookups, six calls at a time; the progress line moves every few seconds. Give it a minute or two.
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.
- **Never paste your API key into code or into a chat.** If a key leaks, disable it in the Console first, then create a new one (Lesson 0.4).

## Key terms

- **Decision complexity:** the exam guide's reason why many tools select worse: every tool an agent is given is one more option it weighs on every request, and similar tools are the easiest to confuse.
- **Scoped tool access:** giving an agent only the tools its role needs, so a tool it must not use is never offered (Lesson 4.5 extends it to subagents).
- **`tool_choice`:** the request setting that says whether Claude may, must or must not call a tool: `auto` (the default with tools), `any`, a named `tool`, or `none`.
- **Forced tool use:** `tool_choice` `any` or a named tool. The response is a tool call with no text before it and, on models that accept it, no thinking. Opus 5.5 and Sonnet 5.5 reject it today with a 400 error.
- **Strict tool use:** `"strict": true` on a tool definition: Claude's input is guaranteed to match the schema. It doesn't make Claude call the tool (Lesson 7.1).

## Sources (checked 2026-10-14)

- Anthropic, *Writing effective tools for agents* (published September 11, 2025), "Choosing the right tools for agents": more tools don't always lead to better outcomes; too many tools or overlapping tools can also distract agents: https://www.anthropic.com/engineering/writing-tools-for-agents
- Tool search tool: Claude's ability to pick the right tool degrades once you exceed 30–50 available tools; tool search is the answer for large libraries: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool
- Define tools, "Forcing tool use": the four `tool_choice` options (`auto`, `any`, `tool`, `none`); with `any` or `tool`, no natural-language response or explanation before the tool call; forcing a tool also skips thinking; the table of models and settings that don't support forced tool use (Opus 5.5, Sonnet 5.5 and other recent models return a 400), and what to use there: `auto` with strict tool use, or structured outputs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- Tool use overview, pricing: the tool use system prompt on Haiku 5.5 is 286 tokens with `auto` or `none` and 406 with `any` or `tool`: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- Claude API errors, "Forced tool use not supported": the exact 400 message: https://platform.claude.com/docs/en/api/errors
- Strict tool use and structured outputs (taught in Lesson 7.1): https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use and https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 2.3 (Domain 2: Tool Design & MCP Integration) and Task Statement 4.3, Scenario 1: Customer Support Resolution Agent and Scenario 5: Claude Code for Continuous Integration

Models and APIs change. If a number or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 2.4: structured error responses.
