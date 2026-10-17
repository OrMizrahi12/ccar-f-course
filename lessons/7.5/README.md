# Student kit: Lesson 7.5, Batch processing at scale

Claude Certified Architect – Foundations (CCAR-F) · Module 7: Structured Data Extraction · Lesson 7.5

This kit holds everything you need to repeat the lesson on your own computer: every command in order, the files the lesson ends with, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Know what a batch trades for half the price
2. Batch the work nobody is waiting on
3. Resubmit only what failed, with a fix

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |
| `harborline/extraction/batch.py` | The new file: the batch folder through the Message Batches API, two batches, the retries, the join |
| `harborline/extraction/extract.py` | `extract.py` as the lesson ends it: `request()` returns the parameters of one forced call |
| `harborline/extraction/validate.py` | `validate.py` as the lesson ends it: `finish()` adds the totals and the status |

You type the code yourself, as in the lesson, or paste it from the kit.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The code and the steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 7.4 done**: your own `harborline` repository in `~/projects/harborline`, with its `.venv`, `extraction/extract.py`, `schema.py`, `validate.py` and `prompts/examples.md` from Lessons 7.1 to 7.4, and `origin` pointing at your own private `harborline` repository.
- **Your Anthropic API key in `.env`** (Lesson 0.4). `.env` is in `.gitignore`, so it is never committed.
- The model in `harborline/config.py` is `claude-haiku-5-5`. **Keep it for this lesson**: the calls force a tool (Lesson 7.1).
- About 45 minutes, most of it waiting for the batches. **This lesson makes API calls**: three batches over the 100 documents in `data/invoices/batch` (100, then 94, then 38 requests in the lesson). The lesson's run cost about $0.05 at batch prices.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### 1. One request, two ways

```bash
git status --short
code extraction/extract.py
```

Add `request(text, tool, note="")` above `call()`: it returns the parameters of one forced call (the model, `max_tokens`, the tool, the forced `tool_choice` and the message with the rules, the examples and the document). `call()` now sends `client.messages.create(**request(text, tool, note))`. The same parameters work for a single call and inside a batch. Save, then:

```bash
code extraction/validate.py
```

Add `finish(record)`: it takes the totals and the status out of `extract_checked()` (the calculated total, whether it conflicts with the stated total, and the status: `ok`, or a reason for review). `extract_checked()` now returns `meta | finish(record)`. Save.

### 2. Batch, match, resubmit

```bash
code extraction/batch.py
```

Type `batch.py` (the kit's file is the result):

- **The docstring** holds the math: invoices must be in the books within 36 hours of arriving, a batch can take up to 24, so a batch goes out every 8 hours (8 waiting + 24 processing, 4 to spare). The 36 hours are Harborline's own deadline, a number for the example.
- **`run(client, requests)`** sends one batch (`client.messages.batches.create`, each request with its `custom_id`), checks once a minute until `processing_status` is `ended`, prints how long it took and the counts, and returns each result by its `custom_id`. It adds up the cost with `estimate_cost(..., batch=True)`.
- **`tool_input(result)`**: no input for an errored, canceled or expired request; `max_tokens` when the reply was cut off; otherwise the input Claude gave the tool.
- **`parts(text, size=8)`**: a long line table split into parts of 8 lines, each with the header and the totals.
- **`check(record)`**: Lesson 7.3's checks; the finished record, or the errors for a retry.
- **`main(folder)`**: batch one classifies every document (`custom_id` = the document's id); anything that isn't an invoice or a credit note is set aside. Batch two records the rest. Then, up to two attempts, **only the failed `custom_id`s go out again, each with its fix**: a record that failed the checks goes back with its errors, a reply cut off at `max_tokens` goes back in parts (`INV-0008_part1`, ...), an errored or expired request goes back as it was. Parts are joined into one record (the first part's fields, every part's lines) and checked. Everything goes to `runs/batch.jsonl`, with a count of each status and the cost.

Save.

### 3. A hundred documents

```bash
clear
ls data/invoices/batch | wc -l
python -m extraction.batch data/invoices/batch
```

The script prints each batch as it goes out, then nothing until it has ended (a check every minute). In the lesson the three batches took 7, 4 and 4 minutes. That's that run, not a promise: most batches end within an hour, and any batch can take up to 24 hours. You can stop waiting at any time with **Ctrl+C**: the batch keeps running on the server, and you can see it in the Claude Console.

Then look at one joined record:

```bash
grep INV-0008 runs/batch.jsonl | python -m json.tool | tail -14
```

### Commit and push

```bash
clear
git status --short
git add extraction
git commit -m "Lesson 7.5: the batch folder through the Message Batches API, resubmitting only what failed"
git push
```

Three files changed, 153 insertions, 9 deletions. `runs/batch.jsonl` is ignored by git; it stays on disk for Lesson 7.6.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Count the documents | `ls data/invoices/batch \| wc -l` | PowerShell: `(Get-ChildItem data\invoices\batch).Count` |
| Show one record | `grep INV-0008 runs/batch.jsonl \| python -m json.tool \| tail -14` | PowerShell: `Select-String INV-0008 runs\batch.jsonl` (the whole line), or open `runs\batch.jsonl` in VS Code |
| Run the batch | `python -m extraction.batch data/invoices/batch` | the same (forward slashes work in Python) |
| Clear the terminal | `clear` | `cls` (or `clear` in PowerShell) |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal, Cmd+S to save).

## What the lesson showed

| Step | Result in the lesson |
|---|---|
| `ls data/invoices/batch \| wc -l` | `100` |
| Batch 1 (classify) | 100 requests; ended after 7 min: 100 succeeded, 0 errored, 0 expired |
| Batch 2 (record) | 94 requests (6 documents aren't invoices or credit notes); ended after 4 min: 94 succeeded; `INV-0008: max_tokens`, `INV-0016: max_tokens` |
| Batch 3 (only the failures, in parts) | 38 requests (19 parts each); ended after 4 min: 38 succeeded |
| The count | 85 `ok` · 1 `review: the document states no total` · 8 `review: the document's total disagrees` · 6 `skipped` |
| The cost | `100 documents, $0.0486 at batch prices (half of $0.0972) -> batch.jsonl` |
| INV-0008, joined | 150 lines from 19 parts; `calculated_total` 37042.82 = `stated_total`; `status` `ok` |
| The commit | `4604883`, 3 files changed, 153 insertions, 9 deletions |

No record failed the checks in the lesson's run, so no check retry went out; the path is in the code for when one does. See `expected-output.md` for the full outputs. Model output and batch times change from run to run: compare the behavior, not the exact values.

## Troubleshooting

- **The script seems stuck**: it prints nothing while a batch is processing. Wait, or check the batch in the Claude Console. Most batches end within an hour; a batch that doesn't end within 24 hours expires, and its requests come back `expired` (the script sends them again).
- **`AttributeError` on `client.messages.batches`**: your `anthropic` package is old. Run `pip install -r requirements.txt` with `.venv` active.
- **`ImportError: cannot import name 'request'` or `'finish'`**: step 1's changes to `extract.py` or `validate.py` are missing or not saved.
- **A `max_tokens` part again**: a part of 8 lines fits in `MAX_TOKENS` (1024) with room to spare on Haiku 5.5. If you changed the model or `MAX_TOKENS`, use smaller parts: `parts(text, size=6)`.
- **More documents to review than in the lesson**: model output varies. Compare the statuses, not the exact counts.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Message Batch:** many Messages requests sent as one job; 50% of the price, results within 24 hours.
- **`custom_id`:** your id for each request; the only way to match a result, since order isn't kept.
- **Latency-tolerant work:** nobody is waiting on it (overnight extraction, reports).
- **Blocking work:** someone waits for the answer (a check before a merge, a chat reply).
- **Submission frequency:** how often a batch must go out so that the wait plus 24 hours still meets the deadline.

## Sources (checked 2026-10-17)

- Batch processing: https://platform.claude.com/docs/en/build-with-claude/batch-processing
- Claude Certified Architect – Foundations Exam Guide: Task Statement 4.5, Scenario 6

Models and the API change. If an option, a field or a message doesn't match what you see, follow the official pages.
