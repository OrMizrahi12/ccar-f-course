# Student kit: Lesson 7.1, Structured output with tool use

Claude Certified Architect – Foundations (CCAR-F) · Module 7: Structured Data Extraction · Lesson 7.1

This kit holds everything you need to repeat the lesson on your own computer: every command in order, the file the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Make the schema the output
2. Classify first, then extract
3. Know what a schema can't promise

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/extraction/extract.py` | The extractor as the lesson ends it: two strict recorder tools, a forced `extract_metadata` call first, routing by document type, and the totals line |
| `harborline/extraction/__init__.py` | An empty file that makes `extraction` a package |

You type `extract.py` yourself, in three versions, as in the lesson, or paste the final one from the kit. The steps below say what each version changes.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The code and the steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 6.6 done**: your own `harborline` repository in `~/projects/harborline`, with its `.venv` and the `anthropic` and `python-dotenv` packages, and `origin` pointing at your own private `harborline` repository. The supplier documents ship in the repository: `data/invoices/dev/INV-D01.txt` to `INV-D12.txt`.
- **Your Anthropic API key in `.env`** (Lesson 0.4): `ANTHROPIC_API_KEY=...`. `extract.py` loads it with `load_dotenv()`. `.env` is in `.gitignore`, so it is never committed.
- The model in `harborline/config.py` is `claude-haiku-5-5`. **Keep it for this lesson**: forced tool choice works on Haiku 5.5, and returns an error on some newer models (see [Forced tool choice today](#forced-tool-choice-today)).
- About 25 minutes. **This lesson makes API calls**: five runs, seven calls in all, each about 800 to 1,400 input tokens and 70 to 320 output tokens. The whole lesson costs well under a cent.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### 1. One invoice, one tool

```bash
git status --short
clear
cat data/invoices/dev/INV-D01.txt
mkdir extraction && touch extraction/__init__.py
code extraction/extract.py
```

The tree is clean. `INV-D01` is a plain-text invoice from Kestrel Outdoor Supply: a number, a date, two lines and a total due of 2,166.96. In `extract.py` (version 1):

- **`ITEM`**: the schema of one invoice line: `description` (a string), `quantity`, `unit_price` and `amount` (numbers), all four required.
- **`record_tool(name, kind, number)`**: builds one tool per kind of document. Its `input_schema` *is* the record you keep: `supplier_name`, the document's number, `date` (described as `YYYY-MM-DD`), `currency` (an ISO 4217 code), `line_items` (a list of `ITEM`) and `stated_total`. Every field is required.
- **`RECORD_INVOICE`**: that tool for invoices.
- **`call(client, text, tools, choice)`**: one request with the document in `<document>` tags, the tools and a `tool_choice`; it logs the usage, finds the `tool_use` block and returns its `name` and its `input`. Nothing runs the tool: the input is the data.
- **`extract()`**: forces the tool with `{"type": "tool", "name": "record_invoice"}`.
- **At the bottom**: load the key, extract the file given on the command line, and print the tool's name and the record as JSON.

Save, then:

```bash
clear
python -m extraction.extract data/invoices/dev/INV-D01.txt
```

`record_invoice` and a record that matches the document: supplier, number, the date as `2026-06-18`, `USD`, both lines, and `"stated_total": 2166.96`.

### 2. Two kinds of documents

```bash
code extraction/extract.py
```

Version 2, from the bottom up:

- `extract()` now passes a list of tools, `TOOLS`, with `tool_choice` `{"type": "any"}`: Claude must call a tool, but it picks which.
- Under `RECORD_INVOICE`, a second tool: `RECORD_CREDIT_NOTE = record_tool("record_credit_note", "credit note", "credit_note_number")`, and `TOOLS = [RECORD_INVOICE, RECORD_CREDIT_NOTE]`.

Save, then:

```bash
clear
python -m extraction.extract data/invoices/dev/INV-D09.txt
clear
cat data/invoices/dev/INV-D10.txt
clear
python -m extraction.extract data/invoices/dev/INV-D10.txt
```

`INV-D09` is a credit note: Claude picks `record_credit_note`. `INV-D10` is an email with a pro-forma invoice: "for approval only; no payment is due yet". Claude still has to pick one of the two tools, and picks `record_invoice`, with every field filled in. A pro-forma, filed as an invoice to pay.

### 3. Classify first, strict schemas

```bash
code extraction/extract.py
```

The final version (the kit's copy), from the bottom up:

- **The totals line**: when the record has `line_items`, print what the lines add up to next to the stated total. It's naive on purpose: it ignores shipping and discounts. Lesson 7.3 builds the real check.
- **`extract()`**: first a forced call to `extract_metadata`; if `doc_type` isn't one we record, return `"skipped"` and the metadata; otherwise force the matching recorder from `RECORDERS`.
- **`EXTRACT_METADATA`**: a strict tool whose input is `doc_type` (an enum: `invoice`, `credit_note` or `other`) and `supplier_name`. `other` gives a document that is neither an honest answer. **`RECORDERS`** maps each type to its tool.
- **`"strict": True`** on every tool, and **`"additionalProperties": False`** on every object (`ITEM`, the recorder's `input_schema`, the metadata tool's): strict schemas require it, and no field can appear that the schema doesn't name.

Save, then:

```bash
clear
python -m extraction.extract data/invoices/dev/INV-D10.txt
clear
cat data/invoices/dev/INV-D07.txt
clear
python -m extraction.extract data/invoices/dev/INV-D07.txt
```

`INV-D10` is now `skipped`, with `"doc_type": "other"`. `INV-D07`, from Ironleaf Tools, has a first line of "LED desk lamp, 1 gross, 19.70, 2,836.80" (a gross is 144), and a subtotal of 3,603.96 against a total due of 3,594.96. The record is valid, every field in the schema, but the lamp line says `"quantity": 1`, and the totals line prints `lines add up to 3,603.96; stated total 3,594.96`. Valid, and wrong: a schema guarantees the shape, not the values.

Strict changed nothing you could see in these runs: on Haiku 5.5 the forced calls already came back in shape. Strict is the guarantee, not a visible fix.

### Commit and push

```bash
clear
git status --short
git add extraction
git commit -m "Lesson 7.1: extraction with a forced tool, metadata first, strict schemas"
git push
```

Two files changed, 95 insertions.

## Forced tool choice today

True on 2026-10-17, and it may change: the Define tools page lists where forced tool use (`tool_choice` `any` or `tool`) isn't supported. With manual extended thinking it returns an error. Models with thinking on by default accept it, but a forced call skips thinking. And on the newest models (Claude Opus 5.5 and Claude Sonnet 5.5 among them), `any` and `tool` return a 400 error. There, use `auto` with strict tools, or structured outputs (`output_config.format`; in Python, `client.messages.parse()` with a Pydantic model) when you need the answer itself in a fixed shape. Check the page for the current list.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Show a document | `cat data/invoices/dev/INV-D01.txt` | PowerShell: `Get-Content data\invoices\dev\INV-D01.txt` |
| Make the package | `mkdir extraction && touch extraction/__init__.py` | PowerShell: `mkdir extraction; New-Item extraction\__init__.py` |
| Run the extractor | `python -m extraction.extract data/invoices/dev/INV-D01.txt` | the same (forward slashes work in Python) |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save).

## What the lesson showed

| Run | Result in the lesson |
|---|---|
| Version 1, `INV-D01` | `record_invoice`: Kestrel Outdoor Supply, `KOS-50960`, `2026-06-18`, `USD`, 2 lines, `"stated_total": 2166.96` (exact) |
| Version 2, `INV-D09` | `record_credit_note`: Kestrel, `KOS-79465`, `2026-04-08`, 3 lines, `"stated_total": 555.4` |
| Version 2, `INV-D10` (a pro-forma) | `record_invoice`: Quayside Electronics Wholesale, `QEW-33236`, 3 lines, `"stated_total": 2315.6` |
| Final, `INV-D10` | `skipped {"doc_type": "other", "supplier_name": "Quayside Electronics Wholesale"}` |
| Final, `INV-D07` | `record_invoice`: Ironleaf Tools Inc., `ILT-51418`; the lamp line `"quantity": 1` for "1 gross"; `lines add up to 3,603.96; stated total 3,594.96` |
| The commit | `9e83444`, 2 files changed, 95 insertions |

See `expected-output.md` for the full records. Model output changes from run to run: compare the behavior, not the exact values.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'extraction'`**: run from the `harborline` folder with `python -m extraction.extract ...`, and check that `extraction/__init__.py` exists.
- **An authentication error, or `Invalid API key`**: check `ANTHROPIC_API_KEY` in `.env` (Lesson 0.4); `load_dotenv()` reads it from the folder you run in.
- **A 400 error about forced tool use, or `tool_choice`**: your `harborline/config.py` names a model that rejects forced tool choice. Set it back to `claude-haiku-5-5` for this lesson (see [Forced tool choice today](#forced-tool-choice-today)).
- **`StopIteration`** in `call()`: the response had no `tool_use` block, which can only happen when `tool_choice` doesn't force a tool. Check the `choice` you pass.
- **A 400 error that mentions the schema** after step 3: a strict schema needs `"additionalProperties": False` on every object. Compare with the kit's copy.
- **`INV-D10` is not filed as an invoice in step 2, or `INV-D07`'s lamp line comes back right**: that's normal; model output varies. The point stands: `any` must pick a tool, and a valid record can still be wrong.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Extraction tool:** a tool Claude fills in but nothing runs; its input schema is the record you keep.
- **Forced tool choice:** `tool_choice` naming one tool, so the reply is that tool call.
- **`any`:** Claude must call a tool, and chooses which.
- **Strict tool:** `strict: true`; the inputs always match the schema.
- **Semantic error:** valid JSON with wrong values.

## Sources (checked 2026-10-17)

- Define tools: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- Strict tool use: https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use
- Structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Claude Certified Architect – Foundations Exam Guide: Task Statement 4.3, Scenario 6

Models and the API change. If an option, a field or a message doesn't match what you see, follow the official pages.
