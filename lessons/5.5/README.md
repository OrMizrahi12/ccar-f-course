# Student kit: Lesson 5.5, Plan mode or direct execution

Claude Certified Architect – Foundations (CCAR-F) · Module 5: Configuring Claude Code for a Team · Lesson 5.5

This kit holds everything you need to repeat the lesson on your own computer: the files as they stand at the end of the lesson, the plan Claude wrote, every command and prompt in order, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Go direct on a clear, small change
2. Plan first when files, risk or designs multiply
3. Let Explore do the searching

## What's in the kit

| File | What it is |
|---|---|
| `harborline/legacy/warehouse/shipping.py` | After step 1: free shipping from $75.00 (`>=`), and the docstring points at `data/refund_policy.md` |
| `harborline/legacy/warehouse/__init__.py` | After step 3: the package without the compat import and without `getStatus` / `get_status_text` in `__all__` |
| `harborline/tests/test_legacy.py` | After both changes: `test_status_codes_have_names` calls `codes.status_name` directly; `test_free_shipping_starts_at_75_dollars` expects 0.0 at $75.00 and 6.95 at $74.99 |
| `before/shipping.py`, `before/compat.py` | The two files as they were before the lesson, for comparison (`compat.py` is deleted in step 3) |
| `the-plan.md` | The plan Claude wrote in plan mode in the lesson, word for word |
| `commands.txt` | Every command, prompt and key in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |

You don't need to type the `harborline/` files: Claude makes these changes in the lesson. They are there so you can compare your result with ours.

The video is filmed on Ubuntu 24.04, in the VS Code terminal. Claude Code behaves the same on Windows, macOS and Linux; a few shell commands differ, see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 5.4 done**: your own `harborline` repository in `~/projects/harborline` at the Lesson 5.4 commit, pushed, with `origin` pointing at your own private `harborline` repository. It has `.claude/rules/testing.md` from Lesson 5.3.
- **Claude Code** (Lesson 0.5), signed in, with the `harborline` folder trusted. The lesson runs it on Haiku 5.5, and new sessions start in auto mode.
- About 20 minutes. **No API calls: Claude Code runs on your Claude sign-in.** Each prompt counts toward your Claude Code usage like any other.

## How to choose (the lesson's signals)

| Ask | Points to direct execution | Points to plan mode |
|---|---|---|
| How many files will the change touch? | one | several, or you don't know yet |
| Who calls the code you're changing (the blast radius)? | nobody new; a test proves it | unknown callers, other teams' code |
| How many sensible designs are there? | one obvious one | two or more (email, a queue or a webhook) |
| Can you describe the diff in one sentence? | yes | no |

Plan mode is research first: Claude reads, searches and writes a plan, and your source isn't edited until you approve it. The **Explore subagent** is a built-in, read-only helper that searches in its own context window and returns only a summary, so the noisy discovery output stays out of your conversation. Plan to investigate, then execute the approved plan directly.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6).

### 1. Direct: the $75 rule

```bash
git status --short
claude
```

`git status --short` prints nothing: the tree is clean. Claude Code opens with `auto mode on (shift+tab to cycle)` under the prompt. Type:

```text
Free shipping starts at orders of $75.00 or more, as data/refund_policy.md says. Fix the comparison in legacy/warehouse/shipping.py and update its test, then run that test file.
```

No plan and no approval menu: Claude reads the file and the policy, notices that `quote` and `shipping_quote` point at the same function, edits `shipping.py` (`>` becomes `>=`) and `tests/test_legacy.py`, and runs the test file ("Allowed by auto mode classifier"). That run loads `.claude/rules/testing.md` (Lesson 5.3), which says to run the whole suite after a single file, so Claude renames the test and runs both. In the lesson: 3 passed, then 118 passed.

Scroll up through the diff, then leave Claude Code and commit yourself:

```text
/exit
```

```bash
clear
git diff --stat
git commit -am 'Lesson 5.5: free shipping from $75.00 (>=), as the refund policy says'
```

The message is in single quotes so the shell leaves `$75` alone (in double quotes, `$7` would be replaced by an empty variable).

### 2. Plan: retire the shim

`legacy/warehouse/compat.py` is a **shim**: two old names (`getStatus`, `get_status_text`) kept so that old code keeps working. Deleting it breaks anything that still imports them, and you don't know yet what does.

```bash
clear
claude
```

Press **Shift+Tab** three times: `manual mode on`, `accept edits on`, then `plan mode on`. Type:

```text
Use the Explore subagent to find everything that depends on legacy/warehouse/compat.py, then plan how to retire it.
```

Claude starts `Explore(Find compat.py dependents)` as a backgrounded agent. The agent panel under the prompt shows it working with its own token count (over 20k in the lesson); those searches stay in Explore's context. When it finishes (23 s in the lesson), Claude writes the plan (`the-plan.md`) and asks how to proceed:

```text
1. Yes, and use auto mode
2. Yes, manually approve edits
3. Tell Claude what to change
```

Scroll up and read the plan before you choose. **Ctrl+G** opens it in your editor if you want to change it first; the file lives under `~/.claude/plans/` with a generated name.

### 3. Approve, run, share

Press **1** (yes, and use auto mode). Claude removes the import and the two `__all__` entries, rewrites the test's assertions, deletes `compat.py`, runs the test file, the full suite and the plan's grep, and checks `experiments/m4/decompose.py`. In the lesson: 118 passed, "Brewed for 2m 37s", and the session took the name `retire-legacy-warehouse-compat` from the plan. Claude offers to commit; commit yourself:

```text
/exit
```

```bash
clear
git status --short
git add -A legacy tests
git commit -m "Lesson 5.5: retire legacy/warehouse/compat.py after a plan"
git push
```

`git add -A legacy tests` stages the deletion of `compat.py` together with the two edits. The push sends both of the lesson's commits.

## Windows, macOS and Linux

| | Linux and macOS (the lesson) | Windows (PowerShell) |
|---|---|---|
| Cycle the permission modes | Shift+Tab | Shift+Tab |
| Open the plan in your editor | Ctrl+G | Ctrl+G |
| The commit with `$75.00` in the message | single quotes: `git commit -am 'Lesson 5.5: … $75.00 …'` | PowerShell also expands `$` in double quotes: use single quotes the same way |
| Clear the terminal | `clear` | `clear` or `cls` |
| Where plans are saved | `~/.claude/plans/` | `$HOME\.claude\plans\` |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** for VS Code itself (Cmd+` for the terminal); Claude Code's own keys (Shift+Tab, Ctrl+G) are the same. **WSL** follows the Linux column.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| Step 1, direct (auto mode) | `>` → `>=`; the test expects 0.0 at $75.00 and 6.95 at $74.99, renamed `test_free_shipping_starts_at_75_dollars`; 3 passed, full suite 118 passed; "Baked for 26s" |
| Step 1 commit | `[main 764115e] Lesson 5.5: free shipping from $75.00 (>=), as the refund policy says`, 2 files changed, 5 insertions(+), 5 deletions(-) |
| Step 2, Explore | `Explore(Find compat.py dependents)`, backgrounded, finished in 23 s |
| Step 2, the plan | dependents: `legacy/warehouse/__init__.py:8` and `tests/test_legacy.py:10-11`; no dynamic imports, config, docs, CI or packaging references; 4 steps; verification by the test file, the full suite and a grep |
| Step 3, the build | `compat.py` deleted, 118 passed, "Brewed for 2m 37s" |
| Step 3 commit | `[main 3e0ebe2] Lesson 5.5: retire legacy/warehouse/compat.py after a plan`, 3 files changed, 3 insertions(+), 17 deletions(-), `delete mode 100644 legacy/warehouse/compat.py` |
| API spend | $0: Claude Code on the subscription, no API calls |

See `expected-output.md` for the exact lines.

## Troubleshooting

- **No `plan mode on` after three presses**: the order of the cycle depends on the modes your session has. Keep pressing **Shift+Tab** until the status line reads `plan mode on`, or start with `claude --permission-mode plan`, or put `/plan` in front of a single prompt.
- **Claude doesn't use Explore**: say it in the prompt, as the lesson does ("Use the Explore subagent to …"). Claude may still run a few searches of its own; what matters is that the bulk of the discovery happens in the agent.
- **Your plan differs from ours**: it will. Check that it names the same dependents (`__init__.py` and `tests/test_legacy.py`) and a way to verify. If something is missing, choose "Tell Claude what to change".
- **The approval menu shows "Yes, auto-accept edits"** instead of "Yes, and use auto mode": auto mode isn't available to your session (for example, your organization turned it off). Choose it anyway, or approve edits one by one.
- **Claude commits for you**: it asked first in the lesson. If it commits, check `git log --oneline -2` and skip your own commit.
- **The commit message lost `$75`**: it was in double quotes. Fix it with `git commit --amend -m 'Lesson 5.5: free shipping from $75.00 (>=), as the refund policy says'` before you push.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Direct execution**: Claude edits right away (auto mode, accept edits, or approving each edit yourself).
- **Plan mode**: research and a plan first; your source isn't edited until you approve the plan.
- **Explore subagent**: a built-in, read-only subagent that searches a codebase in its own context and returns a summary.
- **Shim**: old names kept so that old code keeps working (`compat.py`).
- **Blast radius**: everything a change can break.

## Sources (all checked 2026-10-17)

- **Claude Code docs, Best practices for Claude Code.** https://code.claude.com/docs/en/best-practices : "Explore first, then plan, then code"; plan mode adds overhead; for a small fix with a clear scope, ask Claude to do it directly; planning helps when the approach is uncertain, the change modifies multiple files, or the code is unfamiliar; "If you could describe the diff in one sentence, skip the plan."
- **Claude Code docs, Choose a permission mode.** https://code.claude.com/docs/en/permission-modes : plan mode researches and proposes without editing your source until you approve the plan; Shift+Tab, `/plan` and `--permission-mode plan`; the approval choices; Ctrl+G opens the plan in your editor; accepting a plan names the session.
- **Claude Code docs, Create custom subagents.** https://code.claude.com/docs/en/sub-agents : the built-in Explore subagent, "A fast, read-only agent optimized for searching and analyzing codebases", which keeps exploration results out of your main conversation.
- **Anthropic, *Claude Certified Architect – Foundations Exam Guide*.** Version 1.0, effective July 2026: Task Statement 3.4 (Domain 3), Scenario 2: Code Generation with Claude Code and Scenario 4: Developer Productivity with Claude.

Claude Code changes often. If a screen or a message doesn't match what you see, follow the official page.

## What's next

Lesson 5.6: iterative refinement, for changes where the first result isn't the last.
