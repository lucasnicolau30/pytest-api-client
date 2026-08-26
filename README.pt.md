# pytest-api-client Framework

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Read in: Português | [English](README.md)

Framework modularizado para testes de API com pytest, projetado para ser reutilizável e escalável.

## Estrutura do Projeto

```
pytest-api-client/
├─ api_framework/              # Framework reutilizável
│  ├─ client.py                # Cliente HTTP com medição de tempo
│  ├─ config.py                # Configuração (carrega .env)
│  ├─ utils.py                 # Utilitários
│  ├─ csv_handler.py           # Gerencia resultados em CSV
│  └─ __init__.py
│
├─ tests/
│  ├─ test_base.py             # Template de teste (copiar por endpoint)
│  └─ scenarios.py             # Template de cenários (copiar por endpoint)
│
├─ json/                       # Scripts para visualizar respostas da API
│  └─ fetch_route_template.py  # Template (usa BASE_URL do .env)
│
├─ csv/                        # Resultados dos testes (gerado automaticamente)
│
├─ .env.example                # Template de variáveis de ambiente
├─ .gitignore
├─ conftest.py                 # Fixtures compartilhadas
├─ requirements.txt
└─ README.md
```

## Contexto

Desenvolvido durante um estágio de QA para automatizar testes de API em múltiplos endpoints.
Alcançou 98% de acurácia nas rotas em cenários positivos/negativos, validação de status code
e verificação da estrutura das respostas JSON. Os resultados são exportados para CSV para rastreabilidade.

## Início Rápido

### 1. Configuração

```bash
# Instalar dependências
pip install -r requirements.txt

# Criar .env (opcional, usa valores padrão se não existir)
cp .env.example .env
```

### 2. Editar .env

```env
BASE_URL=http://localhost:8000
TIMEOUT=10
REPETITIONS=5
MAX_AVERAGE_TIME=30
```

### 3. Visualizar uma resposta da API

```bash
cd json
cp fetch_route_template.py fetch_route_<nome_endpoint>.py
```

Editar `fetch_route_<nome_endpoint>.py`:

```python
ENDPOINT = "<nome_endpoint>"  # Altere para o caminho do seu endpoint
```

Executar:

```bash
python fetch_route_<nome_endpoint>.py
# 200
#
# [{...}, {...}]
```

### 4. Criar um teste

```bash
# Passo 1: Copiar template de cenários
cp tests/scenarios.py tests/scenarios_<nome_endpoint>.py

# Passo 2: Copiar template de teste
cp tests/test_base.py tests/test_<nome_endpoint>.py
```

Editar `tests/scenarios_<nome_endpoint>.py`:

```python
SCENARIOS = [
    ({}, "Sem parâmetros", 200),
    ({"page": 1}, "Página 1", 200),
]

def validate_response(data):
    assert isinstance(data, list)
```

Editar `tests/test_<nome_endpoint>.py`:

```python
from tests import scenarios_<nome_endpoint> as scenarios

ENDPOINT = "<nome_endpoint>"  # Altere para o caminho do seu endpoint
```

### 5. Executar os testes

```bash
pytest tests/test_<nome_endpoint>.py -v
# Resultados salvos em: csv/<nome_endpoint>_results.csv
```

## O Script de Fetch

O script em `json/fetch_route_template.py` é uma **ferramenta simples de visualização** que usa a `BASE_URL` do seu `.env`:

```python
# Uso - especifique apenas o caminho do endpoint, não a URL completa
ENDPOINT = "<nome_endpoint>"  # Apenas o caminho do endpoint
fetch_endpoint(ENDPOINT)

# Saída
# Fetching: http://localhost:8000/<nome_endpoint>
# 200
#
# [{...}, {...}]
```

Serve apenas para você **ver o que a API está retornando** antes de escrever os testes.

**NÃO cria arquivos, NÃO salva nada, apenas IMPRIME!**

## Componentes

### `config.py` - Configuração

- Carrega variáveis do `.env`
- Fornece valores padrão caso o `.env` não exista
- `get_test_config()` - Configuração global
- `get_endpoint_config(endpoint)` - Configuração por endpoint (para nomeação de CSV)

### `client.py` - Cliente HTTP

- Medição de tempo automática com `resp.elapsed_custom`
- Headers customizáveis
- Timeout configurável
- Constrói a URL completa a partir de `BASE_URL + endpoint`

### `csv_handler.py` - Resultados

- `initialize_csv()` - Cria o arquivo com cabeçalhos
- `append_result()` - Adiciona linha de resultado

### `conftest.py` - Fixtures

- `client` - Fixture para todos os testes (escopo por função)

## Exemplo Completo

### Passo 1: Documentar

```bash
cd json
cp fetch_route_template.py fetch_route_<nome_endpoint>.py
```

Editar `fetch_route_template.py fetch_route_<nome_endpoint>.py`:

```python
ENDPOINT = "<nome_endpoint>"  # Altere para o seu endpoint
fetch_endpoint(ENDPOINT)
```

Executar:

```bash
python fetch_route_template.py fetch_route_<nome_endpoint>.py
# 200
#
# {...}
```

### Passo 2: Criar Cenários

```bash
cp tests/scenarios.py tests/scenarios_<nome_endpoint>.py
```

Editar `tests/scenarios_<nome_endpoint>.py`:

```python
SCENARIOS = [
    ({}, "Sem parâmetros", 200),
    ({"id": 1}, "Com id", 200),
]

def validate_response(data):
    assert isinstance(data, dict)
    assert "id" in data
```

### Passo 3: Testar

```bash
cp tests/test_base.py tests/test_<nome_endpoint>.py
```

Editar `tests/test_<nome_endpoint>.py`:

```python
from tests import scenarios_<nome_endpoint> as scenarios

ENDPOINT = "<nome_endpoint>"  # Altere para o seu endpoint
```

Executar:

```bash
pytest tests/test_<nome_endpoint>.py -v
# Resultados em: csv/<nome_endpoint>_results.csv
```

## Customização

### Validação Customizada

```python
def validate_response(data):
    assert isinstance(data, dict)
    assert "id" in data

# Chamada automaticamente em test_endpoint
```

### Headers Customizados

Edite o `.env` ou sobrescreva no teste:

```python
from api_framework.config import get_test_config

CONFIG = get_test_config()
CONFIG["headers"]["Authorization"] = "Bearer token"
```

## Solução de Problemas

| Problema                      | Solução                                          |
| ------------------------------ | ------------------------------------------------ |
| `ModuleNotFoundError: dotenv`  | `pip install python-dotenv`                       |
| `Client fixture not found`     | Verifique se o `conftest.py` está na raiz         |
| CSV não criado                 | Verifique se o diretório `csv/` existe (criado automaticamente) |
| URL não reconhecida            | Verifique o `BASE_URL` no `.env`                  |

## Variáveis de Ambiente

| Variável            | Padrão                   | Descrição                  |
| -------------------- | ------------------------ | --------------------------- |
| `BASE_URL`           | `http://localhost:8000`  | URL base da API             |
| `TIMEOUT`            | `10`                     | Timeout em segundos         |
| `REPETITIONS`        | `5`                      | Repetições por cenário      |
| `MAX_AVERAGE_TIME`   | `30`                     | Limite de tempo em segundos |

## Próximos Passos

1. Criar `.env` com suas URLs
2. Documentar suas rotas com `fetch_route_template.py`
3. Criar testes copiando `tests/test_base.py`
4. Executar e analisar resultados em `csv/`

## Referências

- [pytest](https://docs.pytest.org/)
- [requests](https://requests.readthedocs.io/)
- [python-dotenv](https://python-dotenv.readthedocs.io/)

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## Autor

Lucas Nicolau — Estudante de Engenharia de Software na @UFAM
