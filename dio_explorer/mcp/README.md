# DIO Explorer — MCP Server

Servidor MCP que expõe as funcionalidades do **DIO Explorer** como ferramentas consumíveis por agentes de IA (como IBM Bob).

## Ferramentas disponíveis

| Tool | Descrição |
|------|-----------|
| `dio_listar_trilhas` | Lista todas as trilhas cadastradas com tecnologia, nível, XP e promoção |
| `dio_buscar_trilha` | Retorna detalhes completos de uma trilha por tecnologia |
| `dio_gerar_desafio` | Gera um desafio de código para tecnologia e nível informados |
| `dio_gerar_certificado` | Emite um certificado de conclusão fictício para um aluno |

---

## Requisitos

- **Node.js** ≥ 18
- **npm** ≥ 9

---

## Instalação e build

```bash
cd dio_explorer/mcp
npm install
npm run build
```

---

## Executar localmente (stdio)

```bash
node build/index.js
```

O servidor se comunica via **stdio** — ele é gerenciado automaticamente pelo Bob/MCP client ao ser registrado em `mcp.json`.

---

## Registro no Bob (mcp.json)

Após o build, o servidor já está registrado em `.bob/mcp.json`.  
Para registrar manualmente em outro ambiente, adicione:

```json
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

## Acesso remoto (HTTPS / SSO / API)

Para expor este servidor via HTTPS, SSO ou uma API REST, existem dois caminhos:

### Opção A — HTTP Gateway com Express

Crie um wrapper HTTP que recebe requisições REST e repassa ao servidor MCP via stdio.  
Use autenticação JWT/Bearer (SSO) no middleware Express.

### Opção B — MCP StreamableHTTP Transport

O SDK MCP suporta transporte HTTP nativo:

```typescript
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express from "express";

const app = express();
// Adicione middleware de autenticação SSO/JWT aqui
app.use(bearerTokenMiddleware);
app.post("/mcp", async (req, res) => {
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});
app.listen(3000);
```

### Variáveis de ambiente para autenticação

| Variável | Descrição |
|----------|-----------|
| `MCP_API_KEY` | Chave de API para autenticação Bearer |
| `MCP_JWT_SECRET` | Secret para validação de tokens JWT/SSO |
| `PORT` | Porta HTTP (padrão: 3000) |

---

## Estrutura de pastas

```
dio_explorer/mcp/
├── src/
│   └── index.ts        ← Implementação principal
├── build/              ← Gerado pelo tsc (não versionar)
│   └── index.js
├── package.json
├── tsconfig.json
└── README.md
```
