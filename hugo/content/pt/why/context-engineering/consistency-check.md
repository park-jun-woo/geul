---
title: "Por Que Verificacoes de Consistencia Sao Necessarias"
weight: 6
date: 2026-02-26T12:00:08+09:00
lastmod: 2026-02-26T12:00:08+09:00
tags: ["consistencia", "contradicao", "coerencia"]
summary: "Informacoes individualmente corretas podem ser coletivamente erradas"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Informacoes individualmente corretas podem ser coletivamente erradas.

---

## Verificacao Passou. Filtragem Passou.

Verificacao mecanica filtrou erros de formato.
Filtragem selecionou com base em relevancia, confiabilidade e atualidade.

30 pecas de informacao permanecem.
Todas validas, todas relevantes, todas confiaveis, todas atuais.

Voce coloca essas 30 no contexto?

Nao.
Mais uma coisa precisa ser verificada.
Essas 30 se contradizem?

---

## Contradicao Nao e uma Propriedade de Informacao Individual

Considere estas duas afirmacoes.

- Fonte: divulgacao de RI da Samsung Electronics, outubro de 2024. "CEO da Samsung Electronics: Jun Young-hyun."
- Fonte: divulgacao de RI da Samsung Electronics, marco de 2024. "CEO da Samsung Electronics: Kyung Kye-hyun."

Individualmente, ambas sao validas.
O formato esta correto, a fonte esta presente, o tempo esta presente, e sao confiaveis.
Passam na verificacao. Passam na filtragem.

Mas quando ambas entram no mesmo contexto, ha um problema.
O CEO da Samsung Electronics e Jun Young-hyun ou Kyung Kye-hyun?

Nenhuma das afirmacoes esta errada.
Em marco, Kyung Kye-hyun estava correto. Em outubro, Jun Young-hyun esta correto.
Individualmente, ambas estao certas.
Mas quando coexistem no contexto, o LLM se confunde.

Esse e o problema de consistencia.
Ele surge nao da informacao individual, mas do conjunto de informacoes.
Verificacao examina informacao individual. Filtragem examina informacao individual.
Consistencia examina o espaco entre as pecas de informacao.

---

## Tipos de Contradicao

Contradicoes no contexto se dividem em varios tipos.

### Contradicao Temporal

A mais comum.

A mesma propriedade da mesma entidade mudou ao longo do tempo,
e valores de diferentes pontos no tempo coexistem no contexto.

"CEO da Tesla: Elon Musk" e
"Preco das acoes da Tesla: $194" estao no mesmo contexto,
mas a informacao do CEO e de 2024 e o preco das acoes e de junho de 2023.
O LLM pode trata-los como informacoes do mesmo ponto no tempo.

Casos mais sutis tambem surgem.
"Taxa de juros basica da Coreia do Sul: 3,50%" e de janeiro de 2024, e
"Inflacao de precos ao consumidor da Coreia do Sul: 2,0%" e de outubro de 2024.
Ambas sao validas e ambas se relacionam a economia coreana,
mas ha uma diferenca de 9 meses.
Se essa diferenca afeta a inferencia depende do contexto.

### Contradicao Entre Fontes

Fontes diferentes apresentam valores diferentes para o mesmo fato.

- Fonte A: "Tamanho do mercado global de IA em 2024: $184 bilhoes."
- Fonte B: "Tamanho do mercado global de IA em 2024: $214 bilhoes."

Nenhuma pode ser declarada definitivamente "errada."
A definicao do escopo do mercado pode diferir. Os metodos de medicao podem diferir.
Mas se ambas estao no contexto,
o LLM deve escolher uma, mesclar ambas, ou se confundir.

### Contradicao Inferencial

Nao sao valores diretamente contraditorios,
mas logicamente incompativeis quando colocados juntos.

"Participacao de mercado da Empresa A: 60%."
"Participacao de mercado da Empresa B: 55%."

Cada uma e valida. Mas somam 115%.
Adicionando os concorrentes restantes, ultrapassaria 100%.
Uma delas e de um momento diferente, usa uma definicao de mercado diferente, ou esta errada.

Esse tipo de contradicao nao pode ser encontrado olhando afirmacoes individuais.
Voce deve examinar o conjunto.

---

## LLMs Nao Lidam Bem com Contradicoes

Em teoria, o LLM deveria ser capaz de detectar e resolver contradicoes.
"Essas duas pecas de informacao diferem no tempo, entao vou responder com base na mais recente."

Na pratica, nao e isso que acontece.

**LLMs tendem a confiar na informacao do contexto.**
O ato de colocar algo no contexto e em si um sinal que diz "consulte isso."
Quando duas pecas de informacao contraditorias estao presentes,
o LLM tende a referenciar ambas em vez de ignorar uma.
O resultado e uma mistura ou confusao.

**Deteccao de contradicao requer raciocinio.**
Saber que "CEO: Jun Young-hyun" e "CEO: Kyung Kye-hyun" se contradizem
requer o conhecimento previo de que so existe um CEO em um dado momento.
Verificar se participacoes de mercado somam mais de 100% requer aritmetica.
Isso depende da capacidade de raciocinio do LLM.

**Resolucao e ainda mais dificil.**
Mesmo se uma contradicao e detectada, um julgamento deve ser feito sobre qual lado escolher.
O mais recente? A fonte mais confiavel? O que e apoiado por mais fontes?
Se esse julgamento e deixado para o LLM, consistencia nao e garantida.
Para a mesma contradicao, ele escolhe A as vezes e B outras vezes.

Em conclusao, lidar com contradicoes depois que entram no contexto
e caro e o resultado e incerto.
Contradicoes devem ser resolvidas antes de entrar no contexto.

---

## Por Que Verificacao de Consistencia e Dificil em Linguagem Natural

Suponha que voce esteja verificando a consistencia de 30 chunks de linguagem natural.

Primeiro, voce deve determinar se eles sao sobre o mesmo assunto.
Se "Samsung Electronics," "Samsung Electronics" e "Samsung" se referem a mesma entidade.
Em linguagem natural, isso e incerto.
Se "Samsung" significa Samsung Electronics, Samsung C&T ou Samsung Life requer ler o contexto.

Em seguida, voce deve determinar se descrevem a mesma propriedade.
Se "receita," "receita," "receita total" e "receita bruta" sao a mesma coisa.
Se "lucro operacional," "lucro operacional" e "margem operacional" sao iguais ou diferentes.

Em seguida, voce deve extrair as referencias temporais.
Quando e "trimestre passado"? Quando e "recentemente"? Quando e "este ano"?

Somente depois de tudo isso voce pode finalmente comparar se duas afirmacoes se contradizem.

Com 30 afirmacoes, ha 435 pares de comparacao.
Cada par deve passar pelo processo acima.
Tudo raciocinio de LLM.
Tudo caro.
Tudo probabilistico.

---

## Verificacao de Consistencia em Representacoes Estruturadas

Em uma representacao estruturada, a situacao e diferente.

**Identificacao de entidade e deterministica.**
A entidade "Samsung Electronics" tem um identificador unico.
"Samsung Electronics" aponta para o mesmo identificador.
Nenhum raciocinio e necessario para determinar identidade.

**Propriedades sao explicitas.**
"Receita" e uma propriedade tipada.
"Margem operacional" e uma propriedade diferente.
Se duas propriedades sao iguais ou diferentes e confirmado por comparacao de campos.

**Tempo e um campo.**
Ha um valor como "2024-Q3."
Nao e preciso interpretar "trimestre passado."
Se duas afirmacoes compartilham o mesmo tempo e uma comparacao de valores.

Quando essas tres coisas sao deterministicas, padroes de deteccao de contradicao se tornam mecanizaveis.

Mesma entidade + mesma propriedade + mesmo tempo + valor diferente = contradicao.
Mesma entidade + mesma propriedade + tempo diferente + valor diferente = mudanca. Nao uma contradicao.
Entidade diferente + mesma propriedade + mesmo tempo + soma de valores > 100% = contradicao inferencial.

Nenhum LLM necessario para isso.
Comparacao de campos e aritmetica.

Nem todas as contradicoes podem ser capturadas.
Se "o mercado de IA esta crescendo" e "investimento em IA esta diminuindo" se contradizem
ainda requer julgamento semantico.
Mas se contradicoes mecanicamente detectaveis sao capturadas primeiro,
apenas casos que requerem julgamento semantico permanecem.
Mais uma vez, o barato vem primeiro.

---

## Estrategias de Resolucao para Verificacoes de Consistencia

Apos detectar uma contradicao, ela deve ser resolvida.

Estrategias de resolucao variam por contexto, mas em uma representacao estruturada podem ser declaradas como politica.

**Mais recente primeiro.** Quando a mesma propriedade da mesma entidade conflita, escolha a que tem o timestamp mais recente. Adequado para valores que mudam como CEO, preco de acoes, populacao.

**Maior confianca primeiro.** Escolha a com maior confianca. Ou se uma hierarquia de fontes e definida, escolha a fonte de maior classificacao. Fonte primaria > fonte secundaria > fonte nao oficial.

**Apresentar ambas.** Nao resolver a contradicao. Colocar ambas no contexto, mas marcar a contradicao explicitamente. "Fonte A diz $184 bilhoes; Fonte B diz $214 bilhoes. Provavelmente devido a diferencas de definicao." Deixar o LLM raciocinar com consciencia da contradicao.

**Excluir ambas.** Se a contradicao nao pode ser resolvida, excluir ambos os lados. Nenhuma informacao e melhor que informacao errada.

Em um pipeline de linguagem natural, essas estrategias sao escritas em linguagem natural no prompt.
"Por favor, priorize a informacao mais recente."
Se o LLM segue isso consistentemente e, novamente, uma questao de probabilidade.

Em uma representacao estruturada, essas estrategias sao declaradas como politica.
"Em conflito mesma-entidade + mesma-propriedade: timestamp mais recente primeiro. Se timestamps sao iguais: maior confianca primeiro. Se confianca e igual: apresentar ambas."
A maquina executa. Nao e probabilidade.

---

## Posicao no Pipeline

Verificacao de consistencia vem depois da filtragem.

Verificacao -> Filtragem -> Consistencia.

Por que essa ordem?

Verificacao filtra erros de formato.
Filtragem remove informacao desnecessaria.
Verificacao de consistencia so precisa processar o que passou na verificacao e filtragem.

Verificacao de consistencia compara pares.
Para n afirmacoes, ha n(n-1)/2 pares.
1.000 gera aproximadamente 500.000 pares. 30 gera 435.

Se verificacao e filtragem reduzem 1.000 para 30,
o custo da verificacao de consistencia cai de 500.000 para 435 -- um milesimo.

Ordem importa.

---

## Resumo

Informacao que e individualmente valida, relevante e confiavel
pode se contradizer quando reunida como um conjunto.

Ha tres tipos de contradicao.
Contradicao temporal -- valores de diferentes pontos no tempo coexistem.
Contradicao entre fontes -- fontes diferentes apresentam valores diferentes.
Contradicao inferencial -- individualmente valida, mas logicamente incompativel quando combinada.

LLMs nao lidam bem com contradicoes.
Tendem a confiar na informacao do contexto,
deteccao de contradicao requer raciocinio,
e consistencia de resolucao nao e garantida.

Em linguagem natural, verificacao de consistencia e raciocinio de LLM do comeco ao fim.
Identidade de entidade, identidade de propriedade, extracao temporal, comparacao de valores -- tudo probabilistico e caro.

Em uma representacao estruturada, identificadores de entidade, tipos de propriedade e campos de tempo existem,
entao grande parte da deteccao de contradicao se converte em comparacao de campos e aritmetica.
Estrategias de resolucao tambem sao declaradas como politica.

Verificacao de consistencia vem depois da filtragem no pipeline.
Verificacao e filtragem devem reduzir o conjunto para que o numero de pares de comparacao diminua.
O barato vem primeiro, e verificacoes coletivas vem depois que verificacoes individuais estao feitas.
