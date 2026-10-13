# Student kit: Lesson 0.4, The Claude Console and your API key

Claude Certified Architect – Foundations (CCAR-F) · Section 0: Start Here · Lesson 0.4

This kit holds everything you need to repeat the lesson on your own computer: the two files the lesson adds to the `hello-claude` project, exactly as they were typed, every step in order, the output of the lesson's first call, and what to do when something goes wrong.

By the end of the lesson you can:

1. Set up the Console: a workspace, a spend limit and an expiring key
2. Keep your key in .env, out of code and out of git
3. Make your first API call and read the reply

## What's in the kit

| File | What it is |
|---|---|
| `hello-claude/.env.example` | Three lines: two comments and `ANTHROPIC_API_KEY=` with no value. Safe to commit. |
| `hello-claude/first_call.py` | The 23-line script from the lesson: one call to Claude Haiku 5.5, then the reply's text, stop reason, token counts and request ID |
| `expected-output.md` | What the script printed in the lesson, with and without a key, and how to read each line |

The video is filmed on Ubuntu 24.04. The Console steps are the same everywhere; the few terminal commands that differ on Windows are under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 0.3's project**: `~/projects/hello-claude` with its `.venv`, a `requirements.txt` that pins `anthropic==1.13.0` and `python-dotenv==1.2.4`, and a `.gitignore` with `.venv/`, `.env` and `__pycache__/`, committed and pushed to GitHub. If you skipped it, follow Lesson 0.3's kit first.
- **A Claude Console account** at https://platform.claude.com (sign up with your email). API calls are paid from your organization's credits, so add credits before your first call: in the Console, go to **Settings > Billing**. You can also turn on auto-reload there. Anthropic's pricing page says new users receive a small amount of free credits to test the API.
- About 20 minutes. The lesson's call cost about $0.00003.

## The steps (the lesson's order)

Lines that start with `#` are notes, not commands.

### 1. The Console: a workspace, a spend limit and an expiring key

**Tip:** do step 2 up to `cp .env.example .env` first, so that `.env` is ready when the Console shows your new key.

1. **Sign in** at https://platform.claude.com.
2. **Create a workspace.** Open **Organization settings**, then **Workspaces** (the docs call it Settings > Workspaces). Your organization starts with a Default workspace. Click **Create workspace**, give it a name such as `hello-claude` (and a color, if the form asks), and click **Create workspace** to finish. Only organization admins can create workspaces; in a company organization, ask your admin. A workspace is a group inside your organization with its own keys and limits. You need one of your own because the Default workspace can't have limits.
3. **Set a spend limit (recommended).** In the Workspaces list, click your workspace; a panel opens with this month's spend. Click **Spend limits**. The page shows your organization's monthly spend limit. Click **Change limit**, type your cap (for example `10` for $10 a month) and click **Set limit**. A workspace limit can be lower than the organization's limit, never higher. Until you set one, the organization's limit applies. In the lesson, the dialog is closed without saving.
4. **Create an API key.** Go to **Settings > API keys** and click **Create key**.
   - If a note about identity federation appears, click **Continue with an API key**. Federation is for workloads on cloud platforms; for your own development you want a plain API key.
   - **Name:** `hello-claude-dev`.
   - **Expires:** the presets are 3 hours, 1 day, 7 days and 30 days, plus Custom and Never. Pick 30 days for learning. The expiry is fixed when you create the key and can't be changed later.
   - **Linked account:** you. That makes it a personal key: it acts as you, and it stops working if you leave the organization. Shared jobs, such as a CI pipeline, should use a service account key instead.
   - **Scope:** your workspace, so the key only works there.
   - Click **Create key**.
5. **Copy the key once.** The Console shows the full key, which starts with `sk-ant-`, only once. Paste it straight into `.env` (step 2). Don't paste it anywhere else: not into code, a chat, a document or a screenshot. If you lose it, you can't view it again: create a new key.

In the lesson, the workspace and the key already existed, so both forms are filled in and closed without saving. The lesson's key was pasted into `.env` off screen.

### 2. Your key in `.env`

Open the project in VS Code and open its terminal (**Ctrl+`**):

```bash
cd ~/projects/hello-claude
source .venv/bin/activate      # if the prompt doesn't already start with (.venv)
git status                     # nothing to commit, working tree clean
code .env.example
```

Type these three lines and save (**Ctrl+S**), or copy the kit's `hello-claude/.env.example`:

```
# Copy this file to .env, then paste your key after the '='.
# .env is in .gitignore, so git never commits it.
ANTHROPIC_API_KEY=
```

`.env.example` documents which variable the project needs, without the secret, so it's safe to commit. Now make your real `.env` from it and check that git ignores it:

```bash
cp .env.example .env
git status                     # only .env.example is untracked; .env isn't listed
git check-ignore -v .env       # .gitignore:2:.env	.env
```

`git check-ignore -v` names the rule that ignores the file: line 2 of `.gitignore`.

Open `.env` (`code .env`), paste your key right after the `=` with no spaces, and save:

```
ANTHROPIC_API_KEY=sk-ant-...
```

VS Code may show a notification that an environment file is configured but terminal environment injection is disabled, and suggest the `python.terminal.useEnvFile` setting. You don't need it: the script loads `.env` itself.

### 3. Your first call

```bash
code first_call.py
```

Type the script from the lesson, or copy the kit's `hello-claude/first_call.py`:

```python
import anthropic
from dotenv import load_dotenv

load_dotenv()  # copies ANTHROPIC_API_KEY from .env into the environment

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY by itself

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=200,
    thinking={"type": "disabled"},
    messages=[
        {"role": "user", "content": "In one sentence, what is an API key?"}
    ],
)

for block in response.content:
    if block.type == "text":
        print(block.text)

print("stop_reason:", response.stop_reason)
print("tokens in:", response.usage.input_tokens, "out:", response.usage.output_tokens)
print("request id:", response._request_id)
```

What each part does:

- `load_dotenv()` reads `.env` and puts `ANTHROPIC_API_KEY` into the environment. `anthropic.Anthropic()` then finds the key there by itself, so the key never appears in the code.
- `model="claude-haiku-5-5"` is Claude Haiku 5.5's model ID.
- `max_tokens=200` is the most tokens the reply may use. On Claude Haiku 5.5, thinking counts toward `max_tokens`, so a small `max_tokens` can stop after a thinking block, before any text. For a one-sentence answer, `thinking={"type": "disabled"}` turns thinking off and leaves all 200 tokens for the text.
- The loop prints the blocks whose type is `text`. Always pick content blocks by their type, never by position (`content[0]`): with thinking on, a reply can start with a thinking block.
- The last three lines print why Claude stopped, the input and output token counts, and the request ID.

Run it:

```bash
python first_call.py
```

If `.env` has no key yet, you get a `TypeError` that ends with "Could not resolve authentication method…". That's expected: the SDK found no key, so it refused to send anything. With the key in `.env`, run it again: you get one sentence, `stop_reason: end_turn`, the token counts and a request ID. Compare with `expected-output.md`.

### 4. Commit it

```bash
git status                     # untracked: .env.example, first_call.py (no .env)
git add .env.example first_call.py
git commit -m "Add the first Claude API call"
git push
git log --oneline              # two commits on main
```

Add the two files by name, and check that `.env` never appears in `git status`.

## Windows, macOS and Linux

The Console steps are the same on every system. In the terminal, only these commands differ:

| Step | macOS and Linux (the lesson) | Windows (PowerShell) |
|---|---|---|
| Activate the environment | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| Make `.env` from the example | `cp .env.example .env` | `Copy-Item .env.example .env` |
| Run the script | `python first_call.py` | `python first_call.py` |

`git`, `code` and the file contents are the same everywhere. Run `python` with the environment active, so it uses the project's packages.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| Workspaces | Default, Claude Code, CCDV-F, CCAR-F (the course's workspace) |
| CCAR-F spend | This month $0.00, no workspace limit; organization monthly spend limit $100.00 |
| Create key form | Expires presets 3 hours, 1 day, 7 days, 30 days, Custom, Never; Linked account: the presenter (a personal key); Scope: CCAR-F |
| `git check-ignore -v .env` | `.gitignore:2:.env	.env` |
| First run, no key | `TypeError: "Could not resolve authentication method. …"`, raised locally |
| Second run | one sentence, `stop_reason: end_turn`, `tokens in: 18 out: 59`, `request id: req_…` |
| Cost | about $0.00003 |
| Commit | "Add the first Claude API call": `.env.example` and `first_call.py`; `git log --oneline` shows two commits |

## Troubleshooting

- **`TypeError: "Could not resolve authentication method…"`**: no key reached the SDK. Check that `.env` exists in the project folder, next to `first_call.py`, that it's named exactly `.env`, that the key comes right after `ANTHROPIC_API_KEY=`, and that you saved it. `load_dotenv()` looks for `.env` in the script's folder first, then in the folders above it. The error is raised on your computer, before anything is sent.
- **You changed the key in `.env`, but the old one is still used**: an `ANTHROPIC_API_KEY` that is already set in your terminal wins, because `load_dotenv()` doesn't overwrite variables that already exist. Open a new terminal, or remove the variable: `unset ANTHROPIC_API_KEY` (PowerShell: `Remove-Item Env:ANTHROPIC_API_KEY`).
- **`401` `authentication_error`**: the API rejected the key. It may be incomplete (copied in part, or with a space), disabled or deleted, or expired. Expired keys can't be reactivated: create a new key and paste it into `.env`.
- **"Your credit balance is too low to access the Anthropic API…"**: your organization has no credits left. Add credits, or turn on auto-reload, under **Settings > Billing** in the Console.
- **`402` `billing_error`**: there's an issue with your billing or payment information. Check your payment details in the Console.
- **`400` `invalid_request_error` that begins "You have reached your specified workspace API usage limits"**: the workspace hit the spend limit you set. Raise or remove the limit to continue sooner; the message says when access resumes.
- **The Create key button is disabled**: your role in the organization doesn't allow you to create keys there. Ask an organization admin to change your role, or to create a service account key for you.
- **`ModuleNotFoundError: No module named 'dotenv'` (or `'anthropic'`)**: the environment isn't active. Activate it (see the table above) and run the script again. If the packages are missing, run `pip install -r requirements.txt`.
- **`.env` appears in `git status`**: `.gitignore` doesn't have the `.env` line, or `.gitignore` isn't saved in the project folder. Fix it before you commit. If you already staged `.env`, unstage it with `git rm --cached .env`.
- **Never paste a key into code or into a chat**, and never share `.env`. Anyone who has the key can spend your credits.
- **If a key leaks** (committed, pushed, pasted into a chat, shown in a screenshot): disable it in the Console first, under **Settings > API keys** (Disable is reversible; Delete is permanent). Then create a new key and put it in `.env`. Deleting the key from your code in a new commit isn't enough: the old commit still holds it.

## Key terms

- **API key:** the secret that lets your code call the Claude API and bills your organization. The Console shows it once, when you create it.
- **Workspace:** a group inside your Console organization with its own keys, spend limit and rate limits.
- **Spend limit:** a monthly cap on what a workspace (or the organization) can spend.
- **.env file:** a local, git-ignored file holding environment variables such as `ANTHROPIC_API_KEY`.
- **Token:** the unit a model reads and writes. You pay per input and output token.
- **max_tokens:** the most tokens one reply may use. On Claude Haiku 5.5, thinking counts toward it.

## Sources (checked 2026-10-14)

- Get your Claude API key: https://platform.claude.com/docs/en/get-api-key
- Authentication, key expiration and key safety: https://platform.claude.com/docs/en/manage-claude/authentication#key-expiration
- Workspaces, set workspace limits: https://platform.claude.com/docs/en/manage-claude/workspaces#set-workspace-limits
- Rate limits and spend limits: https://platform.claude.com/docs/en/api/rate-limits
- Python SDK (installation, the python-dotenv tip, request IDs): https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python
- Models overview (`claude-haiku-5-5`): https://platform.claude.com/docs/en/about-claude/models/overview
- Pricing (Claude Haiku 5.5, free credits for new users): https://platform.claude.com/docs/en/about-claude/pricing
- Claude Haiku 5.5 migration guide, configure thinking: https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide#configure-thinking
- API errors (401, 402, 400, request IDs): https://platform.claude.com/docs/en/api/errors
- API credits and the "credit balance is too low" message: https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers
- python-dotenv: https://pypi.org/project/python-dotenv/

The Console changes over time. If a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes.
