# Expected output: Lesson 5.2, The CLAUDE.md hierarchy

What each step showed in the lesson, copied from the screen. Claude's wording will differ on your machine, and so will token counts, times and commit ids. What should match: where each answer says the rules came from, the files `/memory` lists, the `Loaded support/CLAUDE.md` line, the teammate's check finding nothing before the push and your project files after it, and the shape of the git output. Long passages are shortened with `…`.

## 1. The rules nobody else gets

```text
$ git status --short
$ code ~/.claude/CLAUDE.md
```

After typing and saving the user file (see README.md, step 1):

```text
$ claude -p "Without reading any files: quote the rules you were given for working in this repository, or say there are none. Nothing else."
Rules from your global notes (`~/.claude/CLAUDE.md`), which apply to all projects:

- "Run the tests with: .venv/bin/python -m pytest -q"
- "Money: take refund amounts from policy.check_refund, never compute them by hand."
- "Dates: read orders through harborline.normalize, never parse the raw date fields."
- "Commit messages: one line that says what changed."
- "Keep answers short."

I have not checked for a project-level CLAUDE.md in the repo, since I was told not to read files.
```

## 2. and 3. The project file, its imports, the support file

These steps print nothing but the commands (`code …` opens each file in VS Code). The files are the kit's `harborline/` files. At the end, your user file holds:

```markdown
# My notes for Claude

- Keep answers short.
```

## 4. Check and share

The teammate's check, before the commit (the new files exist only on your disk):

```text
$ cd /tmp/teammate && git pull -q && claude -p --setting-sources project,local "Without reading any files: quote the rules you were given for working in this repository, or say there are none. Nothing else."
I wasn't given any rules specific to this repository. No CLAUDE.md or other project instructions were loaded into my context.
```

Back in your repo:

```text
$ claude
 Claude Code v2.1.301
 Haiku 5.5 · Claude Max
 ~/projects/harborline
```

`/memory`:

```text
Memory

❯ Auto-memory  true

❯ User instructions               Saved in ~/.claude/CLAUDE.md
  Project instructions            Checked in at ./CLAUDE.md
  L docs/conventions/money.md     @-imported
  L docs/conventions/dates.md     @-imported
  Open auto-memory folder

Learn more: https://code.claude.com/docs/en/memory

Enter to confirm · Esc to cancel
```

**Esc** prints `Cancelled memory editing`. Then `/context`; at the top of its report:

```text
Context Usage
…  Haiku 5.5
   claude-haiku-5-5
   31.2k/1m tokens (3%)

   Estimated usage by category
   System prompt: 3.7k tokens (0.4%)
   System tools: 18.7k tokens (1.9%)
   MCP tools: 640 tokens (0.1%)
   MCP server instructions: 1.2k tokens (0.1%)
   Memory files: 295 tokens (0.0%)
   Skills: 6.6k tokens (0.7%)
   …
```

Further down in the same report (the other sections list your account's skills and connectors, and will differ):

```text
Memory files · /memory
├ ~/.claude/CLAUDE.md: 25 tokens
├ CLAUDE.md: 140 tokens
├ docs/conventions/money.md: 61 tokens
└ docs/conventions/dates.md: 69 tokens
```

The folder's file, on demand:

```text
❯ Read support/agent.py and tell me in two lines what it does.

  Read 1 file (ctrl+o to expand)
  ⎿ Loaded support/CLAUDE.md

● It runs one support ticket through a Claude agent with Harborline's tools, capped at
  10 turns and $0.10, and gates and hooks enforce the rules.

  It prints the tools called, the final reply, and the turns, cost and session ID, and
  can resume a session for a customer's follow-up message.
```

`/exit` prints a `claude --resume <session id>` line for this session. Then the commit and the push:

```text
$ git add CLAUDE.md docs support/CLAUDE.md
$ git commit -m "Lesson 5.2: team rules in CLAUDE.md with imports, and support/CLAUDE.md for the support agent"
[main 242274d] Lesson 5.2: team rules in CLAUDE.md with imports, and support/CLAUDE.md for the support agent
 4 files changed, 26 insertions(+)
 create mode 100644 CLAUDE.md
 create mode 100644 docs/conventions/dates.md
 create mode 100644 docs/conventions/money.md
 create mode 100644 support/CLAUDE.md
$ git push
…
To https://github.com/YOUR-USERNAME/harborline.git
   cf8ab59..242274d  main -> main
```

The teammate's check again (the end of the answer; the top quotes the first lines of `CLAUDE.md`):

```text
$ cd /tmp/teammate && git pull -q && claude -p --setting-sources project,local "Without reading any files: quote the rules you were given for working in this repository, or say there are none. Nothing else."
…
> - One test file: .venv/bin/python -m pytest -q tests/test_policy.py
>
> ## Conventions
> @docs/conventions/money.md
> @docs/conventions/dates.md
>
> ## Commits
> - One line that says what changed.

**docs/conventions/money.md**

> # Money
>
> - Amounts are US dollars, rounded to cents only at the end.
> - Refund amounts come from policy.check_refund. Never compute them by hand.

**docs/conventions/dates.md**

> # Dates
>
> - Orders mix Unix seconds, ISO 8601 with offsets and plain dates.
> - Read orders through harborline.normalize. Never parse the raw date fields.
```

`Keep answers short.` is not in it, and neither is `support/CLAUDE.md`.
