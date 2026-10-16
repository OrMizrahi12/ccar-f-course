# Expected output: Lesson 5.3, Rules and path-scoped conventions

What each step showed in the lesson, copied from the screen. Claude's wording will differ on your machine, and so will token counts, times and commit ids. What should match: which reads print a `Loaded` line, which rules Claude quotes after each read, `Memory files` in `/context` counting only what loaded at launch, and the shape of the git output. Long passages are shortened with `…`.

## 1. Two scoped rules

```text
$ git status --short
$ mkdir -p .claude/rules
$ code .claude/rules/testing.md
$ code .claude/rules/tools.md
```

`git status --short` prints nothing (a clean tree), and so do the other commands: each `code …` opens the file in VS Code. The files are the kit's `harborline/.claude/rules/testing.md` and `tools.md`.

## 2. Watch them load

```text
$ claude
 Claude Code v2.1.301
 Haiku 5.5 · Claude Max
 ~/projects/harborline

❯ [In tools.md] Try "how does agent.py work?"
  auto mode on (shift+tab to cycle)
```

The plan name and the suggested prompt depend on your account. `[In tools.md]` appears because `tools.md` is open in the editor.

A file that no rule covers:

```text
❯ Read harborline/costs.py. Then quote any rules from .claude/rules that you were given, or say there are none.

  Read 1 file, listed 1 directory (ctrl+o to expand)

● I read harborline/costs.py. It prices API calls in US dollars per million tokens, with separate rates for input, output
  and cache reads, a higher Haiku rate for prompts over 100,000 tokens, and a 50% discount for batch requests.

  No rules from .claude/rules were given to me in this conversation. The directory does contain testing.md and tools.md,
  including the one you opened in the IDE, but I haven't read them. I can read them if you want their contents.
```

A test file (it matches `tests/**/*.py`):

```text
❯ Read tests/test_policy.py. Then quote any rules from .claude/rules that you were given, or say there are none.

  Read 1 file (ctrl+o to expand)
  Loaded .claude/rules/testing.md

● I read tests/test_policy.py. It covers the refund rules: date parsing, 30-day change of mind, 15 days for opened
  electronics, final sale (damage only), cancel before shipment, shipping refunds for late or mis-charged delivery, and
  approval above $500.

  I didn't read .claude/rules earlier, so my last answer was wrong to say none were given. The contents of testing.md are
  now in my context, and these are its rules:

  - Name each test for the behavior it checks.
  - Build small order dicts inside the test. Never edit data/*.json for a test.
  - Run the one test file first, then the whole suite.

  tools.md was not included, so I can't quote it.
```

The previous answer wasn't wrong: `testing.md` loaded only now, with the first matching read.

The MCP server (it matches `mcp_server/**`):

```text
❯ Read mcp_server/server.py. Then quote any rules from .claude/rules that you were given, or say there are none.

  Read 1 file (ctrl+o to expand)
  Loaded .claude/rules/tools.md

● I read mcp_server/server.py. It defines the Harborline MCP server: four tools (customer lookup, order lookup, order list,
  refund), two resources (the refund policy and the product catalog), a status-codes resource, and one prompt for order
  help. Tool errors go through tool_error.

  The contents of .claude/rules/tools.md are now in my context, and they say:

  - A description says what the tool returns, and when to use it instead of a similar tool.
  - Errors go through harborline/tool_errors.py: errorCategory, isRetryable and a message.

  My last answer said tools.md wasn't included. That was wrong; it is now in my context, so I'm quoting it here.
```

`/context`, scrolled up to the grid (the categories beside it):

```text
  Estimated usage by category
  System prompt: 3.7k tokens (0.4%)
  System tools: 19.4k tokens (1.9%)
  MCP server instructions: 1.2k tokens
  Memory files: 295 tokens (0.0%)
  Skills: 6.6k tokens (0.7%)
  Messages: 19k tokens (1.9%)
  Free space: 916.9k (91.7%)
  Autocompact buffer: 33k tokens (3.3%)
```

Your numbers will differ (they depend on your account's skills and connectors). `Memory files` counts what loaded at launch: your user file, `CLAUDE.md` and its two imports. The two path rules loaded later, with the reads.

```text
❯ /exit
Resume this session with:
claude --resume <your session id>
```

## 3. Commit and share

```text
$ git status --short
?? .claude/
$ git add .claude/rules
$ git commit -m "Lesson 5.3: path-scoped rules for tests and for tool definitions"
[main b46b623] Lesson 5.3: path-scoped rules for tests and for tool definitions
 2 files changed, 21 insertions(+)
 create mode 100644 .claude/rules/testing.md
 create mode 100644 .claude/rules/tools.md
$ git push
Enumerating objects: 7, done.
…
To https://github.com/YOUR-USERNAME/harborline.git
   5407458..b46b623  main -> main
```

Your commit ids will differ.
