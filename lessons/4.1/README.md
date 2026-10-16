# Student kit: Lesson 4.1, Coordinators and subagents

Claude Certified Architect – Foundations (CCAR-F) · Module 4: Multi-Agent Systems: the Research Pipeline · Lesson 4.1

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Build a coordinator with subagents
2. Brief subagents with everything
3. Pick subagents by the question

## What's in the kit

| File | What it is |
|---|---|
| `research/tools.py` | New: the two research tools, served in-process to the Agent SDK. `search_web` keyword-matches the 14 sources in `data/research/` and returns up to 5 hits (title, URL, publisher, date, snippet); `fetch_url` returns one page in full by its URL, or an error for a URL it doesn't have. `server = create_sdk_mcp_server("research", ...)` |
| `research/coordinator.py` | New: the coordinator, built with the Agent SDK. Two subagents as `AgentDefinition`s (`searcher` with `search_web`, `analyst` with `fetch_url`, both on Haiku); a `PreToolUse` hook, `spokes_only`, that denies the research tools to the coordinator itself; `tools=["Agent"]`. Each run prints every prompt the coordinator writes for a subagent, every tool call tagged with the subagent that made it, the answer, and `subagents: ... · turns · $` |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `research` folder into your `harborline` folder.

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lab 3 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv` (with `claude-agent-sdk` installed since Module 3), and `origin` pointing at your own private `harborline` on GitHub. The research corpus, `data/research/` (14 sources: 10 "web" pages and 4 Harborline documents), has been in the repository since the starter.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 25 minutes, most of it typing. **API spend:** the broad question costs about half a cent, each narrow one a tenth to a quarter of a cent; the whole lesson is about one cent. `python -m research.tools` makes no API call at all.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open.

### 1. The research tools

```bash
git status --short                       # prints nothing: a clean tree after Lab 3
mkdir research
code research/tools.py                   # type the file (or copy it from the kit), save
clear; python -m research.tools "return fee"
```

- **Our web is local.** `data/research/` holds 14 fixed sources on one question, so the same query always finds the same pages and a search costs nothing. Their domains end in `.example` on purpose: they aren't real sites. Four sources are Harborline's own documents, at `harborline://internal/...` addresses.
- **`search(query)`** scores every source by how many of the query's words (minus `COMMON` small words) appear in its title and page, and returns the best 5.
- **`fetch(url)`** returns one page by its URL, or raises `KeyError`.
- **`search_web` and `fetch_url`** are SDK tools (`@tool`): their descriptions are what the subagents read. An unknown URL comes back as an error result (`is_error`), not a crash.
- **`create_sdk_mcp_server("research", ...)`** puts both tools in one MCP server that runs inside your Python process. Inside the SDK their names are `mcp__research__search_web` and `mcp__research__fetch_url`.

**In the lesson:** five hits for "return fee", best match first (Meridian 2025, Retail Signals 2026-05, Consumer Pulse, Northgate, the Harborline customer survey).

### 2. The coordinator

```bash
code research/coordinator.py             # type the file (or copy it from the kit), save
```

- **`SEARCHER` and `ANALYST`** are `AgentDefinition`s: a `description` (the coordinator reads it to decide when to use the subagent), a `prompt` (the subagent's own system prompt), `tools` (one each) and `model="haiku"`.
- **`spokes_only`** is a `PreToolUse` hook on the research tools. A call made inside a subagent carries an `agent_id` and is allowed; without one, the call comes from the coordinator, and it's denied with a reason ("Delegate with the Agent tool"). A system prompt can ask the coordinator not to search; the hook makes it hold.
- **`OPTIONS`**: the coordinator's system prompt (don't search or read yourself; use only the subagents the question needs; they know only what you write in their prompt, so include the question and every URL or fact; use only what they report; at most eight lines, citing URLs), `agents=`, `mcp_servers=`, `tools=["Agent"]` (the tool that starts a subagent), `allowed_tools=["Agent"] + RESEARCH_TOOLS`, the hook, `permission_mode="dontAsk"`, no settings files, `env={"CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "1"}` so subagents run in the foreground and the coordinator waits for each report, at most 10 turns and $0.10.
- **`main(question)`** reads the message stream. `parent_tool_use_id` says where a message comes from (`None`: the coordinator). Each `Agent` call prints `-> <subagent> gets only this prompt:` and the prompt in full; every other tool call prints `[<subagent>] <tool> <input>`; at the end, the answer and `subagents: ... · <turns> turns · $<cost>`.

### 3. One question, two subagents

```bash
clear; python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs/research.log
```

`2> runs/research.log` keeps Claude Code's connectors notice out of the output. **In the lesson:** the searcher's prompt (the question restated for an online home-goods retailer, three things to look for, how to search), nine searches; then the analyst's prompt with six URLs, written out by the coordinator, and six fetches (one URL, an EU law page, isn't in our local web, so that fetch returned an error, and the answer says it didn't load); an answer with a source on each point and a caution that every domain ends in `.example`; `subagents: searcher, analyst · 3 turns · $0.0057`.

### 4. Only what the question needs

```bash
clear; python -m research.coordinator "What return rate does https://meridian-institute.example/reports/returns-benchmark-2025 report?" 2> runs/research.log
clear; python -m research.coordinator "Which sources cover return fraud? Just list them." 2> runs/research.log
```

**In the lesson:** the question with a URL went to the analyst only (one fetch; 17.6% of units, January to September 2025, and four category rates; `subagents: analyst · 2 turns · $0.0012`). The list question went to the searcher only (six searches; five sources, of which the coordinator said only the first is clearly about return fraud; `subagents: searcher · 2 turns · $0.0024`).

### 5. Commit

```bash
clear; git status --short
git add research
git commit -m "Lesson 4.1: a research coordinator with two subagents"
git push
```

`git status --short` shows `?? research/`; `runs/research.log` stays out (`runs/` is git-ignored). The commit has `2 files changed, 187 insertions(+)`. Your commit ID will differ from the lesson's.

## How it fits together

| Who | Gets | Does | Returns |
|---|---|---|---|
| Coordinator | The user's question, its system prompt, the subagents' descriptions | Picks subagents, writes each one's prompt, writes the answer | The answer |
| `searcher` | Its own system prompt, `search_web`, and the coordinator's prompt: nothing else | Searches | A short list of sources (its final message only) |
| `analyst` | Its own system prompt, `fetch_url`, and the coordinator's prompt: nothing else | Reads the pages it was given | Facts with their URLs (its final message only) |

The subagents never talk to each other: when the searcher finds a URL, the analyst sees it only if the coordinator writes it into the analyst's prompt. That's hub-and-spoke. `num_turns` counts the coordinator's turns; the subagents' work happens inside them, and the cost includes the subagents. The exam guide calls the subagent tool `Task`, its older name; current SDK versions show `Agent` in `tool_use` blocks.

## Windows, macOS and Linux

`git`, `code`, `mkdir` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m research.coordinator "..." 2> runs/research.log` | the same line | `cls`, then `python -m research.coordinator "..." 2> runs\research.log` on its own line |

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `python -m research.tools "return fee"` | five hits, no API call |
| the broad question | searcher, then analyst; `3 turns · $0.0057` |
| a question that names its page | analyst only; `2 turns · $0.0012` |
| "Just list them" | searcher only; `2 turns · $0.0024` |
| `git commit` | `2 files changed, 187 insertions(+)` |

The wording, the searches and the chosen URLs differ on every run. In every practice run before filming, the shape held: both subagents for the broad question, the analyst alone for the question with a URL, the searcher alone for the list question.

## Troubleshooting

- **The coordinator answers without any `->` lines**: check `tools=["Agent"]`. With `tools=[]` the coordinator has no Agent tool and can't delegate.
- **`[coordinator] search_web ...` appears**: the coordinator tried a research tool itself. The `spokes_only` hook denies it (the reason is in the result), and the coordinator then delegates. Check the hook's `matcher` if it doesn't.
- **"I don't have the result yet" and the run ends**: the subagent ran in the background. Keep `env={"CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "1"}` in the options.
- **Don't use `disallowed_tools` for the research tools**: it removes them for the subagents as well.
- **`ModuleNotFoundError: No module named 'research'`**: run from the `harborline` folder with `python -m research.coordinator`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Coordinator:** the agent that plans, delegates to subagents, and writes the answer; the hub everything goes through.
- **Subagent:** a separate agent the coordinator starts for one focused task, with its own prompt, tools and context.
- **Hub-and-spoke:** subagents talk only to the coordinator, never to each other; the coordinator routes every result.
- **Isolated context:** a subagent starts fresh, with only its own system prompt and the coordinator's prompt, none of the coordinator's conversation.
- **Agent tool:** the tool a coordinator calls to start a subagent (`subagent_type` + `prompt`); the exam guide calls it Task.

## Sources (checked 2026-10-15)

- Agent SDK docs, *Subagents in the SDK*: context isolation ("only its final message returns to the parent"; "The parent receives a concise summary"); what subagents inherit ("The only content you pass from parent to subagent is the Agent tool's prompt string"); automatic invocation ("Claude automatically decides when to invoke subagents", based on each subagent's `description`); subagents run in the background by default; the tool appears as `Agent` in `tool_use` blocks and as `Task` in the `system:init` tools list: https://code.claude.com/docs/en/agent-sdk/subagents
- Claude Code docs, *Tools reference*: `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` turns off the background task features: https://code.claude.com/docs/en/tools-reference
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.2 (hub-and-spoke architecture where the coordinator manages all inter-subagent communication, error handling and information routing; subagents with isolated context; the coordinator deciding which subagents to invoke). Scenario 3: Multi-Agent Research System.

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 4.2: subagents in the Agent SDK, up close: the definitions, the Agent tool, and structured findings.
