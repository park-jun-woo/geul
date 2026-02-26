---
title: "Por que el lenguaje natural crea alucinaciones?"
weight: 8
date: 2026-02-26T12:00:16+09:00
lastmod: 2026-02-26T12:00:16+09:00
tags: ["lenguaje natural", "alucinacion", "ambiguedad"]
summary: "La alucinacion no es un bug del LLM — es consecuencia estructural inevitable de cuatro defectos del lenguaje natural: ambiguedad, ausencia de fuente, de confianza y de tiempo. Modelos mas grandes no lo solucionan."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## La alucinacion no es un bug. Es una inevitabilidad estructural mientras usemos lenguaje natural.

---

## El milagro del lenguaje natural

Hace 100,000 anos aparecio el lenguaje hablado. Las relaciones sociales que los primates podian mantener acicalandose mutuamente estaban limitadas a unos 150 individuos. El lenguaje rompio ese techo. Una vez que una persona podia hablar a muchas al mismo tiempo, una nueva escala de sociedad --- la tribu --- se hizo posible.

Hace 10,000 anos, la agricultura creo excedentes de alimentos y las personas se reunieron en un lugar para formar ciudades. Hace 5,000 anos, alguien en Mesopotamia presiono marcas en forma de cuna en una tablilla de arcilla humeda. Era para registrar inventarios de grano. El nacimiento de la escritura. El habla se desvanece, pero los registros perduran. Una vez que los registros perduraron, la burocracia se hizo posible, la ley se hizo posible, el estado se hizo posible.

El lenguaje hablado creo la tribu. La escritura creo el estado.

El lenguaje natural es la mayor tecnologia que la humanidad haya creado jamas. No el descubrimiento del fuego, no la invencion de la rueda, no la invencion del semiconductor. Lo que hizo posible todo eso fue el lenguaje natural. Porque existia el lenguaje natural, el conocimiento pudo transmitirse, la cooperacion pudo ocurrir y los pensamientos de los muertos pudieron ser heredados por los vivos. Durante decenas de miles de anos, el lenguaje natural fue el medio de toda la civilizacion humana.

Y ahora, ese gran lenguaje natural se ha convertido en el cuello de botella de la era de la IA.

---

## El malentendido llamado alucinacion

Cuando la IA dice algo falso, lo llamamos "alucinacion."

Este nombre conlleva implicaciones.
La implicacion de que la alucinacion es anormal.
La implicacion de que puede arreglarse.
La implicacion de que un modelo mejor lo solucionara.

Esto es un malentendido.

La alucinacion no es un bug de los LLM.
La alucinacion es una inevitabilidad estructural que no puede evitarse
mientras se use lenguaje natural como lenguaje de razonamiento de la IA.

No importa cuanto escales el modelo,
no importa cuanto expandes los datos,
no importa cuan refinado sea el RLHF,
mientras la entrada sea lenguaje natural y la salida sea lenguaje natural,
la alucinacion no desaparecera.

Permitan explicar por que.

---

## Los cuatro defectos estructurales del lenguaje natural

El lenguaje natural evoluciono para la comunicacion entre humanos.
Las cuatro caracteristicas que adquirio en el proceso
se convierten en defectos fatales para el razonamiento de la IA.

---

### Defecto 1: Ambiguedad

"El fue al banco."

Es "banco" una institucion financiera o la orilla de un rio?
Quien es "el"?
Cuando fue?

Los humanos resuelven esto con contexto.
El flujo de la conversacion, la expresion facial del hablante, conocimiento de fondo compartido.

La IA solo tiene texto.
El texto solo no puede resolver completamente la ambiguedad.
Si no puede resolverse, la IA adivina.
Las adivinanzas a veces son incorrectas.
Cuando una adivinanza incorrecta se produce con confianza, eso es alucinacion.

---

### Defecto 2: Ausencia de fuente

"Yi Sun-sin derroto 133 barcos con solo 12."

Esta frase no tiene fuente.

Quien hizo esta afirmacion?
Que registros historicos la respaldan?
Hay desacuerdo academico sobre estos numeros?

El lenguaje natural no tiene un lugar estructural para metadatos.
Para incluir fuentes, hay que alargar la frase,
y alargarla oscurece el punto.
Asi que en la mayoria de las frases en lenguaje natural, las fuentes se omiten. Este problema se explora con mas profundidad en [Por que afirmaciones, no hechos?](/es/why/claims-not-facts/).

Los LLM se entrenan con miles de millones de tales frases.
Afirmaciones con fuentes omitidas se mezclan
en una enorme sopa estadistica.

Rastrear la base del numero "12" dentro de esa sopa
es imposible en principio.
Como la base no puede rastrearse, numeros sin fundamento tambien pueden fabricarse.
Eso es alucinacion.

---

### Defecto 3: Ausencia de confianza

"La Tierra es redonda."
"La energia oscura constituye el 68% del universo."
"Manana llovera."

Los niveles de confianza de estas tres frases son completamente diferentes.

La primera es un consenso abrumador.
La segunda es la mejor estimacion actual, pero la teoria puede cambiar.
La tercera es una prediccion probabilistica.

Sin embargo, en lenguaje natural, las tres tienen estructuras gramaticales identicas.
Sujeto + predicado. Frase declarativa. Punto.

El lenguaje natural no puede expresar estructuralmente "que tan seguro es esto."
Hay dispositivos adverbiales como "quiza", "casi seguramente", "podria",
pero son opcionales, imprecisos y usualmente se omiten.

Los LLM aprenden todas las frases a niveles de confianza identicos.
No hay forma de que el modelo distinga internamente la diferencia de confianza
entre "la Tierra es redonda" y "la energia oscura es el 68%."

Asi que afirma estimaciones como hechos,
afirma hipotesis como visiones establecidas,
y afirma cosas inciertas con certeza.
Eso es alucinacion.

---

### Defecto 4: Ausencia de contexto temporal

"El CEO de Tesla es Elon Musk."

A partir de cuando?

En 2024, esto es correcto.
En 2030, quien sabe.
Si no se especifica el momento de escritura,
el periodo de validez de esta frase no puede determinarse.

La mayoria de las frases en lenguaje natural omiten el contexto temporal.
El "tiempo presente" puede significar "ahora mismo"
o puede significar "generalmente."

Los LLM aprenden articulos de 2020 y articulos de 2024 como los mismos datos.
Como la informacion temporal no se preserva estructuralmente,
afirman hechos pasados como si fueran presentes,
o mezclan informacion de diferentes periodos de tiempo.
Eso es alucinacion.

---

## La confluencia de los cuatro defectos

La alucinacion escala explosivamente cuando estos cuatro defectos convergen.

Analicemos una sola salida de un LLM.

> "Yi Sun-sin destruyo 330 barcos japoneses con 12 navios,
> y mas tarde murio en la Batalla de Noryang, dejando las ultimas palabras 'No anuncien mi muerte.'"

En esta frase:

**Ambiguedad:** Que significa "destruyo" precisamente? Hundio? Puso en fuga? Dano parcialmente?

**Ausencia de fuente:** Cual es la base de los numeros 12 y 330? Diferentes registros historicos citan cifras diferentes --- cual se siguio?

**Ausencia de confianza:** Es "No anuncien mi muerte" un testamento historicamente confirmado, o tradicion oral posterior? Los niveles de confianza de ambos son diferentes, pero se listan en la misma frase declarativa.

**Ausencia de contexto temporal:** Que punto en el tiempo del consenso academico refleja esta informacion?

El LLM llena toda esta ambiguedad con "la secuencia de tokens mas plausible."
La plausibilidad no es precision.
La brecha entre ambas es alucinacion.

---

## Por que modelos mas grandes no pueden resolver esto

"No disminuira la alucinacion cuando salga GPT-5?"

Disminuira. Pero no desaparecera.

Modelos mas grandes aprenden patrones mas sofisticados de mas datos.
Asi que la precision de la "plausibilidad" sube.

Pero el problema fundamental no cambia.

Mientras la entrada sea lenguaje natural, la ambiguedad permanece.
Mientras los datos de entrenamiento sean lenguaje natural, las fuentes permanecen perdidas.
Mientras la salida sea lenguaje natural, la confianza no se expresa.
Mientras la informacion temporal este ausente de la estructura, el tiempo permanece desordenado.

Incluso si escalas el modelo 100x,
los defectos estructurales del lenguaje natural no crecen 100x ---
pero tampoco llegan a cero.

Esto no es un problema de resolucion. Es un problema de medio.

No importa cuanto aumentes la resolucion de una fotografia en blanco y negro, el color no aparece.
No importa cuanto aumentes la precision del lenguaje natural,
la fuente, la confianza y el contexto temporal no aparecen en la estructura.

Si quieres color, necesitas pelicula a color.
Si quieres eliminar la alucinacion, necesitas un lenguaje diferente.

---

## Condiciones para una solucion estructural

Para resolver estos cuatro defectos, la estructura del lenguaje mismo debe ser diferente.

**Ambiguedad --> Estructuracion explicita.**
Cuando "El fue al banco" se convierte en un lenguaje estructurado,
"el" se resuelve a un SIDX de entidad especifico,
y "banco" se resuelve al SIDX de una institucion financiera o de la orilla de un rio.
Si no puede resolverse, "no resuelto" se declara explicitamente.
Resolver la ambiguedad, o registrar el hecho de que es ambiguo.

**Ausencia de fuente --> Fuente incrustada.**
Cada narracion incluye estructuralmente una entidad fuente.
"Quien hizo esta afirmacion" es parte de la narracion.
No es opcional. Si el campo esta vacio, se marca como vacio.

**Ausencia de confianza --> Confianza incrustada.**
Cada arista de verbo tiene un campo de confianza.
"Seguro", "estimado", "hipotetico"
se especifican estructuralmente como modificadores del verbo.

**Ausencia de contexto temporal --> Contexto temporal incrustado.**
Cada narracion incluye un contexto de tiempo.
"A partir de cuando es esta narracion" siempre se especifica.

Lo que se omite en lenguaje natural
existe como parte de la estructura en un lenguaje estructurado.

Cuando la omision es imposible, el espacio para la alucinacion se reduce. [Por que es necesaria la clarificacion](/es/why/clarification/) explica este principio.
Cuando no puedes hablar sin base, las afirmaciones sin fundamento no se producen.

---

## El fin de la alucinacion esta en reemplazar el lenguaje

Veamos los enfoques actuales para reducir la alucinacion.

**RAG (Retrieval-Augmented Generation):** Recupera documentos externos y los proporciona como contexto. Efectivo, pero los documentos recuperados tambien son lenguaje natural, asi que los problemas de ambiguedad, fuentes ausentes y confianza ausente los acompanan sin cambios. [Por que RAG no es suficiente](/es/why/rag-not-enough/) explora esta limitacion en detalle.

**RLHF:** Entrena al modelo para decir "No se" cuando esta inseguro. Reduce la frecuencia de la alucinacion, pero no resuelve el problema fundamental de que el lenguaje natural carece de estructura de confianza.

**Chain-of-Thought:** Registra el proceso de razonamiento en lenguaje natural. La direccion es correcta, pero el medio del registro es lenguaje natural, asi que hereda los mismos defectos.

Todos estos enfoques intentan mitigar la alucinacion dentro del marco del lenguaje natural.
Funcionan. Pero no son fundamentales.

La solucion fundamental es remover el lenguaje natural del interior de la IA.

La interfaz con los usuarios se queda en lenguaje natural.
Los humanos siguen hablando en lenguaje natural y recibiendo respuestas en lenguaje natural.

Pero el lenguaje en el que la IA razona, registra y verifica internamente
debe ser algo diferente al lenguaje natural.

Un lenguaje donde la fuente esta en la estructura.
Un lenguaje donde la confianza esta en la estructura.
Un lenguaje donde el contexto temporal esta en la estructura.
Un lenguaje donde la ambiguedad se maneja explicitamente.

El lenguaje hablado creo la tribu.
La escritura creo el estado.
Que creara el tercer lenguaje?

El fin de la alucinacion no esta en modelos mas grandes
sino en un lenguaje mejor.

---

## Resumen

La alucinacion nace de los cuatro defectos estructurales del lenguaje natural.

1. **Ambiguedad:** Irresolvable sin contexto. La IA adivina, y las adivinanzas son incorrectas.
2. **Ausencia de fuente:** La base de las afirmaciones se pierde. Se fabrican combinaciones sin fundamento.
3. **Ausencia de confianza:** Hechos y estimaciones se expresan con gramatica identica. La IA no puede distinguirlos.
4. **Ausencia de contexto temporal:** Informacion de diferentes periodos de tiempo se mezcla.

Modelos mas grandes reducen la alucinacion pero no pueden eliminarla.
Sin cambiar el medio, los defectos estructurales permanecen.

No importa cuanto aumentes la resolucion de pelicula en blanco y negro, el color no aparece.
Si quieres color, debes cambiar la pelicula.
