# Setup sheet: Linux (Ubuntu and Debian)

This is the system the lesson is filmed on (Ubuntu 24.04, Python 3.12.3). The commands are the ones on screen, in the same order. Checked against the official install docs on 2026-10-13 (links at the end). On another distribution, use its package manager for the same pieces: git, Python 3.10 or newer with `venv`, VS Code, and the GitHub CLI.

Open a terminal with **Ctrl+Alt+T**.

## 1. Python and git

```bash
python3 --version
git --version
sudo apt update
sudo apt install git python3-venv
git --version
```

Answer `y` when apt asks to continue. Ubuntu 24.04 ships Python 3.12 (the lesson shows 3.12.3) but not git or the `venv` module, so a fresh system says `git: command not found` at first. The course needs Python 3.10 or newer; if `python3 --version` shows something older, install a newer Python before you go on.

## 2. VS Code

1. Download the **.deb** package (Debian, Ubuntu) from https://code.visualstudio.com/download. It saves to `~/Downloads`.
2. Install it (press **Tab** to complete the file name):
   ```bash
   sudo apt install ./Downloads/code_*.deb
   ```
   Answer `y` to continue, and **Yes** when the installer asks to add Microsoft's apt repository, so VS Code updates with the rest of the system.
3. Check: `code --version`.

## 3. The project and the Python extension

```bash
mkdir -p ~/projects/hello-claude
cd ~/projects/hello-claude
code .
```

VS Code opens in **Restricted Mode** because it hasn't seen this folder before. It's your own empty folder: click **Manage**, then **Trust**.

Open Extensions (**Ctrl+Shift+X**), search for `python`, and install **Python** by **Microsoft**.

## 4. The environment

Open the VS Code terminal with **Ctrl+`** (it starts in the project folder):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic==1.13.0 python-dotenv==1.2.4
pip freeze > requirements.txt
code requirements.txt
python -c "import anthropic; print(anthropic.__version__)"
```

The prompt starts with `(.venv)` once the environment is active. `requirements.txt` gets 16 lines, and the last command prints `1.13.0`. VS Code's status bar should show the `.venv` interpreter; if not, run **Python: Select Interpreter** (**Ctrl+Shift+P**) and pick it.

## 5. git: ignore, identity, first commit

```bash
git init -b main
code .gitignore
```

Put these three lines in `.gitignore` and save (or copy the kit's `hello-claude/.gitignore`):

```
.venv/
.env
__pycache__/
```

```bash
git status
git config --global user.name "Your Name"
git config --global user.email "ID+USERNAME@users.noreply.github.com"
git add .
git commit -m "Set up the hello-claude workbench"
git log --oneline
```

`git status` must list only `.gitignore` and `requirements.txt`. For the email, use your GitHub no-reply address (GitHub: **Settings**, **Emails**, **Keep my email addresses private**), or any address you're happy to publish.

## 6. GitHub CLI, sign-in and push

Copy the **Debian** install block from the official page, https://github.com/cli/cli/blob/trunk/docs/install_linux.md (the copy button takes all of it), paste it into the terminal, read it, and press Enter. It adds GitHub's signed package repository and installs `gh`. Use it rather than `sudo apt install gh` from your distribution's own repositories: the GitHub CLI docs warn that the community-packaged versions 2.45.x and 2.46.x no longer work with GitHub. Then:

```bash
gh --version
gh auth login
```

Answer: **GitHub.com** · **HTTPS** · **Yes** (authenticate git with your GitHub credentials) · **Login with a web browser**. Press **Enter** to open the browser, check the account, **Continue**, enter the one-time code, **Continue**, review the permissions and **Authorize**. GitHub may ask you to confirm with a passkey, GitHub Mobile, an authenticator app or an email code.

```bash
gh auth status
gh repo create hello-claude --private --source=. --push
gh repo view --web
```

The repository page shows one commit, `.gitignore` and `requirements.txt`, and no `.venv`.

## Official sources
- VS Code on Linux: https://code.visualstudio.com/docs/setup/linux
- venv: https://docs.python.org/3/library/venv.html
- pip freeze: https://pip.pypa.io/en/stable/cli/pip_freeze/
- git init: https://git-scm.com/docs/git-init
- GitHub CLI on Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md
- gh auth login: https://cli.github.com/manual/gh_auth_login · gh repo create: https://cli.github.com/manual/gh_repo_create
- Python SDK (requires Python 3.10 or later): https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python
