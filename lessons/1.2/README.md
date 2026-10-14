# Student kit: Lesson 1.2, Reading the response

Claude Certified Architect – Foundations (CCAR-F) · Module 1: Claude API Foundations for Architects · Lesson 1.2

This kit holds everything you need to repeat the lesson on your own computer: the three Python files written in the lesson, every command in order, what each run printed in the lesson, the one command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Read a reply's blocks, usage and request ID
2. Decide the next step from every stop_reason
3. Run a chat by appending every turn correctly

## What's in the kit

| File | What it is |
|---|---|
| `harborline/usage.py` | Step 1, Log every call: `log_usage(response, label)` appends one JSON line per call to `runs/usage.jsonl`, with the request ID, the token counts and the cost. From this lesson on, every call in the course goes through it |
| `experiments/m1/read_response.py` | Step 2, Read a reply: one request sent two ways (`plain`, and `tool` with a tool definition), every part of the reply printed, and `next_step()`, which decides what to do from `stop_reason` |
| `experiments/m1/conversation.py` | Step 3, Chat turn by turn: a support chat in the terminal that appends every turn correctly and prints each turn's usage |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each run printed in the lesson, line by line, and what will differ on yours |

The three files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them; if you'd rather not, copy them into your `harborline` folder at the same paths: `usage.py` goes into the package folder, next to `config.py` and `costs.py` (`~/projects/harborline/harborline/usage.py`), and the two experiments go next to Lesson 1.1's files in `experiments/m1/`.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 1.1 done**: your own `harborline` repository in `~/projects/harborline` with `experiments/m1/` from Lesson 1.1 committed and pushed, its `.venv` with the pinned packages (`anthropic` 1.13.0, `python-dotenv` 1.2.4, `pytest` 9.1.1), and `origin` pointing at your own private `harborline`.
- **Your API key in Harborline's `.env`** (Lesson 0.6). `python -m scripts.check_setup` should say `ANTHROPIC_API_KEY is set`. The scripts load the key from `.env` and never print it.
- About 25 minutes. The lesson's API spend was **about five hundredths of a cent** on Claude Haiku 5.5 (about $0.0005): the `plain` call cost about $0.000059, the `tool` call about $0.000072, and the three chat turns about $0.00035.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder: the scripts are run as modules (`python -m experiments.m1.read_response`), so they can import Harborline's shared code.

### 1. Log every call

```bash
git status --short              # prints nothing: a clean tree after Lesson 1.1
code harborline/usage.py        # type the file (or copy it from the kit), save
```

What `usage.py` does:

- `USAGE_LOG` is `runs/usage.jsonl` under the project root. The `runs/` folder is already in `.gitignore` (since Lesson 0.6), so the log stays on your machine and is never committed.
- `log_usage(response, label)` builds one record per call: the time in UTC, your label, **the request ID** (`response._request_id`, which the Python SDK copies from the `request-id` response header; it's public despite the underscore), the model, the `stop_reason`, and the tokens.
- `usage.input_tokens` is only the part of the prompt that wasn't read from or written to the cache, so cache reads and cache writes get their own fields. `output_tokens` includes the thinking; `thinking_tokens` (from `usage.output_tokens_details`) shows how much of the output was thinking.
- The cost comes from `estimate_cost()` in `costs.py`, Harborline's price table from Lesson 0.6, rounded to 8 decimal places. The comment says it honestly: `costs.py` has no price for cache writes yet, because Module 1 never writes a cache.
- The record is appended to the log as one JSON line, and returned.

Nothing runs yet: the next step calls it.

### 2. Read a reply

```bash
code experiments/m1/read_response.py               # type the file (or copy it), save
clear; python -m experiments.m1.read_response plain
clear; python -m experiments.m1.read_response tool
```

What `read_response.py` does:

- `LOOKUP_ORDER` is a tool definition: a name, a description and a JSON Schema that asks for one `order_id`. Claude only gets to see it here; Lesson 1.3 runs it for real.
- `CASES` holds two versions of one request: `plain` adds nothing, and `tool` adds the tool. `request | CASES[case]` merges the case's settings into the request.
- The request: Harborline's model and `MAX_TOKENS` from `config.py`, a short system prompt ("Reply in two sentences or fewer."), and one user turn, ticket T-008: "Hi, can you tell me where order HL-10196 is? I haven't had a shipping email yet."
- `show()` walks the content blocks **by type, never by position**: a `thinking` block prints the length of its text and of its signature (never the signature itself), a `text` block prints its text, a `tool_use` block prints the tool's name, its input and its ID. Then the `usage` object on one line, exactly as returned, `stop_reason`, the message ID and the request ID.
- `next_step()` decides with a `match` on `stop_reason`: `end_turn` → use the text; `tool_use` → run the tool, then send its result back; `max_tokens` → cut off (mid-answer if there's text, before any text if not): don't use it; `pause_turn` → send the content back as is; `refusal` → read the category from `stop_details`, don't use the reply, log the request ID; anything else → log it and stop.
- Every call goes through `log_usage()`, and the last line prints the cost.

In the lesson, the `plain` case printed a `[thinking]` block (0 characters of text, a 980-character signature), then a two-sentence `[text]` reply: it can't look up the order, so it points to the confirmation email or support. Usage: `input_tokens` 68, `output_tokens` 104, of which `thinking_tokens` 44, both cache fields 0. `stop_reason: end_turn`, a message ID (`msg_…`) and a different request ID (`req_…`), `next step: done: use the text`, about $0.000059.

The `tool` case, the same question with one tool added, printed no thinking and no text: just `[tool_use] lookup_order {'order_id': 'HL-10196'}`. `input_tokens` jumped from 68 to 443: the tool definition, plus the tool-use system prompt the API adds when tools are present (286 tokens on Claude Haiku 5.5). `stop_reason: tool_use`, and `next step: run the tool, then send its result back (Lesson 1.3)`. Code that only looked for text would have sent the customer nothing.

Back in the editor, `next_step()` starts at line 47 (**Ctrl+G**, `47`): it decides from `stop_reason`, never from whether there's text. `max_tokens` is the stop you produced in Lesson 1.1; `pause_turn` and `refusal` aren't produced in the lesson (one needs a server tool's long loop, the other a declined request), so they're taught from the docs.

Then open the log:

```bash
code runs/usage.jsonl
```

Two lines, one per call, each with its `request_id`, its tokens and its `cost_usd`. Small costs print in e-notation: `5.88e-05` is $0.0000588, about six thousandths of a cent; `7.18e-05`, about seven.

### 3. Chat, turn by turn

```bash
code experiments/m1/conversation.py              # type the file (or copy it), save
clear; python -m experiments.m1.conversation
```

What `conversation.py` does:

- `system` is Harborline's role, "Answer from this policy, in two sentences or fewer.", and the refund policy itself. It never changes during the chat.
- `messages` starts empty and is only ever appended to.
- Each loop reads a question (an empty line or `quit` ends the chat), appends it as a `user` turn, sends the whole list, and logs the usage.
- If `stop_reason` isn't `end_turn`, it stops without storing a reply the customer never got. Otherwise it appends `{"role": "assistant", "content": response.content}`: every block exactly as returned, thinking included, never rebuilt from the text.
- It prints the text, the turn's input and output tokens, and how many messages it keeps. At the end, the roles in order.

At the `You:` prompts, type the lesson's three questions (or your own), then `quit`:

```text
Hi, I'm Elijah. Can I cancel order HL-10196 before it ships?
And if it already shipped?
How long will the refund take?
quit
```

In the lesson:

| Turn | Answer (from the refund policy) | Input tokens | Messages kept |
|---|---|---|---|
| 1 | Yes, a full refund, shipping included | 676 | 2 |
| 2 | It can't be cancelled once shipped; return it within 30 days of delivery | 754 | 4 |
| 3 | Back to the original payment method within 5 business days | 884 | 6 |

Then `History: user, assistant, user, assistant, user, assistant`. Turn 2 is only answerable because turn 1 is in the history. And the input grows every turn, because every turn re-sends everything before it: 754 − 676 is turn 1's 68-token reply plus the new question. No turn thought in the lesson's run; if one does on yours, its thinking block rides along as input on every later turn too (Claude Haiku 5.5 keeps earlier thinking in context).

### 4. Commit

```bash
git status --short
git add harborline/usage.py experiments/m1/read_response.py experiments/m1/conversation.py
git commit -m "Lesson 1.2: read responses, handle stop reasons, log usage"
git push
```

`git status --short` lists the three new files and no `runs/` folder: git ignores it, so the usage log stays on your machine. The commit adds the three files (`3 files changed, 158 insertions(+)`), and `git push` sends it to `origin`, your own private `harborline`. Your commit id will differ from the lesson's.

## Windows, macOS and Linux

`git`, `code` and the `python -m experiments...` commands are the same on every system (run them with the environment active). Only one differs:

| Step | Linux and macOS (the lesson) | Windows |
|---|---|---|
| Clear the terminal, then run | `clear; python -m experiments.m1.read_response plain` | PowerShell: the same line works. cmd.exe: `cls & python -m experiments.m1.read_response plain` |

Clearing is only for a tidy screen; you can also run the `python -m ...` command on its own.

- **Windows:** `code harborline/usage.py` works with forward slashes in PowerShell. If your venv's `python` isn't found, activate the environment first (`.venv\Scripts\Activate.ps1`, Lesson 0.6).
- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**; go to a line with **Ctrl+G**).
- **WSL:** run the Linux commands inside the WSL terminal, in your WSL home folder.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` | Nothing printed (clean tree) |
| `read_response plain` | `[thinking] 0 characters, signature 980 characters`; a two-sentence `[text]`; `input_tokens` 68, `output_tokens` 104 (`thinking_tokens` 44), cache fields 0; `stop_reason: end_turn`; `next step: done: use the text`; about $0.000059 |
| `read_response tool` | `[tool_use] lookup_order {'order_id': 'HL-10196'}`, no thinking, no text; `input_tokens` 443, `output_tokens` 55; `stop_reason: tool_use`; `next step: run the tool, then send its result back (Lesson 1.3)`; about $0.000072 |
| `runs/usage.jsonl` | Two lines with `request_id`, tokens and `cost_usd` (`5.88e-05`, `7.18e-05`) |
| `conversation` | Input 676 / 754 / 884 tokens; 2 / 4 / 6 messages kept; 0 thinking each turn; `History: user, assistant, user, assistant, user, assistant` |
| `git commit` | `3 files changed, 158 insertions(+)` |
| `git push` | `main -> main` to your own `harborline` |
| API spend | About five hundredths of a cent on Claude Haiku 5.5 |

Your replies, token counts, thinking and IDs will differ from these, run to run. See `expected-output.md` for what should match.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'harborline'`**: you ran a file directly (`python experiments/m1/read_response.py`). Run it as a module, from the `harborline` folder: `python -m experiments.m1.read_response plain`.
- **`ImportError: cannot import name 'log_usage' from 'harborline.usage'`** or **`No module named 'harborline.usage'`**: `usage.py` isn't saved in the package folder. It belongs next to `config.py` and `costs.py`, and the file must be saved.
- **`ModuleNotFoundError: No module named 'anthropic'`** or **`python: command not found`**: the environment isn't active in this terminal. Activate it (Lesson 0.6); the prompt should start with `(.venv)`.
- **An error about the API key, or `401` `authentication_error`**: `.env` is missing, empty or not saved, or the key is incomplete or disabled. Run `python -m scripts.check_setup`: it says which.
- **`AttributeError` on `_request_id` or `output_tokens_details`**: your `anthropic` package isn't the pinned 1.13.0. Run `pip install -r requirements.txt` with the environment active.
- **`KeyError` in `estimate_cost`**: the reply's model isn't in `costs.PRICES`, for example because `MODEL` in `config.py` was changed. The cost lookup fails on purpose rather than guess a price; the call itself already ran. Put `MODEL` back to `claude-haiku-5-5`.
- **A `KeyError` naming your case, such as `'tools'`**: the case name is misspelled. Use `plain` or `tool`.
- **The `plain` case has no `[thinking]` line**: Claude Haiku 5.5 decides per request whether to think. Run it again, or move on: the point is the same.
- **The `tool` case answers in text instead of calling the tool**, or prints a short `[text]` line before `[tool_use]`: Claude decides when to call a tool. A text line before the call is fine. If there's no `[tool_use]` at all, `stop_reason` says `end_turn`; run it again.
- **`stop_reason: max_tokens`**: the reply was cut off. `next_step()` says so and doesn't use it. Check that `MAX_TOKENS` in `config.py` is still 1024.
- **The chat prints `Stopped: …` and ends**: a turn ended with something other than `end_turn`, so the reply wasn't stored. Start the chat again.
- **`400` `invalid_request_error` on turn 2 or 3**: the history changed between requests. Append `response.content` exactly as it came back, keep the system prompt the same, and never edit or rebuild earlier turns.
- **`429` `rate_limit_error`, or `529` `overloaded_error`**: wait a minute and run again.
- **`runs/` or `usage.jsonl` shows up in `git status`**: `.gitignore` must list `runs/` (it does in the Harborline starter). The usage log is never committed.
- **`cost_usd` looks like `5.88e-05`**: that's dollars in scientific notation: 0.0000588.
- **Your numbers differ from the lesson's**: that's expected. Replies, thinking and token counts change from run to run, and every ID is new.
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6).
- **Never paste your API key into code or into a chat.** If a key leaks, disable it in the Console first, then create a new one (Lesson 0.4). The request ID and the message ID aren't secrets: they identify a call, and support asks for the request ID.

## Key terms

- **Content block:** one typed piece of a reply (`thinking`, `text`, `tool_use`, …). `content` is a list of them: read them by `type`, never by position.
- **Thinking block:** Claude's reasoning before it answers. On Claude Haiku 5.5 its text comes back empty by default, with a `signature` you send back unchanged; its tokens are billed as output.
- **`stop_reason`:** why Claude stopped this turn (`end_turn`, `tool_use`, `max_tokens`, `pause_turn`, `refusal`, and two more). Your code decides the next step from it.
- **Usage:** the reply's token counts, what you're billed for: `input_tokens` (the part not cached), cache writes and reads, and `output_tokens` (thinking included).
- **Request ID:** the `request-id` response header (`req_…`; `_request_id` in the Python SDK) that names one API call. Log it, and give it to support.

## Sources (checked 2026-10-14)

- Stop reasons and fallback (every `stop_reason`, the Quick reference table, `pause_turn`'s default limit of 10 iterations, a refusal is a normal HTTP 200 response): https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
- Refusals and fallback (what a refusal looks like, `stop_details.category`, discard partial output, `reasoning_extraction`: change the prompt rather than retry, Claude Haiku 5.5 has no server-side fallback): https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback
- API errors, request ID (the `request-id` header, `_request_id` in the Python and TypeScript SDKs): https://platform.claude.com/docs/en/api/errors#request-id
- Python SDK (request IDs): https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python
- Prompt caching (`input_tokens` counts only the tokens after the last cache breakpoint; total input = cache reads + cache writes + `input_tokens`): https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- API reference, create a message (the response: `id`, `content` blocks, `stop_reason`, `stop_details`, `usage`; consecutive same-role turns are combined): https://platform.claude.com/docs/en/api/messages/create
- Claude Haiku 5.5 migration guide (read blocks by type; thinking blocks from earlier turns stay in context and count as input; keep conversations append-only): https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide
- Thinking (thinking blocks, the signature, billed as output): https://platform.claude.com/docs/en/build-with-claude/thinking
- Server tools (the server-side loop and `pause_turn`): https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools
- Pricing (Claude Haiku 5.5: $0.10 per million input tokens, $0.50 per million output tokens; the tool-use system prompt): https://platform.claude.com/docs/en/about-claude/pricing
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.1 (Domain 1), Task Statement 5.1 (Domain 5), and Scenario 1: Customer Support Resolution Agent

Models and APIs change. If a number or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 1.3 you run the `lookup_order` tool for real and send its result back.
