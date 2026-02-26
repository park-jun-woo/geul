---
title: "Por que Wikidata"
weight: 13
date: 2026-02-26T12:00:17+09:00
lastmod: 2026-02-26T12:00:17+09:00
tags: ["Wikidata", "Ontologia", "SIDX"]
summary: "GEUL não rejeita o Wikidata. Transforma o sistema de classificação e as estatísticas de frequência de 100 milhões de entidades em livros de códigos SIDX. Constrói gramática sobre um dicionário."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## GEUL não rejeita o Wikidata. Ergue-se sobre ele.

---

## Não se pode criar uma língua sem um dicionário

Toda língua precisa de um vocabulário.

O coreano tem o dicionário coreano.
O inglês tem o dicionário inglês.
Linguagens de programação têm bibliotecas padrão.

O mesmo vale para uma língua artificial.
Uma lista de entidades, uma lista de relações, uma lista de propriedades.
Qual código representa a "Samsung Electronics" nesta língua?
Qual código representa a relação "capital"?
É preciso ter um vocabulário antes de poder escrever uma frase.

Como se constrói esse vocabulário?
Há dois caminhos.

Construí-lo do zero.
Ou usar o que já existe.

---

## Construir do zero: a lição do CYC

O projeto CYC começou em 1984.

Seu objetivo era formalizar e armazenar conhecimento geral de senso comum.
A ontologia foi projetada do zero.
Conceitos foram definidos, relações foram definidas, regras foram definidas.
Especialistas os inseriram manualmente.

Trinta anos se passaram.
Milhões de regras foram inseridas.

Porém, estava longe de cobrir o conhecimento do mundo.
Cada domínio exigia o projeto de uma ontologia separada.
Manter a consistência entre domínios se mostrou difícil.
Sempre que um novo conceito surgia, a ontologia precisava ser revisada.
Revisões frequentemente entravam em conflito com regras existentes.

O que o CYC demonstrou não foi seu potencial, mas seus limites.
Ter uma pequena equipe de especialistas projetando a ontologia do mundo
torna-se insustentável em escala.

---

## O que já existe: Wikidata

O Wikidata foi lançado em 2012.

Uma base de conhecimento estruturada operada pela Fundação Wikimedia.
Qualquer pessoa pode editá-la.
Em 2024, contém mais de 100 milhões de entidades.
Mais de 10.000 propriedades.
Bilhões de declarações.
Rótulos em mais de 300 idiomas.

A escala que o CYC não conseguiu alcançar em 30 anos com uma equipe de especialistas,
o Wikidata alcançou em 10 anos com uma comunidade.

Veja o que o Wikidata oferece.

**Identificadores de entidades.** Q-IDs. Samsung Electronics é Q20718. Seul é Q8684. Yi Sun-sin é Q217300. Identificadores únicos globalmente. Independentes de idioma.

**Identificadores de propriedades.** P-IDs. "Localização da sede" é P159. "Data de fundação" é P571. "População" é P1082. Relações e propriedades são identificadas de forma única.

**Estrutura hierárquica.** P31 (instance of) e P279 (subclass of) formam uma hierarquia de tipos. "Seul → cidade → assentamento humano → entidade geográfica." O sistema de classificação do mundo é expresso por meio dessas duas propriedades.

**Rótulos multilíngues.** O rótulo coreano de Q20718 é "삼성전자", o rótulo em inglês é "Samsung Electronics", o rótulo em japonês é "サムスン電子". Um identificador, nomes diferentes para cada idioma.

**Validação comunitária.** Milhões de editores. Detecção de vandalismo. Exigência de fontes. Não é perfeito, mas é mais escalável do que uma pequena equipe de especialistas.

Não há razão para construir tudo isso do zero.

---

## O vocabulário de GEUL vem do Wikidata

O SIDX (Semantic-aligned Index) de GEUL é um identificador semanticamente alinhado de 64 bits.
O significado está codificado nos próprios bits.
Apenas examinando os bits superiores, é possível saber se algo é uma pessoa, um lugar ou uma organização.

O livro de códigos do SIDX — qual padrão de bits corresponde a qual significado — é extraído do Wikidata.

O processo funciona assim.

**Etapa 1: Extração de tipos.**
Extraem-se todos os Q-IDs usados como objetos de P31 (instance of) no Wikidata.
Isso produz a lista de "tipos".
"Humano (Q5)", "cidade (Q515)", "país (Q6256)", "empresa (Q4830453)"...
Conta-se quantas vezes cada tipo é usado — o número de instâncias.

**Etapa 2: Construção da hierarquia.**
Extraem-se as relações P279 (subclass of) entre tipos.
"Cidade → assentamento humano → entidade geográfica → entidade."
Isso forma a estrutura de árvore dos tipos.
Identificam-se nós raiz, nós folha e nós intermediários.
Detecta-se e trata-se a herança múltipla — casos em que um tipo pertence a vários tipos pai.

**Etapa 3: Atribuição de bits.**
A estrutura da árvore determina as relações de prefixo dos padrões de bits.
Subtipos sob o mesmo pai compartilham o mesmo prefixo.
"Cidade" e "vila" compartilham o prefixo de "assentamento humano".

O número de instâncias influencia o comprimento dos bits.
Tipos usados com frequência recebem códigos mais eficientes.
O mesmo princípio da codificação de Huffman: códigos mais curtos para frequências mais altas.

---

## O que o Wikidata fornece

Nesse processo, o Wikidata fornece três coisas.

**Um sistema de classificação.**
Uma resposta a "Que tipos de coisas existem no mundo?"
O CYC tinha uma equipe de especialistas projetando isso.
GEUL o extrai do Wikidata.
Um sistema de classificação construído por milhões de editores ao longo de 10 anos,
transformado em uma árvore de bits.

**Estatísticas de frequência.**
Uma resposta a "Quantas de cada tipo existem no mundo?"
Se há 9 milhões de entidades humanas e 1 milhão de asteroides,
o tipo "humano" deve receber um código mais eficiente que "asteroide".
A frequência de uso real determina o projeto do código.

**Mapeamento de identificadores.**
Um mapeamento entre os Q-IDs do Wikidata e os SIDX de GEUL.
Qual padrão de bits no SIDX corresponde a Q20718 (Samsung Electronics)?
Com esse mapeamento, o conhecimento do Wikidata pode ser convertido para GEUL,
e as declarações de GEUL podem ser reconvertidas para o Wikidata.

---

## O que o Wikidata não fornece

O Wikidata é um dicionário. Um dicionário não é uma língua.

Um dicionário fornece uma lista de palavras.
Uma língua fornece a gramática para compor frases com palavras.

O que o Wikidata não fornece é o que GEUL acrescenta.

**De fatos a alegações.**
A unidade básica do Wikidata é um fato (Fact).
"A população de Seul é 9,74 milhões."
É verdadeiro ou falso.

A unidade básica de GEUL é uma alegação (Claim).
"Segundo A, a população de Seul é aproximadamente 9,74 milhões. (confiança 0,9, referência 2023)"
Quem está alegando, com que nível de certeza e com base em que data — tudo isso está incorporado na declaração.
Essa diferença é discutida em detalhe em [Por que alegações, não fatos](/pt/why/claims-not-facts/).

**Qualificadores verbais.**
O Wikidata não tem um lugar para expressar as nuances dos verbos.
Em "Yi Sun-sin venceu a Batalha de Myeongnyang",
onde estão o tempo, o aspecto, a evidencialidade, o modo e a confiança?
No Wikidata, estes são parcialmente expressos por meio de qualificadores,
mas não existe um sistema sistemático de qualificação verbal.

GEUL tem um sistema de qualificadores verbais de 28 bits.
Treze dimensões — tempo, aspecto, polaridade, evidencialidade, modo, volicionalidade, confiança e outros — são estruturalmente incorporadas em cada declaração.

**Compressão de 16 bits.**
A representação do Wikidata não foi projetada para janelas de contexto.
JSON-LD, RDF, SPARQL.
Legíveis por máquinas, mas não eficientes em tokens.

GEUL é projetada em unidades de palavras de 16 bits.
Mapeamento um para um com tokens de LLM.
Um sistema de representação construído sobre a premissa de janelas de contexto finitas.
Isso já foi discutido em [Por que não MD/JSON/XML](/pt/why/not-md-json-xml/).

**Pipeline de contexto.**
O Wikidata é um repositório. GEUL é parte de um pipeline.
Clarificação, validação, filtragem, verificação de consistência, exploração — tudo o que foi discutido nesta série opera sobre a representação estruturada de GEUL.
O Wikidata não tem esse pipeline.
Nem precisa. O propósito do Wikidata é diferente.

---

## A relação entre um dicionário e uma língua

Em resumo:

O Wikidata é o vocabulário do mundo.
Quais entidades existem,
quais relações existem,
quais tipos existem e como são classificados.
Milhões de pessoas construíram isso ao longo de 10 anos.

GEUL constrói gramática sobre esse vocabulário.
O sistema de classificação do vocabulário → a árvore de bits do SIDX.
As estatísticas de frequência do vocabulário → as prioridades de atribuição de bits.
Os identificadores do vocabulário → o mapeamento com SIDX.

E acrescenta o que falta ao vocabulário.
Estrutura de alegações. Qualificação verbal. Compressão em nível de token. Pipeline de contexto.

Seria possível construir GEUL sem o Wikidata?
Sim. Projetando a ontologia do zero, como fez o CYC.
Mas isso foi tentado há 30 anos, e os resultados falam por si.

Porque o Wikidata existe, GEUL não projeta uma ontologia.
Transforma um consenso existente.

---

## Resumo

Uma língua artificial precisa de um vocabulário.
Construir um do zero foi o que o CYC tentou, e 30 anos provaram os limites dessa abordagem.

O Wikidata é o vocabulário do mundo, com mais de 100 milhões de entidades, mais de 10.000 propriedades e bilhões de declarações.
Milhões de editores o construíram ao longo de 10 anos.

O livro de códigos SIDX de GEUL é extraído do Wikidata.
As frequências de instâncias de P31 determinam a atribuição de bits,
e a hierarquia de P279 forma o esqueleto da árvore de bits.

O Wikidata é um dicionário; GEUL é uma língua.
Um dicionário fornece palavras; uma língua fornece gramática.
GEUL constrói estrutura de alegações, qualificação verbal, compressão de 16 bits e um pipeline de contexto sobre o vocabulário do Wikidata.

GEUL não rejeita o Wikidata.
Ergue-se sobre ele.
