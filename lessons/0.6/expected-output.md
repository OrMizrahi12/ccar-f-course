# Expected output: Lesson 0.6, Harborline on your machine

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12.3. Some lines will differ on your computer: your username and folder paths, transfer speeds and timings, and on Windows or macOS the platform name. Each section says what should match.

## Step 1: the clone

```text
$ cd ~/projects
$ git clone https://github.com/OrMizrahi12/harborline-starter.git harborline
Cloning into 'harborline'...
remote: Enumerating objects: 180, done.
remote: Counting objects: 100% (180/180), done.
remote: Compressing objects: 100% (136/136), done.
remote: Total 180 (delta 40), reused 180 (delta 40), pack-reused 0 (from 0)
Receiving objects: 100% (180/180), 99.83 KiB | 1.92 MiB/s, done.
Resolving deltas: 100% (40/40), done.
```

The download speed will differ. If the starter gets a fix after this lesson, the object count can grow a little.

Then `cd harborline` and `code -r .`. VS Code shows the banner "Restricted Mode is intended for safe code browsing. Trust this folder to enable all features." **Manage** opens Workspace Trust ("You are in Restricted Mode"); **Trust** turns everything on.

## Step 2: install and test

```text
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $
```

VS Code: "We noticed a new environment has been created. Do you want to select it for the workspace folder?" **Yes**.

```text
(.venv) $ pip install -r requirements.txt
...
Successfully installed annotated-types-0.8.0 anthropic-1.13.0 anyio-4.15.1 docstring-parser-0.18.0
h11-0.16.0 httpcore2-2.13.1 httpx2-2.13.1 idna-3.20 iniconfig-2.3.1 jiter-0.17.0 packaging-26.3
pluggy-1.6.0 pydantic-2.14.1 pydantic-core-2.50.1 pygments-2.21.0 pytest-9.1.1 python-dotenv-1.2.4
sniffio-1.3.1 truststore-0.10.5 typing-extensions-4.16.0 typing-inspection-0.4.4
```

In the lesson, pip used its cache (`Using cached ...`); yours shows `Downloading ...` lines first. The three pinned packages, `anthropic-1.13.0`, `pytest-9.1.1` and `python-dotenv-1.2.4`, must match. The packages they depend on aren't pinned, so some of their versions may be newer.

```text
(.venv) $ pytest
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/<you>/projects/harborline
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.15.1
collected 44 items

tests/test_backend.py ............                                       [ 27%]
tests/test_costs.py .....                                                [ 38%]
tests/test_data.py .......                                               [ 54%]
tests/test_invoices.py ...                                               [ 61%]
tests/test_legacy.py ...                                                 [ 68%]
tests/test_policy.py .........                                           [ 88%]
tests/test_tickets.py .....                                              [100%]

============================== 44 passed in 0.14s ==============================
```

What should match: `collected 44 items`, the seven test files, and **44 passed**. What may differ: the platform (`win32`, `darwin`), your Python version, the `rootdir` path, the time, and the width of the `=` lines (it follows your terminal's width).

```text
(.venv) $ python -m scripts.check_setup
Harborline setup check
  [ok  ] Python 3.12.3
  [ok  ] anthropic 1.13.0
  [ok  ] python-dotenv 1.2.4
  [ok  ] pytest 9.1.1
  [note] .env not found yet (copy .env.example to .env; the API lessons need it)
  [ok  ] 60 customers, 213 orders, 50 tickets, 112 invoices, 14 research sources
  Default model: claude-haiku-5-5
All set.
```

`[note]` lines are reminders, not errors. Any `[FAIL]` line ends with "Fix the FAIL lines above, then run this again." instead of `All set.`

## Step 3: cost habits

After `cp .env.example .env`, with nothing pasted yet:

```text
(.venv) $ python -m scripts.check_setup
...
  [note] .env found, but ANTHROPIC_API_KEY is empty
...
All set.
```

VS Code may show "An environment file is configured but terminal environment injection is disabled. Enable "python.terminal.useEnvFile" to use environment variables from .env files in terminals." You don't need that setting: Harborline's scripts load `.env` themselves. Close the notification.

With your key pasted into `.env` and saved:

```text
(.venv) $ python -m scripts.check_setup
...
  [ok  ] .env found, ANTHROPIC_API_KEY is set
...
All set.
```

The key itself never appears.

```text
(.venv) $ python -m scripts.count_tokens data/refund_policy.md data/orders.json
Tokens counted for claude-haiku-5-5. Cost = sending the file once as input.

data/refund_policy.md: 1,771 characters, 612 tokens
  claude-haiku-5-5   $0.00006   (batch $0.00003)
  claude-sonnet-5-5  $0.00122   (batch $0.00061)
  claude-opus-5-5    $0.00245   (batch $0.00122)

data/orders.json: 161,874 characters, 72,666 tokens
  claude-haiku-5-5   $0.00727   (batch $0.00363)
  claude-sonnet-5-5  $0.14533   (batch $0.07267)
  claude-opus-5-5    $0.29066   (batch $0.14533)
```

How to read it:

| Part | What it means |
|---|---|
| `Tokens counted for claude-haiku-5-5` | The count comes from the API's token counting endpoint, for the course's default model. It doesn't run the model, and it's free. |
| `1,771 characters, 612 tokens` | The file's length, and how many input tokens it would be as one message. |
| `claude-haiku-5-5   $0.00006` | The cost of sending the file once as input on that model, from the prices in `harborline/costs.py`. Output tokens would cost extra. |
| `(batch $0.00003)` | The same request through the Message Batches API, at half price. |

The arithmetic for `orders.json` on Claude Haiku 5.5: 72,666 tokens × $0.10 per million = $0.0072666, shown as `$0.00727`: under a cent. On Claude Opus 5.5, at $4 per million, the same file costs about 29 cents, forty times more. At 72,666 tokens the file is under Haiku 5.5's 100,000-token line, so the standard price applies.

Your character counts should match exactly. Your token counts should match or be very close: the count is an estimate, and it can change if the model's tokenizer changes. The costs follow from the tokens.

## Step 4: make it yours

```text
(.venv) $ git remote -v
origin  https://github.com/OrMizrahi12/harborline-starter.git (fetch)
origin  https://github.com/OrMizrahi12/harborline-starter.git (push)
(.venv) $ git remote rename origin upstream
Renaming remote references: 100% (3/3), done.
(.venv) $ git remote -v
upstream        https://github.com/OrMizrahi12/harborline-starter.git (fetch)
upstream        https://github.com/OrMizrahi12/harborline-starter.git (push)
```

```text
(.venv) $ gh repo create harborline --private --source . --remote origin --push
✓ Created repository YOUR-USERNAME/harborline on github.com
  https://github.com/YOUR-USERNAME/harborline
✓ Added remote https://github.com/YOUR-USERNAME/harborline.git
Enumerating objects: 179, done.
Counting objects: 100% (179/179), done.
Delta compression using up to 24 threads
Compressing objects: 100% (135/135), done.
Writing objects: 100% (179/179), 99.67 KiB | 99.67 MiB/s, done.
Total 179 (delta 40), reused 179 (delta 40), pack-reused 0
remote: Resolving deltas: 100% (40/40), done.
To https://github.com/YOUR-USERNAME/harborline.git
 * [new branch]      HEAD -> main
branch 'main' set up to track 'origin/main'.
✓ Pushed commits to https://github.com/YOUR-USERNAME/harborline.git
(.venv) $ git remote -v
origin  https://github.com/YOUR-USERNAME/harborline.git (fetch)
origin  https://github.com/YOUR-USERNAME/harborline.git (push)
upstream        https://github.com/OrMizrahi12/harborline-starter.git (fetch)
upstream        https://github.com/OrMizrahi12/harborline-starter.git (push)
```

`YOUR-USERNAME` is your GitHub username; in the lesson it was the presenter's account. The thread count and the speed depend on your computer and connection. What must match: the three `✓` lines, and `git remote -v` showing your `harborline` as `origin` and the starter as `upstream`.

On GitHub, `https://github.com/YOUR-USERNAME/harborline` shows the repository marked **Private**, branch `main`, **1 Branch**, **1 Commit** ("Harborline starter: shared package, synthetic data, offline tests"), and the folders `data`, `harborline`, `legacy`, `scripts`, `tests` with `.env.example`, `.gitignore`, `README.md`. There's no `.env` and no `.venv`: git ignores both.

## What to compare with yours

- `pytest` reports **44 passed**, with no failures or errors.
- `check_setup` ends with **All set.** and, after step 3, says `ANTHROPIC_API_KEY is set`.
- `count_tokens` prints 1,771 and 161,874 characters, and token counts at or near 612 and 72,666.
- `git remote -v` lists `origin` (your `harborline`) and `upstream` (the starter).
- Your GitHub repository is private and has no `.env`.
