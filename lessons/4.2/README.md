# Student kit: Lesson 4.2, Subagents in the Agent SDK

Claude Certified Architect – Foundations (CCAR-F) · Module 4: Multi-Agent Systems: the Research Pipeline · Lesson 4.2

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Define subagents with AgentDefinition
2. Give the coordinator the Agent tool
3. Pass findings as structured data

## What's in the kit

| File | What it is |
|---|---|
| `research/agents.py` | New: the three research subagents, each an `AgentDefinition` (description, prompt, tools, model), defined once and shared. `SEARCHER` finds sources with `search_web`; `ANALYST` reads pages with `fetch_url` and returns findings as a JSON array (`claim`, `evidence`, `url`, `publisher`, `published`, `method`); `SYNTHESIZER` has no tools (`tools=[]`) and writes the answer only from the findings in its prompt. `AGENTS` names all three |
| `research/coordinator.py` | Changed: imports `AGENTS` instead of defining subagents inline; its system prompt says the research tools work on a saved copy of the web, names the three subagents, and asks for the analyst's findings to be passed to the synthesizer complete and unchanged; it prints the init message's tool list, and shows a handed-over JSON array as one line |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `research` folder into your `harborline` folder (it adds `agents.py` and replaces `coordinator.py`; `tools.py` stays).

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 4.1 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, `research/tools.py` and `research/coordinator.py` committed, and `origin` pointing at your own private `harborline` on GitHub.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 20 minutes, most of it typing. **API spend:** the run in step 3 cost about one and a half cents in the lesson (the coordinator and three subagents, all on Haiku 5.5).

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, **Ctrl+G** jumps to a line, and **Ctrl+L** selects the whole line.

### 1. Three definitions

```bash
git status --short                       # prints nothing: a clean tree after Lesson 4.1
code research/agents.py                  # type the file (or copy it from the kit), save
```

An `AgentDefinition` is one subagent, in four fields:

- **`description`**: when to use it. The coordinator reads the descriptions and picks subagents by them.
- **`prompt`**: how it works. It becomes the subagent's system prompt.
- **`tools`**: what it may use. An empty list means no tools at all; leaving the field out means the subagent inherits every tool available to subagents.
- **`model`**: the model that runs it (`"haiku"` here).

The analyst's prompt fixes the shape of its findings: one JSON object per finding, the content (`claim`, `evidence`) apart from the source's metadata (`url`, `publisher`, `published`, `method`).

### 2. The coordinator uses them

```bash
code research/coordinator.py             # change it in place, save
```

Starting from Lesson 4.1's `coordinator.py` (110 lines), the lesson makes these changes, top to bottom (the kit's file is the result, 115 lines):

1. Line 1 of the docstring: a hub with **three** subagents.
2. `import json`, after `import asyncio`.
3. The SDK import: `SystemMessage` in, `AgentDefinition` out (the definitions live in `agents.py` now).
4. `from research.agents import AGENTS`.
5. The 17 lines of inline `SEARCHER` and `ANALYST` definitions: deleted.
6. The system prompt: the research tools work on a saved copy of the web (every URL ends in `.example`); the three subagents; give the synthesizer the analyst's findings complete and unchanged, the whole JSON, never a summary; at most eight lines; the answer is the synthesizer's.
7. `agents=AGENTS` in the options. `tools=["Agent"]` and `allowed_tools=["Agent"] + RESEARCH_TOOLS` stay as they were: the Agent tool is how the coordinator starts a subagent.
8. A new helper, `findings(text)`: the JSON list of objects in a prompt, if there is one.
9. `show(prompt)`: prints the text before the list, then one line in place of the list: how many findings, and their keys. Only the printout is shortened; the prompt itself is passed on untouched.
10. In `main()`: when the `SystemMessage` with subtype `init` arrives, print the coordinator's tools.

### 3. Findings handed over whole

```bash
clear; python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs/research.log
```

- **`coordinator tools: Task, ...`**: the init message's tool list still calls the Agent tool `Task`, its older name (the exam guide says `Task` too). Tool calls name it `Agent`, which is what `main()` matches.
- Each subagent's prompt is printed as the coordinator wrote it: everything that subagent knows about the job.
- The synthesizer's prompt ends with the findings, complete: our printout shows them as one line, `[ 21 findings as JSON, keys: ... ]` in the lesson.
- **`2> runs/research.log`** keeps Claude Code's connectors notice out of the output.

**In the lesson:** searcher (five searches), analyst (seven fetches), synthesizer (no tools); a conditional answer, each claim with its publisher and date; `subagents: searcher, analyst, synthesizer · 4 turns · $0.0147`.

### 4. Commit

```bash
clear; git status --short
git add research
git commit -m "Lesson 4.2: subagent definitions in one file, and findings handed over as JSON"
git push
```

`git status --short` shows `coordinator.py` changed and `agents.py` new. The commit has `2 files changed, 75 insertions(+), 29 deletions(-)`. Your commit ID will differ from the lesson's.

## Hand-overs: summary or structured findings

| Hand-over | What the next subagent gets |
|---|---|
| A summary the coordinator writes | A paraphrase: dates, publishers and methods can be dropped or attached to the wrong claim, and the next subagent can't cite what it never saw |
| The complete findings as structured data | Every claim with its evidence, and its source's URL, publisher, date and method in fields of their own |

A subagent knows only its own definition and the prompt it's given. Anything it needs (file paths, error messages, decisions, earlier findings) has to be in that prompt.

## Windows, macOS and Linux

`git`, `code` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m research.coordinator "..." 2> runs/research.log` | the same line | `cls`, then `python -m research.coordinator "..." 2> runs\research.log` on its own line |

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| init tool list | `coordinator tools: Task, mcp__research__fetch_url, mcp__research__search_web` |
| subagents used | searcher, analyst, synthesizer (in that order) |
| the hand-over | `[ 21 findings as JSON, keys: claim, evidence, url, publisher, published, method ]` |
| the run | 4 turns, $0.0147 |
| `git commit` | `2 files changed, 75 insertions(+), 29 deletions(-)` |

In the three practice runs before filming, every run used all three subagents, with 17 to 21 findings. In an earlier run without the saved-web sentence, the coordinator took the `.example` URLs for fakes, sent the searcher out twice and never answered: the coordinator, too, knows only what its prompt tells it.

## Troubleshooting

- **`subagents: none`, and the coordinator answers by itself**: check the system prompt's "Use only what they report, never your own knowledge", and that `tools` and `allowed_tools` both include `"Agent"`.
- **`subagents: searcher, searcher` and no answer**: the coordinator distrusted the `.example` URLs. Check the sentence about the saved copy of the web in the system prompt.
- **No `[ N findings as JSON, ... ]` line**: the coordinator passed the findings as prose, or the analyst didn't return a JSON array. Check the analyst's prompt in `agents.py` and the hand-over sentence in the system prompt, then run again.
- **`ModuleNotFoundError: No module named 'research'`**: run from the `harborline` folder with `python -m research.coordinator`.
- **`ImportError: cannot import name 'AGENTS'`**: save `research/agents.py` first; check the spelling of `AGENTS`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **AgentDefinition:** a subagent's definition: description, prompt, tools and model.
- **Description:** tells the coordinator when to use the subagent; it picks by description.
- **Agent tool:** how the coordinator starts a subagent; named `Task` in older docs and in the init tool list.
- **Structured findings:** each claim as data (claim and evidence) with its source's metadata (URL, publisher, date, method) in separate fields.
- **Hand-over:** passing one subagent's complete output into the next subagent's prompt, unchanged.

## Sources (checked 2026-10-15)

- Agent SDK docs, *Agent SDK reference - Python*, `AgentDefinition`: "Configuration for a subagent defined programmatically"; `description`, "Natural language description of when to use this agent"; `tools`, omitted means every tool available to subagents: https://code.claude.com/docs/en/agent-sdk/python
- Agent SDK docs, *Subagents in the SDK*: the only content passed from parent to subagent is the Agent tool's prompt string, so "include any file paths, error messages, or decisions" the subagent needs; the tool "appears as "Agent" in tool_use blocks but as "Task" in the system:init tools list": https://code.claude.com/docs/en/agent-sdk/subagents
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 1.3 (`AgentDefinition` with descriptions, system prompts and tool restrictions; the coordinator's `allowedTools` must include "Task"; complete findings in the subagent's prompt; structured data that separates content from metadata). Scenario 3: Multi-Agent Research System.

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 4.3: subagents in parallel, how to scope each one, and how to refine what they find.
