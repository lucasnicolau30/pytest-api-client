"""
Scenarios template for API endpoint testing.

INSTRUCTIONS:
1. Copy this file and rename to scenarios_<endpoint_name>.py
2. Update SCENARIOS with your endpoint-specific test cases
3. Implement validate_response() for your API's response schema
4. Import in your test file: from tests import scenarios_<name> as scenarios

Example:
    # Step 1: Copy and rename
    copy: tests/scenarios.py → tests/scenarios_<endpoint_name>.py

    # Step 2: Update SCENARIOS
    SCENARIOS = [
        ({}, "Without parameters", 200),
        ({"limit": 5}, "Limit = 5", 200),
        ({"limit": 1}, "Limit = 1", 200),
    ]

    # Step 3: Implement validation
    def validate_response(data):
        assert isinstance(data, list), "Response must be a list"
        if len(data) > 0:
            assert "id" in data[0]
            assert isinstance(data[0]["id"], int)

STRUCTURE:
    Each scenario is a tuple of:
    (params_dict, description_string, expected_status_code)

    - params_dict: Query parameters to send with request
    - description_string: Human-readable test description
    - expected_status_code: Expected HTTP status (e.g., 200, 422)
"""

# ===============================================================
# CUSTOMIZE THIS FOR YOUR ENDPOINT/ROUTE
# ===============================================================

# Test scenarios - Define your endpoint test cases here
SCENARIOS = [
    ({}, "Without parameters", 200)
]


def validate_response(data):
    """
    Validate API response structure for your endpoint.

    Customize this function to match your API's response schema.
    Called after each successful request (status == 200).

    Args:
        data: Response JSON data from the API

    Raises:
        AssertionError: If response structure is invalid

    Example:
        # For a list endpoint:
        assert isinstance(data, list), "Response should be a list"
        for item in data:
            assert "id" in item, "Each item must have 'id'"
            assert isinstance(item["id"], int)
    """
    # TODO: Add your validation logic here
    pass
