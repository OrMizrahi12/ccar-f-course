# CCAR-F Exam Plan

Sources: `ccar-f-exam-guide.pdf` (domain weights, §4) and `ccar-f-cheatsheets/module-1.md` to `module-7.md`. Item counts are **estimates**: weight × 60, rounded.

## 1. Items per domain (estimates)

| Domain | Weight | Est. items |
|---|---|---|
| 1 Agentic Architecture & Orchestration | 27% | ~16 (16.2) |
| 2 Tool Design & MCP Integration | 18% | ~11 (10.8) |
| 3 Claude Code Configuration & Workflows | 20% | ~12 |
| 4 Prompt Engineering & Structured Output | 20% | ~12 |
| 5 Context Management & Reliability | 15% | ~9 |
| **Total** | 100% | **60** |

## 2. What to review, by domain

- **D1 (~16 items):** M1 L1.4 (agentic loop), L1.5 (who decides); M3 L3.1–3.4 (Agent SDK, support agent, hooks), L3.8 (sessions); M4 L4.1–4.4 (coordinator, SDK subagents, parallel runs, decomposition).
- **D2 (~11 items):** M2 L2.1–2.5 (tool descriptions, rename/split, tool count and `tool_choice`, structured errors, MCP basics); M2 L2.6–2.7 (MCP scope in Claude Code, built-in tools); M4 L4.5 (tool distribution).
- **D3 (~12 items):** M5 L5.1–5.5 (permission modes, CLAUDE.md hierarchy, rules, skills and commands, plan vs direct), L5.6 (iterative refinement); M6 L6.1–6.2 (`claude -p`, PR review pipeline).
- **D4 (~12 items):** M6 L6.3–6.5 (explicit criteria, few-shot, independent and multi-pass review); M7 L7.1–7.5 (tool-use output, nullable schemas, validate and retry, few-shot for documents, batches).
- **D5 (~9 items):** M1 L1.1–1.2 (context window, reading responses); M3 L3.5, L3.7 (escalation, case facts); M4 L4.6–4.8 (errors, provenance, state and context budgets); M5 L5.7 (large codebases); M7 L7.6 (human review).

## 3. Pacing: 60 items in 120 minutes

Budget: 115 min for items, 5 min buffer at the end. About 1 min 55 s per item.

| Checkpoint | Items done by | Elapsed by |
|---|---|---|
| A | 15 | 0:29 |
| B | 30 | 0:58 |
| C | 45 | 1:27 |
| D | 60 | 1:55 |
| Buffer | — | 1:55 to 2:00 |

- At each checkpoint, compare the clock with the target. If behind, flag the current item, answer a best guess, and move on.
- Read "select N" in multiple-response items before the options.
- Use the buffer only for a final pass over flagged items.

## 4. Practice exam tracker

Percent = correct ÷ items in that domain on that exam. Targets: **80% overall**, **70% in every domain**.

| Domain | Est. items | Target | Practice 1 | Practice 2 | Practice 3 |
|---|---|---|---|---|---|
| 1 Agentic Architecture | ~16 | ≥70% | | | |
| 2 Tool Design & MCP | ~11 | ≥70% | | | |
| 3 Claude Code Config | ~12 | ≥70% | | | |
| 4 Prompt Eng & Structured Output | ~12 | ≥70% | | | |
| 5 Context & Reliability | ~9 | ≥70% | | | |
| **Overall** | 60 | ≥80% | | | |
