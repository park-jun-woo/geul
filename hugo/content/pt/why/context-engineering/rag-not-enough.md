---
title: "Por Que RAG Nao e Suficiente"
weight: 2
date: 2026-02-26T12:00:11+09:00
lastmod: 2026-02-26T12:00:11+09:00
tags: ["RAG", "busca", "embedding"]
summary: "Parecer relevante e ser relevante nao sao a mesma coisa"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Parecer relevante e ser relevante nao sao a mesma coisa.

---

## RAG e o Padrao Atual

Em 2024, RAG e a forma mais comum de empresas colocarem LLMs para trabalhar.

Retrieval-Augmented Generation.
Buscar documentos externos, inseri-los no contexto e fazer o modelo responder com base nisso.

RAG funciona.
Permite que LLMs referenciem documentos internos nos quais nunca foram treinados.
Permite que reflitam informacoes atualizadas.
Reduz significativamente alucinacoes.

Sem RAG, a adocao empresarial de LLMs teria sido muito mais lenta.
RAG e uma tecnologia que merece respeito.

Mas RAG tem limitacoes fundamentais.
Essas limitacoes nao sao resolvidas construindo um RAG melhor.
Elas decorrem da propria premissa do RAG.

---

## Como RAG Funciona

O nucleo do RAG sao tres etapas.

**Etapa 1: Dividir documentos em chunks.**
PDFs, wikis, documentos internos sao divididos em tamanhos fixos (tipicamente 200--500 tokens).

**Etapa 2: Converter cada chunk em um vetor de embedding.**
Um vetor de valores reais com centenas a milhares de dimensoes.
O "significado" do texto mapeado em um unico ponto no espaco vetorial.

**Etapa 3: Quando uma consulta chega, encontrar vetores similares.**
A consulta tambem e convertida em um vetor.
Os 5--20 chunks com maior similaridade cosine sao selecionados e inseridos no contexto.

Simples e elegante.
E aqui residem tres problemas fundamentais.

---

## Problema 1: Similar Nao e Relevante

Similaridade de embedding mede "se dois textos usam palavras semelhantes em contextos semelhantes."

Isso nao e relevancia.

Exemplo.

Consulta: "Qual foi a receita da Apple no Q3 2024?"

Chunks que a busca por embedding pode retornar:
- "A receita da Apple no Q3 2024 foi de $94,9 bilhoes." -- Relevante
- "A receita da Apple no Q3 2023 foi de $81,8 bilhoes." -- Similar, mas periodo diferente
- "A receita da Samsung Electronics no Q3 2024 foi de 79 trilhoes de won." -- Similar, mas empresa diferente
- "Uma torta de maca tem cerca de 296 kcal." -- Sobreposicao de palavras-chave

Similaridade de embedding nao consegue distinguir esses quatro.
No espaco vetorial, "receita da Apple" se agrupa em uma unica regiao.
Seja 2023 ou 2024, Apple ou Samsung --
a distancia vetorial nao os separa de forma confiavel.

Adicionar um reranker melhora as coisas.
Mas um reranker tambem le e julga texto em linguagem natural,
entao o problema fundamental de ambiguidade permanece.

Busca baseada em estrutura semantica e diferente.
Se "Apple" a entidade tem um identificador unico,
nunca e confundida com "apple" a fruta.
Se "Q3 2024" e um campo de tempo,
e mecanicamente distinguido de "Q3 2023."

Nao e preciso calcular similaridade.
Corresponde ou nao? Sim ou nao.

---

## Problema 2: Chunks Nao Sao Unidades de Significado

Olhe para a primeira etapa do RAG novamente.
"Dividir documentos em chunks."

Esse "dividir" e o problema.

Quando voce divide um documento em unidades de 500 tokens,
o significado e cortado no meio.
Um paragrafo abrange dois chunks.
A premissa e a conclusao de um argumento sao separadas.

"Yi Sun-sin enfrentou 133 navios com apenas 12 na Batalha de Myeongnyang" esta no Chunk A,
e "estudiosos contestam esses numeros" esta no Chunk B.
Se apenas o Chunk A e recuperado para uma consulta,
a informacao de confianca entra no contexto ja perdida.

Fazer chunks maiores? Eles consomem mais da janela.
Fazer chunks menores? Mais contexto e cortado.
Adicionar sobreposicao? Voce desperica a janela com duplicatas.

Nao importa como voce ajuste, o problema fundamental e o mesmo.
Dividir texto em linguagem natural por contagem de tokens
e o mesmo que dividir significado por contagem de tokens.
Significado tem um tamanho inerente,
e dividi-lo por uma unidade nao relacionada causa problemas.

Em uma representacao estruturada, unidades de significado sao explicitas.
Uma predicacao e uma aresta.
Uma aresta nao e dividida.
A busca opera no nivel da aresta.
Nao ha corte no meio do significado.

---

## Problema 3: A Qualidade dos Resultados Recuperados e Desconhecida

RAG retornou 5 chunks.
Antes de colocar esses 5 no contexto, ha perguntas a fazer.

Qual e a fonte dessa informacao?
Qual e a data de referencia?
Quao certa ela e?
Esses 5 se contradizem?

Em chunks de linguagem natural, voce nao consegue saber essas coisas.

A fonte pode ou nao ser mencionada em algum lugar no chunk como linguagem natural.
A referencia temporal pode estar em algum lugar no documento, ou pode ter sido perdida quando o chunk foi dividido.
Confianca nao tem um espaco estrutural em linguagem natural, entao quase sempre esta ausente.
Verificacao de contradicao requer ler todos os 5 chunks e raciocinar sobre eles.

No fim, voce precisa delegar o julgamento de qualidade ao LLM.
Voce usa RAG para reduzir custos de chamadas ao LLM,
mas chama o LLM para verificar os resultados do RAG.

Em uma representacao estruturada, fonte, tempo e confianca sao campos.
"Excluir afirmacoes sem fonte" e uma linha de consulta.
"Excluir informacoes anteriores a 2023" e uma comparacao de campo.
"Excluir confianca abaixo de 0,5" e uma comparacao numerica.
Nenhuma chamada ao LLM necessaria.

---

## A Premissa Fundamental do RAG

A raiz desses tres problemas e uma so.

RAG busca linguagem natural como linguagem natural.

Os documentos sao linguagem natural.
Os chunks sao linguagem natural.
Os embeddings sao aproximacoes estatisticas de linguagem natural.
Os resultados da busca sao linguagem natural.
O que entra no contexto e linguagem natural.

A ambiguidade da linguagem natural permeia todo o pipeline.

A busca e imprecisa porque voce busca conteudo ambiguo em sua forma ambigua.
O contexto e perdido porque voce divide conteudo ambiguo por um tamanho nao relacionado ao significado.
A verificacao e impossivel porque voce nao consegue extrair informacao de qualidade de conteudo ambiguo.

A maioria das tentativas de melhorar o RAG opera dentro dessa premissa.

Usar um modelo de embedding melhor. -- A aproximacao estatistica fica mais refinada, so isso.
Usar uma estrategia de chunking melhor. -- As posicoes de corte melhoram, so isso.
Adicionar um reranker. -- Voce le a linguagem natural mais uma vez, so isso.
Usar busca hibrida. -- Voce mistura palavras-chave e similaridade, so isso.

Todas funcionam.
Todas permanecem dentro do quadro da linguagem natural.
Nenhuma e fundamental.

---

## Condicoes para uma Alternativa Fundamental

Para ir alem dos limites do RAG, a premissa deve mudar.
Nao buscar linguagem natural como linguagem natural,
mas buscar representacoes estruturadas de forma estrutural.

Essa alternativa deve satisfazer tres condicoes.

**Busca por correspondencia, nao por similaridade.**
Nao encontrar "coisas que parecem semelhantes"
mas encontrar "coisas que correspondem."
O identificador corresponde? Esta dentro do intervalo de tempo?
Sim ou nao. Nao uma probabilidade.

**A unidade de significado e a unidade de busca.**
Nao dividir por contagem de tokens
mas armazenar por predicacao e buscar por predicacao.
Sem corte no meio do significado.

**Metadados estao embutidos na estrutura.**
Nao e preciso chamar um LLM para julgar a qualidade dos resultados da busca.
Fonte, tempo e confianca sao campos,
entao filtragem mecanica e possivel.

Quando essas tres condicoes sao atendidas,
a busca passa de "adivinhar candidatos plausiveis"
para "confirmar o que corresponde."

---

## RAG e uma Tecnologia de Transicao

Isso nao e para depreciar o RAG.

RAG foi a melhor resposta em um mundo onde linguagem natural era tudo o que existia.
Quando documentos eram linguagem natural, conhecimento era armazenado em linguagem natural,
e LLMs eram ferramentas que processam linguagem natural,
buscar linguagem natural com linguagem natural era a escolha obvia.

E RAG de fato funciona.
Um LLM com RAG e muito mais preciso do que um sem.
Isso e um fato.

Mas se a premissa de "um mundo onde linguagem natural e tudo o que existe" mudar,
a posicao do RAG muda tambem.

Se representacoes estruturadas existem,
RAG se torna o front end que "recebe entrada em linguagem natural e busca em um armazenamento estruturado."
Linguagem natural -> consulta estruturada -> busca estrutural -> resultados estruturados -> contexto.

RAG nao desaparece.
Seu backend muda.
De busca por similaridade de embedding para busca baseada em estrutura semantica.

---

## Resumo

RAG e o padrao atual de engenharia de contexto.
E tem tres limitacoes fundamentais.

1. **Similar ≠ relevante.** Similaridade de embedding nao garante relevancia. "Parece similar" e "e relevante" sao coisas diferentes.
2. **Chunk ≠ significado.** Dividir por contagem de tokens corta no meio do significado. Premissas e conclusoes sao separadas. Informacao de confianca e perdida.
3. **Julgamento de qualidade e impossivel.** A fonte, o tempo e a confianca dos chunks recuperados nao podem ser determinados mecanicamente. Julga-los requer uma chamada ao LLM.

A raiz dos tres problemas e uma so.
Buscar linguagem natural como linguagem natural.

A alternativa fundamental e mudar a premissa.
Correspondencia, nao similaridade.
Predicacao, nao chunks de tokens.
Metadados embutidos, nao julgamento externo.

RAG e uma tecnologia de transicao.
Foi a melhor resposta em um mundo onde linguagem natural era tudo o que existia.
Quando essa premissa mudar, o backend do RAG muda.
