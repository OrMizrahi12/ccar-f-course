# Lab 7: the extraction pipeline, finished

Claude Certified Architect – Foundations (CCAR-F) · Module 7: Structured Data Extraction · the module checkpoint

In Module 7 you built Harborline's supplier-invoice pipeline. A forced tool turns each document into a record, metadata first. The Pydantic schema lets a field say "not stated", and the format rules sit beside it. Validators check what the schema can't, and a retry sends back the document, the failed output and the exact errors. Few-shot examples cover each layout. The batch folder goes through the Message Batches API, and only the failures go back, each with its fix. `review.py` measures the batch by layout and field, routes weak records to people, and samples the rest.

In this lab you add the four pieces a production pipeline still needs: confidence that Claude reports and you calibrate, a log of which failures a retry actually fixed, the SLA arithmetic and a safe fallback for long documents, and one more example for the weakness the batch measured. You pass when the self-check tests pass and one real run of the batch and the review shows the numbers move.

## What you start from

`starter/` is the `harborline` project exactly as it stands after Lesson 7.6: everything from Modules 1 to 6, and `extraction/` with `schema.py`, `extract.py`, `validate.py`, `dev_check.py`, `batch.py`, `review.py` and `prompts/examples.md`. If your own project is there too, keep working in it. If not, copy `starter/` to `~/projects/harborline`, create the virtual environment, install `requirements.txt`, and add your `.env` with `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6 show how).

`solution/` is a finished version to compare with when you're done. `tests/` holds the self-check.

## What you change

- `extraction/schema.py`: a `Confidence` record, and a `confidence` field on `Document`.
- `extraction/review.py`: `calibrate()`, `weak_fields()`, and the calibration table in the report.
- `extraction/validate.py`: `kinds()` and a `retry_log` on every result.
- `extraction/dev_check.py`: `supplier_name` in `FIELDS`, and a line that counts the retries.
- `extraction/batch.py`: `submit_every()`, and `parts()` that leaves a document without a table whole.
- `extraction/prompts/examples.md`: a sixth example, for names printed in capitals.

## Steps

### 1. Confidence that Claude reports (Lessons 7.2 and 7.6)
Lesson 7.6 measured confidence from the labels. Now let Claude say how sure it is, field by field, and then check whether it's right to be.

In `schema.py`, add a `Confidence` record with four fields, `supplier_name`, `invoice_date`, `due_date` and `stated_total`, each `Literal["high", "low"]`, and give `Document` a `confidence: Confidence` field with a description that says when to answer low: the field is hard to read, ambiguous, or not stated. The tool schema comes from the model through `transform_schema()`, so `record_document` asks for it with no other change.

In `review.py`, add `calibrate(records, labels)`: for every record that has a `confidence`, and every field it rates, collect `(field, right)` pairs under the key `(field, level)`. Then `weak_fields(record, layout_low, calibration)`: a field is weak when Lesson 7.6's table says it's below `TARGET` in this layout, when Claude rated it low, or when Claude rated it at a level that was right less than `TARGET` of the time. Use it for the queue, and print the calibration table: one line per field and rating, with how often it was right.

A rating is only worth routing on after you've measured it. A field Claude rates "high" that's right 60% of the time is a low-confidence field.

### 2. Which failures a retry fixes (Lesson 7.3)
In `validate.py`, add `kinds(error)`: the kind of each failed check (`date format`, `line arithmetic`, or `other`). In `extract_checked()`, keep a log: one entry per failed attempt with its kinds and `resolved: False`; when a later attempt passes, mark the earlier entries resolved. Return it as `retry_log` with every result, including the ones that still fail, and an empty list when nothing failed. A missing total still never gets a retry: the document can't give back what it doesn't contain.

In `dev_check.py`, count the log across the dev set and print one line, for example `retries: line arithmetic fixed x2`. Over many runs, that line tells you which checks are worth a retry and which should go straight to a person.

### 3. The SLA and long documents (Lesson 7.5)
In `batch.py`, add `submit_every(sla_hours, batch_hours=24, margin_hours=4)`: the longest gap between batches that still meets the SLA, so that the wait for the next batch, plus the batch's own worst case, plus a margin, fits. Raise `ValueError` when no gap can work. For Harborline's 36 hours it's 8.

`parts()` assumes a table with a rule above and below its lines. A long letter or email has no such rule, and today `parts()` would crash on it. Make it return the whole text as a single part when it can't find two rules.

### 4. One more example (Lesson 7.4)
Lesson 7.6's report put `supplier_name` far below every other field, in tables and scans: the letterhead prints the name in capitals, and the record copied them. The dev-set check from Lesson 7.4 never compared that field, so it never saw it.

Add `supplier_name` to `FIELDS` in `dev_check.py`. Then add a sixth example to `examples.md`: a letterhead in capitals, the name as the company writes it in a sentence, and a `<why>` that names the wrong answer. Use a supplier that isn't in the data.

### 5. Run it once
```bash
python -m extraction.dev_check
python -m extraction.batch data/invoices/batch
python -m extraction.review
```
The dev check takes about a minute and costs about a cent. The batch takes three batches and several minutes each (most batches end within an hour; any batch can take up to 24) and costs about five cents at batch prices. The review costs nothing.

In our practice run (Claude Haiku 5.5, 2026-10-16):
- The dev check: `12 of 12 documents exact; 0 wrong values`, now with `supplier_name` compared, and `retries: line arithmetic fixed x2` (two documents passed on their second attempt; nothing failed for good).
- The batch: 100 requests ended after 3 minutes, 95 after 5, and the 38 parts of INV-0008 and INV-0016 after 3. Status: 85 ok, 8 totals that disagree, 2 that state no total, 5 skipped. `$0.0541 at batch prices (half of $0.1082)`.
- The review: `overall 99.9% of 3213 values`, and `supplier_name` is gone from the weak fields: no field fell below the target in any layout (Lesson 7.6's run had it at 61.7%). The calibration table showed every "high" rating right 100% of the time, on 90 to 94 records each, and "low" used sparingly: 1 to 5 times per field, with `invoice_date` rated low right 80% of 5. The queue: 10 flagged by the batch, 5 with a field rated low, and 8 random samples, two per layout; 80 records trusted.
- One miss the numbers don't show: INV-0023, a pro-forma invoice the labels call `other`, was recorded as an invoice this time (Lesson 7.5's run skipped it). It still reached a person, because it states no total, but `review.py` compares `doc_type` only for skipped records. Comparing it for every record is a good next step.
- Your numbers will differ a little from run to run; the shape should not.

## Check your work

1. Copy `labs/L7/tests/test_lab7.py` into your project's `tests/`, and run the whole suite:
   ```bash
   .venv/bin/python -m pytest -q
   ```
   Our solution: `147 passed` (the starter's 139 tests plus the lab's 8). On the starter, all eight lab tests fail. It needs no key and costs nothing: a fake model and fake records stand in for Claude. It covers:
   - the `Confidence` record, its high/low ratings, and `confidence` required by the `record_document` tool
   - `calibrate()` and `weak_fields()`: a rating measured against the labels, a low rating, a weak layout
   - the retry log: a failure a retry fixed, failures it didn't, and a missing total that's never retried
   - `submit_every()` for 36 and 48 hours, and an SLA no batch can meet
   - `parts()` on INV-0008 (19 parts, each with the header and the totals) and on a letter with no table
   - the examples: well formed, a name in capitals written the company's way, and `supplier_name` in the dev check
2. Run step 5 once, and compare your numbers with ours.

## Compare with the solution

`solution/` holds one way to do it. Other designs pass too: you might rate confidence as numbers instead of high/low, or log retries per field. The tests check behavior through the functions named above; your wording, your example and your thresholds are yours.
