# pytest-api-client Framework

Modularized framework for API testing with pytest, designed to be reusable and scalable.

## 📁 Project Structure

```
pytest-api-client/
├─ api-framework/              # Reusable framework
│  ├─ client.py                # HTTP client with timing
│  ├─ config.py                # Configuration (loads .env)
│  ├─ utils.py                 # Utilities
│  ├─ csv_handler.py           # Manages CSV results
│  ├─ json_handler.py          # Loads responses
│  └─ __init__.py
│
├─ json/                       # Scripts to visualize API responses
│  └─ fetch_route_template.py  # Template (only prints, doesn't save)
│
├─ tests/
│  └─ test.py                  # Test template
│
├─ csv/                        # Test results (auto-generated)
│  ├─ users_list_results.csv
│  └─ products_get_results.csv
│
├─ .env.example                # Environment variables template
├─ .gitignore
├─ conftest.py                 # Shared fixtures
├─ test_base.py                # Reference test
├─ requirements.txt
└─ README.md
```

## 🚀 Quick Start

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
cp fetch_route_template.py fetch_users.py
```

Edit `fetch_users.py`:
```python
ENDPOINT_URL = "http://localhost:8000/users/list"
```

Run:
```bash
python fetch_users.py
# 200
#
# [{...}, {...}]
```

### 4. Create a test

```bash
cp tests/test.py tests/test_users_list.py
```

Edit `tests/test_users_list.py`:
```python
ENDPOINT = "users/list"
endpoint = "users/list"

CENARIOS = [
    ({}, "Without parameters", 200),
    ({"page": 1}, "Page 1", 200),
]
```

### 5. Run tests

```bash
pytest tests/test_users_list.py -v
# Results saved to: csv/users_list_results.csv
```

## 🔧 The Fetch Script

The script in `json/fetch_route_template.py` is a **simple visualization tool**:

```python
# Usage
ENDPOINT_URL = "http://localhost:8000/users/list"
fetch_endpoint(ENDPOINT_URL)

# Output
# 200
#
# [{...}, {...}]
```

It's just for you to **see what the API is returning** before writing tests.

**Does NOT create files, does NOT save anything, just PRINTS!**

## 📊 Components

### `config.py` - Configuration
- Loads variables from `.env`
- Provides defaults if `.env` doesn't exist
- `get_test_config()` - Global config
- `get_endpoint_config(endpoint_id)` - Per-endpoint config

### `client.py` - HTTP Client
- Automatic timing with `resp.elapsed_custom`
- Customizable headers
- Configurable timeout

### `csv_handler.py` - Results
- `initialize_csv()` - Creates file with headers
- `append_result()` - Adds result row

### `conftest.py` - Fixtures
- `client` - Fixture for all tests

## 📝 Complete Example

### Step 1: Document

```bash
cp fetch_route_template.py fetch_endpoint.py
```

```python
# fetch_endpoint.py
ENDPOINT_URL = "http://localhost:8000/api/endpoint"
fetch_endpoint(ENDPOINT_URL)
```

```bash
python fetch_endpoint.py
# 200
#
# {...}
```

### Step 2: Test

```bash
cp tests/test.py tests/test_endpoint.py
```

```python
# tests/test_endpoint.py
ENDPOINT = "api/endpoint"
endpoint = "api/endpoint"

CENARIOS = [
    ({}, "Without parameters", 200),
    ({"id": 1}, "With id", 200),
]

@pytest.mark.parametrize("params, description, expected_status", CENARIOS)
def test_endpoint(client, params, description, expected_status):
    resp = client.get(endpoint, params=params)
    assert resp.status_code == expected_status
```

```bash
pytest tests/test_endpoint.py -v
# Results in: csv/api_endpoint_results.csv
```

## ⚙️ Customization

### Custom Validation

```python
def validate_response(data):
    assert isinstance(data, dict)
    assert "id" in data

resp = client.get(endpoint, params=params)
validate_response(resp.json())
```

### Custom Headers

```python
from api_framework.config import get_test_config

CONFIG = get_test_config()
CONFIG["headers"]["Authorization"] = "Bearer token"
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: dotenv` | `pip install python-dotenv` |
| `Client fixture not found` | Check if `conftest.py` is in root |
| CSV not created | Add `autouse=True` to `setup_csv()` fixture |
| URL not recognized | Check `BASE_URL` in `.env` |

## 📚 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `http://localhost:8000` | API base URL |
| `TIMEOUT` | `10` | Timeout in seconds |
| `REPETITIONS` | `5` | Repetitions per scenario |
| `MAX_AVERAGE_TIME` | `30` | Time limit in seconds |

## 🚀 Next Steps

1. Create `.env` with your URLs
2. Document your routes with `fetch_route_template.py`
3. Create tests by copying `tests/test.py`
4. Run and analyze results in `csv/`

## 📖 References

- [pytest](https://docs.pytest.org/)
- [requests](https://requests.readthedocs.io/)
- [python-dotenv](https://python-dotenv.readthedocs.io/)
