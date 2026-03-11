def build_url(base_url, endpoint):
    """
    Join base_url and endpoint removing duplicate slashes.
    
    Example:
        build_url('http://localhost:8000', 'users/list')  # 'http://localhost:8000/users/list'
    """
    return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"


def build_path(base_path, filename):
    """
    Build file path safely, handling trailing/leading slashes.
    
    Args:
        base_path: Base directory path (e.g., 'csv')
        filename: Filename (e.g., 'users_list_results.csv')
        
    Returns:
        Safe path with proper separators
        
    Example:
        build_path('csv', 'users_list_results.csv')  # 'csv/users_list_results.csv'
    """
    return f"{base_path.rstrip('/')}/{filename.lstrip('/')}"