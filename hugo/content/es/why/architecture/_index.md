---
title: "Arquitectura"
date: 2026-02-26T12:00:00+09:00
image: "/images/og-default.webp"
summary: "Cómo se construye GEUL: indexación semánticamente alineada, unidades de palabra de 16 bits, memoria estructurada y representación del conocimiento basada en afirmaciones."
---

## Subtemas

### Por que 16 bits
Todos los datos en GEUL son en unidades de 16 bits (1 palabra). Es la unidad minima que combina la eficiencia del codigo maquina con el significado del lenguaje humano en una sola palabra.

### Por que cachear el razonamiento como codigo
Descartar los resultados cada vez que una IA razona es un desperdicio de computacion. Registrar el razonamiento en un lenguaje estructurado permite la reutilizacion y la acumulacion.

### Por que afirmaciones, no hechos
Las oraciones en lenguaje natural parecen hechos, pero en realidad son afirmaciones de alguien. Incorporar estructuralmente la fuente, el momento y la confianza reduce el margen para la alucinacion.

### Por que un indice semanticamente alineado
SIDX es un identificador de 64 bits que codifica el significado en los propios bits. El tipo se puede determinar solo con los bits superiores, y cuantos menos bits se llenen, mas abstracta es la expresion.

### Por que es necesaria la memoria estructurada
La ventana de contexto de un LLM es finita. Para encajar experiencia infinita en una ventana finita, la memoria debe estar estructurada.
