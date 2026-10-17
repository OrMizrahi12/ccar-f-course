# Student kit: Lesson 7.2, Schemas that don't invite fabrication

Claude Certified Architect – Foundations (CCAR-F) · Module 7: Structured Data Extraction · Lesson 7.2

This kit holds everything you need to repeat the lesson on your own computer: every command in order, the files the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Let the schema say "not stated"
2. Give "other" and "unclear" a place to go
3. Put the format rules next to the schema

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/extraction/schema.py` | The record as Pydantic models, as the lesson ends it: nullable fields, `unclear`, `doc_type_detail` |
| `harborline/extraction/extract.py` | `extract.py` as the lesson ends it: tools built from the models with `transform_schema()`, and `RULES` sent before the document |
| `harborline/requirements.txt` | The pinned packages, with `pydantic==2.14.1` added |

You type the code yourself, as in the lesson, or paste it from the kit. Step 1's first version of `schema.py` is printed below, so you can see the "before" for yourself.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The code and the steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 7.1 done**: your own `harborline` repository in `~/projects/harborline`, with its `.venv` (the `anthropic` and `python-dotenv` packages; `pydantic` comes with `anthropic`), `extraction/extract.py` from Lesson 7.1, and `origin` pointing at your own private `harborline` repository.
- **Your Anthropic API key in `.env`** (Lesson 0.4). `.env` is in `.gitignore`, so it is never committed.
- The model in `harborline/config.py` is `claude-haiku-5-5`. **Keep it for this lesson**: the calls force a tool, which works on Haiku 5.5 and returns an error on some newer models (Lesson 7.1).
- About 35 minutes. **This lesson makes API calls**: nine runs, two calls each (D10 stops after one). The whole lesson costs under a cent.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### 1. Every field required

```bash
git status --short
code requirements.txt
```

Add `pydantic==2.14.1` at the end and save. It's already installed with the `anthropic` package; now the version is pinned. Then:

```bash
code extraction/schema.py
```

Type the first version, where every field is required and none can be null:

```python
"""What we keep from each supplier document."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Metadata(Strict):
    doc_type: Literal["invoice", "credit_note", "other"]
    supplier_name: str


class LineItem(Strict):
    description: str
    quantity: float
    unit: str
    unit_price: float
    amount: float


class Document(Strict):
    supplier_name: str
    invoice_number: str
    invoice_date: str
    due_date: str
    payment_terms: str
    po_number: str
    currency: str
    line_items: list[LineItem]
    subtotal: float
    tax: float
    shipping: float
    stated_total: float
```

Save, then `code extraction/extract.py`. The hand-written schemas from Lesson 7.1 go (`ITEM`, `record_tool()`, the `EXTRACT_METADATA` dictionary, `RECORDERS`). In their place:

- **`from anthropic import transform_schema`** and **`from extraction import schema`**.
- **`tool(name, description, model)`**: a strict tool whose `input_schema` is `transform_schema(model)`, the SDK's conversion of a Pydantic model to a schema that strict tool use accepts.
- **`EXTRACT_METADATA`** from `schema.Metadata`, and **one `RECORD_DOCUMENT`** from `schema.Document`, for invoices and credit notes alike.
- **`call(client, text, tool)`**: one forced call to that tool; returns its input.
- **`extract()`**: metadata first; anything that isn't an invoice or a credit note is `skipped`; otherwise `meta | call(..., RECORD_DOCUMENT)`.

Save, then look at two documents and run them:

```bash
clear
cat data/invoices/dev/INV-D06.txt
clear
python -m extraction.extract data/invoices/dev/INV-D06.txt
clear
cat data/invoices/dev/INV-D11.txt
clear
python -m extraction.extract data/invoices/dev/INV-D11.txt
```

- **D06** (Brightwater Paper Co., a letter): it states no purchase order and no due date, only terms of Net 45. In the lesson, `"due_date"` and `"po_number"` both came back as `"<UNKNOWN>"`: placeholders, written because the fields are required.
- **D11** (Harrow Valley Ceramics, a scanned copy): `TOTAL DUE CAD [illegible]`. In the lesson, `"stated_total"` came back as `-1`, a number the document doesn't contain, and the purchase order as `"<UNKNOWN>"` again. Its due date (2026-10-17) is right: the document states it.

### 2. Nullable, other and unclear

```bash
code extraction/schema.py
```

Four changes (the kit's `schema.py` is the result):

- The docstring adds: `A field the document doesn't state is None: never a guess.`
- `doc_type` gains `"unclear"`.
- `doc_type_detail: str | None = Field(description="What the document is, only when doc_type is other or unclear")` (import `Field`).
- `| None` on every field a document may lack: `invoice_number`, `invoice_date`, `due_date`, `payment_terms`, `po_number`, `currency`, `subtotal`, `tax`, `shipping`, `stated_total`. The supplier and the lines stay required.

Save, then run four documents: `INV-D06`, `INV-D11`, `INV-D10` and `INV-D01` (see `commands.txt`).

- **D06**: `"due_date": null`, `"po_number": null`; `"tax": null` where the letter charges none.
- **D11**: `"stated_total": null` (not -1), `"shipping": null`, `"po_number": null`; the stated due date is still there.
- **D10** (Quayside Electronics Wholesale): `skipped`, `"doc_type": "other"`, `"doc_type_detail": "Pro-forma invoice (approval only, no payment due)"`.
- **D01** (Kestrel Outdoor Supply): `"tax": null`, `"shipping": null`. The dates came back as `2026-06-18` and `2026-07-18`, right, but by luck: nothing tells the model which format to use yet.

### 3. Rules next to the schema

```bash
code extraction/extract.py
```

Add `RULES` under the tools (the kit's `extract.py` has it) and send it before the document: `f"{RULES}\n<document>\n{text}\n</document>"`. The rules: null when the document doesn't state a value, never computed, inferred or guessed; tax and shipping 0 when none is shown; dates as `YYYY-MM-DD`, US suppliers month first and everyone else day first, with an example of each; amounts as plain numbers (`"1.234,56"` and `"1,234.56"` are both 1234.56); currency as its ISO 4217 code. Save, then:

```bash
clear
python -m extraction.extract data/invoices/dev/INV-D01.txt
clear
cat data/invoices/dev/INV-D03.txt
clear
python -m extraction.extract data/invoices/dev/INV-D03.txt
```

- **D01**: `"tax": 0`, `"shipping": 0`, the dates `YYYY-MM-DD`, by rule this time.
- **D03** (Lumen Kitchenware GmbH, Germany: `Date: 02.08.2026`, `Due: 16.09.2026`, decimal commas, EUR): `"invoice_date": "2026-08-02"`, `"due_date": "2026-09-16"`, amounts as plain numbers (16.72 … 885.81), `"currency": "EUR"`. Right in the lesson's run; in practice runs the same date once came back as February 8. A rule helps, but it isn't a guarantee.

### Commit and push

```bash
clear
git status --short
git add requirements.txt extraction
git commit -m "Lesson 7.2: Pydantic schema with nullable fields, unclear and other, normalization rules"
git push
```

Three files changed, 67 insertions, 61 deletions.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Show a document | `cat data/invoices/dev/INV-D06.txt` | PowerShell: `Get-Content data\invoices\dev\INV-D06.txt` |
| Run the extraction | `python -m extraction.extract data/invoices/dev/INV-D06.txt` | the same (forward slashes work in Python) |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save).

## What the lesson showed

| Run | Result in the lesson |
|---|---|
| Step 1, `INV-D06` | `"due_date": "<UNKNOWN>"`, `"po_number": "<UNKNOWN>"`; terms `Net 45` |
| Step 1, `INV-D11` | `"stated_total": -1`, `"po_number": "<UNKNOWN>"`; due 2026-10-17 (stated) |
| Step 2, `INV-D06` / `D11` | the same fields `null`; D06 `"tax": null`; D11 `"shipping": null` |
| Step 2, `INV-D10` | `skipped`, `other`, `"Pro-forma invoice (approval only, no payment due)"` |
| Step 2, `INV-D01` | `"tax": null`, `"shipping": null`; dates ISO (by luck) |
| Step 3, `INV-D01` | `"tax": 0`, `"shipping": 0`; dates ISO |
| Step 3, `INV-D03` | `2026-08-02`, `2026-09-16`, `EUR`, amounts as plain numbers |
| The commit | `fbbb403`, 3 files changed, 67 insertions, 61 deletions |

See `expected-output.md` for the full outputs. Model output changes from run to run: compare the behavior, not the exact values.

## Troubleshooting

- **`ImportError: cannot import name 'transform_schema' from 'anthropic'`**: your `anthropic` package is older than the one in `requirements.txt`. Run `pip install -r requirements.txt` with `.venv` active.
- **`ModuleNotFoundError: No module named 'extraction'`**: run from the `harborline` folder with `python -m extraction.extract ...`.
- **A 400 error about the schema**: a model without `extra="forbid"` produces a schema strict tool use rejects (objects need `additionalProperties: false`). Check `Strict` and that every model inherits from it.
- **A 400 error about forced tool use**: your `harborline/config.py` names a model that rejects forced tool choice. Set it back to `claude-haiku-5-5`.
- **Step 1 doesn't invent anything on your run**: model output varies. Try `INV-D04` or `INV-D12`, which also lack a purchase order.
- **`doc_type_detail` filled on ordinary invoices**: check its `Field(description=...)`: "only when doc_type is other or unclear".
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Fabrication:** a value the document doesn't contain, made up to fill a required field.
- **Nullable field:** `str | None`; null means "the document doesn't say".
- **`other` + detail:** an enum's escape hatch, with a field that says what the document really is.
- **`unclear`:** the honest answer when the type can't be told.
- **Normalization rule:** one canonical format for dates, amounts and codes, stated in the prompt.

## Sources (checked 2026-10-17)

- Reduce hallucinations: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- Structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Claude Certified Architect – Foundations Exam Guide: Task Statement 4.3, Scenario 6

Models and the API change. If an option, a field or a message doesn't match what you see, follow the official pages.
