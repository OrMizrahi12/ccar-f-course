# Lab 1: a raw agentic loop that handles every stop reason

Claude Certified Architect – Foundations (CCAR-F) · Module 1: Claude API Foundations for Architects · the module checkpoint

In Lesson 1.4 you wrote Harborline's agentic loop. It runs tools while `stop_reason` is `"tool_use"`, returns on `"end_turn"`, and raises `LoopStopped` for everything else. That was the right first rule: a cut-off reply is not an answer. In this lab you give every stop reason its own handling, and you prove each branch with tests that need no API key.

You pass the lab when the self-check tests pass and one real run either answers the ticket or ends with a clear hand-off line.

## What you start from

`starter/` is the `harborline` project exactly as it stands after Lesson 1.5: the starter package, `loop/tools.py` (1.3), `loop/agent.py` (1.4), `loop/workflow.py` (1.5) and the experiments from Lessons 1.1 to 1.5. If your own project is there too, keep working in it. If not, copy `starter/` to `~/projects/harborline`, create the virtual environment, install `requirements.txt`, and add your `.env` (Lessons 0.4 and 0.6 show how).

`solution/` is a finished version to compare with when you're done. `tests/` holds the self-check.

## What you change

Only `loop/agent.py`. Keep `run(client, messages)` and `first_message(ticket_id)` as they are: `experiments/m1/antipatterns.py` and `experiments/m1/who_decides.py` import them, and they must keep working.

## Steps

### 1. Name the ways a run can end without an answer (Lesson 1.4)
Keep `LoopStopped` as the base class and add two kinds of it:
- `CutOff(LoopStopped)`: the reply was still cut off by `max_tokens` with the most room you allow.
- `Refused(LoopStopped)`: Claude declined. Give it a `category` attribute.

Code that already catches `LoopStopped` (like `who_decides.py`) still catches both.

### 2. `max_tokens`: retry with more room, never keep the cut reply (Lessons 1.1, 1.2)
A response that stops on `max_tokens` is cut off: half a sentence, or half a tool call. Don't append it to `messages`. Send the same request again with `max_tokens` doubled, up to a ceiling: add `MAX_TOKENS_CEILING = 4 * MAX_TOKENS`. If the reply is still cut off at the ceiling, raise `CutOff`.

This is the case Lesson 1.4 met on T-016: thinking plus a long answer filled the 1,024-token budget. The docs give the same fix for a cut-off tool call: retry the request with a higher `max_tokens` ([Handling stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)).

### 3. `refusal`: stop, and don't resend it (Lesson 1.2)
A refusal is a normal response, not an error. Its `stop_details.category` names the policy area. On Claude Haiku 5.5, sending the same request again usually returns another refusal, and there is no server-side fallback ([Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)). Raise `Refused(category)` without appending anything. A person takes the ticket over.

### 4. `pause_turn`: send the paused turn back (Lesson 1.2)
`pause_turn` comes only from server tools, such as web search, when the server-side loop reaches its iteration limit. Harborline's tools all run in your code, so today it never happens. When Claude stops to call your tools, the stop reason is `tool_use`. Handle it anyway, as the docs describe: append the response as the assistant turn, unchanged, and send the request again with no new user message. Allow at most `MAX_CONTINUATIONS = 3`, then raise `LoopStopped`.

### 5. Everything else is not an answer (Lesson 1.4)
`stop_sequence` (Harborline sets none), `model_context_window_exceeded`, or any value you don't know: raise `LoopStopped` naming the stop reason. `MAX_TURNS` stays what it was: a safety net, and running out of turns is a failure.

`tool_use` and `end_turn` keep the Lesson 1.4 code: Claude's turn joins the history as returned, every `tool_use` block runs, and all the results go back in one user turn.

### 6. The command line
In the `__main__` block, catch `Refused` and `LoopStopped`. Print one line that says the ticket needs a person, then print the history as before.

## Check your work

1. Copy `labs/L1/tests/test_loop.py` into your project's `tests/` and run the whole suite:
   ```bash
   python -m pytest -q
   ```
   Our solution: `54 passed` (the starter's 44 tests plus the lab's 10). The lab's tests use a `FakeClient` that returns scripted responses, so they cost nothing and need no key. They cover:
   - `end_turn`
   - `tool_use` then `end_turn`
   - two parallel calls answered in one user turn
   - a bad order ID that comes back with `is_error`
   - `max_tokens`: retried with twice the room, and failing loudly at the ceiling
   - `pause_turn`
   - `refusal`: no retry
   - an unknown stop reason
   - running out of turns
2. Run it for real once (about $0.001):
   ```bash
   python -m loop.agent T-016
   ```
   Our run took three turns: verify Callum, look up both orders in one turn, then `end_turn` with a four-point answer. That was 3 requests and $0.00115 in `runs/usage.jsonl`. Your run will differ. If a turn hits `max_tokens`, you'll see `retrying with max_tokens=2048` and the turn sent again; if it never does, the tests have still exercised that branch.
3. Run `python -m experiments.m1.antipatterns T-003` again. It imports your new `run` and still judges the same four stop rules.

## Compare with the solution

`solution/loop/agent.py` is one way to do it, and `solution/tests/test_loop.py` is the self-check. Other designs pass too. For example, you might keep the larger `max_tokens` for one turn only, instead of for the rest of the run.

## Commit

```bash
git add loop/agent.py tests/test_loop.py
git commit -m "Lab 1: handle every stop reason, with tests"
git push
```
