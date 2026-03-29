"""
Simple script to fetch and print API responses.

USAGE:
    1. Copy this file and rename
    2. Update ENDPOINT below
    3. Run: python fetch_<endpoint_name>.py
    4. Response is printed to console

That's it! No files created, just visualization.
"""

import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from api_framework.config import get_base_url
from api_framework.utils import build_url


def fetch_endpoint(endpoint, headers = None):
    """
    Fetch and print API response.

    Args:
        endpoint: API endpoint path
        headers: Optional request headers (default: json accept)
    """
    if headers is None:
        headers = {"accept": "application/json"}

    # Build full URL from base_url + endpoint
    base_url = get_base_url()
    url = build_url(base_url, endpoint)

    print(f"Fetching: {url}\n")

    resp = requests.get(url, headers = headers)

    # Print status
    print(resp.status_code)

    # Print response (empty line between)
    print()
    print(json.dumps(resp.json(), indent = 2, ensure_ascii = False))


if __name__ == "__main__":
    # ===================================================
    # CUSTOMIZE THIS - Change to your endpoint path
    # ===================================================
    ENDPOINT = "<endpoint_name>"  # Example 

    fetch_endpoint(ENDPOINT)