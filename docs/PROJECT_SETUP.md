# Project Setup & Development Guide

> Reference document for the rippling-client-python-test project and its relationship to the main library.

**Last Updated:** 2026-01-22

---

## Overview

This project (`rippling-client-python-test`) is a dedicated test workspace for validating and exploring the `rippling-client-python` library. It exists as a separate project to test the library from a consumer's perspective.

---

## Project Relationships

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         VS Code Workspace                                │
├─────────────────────────────────┬───────────────────────────────────────┤
│                                 │                                       │
│  rippling-client-python/        │  rippling-client-python-test/         │
│  ─────────────────────────      │  ────────────────────────────         │
│  THE LIBRARY                    │  THE TEST PROJECT                     │
│                                 │                                       │
│  • src/rippling_client/         │  • examples/                          │
│    ├── client.py                │    ├── 01_basic_usage.py              │
│    ├── config.py                │    ├── 02_hr_operations.py            │
│    ├── exceptions.py            │    ├── 03_time_attendance.py          │
│    ├── auth/                    │    ├── ...                            │
│    ├── http/                    │  • test_connection.py                 │
│    ├── models/                  │  • docs/ (this folder)                │
│    └── resources/               │                                       │
│                                 │  Uses library via:                    │
│  • docs/DESIGN.md               │  pip install -e ../rippling-client-   │
│  • docs/TODO.md                 │       python                          │
│  • tests/ (unit tests)          │                                       │
│                                 │                                       │
└─────────────────────────────────┴───────────────────────────────────────┘
```

### Key Distinction

| Project | Purpose | Tests Type |
|---------|---------|------------|
| `rippling-client-python` | The library itself | Unit tests (mocked HTTP) |
| `rippling-client-python-test` | Consumer test workspace | Integration tests (real API) |

---

## Local Development Setup

### Directory Locations

```
/Users/nathan.nelson/Development/
├── rippling-client-python/        # The library source
└── rippling-client-python-test/   # This test project
```

### Editable Install

The library is installed in **editable mode** so changes to the library source are immediately available without reinstalling:

```bash
# From rippling-client-python-test directory, with venv activated:
pip install -e /Users/nathan.nelson/Development/rippling-client-python
```

This means:
- Changes to `rippling-client-python/src/rippling_client/` are **immediately reflected**
- No need to reinstall after modifying library code
- Enables rapid iteration: fix bug → test → verify

### Verify Editable Install

```bash
# Check where the package is installed from
pip show rippling-client

# Should show:
# Location: /Users/nathan.nelson/Development/rippling-client-python/src
# Editable project location: /Users/nathan.nelson/Development/rippling-client-python
```

---

## Environment Configuration

### Required Files

| File | Purpose | Git Status |
|------|---------|------------|
| `.env.example` | Template with placeholder values | Committed |
| `.env` | Actual credentials (NEVER commit) | Gitignored |
| `.env.test` | Test-specific overrides (optional) | Gitignored |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `RIPPLING_BEARER_TOKEN` | **Yes** | API bearer token for authentication |
| `RIPPLING_BASE_URL` | No | Defaults to `https://rest.ripplingapis.com` |

### Setup Steps

```bash
# 1. Navigate to test project
cd /Users/nathan.nelson/Development/rippling-client-python-test

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Verify Python is from venv
which python  # Should show: .../rippling-client-python-test/.venv/bin/python

# 4. Copy environment template
cp .env.example .env

# 5. Edit .env and add your bearer token
# RIPPLING_BEARER_TOKEN=your_actual_token_here

# 6. Run a test
python test_connection.py
```

---

## Workflow: Making Changes to the Library

When you encounter an issue while testing:

### 1. Identify the Issue
Run an example, observe the error or unexpected behavior.

### 2. Fix in the Library
Make changes in `rippling-client-python/src/rippling_client/`

### 3. Test Immediately
Run the same example again — changes are picked up automatically (editable install).

### 4. Run Library Unit Tests
```bash
cd /Users/nathan.nelson/Development/rippling-client-python
source .venv/bin/activate
make test
```

### 5. Commit Both Projects (if needed)
- Commit the fix to `rippling-client-python`
- Commit updated tests/examples to `rippling-client-python-test`

---

## Project Structure

```
rippling-client-python-test/
├── .env                    # Credentials (gitignored)
├── .env.example            # Template for credentials
├── .venv/                  # Virtual environment
├── README.md               # Project overview
├── test_connection.py      # Basic connectivity test
├── docs/
│   └── PROJECT_SETUP.md    # This file
└── examples/
    ├── 01_basic_usage.py       # Getting started
    ├── 02_hr_operations.py     # Workers, departments, teams
    ├── 03_time_attendance.py   # Time entries, time cards
    ├── 04_recruiting.py        # Candidates, applications
    ├── 05_custom_data.py       # Custom objects, custom fields
    ├── 06_async_usage.py       # Async client patterns
    ├── 07_error_handling.py    # Exception handling patterns
    ├── 08_real_world_use_cases.py  # Practical scenarios
    └── 09_interactive_explorer.py  # Interactive REPL-style explorer
```

---

## Library Reference

### Key Library Files

When debugging, these are the important files in `rippling-client-python`:

| File | Purpose |
|------|---------|
| `src/rippling_client/client.py` | `AsyncRipplingClient`, `SyncRipplingClient` |
| `src/rippling_client/config.py` | `RipplingSettings` configuration |
| `src/rippling_client/exceptions.py` | Error types (`RipplingAPIError`, etc.) |
| `src/rippling_client/resources/base.py` | Base resource with CRUD + pagination |
| `src/rippling_client/resources/*.py` | Individual resource implementations |
| `src/rippling_client/models/*.py` | Pydantic models for API responses |
| `docs/DESIGN.md` | Architectural decisions |
| `docs/TODO.md` | Implementation status tracking |

### Import Examples

```python
# Main clients
from rippling_client import AsyncRipplingClient, SyncRipplingClient

# Configuration
from rippling_client import RipplingSettings

# Exceptions
from rippling_client import (
    RipplingError,
    RipplingAPIError,
    RipplingAuthError,
    RipplingRateLimitError,
    RipplingServerError,
    RipplingTimeoutError,
)

# Models (if needed for type hints)
from rippling_client.models import Worker, Company, Department
```

---

## Troubleshooting

### Import Errors

```
ModuleNotFoundError: No module named 'rippling_client'
```

**Solution**: Ensure editable install is done:
```bash
source .venv/bin/activate
pip install -e /Users/nathan.nelson/Development/rippling-client-python
```

### Authentication Errors

```
RipplingAuthError: 401 Unauthorized
```

**Solution**: Check `.env` file has valid `RIPPLING_BEARER_TOKEN`

### Changes Not Reflected

If library changes aren't being picked up:

```bash
# Verify editable install
pip show rippling-client | grep -i editable

# If not editable, reinstall
pip uninstall rippling-client
pip install -e /Users/nathan.nelson/Development/rippling-client-python
```

---

## Session Continuity

This document helps maintain context between development sessions. When resuming work:

1. **Read this file** — Understand the project setup
2. **Check [docs/TODO.md](../../rippling-client-python/docs/TODO.md)** — See implementation status
3. **Activate venv** — `source .venv/bin/activate`
4. **Run a test** — `python test_connection.py` to verify everything works

---

## Related Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| Library README | `rippling-client-python/README.md` | Library usage guide |
| Design Decisions | `rippling-client-python/docs/DESIGN.md` | Architecture & rationale |
| Implementation Status | `rippling-client-python/docs/TODO.md` | What's done, what's pending |
| Coding Standards | `rippling-client-python/.github/copilot-instructions.md` | Code style rules |
