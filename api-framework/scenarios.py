"""
Test scenarios and validation template for API endpoints.

This module should be customized per endpoint/route to define test cases
and API response validation logic.

CUSTOMIZATION:
1. Update SCENARIOS with your endpoint-specific test cases
2. Implement validate_response() for your API's response schema

STRUCTURE:
    Each scenario is a tuple of:
    (params_dict, description_string, expected_status_code)

    - params_dict: Query parameters to send with request
    - description_string: Human-readable test description
    - expected_status_code: Expected HTTP status (e.g., 200, 422)

EXAMPLE (for temporal series endpoint):
    SCENARIOS = [
        ({}, "Without parameters", 200),
        ({"limit": 1000}, "Limit 1000", 200),
        ({"limit": 10000}, "Maximum allowed limit (10000)", 200),
        ({"limit": 20000}, "Limit above allowed (expected error)", 422),
        ({"data_inicio": "2024-01-01T00:00:00"}, "Only start date", 200),
        ({"data_fim": "2024-12-31T23:59:59"}, "Only end date", 200),
        ({
            "data_inicio": "2024-01-01T00:00:00",
            "data_fim": "2024-12-31T23:59:59"
        }, "With start and end dates", 200),
    ]
    
    def validate_response(data):
        assert isinstance(data, list)
        for item in data:
            assert "timestamp" in item
            assert "value" in item
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
        # For a list endpoint returning items with id and name:
        assert isinstance(data, list), "Response should be a list"
        for item in data:
            assert "id" in item, "Each item must have 'id'"
            assert "name" in item, "Each item must have 'name'"
    """
    # TODO: Add your validation logic here
    # Example: assert isinstance(data, dict), "Response should be a dictionary"
    pass

