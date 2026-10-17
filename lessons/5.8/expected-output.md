# Expected output: Lesson 5.8, A developer productivity agent

What each step showed in the lesson (claude-agent-sdk 0.2.165 with Haiku 5.5 on the API, mcp 2.3.0, Python 3.12, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. The agent's wording, its tool calls and its costs change from run to run; compare the behavior, not the exact text. Paths below are shortened to `<home>/projects/harborline`.

## Step 1: the MCP server

`git status --short` prints nothing (the tree is clean). `mkdir` and `touch` print nothing either. `codemap_server.py` is typed and saved; nothing runs yet.

## Step 2: its test

```text
$ .venv/bin/python -m pytest -q tests/test_codemap.py
..                                                                       [100%]
2 passed in 0.69s
```

## Step 3: the agent

`explorer.py` is typed and saved; nothing runs yet.

## Step 4: map and generate

Question 1. First a notice (the API key takes precedence over your claude.ai sign-in for this run; harmless), then the tool calls and the answer:

```text
⚠ claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set and takes precedence over your claude.ai login · Unset it to load your organization's connectors
tool: trace_export {'module': 'legacy.warehouse', 'name': 'load_record'}
tool: Read {'file_path': '<home>/projects/harborline/legacy/warehouse/records.py'}
`legacy.warehouse.load_record` is a re-export of `read_record`. It is not a separate function.

**Where it comes from:** The export chain is `legacy.warehouse:load_record` → `legacy.warehouse.records:read_record`. The definition is in `legacy/warehouse/records.py`, line 15. Because the name is renamed on export, a text search for `load_record` won't find the definition. Search for `read_record` instead.

**What it returns:** It takes a raw legacy order (a dict-like object) and returns a new dict copy (`dict(raw)`), so the input is not mutated. Two fields are converted:

- `placed_at`, `delivered_at`, and `promised_by`: if the value is an `int`, it is converted from Unix seconds to a UTC ISO 8601 string via `epoch_to_iso` (line 8). Other values, including `None`, are left as they are.
- `status`: if it is an `int`, it is replaced with a readable name via `status_name` from `legacy.warehouse.codes`.

All other fields are passed through unchanged.
success: 3 turns, $0.0013
```

The point to check: the first tool call is `trace_export`, and there is no Grep.

Question 2. The first lines:

```text
I'll start by checking the legacy.warehouse exports and the normalize.order() shape.
tool: list_public_names {'module': 'legacy.warehouse'}
tool: list_public_names {'module': 'harborline.normalize'}
tool: Bash {'command': 'git status --short && ls -la && ls devtools tests 2>&1; ls .venv/bin/python 2>&1', 'description': 'Check repo state, layout, and venv'}
Bash is denied in this session, so I can't run pytest. I'll read the source with the file tools and come back to that.
```

That Bash call doesn't match the one allowed rule, `Bash(.venv/bin/python -m pytest *)`, so `dontAsk` refused it. The agent then read `normalize.py`, the legacy package and two existing tests, said "The package exports `load_record`, which is `read_record` under another name. That's the one to use.", and wrote `devtools/warehouse_adapter.py` and `tests/test_warehouse_adapter.py`. The end of its answer:

```text
Both imports resolve through the `pythonpath = .` setting in `pytest.ini`. I checked the epoch values by hand, not by running them, so a failing run would most likely point to one of those.

To run the test, approve Bash for that one command or run it yourself:

    .venv/bin/python -m pytest -q tests/test_warehouse_adapter.py

I haven't committed anything.
success: 16 turns, $0.0058
```

Yours may run the allowed pytest command itself, or not; it may also take a different number of turns. What matters: it uses codemap's tools, writes both files, and you verify.

## Verify, then commit

```text
$ .venv/bin/python -m pytest -q
........................................................................ [ 61%]
...............................................                          [100%]
129 passed in 3.90s
$ git status --short
?? devtools/
?? tests/test_codemap.py
?? tests/test_warehouse_adapter.py
$ git add devtools tests/test_codemap.py tests/test_warehouse_adapter.py
$ git commit -m "Lesson 5.8: codemap MCP server and an Agent SDK explorer that uses it"
[main 1c77648] Lesson 5.8: codemap MCP server and an Agent SDK explorer that uses it
 6 files changed, 202 insertions(+)
 create mode 100644 devtools/__init__.py
 create mode 100644 devtools/codemap_server.py
 create mode 100644 devtools/explorer.py
 create mode 100644 devtools/warehouse_adapter.py
 create mode 100644 tests/test_codemap.py
 create mode 100644 tests/test_warehouse_adapter.py
$ git push
...
   37c0ab3..1c77648  main -> main
```

Your count of passing tests, your commit hash and your insertions will differ a little. If `__pycache__` folders show up under `devtools/`, they are ignored by `.gitignore` and not committed.
