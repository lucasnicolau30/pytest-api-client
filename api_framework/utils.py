def build_url(base_url, endpoint):
    """
    Join base_url and endpoint removing duplicate slashes.
    
    Example:
        build_url('http://localhost:8000', '<endpoint_name>')  # 'http://localhost:8000/<endpoint_name>'
    """
    return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"


def build_path(base_path, filename):
    """
    Build file path safely, handling trailing/leading slashes.
    
    Args:
        base_path: Base directory path (e.g., 'csv')
        filename: Filename 
        
    Returns:
        Safe path with proper separators
        
    Example:
        build_path('csv', '<endpoint_name>.csv')  # 'csv/<endpoint_name>.csv'
    """
    return f"{base_path.rstrip('/')}/{filename.lstrip('/')}"

def calculate_statistics(times):
    """
    Calculate timing statistics from a list of response times.

    Args:
        times: List of float values representing response times in seconds

    Returns:
        dict with average, min, max statistics

    Raises:
        ValueError: If times list is empty
    """

    if not times:
        raise ValueError("Cannot calculate statistics from empty time list")

    return {
        "average": sum(times) / len(times),
        "min": min(times),
        "max": max(times)
    }