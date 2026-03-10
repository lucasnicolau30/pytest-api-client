import os 
from .utils import build_path

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
        "repeticoes": int(os.getenv("REPETICOES", 5)),
        "limite_tempo_medio": int(os.getenv("LIMITE_TEMPO_MEDIO", 30)),
    }

def get_endpoint_config(endpoint_id):
    """
    Get endpoint-specific configuration.
    
    Args:
        endpoint_id: Identifier for the endpoint 
        
    Returns:
        dict with endpoint-specific config
    """
    csv_filename = f"{endpoint_id}_results.csv"
    
    return {
        "endpoint_id": endpoint_id,
        "csv_path": build_path("csv", csv_filename),
    }