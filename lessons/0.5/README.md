# Student kit: Lesson 0.5, Install Claude Code

Claude Certified Architect – Foundations (CCAR-F) · Section 0: Start Here · Lesson 0.5

This kit holds everything you need to repeat the lesson on your own computer: the install commands for every system, the exact prompts typed into Claude Code, the README that Claude Code wrote in the lesson, every step in order, what each screen showed, and what to do when something goes wrong.

By the end of the lesson you can:

1. Install Claude Code and the VS Code extension, and sign in
2. Run a first session and answer permission prompts
3. Install Node.js LTS with nvm

## What's in the kit

| File | What it is |
|---|---|
| `prompts.txt` | Everything typed into Claude Code in the lesson, in order: `/model`, Shift+Tab, the three prompts, the reason for the denial, and the git commands |
| `hello-claude/README.md` | The README that Claude Code wrote in the lesson, exactly as it was committed (40 lines). Yours will be worded differently. |
| `expected-output.md` | What each screen showed in the lesson, from `claude --version` to `node --version`, and how to compare your results |

The video is filmed on Ubuntu 24.04. Claude Code works the same way on every system once it's installed; the commands that differ are under [Windows, macOS and Linux](#windows-macos-and-linux).

## What you need

- **Lesson 0.4's project**: `~/projects/hello-claude` with `first_call.py`, `.env.example`, your `.env` (ignored by git) and two commits pushed to GitHub. If you skipped it, follow the kits for Lessons 0.3 and 0.4 first.
- **A Claude account that includes Claude Code**: a Claude Pro, Max, Team or Enterprise subscription, or a Claude Console account. The free Claude plan doesn't include Claude Code. The lesson signs in with a subscription; with a Console account, Claude Code's usage is billed to your API credits instead.
- **VS Code 1.94.0 or later**, from Lesson 0.3.
- About 25 minutes. This lesson sends nothing with your API key: the one command that would have spent API credit is denied on purpose.

**Before you start, check that your API key isn't set in your shell.** In Lesson 0.4 the key went into `.env` only, and that's where it should stay. If `ANTHROPIC_API_KEY` is set in your terminal, Claude Code asks whether to use it, and if you say yes it uses the key instead of your Claude plan. This check prints `unset` and never prints the key:

```bash
test -z "$ANTHROPIC_API_KEY" && echo unset
```

If it prints nothing, the variable is set: see [Troubleshooting](#troubleshooting).

## The steps (the lesson's order)

Lines that start with `#` are notes, not commands.

### 1. Install Claude Code and the VS Code extension

Open `~/projects/hello-claude` in VS Code and open its terminal (**Ctrl+`**). The install command comes from Anthropic's setup page, https://code.claude.com/docs/en/setup (copy it from there; it's the same command for macOS, Linux and WSL):

```bash
cd ~/projects/hello-claude
curl -fsSL https://claude.ai/install.sh | bash
```

- The installer shows no progress while it downloads, so wait for it to finish.
- It installs the `claude` command at `~/.local/bin/claude`. A native install keeps itself up to date in the background.
- On a fresh Ubuntu, `curl` may be missing: if the shell says `curl: command not found`, run `sudo apt install curl` first.

Check the version (the docs suggest a new terminal window for this, so the shell finds the new command):

```bash
claude --version              # the lesson: 2.1.296 (Claude Code)
```

The course uses Claude Haiku 5.5 in Claude Code, which needs **version 2.1.293 or later**. A newer version is fine.

Now the extension. In VS Code, open Extensions (**Ctrl+Shift+X**), search for `Claude Code`, and pick **Claude Code for VS Code** published by **Anthropic** (with the verified publisher badge). Click **Install**; if VS Code asks, click **Trust Publisher & Install**. The Spark icon appears in the Activity Bar on the left.

- The extension bundles its own copy of Claude Code for its chat panel, and its version number is the Claude Code version it bundles.
- It doesn't add a `claude` command to your terminal. That's what the install command above is for. The two share settings on disk (`~/.claude/settings.json`).

### 2. Sign in

Start Claude Code in the project folder:

```bash
claude
```

The first run walks you through a few screens:

1. **Theme.** Pick a theme; the lesson keeps the default, Dark mode, with **Enter**.
2. **Select login method.** Three options: `1. Claude account with subscription` (Pro, Max, Team, or Enterprise), `2. Anthropic Console account` (API usage billing), `3. 3rd-party platform`. With a Claude subscription, choose **1**. With only a Console account, choose 2.
3. **The browser opens** a page that says Claude Code would like to connect to your Claude chat account. Check the account it shows, then click **Authorize**. If a CAPTCHA appears, complete it. The page then says **Sign in successful**.
4. **Back in the terminal:** "Login successful. Press Enter to continue". Press **Enter**.
5. **Security notes.** Read them, then press **Enter**.
6. **"Use Claude Code's terminal setup?"** Choose **Yes, use recommended settings**. It lets you press **Shift+Enter** for a new line in your prompt.
7. **Folder trust.** Claude Code asks whether you trust the files in this folder. Careful: the highlighted default is **No, exit**. Press **Down** first, then **Enter** on **Yes, I trust this folder**. It's your own project, so it's safe to trust.

Claude Code opens. The banner above the prompt shows the version, the model and the folder. In the lesson the model was Opus 5.5, the default on a Max plan. The footer reads `auto mode on (shift+tab to cycle)`, and a note says auto mode is now Claude Code's default permission mode.

Your login is saved, so you won't need to sign in again on this computer. Now click the **Spark icon** in VS Code's Activity Bar. In the lesson, the extension's panel was already signed in, with the same login, and showed the account's email and usage: there was no second sign-in. If your panel shows a **Sign in** button instead, click it and complete the same browser steps.

### 3. Choose the model and effort

Back in the terminal, inside Claude Code:

```text
/model
```

The picker lists five rows: `1. Default (recommended)` (Opus 5.5 in the lesson), `2. Opus`, `3. Fable 5.1`, `4. Sonnet 5.5` and `5. Haiku 5.5`. Under the list: `Medium effort (default) ←/→ to adjust`, and the keys `Enter to set as default · s to use this session only · Esc to cancel`.

1. Arrow down to **Haiku 5.5**.
2. Leave the effort at **Medium**, Haiku 5.5's default. The left and right arrow keys would change it.
3. Press **Enter**. Claude Code answers: "Set model to Haiku 5.5 and saved as your default for new sessions".

**Enter** saves the choice as your default by writing `"model": "haiku"` to `~/.claude/settings.json`; **s** would switch for this session only. The course's rule: start with the smallest model that does the job, and step up only when the work shows you need to.

### 4. Your first session

**Switch to Manual mode.** Press **Shift+Tab** once. The footer changes from `auto mode on` to `manual mode on`. In Manual mode, Claude reads files freely but asks you before it edits a file or runs a command. In auto mode, a classifier reviews those actions instead of you. Shift+Tab changes only the session you're in.

Type the three prompts from `prompts.txt`, one at a time, and wait for each answer.

**Prompt 1**, reading only:

```text
Read first_call.py and requirements.txt. In three sentences, what does this project do?
```

Claude reads the two files and answers in three sentences. No permission prompt: reading files inside your project needs no approval.

**Prompt 2**, a new file:

```text
Add a short README.md that explains how to set up and run this project.
```

Claude may first run a command that only reads, such as `ls` or `git log`, without asking: Claude Code runs a built-in set of read-only commands in every mode. When it's ready to write, VS Code opens a diff with the proposed `README.md`, and the terminal asks **"Do you want to create README.md?"** Read the proposed file, check that it holds no real key (only a placeholder such as `sk-ant-...`), then choose **Yes**.

**Prompt 3**, a command:

```text
Run first_call.py to check that it still works.
```

Claude asks to run `.venv/bin/python first_call.py` (on Windows the path is different). The prompt says **"This command requires approval. Do you want to proceed?"** with four options:

1. **Yes**: run it once.
2. **Yes, and don't ask again for: `.venv/bin/python *`**: run it, and save a rule so commands that start this way never ask again in this repository.
3. **Yes, and switch to auto mode**: run it, and let the classifier review from now on.
4. **No**: don't run it.

Choose **No**, then press **Tab** to add a note, type the reason, and press **Enter**:

```text
No need: running it spends API credit, and it ran in the last lesson.
```

Claude Code shows "Tool use rejected". Claude acknowledges the reason and doesn't run the script. A denial with a reason keeps you in control and tells Claude what to do instead.

**Leave Claude Code and commit the README:**

```text
/exit
```

```bash
git status                     # README.md is untracked
git add README.md
git commit -m "Add a README"   # 1 file changed, 40 insertions in the lesson
git push
```

Your repository now has three commits on `main`.

### 5. Node.js LTS with nvm

Claude Code itself doesn't need Node.js. You install it now because Module 2 runs MCP tools with `npx`, which comes with Node.js. nvm (Node Version Manager) installs Node.js in your home folder, without `sudo`, and can switch between versions per project.

1. Open the nvm README at https://github.com/nvm-sh/nvm and find **Install & Update Script**. Copy the `curl` line from there; it names the current nvm release. In the lesson (v0.40.8):

   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh | bash
   ```

   The script clones nvm into `~/.nvm` and adds the lines that load it to your shell file (`~/.bashrc` on Ubuntu).
2. **Open a new terminal** (or run `source ~/.bashrc`), so the shell loads nvm. Check it:

   ```bash
   command -v nvm                 # prints: nvm
   ```

   `which nvm` prints nothing even when nvm works: nvm is a shell function, not a program file.
3. Install the current LTS (long-term support) release:

   ```bash
   nvm install --lts              # the lesson: Node.js v24.21.0 with npm v11.19.0
   node --version                 # v24.21.0
   npm --version                  # 11.19.0
   npx --version                  # 11.19.0
   ```

   nvm also makes it your default version (the alias `default` points to `lts/*`), so every new terminal uses it. If `--lts` installs a newer release than the lesson's, that's expected: it always picks the newest LTS. To match the lesson exactly, run `nvm install 24.21.0`.

## Windows, macOS and Linux

Inside Claude Code, everything is the same on every system: the sign-in, `/model`, Shift+Tab, the prompts and the permission prompts. Only the installs differ.

### Install Claude Code

| System | Command |
|---|---|
| macOS, Linux, WSL | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Windows PowerShell (prompt starts with `PS C:\`) | `irm https://claude.ai/install.ps1 \| iex` |
| Windows CMD (prompt starts with `C:\`, no `PS`) | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` |

Then open a new terminal and run `claude --version`. Check that it prints **2.1.293 or later**.

- **Windows:** you don't need to run the terminal as Administrator. Installing [Git for Windows](https://git-scm.com/downloads/win) is recommended: with it, Claude Code runs shell commands through Git Bash; without it, Claude Code uses PowerShell instead. In WSL, run the macOS/Linux command inside the WSL terminal, and run `claude` there too.
- **macOS with Homebrew:** there are two casks. `claude-code` tracks the **stable** channel, about a week behind, and on 2026-10-14 it served 2.1.287, which is too old for Claude Haiku 5.5. Use the native installer above, or the latest cask: `brew install --cask claude-code@latest`. Homebrew installs don't update themselves: run `brew upgrade claude-code@latest` from time to time.
- **WinGet:** `winget install Anthropic.ClaudeCode` also works, but it doesn't update itself (`winget upgrade Anthropic.ClaudeCode`). Check the version after installing.

### Check that your API key isn't set in the shell

| System | Command | Prints when the key isn't set |
|---|---|---|
| macOS, Linux, WSL | `test -z "$ANTHROPIC_API_KEY" && echo unset` | `unset` |
| Windows PowerShell | `if (-not $env:ANTHROPIC_API_KEY) { "unset" }` | `unset` |

### Install Node.js

| System | How |
|---|---|
| Linux, WSL | nvm, exactly as in step 5 |
| macOS | nvm, as in step 5. Install Apple's Xcode command line tools first: the nvm README says the install script fails without them. macOS uses zsh, so nvm writes to `~/.zshrc`; if you don't have that file, create it with `touch ~/.zshrc` and run the nvm script again. Load it with `source ~/.zshrc` or a new terminal. |
| Windows (native) | nvm doesn't run in PowerShell or CMD. Use WSL and follow the Linux steps, or install the LTS release from https://nodejs.org/en/download (v24.21.0 LTS on 2026-10-14). The nvm README lists Windows alternatives such as nvm-windows, which the nvm project doesn't support or develop. |

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `claude --version` | `2.1.296 (Claude Code)` |
| VS Code extension | Claude Code for VS Code, by Anthropic (verified); the Spark icon in the Activity Bar; the panel used the terminal's sign-in |
| Login method | 1. Claude account with subscription; Authorize in the browser; "Sign in successful" |
| Folder trust | default **No, exit**; Down, then Enter on **Yes, I trust this folder** |
| Starting model and mode | Opus 5.5 (the default on a Max plan); `auto mode on` |
| `/model` | Haiku 5.5, Medium effort (default), Enter: "Set model to Haiku 5.5 and saved as your default for new sessions"; `~/.claude/settings.json` holds `"model": "haiku"` |
| Shift+Tab | `manual mode on` |
| Prompt 1 | Claude read 2 files and answered in three sentences; no permission prompt |
| Prompt 2 | a read-only command ran without asking; diff in VS Code; "Do you want to create README.md?": Yes |
| Prompt 3 | Bash command `.venv/bin/python first_call.py`, "This command requires approval": No, with a reason; "Tool use rejected"; the script didn't run |
| Commit | "Add a README": 1 file changed, 40 insertions; pushed (`main -> main`); three commits on GitHub |
| nvm | v0.40.8; `command -v nvm` prints `nvm` |
| Node.js | `nvm install --lts`: v24.21.0, npm 11.19.0, `npx` 11.19.0 |

## Troubleshooting

- **`claude: command not found`** (Windows: `'claude' is not recognized`): first open a new terminal window. If it still fails, the install folder isn't on your PATH. Check that the program exists with `ls -la ~/.local/bin/claude`. If it does, add the folder to your PATH once, for your shell:
  - Bash (Linux): `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc` then `source ~/.bashrc`
  - Zsh (macOS): `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc` then `source ~/.zshrc`
  - Windows PowerShell: run these two lines, then restart the terminal:

    ```powershell
    $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    [Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
    ```


  A terminal inside VS Code takes its PATH from VS Code, so quit and reopen VS Code too. The installer prints a `Setup notes:` line when the folder isn't on your PATH.
- **The extension works, but `claude` isn't found in the terminal**: the extension's bundled copy serves its panel only. Run the install command from step 1.
- **`The token '&&' is not a valid statement separator`**: you're in PowerShell, not CMD; use the PowerShell command. **`'irm' is not recognized`**: you're in CMD; use the CMD command.
- **`/model` has no Haiku 5.5, or your version is below 2.1.293**: run `claude update` (native install). With Homebrew, install `claude-code@latest` instead of `claude-code`. For the extension, update it in the Extensions view: its version is the Claude Code version it bundles.
- **Claude Code asks whether to use an API key**, or you see "This organization has been disabled": `ANTHROPIC_API_KEY` is set in your shell. For this course, keep the key in `.env` only. Run `unset ANTHROPIC_API_KEY` (PowerShell: `Remove-Item Env:ANTHROPIC_API_KEY`), remove any `export ANTHROPIC_API_KEY=...` line from `~/.bashrc`, `~/.zshrc` or `~/.profile`, open a new terminal and start `claude` again. Inside Claude Code, `/status` shows which sign-in is in use.
- **The browser didn't open during sign-in**: at the login prompt, press `c` to copy the sign-in link, and paste it into your browser. In WSL or over SSH, the browser may show a code instead of returning you to the terminal: paste it at `Paste code here if prompted`.
- **Sign-in failed and you can't tell why**: inside Claude Code, run `/logout`, close Claude Code, start `claude` again and sign in again.
- **Claude Code closed at the folder trust question**: Enter on the default, **No, exit**, closes it. Run `claude` again, press **Down**, then **Enter** on **Yes, I trust this folder**.
- **The extension doesn't appear after installing**: restart VS Code, or run **Developer: Reload Window** from the Command Palette (**Ctrl+Shift+P**).
- **The next session starts in auto mode again**: Shift+Tab changes only the current session. To start every session in Manual mode, add this to `~/.claude/settings.json` (keep any keys already there, such as `"model"`):

  ```json
  {
    "permissions": {
      "defaultMode": "default"
    }
  }
  ```

  `default` is Manual mode's setting value.
- **You chose "Yes, and don't ask again" by mistake**: the rule was saved for this repository in `.claude/settings.local.json`. Run `/permissions` inside Claude Code to see your rules and remove it.
- **The model switched back after a restart**: you pressed **s** (this session only) in `/model`. Open `/model` again and press **Enter** on Haiku 5.5.
- **`nvm: command not found`**, or `command -v nvm` prints nothing: close the terminal and open a new one, or run `source ~/.bashrc` (zsh: `source ~/.zshrc`).
- **Never paste your API key into a prompt**, and check every file Claude writes before you commit it.

## Key terms

- **Claude Code:** Anthropic's coding agent that reads your files, edits them and runs commands, in the terminal or in VS Code.
- **Agent:** a model that works in a loop, choosing tools and acting on the results until the task is done.
- **Tool:** an action the model can ask to take, such as reading a file or running a command.
- **Permission prompt:** Claude Code's request for your approval before it edits a file or runs a command.
- **Permission mode:** the session setting that decides what runs without asking. Manual asks before edits and commands; auto lets a classifier review instead.
- **Effort:** how much the model thinks before answering; higher costs more tokens.

## Sources (checked 2026-10-14)

- Claude Code advanced setup (install commands, `claude --version`, Homebrew casks and release channels, Windows notes): https://code.claude.com/docs/en/setup
- Claude Code quickstart (first session, sign-in, first questions): https://code.claude.com/docs/en/quickstart
- Claude Code in VS Code (install, the bundled CLI, the Spark icon, sign-in): https://code.claude.com/docs/en/vs-code
- Authentication (account types, `ANTHROPIC_API_KEY` and the subscription): https://code.claude.com/docs/en/authentication
- Model configuration (`/model`, Enter and `s`, effort levels, Haiku 5.5 needs v2.1.293 or later): https://code.claude.com/docs/en/model-config
- Permission modes (Manual and auto, Shift+Tab, the starting mode, `defaultMode`): https://code.claude.com/docs/en/permission-modes
- Permissions (what needs approval, read-only commands, "don't ask again", `/permissions`): https://code.claude.com/docs/en/permissions
- Troubleshoot installation and login (PATH, wrong shell, Homebrew, login): https://code.claude.com/docs/en/troubleshoot-install
- nvm README (install script, `command -v nvm`, `nvm install --lts`, macOS and Windows notes): https://github.com/nvm-sh/nvm
- Node.js releases (v24.21.0 LTS): https://nodejs.org/dist/index.json and https://nodejs.org/en/download

Claude Code changes quickly. If a screen doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes.
