# Lesson 0.1: How CCAR-F works and how to use this course

No code in this lesson. The hands-on happens in Claude in the browser: you attach Anthropic's official exam guide (PDF), ask for a one-page study map, and check it against the guide.

| File | What it is |
|---|---|
| `prompt-study-map.txt` | The exact prompt from the lesson (five lines). |
| `claude-haiku-5.5-study-map.md` | The study map Claude (Haiku 5.5) wrote in the lesson, word for word. |

The exam guide isn't copied here. Download it from Anthropic: *Claude Certified Architect – Foundations Exam Guide*, Version 1.0 (effective July 2026), linked from the **Exam guide** column of the Claude Certified Architect – Foundations row on Anthropic's Partner Certifications page (https://anthropic-partners.skilljar.com/page/partner-certifications).

## Reproduce it
1. Download the guide PDF.
2. Open Claude in the browser, start a new chat, and choose **Haiku 5.5** in the model menu (any current model works).
3. Attach the PDF (**Ctrl+U**, or `+` and add files), paste the prompt from `prompt-study-map.txt`, and send.
4. Check the reply against the guide, pages 2–4: page 2 has the exam details (60 items, 120 minutes, 720 on 100–1,000, 4 scenarios from 6); page 3 has the weights (27, 18, 20, 20, 15); pages 3–4 list each scenario's primary domains.

Our map got every number right but missed one instruction: the prompt asked for the domains heaviest first, and the table kept the guide's own order (Tool Design & MCP Integration, 18%, above two domains at 20%). Check yours for the same slip. Item counts (weight × 60) are estimates; the guide states only the weights.

Sources checked 2026-10-13. Exam details can change, so confirm them in the official guide and FAQ before you book (the FAQ's rescheduling rule, at least 48 hours, is stricter than the guide's 24 hours).
