# Student kit: Lesson 8.5, Exam strategy

Claude Certified Architect – Foundations (CCAR-F) · Section 8: Exam Readiness · Lesson 8.5

This kit holds what you need to write and check your own exam-day plan, as in the lesson, and the tracker you fill in as you take the practice exams. By the end of the lesson you can:

1. Carry the scenario and find the deciding constraint
2. Eliminate with reasons, and handle the questions that ask for two
3. Pace sixty questions in 120 minutes, and know the rules

## What's in the kit

| File | What it is |
|---|---|
| `prompt.txt` | The exact prompt from the lesson: two inputs, four parts |
| `commands.txt` | Every command in the hands-on, in order, with the three checks |
| `exam-plan.md` | The plan the lesson ends with (Lesson 5.6 added by the check): items per domain, what to review, the pacing checkpoints and the practice-exam tracker |

If you'd rather not run Claude Code, copy `exam-plan.md` and use its tracker as it is.

## What you need

- **Claude Code** (Lesson 0.5), signed in. The lesson used a subscription plan and made no API calls.
- **The official exam guide**, `ccar-f-exam-guide.pdf`, downloaded in Lesson 0.1, in `~/Downloads`.
- **This course's seven cheat sheets** (course materials, `cheatsheets/module-1.md` to `module-7.md`) in a folder `~/Downloads/ccar-f-cheatsheets/`.
- About 15 minutes.

## The steps (the lesson's order)

1. **A new folder with the two inputs.** In a terminal (the lesson used VS Code's): `mkdir exam-plan && cd exam-plan`, then copy in the guide and the cheat sheets, and `ls *` to see them (`commands.txt` has the lines).
2. **Start Claude Code.** `claude`. The folder is new, so Claude Code asks whether you trust it. The default is "No, exit", so press Down, then Enter, for "Yes, I trust this folder". Press Shift+Tab twice, until the footer says *accept edits on*, so Claude Code can write the file without asking.
3. **One prompt.** Paste `prompt.txt` and press Enter. In the lesson, Claude Code read the guide and all seven sheets and wrote `exam-plan.md` in 34 seconds. Then `/exit`.
4. **Read the plan.** `code exam-plan.md`, then Ctrl+Shift+V (macOS: Cmd+Shift+V) for the Markdown preview.
5. **Check three things by hand.** Claude Code did most of the work, but the checking is still yours:
   - **The counts.** Section 4 of the guide lists the five weights. Domain 1 is 27%, and 27% of 60 is 16.2, so about 16 questions. Every count is an estimate, because the weights are approximate.
   - **The pacing.** 115 minutes for questions plus a 5-minute buffer is about 1 minute 55 a question. 15 questions at that pace take 28.75 minutes, so question 15 should be done by minute 29.
   - **One mapping against a cheat sheet.** `head -3 ccar-f-cheatsheets/module-5.md` shows that Module 5 covers Domain 3, Task Statements 3.1 to 3.5. Task 3.5 is iterative refinement, Lesson 5.6. `grep -c 'L5.6' exam-plan.md` printed `0` in the lesson, so the plan had left it out. One `sed` line added it, and the count became `1`. Your plan will be worded differently, so check every domain's list against its sheet, and fix what's missing in the editor or with your own `sed` pattern.

## Use the tracker

Take the three practice exams in this section under exam conditions: 60 questions, 120 minutes, no notes. After each one, fill in the tracker in part 4 of the plan. A domain's percentage is the number you got right in that domain divided by that domain's questions on that exam. Book the exam when you reach **80% overall and 70% in every domain**. The Extra full simulation (course materials, `extra/`) scores you the same way, with its own `domain-tracker.md`.

## Windows, macOS and Linux

- **Linux and macOS:** the commands work as they are. On macOS, `sed -i` needs an empty suffix: `sed -i '' 's/.../.../' exam-plan.md`.
- **Windows (PowerShell):** `mkdir exam-plan; cd exam-plan`, `Copy-Item ~\Downloads\ccar-f-exam-guide.pdf .`, `Copy-Item -Recurse ~\Downloads\ccar-f-cheatsheets .`, `Get-ChildItem -Recurse`; Claude Code and the prompt are the same. Check the plan with `Select-String -Pattern 'L5.6' exam-plan.md`, and fix it in the editor.

## If something goes wrong

- **Claude Code exits right away:** you pressed Enter on the trust prompt's default, "No, exit". Start `claude` again, press Down, then Enter.
- **Claude Code asks before writing the file:** the footer doesn't say *accept edits on*. Approve it once, or press Shift+Tab until it does.
- **The plan's numbers differ from ours:** check them against the guide (section 4) and the arithmetic above. The guide is the source, not the plan.

## Sources (checked 2026-10-17)

- Claude Certified Architect – Foundations Exam Guide: sections 3, 4, 9 and 10–15
- Anthropic Partner Academy, FAQ – Certifications ("Can I reschedule or cancel?": at least 48 hours): https://anthropic-partners.skilljar.com/page/faq-certifications

Policies and pages change. Before you book, check the guide and the FAQ again.
