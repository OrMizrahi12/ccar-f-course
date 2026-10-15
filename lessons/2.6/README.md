# Student kit: Lesson 2.6, MCP in Claude Code: scopes, secrets, and many servers at once

Claude Certified Architect – Foundations (CCAR-F) · Module 2: Tool Design & MCP Integration · Lesson 2.6

This kit holds everything you need to repeat the lesson on your own computer: the files changed in the lesson, every command in order, what each step printed in the lesson, what differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Choose local, project or user scope for an MCP server
2. Keep tokens out of git with ${VAR} expansion
3. Run several servers at once, and know when to build your own

## What's in the kit

| File | What it is |
|---|---|
| `.mcp.json` | New: the project-scope config Claude Code wrote with `claude mcp add --scope project`, plus one line typed in the lesson: `"HARBORLINE_API_TOKEN": "${HARBORLINE_API_TOKEN}"`, a reference to a variable, never its value. Safe to commit |
| `.env.example` | Lesson 0.6's file plus two comment lines and an empty `HARBORLINE_API_TOKEN=`: it tells a new teammate what to set |
| `mcp_server/server.py` | Lesson 2.5's server with three changes: `import os` and `import sys`, server `instructions`, and a token check before `app.run()` |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

`.mcp.json` and `.env.example` start with a dot, so some file managers hide them: show hidden files, or list them with `ls -a`. The files are exactly the ones in the lesson's commit. Typing the changes yourself is the best way to learn them; if you'd rather not, copy the three files into your `harborline` folder. Don't copy `.mcp.json` *instead* of running the `claude mcp add` commands in step 1: watching where each command writes is the point of that step.

The video is filmed on Ubuntu 24.04. Most commands are the same on Windows, macOS and Linux; the differences are under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 2.5 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, Lesson 2.5's `mcp_server/server.py`, `pytest` passing (57 tests), and `origin` pointing at your own private `harborline` on GitHub.
- **Claude Code** (Lesson 0.5), signed in. The lesson's Claude Code was signed in with a Claude subscription, so its account connectors showed up and no API key was used.
- **Node.js** (Lesson 0.5): `npx` starts the memory server.
- **A local token in your `.env`.** Harborline's backend is a local simulation, so its token is one you make up. Before you start, open your `.env` in the editor and add one line: `HARBORLINE_API_TOKEN=hl_test_` followed by any letters and digits (the server only checks that it starts with `hl_`). `.env` is git-ignored (Lesson 0.6). In the lesson this line was already there; the lesson never opens or prints `.env`, and neither should you on a shared screen.
- About 30 minutes. **No API calls: Claude Code runs on your Claude sign-in.** The two questions in step 3 count toward your Claude Code usage like any other prompt.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder.

### 1. Pick a scope

```bash
clear; claude mcp list
clear; claude mcp add harborline -- .venv/bin/python -m mcp_server.server
claude mcp get harborline
clear; claude mcp remove harborline -s local
claude mcp add --scope project harborline -- .venv/bin/python -m mcp_server.server
code .mcp.json
clear; claude mcp add --scope user memory -- npx -y @modelcontextprotocol/server-memory@2026.8.31
clear; claude mcp list
```

- **`claude mcp list`** first, before you add anything. In the lesson it listed the account's connectors (`claude.ai Gmail`, `claude.ai Google Drive` and others) and a productivity plugin's servers (Slack, Notion, Linear, Atlassian, which serves Jira). Standard systems, with servers that already exist. Yours depends on your account and plugins; it can be empty.
- **`claude mcp add harborline -- …`** with no scope flag: everything after `--` is the command that starts the server. It goes to **local** scope, the default: `~/.claude.json` in your home folder, filed under this project's path. Nothing in the repo.
- **`claude mcp get harborline`**: `Scope: Local config (private to you in this project)`, `Status: ✔ Connected`. Claude Code started the server and talked to it over stdio. Nobody who clones the repo gets it.
- **`remove … -s local`**, then **`add --scope project`**: this time it's written to `.mcp.json` at the root of the repo. Open it: an `mcpServers` object with `harborline` inside: `"type": "stdio"`, the command, its arguments, and an empty `"env": {}`. This file is meant for git.
- **`add --scope user memory …`**: the reference memory server from the Model Context Protocol project, pinned to a version, at **user** scope: private to you, in every project. A personal experiment, so it doesn't belong in the repo.
- **`claude mcp list`** again, and give the health check a moment: Claude Code starts every server and asks it to respond. `memory` is `✔ Connected`; `harborline` is `Pending approval (run `claude` to approve)`: a project server waits until each developer starts Claude Code and says yes to it.

### 2. Keep the token out of git

```bash
code mcp_server/server.py
code .mcp.json
code .env.example
clear; claude mcp list
clear; export HARBORLINE_API_TOKEN="$(grep '^HARBORLINE_API_TOKEN=' .env | cut -d= -f2-)"
claude mcp list
clear; claude mcp get harborline
git status --short
git check-ignore -v .env
```

In the lesson, **Ctrl+J** hides the terminal panel while a file is edited, and **Ctrl+`** brings the terminal back.

**`mcp_server/server.py`** (compare with the kit's file):

- Under `import json`: `import os` (to read the environment) and `import sys` (to exit cleanly).
- `app = MCPServer("harborline", instructions=(…))`: the server's instructions. Use these tools for any question about a customer, an order or a refund, and don't read or search `data/` for that: it holds seed files, and it never shows the refunds made through these tools. With tool search, Claude Code loads only tool names and server instructions at the start of a session, so this paragraph is what tells Claude to reach for these tools.
- At the bottom, before `app.run()`: if `HARBORLINE_API_TOKEN` doesn't start with `hl_`, exit with `Set HARBORLINE_API_TOKEN: see .env.example`. `sys.exit` writes that to stderr, so stdout stays clean for the protocol (Lesson 2.5's rule). A real backend would check the token itself; this one only checks its shape.

**`.mcp.json`**: the empty `"env": {}` gets one entry, `"HARBORLINE_API_TOKEN": "${HARBORLINE_API_TOKEN}"`. The name of a variable, not its value: this line is safe to commit.

**`.env.example`**: under the Anthropic key line, a blank line, two comment lines and `HARBORLINE_API_TOKEN=`, left empty. The real value only ever goes in `.env`.

Then:

- **`claude mcp list`**: a new section at the bottom, `MCP config diagnostics`: `[Contains warnings] Project config (shared via .mcp.json)` and `[Warning] [harborline] mcpServers.harborline: Missing environment variables: HARBORLINE_API_TOKEN`. The config still loads, and Claude Code passes `${HARBORLINE_API_TOKEN}` through as plain text, which the server would reject: it doesn't start with `hl_`.
- **`export HARBORLINE_API_TOKEN="$(…)"`**: sets that one variable in this terminal, from your `.env`, and prints nothing. Only that one: with your `ANTHROPIC_API_KEY` in the environment too, Claude Code would use the key instead of your subscription sign-in, and your account's connectors wouldn't load.
- **`claude mcp list`** once more, and wait for the health check: no diagnostics. The variable is set, so the reference expands when the server starts.
- **`claude mcp get harborline`**: `Scope: Project config (shared via .mcp.json)`, and under `Environment:` the line `HARBORLINE_API_TOKEN=${HARBORLINE_API_TOKEN}`: the token by name, never its value.
- **`git status --short`**: ` M .env.example`, ` M mcp_server/server.py`, `?? .mcp.json`. `.env` isn't there, and **`git check-ignore -v .env`** says why: `.gitignore:9:.env`.

The export lasts as long as this terminal. Open a new terminal, and you'll need to export it again (or set the variable in your shell's startup file, never in a committed file).

### 3. Several servers at once

Start Claude Code in the same terminal, so it inherits the variable:

```bash
clear; claude
```

1. **Workspace trust.** `Quick safety check: Is this a project you created or one you trust?` The answer selected first is `No, exit`. It's your own project: press **Down**, then **Enter** for `Yes, I trust this folder`.
2. **Project server approval.** `New MCP server found in this project: harborline`. The answer selected first is `Continue without using this MCP server`. Press **Up** twice, then **Enter** for `Use this MCP server`.
3. **`/mcp`**: the servers Claude Code knows, grouped by where they're configured. In the lesson: `17 servers`; `Project MCPs (…/harborline/.mcp.json)`: `✔ harborline  4 tools`; `User MCPs (…/.claude.json)`: `✔ memory  9 tools`; then the account's connectors. **Esc** closes it.
4. Ask: `Look through the order data: what did customer C-1047 buy most recently, and when?` The repo has order data files right there, but Claude called harborline. **Ctrl+O** shows the call: `harborline - list_orders (MCP)(customer_id: "C-1047")` and the six orders it returned, newest first. **Ctrl+O** again hides it.
5. Ask: `Add C-1047 and that order to the memory server's knowledge graph.` `Called memory 2 times`: a customer, an order, and a `placed` relation between them. **Ctrl+O** shows `create_entities`, then `create_relations`.
6. **`/exit`** leaves Claude Code.

The lesson's Claude Code ran in auto mode, where it checks each tool call and runs the safe ones without asking. If yours asks before a tool call, read it and approve it: `list_orders` from harborline, `create_entities` and `create_relations` from memory.

### 4. Commit

```bash
clear; git status --short
git add .mcp.json .env.example mcp_server/server.py
git commit -m "Lesson 2.6: harborline-mcp in Claude Code, token from the environment"
git push
```

The commit has the three files (`3 files changed, 28 insertions(+), 1 deletion(-)`, `create mode 100644 .mcp.json`), and `git push` sends it to `origin`, your own private `harborline`. `.mcp.json` goes into the repo with no secret in it. A teammate who pulls gets the server, one approval prompt, and a warning until they set their own token.

**Keep the memory server and the approval.** Later lessons use the user-scope `memory` server and the approved `harborline` project server, so don't remove them.

## Windows, macOS and Linux

`git`, `code`, `claude` and `npx` are the same on every system. These lines differ:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; claude mcp list` | the same line | `cls`, then `claude mcp list` on its own line |
| The server's command | `.venv/bin/python -m mcp_server.server` | `.venv/Scripts/python -m mcp_server.server` | `.venv\Scripts\python -m mcp_server.server` |
| Set the one variable from `.env` | `export HARBORLINE_API_TOKEN="$(grep '^HARBORLINE_API_TOKEN=' .env \| cut -d= -f2-)"` | `$env:HARBORLINE_API_TOKEN = ((Select-String -Path .env -Pattern '^HARBORLINE_API_TOKEN=').Line -split '=', 2)[1]` | `for /f "tokens=1,* delims==" %a in ('findstr /b "HARBORLINE_API_TOKEN=" .env') do set "%a=%b"` |

- **Windows:** the venv's Python lives in `.venv\Scripts`, so the `claude mcp add` commands use that path, and Claude Code writes it into `.mcp.json`. That makes the file work on Windows only. A team that mixes systems can point `command` at `python` and have everyone start Claude Code with the venv active, or keep one `.mcp.json` per system out of git: pick one and write it down in the README. In PowerShell and cmd.exe, nothing is printed by the line that sets the variable either.
- **macOS:** the same commands as Linux. In VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel); in Claude Code, **Ctrl+O** is still Ctrl.
- **WSL:** run the Linux commands inside the WSL terminal, with Claude Code installed in WSL.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `claude mcp add harborline -- …` | `… to local config`, `File modified: …/.claude.json [project: …/harborline]` |
| `claude mcp get harborline` (local) | `Scope: Local config (private to you in this project)`, `Status: ✔ Connected`, `Type: stdio` |
| `claude mcp add --scope project …` | `… to project config`, `File modified: …/harborline/.mcp.json` |
| `claude mcp add --scope user memory …` | `… to user config`, `File modified: …/.claude.json` |
| `claude mcp list` | `memory: … ✔ Connected`; `harborline: … Pending approval (run `claude` to approve)` |
| `claude mcp list` with the variable unset | `MCP config diagnostics`: `Missing environment variables: HARBORLINE_API_TOKEN` |
| After the export | no diagnostics; `get` shows `HARBORLINE_API_TOKEN=${HARBORLINE_API_TOKEN}` |
| `git check-ignore -v .env` | `.gitignore:9:.env` |
| `/mcp` | `17 servers`: harborline 4 tools (project), memory 9 tools (user), the account's connectors |
| C-1047's latest order | `Called harborline`: HL-10192, October 8, 2026, a Dual-Boiler Espresso Machine, $549.00 |
| The memory request | `Called memory 2 times`: C-1047 (Customer), HL-10192 (Order), a `placed` relation |
| `git commit` | `3 files changed, 28 insertions(+), 1 deletion(-)` |
| API spend | $0: Claude Code on the subscription, no API calls |

See `expected-output.md` for the exact lines and what should match.

## Troubleshooting

- **`claude: command not found`**: Claude Code isn't installed or isn't on your PATH. Do Lesson 0.5, then open a new terminal.
- **`claude mcp get harborline` says it failed to connect**: run `.venv/bin/python -m mcp_server.server` yourself from the `harborline` folder. In step 1 it should wait silently (Ctrl+C to stop). After step 2 it exits with `Set HARBORLINE_API_TOKEN: see .env.example` unless the variable is set in that terminal.
- **The missing-variable warning won't go away**: the variable isn't set in the terminal you ran `claude mcp list` from. Check your `.env` has the line `HARBORLINE_API_TOKEN=hl_…` with no spaces around `=`, run the export line again, and run `claude mcp list` in the same terminal. Check without printing the value: `[ -n "$HARBORLINE_API_TOKEN" ] && echo set`.
- **harborline shows as failed inside Claude Code**: you started `claude` from a terminal without the variable, or the token doesn't start with `hl_`. Exit, export, start `claude` again.
- **`harborline` stays `Pending approval`**: start `claude` in the repo and choose `Use this MCP server`. If you chose `Continue without using this MCP server` by mistake, `claude mcp reset-project-choices` asks again next time.
- **`claude mcp add` says harborline already exists**: you added it twice in one scope. `claude mcp remove harborline -s local` (or `-s project`), then add it again.
- **The memory server fails to start**: `npx` needs Node.js (Lesson 0.5) and a network connection the first time, to download the package.
- **No `claude.ai` connectors in your list**: they load only when you sign in to Claude Code with a Claude subscription, and only the ones you've connected on your account. With an `ANTHROPIC_API_KEY` in the environment, they don't load. Nothing in this lesson needs them.
- **Claude reads `data/*.json` instead of calling harborline**: check the server's `instructions` and that `harborline` shows `✔` in `/mcp`. Ask about a customer or an order, as in the lesson.
- **`git status` shows `.env`**: your `.gitignore` is missing the `.env` line. Add it before you commit anything (Lesson 0.6).
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **MCP scope**: where Claude Code stores a server's config, and so who gets it: local (the default: private, one project), project (`.mcp.json`, shared through git), user (private, every project).
- **`.mcp.json`**: the project-scope file at the root of the repo, committed to version control; Claude Code asks each developer to approve its servers once.
- **Environment variable expansion**: `${VAR}`, or `${VAR:-default}`, in a server's command, args, env, URL or headers, filled in from each developer's environment.
- **Tool search**: Claude Code loads only tool names and server instructions at the start of a session, and fetches a tool's full definition when it needs it.
- **Community server**: an existing MCP server for a standard system (Jira, Slack, Gmail), used instead of writing your own.

## Sources (all checked 2026-10-14)

- **Claude Code docs, Connect Claude Code to tools via MCP.** https://code.claude.com/docs/en/mcp : installation scopes (local is the default; project scope and `.mcp.json`; user scope), scope precedence, approval of project servers, environment variable expansion in `.mcp.json`, connectors from your Claude account, tool search, and trusting servers.
- **Anthropic, *Claude Certified Architect – Foundations Exam Guide*.** Version 1.0, effective July 2026: Task Statement 2.4 (Domain 2), Scenario 2: Code Generation with Claude Code and Scenario 4: Developer Productivity with Claude.

Claude Code changes often. If a command, a message or a screen doesn't match what you see, follow the official page.

## What's next

Lesson 2.7 is about the tools Claude Code brings with it, like Read, Grep, Glob and Edit, and which one fits which job.
