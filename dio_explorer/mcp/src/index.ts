#!/usr/bin/env node
/**
 * DIO Explorer MCP Server
 * -----------------------
 * Exposes the DIO Explorer capabilities as MCP tools:
 *   - dio_listar_trilhas   → list all available learning paths
 *   - dio_buscar_trilha    → get details for a specific technology path
 *   - dio_gerar_desafio    → generate a coding challenge
 *   - dio_gerar_certificado → issue a completion certificate
 *
 * Transport: stdio (local) by default.
 * For remote/HTTPS access, wrap this server behind an HTTP gateway
 * (see README.md in this folder for deployment options).
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, resolve, join } from "path";

// ---------------------------------------------------------------------------
// Data loading
// ---------------------------------------------------------------------------

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Resolve data path relative to the repo structure:
// build/index.js → ../../data/trilhas_dio.json
const DATA_PATH = resolve(__dirname, "../../data/trilhas_dio.json");

interface Live {
  titulo: string;
  data: string;
  duracao_min: number;
}

interface Promocao {
  ativa: boolean;
  desconto_percentual: number;
  validade: string | null;
}

interface Trilha {
  id: number;
  nome: string;
  tecnologia: string;
  nivel: string;
  modulos: number;
  xp_total: number;
  badges: string[];
  promocao: Promocao;
  vitalicio: boolean;
  lives_ao_vivo: Live[];
}

interface DadosTrilhas {
  trilhas: Trilha[];
  metadata: {
    total_trilhas: number;
    fonte: string;
    url_base: string;
    gerado_em: string;
    niveis_disponiveis: string[];
    xp_medio: number;
    trilhas_com_promocao: number;
    trilhas_vitalicio: number;
  };
}

function carregarTrilhas(): DadosTrilhas {
  const raw = readFileSync(DATA_PATH, "utf-8");
  return JSON.parse(raw) as DadosTrilhas;
}

function buscarTrilha(tecnologia: string): Trilha | null {
  const dados = carregarTrilhas();
  const tech = tecnologia.trim().toLowerCase();
  return dados.trilhas.find((t) => t.tecnologia.toLowerCase() === tech) ?? null;
}

// ---------------------------------------------------------------------------
// Challenge generation (mirrors Python logic)
// ---------------------------------------------------------------------------

const XP_NIVEL: Record<string, number> = {
  Básico: 150,
  Intermediário: 350,
  Avançado: 600,
};

const TEMPO_NIVEL: Record<string, string> = {
  Básico: "15–30 min",
  Intermediário: "30–60 min",
  Avançado: "60–120 min",
};

const TEMAS_POR_TECNOLOGIA: Record<string, string[]> = {
  java: [
    "Calculadora de Impostos com OOP",
    "Sistema de Filas com BlockingQueue",
    "CRUD com Spring Boot e JPA",
    "Streams API — Processamento de Dados",
  ],
  python: [
    "Análise de CSV com pandas",
    "Web scraper simples com requests",
    "Gerador de senhas seguras",
    "Decorators e Context Managers",
  ],
  default: [
    "Algoritmo de busca binária",
    "Implementação de pilha e fila",
    "Validador de expressões matemáticas",
    "Gerador de relatório em texto",
  ],
};

const NIVEL_MAP: Record<string, string> = {
  basico: "Básico",
  básico: "Básico",
  intermediario: "Intermediário",
  intermediário: "Intermediário",
  avancado: "Avançado",
  avançado: "Avançado",
};

function normalizarNivel(nivel: string): string {
  return NIVEL_MAP[nivel.trim().toLowerCase()] ?? "Intermediário";
}

function pick<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

// ---------------------------------------------------------------------------
// MCP Server setup
// ---------------------------------------------------------------------------

const server = new McpServer({
  name: "dio-explorer-mcp",
  version: "0.1.0",
});

// ── Tool: dio_listar_trilhas ────────────────────────────────────────────────
server.registerTool(
  "dio_listar_trilhas",
  {
    description:
      "Lista todas as trilhas de aprendizado disponíveis na DIO com tecnologia e nível. " +
      "Útil para descobrir quais tecnologias estão cadastradas.",
    inputSchema: z.object({}),
  },
  async () => {
    try {
      const dados = carregarTrilhas();
      const lista = dados.trilhas.map((t) => ({
        id: t.id,
        tecnologia: t.tecnologia,
        nivel: t.nivel,
        modulos: t.modulos,
        xp_total: t.xp_total,
        promocao_ativa: t.promocao.ativa,
        vitalicio: t.vitalicio,
      }));
      const meta = dados.metadata;
      const texto =
        `📚 **Trilhas DIO disponíveis** (${meta.total_trilhas} total)\n\n` +
        lista
          .map(
            (t) =>
              `• **${t.tecnologia}** — ${t.nivel} | ${t.modulos} módulos | ${t.xp_total} XP` +
              (t.promocao_ativa ? " 🔥 Promoção ativa" : "") +
              (t.vitalicio ? " | Vitalício" : "")
          )
          .join("\n");
      return { content: [{ type: "text" as const, text: texto }] };
    } catch (err) {
      return {
        content: [
          {
            type: "text" as const,
            text: `Erro ao carregar trilhas: ${err instanceof Error ? err.message : String(err)}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// ── Tool: dio_buscar_trilha ─────────────────────────────────────────────────
server.registerTool(
  "dio_buscar_trilha",
  {
    description:
      "Retorna os detalhes completos de uma trilha DIO pela tecnologia: " +
      "módulos, XP, badges, lives e promoções.",
    inputSchema: z.object({
      tecnologia: z
        .string()
        .describe(
          "Nome da tecnologia da trilha (ex: Python, Java, React, Node.js)"
        ),
    }),
  },
  async ({ tecnologia }) => {
    try {
      const trilha = buscarTrilha(tecnologia);
      if (!trilha) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Trilha para '${tecnologia}' não encontrada. Use a ferramenta dio_listar_trilhas para ver as tecnologias disponíveis.`,
            },
          ],
          isError: true,
        };
      }

      const vitalicio = trilha.vitalicio ? "Sim" : "Não";
      const badges = trilha.badges.map((b) => `  - ${b}`).join("\n");
      const lives = trilha.lives_ao_vivo
        .map(
          (l) => `  [${l.data}] ${l.titulo} (${l.duracao_min} min)`
        )
        .join("\n");
      const promo = trilha.promocao.ativa
        ? `${trilha.promocao.desconto_percentual}% de desconto (válido até ${trilha.promocao.validade})`
        : "Sem promoção ativa no momento.";

      const texto =
        `# Trilha DIO: ${trilha.nome}\n` +
        `Tecnologia : ${trilha.tecnologia}\n` +
        `Nível      : ${trilha.nivel}\n` +
        `Módulos    : ${trilha.modulos}\n` +
        `XP Total   : ${trilha.xp_total} XP\n` +
        `Vitalício  : ${vitalicio}\n\n` +
        `Badges:\n${badges}\n\n` +
        `Lives:\n${lives}\n\n` +
        `Promoção   : ${promo}`;

      return { content: [{ type: "text" as const, text: texto }] };
    } catch (err) {
      return {
        content: [
          {
            type: "text" as const,
            text: `Erro ao buscar trilha: ${err instanceof Error ? err.message : String(err)}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// ── Tool: dio_gerar_desafio ─────────────────────────────────────────────────
server.registerTool(
  "dio_gerar_desafio",
  {
    description:
      "Gera um desafio de código para praticar uma tecnologia em um nível específico. " +
      "Retorna o tema do desafio, XP a ganhar e tempo sugerido.",
    inputSchema: z.object({
      tecnologia: z
        .string()
        .describe("Tecnologia do desafio (ex: Python, Java)"),
      nivel: z
        .string()
        .describe(
          "Nível do desafio: Básico, Intermediário ou Avançado"
        ),
    }),
  },
  async ({ tecnologia, nivel }) => {
    try {
      const nivelNorm = normalizarNivel(nivel);
      const techKey = tecnologia.trim().toLowerCase();
      const temas =
        TEMAS_POR_TECNOLOGIA[techKey] ?? TEMAS_POR_TECNOLOGIA["default"];
      const tema = pick(temas);

      const avisos: string[] = [];
      if (!NIVEL_MAP[nivel.trim().toLowerCase()]) {
        avisos.push(
          `Nível '${nivel}' não reconhecido. Usando 'Intermediário' como padrão.`
        );
      }
      if (!TEMAS_POR_TECNOLOGIA[techKey]) {
        avisos.push(
          `Tecnologia '${tecnologia}' não mapeada; usando desafio genérico.`
        );
      }

      const xp = XP_NIVEL[nivelNorm];
      const tempo = TEMPO_NIVEL[nivelNorm];

      const texto =
        `🎯 **Desafio DIO**\n\n` +
        `Tecnologia     : ${tecnologia}\n` +
        `Nível          : ${nivelNorm}\n` +
        `Tema           : ${tema}\n` +
        `XP a ganhar    : ${xp} XP\n` +
        `Tempo sugerido : ${tempo}` +
        (avisos.length > 0 ? `\n\n⚠️ ${avisos.join(" ")}` : "");

      return { content: [{ type: "text" as const, text: texto }] };
    } catch (err) {
      return {
        content: [
          {
            type: "text" as const,
            text: `Erro ao gerar desafio: ${err instanceof Error ? err.message : String(err)}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// ── Tool: dio_gerar_certificado ─────────────────────────────────────────────
server.registerTool(
  "dio_gerar_certificado",
  {
    description:
      "Emite um certificado de conclusão fictício para um aluno em uma trilha DIO. " +
      "Gera código único no formato DIO-{id}-{ano}-XXXXXX.",
    inputSchema: z.object({
      nome_aluno: z.string().describe("Nome completo do aluno"),
      tecnologia: z
        .string()
        .describe("Tecnologia da trilha concluída (ex: Python, React)"),
    }),
  },
  async ({ nome_aluno, tecnologia }) => {
    try {
      let trilha = buscarTrilha(tecnologia);
      let aviso: string | null = null;

      if (!trilha) {
        aviso = `Trilha '${tecnologia}' não encontrada. Certificado gerado com dados genéricos.`;
        trilha = {
          id: 0,
          nome: `Trilha ${tecnologia}`,
          tecnologia,
          nivel: "Concluído",
          modulos: 0,
          xp_total: 5000,
          badges: [],
          promocao: { ativa: false, desconto_percentual: 0, validade: null },
          vitalicio: false,
          lives_ao_vivo: [],
        };
      }

      const ano = new Date().getFullYear();
      const sufixo = Array.from({ length: 6 }, () =>
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".charAt(
          Math.floor(Math.random() * 36)
        )
      ).join("");
      const codigo = `DIO-${trilha.id}-${ano}-${sufixo}`;
      const dataEmissao = new Date().toLocaleDateString("pt-BR");
      const badges =
        trilha.badges.length > 0
          ? trilha.badges.map((b) => `  - ${b}`).join("\n")
          : "  (nenhum badge nesta trilha)";

      const texto =
        `🏆 **Certificado DIO**\n\n` +
        `Aluno          : ${nome_aluno}\n` +
        `Trilha         : ${trilha.nome}\n` +
        `Tecnologia     : ${trilha.tecnologia}\n` +
        `Nível          : ${trilha.nivel}\n` +
        `Módulos        : ${trilha.modulos}\n` +
        `XP Total       : ${trilha.xp_total} XP\n` +
        `Código         : ${codigo}\n` +
        `Data de emissão: ${dataEmissao}\n\n` +
        `Badges conquistadas:\n${badges}` +
        (aviso ? `\n\n⚠️ ${aviso}` : "");

      return { content: [{ type: "text" as const, text: texto }] };
    } catch (err) {
      return {
        content: [
          {
            type: "text" as const,
            text: `Erro ao gerar certificado: ${err instanceof Error ? err.message : String(err)}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("DIO Explorer MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
