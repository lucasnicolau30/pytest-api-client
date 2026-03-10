"""
Test suite for /placas/top-dias endpoint.

This is an example of how to use the pytest-api-client framework.
"""

import pytest
from api_framework.client import APIClient
from api_framework.config import get_test_config, get_endpoint_config
from api_framework.scenarios import CENARIOS
from api_framework.utils import calculate_statistics
from api_framework.json_handler import get_expected_response
from api_framework.csv_handler import initialize_csv, append_result


# ===============================================================
# CONFIGURATION
# ===============================================================
CONFIG = get_test_config()
ENDPOINT = "placas/top-dias"
ENDPOINT_CONFIG = get_endpoint_config(ENDPOINT)


# ===============================================================
# FIXTURES
# ===============================================================
@pytest.fixture(scope="session", autouse=True)
def setup_csv():
    """Initialize CSV file before tests."""
    initialize_csv(ENDPOINT_CONFIG["csv_path"])


@pytest.fixture(scope="function")
def client():
    """Create API client for each test."""
    api_client = APIClient(
        base_url=CONFIG["base_url"],
        headers=CONFIG["headers"],
        timeout=CONFIG["timeout"]
    )
    yield api_client
    api_client.close()


# ===============================================================
# TEST SCENARIOS (Customize for this endpoint)
# ===============================================================
# Replace CENARIOS in api_framework.scenarios with specific ones:
top_dias_scenarios = [
    ({}, "Sem parâmetros", 200),
    ({"limit": 10}, "Limit 10", 200),
    ({"limit": 100}, "Limit 100", 200),
]


# ===============================================================
# PARAMETRIZED TEST
# ===============================================================
@pytest.mark.parametrize(
    "params, descricao, status_esperado",
    top_dias_scenarios,
    ids=[d for _, d, _ in top_dias_scenarios]
)
def test_top_dias(client, params, descricao, status_esperado):
    """
    Test /placas/top-dias endpoint.
    
    Args:
        client: APIClient fixture
        params: Query parameters
        descricao: Test description
        status_esperado: Expected HTTP status
    """
    tempos = []
    sucesso = True
    status_real = None
    
    endpoint = "top-dias"  # Endpoint path
    
    print(f"\n=== Cenário: {descricao} ===")
    print(f"Parâmetros: {params}")
    
    # ============================================================
    # EXECUTE REQUESTS
    # ============================================================
    for i in range(CONFIG["repeticoes"]):
        resp = client.get(endpoint, params=params)
        
        duracao = resp.elapsed_custom
        tempos.append(duracao)
        status_real = resp.status_code
        
        print(f"➡️ Tentativa {i+1}: {status_real} em {duracao:.3f}s")
        
        # ====================================================================
        # HANDLE ERROR RESPONSES
        # ====================================================================
        if status_esperado != 200:
            if status_real == status_esperado:
                print("✔ Erro esperado recebido corretamente.")
            else:
                print(f"❌ Erro incorreto: recebido {status_real}, esperado {status_esperado}")
                sucesso = False
            break
        
        # ====================================================================
        # VALIDATE SUCCESS RESPONSES
        # ====================================================================
        if status_real != 200:
            sucesso = False
            print(f"❌ Status inesperado: {status_real}, esperado: {status_esperado}")
            break
        
        # Validate response structure
        data = resp.json()
        # TODO: Add custom validation for top-dias response
    
    # ============================================================
    # CALCULATE STATISTICS
    # ============================================================
    stats = calculate_statistics(tempos)
    media = stats["media"]
    menor = stats["menor"]
    maior = stats["maior"]
    
    print(f"\nResultados — {descricao}")
    print(f"  Status Esperado: {status_esperado}")
    print(f"  Status Real: {status_real}")
    print(f"  Média: {media:.3f}s | Mínimo: {menor:.3f}s | Máximo: {maior:.3f}s")
    
    # ============================================================
    # SAVE TO CSV
    # ============================================================
    append_result(
        ENDPOINT_CONFIG["csv_path"],
        descricao,
        params,
        status_esperado,
        status_real,
        media,
        menor,
        maior,
        sucesso
    )
    
    # ============================================================
    # ASSERT TIME LIMIT (only for successful responses)
    # ============================================================
    if status_esperado == 200:
        assert media < CONFIG["limite_tempo_medio"], \
            f"Tempo médio alto ({media:.2f}s) em {descricao}"
