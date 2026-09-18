---
description: Gera um desafio de código aleatório baseado em tecnologia e nível
argument-hint: <tecnologia> <nivel: Básico|Intermediário|Avançado>
---
O usuário quer um desafio de código em **$1** com nível **$2**.

Gere **um único desafio de código aleatório** (escolha um tema diferente a cada vez) seguindo **exatamente** esta estrutura em markdown:

---

# ⚔️ Desafio DIO — {tecnologia} [{nivel}]

> 💡 *"{Uma frase motivacional curta sobre programação ou aprendizado}"*

## 📌 Enunciado

Escreva o enunciado completo do desafio. Deve ser:
- Condizente com a tecnologia **$1** e o nível **$2**
- Objetivo e claro, com contexto de problema real
- Entre 4 e 8 linhas descrevendo o que deve ser implementado

## 📥 Entrada

Descreva o formato da entrada esperada (tipo de dado, restrições, exemplos de valores).

## 📤 Saída

Descreva o formato da saída esperada.

## 🧪 Exemplos

Forneça de 2 a 3 casos de teste no formato:

**Exemplo 1:**
- Entrada: `{valor_entrada}`
- Saída esperada: `{valor_saida}`

**Exemplo 2:**
- Entrada: `{valor_entrada}`
- Saída esperada: `{valor_saida}`

## 💎 Critérios de Avaliação

Liste de 3 a 5 critérios objetivos que serão avaliados (ex: eficiência, legibilidade, cobertura de edge cases).

## 🧩 Dica

Dê uma dica sutil que ajude o raciocínio sem entregar a solução. Máximo 2 linhas.

## ⏱️ Tempo sugerido

Indique um tempo recomendado para resolução com base no nível:
- Básico: 15–30 min
- Intermediário: 30–60 min  
- Avançado: 60–120 min

## 🏆 Recompensa estimada

Calcule e exiba a XP estimada:
- Básico: 150 XP
- Intermediário: 350 XP
- Avançado: 600 XP

---

## 🚀 Pronto para começar?

Escreva sua solução aqui embaixo e me envie para revisão! Ou peça `/desafio $1 $2` novamente para um novo desafio diferente.

---

**Regras de geração:**
- Para nível **Básico**: exercícios de lógica, estruturas básicas, algoritmos simples
- Para nível **Intermediário**: estruturas de dados, padrões, integração com APIs, OOP
- Para nível **Avançado**: performance, concorrência, arquitetura, sistemas distribuídos, otimização
- Varie os temas a cada invocação: nunca repita o mesmo enunciado
- Se $2 não for um nível válido (Básico, Intermediário, Avançado), use "Intermediário" como padrão e avise o usuário
- Se $1 não for reconhecida como tecnologia, crie um desafio genérico de programação e avise
