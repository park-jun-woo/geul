---
title: "Por Que Exploracao e Necessaria"
weight: 7
date: 2026-02-26T12:00:07+09:00
lastmod: 2026-02-26T12:00:07+09:00
tags: ["exploracao", "busca", "escala"]
summary: "Quando o indice excede a janela, o proprio paradigma de busca atinge seu limite"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Quando o indice excede a janela, o proprio paradigma de busca atinge seu limite.

---

## A Busca Teve Sucesso

Discutimos os limites do RAG.
A imprecisao da similaridade de embedding, a arbitrariedade da divisao em chunks, a impossibilidade do julgamento de qualidade.

Mas essa discussao era sobre a qualidade da busca.
"Como devemos buscar com mais precisao?"

Agora uma pergunta diferente deve ser feita.
Suponha que a busca e perfeita.
Suponha que ela retorna apenas informacao precisamente relevante para a consulta.

Ainda ha casos em que nao funciona.

---

## O Problema de Escala

Uma base de conhecimento interna tem 1.000 afirmacoes.
Ha um indice. Coloque o indice no contexto. Consulte. Recupere resultados.
Funciona.

Afirmacoes crescem para 100.000.
O indice fica maior. Ainda cabe na janela. Funciona.

Afirmacoes crescem para 10 milhoes.
O proprio indice excede a janela.

Isso nao e um problema de qualidade de busca.
Nao importa quao precisa a busca seja,
se o indice que deve ser consultado para buscar nao cabe na janela,
a busca nem pode comecar.

E o conhecimento cresce.
Documentos corporativos aumentam todo dia.
O que um agente aprendeu continua acumulando.
O conhecimento do mundo nao encolhe.

Uma janela maior resolve isso?
Se 128K se torna 1M se torna 10M?
Se o conhecimento chega a 100M, o mesmo problema se repete.
A janela e sempre finita, e o conhecimento sempre cresce.
Esse desequilibrio e permanente.

---

## A Diferenca Entre Busca e Exploracao

Busca obtem resultados com uma unica consulta.

Consulta: "Lucro operacional da Samsung Electronics Q3 2024"
-> Resultado: 9,18 trilhoes de won.

Um disparo. Feito.

Exploracao alcanca resultados atraves de multiplas etapas.

Etapa 1: Ver o mapa de conhecimento de nivel superior. "Corporacoes," "Industrias," "Macroeconomia," "Tecnologia"...
-> Selecionar "Corporacoes."

Etapa 2: Ver o mapa de corporacoes. "Samsung Electronics," "SK Hynix," "Hyundai Motor"...
-> Selecionar "Samsung Electronics."

Etapa 3: Ver o mapa da Samsung Electronics. "Financeiro," "RH," "Tecnologia," "Juridico"...
-> Selecionar "Financeiro."

Etapa 4: Ver o mapa financeiro. "Resultados trimestrais," "Resultados anuais," "Planos de investimento"...
-> Selecionar "Resultados trimestrais."

Etapa 5: Recuperar "Q3 2024" dos resultados trimestrais.
-> Lucro operacional: 9,18 trilhoes de won.

O resultado e o mesmo.
O processo e diferente.

Busca e perguntar "Voce tem isso?"
Exploracao e rastrear "Onde pode estar?"

Busca requer que o indice seja visivel para quem consulta. O indice inteiro deve ser acessivel.
Exploracao so precisa ver a camada atual do mapa. A cada passo, apenas uma camada entra na janela.

---

## A Analogia da Biblioteca

Voce visita uma biblioteca de bairro.
Ela tem 3.000 livros.
Voce pergunta ao bibliotecario: "Voce tem uma biografia de Yi Sun-sin?"
O bibliotecario lembra: "Esta no final da estante 3."
Busca. Funciona.

Voce visita a Biblioteca Nacional.
Ela tem 10 milhoes de volumes.
Voce pergunta ao bibliotecario: "Voce tem uma biografia de Yi Sun-sin?"
O bibliotecario tambem nao sabe. Ninguem memoriza 10 milhoes de volumes.

Em vez disso, ha um sistema de classificacao.

Voce confere o diretorio do terreo. -> A secao de "Historia" fica no 3o andar.
Voce vai ao 3o andar. -> "Historia Coreana" fica na ala leste.
Voce vai a ala leste. -> "Dinastia Joseon" fica na fileira D.
Voce vai a fileira D. -> "Figuras" fica na 3a secao da fileira D.
Voce busca na 3a secao. -> Ha uma biografia de Yi Sun-sin.

A capacidade de memoria do bibliotecario nao mudou.
A escala da biblioteca mudou.
O metodo mudou de perguntar ao bibliotecario (busca) para percorrer o sistema de classificacao (exploracao).

Eis o ponto-chave.
A cada passo, o tamanho do que deve ser visto cabe na capacidade de memoria do bibliotecario.
O diretorio do terreo. O mapa de zonas do 3o andar. A lista de fileiras da ala leste. A lista de secoes da fileira D.
Tudo cabe em um unico olhar.

O catalogo completo de todo o acervo nao cabe em um unico olhar.
Mas o mapa de cada andar cabe.

E assim que exploracao difere de busca.
Voce nao precisa ver o todo de uma vez.
Voce so precisa julgar a proxima direcao de onde voce esta agora.

---

## Mapas de Mapas

Em termos tecnicos, isso e uma estrutura hierarquica de mapas.

**Mapa nivel 1**: a classificacao de nivel superior de todo o conhecimento.
"Esta base de conhecimento contem informacoes sobre corporacoes, industrias, macroeconomia e tecnologia."
Dezenas de itens. Cabe na janela.

**Mapa nivel 2**: as subcategorias de cada classificacao de nivel superior.
"A categoria corporacoes contem Samsung Electronics, SK Hynix, Hyundai Motor..."
Dezenas a centenas de itens. Cabe na janela.

**Mapa nivel 3**: as categorias detalhadas de cada subcategoria.
"Samsung Electronics contem Financeiro, RH, Tecnologia, Juridico..."
Dezenas de itens. Cabe na janela.

**Afirmacoes reais**: as informacoes concretas apontadas pelo mapa de nivel mais baixo.
"O lucro operacional da Samsung Electronics no Q3 2024 foi de 9,18 trilhoes de won."

Se o tamanho de cada camada cabe na janela,
exploracao e possivel independentemente da escala total do conhecimento.

Mesmo com 10 milhoes de afirmacoes,
se cada camada tem 100 itens, voce alcanca o alvo em 5 passos de exploracao.
100 -> 100 -> 100 -> 100 -> 100 = cobertura de ate 10 bilhoes.
A cada passo, apenas 100 itens entram na janela.

Esse e o mesmo modo como uma B-tree encontra dados no disco.
Ela nao carrega todos os dados na memoria.
Ela le apenas o no atual da arvore e move para o proximo.
Dados de qualquer escala podem ser explorados independentemente do tamanho da memoria.

A janela de contexto e memoria.
A base de conhecimento e disco.
O mapa e um no de B-tree.

---

## O Agente Caminha

Na exploracao em multiplas etapas, quem seleciona a direcao em cada passo?

O agente.

Coloque o mapa nivel 1 no contexto.
O agente le, compara com a consulta e seleciona a direcao "Corporacoes."

Solicite o mapa nivel 2.
O mapa de subcategoria de corporacoes entra no contexto.
O agente le e seleciona a direcao "Samsung Electronics."

Solicite o mapa nivel 3.
O agente seleciona "Financeiro."

Isso e uso de ferramentas pelo agente.
Ler um mapa e uma chamada de ferramenta.
Selecionar uma direcao e um julgamento.
Solicitar o proximo mapa e a proxima chamada de ferramenta.

Na busca, o agente consulta uma vez e recebe um resultado. Passivo.
Na exploracao, o agente faz multiplos julgamentos e seleciona direcoes. Ativo.

E aqui que engenharia de contexto encontra design de agentes.
O que entra no contexto e determinado passo a passo pelo julgamento do agente.
A construcao do contexto muda de montagem estatica para exploracao dinamica.

---

## Esse Problema Quase Nao e Discutido Hoje

Olhando as discussoes na comunidade RAG,
a maioria da energia esta focada na qualidade da busca.

Modelos de embedding melhores.
Estrategias de chunking melhores.
Arquiteturas de reranker.
Busca hibrida.
Graph RAG.

Tudo importante.
Tudo sobre "como obter melhores resultados de uma unica busca."

"E se uma unica busca nao for suficiente?" quase nao e discutido.

O ponto em que o indice excede a janela.
O ponto em que os resultados sao numerosos demais para caber.
O ponto em que a escala do conhecimento quebra a premissa do proprio paradigma de busca.

Esse ponto esta chegando.
O conhecimento cresce e a janela e finita.

A maioria das solucoes atuais sao evasivas.
Recuperar apenas os top k. Descartar o resto.
Aumentar a janela. Custos aumentam.
Particionar o conhecimento. Armazenamentos vetoriais separados por dominio.

Todas encontram o mesmo problema novamente quando a escala cresce mais.

---

## Pre-requisitos para Exploracao

Para que exploracao funcione, o conhecimento deve estar em uma estrutura exploravel.

**Hierarquia deve existir.** Se o conhecimento esta disposto de forma plana, exploracao e impossivel. Um armazenamento de vetores de embedding e plano. Todos os chunks estao no mesmo nivel. Nao ha hierarquia, entao o conceito de "ir mais fundo" nao existe.

**Cada camada deve caber na janela.** Se um unico mapa excede a janela, a exploracao falha. O numero de opcoes em cada nivel da hierarquia deve ser de tamanho apropriado. Esse e um problema de design de classificacao.

**Caminhos devem ser diversos.** Deve ser possivel alcancar a mesma informacao por multiplos caminhos. Via "Samsung Electronics -> Financeiro -> Lucro operacional" ou via "Industria de semicondutores -> Principais empresas -> Samsung Electronics -> Resultados." Porque o caminho natural varia dependendo da pergunta. Se o criterio de classificacao e fixo em um so, ele se encaixa em algumas perguntas e nao em outras.

Uma estrutura de pastas tem hierarquia mas apenas um caminho.
Um arquivo pertence a apenas uma pasta.
Somente o caminho "Samsung Electronics/Financeiro/Lucro operacional" existe.
Quando uma pergunta sobre "a industria de semicondutores" chega, exploracao natural por essa estrutura de pastas e impossivel.

Um grafo tem tanto hierarquia quanto caminhos diversos.
Um unico no pode ser conectado a multiplos nos pais.
O no Samsung Electronics pode ser alcancado via um caminho "Corporacoes," um caminho "Industria de semicondutores" ou um caminho "Empresas listadas no KOSPI."
Independentemente do contexto de onde a pergunta se origina, um caminho natural existe.

---

## Esse e um Problema Nao Resolvido

Ha algo que precisa ser dito honestamente.

A necessidade de exploracao em multiplas etapas e clara.
Mas nao ha um sistema padrao que implemente isso efetivamente ainda.

Como voce gera automaticamente a hierarquia de mapas?
Como voce determina o tamanho apropriado de cada camada?
O que acontece quando o agente seleciona a direcao errada?
O que acontece com a latencia conforme a profundidade de exploracao aumenta?

Essas sao perguntas em aberto.

Mas o fato de que um problema nao esta resolvido
nao significa que o problema nao existe.

O conhecimento esta crescendo.
A janela e finita.
O ponto em que busca sozinha nao e suficiente esta chegando.

Exploracao deve estar pronta como resposta para esse ponto.
Se nao estiver pronta,
as unicas opcoes restantes sao aumentar a janela ou descartar conhecimento.

---

## Resumo

Busca retorna resultados com uma unica consulta.
Quando a escala do conhecimento cresce o suficiente, isso nao e suficiente.
Porque o proprio indice excede a janela.

Exploracao segue mapas hierarquicos, selecionando direcoes conforme desce.
O que deve ser visto a cada passo cabe na janela.
Cada passo e finito independentemente da escala total.
Assim como uma B-tree encontra dados sem carregar o disco inteiro na memoria.

O agente julga a direcao a cada passo.
A construcao do contexto muda de montagem estatica para exploracao dinamica.
E aqui que engenharia de contexto encontra design de agentes.

Para que exploracao funcione, o conhecimento deve ser hierarquico, cada camada deve ser finita e os caminhos devem ser diversos.
Uma estrutura de pastas tem apenas um caminho. Um grafo tem caminhos diversos.

Esse ainda e um problema nao resolvido sem solucao padrao.
Mas enquanto o conhecimento cresce e a janela e finita, e um problema que deve ser resolvido.
