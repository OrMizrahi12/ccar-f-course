# Student kit: Lesson 2.5, MCP from zero: build a server

Claude Certified Architect – Foundations (CCAR-F) · Module 2: Tool Design & MCP Integration · Lesson 2.5

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Explain hosts, clients, servers, and the three building blocks
2. Build an MCP server with tools, resources and a prompt
3. Test it in memory and in the MCP Inspector

## What's in the kit

| File | What it is |
|---|---|
| `requirements.txt` | Lesson 0.6's three pinned packages plus one line: `mcp==2.3.0`, the official MCP Python SDK |
| `mcp_server/server.py` | New: `harborline-mcp`. Four tools (`get_customer`, `lookup_order`, `list_orders`, `process_refund`) whose descriptions come straight from `loop/tools.py`, failures returned as tool results with `is_error` and Lesson 2.4's structured body, two resources (the refund policy and the product catalog), one prompt (`order_help`), and `app.run()` over stdio |
| `tests/test_mcp_server.py` | New: three tests with the SDK's own `Client`, connected to the app in memory: no subprocess, no stdout |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `requirements.txt`, `mcp_server` folder and `tests/test_mcp_server.py` into your `harborline` folder.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 2.4 and Lab 1 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, `pytest` passing (54 tests), `origin` pointing at your own private `harborline` on GitHub, Lesson 2.1 and 2.2's `loop/tools.py` (the tuned descriptions) and Lesson 2.4's `harborline/tool_errors.py`.
- **Node.js 22.19 or newer** for the MCP Inspector (Lesson 0.5 installed Node.js with nvm). `node --version` prints it. You don't install the Inspector: `npx` fetches it the first time you run it.
- **Chrome or another browser**: the Inspector opens its page there.
- About 35 minutes, most of it typing. **No API key is used and no model is called in this lesson: it costs nothing.**

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder.

### 1. Install and write

```bash
git status --short                 # prints nothing: a clean tree after Lesson 2.4
code requirements.txt              # line 5: mcp==2.3.0, save
clear; pip install -r requirements.txt
code mcp_server/server.py          # type the file (or copy it from the kit), save
```

In the lesson, **Ctrl+J** hides the terminal panel while a file is typed, so the editor gets the full height.

**`requirements.txt`**: four lines, every version pinned. Line 5, `mcp==2.3.0`, is the official MCP Python SDK. `pip install -r requirements.txt` says anthropic, python-dotenv and pytest are already satisfied, then installs `mcp-2.3.0`, `mcp-types-2.3.0` and what they need: 17 packages in all.

**`mcp_server/server.py`**: the `mcp_server` folder doesn't exist yet; VS Code creates it when you save. What it holds:

- **The docstring** names the three building blocks. Tools are actions Claude can call. Resources are documents and catalogs the app reads and gives to Claude, with no tool call. Prompts are templates a user picks.
- **The imports**: `json`, `Literal`, `MCPServer`, and two types for a tool result (`CallToolResult`, `TextContent`); Harborline's backend and data, `BackendError`, Lesson 2.4's `tool_error`, and four tool definitions from `loop/tools.py`.
- **`app = MCPServer("harborline")`**: the server, named harborline. **`Reason`**: the policy's seven refund reasons as a `Literal`, so the schema lists them.
- **`call()`** runs one backend call, like `run_tool` in the loop. A `BackendError` comes back as a `CallToolResult` with `is_error=True` and the structured body. Success is the output as JSON text, so an empty list stays one text block and a success.
- **Four tools.** Each `@app.tool` takes its description straight from `loop/tools.py`, the wording tuned in Lessons 2.1 and 2.2: one source of truth. `get_customer` (by email or name), `lookup_order`, `list_orders`, and `process_refund` (an order, a reason, an amount, an optional SKU). The type hints become the input schema. Each tool hands its arguments to `call()`.
- **Two resources.** The refund policy at `harborline://policy/refunds` as Markdown, and the product catalog at `harborline://catalog/products` as JSON (every product, its price, and whether it's final sale). An app can read both up front.
- **One prompt**, `order_help`: give it an order ID and it returns the opening message for a conversation about that order.
- **`app.run()`**: stdio. The host starts this process and talks to it over stdin and stdout, which is why nothing in this file prints.

### 2. Test it in memory

```bash
code tests/test_mcp_server.py      # type the file (or copy it from the kit), save
clear; pytest -q
```

The trick is the SDK's own client: `Client(app)` takes the app object and connects in memory. It's a real MCP client, with no subprocess and no stdout. The tests run as async functions on asyncio (`pytestmark = pytest.mark.anyio` and the `anyio_backend` fixture).

- **Test one**: it lists everything. Four tool names, the two resource addresses, and the one prompt, `order_help`. Forget a decorator, and this test catches it.
- **Test two**: a failure is an error result with a category. `backend.reset()` arms one timeout on HL-10211; the lookup comes back with `is_error`, `errorCategory` transient and `isRetryable` true.
- **Test three**: no orders is a valid empty result. `list_orders` for C-1058, a customer with no orders: not an error, and the text is `[]`.

**In the lesson:** `57 passed in 1.05s`: the 54 tests from before, plus the three new ones.

### 3. The MCP Inspector

```bash
clear; npx @modelcontextprotocol/inspector@2.10.1 python -m mcp_server.server
```

The first time, `npx` asks to install the package (`Ok to proceed? (y)`): answer `y`. The Inspector is a host built for testing: it starts your server as a process and talks to it over stdio, the same way Claude Code will. No model is involved. When it's ready it prints its address and opens it in your browser. **That address carries a session token: treat it like a password and don't share it.** (In the lesson it also warned that no OS keychain was available on that machine, so it kept its secrets in a file: fine for a local test.)

In the browser, in the order of the lesson:

1. **Connect.** The server is set to `python` over stdio. The header shows `harborline`, the name you gave it, and `MCP 2025-11-25`: the protocol version the two sides agreed on. (The docs show a newer one, from July 2026.)
2. **Tools**: all four. Click `lookup_order`: its description from Lesson 2.1, word for word, and one required field, **Order Id**, built from the type hint. Type `HL-10211` and **Execute**.
3. **Tool Error**: `{"errorCategory": "transient", "isRetryable": true, "message": "The warehouse system timed out. Try again in a moment."}`. Close it and **Execute** again: this time the order (a cast iron skillet, `"status": "processing"`). A retry the error invited. The protocol log on the right lists each `tools/call`.
4. **`list_orders`**, Customer ID `C-1058`, **Execute**: `[]` and no error card. The lookup worked and found nothing.
5. **Resources**: two (`refund_policy`, `product_catalog`). Open `refund_policy`: the Inspector reads `harborline://policy/refunds` (`text/markdown`) and renders it. No tool call.
6. **Prompts**: `order_help` takes one argument, the order ID. `HL-10163`, **Get prompt**: one message, role user: "A customer is asking about order HL-10163. Look it up with lookup_order, then answer from what it returns." A user picks this; the model doesn't.

Then back in VS Code, **Ctrl+C** in the terminal stops the Inspector.

### 4. Commit

```bash
clear; git status --short
git add requirements.txt mcp_server tests/test_mcp_server.py
git commit -m "Lesson 2.5: harborline-mcp server, in-memory tests"
git push
```

`git status --short` shows ` M requirements.txt`, `?? mcp_server/` and `?? tests/test_mcp_server.py`. The commit has the three files (`3 files changed, 129 insertions(+)`), and `git push` sends it to `origin`, your own private `harborline`. Your commit ID will differ from the lesson's.

## Windows, macOS and Linux

`git`, `code`, `pip`, `pytest`, `npx` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; npx @modelcontextprotocol/inspector@2.10.1 python -m mcp_server.server` | the same line | `cls`, then `npx @modelcontextprotocol/inspector@2.10.1 python -m mcp_server.server` on its own line |

The same goes for `clear; pip install -r requirements.txt`, `clear; pytest -q` and `clear; git status --short`.

- **Windows:** start the Inspector from a terminal where the environment is active, so `python` is your venv's Python (the Inspector starts the server with whatever `python` that terminal finds). If `npx` isn't found, Node.js isn't on your PATH: open a new terminal after installing it.
- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel); **Ctrl+C** still stops the Inspector in the terminal.
- **WSL:** run the Linux commands inside the WSL terminal; open the Inspector's address in your Windows browser if it doesn't open by itself.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `pip install -r requirements.txt` | anthropic, python-dotenv, pytest already satisfied; 17 packages installed, `mcp-2.3.0` and `mcp-types-2.3.0` among them |
| `pytest -q` | `57 passed in 1.05s` |
| Inspector: Connect | `harborline`, `MCP 2025-11-25` |
| `lookup_order` HL-10211 | Tool Error: transient, `isRetryable` true; again: the order, `"status": "processing"` |
| `list_orders` C-1058 | `[]`, no error card |
| Resources / Prompts | `refund_policy` rendered (`harborline://policy/refunds`, `text/markdown`); `order_help` HL-10163: one user message |
| `git commit` | `3 files changed, 129 insertions(+)` |
| `git push` | `main -> main` to your own `harborline` |
| API spend | $0: no model calls |

See `expected-output.md` for the exact lines and what should match.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'mcp'`**: the install went into another Python. Activate the environment, then run `pip install -r requirements.txt` again.
- **`ModuleNotFoundError: No module named 'mcp_server'`**, **`'loop'`** or **`'harborline'`**: you're not in the `harborline` folder, or you ran the file directly. `cd ~/projects/harborline` and use `python -m mcp_server.server` (or `pytest` from the folder).
- **`ImportError: cannot import name 'tool_error'`**: Lesson 2.4's `harborline/tool_errors.py` is missing. Do Lesson 2.4 first.
- **pytest: `async def functions are not natively supported`**: the `pytestmark = pytest.mark.anyio` line or the `anyio_backend` fixture is missing. Compare with the kit's test file.
- **Test one fails on the names**: a decorator is missing or a function is misnamed. The tool names are the function names.
- **`npx: command not found`** or a Node.js version error: install Node.js 22.19 or newer (Lesson 0.5), then open a new terminal.
- **The Inspector connects, then shows an error, or the server exits at once**: start it from the `harborline` folder with the environment active, so `python -m mcp_server.server` can import Harborline. Run `python -m mcp_server.server` alone: it should wait silently (Ctrl+C to stop). Any output or traceback there is your bug.
- **Your server prints something**: never `print()` in a stdio server. stdout belongs to the protocol; log to stderr instead.
- **The browser doesn't open**: copy the address the Inspector printed, token included, into your browser. Don't paste it anywhere else.
- **The Tool Error doesn't appear for HL-10211**: the timeout fires once per server process. Stop the Inspector (Ctrl+C) and start it again to re-arm it.
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **MCP host / client / server:** the host is the AI application (Claude Code, Claude Desktop, an IDE); it creates one MCP client per server, each with its own connection; the server exposes capabilities.
- **MCP resource:** read-only data or a catalog a server exposes by URI (`harborline://policy/refunds`); the application reads it and gives it to Claude, so Claude doesn't need exploratory tool calls.
- **MCP prompt:** a reusable template a server offers, which a user picks (here `order_help`).
- **stdio transport:** the host starts the server as a process and talks JSON-RPC over stdin and stdout; stdout belongs to the protocol.
- **MCP Inspector:** the reference tool for testing a server: it lists tools, resources and prompts, calls them, and shows the raw results.

## Sources (checked 2026-10-14)

- Model Context Protocol, *Architecture overview*: the host creates one MCP client for each MCP server; local stdio servers typically serve a single client; servers provide tools for AI actions, resources for context data, and prompts for interaction templates: https://modelcontextprotocol.io/docs/learn/architecture
- Model Context Protocol, *Understanding MCP servers*: three building blocks and who controls each (tools: the model; resources: the application; prompts: the user): https://modelcontextprotocol.io/docs/learn/server-concepts
- Model Context Protocol, *Build an MCP server* (Python): never write to stdout in a stdio server; the server class builds tool definitions from type hints and docstrings: https://modelcontextprotocol.io/docs/develop/build-server
- Model Context Protocol, *MCP Inspector*: a full graphical inspector in the browser; no installation required, it runs through `npx`: https://modelcontextprotocol.io/docs/tools/inspector
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 2.4 (Domain 2: Tool Design & MCP Integration), Scenario 1: Customer Support Resolution Agent and Scenario 4: Developer Productivity with Claude

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 2.6: MCP in Claude Code and agents, plugging this server into Claude Code.
