# Student kit: Lesson 7.3, Validate, retry, self-correct

Claude Certified Architect – Foundations (CCAR-F) · Module 7: Structured Data Extraction · Lesson 7.3

This kit holds everything you need to repeat the lesson on your own computer: every command in order, the files the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Check what the schema can't
2. Retry with the evidence, and stop in time
3. Flag documents that disagree with themselves

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/extraction/validate.py` | The new file: `RETRY`, `Checked` with two validators, `problems()`, `totals()`, `extract_checked()` with three attempts and the review statuses |
| `harborline/extraction/extract.py` | `extract.py` as the lesson ends it: `call()` takes a `note`, appended after the document |

You type `validate.py` yourself, as in the lesson, or paste it from the kit. `extraction/schema.py` is Lesson 7.2's, unchanged.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The code and the steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 7.2 done**: your own `harborline` repository in `~/projects/harborline`, with its `.venv` (the `anthropic`, `python-dotenv` and `pydantic` packages), `extraction/schema.py` and `extraction/extract.py` from Lesson 7.2, and `origin` pointing at your own private `harborline` repository.
- **Your Anthropic API key in `.env`** (Lesson 0.4). `.env` is in `.gitignore`, so it is never committed.
- The model in `harborline/config.py` is `claude-haiku-5-5`. **Keep it for this lesson**: the calls force a tool, which works on Haiku 5.5 and returns an error on some newer models (Lesson 7.1).
- About 25 minutes. **This lesson makes API calls**: four runs, about a dozen calls in all (D07 alone makes four). The whole lesson costs under a cent.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### 1. Checks and a retry

```bash
git status --short
code extraction/extract.py
```

One change, from the bottom up: the user message ends with `</document>{note}`, and `call()` takes it: `def call(client, text, tool, note=""):`. A retry's evidence goes in the note. Save, then:

```bash
code extraction/validate.py
```

Type `validate.py`, top to bottom:

- **`RETRY`**: the retry message. "Your last extraction of this document failed these checks:", the errors, "Your last extraction was:", the output, and "Read the document again and extract it again. Fix what the checks found and keep the rest."
- **`Checked(schema.Document)`**: the same record, plus checks. `iso_date` (a field validator on `invoice_date` and `due_date`): a date that isn't `YYYY-MM-DD` fails. `lines_add_up` (a model validator): on every line, quantity × unit price must equal the amount within a cent. Its error carries the evidence: what quantity × price comes to, and how many of that price the amount is.
- **`problems(error)`**: one short line per failed check.
- **`totals(record)`**: `calculated_total` from the lines, tax and shipping, and a conflict when the stated total disagrees by more than a cent.
- **`extract_checked(client, path, tries=3)`**: `extract_metadata` first (skip what isn't an invoice or a credit note), then up to three attempts. A failed check prints the problems and puts them, with the failed output, in the next note. A passed check computes the totals and sets the status: `review: the document states no total` (no retry: it isn't in the document), `review: the document's total disagrees`, or `ok`. After three failures: `review: still failing after 3 attempts`.
- **At the bottom**: each line on one row, then the invoice number, both totals, `conflict_detected` and the status.

Save.

### 2. Fixed, capped, hopeless

```bash
clear
python -m extraction.validate data/invoices/dev/INV-D08.txt
clear
python -m extraction.validate data/invoices/dev/INV-D07.txt
clear
cat data/invoices/dev/INV-D11.txt
clear
python -m extraction.validate data/invoices/dev/INV-D11.txt
```

- **D08** (Cedar & Pine, "1 gross" velvet throw pillows): attempt 1 fails with the evidence (`... but the amount 984.96 is 144 x 6.84`); attempt 2 passes with 144, and the status is `ok`. The unit still says `gross`: Lesson 7.4's job.
- **D07** (Ironleaf, "1 gross" LED desk lamps): three attempts, the same reading every time, two lines with an empty unit, and `review: still failing after 3 attempts`. That's the real limit: better errors don't guarantee a fix, so the cap and the review route are the design.
- **D11** (Harrow Valley Ceramics, a scanned copy): `TOTAL DUE CAD [illegible]`. Attempt 1 passes, `stated_total` is null, `calculated_total` is 451.68, and the status is `review: the document states no total`. No retry: no second look can find a number that isn't there.

### 3. A document that disagrees with itself

```bash
clear
cat data/invoices/batch/INV-0048.txt
clear
python -m extraction.validate data/invoices/batch/INV-0048.txt
```

Six LED desk lamps at 19.70 (118.20), shipping 12.50, and a total due of 121.70. The extraction passes, but the lines plus shipping come to 130.70: `conflict_detected: true` and `review: the document's total disagrees`. The extraction is right; the document isn't, and a person decides.

### Commit and push

```bash
clear
git status --short
git add extraction
git commit -m "Lesson 7.3: validation with Pydantic, retries with the exact errors, calculated and stated totals"
git push
```

Two files changed, 91 insertions, 2 deletions.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Show a document | `cat data/invoices/dev/INV-D11.txt` | PowerShell: `Get-Content data\invoices\dev\INV-D11.txt` |
| Run the validator | `python -m extraction.validate data/invoices/dev/INV-D08.txt` | the same (forward slashes work in Python) |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save).

## What the lesson showed

| Run | Result in the lesson |
|---|---|
| `INV-D08` | attempt 1 failed (`... the amount 984.96 is 144 x 6.84`), attempt 2 passed; 2245.91 both; `ok` |
| `INV-D07` | attempts 1 to 3 failed, the same reading; `review: still failing after 3 attempts` |
| `INV-D11` | attempt 1 passed; `stated_total` null, `calculated_total` 451.68; `review: the document states no total` |
| `INV-0048` | attempt 1 passed; 121.7 stated vs 130.7 calculated; `conflict_detected: true`; `review: the document's total disagrees` |
| The commit | `eaa5585`, 2 files changed, 91 insertions, 2 deletions |

See `expected-output.md` for the full outputs. Model output changes from run to run: compare the behavior, not the exact values.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pydantic'`** (or `extraction`): activate `.venv`, run from the `harborline` folder with `python -m extraction.validate ...`, and check Lesson 7.2's setup.
- **`ImportError: cannot import name 'RECORD_DOCUMENT'`**: your `extract.py` is older than Lesson 7.2's. Compare with the kit's copy.
- **`TypeError: call() takes 3 positional arguments but 4 were given`**: the `note` parameter is missing from `call()`. Step 1's first edit.
- **A 400 error about forced tool use**: your `harborline/config.py` names a model that rejects forced tool choice. Set it back to `claude-haiku-5-5`.
- **D08 passes on the first attempt, or D07 gets fixed**: that's normal; model output varies. The design stands: retry with the evidence, and stop after three attempts.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Validator:** a check on the extracted record (format, arithmetic) beyond its shape.
- **Instructive error:** an error that says what's wrong and what the document shows.
- **Retryable failure:** a reading or format mistake the model can fix on a second look.
- **Hopeless failure:** the data isn't in the source; retrying can only invent it.
- **`conflict_detected`:** the calculated total and the stated total disagree.

## Sources (checked 2026-10-17)

- Handle tool calls: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
- Structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Claude Certified Architect – Foundations Exam Guide: Task Statement 4.4, Scenario 6

Models and the API change. If an option, a field or a message doesn't match what you see, follow the official pages.
