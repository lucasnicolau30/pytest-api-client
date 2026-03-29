import os
from pathlib import Path
from .utils import build_path

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent.parent / ".env"
    load_dotenv(env_file)
except ImportError:
    pass  # python-dotenv not installed, use environment variables only


def get_base_url():
    """Get base URL from environment or use default."""
    return os.getenv("BASE_URL", "http://localhost:8000")

def get_headers():
    """Get default headers."""
    return {"accept": "application/json"}

def get_test_config():
    """
    Get universal test configuration (endpoint-agnostic).
    
    These settings apply to ANY API test.
    Use environment variables to override defaults.
    """
    return {
        "base_url": get_base_url(),
        "headers": get_headers(),
        "timeout": int(os.getenv("TIMEOUT", 10)),
        "repetitions": int(os.getenv("REPETITIONS", 5)),
        "max_average_time": int(os.getenv("MAX_AVERAGE_TIME", 30)),
    }

def get_endpoint_config(endpoint_id):
    """
    Get endpoint-specific configuration.
    
    Args:
        endpoint_id: Identifier for the endpoint 
        
    Returns:
        dict with endpoint-specific config
    """
    csv_filename = f"{endpoint_id.replace('/', '_')}_results.csv"
    
    return {
        "endpoint_id": endpoint_id,
        "csv_path": build_path("csv", csv_filename),
    }