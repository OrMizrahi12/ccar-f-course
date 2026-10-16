# Expected output: Lesson 5.4, Slash commands and skills

What each step showed in the lesson (Claude Code v2.1.301, Haiku 5.5, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. Claude's wording changes from run to run; compare the behavior, not the exact text.

## Step 1: a project command

```text
$ git status --short
$ mkdir -p .claude/commands .claude/skills/review-tool-descriptions
$ code .claude/commands/run-tests.md
```

`git status --short` prints nothing (the tree is clean). After saving, VS Code's Explorer shows `.claude/commands/run-tests.md` marked `U` (untracked). The file:

```markdown
---
description: Run one test file, then the whole suite, and summarize the result
argument-hint: [test-file]
allowed-tools: Bash(.venv/bin/python -m pytest *)
---

Run .venv/bin/python -m pytest -q $ARGUMENTS, then the whole suite with .venv/bin/python -m pytest -q.
Report the pass and fail counts of each run. For a failure, name the test and the line that failed.
```

## Step 2: a forked skill

`.claude/skills/review-tool-descriptions/SKILL.md`:

```markdown
---
description: Review the tool descriptions in a file against the team's tool rules. Use when tool definitions change.
argument-hint: [file]
context: fork
agent: Explore
background: false
allowed-tools: Read Grep Glob
---

Review every tool description in $ARGUMENTS. For each tool, check that it:
1. says what the tool returns,
2. says when to use it instead of a similar tool,
3. reports errors through harborline/tool_errors.py.

Answer with one line per tool: its name, then OK or the gap and a suggested fix.
Change no files.
```

VS Code may underline some front matter keys and show a count in the Problems tab. That's the editor's own Markdown check, not an error in the skill; Claude Code reads these keys.

## Step 3: a personal variant

`~/.claude/skills/my-tool-review/SKILL.md` (the editor's breadcrumb shows your home folder, then `.claude > skills > my-tool-review`):

```markdown
---
description: My quick tool check, with a rewrite I can paste.
argument-hint: [file]
context: fork
agent: Explore
background: false
---

Review the tool descriptions in $ARGUMENTS against the team's rules,
and for each gap write a full replacement description I can paste.
Change no files.
```

## Step 4: run them and share

Typing `/rev` in Claude Code lists, among others:

```text
/review-tool-descriptions   Review the tool descriptions in a file against the team's tool rules. Use when tool definitio…
/code-review (review)       …
/my-tool-review             My quick tool check, with a rewrite I can paste. (user)
/security-review            Complete a security review of the pending changes on the current branch
/ultrareview                …
```

`(user)` marks a personal skill from your home folder. The built-in entries depend on your Claude Code version.

`/run-tests tests/test_policy.py`: two Bash calls, with no permission prompt (`allowed-tools` pre-approves the project's pytest command for that turn):

```text
● Bash(.venv/bin/python -m pytest -q tests/test_policy.py)
  ⎿  9 passed in 0.01s
● Bash(.venv/bin/python -m pytest -q)
● - tests/test_policy.py: 9 passed, 0 failed.
  - Full suite: 118 passed, 0 failed.
```

`/review-tool-descriptions loop/tools.py`: the work runs nested under the command (a forked Explore subagent): it reads `loop/tools.py` and `harborline/tool_errors.py` and searches `harborline/backend.py`; some tool uses fold into `… +2 tool uses (ctrl+o to expand)`. The answer in the lesson (one line per tool; `get_customer` and `lookup_order` were OK, above the fold):

```text
- list_orders: OK
- process_refund: Gap: the description never says what it returns. The backend returns the refund record (refund_id, order_id, customer_id, amount, reason, sku, status). Fix: add "Returns the refund record: refund_id, amount, reason, sku and status (processed)."
- escalate_to_human: OK
- check_refund: OK

Rule 3 is met in code for all six tools, not in the descriptions. run_tool in …/loop/tools.py sends every BackendError through tool_error in …/harborline/tool_errors.py. Two paths skip it: other exceptions raised by a handler propagate instead of returning a tool_result, and the unknown-tool reply is plain text rather than a tool_error body. Fixing those would cover all six tools at once.

No files were changed.
```

Your review may word things differently or flag a different detail. The `process_refund` gap is a fact of the course code, so expect it.

Then, after `/exit`:

```text
$ git status --short
?? .claude/commands/
?? .claude/skills/
$ git add .claude/commands .claude/skills
$ git commit -m "Lesson 5.4: a /run-tests command and a forked review-tool-descriptions skill"
[main bac276b] Lesson 5.4: a /run-tests command and a forked review-tool-descriptions skill
 2 files changed, 24 insertions(+)
 create mode 100644 .claude/commands/run-tests.md
 create mode 100644 .claude/skills/review-tool-descriptions/SKILL.md
$ git push
   b46b623..bac276b  main -> main
```

Your commit hashes will differ. The personal skill is not in the commit: it lives in `~/.claude/skills/`, outside the repository.
