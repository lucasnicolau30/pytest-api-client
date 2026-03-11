"""
Simple script to fetch and print API responses.

USAGE:
    1. Copy this file and rename (e.g., fetch_users.py)
    2. Update ENDPOINT_URL below
    3. Run: python fetch_users.py
    4. Response is printed to console

That's it! No files created, just visualization.
"""

import requests
import json


def fetch_endpoint(endpoint_url, headers=None):
    """
    Fetch and print API response.
    
    Args:
        endpoint_url: Full API endpoint URL
        headers: Optional request headers (default: json accept)
    """
    if headers is None:
        headers = {"accept": "application/json"}
    
    print(f"Fetching: {endpoint_url}\n")
    
    resp = requests.get(endpoint_url, headers=headers)
    
    # Print status
    print(resp.status_code)
    
    # Print response (empty line between)
    print()
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    # ===================================================
    # CUSTOMIZE THIS
    # ===================================================
    ENDPOINT_URL = "http://localhost:8000/users/list"  # TODO: Change to your endpoint
    
    fetch_endpoint(ENDPOINT_URL)
