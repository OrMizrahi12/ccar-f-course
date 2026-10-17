# Expected output: Lesson 7.2, Schemas that don't invite fabrication

What each step showed in the lesson (Haiku 5.5 on the API, Python 3.12, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. The documents are the same for everyone (they ship in `data/invoices/`); what Claude reads from them can vary from run to run, so compare the behavior, not every value. Long outputs are shortened here with `...` where nothing changes between steps.

## Step 1: every field required

`git status --short` prints nothing (the tree is clean, at the Lesson 7.1 commit). Editing `requirements.txt`, `schema.py` and `extract.py` prints nothing.

`cat data/invoices/dev/INV-D06.txt` shows a letter from Brightwater Paper Co.: invoice BWP-12132, dated August 3, 2026, packing tape and thermal labels (eight rolls each), carriage $18.00, a total of $112.88, "payable on our usual terms (Net 45)". No purchase order, no due date.

```text
$ python -m extraction.extract data/invoices/dev/INV-D06.txt
record_document {
  "doc_type": "invoice",
  "supplier_name": "Brightwater Paper Co.",
  "invoice_number": "BWP-12132",
  "invoice_date": "2026-08-03",
  "due_date": "<UNKNOWN>",
  "payment_terms": "Net 45",
  "po_number": "<UNKNOWN>",
  "currency": "USD",
  "line_items": [
    {"description": "Packing tape roll", "quantity": 8, "unit": "roll", "unit_price": 2.15, "amount": 17.2},
    {"description": "Thermal shipping labels (roll)", "quantity": 8, "unit": "roll", "unit_price": 9.71, "amount": 77.68}
  ],
  "subtotal": 94.88,
  "tax": 0,
  "shipping": 18.0,
  "stated_total": 112.88
}
```

(The terminal prints each line item over several lines; they're folded here.) Two placeholders, because the fields are required strings. On your run the placeholder may read differently, or a due date may be computed from the terms: either way, a value the letter doesn't contain.

`cat data/invoices/dev/INV-D11.txt` shows a scanned copy from Harrow Valley Ceramics: `No. HVC-97012`, `Date 2026-09-17`, `Terms Net 30 / due 2026-10-17`, two lines, `Sub-total 399.72`, `HST 13% 51.96`, and `TOTAL DUE CAD [illegible]`.

```text
$ python -m extraction.extract data/invoices/dev/INV-D11.txt
record_document {
  "doc_type": "invoice",
  "supplier_name": "Harrow Valley Ceramics",
  "invoice_number": "HVC-97012",
  "invoice_date": "2026-09-17",
  "due_date": "2026-10-17",
  "payment_terms": "Net 30",
  "po_number": "<UNKNOWN>",
  "currency": "CAD",
  "line_items": [ ... Stoneware vase 24 x 13.02 = 312.48, Serving platter 6 x 14.54 = 87.24 ... ],
  "subtotal": 399.72,
  "tax": 51.96,
  "shipping": 0,
  "stated_total": -1
}
```

`-1` is a number the document doesn't contain, written into a field that had to be a number. (In practice runs, the subtotal was copied into it instead.) The due date is right: the document states it.

## Step 2: nullable, other and unclear

```text
$ python -m extraction.extract data/invoices/dev/INV-D06.txt
record_document {
  "doc_type": "invoice",
  "doc_type_detail": null,
  "supplier_name": "Brightwater Paper Co.",
  "invoice_number": "BWP-12132",
  "invoice_date": "2026-08-03",
  "due_date": null,
  "payment_terms": "Net 45",
  "po_number": null,
  "currency": "USD",
  ...
  "subtotal": 94.88,
  "tax": null,
  "shipping": 18.0,
  "stated_total": 112.88
}
```

```text
$ python -m extraction.extract data/invoices/dev/INV-D11.txt
record_document {
  ...
  "due_date": "2026-10-17",
  "payment_terms": "Net 30",
  "po_number": null,
  ...
  "tax": 51.96,
  "shipping": null,
  "stated_total": null
}
```

```text
$ python -m extraction.extract data/invoices/dev/INV-D10.txt
skipped {
  "doc_type": "other",
  "doc_type_detail": "Pro-forma invoice (approval only, no payment due)",
  "supplier_name": "Quayside Electronics Wholesale"
}
```

```text
$ python -m extraction.extract data/invoices/dev/INV-D01.txt
record_document {
  "doc_type": "invoice",
  "doc_type_detail": null,
  "supplier_name": "Kestrel Outdoor Supply",
  "invoice_number": "KOS-50960",
  "invoice_date": "2026-06-18",
  "due_date": "2026-07-18",
  "payment_terms": "Net 30",
  "po_number": "PO-26-0559",
  "currency": "USD",
  "line_items": [ ... Two-Person Tent 20 x 96.0 = 1920.0, Tent Footprint 24 x 10.29 = 246.96 ... ],
  "subtotal": 2166.96,
  "tax": null,
  "shipping": null,
  "stated_total": 2166.96
}
```

Nothing invented anymore. Tax and shipping are `null` where the documents simply show none. D01's dates came back as `YYYY-MM-DD` in the lesson, but nothing asks for that format yet: in practice runs they came back as printed (`06/18/2026`).

## Step 3: rules next to the schema

```text
$ python -m extraction.extract data/invoices/dev/INV-D01.txt
record_document {
  ...
  "invoice_date": "2026-06-18",
  "due_date": "2026-07-18",
  ...
  "tax": 0,
  "shipping": 0,
  "stated_total": 2166.96
}
```

`cat data/invoices/dev/INV-D03.txt` shows Lumen Kitchenware GmbH: `Date: 02.08.2026`, `Invoice No: LK-51957`, `Your PO: PO-26-0526`, `Terms: Net 45`, `Due: 16.09.2026`, amounts with decimal commas (`16,72` ... `885,81`), `TOTAL DUE (EUR)`.

```text
$ python -m extraction.extract data/invoices/dev/INV-D03.txt
record_document {
  "doc_type": "invoice",
  "doc_type_detail": null,
  ...
  "invoice_number": "LK-51957",
  "invoice_date": "2026-08-02",
  "due_date": "2026-09-16",
  "payment_terms": "Net 45",
  "po_number": "PO-26-0526",
  "currency": "EUR",
  "line_items": [ ... Pour-over kettle 4 x 16.72 = 66.88, Mixing bowl set 10 x 14.15 = 141.5,
                  Espresso machine, dual boiler 2 x 268.0 = 536.0 ... ],
  "subtotal": 744.38,
  "tax": 141.43,
  "shipping": 0,
  "stated_total": 885.81
}
```

Day-first dates read right, and decimal commas became plain numbers. In practice runs the same date once came back as `2026-02-08`: a rule helps, but it isn't a guarantee. Lesson 7.4 measures a whole dev set.

## Commit and push

```text
$ git status --short
 M extraction/extract.py
 M requirements.txt
?? extraction/schema.py
$ git add requirements.txt extraction
$ git commit -m "Lesson 7.2: Pydantic schema with nullable fields, unclear and other, normalization rules"
[main fbbb403] Lesson 7.2: Pydantic schema with nullable fields, unclear and other, normalization rules
 3 files changed, 67 insertions(+), 61 deletions(-)
 create mode 100644 extraction/schema.py
```

`git push` ends with `main -> main`. Your hashes will differ.
