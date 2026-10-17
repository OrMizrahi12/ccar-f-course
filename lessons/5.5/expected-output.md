# Expected output: Lesson 5.5, Plan mode or direct execution

What each step showed in the lesson, copied from the screen. Claude's wording and the order of its tool calls will differ on your machine, and so will times, token counts and commit ids. What should match: no plan and no approval menu in step 1; `>=` in `shipping.py` and the two test values; Explore running as its own agent in step 2; a plan that names `legacy/warehouse/__init__.py` and `tests/test_legacy.py` before any edit; the approval menu; `compat.py` deleted and the suite passing in step 3; the shape of the git output. Long passages are shortened with `…`.

## 1. Direct: the $75 rule

```text
$ git status --short
$ claude
 Claude Code v2.1.301
 Haiku 5.5 · Claude Max
 ~/projects/harborline
 ⏵⏵ auto mode on (shift+tab to cycle)
```

After the prompt:

```text
  Searched for 2 patterns, listed 1 directory (ctrl+o to expand)

● Both quote and shipping_quote point at the same function, so one fix covers both.

● Update(legacy/warehouse/shipping.py)
  ⎿  Added 2 lines, removed 3 lines
     10 -    Note: the old system used '>' here, so an order of exactly $75.00
     11 -    was charged shipping. The web store uses '>='.
     10 +    Free shipping starts at $75.00 (data/refund_policy.md).
     13 -    if zone == "domestic" and subtotal > FREE_SHIPPING_OVER:
     12 +    if zone == "domestic" and subtotal >= FREE_SHIPPING_OVER:

● Update(tests/test_legacy.py)
  ⎿  Added 2 lines, removed 1 line
     24 -    assert shipping.quote(75.00) == 6.95  # the old system's '>' rule
     24 +    assert shipping.quote(75.00) == 0.0  # $75.00 exactly ships free
     25 +    assert shipping.quote(74.99) == 6.95

● Bash(.venv/bin/python -m pytest -q tests/test_legacy.py)
  ⎿  3 passed in 0.04s
  ⎿  Allowed by auto mode classifier
  ⎿  Loaded .claude/rules/testing.md

● The rules say to run the whole suite after the single file. The test name test_the_old_shipping_rule also no longer describes the behavior, so I'll rename it.

● Update(tests/test_legacy.py)
     22 -def test_the_old_shipping_rule():
     22 +def test_free_shipping_starts_at_75_dollars():

● Bash(.venv/bin/python -m pytest -q tests/test_legacy.py && .venv/bin/python -m pytest -q)
…
● Fixed. Free shipping now starts at $75.00, matching data/refund_policy.md.

  - legacy/warehouse/shipping.py: changed > to >= and removed the old-system note from the docstring.
  - tests/test_legacy.py: shipping.quote(75.00) now expects 0.0, and I added a check that 74.99 still pays $6.95. I renamed the test to test_free_shipping_starts_at_75_dollars.

  tests/test_legacy.py passes (3 passed). The full suite also passes (118 passed).

✻ Baked for 26s
```

```text
$ git diff --stat
 legacy/warehouse/shipping.py | 5 ++---
 tests/test_legacy.py         | 5 +++--
 2 files changed, 5 insertions(+), 5 deletions(-)
$ git commit -am 'Lesson 5.5: free shipping from $75.00 (>=), as the refund policy says'
[main 764115e] Lesson 5.5: free shipping from $75.00 (>=), as the refund policy says
 2 files changed, 5 insertions(+), 5 deletions(-)
```

## 2. Plan: retire the shim

Three presses of Shift+Tab: `manual mode on`, `accept edits on`, `⏸ plan mode on`. After the prompt:

```text
● Explore(Find compat.py dependents)
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

● The Explore agent is searching for dependents of legacy/warehouse/compat.py. I'll draft the retirement plan once its results arrive.

✻ Waiting for 1 background agent to finish
…
  ● main
  ○ Explore  Find compat.py dependents                    15s · ↓ 22.4k tokens
…
● Agent "Find compat.py dependents" finished · 23s

● Updated plan
  ⎿  /plan to preview
```

The plan (the kit's `the-plan.md`) ends with its Verification section, then:

```text
 Claude has written up a plan and is ready to execute. Would you like to proceed?

 ❯ 1. Yes, and use auto mode
   2. Yes, manually approve edits
   3. Tell Claude what to change
      shift+tab to approve with this feedback

 ctrl+g to edit in VS Code · ~/.claude/plans/<generated-name>.md
```

## 3. Approve, run, share

After **1**:

```text
● Plan approved. Making the edits now, starting with the package re-export and the test.

● Update(legacy/warehouse/__init__.py)
  ⎿  Removed 1 line
      8 -from legacy.warehouse.compat import getStatus, get_status_text

● Update(legacy/warehouse/__init__.py)
  ⎿  Removed 2 lines
     14 -    "getStatus",
     15 -    "get_status_text",

● Update(tests/test_legacy.py)
  ⎿  Added 3 lines, removed 3 lines
      7 -def test_status_codes_and_old_names():
      7 +def test_status_codes_have_names():
      8 +    assert codes.status_name(3) == "shipped"
     10 -    assert warehouse.getStatus(3) == "shipped"
     11 -    assert warehouse.get_status_text("9") == "CANCELLED"
     11 +    assert codes.status_name(9).upper() == "CANCELLED"

● Bash(rm legacy/warehouse/compat.py && .venv/bin/python -m pytest -q tests/test_legacy.py)
  ⎿  3 passed in 0.01s
…
  ⎿  118 passed in 1.78s
…
  Changes (not committed):
  - Deleted legacy/warehouse/compat.py.
  - legacy/warehouse/__init__.py: removed the compat import and the two __all__ entries.
  - tests/test_legacy.py: the compat assertions now call codes.status_name directly. I renamed the test to test_status_codes_have_names because "old_names" no longer described it.

  experiments/m4/decompose.py doesn't reference compat, so it needed no change.

  Want me to commit with a one-line message, e.g. "Remove legacy warehouse compat shim"?

✻ Brewed for 2m 37s
```

```text
$ git status --short
 M legacy/warehouse/__init__.py
 D legacy/warehouse/compat.py
 M tests/test_legacy.py
$ git add -A legacy tests
$ git commit -m "Lesson 5.5: retire legacy/warehouse/compat.py after a plan"
[main 3e0ebe2] Lesson 5.5: retire legacy/warehouse/compat.py after a plan
 3 files changed, 3 insertions(+), 17 deletions(-)
 delete mode 100644 legacy/warehouse/compat.py
$ git push
…
To https://github.com/YOUR-USERNAME/harborline.git
   bac276b..3e0ebe2  main -> main
```
