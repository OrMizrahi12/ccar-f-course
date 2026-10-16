# Student kit: Lesson 4.9, Module 4 exam traps and recap

Claude Certified Architect – Foundations (CCAR-F) · Module 4: Multi-Agent Systems: the Research Pipeline · Lesson 4.9

This lesson adds no code. It goes back over Module 4 using the module's own runs. By the end of it you can:

1. Spot Module 4's seven classic traps
2. Know where a multi-agent failure really starts
3. Hold Module 4 on one page

## What's in the kit

| File | What it is |
|---|---|
| `module-4.md` | The Module 4 cheat sheet: one row per lesson, plus the seven traps and why each one is wrong |

## The seven traps

In a multi-agent question, the agent that shows the failure is rarely where it starts. And each wrong option sounds sensible.

| Trap | It sounds like | The fix it hides |
|---|---|---|
| Hand out every tool | "Give every agent every tool." "Let the analyst search too, just in case." | Each role gets only its own tools. Swap a general tool for a constrained one (`load_document` opens only what the searchers found); add one scoped tool for a common cross-role need (`verify_fact`); route the rest through the coordinator. |
| Assume shared memory | "The subagent can see the conversation." "It already knows the date range." "The coordinator's summary is enough." | A subagent starts with only its prompt and inherits nothing. Put every constraint in that prompt, and pass complete findings as structured data: claim, evidence, URL, publisher, date. |
| Blame the synthesizer | "Give the synthesis agent a better model." "Tell it to cover more." | The writer writes what it receives. Read upstream first (the coordinator's split, each hand-over), then add a refinement loop that finds the gaps and sends targeted work back out. |
| One shape for every task | "Always decompose dynamically." "Fix the investigation's steps in advance." "Run the subagents one at a time to be safe." | Known, repeatable steps suit a chain; an open investigation needs a plan that adapts; a big review needs per-file passes plus a cross-file pass; independent subtopics run in parallel, with several Agent calls in one response. |
| Swallow or abort | "Return an empty list so the run never stops." "Stop the whole run on any error." "Retry until something comes back." | Return structured error context (the failure type, the query, partial results, alternatives). Retry brief failures locally, let the rest of the work go on, and name the gap in the report. |
| Pick a winner | "Report the average." "Keep the larger sample." "Let the newer figure replace the older one." | Keep each figure with its source, measure and date. Figures from different years may simply show change over time. Separate established from contested, and flag a source with no stated method. |
| Start over | "Run everything again after a crash." "Write one summary at the very end." "Use a bigger context window." | Save each agent's report as it lands, with a manifest written in one step, and resume from it. Have upstream agents hand over compact facts with relevance and metadata, not their whole reasoning. |

## Where the runs come from

Every run in the lesson was recorded in an earlier lesson. To run one again, use that lesson's kit:

- **Lesson 4.5** (trap 1), `research/agents.py`: the analyst's only tool is `load_document`; the synthesizer can't search or read, and its only tool is `verify_fact`. In the run, the analyst loaded only URLs the searchers had found, and the synthesizer checked each figure with a claim and its URL.
- **Lesson 4.1** (trap 2), the question about one Meridian page: the coordinator sent only the analyst, with a prompt that names the URL, what to extract, what to do if the page fails, and to report the source for each fact. Answer: 17.6% of units sold, January to September 2025 (`subagents: analyst · 2 turns · $0.0012`).
- **Lesson 4.2** (trap 2): the synthesizer gets only its prompt: the question, the rules, and `[ 21 findings as JSON, keys: claim, evidence, url, publisher, published, method ]`.
- **Lesson 4.7** (trap 3): after the analysts finished, the coordinator sent `searcher 5` on a gap search (a named online retailer's own return policy) before the synthesizer wrote anything.
- **Lesson 4.4** (trap 4), `python -m experiments.m4.decompose chain` and `... explore`: the chain reviewed each file, then across the files (`6 calls, fixed before the run`); one per-file pass said it couldn't see the other file. The exploration chose its steps as it went (`14 tool calls, chosen during the run`).
- **Lesson 4.3** (trap 4): independent searchers ran together: `subagents worked 98s in 57s of clock time: running together saved 41s`. The same answer already said the return rates use different metrics, "so don't average them".
- **Lesson 4.6** (trap 5), the question about fees and return fraud: three searches timed out, each was retried once and reported as a failure, the run went on, and the answer's gaps line says Harborline's own fraud rate is unknown.
- **Lesson 4.8** (traps 6 and 7): the report's contested section is a table, each return-rate figure with its source, date and method (24.0% of order value from a survey of retail executives; 17.6% of units sold from Meridian). With `CRASH_AFTER=3`, the run stopped with analyst 1 still working; three reports were saved, and the manifest kept every source found. The resume printed `3 reports already saved` and ran only the missing analyst.
- **Lesson 4.7** (trap 6), `python -m pytest -q tests/test_provenance.py`: `4 passed`, including a test that flags a source with no stated method.

Each number comes from one run on the day it was recorded, so yours will differ. This lesson made no API calls and cost nothing.

## Next

1. **Lab 4: the research pipeline, checked on a hard question**, in the course materials under `labs/L4/`: run the whole pipeline on a question where fraud searches time out and the return-rate sources disagree, and check its report in code.
2. **The Module 4 quiz**: 14 questions, three of them from Modules 1 to 3. This lesson has no quick check, because the quiz takes its place.

## Sources (checked 2026-10-16)

- Subagents in the SDK: https://code.claude.com/docs/en/agent-sdk/subagents
- How we built our multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
- Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Writing effective tools for agents: https://www.anthropic.com/engineering/writing-tools-for-agents
- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Claude Certified Architect – Foundations Exam Guide: Domains 1, 2 and 5, Task Statements 1.2, 1.3, 1.6, 2.3, 5.1, 5.3, 5.4 and 5.6, Scenario 3

Models and tools change. Always confirm current details in the official docs.
