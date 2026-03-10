"""
Test scenarios template for API testing.

This module should be customized per endpoint/route.

STRUCTURE:
    Each scenario is a tuple of:
    (params_dict, description_string, expected_status_code)

    - params_dict: Query parameters to send with request
    - description_string: Human-readable test description
    - expected_status_code: Expected HTTP status (e.g., 200, 422)

EXAMPLE (for temporal series endpoint):
    CENARIOS = [
        ({}, "Sem parâmetros", 200),
        ({"limit": 1000}, "Limit 1000", 200),
        ({"limit": 10000}, "Limit máximo permitido (10000)", 200),
        ({"limit": 20000}, "Limit acima do permitido (erro esperado)", 422),
        ({"data_inicio": "2024-01-01T00:00:00"}, "Apenas data_inicio", 200),
        ({"data_fim": "2024-12-31T23:59:59"}, "Apenas data_fim", 200),
        ({
            "data_inicio": "2024-01-01T00:00:00",
            "data_fim": "2024-12-31T23:59:59"
        }, "Com data início e fim", 200),
    ]

INSTRUCTIONS:
    1. Replace CENARIOS list below with your endpoint-specific scenarios
    2. Each scenario tests a different combination of parameters
    3. Include both success cases (200) and error cases (4xx, 5xx)
    4. Use descriptive names that explain what's being tested
"""

# ✏️ CUSTOMIZE THIS FOR YOUR ENDPOINT/ROUTE
CENARIOS = [
    # Example structure:
    # ({}, "Scenario description", 200),
    # ({"param": "value"}, "Another scenario", 200),
    # ({"invalid": "params"}, "Error case", 422),
]

