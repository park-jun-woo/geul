---
title: "Por que los filtros son necesarios"
weight: 5
date: 2026-02-26T12:00:09+09:00
lastmod: 2026-02-26T12:00:09+09:00
tags: ["filtro", "relevancia", "confianza"]
summary: "La informacion valida no siempre es informacion necesaria"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## La informacion valida no siempre es informacion necesaria.

---

## Tienes 1.000 piezas de informacion que pasaron la verificacion

Supongamos que la verificacion mecanica funciono.

El formato es correcto,
los campos requeridos existen,
los identificadores son validos,
los tipos son apropiados,
y la integridad referencial se mantiene -- quedan 1.000 declaraciones.

Todas son informacion valida.
Se ajustan a la especificacion. No hay razon para rechazarlas.

Pero la ventana de contexto solo puede contener 300.

Cuales 300 pones?

Este es el problema del filtrado.

---

## Verificacion y filtrado hacen preguntas diferentes

Lo que la verificacion pregunta: "Es valida esta informacion?"
Lo que el filtrado pregunta: "Se necesita esta informacion ahora mismo?"

La verificacion mira las propiedades de la informacion en si.
Es correcto el formato? Estan presentes los campos? Son validas las referencias?
No le importa de que trata la informacion ni que proposito servira.

El filtrado mira la relacion entre la informacion y la situacion.
Es relevante para esta inferencia particular en este momento?
Se puede confiar en esta informacion?
Es suficientemente reciente?

La verificacion es posible sin contexto. Solo necesitas la especificacion.
El filtrado es imposible sin contexto. Necesitas saber "que se necesita ahora mismo."

La verificacion es determinista. Valido o invalido.
El filtrado es juicio. La relevancia tiene grados, la confiabilidad tiene umbrales, la actualidad tiene contexto.

La verificacion es barata.
El filtrado es relativamente caro.

Por eso la verificacion va primero y el filtrado va despues.
Si la verificacion filtra primero, el filtrado juzga un conjunto mas pequeno.
El costo del juicio caro disminuye.

---

## Tres cosas que el filtrado juzga

El filtrado mira tres cosas principales.

### Relevancia: Se necesita para esta inferencia?

El usuario pregunto sobre "el beneficio operativo de Samsung Electronics en el Q3 2024."

Entre las declaraciones validas que pasaron la verificacion:

- El beneficio operativo de Samsung Electronics en el Q3 2024 fue de 9,18 billones de won.
- Los ingresos de Samsung Electronics en el Q3 2024 fueron de 79 billones de won.
- El beneficio operativo de Samsung Electronics en el Q3 2023 fue de 2,43 billones de won.
- El plan de inversiones en semiconductores de Samsung Electronics es de 53 billones de won a partir de 2025.
- La sede central de Samsung Electronics esta en Suwon.

Todas validas. Todas sobre Samsung Electronics.
Las pones todas en el contexto?

La ubicacion de la sede es irrelevante.
El plan de inversiones tiene baja relevancia.
El beneficio operativo de 2023 puede ser util para comparar.
Los ingresos estan estrechamente relacionados con el beneficio operativo.

En RAG con lenguaje natural, este juicio se delega a la similitud de embedding.
Clasificado por distancia vectorial a "beneficio operativo de Samsung Electronics."
Pero como ya discutimos, similar no es relevante.

En una representacion estructurada, el juicio de relevancia tiene entradas diferentes.
A que entidad apunta la declaracion? Samsung Electronics.
Que propiedad? Beneficio operativo.
Que momento? Q3 2024.

Si la entidad, la propiedad y el tiempo existen como campos,
puedes encontrar "misma entidad, misma propiedad, mismo tiempo" con precision.
Y puedes incluir o excluir intencionalmente "misma entidad, misma propiedad, tiempo diferente."
Coincidencia de campos, no distancia vectorial.

La relevancia sigue siendo un juicio. No determinista.
Pero si la entrada a ese juicio es distancia vectorial o campos estructurados marca una diferencia en la precision.

### Confiabilidad: Se puede creer esta informacion?

Existen dos declaraciones sobre el mismo contenido.

- Fuente: divulgacion IR de Samsung Electronics. Confianza: 1.0. "Beneficio operativo Q3 2024: 9,18 billones de won."
- Fuente: blog anonimo. Confianza: 0.3. "Beneficio operativo Q3 2024: aproximadamente 10 billones de won."

Cual entra al contexto?

Obviamente la primera.

Pero para que este juicio sea "obvio,"
la fuente y la confianza deben existir en una forma legible.

En fragmentos de lenguaje natural, la fuente esta enterrada en algun lugar del texto o ausente.
La confianza nunca se ha expresado.
Para comparar dos fragmentos y juzgar cual es mas confiable,
un LLM debe leer y razonar.

En una representacion estructurada, la fuente y la confianza son campos.
"Excluir confianza inferior a 0.5" es una comparacion.
"Incluir solo fuentes primarias" es coincidencia de campos.

El costo del filtrado por confiabilidad pasa de inferencia del LLM a comparacion de campos.

### Actualidad: Es esta informacion suficientemente reciente?

"Quien es el CEO de Samsung Electronics?"

- Fecha: marzo 2024. "CEO de Samsung Electronics: Kyung Kye-hyun."
- Fecha: diciembre 2022. "Co-CEOs de Samsung Electronics: Han Jong-hee, Kyung Kye-hyun."

Ambas son validas. Formato correcto, fuentes presentes.
Pero se necesita la mas reciente.

En lenguaje natural, el tiempo puede o no estar mencionado en el texto.
Si dice "el ano pasado," tambien tienes que calcular cuando fue "el ano pasado."

En una representacion estructurada, el tiempo es un campo.
Una fecha ISO 8601.
"Incluir solo la declaracion mas reciente" es una operacion de ordenamiento.

Mas importante aun, el criterio de actualidad depende del contexto.
Si alguien pregunta por el CEO, se necesita la entrada mas reciente.
Si alguien pregunta por todos los CEOs anteriores, se necesita cada entrada.
Si alguien pregunta por las tendencias de ingresos, se necesitan los ultimos 8 trimestres.

Si el tiempo existe como campo, estas condiciones pueden expresarse como una consulta.
Si el tiempo esta enterrado en lenguaje natural, debe extraerse cada vez.

---

## Por que el filtrado no es verificacion mecanica

Hay una distincion importante aqui.

De los tres criterios del filtrado -- relevancia, confiabilidad, actualidad --
la confiabilidad y la actualidad pueden procesarse en gran medida de forma mecanica en una representacion estructurada.
Comparacion de campos, ordenamiento de valores, filtrado por rango.

Entonces por que llamar a esto "filtrado" y no "verificacion"?

La verificacion solo mira las propiedades de la informacion en si.
"Esta declaracion tiene un campo de tiempo?" Presente o ausente. No se necesita contexto.

El filtrado mira la relacion entre la informacion y la situacion.
"El tiempo de esta declaracion es apropiado para esta pregunta?" Debes saber cual es la pregunta para responder.

Ambos examinan el mismo campo de tiempo,
pero la verificacion comprueba "existencia"
y el filtrado juzga "adecuacion."

La existencia no necesita contexto.
La adecuacion necesita contexto.

Esta diferencia es la razon por la que el pipeline separa las dos etapas.

---

## La estructura de costos del filtrado

El filtrado es mas caro que la verificacion. Pero que tan caro depende de la representacion.

**Filtrado en un pipeline de lenguaje natural:**
Juicio de relevancia -- inferencia del LLM o calculo de similitud de embedding.
Juicio de confiabilidad -- el LLM extrae informacion de la fuente del texto y evalua.
Juicio de actualidad -- el LLM extrae informacion temporal del texto y compara.
Todo razonamiento. Todo caro.

**Filtrado en una representacion estructurada:**
Juicio de relevancia -- coincidencia de campos de entidad/propiedad + juicio basado en contexto.
Juicio de confiabilidad -- comparacion del campo de confianza. Coincidencia del campo de fuente.
Juicio de actualidad -- ordenamiento del campo de tiempo. Comparacion de rango.
La confiabilidad y la actualidad son operaciones de campo. Solo la relevancia requiere juicio.

En otras palabras, la estructuracion convierte dos de los tres criterios de filtrado en operaciones mecanicas.
Lo que queda es solo la relevancia.
Incluso la relevancia se estrecha de "es esta masa de texto similar a la pregunta" a "esta propiedad de esta entidad es relevante para la pregunta," haciendo el juicio mas claro.

El costo total del filtrado cae significativamente.

---

## Que pasa sin filtrado

Si verificas pero metes todo al contexto sin filtrar.

Las 1.000 piezas de informacion valida entran.
De esas, solo 30 se necesitan ahora mismo.

El LLM lee las 1.000.
Leer cuesta dinero.
970 piezas de informacion innecesarias dispersan la atencion.
La investigacion muestra que mas informacion irrelevante en el contexto aumenta la probabilidad de alucinacion.
La calidad del razonamiento sobre las 30 que realmente importan se degrada.

La ventana tambien se desperdicia.
Del espacio que ocupan 1.000 elementos, el equivalente a 970 elementos es desperdicio.
Ese espacio podria haber contenido otra informacion mas relevante.

El filtrado se trata de gestionar una ventana finita de forma finita.
Si la verificacion confirma "cumple los requisitos para entrar,"
el filtrado juzga "tiene una razon para entrar."

Los requisitos son cuestion de formato. La razon es cuestion de contexto.
Ambos son necesarios.

---

## El filtrado es politica

Un punto mas importante.

Los criterios de filtrado no son fijos.
Varian con el contexto.

Filtrado para un agente de consulta medica:
El umbral de confiabilidad es alto. Excluir confianza inferior a 0.9.
El estandar de actualidad es estricto. Excluir informacion medica de mas de 3 anos.
Excluir fuentes que no sean revistas con revision por pares.

Filtrado para un agente de conversacion casual:
El umbral de confiabilidad es bajo. La informacion aproximada es aceptable.
El estandar de actualidad es flexible. La informacion mas antigua puede incluirse segun el contexto.
Las restricciones de fuente son laxas.

La misma informacion pasa en un agente y es rechazada en otro.
La informacion no ha cambiado. La politica es diferente.

Esto significa que el filtrado no es meramente un problema tecnico
sino un problema de diseno.
"Que entra al contexto" es la misma pregunta que
"bajo que estandares queremos que opere este agente."

En una representacion estructurada, esta politica se expresa declarativamente.
"confidence >= 0.9, time >= 2022, source_type = peer-reviewed."
Una linea de consulta.

En lenguaje natural, esta politica se escribe como lenguaje natural en un prompt.
"Por favor, consulte solo informacion confiable y reciente."
Que el LLM siga esto de forma consistente es cuestion de probabilidad.

---

## Resumen

No toda la informacion que pasa la verificacion es necesaria.
Una ventana de contexto finita deberia contener solo lo que se necesita para la inferencia actual.

El filtrado juzga tres cosas.
Relevancia -- se necesita esta informacion para la pregunta actual?
Confiabilidad -- se puede creer esta informacion?
Actualidad -- es esta informacion suficientemente reciente?

La verificacion y el filtrado hacen preguntas diferentes.
La verificacion pregunta "es valida?"; el filtrado pregunta "se necesita?"
La verificacion es posible sin contexto; el filtrado requiere contexto.
La verificacion va primero; el filtrado va despues.

En una representacion estructurada, dos de los tres criterios del filtrado -- confiabilidad y actualidad -- se convierten en operaciones de campo. Lo que queda es solo la relevancia, e incluso esa se vuelve mas clara a traves de la coincidencia de campos estructurales.

El filtrado es politica.
La misma informacion se incluye o excluye segun el contexto.
En una representacion estructurada, esta politica se declara como una consulta.
En lenguaje natural, esta politica se escribe en el prompt como una esperanza.
