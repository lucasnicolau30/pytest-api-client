"""
Generic test template for API endpoints.

INSTRUCTIONS:
1. Copy this file and rename to test_<endpoint_name>.py
2. Copy scenarios.py and rename to scenarios_<endpoint_name>.py
3. Update both files with your endpoint-specific configuration
4. Run tests with: pytest -v tests/test_<endpoint_name>.py

"""

import pytest
from api_framework.config import get_test_config, get_endpoint_config
from api_framework.utils import calculate_statistics
from api_framework.csv_handler import initialize_csv, append_result

# TODO: Import your endpoint's scenarios and validation
# For now, it imports the template scenarios:
from tests.scenarios import SCENARIOS, validate_response


# ===============================================================
# CONFIGURATION
# ===============================================================
ENDPOINT = "<endpoint_name>"  # TODO: Change to your endpoint 
CONFIG = get_test_config()
ENDPOINT_CONFIG = get_endpoint_config(ENDPOINT)


# ===============================================================
# FIXTURES
# ===============================================================
@pytest.fixture(scope="session", autouse=True)
def setup_csv():
    """Initialize CSV file before tests."""
    initialize_csv(ENDPOINT_CONFIG["csv_path"])


# ===============================================================
# PARAMETRIZED TEST
# ===============================================================
@pytest.mark.parametrize(
    "params, description, expected_status",
    SCENARIOS,
    ids=[desc for _, desc, _ in SCENARIOS]
)
def test_endpoint(client, params, description, expected_status):
    """
    Test API endpoint with scenarios and validation.

    Args:
        client: APIClient fixture (from conftest.py)
        params: Query parameters for the request
        description: Test scenario description
        expected_status: Expected HTTP status code
    """
    times = []
    success = True
    actual_status = None

    print(f"\n=== Scenario: {description} ===")
    print(f"Parameters: {params}")

    # ============================================================
    # EXECUTE REQUESTS
    # ============================================================
    for i in range(CONFIG["repetitions"]):
        resp = client.get(ENDPOINT, params=params)

        duration = resp.elapsed_custom
        times.append(duration)
        actual_status = resp.status_code

        print(f"➡️ Attempt {i+1}: {actual_status} in {duration:.3f}s")

        # ====================================================================
        # HANDLE ERROR RESPONSES (status != 200)
        # ====================================================================
        if expected_status != 200:
            if actual_status == expected_status:
                print("✔ Expected error received correctly.")
            else:
                print(f"❌ Incorrect error: received {actual_status}, expected {expected_status}")
                success = False
            break

        # ====================================================================
        # VALIDATE SUCCESS RESPONSES
        # ====================================================================
        if actual_status != 200:
            success = False
            print(f"❌ Unexpected status: {actual_status}, expected: {expected_status}")
            break

        # Validate response structure
        try:
            data = resp.json()
            validate_response(data)
        except (ValueError, AssertionError) as e:
            success = False
            print(f"❌ Response validation failed: {e}")
            break

    # ============================================================
    # CALCULATE STATISTICS
    # ============================================================
    stats = calculate_statistics(times)
    average = stats["average"]
    min_time = stats["min"]
    max_time = stats["max"]

    print(f"\nResults — {description}")
    print(f"  Expected Status: {expected_status}")
    print(f"  Actual Status: {actual_status}")
    print(f"  Average: {average:.3f}s | Min: {min_time:.3f}s | Max: {max_time:.3f}s")

    # ============================================================
    # SAVE TO CSV
    # ============================================================
    append_result(
        ENDPOINT_CONFIG["csv_path"],
        description,
        params,
        expected_status,
        actual_status,
        average,
        min_time,
        max_time,
        success
    )

    # ============================================================
    # ASSERT TIME LIMIT (only for successful responses)
    # ============================================================
    if expected_status == 200:
        assert average < CONFIG["max_average_time"], \
            f"High average response time ({average:.2f}s) in {description}"
