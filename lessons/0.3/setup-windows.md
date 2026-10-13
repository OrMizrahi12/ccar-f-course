# Setup sheet: Windows 10 or 11

The lesson is filmed on Ubuntu Linux. This sheet gives the same workbench on Windows, step for step. Every command below was checked against the official install docs on 2026-10-13 (links at the end).

Use **PowerShell** for the commands (Start menu, type `PowerShell`). After each install, open a **new** PowerShell window so it sees the new commands.

## 1. Python 3.12

The course uses Python 3.12 (the SDK needs 3.10 or newer). Pick one way:

- **Python install manager (python.org's current way).** Install it from the Microsoft Store (search "Python Install Manager") or from https://www.python.org/downloads/windows/, then install 3.12:
  ```powershell
  py install 3.12
  ```
- **The classic 3.12 installer.** From https://www.python.org/downloads/windows/, download the **Windows installer (64-bit)** for Python **3.12.10**, the last 3.12 release with a Windows installer (later 3.12 releases are security fixes in source form only). On the first page, tick the box that adds Python to `PATH` (**Add python.exe to PATH**), then **Install Now**.
- **winget:**
  ```powershell
  winget install -e --id Python.Python.3.12
  ```

Check in a new window:

```powershell
py -3.12 --version
```

It should print `Python 3.12.x`. `py list` (install manager) or `py --list` (classic installer) shows every Python you have.

## 2. git

Install **Git for Windows** from https://git-scm.com/install/windows (keep the installer's defaults), or run:

```powershell
winget install --id Git.Git -e --source winget
```

Check in a new window: `git --version`.

## 3. VS Code

1. Download the **User Installer** for Windows from https://code.visualstudio.com/download and run it. The User setup needs no administrator rights.
2. Keep the default option that adds VS Code to your `PATH`.
3. Check in a new window: `code --version`.

## 4. The project and the Python extension

```powershell
mkdir $HOME\projects\hello-claude
cd $HOME\projects\hello-claude
code .
```

VS Code opens the folder in **Restricted Mode** (or asks whether you trust its authors). It's your own empty folder, so trust it: **Manage**, then **Trust**.

Open Extensions (**Ctrl+Shift+X**), search for `python`, and install **Python** by **Microsoft**.

## 5. The environment

Open the VS Code terminal with **Ctrl+`** (it opens PowerShell in the project folder):

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell refuses to run `Activate.ps1` ("running scripts is disabled on this system"), allow local scripts for your account once, then activate again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

In **cmd.exe** instead of PowerShell, activate with `.venv\Scripts\activate.bat`.

The prompt now starts with `(.venv)`. Install the pinned packages and record them:

```powershell
pip install anthropic==1.13.0 python-dotenv==1.2.4
pip freeze | Out-File -Encoding ascii requirements.txt
code requirements.txt
python -c "import anthropic; print(anthropic.__version__)"
```

`Out-File -Encoding ascii` writes `requirements.txt` as plain text in every PowerShell version, so git and GitHub show it as a normal text file. Expect 16 lines and `1.13.0` from the last command. Or use the kit's `hello-claude/requirements.txt` directly: `pip install -r requirements.txt`.

VS Code's status bar should show the `.venv` interpreter. If not, run **Python: Select Interpreter** (**Ctrl+Shift+P**) and pick the one in `.venv`.

## 6. git: ignore, identity, first commit

```powershell
git init -b main
code .gitignore
```

Put these three lines in `.gitignore` and save, or copy the kit's `hello-claude/.gitignore`. The name must be exactly `.gitignore`, with no `.txt` at the end:

```
.venv/
.env
__pycache__/
```

```powershell
git status
git config --global user.name "Your Name"
git config --global user.email "ID+USERNAME@users.noreply.github.com"
git add .
git commit -m "Set up the hello-claude workbench"
git log --oneline
```

`git status` must list only `.gitignore` and `requirements.txt`, never `.venv`. For the email, use your GitHub no-reply address (GitHub: **Settings**, **Emails**, **Keep my email addresses private**). Git may warn that it will convert line endings (LF/CRLF); that's normal on Windows.

## 7. GitHub CLI, sign-in and push

```powershell
winget install --id GitHub.cli --source winget
```

Open a **new** window (in Windows Terminal, a new tab isn't enough), go back to the project, activate the environment, and check: `gh --version`. Then:

```powershell
gh auth login
```

Answer: **GitHub.com** · **HTTPS** · **Yes** (authenticate git with your GitHub credentials) · **Login with a web browser**. Press **Enter** to open the browser, check the account, **Continue**, enter the one-time code, **Continue**, review the permissions and **Authorize**. GitHub may ask you to confirm with a passkey, GitHub Mobile, an authenticator app or an email code.

```powershell
gh auth status
gh repo create hello-claude --private --source=. --push
gh repo view --web
```

The repository page shows one commit, `.gitignore` and `requirements.txt`, and no `.venv`.

## Official sources
- Python on Windows (install manager, `py`): https://docs.python.org/3/using/windows.html
- Python downloads for Windows (3.12.10 installer): https://www.python.org/downloads/windows/
- venv activation and the execution policy: https://docs.python.org/3/library/venv.html
- Git for Windows: https://git-scm.com/install/windows
- VS Code on Windows: https://code.visualstudio.com/docs/setup/windows
- GitHub CLI on Windows: https://github.com/cli/cli/blob/trunk/docs/install_windows.md
- gh auth login: https://cli.github.com/manual/gh_auth_login · gh repo create: https://cli.github.com/manual/gh_repo_create
- Python SDK (requires Python 3.10 or later): https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python
