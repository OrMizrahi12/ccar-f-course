# Student kit: Lesson 0.1, How CCAR-F works and how to use this course

Claude Certified Architect – Foundations (CCAR-F) · Section 0: Start Here · Lesson 0.1

This kit holds everything you need to repeat the lesson's hands-on yourself: where to get the official exam guide (the file you attach), the exact prompt, and the study map Claude actually wrote in the lesson, word for word. Nothing here is a made-up sample.

By the end of the lesson you can explain how the exam works and who can take it, read the blueprint and the six scenarios, and use this course's study system.

**Quick check:** before you move on, take this lesson's quick check. It's a few short questions, and it takes a couple of minutes.

## What's in the kit

| File | What it is |
|---|---|
| `prompt-study-map.txt` | The exact prompt from the lesson: five lines (the task, three format lines, a guardrail). |
| `claude-haiku-5.5-study-map.md` | The study map exactly as Claude (Haiku 5.5) wrote it in the lesson, word for word, including its one slip (see below). |

The exam guide isn't copied into this kit. Download it from Anthropic: *Claude Certified Architect – Foundations Exam Guide*, Version 1.0 (effective July 2026, exam code CCAR-F, 39 pages). It is linked from the **Exam guide** column of the Claude Certified Architect – Foundations row on Anthropic's Partner Certifications page (https://anthropic-partners.skilljar.com/page/partner-certifications). Direct link: https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542750%2FClaude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf

## The exam in one table (checked 2026-10-13)

| | | Where it says so |
|---|---|---|
| Items | 60, multiple choice and multiple response; each item states how many responses to select | Guide §3 (p. 2) |
| Structure | 4 scenarios drawn at random from a bank of 6; each scenario frames a set of questions | Guide §3 (p. 2), §5 (p. 3) |
| Time | 120 minutes, about 2 minutes per item (our arithmetic). Plan for about 135 minutes of seat time with check-in | Guide §3 (p. 2); FAQ |
| Delivery | Proctored, online or at a Pearson VUE test center | Guide §3 (p. 2), §11 (p. 33–34) |
| Book | Closed: no notes, documentation, translation tools or AI assistants | FAQ; Guide §13 (p. 35) |
| Score | Scaled, 100 to 1,000; 720 passes. 720 is not "72% correct": scaling equates exam versions of different difficulty | Guide §3 (p. 2), §10 (p. 33) |
| Standard | Criterion-referenced: measured against a fixed standard, not against other candidates | Guide §10 (p. 33) |
| Score report | Pass/fail, the scaled score, and your percent correct in each domain (feedback only; pass/fail uses the total) | Guide §3 (p. 2), §10 (p. 33) |
| Fee | $125 USD per attempt, before any partner-tier discount | Guide §3 (p. 2); Partner Certifications page; FAQ |
| Retakes | Wait 14 days after a first fail, 30 after a second, 90 after a third; at most 4 attempts in a rolling 12 months | Guide §12 (p. 34) |
| Validity | 12 months. On-time renewal is a free, non-proctored assessment; if it lapses, you retake the full exam at the full fee | Guide §3 (p. 2), §15 (p. 35) |
| Who can take it today | People at Claude Partner Network organizations, registering with a partner email on a recognized company domain | FAQ |

**Before you book:** the guide (§11) says you can cancel or reschedule up to 24 hours before your appointment, but the current FAQ says at least **48 hours**. The FAQ is stricter and newer, so check it on the day you book and plan for 48 hours.

## The five domains (guide §4, p. 3)

The weights are the *approximate* share of *scored* items. Item counts are estimates (weight × 60, rounded); the guide doesn't state them.

| Domain | Weight | ≈ Items of 60 | Task statements |
|---|---|---|---|
| Domain 1: Agentic Architecture & Orchestration | 27% | ≈ 16 | 7 (1.1–1.7) |
| Domain 3: Claude Code Configuration & Workflows | 20% | ≈ 12 | 6 (3.1–3.6) |
| Domain 4: Prompt Engineering & Structured Output | 20% | ≈ 12 | 6 (4.1–4.6) |
| Domain 2: Tool Design & MCP Integration | 18% | ≈ 11 | 5 (2.1–2.5) |
| Domain 5: Context Management & Reliability | 15% | ≈ 9 | 6 (5.1–5.6) |

The 30 task statements, each with its "Knowledge of" and "Skills in" lists, are in guide §6 (from p. 5). They are the most precise study list you'll get.

## The six scenarios (guide §5, p. 3–4)

| Scenario | Primary domains (as the guide lists them) |
|---|---|
| 1: Customer Support Resolution Agent | Agentic Architecture & Orchestration · Tool Design & MCP Integration · Context Management & Reliability |
| 2: Code Generation with Claude Code | Claude Code Configuration & Workflows · Context Management & Reliability |
| 3: Multi-Agent Research System | Agentic Architecture & Orchestration · Tool Design & MCP Integration · Context Management & Reliability |
| 4: Developer Productivity with Claude | Tool Design & MCP Integration · Claude Code Configuration & Workflows · Agentic Architecture & Orchestration |
| 5: Claude Code for Continuous Integration | Claude Code Configuration & Workflows · Prompt Engineering & Structured Output |
| 6: Structured Data Extraction | Prompt Engineering & Structured Output · Context Management & Reliability |

**The 4-of-6 rule:** your exam draws 4 of these 6 at random, so any of the six can appear, and you can't skip one. Context Management & Reliability is the lightest domain (15%), but it is primary in four scenarios (1, 2, 3, 6), so every possible draw includes at least two scenarios that list it.

## Reproduce the hands-on

You need a Claude account and the exam guide PDF (link above). It runs in the Claude app on your plan, so no API key is needed. Your map won't match ours word for word, so check *yours* against the guide, not against ours.

1. **Get the guide.** On the Partner Certifications page, click **Exam guide** in the Claude Certified Architect – Foundations row. The PDF opens in the browser; download it and save it somewhere easy to find (the lesson saves it to Downloads as `ccar-f-exam-guide.pdf`).
2. **Open Claude.** Open Claude in your browser and start a new chat.
3. **Pick the model.** Open the model menu in the message box and choose **Haiku 5.5**, the fastest and cheapest model; reading one PDF and organizing it doesn't need more. Any current model works.
4. **Attach the guide.** Press **Ctrl+U** (or click `+` and choose to add files), pick the PDF and click **Open**. A PDF chip appears in the message box.
5. **Paste the prompt.** Copy all five lines from `prompt-study-map.txt` and paste them into the message box (if you type it instead, use **Shift+Enter** between lines).
6. **Send** and let the reply finish.
7. **Check it against the guide, pages 2–4:**
   - Page 2 (§3): 60 items, 120 minutes, 720 on 100–1,000, 4 scenarios from 6, $125, 12 months.
   - Page 3 (§4): the weights are 27, 18, 20, 20 and 15. Did your map put the domains **heaviest first**, as the prompt asked? Ours didn't: it kept the guide's own order, so Tool Design (18%) sat above two 20% domains. The numbers were right; the order wasn't.
   - Pages 3–4 (§5): each scenario's primary domains. Spot-check one (the lesson checks Scenario 4: Tool Design, Claude Code, Agentic Architecture), then the count per domain (3, 3, 3, 2, 4 for Domains 1–5).
8. **Stated or estimated?** Weights are stated in the guide. Item counts (weight × 60), "about 2 minutes per item" and "each scenario appears in about two-thirds of exams" (4 of 6, assuming a uniform draw) are arithmetic. Check that your map labels them as estimates.
9. **Read "What the guide doesn't say".** A good answer says when the source is silent.

## What the guide doesn't say

- How the 60 items split between multiple choice and multiple response, or how multiple-response items are scored (partial credit or all-or-nothing).
- How many items come from each scenario or domain on your form. The weights are approximate, and they describe *scored* items, which suggests some items may not count.
- How the 720 cut maps to percent correct. There is no minimum per domain: pass/fail uses the total scaled score.
- How to spend the time across scenarios. (The FAQ adds that seat time is about 135 minutes, including check-in.)
- Which domain each of the guide's 12 sample questions belongs to. They show the format and style; they are not a slice of the real exam.

## How this course is built

- **Lessons and quick checks.** Every lesson is a short video, followed by a quick check of three questions.
- **Module labs.** Every module ends with a hands-on lab, where you build one piece of a single real project, **Harborline**, an online store whose systems match the exam's six scenarios.
- **Module quizzes.** Each module ends with a module quiz, mostly on that module, with a little review of earlier ones from Module 2 on.
- **Three practice exams.** 60 items each, built like the real one: 4 scenarios × 15 items, 120 minutes, scored by domain.
- **Next: the readiness check** (Lesson 0.2), which shows you where to focus.

Anthropic retired its official practice exam, so every question in this course is original, written against the same blueprint. None comes from the real exam.

## Key terms

- **Scenario:** a realistic production setting (a support agent, a CI pipeline…) that frames a set of exam questions. The exam draws 4 of the 6 published scenarios.
- **Blueprint:** the guide's outline of what the exam tests: 5 domains, each with a weight.
- **Task statement:** one of the 30 numbered skills under the domains (e.g. Task Statement 1.1), each with "Knowledge of" and "Skills in" lists.
- **Scaled score:** your result on a 100–1,000 scale; 720 passes on every version of the exam, so 720 is not the same as 72% correct.
- **Criterion-referenced:** measured against a fixed standard, not against other candidates.

## Sources (checked 2026-10-13)

- Anthropic, *Claude Certified Architect – Foundations Exam Guide*, Version 1.0, effective July 2026 (link above): §1–6, §9 (sample question 1), §10–13, §15.
- Anthropic Partner Academy, *Partner Certifications* page: https://anthropic-partners.skilljar.com/page/partner-certifications (the three roles, the Architect card, the fee and the exam-guide link).
- Anthropic Partner Academy, *Certification FAQ*: https://anthropic-partners.skilljar.com/page/faq-certifications (partner organizations and company email; closed book; seat time; the retired practice exam; rescheduling, now at least 48 hours, stricter than the guide's 24 hours, so check it before booking).

Exam details can change. Always confirm the current details in the official guide and FAQ before you book.
