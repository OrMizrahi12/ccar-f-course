# Student kit: Lesson 5.1, Working with Claude Code

Claude Certified Architect – Foundations (CCAR-F) · Module 5: Configuring Claude Code for a Team · Lesson 5.1

This kit holds everything you need to repeat the lesson on your own computer: the two files Claude Code wrote in the lesson, every prompt and command in order, what each step showed in the lesson, what differs on Windows and macOS, and what to do when something goes wrong.

By the end of the lesson you can:

1. Explore, plan, code, commit
2. Pick the permission mode for the risk
3. Keep context and sessions under control

## What's in the kit

| File | What it is |
|---|---|
| `scripts/late_deliveries.py` | The script Claude Code wrote (54 lines): lists the orders delivered more than 5 days after the promised date, with the shipping fee the refund policy owes for each, and the total. It calls `policy.check_refund(order, "late_delivery")`, so the rule and the amount come from the same code the refund tool uses. Read-only: it never issues a refund |
| `tests/test_late_deliveries.py` | Its six tests (71 lines): the real data's two orders and the $13.90 total, the 5-day boundary (5 days late is not included, 6 is), legacy Unix-seconds and offset ISO dates, undelivered and cancelled orders skipped, and the printed output |
| `commands.txt` | Every prompt, key and command in the lesson, in order |
| `expected-output.md` | What each step showed in the lesson, and what will differ on yours |

In this lesson you don't type code: you ask Claude Code, read its plan, approve it, and Claude writes the two files. Claude's files on your machine will not match the kit's line for line; that's expected. Compare the behavior (the same two orders, the same total, the tests passing), and use the kit's files if yours went wrong.

The video is filmed on Ubuntu 24.04 in the VS Code terminal. The prompts and Claude Code's keys are the same on Windows, macOS and Linux; see [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lessons 0.6 to 4.9 done**: your own `harborline` repository in `~/projects/harborline` at the Lab 4 commit, with its `.venv`, `pytest` passing, the harborline MCP server from Lesson 2.6, and `origin` pointing at your own private `harborline` repository.
- **Claude Code** (Lesson 0.5), signed in, with the `harborline` folder trusted.
- About 25 minutes. **No API calls: Claude Code runs on your Claude sign-in.** Each prompt counts toward your Claude Code usage like any other.

## The steps (the lesson's order)

Open VS Code on your `harborline` folder and its terminal (**Ctrl+`**). Activate the environment if the prompt doesn't start with `(.venv)` (Lesson 0.6). Start every session from the `harborline` folder.

### 1. Explore and plan

```bash
git status --short
claude
```

`git status --short` prints nothing: the tree is clean. The banner shows Claude Code's version and model; the status bar under the input shows the permission mode. In the lesson it started in **auto mode** (`⏵⏵ auto mode on`), the starting mode for new interactive sessions on current versions.

Press **Shift+Tab** three times, pausing to read the status bar each time:

| Press | Status bar | What runs without asking |
|---|---|---|
| 1 | `⏸ manual mode on` (the `default` mode) | reads only |
| 2 | `⏵⏵ accept edits on` | reads, file edits, common filesystem commands |
| 3 | `⏸ plan mode on` | reads and exploring commands; no edits until you approve a plan |

Pressing it once more brings you back to auto mode. In plan mode, ask:

```text
Which orders were delivered more than 5 days after the promised date, and what does our refund policy say we owe for them? Look at how the data and its dates are handled before you answer.
```

Claude reads files and runs small read-only Python checks. In the lesson each check showed `Allowed by auto mode classifier`: with auto mode available, the classifier reviews commands during planning. When Claude wanted the harborline MCP server's **Lookup Order** tool, Claude Code asked first (`Do you want to proceed?`); the lesson answered `1. Yes` for each of the two orders. Nothing is edited in plan mode.

The answer: **HL-10147** and **HL-10148**, each delivered 8 days after the promised date, $6.95 shipping fee owed on each, **$13.90** in total, from Section 4 of `data/refund_policy.md` (a delivery more than 5 days late gets its shipping fee back), which `harborline/policy.py` implements as `check_refund(..., "late_delivery")`. It also explained how the dates are stored (Unix seconds, ISO text with `Z` or a `-04:00` offset, and bare dates) and left out the 23 orders with no delivery date. Scroll up with the mouse wheel to read all of it.

Then ask for the plan, still in plan mode:

```text
Plan a script, scripts/late_deliveries.py, that lists those orders with the shipping fee we owe and the total, plus a test for it. Keep the change to those two files.
```

Read the plan before you approve anything: what it reuses (`data.orders()`, `policy.as_date`, `LATE_DELIVERY_DAYS`, `check_refund`), what the script does (read-only; never calls `process_refund`), the tests, and how it will be verified. Claude Code saves the plan as a Markdown file (its path is shown under the menu; **Ctrl+G** opens it for editing). Then it asks:

```text
1. Yes, and use auto mode
2. Yes, manually approve edits
3. Tell Claude what to change
```

The lesson picked **1**: two new files, a read-only script and its tests, and a plan just read, so low risk; the classifier reviews each action. Pick **2** if you want to approve each file write yourself, or **3** to send the plan back with your changes.

### 2. Code and test

After approval Claude writes `scripts/late_deliveries.py` and `tests/test_late_deliveries.py`, runs the new tests (`6 passed`), runs the script, and, because the plan said so, the full suite. In the lesson its summary read: HL-10147 and HL-10148 with $6.95 each, a total of $13.90; the new tests pass (6), and so does the full suite (118). Nothing is committed yet. To see the script's output yourself (in a second terminal, or after `/exit`):

```bash
python -m scripts.late_deliveries
python -m pytest -q
```

### 3. Context

In the same session:

```text
/context
```

It prints a long report. Scroll up to its grid: the model, the tokens in use out of the context window, and the categories (system prompt, system tools, MCP tools, skills, messages, free space). In the lesson: 67.1k of 1m tokens (7%), messages 36.1k, and only `mcp__harborline__lookup_order` loaded among the MCP tools (the rest load on demand). Your numbers will differ: they depend on your account's skills and connectors.

```text
/compact Keep the late-delivery script, its test and the policy rule
```

Claude replaces the conversation with a summary focused on what you named, then re-reads the files you're working on and keeps a reference to the plan file. Run `/context` again and scroll up: in the lesson, 59k tokens (6%), messages down from 36.1k to 28.9k. A young session saves little; a long exploration full of verbose output saves much more.

### 4. Commit, clear, resume

```text
Commit the script and its test with a descriptive message.
```

In the lesson Claude checked `git status`, the branch and the tests, said "You're on main, so I'll commit on a new branch", and committed both files on a new branch `late-delivery-report` with a message starting `Add late-delivery report: list orders the refund policy covers, with the shipping fee owed`. Nothing was pushed. Claude may decide differently on yours (for example, commit on `main`): read what it did, then follow the matching path below.

```text
/clear
What did I ask you to plan earlier in this conversation?
```

After `/clear` the context is empty: Claude can't answer (it only sees the git state). The old session stays on disk.

```text
/resume
```

Pick the session at the top of the list (the arrow keys, then **Enter**), and ask the same question again:

```text
What did I ask you to plan earlier in this conversation?
```

This time Claude answers from the restored conversation: the script and its test, the plan file, the commit. Then `/exit`; Claude Code prints the `claude --resume …` command for this session.

```bash
git log --oneline -1
git push
```

If Claude committed on a new branch, `git push` fails with `fatal: The current branch late-delivery-report has no upstream branch.` That's correct: the branch exists only on your machine. Bring it into `main` yourself:

```bash
clear
git switch main
git merge --ff-only late-delivery-report
git push
git branch -d late-delivery-report
git log --oneline -2
```

`git merge --ff-only` shows `2 files changed, 125 insertions(+)` (your numbers depend on Claude's files); `git log --oneline -2` shows your commit with `(HEAD -> main, origin/main)`. If Claude committed on `main` instead, a plain `git push` is all you need.

Finally, the shortcut back into your latest session:

```bash
clear
claude --continue
```

It reopens the most recent conversation in this folder where it ended. `/exit` when you're done.

## Windows, macOS and Linux

| | Linux, macOS and WSL (the lesson) | Windows (native) |
|---|---|---|
| Clear the terminal | `clear` | PowerShell: `clear` or `cls`. cmd.exe: `cls` |
| Cycle permission modes | **Shift+Tab** | **Shift+Tab** |
| The starting mode | auto mode (current versions) | auto mode (current versions) |

**macOS:** in VS Code the shortcuts use **Cmd** where the lesson uses **Ctrl** (Cmd+` for the terminal); inside Claude Code, **Shift+Tab**, **Ctrl+G** and **Ctrl+O** are the same. **Older Claude Code versions** start in manual mode; then the first Shift+Tab gives accept edits. Update Claude Code (Lesson 0.5) to match the lesson.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `claude` | Claude Code v2.1.301, Haiku 5.5, `⏵⏵ auto mode on` |
| Shift+Tab ×3 | `⏸ manual mode on` → `⏵⏵ accept edits on` → `⏸ plan mode on` |
| The explore question (plan mode) | `Read 3 files, listed 2 directories`, Python checks `Allowed by auto mode classifier`, two Lookup Order calls approved once each; HL-10147 and HL-10148, 8 days late, $6.95 each, $13.90; 23 undelivered orders left out |
| The plan | reuse `check_refund` and `LATE_DELIVERY_DAYS`; a read-only script; tests; verification by `pytest` and a run of the script; the approval menu |
| Approved with `1. Yes, and use auto mode` | the script (54 lines) and the tests (71 lines); `6 passed`; full suite 118 passed; "Worked for 42s" |
| `/context` before / after `/compact` | 67.1k/1m tokens (7%), messages 36.1k → 59k (6%), messages 28.9k |
| The commit | `cf8ab59` on a new branch `late-delivery-report`, 2 files |
| `/clear`, then the question | no record of the earlier request |
| `/resume`, the same question | answered from the restored conversation |
| `git push` on the new branch | `fatal: … has no upstream branch` |
| Merge and push | `a543410..cf8ab59  main -> main` |
| API spend | $0: Claude Code on the subscription, no API calls |

See `expected-output.md` for the exact lines.

## Troubleshooting

- **The status bar shows `manual mode on` at start**: your Claude Code is older, or a setting sets the starting mode. Shift+Tab still cycles; the order starts from where you are. Update Claude Code (Lesson 0.5) to match the lesson.
- **Plan mode doesn't stop Claude from asking about commands**: without auto mode available, commands outside the read-only set ask for approval during planning. Read them and approve the read-only ones.
- **Claude didn't call the Lookup Order tool**: that's fine; it may answer from `data/orders.json` alone. Check that the harborline server is connected with `/mcp` (Lesson 2.6).
- **Claude found a different number of late orders**: check that your repo is at the Lab 4 commit (`git log --oneline -3`) and that `data/orders.json` is unchanged (`git status`). The two late orders are a fact of the course data.
- **The approval menu offers `Yes, auto-accept edits` instead of auto mode**: auto mode isn't available to your session. Pick it or `2`; both approve the plan.
- **Claude committed on `main`**: then skip the merge; `git push` works directly.
- **`git merge --ff-only` refuses**: `main` moved since the branch was created. Run `git log --oneline --graph --all -5`, then `git merge late-delivery-report` (a merge commit) or ask Claude to rebase the branch.
- **`/resume` shows a long list**: the newest session is at the top; type to search, **Esc** to cancel.
- **Tests fail after Claude's changes**: compare your two files with the kit's, or copy the kit's files over yours and run `python -m pytest -q` again.
- **`git push` goes to the starter**: run `git remote -v`. `origin` must be your own `harborline` (Lesson 0.6, step 4).

## Key terms

- **Plan mode**: Claude reads, explores and proposes a plan, but edits nothing until you approve it.
- **Permission mode**: what Claude may do without asking: manual (reads only), accept edits, plan, auto (a classifier reviews each action).
- **`/context`**: shows what fills the context window right now.
- **`/compact`**: replaces the conversation with a summary, focused on what you name.
- **`/resume`**: picks up an earlier session with its conversation; `/clear` starts a fresh one.

## Sources (all checked 2026-10-16)

- **Claude Code docs, Best practices for Claude Code.** https://code.claude.com/docs/en/best-practices : "Explore first, then plan, then code"; "If you could describe the diff in one sentence, skip the plan"; `/clear` to reset context between unrelated tasks; `/compact <instructions>`; `claude --continue` and `claude --resume`; the context window fills fast, and performance degrades as it fills.
- **Claude Code docs, Choose a permission mode.** https://code.claude.com/docs/en/permission-modes : the modes and what runs without asking in each; the Shift+Tab cycle (from auto: default → acceptEdits → plan); plan mode and the plan-approval choices; auto mode's classifier and its limits; `dontAsk` and `bypassPermissions` outside the cycle.
- **Anthropic, *Claude Certified Architect – Foundations Exam Guide*.** Version 1.0, effective July 2026: Task Statement 3.4 (Domain 3), Task Statement 5.4 (Domain 5), Scenario 2: Code Generation with Claude Code and Scenario 4: Developer Productivity with Claude.

Claude Code changes often. If a mode, a message or a screen doesn't match what you see, follow the official pages.

## What's next

Lesson 5.2: the CLAUDE.md hierarchy, where your team's instructions for Claude Code live.
