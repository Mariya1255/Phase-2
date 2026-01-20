---
id: "0002"
title: "Fix Uvicorn Command Issue"
stage: "general"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "icon"
command: "sp.implement"
labels: ["uvicorn", "fastapi", "windows", "path", "command"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/src/main.py"
  - "backend/requirements.txt"
tests_yaml:
  - "none"
---

# Prompt History Record: Fix Uvicorn Command Issue

## PROMPT_TEXT

```
i m trying to start backend fastapi server by this command uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 but i m getting this error 'uvicorn is not recognized as internal or external command' solve this issue permanently i m stuck here for last few hours.. and after solving the issue remember to mention the cause so i could know.
```

## RESPONSE_TEXT

Successfully diagnosed and fixed the uvicorn command issue on Windows by using python -m uvicorn syntax instead of direct uvicorn command.

## OUTCOME_IMPACT

Resolved the 'uvicorn is not recognized as internal or external command' error by using the proper Python module syntax.

## TESTS_SUMMARY

Verified that the FastAPI server starts successfully with python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

## FILES_SUMMARY

- backend/src/main.py (verified file exists for server startup)
- backend/requirements.txt (confirmed dependencies installed)

## NEXT_PROMPTS

- Start the FastAPI server using python -m uvicorn
- Continue with application development

## REFLECTION_NOTE

Windows PATH configuration often causes issues with Python package executables; using python -m is the most reliable cross-platform approach.

---

## Failure Modes Observed

None - issue was properly diagnosed and resolved.

## Next Experiment to Improve Prompt Quality

Provide more detailed Windows-specific troubleshooting for Python package commands.