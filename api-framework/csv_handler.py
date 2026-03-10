"""
CSV handling for test results.
"""

import csv
import os


def initialize_csv(arquivo_csv):
    """
    Create and initialize CSV file with headers.
    
    Args:
        arquivo_csv: Path to the CSV file
    """
    # Create directory if not exists
    diretorio = os.path.dirname(arquivo_csv)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio, exist_ok=True)
    
    with open(arquivo_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Cenário",
            "Parâmetros",
            "Status Esperado",
            "Status Real",
            "Tempo Médio (s)",
            "Tempo Mínimo (s)",
            "Tempo Máximo (s)",
            "Sucesso"
        ])


def append_result(arquivo_csv, descricao, params, status_esperado, status_real, tempo_medio, tempo_minimo, tempo_maximo, sucesso):
    """
    Append a test result row to CSV.
    
    Args:
        arquivo_csv: Path to CSV file
        descricao: Scenario description
        params: Request parameters dict
        status_esperado: Expected HTTP status
        status_real: Actual HTTP status
        tempo_medio: Average response time
        tempo_minimo: Minimum response time
        tempo_maximo: Maximum response time
        sucesso: Whether test passed
    """
    with open(arquivo_csv, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            descricao,
            str(params),
            status_esperado,
            status_real,
            round(tempo_medio, 3),
            round(tempo_minimo, 3),
            round(tempo_maximo, 3),
            "OK" if sucesso else "FAIL"
        ])