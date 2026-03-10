"""
JSON response loader for endpoints.

This module loads pre-defined JSON responses for API validation and testing.
Each endpoint should have a corresponding JSON file in json/<endpoint_path>/ directory.
"""

import json
import os
from pathlib import Path


def load_response_json(endpoint_path):
    """
    Load response JSON for an endpoint.
    
    Args:
        endpoint_path: Path to endpoint (e.g., 'placas/top-dias')
        
    Returns:
        dict: Parsed JSON response
        
    Raises:
        FileNotFoundError: If response.json doesn't exist for endpoint
        json.JSONDecodeError: If JSON is invalid
    """
    # Build path to response.json
    base_dir = Path(__file__).parent.parent  # Go up from api-framework to root
    json_file = base_dir / "json" / endpoint_path / "response.json"
    
    if not json_file.exists():
        raise FileNotFoundError(
            f"Response file not found: {json_file}\n"
            f"Create it at: json/{endpoint_path}/response.json"
        )
    
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_expected_response(endpoint_path):
    """
    Get expected response structure for an endpoint.
    
    Args:
        endpoint_path: Path to endpoint (e.g., 'placas/top-dias')
        
    Returns:
        dict: Response with status and data
    """
    return load_response_json(endpoint_path)


def validate_response_against_template(actual_response, endpoint_path):
    """
    Validate actual response against template structure.
    
    Args:
        actual_response: Actual API response
        endpoint_path: Path to endpoint for template lookup
        
    Returns:
        bool: True if response matches template structure
        
    Raises:
        AssertionError: If validation fails
    """
    template = get_expected_response(endpoint_path)
    
    # Check status code
    assert actual_response.get("status") == template.get("status"), \
        f"Status mismatch: expected {template.get('status')}, got {actual_response.get('status')}"
    
    # Check data structure exists
    assert "data" in actual_response, "Missing 'data' field in response"
    
    return True
