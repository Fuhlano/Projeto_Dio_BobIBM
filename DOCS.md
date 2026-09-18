# DOCS — Guia Completo do Projeto DioBobIBM

Este documento reúne todos os prompts utilizados durante a construção do projeto, os modos de uso do IBM Bob, dicas práticas e insights para profissionais que vão aprender com este material.

---

## Índice

1. [O que foi construído](#1-o-que-foi-construído)
2. [Prompts utilizados](#2-prompts-utilizados)
3. [Modos do Bob e quando usá-los](#3-modos-do-bob-e-quando-usá-los)
4. [Modos de uso dos comandos](#4-modos-de-uso-dos-comandos)
5. [Dicas de uso](#5-dicas-de-uso)
6. [Insights para profissionais](#6-insights-para-profissionais)
7. [Próximos passos sugeridos](#7-próximos-passos-sugeridos)

---

## 1. O que foi construído

O projeto criou três camadas de extensão do IBM Bob integradas à plataforma DIO:

| Camada | O que é | Onde fica |
|--------|---------|-----------|
| **Commands** | Comandos `/trilha`, `/desafio`, `/certificado` ativados pelo usuário | `.bob/commands/` |
| **Skills** | Fragmentos de instrução reutilizáveis por outros artefatos | `.bob/skills/` |
| **MCP Server** | Servidor TypeScript que expõe 4 ferramentas ao agente | `dio_explorer/mcp/` |
| **Core Python** | Lógica central testável e independente do agente | `dio_explorer/src/` |
| **Base de dados** | JSON com 10 trilhas DIO fictícias e estrutura rica | `dio_explorer/data/` |

---

## 2. Prompts Utilizados

Todos os prompts dados ao Bob durante a construção do projeto, em ordem cronológica.

### Fase 1 — Base de dados JSON

> **Prompt:**
> Crie um arquivo JSON com trilhas fictícias da DIO contendo: id, nome, tecnologia, nível (Básico/Intermediário/Avançado), módulos, XP total, badges, promoção (com desconto percentual e validade), vitalício e lives ao vivo — com pelo menos 10 trilhas variadas cobrindo tecnologias populares como Python, Java, React, DevOps, Machine Learning, AWS, Flutter, CyberSecurity, PostgreSQL e Node.js. Salve em `dio_explorer/data/trilhas_dio.json`.

**Resultado:** [`dio_explorer/data/trilhas_dio.json`](./dio_explorer/data/trilhas_dio.json) com 10 trilhas, metadata e schema consistente.

---

### Fase 2 — Módulo Python central

> **Prompt:**
> Crie um módulo Python `dio_explorer.py` em `dio_explorer/src/` com as seguintes funções:
> - `carregar_trilhas(caminho)` — carrega o JSON do disco
> - `buscar_trilha(tecnologia, caminho)` — busca case-insensitive, retorna `None` se não encontrar
> - `listar_tecnologias(caminho)` — retorna lista de `{tecnologia, nivel}`
> - `formatar_trilha(trilha)` — formata dados em texto markdown
> - `normalizar_nivel(nivel)` — normaliza com/sem acento para Básico/Intermediário/Avançado
> - `gerar_desafio(tecnologia, nivel)` — retorna dict com tema sorteado aleatoriamente, XP e tempo sugerido
> - `gerar_certificado(nome_aluno, tecnologia, caminho)` — emite certificado com código único `DIO-{id}-{ano}-XXXXXX`
>
> O caminho do JSON deve ser resolvido com `Path(__file__)` para funcionar independente de onde o script é chamado.

**Resultado:** [`dio_explorer/src/dio_explorer.py`](./dio_explorer/src/dio_explorer.py) com 61 statements.

---

### Fase 3 — Testes unitários e de integração

> **Prompt:**
> Crie testes unitários com pytest para todas as funções do `dio_explorer.py` com cobertura mínima de 70%. Requisitos:
> - Use arquivos JSON temporários (`tempfile.NamedTemporaryFile`) nos testes — não use o JSON real
> - Limpe os arquivos temporários em `tearDown`
> - Cubra: casos de sucesso, casos de falha (tecnologia inexistente, string vazia), edge cases (espaços extras, maiúsculas/minúsculas, acentos)
> - Inclua uma classe `TestFluxoCompleto` simulando o fluxo `/trilha → /desafio → /certificado`
> - Ao final, salve um relatório completo em `dio_explorer/docs/resultado_testes.txt`

**Resultado:** [`dio_explorer/src/test_dio_explorer.py`](./dio_explorer/src/test_dio_explorer.py) com 66 testes, 100% de cobertura.

---

### Fase 4 — Commands do Bob

> **Prompt:**
> Crie três commands Bob em `.bob/commands/` com frontmatter YAML (`description`, `argument-hint`):
>
> **`/trilha <tecnologia>`**: leia `dio_explorer/data/trilhas_dio.json`, encontre a trilha pela tecnologia (case-insensitive) e exiba: tabela de detalhes, plano de estudos com módulos e duração estimada, badges, lives ao vivo e status de promoção. Se não encontrar, liste todas as tecnologias disponíveis.
>
> **`/desafio <tecnologia> <nivel>`**: gere um desafio único com enunciado de problema real, entrada/saída, 2-3 exemplos de teste, critérios de avaliação, dica sutil, tempo sugerido e XP (Básico=150 · Intermediário=350 · Avançado=600). Varie o tema a cada invocação.
>
> **`/certificado <nome> <tecnologia>`**: emita um certificado markdown completo com banner ASCII, competências, badges, XP, código `DIO-{id}-{ano}-XXXXXX`, data de emissão e mensagem motivacional personalizada.

**Resultado:** `.bob/commands/trilha.md`, `.bob/commands/desafio.md`, `.bob/commands/certificado.md`

---

### Fase 5 — Skills reutilizáveis

> **Prompt:**
> Crie skills Bob para `trilha` e `certificado` em `.bob/skills/<nome>/SKILL.md`. O frontmatter YAML deve conter os campos: `name`, `description`, `metadata.user-invocable: true`, `metadata.disable-model-invocation: true` e `metadata.argument-hint`. O conteúdo das skills deve ser idêntico ao dos commands correspondentes, pois o objetivo é demonstrar as duas formas de extensão do Bob lado a lado.

**Resultado:** `.bob/skills/trilha/SKILL.md` e `.bob/skills/certificado/SKILL.md`

---

### Fase 6 — Servidor MCP em TypeScript

> **Prompt:**
> Crie um servidor MCP em TypeScript em `dio_explorer/mcp/src/index.ts` usando `@modelcontextprotocol/sdk` e `zod`. O servidor deve:
> - Registrar 4 tools: `dio_listar_trilhas`, `dio_buscar_trilha`, `dio_gerar_desafio`, `dio_gerar_certificado`
> - Ler o mesmo `trilhas_dio.json` resolvendo o path relativo ao `build/index.js`
> - Usar transporte stdio (local, sem porta de rede)
> - Ter `package.json` com `"type": "module"`, scripts `build` (tsc) e `start`
> - Ter `tsconfig.json` com `target: ES2022`, `module: Node16`, `strict: true`
> - Registrar-se automaticamente em `.bob/mcp.json` após o build
> - Incluir `README.md` com instruções de build, registro e opções de acesso remoto via HTTP

**Resultado:** `dio_explorer/mcp/src/index.ts`, `package.json`, `tsconfig.json`, `build/index.js`, `.bob/mcp.json`, `dio_explorer/mcp/README.md`

---

### Fase 7 — Documentação do projeto

> **Prompt:**
> Gostaria que você documentasse todo o projeto feito até o momento, com todos os prompts usados, modos de uso, dicas de uso e insights para futuros profissionais que vão aprender com nosso projeto.

> **Prompt (refinamento):**
> A documentação deveria estar nos arquivos do projeto.

**Resultado:** `README.md`, `DOCS.md` (este arquivo), `dio_explorer/docs/ARCHITECTURE.md`

---

## 3. Modos do Bob e quando usá-los

O Bob possui três modos principais. Neste projeto, cada um foi usado em momentos distintos:

### Agent (modo padrão)
**Quando usar:** sempre que precisar criar ou modificar arquivos.

Usado para: criar o JSON, o módulo Python, os testes, os commands, as skills, o servidor MCP TypeScript e toda a documentação. É o modo com acesso completo a ferramentas de escrita, execução de código e leitura de arquivos.

```
# Exemplo de tarefa Agent
"Crie o arquivo dio_explorer.py com as funções de busca e certificado"
"Execute os testes e mostre o relatório de cobertura"
```

### Plan
**Quando usar:** antes de implementar algo complexo — para pensar na arquitetura sem mexer em arquivos ainda.

Usado para: discutir a estrutura de pastas antes de criar, planejar o schema do JSON, decidir entre Command vs Skill vs MCP Tool antes de escrever código.

```
# Exemplo de tarefa Plan
"Como devo estruturar as pastas para ter tanto commands quanto um servidor MCP?"
"Qual a diferença entre usar uma skill e um command para este caso?"
```

### Ask
**Quando usar:** perguntas técnicas e conceituais sobre o Bob, MCP ou tecnologias — sem modificar arquivos.

Usado para: entender o protocolo MCP, diferença entre transporte stdio e HTTP, frontmatter de skills, como o Bob resolve `$1` e `$2` nos prompts.

```
# Exemplo de tarefa Ask
"O que é o campo disable-model-invocation no frontmatter de uma skill?"
"Como o servidor MCP se comunica com o Bob via stdio?"
```

---

## 4. Modos de uso dos comandos

### /trilha — Consultar plano de estudos

```
/trilha Python
/trilha java
/trilha REACT
/trilha "Node.js"
```

**O que acontece:**
1. Bob lê `trilhas_dio.json` e encontra a trilha pela tecnologia (case-insensitive)
2. Exibe tabela de detalhes (nível, módulos, XP, vitalício)
3. Gera plano de estudos com módulos numerados e tempo estimado
4. Lista badges a conquistar
5. Mostra agenda de lives ao vivo
6. Informa se há promoção ativa

**Fallback:** se a tecnologia não existir, lista todas as disponíveis em tabela por nível.

---

### /desafio — Praticar com código

```
/desafio Python Básico
/desafio Java Avançado
/desafio React Intermediário
/desafio AWS avancado
```

**O que acontece:**
1. Normaliza o nível (com ou sem acento, maiúsculas/minúsculas)
2. Sorteia um tema diferente a cada invocação
3. Gera enunciado completo com contexto de problema real
4. Inclui exemplos de entrada/saída e critérios de avaliação
5. Mostra XP estimada e tempo sugerido

**Níveis válidos:** `Básico` (150 XP · 15–30 min) · `Intermediário` (350 XP · 30–60 min) · `Avançado` (600 XP · 60–120 min)

---

### /certificado — Emitir certificado de conclusão

```
/certificado "Ana Lima" Python
/certificado "João Silva" Java
/certificado "Carlos Souza" react
```

**O que acontece:**
1. Busca a trilha no JSON pela tecnologia
2. Gera código único no formato `DIO-{id}-{ano}-XXXXXX`
3. Emite certificado completo em markdown com:
   - Banner ASCII DIO
   - Competências desenvolvidas
   - Lista de badges conquistados
   - XP total acumulado
   - Tabela de informações com data de emissão
   - Mensagem motivacional personalizada

**Fallback:** tecnologia não cadastrada → certificado genérico com XP=5000, aviso ao usuário.

---

## 5. Dicas de Uso

### Para usuários finais

- **Case-insensitive em tudo:** `python`, `Python`, `PYTHON` — todos funcionam igual em qualquer comando.
- **Repita o `/desafio`:** cada chamada sorteia um tema diferente — use para praticar múltiplos ângulos da mesma tecnologia.
- **Fluxo recomendado:** consulte `/trilha` primeiro para conhecer os badges, depois faça os desafios e por fim emita o `/certificado`.
- **Tecnologia com espaço:** use aspas — `/trilha "Node.js"` ou `/trilha "Machine Learning"`.
- **Nível sem acento aceito:** `/desafio Java avancado` funciona igual a `/desafio Java Avançado`.

### Para desenvolvedores que vão estender

- **Adicionar nova trilha:** insira um objeto no array `trilhas` de [`dio_explorer/data/trilhas_dio.json`](./dio_explorer/data/trilhas_dio.json). Nenhum código precisa mudar.
- **Adicionar temas de desafio:** edite `_TEMAS_POR_TECNOLOGIA` em [`dio_explorer/src/dio_explorer.py`](./dio_explorer/src/dio_explorer.py) e o espelho `TEMAS_POR_TECNOLOGIA` em [`dio_explorer/mcp/src/index.ts`](./dio_explorer/mcp/src/index.ts).
- **Novo command Bob:** crie `<nome>.md` em `.bob/commands/` com frontmatter `description` e `argument-hint` — o Bob o reconhece automaticamente.
- **Nova ferramenta MCP:** adicione `server.registerTool(...)` no `index.ts`, rode `npm run build` e reinicie o Bob.
- **Manter cobertura:** toda nova função em `dio_explorer.py` deve ter testes correspondentes em `test_dio_explorer.py`.

### Sobre o servidor MCP

- O caminho em `.bob/mcp.json` é **absoluto** — ao clonar em outro ambiente, atualize o path do `build/index.js`.
- Para testar o servidor manualmente antes de registrá-lo: `node dio_explorer/mcp/build/index.js` — ele ficará aguardando input no stdin.
- O servidor carrega o JSON a cada chamada de tool (sem cache) — em produção, considere memoizar `carregarTrilhas()`.

---

## 6. Insights para Profissionais

### Sobre desenvolvimento com agentes de IA

**Prompts como código**
Cada command e skill é essencialmente um programa de instrução. A qualidade do output do Bob é diretamente proporcional à precisão das instruções. Trate prompts com o mesmo rigor que código: versione, revise e teste iterativamente.

**Estrutura de frontmatter importa**
O campo `argument-hint` no frontmatter de skills e commands não é decorativo — ele é exibido ao usuário como dica de preenchimento. Sempre documente os argumentos esperados.

**Fallback explícito > falha silenciosa**
Todo command deste projeto tem um comportamento de fallback explícito (tecnologia não encontrada → lista disponíveis, nível inválido → usa padrão + avisa). Defina o comportamento de erro no prompt, não deixe o modelo improvisar.

---

### Sobre commands vs skills vs MCP tools

| | Command | Skill | MCP Tool |
|---|---------|-------|----------|
| **Quem aciona** | Usuário (via `/`) | Bob internamente | Bob automaticamente |
| **Como ativar** | `/nome arg1 arg2` | `use_skill "nome"` | Bob decide sozinho |
| **Quando usar** | Fluxo iniciado pelo usuário | Reutilização em outros artefatos | Quando o Bob precisa de dados durante raciocínio |
| **Depende de prompt** | Sim | Sim | Não — é código real |

Para este projeto, Commands e Skills têm o mesmo conteúdo — isso é proposital para demonstrar as duas formas de extensão lado a lado.

---

### Sobre o protocolo MCP

**stdio é simples e seguro**
O transporte stdio não abre nenhuma porta de rede. O Bob lança o servidor como processo filho e se comunica via stdin/stdout. Ideal para desenvolvimento local e projetos educacionais.

**Schema com Zod = contrato formal**
Ao definir `inputSchema` com Zod, o modelo de IA recebe o JSON Schema automaticamente e sabe exatamente o que passar para cada tool — sem ambiguidade. É o equivalente a escrever uma interface TypeScript para o modelo entender.

**Para produção: StreamableHTTPServerTransport**
Quando precisar de múltiplos usuários simultâneos ou acesso remoto, troque para HTTP:

```typescript
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";

app.post("/mcp", async (req, res) => {
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});
```

---

### Sobre testes e qualidade

**Arquivos temporários garantem isolamento**
Nunca use os dados reais de produção nos testes. Crie fixtures com `tempfile.NamedTemporaryFile`, escreva o JSON de teste mínimo e destrua o arquivo em `tearDown`. Testes que dependem de arquivos reais são frágeis.

**Cobertura 100% é possível com módulos focados**
Atingir 100% aqui foi viável porque o módulo tem responsabilidade única e lógica clara. Em projetos maiores, foque nos caminhos críticos: tratamento de erros, fallbacks e edge cases valem mais do que linhas simples.

**`Path(__file__)` resolve o problema de working directory**
```python
_BASE_DIR = Path(__file__).resolve().parent.parent
_DATA_PATH = _BASE_DIR / "data" / "trilhas_dio.json"
```
Este padrão garante que o módulo encontre seus arquivos independentemente de onde `pytest` é executado — fundamental para CI/CD.

---

### Sobre arquitetura de dados

**JSON como banco educacional**
JSON estático é perfeito para projetos educacionais: sem configuração, sem infraestrutura, portável, versionável com git. Para produção, migre para um banco real (Appwrite, PostgreSQL) mantendo as mesmas assinaturas de função.

**Separação de camadas facilita evolução**
```
dados (JSON) → lógica (Python) → interface IA (Commands/Skills) → protocolo (MCP)
```
Cada camada pode evoluir independentemente. Trocar o JSON por Appwrite não afeta os commands. Adicionar novos commands não afeta o servidor MCP.

**Espelho Python ↔ TypeScript**
A lógica de `gerar_desafio` existe em Python (`dio_explorer.py`) e em TypeScript (`index.ts`). Em projetos reais, evite duplicação — o TypeScript poderia chamar um microserviço Python ou ambos poderiam ler de uma API comum.

---

## 7. Próximos Passos Sugeridos

| Expansão | Descrição | Complexidade |
|----------|-----------|-------------|
| Integração com Appwrite | Migrar `trilhas_dio.json` para banco Appwrite; usar o MCP do Appwrite já disponível no Bob | Baixa |
| Mais tecnologias de desafio | Adicionar bancos de temas para React, DevOps, AWS, etc. em `TEMAS_POR_TECNOLOGIA` | Baixa |
| Modo HTTP para o servidor MCP | Adicionar `StreamableHTTPServerTransport` com autenticação JWT para acesso remoto | Média |
| Command `/revisar` | Novo command que recebe a solução do desafio e gera feedback detalhado | Média |
| Histórico de progresso do aluno | Rastrear desafios resolvidos e certificados emitidos por usuário em banco de dados | Alta |
| Cache no servidor MCP | Memoizar `carregarTrilhas()` para evitar leitura de disco a cada chamada de tool | Baixa |
| Testes para o servidor MCP | Criar testes unitários TypeScript (Jest/Vitest) para as tools do `index.ts` | Média |

---

*Documentação gerada com IBM Bob — DioBobIBM · DIO × IBM*
