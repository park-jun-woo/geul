---
title: "Por Que a Verificacao Mecanica e Necessaria"
weight: 4
date: 2026-02-26T12:00:10+09:00
lastmod: 2026-02-26T12:00:10+09:00
tags: ["verificacao", "especificacao", "compilador"]
summary: "Linguagem natural nao tem o conceito de sentenca invalida"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Linguagem natural nao tem o conceito de "sentenca invalida."

---

## Ninguem Inspeciona o Que Entra no Contexto

Observe como informacao entra no contexto nos pipelines atuais de LLM.

RAG retorna chunks.
Um agente recebe respostas de API.
Conversas anteriores se acumulam no historico.
Um usuario faz upload de um documento.

Tudo isso vai para a janela de contexto.
Sem inspecao.

Por que nao ha inspecao?
Porque linguagem natural nao tem o conceito de "invalido."

---

## Linguagem Natural Aceita Qualquer String

Em programacao, existe algo chamado erro de sintaxe.

```python
def calculate(x, y
    return x + y
```

O parentese nao foi fechado. E rejeitado antes da execucao.
Codigo pode ser declarado definitivamente como "isso nao e codigo valido" antes de ser executado, antes mesmo de ser lido.

Linguagem natural nao tem isso.

"Ele foi ao banco."
Gramaticalmente perfeito.
Voce nao consegue dizer quem foi, qual banco, ou por que,
mas nada viola as regras gramaticais da linguagem natural.

"Relatorio de vendas do 45o dia do 13o mes de 2024."
Nao existe 13o mes e nao existe 45o dia.
Mas nada viola as regras gramaticais da linguagem natural.
E uma sentenca gramaticalmente valida.

"Fonte: desconhecida. Confianca: desconhecida. Data: desconhecida. O valor de mercado da Samsung Electronics e 1.200 trilhoes de won."
A fonte e desconhecida, a confianca e desconhecida, a data de referencia e desconhecida.
Mas nada viola as regras gramaticais da linguagem natural.

Linguagem natural aceita tudo.
Uma sentenca invalida em linguagem natural estruturalmente nao existe.
Portanto, nao ha criterio mecanico para "rejeitar" informacao expressa em linguagem natural.

---

## O Que e Necessario para Verificacao Mecanica

Observe o compilador Go.

Go se recusa a compilar se houver um import nao utilizado.
Mesmo que o codigo funcione perfeitamente.
Mesmo que nao haja nada de errado com a logica.
Ele se recusa unicamente porque uma linha de import nao e usada.

Isso e verificacao mecanica.

Verificacao mecanica tem tres caracteristicas.

**E deterministica.** O resultado e sim ou nao. Nao uma probabilidade. Nao existe "provavelmente esta certo." Valido ou invalido.

**E barata.** Nenhuma chamada ao LLM necessaria. Comparacao de strings, verificacao de existencia de campos, verificacao de faixa de valores. Operacoes de CPU na escala de nanossegundos.

**Nao le o significado.** Nao julga se o conteudo e verdadeiro ou falso. Apenas verifica se o formato esta em conformidade com a especificacao. Nao sabe se "o valor de mercado da Samsung Electronics e 1.200 trilhoes de won" e verdade. Mas sabe se o campo de fonte esta vazio.

Para que essas tres coisas sejam possiveis, ha um pre-requisito.
A informacao deve ter uma especificacao.

Se ha uma especificacao, violacoes sao definidas.
Se violacoes sao definidas, rejeicao e possivel.
Se rejeicao e possivel, verificacao existe.

Linguagem natural nao tem especificacao, entao nao ha violacoes.
Sem violacoes significa sem rejeicao.
Sem rejeicao significa sem verificacao.

---

## Por Que Verificacao Pre-Contexto e Necessaria

A janela de contexto e finita.

Seja 128K tokens ou 1M tokens, e finita.
A qualidade da informacao que entra em um espaco finito determina a qualidade da saida.

Porem, nos pipelines atuais,
o julgamento de qualidade acontece apenas depois que a informacao entra no contexto.
Espera-se que o LLM leia, julgue e conclua por conta propria que "essa informacao e dificil de confiar."

Isso esta errado de tres formas.

**E caro.** Voce esta usando custos de inferencia do LLM para fazer verificacao de formato. Voce roda um modelo com bilhoes de parametros para filtrar chunks sem fonte. Voce usa raciocinio probabilistico para uma tarefa que requer verificar um unico campo.

**E nao confiavel.** Nao ha garantia de que o LLM sempre ignorara informacao sem fonte. Na verdade, uma vez que algo esta no contexto, o LLM tem mais probabilidade de usa-lo. Esperar que o modelo ignore algo que voce colocou no contexto e uma contradicao.

**E tardio.** O espaco da janela ja foi consumido. Se 5 chunks sem fonte ocupam 200 tokens cada, 1.000 tokens sao desperdicados. Mesmo que sejam filtrados depois, esse espaco ja foi gasto.

Verificacao mecanica vem antes de tudo isso.
Antes de entrar no contexto.
Antes de o LLM ler.
Antes de a janela ser consumida.

---

## O Que e Verificado

Verificacao mecanica nao verifica a veracidade do conteudo, mas a conformidade com uma especificacao de formato.

Especificamente, estas coisas:

**Completude estrutural.** Campos obrigatorios existem? A aresta tem sujeito e objeto? Algo esta faltando?

**Validade de identificadores.** O no referenciado existe? O que esta escrito como "Samsung Electronics" realmente aponta para uma entidade definida? A referencia esta pendente?

**Conformidade de tipos.** Ha uma data no campo de data? Ha um numero no campo de numero? "O 45o dia do 13o mes de 2024" e pego aqui.

**Presenca de metadados.** Ha um campo de fonte? Ha um campo de tempo? A confianca esta especificada? Se nao, rejeitar, marcar como ausente, ou atribuir um padrao.

**Integridade referencial.** O no apontado pela aresta realmente existe? Esta referenciando um no excluido?

Essas verificacoes tem uma coisa em comum.
Todas podem ser realizadas sem ler o conteudo.
Voce nao sabe se "o valor de mercado da Samsung Electronics e 1.200 trilhoes de won" e verdade.
Mas sabe se uma fonte esta especificada para essa afirmacao.
Sabe se um tempo esta registrado para essa afirmacao.
Sabe se o formato dessa afirmacao esta em conformidade com a especificacao.

---

## O Barato Vem Primeiro

Em um pipeline de engenharia de contexto, inspecoes tem uma ordem.

**Verificacao mecanica**: conformidade com a especificacao. Custo proximo de zero. Deterministica.
**Filtragem semantica**: julgamento de relevancia, confiabilidade, utilidade. Custo alto. Probabilistica.
**Verificacao de consistencia**: contradicoes entre pecas de informacao selecionadas. Custo ainda maior. Requer raciocinio.

Se voce as organiza da mais barata para a mais cara,
as verificacoes caras tem menos para processar.

Se a verificacao mecanica filtra 30% das afirmacoes sem fonte,
a filtragem semantica so precisa processar 70%.
Se a filtragem semantica remove o irrelevante,
a verificacao de consistencia lida com um conjunto ainda menor.

Esse e o mesmo principio da otimizacao de consultas em bancos de dados.
Aplique condicoes filtraveis por indice na clausula WHERE primeiro.
Condicoes de varredura completa vem depois.
Se o barato vem primeiro, a carga sobre a parte cara diminui.

Por outro lado,
se voce roda a verificacao cara primeiro e a barata depois,
descobre erros de formato apenas depois de ja ter gasto o custo.
Voce analisa o significado de uma afirmacao que referencia um no inexistente,
so para descobrir depois que a referencia e invalida.

---

## Essa Ordem e Impossivel em um Pipeline de Linguagem Natural

Linguagem natural nao tem especificacao, entao verificacao mecanica e impossivel.
Como verificacao mecanica e impossivel, a verificacao mais barata nao existe.

Consequentemente, toda verificacao e uma verificacao semantica.
Toda verificacao requer um LLM.
Toda verificacao e cara.

"Esse chunk tem uma fonte?" -- O LLM precisa ler.
"A referencia temporal desse chunk e apropriada?" -- O LLM precisa ler.
"O formato desse chunk esta correto?" -- Linguagem natural nao tem formato, entao a pergunta em si nao se sustenta.

Essa e a realidade atual da engenharia de contexto.
Ate a verificacao mais simples e feita com a ferramenta mais cara.
Uma tarefa que poderia terminar com comparacao de strings e tratada por um motor de inferencia.

---

## Pre-requisitos para Verificacao

Para que verificacao mecanica exista, tres coisas sao necessarias.

**Uma especificacao.** O formato que a informacao deve seguir precisa ser definido. Quais campos sao obrigatorios, quais valores sao permitidos, quais referencias sao validas. Sem uma especificacao, violacoes nao podem ser definidas.

**Formalizacao.** A informacao deve ser expressa no formato que a especificacao exige. Nao como sentencas em linguagem natural, mas codificada na estrutura que a especificacao demanda. Informacao que nao e formalizada nao pode ser inspecionada.

**O poder de rejeitar.** Deve ser possivel realmente rejeitar informacao que nao esta em conformidade. Se voce inspeciona mas sempre aprova, nao e verificacao. Informacao invalida deve ser impedida de entrar no contexto.

Essas tres coisas sao dadas como certas em linguagens de programacao.
Ha uma especificacao chamada gramatica, um formato chamado codigo, e um poder de rejeitar chamado compilador.

Em linguagem natural, as tres estao ausentes.
Gramatica nao e uma especificacao de formato, mas uma convencao.
Sentencas nao sao formatos estruturados, mas texto livre.
O conceito de "linguagem natural invalida" nao existe, entao nao ha nada a rejeitar.

Para introduzir verificacao mecanica na engenharia de contexto,
a representacao da informacao em si deve mudar.

---

## Resumo

No pipeline de contexto atual, informacao entra no contexto sem inspecao.
Porque linguagem natural nao tem o conceito de "sentenca invalida."

Verificacao mecanica nao verifica a veracidade do conteudo, mas a conformidade com uma especificacao de formato.
Completude estrutural, validade de identificadores, conformidade de tipos, presenca de metadados, integridade referencial.
Deterministica, barata, e nao le o significado.

No pipeline, verificacoes baratas devem vir primeiro.
Se a verificacao mecanica filtra erros de formato,
os julgamentos semanticos caros tem menos para processar.

Linguagem natural nao tem especificacao, entao essa verificacao e impossivel.
Toda verificacao se torna verificacao semantica, e toda verificacao e cara.

Para que verificacao mecanica seja possivel,
deve haver uma especificacao, formalizacao e o poder de rejeitar.
A representacao da informacao em si deve mudar.
