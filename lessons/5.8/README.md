# Student kit: Lesson 5.8, A developer productivity agent

Claude Certified Architect – Foundations (CCAR-F) · Module 5: Configuring Claude Code for a Team · Lesson 5.8

This kit holds everything you need to repeat the lesson on your own computer: every command and prompt in order, the files the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Give an SDK agent built-in tools plus your MCP server
2. Write tool descriptions the agent prefers over Grep
3. Map legacy code and generate tested boilerplate

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command and prompt in the lesson, in order (copy the two questions from here) |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/devtools/codemap_server.py` | The MCP server you write in step 1: `list_public_names` and `trace_export`, with the descriptions the agent trusts |
| `harborline/tests/test_codemap.py` | Its two tests (step 2): the tools are plain functions, so the tests call them directly |
| `harborline/devtools/explorer.py` | The Agent SDK agent you write in step 3: built-in tools, codemap over standard input and output, `allowed_tools` and `dontAsk` |
| `harborline/devtools/warehouse_adapter.py` | What the agent wrote in step 4, as committed: `to_order(raw)` |
| `harborline/tests/test_warehouse_adapter.py` | The agent's two tests for it, as committed |
| `harborline/devtools/__init__.py` | Empty: it makes `devtools` a package |

You type the first three files yourself, as in the lesson (or paste them from the kit). The last two are the agent's work: yours will differ in the details, which is fine. Use the kit's copies to compare, or to recover.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The code and the steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 5.7 done**: your own `harborline` repository in `~/projects/harborline` at the Lesson 5.7 commit, its `.venv` with the packages from `requirements.txt` (`claude-agent-sdk`, `mcp`, `python-dotenv` and `pytest` came with earlier lessons), `pytest` passing, and `origin` pointing at your own private `harborline` repository. The `legacy/warehouse` package is already in the repository.
- **Your Anthropic API key in `.env`** (Lesson 0.4): `ANTHROPIC_API_KEY=...`. `.env` is in `.gitignore`, so it is never committed.
- About 25 minutes. **This lesson makes API calls**: an Agent SDK agent runs on the API key, not on your Claude subscription. In the lesson, the first question cost about a tenth of a cent ($0.0013) and the second about half a cent ($0.0058). The agent's limits cap each run at 20 turns and $0.10.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### 1. The MCP server

```bash
git status --short
mkdir -p devtools && touch devtools/__init__.py
code devtools/codemap_server.py
```

Type `devtools/codemap_server.py` (it's in the kit). Its idea is in the docstring: Grep finds text; these tools read the code's structure with `ast`, Python's own parser.

- `source(module)` turns a dotted name like `legacy.warehouse` into its file and parses it. `names(tree)` lists every top-level function, class, assignment and import, under the name it's bound to: `from .records import read_record as load_record` is listed as `load_record`.
- `list_public_names` returns a package's public names, the line of each and, for re-exports, the module it comes from.
- `trace_export` follows re-exports and renames, one import at a time and at most 10 steps, to the real definition: the file, the line and the original name.

Read the two **descriptions**: each says what the tool returns, and when to use it instead of Grep. That's what makes the agent choose them.

### 2. Its test

```bash
code tests/test_codemap.py
```

Type the two tests from the kit, save, then run just this file:

```bash
.venv/bin/python -m pytest -q tests/test_codemap.py
```

You should see `2 passed`. The server works before any agent touches it.

### 3. The agent

```bash
code devtools/explorer.py
```

Type `devtools/explorer.py` from the kit. What to look at in `OPTIONS`:

- `mcp_servers` registers codemap as a standard input and output server: the same Python, running `devtools.codemap_server`.
- `tools` lists the built-in tools the agent can see: Read, Grep, Glob, Write, Edit and Bash.
- `allowed_tools` is what runs without asking: the file tools, Bash **only** for `.venv/bin/python -m pytest *`, and the two codemap tools by their full names, `mcp__codemap__list_public_names` and `mcp__codemap__trace_export`.
- `permission_mode="dontAsk"` refuses everything else, with no prompt. `setting_sources=[]` means no settings or memory files from the repository change how the agent behaves.
- `max_turns=20` and `max_budget_usd=0.10` cap each run.

`main()` prints every tool call with its input, the text as it arrives, and at the end the turns and the cost.

### 4. Map and generate

Ask the first question (from `commands.txt`):

```bash
python -m devtools.explorer "Where does legacy.warehouse.load_record come from, and what does it return?"
```

In the lesson the agent's first call was `trace_export`, then it read `records.py`, and it answered in 3 turns, without a single Grep: `load_record` is a re-export of `read_record`, defined in `legacy/warehouse/records.py`, line 15.

Then the boilerplate:

```bash
python -m devtools.explorer "Write devtools/warehouse_adapter.py: a function to_order(raw) that turns a legacy warehouse record into the order shape harborline.normalize.order() returns, using the names the legacy.warehouse package exports. Add tests/test_warehouse_adapter.py with two cases and run it."
```

In the lesson the agent called `list_public_names` twice, then one chained Bash call (`git status --short && ls -la && ...`). `dontAsk` refused it as a whole: it isn't the allowed pytest command. The agent then decided that Bash was denied in this session, so it never ran its tests, even though its prompt names the allowed command. It read the legacy package, used `load_record`, wrote both files, and said plainly that it had checked the values by hand and that you should run the command yourself. Your agent may run the allowed pytest command instead: both are fine, as long as you check.

### 5. Verify, then commit

```bash
.venv/bin/python -m pytest -q
git status --short
git add devtools tests/test_codemap.py tests/test_warehouse_adapter.py
git commit -m "Lesson 5.8: codemap MCP server and an Agent SDK explorer that uses it"
git push
```

The whole suite must pass: in the lesson, 129 passed (your count may differ by a few, depending on your earlier lessons). The commit has 6 files and 202 insertions.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Run the tests | `.venv/bin/python -m pytest -q` | `.venv\Scripts\python -m pytest -q` |
| The pytest rule in `explorer.py` | `Bash(.venv/bin/python -m pytest *)`, and the same path in the system prompt | change both to `.venv/Scripts/python -m pytest` (Claude Code runs Bash commands through Git Bash on Windows) |
| Make the folder | `mkdir -p devtools && touch devtools/__init__.py` | PowerShell: `mkdir devtools; New-Item devtools\__init__.py` |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save).

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` at the start | nothing: the tree is clean |
| `tests/test_codemap.py` | 2 passed in 0.69s |
| Question 1 | `tool: trace_export`, then `tool: Read` of `records.py`; a re-export of `read_record`, line 15; 3 turns, $0.0013; no Grep |
| Question 2 | `list_public_names` twice; one chained Bash call refused by `dontAsk`; both files written; tests checked by hand, not run; 16 turns, $0.0058; nothing committed |
| The whole suite | 129 passed in 3.90s |
| The commit | `1c77648`, 6 files changed, 202 insertions |

See `expected-output.md` for the exact lines.

## Troubleshooting

- **`ModuleNotFoundError: claude_agent_sdk` or `mcp`**: the packages come from `requirements.txt` (earlier lessons). Run `.venv/bin/python -m pip install -r requirements.txt` and try again.
- **An authentication error from the agent**: `.env` has no key, or the shell exported a different one. Check `ANTHROPIC_API_KEY` in `.env` (Lesson 0.4). The agent runs on the API, so a Claude subscription alone isn't enough.
- **A notice that claude.ai connectors are disabled**: expected. The API key takes precedence over your claude.ai sign-in for this run; it changes nothing for the lesson.
- **The agent uses Grep instead of codemap**: read your two descriptions again. Each must say what the tool returns and when to use it instead of Grep. A one-line description ("Trace an export.") is not enough.
- **`trace_export` raises "has no top-level name"**: the name isn't defined or imported at the top of that module. Check the spelling, and that `legacy/warehouse/__init__.py` re-exports it.
- **The agent runs pytest, or doesn't**: both happen. Either way, run the whole suite yourself before you commit.
- **The run stops at the turn or budget limit**: that's `max_turns` and `max_budget_usd` doing their job. Ask a narrower question, or raise the limit a little.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Built-in tools:** Claude Code's Read, Grep, Glob, Write, Edit and Bash, which an Agent SDK agent gets by name.
- **`allowed_tools`:** what runs without asking; with `dontAsk`, anything else is refused.
- **Re-export:** a package importing a name from one of its modules (maybe renamed) so that others import it from the package.
- **AST:** Python's parser: code as structure, not text.
- **Tool description:** what the model reads to choose a tool: what it returns, and when to use it instead of another.

Claude Code and the Agent SDK change often. If an option or a message doesn't match what you see, follow the official pages: Agent SDK overview (https://code.claude.com/docs/en/agent-sdk/overview), Connect to external tools with MCP (https://code.claude.com/docs/en/agent-sdk/mcp) and Configure permissions (https://code.claude.com/docs/en/agent-sdk/permissions).
