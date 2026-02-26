---
title: "Por qué Wikidata"
weight: 13
date: 2026-02-26T12:00:17+09:00
lastmod: 2026-02-26T12:00:17+09:00
tags: ["Wikidata", "Ontología", "SIDX"]
summary: "GEUL no rechaza Wikidata. Transforma el sistema de clasificación y las estadísticas de frecuencia de 100 millones de entidades en libros de códigos SIDX. Construye gramática sobre un diccionario."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## GEUL no rechaza Wikidata. Se alza sobre ella.

---

## No se puede crear un idioma sin un diccionario

Todo idioma necesita un vocabulario.

El coreano tiene el diccionario coreano.
El inglés tiene el diccionario inglés.
Los lenguajes de programación tienen bibliotecas estándar.

Lo mismo ocurre con un idioma artificial.
Una lista de entidades, una lista de relaciones, una lista de propiedades.
¿Qué código representa a "Samsung Electronics" en este idioma?
¿Qué código representa la relación "capital"?
Se necesita un vocabulario antes de poder escribir una oración.

¿Cómo se construye este vocabulario?
Hay dos caminos.

Construirlo desde cero.
O utilizar lo que ya existe.

---

## Construir desde cero: la lección de CYC

El proyecto CYC comenzó en 1984.

Su objetivo era formalizar y almacenar conocimiento de sentido común general.
La ontología se diseñó desde cero.
Se definieron conceptos, se definieron relaciones, se definieron reglas.
Los expertos los ingresaron manualmente.

Pasaron treinta años.
Se ingresaron millones de reglas.

Sin embargo, estaba lejos de cubrir el conocimiento del mundo.
Cada dominio requería diseñar una ontología separada.
Mantener la coherencia entre dominios resultaba difícil.
Cada vez que surgía un concepto nuevo, la ontología debía revisarse.
Las revisiones entraban en conflicto con las reglas existentes con frecuencia.

Lo que CYC demostró no fue su potencial, sino sus límites.
Que un pequeño equipo de expertos diseñe la ontología del mundo
se vuelve insostenible a escala.

---

## Lo que ya existe: Wikidata

Wikidata se lanzó en 2012.

Una base de conocimiento estructurada operada por la Fundación Wikimedia.
Cualquiera puede editarla.
En 2024, contiene más de 100 millones de entidades.
Más de 10.000 propiedades.
Miles de millones de declaraciones.
Etiquetas en más de 300 idiomas.

La escala que CYC no logró en 30 años con un equipo de expertos,
Wikidata la alcanzó en 10 años con una comunidad.

Veamos qué ofrece Wikidata.

**Identificadores de entidades.** Q-ID. Samsung Electronics es Q20718. Seúl es Q8684. Yi Sun-sin es Q217300. Identificadores únicos a nivel mundial. Independientes del idioma.

**Identificadores de propiedades.** P-ID. "Sede" es P159. "Fecha de fundación" es P571. "Población" es P1082. Las relaciones y propiedades se identifican de forma única.

**Estructura jerárquica.** P31 (instance of) y P279 (subclass of) forman una jerarquía de tipos. "Seúl → ciudad → asentamiento humano → entidad geográfica." El sistema de clasificación del mundo se expresa mediante estas dos propiedades.

**Etiquetas multilingües.** La etiqueta en coreano de Q20718 es "삼성전자", la etiqueta en inglés es "Samsung Electronics", la etiqueta en japonés es "サムスン電子". Un identificador, nombres distintos para cada idioma.

**Validación comunitaria.** Millones de editores. Detección de vandalismo. Requisitos de fuentes. No es perfecto, pero es más escalable que un pequeño equipo de expertos.

No hay razón para construir esto desde cero.

---

## El vocabulario de GEUL proviene de Wikidata

El SIDX (Semantic-aligned Index) de GEUL es un identificador semánticamente alineado de 64 bits.
El significado está codificado en los propios bits.
Solo examinando los bits superiores se puede saber si algo es una persona, un lugar o una organización.

El libro de códigos del SIDX — qué patrón de bits corresponde a qué significado — se extrae de Wikidata.

El proceso es el siguiente.

**Paso 1: Extracción de tipos.**
Se extraen todos los Q-ID utilizados como objetos de P31 (instance of) en Wikidata.
Esto produce la lista de "tipos".
"Humano (Q5)", "ciudad (Q515)", "país (Q6256)", "empresa (Q4830453)"...
Se cuenta cuántas veces se usa cada tipo — el número de instancias.

**Paso 2: Construcción de la jerarquía.**
Se extraen las relaciones P279 (subclass of) entre tipos.
"Ciudad → asentamiento humano → entidad geográfica → entidad."
Esto forma la estructura de árbol de los tipos.
Se identifican nodos raíz, nodos hoja y nodos intermedios.
Se detecta y gestiona la herencia múltiple — casos donde un tipo pertenece a varios tipos padre.

**Paso 3: Asignación de bits.**
La estructura del árbol determina las relaciones de prefijo de los patrones de bits.
Los subtipos bajo el mismo padre comparten el mismo prefijo.
"Ciudad" y "pueblo" comparten el prefijo de "asentamiento humano".

El número de instancias influye en la longitud de bits.
Los tipos más utilizados reciben códigos más eficientes.
El mismo principio que la codificación de Huffman: códigos más cortos para frecuencias más altas.

---

## Lo que Wikidata proporciona

En este proceso, Wikidata proporciona tres cosas.

**Un sistema de clasificación.**
Una respuesta a "¿Qué tipos de cosas existen en el mundo?"
CYC lo diseñó con un equipo de expertos.
GEUL lo extrae de Wikidata.
Un sistema de clasificación construido por millones de editores durante 10 años,
transformado en un árbol de bits.

**Estadísticas de frecuencia.**
Una respuesta a "¿Cuántas hay de cada tipo en el mundo?"
Si hay 9 millones de entidades humanas y 1 millón de asteroides,
el tipo "humano" debería recibir un código más eficiente que "asteroide".
La frecuencia de uso real determina el diseño del código.

**Mapeo de identificadores.**
Un mapeo entre los Q-ID de Wikidata y los SIDX de GEUL.
¿Qué patrón de bits en SIDX corresponde a Q20718 (Samsung Electronics)?
Con este mapeo, el conocimiento de Wikidata puede convertirse a GEUL,
y las declaraciones de GEUL pueden reconvertirse a Wikidata.

---

## Lo que Wikidata no proporciona

Wikidata es un diccionario. Un diccionario no es un idioma.

Un diccionario proporciona una lista de palabras.
Un idioma proporciona la gramática para componer oraciones con palabras.

Lo que Wikidata no proporciona es lo que GEUL añade.

**De hechos a afirmaciones.**
La unidad básica de Wikidata es un hecho (Fact).
"La población de Seúl es 9,74 millones."
Es verdadero o falso.

La unidad básica de GEUL es una afirmación (Claim).
"Según A, la población de Seúl es aproximadamente 9,74 millones. (confianza 0,9, referencia 2023)"
Quién lo afirma, con qué nivel de certeza y a partir de qué fecha — todo esto se incorpora en la declaración.
Esta diferencia se analiza en detalle en [Por qué afirmaciones, no hechos](/es/why/claims-not-facts/).

**Calificadores verbales.**
Wikidata no tiene un lugar para expresar los matices de los verbos.
En "Yi Sun-sin venció en la Batalla de Myeongnyang",
¿dónde están el tiempo, el aspecto, la evidencialidad, el modo y la confianza?
En Wikidata, estos se expresan parcialmente mediante calificadores,
pero no existe un sistema sistemático de calificación verbal.

GEUL tiene un sistema de calificadores verbales de 28 bits.
Trece dimensiones — tiempo, aspecto, polaridad, evidencialidad, modo, volitividad, confianza y más — se integran estructuralmente en cada declaración.

**Compresión de 16 bits.**
La representación de Wikidata no fue diseñada para ventanas de contexto.
JSON-LD, RDF, SPARQL.
Legibles por máquinas, pero no eficientes en tokens.

GEUL está diseñado en unidades de palabras de 16 bits.
Mapeo uno a uno con los tokens de LLM.
Un sistema de representación construido sobre la premisa de ventanas de contexto finitas.
Esto ya se discutió en [Por qué no MD/JSON/XML](/es/why/not-md-json-xml/).

**Pipeline de contexto.**
Wikidata es un repositorio. GEUL es parte de un pipeline.
Clarificación, validación, filtrado, verificación de coherencia, exploración — todo lo discutido en esta serie opera sobre la representación estructurada de GEUL.
Wikidata no tiene este pipeline.
Ni lo necesita. El propósito de Wikidata es diferente.

---

## La relación entre un diccionario y un idioma

En resumen:

Wikidata es el vocabulario del mundo.
Qué entidades existen,
qué relaciones existen,
qué tipos existen y cómo se clasifican.
Millones de personas lo construyeron durante 10 años.

GEUL construye gramática sobre este vocabulario.
El sistema de clasificación del vocabulario → el árbol de bits de SIDX.
Las estadísticas de frecuencia del vocabulario → las prioridades de asignación de bits.
Los identificadores del vocabulario → el mapeo con SIDX.

Y añade lo que al vocabulario le falta.
Estructura de afirmaciones. Calificación verbal. Compresión a nivel de token. Pipeline de contexto.

¿Se podría construir GEUL sin Wikidata?
Sí. Se diseñaría la ontología desde cero, como hizo CYC.
Pero eso se intentó hace 30 años, y los resultados hablan por sí solos.

Porque Wikidata existe, GEUL no diseña una ontología.
Transforma un consenso existente.

---

## Resumen

Un idioma artificial necesita un vocabulario.
Construirlo desde cero fue lo que intentó CYC, y 30 años demostraron los límites de ese enfoque.

Wikidata es el vocabulario del mundo, con más de 100 millones de entidades, más de 10.000 propiedades y miles de millones de declaraciones.
Millones de editores lo construyeron durante 10 años.

El libro de códigos SIDX de GEUL se extrae de Wikidata.
Las frecuencias de instancias de P31 determinan la asignación de bits,
y la jerarquía de P279 forma el esqueleto del árbol de bits.

Wikidata es un diccionario; GEUL es un idioma.
Un diccionario proporciona palabras; un idioma proporciona gramática.
GEUL construye estructura de afirmaciones, calificación verbal, compresión de 16 bits y un pipeline de contexto sobre el vocabulario de Wikidata.

GEUL no rechaza Wikidata.
Se alza sobre ella.
