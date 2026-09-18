"""
test_dio_explorer.py
---------------------
Testes unitários para os comandos /trilha, /desafio e /certificado.

Cobertura alvo: ≥ 70%

Execute com:
    python -m pytest src/test_dio_explorer.py -v
ou com cobertura:
    python -m pytest src/test_dio_explorer.py -v --cov=src.dio_explorer --cov-report=term-missing
"""

import sys
import os
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open
from datetime import date

# Garante que o pacote src seja encontrado independentemente de onde pytest roda
sys.path.insert(0, str(Path(__file__).resolve().parent))

import dio_explorer as de


# ---------------------------------------------------------------------------
# Fixture: JSON mínimo para testes (sem depender do arquivo real)
# ---------------------------------------------------------------------------

TRILHA_JAVA = {
    "id": 5,
    "nome": "Java Spring Boot Microservices",
    "tecnologia": "Java",
    "nivel": "Avançado",
    "modulos": 18,
    "xp_total": 15000,
    "badges": ["Java Champion", "Spring Expert", "Microservices Architect", "API Designer"],
    "promocao": {
        "ativa": True,
        "desconto_percentual": 40,
        "validade": "2025-07-31",
    },
    "vitalicio": True,
    "lives_ao_vivo": [
        {"titulo": "Spring Boot com Docker", "data": "2025-07-12", "duracao_min": 120},
        {"titulo": "Kafka com Spring", "data": "2025-07-26", "duracao_min": 90},
    ],
}

TRILHA_PYTHON = {
    "id": 1,
    "nome": "Fundamentos de Python para Iniciantes",
    "tecnologia": "Python",
    "nivel": "Básico",
    "modulos": 8,
    "xp_total": 4500,
    "badges": ["Python Explorer", "Code Starter", "Logic Master"],
    "promocao": {"ativa": False, "desconto_percentual": 0, "validade": None},
    "vitalicio": True,
    "lives_ao_vivo": [
        {"titulo": "Introdução ao Python", "data": "2025-07-10", "duracao_min": 90},
    ],
}

MOCK_JSON = {
    "trilhas": [TRILHA_JAVA, TRILHA_PYTHON],
    "metadata": {
        "total_trilhas": 2,
        "fonte": "DIO",
        "url_base": "https://web.dio.me/",
        "gerado_em": "2025-07-01",
        "niveis_disponiveis": ["Básico", "Intermediário", "Avançado"],
        "xp_medio": 9750,
        "trilhas_com_promocao": 1,
        "trilhas_vitalicio": 2,
    },
}


def _criar_json_temp() -> Path:
    """Cria um arquivo JSON temporário com MOCK_JSON e retorna o caminho."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    json.dump(MOCK_JSON, tmp, ensure_ascii=False)
    tmp.close()
    return Path(tmp.name)


# ---------------------------------------------------------------------------
# Testes: carregar_trilhas
# ---------------------------------------------------------------------------

class TestCarregarTrilhas(unittest.TestCase):

    def setUp(self):
        self.json_path = _criar_json_temp()

    def tearDown(self):
        os.unlink(self.json_path)

    def test_retorna_dict_com_chave_trilhas(self):
        dados = de.carregar_trilhas(self.json_path)
        self.assertIn("trilhas", dados)

    def test_retorna_dict_com_chave_metadata(self):
        dados = de.carregar_trilhas(self.json_path)
        self.assertIn("metadata", dados)

    def test_quantidade_trilhas_corretas(self):
        dados = de.carregar_trilhas(self.json_path)
        self.assertEqual(len(dados["trilhas"]), 2)

    def test_arquivo_inexistente_lanca_excecao(self):
        with self.assertRaises(FileNotFoundError):
            de.carregar_trilhas("/caminho/que/nao/existe.json")


# ---------------------------------------------------------------------------
# Testes: buscar_trilha  →  comando /trilha
# ---------------------------------------------------------------------------

class TestBuscarTrilha(unittest.TestCase):

    def setUp(self):
        self.json_path = _criar_json_temp()

    def tearDown(self):
        os.unlink(self.json_path)

    # --- Casos de sucesso ---

    def test_encontra_java_exato(self):
        """Deve encontrar trilha Java com nome exato."""
        resultado = de.buscar_trilha("Java", self.json_path)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["tecnologia"], "Java")

    def test_encontra_java_minusculo(self):
        """Deve encontrar trilha Java com entrada em minúsculas."""
        resultado = de.buscar_trilha("java", self.json_path)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["id"], 5)

    def test_encontra_java_maiusculo(self):
        """Deve encontrar trilha Java com entrada em maiúsculas."""
        resultado = de.buscar_trilha("JAVA", self.json_path)
        self.assertIsNotNone(resultado)

    def test_encontra_python(self):
        resultado = de.buscar_trilha("Python", self.json_path)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["nome"], "Fundamentos de Python para Iniciantes")

    def test_encontra_python_minusculo(self):
        resultado = de.buscar_trilha("python", self.json_path)
        self.assertIsNotNone(resultado)

    # --- Campos da trilha Java ---

    def test_trilha_java_tem_modulos_corretos(self):
        trilha = de.buscar_trilha("java", self.json_path)
        self.assertEqual(trilha["modulos"], 18)

    def test_trilha_java_tem_xp_correto(self):
        trilha = de.buscar_trilha("java", self.json_path)
        self.assertEqual(trilha["xp_total"], 15000)

    def test_trilha_java_nivel_avancado(self):
        trilha = de.buscar_trilha("java", self.json_path)
        self.assertEqual(trilha["nivel"], "Avançado")

    def test_trilha_java_vitalicio_true(self):
        trilha = de.buscar_trilha("java", self.json_path)
        self.assertTrue(trilha["vitalicio"])

    def test_trilha_java_tem_badges(self):
        trilha = de.buscar_trilha("java", self.json_path)
        self.assertGreater(len(trilha["badges"]), 0)
        self.assertIn("Java Champion", trilha["badges"])

    def test_trilha_java_promocao_ativa(self):
        trilha = de.buscar_trilha("java", self.json_path)
        self.assertTrue(trilha["promocao"]["ativa"])
        self.assertEqual(trilha["promocao"]["desconto_percentual"], 40)

    def test_trilha_java_tem_lives(self):
        trilha = de.buscar_trilha("java", self.json_path)
        self.assertEqual(len(trilha["lives_ao_vivo"]), 2)

    # --- Casos de falha ---

    def test_tecnologia_inexistente_retorna_none(self):
        resultado = de.buscar_trilha("Cobol", self.json_path)
        self.assertIsNone(resultado)

    def test_string_vazia_retorna_none(self):
        resultado = de.buscar_trilha("", self.json_path)
        self.assertIsNone(resultado)

    def test_espacos_extras_sao_ignorados(self):
        resultado = de.buscar_trilha("  java  ", self.json_path)
        self.assertIsNotNone(resultado)


# ---------------------------------------------------------------------------
# Testes: listar_tecnologias
# ---------------------------------------------------------------------------

class TestListarTecnologias(unittest.TestCase):

    def setUp(self):
        self.json_path = _criar_json_temp()

    def tearDown(self):
        os.unlink(self.json_path)

    def test_retorna_lista(self):
        resultado = de.listar_tecnologias(self.json_path)
        self.assertIsInstance(resultado, list)

    def test_quantidade_correta(self):
        resultado = de.listar_tecnologias(self.json_path)
        self.assertEqual(len(resultado), 2)

    def test_cada_item_tem_tecnologia_e_nivel(self):
        resultado = de.listar_tecnologias(self.json_path)
        for item in resultado:
            self.assertIn("tecnologia", item)
            self.assertIn("nivel", item)


# ---------------------------------------------------------------------------
# Testes: formatar_trilha
# ---------------------------------------------------------------------------

class TestFormatarTrilha(unittest.TestCase):

    def test_formatacao_java_contem_nome(self):
        texto = de.formatar_trilha(TRILHA_JAVA)
        self.assertIn("Java Spring Boot Microservices", texto)

    def test_formatacao_java_contem_tecnologia(self):
        texto = de.formatar_trilha(TRILHA_JAVA)
        self.assertIn("Java", texto)

    def test_formatacao_java_contem_xp(self):
        texto = de.formatar_trilha(TRILHA_JAVA)
        self.assertIn("15000", texto)

    def test_formatacao_java_contem_badge(self):
        texto = de.formatar_trilha(TRILHA_JAVA)
        self.assertIn("Java Champion", texto)

    def test_formatacao_java_promocao_ativa(self):
        texto = de.formatar_trilha(TRILHA_JAVA)
        self.assertIn("40%", texto)

    def test_formatacao_python_sem_promocao(self):
        texto = de.formatar_trilha(TRILHA_PYTHON)
        self.assertIn("Sem promoção ativa", texto)

    def test_formatacao_vitalicio_sim(self):
        texto = de.formatar_trilha(TRILHA_JAVA)
        self.assertIn("Sim", texto)


# ---------------------------------------------------------------------------
# Testes: normalizar_nivel  →  auxiliar do /desafio
# ---------------------------------------------------------------------------

class TestNormalizarNivel(unittest.TestCase):

    def test_basico_lower(self):
        self.assertEqual(de.normalizar_nivel("basico"), "Básico")

    def test_basico_acentuado(self):
        self.assertEqual(de.normalizar_nivel("básico"), "Básico")

    def test_intermediario(self):
        self.assertEqual(de.normalizar_nivel("intermediário"), "Intermediário")

    def test_intermediario_sem_acento(self):
        self.assertEqual(de.normalizar_nivel("intermediario"), "Intermediário")

    def test_avancado_sem_acento(self):
        self.assertEqual(de.normalizar_nivel("avancado"), "Avançado")

    def test_avancado_com_acento(self):
        self.assertEqual(de.normalizar_nivel("avançado"), "Avançado")

    def test_nivel_invalido_retorna_intermediario(self):
        self.assertEqual(de.normalizar_nivel("mestre"), "Intermediário")

    def test_string_vazia_retorna_intermediario(self):
        self.assertEqual(de.normalizar_nivel(""), "Intermediário")


# ---------------------------------------------------------------------------
# Testes: gerar_desafio  →  comando /desafio
# ---------------------------------------------------------------------------

class TestGerarDesafio(unittest.TestCase):

    def test_retorna_dict(self):
        resultado = de.gerar_desafio("Java", "Avançado")
        self.assertIsInstance(resultado, dict)

    def test_campos_obrigatorios(self):
        resultado = de.gerar_desafio("Java", "Avançado")
        for campo in ("tecnologia", "nivel", "tema", "xp", "tempo_sugerido"):
            self.assertIn(campo, resultado)

    def test_xp_avancado(self):
        resultado = de.gerar_desafio("Java", "Avançado")
        self.assertEqual(resultado["xp"], 600)

    def test_xp_basico(self):
        resultado = de.gerar_desafio("Python", "Básico")
        self.assertEqual(resultado["xp"], 150)

    def test_xp_intermediario(self):
        resultado = de.gerar_desafio("Python", "Intermediário")
        self.assertEqual(resultado["xp"], 350)

    def test_tempo_avancado(self):
        resultado = de.gerar_desafio("Java", "Avançado")
        self.assertEqual(resultado["tempo_sugerido"], "60–120 min")

    def test_tecnologia_preservada(self):
        resultado = de.gerar_desafio("Java", "Avançado")
        self.assertEqual(resultado["tecnologia"], "Java")

    def test_nivel_normalizado_avancado(self):
        resultado = de.gerar_desafio("Java", "avancado")
        self.assertEqual(resultado["nivel"], "Avançado")

    def test_nivel_invalido_gera_aviso(self):
        resultado = de.gerar_desafio("Java", "Expert")
        self.assertIsNotNone(resultado["aviso"])

    def test_tecnologia_desconhecida_gera_aviso(self):
        resultado = de.gerar_desafio("Cobol", "Básico")
        self.assertIsNotNone(resultado["aviso"])

    def test_java_tem_tema_especifico(self):
        """Tema Java deve vir da lista mapeada."""
        resultado = de.gerar_desafio("java", "Avançado")
        temas_java = de._TEMAS_POR_TECNOLOGIA["java"]
        self.assertIn(resultado["tema"], temas_java)

    def test_sem_aviso_para_parametros_validos(self):
        resultado = de.gerar_desafio("java", "Básico")
        self.assertIsNone(resultado["aviso"])


# ---------------------------------------------------------------------------
# Testes: gerar_certificado  →  comando /certificado
# ---------------------------------------------------------------------------

class TestGerarCertificado(unittest.TestCase):

    def setUp(self):
        self.json_path = _criar_json_temp()

    def tearDown(self):
        os.unlink(self.json_path)

    def test_retorna_dict(self):
        resultado = de.gerar_certificado("João Silva", "Java", self.json_path)
        self.assertIsInstance(resultado, dict)

    def test_campos_obrigatorios(self):
        resultado = de.gerar_certificado("João Silva", "Java", self.json_path)
        for campo in ("aluno", "trilha_nome", "tecnologia", "nivel", "modulos",
                      "xp_total", "badges", "codigo", "data_emissao"):
            self.assertIn(campo, resultado)

    def test_nome_aluno_correto(self):
        resultado = de.gerar_certificado("Maria Souza", "Java", self.json_path)
        self.assertEqual(resultado["aluno"], "Maria Souza")

    def test_trilha_java_xp_correto(self):
        resultado = de.gerar_certificado("João Silva", "Java", self.json_path)
        self.assertEqual(resultado["xp_total"], 15000)

    def test_trilha_java_nivel_avancado(self):
        resultado = de.gerar_certificado("João Silva", "Java", self.json_path)
        self.assertEqual(resultado["nivel"], "Avançado")

    def test_codigo_formato_correto(self):
        """Código deve seguir o padrão DIO-<id>-<ano>-XXXXXX."""
        resultado = de.gerar_certificado("João Silva", "Java", self.json_path)
        partes = resultado["codigo"].split("-")
        self.assertEqual(partes[0], "DIO")
        self.assertEqual(partes[1], "5")         # id da trilha Java
        self.assertEqual(partes[2], str(date.today().year))
        self.assertEqual(len(partes[3]), 6)

    def test_data_emissao_formato_correto(self):
        """Data de emissão deve ter formato DD/MM/YYYY."""
        resultado = de.gerar_certificado("João Silva", "Java", self.json_path)
        partes = resultado["data_emissao"].split("/")
        self.assertEqual(len(partes), 3)
        self.assertEqual(len(partes[2]), 4)       # ano com 4 dígitos

    def test_badges_java_presentes(self):
        resultado = de.gerar_certificado("João Silva", "Java", self.json_path)
        self.assertIn("Java Champion", resultado["badges"])

    def test_trilha_inexistente_sem_aviso_none(self):
        """Tecnologia não encontrada deve retornar aviso não nulo."""
        resultado = de.gerar_certificado("João Silva", "Cobol", self.json_path)
        self.assertIsNotNone(resultado["aviso"])

    def test_trilha_inexistente_xp_generico(self):
        resultado = de.gerar_certificado("João Silva", "Cobol", self.json_path)
        self.assertEqual(resultado["xp_total"], 5000)

    def test_trilha_encontrada_aviso_none(self):
        resultado = de.gerar_certificado("João Silva", "Java", self.json_path)
        self.assertIsNone(resultado["aviso"])

    def test_case_insensitive_java_minusculo(self):
        resultado = de.gerar_certificado("Ana", "java", self.json_path)
        self.assertEqual(resultado["tecnologia"], "Java")

    def test_certificado_python(self):
        resultado = de.gerar_certificado("Carlos", "Python", self.json_path)
        self.assertEqual(resultado["nivel"], "Básico")
        self.assertEqual(resultado["xp_total"], 4500)


# ---------------------------------------------------------------------------
# Testes de integração leve: /trilha → /desafio → /certificado (fluxo completo)
# ---------------------------------------------------------------------------

class TestFluxoCompleto(unittest.TestCase):
    """Simula o fluxo: consultar trilha Java → gerar desafio → gerar certificado."""

    def setUp(self):
        self.json_path = _criar_json_temp()
        self.trilha = de.buscar_trilha("Java", self.json_path)

    def tearDown(self):
        os.unlink(self.json_path)

    def test_fluxo_trilha_existe(self):
        self.assertIsNotNone(self.trilha)

    def test_fluxo_desafio_nivel_da_trilha(self):
        nivel = self.trilha["nivel"]
        desafio = de.gerar_desafio("Java", nivel)
        self.assertEqual(desafio["nivel"], "Avançado")

    def test_fluxo_certificado_com_dados_da_trilha(self):
        cert = de.gerar_certificado("Aluno Teste", "Java", self.json_path)
        self.assertEqual(cert["trilha_nome"], self.trilha["nome"])
        self.assertEqual(cert["xp_total"], self.trilha["xp_total"])

    def test_fluxo_codigo_certificado_unico(self):
        cert1 = de.gerar_certificado("Aluno A", "Java", self.json_path)
        cert2 = de.gerar_certificado("Aluno B", "Java", self.json_path)
        # sufixo aleatório → probabilidade de colisão ≈ 0
        self.assertNotEqual(cert1["codigo"], cert2["codigo"])


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
