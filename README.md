# pytest-api-client Framework

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Read in: [Português](README.pt-br.md) | English

Modularized framework for API testing with pytest, designed to be reusable and scalable.

## Project Structure

```
pytest-api-client/
├─ api_framework/              # Reusable framework
│  ├─ client.py                # HTTP client with timing
│  ├─ config.py                # Configuration (loads .env)
│  ├─ utils.py                 # Utilities
│  ├─ csv_handler.py           # Manages CSV results
│  └─ __init__.py
│
├─ tests/
│  ├─ test_base.py             # Test template (copy per endpoint)
│  └─ scenarios.py             # Scenarios template (copy per endpoint)
│
├─ json/                       # Scripts to visualize API responses
│  └─ fetch_route_template.py  # Template (uses BASE_URL from .env)
│
├─ csv/                        # Test results (auto-generated)
│
├─ .env.example                # Environment variables template
├─ .gitignore
├─ conftest.py                 # Shared fixtures
├─ requirements.txt
└─ README.md
```

## Context

Developed during a QA internship to automate API testing across multiple endpoints.
Achieved 98% route accuracy across positive/negative scenarios, status code validation
and JSON response structure verification. Results are exported to CSV for traceability.

## Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env (optional, uses defaults if not present)
cp .env.example .env
```

### 2. Edit .env

```env
BASE_URL=http://localhost:8000
TIMEOUT=10
REPETITIONS=5
MAX_AVERAGE_TIME=30
```

### 3. View an API response

```bash
cd json
cp fetch_route_template.py fetch_route_<endpoint_name>.py
```

Edit `fetch_route_<endpoint_name>.py`:

```python
ENDPOINT = "<endpoint_name>"  # Change to your endpoint path
```

Run:

```bash
python fetch_route_<endpoint_name>.py
# 200
#
# [{...}, {...}]
```

### 4. Create a test

```bash
# Step 1: Copy scenarios template
cp tests/scenarios.py tests/scenarios_<endpoint_name>.py

# Step 2: Copy test template
cp tests/test_base.py tests/test_<endpoint_name>.py
```

Edit `tests/scenarios_<endpoint_name>.py`:

```python
SCENARIOS = [
    ({}, "Without parameters", 200),
    ({"page": 1}, "Page 1", 200),
]

def validate_response(data):
    assert isinstance(data, list)
```

Edit `tests/test_<endpoint_name>.py`:

```python
from tests import scenarios_<endpoint_name> as scenarios

ENDPOINT = "<endpoint_name>"  # Change to your endpoint path
```

### 5. Run tests

```bash
pytest tests/test_<endpoint_name>.py -v
# Results saved to: csv/<endpoint_name>_results.csv
```

## The Fetch Script

The script in `json/fetch_route_template.py` is a **simple visualization tool** that uses `BASE_URL` from your `.env`:

```python
# Usage - only specify the endpoint path, not full URL
ENDPOINT = "<endpoint_name>"  # Endpoint path only
fetch_endpoint(ENDPOINT)

# Output
# Fetching: http://localhost:8000/<endpoint_name>
# 200
#
# [{...}, {...}]
```

It's just for you to **see what the API is returning** before writing tests.

**Does NOT create files, does NOT save anything, just PRINTS!**

## Components

### `config.py` - Configuration

- Loads variables from `.env`
- Provides defaults if `.env` doesn't exist
- `get_test_config()` - Global config
- `get_endpoint_config(endpoint)` - Per-endpoint config (for CSV naming)

### `client.py` - HTTP Client

- Automatic timing with `resp.elapsed_custom`
- Customizable headers
- Configurable timeout
- Builds full URL from `BASE_URL + endpoint`

### `csv_handler.py` - Results

- `initialize_csv()` - Creates file with headers
- `append_result()` - Adds result row

### `conftest.py` - Fixtures

- `client` - Fixture for all tests (scoped per function)

## Complete Example

### Step 1: Document

```bash
cd json
cp fetch_route_template.py fetch_route_<endpoint_name>.py
```

Edit `cp fetch_route_template.py fetch_route_<endpoint_name>.py`:

```python
ENDPOINT = "<endpoint_name>"  # Change to your endpoint
fetch_endpoint(ENDPOINT)
```

Run:

```bash
python cp fetch_route_template.py fetch_route_<endpoint_name>.py
# 200
#
# {...}
```

### Step 2: Create Scenarios

```bash
cp tests/scenarios.py tests/scenarios_<endpoint_name>.py
```

Edit `tests/scenarios_<endpoint_name>.py`:

```python
SCENARIOS = [
    ({}, "Without parameters", 200),
    ({"id": 1}, "With id", 200),
]

def validate_response(data):
    assert isinstance(data, dict)
    assert "id" in data
```

### Step 3: Test

```bash
cp tests/test_base.py tests/test_<endpoint_name>.py
```

Edit `tests/test_<endpoint_name>.py`:

```python
from tests import scenarios_<endpoint_name> as scenarios

ENDPOINT = "<endpoint_name>"  # Change to your endpoint
```

Run:

```bash
pytest tests/test_<endpoint_name>.py -v
# Results in: csv/<endpoint_name>_results.csv
```

## Customization

### Custom Validation

```python
def validate_response(data):
    assert isinstance(data, dict)
    assert "id" in data

# Called automatically in test_endpoint
```

### Custom Headers

Edit `.env` or override in test:

```python
from api_framework.config import get_test_config

CONFIG = get_test_config()
CONFIG["headers"]["Authorization"] = "Bearer token"
```

## Troubleshooting

| Problem                       | Solution                                        |
| ----------------------------- | ----------------------------------------------- |
| `ModuleNotFoundError: dotenv` | `pip install python-dotenv`                     |
| `Client fixture not found`    | Check if `conftest.py` is in root               |
| CSV not created               | Check if `csv/` directory exists (auto-created) |
| URL not recognized            | Check `BASE_URL` in `.env`                      |

## Environment Variables

| Variable           | Default                 | Description              |
| ------------------ | ----------------------- | ------------------------ |
| `BASE_URL`         | `http://localhost:8000` | API base URL             |
| `TIMEOUT`          | `10`                    | Timeout in seconds       |
| `REPETITIONS`      | `5`                     | Repetitions per scenario |
| `MAX_AVERAGE_TIME` | `30`                    | Time limit in seconds    |

## Next Steps

1. Create `.env` with your URLs
2. Document your routes with `fetch_route_template.py`
3. Create tests by copying `tests/test_base.py`
4. Run and analyze results in `csv/`

## References

- [pytest](https://docs.pytest.org/)
- [requests](https://requests.readthedocs.io/)
- [python-dotenv](https://python-dotenv.readthedocs.io/)

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Lucas Nicolau — Software Engineering Student at @UFAM
