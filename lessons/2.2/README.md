# Student kit: Lesson 2.2, Rename, split, constrain

Claude Certified Architect – Foundations (CCAR-F) · Module 2: Tool Design & MCP Integration · Lesson 2.2

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson (the generic tool of step 1 and the split of step 2), every command in order, what the run printed in the lesson, the one command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Rename overlapping tools so each has one distinct job
2. Split a generic tool into tools with clear inputs and outputs
3. Find system-prompt lines that override good descriptions

## What's in the kit

| File | What it is |
|---|---|
| `step-1/loop/tools.py` | Step 1: Lesson 2.1's five tools plus `query_backend`, one generic tool over the whole backend (a `kind` switch and one free-text `query`), with its handler. The problem, typed out |
| `loop/tools.py` | Step 2: the split. `query_backend` is gone; its one new job became `check_refund`, with an input contract (`order_id`, `reason`, optional `sku` and `opened`) and an output contract (`allowed`, `refund`, `rule`). `process_refund`'s description gains one boundary sentence. This is the file the lesson committed |
| `experiments/m2/prompt_override.py` | The test: the 16 labeled requests, three tries per column, scored on the first tool Claude calls. Column 1 sends no system prompt; each line you pass on the command line gets its own column |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What the run printed in the lesson, line by line, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy `step-1/loop/tools.py` to `harborline/loop/tools.py` and the kit's `experiments` folder into `harborline`; for step 2, copy the kit's `loop/tools.py` over it.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 2.1 and Lab 1 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv` (`anthropic` 1.13.0, `python-dotenv` 1.2.4, `pytest` 9.1.1), `pytest` passing, `origin` pointing at your own private `harborline` on GitHub, Lesson 1.2's usage logger (`harborline/usage.py`), Lesson 2.1's `loop/tools.py` (five tools with the rewritten descriptions) and the `experiments/m2` folder.
- **Your API key in Harborline's `.env`** (Lesson 0.6, step 3). `python -m scripts.check_setup` should say `ANTHROPIC_API_KEY is set`. The script loads the key from `.env` and never prints it.
- About 30 minutes, most of it typing. The lesson's API spend was **about three and a half cents** on Claude Haiku 5.5 for its one run (144 calls).

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder: the script is run as a module (`python -m experiments.m2.prompt_override`), so it can import Harborline's shared code and the tools.

### 1. One tool for everything

```bash
git status --short                 # prints nothing: a clean tree after Lesson 2.1
code loop/tools.py                 # add the generic tool (or copy step-1/loop/tools.py), save
code experiments/m2/prompt_override.py   # type the file (or copy it from the kit), save
```

In the lesson, **Ctrl+J** hides the terminal panel while a file is typed, so the editor gets the full height.

Customers keep asking whether they can return something, and none of the five tools answers that without paying. The quick fix many teams reach for is one tool over the whole backend:

- **`from harborline import backend, data, policy`**: `data` brings in the policy text.
- **`QUERY_BACKEND`**: an honest description (it says what every kind does) and a schema with `kind` (customer, order, orders or refund) and one `query` string, which has to be an email, an order ID, a customer ID or a whole question, depending on `kind`. The schema can't say which.
- **`query_backend(kind, query)`**: four branches, four result shapes. An account, an order, a list of orders, and for `refund` the whole policy as text (1,771 characters): Claude has to work out the rule itself.
- Added to `TOOLS` and `HANDLERS`. Three of its four kinds do exactly what tools you already have do.

What `experiments/m2/prompt_override.py` holds:

- **The docstring**: the two ways to run it. Column 1 sends no system prompt; each line you pass gets its own column, sent as the whole system prompt.
- **`SIGNED_IN`**: every request starts with "Signed-in customer: C-1046", because `list_orders` needs a customer ID.
- **`ALSO_OK`**, written before the first run: a refund request may start with `lookup_order` or `check_refund` (a refund needs the order's facts first).
- **`first_call()`**: one request. With no line, the `system` key is left out entirely, so column 1 has no system prompt at all; with a line, that line is the whole system prompt. Same model, `MAX_TOKENS` and tools in every column. Every call is logged. It returns the first `tool_use` block's name and input, found by type, or the stop reason of a text answer.
- **The main block**: column 1 is always "no line", and each command-line argument adds a column. All the tries for one request (three per column) go to a thread pool at once. A miss is a first call outside the label and `ALSO_OK`. Each row prints the scores per column; under a row with misses, the request and, per column, the most common wrong first call with the input Claude sent. Last, one total per column and the input tokens and cost.

**Run it now?** The lesson doesn't. Run off camera three times with `query_backend` in the set, Claude never picked it first: 0 of 48 tries, every run. Solved? No. Two right answers for one request is a risk you don't control, and the contract problem doesn't go away.

### 2. Split it by purpose

```bash
code loop/tools.py                 # the split (or copy the kit's loop/tools.py), save
```

`customer`, `order` and `orders` already have tools of their own: that was the overlap, so they go. The one new job, answering whether a refund is allowed without paying it, becomes a purpose-specific tool:

- **Drop `data`** from the import: nothing needs it now.
- **`process_refund`'s description** gets a boundary at the end: "Only asking what the policy allows? Use check_refund." It's the only change to Lesson 2.1's descriptions.
- **Replace the generic block** (the dictionary and its handler, 33 lines) with `CHECK_REFUND`. Its description states the output contract first: returns `allowed` (true or false), `refund` (the most it can pay, in US dollars) and `rule` (the policy rule that decided); then when to use it (a customer asks whether they can return something, or how much they'd get back); then where its job ends: to pay, use `process_refund`.
- **The input contract**: `order_id` (HL- plus five digits), `reason` (from the policy's own list, the same enum as `process_refund`), and two optional fields: `sku` and `opened` (for electronics). Four named fields, two of them required.
- **`check_refund()`**: looks up the order, then runs the policy's own check, the same rule code `process_refund` runs. A check and a payment can never disagree, and nothing is paid.
- **`TOOLS` and `HANDLERS`**: swap `QUERY_BACKEND` / `query_backend` for `CHECK_REFUND` / `check_refund`.

Side by side: `query_backend` took a kind and a string, and could return anything. `check_refund` takes four named fields, and returns three.

### 3. One line in the system prompt

```bash
clear; python -m experiments.m2.prompt_override "When a customer mentions shipping or delivery, call list_orders first." "If a customer asks about an order but has no order ID, use list_orders to find it."
```

Line 2 is the kind of line a team adds after customers kept being asked for order numbers they didn't have. Line 3 says the same thing by the situation, not by a word. 144 calls, nine side by side for each request.

**In the lesson:** no line, 45 of 48; the keyword line, 39; the same intent keyed to the situation, 46; 271,371 input tokens, $0.0356. With the keyword line, R01 ("Has order HL-10190 shipped yet?") and R12 ("... Please refund the shipping fee") went to `list_orders` three times out of three, and R09 ("When was HL-10072 delivered?") two of three, each with the signed-in customer's ID and the order number ignored. The same intent without the keyword: back to the right tools. Only one line changed, and the three rows that moved each contain one of its words. R15 ("Track HL-10063") stayed put this time; in earlier test runs it sometimes moved: a line can reach past its own words. Column 1 sent nothing outside the refund requests to `check_refund`.

Then one look at your own prompt:

```bash
code loop/agent.py                 # a look only; nothing changes
```

The agent from Lab 1 imports `TOOLS`, every tool you have. Its system prompt says it can't issue refunds yet; in Lesson 1.4 that was true, because it had two tools. Now it holds `process_refund` and `check_refund`. The prompt says one thing, the tool list another. More wording isn't the fix: an agent that mustn't refund shouldn't get the refund tool. Choosing each agent's tools is the next lesson's topic.

### 4. Commit

```bash
git status --short          # M loop/tools.py   ?? experiments/m2/prompt_override.py
git add loop/tools.py experiments/m2/prompt_override.py
git commit -m "Lesson 2.2: split a generic tool, test system-prompt lines"
git push
```

The commit has the two files (`2 files changed, 120 insertions(+), 2 deletions(-)`), and `git push` sends it to `origin`, your own private `harborline`. Your commit ID will differ from the lesson's. `runs/` doesn't show up in `git status`: it's ignored, and its usage log now holds this lesson's calls too, labelled `2.2 no line` and `2.2 with a line`.

## Windows, macOS and Linux

`git`, `code` and the `python -m ...` commands are the same on every system (run them with the environment active). Only one line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m experiments.m2.prompt_override "..." "..."` | the same line | `cls`, then `python -m experiments.m2.prompt_override "..." "..."` on its own line |

Keep each line in double quotes, so it arrives as one argument.

- **Windows:** `code loop/tools.py` works with forward slashes in PowerShell. If your venv's `python` isn't found, activate the environment first (`.venv\Scripts\Activate.ps1`, Lesson 0.6).
- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, and **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal, in your WSL home folder.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| The generic tool, off camera (three runs, no line) | `query_backend` was never the first pick: 0 of 48 tries in every run |
| `python -m experiments.m2.prompt_override "<keyword line>" "<intent line>"` | No line 45/48; keyword line 39/48 (R01 0/3, R12 0/3, R09 2/3, all to `list_orders`); intent line 46/48; 271,371 input tokens, $0.0356 |
| `git commit` | `2 files changed, 120 insertions(+), 2 deletions(-)` |
| `git push` | `main -> main` to your own `harborline` |
| API spend | About three and a half cents on Claude Haiku 5.5 |

Your scores, token counts and costs can differ from these, run to run. See `expected-output.md` for what should match.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'experiments'`**, **`'loop'`** or **`'harborline'`**: you ran the file directly (`python experiments/m2/prompt_override.py`), or you're not in the `harborline` folder. `cd ~/projects/harborline` and run it as a module.
- **`ImportError: cannot import name 'TOOLS' from 'loop.tools'`** or a `SyntaxError` in `loop/tools.py`: a typo in the edit, often a missing comma or bracket where the generic block was replaced. Compare your file with the kit's `loop/tools.py`.
- **`TypeError: check_refund() got an unexpected keyword argument`**: the handler's parameters don't match the schema's property names. They must be `order_id`, `reason`, `sku` and `opened`.
- **`ModuleNotFoundError: No module named 'harborline.usage'`**: Lesson 1.2's `harborline/usage.py` is missing. Do Lesson 1.2 first.
- **Only one column in the output**: the shell split or dropped your lines. Put each line in double quotes, and type the whole command on one line.
- **`ModuleNotFoundError: No module named 'anthropic'`** or **`python: command not found`**: the environment isn't active in this terminal. Activate it (Lesson 0.6); the prompt should start with `(.venv)`.
- **An error about the API key, or `401` `authentication_error`**: `.env` is missing, empty or not saved, or the key is incomplete or disabled. Run `python -m scripts.check_setup`: it says which. Create a new key in the Console if you need one (Lesson 0.4).
- **`429` `rate_limit_error`**: nine calls go out at once for each request. Wait a minute and run it again; the SDK already retries a few times on its own.
- **Your numbers differ from the lesson's**: expected. Look for the shape: the keyword line moves requests that contain its words, and the same intent written for the situation doesn't.
- **The run seems stuck**: 144 real calls, nine at a time, and each row prints when its nine tries finish. Give it a minute or two.
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.
- **Never paste your API key into code or into a chat.** If a key leaks, disable it in the Console first, then create a new one (Lesson 0.4).

## Key terms

- **Functional overlap:** two or more tools whose names or descriptions claim the same job, so Claude has more than one plausible pick for the same request.
- **Generic tool:** one tool that does several different jobs behind a mode switch (`kind`, `action`, `mode`) and a loose input, so its schema can't say what each job needs or returns.
- **Input/output contract:** what a tool requires (named, typed, required fields) and what it returns (named fields), stated in its schema and description.
- **Purpose-specific tool:** a tool with one job, a name that says that job, and its own contract.
- **Keyword-sensitive instruction:** a system-prompt line triggered by a word rather than by the situation it was written for. It creates an unintended link between that word and a tool, and can override the tools' descriptions.

## Sources (checked 2026-10-14)

- Anthropic, *Writing effective tools for agents* (published September 11, 2025): each tool needs a clear, distinct purpose; tools that overlap in function or have a vague purpose confuse agents; describe and enforce expected inputs and outputs with strict data models; name input parameters unambiguously (`user_id`, not `user`): https://www.anthropic.com/engineering/writing-tools-for-agents
- Define tools, best practices for tool definitions: consolidate related operations into fewer tools, such as one tool with an `action` parameter instead of `create_pr`, `review_pr` and `merge_pr`. The lesson's rule: same resource and same contract, consolidate; different inputs or results, split: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- Prompting best practices, tool usage: Claude's latest models are trained for precise instruction following and benefit from explicit direction to use specific tools; replace blanket defaults with more targeted instructions (that section was written for an earlier Opus model; the advice is general): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 2.1 (Domain 2: Tool Design & MCP Integration), Scenario 1: Customer Support Resolution Agent and Scenario 4: Developer Productivity with Claude

Models and APIs change. If a number or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 2.3: how many tools an agent should have, and how `tool_choice` decides whether Claude must call one.
