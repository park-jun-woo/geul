---
title: "Por Que a Era da Engenharia de Prompt Acabou"
weight: 1
date: 2026-02-26T12:00:12+09:00
lastmod: 2026-02-26T12:00:12+09:00
tags: ["prompt", "contexto", "engenharia"]
summary: "De como voce diz para o que voce mostra — o jogo mudou"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Por Que a Era da Engenharia de Prompt Acabou

### De "como voce diz" para "o que voce mostra" — o jogo mudou.

---

### Engenharia de Prompt como Profissao

Em 2023, uma nova profissao surgiu.

Engenheiro de prompt.

"Pense passo a passo."
"Voce e um especialista com 20 anos de experiencia."
"Deixe-me mostrar alguns exemplos primeiro."

Frases como essas se tornaram know-how que valia dezenas de milhares de dolares. A mesma pergunta produzia respostas dramaticamente diferentes da IA dependendo de como voce a formulava.

A engenharia de prompt genuinamente funcionava.
Uma unica linha de Chain-of-Thought elevava notas de matematica em 20%.
Uma unica frase atribuindo um papel mudava a profundidade da expertise.
Tres exemplos few-shot davam controle completo sobre o formato de saida.

Isso nao era hype. Era real.
Entao por que esta acabando?

---

### Por Que Funcionava: Porque os Modelos Eram Burros o Suficiente

Olhe por que a engenharia de prompt funcionava a partir de primeiros principios. E simples.

LLMs iniciais eram ruins em captar a intencao do usuario.
Diga "resuma" e eles reescreviam em vez disso.
Diga "compare" e eles listavam em vez disso.

Porque o modelo lia errado a intencao,
a habilidade de transmitir intencao precisamente se tornou valiosa.
Engenharia de prompt era essencialmente "interpretacao" —
traduzir a intencao humana em uma forma que o LLM pudesse entender.

Para que interpretacao seja valiosa, deve haver uma barreira linguistica.

---

### O Que Mudou: Os Modelos Ficaram Inteligentes

De GPT-3.5 para GPT-4. De Claude 2 para Claude 3.5.
A cada geracao, a capacidade dos modelos de captar intencao melhorou dramaticamente.

Diga "resuma" e eles resumem.
Diga "compare" e eles comparam.
Mesmo sem ser dito para "pensar passo a passo", eles decompoe problemas complexos em etapas por conta propria.

A barreira linguistica diminuiu.
O valor da interpretacao encolheu.

Tecnicas de prompt que produziam diferencas dramaticas em 2023
produzem apenas diferencas marginais em 2025.
Quando o modelo e inteligente o suficiente, a formulacao importa cada vez menos.

Entao o que importa em vez disso?

---

### A Janela de Contexto: Uma Lei da Fisica

LLMs tem uma restricao fisica.

A janela de contexto.

Seja 128K tokens ou 1M tokens, e finita.
Somente informacao que cabe dentro desse espaco finito influencia o raciocinio.
Informacao fora da janela, nao importa o quao importante, pode nao existir.

Isso e independente do tamanho do modelo.
Mesmo com um trilhao de parametros, a janela de contexto e finita.
Mesmo com dados de treinamento abrangendo toda a internet, a janela de contexto e finita.

Nao importa o quao inteligente o modelo seja,
se informacao errada entrar no contexto, ele produz respostas erradas.
Se informacao irrelevante preencher o contexto, ele perde o que importa.
Se informacao necessaria estiver faltando no contexto, e como se fosse desconhecida.

Engenharia de prompt era um problema de "como voce diz".
O novo jogo e um problema de "o que voce mostra".

Isso e engenharia de contexto.

---

### Analogia: A Prova com Consulta

Aqui esta uma analogia para a diferenca entre engenharia de prompt e engenharia de contexto.

Engenharia de prompt e escrever bem as questoes da prova.
Em vez de "escolha a resposta correta abaixo",
escreva "derive passo a passo a resposta que satisfaz todas as seguintes condicoes" —
e o estudante da uma resposta melhor.

Engenharia de contexto e a questao de quais livros voce leva para uma prova com consulta.
Nao importa o quao bem as questoes da prova foram escritas,
se o estudante trouxe os livros errados, nao consegue responder.
O numero de livros que voce pode trazer e limitado.
Quais livros voce traz determina sua nota.

Quando o modelo era burro, o formato da questao (prompt) importava.
Quando o modelo e inteligente, o material de referencia (contexto) importa.

---

### A Era dos Agentes Acelera a Mudanca

Essa mudanca esta sendo acelerada com o surgimento dos agentes.

Engenharia de prompt e escrita por humanos toda vez.
Humanos escrevem a pergunta, humanos explicam o contexto, humanos especificam o formato.

Agentes sao diferentes.
Agentes raciocinam por conta propria, chamam ferramentas e colaboram com outros agentes.
Em cada etapa, eles devem compor o contexto por conta propria.

Um agente chamou uma API externa e recebeu dados.
Esses dados precisam entrar no contexto para a proxima rodada de raciocinio.
Quais partes entram e quais ficam de fora?
Quais resultados de raciocinio anteriores sao mantidos e quais sao descartados?
Informacao enviada por outro agente pode ser confiavel?

Um humano nao pode tomar todas essas decisoes toda vez.
Para que agentes operem autonomamente,
a composicao de contexto deve ser automatizada.

Engenharia de prompt era uma habilidade humana.
Engenharia de contexto deve ser uma capacidade do sistema.

---

### A Engenharia de Prompt Nao Esta Desaparecendo

Vou prevenir um mal-entendido.

Nao estou dizendo que a engenharia de prompt esta se tornando sem sentido.
System prompts ainda sao importantes.
Especificacao de formato de saida ainda e necessaria.
Declarar papeis e restricoes ainda e eficaz.

O que esta encolhendo e a parcela que a engenharia de prompt ocupa.

Se 70% da qualidade da saida era determinada pelo prompt em 2023,
em 2025, 30% e determinado pelo prompt e 70% pelo contexto.

A proporcao se inverteu.

E essa tendencia nao esta se revertendo.
Os modelos vao continuar ficando mais inteligentes,
e quanto mais inteligentes ficam, menos a formulacao importa
e mais o contexto importa.

---

### Mas a Engenharia de Contexto Nao Tem Infraestrutura

Aqui esta o ponto crucial.

A engenharia de prompt tinha ferramentas.
Templates de prompt, bibliotecas de prompt, frameworks de teste de prompt.
Todo um ecossistema para gerenciar sistematicamente "como voce diz" foi construido.

A engenharia de contexto ainda nao tem isso.

Veja como o contexto e tratado na pratica agora.

Tamanhos de chunks de pipelines RAG sao ajustados manualmente.
Informacoes de fundo sao escritas em system prompts manualmente.
O que armazenar na memoria de um agente e projetado manualmente.
Quais resultados de busca colocar no contexto e decidido manualmente.

Tudo e manual.

E a materia-prima de todo esse trabalho manual e linguagem natural.
Documentos em linguagem natural sao recortados em linguagem natural e colados em um contexto de linguagem natural.

Linguagem natural tem baixa densidade de informacao.
Sem fontes. Sem niveis de confianca. Sem timestamps.
Tokens desnecessarios sao consumidos para transmitir o mesmo significado.
Nao ha como automatizar o julgamento de qualidade.

Isso se assemelha a era pre-engenharia de prompt.
A engenharia de prompt tambem era manual no inicio.
Dependia da intuicao e experiencia individual.
Entao ferramentas e metodologias surgiram e ela se tornou sistematizada.

A engenharia de contexto esta nesse estagio anterior agora.
O problema foi reconhecido, mas a infraestrutura nao existe.

---

### O Que a Infraestrutura Precisa

Para que a engenharia de contexto passe de trabalho manual para um sistema,
no minimo o seguinte e necessario.

**Compressao.** Uma forma de encaixar mais significado na mesma janela.
Remova a cola gramatical da linguagem natural e deixe apenas o significado,
e o tamanho efetivo da janela multiplica — sem mudar o modelo.

**Indexacao.** Uma forma de encontrar a informacao certa com precisao.
Busca baseada em estrutura semantica, nao similaridade de embedding.
Uma busca onde procurar "receita da Apple" nao traga "valor nutricional da maca".

**Validacao.** Uma forma de rejeitar mecanicamente informacao que nao atende a especificacao.
Assim como um compilador Go detecta variaveis nao utilizadas como erros,
afirmacoes sem fontes e fatos sem timestamps devem ser filtrados antes de entrar no contexto.
As verificacoes mais baratas e deterministicas devem vir primeiro.

**Filtragem.** Uma forma de julgar a qualidade semantica.
Se a validacao olha para a forma, a filtragem olha para o conteudo.
Relevancia, confiabilidade, atualidade. Essa informacao e realmente necessaria para esta rodada de raciocinio?

**Consistencia.** Uma forma de garantir a coerencia interna do conjunto de informacoes selecionadas.
Pecas de informacao individualmente boas podem se contradizer quando combinadas.
Se o CEO de 2020 e o CEO de 2024 entrarem no contexto simultaneamente,
o LLM se confunde.

**Composicao.** Uma forma de otimizar posicionamento e estrutura dentro da janela.
A mesma informacao recebe pesos de atencao diferentes dependendo de onde e colocada.
Na frente ou atras? Como e agrupada?

**Acumulacao.** Uma forma do sistema aprender e crescer ao longo do tempo.
Caching e a reutilizacao de resultados individuais.
Acumulacao e aprender quais composicoes de contexto produziram bons resultados,
e fazer crescer a propria base de conhecimento.

Esses sete sao a stack completa da infraestrutura de engenharia de contexto.

---

### Isso Nao e Sobre Nenhuma Ferramenta Especifica

Vou ser franco.

Quem constroi essa infraestrutura e uma questao em aberto.
Uma ferramenta pode resolver tudo,
ou multiplas ferramentas podem lidar com uma camada cada.

Mas o fato de que infraestrutura e necessaria nao e uma questao em aberto.

Que a janela de contexto e finita e um fato fisico.
Mesmo que a janela cresca 10x, a informacao do mundo cresce mais rapido.
Que a linguagem natural tem baixa densidade de informacao e um fato estrutural.
Que agentes precisam de gerenciamento automatizado de contexto para operar autonomamente e uma necessidade logica.

Assim como a engenharia de prompt precisou de ferramentas,
a engenharia de contexto precisa de ferramentas.
Mas desta vez, a natureza das ferramentas e diferente.

Ferramentas de engenharia de prompt eram mais proximas de editores de texto.
Ferramentas de engenharia de contexto sao mais proximas de compiladores.

Comprimir informacao, indexa-la, valida-la, filtra-la,
verificar consistencia, otimizar posicionamento e acumular resultados.
Isso nao e edicao. Isso e engenharia.

E por isso que se chama engenharia de "contexto".

---

### Resumo

A engenharia de prompt era valiosa quando os modelos eram burros.
Porque os modelos nao liam a intencao, a habilidade de transmitir bem a intencao importava.

Conforme os modelos ficaram mais inteligentes, o jogo mudou.
De "como voce diz" para "o que voce mostra".
De prompt para contexto.

O surgimento dos agentes acelera essa mudanca.
Humanos nao podem montar contexto toda vez.
O sistema deve faze-lo por conta propria.

Mas agora, a engenharia de contexto nao tem infraestrutura.
Linguagem natural esta sendo recortada e colada manualmente.

A infraestrutura necessaria tem sete camadas:
compressao, indexacao, validacao, filtragem, consistencia, composicao, acumulacao.

Nao e a era da engenharia de prompt que esta acabando.
E a era em que a engenharia de prompt sozinha era suficiente.
