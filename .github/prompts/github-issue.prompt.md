---
name: github-issue
description: Generate a concise GitHub issue
argument-hint: "Describe the feature or bug"
---

Generate a concise (no need for a novel), human readable GitHub issue from the provided request. The result should be returned as a plain text code block, but copiable markdown text in it that can be directly pasted into a GitHub issue with all code formatting preserved.

Use this format:

# Title (title-case, one line)

**Description**

Include the context, scope, and any implementation notes if applicable.

**Acceptance Criteria**

- List the acceptance criteria as bullet points, if applicable.

Request:
{{input}}
