---
name: no-code
description: Answer without modifying or suggesting changes to the codebase
argument-hint: "Ask your question"
---

Answer the user's request normally.

Rules:
- You may use the active file and workspace context for understanding.
- Do not suggest edits, refactors, or changes to the existing codebase.
- Do not generate patches or file modifications.
- You may include general code examples if helpful.

Request:
{{input}}
