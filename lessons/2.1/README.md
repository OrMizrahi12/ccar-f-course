# Student kit: Lesson 2.1, Tool descriptions that route correctly

Claude Certified Architect – Foundations (CCAR-F) · Module 2: Tool Design & MCP Integration · Lesson 2.1

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson (the first drafts and the final descriptions), every command in order, what each run printed in the lesson, the two commands that differ on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Explain why the description decides which tool Claude picks
2. Write descriptions with inputs, examples, edge cases and boundaries
3. Measure tool selection before and after a change

## What's in the kit

| File | What it is |
|---|---|
| `first-drafts/loop/tools.py` | Step 1: Harborline's five tools with the first drafts most of us would write, one line each. Lesson 1.3's `get_customer` and `lookup_order`, plus `list_orders`, `process_refund` and `escalate_to_human`, all in `TOOLS`, with a handler each. This is the file the before run measures |
| `loop/tools.py` | Step 2: the same file after the rewrite. Only the five description strings and `lookup_order`'s `order_id` line changed: no names, no schemas, no code. This is the file the lesson committed |
| `experiments/m2/routing_eval.py` | The measurement: 16 labeled requests and 8 held out, three tries each. Prints one row per request (the tool it wanted, the most common miss, the score out of three), then one summary line per run |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each run printed in the lesson, line by line, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy `first-drafts/loop/tools.py` to `harborline/loop/tools.py` and the kit's `experiments` folder into `harborline`, run the before measurement, then copy the kit's `loop/tools.py` over it and run the after measurement. Keep the order: the after run reads the before scores.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except two, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 1.6 and Lab 1 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv` (`anthropic` 1.13.0, `python-dotenv` 1.2.4, `pytest` 9.1.1), `pytest` passing, `origin` pointing at your own private `harborline` on GitHub, Lesson 1.2's usage logger (`harborline/usage.py`) and Lesson 1.3's tools (`loop/tools.py`, with `get_customer`, `lookup_order` and `run_tool`).
- **Your API key in Harborline's `.env`** (Lesson 0.6, step 3). `python -m scripts.check_setup` should say `ANTHROPIC_API_KEY is set`. The script loads the key from `.env` and never prints it.
- About 35 minutes, most of it typing. The lesson's API spend was **under four cents** on Claude Haiku 5.5: the before run cost $0.0157 and the after run $0.0203 (each makes at least 72 calls: 24 requests × 3 tries, plus the lookups that run on the way).

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder: the script is run as a module (`python -m experiments.m2.routing_eval`), so it can import Harborline's shared code and the tools.

### 1. Measure the first drafts

```bash
git status --short                 # prints nothing: a clean tree after Lab 1
code loop/tools.py                 # step 1 edits (or copy first-drafts/loop/tools.py), save
mkdir -p experiments/m2
code experiments/m2/routing_eval.py   # type the file (or copy it from the kit), save
clear; python -m experiments.m2.routing_eval before
```

In the lesson, **Ctrl+J** hides the terminal panel while a file is typed, so the editor gets the full height, and **Ctrl+G** jumps to a line.

What changes in `loop/tools.py` in step 1:

- **`import policy`** next to `backend`: `process_refund`'s `reason` takes its allowed values from the policy's own list (`policy.REASONS`).
- **`get_customer`** gains an optional `name`, so `email` is no longer required.
- **Three new tools**, each with a one-line first draft: `list_orders` ("List a customer's orders."), `process_refund` ("Refund an order.", with the order ID, a reason, the amount and, for one item, its SKU) and `escalate_to_human` ("Escalate the case to a human.", with the customer ID, a reason and a summary). Harborline's backend had these functions all along; Claude had no way to ask for them.
- **`TOOLS`** lists all five; **`HANDLERS`** gains three lines, so `run_tool` can reach the new backend functions.
- `lookup_order`'s `order_id` parameter still says "The order ID, as the customer wrote it", Lesson 1.3's line. Remember it.

What `experiments/m2/routing_eval.py` holds, top to bottom:

- **The docstring**: which tool does Claude call, and with what input? Three tries each.
- **`LOOKUPS`** (line 21): the three tools that only read. **`TRIES`** (line 22): three, because one try is an anecdote. **`SAVED`** (line 23): where the before scores go (`runs/routing-before.json`, ignored by git).
- **`HELD_OUT`** (lines 26-43): eight requests written for the lesson, each with its signed-in customer, the right tool and the input it must carry. Labeled before the first run and never edited after it. H1 to H4 type order numbers the way customers do (`10190`, `#10199`, `hl 10203`, `10164`); H5 and H6 want refunds above $500, which Harborline's policy sends to a support lead; H7 and H8 are below that.
- **`decide()`** (lines 46-66): one request with the signed-in customer and the request, the same model, the tools and **no system prompt**. If Claude calls the expected tool, or anything that isn't a lookup, that's the decision, and it never runs: no refund, no escalation. If it calls a lookup first, the lookup runs for real (read only) and Claude gets the record; two rounds at most. A text reply records its stop reason.
- **`correct()`** (lines 69-74): the right tool, an order ID in `HL-` form, the signed-in customer, and the input the label asks for. Anything else is a miss.
- **The main block** (lines 77-116): `before` or `after`; the after run loads the saved before scores. One client and a pool of three, so the tries run side by side. The labeled set is Harborline's 16 routing requests (`data/evals/tool_routing.jsonl`), all signed in as customer `C-1046`. Each row prints the request's ID, the wanted tool, the most common miss and the score out of three (and, in the after run, what it was); the request itself is printed under every miss. Then one summary line per run: labeled score, held-out score, input tokens and cost.

**The before run, in the lesson:** labeled 39/48, held-out 6/24, 97,383 input tokens, $0.0157. The names carry most of the labeled set. H1 to H4 called the right tool, `lookup_order`, with the number as typed (`10190`): the parameter line said "as the customer wrote it", and the backend rejects anything that isn't `HL-` plus five digits. H5 and H6 went straight to `process_refund`, for a $549 espresso machine and a $649 desk. H7 and H8, the small refunds, passed.

### 2. Write descriptions that route

```bash
code loop/tools.py                 # rewrite the six strings (or copy the kit's loop/tools.py), save
```

Only description strings change. Each description now covers what a description that routes needs:

| Part | On `lookup_order` |
|---|---|
| Purpose and returns | One order by its ID: status, items, total, shipping fee, payment, tracking and dates |
| When to use it | Whenever the customer gives an order number |
| Input format | `HL-` plus five digits |
| Edge case | Customers drop the `HL-` or type it in lower case: pass `HL-10234` anyway |
| Boundary | No order number at all? Use `list_orders` first; never guess an ID |

And its `order_id` line now says "HL- plus five digits, like HL-10234": the description and the parameter tell one story. `get_customer`, `list_orders`, `process_refund` and `escalate_to_human` get the same treatment (see the kit's `loop/tools.py`). `process_refund` ends with the sentence that matters most: "Above $500? Use escalate_to_human instead." Write facts, not praise; none of the examples is one of the test requests.

### 3. Measure again

```bash
clear; python -m experiments.m2.routing_eval after
```

**In the lesson:** labeled 40/48, held-out 23/24 (up from 6), 145,177 input tokens, $0.0203. H1 to H4 3/3 (the ID now in `HL-` form); H6 escalated 3/3; H5 2/3 (one try still refunded the espresso machine); H7 and H8 still refunds; R13 1/3. About half again the input tokens, because every description is billed as input on every request. On plain requests the words bought nothing; on order numbers and the $500 rule, nearly everything.

Then read the misses. A description steers; it doesn't enforce (Module 3 puts the $500 rule in code). R13 asks for a supervisor; Claude asks which order, how much and why first, so the label was stricter than the right answer. R06 and R12 were 0/3 in both runs, and Claude was right: their orders don't match the requests, and it said no. Labels can be wrong too.

### 4. Commit

```bash
git status --short          # M loop/tools.py   ?? experiments/m2/
git add loop/tools.py experiments/m2/routing_eval.py
git commit -m "Lesson 2.1: tool descriptions that route, measured before and after"
git push
```

The commit has the two files (`2 files changed, 212 insertions(+), 9 deletions(-)`), and `git push` sends it to `origin`, your own private `harborline`. Your commit ID will differ from the lesson's. `runs/` doesn't show up in `git status`: it's ignored, and its usage log now holds this lesson's calls too, labelled `2.1 routing before` and `2.1 routing after`.

## Windows, macOS and Linux

`git`, `code` and the `python -m ...` commands are the same on every system (run them with the environment active). Two lines differ:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Make the folder | `mkdir -p experiments/m2` | `mkdir experiments/m2` | `mkdir experiments\m2` |
| Clear, then run | `clear; python -m experiments.m2.routing_eval before` | the same line | `cls`, then `python -m experiments.m2.routing_eval before` on its own line |

The same goes for the `after` run. On Windows, `mkdir` creates the missing parent folder by itself, so it needs no `-p`.

- **Windows:** `code loop/tools.py` works with forward slashes in PowerShell. If your venv's `python` isn't found, activate the environment first (`.venv\Scripts\Activate.ps1`, Lesson 0.6).
- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel, and **Ctrl+G** goes to a line).
- **WSL:** run the Linux commands inside the WSL terminal, in your WSL home folder.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `python -m experiments.m2.routing_eval before` | Labeled 39/48, held-out 6/24, 97,383 input tokens, $0.0157. H1-H4: `lookup_order` with the number as typed, 0/3; H5, H6: `process_refund`, 0/3; R06, R12, R13: text replies, 0/3 |
| `python -m experiments.m2.routing_eval after` | Labeled 40/48, held-out 23/24, 145,177 input tokens, $0.0203. H1-H4 3/3, H5 2/3, H6 3/3 (`escalate_to_human`), R13 1/3; R06, R12 still 0/3 |
| `git commit` | `2 files changed, 212 insertions(+), 9 deletions(-)` |
| `git push` | `main -> main` to your own `harborline` |
| API spend | Under four cents on Claude Haiku 5.5 |

Your scores, token counts and costs can differ from these, run to run. See `expected-output.md` for what should match.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'experiments'`**, **`'loop'`** or **`'harborline'`**: you ran the file directly (`python experiments/m2/routing_eval.py`), or you're not in the `harborline` folder. `cd ~/projects/harborline` and run it as a module: `python -m experiments.m2.routing_eval before`.
- **`ImportError: cannot import name 'policy' from 'harborline'`** or **`ORDER_ID_PATTERN`**: your starter is older than the course's. Check that `harborline/policy.py` exists and that `harborline/backend.py` defines `ORDER_ID_PATTERN` (Lesson 0.6's starter has both).
- **`ModuleNotFoundError: No module named 'harborline.usage'`**: Lesson 1.2's `harborline/usage.py` is missing. Do Lesson 1.2 first: it writes that file.
- **`FileNotFoundError: ... runs/routing-before.json`**: you ran `after` before `before`. The after run compares against the saved before scores; run `before` first, with the first drafts.
- **`IndexError: list index out of range`**: you left out the label. Run `python -m experiments.m2.routing_eval before` (or `after`).
- **Your after run shows no `was` marks at all**: the before run already used the new descriptions. Put the first drafts back (`first-drafts/loop/tools.py`), run `before`, then the rewrite, then `after`.
- **`400` `invalid_request_error` about a tool or its schema**: a typo in `loop/tools.py`, such as a missing comma, a property outside `"properties"`, or a `"required"` name that isn't a property. Compare your file with the kit's.
- **`ModuleNotFoundError: No module named 'anthropic'`** or **`python: command not found`**: the environment isn't active in this terminal. Activate it (Lesson 0.6); the prompt should start with `(.venv)`.
- **An error about the API key, or `401` `authentication_error`**: `.env` is missing, empty or not saved, or the key is incomplete or disabled. Run `python -m scripts.check_setup`: it says which. Create a new key in the Console if you need one (Lesson 0.4).
- **`429` `rate_limit_error`**: the three tries of each request run side by side. Wait a minute and run it again; the SDK already retries a few times on its own.
- **Your numbers differ from the lesson's**: expected. Scores move by a try or two from run to run, most of all on requests near a boundary (R13, H5). Look for the shape: the held-out set improves far more than the labeled one, and the after run costs more input tokens.
- **The run seems stuck**: it makes at least 72 real calls, three at a time, and prints each row when its three tries finish. Give it a minute or two.
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them. `git add loop/tools.py experiments/m2/routing_eval.py` adds only the two files.
- **Never paste your API key into code or into a chat.** If a key leaks, disable it in the Console first, then create a new one (Lesson 0.4).

## Key terms

- **Tool selection:** Claude's choice of which tool to call, and with what input, made by reading the request against every tool definition it was sent.
- **Tool description:** the text in a tool definition that says what the tool does and returns, when to use it and when not, what its inputs look like, and its limits. The biggest lever on tool performance.
- **Boundary:** the sentence in a description that says when **not** to use the tool, and what to use instead ("No order number? Use `list_orders` first.").
- **Edge case:** an input the tool will meet that doesn't look like the normal one, and what to do with it ("customers often drop the HL-: pass HL-10234 anyway").
- **Held-out set:** test cases set aside and labeled before you change anything, and never used while you tune, so a score on them shows whether the change works beyond the cases you tuned on.

## Sources (checked 2026-10-14)

- How tool use works, the tool-use contract: the caller is a language model choosing which function to call based on the conversation; Claude sees only the schema you provided, never your code: https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works
- Define tools, best practices for tool definitions: provide extremely detailed descriptions, "by far the most important factor in tool performance"; cover what the tool does, when to use it and when not, what each parameter means and how it affects the tool's behavior, and caveats such as what the tool does not return; aim for at least 3–4 sentences per tool: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- Tool use overview, pricing: tool names, descriptions and schemas are billed as input tokens on every request: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- Anthropic, *Writing effective tools for agents* (published September 11, 2025): describe your tool as you would to a new hire on your team, and make implicit context explicit, such as specialized query formats; in evaluations, specify the tools you expect an agent to call, allow for multiple valid paths, and use held-out test sets so you don't overfit: https://www.anthropic.com/engineering/writing-tools-for-agents
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 2.1 (Domain 2: Tool Design & MCP Integration), Scenario 1: Customer Support Resolution Agent and Scenario 3: Multi-Agent Research System

Models and APIs change. If a number or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 2.2, you rename, split and constrain tools, and test what a system prompt line does to tool selection.
