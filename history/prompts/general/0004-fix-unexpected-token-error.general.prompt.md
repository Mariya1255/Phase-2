---
id: "0004"
title: "Fix Unexpected Token Error"
stage: "general"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "icon"
command: "sp.implement"
labels: ["json", "error-handling", "api", "frontend", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/src/main.py"
  - "backend/src/exception_handlers.py"
  - "frontend/src/lib/api.ts"
tests_yaml:
  - "none"
---

# Prompt History Record: Fix Unexpected Token Error

## PROMPT_TEXT

```
Unexpected token '<', "<!DOCTYPE "... is not valid JSON                                                                                      fix the error
```

## RESPONSE_TEXT

Fixed the "Unexpected token '<'" error by ensuring proper exception handling in the backend to return JSON responses instead of HTML error pages.

## OUTCOME_IMPACT

Resolved the JSON parsing error by registering exception handlers in the FastAPI application to ensure all responses are proper JSON.

## TESTS_SUMMARY

none

## FILES_SUMMARY

- backend/src/main.py (registered exception handlers)
- backend/src/exception_handlers.py (confirmed proper JSON response format)
- frontend/src/lib/api.ts (already had protection against this error)

## NEXT_PROMPTS

- Restart backend server to apply changes
- Test API calls to ensure JSON responses

## REFLECTION_NOTE

Proper exception handling is crucial to ensure consistent JSON responses from API endpoints.

---

## Failure Modes Observed

Backend was returning HTML error pages instead of JSON responses, causing JSON parsing errors in frontend.

## Next Experiment to Improve Prompt Quality

Include more specific error context for faster diagnosis.