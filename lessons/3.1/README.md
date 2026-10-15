# Student kit: Lesson 3.1, The Claude Agent SDK from zero

Claude Certified Architect – Foundations (CCAR-F) · Module 3: Agents with the Claude Agent SDK: the Support Resolution Agent · Lesson 3.1

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Explain the SDK: Claude Code's agent loop as a library
2. Configure query() with ClaudeAgentOptions
3. Turn Python functions into tools, in-process

## What's in the kit

| File | What it is |
|---|---|
| `requirements.txt` | The four pinned packages from before plus one line: `claude-agent-sdk==0.2.165`, the Claude Agent SDK for Python |
| `support/tools.py` | New: Harborline's backend as two Agent SDK tools, `get_customer` and `lookup_order`, with the descriptions and input schemas from `loop/tools.py`, failures returned with `is_error` and Lesson 2.4's structured body, and `server = create_sdk_mcp_server("harborline", ...)`: an MCP server that runs inside your app |
| `support/hello_agent.py` | New: `ClaudeAgentOptions` for a locked-down support agent and a `main()` that runs `query()` on one ticket and prints what comes back |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `requirements.txt` and `support` folder into your `harborline` folder.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 2.7, Lab 1 and Lab 2 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, `origin` pointing at your own private `harborline` on GitHub, Lab 1's `loop/agent.py` and `loop/tools.py`, and Lesson 2.4's `harborline/tool_errors.py`.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). The agent reads it with `load_dotenv()`. Never paste the key into a file you commit, and never print it.
- About 30 minutes, most of it typing. **API spend in the lesson: $0.0006** for one run (Haiku 5.5).

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder.

### 1. Install the SDK

```bash
git status --short                 # prints nothing: a clean tree after Lab 2
code loop/agent.py                 # a look back at Lab 1's loop (read only)
code requirements.txt              # line 6: claude-agent-sdk==0.2.165, save
clear; pip install -r requirements.txt
```

In the lesson, **Ctrl+J** hides the terminal panel while a file is open, so the editor gets the full height.

**`loop/agent.py`** is the loop you wrote in Lab 1: `run()` calls Claude, checks `stop_reason`, has a branch for `max_tokens`, one for `refusal` and one for `pause_turn`, appends the reply, runs each tool, appends the results, and goes around again. 147 lines in all. VS Code opens a file where you last left it, so yours may open at the top.

**`requirements.txt`**: one new line, `claude-agent-sdk==0.2.165`. `pip install -r requirements.txt` says the other packages are already satisfied, then installs `claude-agent-sdk-0.2.165`. The download is large (107.8 MB in the lesson, for Linux) because the package carries the Claude Code binary that the SDK runs. In the lesson it came from pip's cache on that machine ("Using cached …"); yours downloads it, and pip picks the build for your system.

### 2. Your functions as tools

```bash
code support/tools.py              # type the file (or copy it from the kit), save
```

The `support` folder doesn't exist yet; VS Code creates it when you save. What the file holds:

- **The docstring**: the same backend calls and descriptions as Lesson 2.5's harborline-mcp, but no separate process: the MCP server runs inside your app.
- **The imports**: `json`; from the SDK, `create_sdk_mcp_server` and `tool`; Harborline's `backend`, `BackendError`, Lesson 2.4's `tool_error`, and the `GET_CUSTOMER` and `LOOKUP_ORDER` definitions from `loop/tools.py`.
- **`reply()`** runs one backend call and returns `{"content": [{"type": "text", "text": ...}]}` with the output as JSON. A `BackendError` comes back as the structured error with `"is_error": True`, so Claude knows the call failed.
- **Two tools.** `@tool(name, description, input_schema)` on an async function. The description and the schema are Lab 1's, word for word. `get_customer` passes the email or the name to the backend; `lookup_order` passes the order ID.
- **`server = create_sdk_mcp_server("harborline", version="1.0.0", tools=[...])`**: both tools on one in-process server. Nothing runs yet: it's a Python object you hand to the agent.

### 3. Options and a first run

```bash
code support/hello_agent.py        # type the file (or copy it from the kit), save
clear; python -m support.hello_agent T-008
```

**`OPTIONS = ClaudeAgentOptions(...)`**, option by option:

| Option | In the lesson | Why |
|---|---|---|
| `system_prompt` | A short prompt of our own: verify the sender with `get_customer` first, then look up the order; no refunds yet; four sentences or fewer | Without one, the SDK uses a minimal prompt that only covers tool calling |
| `model` | `MODEL` from `harborline/config.py` (Haiku 5.5) | The same model as every lesson |
| `mcp_servers` | `{"harborline": server}` | The key names the tools: `mcp__harborline__get_customer` |
| `tools` | `[]` | Availability: no built-in tools at all (no Bash, no file access) |
| `allowed_tools` | the two full tool names | Permission: these run without asking |
| `permission_mode` | `"dontAsk"` | Anything not pre-approved is denied, never asked |
| `setting_sources` | `[]` | None of your computer's Claude Code settings or instruction files reach the app |
| `max_turns`, `max_budget_usd` | `6`, `0.05` | Safety nets, not how the agent stops |

**`main()`**: `first_message(ticket_id)` (from Lab 1) turns the ticket into a prompt; `async for message in query(prompt=prompt, options=OPTIONS)` is the whole loop. It prints the init message's tools, each tool call with its input (`ToolUseBlock`), Claude's text (`TextBlock`), and the `ResultMessage`: its subtype, the number of turns and the cost. At the bottom, `load_dotenv()` reads your API key from `.env` and `asyncio.run(main(...))` runs it.

**In the lesson** (ticket T-008, a customer asking where order HL-10196 is):

1. A notice from Claude Code: `claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set and takes precedence over your claude.ai login`. The SDK runs the Claude Code binary, the lesson's computer was signed in to Claude Code (Lesson 0.5), and the API key from `.env` takes precedence: that's what an SDK app should use. If you're not signed in to Claude Code, you won't see it.
2. `tools: ['mcp__harborline__get_customer', 'mcp__harborline__lookup_order']`: only your two tools.
3. `[tool] mcp__harborline__get_customer {'email': 'elijah.petrov@example.com'}`, then `[tool] mcp__harborline__lookup_order {'order_id': 'HL-10196'}`: the sender verified first, as the system prompt asked.
4. `[text] Hi Elijah, order HL-10196 (Stoneware Vase) has shipped with Parcelway, tracking number PW4974187387. …`
5. `success: 3 turns, $0.0006`.

### 4. Commit

```bash
clear; git status --short
git add requirements.txt support
git commit -m "Lesson 3.1: a first agent on the Claude Agent SDK, with in-process tools"
git push
```

`git status --short` shows ` M requirements.txt` and `?? support/`. The commit has three files (`3 files changed, 99 insertions(+)`), and `git push` sends it to `origin`, your own private `harborline`. Your commit ID will differ from the lesson's.

## Windows, macOS and Linux

`git`, `code`, `pip` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m support.hello_agent T-008` | the same line | `cls`, then `python -m support.hello_agent T-008` on its own line |

The same goes for `clear; pip install -r requirements.txt` and `clear; git status --short`.

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `pip install -r requirements.txt` | `Successfully installed claude-agent-sdk-0.2.165` (a 107.8 MB wheel, from pip's cache on that machine) |
| `python -m support.hello_agent T-008`: tools | `['mcp__harborline__get_customer', 'mcp__harborline__lookup_order']` |
| Tool calls | `get_customer` with the sender's email, then `lookup_order` with `HL-10196` |
| Result | `success: 3 turns, $0.0006` |
| `git commit` | `3 files changed, 99 insertions(+)` |
| `git push` | `main -> main` to your own `harborline` |
| API spend | $0.0006 |

See `expected-output.md` for the exact lines and what should match.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'claude_agent_sdk'`**: the install went into another Python. Activate the environment, then run `pip install -r requirements.txt` again.
- **`ModuleNotFoundError: No module named 'support'`**, **`'loop'`** or **`'harborline'`**: you're not in the `harborline` folder, or you ran the file directly. `cd ~/projects/harborline` and use `python -m support.hello_agent T-008`.
- **`ImportError: cannot import name 'tool_error'`**: Lesson 2.4's `harborline/tool_errors.py` is missing. Do Lesson 2.4 first.
- **An authentication error, or the run asks you to log in**: `ANTHROPIC_API_KEY` isn't in your `.env`, or `.env` isn't in the `harborline` folder. Check with `python scripts/check_setup.py` (Lesson 0.6); it says whether the key is set without printing it.
- **`tools:` lists Bash, Read and many more**: `tools=[]` is missing from your options. Compare with the kit's file.
- **A tool call is denied**: its full name in `allowed_tools` doesn't match. The name is `mcp__` + the key in `mcp_servers` + `__` + the tool's name.
- **`error_max_turns` or `error_max_budget_usd`**: a safety net stopped the run. With this ticket it shouldn't happen; check the system prompt and the tools.
- **`No ticket T-008`**: type the ID exactly, with the capital T and the dash.
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Claude Agent SDK:** a Python and TypeScript library that runs Claude Code's agent loop, tools and permissions inside your own app.
- **query():** the SDK's entry point: send a prompt with options, get an async stream of messages back, ending with a result.
- **ClaudeAgentOptions:** the agent's configuration: system prompt, model, tools, permissions, MCP servers, limits.
- **In-process MCP server:** an MCP server that runs inside your app (`create_sdk_mcp_server`), not as a separate process.
- **dontAsk:** the permission mode that denies anything not pre-approved instead of asking someone.

## Sources (checked 2026-10-15)

- Claude Code docs, *Agent SDK overview*: the same tools, agent loop and context management that power Claude Code, as a library; with the Client SDK you write the tool loop yourself; products built on the SDK use API key authentication: https://code.claude.com/docs/en/agent-sdk/overview
- Claude Code docs, *Give Claude custom tools*: `@tool` and `create_sdk_mcp_server`; the server runs in-process inside your application; the key in `mcp_servers` names the tools (`mcp__{server_name}__{tool_name}`); `tools: []` removes all built-ins, allowed tools set permission: https://code.claude.com/docs/en/agent-sdk/custom-tools
- Claude Code docs, *Configure permissions*: for a locked-down agent, pair allowed tools with `dontAsk`; `dontAsk` turns any permission prompt into a denial; allowed tools don't constrain `bypassPermissions`: https://code.claude.com/docs/en/agent-sdk/permissions
- Claude Code docs, *Modifying system prompts*: without a system prompt the SDK uses a minimal prompt that covers tool calling: https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts
- Claude Code docs, *Use Claude Code features*: without `setting_sources`, `query()` reads the same filesystem settings as the Claude Code CLI; an empty list limits the agent to what you configure: https://code.claude.com/docs/en/agent-sdk/claude-code-features
- Claude Code docs, *How the agent loop works*: turns, messages, and the result message with cost and session ID: https://code.claude.com/docs/en/agent-sdk/agent-loop
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statements 1.1 (Domain 1) and 2.4 (Domain 2), Scenario 1: Customer Support Resolution Agent

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 3.2, this agent gets its full set of support tools, and a number to beat.
