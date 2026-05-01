---
name: docs-gen-api-method
description: Add or update MkDocs Material documentation for one SDK API method in the current docs file.
argument-hint: "Paste the method signature, docstring, and related Swagger endpoint"
---

Add or update documentation for a single SDK API method in the currently open documentation file.

Use the provided method signature, docstring, and Swagger/OpenAPI reference. If the docstring is incomplete, infer missing details from the signature and Swagger reference. Do not invent behavior that is not supported by the provided input.

Rules:
- Modify the current documentation file directly.
- Insert the method under the existing resource or resource-group heading.
- Do not create a new file.
- Do not return a standalone copy-paste result.
- Do not duplicate existing method documentation; update it if it already exists.
- Use Markdown compatible with MkDocs Material.
- Keep the documentation concise.
- Preserve the exact SDK method name.
- Preserve the exact endpoint path from Swagger/OpenAPI.
- Use realistic Python examples.
- If required information is missing, add `TODO:` instead of guessing.
- Keep the tab structure consistent with existing documentation for the same resource or group.
- No need to build the docs locally; just ensure the Markdown is correct and follows the existing style.

Use this structure for the method section:

#### `<method_name>`

Short description of what the method does.

**Endpoint Mapping**

<code style="color: <unique readable color>;">HTTP_METHOD</code> <code>ENDPOINT_PATH</code>

**SDK Method**

!!! info "`method_signature_with_types_and_return_type`"

    ```python title="Basic usage"
    example_code_here
    ```

Optional notes, warnings, exceptions, or usage tips, only if relevant.

Request:
{{input}}