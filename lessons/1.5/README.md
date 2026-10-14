# Student kit: Lesson 1.5, Who decides: model-driven agents vs fixed workflows

Claude Certified Architect – Foundations (CCAR-F) · Module 1: Claude API Foundations for Architects · Lesson 1.5

This kit holds everything you need to repeat the lesson on your own computer: the two Python files written in the lesson, every command in order, what each run printed in the lesson, the one command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Tell who decides the next step: Claude or your code
2. Match a task to chaining, routing or orchestrator-workers
3. Choose the simplest design that meets the requirement

## What's in the kit

| File | What it is |
|---|---|
| `loop/workflow.py` | Steps 1 and 2: Harborline's fixed routing workflow. `ROUTE` (the `route_ticket` tool: Claude fills it in, nobody runs it), `ROLE` and `TASKS` (one specialized prompt per route; only the refund route carries the refund policy), `HUMAN` (anything without a fixed path goes to people), `route()` (step 1: a forced tool call, read as a label), `write()` (step 3: one reply from the facts, no tools) and `handle()`, the chain that ties them together. Run on its own, it handles one ticket and prints the route, the orders it checked, the number of model calls and the reply |
| `experiments/m1/who_decides.py` | Step 3: the same five tickets through both designs, this lesson's workflow and Lesson 1.4's agent. One row per ticket and design (model calls, how many of the ticket's orders it looked up), then token and cost totals per design |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each run printed in the lesson, line by line, and what will differ on yours |

The two files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them; if you'd rather not, copy the kit's `loop` and `experiments` folders into your `harborline` folder, so that you have `harborline/loop/workflow.py` and `harborline/experiments/m1/who_decides.py`. Lesson 1.4's `loop/agent.py` and Lesson 1.3's `loop/tools.py` stay exactly as they are.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 1.4 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv` (`anthropic` 1.13.0, `python-dotenv` 1.2.4, `pytest` 9.1.1), `pytest` passing, `origin` pointing at your own private `harborline` on GitHub, Lesson 1.2's usage logger (`harborline/usage.py`), Lesson 1.3's tools (`loop/tools.py`) and Lesson 1.4's loop (`loop/agent.py` with `first_message`, `run` and `LoopStopped`). `workflow.py` borrows `first_message` from the agent; `who_decides.py` runs the agent itself.
- **Your API key in Harborline's `.env`** (Lesson 0.6, step 3). `python -m scripts.check_setup` should say `ANTHROPIC_API_KEY is set`. The scripts load the key from `.env` and never print it.
- About 25 minutes, most of it typing. The lesson's API spend was **under a cent** on Claude Haiku 5.5: two single tickets through the workflow (two short calls each) and one comparison run (29 calls in all).

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder: the scripts are run as modules (`python -m loop.workflow`), so they can import Harborline's shared code and each other.

### 1. Fix the path

```bash
git status --short          # prints nothing: a clean tree after Lesson 1.4
code loop/agent.py          # a quick look at Lesson 1.4's run(): tools=TOOLS, Claude picks each step
code loop/workflow.py       # type the file (or copy it from the kit), save
clear; python -m loop.workflow T-008
```

In the lesson, **Ctrl+J** hides the terminal panel while the file is typed, so the editor gets the full height, and **Ctrl+`** brings the terminal back. What `loop/workflow.py` holds, top to bottom:

- **The docstring**: the whole idea. Our code decides every step; Claude fills in one label, then writes one reply.
- **`ROUTE`** (lines 22-35): a tool definition, `route_ticket`, that Claude will never run. Its description names the three categories (status: where an order is; refund: returning an item; other: anything else), and its `enum` limits the answer to `status`, `refund` or `other`. A decision you'd otherwise parse out of text lives in a tool input instead (Lesson 1.4's rule from the docs).
- **`ROLE`** (lines 36-40): a shared opening for every reply, three sentences or fewer, with Harborline's fixed "today".
- **`TASKS`** (lines 41-45): one specialized prompt per route. Only `refund` carries the refund policy: each path gets only what it needs.
- **`HUMAN`** (line 46): the answer when there's no fixed path. People take it.
- **`route(client, ticket)`** (lines 49-58), step 1: one request whose only tool is `ROUTE`, with `tool_choice={"type": "tool", "name": "route_ticket"}`, which forces that call. Our code decides the call happens; Claude only fills in the label. The function reads `input["route"]` from the `tool_use` block, logs the usage and returns. No `tool_result` ever goes back: the call's input is the answer. (`tool_choice` has more settings, and not every model accepts a forced tool; Lesson 2.3 covers both. Claude Haiku 5.5 accepts it, and a forced call skips thinking.)
- **`write(client, name, ticket, facts)`** (lines 61-70), step 3: no `tools` at all, so here Claude can only write: from `ROLE`, this route's task, and the facts our code fetched.
- **`handle(client, ticket)`** (lines 73-87), the chain: step 1, route; then a gate (no fixed path, or no order number, and the ticket goes to people); step 2, always the same two lookups, `get_customer` then `lookup_order`, run by our code; step 3, one reply. The regex takes the **first** order ID only. That's prompt chaining (fixed steps, each feeding the next, with checks in code between), with routing at the front.
- **The `__main__` block** (lines 90-96): one ticket from the command line; prints the route, the orders checked, the number of calls and the reply.

**T-008**: Elijah asks where order HL-10196 is. In the lesson: `route: status  orders checked: ['HL-10196']  calls: 2`, and the reply said it shipped with Parcelway and is due tomorrow, October 16, by the carrier's estimate. Two calls: one to label, one to write. Claude never chose a tool; our code looked up the customer and the order, as the status path always does.

### 2. Where the path ends

```bash
clear; python -m loop.workflow T-004
```

**T-004**: Lorenzo asks three things at once: return the LED desk lamp from HL-10164, where is his other order HL-10203, and how long do refunds take? In the lesson: `route: refund  orders checked: ['HL-10164']  calls: 2`. The lamp: delivered October 3, so it's eligible, and $48 would go back to the card ending 8423 within 5 business days. The second order? "I can't see order HL-10203 in the information I have": our code never looked it up. One label, one path, one order. Tested alone, the router returned three `route_ticket` blocks for this ticket (refund, status, other): it saw all three requests, and our code reads the first. You could add a branch for two orders, then three, then none: that's how decision trees grow, and when the branches keep multiplying, the steps can't be predicted. That's the agent's job.

### 3. Measure, then decide

```bash
code experiments/m1/who_decides.py              # type the file (or copy it), save
clear; python -m experiments.m1.who_decides
```

What `who_decides.py` holds: imports (two helpers to silence printing, `Counter` for the totals, the client, Harborline's data, `estimate_cost` from Lesson 0.6, and both designs). `TICKETS`: the same five dev tickets (status, refund, a cracked mirror, a billing question with no route, and the three-in-one). `LABELS`: each ticket's real order IDs. `tally()` prints one row per design: the model calls and how many of the ticket's orders it looked up (a rough coverage check, not a quality score), then adds up tokens and cost from each response's `usage`. The loop runs the workflow on each ticket, then Lesson 1.4's agent on the same one with its turn printout silenced; if the agent ever stops on something other than `end_turn`, the script catches `LoopStopped`, records the row and goes on. The agent's lookups come from its `tool_use` blocks: what Claude chose to call. Last, one totals line per design.

In the lesson (the rows print as each ticket finishes, about 50 seconds in all):

- T-008, T-003, T-014: the workflow took 2 calls, the agent 3, and both looked up the order.
- T-006 is a billing question about a shipping fee. There's no billing route, so the router called it `status`. In practice runs it once said `other` instead.
- T-004: the workflow looked up 1 order out of 2; the agent made three tool calls and looked up both.
- Totals: **workflow** 10 calls, 10,553 tokens, $0.0024, orders 5/6; **agent** 15 calls, 26,465 tokens, $0.0039, orders 6/6. The workflow used about 40% of the agent's tokens.

Same model, tickets and policy; the agent carries its tools and history on every call. Five tickets are an illustration, not a benchmark. Then decide: if the requirement is answering order-status questions, the workflow meets it with fewer tokens and a predictable path. Harborline's real inbox is open-ended, and there the agent earns its extra calls. Or combine them: predictable tickets down a fixed path, the rest to the agent. The simplest design that meets the requirement, and a measurement to prove it.

### 4. Commit

```bash
git status --short          # ?? experiments/m1/who_decides.py   ?? loop/workflow.py
git add loop/workflow.py experiments/m1/who_decides.py
git commit -m "Lesson 1.5: a fixed routing workflow next to the agent"
git push
```

The commit adds the two files (`2 files changed, 154 insertions(+)`), and `git push` sends it to `origin`, your own private `harborline`. Your commit id will differ from the lesson's. `runs/` doesn't show up in `git status`: it's ignored, and its usage log now holds this lesson's calls too, labelled `1.5 workflow` and `1.4 agent`.

## Windows, macOS and Linux

`git`, `code` and the `python -m ...` commands are the same on every system (run them with the environment active). Only one line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m loop.workflow T-008` | the same line | `cls`, then `python -m loop.workflow T-008` on its own line |

The same goes for the T-004 run and for `python -m experiments.m1.who_decides`.

- **Windows:** `code loop/workflow.py` works with forward slashes in PowerShell. If your venv's `python` isn't found, activate the environment first (`.venv\Scripts\Activate.ps1`, Lesson 0.6).
- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, and **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal, in your WSL home folder.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `git status --short` (start) | Nothing printed (clean tree) |
| `python -m loop.workflow T-008` | `route: status  orders checked: ['HL-10196']  calls: 2`; shipped with Parcelway, estimated October 16, one day after the promised October 15 |
| `python -m loop.workflow T-004` | `route: refund  orders checked: ['HL-10164']  calls: 2`; the lamp is eligible ($48 to the card ending 8423); "I can't see order HL-10203" |
| `python -m experiments.m1.who_decides` | Workflow 2 calls per ticket, agent 3; orders 1/1 for both on four tickets; T-004 workflow 1/2, agent 2/2; totals workflow 10 calls, 10,553 tokens, $0.0024, 5/6; agent 15 calls, 26,465 tokens, $0.0039, 6/6 |
| `git commit` | `2 files changed, 154 insertions(+)` |
| `git push` | `main -> main` to your own `harborline` |
| API spend | Under a cent on Claude Haiku 5.5 |

Your routes, replies, token counts and costs can differ from these, run to run. See `expected-output.md` for what should match.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'loop'`** or **`'harborline'`**: you ran a file directly (`python loop/workflow.py`), or you're not in the `harborline` folder. `cd ~/projects/harborline` and run it as a module: `python -m loop.workflow T-008`.
- **`ImportError: cannot import name 'first_message' from 'loop.agent'`** (or `run`, `LoopStopped`): Lesson 1.4's `loop/agent.py` is missing or different. Do Lesson 1.4 first, or copy its kit's `loop/agent.py`.
- **`ModuleNotFoundError: No module named 'harborline.usage'`**: Lesson 1.2's `harborline/usage.py` is missing. Do Lesson 1.2 first: it writes that file.
- **`IndexError: list index out of range`**: you left out the ticket id. Run `python -m loop.workflow T-008`.
- **`No ticket T-08`**: the ticket id is misspelled. Harborline's tickets are `T-001` to `T-050`, with three digits.
- **`ModuleNotFoundError: No module named 'anthropic'`** or **`python: command not found`**: the environment isn't active in this terminal. Activate it (Lesson 0.6); the prompt should start with `(.venv)`.
- **An error about the API key, or `401` `authentication_error`**: `.env` is missing, empty or not saved, or the key is incomplete or disabled. Run `python -m scripts.check_setup`: it says which. Create a new key in the Console if you need one (Lesson 0.4).
- **`400` `invalid_request_error` about `tool_choice` or forced tool use**: some models don't accept a forced tool (Lesson 2.3 lists them). The lesson uses Harborline's model, Claude Haiku 5.5, from `harborline/config.py`; if you changed `MODEL`, change it back.
- **`route: other  orders checked: []  calls: 1` and `(sent to the human queue)`**: the router chose `other`, or the ticket has no order number, so the gate sent it to people. That's the designed path, not a bug. Routes can vary run to run, especially on a ticket like T-006 that fits no route.
- **A row like `T-004  agent     calls 0  orders 0/2  stopped on max_tokens`**: the agent stopped on `max_tokens` (Lesson 1.4's `LoopStopped`), and the script recorded the row and went on, as it's written to do. That run's tokens aren't in the agent's total. Run the comparison again if you want a full table.
- **Your numbers differ from the lesson's**: expected. Token counts, costs and even routes change from run to run; the shape (the workflow cheaper and predictable, the agent covering more orders on the multi-request ticket) is what to look for.
- **The comparison seems stuck**: it makes about 25 real calls one after another. Each row appears when its ticket finishes; give it a minute.
- **`git push` is rejected or goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them. `git add loop/workflow.py experiments/m1/who_decides.py` adds only the two new files.
- **Never paste your API key into code or into a chat.** If a key leaks, disable it in the Console first, then create a new one (Lesson 0.4).

## Key terms

- **Workflow:** a system where your code fixes the steps and their order in advance. Claude may be called at any step, but it never picks the next one.
- **Agent:** a system where Claude decides its next action, such as which tool to call, from what it has learned so far, in a loop (Lesson 1.4's `loop/agent.py`).
- **Prompt chaining:** a fixed sequence of steps where each step uses the previous step's output, with checks in code ("gates") between steps.
- **Routing:** one step classifies the input, and the label sends it down a specialized path with its own prompt (and possibly its own tools or model).
- **Orchestrator-workers:** a central model breaks each task into subtasks it decides at run time, hands them to workers and combines their results. Module 4 builds it.

## Sources (checked 2026-10-14)

- Anthropic, *Building effective agents* (published December 19, 2024; its own note says much of the tooling has changed since, and the lesson uses only its definitions, patterns and advice): workflows are systems where LLMs and tools are "orchestrated through predefined code paths"; agents "dynamically direct their own processes and tool usage"; prompt chaining, routing (its example: directing different types of customer service queries), orchestrator-workers, parallelization and evaluator-optimizer; "finding the simplest solution possible"; "adding complexity only when it demonstrably improves outcomes": https://www.anthropic.com/engineering/building-effective-agents
- Ticket routing (use-case guide): Claude Haiku 5.5 suits ticket routing as the fastest and most cost-effective current model: https://platform.claude.com/docs/en/about-claude/use-case-guides/ticket-routing
- Subagents in the Agent SDK: Claude decides on its own when to spawn a subagent and how many to spawn: https://code.claude.com/docs/en/agent-sdk/subagents
- How tool use works, when to use tools and when not to (one-shot Q&A with no side effects needs no tools; a decision parsed from model output should have been a tool call): https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works
- Define tools, forcing tool use (`tool_choice` with `{"type": "tool", "name": ...}`; which models accept it; a forced call skips thinking): https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.1 and Task Statement 1.6 (Domain 1: Agentic Architecture & Orchestration), Scenario 1: Customer Support Resolution Agent and Scenario 3: Multi-Agent Research System

Models and APIs change. If a number or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 1.6, all of Module 1's exam traps on one page.
