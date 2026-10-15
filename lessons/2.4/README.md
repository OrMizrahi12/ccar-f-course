# Student kit: Lesson 2.4, Structured error responses

Claude Certified Architect – Foundations (CCAR-F) · Module 2: Tool Design & MCP Integration · Lesson 2.4

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each run printed in the lesson, the one command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Flag tool failures and tell four error kinds apart
2. Return a category, a retry flag and a readable reason
3. Tell a failed lookup from an empty answer

## What's in the kit

| File | What it is |
|---|---|
| `harborline/tool_errors.py` | New in step 1: `tool_error(error)`, the content of the `tool_result` for one backend error, as JSON: `errorCategory`, `isRetryable` and the `message`; a policy refusal adds `retriable: false` and a `customerReason` |
| `loop/tools.py` | Step 1: Lesson 2.3's file with one import added and the `except` branch of `run_tool` changed, so a failure goes back as `tool_error(error)`, still with `is_error` |
| `experiments/m2/error_replies.py` | Step 2: the test. Five requests, each a short conversation with a refunds agent's tools, all running for real; a failure goes back one of three ways (generic, sentence, structured); three tries each |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each run printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `harborline`, `loop` and `experiments` folders into your `harborline` folder (the kit's `loop/tools.py` replaces yours).

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 2.3 and Lab 1 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv` (`anthropic` 1.13.0, `python-dotenv` 1.2.4, `pytest` 9.1.1), `pytest` passing (54 tests), `origin` pointing at your own private `harborline` on GitHub, Lesson 1.2's usage logger (`harborline/usage.py`), Lab 1's agent (`loop/agent.py`, with Lesson 2.3's `ROLE_TOOLS`) and Lesson 2.2's `loop/tools.py`.
- **Your API key in Harborline's `.env`** (Lesson 0.6, step 3). `python -m scripts.check_setup` should say `ANTHROPIC_API_KEY is set`. The scripts load the key from `.env` and never print it.
- About 40 minutes, most of it typing. The lesson's API spend was **about four cents** on Claude Haiku 5.5: less than four cents for the test (131 calls) and about a sixth of a cent for the agent.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder: the scripts are run as modules (`python -m experiments.m2.error_replies`), so they can import Harborline's shared code and the tools.

### 1. Name the failure

```bash
git status --short                 # prints nothing: a clean tree after Lesson 2.3
code harborline/errors.py          # a look: one class per kind of failure
code loop/tools.py                 # a look: run_tool's except branch (Ctrl+G 174)
code harborline/tool_errors.py     # type the new file (or copy it from the kit), save
code loop/tools.py                 # one import, the except branch; save
clear; pytest -q                   # 54 passed
```

In the lesson, **Ctrl+J** hides the terminal panel while a file is read or typed, so the editor gets the full height.

**`harborline/errors.py`** (from the starter, not changed) already knows what kind of failure it was. `BackendError` is the base (`kind = "backend"`, `retryable = False`), and each subclass sets its own `kind`: `NotFound` (`not_found`), `InvalidRequest` (`validation`), `PermissionDenied` (`permission`), `PolicyViolation` (`business`) and `ServiceUnavailable` (`transient`, the only one with `retryable = True`).

**`run_tool`** in `loop/tools.py` is where they meet Claude. Until now, a `BackendError` went back as `{"content": str(error), "is_error": True}`: the flag was there, but the content was only the backend's sentence. The kind it knew was dropped.

**`harborline/tool_errors.py`**, one function:

- **The docstring**: `run_tool` sends one of these back with `is_error` true, so Claude can choose its next move: try again, fix the input, explain, or hand off.
- **`tool_error(error)`**: a `BackendError` in, the `tool_result`'s content out. The body has `"errorCategory"` (the error's `kind`), `"isRetryable"` (true only for transient) and `"message"` (the backend's sentence, kept).
- **A business error** (the policy said no, so don't retry): it strips the prefix `Refund not allowed: `, keeps the reason, and adds `"retriable": False` and a `"customerReason"` with a capital first letter, ready to pass on.
- **`json.dumps(body)`**: the content of a `tool_result` is text, so the body goes back as JSON.

**`loop/tools.py`**, the whole change in the loop:

- After `from harborline.errors import BackendError` (line 6), add `from harborline.tool_errors import tool_error`.
- In `run_tool`, the `except` branch (lines 175 and 176 after the import) becomes:

```python
    except BackendError as error:  # what kind, and retry or not
        return result | {"content": tool_error(error), "is_error": True}
```

`pytest -q` still says `54 passed`: the test that checks the error text still finds it, now inside the JSON.

### 2. Same requests, three error replies

```bash
code experiments/m2/error_replies.py      # type the file (or copy it from the kit), save
clear; python -m experiments.m2.error_replies
```

What `experiments/m2/error_replies.py` holds:

- **The imports**: the backend, the model settings (`MAX_TOKENS`, `MODEL`), `BackendError` and `tool_error`, the usage logger, and Lab 1's tools.
- **`TOOLS`**: a refunds agent's five tools: `get_customer`, `lookup_order`, `list_orders`, `process_refund` and `escalate_to_human`. No `check_refund`: this agent goes straight for the refund, so a refusal is something it could try again.
- **`TRIES, TURNS = 3, 5`**: three tries per case and style, up to five turns each.
- **`STYLES`**: how a failure goes back. `generic` always says `Operation failed.`; `sentence` is `str(error)`, the backend's message (what `run_tool` sent until today); `structured` is `tool_error`.
- **`CASES`**, written before the first run, each with what makes the outcome right (a word in the last reply, or a call): **transient** ("Where is my order HL-10211?": its lookup times out once; right if the order's status reaches the customer), **not found** ("Where is my order 12345?": not an order ID), **business** (a refund for final-sale cushion covers from HL-10159), **permission** (a refund on HL-10184, whose customer's account is on review hold; right if the reply names the hold or a lead, or Claude escalates) and **empty** (a customer with no orders).
- **`conversation()`**: one try. The first message is the signed-in customer and the request. It tracks the calls that failed for good, a counter for calls sent again, and the tools Claude used. Each turn is one request with the same model, `MAX_TOKENS` and tools, logged with `log_usage`; no tool calls means Claude is done. Each tool call gets a key, the tool's name and the order: if that key already failed with an error a retry can't fix, the call counts as **sent again**. Then the tool runs for real. On a `BackendError`, the content comes from the style being tested, with `is_error` true, and a non-retryable error marks its key as failed. A try is **right** only if nothing was sent again and one of the case's words shows up in the last reply or in the tools Claude used.
- **`run_case()`**: one case's nine tries in a row (three styles, three tries), re-arming the HL-10211 timeout (`backend.reset()`) before each transient try.
- **The main block**: one client, five threads, so the five cases run side by side. Then the table: a header with the three styles, one row per case (right tries out of three per style), two totals (`right` and `sent again`), and the first 40 characters of each style's last reply in the business case (try 1). Nothing else prints while it runs.

It's 45 conversations with every tool running for real (the backend is fictional: refunds are only recorded in Harborline's data). It takes about a minute and prints nothing until the end.

**In the lesson:** transient, not found, business and empty were 3/3 in every style: Claude retried the timeout on its own and found "final sale" in the order data even with the generic string. **Permission** is where it broke: generic 0/3, sentence 3/3, structured 2/3. **Right** 12, 15 and 14 of 15; **sent again** 2, 0 and 0. With only "Operation failed.", Claude sent the refund again after the account hold had refused it; with a reason, it stopped. The one structured miss: its last reply named no hold and no lead, and it didn't escalate. So for Claude, here, a sentence and the structured body did about the same. The generic string is the bug, and the structure is also for your code: a category to branch on, a retry flag, a customer reason you write once. The business replies: generic "I couldn't process the refund for the ou...", which sounds like a glitch; sentence "I'm sorry the cushion covers weren't wha..."; structured "I can't refund the outdoor cushion cover...", a clear no. 131 calls, $0.0358.

### 3. Retry, explain, or an empty answer

```bash
code harborline/backend.py         # a look: list_orders (Ctrl+G 95)
clear; python -c "from harborline.backend import list_orders; print(list_orders('C-1058'))"
clear; python -m loop.agent T-040
```

`list_orders`' docstring says it: "A customer with no orders gets an empty list: that is a valid answer, not an error." Just above, `lookup_order`'s timeout raises `ServiceUnavailable("The warehouse system timed out. Try again in a moment.")`.

The one-liner prints `[]` for C-1058: the lookup worked and found nothing, so it goes back as a plain result, with no error flag. A timeout is different: the lookup never happened, so it's a transient error.

Then Lab 1's agent, now with the structured errors, on ticket T-040 ("where's my cast iron skillet?"): turn 1 `get_customer`, turn 2 `list_orders`, turn 3 `lookup_order` on HL-10211 and the timeout, `[tool_result is_error] {"errorCategory": "transient", "isRetryable": true, ...`. Turn 4 is the same lookup on the same order, and this time the order comes back. Turn 5, `end_turn`: the skillet is on order HL-10211, still processing, not shipped yet, promised for October 19, 2026. A retry the error invited, not a guess. About a sixth of a cent.

### 4. Commit

```bash
clear; git status --short
git add harborline/tool_errors.py loop/tools.py experiments/m2/error_replies.py
git commit -m "Lesson 2.4: structured tool errors, error replies compared"
git push
```

`git status --short` shows ` M loop/tools.py` and two new files (`?? experiments/m2/error_replies.py`, `?? harborline/tool_errors.py`). The commit has the three files (`3 files changed, 137 insertions(+), 2 deletions(-)`), and `git push` sends it to `origin`, your own private `harborline`. Your commit ID will differ from the lesson's. `runs/` doesn't show up in `git status`: it's ignored, and its usage log now holds this lesson's calls too, labelled `2.4 errors generic`, `2.4 errors sentence`, `2.4 errors structured` and `lab 1 agent`.

## Windows, macOS and Linux

`git`, `code`, `pytest` and the `python ...` commands are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m experiments.m2.error_replies` | the same line | `cls`, then `python -m experiments.m2.error_replies` on its own line |

The same goes for `clear; pytest -q`, the one-liner, `clear; python -m loop.agent T-040` and `clear; git status --short`. Keep the one-liner's outer double quotes and the single quotes around `'C-1058'`.

- **Windows:** `code loop/tools.py` works with forward slashes in PowerShell. If your venv's `python` isn't found, activate the environment first (`.venv\Scripts\Activate.ps1`, Lesson 0.6).
- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel and **Ctrl+G** goes to a line).
- **WSL:** run the Linux commands inside the WSL terminal, in your WSL home folder.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `pytest -q` after step 1 | `54 passed in 0.75s` |
| `python -m experiments.m2.error_replies` | Transient, not found, business, empty 3/3 in every style; permission 0/3, 3/3, 2/3; right 12, 15, 14; sent again 2, 0, 0; 131 calls, $0.0358 |
| `list_orders('C-1058')` | `[]` |
| `python -m loop.agent T-040` | The transient error on HL-10211, the same lookup again, then the answer (5 turns, `end_turn`) |
| `git commit` | `3 files changed, 137 insertions(+), 2 deletions(-)` |
| `git push` | `main -> main` to your own `harborline` |
| API spend | About four cents on Claude Haiku 5.5 |

Your scores, replies, token counts and costs can differ from these, run to run. See `expected-output.md` for what should match.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'experiments'`**, **`'loop'`** or **`'harborline'`**: you ran the file directly (`python experiments/m2/error_replies.py`), or you're not in the `harborline` folder. `cd ~/projects/harborline` and run it as a module.
- **`ModuleNotFoundError: No module named 'harborline.tool_errors'`**: the new file isn't saved, or it's in the wrong folder. It belongs in `harborline/`, next to `errors.py`.
- **`pytest` fails after step 1**: compare `loop/tools.py` with the kit's. Only the import line and the two lines of the `except` branch change; the content must still carry `"is_error": True`.
- **`AttributeError: 'str' object has no attribute 'removeprefix'`**: your Python is older than 3.9. The lesson uses Python 3.12 (Lesson 0.6).
- **`ImportError: cannot import name 'ESCALATE_TO_HUMAN'`** (or another tool): your `loop/tools.py` is missing a tool from the earlier lessons. Compare it with the kit's.
- **The test prints nothing for a minute**: expected. 45 conversations run first; the table prints at the end.
- **`ModuleNotFoundError: No module named 'anthropic'`** or **`python: command not found`**: the environment isn't active in this terminal. Activate it (Lesson 0.6); the prompt should start with `(.venv)`.
- **An error about the API key, or `401` `authentication_error`**: `.env` is missing, empty or not saved, or the key is incomplete or disabled. Run `python -m scripts.check_setup`: it says which. Create a new key in the Console if you need one (Lesson 0.4).
- **`429` `rate_limit_error`**: five conversations run at once. Wait a minute and run it again; the SDK already retries a few times on its own.
- **Your numbers differ from the lesson's**: expected. Look for the shape: with the generic string, Claude may send a refusal's refund again; with a reason, it stops.
- **The agent doesn't retry on T-040**: Claude may explain the delay instead; both are answers to a retryable error. Run it again if you want to see the retry: `lookup_order` times out only on the first call to HL-10211 after the agent starts.
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.
- **Never paste your API key into code or into a chat.** If a key leaks, disable it in the Console first, then create a new one (Lesson 0.4).

## Key terms

- **`is_error` / `isError`:** the flag on a tool result that says the tool failed. The Messages API spells it `is_error`, MCP `isError`. The error goes back to Claude as a result it can act on.
- **Error category:** what kind of failure it was: transient, validation, business or permission (Harborline adds not_found). Each one points to a different next move.
- **Retryable error:** a failure where the same call can work later (a timeout). `isRetryable: false` tells the agent not to waste a try.
- **Customer-friendly reason:** for a policy refusal, the reason in words the agent can pass on, next to `retriable: false`.
- **Valid empty result:** a lookup that worked and found nothing (`[]`): a success, never an error. The opposite of an access failure.

A spelling note: the exam guide writes `isRetryable` on errors and `retriable` on policy violations. The lesson keeps both, as the guide does. Only the flag is a standard.

## Sources (checked 2026-10-14)

- Anthropic, *Writing effective tools for agents* (published September 11, 2025), optimizing tool responses: prompt-engineer your error responses to communicate specific and actionable improvements, rather than opaque error codes or tracebacks: https://www.anthropic.com/engineering/writing-tools-for-agents
- Handle tool calls, handling errors with `is_error`: return the error message in the content with `is_error: true`; write instructive error messages that say what went wrong and what Claude should try next, so it can recover or adapt without guessing: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
- Model Context Protocol specification, version 2026-07-28, Tools, error handling: protocol errors (issues with the request structure, like an unknown tool) and tool execution errors (API failures, input validation, business logic errors) reported in tool results with `isError: true`; clients should give them to the language model to enable self-correction: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 2.2 (Domain 2: Tool Design & MCP Integration), Scenario 1: Customer Support Resolution Agent and Scenario 4: Developer Productivity with Claude

Models and APIs change. If a number or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 2.5: MCP from zero, building a server for Harborline's tools.
