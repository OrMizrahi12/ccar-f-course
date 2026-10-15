# Expected output: Lesson 2.5, MCP from zero: build a server

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12.3 and Node.js 22, from the `harborline` folder with `.venv` active. No model is called in this lesson. The terminal wrapped long lines; they're shown unwrapped here, and long lists are shortened with `…`.

**What will differ on yours:** times, timestamps, pip's download lines (the lesson's machine had the wheels cached, so pip printed `Using cached …`; yours may print `Downloading …`), the Inspector's address and token, and your commit IDs. Each section says what should match.

## Step 1: Install and write

```text
(.venv) $ git status --short
(.venv) $ code requirements.txt
(.venv) $ clear; pip install -r requirements.txt
Requirement already satisfied: anthropic==1.13.0 in ./.venv/lib/python3.12/site-packages (from -r requirements.txt (line 2)) (1.13.0)
Requirement already satisfied: python-dotenv==1.2.4 in ./.venv/lib/python3.12/site-packages (from -r requirements.txt (line 3)) (1.2.4)
Requirement already satisfied: pytest==9.1.1 in ./.venv/lib/python3.12/site-packages (from -r requirements.txt (line 4)) (9.1.1)
…
Collecting mcp-types==2.3.0 (from mcp==2.3.0->-r requirements.txt (line 5))
…
Installing collected packages: rpds-py, python-multipart, pyjwt, pycparser, opentelemetry-api, click, attrs, uvicorn, starlette, referencing, cffi, sse-starlette, mcp-types, jsonschema-specifications, cryptography, jsonschema, mcp
Successfully installed attrs-26.1.0 cffi-2.1.1 click-8.5.0 cryptography-50.0.2 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 mcp-2.3.0 mcp-types-2.3.0 opentelemetry-api-1.45.1 pycparser-3.11 pyjwt-2.15.1 python-multipart-0.0.32 referencing-0.37.0 rpds-py-2026.9.1 sse-starlette-3.5.0 starlette-1.8.0 uvicorn-0.54.0
(.venv) $ code mcp_server/server.py
```

`git status --short` prints nothing: the tree is clean after Lesson 2.4. Saving prints nothing. What should match: the three "already satisfied" lines, and `mcp-2.3.0` and `mcp-types-2.3.0` in the `Successfully installed` line (17 packages). The other versions are what `mcp` 2.3.0 pulled in on the lesson's day; yours can be newer.

## Step 2: Test it in memory

```text
(.venv) $ code tests/test_mcp_server.py
(.venv) $ clear; pytest -q
.........................................................                [100%]
57 passed in 1.05s
```

What should match: `57 passed` (Lesson 2.4's 54 plus the three new ones). Your time will differ.

## Step 3: The MCP Inspector

```text
(.venv) $ clear; npx @modelcontextprotocol/inspector@2.10.1 python -m mcp_server.server
Need to install the following packages:
@modelcontextprotocol/inspector@2.10.1
Ok to proceed? (y) y
```

The first run downloads the package (in the lesson, about 17 seconds of an empty terminal). Then the Inspector prints a few lines: its address, which looks like `http://127.0.0.1:6274/?MCP_INSPECTOR_API_TOKEN=<your token>`, and an `Auth token:` line. Never share them. In the lesson it also printed a warning that the OS keychain wasn't available, so secrets went to a file instead. It opens the address in your browser.

In the browser:

| Action | What the Inspector showed in the lesson |
|---|---|
| Connect | `Connected`; the header shows `harborline` and `MCP 2025-11-25` |
| Tools | `get_customer`, `lookup_order`, `list_orders`, `process_refund` |
| `lookup_order`, Order Id `HL-10211`, Execute tool | **Tool Error**: `{"errorCategory": "transient", "isRetryable": true, "message": "The warehouse system timed out. Try again in a moment."}` |
| Close, Execute again | The order as JSON: `"order_id": "HL-10211"`, `"customer_id": "C-1010"`, `"status": "processing"`, `"promised_by": "2026-10-19"`, one item `"name": "Cast Iron Skillet 12in"`, `"total": 55.95`, `"tracking": null` |
| `list_orders`, Customer ID `C-1058`, Execute tool | `[]` and no error card |
| Resources | `URIs (2)`: `refund_policy`, `product_catalog` |
| `refund_policy` | `harborline://policy/refunds`, `text/markdown`, rendered: "Harborline Refund and Returns Policy", "Effective July 1, 2026. …" |
| Prompts, `order_help`, order_id `HL-10163`, Get prompt | `[0] role: user` "A customer is asking about order HL-10163. Look it up with lookup_order, then answer from what it returns." |

The protocol log on the right lists each request, newest first: `TOOLS/CALL`, `RESOURCES/READ`, `PROMPTS/GET`. What should match: everything in the table except timestamps. The Tool Error appears on the first lookup of HL-10211 after the server starts; if you've already looked it up, stop the Inspector and start it again.

```text
^C
(.venv) $
```

**Ctrl+C** in the terminal stops the Inspector and the server it started.

## Step 4: Commit

```text
(.venv) $ clear; git status --short
 M requirements.txt
?? mcp_server/
?? tests/test_mcp_server.py
(.venv) $ git add requirements.txt mcp_server tests/test_mcp_server.py
(.venv) $ git commit -m "Lesson 2.5: harborline-mcp server, in-memory tests"
[main 7079c07] Lesson 2.5: harborline-mcp server, in-memory tests
 3 files changed, 129 insertions(+)
 create mode 100644 mcp_server/server.py
 create mode 100644 tests/test_mcp_server.py
(.venv) $ git push
Enumerating objects: 10, done.
Counting objects: 100% (10/10), done.
Delta compression using up to 24 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (7/7), 2.30 KiB | 2.30 MiB/s, done.
Total 7 (delta 3), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To https://github.com/YOUR-USERNAME/harborline.git
   a71f1e8..7079c07  main -> main
```

What should match: the three entries in `git status`, `3 files changed, 129 insertions(+)` if your files match the kit's, and `main -> main`. What will differ: the commit IDs (yours are your own), the object counts and sizes, the thread count, and the URL (your own account). `mcp_server/__pycache__/` doesn't show up: Lesson 0.6's `.gitignore` ignores `__pycache__`.
