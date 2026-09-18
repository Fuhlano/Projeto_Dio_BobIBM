---
name: trilha
description: Exibe o plano de estudos formatado de uma trilha DIO pela tecnologia
metadata:
  user-invocable: true
  disable-model-invocation: true
  argument-hint: <tecnologia>
---

O usuário quer visualizar o plano de estudos da trilha de **$1** disponível na DIO.

Leia o arquivo `dio_explorer/data/trilhas_dio.json` e procure a trilha cuja propriedade `tecnologia` corresponda a "$1" (comparação case-insensitive, aceite variações como "python", "Python", "PYTHON").

Se encontrar a trilha, formate e apresente o plano de estudos como um documento markdown rico seguindo **exatamente** esta estrutura:

---

# 🎓 Trilha DIO: {nome}

| Campo        | Detalhes                          |
|--------------|-----------------------------------|
| 🏷️ Tecnologia | {tecnologia}                      |
| 📊 Nível      | {nivel}                           |
| 📦 Módulos    | {modulos} módulos                 |
| ⭐ XP Total   | {xp_total} XP                    |
| ♾️ Vitalício  | Sim / Não                         |

## 📋 Plano de Estudos

Gere uma lista numerada de módulos com títulos realistas e progressivos para a tecnologia em questão, com base no nível e no número de módulos indicado no JSON. Para cada módulo, inclua:
- Um título temático condizente com a trilha
- Uma breve descrição do que será aprendido (1 linha)
- Uma estimativa de duração (ex: "~2h")

Formato de cada item:
**Módulo N — Título do Módulo** `~Xh`
> Descrição breve do conteúdo.

## 🏅 Badges que você vai conquistar

Liste cada badge da trilha como um item com emoji de medalha:
- 🥇 {badge1}
- 🥈 {badge2}
- ...

## 📡 Lives ao Vivo

Liste cada live com data, título e duração:
| # | Título | Data | Duração |
|---|--------|------|---------|
| 1 | {titulo} | {data} | {duracao_min} min |

## 💰 Promoção

- Se `promocao.ativa` for `true`: exiba um bloco de destaque com o desconto e a validade.
- Se for `false`: escreva "Sem promoção ativa no momento."

## 🚀 Por onde começar?

Escreva uma dica motivacional de 2-3 frases específica para a tecnologia, encorajando o usuário a iniciar a trilha na plataforma DIO (https://web.dio.me/).

---

Se **não encontrar** nenhuma trilha com a tecnologia "$1", liste todas as tecnologias disponíveis no JSON em uma tabela organizada por nível, e sugira as trilhas mais próximas.
