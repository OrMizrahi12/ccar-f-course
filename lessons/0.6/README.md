# Student kit: Lesson 0.6, Meet Harborline

Claude Certified Architect – Foundations (CCAR-F) · Section 0: Start Here · Lesson 0.6

This kit holds everything you need to repeat the lesson on your own computer: every command in order, what each one printed in the lesson, the map from the exam's six scenarios to the systems you'll build, the commands for Windows, macOS and Linux, and what to do when something goes wrong. The Harborline code itself isn't in the kit: you clone it from GitHub in step 1, exactly as in the lesson.

By the end of the lesson you can:

1. Map the six exam scenarios to the systems you'll build
2. Clone Harborline, install it and run its tests
3. Adopt the cost habits: Haiku first, small max_tokens, count first

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command typed in the lesson, in order, from `deactivate` to `gh repo create` |
| `expected-output.md` | What each command printed in the lesson: the clone, `pytest`, `check_setup`, the token counts and costs, the new GitHub repository. Where yours will differ, it says so. |
| `scenario-map.md` | The six exam scenarios and the Harborline module that builds each one |

The starter repository: https://github.com/OrMizrahi12/harborline-starter

The video is filmed on Ubuntu 24.04. Every command is the same on macOS and Linux; the few that differ on Windows are under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.3 and 0.4 done**: VS Code with the Python extension, Python 3.12, git, and the GitHub CLI (`gh`) signed in to your GitHub account (Lesson 0.3), and the `~/projects` folder. Check with `gh auth status`: it should say you're logged in to github.com.
- **Your API key from Lesson 0.4.** You paste it into Harborline's own `.env` in step 3. Have it ready where you keep it safe; never in a chat, a document or a screenshot.
- **Python 3.12 or newer.** The setup check fails on anything older.
- About 25 minutes. The lesson's API spend was **$0.00**: the tests and the setup check make no API calls, and the one call that does, the token count, is free.

## The steps (the lesson's order)

Lines that start with `#` are notes, not commands.

### 1. Clone

1. In your browser, open the starter repository: https://github.com/OrMizrahi12/harborline-starter. Scroll down to its README: the table under **The six systems you will build** is the same map as `scenario-map.md` in this kit.
2. Click the green **Code** button, stay on the **HTTPS** tab, and click the copy button beside the address.
3. In VS Code's terminal, leave the last project's environment, go to your projects folder and clone:

   ```bash
   deactivate                     # only if your prompt starts with (.venv)
   cd ~/projects
   git clone https://github.com/OrMizrahi12/harborline-starter.git harborline
   cd harborline
   code -r .
   ```

   - The last word, `harborline`, names the folder. Without it, git would call it `harborline-starter`.
   - `deactivate` leaves `hello-claude`'s virtual environment: Harborline gets its own. If your prompt doesn't start with `(.venv)`, skip it.
   - `code -r .` reopens the current VS Code window on the new folder. `code .` opens a new window instead; either is fine.
4. VS Code opens the folder in **Restricted Mode**, because it hasn't seen it before. Click **Manage** in the banner, then **Trust**. You know where this code comes from, so it's safe to trust; in Restricted Mode, tasks, debugging and some extensions are turned off.
5. Look around the Explorer:

   | Folder or file | What it holds |
   |---|---|
   | `harborline/` | The shared code every system uses: `config.py`, `data.py`, `backend.py`, `policy.py`, `errors.py`, `costs.py` |
   | `data/` | Harborline's synthetic world: customers, products, orders, the refund policy, labeled tickets, invoices and research sources (`data/README.md` describes each file) |
   | `legacy/warehouse/` | Code from the old warehouse system, explored in Modules 2 and 5 |
   | `scripts/` | `check_setup.py` and `count_tokens.py` |
   | `tests/` | 44 tests that run offline, with no API key |
   | `requirements.txt` | Three pinned packages: `anthropic==1.13.0`, `python-dotenv==1.2.4`, `pytest==9.1.1` |
   | `.env.example`, `.gitignore` | The template for your `.env`, and the files git ignores (`.env`, `.venv/`, `runs/` among them) |

### 2. Install and test

Open the terminal with **Ctrl+`** (backtick). It opens in the `harborline` folder.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
python -m scripts.check_setup
```

- After `activate`, the prompt starts with `(.venv)`. VS Code may ask: "We noticed a new environment has been created. Do you want to select it for the workspace folder?" Click **Yes**. The status bar then shows `.venv (3.12.3)` (or your version).
- `pip install` installs the three pinned packages and the packages they depend on. In the lesson pip took them from its cache; yours downloads them, which takes a little longer.
- `pytest` runs the 44 tests in under a second: **44 passed**. They check the data and the shared code you'll build on. They need no API key and no network.
- `check_setup` prints `[ok  ]` for Python and the three packages, a `[note]` that `.env` isn't there yet, the data counts (60 customers, 213 orders, 50 tickets, 112 invoices, 14 research sources), the default model `claude-haiku-5-5`, and **All set.** It makes no API calls.

### 3. Cost habits

Open `harborline/config.py`:

- `MODEL = "claude-haiku-5-5"`, with the rule in a comment: start with the cheapest model that does the job; step up only on evidence.
- `MAX_TOKENS = 1024`: the most tokens one reply may use, **thinking included**. On Claude Haiku 5.5, thinking counts toward `max_tokens`, so keep it small but leave room.
- `BUSINESS_DATE = date(2026, 10, 15)`: Harborline's "today", fixed so that refund windows and order ages always work out the same.

Open `harborline/costs.py`: `PRICES` per million tokens for Haiku 5.5 ($0.10 in, $0.50 out), Sonnet 5.5 ($2 / $10) and Opus 5.5 ($4 / $20); scroll down for Haiku 5.5's higher prices for prompts over 100,000 tokens, and `BATCH_DISCOUNT = 0.50` (the Message Batches API costs half).

Now your key. Make `.env` from the template and check it:

```bash
cp .env.example .env
python -m scripts.check_setup     # [note] .env found, but ANTHROPIC_API_KEY is empty
```

Open `.env` (`code .env`) and paste **your own key** from Lesson 0.4 right after `ANTHROPIC_API_KEY=`, with no spaces, and save. In the lesson this was done off screen. `.env` is in `.gitignore`, so git never commits it. Check again:

```bash
python -m scripts.check_setup     # [ok  ] .env found, ANTHROPIC_API_KEY is set
```

The script only says whether the key is there; it never prints it.

**Count before you send:**

```bash
python -m scripts.count_tokens data/refund_policy.md data/orders.json
```

The script asks the API how many input tokens each file would be, without running the model. Token counting is free (it has its own rate limits), and the count is an estimate. In the lesson:

| File | Characters | Tokens | Sent once on Haiku 5.5 | Sonnet 5.5 | Opus 5.5 |
|---|---|---|---|---|---|
| `data/refund_policy.md` | 1,771 | 612 | $0.00006 | $0.00122 | $0.00245 |
| `data/orders.json` | 161,874 | 72,666 | $0.00727 | $0.14533 | $0.29066 |

A batch halves each price. The whole orders file fits easily in Haiku 5.5's 1M-token context window, but almost no question needs all 213 orders: send one order, not the whole file.

### 4. Make it yours

`origin` points at the starter repository, which you can't push to. Rename it to `upstream`, then create your own private repository and push:

```bash
git remote -v                     # origin = .../harborline-starter.git
git remote rename origin upstream
git remote -v                     # upstream = .../harborline-starter.git
gh repo create harborline --private --source . --remote origin --push
git remote -v                     # origin = your harborline, upstream = the starter
```

- `--source .` creates the GitHub repository from this folder, `--remote origin` names the new remote `origin`, and `--push` pushes your commits. `gh` creates it in the account you signed in with.
- **Run `gh repo create` once.** It creates a real repository on your account; a second run fails because the name is taken.
- `upstream` keeps the link to the starter, so you can pull in any later fixes with `git pull upstream main`.

Open `https://github.com/YOUR-USERNAME/harborline` in your browser (with your GitHub username): a **Private** repository with the starter's files and **1 Commit**. Careful: the browser's autocomplete may finish the address as `harborline-starter`. If it does, retype it and press **Delete** to drop the suggestion before **Enter**. You'll push to this repository for the rest of the course, and in Module 6 GitHub Actions reviews pull requests on it.

## Windows, macOS and Linux

`git`, `gh`, `code`, `pytest` and the `python -m scripts...` commands are the same on every system (run them with the environment active). Only these differ:

| Step | Linux (the lesson) | macOS | Windows (PowerShell) |
|---|---|---|---|
| Create the environment | `python3 -m venv .venv` | `python3.12 -m venv .venv` (the Python you installed in Lesson 0.3) | `py -3.12 -m venv .venv` |
| Activate it | `source .venv/bin/activate` | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` (cmd.exe: `.venv\Scripts\activate.bat`) |
| Make `.env` | `cp .env.example .env` | `cp .env.example .env` | `Copy-Item .env.example .env` (cmd.exe: `copy .env.example .env`) |
| Go to your projects folder | `cd ~/projects` | `cd ~/projects` | `cd $HOME\projects` |

- **Windows:** git may check the files out with Windows line endings (CRLF). That's fine: the code reads text the same way on every system, so the tests and the token counts don't change. The `pytest` header says `platform win32` instead of `platform linux`.
- **macOS:** the `pytest` header says `platform darwin`. In VS Code, the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**).
- **WSL:** run the Linux commands inside the WSL terminal, with the project in your WSL home folder (`~/projects`).

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git clone` | `Cloning into 'harborline'...`, 180 objects, 99.83 KiB |
| VS Code | Restricted Mode → Manage → Trust |
| `python3 -m venv .venv` | VS Code offered the new environment for the workspace: Yes; status bar `.venv (3.12.3)` |
| `pip install -r requirements.txt` | `Successfully installed` … `anthropic-1.13.0` … `pytest-9.1.1 python-dotenv-1.2.4` … |
| `pytest` | `collected 44 items`, 7 test files, `44 passed in 0.14s` |
| `check_setup` (no `.env`) | Python 3.12.3, anthropic 1.13.0, python-dotenv 1.2.4, pytest 9.1.1; `.env not found yet`; the data counts; `All set.` |
| `check_setup` (empty `.env`) | `[note] .env found, but ANTHROPIC_API_KEY is empty` |
| `check_setup` (key pasted) | `[ok  ] .env found, ANTHROPIC_API_KEY is set` |
| `count_tokens` | `refund_policy.md`: 1,771 characters, 612 tokens; `orders.json`: 161,874 characters, 72,666 tokens |
| `git remote rename origin upstream` | `Renaming remote references: 100% (3/3), done.` |
| `gh repo create` | `✓ Created repository …/harborline on github.com`, `✓ Added remote …`, `✓ Pushed commits to …` |
| GitHub | `harborline`, Private, 1 branch, 1 commit |
| API spend | $0.00 (token counting is free) |

## Troubleshooting

- **`python3 -m venv .venv` fails with "ensurepip is not available"** (Ubuntu, Debian): run `sudo apt install python3-venv`, move the half-made `.venv` folder to the trash, and run the command again.
- **`pip` says "externally-managed-environment", or installs somewhere else**: the environment isn't active. Activate it (see the table above) and check that the prompt starts with `(.venv)`.
- **`check_setup` says `anthropic is not installed`, or `pytest: command not found`**: this terminal hasn't activated `.venv`. Every new terminal starts without it: activate it again.
- **`[FAIL] Python 3.10.x (this course uses 3.12 or newer)`**: the environment was made with an older Python. Move `.venv` to the trash and create it again with Python 3.12 (macOS: `python3.12`, Windows: `py -3.12`).
- **`pytest` reports failures or errors**: check that you're in the `harborline` folder (the one with `pytest.ini`), that `.venv` is active, and that `pip install -r requirements.txt` finished with `Successfully installed`. Don't edit anything under `data/`: the tests check it.
- **`ModuleNotFoundError: No module named 'harborline'` (or `'scripts'`)**: run the scripts from the repository folder, as modules: `python -m scripts.check_setup`, not `python scripts/check_setup.py`.
- **`count_tokens` prints `No API key found. Copy .env.example to .env and add your key.`**: `.env` is missing, empty, or not saved, or it's not in the `harborline` folder. Run `check_setup`: it says which.
- **`count_tokens` fails with `401` `authentication_error`**: the key is incomplete (copied in part, or with a space), disabled, or expired. Create a new key in the Console (Lesson 0.4) and paste it into `.env`.
- **Your token counts differ a little from the lesson's**: the count is an estimate, and it can change when the model's tokenizer changes. A count close to the lesson's is fine.
- **`.env` shows up in `git status`**: it must never be committed. Check that `.gitignore` is the starter's (it lists `.env`) and that the file is named exactly `.env`.
- **`gh repo create` says the name already exists on your account**: you already have a repository named `harborline` (perhaps from an earlier try). If it's your own copy of this project, point `origin` at it instead: `git remote add origin https://github.com/YOUR-USERNAME/harborline.git`, then `git push -u origin main`. Otherwise, use another name in the command.
- **`gh repo create` can't add the remote because `origin` already exists**: you skipped `git remote rename origin upstream`. Run it. Then, if the repository was already created on GitHub, don't run `gh repo create` again: add it with `git remote add origin https://github.com/YOUR-USERNAME/harborline.git` and push with `git push -u origin main`.
- **`gh: command not found`, or `gh` isn't logged in**: install the GitHub CLI and run `gh auth login` (Lesson 0.3's kit has the steps for every system).
- **`git push` to the starter is rejected**: that's expected. You can read the starter but not push to it; push to your own `origin`.
- **Restricted Mode came back, or a VS Code feature doesn't work**: click **Restricted Mode** in the status bar, then **Trust**.
- **Never paste your API key into code or into a chat**, and never commit `.env`. If a key leaks, disable it in the Console first, then create a new one (Lesson 0.4).

## Key terms

- **Exam scenario:** one of the six published situations that frame the exam's questions; four are drawn for each exam.
- **Starter repository:** the shared starting code you clone once and build on, module by module.
- **Test suite:** code that checks other code; `pytest` runs Harborline's 44 tests offline, with no API key.
- **Token counting:** asking the API how many input tokens a request would use, without running the model (free; an estimate).
- **Context window:** the most tokens a model can read in one request (1M on Claude Haiku 5.5). The 72,666-token orders file fits easily.

## Sources (checked 2026-10-14)

- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0, §5 Exam Scenarios (the six scenarios; four are presented, picked at random)
- Choosing a model ("Option 1: Start efficiency-first", with Claude Haiku 5.5): https://platform.claude.com/docs/en/about-claude/models/choosing-a-model
- Pricing (Claude Haiku 5.5, Sonnet 5.5 and Opus 5.5; prompts over 100,000 tokens; batch processing): https://platform.claude.com/docs/en/about-claude/pricing
- Token counting (free to use, rate-limited, an estimate): https://platform.claude.com/docs/en/build-with-claude/token-counting
- Claude Haiku 5.5 migration guide, configure thinking (thinking tokens count toward `max_tokens`): https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide#configure-thinking
- Batch processing (50% of standard prices): https://platform.claude.com/docs/en/build-with-claude/batch-processing
- Context windows (1M tokens on Claude Haiku 5.5): https://platform.claude.com/docs/en/build-with-claude/context-windows
- GitHub CLI, `gh repo create` (`--source`, `--remote`, `--push`): https://cli.github.com/manual/gh_repo_create
- GitHub, managing remote repositories (renaming a remote): https://docs.github.com/en/get-started/git-basics/managing-remote-repositories
- GitHub, cloning a repository: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
- pytest, get started: https://docs.pytest.org/en/stable/getting-started.html
- Python, *venv: creation of virtual environments*: https://docs.python.org/3/library/venv.html

Prices and tools change. If a number or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. This lesson ends Section 0; Module 1 builds Harborline's first agent loop.
