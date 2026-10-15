# Expected output: Lesson 2.6, MCP in Claude Code: scopes, secrets, and many servers at once

What each step printed in the lesson, on Ubuntu 24.04 with Claude Code 2.1.300 signed in with a Claude subscription, from the `harborline` folder with `.venv` active. The terminal wrapped long lines; they're shown unwrapped here, and long lists are shortened with `…`. `~` stands for your home folder: Claude Code prints the full path.

**What will differ on yours:** the account's connectors and plugin servers in every list (they depend on your account; yours may have none), the number of servers in `/mcp`, the model and the wording of Claude's answers, the session's timings, and your commit IDs. Each section says what should match.

## Step 1: Pick a scope

```text
(.venv) $ clear; claude mcp list
claude.ai Claude Docs: https://api.anthropic.com/v1/pages/mcp - ✔ Connected
claude.ai Google Calendar: https://calendarmcp.googleapis.com/mcp/v1 - ✔ Connected
…
claude.ai Gmail: https://gmailmcp.googleapis.com/mcp/v1 - ✔ Connected
claude.ai Google Drive: https://drivemcp.googleapis.com/mcp/v1 - ✔ Connected
plugin:productivity:slack: https://mcp.slack.com/mcp (HTTP) - ! Needs authentication
plugin:productivity:notion: https://mcp.notion.com/mcp (HTTP) - ! Needs authentication
plugin:productivity:linear: https://mcp.linear.app/mcp (HTTP) - ! Needs authentication
plugin:productivity:atlassian: https://mcp.atlassian.com/v1/mcp (HTTP) - ! Needs authentication
…
(.venv) $ clear; claude mcp add harborline -- .venv/bin/python -m mcp_server.server
Added stdio MCP server harborline with command: .venv/bin/python -m mcp_server.server to local config
File modified: ~/.claude.json [project: ~/projects/harborline]
(.venv) $ claude mcp get harborline
harborline:
  Scope: Local config (private to you in this project)
  Status: ✔ Connected
  Type: stdio
  Command: .venv/bin/python
  Args: -m mcp_server.server
  Environment:

To remove this server, run: claude mcp remove harborline -s local
(.venv) $ clear; claude mcp remove harborline -s local
Removed MCP server harborline from local config
File modified: ~/.claude.json [project: ~/projects/harborline]
(.venv) $ claude mcp add --scope project harborline -- .venv/bin/python -m mcp_server.server
Added stdio MCP server harborline with command: .venv/bin/python -m mcp_server.server to project config
File modified: ~/projects/harborline/.mcp.json
(.venv) $ code .mcp.json
(.venv) $ clear; claude mcp add --scope user memory -- npx -y @modelcontextprotocol/server-memory@2026.8.31
Added stdio MCP server memory with command: npx -y @modelcontextprotocol/server-memory@2026.8.31 to user config
File modified: ~/.claude.json
(.venv) $ clear; claude mcp list
…
memory: npx -y @modelcontextprotocol/server-memory@2026.8.31 - ✔ Connected
harborline: .venv/bin/python -m mcp_server.server - □ Pending approval (run `claude` to approve)
```

Each `claude mcp list` first prints `Checking MCP server health…` while Claude Code starts the servers; give it a few seconds (in the lesson, up to about ten). The `□` before `Pending approval` is a symbol the lesson's terminal font couldn't draw; yours may show it properly.

`.mcp.json`, as Claude Code wrote it:

```json
{
  "mcpServers": {
    "harborline": {
      "type": "stdio",
      "command": ".venv/bin/python",
      "args": [
        "-m",
        "mcp_server.server"
      ],
      "env": {}
    }
  }
}
```

What should match: `to local config` for the first add and `Scope: Local config (private to you in this project)`; `to project config` and `.mcp.json` for the second; `to user config` for memory; at the end, `memory` connected and `harborline` pending approval. The connectors and plugin servers above them are the lesson account's.

## Step 2: Keep the token out of git

```text
(.venv) $ code mcp_server/server.py
(.venv) $ code .mcp.json
(.venv) $ code .env.example
(.venv) $ clear; claude mcp list
…
memory: npx -y @modelcontextprotocol/server-memory@2026.8.31 - ✔ Connected
harborline: .venv/bin/python -m mcp_server.server - □ Pending approval (run `claude` to approve)

MCP config diagnostics ⚠

For help configuring MCP servers, see: https://code.claude.com/docs/en/mcp

[Contains warnings] Project config (shared via .mcp.json)
Location: ~/projects/harborline/.mcp.json
 └ [Warning] [harborline] mcpServers.harborline: Missing environment variables: HARBORLINE_API_TOKEN

(.venv) $ clear; export HARBORLINE_API_TOKEN="$(grep '^HARBORLINE_API_TOKEN=' .env | cut -d= -f2-)"
(.venv) $ claude mcp list
…
memory: npx -y @modelcontextprotocol/server-memory@2026.8.31 - ✔ Connected
harborline: .venv/bin/python -m mcp_server.server - □ Pending approval (run `claude` to approve)
(.venv) $ clear; claude mcp get harborline
harborline:
  Scope: Project config (shared via .mcp.json)
  Status: □ Pending approval (run `claude` to approve)
  Type: stdio
  Command: .venv/bin/python
  Args: -m mcp_server.server
  Environment:
    HARBORLINE_API_TOKEN=${HARBORLINE_API_TOKEN}

To remove this server, run: claude mcp remove harborline -s project
(.venv) $ git status --short
 M .env.example
 M mcp_server/server.py
?? .mcp.json
(.venv) $ git check-ignore -v .env
.gitignore:9:.env	.env
```

Saving the three files prints nothing, and so does the export. What should match: the missing-variable warning while the variable is unset, no `MCP config diagnostics` after the export, the token shown by name (`${HARBORLINE_API_TOKEN}`) and never by value, the three `git status` entries, and `.env` ignored. The line number in `.gitignore:9` can differ if your `.gitignore` differs from Lesson 0.6's.

## Step 3: Several servers at once

```text
(.venv) $ clear; claude
```

| Action | What Claude Code showed in the lesson |
|---|---|
| Start | `Accessing workspace:` `~/projects/harborline`, `Quick safety check: Is this a project you created or one you trust?`, `❯ No, exit` selected, `Yes, I trust this folder` below it |
| Down, Enter | `New MCP server found in this project: harborline`: `Use this MCP server`, `Use this and all future MCP servers in this project`, `❯ Continue without using this MCP server` selected |
| Up, Up, Enter | The banner: `Claude Code v2.1.300`, `Haiku 5.5 · Claude Max`, `~/projects/harborline`; below the prompt, `auto mode on` |
| `/mcp` | `Manage MCP servers`, `17 servers`; `Project MCPs (~/projects/harborline/.mcp.json)`: `✔ harborline  4 tools`; `User MCPs (~/.claude.json)`: `✔ memory  9 tools`; `claude.ai`: `Claude Docs  8 tools`, `Gmail  30 tools`, `Google Calendar  9 tools`, `↓ 11 more` |
| Esc, then the first question | `Called harborline (ctrl+o to expand)`, then: "The most recent order from customer C-1047 is **HL-10192**, placed on **October 8, 2026**. It contained one item, a Dual-Boiler Espresso Machine, for $549.00." and a line on reading "most recently" as the latest order |
| Ctrl+O | `harborline - list_orders (MCP)(customer_id: "C-1047")` and its result: six orders, newest first: HL-10192 (2026-10-08, $549.00), HL-10139 (2026-09-19), HL-10130 (2026-09-11), HL-10092 (2026-08-12), HL-10053 (2026-07-11), HL-10006 (2026-06-03) |
| Ctrl+O, then the second question | `Called memory 2 times (ctrl+o to expand)`, then "I added both to the memory server's knowledge graph:" C-1047 (Customer), HL-10192 (Order), "A placed relation from C-1047 to HL-10192." |
| Ctrl+O | The two calls, `create_entities` then `create_relations`, ending in `"relationType": "placed"` |
| `/exit` | `Resume this session with:` `claude --resume` and the session's ID, then the shell prompt |

What should match: the two dialogs and their first selected answers, `harborline` under `Project MCPs` with 4 tools, `memory` under `User MCPs` with 9 tools, the call to `harborline - list_orders (MCP)` for C-1047, HL-10192 as the latest order, and two memory calls. What will differ: the server count and the connectors, the model in the banner, the permission mode, and the wording of each answer. Each answer is written fresh; the facts come from the tools.

## Step 4: Commit

```text
(.venv) $ clear; git status --short
 M .env.example
 M mcp_server/server.py
?? .mcp.json
(.venv) $ git add .mcp.json .env.example mcp_server/server.py
(.venv) $ git commit -m "Lesson 2.6: harborline-mcp in Claude Code, token from the environment"
[main f10037e] Lesson 2.6: harborline-mcp in Claude Code, token from the environment
 3 files changed, 28 insertions(+), 1 deletion(-)
 create mode 100644 .mcp.json
(.venv) $ git push
Enumerating objects: 10, done.
Counting objects: 100% (10/10), done.
Delta compression using up to 24 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (6/6), 1.13 KiB | 1.13 MiB/s, done.
Total 6 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/YOUR-USERNAME/harborline.git
   7079c07..f10037e  main -> main
```

What should match: the three entries in `git status`, `3 files changed, 28 insertions(+), 1 deletion(-)` and `create mode 100644 .mcp.json` if your files match the kit's, and `main -> main`. What will differ: the commit IDs (yours are your own), the object counts and sizes, the thread count, and the URL (your own account).
