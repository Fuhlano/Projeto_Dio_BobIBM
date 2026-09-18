# Arquitetura do Projeto DioBobIBM

## Visão Geral

O projeto é composto por quatro camadas independentes que se comunicam de forma clara e desacoplada:

```
┌─────────────────────────────────────────────────────────────────┐
│                        IBM BOB (Agente IA)                       │
└──────────────┬──────────────────────────────────────────────────┘
               │ usa
   ┌───────────┼────────────────────────────┐
   │           │                            │
   ▼           ▼                            ▼
┌──────────┐ ┌──────────────┐ ┌─────────────────────────────────┐
│ Commands │ │    Skills    │ │   MCP Server (dio-explorer-mcp) │
│          │ │              │ │   TypeScript · stdio transport  │
│/trilha   │ │trilha SKILL  │ │                                 │
│/desafio  │ │certificado   │ │   dio_listar_trilhas            │
│/certific.│ │  SKILL       │ │   dio_buscar_trilha             │
└────┬─────┘ └──────┬───────┘ │   dio_gerar_desafio             │
     │              │         │   dio_gerar_certificado         │
     │              │         └──────────────┬──────────────────┘
     └──────────────┴──────────────────────┐ │
                                           ▼ ▼
                               ┌──────────────────────────────┐
                               │  Python Core (dio_explorer.py)│
                               │  carregar_trilhas()           │
                               │  buscar_trilha()              │
                               │  gerar_desafio()              │
                               │  gerar_certificado()          │
                               └──────────────┬───────────────┘
                                              │ lê
                               ┌──────────────────────────────┐
                               │  trilhas_dio.json             │
                               │  10 trilhas · badges          │
                               │  lives · promoções            │
                               └──────────────────────────────┘
```

---

## Camada 1 — Base de Dados

**Arquivo:** `dio_explorer/data/trilhas_dio.json`

JSON estático com 10 trilhas DIO fictícias. Serve como fonte de dados para todas as camadas superiores.

### Schema de uma trilha

```json
{
  "id": 5,
  "nome": "Java Spring Boot Microservices",
  "tecnologia": "Java",
  "nivel": "Avançado",
  "modulos": 18,
  "xp_total": 15000,
  "badges": ["Java Champion", "Spring Expert", "Microservices Architect", "API Designer"],
  "promocao": {
    "ativa": true,
    "desconto_percentual": 40,
    "validade": "2025-07-31"
  },
  "vitalicio": true,
  "lives_ao_vivo": [
    { "titulo": "Spring Boot com Docker", "data": "2025-07-12", "duracao_min": 120 }
  ]
}
```

### Trilhas cadastradas

| ID | Tecnologia | Nível | Módulos | XP |
|----|-----------|-------|---------|-----|
| 1 | Python | Básico | 8 | 4.500 |
| 2 | React | Intermediário | 14 | 9.800 |
| 3 | DevOps | Avançado | 12 | 11.200 |
| 4 | Machine Learning | Intermediário | 16 | 13.500 |
| 5 | Java | Avançado | 18 | 15.000 |
| 6 | AWS | Básico | 10 | 6.200 |
| 7 | Flutter | Intermediário | 13 | 10.500 |
| 8 | CyberSecurity | Avançado | 20 | 18.000 |
| 9 | PostgreSQL | Intermediário | 11 | 7.800 |
| 10 | Node.js | Intermediário | 12 | 9.200 |

---

## Camada 2 — Python Core

**Arquivo:** `dio_explorer/src/dio_explorer.py`

Módulo Python puro com toda a lógica de negócio. Sem dependências externas, sem acoplamento ao agente de IA.

### Funções públicas

| Função | Assinatura | Descrição |
|--------|-----------|-----------|
| `carregar_trilhas` | `(caminho?) → dict` | Carrega o JSON do disco |
| `buscar_trilha` | `(tecnologia, caminho?) → dict\|None` | Busca case-insensitive, retorna `None` se não encontrar |
| `listar_tecnologias` | `(caminho?) → list[dict]` | Retorna `[{tecnologia, nivel}, ...]` |
| `formatar_trilha` | `(trilha) → str` | Formata dados em markdown |
| `normalizar_nivel` | `(nivel) → str` | Normaliza `avancado` → `Avançado`, fallback `Intermediário` |
| `gerar_desafio` | `(tecnologia, nivel) → dict` | Sorteia tema, retorna XP e tempo sugerido |
| `gerar_certificado` | `(nome, tecnologia, caminho?) → dict` | Emite certificado com código `DIO-{id}-{ano}-XXXXXX` |

### Resolução de caminho

O módulo resolve o path do JSON relativo à sua própria localização:

```python
_BASE_DIR = Path(__file__).resolve().parent.parent  # → dio_explorer/
_DATA_PATH = _BASE_DIR / "data" / "trilhas_dio.json"
```

Isso garante que o módulo funciona independentemente de onde `pytest` ou o servidor MCP é chamado.

### Temas de desafio mapeados

```python
_TEMAS_POR_TECNOLOGIA = {
    "java":   ["Calculadora de Impostos com OOP", "Sistema de Filas com BlockingQueue", ...],
    "python": ["Análise de CSV com pandas", "Web scraper simples com requests", ...],
    "default": ["Algoritmo de busca binária", "Implementação de pilha e fila", ...],
}
```

Tecnologias não mapeadas usam `default` e o Bob recebe um aviso no campo `aviso` do retorno.

---

## Camada 3a — Commands Bob

**Pasta:** `.bob/commands/`

Commands são arquivos `.md` com frontmatter YAML acionados pelo usuário via `/nome argumento`.

### Estrutura de um command

```markdown
---
description: Descrição curta exibida ao usuário
argument-hint: <arg1> <arg2>
---

Conteúdo do prompt com $1, $2 como placeholders para os argumentos.
```

### Mapeamento argumento → prompt

| Placeholder | Corresponde a |
|-------------|--------------|
| `$1` | Primeiro argumento após o nome do command |
| `$2` | Segundo argumento |

Exemplo: `/certificado "Ana Lima" Python` → `$1 = "Ana Lima"`, `$2 = Python`

---

## Camada 3b — Skills Bob

**Pasta:** `.bob/skills/<nome>/SKILL.md`

Skills são fragmentos de instrução reutilizáveis. Podem ser ativadas por outros artefatos via `use_skill`.

### Estrutura de uma skill

```yaml
---
name: nome-da-skill
description: >-
  Descrição para o Bob entender quando usar esta skill
metadata:
  user-invocable: true
  disable-model-invocation: true
  argument-hint: <arg1> <arg2>
---

Conteúdo da instrução...
```

### Diferença entre Command e Skill

| | Command | Skill |
|---|---------|-------|
| Ativação | Usuário digita `/comando` | Código chama `use_skill "nome"` |
| Visibilidade | Listado no menu de commands | Interno ao Bob |
| Reutilização | Por chamada direta | Por referência em outros artefatos |

---

## Camada 3c — Servidor MCP

**Pasta:** `dio_explorer/mcp/`

Servidor TypeScript que expõe as funcionalidades como ferramentas consumíveis pelo Bob durante raciocínio — sem precisar de instrução explícita do usuário.

### Stack

| Dependência | Versão | Papel |
|-------------|--------|-------|
| `@modelcontextprotocol/sdk` | ^1.12.0 | Framework MCP (transport, server, tools) |
| `zod` | ^3.24.0 | Validação e schema das tools |
| `typescript` | ^5.6.0 | Compilação |
| `@types/node` | ^22.0.0 | Tipos Node.js |

### Ferramentas registradas

```typescript
server.registerTool("dio_listar_trilhas", {
  description: "...",
  inputSchema: z.object({})          // sem parâmetros
}, async () => { ... });

server.registerTool("dio_buscar_trilha", {
  inputSchema: z.object({
    tecnologia: z.string().describe("Nome da tecnologia (ex: Python, Java)")
  })
}, async ({ tecnologia }) => { ... });

server.registerTool("dio_gerar_desafio", {
  inputSchema: z.object({
    tecnologia: z.string(),
    nivel: z.string().describe("Básico, Intermediário ou Avançado")
  })
}, async ({ tecnologia, nivel }) => { ... });

server.registerTool("dio_gerar_certificado", {
  inputSchema: z.object({
    nome_aluno: z.string(),
    tecnologia: z.string()
  })
}, async ({ nome_aluno, tecnologia }) => { ... });
```

### Transporte stdio

```
Bob (processo pai)
    │  stdin  →  JSON-RPC request
    │  stdout ←  JSON-RPC response
    ▼
node build/index.js (processo filho)
```

O Bob gerencia o ciclo de vida do processo filho automaticamente a partir do `mcp.json`.

### Build

```bash
cd dio_explorer/mcp
npm install
npm run build   # tsc → build/index.js
```

### Registro

```json
// .bob/mcp.json
{
  "mcpServers": {
    "dio-explorer-mcp": {
      "command": "node",
      "args": ["<caminho-absoluto>/dio_explorer/mcp/build/index.js"]
    }
  }
}
```

---

## Testes

**Arquivos:** `dio_explorer/src/test_dio_explorer.py`, `dio_explorer/src/run_tests.py`

### Resultado

| Métrica | Valor |
|---------|-------|
| Total de testes | 66 |
| Aprovados | 66 ✅ |
| Reprovados | 0 |
| Cobertura de linhas | 100% |
| Statements cobertos | 61 / 61 |

### Classes de teste

| Classe | Testes | O que cobre |
|--------|--------|-------------|
| `TestCarregarTrilhas` | 4 | Carregamento JSON, arquivo inexistente |
| `TestBuscarTrilha` | 15 | Case-insensitive, espaços extras, campos validados |
| `TestListarTecnologias` | 3 | Lista e estrutura de retorno |
| `TestFormatarTrilha` | 7 | Saída de texto, promoção, vitalício |
| `TestNormalizarNivel` | 8 | Acentos, maiúsculas, fallback Intermediário |
| `TestGerarDesafio` | 12 | XP por nível, temas mapeados, avisos |
| `TestGerarCertificado` | 13 | Formato do código, data, badges, fallback genérico |
| `TestFluxoCompleto` | 4 | Integração /trilha → /desafio → /certificado |

### Executar

```bash
# Com cobertura
python -m pytest dio_explorer/src/test_dio_explorer.py -v \
  --cov=dio_explorer/src/dio_explorer \
  --cov-report=term-missing

# Somente os testes
python -m pytest dio_explorer/src/test_dio_explorer.py -v
```

---

## Fluxo de dados — exemplo completo

```
Usuário: /certificado "Ana Lima" Python
              │
              ▼
         Command .bob/commands/certificado.md
         ($1="Ana Lima", $2="Python")
              │
              ▼ Bob lê o arquivo de dados
         trilhas_dio.json
         {"id":1, "nome":"Fundamentos de Python...", "nivel":"Básico", ...}
              │
              ▼ Bob gera código único
         DIO-1-2025-K7XR2M
              │
              ▼
         Certificado markdown completo renderizado no chat
```

---

## Considerações de segurança e produção

| Aspecto | Desenvolvimento (atual) | Produção (recomendado) |
|---------|------------------------|----------------------|
| Transporte MCP | stdio (local) | StreamableHTTPServerTransport + JWT |
| Dados | JSON estático | Banco de dados (Appwrite, PostgreSQL) |
| Caminho no mcp.json | Absoluto hardcoded | Variável de ambiente |
| Cache de dados | Sem cache (lê a cada chamada) | Memoização ou TTL cache |
| Autenticação | Nenhuma (local) | Bearer token / SSO |
