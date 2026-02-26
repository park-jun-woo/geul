---
title: "Arquitetura"
date: 2026-02-26T12:00:00+09:00
image: "/images/og-default.webp"
summary: "Como o GEUL é construído: indexação semanticamente alinhada, unidades de palavra de 16 bits, memória estruturada e representação de conhecimento baseada em afirmações."
---

## Subtopicos

### Por que 16 bits
Todos os dados em GEUL sao em unidades de 16 bits (1 palavra). E a unidade minima que combina a eficiencia do codigo de maquina com o significado da linguagem humana em uma unica palavra.

### Por que armazenar o raciocinio como codigo
Descartar resultados toda vez que uma IA raciocina e desperdicio computacional. Registrar o raciocinio em uma linguagem estruturada permite reutilizacao e acumulacao.

### Por que afirmacoes, nao fatos
Sentencas em linguagem natural parecem fatos, mas na verdade sao afirmacoes de alguem. Incorporar estruturalmente a fonte, o momento e a confianca reduz o espaco para alucinacao.

### Por que um indice semanticamente alinhado
SIDX e um identificador de 64 bits que codifica o significado nos proprios bits. O tipo pode ser determinado apenas pelos bits superiores, e quanto menos bits preenchidos, mais abstrata e a expressao.

### Por que a memoria estruturada e necessaria
A janela de contexto de um LLM e finita. Para encaixar experiencia infinita em uma janela finita, a memoria deve ser estruturada.
