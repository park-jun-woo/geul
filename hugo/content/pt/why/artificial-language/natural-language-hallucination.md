---
title: "Por Que a Linguagem Natural Cria Alucinacoes?"
weight: 8
date: 2026-02-26T12:00:16+09:00
lastmod: 2026-02-26T12:00:16+09:00
tags: ["linguagem natural", "alucinacao", "ambiguidade"]
summary: "A alucinacao nao e um bug do LLM — e uma consequencia estrutural inevitavel de quatro falhas da linguagem natural: ambiguidade, ausencia de fonte, de confianca e de tempo. Modelos maiores nao resolvem."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## A alucinacao nao e um bug. E uma inevitabilidade estrutural enquanto usarmos linguagem natural.

---

## O Milagre da Linguagem Natural

Ha 100.000 anos, a linguagem falada surgiu. As relacoes sociais que primatas conseguiam manter por meio de catacao mutua eram limitadas a cerca de 150 individuos. A linguagem quebrou esse teto. Uma vez que uma pessoa podia falar para muitas ao mesmo tempo, uma nova escala de sociedade --- a tribo --- se tornou possivel.

Ha 10.000 anos, a agricultura criou excedentes alimentares, e as pessoas se reuniram em um so lugar para formar cidades. Ha 5.000 anos, alguem na Mesopotamia pressionou marcas em forma de cunha em uma tabua de argila umida. Era para registrar inventarios de graos. O nascimento da escrita. A fala desaparece, mas os registros perduram. Uma vez que registros perduraram, a burocracia se tornou possivel, a lei se tornou possivel, o Estado se tornou possivel.

A linguagem falada criou a tribo. A escrita criou o Estado.

A linguagem natural e a maior tecnologia que a humanidade ja criou. Nao a descoberta do fogo, nao a invencao da roda, nao a invencao do semicondutor. O que tornou tudo isso possivel foi a linguagem natural. Porque a linguagem natural existia, o conhecimento podia ser transmitido, a cooperacao podia acontecer, e os pensamentos dos mortos podiam ser herdados pelos vivos. Por dezenas de milhares de anos, a linguagem natural foi o meio de toda a civilizacao humana.

E agora, essa grande linguagem natural se tornou o gargalo da era da IA.

---

## O Mal-Entendido Chamado Alucinacao

Quando a IA diz algo falso, chamamos de "alucinacao".

Esse nome carrega implicacoes.
A implicacao de que a alucinacao e anormal.
A implicacao de que pode ser corrigida.
A implicacao de que um modelo melhor vai resolver.

Isso e um mal-entendido.

A alucinacao nao e um bug dos LLMs.
A alucinacao e uma inevitabilidade estrutural que nao pode ser evitada
enquanto a linguagem natural for usada como linguagem de raciocinio da IA.

Nao importa o quanto voce escale o modelo,
nao importa o quanto voce expanda os dados,
nao importa o quao refinado seja o RLHF,
enquanto a entrada for linguagem natural e a saida for linguagem natural,
a alucinacao nao vai desaparecer.

Vou explicar por que.

---

## As Quatro Falhas Estruturais da Linguagem Natural

A linguagem natural evoluiu para comunicacao entre humanos.
As quatro caracteristicas que ela adquiriu nesse processo
se tornam falhas fatais no raciocinio da IA.

---

### Falha 1: Ambiguidade

"Ele foi ao banco."

"Banco" e uma instituicao financeira ou a margem de um rio?
Quem e "ele"?
Quando ele foi?

Humanos resolvem isso com contexto.
O fluxo da conversa, a expressao facial do falante, conhecimento de fundo compartilhado.

A IA tem apenas texto.
Texto sozinho nao consegue resolver completamente a ambiguidade.
Se nao pode ser resolvida, a IA adivinha.
Adivinhar as vezes esta errado.
Quando um palpite errado e produzido com confianca, isso e alucinacao.

---

### Falha 2: Ausencia de Fonte

"Yi Sun-sin derrotou 133 navios com apenas 12."

Essa frase nao tem fonte.

Quem fez essa afirmacao?
Quais registros historicos a sustentam?
Ha desacordo academico sobre esses numeros?

A linguagem natural nao tem lugar estrutural para metadados.
Para incluir fontes, voce tem que alongar a frase,
e alonga-la obscurece o ponto.
Entao na maioria das frases em linguagem natural, fontes sao omitidas. Esse problema e aprofundado em [Por Que Afirmacoes, Nao Fatos?](/pt/why/claims-not-facts/).

LLMs sao treinados com bilhoes de tais frases.
Afirmacoes com fontes omitidas se misturam
em uma enorme sopa estatistica.

Rastrear a base para o numero "12" dentro dessa sopa
e impossivel em principio.
Ja que a base nao pode ser rastreada, numeros sem base tambem podem ser fabricados.
Isso e alucinacao.

---

### Falha 3: Ausencia de Confianca

"A Terra e redonda."
"A energia escura compoe 68% do universo."
"Vai chover amanha."

Os niveis de confianca dessas tres frases sao completamente diferentes.

A primeira e um consenso esmagador.
A segunda e a melhor estimativa atual, mas a teoria pode mudar.
A terceira e uma previsao probabilistica.

No entanto, em linguagem natural, todas as tres tem estruturas gramaticais identicas.
Sujeito + predicado. Frase declarativa. Ponto final.

A linguagem natural nao consegue expressar estruturalmente "qual a certeza disso".
Existem recursos adverbiais como "talvez", "quase certamente", "pode ser",
mas eles sao opcionais, imprecisos e geralmente omitidos.

LLMs aprendem todas as frases em niveis de confianca identicos.
Nao ha como o modelo distinguir internamente a diferenca de confianca
entre "a Terra e redonda" e "a energia escura e 68%".

Entao ele afirma estimativas como fatos,
afirma hipoteses como visoes estabelecidas,
e afirma coisas incertas com certeza.
Isso e alucinacao.

---

### Falha 4: Ausencia de Contexto Temporal

"O CEO da Tesla e Elon Musk."

A partir de quando?

Em 2024, isso esta correto.
Em 2030, quem sabe.
Se o momento da escrita nao e especificado,
o periodo de validade dessa frase nao pode ser determinado.

A maioria das frases em linguagem natural omite contexto temporal.
O "presente" pode significar "agora mesmo"
ou pode significar "geralmente".

LLMs aprendem artigos de 2020 e artigos de 2024 como os mesmos dados.
Como a informacao temporal nao e estruturalmente preservada,
eles afirmam fatos passados como se fossem presentes,
ou misturam informacoes de diferentes periodos.
Isso e alucinacao.

---

## A Confluencia das Quatro Falhas

A alucinacao escala explosivamente quando essas quatro falhas convergem.

Vamos analisar uma unica saida de LLM.

> "Yi Sun-sin destruiu 330 navios japoneses com 12 embarcacoes,
> e mais tarde morreu na Batalha de Noryang, deixando as ultimas palavras 'Nao anunciem minha morte.'"

Nessa frase:

**Ambiguidade:** O que "destruiu" significa precisamente? Afundou? Derrotou? Danificou parcialmente?

**Ausencia de fonte:** Qual a base para os numeros 12 e 330? Diferentes registros historicos citam numeros diferentes --- qual foi seguido?

**Ausencia de confianca:** "Nao anunciem minha morte" e um ultimo testamento historicamente confirmado, ou tradicao oral posterior? Os niveis de confianca dos dois sao diferentes, mas estao listados na mesma frase declarativa.

**Ausencia de contexto temporal:** Qual ponto no tempo do consenso academico essa informacao reflete?

O LLM preenche toda essa ambiguidade com "a sequencia de tokens mais plausivel".
Plausibilidade nao e precisao.
A lacuna entre as duas e alucinacao.

---

## Por Que Modelos Maiores Nao Podem Resolver Isso

"A alucinacao nao vai diminuir quando o GPT-5 sair?"

Vai diminuir. Mas nao vai desaparecer.

Modelos maiores aprendem padroes mais sofisticados de mais dados.
Entao a precisao da "plausibilidade" sobe.

Mas o problema fundamental nao muda.

Enquanto a entrada for linguagem natural, a ambiguidade permanece.
Enquanto os dados de treinamento forem linguagem natural, as fontes permanecem perdidas.
Enquanto a saida for linguagem natural, a confianca nao e expressa.
Enquanto a informacao temporal estiver ausente da estrutura, o tempo permanece embaralhado.

Mesmo que voce escale o modelo em 100x,
as falhas estruturais da linguagem natural nao crescem 100x ---
mas tambem nao chegam a zero.

Isso nao e um problema de resolucao. E um problema de meio.

Nao importa o quanto voce aumente a resolucao de uma fotografia em preto e branco, a cor nao aparece.
Nao importa o quanto voce aumente a precisao da linguagem natural,
fonte, confianca e contexto temporal nao aparecem na estrutura.

Se voce quer cor, precisa de filme colorido.
Se voce quer eliminar a alucinacao, precisa de uma linguagem diferente.

---

## Condicoes para uma Solucao Estrutural

Para resolver essas quatro falhas, a estrutura da linguagem em si deve ser diferente.

**Ambiguidade --> Estruturacao explicita.**
Quando "Ele foi ao banco" e convertido em uma linguagem estruturada,
"ele" e resolvido para um SIDX de entidade especifica,
e "banco" e resolvido para o SIDX de uma instituicao financeira ou margem de rio.
Se nao pode ser resolvido, "nao resolvido" e explicitamente declarado.
Ou resolva a ambiguidade, ou registre o fato de que e ambiguo.

**Ausencia de fonte --> Fonte incorporada.**
Cada narracao inclui estruturalmente uma entidade fonte.
"Quem fez essa afirmacao" faz parte da narracao.
Nao e opcional. Se o campo esta vazio, e marcado como vazio.

**Ausencia de confianca --> Confianca incorporada.**
Cada verb edge tem um campo de confianca.
"Certo", "estimado", "hipotetico"
sao especificados estruturalmente como modificadores verbais.

**Ausencia de contexto temporal --> Contexto temporal incorporado.**
Cada narracao inclui um contexto temporal.
"A partir de quando e esta narracao" e sempre especificado.

O que e omitido na linguagem natural
existe como parte da estrutura em uma linguagem estruturada.

Quando a omissao e impossivel, o espaco para alucinacao encolhe. [Por Que a Clarificacao e Necessaria](/pt/why/clarification/) explica esse principio.
Quando voce nao pode falar sem base, declaracoes sem base nao sao produzidas.

---

## O Fim da Alucinacao Esta na Substituicao da Linguagem

Vamos olhar para as abordagens atuais de reducao de alucinacao.

**RAG (Retrieval-Augmented Generation):** Recupera documentos externos e os fornece como contexto. Eficaz, mas os documentos recuperados tambem sao linguagem natural, entao os problemas de ambiguidade, fontes ausentes e confianca ausente seguem inalterados. [Por Que RAG Nao e Suficiente](/pt/why/rag-not-enough/) explora essa limitacao em detalhe.

**RLHF:** Treina o modelo a dizer "nao sei" quando incerto. Reduz a frequencia da alucinacao, mas nao resolve o problema fundamental de que a linguagem natural carece de uma estrutura de confianca.

**Chain-of-Thought:** Registra o processo de raciocinio em linguagem natural. A direcao esta certa, mas o meio do registro e linguagem natural, entao herda as mesmas falhas.

Todas essas abordagens tentam mitigar a alucinacao dentro do arcabouco da linguagem natural.
Elas funcionam. Mas nao sao fundamentais.

A solucao fundamental e remover a linguagem natural de dentro da IA.

A interface com os usuarios permanece em linguagem natural.
Humanos continuam falando em linguagem natural e recebendo respostas em linguagem natural.

Mas a linguagem na qual a IA raciocina, registra e verifica internamente
deve ser algo diferente da linguagem natural.

Uma linguagem onde a fonte esta na estrutura.
Uma linguagem onde a confianca esta na estrutura.
Uma linguagem onde o contexto temporal esta na estrutura.
Uma linguagem onde a ambiguidade e explicitamente tratada.

A linguagem falada criou a tribo.
A escrita criou o Estado.
O que a terceira linguagem vai criar?

O fim da alucinacao nao esta em modelos maiores
mas em uma linguagem melhor.

---

## Resumo

A alucinacao nasce das quatro falhas estruturais da linguagem natural.

1. **Ambiguidade:** Irresoluvel sem contexto. A IA adivinha, e palpites estao errados.
2. **Ausencia de fonte:** A base das afirmacoes e perdida. Combinacoes sem base sao fabricadas.
3. **Ausencia de confianca:** Fatos e estimativas sao expressos na mesma gramatica. A IA nao consegue distingui-los.
4. **Ausencia de contexto temporal:** Informacoes de diferentes periodos sao embaralhadas.

Modelos maiores reduzem a alucinacao mas nao podem elimina-la.
Sem mudar o meio, as falhas estruturais permanecem.

Nao importa o quanto voce aumente a resolucao do filme preto e branco, a cor nao aparece.
Se voce quer cor, deve trocar o filme.
