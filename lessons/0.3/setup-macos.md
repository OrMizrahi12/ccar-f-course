# Setup sheet: macOS

The lesson is filmed on Ubuntu Linux. This sheet gives the same workbench on a Mac (Apple silicon or Intel), step for step. Every command below was checked against the official install docs on 2026-10-13 (links at the end).

Open **Terminal** (Spotlight: **Cmd+Space**, type `Terminal`).

The easiest route uses **Homebrew**, the package manager most Mac developers use. If you don't have it, install it with the one-line command on https://brew.sh and follow what it prints at the end (it may ask you to add Homebrew to your `PATH`). Each step below also gives a way without Homebrew.

## 1. git

Either install Apple's Command Line Tools, which include git:

```bash
xcode-select --install
```

or, with Homebrew:

```bash
brew install git
```

Check: `git --version`.

## 2. Python 3.12

The course uses Python 3.12 (the SDK needs 3.10 or newer). Don't rely on the Python that comes with macOS: VS Code's docs say the macOS system Python isn't supported.

- **Homebrew:**
  ```bash
  brew install python@3.12
  ```
- **Or python.org:** from https://www.python.org/downloads/macos/, download the **macOS 64-bit universal2 installer** for Python **3.12.10** (the last 3.12 release with a macOS installer) and double-click the `.pkg`.

Check in a new Terminal window:

```bash
python3.12 --version
```

It should print `Python 3.12.x`. You'll create the environment with `python3.12`, so it uses exactly this version.

## 3. VS Code

1. Download VS Code for macOS from https://code.visualstudio.com/download (**Universal** works on Apple silicon and Intel). It comes as a disk image (`.dmg`).
2. Open it and drag **Visual Studio Code.app** into **Applications**. Launch it from there.
3. Add the `code` command: open the Command Palette (**Cmd+Shift+P**), run **Shell Command: Install 'code' command in PATH**, then open a new Terminal window. Check: `code --version`.

With Homebrew, `brew install --cask visual-studio-code` does steps 1 and 2.

## 4. The project and the Python extension

```bash
mkdir -p ~/projects/hello-claude
cd ~/projects/hello-claude
code .
```

VS Code opens the folder in **Restricted Mode** (or asks whether you trust its authors). It's your own empty folder, so trust it: **Manage**, then **Trust**.

Open Extensions (**Cmd+Shift+X**), search for `python`, and install **Python** by **Microsoft**.

## 5. The environment

Open the VS Code terminal with **Ctrl+`** (it starts in the project folder):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install anthropic==1.13.0 python-dotenv==1.2.4
pip freeze > requirements.txt
code requirements.txt
python -c "import anthropic; print(anthropic.__version__)"
```

The prompt starts with `(.venv)` once the environment is active. Expect 16 lines in `requirements.txt` and `1.13.0` from the last command. Or use the kit's `hello-claude/requirements.txt` directly: `pip install -r requirements.txt`.

VS Code's status bar should show the `.venv` interpreter. If not, run **Python: Select Interpreter** (**Cmd+Shift+P**) and pick the one in `.venv`.

## 6. git: ignore, identity, first commit

```bash
git init -b main
code .gitignore
```

Put these three lines in `.gitignore` and save, or copy the kit's `hello-claude/.gitignore` (in Finder, press **Cmd+Shift+.** to see files that start with a dot):

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

`git status` must list only `.gitignore` and `requirements.txt`, never `.venv`. For the email, use your GitHub no-reply address (GitHub: **Settings**, **Emails**, **Keep my email addresses private**).

## 7. GitHub CLI, sign-in and push

```bash
brew install gh
gh --version
```

Without Homebrew, download the macOS installer from the GitHub CLI releases page (link below).

```bash
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
- Homebrew: https://brew.sh
- git on macOS: https://git-scm.com/install/mac
- Python on macOS: https://www.python.org/downloads/macos/ · Homebrew formula: https://formulae.brew.sh/formula/python@3.12
- VS Code on macOS: https://code.visualstudio.com/docs/setup/mac
- Python in VS Code (system Python on macOS not supported): https://code.visualstudio.com/docs/python/python-tutorial
- venv: https://docs.python.org/3/library/venv.html
- GitHub CLI on macOS: https://github.com/cli/cli/blob/trunk/docs/install_macos.md · releases: https://github.com/cli/cli/releases/latest
- gh auth login: https://cli.github.com/manual/gh_auth_login · gh repo create: https://cli.github.com/manual/gh_repo_create
- Python SDK (requires Python 3.10 or later): https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python
