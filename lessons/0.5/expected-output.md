# Expected output: Lesson 0.5, Claude Code on your project

What each step showed in the lesson, on Ubuntu 24.04, with Claude Code 2.1.296 signed in with a Claude subscription. Your version numbers may be newer, and Claude's answers and README will be worded differently: compare the shape, not the words.

## The install

```text
$ claude --version
2.1.296 (Claude Code)
```

Anything at **2.1.293 or later** works with Claude Haiku 5.5.

In VS Code, the extension is **Claude Code for VS Code**, published by Anthropic (verified). After installing it, the Spark icon appears in the Activity Bar.

## The first run of `claude`

The screens, in order:

| Screen | What you do |
|---|---|
| Theme picker | Enter on the default, Dark mode (or pick another) |
| Select login method: `1. Claude account with subscription` (Pro, Max, Team, or Enterprise) · `2. Anthropic Console account` (API usage billing) · `3. 3rd-party platform` | 1 for a subscription |
| Browser: Claude Code would like to connect to your Claude chat account | Authorize (and a CAPTCHA, if one appears) |
| Browser: Sign in successful | Go back to the terminal |
| Terminal: `Login successful. Press Enter to continue` | Enter |
| Security notes | Enter |
| `Use Claude Code's terminal setup?` | Yes, use recommended settings (Shift+Enter for newlines) |
| Folder trust, with **No, exit** highlighted | Down, then Enter on **Yes, I trust this folder** |

Then the session opens. The banner shows the version, the model and the folder: `~/projects/hello-claude`. In the lesson the model was Opus 5.5, the default on a Max plan; yours depends on your plan. The footer reads:

```text
auto mode on (shift+tab to cycle)
```

with a note that auto mode is now Claude Code's default permission mode.

In VS Code, the Claude Code panel (Spark icon) was already signed in with the same login and showed the account's email and usage.

## `/model`

The picker in the lesson:

```text
1. Default (recommended)   Opus 5.5
2. Opus
3. Fable 5.1
4. Sonnet 5.5
5. Haiku 5.5

Medium effort (default) ←/→ to adjust
Enter to set as default · s to use this session only · Esc to cancel
```

After Down to Haiku 5.5 and Enter:

```text
Set model to Haiku 5.5 and saved as your default for new sessions
```

`~/.claude/settings.json` now holds `"model": "haiku"`. The rows on your picker can differ with your plan and your Claude Code version; what matters is a Haiku 5.5 row, saved with Enter.

## Shift+Tab

One press, and the footer changes to:

```text
manual mode on
```

## Prompt 1: a question, reading only

Claude read the two files (`first_call.py`, `requirements.txt`) and answered in three sentences. There was no permission prompt. A good answer says that the project makes one call to Claude Haiku 5.5 with the Anthropic Python SDK, that it loads the API key from `.env`, and that it prints the reply's text, the stop reason, the token counts and the request ID. It shouldn't say anything about the key's value: Claude didn't need to read `.env`, and didn't.

## Prompt 2: a new file

Claude first ran a read-only command (such as `ls` or `git log`) without asking. Then VS Code opened a diff of the proposed `README.md`, and the terminal asked:

```text
Do you want to create README.md?
```

The answer in the lesson: **Yes**. The file Claude wrote is in this kit: `hello-claude/README.md` (40 lines). It has:

- a title, `hello-claude`, and a one-line summary of `first_call.py`;
- **Setup**: create and activate a virtual environment, `pip install -r requirements.txt`, then `cp .env.example .env` and paste your key after the `=`, shown only as the placeholder `ANTHROPIC_API_KEY=sk-ant-...`;
- **Run**: `python first_call.py`, and what you should see.

Your README may differ: other headings, other words, more or fewer steps. Check three things before you commit it: the setup steps are right for your project, it says the key goes in `.env`, and it holds no real key. One detail in the lesson's README: it links to `console.anthropic.com` for getting a key. That address now redirects to `platform.claude.com`, the Console you used in Lesson 0.4, so the link still works.

## Prompt 3: a command, denied

```text
Bash command

  .venv/bin/python first_call.py
  ...

This command requires approval

Do you want to proceed?
  1. Yes
  2. Yes, and don't ask again for: .venv/bin/python *
  3. Yes, and switch to auto mode
  4. No
```

Above the command, Claude Code's docs show a short description of what it does; the footer lists `Esc to cancel` and `Tab to amend`. In the lesson: **No**, then Tab, then the reason:

```text
No need: running it spends API credit, and it ran in the last lesson.
```

Claude Code printed `Tool use rejected`. Claude acknowledged the reason and didn't run the script, so no API call was made.

## The commit

```text
$ git status
...
Untracked files:
        README.md

$ git add README.md
$ git commit -m "Add a README"
 1 file changed, 40 insertions(+)
$ git push
...
   main -> main
```

The lesson's commit added 40 lines; yours will match the length of your README. On GitHub, the repository now has three commits: "Set up the hello-claude workbench", "Add the first Claude API call" and "Add a README".

## Node.js with nvm

```text
$ command -v nvm
nvm
$ nvm install --lts
...                     (nvm installs Node.js v24.21.0 and npm v11.19.0,
                         and sets the default alias to lts/*)
$ node --version
v24.21.0
$ npm --version
11.19.0
$ npx --version
11.19.0
```

`nvm install --lts` installs the newest LTS release on the day you run it, so your version may be newer. To match the lesson exactly, run `nvm install 24.21.0`.

## What to compare with yours

- `claude --version` prints 2.1.293 or later.
- `/model` says Haiku 5.5 was saved as your default.
- The footer says `manual mode on` before the three prompts.
- Prompt 1: no permission prompt. Prompt 2: a prompt before the file is created. Prompt 3: a prompt before the command runs, and nothing runs after your No.
- `git status` shows only `README.md`, and never `.env`.
- `node --version`, `npm --version` and `npx --version` each print a version.
