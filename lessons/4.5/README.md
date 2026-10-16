# Student kit: Lesson 4.5, Distributing tools across agents

Claude Certified Architect – Foundations (CCAR-F) · Module 4: Multi-Agent Systems: the Research Pipeline · Lesson 4.5

This kit holds everything you need to repeat the lesson on your own computer: the files written in the lesson, every command in order, what each step printed in the lesson, the one kind of command that differs on Windows, and what to do when something goes wrong.

By the end of the lesson you can:

1. Give each subagent its role's tools
2. Swap generic tools for constrained ones
3. Add a scoped tool, route the rest

## What's in the kit

| File | What it is |
|---|---|
| `research/tools.py` | Changed: `FOUND` (the URLs `search_web` returned in this run); `fetch_url` is replaced by `load_document`, which loads only a source a search returned, returns the source's details (`url`, `publisher`, `published`, `method`) as JSON and then its text, and refuses anything else with an error that says what to do instead; a new `verify_fact(claim, url)` returns up to 3 sentences from that one source that match the claim, or none. The server offers three tools |
| `research/agents.py` | Changed: each subagent gets only its role's tools. `SEARCHER` keeps `search_web`; `ANALYST` gets `load_document` only (and copies `url`, `publisher`, `published` and `method` from the source's details); `SYNTHESIZER` gets `verify_fact` only (check each figure against its URL, drop what doesn't match, say at the end if a source is missing) |
| `research/coordinator.py` | Changed: `RESEARCH_TOOLS` lists `search_web`, `load_document` and `verify_fact`; the system prompt says the synthesizer checks figures, and if it says a source is missing, the coordinator sends a searcher for that only |
| `tests/test_research_tools.py` | New: four tests of the tools' limits, without calling Claude: `load` refuses a URL no search returned; it returns the details, then the text; `verify` finds the sentence behind "18%"; it finds nothing for an unrelated claim |
| `commands.txt` | Every command typed in the lesson, in order |
| `expected-output.md` | What each step printed in the lesson, and what will differ on yours |

The files are exactly the ones written in the lesson. Typing them yourself is the best way to learn them. If you'd rather not, copy the kit's `research` and `tests` folders into your `harborline` folder (they replace `tools.py`, `agents.py` and `coordinator.py`, and add `tests/test_research_tools.py`).

The video is filmed on Ubuntu 24.04. Every command is the same on Windows, macOS and Linux except one kind of line, under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 4.1 to 4.4 done**: your own `harborline` repository in `~/projects/harborline` with its `.venv`, the research pipeline (`research/tools.py`, `research/agents.py`, `research/coordinator.py`) committed, and `origin` pointing at your own private `harborline` on GitHub.
- **Your Anthropic API key in `.env`** as `ANTHROPIC_API_KEY` (Lessons 0.4 and 0.6). Never paste the key into a file you commit, and never print it.
- About 25 minutes, most of it typing. **API spend:** the run in step 4 cost about two and a half cents in the lesson (the coordinator and four subagents, all on Haiku 5.5). The tests in step 3 call no model and cost nothing.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Run everything from the `harborline` folder. In the lesson, **Ctrl+J** hides the terminal panel while a file is open, **Ctrl+G** jumps to a line, and **Ctrl+L** selects the whole line.

### 1. Constrained and scoped tools

```bash
git status --short                       # prints nothing: a clean tree after Lesson 4.4
code research/tools.py                   # change it in place, save
```

Starting from Lesson 4.1's `tools.py` (77 lines), the lesson makes these changes, top to bottom (the kit's file is the result, 119 lines):

1. The docstring: `search_web` finds sources; `load_document` returns one source that a search found, with its details; `verify_fact` checks one claim against one source.
2. `FOUND = set()`: the URLs that `search_web` returned in this run.
3. `fetch(url)` becomes `load(url)`: if the URL isn't in `FOUND` it raises `PermissionError`; otherwise it returns the source's details as JSON, a blank line, and the source's text.
4. A new `verify(claim, url)`: the source's sentences, sorted by how many words they share with the claim; the top three, but only those sharing at least three words. It is word overlap, not understanding: good enough to find the sentence behind a figure, not a fact checker.
5. `search_web` adds every URL it returns to `FOUND`.
6. The tool `fetch_url` becomes `load_document`, whose description states its limit: it loads only URLs a search returned in this run.
7. Its refusal: `... wasn't returned by search_web in this run. Load a URL from the search results.` An unknown URL gets `No source at ...`.
8. A new tool, `verify_fact`: one claim and one URL in; up to 3 matching sentences, or "No sentence in this source matches the claim."; it doesn't search or return whole pages.
9. The server offers `search_web`, `load_document` and `verify_fact`.

### 2. Each role its tools

```bash
code research/agents.py                  # change it in place, save
code research/coordinator.py             # change it in place, save
```

In `agents.py`: one sentence in the docstring ("Each gets only its role's tools."); `ANALYST`'s description, prompt (read sources with `load_document`; copy `url`, `publisher`, `published` and `method` from the source's details) and `tools=["mcp__research__load_document"]`; `SYNTHESIZER`'s description (it checks figures against their sources; it can't search or read), prompt (check each figure with `verify_fact` against its URL, drop what doesn't match, say at the end if a source is missing) and `tools=["mcp__research__verify_fact"]`. `SEARCHER` stays as it was.

In `coordinator.py`: `RESEARCH_TOOLS` lists the three research tools (`fetch_url` is gone from the whole pipeline), and the system prompt says the synthesizer "writes the answer from findings and checks their figures. If it says a source is missing, send a searcher for that only." The coordinator itself still has only the Agent tool, and Lesson 4.1's hook still denies it the research tools.

### 3. The limits, tested

```bash
code tests/test_research_tools.py        # type the file (or copy it from the kit), save
clear; python -m pytest -q tests/test_research_tools.py
python -m pytest -q
```

The refusal is proven here, in a test. A well-behaved analyst loads only what the searchers found, so a real run may never show a refusal: in both practice runs before filming, and in the filmed run, `load_document` never had to refuse.

### 4. One run

```bash
clear; python -m research.coordinator "Should Harborline charge customers a fee for return shipping?" 2> runs/research.log
```

- **Searchers** call only `search_web`.
- **The analyst** calls only `load_document`, each time with a URL the searchers returned.
- **The synthesizer** calls only `verify_fact`, each time with one claim and the URL it came from.
- **`2> runs/research.log`** keeps Claude Code's connectors notice out of the output.

**In the lesson:** two searchers together (15 searches), one analyst (11 `load_document` calls: 7 web sources and 4 of Harborline's own documents), one synthesizer (15 `verify_fact` calls); an answer that says not to add a blanket fee yet and to test a narrow one first; `subagents: searcher 1, searcher 2, analyst 1, synthesizer 1`; `120s in all · 5 turns · $0.0242`.

### 5. Commit

```bash
clear; git status --short
git add research tests
git commit -m "Lesson 4.5: each subagent gets only its role's tools: load_document for the analyst, verify_fact for the synthesizer"
git push
```

`git status --short` shows the three research files changed and the test file new. The commit has `4 files changed, 111 insertions(+), 31 deletions(-)`. Your commit ID will differ from the lesson's.

## Tools by role

| Role | Its tools | Why |
|---|---|---|
| Searcher | `search_web` | It finds sources; it doesn't read them |
| Analyst | `load_document` | It reads what a search found, and nothing else |
| Synthesizer | `verify_fact` | It writes the answer; it can check a figure against its source, but can't search or read whole pages |
| Coordinator | the Agent tool only | It routes; Lesson 4.1's hook denies it the research tools |

A tool you leave out of a subagent's `tools` isn't in its session at all. Leave the `tools` field out completely, and the subagent gets every tool available to subagents.

## Windows, macOS and Linux

`git`, `code` and `python -m ...` are the same on every system (run them with the environment active). Only one kind of line differs:

| Step | Linux and macOS (the lesson) | Windows PowerShell | Windows cmd.exe |
|---|---|---|---|
| Clear, then run | `clear; python -m ...` | the same line | `cls`, then the `python -m ...` command on its own line (and `runs\research.log` in step 4) |

- **macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (the terminal is still **Ctrl+`**, **Cmd+J** hides the panel).
- **WSL:** run the Linux commands inside the WSL terminal.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `pytest -q tests/test_research_tools.py` | `4 passed in 1.17s` |
| `pytest -q` (the whole suite) | `98 passed in 5.60s` |
| subagents used | `searcher 1, searcher 2, analyst 1, synthesizer 1` |
| tools called | `search_web` 15 times (searchers), `load_document` 11 times (analyst), `verify_fact` 15 times (synthesizer) |
| refusals | none: every URL the analyst loaded came from a search |
| the run | `120s in all · 5 turns · $0.0242` |
| `git commit` | `4 files changed, 111 insertions(+), 31 deletions(-)` |

In the two practice runs before filming, the analyst made 11 and then 10 `load_document` calls, and the synthesizer 7 and then 10 `verify_fact` calls; `load_document` never refused. In the first practice run, after the synthesizer reported, the coordinator tried `verify_fact` itself and Lesson 4.1's hook denied it (`[coordinator, denied] verify_fact ...`): the hook doing its job. In one earlier practice run (Lesson 4.3), the analyst, which then had `fetch_url`, fetched one of Harborline's internal pages by guessing its address.

## Troubleshooting

- **`[coordinator, denied] verify_fact ...`**: the coordinator tried a research tool itself, and Lesson 4.1's hook stopped it. Nothing to fix; the run goes on.
- **`... wasn't returned by search_web in this run. Load a URL from the search results.`**: `load_document` refused a URL no search returned. If it happens in a real run, the analyst guessed an address; the error tells it what to do instead.
- **The analyst still calls `fetch_url`**: save `research/agents.py`; check its `tools=["mcp__research__load_document"]`, and that `coordinator.py`'s `RESEARCH_TOOLS` no longer lists `fetch_url`.
- **`test_load_returns_the_details_then_the_text` fails on the publisher**: check the spelling, `"Retail Signals Weekly"`.
- **`ModuleNotFoundError: No module named 'research'`**: run from the `harborline` folder with `python -m ...`.
- **`.env` or `runs/` shows up in `git status`**: they must never be committed. Check that `.gitignore` lists them.

## Key terms

- **Tool scoping:** each subagent's `tools` lists only what its role needs; a tool left out isn't in its session.
- **Constrained tool:** a tool that can only do the role's job (`load_document` loads only sources a search returned in this run).
- **Generic tool:** a tool that can do far more than the role needs (`fetch_url` fetches any URL).
- **Scoped cross-role tool:** a narrow tool for a frequent need of another role (`verify_fact` checks one claim against one source, without searching or reading whole pages).
- **Route through the coordinator:** what a scoped tool can't do (a new source) is reported back, and the coordinator decides.

## Sources (checked 2026-10-15)

- Agent SDK docs, *Subagents in the SDK*, Tool restrictions: "Use the tools field to limit what a subagent can do"; omit `tools` and the subagent gets every tool available to subagents; list tools and it gets only those; "A tool you leave out isn't in the subagent's session at all". Common tool combinations: read-only analysis gets `Read`, `Grep`, `Glob` ("Can examine code but not modify or execute"): https://code.claude.com/docs/en/agent-sdk/subagents
- Anthropic Engineering, *Writing effective tools for agents — with agents*: a tool that returns all contacts wastes an agent's limited context; in the address book case, implement a `search_contacts` or `message_contact` tool "instead of a list_contacts tool": https://www.anthropic.com/engineering/writing-tools-for-agents
- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, version 1.0: Task Statement 2.3 (too many tools degrade tool selection; agents with tools outside their specialization tend to misuse them; scoped tool access; constrained alternatives to generic tools; a scoped cross-role tool for high-frequency needs, with complex cases routed through the coordinator). Scenario 3: Multi-Agent Research System.

Models, SDKs and tools change. If a version or a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes. In Lesson 4.6: errors across agents, and how a failure travels from a subagent to the answer.
