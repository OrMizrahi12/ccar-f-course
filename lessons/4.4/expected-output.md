# Expected output: Lesson 4.4, Choosing a decomposition strategy

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. Long lines are wrapped by the terminal, so they're shown here unwrapped.

**What will differ on yours:** the wording of every note, which problems each pass picks, the explorer's steps, its notes and its plan, the costs, and your commit ID. Claude's answers vary from run to run, and the explorer's steps depend on what it finds. Each section says what should match.

## Step 1: Two modes in one file

```text
(.venv) $ git status --short
(.venv) $ mkdir -p experiments/m4
(.venv) $ code experiments/m4/decompose.py
```

`git status --short` prints nothing: a clean tree after Lesson 4.3. Then type `experiments/m4/decompose.py` (106 lines) and save it.

## Step 2: The chain

```text
(.venv) $ clear; python -m experiments.m4.decompose chain 2> runs/decompose.log
--- legacy/warehouse/__init__.py
No definite problems. The file imports each name from its defining submodule and lists them all in `__all__`, and the aliases (`load_record`, `shipping_quote`) match the docstring. Whether the submodules define these names, and whether they import back into `legacy.warehouse` in a way that causes a circular import, can't be checked from this file alone.

--- legacy/warehouse/codes.py
16: `status_name` returns `"unknown"` for any unmapped code, so bad or new codes are silently mislabeled instead of raising or logging.
3: Codes 5, 6 and 8 are missing with no comment; if they exist in the legacy data, they will all map to `"unknown"`.
16: A string code such as `"3"` (common when parsing legacy exports) also silently returns `"unknown"` rather than being converted or rejected.

--- legacy/warehouse/compat.py
7: `get_status_text` is documented as accepting strings, but `int(code)` raises `ValueError` for non-integer strings such as `"A"` or `"1.0"`.
11: `.upper()` raises `AttributeError` if `status_name` returns `None` for an unknown code. I can't see `codes.py`, so this depends on what it returns.
6: `getStatus` is bound at import time, so it will not follow any later change to `status_name`, such as a monkeypatch or reassignment. This is harmless if intended.

--- legacy/warehouse/records.py
- **Line 19:** `isinstance(..., int)` silently leaves float or string timestamps (e.g. `"1719928800"` or `1719928800.0`) as raw values, so the output mixes formats with no error.
- **Line 12:** `datetime.fromtimestamp` raises `OverflowError`/`OSError`/`ValueError` on out-of-range values, and legacy data may contain sentinels like `-1` or huge numbers. One bad record would abort the whole read with no record identified.
- **Line 21:** Whether an unknown integer status raises depends on `status_name`, which isn't shown here. If it raises, one unrecognized code would fail the whole record.

--- legacy/warehouse/shipping.py
15: `ZONE_RATES[zone]` raises a bare `KeyError` for any unrecognised zone name, with no validation or clear error message.
13: The `>` comparison charges shipping on exactly $75.00, unlike the web store's `>=`. The docstring says this is intentional legacy behaviour, but the two systems will quote different totals for the same order.
3: Currency amounts are stored and returned as binary floats, which can produce rounding errors in sums. Decimal or integer cents would be safer.

--- across the files
- **`compat.py` `get_status_text` vs. `codes.py` `status_name` / `compat.py` `getStatus`:** The same code gives different casing ("SHIPPED" vs. "shipped"), and both paths are exported from `__init__.py`.
- **`records.py` `read_record` vs. `compat.py` `get_status_text`:** `read_record` converts only integer statuses, so a string code like `"3"` passes through unchanged, yet `get_status_text` accepts that same string.
- **`records.py` `read_record` / `codes.py` `status_name`:** Unmapped codes (5, 6, 8, or new ones) are replaced with the string `"unknown"`, so the original numeric value is lost from the record and cannot be recovered.
- **`shipping.py` `quote` (exported as `shipping_quote`) vs. the web store:** The package's public shipping function applies the legacy `>` threshold, so it quotes different totals from the web store's `>=` for an order of exactly $75.00.

6 calls, fixed before the run · $0.0032
```

**Should match:**

- Five `--- legacy/warehouse/<file>` blocks in name order, each with at most three problems, then `--- across the files`.
- The per-file passes only see their own file, and may say so (above, `compat.py` and `records.py` do).
- The cross-file block names two or more files per point: problems between files, not inside one.
- The last line reads `6 calls, fixed before the run`, every time. The cost is a fraction of a cent.

The cross-file prompt says not to repeat the per-file notes. In the lesson, its last point (the `>` threshold) still overlapped the note on `shipping.py`: the model doesn't always follow that instruction to the letter. The run takes about half a minute.

## Step 3: The open-ended plan

```text
(.venv) $ clear; python -m experiments.m4.decompose explore 2> runs/decompose.log
I'll list the files under `legacy/warehouse` to map the package.
   1. Glob legacy/warehouse/**/* .
I'll grep for public definitions in the source files so I can record their names.
   2. Grep ^(class|def|[A-Z_][A-Za-z0-9_]*\s*=) legacy/warehouse content True *.py
   3. Grep legacy\.warehouse|from \.+(warehouse)?\.?(shipping|codes|compat|records)|import warehouse|warehouse\.(shipping|codes|compat|records) . content True
The public names are clear now. Next I'll read the four source modules and the existing legacy test, since they're small and I need their logic.
   4. Read legacy/warehouse/shipping.py
   5. Read legacy/warehouse/codes.py
   6. Read legacy/warehouse/compat.py
   7. Read legacy/warehouse/records.py
   8. Read legacy/warehouse/__init__.py
   9. Read tests/test_legacy.py
Two things changed the picture. The existing `tests/test_legacy.py` already covers some happy paths. `codes.status_name` has more importers than the rest of the package. Next I'll check whether any code outside the package uses the re-exported names, which the import grep might have missed.
  10. Grep shipping_quote|load_record|getStatus|get_status_text|epoch_to_iso|read_record|status_name|STATUS_NAMES|ZONE_RATES|FREE_SHIPPING_OVER|warehouse . content True !legacy/**
The data directory shows that real legacy orders flow through this package. Next I'll check which status codes and timestamp types actually appear in `data/orders.json`, to see whether the code table covers them.
  11. Grep "(status|placed_at|delivered_at|promised_by)": *("[^"]*"|[0-9.]+|null) data/orders.json count
  12. Read harborline/normalize.py
The `to_utc` in `harborline/normalize.py` duplicates some of `records.py`, which matters for the plan. Next I'll check whether any status values fall outside the code table.
  13. Grep "status": (5|6|8|[0-9]{2,}|"[^"]*"|[0-9.]+\.[0-9]+)\b data/orders.json content True 15
No out-of-table status values turned up. Last check: whether legacy timestamps are ever floats or strings, since `read_record` only converts `int`.
  14. Grep "(placed_at|delivered_at|promised_by)": (\d+\.\d+|"[^"]*"|true|false) data/orders.json count
I didn't change any files. The package is small: four modules and an `__init__` that re-exports them under new names. `codes.status_name` is the most-used piece, and `shipping.quote` has the riskiest business rule.

**What changed the plan**
- `codes.py` is imported by `harborline/normalize.py`, `mcp_server/server.py`, `tests/test_lab2.py`, and by `compat.py` and `records.py` inside the package. It moves to the top.
- `harborline/normalize.py` has its own `to_utc`, which duplicates `records.epoch_to_iso` with a different format (`Z` instead of `+00:00`) and different handling of floats. That divergence is a risk the package tests alone won't catch.
- `shipping.quote` is only reached through the package and its test, but it charges money. Its `>` rule at exactly $75 is documented as deliberate legacy behavior, and it differs from the web store's `>=`.
- `data/orders.json` has no out-of-table status codes, but I did not confirm whether legacy timestamps are ever floats or strings. The count I ran mixed in web orders, so it proves nothing.

**Plan, most important first**
1. `codes.status_name` and `STATUS_NAMES`: known codes, unknown codes returning `"unknown"`, and a check that the table matches what `mcp_server` and `test_lab2` expect.
2. `harborline/normalize.to_utc` against `records.epoch_to_iso`: pin both formats, floats, `None`, and date-only strings before any consolidation.
3. `records.read_record`: `None` passthrough, non-int values left as-is, `bool` treated as int, input not mutated.
4. `shipping.quote`: all three zones, the `>` boundary at exactly $75 (pin current behavior and flag the `>=` mismatch), and an unknown zone raising `KeyError`.
5. `compat.get_status_text`: int and string input, and `None`, `"4.0"`, or `"abc"` raising.
6. `compat.getStatus` alias identity, and `__init__` exports matching `__all__` and the renamed names (`load_record`, `shipping_quote`).
7. Keep `tests/test_legacy.py` and extend it rather than replace it; it already covers the happy paths.
8. Before finalizing item 3, sample real legacy records in `data/orders.json` to confirm whether non-int timestamps occur.

14 tool calls, chosen during the run · 15 turns · $0.0048
```

**Should match:**

- The agent maps before it ranks: a `Glob` of the package and `Grep` for names and importers come before the plan.
- Every step is a `Read`, `Grep` or `Glob` (it can look, not change), and a one-line note says what it will do next and why.
- At some point a finding changes the plan, and the agent says so.
- The plan has at most eight lines, most important first, and the last line reads `N tool calls, chosen during the run · N turns · $...`.

Your steps, their order and their number will differ: in the practice runs before filming the agent took 13 or 14 tool calls and changed its plan for different reasons. The run takes under a minute.

## Step 4: Commit

```text
(.venv) $ clear; git status --short
?? experiments/m4/
(.venv) $ git add experiments
(.venv) $ git commit -m "Lesson 4.4: a fixed review chain, file by file and then across files, and an open-ended plan that adapts"
[main 4f51458] Lesson 4.4: a fixed review chain, file by file and then across files, and an open-ended plan that adapts
 1 file changed, 106 insertions(+)
 create mode 100644 experiments/m4/decompose.py
(.venv) $ git push
...
   eea31f2..4f51458  main -> main
```

**Should match:** `1 file changed, 106 insertions(+)` if your file matches the kit's. Your commit IDs will differ.
