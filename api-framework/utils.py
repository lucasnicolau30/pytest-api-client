def build_url(base_url, endpoint):
    """Join base_url and endpoint removing duplicate slashes."""
    return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"