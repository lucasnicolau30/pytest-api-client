"""
Shared fixtures and configuration for all tests.

This file is automatically loaded by pytest.
"""

import pytest
from api_framework.client import APIClient
from api_framework.config import get_test_config


@pytest.fixture(scope="function")
def client():
    """Create API client for each test."""
    config = get_test_config()
    api_client = APIClient(
        base_url=config["base_url"],
        headers=config["headers"],
        timeout=config["timeout"]
    )
    yield api_client
    api_client.close()
