# Student kit: Lesson 1.3, Tool use from first principles

Claude Certified Architect – Foundations (CCAR-F) · Module 1: Claude API Foundations for Architects · Lesson 1.3

This kit holds everything you need to repeat the lesson on your own computer: the two Python files written in the lesson, every command in order, what each run printed in the lesson, the one command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Define a tool: name, description, JSON Schema
2. Run a tool call by hand, from `tool_use` to `tool_result`
3. Answer every call in one turn, failures included

## What's in the kit

| File | What it is |
|---|---|
| `loop/tools.py` | Steps 1 and 2: Harborline's first two tool definitions (`GET_CUSTOMER`, `LOOKUP_ORDER`), the `TOOLS` list a request carries, the `HANDLERS` that map each name to a backend function, and `run_tool(call)`, which turns one `tool_use` block into its `tool_result` block |
| `experiments/m1/manual_tool_call.py` | Steps 2 and 3: one tool round trip by hand. It sends the ticket with the tools, runs every `tool_use` block Claude returns, sends all the results back in one user turn, and prints Claude's answer. With `bad`, the customer gives a wrong order number |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each run printed in the lesson, line by line, and what will differ on yours |

The two files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them; if you'd rather not, copy the kit's `loop` and `experiments` folders into your `harborline` folder, so that you have `harborline/loop/tools.py` and `harborline/experiments/m1/manual_tool_call.py`.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 1.2 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv` (`anthropic` 1.13.0, `python-dotenv` 1.2.4, `pytest` 9.1.1), `pytest` passing, `origin` pointing at your own private `harborline` on GitHub, and Lesson 1.2's usage logger, `harborline/usage.py` (`manual_tool_call.py` imports `log_usage` from it).
- **Your API key in Harborline's `.env`** (Lesson 0.6, step 3). `python -m scripts.check_setup` should say `ANTHROPIC_API_KEY is set`. The script loads the key from `.env` and never prints it.
- About 25 minutes, most of it typing. The lesson's API spend was **a fraction of a cent** on Claude Haiku 5.5: each run of `manual_tool_call.py` makes two short requests, and the lesson runs it twice.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder: the script is run as a module (`python -m experiments.m1.manual_tool_call`), so it can import Harborline's shared code and `loop.tools`.

### 1. Define

```bash
git status --short          # prints nothing: a clean tree after Lesson 1.2
mkdir loop
code loop/tools.py          # type lines 1-40 (or copy the file from the kit)
```

A tool is plain data with three fields. What `loop/tools.py` holds:

- **`name`**: what Claude calls the tool by: `get_customer`, `lookup_order`. Letters, digits, underscores and dashes, up to 128 characters.
- **`description`**: the only thing Claude reads to decide whether and when to use the tool. Ours are one or two sentences on purpose: Anthropic's docs ask for extremely detailed descriptions (three or four sentences or more), and Lesson 2.1 measures what better ones buy.
- **`input_schema`**: a JSON Schema object: its `properties`, each with a `type` and a `description`, and the `required` ones. `get_customer` takes one field, `email`; `lookup_order` takes `order_id`, "as the customer wrote it": checking IDs is your code's job, not the model's.
- **`TOOLS`** is the list each request carries. **`HANDLERS`** maps each tool name to a real function in Harborline's backend. That half of the file never leaves your computer: Claude sees the definitions, never the code behind them.

The definitions aren't free: they're billed as input tokens on every request that carries them, plus a tool system prompt the API adds (286 tokens on Claude Haiku 5.5 with the default tool choice).

### 2. Round trip

Still in `loop/tools.py`, type `run_tool` (lines 43-54) and save. It takes one `tool_use` block and returns its `tool_result` block:

- the result starts with `"tool_use_id": call.id`, the thread that ties it to its call;
- an unknown tool name gets an error result;
- otherwise the handler runs with `**call.input` (the input is already a dict that follows the schema);
- a `BackendError` (not found, bad input, …) becomes `"is_error": True` with the backend's own message, and success becomes JSON text.

Every call gets exactly one result, whatever happens.

```bash
code experiments/m1/manual_tool_call.py           # type the file (or copy it), save
clear; python -m experiments.m1.manual_tool_call
```

What `manual_tool_call.py` does:

- `SYSTEM`: Harborline's support assistant; use the tools to check who is writing and to look up any order they mention; call independent tools together, in one turn; two sentences or fewer.
- The ticket is T-008: Elijah asks where order HL-10196 is (the request Lesson 1.2 stopped on). The sender's email goes in a `From:` line. With `bad`, the question becomes "where is my order 12345?".
- `ask()` sends `system`, `tools` and `messages`, logs the usage (Lesson 1.2's habit), and prints the stop reason, the input tokens and every block by type.
- Then three steps, numbered in the code: **1.** Claude asks (if it didn't call a tool, there's nothing to answer and the script stops); **2.** your code runs every `tool_use` block with `run_tool` and prints each result: the end of its id, `is_error`, and the first 45 characters of its content; **3.** it appends Claude's turn exactly as it came back (thinking block included: with tools that's required), then **one** user turn with every result, and asks again.

In the lesson the first response held two `tool_use` blocks, `get_customer` with Elijah's email and `lookup_order` with `HL-10196` (604 tokens in). Your code ran both, each `[tool_result]` line carrying its call's id, and the second response ended the turn (1,168 tokens in, since it carried the tools again, Claude's turn and both results) with the answer: HL-10196 has shipped with Parcelway, estimated to arrive by October 16. Claude never touched the order file: your code did, and Claude read what you sent back.

### 3. Report a failure

```bash
clear; python -m experiments.m1.manual_tool_call bad
```

In the lesson Claude again asked for both tools in one response, and passed `'12345'` to `lookup_order` exactly as written. The backend rejected it, and `run_tool` returned `is_error=True` with the backend's message, `'12345' is not an order ID. Order IDs look like HL-10234.` (the printed preview stops at 45 characters). Both results went back in one turn, and Claude replied that Elijah's account is verified but order 12345 isn't in the system, and asked for the ID from his confirmation email, starting with "HL-". One call worked, one failed, both were answered, and nothing crashed: the failure became information Claude could use.

Finally, save your work to your own repository:

```bash
git status --short          # ?? experiments/m1/manual_tool_call.py   ?? loop/
git add loop experiments/m1/manual_tool_call.py
git commit -m "Lesson 1.3: tool definitions and a tool round trip by hand"
git push
```

The commit adds the two files (`2 files changed, 120 insertions(+)`), and `git push` sends it to `origin`, your own private `harborline`. Your commit id will differ from the lesson's. `runs/` doesn't show up in `git status`: it's ignored, and its usage log now holds this lesson's calls too.

## Windows, macOS and Linux

`git`, `code`, `mkdir loop` and the `python -m experiments...` commands are the same on every system (run them with the environment active). Only one line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m experiments.m1.manual_tool_call` | the same line | `cls`, then `python -m experiments.m1.manual_tool_call` on its own line |

- **Windows:** `code loop/tools.py` works with forward slashes in PowerShell. If your venv's `python` isn't found, activate the environment first (`.venv\Scripts\Activate.ps1`, Lesson 0.6).
- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**).
- **WSL:** run the Linux commands inside the WSL terminal, in your WSL home folder.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| First response | `--- tool_use, 604 tokens in`; `[thinking]`; `[tool_use] get_customer {'email': 'elijah.petrov@example.com'}` and `[tool_use] lookup_order {'order_id': 'HL-10196'}` in one response |
| Results | Two `[tool_result]` lines, `is_error=False`, each with its call's id |
| Second response | `--- end_turn, 1,168 tokens in`; the answer: HL-10196 has shipped with Parcelway, estimated to arrive by October 16, 2026 |
| `bad` run | `--- tool_use, 592 tokens in`; `lookup_order {'order_id': '12345'}`; its result `is_error=True '12345' is not an order ID…`; `--- end_turn, 900 tokens in`; Claude asks for the ID from the confirmation email |
| `git commit` | `2 files changed, 120 insertions(+)` |
| `git push` | `main -> main` to your own `harborline` |
| API spend | A fraction of a cent on Claude Haiku 5.5 |

Your ids, token counts and replies will differ from these, run to run. See `expected-output.md` for what should match.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'loop'`** or **`'harborline'`**: you ran the file directly (`python experiments/m1/manual_tool_call.py`), or you're not in the `harborline` folder. `cd ~/projects/harborline` and run it as a module: `python -m experiments.m1.manual_tool_call`. Check that the file is at `loop/tools.py`.
- **`ModuleNotFoundError: No module named 'harborline.usage'`** or **`ImportError: cannot import name 'log_usage'`**: Lesson 1.2's `harborline/usage.py` is missing. Do Lesson 1.2 first: it writes that file.
- **`ModuleNotFoundError: No module named 'anthropic'`** or **`python: command not found`**: the environment isn't active in this terminal. Activate it (Lesson 0.6); the prompt should start with `(.venv)`.
- **An error about the API key, or `401` `authentication_error`**: `.env` is missing, empty or not saved, or the key is incomplete or disabled. Run `python -m scripts.check_setup`: it says which. Create a new key in the Console if you need one (Lesson 0.4).
- **`No tool call this time.`**: Claude answered without calling a tool, so there was nothing to run. Check that `TOOLS` holds both definitions and that `ask()` passes `tools=TOOLS`; then run it again.
- **Only one `[tool_use]` line in the first response**: Claude asked for the tools one at a time this run. Your code still answers the call it got; the script stops after the second response, so a second call there isn't run (the loop that keeps answering is Lesson 1.4). Run it again to see both calls in one response.
- **`400` `invalid_request_error` on the second request**, mentioning `tool_use` ids without `tool_result` blocks: a call was left unanswered, a tool's output was sent as plain text instead of a `tool_result` block, or the results aren't right after Claude's turn. Every `tool_use` block needs one `tool_result` (the dicts `run_tool` returns, not strings), all of them first in the one user turn that follows.
- **`400` about thinking blocks**: Claude's turn was changed before it went back. Append `response.content` exactly as it came back, thinking block included.
- **A `TypeError` like `get_customer() got an unexpected keyword argument`**: a schema field name doesn't match the backend's parameter. The fields are `email` and `order_id`, spelled exactly like that.
- **`Order HL-10196 does not exist.`** on the normal run: check the order number Claude passed in the `[tool_use]` line; Claude passes it as the customer wrote it.
- **The `bad` run's second response is another `--- tool_use`**: Claude is retrying with a corrected order number, after reading your error message. That's fine; answering it is the loop of Lesson 1.4.
- **`[tool_result]` lines wrap in your terminal**: harmless. The script prints only the first 45 characters of each result.
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them. `git add loop experiments/m1/manual_tool_call.py` adds only the two new files.
- **Never paste your API key into code or into a chat.** If a key leaks, disable it in the Console first, then create a new one (Lesson 0.4).

## Key terms

- **Tool:** a function in your code that Claude can ask you to run. Claude knows it only through its definition: a name, a description and an input schema.
- **`input_schema`:** the JSON Schema in a tool definition: the input object's fields, their types, and which are required.
- **`tool_use` block:** Claude's request to run a tool: an `id`, the tool `name` and an `input` that follows the schema. The response stops with `stop_reason` `"tool_use"`.
- **`tool_result` block:** your answer to one call, sent in the next user turn and tied to its call by `tool_use_id`. Tool results come first in that turn.
- **Parallel tool calls:** several `tool_use` blocks in one response. Run them in any order, and send every result back together, in one user turn.
- **`is_error`:** the flag on a `tool_result` that says the call failed. The content says what went wrong, so Claude can recover.

## Sources (checked 2026-10-14)

- How tool use works, the tool-use contract ("The model never executes anything on its own"; "Claude never sees your implementation"): https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works#the-tool-use-contract
- Define tools, specifying client tools (`name`, `description`, `input_schema`; the tool use system prompt; provide extremely detailed descriptions): https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#specifying-client-tools
- Tool use overview, pricing (tools are billed as input; the tool use system prompt is 286 tokens on Claude Haiku 5.5 with tool choice auto or none): https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview#pricing
- Handle tool calls, handling results from client tools (`tool_use_id`, `content`, `is_error`; the formatting rules): https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls#handling-results-from-client-tools
- Handle tool calls, handling errors with `is_error` (write instructive error messages): https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls#handling-errors-with-is-error
- Parallel tool use (all results together in the next user message; one user message per result teaches Claude to avoid parallel calls): https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use
- Troubleshooting tool use (the `400` errors for missing or misplaced tool results): https://platform.claude.com/docs/en/agents-and-tools/tool-use/troubleshooting-tool-use
- Thinking with tool use (thinking blocks go back with the tool results): https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows
- Claude Haiku 5.5 migration guide (pass thinking blocks back unmodified with tool results): https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide
- API reference, create a message (`tools`, `tool_use`, `tool_result`, `is_error`): https://platform.claude.com/docs/en/api/messages/create
- Tool Runner (the SDK can automate the round trip you built by hand): https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.1 (Domain 1: Agentic Architecture & Orchestration), Task Statement 2.1 (Domain 2: Tool Design & MCP Integration), and Scenario 1: Customer Support Resolution Agent

Models and APIs change. If a number or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 1.4 this round trip becomes a loop: your code keeps answering until Claude ends its turn.
