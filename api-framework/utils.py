def build_url(base_url, endpoint):
    """Join base_url and endpoint removing duplicate slashes."""
    return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"


def build_path(base_path, filename):
    """
    Build file path safely, handling trailing/leading slashes.
    
    Args:
        base_path: Base directory path (e.g., 'csv')
        filename: Filename (e.g., 'serie_temporal_results.csv')
        
    Returns:
        Safe path with proper separators
        
    Example:
        build_path('csv', 'serie_temporal_results.csv')  # 'csv/serie_temporal_results.csv'
        build_path('csv/', '/serie_temporal_results.csv') # 'csv/serie_temporal_results.csv'
    """
    return f"{base_path.rstrip('/')}/{filename.lstrip('/')}"


def validate_temporal_series_response(data):
    """
    Validate temporal series response structure.
    
    Args:
        data: Response data (should be a list)
        
    Raises:
        AssertionError: If validation fails
    """
    assert isinstance(data, list), "A resposta deve ser uma lista (série temporal)."

    if len(data) == 0:
        return  # Empty list is valid

    # Validate first item structure
    ponto = data[0]

    campos_esperados = [
        "data_hora",
        "tensao_media",
        "corrente_media",
        "consumo_kwh",
        "fator_potencia",
        "temperatura",
        "umidade",
        "potencia_kw"  
    ]

    # Check all fields exist
    for campo in campos_esperados:
        assert campo in ponto, f"Campo ausente: {campo}"

    # Check field types
    assert isinstance(ponto["data_hora"], str), "data_hora deve ser string"
    assert isinstance(ponto["tensao_media"], (int, float, type(None))), "tensao_media tipo inválido"
    assert isinstance(ponto["corrente_media"], (int, float, type(None))), "corrente_media tipo inválido"
    assert isinstance(ponto["fator_potencia"], (int, float, type(None))), "fator_potencia tipo inválido"
    assert isinstance(ponto["consumo_kwh"], (int, float, type(None))), "consumo_kwh tipo inválido"
    assert isinstance(ponto["temperatura"], (int, float, type(None))), "temperatura tipo inválido"
    assert isinstance(ponto["umidade"], (int, float, type(None))), "umidade tipo inválido"
    assert isinstance(ponto["potencia_kw"], (int, float, type(None))), "potencia_kw tipo inválido"


def calculate_statistics(tempos):
    """
    Calculate timing statistics.
    
    Args:
        tempos: List of timing measurements
        
    Returns:
        dict with media, menor, maior
    """
    return {
        "media": sum(tempos) / len(tempos),
        "menor": min(tempos),
        "maior": max(tempos)
    }