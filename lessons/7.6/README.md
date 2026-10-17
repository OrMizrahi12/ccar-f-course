# Student kit: Lesson 7.6, Human review and confidence calibration

Claude Certified Architect – Foundations (CCAR-F) · Module 7: Structured Data Extraction · Lesson 7.6

This kit holds everything you need to repeat the lesson on your own computer: every command in order, the file the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Look past the average
2. Route by measured confidence
3. Keep sampling what you trust

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/extraction/review.py` | The new file: accuracy overall, by layout and by field; the confidence table; the review queue with random samples |

You type the code yourself, as in the lesson, or paste it from the kit.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The code and the steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 7.5 done**: your own `harborline` repository in `~/projects/harborline`, with its `.venv`, the extraction files from Lessons 7.1 to 7.5 (`extraction/dev_check.py` from Lesson 7.4 provides `same()`), and `origin` pointing at your own private `harborline` repository.
- **`runs/batch.jsonl` from Lesson 7.5**: the 100 records your batch wrote. `runs/` is ignored by git, so it is only on the computer that ran the batch. If it's missing, run Lesson 7.5's batch first.
- `data/invoices/labels.jsonl` ships with the repository: the right answers for every document in the folder, and each document's layout.
- About 20 minutes. **This lesson makes no API calls** ($0): it compares files on disk.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### 1. Measure by slice

```bash
git status --short
wc -l runs/batch.jsonl
code extraction/review.py
```

Type `review.py` (the kit's file is the result):

- **The docstring** says what it does: compare `runs/batch.jsonl` with `labels.jsonl`, overall, by layout and by field. A field's accuracy in a layout is its confidence.
- **`FIELDS`**: the eleven fields compared, from `supplier_name` to `stated_total`. **`TARGET = 0.95`**: a field this accurate in its layout is trusted without a person. **`SAMPLE = 2`**: trusted records per layout that a person checks anyway.
- **`compare(record, label)`** pairs every value with its label: each field, the number of lines, and each line's quantity, unit, unit price and amount. A skipped document is checked on its type alone. **`accuracy(pairs)`** is the share that's right.
- **`main()`** reads the labels and the batch. The layout comes from the labels, because this month is labeled; in production it would come from the metadata step or the supplier's record. It prints the overall accuracy, then the same values by layout, by field (only the fields that weren't always right), and by layout and field together: that's the confidence table. Any field below `TARGET` in its layout is printed as `below target`.
- **The queue**: a record the batch flagged (`review: ...`) goes in as it is; a record with a weak field goes in as `low confidence: <fields>`; a record that's `ok` with no weak field is trusted. Then `SAMPLE` trusted records per layout are drawn at random. The queue goes to `runs/review_queue.jsonl`, with a count of each reason. The last line counts the wrong values among the trusted records: it needs the labels, so it's what the random samples estimate when there are none.

Save.

### 2. Route by confidence

```bash
clear
python -m extraction.review
```

### 3. Sample what you trust

```bash
clear
head -5 runs/review_queue.jsonl
grep sample runs/review_queue.jsonl
clear
python -m extraction.review | tail -6
grep sample runs/review_queue.jsonl
```

The second run prints the same counts, and different random samples.

### Commit and push

```bash
clear
git status --short
git add extraction
git commit -m "Lesson 7.6: accuracy by layout and field, routing by measured confidence, random samples"
git push
```

One file changed, 85 insertions. `runs/review_queue.jsonl` is ignored by git; it stays on disk.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Count the records | `wc -l runs/batch.jsonl` | PowerShell: `(Get-Content runs\batch.jsonl).Count` |
| The head of the queue | `head -5 runs/review_queue.jsonl` | PowerShell: `Get-Content runs\review_queue.jsonl -TotalCount 5` |
| The random samples | `grep sample runs/review_queue.jsonl` | PowerShell: `Select-String sample runs\review_queue.jsonl` |
| The last lines of the report | `python -m extraction.review \| tail -6` | PowerShell: `python -m extraction.review \| Select-Object -Last 6` |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save).

## What the lesson showed

| Step | Result in the lesson |
|---|---|
| `wc -l runs/batch.jsonl` | `100 runs/batch.jsonl` |
| Overall | `overall 98.8% of 3198 values` |
| By layout | email 100.0%, prose 100.0%, scan 97.2%, table 98.4% |
| By field (not always right) | `supplier_name` 61.7%, `invoice_date` 98.9%, `due_date` 98.9% |
| Below target | `due_date in scan 91%; supplier_name in scan 45%; supplier_name in table 14%` |
| The queue | 42 `low confidence` · 2 `random sample of email` · 2 `random sample of prose` · 9 `review` |
| Trusted | `43 records trusted; 0 wrong values among them: the samples estimate this` |
| The commit | `266527d`, 1 file changed, 85 insertions |

Why `supplier_name` is weak: in tables and scans the letterhead prints the company's name in capitals, and the record keeps the capitals; the labels write the name the way the company does, so for Harborline it doesn't match. Every scan and table record goes to a person for its name, which is why the random samples come from email and prose. The fix (a normalization rule or a few-shot example for names, measured on the dev set with `supplier_name` added) is the next prompt change, not part of this lesson.

Your numbers depend on your Lesson 7.5 batch: compare the behavior, not the exact values. See `expected-output.md` for the full outputs.

## Troubleshooting

- **`FileNotFoundError: runs/batch.jsonl`**: run Lesson 7.5's batch first (`python -m extraction.batch data/invoices/batch`); `runs/` is not in git.
- **`ImportError: cannot import name 'same'`**: `extraction/dev_check.py` from Lesson 7.4 is missing or different. Check out the Lesson 7.5 commit's version.
- **`KeyError` on a document id**: your `runs/batch.jsonl` has a document that `labels.jsonl` doesn't. Use the 100 documents in `data/invoices/batch`.
- **`below target:` is empty**: your batch did better than the lesson's on every slice. The queue then holds only the flagged records and the random samples.
- **Different samples from the lesson's**: that's the point; they're random on every run.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Labeled set:** documents with the right answers, used to measure the pipeline.
- **Slice:** one layout, one field, or both; where an average hides its failures.
- **Calibrated confidence:** how often a field was right on labeled documents like this one.
- **Routing:** sending a record (or a field) to a person when confidence is low or sources conflict.
- **Stratified sample:** a few random trusted records from every layout, every run.

## Sources (checked 2026-10-17)

- Define success criteria and build evaluations: https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- Claude Certified Architect – Foundations Exam Guide: Task Statement 5.5, Scenario 6

Models and the API change. If an option, a field or a message doesn't match what you see, follow the official pages.
