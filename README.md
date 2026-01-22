# Rippling API Client - Test Workspace

A workspace for testing and exploring the Rippling API Python client.

## Setup

1. **Install the client** (already done):
   ```bash
   pip install git+ssh://git@github.com/nathannelson-cbts/rippling-client-python.git
   ```

2. **Configure credentials**:
   ```bash
   cp .env.example .env
   # Edit .env and add your RIPPLING_BEARER_TOKEN
   ```

3. **Run examples**:
   ```bash
   python examples/01_basic_usage.py
   ```

## Library Overview

### Installation

```python
pip install git+ssh://git@github.com/nathannelson-cbts/rippling-client-python.git
```

### Quick Start

```python
import os
from rippling_client import SyncRipplingClient, RipplingSettings

# Explicitly pass required bearer_token (and optional base_url for sandbox)
settings = RipplingSettings(
    bearer_token=os.getenv('RIPPLING_BEARER_TOKEN'),
    base_url=os.getenv('RIPPLING_BASE_URL', 'https://rest.ripplingapis.com'),
)

with SyncRipplingClient(settings=settings) as client:
    # List workers (use max_results to limit pagination)
    workers = list(client.workers.list(max_results=25))
    for worker in workers:
        print(worker.id)
```

### Limiting Results

Use `max_results` to limit how many items are returned:

```python
# Fetch at most 25 workers
workers = list(client.workers.list(max_results=25))

# Fetch all workers (no limit - may be slow for large datasets)
all_workers = list(client.workers.list())
```

> **Note:** All examples in this workspace use `max_results=25` for efficient testing.

### Available Resources

| Resource | Description |
|----------|-------------|
| `client.companies` | Company/organization data |
| `client.workers` | Employee records |
| `client.users` | User accounts |
| `client.departments` | Department structure |
| `client.teams` | Team groupings |
| `client.work_locations` | Office locations |
| `client.legal_entities` | Legal entities |
| `client.levels` | Career levels |
| `client.tracks` | Work schedules/tracks |
| `client.compensations` | Compensation data |
| `client.leave_types` | Types of leave |
| `client.leave_requests` | Leave/PTO requests |
| `client.leave_balances` | Leave balances |
| `client.leave_accruals` | Leave accrual records |
| `client.time_cards` | Time cards |
| `client.time_entries` | Time entries |
| `client.candidates` | Recruiting candidates |
| `client.candidate_applications` | Job applications |
| `client.custom_fields` | Custom field definitions |
| `client.custom_objects` | Custom object definitions |

### Configuration Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `RIPPLING_BEARER_TOKEN` | *required* | API authentication token |
| `RIPPLING_BASE_URL` | `https://rest.ripplingapis.com` | API base URL (use `https://rest.sandbox.ripplingapis.com` for sandbox) |
| `RIPPLING_TIMEOUT_CONNECT` | `30.0` | Connection timeout (seconds) |
| `RIPPLING_TIMEOUT_READ` | `60.0` | Read timeout (seconds) |
| `RIPPLING_MAX_RETRIES` | `3` | Maximum retry attempts |
| `RIPPLING_RATE_LIMIT_REQUESTS` | `300` | Max requests per window |
| `RIPPLING_RATE_LIMIT_WINDOW` | `10.0` | Rate limit window (seconds) |
| `RIPPLING_LOG_LEVEL` | `INFO` | Logging level |
| `RIPPLING_LOG_FORMAT` | `console` | Log format |

### Async Usage

```python
import asyncio
import os
from rippling_client import AsyncRipplingClient, RipplingSettings

async def main():
    settings = RipplingSettings(
        bearer_token=os.getenv('RIPPLING_BEARER_TOKEN'),
        base_url=os.getenv('RIPPLING_BASE_URL', 'https://rest.ripplingapis.com'),
    )

    async with AsyncRipplingClient(settings=settings) as client:
        # Fetch multiple resources concurrently
        workers, departments = await asyncio.gather(
            client.workers.list(),
            client.departments.list()
        )
        print(f"Workers: {len(workers)}, Departments: {len(departments)}")

asyncio.run(main())
```

### Error Handling

```python
from rippling_client import (
    RipplingError,           # Base exception
    RipplingAPIError,        # General API errors
    RipplingAuthError,       # Authentication failures
    RipplingRateLimitError,  # Rate limiting
    RipplingTimeoutError,    # Timeouts
    RipplingServerError,     # 5xx errors
)

try:
    workers = client.workers.list()
except RipplingAuthError:
    print("Check your API token")
except RipplingRateLimitError:
    print("Too many requests, slow down")
except RipplingAPIError as e:
    print(f"API error: {e}")
```

## Examples

All examples use `max_results=25` to limit API calls during testing.

| File | Description |
|------|-------------|
| [01_basic_usage.py](examples/01_basic_usage.py) | Getting started with the client |
| [02_hr_operations.py](examples/02_hr_operations.py) | HR data: workers, departments, teams |
| [03_time_attendance.py](examples/03_time_attendance.py) | Time cards, entries, tracks |
| [04_recruiting.py](examples/04_recruiting.py) | Candidates and applications |
| [05_custom_data.py](examples/05_custom_data.py) | Custom fields and objects |
| [06_async_usage.py](examples/06_async_usage.py) | Async client for concurrency |
| [07_error_handling.py](examples/07_error_handling.py) | Error handling patterns |
| [08_real_world_use_cases.py](examples/08_real_world_use_cases.py) | Practical integration scenarios |
| [09_interactive_explorer.py](examples/09_interactive_explorer.py) | Interactive data explorer (25 items per query) |

## Common Use Cases

### 1. Employee Directory Export
Sync employee data to Slack, internal wikis, or ID systems.

### 2. Org Chart Generation
Build hierarchical org structures for visualization.

### 3. Headcount Reporting
Department-by-department employee counts for analytics.

### 4. Leave Management Dashboard
Track pending/approved leave requests.

### 5. Data Sync Validation
Compare Rippling data with internal systems for integrity.

## Getting Your API Token

1. Log in to Rippling as an admin
2. Navigate to **Company Settings** → **API** → **API Keys**
3. Create a new API key with appropriate permissions
4. Copy the Bearer Token to your `.env` file
