import pytest
import time

from api_framework.client import APIClient
from api_framework.config import get_test_config
from api_framework.scenarios import CENARIOS
from api_framework.utils import validate_temporal_series_response, calculate_statistics
from api_framework.csv_handler import initialize_csv, append_result

# ===============================================================
# LOAD CONFIGURATION
# ===============================================================
CONFIG = get_test_config()

# ===============================================================
# FIXTURE HTTP CLIENT
# ===============================================================
@pytest.fixture(scope="session", autouse=True)
def setup_csv():
    """Initialize CSV file before tests."""
    initialize_csv(CONFIG["arquivo_csv"])


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
# TESTE PARAMETRIZADO
# ===============================================================
@pytest.mark.parametrize(
    "params, descricao, status_esperado",
    CENARIOS,
    ids=[d for _, d, _ in CENARIOS]
)
def test_serie_temporal(client, params, descricao, status_esperado):
    """
    Test temporal series API endpoint with various scenarios.
    
    Args:
        client: APIClient fixture
        params: Query parameters to send
        descricao: Test scenario description
        status_esperado: Expected HTTP status code
    """
    tempos = []
    sucesso = True
    status_real = None

    # Build endpoint URL with quadro ID
    endpoint = f"{CONFIG['quadro_id']}"

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
        # HANDLE ERROR RESPONSES (status != 200)
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
        validate_temporal_series_response(data)

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
        CONFIG["arquivo_csv"],
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
