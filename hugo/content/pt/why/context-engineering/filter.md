---
title: "Por Que Filtros Sao Necessarios"
weight: 5
date: 2026-02-26T12:00:09+09:00
lastmod: 2026-02-26T12:00:09+09:00
tags: ["filtro", "relevancia", "confianca"]
summary: "Informacao valida nem sempre e informacao necessaria"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Informacao valida nem sempre e informacao necessaria.

---

## Voce Tem 1.000 Pecas de Informacao Que Passaram na Verificacao

Suponha que a verificacao mecanica funcionou.

O formato esta correto,
campos obrigatorios existem,
identificadores sao validos,
tipos sao apropriados,
e a integridade referencial se mantem -- 1.000 afirmacoes permanecem.

Todas sao informacao valida.
Estao em conformidade com a especificacao. Nao ha razao para rejeita-las.

Mas a janela de contexto so comporta 300.

Quais 300 voce coloca?

Esse e o problema da filtragem.

---

## Verificacao e Filtragem Fazem Perguntas Diferentes

O que a verificacao pergunta: "Essa informacao e valida?"
O que a filtragem pergunta: "Essa informacao e necessaria agora?"

Verificacao olha para as propriedades da informacao em si.
O formato esta correto? Os campos estao presentes? As referencias sao validas?
Nao importa sobre o que e a informacao ou qual proposito ela servira.

Filtragem olha para a relacao entre informacao e situacao.
E relevante para esta inferencia especifica agora?
Essa informacao pode ser confiavel?
E suficientemente recente?

Verificacao e possivel sem contexto. Voce so precisa da especificacao.
Filtragem e impossivel sem contexto. Voce precisa saber "o que e necessario agora."

Verificacao e deterministica. Valido ou invalido.
Filtragem e julgamento. Relevancia tem graus, confiabilidade tem limites, atualidade tem contexto.

Verificacao e barata.
Filtragem e relativamente cara.

Por isso verificacao vem primeiro e filtragem vem depois.
Se a verificacao filtra primeiro, entao a filtragem julga um conjunto menor.
O custo do julgamento caro diminui.

---

## Tres Coisas Que a Filtragem Julga

Filtragem olha para tres coisas principais.

### Relevancia: E Necessario para Esta Inferencia?

O usuario perguntou sobre "lucro operacional da Samsung Electronics no Q3 2024."

Entre as afirmacoes validas que passaram na verificacao:

- O lucro operacional da Samsung Electronics no Q3 2024 foi de 9,18 trilhoes de won.
- A receita da Samsung Electronics no Q3 2024 foi de 79 trilhoes de won.
- O lucro operacional da Samsung Electronics no Q3 2023 foi de 2,43 trilhoes de won.
- O plano de investimento em semicondutores da Samsung Electronics e de 53 trilhoes de won em 2025.
- A sede da Samsung Electronics fica em Suwon.

Todas validas. Todas sobre Samsung Electronics.
Voce coloca todas no contexto?

A localizacao da sede e irrelevante.
O plano de investimento tem baixa relevancia.
O lucro operacional de 2023 pode ser util para comparacao.
Receita esta intimamente relacionada ao lucro operacional.

Em RAG de linguagem natural, esse julgamento e delegado a similaridade de embedding.
Classificado por distancia vetorial a "Samsung Electronics lucro operacional."
Mas como ja discutido, similar nao e relevante.

Em uma representacao estruturada, o julgamento de relevancia tem entradas diferentes.
A qual entidade a afirmacao aponta? Samsung Electronics.
Qual propriedade? Lucro operacional.
Qual tempo? Q3 2024.

Se entidade, propriedade e tempo existem como campos,
voce pode encontrar "mesma entidade, mesma propriedade, mesmo tempo" com precisao.
E pode intencionalmente incluir ou excluir "mesma entidade, mesma propriedade, tempo diferente."
Correspondencia de campos, nao distancia vetorial.

Relevancia ainda e um julgamento. Nao e deterministica.
Mas se a entrada para esse julgamento e distancia vetorial ou campos estruturados faz diferenca na precisao.

### Confiabilidade: Essa Informacao Pode Ser Acreditada?

Duas afirmacoes existem sobre o mesmo conteudo.

- Fonte: divulgacao de RI da Samsung Electronics. Confianca: 1,0. "Lucro operacional Q3 2024: 9,18 trilhoes de won."
- Fonte: blog anonimo. Confianca: 0,3. "Lucro operacional Q3 2024: aproximadamente 10 trilhoes de won."

Qual vai para o contexto?

Obviamente a primeira.

Mas para que esse julgamento seja "obvio,"
a fonte e a confianca devem existir em uma forma legivel.

Em chunks de linguagem natural, a fonte esta enterrada em algum lugar no texto ou ausente.
Confianca nunca foi expressa.
Para comparar dois chunks e julgar qual e mais confiavel,
um LLM precisa ler e raciocinar.

Em uma representacao estruturada, fonte e confianca sao campos.
"Excluir confianca abaixo de 0,5" e uma comparacao.
"Incluir apenas fontes primarias" e correspondencia de campos.

O custo da filtragem de confiabilidade passa de inferencia de LLM para comparacao de campos.

### Atualidade: Essa Informacao e Suficientemente Atual?

"Quem e o CEO da Samsung Electronics?"

- Tempo: marco de 2024. "CEO da Samsung Electronics: Kyung Kye-hyun."
- Tempo: dezembro de 2022. "Co-CEOs da Samsung Electronics: Han Jong-hee, Kyung Kye-hyun."

Ambas sao validas. Formato correto, fontes presentes.
Mas a mais recente e necessaria.

Em linguagem natural, o tempo pode ou nao ser mencionado no texto.
Se diz "no ano passado," voce tambem precisa calcular quando era "o ano passado."

Em uma representacao estruturada, tempo e um campo.
Uma data ISO 8601.
"Incluir apenas a afirmacao mais recente" e uma operacao de ordenacao.

Mais importante, o criterio de atualidade depende do contexto.
Se alguem pergunta pelo CEO, a entrada mais recente e necessaria.
Se alguem pergunta por todos os CEOs anteriores, todas as entradas sao necessarias.
Se alguem pergunta por tendencias de receita, os ultimos 8 trimestres sao necessarios.

Se tempo existe como um campo, essas condicoes podem ser expressas como uma consulta.
Se tempo esta enterrado em linguagem natural, precisa ser extraido toda vez.

---

## Por Que Filtragem Nao e Verificacao Mecanica

Ha uma distincao importante aqui.

Dos tres criterios da filtragem -- relevancia, confiabilidade, atualidade --
confiabilidade e atualidade podem ser amplamente processadas mecanicamente em uma representacao estruturada.
Comparacao de campos, ordenacao de valores, filtragem por faixa.

Entao por que chamar isso de "filtragem" e nao "verificacao"?

Verificacao olha apenas para propriedades da informacao em si.
"Essa afirmacao tem um campo de tempo?" Presente ou ausente. Nenhum contexto necessario.

Filtragem olha para a relacao entre informacao e situacao.
"O tempo dessa afirmacao e apropriado para esta pergunta?" Voce precisa saber qual e a pergunta para responder.

Ambas examinam o mesmo campo de tempo,
mas verificacao checa "existencia"
e filtragem julga "adequacao."

Existencia nao precisa de contexto.
Adequacao precisa de contexto.

Essa diferenca e o motivo pelo qual o pipeline separa os dois estagios.

---

## A Estrutura de Custos da Filtragem

Filtragem e mais cara que verificacao. Mas quao cara depende da representacao.

**Filtragem em um pipeline de linguagem natural:**
Julgamento de relevancia -- inferencia de LLM ou computacao de similaridade de embedding.
Julgamento de confiabilidade -- LLM extrai informacao de fonte do texto e avalia.
Julgamento de atualidade -- LLM extrai informacao temporal do texto e compara.
Tudo raciocinio. Tudo caro.

**Filtragem em uma representacao estruturada:**
Julgamento de relevancia -- correspondencia de campos entidade/propriedade + julgamento baseado em contexto.
Julgamento de confiabilidade -- comparacao do campo de confianca. Correspondencia do campo de fonte.
Julgamento de atualidade -- ordenacao do campo de tempo. Comparacao de faixa.
Confiabilidade e atualidade sao operacoes de campo. Apenas relevancia requer julgamento.

Em outras palavras, estruturacao converte dois dos tres criterios de filtragem em operacoes mecanicas.
O que resta e apenas relevancia.
Mesmo relevancia se estreita de "esse bloco de texto e similar a pergunta" para "essa propriedade dessa entidade e relevante para a pergunta," tornando o julgamento mais claro.

O custo total da filtragem cai significativamente.

---

## O Que Acontece Sem Filtragem

Se voce verifica mas coloca tudo no contexto sem filtrar.

Todas as 1.000 pecas validas de informacao entram.
Dessas, apenas 30 sao necessarias agora.

O LLM le todas as 1.000.
Ler custa dinheiro.
970 pecas desnecessarias de informacao dispersam a atencao.
Pesquisas mostram que mais informacao irrelevante no contexto aumenta a probabilidade de alucinacao.
A qualidade do raciocinio sobre as 30 que realmente importam se degrada.

A janela tambem e desperdicada.
Do espaco que 1.000 itens ocupam, o espaco de 970 itens e desperdicio.
Esse espaco poderia ter contido outras informacoes mais relevantes.

Filtragem e gerenciar uma janela finita de forma finita.
Se verificacao confirma "qualifica-se para entrar,"
filtragem julga "tem razao para entrar."

Qualificacao e questao de formato. Razao e questao de contexto.
Ambas sao necessarias.

---

## Filtragem e Politica

Mais um ponto importante.

Os criterios de filtragem nao sao fixos.
Eles variam com o contexto.

Filtragem para um agente de consulta medica:
Limite de confiabilidade e alto. Excluir confianca abaixo de 0,9.
Padrao de atualidade e rigoroso. Excluir informacao medica com mais de 3 anos.
Excluir fontes que nao sejam periodicos revisados por pares.

Filtragem para um agente de conversa casual:
Limite de confiabilidade e baixo. Informacao aproximada e aceitavel.
Padrao de atualidade e flexivel. Informacao mais antiga pode ser incluida dependendo do contexto.
Restricoes de fonte sao frouxas.

A mesma informacao passa em um agente e e rejeitada em outro.
A informacao nao mudou. A politica e diferente.

Isso significa que filtragem nao e meramente um problema tecnico
mas um problema de design.
"O que entra no contexto" e a mesma pergunta que
"quais padroes queremos que este agente opere."

Em uma representacao estruturada, essa politica e expressa declarativamente.
"confidence >= 0.9, time >= 2022, source_type = peer-reviewed."
Uma linha de consulta.

Em linguagem natural, essa politica e escrita como linguagem natural no prompt.
"Por favor, refira-se apenas a informacoes confiaveis e recentes."
Se o LLM segue isso consistentemente e uma questao de probabilidade.

---

## Resumo

Nem toda informacao que passa na verificacao e necessaria.
Uma janela de contexto finita deve conter apenas o que e necessario para a inferencia atual.

Filtragem julga tres coisas.
Relevancia -- essa informacao e necessaria para a pergunta atual?
Confiabilidade -- essa informacao pode ser acreditada?
Atualidade -- essa informacao e suficientemente atual?

Verificacao e filtragem fazem perguntas diferentes.
Verificacao pergunta "e valido?"; filtragem pergunta "e necessario?"
Verificacao e possivel sem contexto; filtragem requer contexto.
Verificacao vem primeiro; filtragem vem depois.

Em uma representacao estruturada, dois dos tres criterios da filtragem -- confiabilidade e atualidade -- sao convertidos em operacoes de campo. O que resta e apenas relevancia, e mesmo essa se torna mais clara pela correspondencia de campos estruturais.

Filtragem e politica.
A mesma informacao e incluida ou excluida dependendo do contexto.
Em uma representacao estruturada, essa politica e declarada como uma consulta.
Em linguagem natural, essa politica e escrita no prompt como uma esperanca.
