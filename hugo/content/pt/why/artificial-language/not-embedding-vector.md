---
title: "Por que vetores de embedding não são suficientes"
weight: 11
date: 2026-02-26T12:00:18+09:00
lastmod: 2026-02-26T12:00:18+09:00
tags: ["embedding", "vetor", "caixa branca"]
summary: "Reorganizar vetores de embedding quebra o modelo. Evitar a quebra significa reconstruir o modelo do zero. O que precisamos não é transparência dentro da caixa preta, mas uma camada transparente fora dela."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Vetores são ótimos para cálculo, mas impossíveis de interpretar. Não se pode tornar o interior de uma caixa preta transparente.

---

## Vetores de embedding são uma tecnologia notável

"Rei - Homem + Mulher = Rainha."

Quando o word2vec demonstrou isso, o mundo ficou perplexo.
Represente palavras como vetores com centenas de dimensões
e as relações semânticas emergem como operações vetoriais.

Vetores de embedding são a base dos LLMs.
Tudo num transformer é computação vetorial.
Tokens se tornam vetores.
A atenção calcula a similaridade entre vetores.
As saídas são convertidas de vetores de volta para tokens.

Significados semelhantes são vetores próximos.
Significados diferentes são vetores distantes.
Busca é cálculo de similaridade vetorial.
Classificação é definição de fronteiras no espaço vetorial.

Sem vetores de embedding, a IA atual não existiria.

Então, por que não usar vetores de embedding para representar conhecimento?
Alinhá-los diretamente, estruturá-los, torná-los interpretáveis.

Não funciona.
A forma mais segura de saber isso é tentar.

---

## AILEV: Tentamos

O projeto GEUL começou originalmente com o nome AILEV.

AI Language Embedding Vector.

O nome por si só declarava o propósito:
uma linguagem de IA que manipula diretamente vetores de embedding.

O conceito era o seguinte:

Representar significado com vetores de 512 dimensões.
Atribuir papéis a segmentos do vetor.
As primeiras 128 dimensões para entidades, as próximas 128 para relações, as próximas 128 para propriedades, o restante para metadados.
Assim como o RGBA decompõe cor em quatro canais, decompor significado em segmentos dimensionais.

Treinar o BERT para converter linguagem natural nesses vetores estruturados.
Ao inserir "Seul é a capital da Coreia",
o segmento de entidades produz o vetor de Seul, o de relações produz o vetor de capital, o de propriedades produz o vetor de Coreia.

Como são vetores, o cálculo é possível.
A busca por similaridade é possível.
Reduzir dimensões proporciona degradação elegante.
Passar de 512 para 256 dimensões perde precisão, mas preserva o significado essencial.

Era elegante. Na teoria.

---

## Por que falha

### Reorganizar vetores arbitrariamente quebra o modelo

Os vetores de embedding de um LLM são produto do treinamento.

Após ler bilhões de textos,
o modelo otimiza por conta própria suas representações internas.
O que cada dimensão significa é algo que o modelo decidiu.
Não uma pessoa.

O que acontece se você declara "as primeiras 128 dimensões são para entidades"?

No espaço vetorial que o modelo aprendeu,
a informação de entidades não reside nas primeiras 128 dimensões.
Está distribuída por todas as 768 dimensões.
Informação de relações, propriedades, tempos verbais — tudo misturado.

Isso não é um erro de design, mas a natureza do aprendizado.
A retropropagação encontra
o arranjo vetorial ótimo para a tarefa.
Não encontra um arranjo interpretável.
Ótimo e interpretável não são a mesma coisa.

Se você reorganizar vetores à força — "entidades aqui, relações ali" —
as relações estatísticas que o modelo aprendeu se quebram.
O desempenho cai.

### Reorganizar sem quebrar significa reconstruir o modelo

Então, por que não treinar do zero com a restrição "as primeiras 128 dimensões são para entidades"?

É possível. Na teoria.
Mas isso não é alinhar vetores de embedding.
É projetar uma nova arquitetura de modelo.

Precisa-se de dados de treinamento. Bilhões de tokens.
Precisa-se de infraestrutura. Milhares de GPUs.
Precisa-se de tempo de treinamento. Meses.
E não há garantia de que o modelo resultante funcione tão bem quanto os LLMs existentes.

O esforço é grande demais.

O problema de "alinhar vetores para torná-los interpretáveis"
se transformou em "reconstruir um LLM do zero".
Isso não é resolver o problema, mas ampliá-lo.

### A interpretação é impossível

Suponha que você tenha conseguido criar um vetor estruturado.
Um vetor de 512 dimensões.
Digamos que as primeiras 128 dimensões sejam para entidades.

O segmento de entidades vale `[0.23, -0.47, 0.81, 0.12, ...]`.

Como saber se isso é "Samsung Electronics" ou "Hyundai Motor"?

É preciso encontrar o vetor mais próximo.
É preciso calcular a similaridade num banco de dados vetorial.
E obtém-se uma resposta probabilística: "provavelmente Samsung Electronics".

"Provavelmente."

Vetores são inerentemente contínuos.
Entre os vetores de Samsung Electronics e SK Hynix
existem infinitos vetores intermediários.
Ninguém sabe o que esses vetores intermediários significam.

Isso não é uma limitação técnica, mas uma verdade matemática.
Representar significados discretos num espaço contínuo
torna as fronteiras ambíguas.
A ambiguidade era [o problema da linguagem natural](/pt/why/natural-language-hallucination/).
Trocamos para vetores, e a ambiguidade voltou.

Só a forma mudou.
Na linguagem natural, a ambiguidade das palavras.
Nos vetores, a ambiguidade das coordenadas.

---

## O princípio da caixa branca

Aqui se revela a questão fundamental de design.

Vetores de embedding são uma caixa preta.
Olhando para um vetor de 768 dimensões de valores reais,
ninguém consegue dizer que informação está codificada onde.
O próprio modelo não consegue explicar.

Isso não é uma característica inconveniente, mas uma propriedade ontológica.
É precisamente por isso que os vetores funcionam.
Porque organizam informação de formas que humanos não projetaram,
funcionam melhor do que qualquer projeto humano.
A impossibilidade de interpretação não é um defeito, mas uma funcionalidade.

No entanto, o conhecimento usado como contexto de IA exige o oposto.

É preciso saber a fonte.
É preciso saber o momento.
É preciso saber o nível de confiança.
É preciso saber sobre o que é a afirmação.
É preciso saber se duas afirmações se referem à mesma entidade.

Cada requisito é "é preciso saber". Cada requisito exige interpretabilidade.

Satisfazer exigências de caixa branca com um vetor de caixa preta
é uma contradição.

---

## A lógica da virada

A virada de AILEV para GEUL não foi uma desistência.
Foi uma redefinição do problema.

**Problema original:** LLMs são caixas pretas. Vamos tornar o interior transparente.
→ Vamos tornar vetores de embedding interpretáveis alinhando-os.
→ Mexer nos vetores quebra o modelo.
→ Evitar a quebra significa reconstruir o modelo.
→ Beco sem saída.

**Problema redefinido:** Não é preciso tornar o interior da caixa preta transparente. Vamos construir uma camada transparente do lado de fora.
→ Não se mexe no interior do LLM.
→ Fora do LLM, cria-se um sistema de representação interpretável.
→ O LLM pode ler e escrever esse sistema. Porque são tokens.
→ Uma linguagem artificial.

Não vetores, mas linguagem.
Não contínuo, mas discreto.
Não ininterpretável, mas com a interpretação como único propósito.
Não dentro do modelo, mas fora do modelo.

O "Embedding Vector" de AILEV foi removido,
e surgiu GEUL — que significa "escrita". Esta é a razão.

---

## Vetores para o cálculo, linguagem para a representação

Isso não é uma rejeição dos vetores de embedding.

Vetores são otimizados para o cálculo.
Busca por similaridade, agrupamento, classificação, recuperação.
A linguagem não pode substituir o que os vetores fazem.

A linguagem é otimizada para a representação.
Identidade de entidades, descrição de relações, metadados integrados, interpretabilidade.
Os vetores não podem substituir o que a linguagem faz.

São ferramentas em camadas diferentes.

Dentro do LLM, vetores operam. Uma caixa preta. Assim deve ser.
Fora do LLM, a linguagem opera. Uma caixa branca. Assim deve ser.

O problema começou quando essas duas camadas foram confundidas.
Tentou-se fazer os vetores realizarem o trabalho da linguagem.
Tentou-se atribuir a uma caixa preta o papel de uma caixa branca.

Cada um tem o seu lugar.

---

## Resumo

Vetores de embedding são a base dos LLMs e uma tecnologia notável.
No entanto, como meio de representação de conhecimento, têm limites fundamentais.

GEUL começou como AILEV (AI Language Embedding Vector).
O objetivo era alinhar vetores diretamente e torná-los interpretáveis.
Falhou. Por dois motivos.

Alinhar vetores arbitrariamente quebra as relações que o modelo aprendeu.
Alinhar sem quebrar significa reconstruir o modelo do zero. O esforço é grande demais.

E mesmo se tivesse sucesso, vetores não podem ser interpretados.
Num espaço contínuo, as fronteiras do significado discreto são ambíguas.
Não se pode atribuir a uma caixa preta o papel de uma caixa branca.

A lógica da virada:
Tentou-se tornar o interior da caixa preta transparente.
Mexer no interior o quebra.
Em vez disso, deixar o interior intacto e construir uma camada transparente do lado de fora.
Não vetores, mas linguagem. Não dentro do modelo, mas fora do modelo.

Vetores para o cálculo, linguagem para a representação.
Cada um tem o seu lugar.
