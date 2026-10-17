# Student kit: Lesson 8.1, Capstone tour

Claude Certified Architect – Foundations (CCAR-F) · Section 8: Exam Readiness · Lesson 8.1

This kit holds what you need to walk your own Harborline repository the way the lesson does, and a one-page map of the six systems for exam day. By the end of the lesson you can:

1. Walk Harborline's six systems
2. Place each on its scenario and domains
3. Run the pieces once more, end to end

## What's in the kit

| File | What it is |
|---|---|
| `commands.txt` | Every command in the hands-on, in order: the history, one stop per system, three runs |
| `harborline-map.md` | The map: two foundations, six systems, each with its scenario, the guide's primary domains, its folder and the module that built it |

There is no new code in this lesson. You walk the repository you built.

The video is filmed on Ubuntu 24.04 in VS Code and its terminal. The steps are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Your own `harborline` repository after Lesson 7.6**, in `~/projects/harborline`, with its `.venv` and its `.env` (your API key, from Lesson 0.4). If you skipped a lesson, that lesson's kit has its files.
- **`runs/batch.jsonl` from Lesson 7.5**, for the review report. `runs/` is ignored by git, so it is only on the computer that ran the batch.
- About 15 minutes. The support agent and the invoice each make a call or two to Haiku: well under a cent together. The test suite and the review report make no API calls.

## The steps (the lesson's order)

1. **The history.** `git log --oneline | wc -l` counts the commits (57 in the lesson). `--reverse | head -16` shows the oldest: the starter, then Lesson 1.1, 1.2 and on through Lab 1, Module 2 and Lab 2. `head -16` shows the newest: Module 7's extraction lessons, Module 6's review and Lab 5. `git tag` shows `starter-v1`. Every commit names its lesson, so the history reads like the syllabus. Your count and hashes will differ if you committed differently.
2. **The team setup.** `ls .claude/rules .claude/commands .claude/skills`: one command, three rules and two skills (Module 5).
3. **One stop per system.** `code -g <file>:<line>` opens each file at the lines that matter (`commands.txt` lists all eight). For each one, say which scenario it answers and which rule the exam tests:
   - `loop/agent.py`: a loop ends on the stop reason, never on reading the text.
   - `mcp_server/server.py`: descriptions are how the model chooses a tool, so they're the first fix when it picks the wrong one.
   - `support/hooks.py`: a refund above $500 is denied before the tool runs. That's a control, not an instruction.
   - `research/agents.py`: a subagent knows only what the coordinator passes it.
   - `CLAUDE.md`: in the repository, so the whole team shares it.
   - `devtools/explorer.py`: a scoped tool beats reading the whole codebase into context.
   - `.github/workflows/pr-review.yml`: Claude Code runs with `-p`, so nothing waits for a person.
   - `extraction/schema.py`: a field the document doesn't state is `None`, never a guess.
4. **Three runs.** `python -m pytest -q` (139 passed in the lesson, in under two seconds). `python -m support.agent T-003` (it verifies the customer, looks up the order and refunds $74.00, in four turns). `python -m extraction.validate data/invoices/dev/INV-D08.txt` (the line items and the total add up). `python -m extraction.review | head -14` (last month's report: overall accuracy, by field, and the review queue). Then `git status --short` prints nothing: the runs changed no tracked file.

## What will differ on yours

- **The counts.** Your commit count, test count and hashes depend on how you worked through the labs.
- **The agent's reply.** The model words the reply its own way, and the turn count and cost can differ slightly. The refund amount, $74.00, comes from the order data, so it doesn't change.
- **The invoice.** In Lesson 7.3, INV-D08's first line needed a retry. In this lesson the first attempt passed. Either is fine: the code checks the lines and the total either way.
- **The review report.** It reads your own `runs/batch.jsonl`, so its numbers are yours.

## Windows, macOS and Linux

- **macOS and Linux:** the commands work as they are.
- **Windows (PowerShell):** activate with `.venv\Scripts\Activate.ps1`. Replace `| wc -l` with `| Measure-Object -Line`, and `| head -16` with `| Select-Object -First 16`. `git log --oneline --reverse | Select-Object -First 16` gives the oldest commits. `code -g` and the Python commands are the same.

## If something goes wrong

- **`code: command not found`:** in VS Code, open the Command Palette and run *Shell Command: Install 'code' command in PATH* (macOS), or reinstall VS Code with the PATH option (Windows).
- **The agent or the invoice fails with an authentication error:** your `.env` is missing the key, or the terminal isn't in the repository folder. See Lesson 0.4.
- **The review report says there is no batch:** run Lesson 7.5's batch first; `runs/` isn't in git.
- **A test fails:** run `git status` and `git diff` to see what changed since your last lab, and compare with that lesson's kit.

## Sources (checked 2026-10-17)

- Claude Certified Architect – Foundations Exam Guide: section 4 (the blueprint), section 5 (the six scenarios and their primary domains), section 7 (How to Prepare)
