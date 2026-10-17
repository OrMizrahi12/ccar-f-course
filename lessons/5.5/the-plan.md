# Retire legacy/warehouse/compat.py

## Context
`compat.py` holds two 2023-era shims over `legacy.warehouse.codes.status_name`:
- `getStatus` = alias of `status_name`
- `get_status_text(code)` = `status_name(int(code)).upper()`

Explore found no production users. The only consumers are the package re-export and one test.

## Dependents
- `legacy/warehouse/__init__.py:8` imports both; `__all__` lists them (lines 15-16).
- `tests/test_legacy.py:10-11` call `warehouse.getStatus(3)` (expects "shipped") and `warehouse.get_status_text("9")` (expects "CANCELLED") via the package.
- No dynamic imports, config, docs, CI or packaging references.

## Steps
1. Delete `legacy/warehouse/compat.py`.
2. In `legacy/warehouse/__init__.py`, remove the compat import (line 8) and the `"getStatus"`/`"get_status_text"` entries in `__all__`.
3. In `tests/test_legacy.py`, drop the two compat assertions (or repoint them at `codes.status_name`, e.g. `status_name(3) == "shipped"`, `status_name(int("9")).upper() == "CANCELLED"`) if the behavior is still worth covering.
4. Optionally check `experiments/m4/decompose.py` still runs, since it walks the package's files.

## Verification
- `.venv/bin/python -m pytest -q tests/test_legacy.py`, then the full suite `.venv/bin/python -m pytest -q`.
- `grep -rn "compat\|getStatus\|get_status_text" --include=*.py .` returns nothing.
- One commit, one line, e.g. "Remove legacy warehouse compat shim".
