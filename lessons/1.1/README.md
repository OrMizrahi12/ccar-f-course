# Student kit: Lesson 1.1, How Claude reads a request

Claude Certified Architect – Foundations (CCAR-F) · Module 1: Claude API Foundations for Architects · Lesson 1.1

This kit holds everything you need to repeat the lesson on your own computer: the three small Python files written in the lesson, every command in order, what each run printed in the lesson, the one command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Treat tokens and the context window as a fixed budget
2. Carry the whole conversation on a stateless API
3. Tell system prompt, user turns and max_tokens apart

## What's in the kit

| File | What it is |
|---|---|
| `experiments/m1/budget.py` | Step 1, Count: how much of the context window three versions of one request use (free token counts, no model run) |
| `experiments/m1/first_request.py` | Step 2, Send: one request with a system prompt, a user turn and `max_tokens`, printing every content block, `stop_reason` and the token usage |
| `experiments/m1/stateless.py` | Step 3, Converse: the same question sent without the conversation, then with it |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each run printed in the lesson, line by line, and what will differ on yours |

The three files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them; if you'd rather not, copy the kit's `experiments` folder into your `harborline` folder, so that you have `harborline/experiments/m1/budget.py` and so on.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 0.6 done**: your own `harborline` repository in `~/projects/harborline`, its `.venv` with the three pinned packages (`anthropic` 1.13.0, `python-dotenv` 1.2.4, `pytest` 9.1.1), `pytest` passing, and `origin` pointing at your own private `harborline` on GitHub.
- **Your API key in Harborline's `.env`** (Lesson 0.6, step 3). `python -m scripts.check_setup` should say `ANTHROPIC_API_KEY is set`. The scripts load the key from `.env` and never print it.
- About 20 minutes. The lesson's API spend was **about a tenth of a cent** on Claude Haiku 5.5: `budget.py` runs no model (one lookup of the model's limits and three free token counts), `first_request.py` ran twice, and `stateless.py` makes three short calls.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder: the scripts are run as modules (`python -m experiments.m1.budget`), so they can import Harborline's shared code.

### 1. Count

```bash
git status --short                # prints nothing: a clean tree after Lesson 0.6
mkdir -p experiments/m1
code experiments/m1/budget.py     # type the file (or copy it from the kit), save
python -m experiments.m1.budget
```

What `budget.py` does:

- `client.models.retrieve(MODEL)` asks the Models API for this model's limits: `max_input_tokens` is the context window, and `max_tokens` is the most output one request may ask for.
- It builds three versions of the same request. The user turn is always the same customer ticket (T-003, a refund request); only the system prompt grows: the role alone, the role plus the refund policy, and the role, the policy and every order.
- `client.messages.count_tokens(...)` takes the same inputs as a real request, `system` included, and returns how many input tokens it would be. Counting is free, and it doesn't run the model.

In the lesson:

```text
claude-haiku-5-5: window 1,000,000, max output 128,000
role                          59 tokens   0.01%
role + policy                664 tokens   0.07%
role + policy + orders    73,323 tokens   7.33%
```

The window is enormous: even all 213 orders use about 7% of it. But "it fits" isn't "it's free": every input token is billed on every request, so the third version costs about 110 times more than the second, every time it's sent ($0.0073 against $0.00007 on Haiku 5.5). And more context isn't better context: accuracy and recall degrade as the context grows. The reply has to fit in the same window too.

### 2. Send

```bash
code experiments/m1/first_request.py    # type the file (or copy it), save
python -m experiments.m1.first_request
```

What `first_request.py` sends:

- `MAX_TOKENS = 1024` on line 8: the ceiling for this reply, **thinking included**.
- `system`: who Claude is ("Harborline's customer support assistant"), the rule for every answer ("Answer in two sentences or fewer.") and the refund policy. It's the same for every customer.
- `messages`: one user turn, the customer's own words from ticket T-003. That's the part that changes with every request.
- The loop prints every content block with its type; then `stop_reason`, and from `usage` the output tokens (with the thinking tokens inside them) and the input tokens.

In the lesson the reply started with a `[thinking]` block and then a `[text]` block of two sentences; `stop_reason: end_turn`; `output 179 of 1024 (thinking 91), input 677`. Claude Haiku 5.5 thinks by default and hides the thinking text, so the `[thinking]` line is empty, but its tokens are billed as output. The short answer came from the instruction in the system prompt, not from `max_tokens`: the reply used 179 of its 1,024.

Now make the ceiling tiny. In the editor, change line 8 to:

```python
MAX_TOKENS = 40  # the ceiling for this reply, thinking included
```

Save, and run it again:

```bash
python -m experiments.m1.first_request
```

In the lesson: `[thinking]` only, no text at all, `stop_reason: max_tokens`, `output 40 of 40 (thinking 40), input 677`. A small `max_tokens` didn't make the answer shorter: thinking spent the whole budget, and the customer would have received nothing. `max_tokens` is a ceiling, not a length target. Put length rules in the prompt, and leave room for thinking. (Lesson 1.2 reads `stop_reason` properly.)

**Change line 8 back to `MAX_TOKENS = 1024` and save.** The next lessons start from 1024.

### 3. Converse

```bash
code experiments/m1/stateless.py    # type the file (or copy it), save
python -m experiments.m1.stateless
```

What `stateless.py` does:

- One helper, `ask()`, sends the same short system prompt plus whatever `messages` list it's given, and prints how many messages went out, the input tokens and the reply's text.
- Call 1, `first request`: the ticket ("I changed my mind about the ceramic table lamp (order HL-10163)…").
- Call 2, `new request, no history`: only the question "Which order did I mention?".
- Call 3, `new request, full history`: the same question, with the conversation before it: `[first, answer, question]`. `answer` is Claude's first reply exactly as it came back (`reply.content`, thinking block included, never edited), and the system prompt is unchanged.

In the lesson:

| Request | Messages sent | Input tokens | Reply |
|---|---|---|---|
| first request | 1 | 66 | It can't see the order or the return policy here (this system prompt has no policy), so it can't confirm eligibility for HL-10163 |
| new request, no history | 1 | 38 | "I don't see an order number or any order details in our conversation so far…" |
| new request, full history | 3 | 255 | "You mentioned order HL-10163, for the ceramic table lamp…" |

Same model, same key, seconds later, and the second request had no idea: the API keeps nothing between requests. Send the history and it knows. The input tokens show what that memory costs: 38 without the history, 255 with it, and every later turn re-sends everything before it.

Finally, save your work to your own repository:

```bash
git add experiments
git commit -m "Lesson 1.1: count, send and converse experiments"
git push
```

The commit adds the three files (`3 files changed, 103 insertions(+)`), and `git push` sends it to `origin`, your own private `harborline`. Your commit id will differ from the lesson's.

## Windows, macOS and Linux

`git`, `code` and the `python -m experiments...` commands are the same on every system (run them with the environment active). Only one differs:

| Step | Linux and macOS (the lesson) | Windows (PowerShell or cmd.exe) |
|---|---|---|
| Make the folder | `mkdir -p experiments/m1` | `mkdir experiments\m1` (it creates both folders) |

- **Windows:** `code experiments/m1/budget.py` works with forward slashes in PowerShell. If your venv's `python` isn't found, activate the environment first (`.venv\Scripts\Activate.ps1`, Lesson 0.6).
- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**; go to a line with **Ctrl+G**).
- **WSL:** run the Linux commands inside the WSL terminal, in your WSL home folder.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` | Nothing printed (clean tree) |
| `budget.py`: Models API | `claude-haiku-5-5: window 1,000,000, max output 128,000` |
| `budget.py`: token counts | role 59 tokens (0.01%); role + policy 664 (0.07%); role + policy + orders 73,323 (7.33%) |
| `first_request.py`, `MAX_TOKENS = 1024` | `[thinking]`, `[text]` (two sentences), `stop_reason: end_turn`, `output 179 of 1024 (thinking 91), input 677` |
| `first_request.py`, `MAX_TOKENS = 40` | `[thinking]` only, `stop_reason: max_tokens`, `output 40 of 40 (thinking 40), input 677` |
| `stateless.py` | messages 1 / 1 / 3; input tokens 66 / 38 / 255; no history: no order number; full history: HL-10163 |
| `git commit` | `3 files changed, 103 insertions(+)` |
| `git push` | `main -> main` to your own `harborline` |
| API spend | About a tenth of a cent on Claude Haiku 5.5 |

Your token counts, thinking tokens and replies will differ from these, run to run. See `expected-output.md` for what should match.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'harborline'`**: you ran the file directly (`python experiments/m1/budget.py`). Run it as a module, from the `harborline` folder: `python -m experiments.m1.budget`.
- **`ModuleNotFoundError: No module named 'experiments'`**: you're not in the `harborline` folder, or the folder is named differently. `cd ~/projects/harborline`, and check that the files are at `experiments/m1/`.
- **`ModuleNotFoundError: No module named 'anthropic'`** or **`python: command not found`**: the environment isn't active in this terminal. Activate it (Lesson 0.6); the prompt should start with `(.venv)`.
- **An error about the API key, or `401` `authentication_error`**: `.env` is missing, empty or not saved, or the key is incomplete or disabled. Run `python -m scripts.check_setup`: it says which. Create a new key in the Console if you need one (Lesson 0.4).
- **`AttributeError` on `max_input_tokens` or `output_tokens_details`**: your `anthropic` package isn't the pinned 1.13.0. Run `pip install -r requirements.txt` with the environment active.
- **`429` `rate_limit_error`, or `529` `overloaded_error`**: wait a minute and run again.
- **Your numbers differ from the lesson's**: that's expected. Token counts are estimates, and replies, thinking tokens and output tokens change from run to run.
- **At `MAX_TOKENS = 1024` there's no `[thinking]` line**: Claude Haiku 5.5 decides how much to think; on a simple request it can skip thinking. Run it again, or move on: the point is the same.
- **At `MAX_TOKENS = 40` you see a cut-off `[text]` line**: that run thought for fewer than 40 tokens, so the cap cut the text instead. The lesson's point holds either way: `max_tokens` stops the reply, it doesn't make it shorter. Check that `stop_reason` says `max_tokens`.
- **The no-history request names an order number**: it can't know one; the request didn't carry it. If Claude guesses, that's a made-up answer, which is exactly the risk of not sending the history.
- **`400` `invalid_request_error` on the full-history request**: the history changed between requests. Keep the system prompt the same and send `reply.content` exactly as it came back; never edit earlier turns.
- **You committed `MAX_TOKENS = 40`**: change line 8 back to 1024, save, and commit again (`git commit -am "Restore MAX_TOKENS = 1024"`, then `git push`).
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).
- **`.env` shows up in `git status`**: it must never be committed. Check that `.gitignore` lists it. `git add experiments` adds only the experiments folder.
- **Never paste your API key into code or into a chat.** If a key leaks, disable it in the Console first, then create a new one (Lesson 0.4).

## Key terms

- **Token:** the unit Claude reads and writes, a word or a piece of one. You're billed per token, in and out. Claude Haiku 5.5's tokenizer gives about 30% more tokens for the same text than older models, so count, don't guess.
- **Context window:** the fixed budget of tokens one request can use: the system prompt, every message, tool definitions and the reply, thinking included (1M tokens on Claude Haiku 5.5).
- **Stateless API:** the API keeps no conversation between requests; every request carries the whole history in `messages`.
- **System prompt:** the top-level `system` field: Claude's role and the rules for every turn, kept apart from the user's words.
- **`max_tokens`:** the most tokens Claude may generate for one reply, thinking included. A ceiling, not a length target.

## Sources (checked 2026-10-14)

- Glossary, tokens (about 30% more tokens on the newer tokenizer): https://platform.claude.com/docs/en/about-claude/glossary#tokens
- Context windows (what counts, context rot, 1M on Claude Haiku 5.5, thinking tokens inside `max_tokens`): https://platform.claude.com/docs/en/build-with-claude/context-windows
- Using the Messages API, multiple conversational turns ("The Messages API is stateless"): https://platform.claude.com/docs/en/build-with-claude/working-with-messages#multiple-conversational-turns
- Prompting best practices, give Claude a role (a role in the system prompt): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role
- API reference, create a message (`max_tokens`, `system`, `messages`, `usage`): https://platform.claude.com/docs/en/api/messages/create
- Claude Haiku 5.5 overview (1M context window, 128K max output, prices): https://platform.claude.com/docs/en/models/haiku-5-5/overview
- Claude Haiku 5.5 migration guide, configure thinking (thinking counts toward `max_tokens`; keep earlier turns unchanged): https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide#configure-thinking
- Thinking (thinking tokens are billed as output, even when the thinking text is hidden): https://platform.claude.com/docs/en/build-with-claude/thinking
- Token counting (free to use, an estimate, `system` supported): https://platform.claude.com/docs/en/build-with-claude/token-counting
- API reference, get a model (`max_input_tokens`, `max_tokens`): https://platform.claude.com/docs/en/api/models/retrieve
- Pricing (Claude Haiku 5.5: $0.10 per million input tokens, $0.50 per million output tokens): https://platform.claude.com/docs/en/about-claude/pricing
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 5.1 (Domain 5: Context Management & Reliability), and Scenario 1: Customer Support Resolution Agent

Models and APIs change. If a number or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 1.2 you read the response properly: its content blocks, `stop_reason` and `usage`.
