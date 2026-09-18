# DioBobIBM — DIO Explorer

Projeto educacional que integra o **IBM Bob** com a plataforma **DIO**, demonstrando na prática como criar comandos customizados, skills reutilizáveis e um servidor MCP completo em TypeScript — tudo com testes automatizados e 100% de cobertura.

## Estrutura do Projeto

```
DioBobIBM/
├── .bob/
│   ├── mcp.json                  ← Registro do servidor MCP
│   ├── commands/
│   │   ├── trilha.md             ← Comando /trilha
│   │   ├── desafio.md            ← Comando /desafio
│   │   └── certificado.md        ← Comando /certificado
│   └── skills/
│       ├── trilha/SKILL.md       ← Skill reutilizável: trilha
│       └── certificado/SKILL.md  ← Skill reutilizável: certificado
│
├── dio_explorer/
│   ├── src/
│   │   ├── dio_explorer.py       ← Módulo Python (lógica central)
│   │   ├── test_dio_explorer.py  ← 66 testes unitários + integração
│   │   └── run_tests.py          ← Runner de testes + relatório
│   ├── data/
│   │   └── trilhas_dio.json      ← Base de dados: 10 trilhas DIO
│   ├── mcp/
│   │   ├── src/index.ts          ← Servidor MCP em TypeScript
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── README.md             ← Documentação do servidor MCP
│   └── docs/
│       ├── ARCHITECTURE.md       ← Arquitetura detalhada
│       └── resultado_testes.txt  ← Relatório de testes gerado pelo Bob
│
├── DOCS.md                       ← Guia completo: prompts, dicas e insights
└── README.md                     ← Este arquivo
```

## Início Rápido

### 1. Pré-requisitos

- **IBM Bob** instalado e configurado
- **Python ≥ 3.12** com `pytest` e `pytest-cov`
- **Node.js ≥ 18** e **npm ≥ 9**

### 2. Build do servidor MCP

```bash
cd dio_explorer/mcp
npm install
npm run build
```

O servidor já está registrado em `.bob/mcp.json`. Reinicie o Bob para ativá-lo.

### 3. Executar os testes Python

```bash
python -m pytest dio_explorer/src/test_dio_explorer.py -v \
  --cov=dio_explorer/src/dio_explorer \
  --cov-report=term-missing
```

Resultado esperado: **66/66 ✅ · 100% de cobertura**.

## Comandos Disponíveis

| Comando | Uso | Descrição |
|---------|-----|-----------|
| `/trilha` | `/trilha Python` | Exibe o plano de estudos completo da trilha |
| `/desafio` | `/desafio Java Avançado` | Gera um desafio de código aleatório |
| `/certificado` | `/certificado "Seu Nome" Python` | Emite certificado fictício de conclusão |

## Ferramentas MCP Disponíveis

Após o build, o Bob usa automaticamente:

| Tool | Descrição |
|------|-----------|
| `dio_listar_trilhas` | Lista todas as trilhas com tecnologia, nível e XP |
| `dio_buscar_trilha` | Retorna detalhes completos de uma trilha |
| `dio_gerar_desafio` | Gera desafio com tema, XP e tempo sugerido |
| `dio_gerar_certificado` | Emite certificado com código único `DIO-{id}-{ano}-XXXXXX` |

## Trilhas Cadastradas

Python · React · DevOps · Machine Learning · Java · AWS · Flutter · CyberSecurity · PostgreSQL · Node.js

## Documentação Completa

- **[DOCS.md](./DOCS.md)** — Guia completo com todos os prompts usados, modos de uso, dicas e insights para profissionais
- **[dio_explorer/docs/ARCHITECTURE.md](./dio_explorer/docs/ARCHITECTURE.md)** — Arquitetura detalhada do sistema
- **[dio_explorer/mcp/README.md](./dio_explorer/mcp/README.md)** — Documentação do servidor MCP

## Resultados de Testes

```
Total de testes  : 66
✅ Aprovados      : 66
❌ Reprovados     : 0
% de aprovação   : 100%
Cobertura (lines): 100%  (61 statements, 0 missed)
```

---

*Projeto desenvolvido em parceria DIO × IBM Bob*
