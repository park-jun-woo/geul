---
title: "Por qué los vectores de embedding no son suficientes"
weight: 11
date: 2026-02-26T12:00:18+09:00
lastmod: 2026-02-26T12:00:18+09:00
tags: ["embedding", "vector", "caja blanca"]
summary: "Reordenar los vectores de embedding rompe el modelo. Evitar la rotura implica reconstruir el modelo desde cero. Lo que se necesita no es transparencia dentro de la caja negra, sino una capa transparente fuera de ella."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Los vectores son buenos para el cálculo, pero imposibles de interpretar. No se puede hacer transparente el interior de una caja negra.

---

## Los vectores de embedding son una tecnología asombrosa

"Rey - Hombre + Mujer = Reina."

Cuando word2vec demostró esto, el mundo quedó asombrado.
Si se representan las palabras como vectores de cientos de dimensiones,
las relaciones semánticas emergen como operaciones vectoriales.

Los vectores de embedding son la base de los LLM.
Todo en un transformer es computación vectorial.
Los tokens se convierten en vectores.
La atención calcula similitudes entre vectores.
Las salidas se transforman de vectores a tokens.

Significados similares son vectores cercanos.
Significados diferentes son vectores lejanos.
La búsqueda es un cálculo de similitud vectorial.
La clasificación es trazar fronteras en el espacio vectorial.

Sin vectores de embedding, la IA actual no existiría.

Entonces, ¿por qué no usar vectores de embedding para representar el conocimiento?
Alinearlos directamente, estructurarlos, hacerlos interpretables.

No funciona.
La forma más segura de saberlo es intentarlo.

---

## AILEV: Lo intentamos

El proyecto GEUL comenzó originalmente bajo el nombre AILEV.

AI Language Embedding Vector.

El nombre declaraba el propósito por sí mismo:
un lenguaje de IA que manipula directamente vectores de embedding.

El concepto era el siguiente:

Representar el significado con vectores de 512 dimensiones.
Asignar roles a segmentos del vector.
Las primeras 128 dimensiones para entidades, las siguientes 128 para relaciones, las siguientes 128 para propiedades, el resto para metadatos.
Así como RGBA descompone el color en cuatro canales, descomponer el significado en segmentos dimensionales.

Entrenar BERT para convertir lenguaje natural en estos vectores estructurados.
Al introducir "Seúl es la capital de Corea",
el segmento de entidades produce el vector de Seúl, el de relaciones produce el vector de capital, el de propiedades produce el vector de Corea.

Como son vectores, el cálculo es posible.
La búsqueda por similitud es posible.
Al reducir dimensiones se logra una degradación elegante.
Pasar de 512 a 256 dimensiones pierde precisión pero conserva el significado esencial.

Era elegante. En teoría.

---

## Por qué fracasa

### Reordenar los vectores arbitrariamente rompe el modelo

Los vectores de embedding de un LLM son el producto del entrenamiento.

Tras leer miles de millones de textos,
el modelo optimiza por sí mismo sus representaciones internas.
Lo que significa cada dimensión lo decidió el modelo.
No una persona.

¿Qué ocurre si se declara "las primeras 128 dimensiones son para entidades"?

En el espacio vectorial que el modelo aprendió,
la información de entidades no reside en las primeras 128 dimensiones.
Está distribuida por las 768 dimensiones.
La información de relaciones, propiedades, tiempos verbales — todo mezclado.

Esto no es un error de diseño sino la naturaleza del aprendizaje.
La retropropagación encuentra
la disposición vectorial óptima para la tarea.
No encuentra una disposición interpretable.
Óptimo e interpretable no son lo mismo.

Si se reordenan los vectores a la fuerza — "entidades aquí, relaciones allá" —
las relaciones estadísticas que el modelo aprendió se rompen.
El rendimiento se degrada.

### Reordenar sin romper significa reconstruir el modelo

Entonces, ¿por qué no entrenar desde cero con la restricción "las primeras 128 dimensiones son para entidades"?

Se puede. En teoría.
Pero eso no es alinear vectores de embedding.
Es diseñar una nueva arquitectura de modelo.

Se necesitan datos de entrenamiento. Miles de millones de tokens.
Se necesita infraestructura. Miles de GPUs.
Se necesita tiempo. Meses.
Y no hay garantía de que el modelo resultante funcione tan bien como los LLM existentes.

El esfuerzo es demasiado grande.

El problema de "alinear vectores para hacerlos interpretables"
se ha transformado en "reconstruir un LLM desde cero".
Esto no es resolver el problema sino ampliarlo.

### La interpretación es imposible

Supongamos que se logró crear un vector estructurado.
Un vector de 512 dimensiones.
Digamos que las primeras 128 dimensiones son para entidades.

El segmento de entidades vale `[0.23, -0.47, 0.81, 0.12, ...]`.

¿Cómo se sabe si esto es "Samsung Electronics" o "Hyundai Motor"?

Hay que encontrar el vector más cercano.
Hay que calcular la similitud en una base de datos vectorial.
Y se obtiene una respuesta probabilística: "probablemente Samsung Electronics".

"Probablemente."

Los vectores son intrínsecamente continuos.
Entre los vectores de Samsung Electronics y SK Hynix
existen infinitos vectores intermedios.
Nadie sabe qué significan esos vectores intermedios.

Esto no es una limitación técnica sino una verdad matemática.
Representar significados discretos en un espacio continuo
difumina las fronteras.
La ambigüedad era [el problema del lenguaje natural](/es/why/natural-language-hallucination/).
Se pasó a vectores y la ambigüedad reapareció.

Solo cambió la forma.
En el lenguaje natural, la ambigüedad de las palabras.
En los vectores, la ambigüedad de las coordenadas.

---

## El principio de la caja blanca

Aquí se revela el problema de diseño fundamental.

Los vectores de embedding son una caja negra.
Al observar un vector de 768 dimensiones de valores reales,
nadie puede saber qué información está codificada y dónde.
El propio modelo tampoco puede explicarlo.

Esto no es un rasgo incómodo sino una propiedad ontológica.
Es precisamente la razón por la que los vectores funcionan.
Porque organizan la información de maneras que los humanos no diseñaron,
funcionan mejor que cualquier diseño humano.
La ininterpretabilidad no es un defecto sino una característica.

Sin embargo, el conocimiento utilizado como contexto de la IA exige lo contrario.

Hay que saber la fuente.
Hay que saber el momento temporal.
Hay que saber el nivel de confianza.
Hay que saber de qué trata la afirmación.
Hay que saber si dos afirmaciones se refieren a la misma entidad.

Cada requisito es "hay que saber". Cada requisito exige interpretabilidad.

Satisfacer exigencias de caja blanca con un vector de caja negra
es una contradicción.

---

## La lógica del giro

El giro de AILEV a GEUL no fue una retirada.
Fue una redefinición del problema.

**Problema original:** Los LLM son cajas negras. Hagamos transparente el interior.
→ Hagamos interpretables los vectores de embedding alineándolos.
→ Tocar los vectores rompe el modelo.
→ Evitar la rotura implica reconstruir el modelo.
→ Callejón sin salida.

**Problema redefinido:** No es necesario hacer transparente el interior de la caja negra. Construyamos una capa transparente en el exterior.
→ No se toca el interior del LLM.
→ Fuera del LLM se crea un sistema de representación interpretable.
→ El LLM puede leer y escribir ese sistema. Porque son tokens.
→ Un lenguaje artificial.

No vectores sino lenguaje.
No continuo sino discreto.
No ininterpretable sino con la interpretación como único propósito.
No dentro del modelo sino fuera del modelo.

Se eliminó "Embedding Vector" de AILEV
y nació GEUL — que significa "escritura". Esta es la razón.

---

## Vectores para el cálculo, lenguaje para la representación

Esto no es un rechazo a los vectores de embedding.

Los vectores están optimizados para el cálculo.
Búsqueda por similitud, agrupamiento, clasificación, recuperación.
El lenguaje no puede reemplazar lo que hacen los vectores.

El lenguaje está optimizado para la representación.
Identidad de entidades, descripción de relaciones, metadatos integrados, interpretabilidad.
Los vectores no pueden reemplazar lo que hace el lenguaje.

Son herramientas de capas diferentes.

Dentro del LLM, los vectores operan. Una caja negra. Así debe ser.
Fuera del LLM, el lenguaje opera. Una caja blanca. Así debe ser.

El problema comenzó al confundir estas dos capas.
Se intentó que los vectores hicieran el trabajo del lenguaje.
Se intentó asignar a una caja negra el papel de una caja blanca.

Cada uno tiene su lugar.

---

## Resumen

Los vectores de embedding son la base de los LLM y una tecnología asombrosa.
Sin embargo, como medio de representación del conocimiento, tienen límites fundamentales.

GEUL comenzó como AILEV (AI Language Embedding Vector).
El objetivo era alinear vectores directamente y hacerlos interpretables.
Fracasó. Por dos razones.

Alinear vectores arbitrariamente rompe las relaciones que el modelo aprendió.
Alinear sin romper implica reconstruir el modelo desde cero. El esfuerzo es demasiado grande.

Y aunque se lograra, los vectores no pueden interpretarse.
En un espacio continuo, las fronteras del significado discreto son ambiguas.
No se puede asignar a una caja negra el papel de una caja blanca.

La lógica del giro:
Se intentó hacer transparente el interior de la caja negra.
Tocar el interior lo rompe.
En su lugar, dejar el interior intacto y construir una capa transparente en el exterior.
No vectores sino lenguaje. No dentro del modelo sino fuera del modelo.

Vectores para el cálculo, lenguaje para la representación.
Cada uno tiene su lugar.
