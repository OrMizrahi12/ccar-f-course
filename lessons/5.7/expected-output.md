# Expected output: Lesson 5.7, Exploring a large codebase

What each step showed in the lesson (Claude Code v2.1.301, Haiku 5.5, in the VS Code terminal on Ubuntu 24.04), and what will differ on yours. Claude's findings and wording change from run to run; compare the behavior, not the exact text.

## Step 1: phase 1

```text
$ git status --short
$ claude
```

`git status --short` prints nothing (the tree is clean). After the phase 1 prompt:

```text
● 3 background agents launched (↓ to manage)
   ├ Map refund path in support/
   ├ Map refund path in mcp_server/
   └ Map refund path in loop/

● I've started three Explore agents, one each for support/, mcp_server/ and loop/. I'll
  write notes/exploration.md once all three report back.

✻ Waiting for 3 background agents to finish
```

The panel under the prompt lists the three Explore agents with their own time and token counts (about 16 seconds and 25k to 32k tokens each in the lesson). Then:

```text
● Agent "Map refund path in loop/" finished · 21s
● Agent "Map refund path in mcp_server/" finished · 24s
● Agent "Map refund path in support/" finished · 25s
● All three reports are in. Writing the notes file now.
● Write(notes/exploration.md)
  ⎿  Wrote 39 lines to notes/exploration.md
```

## Step 2: the scratchpad (the end of the answer)

```text
Refunds reach the backend through two paths. The support agent calls the backend
directly after its hooks and gates. The MCP path goes through the mcp_server tool.
The loop/ entry points route through the MCP path or stay text-only.

Open questions from the notes:
- Per-call limit gap: the $500 hook checks each call, but the cumulative check is
  only in harborline/backend.py. Two $400 refunds on a $649 order would each pass the
  hook.
- Two copies of the $500 limit: support/hooks.py and harborline/config.py both define
  it, so they can drift.
- Date parsing: harborline/backend.py and policy.py parse dates via policy.as_date,
  not normalize. That may break the dates convention, and I haven't checked it.
```

In the lesson, the answer's first line said the file was "about 50 lines", over the 40-line limit; the Write line above says 39. Trust the tool's record.

## Step 3: compact

```text
> /compact Keep the phase 1 summary; the details are in notes/exploration.md
  ⎿  Compacted (ctrl+o to see full summary)
  ⎿  Read notes/exploration.md (40 lines)
  ⎿  Read docs/conventions/dates.md (5 lines)
  ⎿  Read docs/conventions/money.md (5 lines)
```

## Step 4: phase 2

```text
● Explore(Answer open question 1 (per-call refund limit))
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)
● Waiting for the subagent to report on open question 1.
...
● Agent "Answer open question 1 (per-call refund limit)" finished · 27s
● Update(notes/exploration.md)
  ⎿  Added 1 line
```

The end of the answer:

```text
● Open question 1 is answered in notes/exploration.md.

  - Second $400 refund: blocked by harborline/backend.py:126, which rejects any refund
    that takes the order past its $649 total. The first $400 call passes the hook and
    guard, since both check only the current amount.
  - Gap: $450 then $199 on the same order passes every check. The $500 approval rule is
    never applied to the running total, and no test covers a split above $500.

  I read backend.py:120-129 myself. The rest came from the subagent's report and I did
  not run any tests.
```

The answer also estimated the file's length (wrongly); the commit below has the real count. Claude Code may suggest a next prompt in the input box, such as "Answer open question 2 the same way".

## Step 5: share it

```text
$ git add notes/exploration.md
$ git commit -m "Lesson 5.7: notes/exploration.md, the refund path mapped in two phases"
[main 37c0ab3] Lesson 5.7: notes/exploration.md, the refund path mapped in two phases
 1 file changed, 40 insertions(+)
 create mode 100644 notes/exploration.md
$ git push
...
   0810f6b..37c0ab3  main -> main
```

Your commit hashes will differ. `harborline/notes/exploration.md` in this kit is the file from the lesson's commit.
