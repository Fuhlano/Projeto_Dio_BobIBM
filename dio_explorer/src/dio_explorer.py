"""
dio_explorer.py
---------------
Módulo principal com as lógicas dos comandos /trilha, /desafio e /certificado.
Lê dados de dio_explorer/data/trilhas_dio.json e retorna dicionários estruturados.
"""

import json
import os
import random
import string
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Resolução do caminho do JSON (independente de onde o script é chamado)
# ---------------------------------------------------------------------------
_BASE_DIR = Path(__file__).resolve().parent.parent          # dio_explorer/
_DATA_PATH = _BASE_DIR / "data" / "trilhas_dio.json"


def carregar_trilhas(caminho: str | Path = _DATA_PATH) -> dict:
    """Carrega e retorna o conteúdo completo do JSON de trilhas."""
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# /trilha <tecnologia>
# ---------------------------------------------------------------------------

def buscar_trilha(tecnologia: str, caminho: str | Path = _DATA_PATH) -> dict | None:
    """
    Busca uma trilha pelo campo `tecnologia` (case-insensitive).

    Retorna o dict da trilha encontrada ou None se não existir.
    """
    dados = carregar_trilhas(caminho)
    tecnologia_lower = tecnologia.strip().lower()
    for trilha in dados["trilhas"]:
        if trilha["tecnologia"].lower() == tecnologia_lower:
            return trilha
    return None


def listar_tecnologias(caminho: str | Path = _DATA_PATH) -> list[dict]:
    """Retorna lista de {tecnologia, nivel} de todas as trilhas cadastradas."""
    dados = carregar_trilhas(caminho)
    return [
        {"tecnologia": t["tecnologia"], "nivel": t["nivel"]}
        for t in dados["trilhas"]
    ]


def formatar_trilha(trilha: dict) -> str:
    """Formata os dados de uma trilha em texto legível (markdown simplificado)."""
    vitalicio = "Sim" if trilha["vitalicio"] else "Não"
    badges = "\n".join(f"  - {b}" for b in trilha["badges"])
    lives = "\n".join(
        f"  [{l['data']}] {l['titulo']} ({l['duracao_min']} min)"
        for l in trilha["lives_ao_vivo"]
    )
    promo = trilha["promocao"]
    if promo["ativa"]:
        promocao_txt = f"{promo['desconto_percentual']}% de desconto (válido até {promo['validade']})"
    else:
        promocao_txt = "Sem promoção ativa no momento."

    return (
        f"# Trilha DIO: {trilha['nome']}\n"
        f"Tecnologia : {trilha['tecnologia']}\n"
        f"Nível      : {trilha['nivel']}\n"
        f"Módulos    : {trilha['modulos']}\n"
        f"XP Total   : {trilha['xp_total']} XP\n"
        f"Vitalício  : {vitalicio}\n\n"
        f"Badges:\n{badges}\n\n"
        f"Lives:\n{lives}\n\n"
        f"Promoção   : {promocao_txt}"
    )


# ---------------------------------------------------------------------------
# /desafio <tecnologia> <nivel>
# ---------------------------------------------------------------------------

_NIVEIS_VALIDOS = {"básico", "intermediário", "avancado", "avançado"}
_XP_NIVEL = {"Básico": 150, "Intermediário": 350, "Avançado": 600}
_TEMPO_NIVEL = {
    "Básico": "15–30 min",
    "Intermediário": "30–60 min",
    "Avançado": "60–120 min",
}

_TEMAS_POR_TECNOLOGIA: dict[str, list[str]] = {
    "java": [
        "Calculadora de Impostos com OOP",
        "Sistema de Filas com BlockingQueue",
        "CRUD com Spring Boot e JPA",
        "Streams API — Processamento de Dados",
    ],
    "python": [
        "Análise de CSV com pandas",
        "Web scraper simples com requests",
        "Gerador de senhas seguras",
        "Decorators e Context Managers",
    ],
    "default": [
        "Algoritmo de busca binária",
        "Implementação de pilha e fila",
        "Validador de expressões matemáticas",
        "Gerador de relatório em texto",
    ],
}


def normalizar_nivel(nivel: str) -> str:
    """Normaliza o nível para um dos valores padrão (Básico/Intermediário/Avançado)."""
    mapa = {
        "basico": "Básico",
        "básico": "Básico",
        "intermediario": "Intermediário",
        "intermediário": "Intermediário",
        "avancado": "Avançado",
        "avançado": "Avançado",
    }
    return mapa.get(nivel.strip().lower(), "Intermediário")


def gerar_desafio(tecnologia: str, nivel: str) -> dict:
    """
    Gera um desafio de código para a tecnologia e nível informados.

    Retorna dict com: tecnologia, nivel, tema, xp, tempo_sugerido, aviso (se houver).
    """
    nivel_normalizado = normalizar_nivel(nivel)
    tech_key = tecnologia.strip().lower()
    temas = _TEMAS_POR_TECNOLOGIA.get(tech_key, _TEMAS_POR_TECNOLOGIA["default"])
    tema = random.choice(temas)

    aviso = None
    if nivel.strip().lower() not in _NIVEIS_VALIDOS:
        aviso = f"Nível '{nivel}' não reconhecido. Usando 'Intermediário' como padrão."
    if tech_key not in _TEMAS_POR_TECNOLOGIA:
        aviso = (aviso or "") + f" Tecnologia '{tecnologia}' não mapeada; usando desafio genérico."

    return {
        "tecnologia": tecnologia,
        "nivel": nivel_normalizado,
        "tema": tema,
        "xp": _XP_NIVEL[nivel_normalizado],
        "tempo_sugerido": _TEMPO_NIVEL[nivel_normalizado],
        "aviso": aviso,
    }


# ---------------------------------------------------------------------------
# /certificado <nome> <tecnologia>
# ---------------------------------------------------------------------------

def _gerar_codigo_certificado(id_trilha: int) -> str:
    """Gera código único no formato DIO-{id}-{ano}-XXXXXX."""
    ano = date.today().year
    sufixo = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"DIO-{id_trilha}-{ano}-{sufixo}"


def gerar_certificado(nome_aluno: str, tecnologia: str, caminho: str | Path = _DATA_PATH) -> dict:
    """
    Gera o dict de um certificado fictício para o aluno na trilha informada.

    Retorna dict com dados do certificado; inclui campo `aviso` quando a trilha
    não é encontrada e dados genéricos são usados.
    """
    trilha = buscar_trilha(tecnologia, caminho)
    aviso = None

    if trilha is None:
        aviso = f"Trilha '{tecnologia}' não encontrada. Certificado gerado com dados genéricos."
        trilha = {
            "id": 0,
            "nome": f"Trilha {tecnologia}",
            "tecnologia": tecnologia,
            "nivel": "Concluído",
            "modulos": 0,
            "xp_total": 5000,
            "badges": [],
        }

    codigo = _gerar_codigo_certificado(trilha["id"])
    data_emissao = date.today().strftime("%d/%m/%Y")

    return {
        "aluno": nome_aluno,
        "trilha_nome": trilha["nome"],
        "tecnologia": trilha["tecnologia"],
        "nivel": trilha["nivel"],
        "modulos": trilha["modulos"],
        "xp_total": trilha["xp_total"],
        "badges": trilha.get("badges", []),
        "codigo": codigo,
        "data_emissao": data_emissao,
        "aviso": aviso,
    }
