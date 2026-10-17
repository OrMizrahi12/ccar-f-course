# Expected output: Lesson 7.1, Structured output with tool use

What each step showed in the lesson (Haiku 5.5 on the API, Python 3.12, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. The documents are the same for everyone (they ship in `data/invoices/dev/`); the records Claude fills in can vary from run to run, so compare the behavior, not every value.

## Step 1: one invoice, one tool

`git status --short` prints nothing (the tree is clean). `cat data/invoices/dev/INV-D01.txt` shows an invoice from Kestrel Outdoor Supply: `Invoice No: KOS-50960`, `Date: 06/18/2026`, two lines (`Two-Person Tent  20  96.00  1,920.00`, `Tent Footprint  24  10.29  246.96`), `Subtotal 2,166.96`, `TOTAL DUE (USD) 2,166.96`.

```text
$ python -m extraction.extract data/invoices/dev/INV-D01.txt
record_invoice {
  "supplier_name": "Kestrel Outdoor Supply",
  "invoice_number": "KOS-50960",
  "date": "2026-06-18",
  "currency": "USD",
  "line_items": [
    {
      "description": "Two-Person Tent",
      "quantity": 20,
      "unit_price": 96.0,
      "amount": 1920.0
    },
    {
      "description": "Tent Footprint",
      "quantity": 24,
      "unit_price": 10.29,
      "amount": 246.96
    }
  ],
  "stated_total": 2166.96
}
```

The points to check: the first word is the tool's name, the record has every field of the schema, the date is in `YYYY-MM-DD` even though the document wrote `06/18/2026`, and the numbers are numbers, not text.

## Step 2: two kinds of documents

```text
$ python -m extraction.extract data/invoices/dev/INV-D09.txt
record_credit_note {
  "supplier_name": "Kestrel Outdoor Supply",
  "credit_note_number": "KOS-79465",
  "date": "2026-04-08",
  "currency": "USD",
  "line_items": [
    { "description": "Insulated Water Bottle", "quantity": 40, "unit_price": 10.64, "amount": 425.6 },
    { "description": "Tent Footprint", "quantity": 8, "unit_price": 9.8, "amount": 78.4 },
    { "description": "Lantern Battery Pack", "quantity": 10, "unit_price": 3.89, "amount": 38.9 }
  ],
  "stated_total": 555.4
}
```

(The line items are shown on one line each here; the script prints each field on its own line.) With `{"type": "any"}`, Claude picked the credit-note tool, and its own number field, `credit_note_number`.

`cat data/invoices/dev/INV-D10.txt` shows an email from `invoices@quayside-wholesale.example`: `Subject: Pro-forma invoice QEW-33236 for PO-26-0461`, then "Please see the details of pro-forma invoice QEW-33236 below. This pro-forma is for approval only; no payment is due yet.", three lines and `Total: USD 2,315.60`.

```text
$ python -m extraction.extract data/invoices/dev/INV-D10.txt
record_invoice {
  "supplier_name": "Quayside Electronics Wholesale",
  "invoice_number": "QEW-33236",
  "date": "2026-06-05",
  "currency": "USD",
  "line_items": [
    { "description": "Bluetooth alarm clock", "quantity": 4, "unit_price": 10.4, "amount": 41.6 },
    { "description": "USB-C charging hub", "quantity": 40, "unit_price": 20.9, "amount": 836.0 },
    { "description": "E-reader", "quantity": 20, "unit_price": 71.0, "amount": 1420.0 }
  ],
  "stated_total": 2315.6
}
```

A pro-forma, filed as an invoice to pay. With `any`, a tool call is guaranteed, so a document that is neither kind still becomes one of them.

## Step 3: classify first, strict schemas

```text
$ python -m extraction.extract data/invoices/dev/INV-D10.txt
skipped {
  "doc_type": "other",
  "supplier_name": "Quayside Electronics Wholesale"
}
```

`cat data/invoices/dev/INV-D07.txt` shows an invoice from Ironleaf Tools Inc.: `Invoice No: ILT-51418`, `Date: 9/24/26`, three lines (`LED desk lamp  1 gross  19.70  2,836.80`, `Desk organizer  6  10.26  61.56`, `Garden tool set  24  29.40  705.60`), `Subtotal 3,603.96`, and `TOTAL DUE (USD) 3,594.96`: the document's own subtotal and total are 9.00 apart.

```text
$ python -m extraction.extract data/invoices/dev/INV-D07.txt
record_invoice {
  "supplier_name": "Ironleaf Tools Inc.",
  "invoice_number": "ILT-51418",
  "date": "2026-09-24",
  "currency": "USD",
  "line_items": [
    { "description": "LED desk lamp (1 gross)", "quantity": 1, "unit_price": 19.7, "amount": 2836.8 },
    { "description": "Desk organizer", "quantity": 6, "unit_price": 10.26, "amount": 61.56 },
    { "description": "Garden tool set", "quantity": 24, "unit_price": 29.4, "amount": 705.6 }
  ],
  "stated_total": 3594.96
}
lines add up to 3,603.96; stated total 3,594.96
```

The points to check:

- **Valid, and wrong.** The record matches the schema, but the lamp line says `"quantity": 1` for one gross (144 lamps). On your run the quantity may come back as 144, or the description may differ; a schema can't tell either way.
- **The totals line.** The lines add up to 9.00 more than the stated total, because the document disagrees with itself. This check is naive on purpose (no shipping or discounts); Lesson 7.3 builds a proper one.
- **Strict.** With `"strict": True` and `"additionalProperties": False`, the input is guaranteed to match the schema. In these runs the forced calls on Haiku 5.5 already came back in shape, so nothing changed on screen.

## Commit and push

```text
$ git status --short
?? extraction/
$ git add extraction
$ git commit -m "Lesson 7.1: extraction with a forced tool, metadata first, strict schemas"
[main 9e83444] Lesson 7.1: extraction with a forced tool, metadata first, strict schemas
 2 files changed, 95 insertions(+)
 create mode 100644 extraction/__init__.py
 create mode 100644 extraction/extract.py
```

`git push` ends with `main -> main`. Your hashes will differ.
