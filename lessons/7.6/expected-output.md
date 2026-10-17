# Expected output: Lesson 7.6, Human review and confidence calibration

What each step showed in the lesson (Python 3.12, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. The labels are the same for everyone (they ship in `data/invoices/labels.jsonl`); `runs/batch.jsonl` is your own Lesson 7.5 batch, so your accuracy, your weak slices and your queue can differ. The random samples differ on every run. Compare the behavior, not every value.

## Step 1: measure by slice

```text
$ git status --short
$ wc -l runs/batch.jsonl
100 runs/batch.jsonl
```

`git status --short` prints nothing (the tree is clean, at the Lesson 7.5 commit). Typing and saving `review.py` prints nothing.

## Step 2: route by confidence

```text
$ python -m extraction.review
overall 98.8% of 3198 values
  email  100.0%
  prose  100.0%
  scan   97.2%
  table  98.4%
  supplier_name  61.7%
  invoice_date   98.9%
  due_date       98.9%
below target: due_date in scan 91%; supplier_name in scan 45%; supplier_name in table 14%
 42  low confidence
  2  random sample of email
  2  random sample of prose
  9  review
43 records trusted; 0 wrong values among them: the samples estimate this
```

- **98.8% of 3198 values**: the two long invoices from Lesson 7.5 add 1,200 line values, all right, and they lift the average. One field is right only 61.7% of the time.
- **By field** lists only the fields that weren't always right.
- **`supplier_name` in scans and tables**: the letterhead prints the company's name in capitals and the record keeps them; the labels write the name the way the company does. For Harborline that's a wrong value: a lookup by exact name finds no supplier.
- **`due_date in scan 91%`** is one wrong value in eleven: a small slice, so a weak estimate.
- **The queue**: 42 records go to a person for low confidence (every scan and table invoice the batch didn't already flag, for `supplier_name`, and the scans' due dates), 9 because the batch flagged them (8 totals that disagree, 1 with no total), and 4 random samples of trusted records. No scan or table record is trusted, so the samples come from email and prose.
- **0 wrong values among the 43 trusted records** this month. The script can count that only because every document is labeled. Next month's documents won't be, and the random samples are what estimates that number then.

## Step 3: sample what you trust

```text
$ head -5 runs/review_queue.jsonl
{"doc_id": "INV-0008", "why": "low confidence: supplier_name"}
{"doc_id": "INV-0016", "why": "low confidence: supplier_name"}
{"doc_id": "INV-0017", "why": "low confidence: supplier_name"}
{"doc_id": "INV-0018", "why": "low confidence: supplier_name"}
{"doc_id": "INV-0019", "why": "review: the document states no total"}
$ grep sample runs/review_queue.jsonl
{"doc_id": "INV-0098", "why": "random sample of email"}
{"doc_id": "INV-0092", "why": "random sample of email"}
{"doc_id": "INV-0097", "why": "random sample of prose"}
{"doc_id": "INV-0070", "why": "random sample of prose"}
```

```text
$ python -m extraction.review | tail -6
below target: due_date in scan 91%; supplier_name in scan 45%; supplier_name in table 14%
 42  low confidence
  2  random sample of email
  2  random sample of prose
  9  review
43 records trusted; 0 wrong values among them: the samples estimate this
$ grep sample runs/review_queue.jsonl
{"doc_id": "INV-0092", "why": "random sample of email"}
{"doc_id": "INV-0064", "why": "random sample of email"}
{"doc_id": "INV-0024", "why": "random sample of prose"}
{"doc_id": "INV-0050", "why": "random sample of prose"}
```

The counts are the same on the second run; the samples are not. Yours will be different again.

## Commit and push

```text
$ git status --short
?? extraction/review.py
$ git add extraction
$ git commit -m "Lesson 7.6: accuracy by layout and field, routing by measured confidence, random samples"
[main 266527d] Lesson 7.6: accuracy by layout and field, routing by measured confidence, random samples
 1 file changed, 85 insertions(+)
 create mode 100644 extraction/review.py
$ git push
...
   4604883..266527d  main -> main
```

Your commit id is different.
