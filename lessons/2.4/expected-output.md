# Expected output: Lesson 2.4, Structured error responses

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12.3, from the `harborline` folder with `.venv` active. Every run is on Claude Haiku 5.5 (`claude-haiku-5-5`). The terminal wrapped long lines; they're shown unwrapped here.

**Your runs will differ from these.** Claude doesn't answer the same way every time: a row can read 2/3 where the lesson's read 3/3, a reply can be worded differently, and costs change with every call. Each section says what should match.

## Step 1: Name the failure

```text
(.venv) $ git status --short
(.venv) $ code harborline/errors.py
(.venv) $ code loop/tools.py
(.venv) $ code harborline/tool_errors.py
(.venv) $ code loop/tools.py
(.venv) $ clear; pytest -q
......................................................                   [100%]
54 passed in 0.75s
```

`git status --short` prints nothing: the tree is clean after Lesson 2.3. Saving prints nothing. What should match: `54 passed`. Your time will differ.

## Step 2: Same requests, three error replies

```text
(.venv) $ code experiments/m2/error_replies.py
(.venv) $ clear; python -m experiments.m2.error_replies
                 generic    sentence  structured
transient            3/3         3/3         3/3
not found            3/3         3/3         3/3
business             3/3         3/3         3/3
permission           0/3         3/3         2/3
empty                3/3         3/3         3/3
right                 12          15          14
sent again             2           0           0

business, the last reply (try 1):
  generic    I couldn't process the refund for the ou [...]
  sentence   I'm sorry the cushion covers weren't wha [...]
  structured I can't refund the outdoor cushion cover [...]
```

Nothing prints for about a minute while the 45 conversations run; then the whole table prints at once.

How to read it:

| Part | What it means |
|---|---|
| `generic` / `sentence` / `structured` | How a failed tool went back to Claude: always `Operation failed.`; the backend's own sentence; the JSON body from `tool_error()` |
| A case row, e.g. `permission  0/3  3/3  2/3` | Tries out of three that were right, per style. Right means nothing was sent again, and one of the case's words (written before the first run) shows up in the last reply or in the tools Claude used |
| `right` | Right tries across the five cases, out of 15 per style |
| `sent again` | Calls Claude sent again, same tool and same order, after an error a retry can't fix |
| `business, the last reply (try 1)` | The first 40 characters of how each style's first business try ended: how Claude tells a customer no |

What should match: most cases are 3/3 in every style, and `sent again` stays 0 for `sentence` and `structured`. What may differ: the permission row and the generic column. In the lesson, the generic string made Claude send the refund again after the account hold refused it (`sent again` 2); in the runs before filming it happened in every run, two or three times. If your generic column scores 3/3 on permission, you've seen Claude cope on its own: the rows that matter are the ones where it has to guess. The lesson's run made 131 calls for $0.0358, logged in `runs/usage.jsonl` with the labels `2.4 errors generic`, `2.4 errors sentence` and `2.4 errors structured`.

## Step 3: Retry, explain, or an empty answer

```text
(.venv) $ code harborline/backend.py
(.venv) $ clear; python -c "from harborline.backend import list_orders; print(list_orders('C-1058'))"
[]
```

What should match: exactly `[]`. It's the data, not Claude: no API call.

```text
(.venv) $ clear; python -m loop.agent T-040
turn 1: tool_use
  [tool_use] get_customer {'email': 'samir.ferreira@example.com'}
  [tool_result] {"verified": true, "customer": {"customer_id": "C-1010", "na
turn 2: tool_use
  [text] Verified the account. Now I'm looking up your recent orders to find the skillet.
  [tool_use] list_orders {'customer_id': 'C-1010'}
  [tool_result] [{"order_id": "HL-10211", "placed_on": "2026-10-14", "items"
turn 3: tool_use
  [tool_use] lookup_order {'order_id': 'HL-10211'}
  [tool_result is_error] {"errorCategory": "transient", "isRetryable": true, "message
turn 4: tool_use
  [tool_use] lookup_order {'order_id': 'HL-10211'}
  [tool_result] {"order_id": "HL-10211", "customer_id": "C-1010", "source":
turn 5: end_turn
  [thinking]
  [text] Your Cast Iron Skillet 12in is on order HL-10211, placed October 14. It's still processing and hasn't shipped yet, so there's no tracking number. The promised delivery date is October 19, 2026.

History:
  user      text
  assistant tool_use
  user      tool_result
  assistant text, tool_use
  user      tool_result
  assistant tool_use
  user      tool_result
  assistant tool_use
  user      tool_result
  assistant thinking, text
```

The agent cuts each `tool_result` to its first characters, so the error's `message` is cut off; in full it's "The warehouse system timed out. Try again in a moment." What should match: the first `lookup_order` on HL-10211 comes back as `[tool_result is_error]` with `"errorCategory": "transient"` and `"isRetryable": true` (the timeout fires on the first lookup of that order in each run). What may differ: the order of the first calls, the wording, and what Claude does next. In the lesson it sent the same lookup again and answered; Claude may also explain the delay instead. Five calls, about a sixth of a cent, labelled `lab 1 agent`. The order's dates come from Harborline's fictional data, so they match.

## Step 4: Commit

```text
(.venv) $ clear; git status --short
 M loop/tools.py
?? experiments/m2/error_replies.py
?? harborline/tool_errors.py
(.venv) $ git add harborline/tool_errors.py loop/tools.py experiments/m2/error_replies.py
(.venv) $ git commit -m "Lesson 2.4: structured tool errors, error replies compared"
[main a71f1e8] Lesson 2.4: structured tool errors, error replies compared
 3 files changed, 137 insertions(+), 2 deletions(-)
 create mode 100644 experiments/m2/error_replies.py
 create mode 100644 harborline/tool_errors.py
(.venv) $ git push
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 24 threads
Compressing objects: 100% (9/9), done.
Writing objects: 100% (9/9), 3.21 KiB | 3.21 MiB/s, done.
Total 9 (delta 4), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
To https://github.com/YOUR-USERNAME/harborline.git
   a68247e..a71f1e8  main -> main
```

What should match: the three files in `git status`, `3 files changed, 137 insertions(+), 2 deletions(-)` if your files match the kit's, and `main -> main`. What will differ: the commit IDs (yours are your own), the object counts and sizes, the thread count, and the URL (your own account).
