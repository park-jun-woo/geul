---
title: "Por que RAG no es suficiente"
weight: 2
date: 2026-02-26T12:00:11+09:00
lastmod: 2026-02-26T12:00:11+09:00
tags: ["RAG", "busqueda", "embedding"]
summary: "Parecer relevante y ser relevante no son lo mismo"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Parecer relevante y ser relevante no son lo mismo.

---

## RAG es el estandar actual

A partir de 2024, RAG es la forma mas comun en que las empresas utilizan los LLM.

Retrieval-Augmented Generation.
Buscar documentos externos, insertarlos en el contexto y hacer que el modelo responda basandose en ellos.

RAG funciona.
Permite que los LLM consulten documentos internos con los que nunca fueron entrenados.
Les permite reflejar informacion actualizada.
Reduce significativamente las alucinaciones.

Sin RAG, la adopcion empresarial de los LLM habria sido mucho mas lenta.
RAG es una tecnologia que merece respeto.

Pero RAG tiene limitaciones fundamentales.
Estas limitaciones no se resuelven construyendo un mejor RAG.
Se derivan de la premisa misma de RAG.

---

## Como funciona RAG

El nucleo de RAG son tres pasos.

**Paso 1: Dividir documentos en fragmentos.**
PDFs, wikis y documentos internos se dividen en tamanos fijos (normalmente 200--500 tokens).

**Paso 2: Convertir cada fragmento en un vector de embedding.**
Un vector de valores reales de cientos a miles de dimensiones.
El "significado" del texto mapeado a un unico punto en el espacio vectorial.

**Paso 3: Cuando llega una consulta, encontrar vectores similares.**
La consulta tambien se convierte en un vector.
Se seleccionan los 5--20 fragmentos con mayor similitud coseno y se insertan en el contexto.

Simple y elegante.
Y aqui residen tres problemas fundamentales.

---

## Problema 1: Similar no es relevante

La similitud de embedding mide "si dos textos usan palabras similares en contextos similares."

Eso no es relevancia.

Ejemplo.

Consulta: "Cual fue el ingreso de Apple en el Q3 2024?"

Los fragmentos que la busqueda por embedding podria devolver:
- "El ingreso de Apple en el Q3 2024 fue de $94.9 mil millones." -- Relevante
- "El ingreso de Apple en el Q3 2023 fue de $81.8 mil millones." -- Similar pero periodo distinto
- "El ingreso de Samsung Electronics en el Q3 2024 fue de 79 billones de won." -- Similar pero empresa distinta
- "Una tarta de manzana tiene unas 296 kcal." -- Coincidencia de palabras clave

La similitud de embedding no puede distinguir estos cuatro casos.
En el espacio vectorial, "ingreso de Apple" se agrupa en una sola region.
Ya sea 2023 o 2024, Apple o Samsung --
la distancia vectorial no los separa de forma fiable.

Agregar un reranker mejora las cosas.
Pero un reranker tambien lee y juzga texto en lenguaje natural,
asi que el problema fundamental de ambiguedad persiste.

La busqueda basada en estructura semantica es diferente.
Si "Apple" como entidad tiene un identificador unico,
nunca se confunde con "manzana" la fruta.
Si "Q3 2024" es un campo temporal,
se distingue mecanicamente de "Q3 2023."

No es necesario calcular similitud.
Coincide o no? Si o no.

---

## Problema 2: Los fragmentos no son unidades de significado

Mira de nuevo el primer paso de RAG.
"Dividir documentos en fragmentos."

Esa "division" es el problema.

Cuando divides un documento en unidades de 500 tokens,
el significado se corta por la mitad.
Un parrafo abarca dos fragmentos.
La premisa y la conclusion de un argumento quedan separadas.

"Yi Sun-sin enfrento 133 barcos con solo 12 en la Batalla de Myeongnyang" esta en el Fragmento A,
y "los historiadores cuestionan estas cifras" esta en el Fragmento B.
Si solo se recupera el Fragmento A para una consulta,
la informacion de confianza entra al contexto ya perdida.

Hacer fragmentos mas grandes? Consumen mas de la ventana.
Hacer fragmentos mas pequenos? Se corta mas contexto.
Agregar solapamiento? Desperdicias la ventana con duplicados.

No importa como ajustes, el problema fundamental es el mismo.
Dividir texto en lenguaje natural por cantidad de tokens
es lo mismo que dividir el significado por cantidad de tokens.
El significado tiene un tamano inherente,
y dividirlo por una unidad ajena causa problemas.

En una representacion estructurada, las unidades de significado son explicitas.
Una predicacion es un edge.
Un edge no se divide.
La busqueda opera a nivel de edge.
No hay corte en medio del significado.

---

## Problema 3: La calidad de los resultados recuperados es desconocida

RAG devolvio 5 fragmentos.
Antes de poner estos 5 en el contexto, hay preguntas que hacer.

Cual es la fuente de esta informacion?
Cual es la fecha de referencia?
Que tan segura es?
Estos 5 se contradicen entre si?

En fragmentos de lenguaje natural, no puedes saber estas cosas.

La fuente puede o no estar mencionada en algun lugar del fragmento como lenguaje natural.
La referencia temporal puede estar en algun lugar del documento, o pudo haberse perdido al dividir el fragmento.
La confianza no tiene un campo estructural en el lenguaje natural, asi que casi siempre esta ausente.
Verificar contradicciones requiere leer los 5 fragmentos y razonar sobre ellos.

Al final, tienes que delegar el juicio de calidad al LLM.
Usas RAG para reducir los costos de llamadas al LLM,
pero llamas al LLM para verificar los resultados de RAG.

En una representacion estructurada, la fuente, el tiempo y la confianza son campos.
"Excluir declaraciones sin fuente" es una linea de consulta.
"Excluir informacion anterior a 2023" es una comparacion de campo.
"Excluir confianza inferior a 0.5" es una comparacion numerica.
No se necesita llamar al LLM.

---

## La premisa fundamental de RAG

La raiz de estos tres problemas es una sola cosa.

RAG busca lenguaje natural como lenguaje natural.

Los documentos son lenguaje natural.
Los fragmentos son lenguaje natural.
Los embeddings son aproximaciones estadisticas del lenguaje natural.
Los resultados de busqueda son lenguaje natural.
Lo que entra al contexto es lenguaje natural.

La ambiguedad del lenguaje natural permea todo el pipeline.

La busqueda es imprecisa porque se busca contenido ambiguo en su forma ambigua.
El contexto se pierde porque se divide contenido ambiguo por un tamano ajeno al significado.
La verificacion es imposible porque no se puede extraer informacion de calidad de contenido ambiguo.

La mayoria de los intentos de mejorar RAG operan dentro de esta premisa.

Usar un mejor modelo de embedding. -- La aproximacion estadistica se vuelve mas refinada, eso es todo.
Usar una mejor estrategia de fragmentacion. -- Las posiciones de corte mejoran, eso es todo.
Agregar un reranker. -- Se lee el lenguaje natural una vez mas, eso es todo.
Usar busqueda hibrida. -- Se mezclan palabras clave y similitud, eso es todo.

Todos funcionan.
Todos permanecen dentro del marco del lenguaje natural.
Ninguno es fundamental.

---

## Condiciones para una alternativa fundamental

Para ir mas alla de los limites de RAG, la premisa debe cambiar.
No buscar lenguaje natural como lenguaje natural,
sino buscar representaciones estructuradas de forma estructural.

Esta alternativa debe satisfacer tres condiciones.

**Busqueda por coincidencia, no por similitud.**
No encontrar "cosas que se ven similares"
sino encontrar "cosas que coinciden."
Coincide el identificador? Esta dentro del rango temporal?
Si o no. No una probabilidad.

**La unidad de significado es la unidad de busqueda.**
No dividir por cantidad de tokens
sino almacenar por predicacion y buscar por predicacion.
Sin cortes en medio del significado.

**Los metadatos estan integrados en la estructura.**
No es necesario llamar a un LLM para juzgar la calidad de los resultados de busqueda.
La fuente, el tiempo y la confianza son campos,
asi que el filtrado mecanico es posible.

Cuando se cumplen estas tres condiciones,
la busqueda pasa de "adivinar candidatos plausibles"
a "confirmar lo que coincide."

---

## RAG es una tecnologia de transicion

Esto no es para menospreciar a RAG.

RAG fue la mejor respuesta en un mundo donde el lenguaje natural era todo lo que habia.
Cuando los documentos eran lenguaje natural, el conocimiento se almacenaba en lenguaje natural,
y los LLM eran herramientas que procesan lenguaje natural,
buscar lenguaje natural con lenguaje natural era la opcion obvia.

Y RAG funciona.
Un LLM con RAG es mucho mas preciso que uno sin RAG.
Esto es un hecho.

Pero si la premisa de "un mundo donde el lenguaje natural es todo lo que hay" cambia,
la posicion de RAG cambia tambien.

Si existen representaciones estructuradas,
RAG se convierte en el front end que "toma entrada en lenguaje natural y busca en un almacen estructurado."
Lenguaje natural -> consulta estructurada -> busqueda estructural -> resultados estructurados -> contexto.

RAG no desaparece.
Su backend cambia.
De busqueda por similitud de embedding a busqueda basada en estructura semantica.

---

## Resumen

RAG es el estandar actual para la ingenieria de contexto.
Y tiene tres limitaciones fundamentales.

1. **Similar no es igual a relevante.** La similitud de embedding no garantiza relevancia. "Se ve similar" y "es relevante" son cosas distintas.
2. **Fragmento no es igual a significado.** Dividir por cantidad de tokens corta en medio del significado. Premisas y conclusiones se separan. La informacion de confianza se pierde.
3. **El juicio de calidad es imposible.** La fuente, el tiempo y la confianza de los fragmentos recuperados no pueden determinarse mecanicamente. Juzgarlos requiere una llamada al LLM.

La raiz de los tres problemas es una sola cosa.
Buscar lenguaje natural como lenguaje natural.

La alternativa fundamental es cambiar la premisa.
Coincidencia, no similitud.
Predicacion, no fragmentos de tokens.
Metadatos integrados, no juicio externo.

RAG es una tecnologia de transicion.
Fue la mejor respuesta en un mundo donde el lenguaje natural era todo lo que habia.
Cuando esa premisa cambia, el backend de RAG cambia.
