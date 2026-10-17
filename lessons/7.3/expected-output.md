# Expected output: Lesson 7.3, Validate, retry, self-correct

What each step showed in the lesson (Haiku 5.5 on the API, Python 3.12, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. The documents are the same for everyone (they ship in `data/invoices/`); what Claude reads from them can vary from run to run, so compare the behavior, not every value.

## Step 1: checks and a retry

`git status --short` prints nothing (the tree is clean). The two edits to `extract.py` and the new `validate.py` produce no output until you run them.

## Step 2: fixed, capped, hopeless

`INV-D08` is an email from Cedar & Pine Home Goods. Its first line is `1 gross x Velvet throw pillow @ 6.84 = 984.96` (a gross is 144).

```text
$ python -m extraction.validate data/invoices/dev/INV-D08.txt
attempt 1: failed
- record: line 1: quantity 1 x unit price 6.84 is 6.84, but the amount 984.96 is 144 x 6.84
attempt 2: passed
  144 gross Velvet throw pillow @ 6.84 = 984.96
  10 each Weighted blanket @ 49.4 = 494
  12 each Round wall mirror @ 55 = 660
{
  "invoice_number": "CPH-56942",
  "stated_total": 2245.91,
  "calculated_total": 2245.91,
  "conflict_detected": false,
  "status": "ok"
}
```

The retry carried the document, the failed output and the error with its evidence, and the quantity came back as 144. The unit still says `gross`, which isn't right either: units are Lesson 7.4's job. On your run, attempt 1 may pass outright, or need a second retry.

`INV-D07` is the Ironleaf Tools invoice from Lesson 7.1 (`LED desk lamp  1 gross  19.70  2,836.80`).

```text
$ python -m extraction.validate data/invoices/dev/INV-D07.txt
attempt 1: failed
- record: line 1: quantity 1 x unit price 19.7 is 19.70, but the amount 2836.8 is 144 x 19.7
attempt 2: failed
- record: line 1: quantity 1 x unit price 19.7 is 19.70, but the amount 2836.8 is 144 x 19.7
attempt 3: failed
- record: line 1: quantity 1 x unit price 19.7 is 19.70, but the amount 2836.8 is 144 x 19.7
  1 gross LED desk lamp @ 19.7 = 2836.8
  6  Desk organizer @ 10.26 = 61.56
  24  Garden tool set @ 29.4 = 705.6
{
  "invoice_number": "ILT-51418",
  "stated_total": 3594.96,
  "calculated_total": null,
  "conflict_detected": null,
  "status": "review: still failing after 3 attempts"
}
```

Three attempts, the same reading every time: the model takes the table's Qty column literally. Two lines came back with an empty unit. The cap stops the loop and the record goes to a person: better errors don't guarantee a fix. (`calculated_total` and `conflict_detected` are null because no attempt passed the checks.) On your run D07 may get fixed; the cap is still the design.

`cat data/invoices/dev/INV-D11.txt` shows a scanned copy from Harrow Valley Ceramics: `INVOICE  No. HVC-97012`, two lines (`Stoneware vase  24  13.02  312.48`, `Serving platter  6  14.54  87.24`), `Sub-total 399.72`, `HST 13% 51.96`, and `TOTAL DUE CAD [illegible]`.

```text
$ python -m extraction.validate data/invoices/dev/INV-D11.txt
attempt 1: passed
  24 each Stoneware vase @ 13.02 = 312.48
  6 each Serving platter @ 14.54 = 87.24
{
  "invoice_number": "HVC-97012",
  "stated_total": null,
  "calculated_total": 451.68,
  "conflict_detected": false,
  "status": "review: the document states no total"
}
```

The total isn't in the document, so it stays null and the record goes to review, with no retry. 451.68 is 399.72 + 51.96.

## Step 3: a document that disagrees with itself

`cat data/invoices/batch/INV-0048.txt` shows an Ironleaf Tools invoice, `ILT-58675`: `LED desk lamp  6  19.70  118.20`, `Subtotal 118.20`, `Shipping 12.50`, `TOTAL DUE (USD) 121.70`.

```text
$ python -m extraction.validate data/invoices/batch/INV-0048.txt
attempt 1: passed
  6 each LED desk lamp @ 19.7 = 118.2
{
  "invoice_number": "ILT-58675",
  "stated_total": 121.7,
  "calculated_total": 130.7,
  "conflict_detected": true,
  "status": "review: the document's total disagrees"
}
```

The extraction is right; the document's own total is 9.00 short of its lines plus shipping. That's a finding for a person, not an error to retry. (In rehearsal the unit once came back as `<UNKNOWN>`: Lesson 7.2's `unit` is a required string with no rule. Lesson 7.4's examples fix units.)

## Commit and push

```text
$ git status --short
 M extraction/extract.py
?? extraction/validate.py
$ git add extraction
$ git commit -m "Lesson 7.3: validation with Pydantic, retries with the exact errors, calculated and stated totals"
[main eaa5585] Lesson 7.3: validation with Pydantic, retries with the exact errors, calculated and stated totals
 2 files changed, 91 insertions(+), 2 deletions(-)
 create mode 100644 extraction/validate.py
```

`git push` ends with `main -> main`. Your hashes will differ.
