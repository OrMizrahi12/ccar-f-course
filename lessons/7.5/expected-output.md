# Expected output: Lesson 7.5, Batch processing at scale

What each step showed in the lesson (Haiku 5.5 on the API, Python 3.12, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. The documents are the same for everyone (they ship in `data/invoices/batch`); batch ids, batch times and what Claude reads from the documents vary from run to run, so compare the behavior, not every value.

## Step 1: one request, two ways

`git status --short` prints nothing (the tree is clean, at the Lesson 7.4 commit). Editing `extract.py` and `validate.py` prints nothing.

## Step 2: batch, match, resubmit

Typing and saving `batch.py` prints nothing.

## Step 3: a hundred documents

```text
$ ls data/invoices/batch | wc -l
100
$ python -m extraction.batch data/invoices/batch
batch msgbatch_01YUHGmoPtxqdASr4jF3ncaz: 100 requests
  ended after 7 min: 100 succeeded, 0 errored, 0 expired
batch msgbatch_01XjnNzSe23ETVFp6Df2eAzK: 94 requests
  ended after 4 min: 94 succeeded, 0 errored, 0 expired
INV-0008: max_tokens
INV-0016: max_tokens
batch msgbatch_01WnHFQCtxUwoPkG2E3bZ1qf: 38 requests
  ended after 4 min: 38 succeeded, 0 errored, 0 expired
 85  ok
  1  review: the document states no total
  8  review: the document's total disagrees
  6  skipped
100 documents, $0.0486 at batch prices (half of $0.0972) -> batch.jsonl
```

- Your batch ids are different, and so are the minutes: that run took 7, 4 and 4. Any batch can take up to 24 hours.
- **6 skipped**: six documents in the folder aren't invoices or credit notes, so batch two carries 94.
- **INV-0008 and INV-0016** list about 150 lines each: the reply stops at `max_tokens`, so only those two go out again, in parts of 8 lines (19 parts each, 38 requests).
- **8 review: the document's total disagrees**: the lines don't add up to the total the document states (the labels have the same 8). **1 review: the document states no total**: nothing to check against.
- No record failed the checks in this run, so no check retry went out. On yours, a record may fail them: it goes back with its errors in the same resubmission, and its line reads `INV-....: failed the checks`.
- The cost is the script's estimate from the token usage at batch prices, not an invoice.

```text
$ grep INV-0008 runs/batch.jsonl | python -m json.tool | tail -14
            "unit": "each",
            "unit_price": 19.7,
            "amount": 197.0
        }
    ],
    "subtotal": 37042.82,
    "tax": 0,
    "shipping": 0,
    "stated_total": 37042.82,
    "calculated_total": 37042.82,
    "conflict_detected": false,
    "status": "ok",
    "parts": 19
}
```

The joined record has every line from the 19 parts (150 in all); its calculated total matches the stated total, so no line was lost.

## Commit and push

```text
$ git status --short
 M extraction/extract.py
 M extraction/validate.py
?? extraction/batch.py
$ git add extraction
$ git commit -m "Lesson 7.5: the batch folder through the Message Batches API, resubmitting only what failed"
[main 4604883] Lesson 7.5: the batch folder through the Message Batches API, resubmitting only what failed
 3 files changed, 153 insertions(+), 9 deletions(-)
 create mode 100644 extraction/batch.py
$ git push
...
   cb00838..4604883  main -> main
```

Your commit id and the numbers in `git push` are different. `runs/batch.jsonl` is ignored by git; it stays on disk for Lesson 7.6.
