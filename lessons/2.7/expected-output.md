# Expected output: Lesson 2.7, Built-in tools: Read, Write, Edit, Bash, Grep, Glob

What each step printed in the lesson, on Ubuntu 24.04 with Claude Code 2.1.300 (Haiku 5.5, auto mode) signed in with a Claude subscription, from the `harborline` folder with `.venv` active. Claude Code's screens are summarized: its answers are written fresh each time, so yours will be worded differently. The terminal wrapped long lines; they're shown unwrapped here, and long output is shortened with `…`.

**What will differ on yours:** the wording of every answer, the order and number of searches and reads, the model in the banner, the permission mode, the timings, and your commit IDs. On native Windows, step 1 uses the Grep tool instead of Bash. Each section says what should match.

## Step 1: The default tool set

```text
(.venv) $ clear; claude
```

| Action | What Claude Code showed in the lesson |
|---|---|
| Start | The banner: `Claude Code v2.1.300`, `Haiku 5.5 · Claude Max`, `~/projects/harborline`; below the prompt, `auto mode on` |
| The getStatus question | `Bash(git grep -n "getStatus" ; echo "---"; git grep -n "get_status\|getstatus\|GetStatus" ; echo "---"; git ls-files \| head -200)`, its first hits `legacy/warehouse/__init__.py:8:from legacy.warehouse.compat import getStatus, get_status_text` and `legacy/warehouse/__init__.py:15:    "getStatus",`, then `Allowed by auto mode classifier` and `Read 1 file` |
| The answer | "The name getStatus is a plain alias. No function is defined under that name. It is the same function object as status_name, bound under a second name in compat.py." Then file by file, ending with `tests/test_legacy.py:10: assert warehouse.getStatus(3) == "shipped"` and "So a call to getStatus(3) runs status_name(3) in codes.py:14, which returns "shipped"." and "I searched the tracked files with git grep." |
| `/exit` | Back at the shell prompt, after Claude Code's resume line |

What should match: no Grep or Glob tool call on macOS, Linux and WSL (the search runs through Bash), and the chain: `codes.py` defines `status_name`; `compat.py` binds `getStatus = status_name`; `__init__.py` re-exports it; the test calls it and gets `"shipped"`. The answer may also mention the file selected in your editor's Explorer, which VS Code passes to Claude Code.

## Step 2: Grep and Glob as tools

```text
(.venv) $ clear; claude --allowedTools Grep Glob
```

| Action | What Claude Code showed in the lesson |
|---|---|
| The same question | `Searching for 1 pattern…` `"getStatus"`, then `Searched for 1 pattern, read 3 files (ctrl+o to expand)`; "Now the function that getStatus actually points to."; `Searching for 1 pattern…` `"status_name\|STATUS_NAMES"` |
| The answer | 1. `legacy/warehouse/codes.py:3-16` defines the real function, `status_name(code)`; 2. `legacy/warehouse/compat.py:3,6` binds it to a second name: `getStatus = status_name`, "a plain assignment"; 3. `legacy/warehouse/__init__.py:8,15` re-exports `getStatus` and lists it in `__all__`; `tests/test_legacy.py:10` calls `warehouse.getStatus(3)`, which runs `status_name(3)` and returns `"shipped"`. "A repo-wide search found only those four hits." |
| The test-file question | Glob, `"**/test_*.py"`; "The repo has 9 test files of its own, all in tests/:" `tests/test_backend.py`, `tests/test_costs.py`, `tests/test_data.py`, `tests/test_invoices.py`, `tests/test_legacy.py`, `tests/test_loop.py`, `tests/test_mcp_server.py`, `tests/test_policy.py`, `tests/test_tickets.py`. "The search also matched about 25 files under .venv/. Those belong to installed packages … and aren't part of the project. I left them out of the list above." |

What should match: Grep tool calls (`Searching for … pattern`) instead of Bash `git grep`, the same chain, and Glob for the test files: the nine `tests/test_*.py` files. How many `.venv` files Glob also matches depends on the packages in your environment.

## Step 3: One Edit, one anchor

| Action | What Claude Code showed in the lesson |
|---|---|
| The rename request | `Reading 1 file…` `legacy/warehouse/records.py`, then one Edit: in `read_record`, lines 17 to 23, every `record` red and every `order` green (`order = dict(raw)`, the two lines in the loop, the status line, `return order`) |
| Claude's own check | `Bash(.venv/bin/python -m pytest tests/test_legacy.py -q 2>&1 \| tail -5)`: `...` `[100%]`, `3 passed in 0.03s`, `Allowed by auto mode classifier` |
| The answer | "I renamed the local variable record to order in read_record in legacy/warehouse/records.py. All four uses changed: the copy, the loop body, the status line, and the return. The function's behavior is the same. tests/test_legacy.py passes (3 tests), including the one that calls read_record through the package." |
| `Run the legacy tests.` | `Bash(.venv/bin/python -m pytest tests/test_legacy.py -v 2>&1 \| tail -15)`; "All 3 legacy tests pass in tests/test_legacy.py:" `test_status_codes_and_old_names`, `test_reading_a_legacy_record`, `test_the_old_shipping_rule` |
| `/exit` | Back at the shell prompt |

What should match: Claude reads `records.py` before changing it, makes one Edit that changes only the variable inside `read_record` (the function keeps its name), and the three legacy tests pass. Whether Claude runs the tests on its own before you ask can vary.

## Step 4: Commit

```text
(.venv) $ clear; git diff --stat
 legacy/warehouse/records.py | 12 ++++++------
 1 file changed, 6 insertions(+), 6 deletions(-)
(.venv) $ git diff
diff --git a/legacy/warehouse/records.py b/legacy/warehouse/records.py
index 1a58c23..e3ff911 100644
--- a/legacy/warehouse/records.py
+++ b/legacy/warehouse/records.py
@@ -14,10 +14,10 @@ def epoch_to_iso(seconds):
 
 def read_record(raw):
     """Return a copy of a legacy order with readable dates and status."""
-    record = dict(raw)
+    order = dict(raw)
     for field in ("placed_at", "delivered_at", "promised_by"):
-        if isinstance(record.get(field), int):
-            record[field] = epoch_to_iso(record[field])
-    if isinstance(record.get("status"), int):
-        record["status"] = status_name(record["status"])
-    return record
+        if isinstance(order.get(field), int):
+            order[field] = epoch_to_iso(order[field])
+    if isinstance(order.get("status"), int):
+        order["status"] = status_name(order["status"])
+    return order
(.venv) $ git add legacy/warehouse/records.py
(.venv) $ git commit -m "Lesson 2.7: rename a local variable with one Edit (a unique anchor)"
[main dcd8ddb] Lesson 2.7: rename a local variable with one Edit (a unique anchor)
 1 file changed, 6 insertions(+), 6 deletions(-)
(.venv) $ git push
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 24 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (5/5), 581 bytes | 581.00 KiB/s, done.
Total 5 (delta 3), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To https://github.com/YOUR-USERNAME/harborline.git
   f10037e..dcd8ddb  main -> main
```

What should match: `1 file changed, 6 insertions(+), 6 deletions(-)` and the diff above if Claude's edit matches the kit's `records.py` (the `index` line's IDs match too if your starter file was unchanged), and `main -> main`. What will differ: the commit IDs (yours are your own), the object counts and sizes, the thread count, and the URL (your own account).
