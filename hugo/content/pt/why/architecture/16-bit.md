---
title: "Por Que 16 Bits?"
weight: 16
date: 2026-02-26T12:00:04+09:00
lastmod: 2026-02-26T12:00:04+09:00
tags: ["16-bit", "binario", "stream"]
summary: "Uma unica palavra atravessa tres mundos"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Uma Unica Palavra Atravessa Tres Mundos

---

## Tres Mundos

Existem tres mundos na ciencia da computacao.

**O mundo das redes.**
Os dados fluem como streams de bytes.
Bytes entram por sockets TCP e bytes saem.
O vocabulario do engenheiro de redes e: pacotes, cabecalhos e payloads.

**O mundo do armazenamento.**
Os dados sao persistidos em formatos de arquivo.
Escritos em disco, lidos do disco.
O vocabulario do engenheiro de armazenamento e: blocos, offsets e alinhamento.

**O mundo da IA.**
Os dados sao processados como sequencias de tokens.
LLMs recebem tokens e produzem tokens.
O vocabulario do engenheiro de IA e: embeddings, atencao e contexto.

Esses tres mundos falam linguas diferentes.
E entre eles, a traducao e sempre necessaria.

---

## O Custo da Traducao

Vamos rastrear o caminho que os dados percorrem em um sistema de IA moderno.

O conhecimento e armazenado em um arquivo. Como JSON ou texto puro.

Para entregar isso a uma IA:

1. Abrir o arquivo e ler o texto.
2. Parsear o texto. Se for JSON, interpretar a estrutura e extrair os campos.
3. Alimentar o texto extraido em um tokenizador.
4. O tokenizador converte o texto em uma sequencia de IDs de tokens.
5. A sequencia de tokens e alimentada no LLM.

Quando a IA gera uma resposta:

6. O LLM produz uma sequencia de tokens.
7. Decodificar os tokens de volta para texto.
8. Serializar o texto em um formato estruturado.
9. Escrever os dados serializados em um arquivo.

Uma simples operacao de "ler e escrever" requer nove etapas.

Cada etapa custa tempo.
Cada etapa custa memoria.
Cada etapa arrisca perda de informacao.

As etapas 3 e 4 -- o processo de tokenizacao -- sao notoriamente problematicas.
Como os limites de palavras da linguagem natural nao se alinham com os limites de tokens do tokenizador,
um nome proprio como "Yi Sun-sin" pode ser dividido em fragmentos arbitrarios,
ou uma unica unidade semantica acaba espalhada por multiplos tokens.

Esse e o preco de tres mundos falando linguas diferentes.

---

## E Se Uma Unica Unidade Atravessasse Todos os Tres Mundos?

Nesta linguagem, uma palavra tem 16 bits (2 bytes).

Uma unica palavra de 16 bits e simultaneamente tres coisas.

**Uma unidade do stream de bytes.**
Palavras de 16 bits chegam em um fluxo continuo pela rede.
Big Endian. Alinhadas em fronteiras de 2 bytes. Nenhum parsing adicional necessario.
Basta le-las na ordem em que chegam.

**Uma unidade do formato de arquivo.**
Grave o stream direto no disco, e isso e o seu arquivo.
Leia os bytes direto do disco e envie pela rede, e isso e o seu stream.
Sem serializacao. Sem desserializacao.

**Uma unidade do token do LLM.**
16 bits = 65.536 simbolos distintos.
Os tamanhos de vocabulario dos LLMs modernos geralmente variam de 50.000 a 100.000.
Modelos da familia GPT usam aproximadamente 50.000; modelos especializados em coreano cerca de 100.000.
65.536 fica exatamente no centro dessa faixa.
Uma palavra de 16 bits se torna um token do LLM.

Tres mundos compartilhando a mesma unidade.
A traducao desaparece.

---

## Zero Conversao, Zero Perda, Zero Overhead

Vamos ver o que isso significa concretamente.

**Abordagem convencional: 9 etapas**

```
[Arquivo] -> Ler -> Parsear -> Extrair texto -> Tokenizar -> [LLM]
[LLM] -> Decodificar -> Serializar -> Escrever -> [Arquivo]
```

**Abordagem de stream binario: 1 etapa**

```
[Arquivo/Stream] -> [LLM]
[LLM] -> [Arquivo/Stream]
```

Leia um arquivo, e ele ja e uma sequencia de tokens.
Grave a sequencia de tokens que o LLM produz, e ela ja e um arquivo.
Pegue um stream da rede e alimente diretamente no LLM.

Zero conversao. Zero parsing. Zero tokenizacao.
Zero perda. Zero overhead.

---

## Por Que Nao 8 Bits?

8 bits dao 256 simbolos distintos.

256 simbolos sao poucos demais para representar o mundo.
Atribua o alfabeto, digitos e pontuacao basica, e metade do espaco ja se foi.

Se voce usar 8 bits como sua unidade fundamental,
a maioria dos tokens significativos acaba exigindo 2 ou mais bytes.
Isso forca codificacao de comprimento variavel,
e comprimento variavel torna o parsing complexo.

Adequado como unidade de stream de bytes,
mas insuficiente como unidade de token.

---

## Por Que Nao 32 Bits?

32 bits dao aproximadamente 4,3 bilhoes de simbolos distintos.

O poder expressivo e mais do que suficiente -- muito mais do que o necessario.
Mas o problema e a eficiencia.

O pacote mais frequente neste formato e o Tiny Verb Edge, com 2 palavras.
Com 16 bits por palavra, sao 4 bytes. Com 32 bits por palavra, sao 8 bytes.
O pacote mais comum dobra de tamanho.

Do ponto de vista do LLM, tambem ha um problema.
Se um unico token tem 32 bits, apenas metade dos tokens cabem na mesma janela de contexto.
Dado que o comprimento de contexto do LLM e um recurso escasso hoje,
o espaco que um token ocupa se torna ineficiente em relacao a informacao que ele carrega.

Uma palavra de 32 bits e excessiva como token para esta linguagem.

---

## Por Que Nao Comprimento Variavel?

UTF-8 e uma codificacao de comprimento variavel.
O comprimento do caractere varia de 1 byte a 4 bytes dependendo do caractere.

Isso oferece vantagens em eficiencia de armazenamento,
mas introduz uma fraqueza fatal na eficiencia de processamento.

Para encontrar o n-esimo caractere, voce precisa contar desde o inicio.
Acesso aleatorio e impossivel.
Processamento paralelo SIMD se torna dificil.

Esta linguagem usa palavras de 16 bits de largura fixa como sua unidade fundamental.
A posicao da n-esima palavra e sempre n * 2 bytes.
Acesso aleatorio e O(1).
SIMD pode comparar multiplas palavras em uma unica instrucao.
GPUs podem escanear bilhoes de palavras em paralelo.

No entanto, no nivel do pacote, comprimento variavel ainda e permitido.
Um Tiny Verb Edge tem 2 palavras; um Event6 Edge pode ter ate 8 palavras.
A unidade de palavra e fixa, mas a unidade de pacote e flexivel.

A eficiencia de processamento da largura fixa combinada com a expressividade do comprimento variavel.
A palavra de 16 bits alcanca ambos simultaneamente.

---

## O Caminho Que o Unicode Provou

Unicode e o padrao de codificacao mais bem-sucedido que a humanidade ja criou.

A unidade basica do UTF-16 e 16 bits (2 bytes).
Ele representa os 65.536 caracteres do Plano Multilingue Basico (BMP) em uma unica palavra,
e se estende a caracteres alem dele usando pares substitutos (2 palavras = 4 bytes).

Nos simplesmente seguimos essa estrutura comprovada.

Representar 65.536 primitivas semanticas basicas em uma unica palavra,
e estender pacotes compostos atraves de multiplas palavras.

Assim como o Unicode expressa cada caractere do mundo
sobre a unidade basica de "um caractere = 2 bytes",
esta linguagem expressa cada elemento do raciocinio da IA
sobre a unidade basica de "uma palavra = 2 bytes".

---

## Compatibilidade Retroativa e Extensao Superior

Outra forca dos 16 bits e o alinhamento.

16 e multiplo de 8, divisor de 32, divisor de 64 e divisor de 128.

Isso significa que o alinhamento nunca se quebra, nao importa em qual direcao voce estenda.

E se a arquitetura do transformer mudar no futuro
e os tokens se tornarem 32 bits?
Duas palavras de 16 bits fazem um token. Sem problemas de alinhamento.

E 64 bits?
Quatro palavras de 16 bits fazem um token. Ainda sem problemas de alinhamento.

Por outro lado, e se um sistema embarcado de 8 bits processar este formato?
Simplesmente leia cada palavra de 16 bits como um byte alto e um byte baixo.

A compatibilidade retroativa deve ser mantida absolutamente.
A palavra de 16 bits garante isso no nivel fisico.

Nao podemos prever o tamanho de palavra das inteligencias futuras,
mas o alinhamento multiplo de 16 bits garante compatibilidade com qualquer tamanho.

---

## A Estrutura Tripla

Vamos resumir.

Uma unica palavra de 16 bits e simultaneamente tres coisas.

| Mundo | Papel de Uma Palavra |
|-------|---------------------|
| Rede | Unidade do stream de bytes |
| Armazenamento | Unidade do formato de arquivo |
| IA | Unidade do token do LLM |

Uma unica unidade atravessa todos os tres mundos.

Armazene um stream como esta, e e um arquivo.
Leia um arquivo como esta, e sao tokens.
Envie tokens como estao, e e um stream.

Sem conversao.
Sem traducao.
Sem perda.

E por isso que 16 bits.
Nao 8 bits, nao 32 bits, nao comprimento variavel.
O numero que fica precisamente na interseccao de tres mundos.

16.
