---
description: Gera um certificado fictício em markdown com nome do usuário e trilha concluída
argument-hint: <seu_nome> <tecnologia_da_trilha>
---
O usuário **$1** concluiu a trilha de **$2** na DIO e quer seu certificado fictício.

Leia o arquivo `dio_explorer/data/trilhas_dio.json` e localize a trilha cuja propriedade `tecnologia` corresponda a "$2" (comparação case-insensitive).

Com os dados encontrados, gere o certificado abaixo em markdown. Se a tecnologia não for encontrada, use dados genéricos e avise o usuário.

---

Produza **exatamente** o seguinte certificado em markdown:

---

```
╔══════════════════════════════════════════════════════════════════╗
║                    🎓  DIO — Digital Innovation One              ║
║                       CERTIFICADO DE CONCLUSÃO                   ║
╚══════════════════════════════════════════════════════════════════╝
```

# 🏆 Certificado de Conclusão

---

**Certificamos que**

## $1

concluiu com êxito a trilha de aprendizado:

---

> ## 🚀 {nome_da_trilha}
> **Tecnologia:** $2 | **Nível:** {nivel} | **Módulos:** {modulos}

---

### 📋 Competências Desenvolvidas

Liste de 4 a 6 competências técnicas relevantes que o aluno dominou ao concluir essa trilha, com base na tecnologia e nos badges da trilha.

### 🏅 Badges Conquistados

Liste todos os badges da trilha com emoji de medalha dourada (🥇) para o primeiro e (🏅) para os demais.

### ⭐ XP Total Acumulado

```
{xp_total} XP
```

### 📅 Informações do Certificado

| Campo              | Valor                                       |
|--------------------|---------------------------------------------|
| 👤 Aluno           | $1                                          |
| 📚 Trilha          | {nome_da_trilha}                            |
| 🛠️ Tecnologia      | $2                                          |
| 🎯 Nível           | {nivel}                                     |
| 📦 Módulos         | {modulos}                                   |
| 📅 Data de Emissão | {data_atual_no_formato DD/MM/YYYY}          |
| 🔑 Código          | DIO-{id_da_trilha}-{ano}-{hash_6_chars}     |
| 🌐 Verificar em    | https://web.dio.me/certificates             |

---

### 💬 Mensagem de Reconhecimento

Escreva um parágrafo motivacional de 3-4 linhas personalizado para **$1**, mencionando a tecnologia **$2**, as possibilidades de carreira abertas e incentivando a continuar aprendendo na DIO.

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         Emitido por DIO — Digital Innovation One
              https://web.dio.me/ · @dioinc
         "Acelerando a carreira de devs no Brasil"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

**Instruções de geração:**
- Substitua todos os campos `{...}` pelos dados reais lidos do JSON
- O código do certificado deve ter formato `DIO-{id}-{ano}-XXXXXX` onde XXXXXX são 6 caracteres alfanuméricos aleatórios em maiúsculas
- A data de emissão é a data de hoje
- Se $2 não corresponder a nenhuma trilha, gere o certificado com tecnologia genérica, use XP = 5000, nível = "Concluído" e avise que a trilha não foi encontrada no catálogo
