# Student kit: Lesson 7.4, Few-shot for messy documents

Claude Certified Architect – Foundations (CCAR-F) · Module 7: Structured Data Extraction · Lesson 7.4

This kit holds everything you need to repeat the lesson on your own computer: every command in order, the files the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Measure a labeled dev set before you change the prompt
2. Show each layout with the exact output
3. Make informal quantities consistent

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/extraction/dev_check.py` | The new dev-set check: runs the 12 dev documents through `extract_checked()` and compares them with `labels.jsonl` |
| `harborline/extraction/prompts/examples.md` | The five examples, in `<example>` tags inside `<examples>` |
| `harborline/extraction/extract.py` | `extract.py` as the lesson ends it: `EXAMPLES` is read from the file and sent with every request |

You type the new files yourself, as in the lesson, or paste them from the kit. `extraction/schema.py` (Lesson 7.2) and `extraction/validate.py` (Lesson 7.3) are unchanged.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The code and the steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 7.3 done**: your own `harborline` repository in `~/projects/harborline`, with its `.venv` (the `anthropic`, `python-dotenv` and `pydantic` packages), `extraction/schema.py`, `extraction/extract.py` and `extraction/validate.py` from Lessons 7.2 and 7.3, and `origin` pointing at your own private `harborline` repository.
- **The dev set**: `data/invoices/labels.jsonl` and `data/invoices/dev/` ship with the starter. Twelve documents are marked `"split": "dev"`; each label has the fields and every line's quantity and unit.
- **Your Anthropic API key in `.env`** (Lesson 0.4). `.env` is in `.gitignore`, so it is never committed.
- The model in `harborline/config.py` is `claude-haiku-5-5`. **Keep it for this lesson**: the calls force a tool, which works on Haiku 5.5 and returns an error on some newer models (Lesson 7.1).
- About 30 minutes. **This lesson makes API calls**: two runs of twelve documents, each with a metadata call and one or more extraction attempts, about thirty calls in all. The whole lesson costs a few cents at most.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### 1. Measure

```bash
git status --short
code extraction/dev_check.py
```

Type `dev_check.py`, top to bottom:

- **`FIELDS`**: what we compare: the document type, the number, the dates, the order number, the currency, the tax, the shipping and the stated total.
- **`same(a, b)`**: numbers match to half a cent; anything else must be equal.
- **`differences(result, label)`**: every field that doesn't match its label, then, line by line, the quantity and the unit. Descriptions vary in wording, so they aren't compared.
- **`main()`**: loads the labels, keeps the dev split, runs each document through Lesson 7.3's `extract_checked()` (with its attempt lines kept out of the table), and prints one row per document (its id, its layout, and what's wrong, or `ok`). The last line counts the exact documents and the wrong values.

Save, then:

```bash
clear
python -m extraction.dev_check
```

In the lesson, before any examples: **9 of 12 documents exact; 7 wrong values.** D06 (a prose letter) had two lines with the unit `roll`; D07 (a table) had quantity 1 where the label says 144, the unit `gross`, and two empty units; D08 (an email) had the unit `gross`. Lesson 7.3's rules and retries didn't fix any of these.

### 2. Five examples

```bash
mkdir extraction/prompts
code extraction/prompts/examples.md
```

Type the five examples. Each has the document text, the exact output and a short `<why>` that names the wrong answer it rules out:

1. **A table row**: `1 gross` steel rulers at 0.85 → quantity 144, unit `each` (not quantity 1 with unit `gross`).
2. **A sentence of prose**: 3 cases of 12 napkins → 36, `each`; the pack size stays out of the description.
3. **An email bullet**: half a dozen saucepans at `31,00` (a decimal comma) → 6 at 31.00.
4. **The plain case**: 4 desk fans → unit `each`, never empty and never a placeholder.
5. **A header line from a German supplier**: `Datum: 03.11.2026` → `2026-11-03`, the third of November.

None of the five is a dev document. Save, then:

```bash
code extraction/extract.py
```

Two changes: under `RULES`, `EXAMPLES = (Path(__file__).parent / "prompts" / "examples.md").read_text()`; and in `call()`, the message sends the examples between the rules and the document: `f"{RULES}\n{EXAMPLES}\n<document>\n{text}\n</document>{note}"`. Save.

### 3. The same twelve documents again

```bash
clear
python -m extraction.dev_check
```

In the lesson: **12 of 12 documents exact; 0 wrong values.** Two runs aren't a guarantee: Lesson 7.5 runs a hundred documents, and Lesson 7.6 measures accuracy at scale.

### Commit and push

```bash
clear
git status --short
git add extraction
git commit -m "Lesson 7.4: few-shot examples for messy documents, and a dev-set check against the labels"
git push
```

Three files changed, 92 insertions, 1 deletion.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Make the folder | `mkdir extraction/prompts` | PowerShell: the same (`mkdir extraction\prompts` also works) |
| Run the check | `python -m extraction.dev_check` | the same |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save).

## What the lesson showed

| Run | Result in the lesson |
|---|---|
| Before (no examples) | 9 of 12 documents exact; 7 wrong values (D06 units `roll`; D07 quantity 1, unit `gross`, two empty units; D08 unit `gross`) |
| After (five examples) | 12 of 12 documents exact; 0 wrong values |
| The commit | `cb00838`, 3 files changed, 92 insertions, 1 deletion |

See `expected-output.md` for the full outputs. Model output changes from run to run: compare the behavior, not the exact values.

## Troubleshooting

- **`FileNotFoundError: ... prompts/examples.md`**: the folder or the file name differs. It must be `extraction/prompts/examples.md`, next to `extract.py`.
- **`ModuleNotFoundError: No module named 'extraction'`**: run from the `harborline` folder with `python -m extraction.dev_check`, with `.venv` active.
- **`ImportError: cannot import name 'extract_checked'`**: Lesson 7.3's `validate.py` is missing or older. Compare with Lesson 7.3's kit.
- **`KeyError: 'split'`** (or `'format'`): your `labels.jsonl` is older than the starter's. Pull the starter's `data/invoices/labels.jsonl`.
- **Your "before" run has more, or fewer, wrong values**: that's normal; model output varies, and in practice runs even more failed. Measure on your own run, add the examples, and run the same twelve again.
- **A 400 error about forced tool use**: your `harborline/config.py` names a model that rejects forced tool choice. Set it back to `claude-haiku-5-5`.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Dev set:** a small set of documents with labels you trust, re-run after every prompt change.
- **Few-shot block:** a handful of examples, each with the exact output, sent with the prompt.
- **Layout coverage:** one example per way the documents are written: table, prose, email, header.
- **Informal quantity:** a gross, a case of twelve, half a dozen, counted in single items.
- **Placeholder value:** an empty string, "null" or "<UNKNOWN>" in a required field.

## Sources (checked 2026-10-17)

- Prompting best practices (Use examples effectively): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Claude Certified Architect – Foundations Exam Guide: Task Statement 4.2, Scenario 6

Models and the API change. If an option, a field or a message doesn't match what you see, follow the official pages.
