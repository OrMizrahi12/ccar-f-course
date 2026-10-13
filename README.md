# Claude Certified Architect – Foundations (CCAR-F): Course Materials

Companion materials for the course: the prompts, outputs and end-state code of each lesson, and (as the course grows) the starter code and reference solutions for every module lab, built on one running project, **Harborline**.

This is independent training material. It is not affiliated with or endorsed by Anthropic, and it contains no live exam content. Anthropic's official exam guide is not copied here; each lesson links to it instead.

## Layout
- `lessons/<id>/`: everything a lesson uses or produces, exactly as it stands at the end of that lesson (for example `lessons/0.1/`). Each folder has a README that says what every file is and how to reproduce the lesson.
- `labs/L<n>/` (from Module 1): `starter/`, `solution/` and self-check tests for each module lab.
- Setup guides for Windows, macOS and Linux: `lessons/0.3/` (`setup-windows.md`, `setup-macos.md`, `setup-linux.md`), with the workbench project files in `lessons/0.3/hello-claude/`.
- Your API key and first call: `lessons/0.4/` (Console steps, per-system commands, troubleshooting), with `hello-claude/.env.example`, `hello-claude/first_call.py` and the lesson's output in `expected-output.md`.

## Before you start
- Lessons that use the Claude app (like 0.1) need only a Claude account.
- Lessons that call the API need your own Anthropic API key in a `.env` file (Lesson 0.4 shows how). Never commit `.env`; it is already in `.gitignore`.
- Your own outputs won't match ours word for word. Check them against the official source, as the lessons do.
