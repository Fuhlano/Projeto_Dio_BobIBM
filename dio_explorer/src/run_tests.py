"""
run_tests.py
------------
Executa os testes unitários com cobertura e grava os resultados em
dio_explorer/docs/resultado_testes.txt

Uso:
    python dio_explorer/src/run_tests.py
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
REPO_ROOT   = Path(__file__).resolve().parent.parent.parent  # raiz do repo
SRC_DIR     = Path(__file__).resolve().parent                 # dio_explorer/src/
DOCS_DIR    = SRC_DIR.parent / "docs"
SAIDA_TXT   = DOCS_DIR / "resultado_testes.txt"

DOCS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Cabeçalho do relatório
# ---------------------------------------------------------------------------
agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
cabecalho = f"""
╔══════════════════════════════════════════════════════════════════╗
║             RELATÓRIO DE TESTES — DIO Explorer                   ║
║             Gerado em: {agora:<41}║
╚══════════════════════════════════════════════════════════════════╝

Comandos testados: /trilha  /desafio  /certificado
Tecnologia foco  : JAVA
Aluno simulado   : João Silva
"""

print(cabecalho)

# ---------------------------------------------------------------------------
# Instala dependências se necessário (pytest, coverage)
# ---------------------------------------------------------------------------
def garantir_dependencia(pacote: str):
    try:
        __import__(pacote.replace("-", "_"))
    except ImportError:
        print(f"[INFO] Instalando {pacote}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote, "-q"])

garantir_dependencia("pytest")
garantir_dependencia("pytest-cov")

# ---------------------------------------------------------------------------
# Executa pytest com cobertura
# ---------------------------------------------------------------------------
cmd = [
    sys.executable, "-m", "pytest",
    str(SRC_DIR / "test_dio_explorer.py"),
    "-v",
    "--tb=short",
    f"--cov={SRC_DIR}",
    "--cov-report=term-missing",
    "--no-header",
]

print("[INFO] Executando testes...\n")
resultado = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    cwd=str(SRC_DIR),
    encoding="utf-8",
    errors="replace",
)

saida_completa = resultado.stdout + resultado.stderr

# ---------------------------------------------------------------------------
# Parse simples: extrai resumo da linha "N passed / N failed / coverage X%"
# ---------------------------------------------------------------------------
linhas = saida_completa.splitlines()

passou     = sum(1 for l in linhas if " PASSED" in l)
falhou     = sum(1 for l in linhas if " FAILED" in l or " ERROR" in l)
total      = passou + falhou
pct_aprovacao = (passou / total * 100) if total > 0 else 0.0

# Linha de cobertura: "TOTAL   xxx   yyy   ZZ%"
cobertura_pct = "N/A"
for linha in reversed(linhas):
    if linha.strip().startswith("TOTAL"):
        partes = linha.split()
        if partes:
            cobertura_pct = partes[-1]   # ex: "82%"
        break

meta_atingida = pct_aprovacao >= 70.0

# ---------------------------------------------------------------------------
# Monta relatório final
# ---------------------------------------------------------------------------
status_meta = "✅ META ATINGIDA" if meta_atingida else "❌ META NÃO ATINGIDA"

relatorio = f"""{cabecalho}
{"="*68}
RESULTADOS DOS TESTES
{"="*68}

{saida_completa}

{"="*68}
RESUMO EXECUTIVO
{"="*68}

  Total de testes  : {total}
  ✅ Aprovados      : {passou}
  ❌ Reprovados     : {falhou}
  % de aprovação   : {pct_aprovacao:.1f}%
  Cobertura (lines): {cobertura_pct}
  Meta (≥ 70%)     : {status_meta}

{"="*68}
FLUXO SIMULADO
{"="*68}

  1. /trilha Java
     → Trilha encontrada: "Java Spring Boot Microservices"
     → Nível: Avançado | Módulos: 18 | XP: 15.000
     → Badges: Java Champion, Spring Expert, Microservices Architect, API Designer
     → Promoção: 40% de desconto (válido até 2025-07-31)

  2. /desafio Java Avançado
     → Tema sorteado a partir do banco de temas Java
     → XP estimado: 600 XP | Tempo sugerido: 60–120 min

  3. /certificado João Silva Java
     → Aluno: João Silva
     → Trilha: Java Spring Boot Microservices
     → Código: DIO-5-{datetime.now().year}-[GERADO DINAMICAMENTE]
     → Data de Emissão: {datetime.now().strftime("%d/%m/%Y")}

{"="*68}
"""

# ---------------------------------------------------------------------------
# Grava no arquivo
# ---------------------------------------------------------------------------
with open(SAIDA_TXT, "w", encoding="utf-8") as f:
    f.write(relatorio)

print(f"\n{'='*68}")
print(f"  Total : {total} testes  |  Aprovados: {passou}  |  Reprovados: {falhou}")
print(f"  Aprovação : {pct_aprovacao:.1f}%   |   Cobertura: {cobertura_pct}")
print(f"  {status_meta}")
print(f"{'='*68}")
print(f"\n📄 Relatório gravado em: {SAIDA_TXT}\n")

# Retorna exit code 0 se meta atingida, 1 caso contrário
sys.exit(0 if meta_atingida else 1)
