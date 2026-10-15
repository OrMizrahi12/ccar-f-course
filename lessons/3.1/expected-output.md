# Expected output: Lesson 3.1, The Claude Agent SDK from zero

What each step printed in the lesson, on Ubuntu 24.04 with Python 3.12, from the `harborline` folder with `.venv` active. The terminal wrapped long lines; they're shown unwrapped here, and long output is shortened with `…`.

**What will differ on yours:** Claude's wording (its answers are written fresh each time), the cost in the last digit, pip's download lines, and your commit IDs. Each section says what should match.

## Step 1: Install the SDK

```text
(.venv) $ git status --short
(.venv) $ code loop/agent.py
(.venv) $ code requirements.txt
(.venv) $ clear; pip install -r requirements.txt
Requirement already satisfied: … (one line for each package you already have)
…
Requirement already satisfied: pycparser in ./.venv/lib/python3.12/site-packages (from cffi>=2.0.0->cryptography>=3.4.0->pyjwt[crypto]>=2.10.1->mcp==2.3.0->-r requirements.txt (line 5)) (3.11)
Using cached claude_agent_sdk-0.2.165-py3-none-manylinux_2_17_x86_64.whl (107.8 MB)
Installing collected packages: claude-agent-sdk
Successfully installed claude-agent-sdk-0.2.165
```

What should match: `git status --short` prints nothing, and pip ends with `Successfully installed claude-agent-sdk-0.2.165`. Yours downloads the wheel instead of "Using cached" (it was in pip's cache on the lesson's computer), and the file name matches your system.

`requirements.txt` after the edit:

```text
# Exact versions, checked 2026-10-13. Later modules add packages here.
anthropic==1.13.0
python-dotenv==1.2.4
pytest==9.1.1
mcp==2.3.0
claude-agent-sdk==0.2.165
```

## Step 2: Your functions as tools

Nothing prints: `support/tools.py` is typed and saved. VS Code creates the `support` folder on save. Compare your file with the kit's.

## Step 3: Options and a first run

```text
(.venv) $ clear; python -m support.hello_agent T-008
⚠ claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set and takes precedence over your claude.ai login · Unset it to load your organization's connectors
tools: ['mcp__harborline__get_customer', 'mcp__harborline__lookup_order']
[tool] mcp__harborline__get_customer {'email': 'elijah.petrov@example.com'}
[tool] mcp__harborline__lookup_order {'order_id': 'HL-10196'}
[text] Hi Elijah, order HL-10196 (Stoneware Vase) has shipped with Parcelway, tracking number PW4974187387. The estimated delivery is October 16, 2026, one day after the October 15 date we promised. I can't see why the shipping email didn't reach you, but the tracking number above should show the latest status on the carrier's site.

success: 3 turns, $0.0006
```

What should match: the `tools:` line lists only the two `mcp__harborline__` tools; `get_customer` with the email comes before `lookup_order` with `HL-10196`; the answer says the order shipped with Parcelway, with tracking number `PW4974187387`; the run ends with `success` in about 3 turns, for well under a cent. The first line appears only if you're signed in to Claude Code on that computer.

## Step 4: Commit

```text
(.venv) $ clear; git status --short
 M requirements.txt
?? support/
(.venv) $ git add requirements.txt support
(.venv) $ git commit -m "Lesson 3.1: a first agent on the Claude Agent SDK, with in-process tools"
[main b0148e9] Lesson 3.1: a first agent on the Claude Agent SDK, with in-process tools
 3 files changed, 99 insertions(+)
 create mode 100644 support/hello_agent.py
 create mode 100644 support/tools.py
(.venv) $ git push
Enumerating objects: 8, done.
Counting objects: 100% (8/8), done.
Delta compression using up to 24 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (6/6), 2.01 KiB | 2.01 MiB/s, done.
Total 6 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/YOUR-USERNAME/harborline.git
   d6e2738..b0148e9  main -> main
```

What should match: `3 files changed, 99 insertions(+)` with the two `create mode` lines, and `main -> main`. What will differ: the commit IDs (yours are your own), the object counts and sizes, the thread count, and the URL (your own account).
