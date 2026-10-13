# Student kit: Lesson 0.3, Your workbench: VS Code, Python and git

Claude Certified Architect – Foundations (CCAR-F) · Section 0: Start Here · Lesson 0.3

This kit holds everything you need to build the lesson's workbench on your own computer: the two project files exactly as they stand at the end of the lesson, every command in order, and a setup sheet for Windows, macOS and Linux. Nothing here is a made-up sample: `requirements.txt` is the file `pip freeze` wrote in the lesson, line for line.

By the end of the lesson you can:

1. Install VS Code, Python 3.12 and git
2. Create a project with its own environment and pinned packages
3. Commit it and push it to GitHub

## What's in the kit

| File | What it is |
|---|---|
| `setup-windows.md` | The whole workbench on Windows 10 or 11 (PowerShell) |
| `setup-macos.md` | The whole workbench on macOS (Terminal) |
| `setup-linux.md` | The whole workbench on Ubuntu or Debian: the exact commands from the lesson |
| `hello-claude/requirements.txt` | The 16 pinned packages from `pip freeze`: `anthropic==1.13.0`, `python-dotenv==1.2.4` and their dependencies |
| `hello-claude/.gitignore` | The three lines from the lesson: `.venv/`, `.env`, `__pycache__/` |

The video is filmed on Ubuntu 24.04. If you use Windows or a Mac, follow your setup sheet: it has the same steps with your system's commands.

## What you need

- A computer running Windows 10 or 11, macOS, or Linux (the lesson uses Ubuntu 24.04), with an internet connection.
- Permission to install software (on Linux, `sudo`; on a work computer, you may need your IT team).
- A GitHub account. A free one is enough; create it at https://github.com/signup before you start.
- About 30 minutes. This lesson needs no API key and costs nothing.

## The steps (the lesson's order, on Ubuntu)

Your setup sheet has the same steps for your system. Lines that start with `#` are notes, not commands.

### 1. The system: Python and git

```bash
python3 --version          # the lesson: Python 3.12.3
git --version              # on a fresh Ubuntu: command not found
sudo apt update
sudo apt install git python3-venv
git --version              # the lesson: git version 2.43.0
```

`apt` asks you to confirm: answer `y`. Ubuntu 24.04 ships Python 3.12, but not the `venv` module or git, so both come from the package manager.

### 2. The editor: VS Code and the Python extension

1. Go to https://code.visualstudio.com/download and take the **.deb** package (Debian, Ubuntu). It saves to your Downloads folder.
2. Install it with apt (press **Tab** to complete the long file name):
   ```bash
   sudo apt install ./Downloads/code_*.deb
   ```
   Confirm with `y`. When the installer asks **Add Microsoft apt repository for Visual Studio Code?**, choose **Yes**, so VS Code updates with the rest of your system. A last line from apt that starts with `N:` is a harmless note.
3. Check: `code --version` (the lesson: 1.141.1).
4. Make the project folder and open it in VS Code:
   ```bash
   mkdir -p ~/projects/hello-claude
   cd ~/projects/hello-claude
   code .
   ```
5. VS Code opens the new folder in **Restricted Mode**. It's your own empty folder, so click **Manage**, then **Trust**.
6. Open Extensions (**Ctrl+Shift+X**), search for `python`, and install **Python** published by **Microsoft**. Watch out for lookalikes from other publishers.

### 3. The environment: a virtual environment and pinned packages

Open the terminal inside VS Code with **Ctrl+`** (backtick). It opens in the project folder.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic==1.13.0 python-dotenv==1.2.4
pip freeze > requirements.txt
code requirements.txt
python -c "import anthropic; print(anthropic.__version__)"
```

- After `activate`, the prompt starts with `(.venv)`: from here on, `pip` installs into this project only.
- `requirements.txt` has 16 lines: the two packages you asked for, plus everything they depend on. Compare yours with `hello-claude/requirements.txt` in this kit.
- The status bar at the bottom of VS Code shows the interpreter it picked: `.venv (3.12.3)` in the lesson. If it shows another Python, run **Python: Select Interpreter** from the Command Palette (**Ctrl+Shift+P**) and pick the one in `.venv`.
- The last command prints `1.13.0`.

Starting from this kit instead? Copy `requirements.txt` into the folder and run `pip install -r requirements.txt` inside the activated environment.

### 4. git and GitHub

**Start the repository and add a `.gitignore` before the first commit:**

```bash
git init -b main
code .gitignore
```

Type three lines into `.gitignore` and save (**Ctrl+S**), or copy the kit's file:

```
.venv/
.env
__pycache__/
```

`.venv/` is the environment (rebuild it from `requirements.txt` instead), `.env` is where your API key will live, and `__pycache__/` holds files Python compiles. Then check what git would track:

```bash
git status
```

You should see `.gitignore` and `requirements.txt` only. No `.venv`.

**Tell git who you are (once per computer), and commit:**

```bash
git config --global user.name "Your Name"
git config --global user.email "ID+USERNAME@users.noreply.github.com"
git add .
git commit -m "Set up the hello-claude workbench"
git log --oneline
```

To keep your personal email private, use your GitHub no-reply address: on GitHub, **Settings**, **Emails**, tick **Keep my email addresses private**, and copy the address shown there. The commit reports 2 files changed; `git log --oneline` shows one commit on `main`.

**Install the GitHub CLI (`gh`).** On Ubuntu, use the official Debian/Ubuntu block from https://github.com/cli/cli/blob/trunk/docs/install_linux.md (the copy button copies all of it). Paste it into the terminal, read it, then press Enter. It adds GitHub's package repository and installs `gh`. The block, as published on 2026-10-13:

```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
	&& sudo mkdir -p -m 755 /etc/apt/keyrings \
	&& out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
	&& cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
	&& sudo mkdir -p -m 755 /etc/apt/sources.list.d \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
	&& sudo apt update \
	&& sudo apt install gh -y
```

Always copy it fresh from the official page; it can change. Check: `gh --version` (the lesson: 2.102.0).

**Sign in:**

```bash
gh auth login
```

Answer the questions: **GitHub.com**; **HTTPS** for git operations; **Yes** to authenticate git with your GitHub credentials; **Login with a web browser**. `gh` shows a one-time code (and copies it to the clipboard). Press **Enter** and the browser opens GitHub's device activation page:

1. Check the account shown, then **Continue**.
2. Paste or type the one-time code, then **Continue**.
3. Read what the GitHub CLI will be allowed to do, make sure the request really came from you, and click **Authorize**.
4. GitHub may ask you to confirm it's you, with a passkey, GitHub Mobile, an authenticator app or a code by email. Do that step.

Back in the terminal, check: `gh auth status` says you're logged in to github.com.

**Create the GitHub repository and push:**

```bash
gh repo create hello-claude --private --source=. --push
gh repo view --web
```

`gh` creates the private repository on your account, adds it as the project's remote, and pushes the commit on `main`. The browser shows the repo: one commit, two files, and no `.venv`.

## What the lesson showed

| Check | Result in the lesson |
|---|---|
| `python3 --version` | Python 3.12.3 |
| `git --version` | git version 2.43.0 |
| `code --version` | 1.141.1 |
| `requirements.txt` | 16 lines |
| `anthropic.__version__` | 1.13.0 |
| First commit | 2 files changed, 19 insertions |
| `gh --version` | 2.102.0 |
| GitHub | a private `hello-claude` repository: `.gitignore` and `requirements.txt` |

Newer versions of VS Code, git and `gh` are fine. Keep Python at 3.10 or newer (the course uses 3.12) and keep the two pinned packages as they are, so your code behaves like the course's.

## Troubleshooting

- **`python3 -m venv .venv` fails with "ensurepip is not available"** (Ubuntu, Debian): the venv module isn't installed. Run `sudo apt install python3-venv`, delete the half-made `.venv` folder, and run the command again.
- **`pip` installs somewhere else, or says "externally-managed-environment"**: the environment isn't active. Run `source .venv/bin/activate` (Windows: `.venv\Scripts\Activate.ps1`) and check that the prompt starts with `(.venv)`.
- **A new terminal lost the environment**: each new terminal starts without it. Activate it again in every new terminal.
- **`code: command not found`** (macOS): in VS Code, run **Shell Command: Install 'code' command in PATH** from the Command Palette, then open a new terminal. On Windows, open a new terminal after installing.
- **PowerShell won't run `Activate.ps1`** (Windows): allow local scripts for your account once with `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`, then activate again.
- **`git status` lists `.venv`**: `.gitignore` isn't saved, or it's in the wrong folder or has another name. It must be named exactly `.gitignore`, in the project folder. If you already ran `git add`, unstage the folder with `git rm -r --cached .venv` after fixing `.gitignore`.
- **`git commit` says "Please tell me who you are"**: run the two `git config --global` commands, then commit again.
- **`gh repo create` says the name already exists**: you already have a `hello-claude` repository on GitHub. Pick another name, or delete the old one on GitHub first.
- **The browser didn't open during `gh auth login`**: open https://github.com/login/device yourself and type the one-time code from the terminal.
- **`ModuleNotFoundError: No module named 'anthropic'`**: the code ran with another Python. Activate `.venv` (and in VS Code, select the `.venv` interpreter), then run it again.

## Key terms

- **Virtual environment:** a project-private Python with its own packages (`.venv`). Nothing leaks between projects, and nothing touches the system's Python.
- **Pinned dependency:** an exact version (`anthropic==1.13.0`), so every machine installs the same code.
- **requirements.txt:** the list of pinned packages that rebuilds the environment anywhere: `pip install -r requirements.txt`.
- **.gitignore:** the list of files git must never track (`.venv/`, `.env`).
- **Remote repository:** the copy of your project on GitHub that you push to.

## Sources (checked 2026-10-13)

- Python, *venv: creation of virtual environments*: https://docs.python.org/3/library/venv.html
- pip, *pip freeze* and *Requirements files*: https://pip.pypa.io/en/stable/cli/pip_freeze/ and https://pip.pypa.io/en/stable/user_guide/
- Claude Agent SDK quickstart (prerequisites: Python 3.10+): https://code.claude.com/docs/en/agent-sdk/quickstart
- Anthropic Python SDK (requires Python 3.10 or later): https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python
- VS Code download and Linux setup: https://code.visualstudio.com/download and https://code.visualstudio.com/docs/setup/linux
- VS Code Workspace Trust: https://code.visualstudio.com/docs/editing/workspaces/workspace-trust
- git, *git init* (`-b`) and *gitignore*: https://git-scm.com/docs/git-init and https://git-scm.com/docs/gitignore
- GitHub CLI, Linux install: https://github.com/cli/cli/blob/trunk/docs/install_linux.md ; manual: https://cli.github.com/manual/gh_auth_login and https://cli.github.com/manual/gh_repo_create
- GitHub, setting your commit email address: https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address

Install steps change over time. If a step doesn't match what you see, follow the official page.

## What's next

Before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes.
