---
title: "Por que la verificacion mecanica es necesaria"
weight: 4
date: 2026-02-26T12:00:10+09:00
lastmod: 2026-02-26T12:00:10+09:00
tags: ["verificacion", "especificacion", "compilador"]
summary: "El lenguaje natural no tiene el concepto de oracion invalida"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## El lenguaje natural no tiene el concepto de "oracion invalida."

---

## Nadie inspecciona lo que entra al contexto

Observa como la informacion entra al contexto en los pipelines actuales de LLM.

RAG devuelve fragmentos.
Un agente recibe respuestas de API.
Las conversaciones previas se acumulan en el historial.
Un usuario sube un documento.

Todo entra a la ventana de contexto.
Sin inspeccion.

Por que no hay inspeccion?
Porque el lenguaje natural no tiene el concepto de "invalido."

---

## El lenguaje natural acepta cualquier cadena

En la programacion, existe algo llamado error de sintaxis.

```python
def calculate(x, y
    return x + y
```

El parentesis no esta cerrado. Se rechaza antes de la ejecucion.
El codigo puede ser declarado definitivamente como "esto no es codigo valido" antes de ejecutarse, antes incluso de leerse.

El lenguaje natural no tiene tal cosa.

"El fue al banco."
Gramaticalmente perfecto.
No puedes saber quien fue, a que banco ni por que,
pero nada viola las reglas gramaticales del lenguaje natural.

"Informe de ventas del dia 45 del mes 13 de 2024."
No existe un mes 13 ni un dia 45.
Sin embargo, nada viola las reglas gramaticales del lenguaje natural.
Es una oracion gramaticalmente valida.

"Fuente: desconocida. Confianza: desconocida. Fecha: desconocida. La capitalizacion bursatil de Samsung Electronics es de 1.200 billones de won."
La fuente es desconocida, la confianza es desconocida, la fecha de referencia es desconocida.
Sin embargo, nada viola las reglas gramaticales del lenguaje natural.

El lenguaje natural acepta todo.
Una oracion invalida en lenguaje natural estructuralmente no existe.
Por lo tanto, no hay criterio mecanico para "rechazar" informacion expresada en lenguaje natural.

---

## Lo que se necesita para la verificacion mecanica

Observa el compilador de Go.

Go se niega a compilar si hay una importacion sin usar.
Aunque el codigo funcione perfectamente.
Aunque la logica no tenga ningun problema.
Se niega unicamente porque una linea de importacion no se usa.

Esto es verificacion mecanica.

La verificacion mecanica tiene tres caracteristicas.

**Es determinista.** El resultado es si o no. No una probabilidad. No hay "probablemente esta bien." Valido o invalido.

**Es barata.** No se necesita llamar al LLM. Comparacion de cadenas, verificacion de existencia de campos, verificacion de rango de valores. Operaciones de CPU en la escala de nanosegundos.

**No lee el significado.** No juzga si el contenido es verdadero o falso. Solo verifica si el formato se ajusta a la especificacion. No sabe si "la capitalizacion bursatil de Samsung Electronics es de 1.200 billones de won" es verdad. Pero sabe si el campo de fuente esta vacio.

Para que estas tres cosas sean posibles, hay un prerrequisito.
La informacion debe tener una especificacion.

Si hay una especificacion, las violaciones estan definidas.
Si las violaciones estan definidas, el rechazo es posible.
Si el rechazo es posible, la verificacion existe.

El lenguaje natural no tiene especificacion, asi que no hay violaciones.
Sin violaciones no hay rechazo.
Sin rechazo no hay verificacion.

---

## Por que se necesita la verificacion previa al contexto

La ventana de contexto es finita.

Ya sean 128K tokens o 1M tokens, es finita.
La calidad de la informacion que entra en un espacio finito determina la calidad de la salida.

Sin embargo, en los pipelines actuales,
el juicio de calidad ocurre solo despues de que la informacion entra al contexto.
Se espera que el LLM la lea, la juzgue y concluya por si mismo que "esta informacion es dificil de confiar."

Esto esta mal por tres razones.

**Es caro.** Estas usando costos de inferencia del LLM para hacer verificacion de formato. Ejecutas un modelo con miles de millones de parametros para filtrar fragmentos sin fuente. Usas razonamiento probabilistico para una tarea que requiere verificar un solo campo.

**No es fiable.** No hay garantia de que el LLM siempre ignore informacion sin fuente. De hecho, una vez que algo esta en el contexto, el LLM tiene mas probabilidad de usarlo. Esperar que el modelo ignore algo que le pusiste en el contexto es una contradiccion.

**Es tardio.** El espacio de la ventana ya fue consumido. Si 5 fragmentos sin fuente ocupan 200 tokens cada uno, se desperdician 1.000 tokens. Aunque se filtren despues, ese espacio ya fue gastado.

La verificacion mecanica viene antes de todo esto.
Antes de entrar al contexto.
Antes de que el LLM lo lea.
Antes de que la ventana se consuma.

---

## Que se verifica

La verificacion mecanica no comprueba la verdad del contenido sino la conformidad con una especificacion de formato.

Especificamente, estas cosas:

**Completitud estructural.** Existen los campos requeridos? El edge tiene sujeto y objeto? Falta algo?

**Validez de identificadores.** Existe el nodo referenciado? Lo que esta escrito como "Samsung Electronics" realmente apunta a una entidad definida? La referencia esta colgando?

**Conformidad de tipos.** Hay una fecha en el campo de fecha? Hay un numero en el campo numerico? "Dia 45 del mes 13 de 2024" se detecta aqui.

**Presencia de metadatos.** Hay un campo de fuente? Hay un campo de tiempo? Esta especificada la confianza? Si no, rechazar, marcar como ausente o asignar un valor por defecto.

**Integridad referencial.** Existe realmente el nodo al que apunta el edge? Referencia un nodo eliminado?

Estas verificaciones tienen algo en comun.
Todas pueden realizarse sin leer el contenido.
No sabes si "la capitalizacion bursatil de Samsung Electronics es de 1.200 billones de won" es verdad.
Pero sabes si hay una fuente especificada para esta declaracion.
Sabes si hay un tiempo registrado para esta declaracion.
Sabes si el formato de esta declaracion se ajusta a la especificacion.

---

## Lo barato va primero

En un pipeline de ingenieria de contexto, las inspecciones tienen un orden.

**Verificacion mecanica**: conformidad con la especificacion. Costo cercano a cero. Determinista.
**Filtrado semantico**: juicio de relevancia, confiabilidad, utilidad. Costo alto. Probabilistico.
**Verificacion de consistencia**: contradicciones entre las piezas de informacion seleccionadas. Costo aun mayor. Requiere razonamiento.

Si las ordenas de la mas barata a la mas cara,
las verificaciones caras tienen menos que procesar.

Si la verificacion mecanica filtra el 30% de las declaraciones que carecen de fuente,
el filtrado semantico solo necesita procesar el 70%.
Si el filtrado semantico elimina lo irrelevante,
la verificacion de consistencia maneja un conjunto aun mas pequeno.

Es el mismo principio que la optimizacion de consultas en bases de datos.
Aplica primero las condiciones filtrables por indice en la clausula WHERE.
Las condiciones de escaneo completo van despues.
Si lo barato va primero, la carga sobre lo caro disminuye.

Por el contrario,
si ejecutas la verificacion cara primero y la barata despues,
descubres errores de formato solo despues de haber gastado el costo.
Analizas el significado de una declaracion que referencia un nodo inexistente,
solo para descubrir despues que la referencia es invalida.

---

## Este orden es imposible en un pipeline de lenguaje natural

El lenguaje natural no tiene especificacion, asi que la verificacion mecanica es imposible.
Como la verificacion mecanica es imposible, la verificacion mas barata no existe.

En consecuencia, toda verificacion es semantica.
Toda verificacion requiere un LLM.
Toda verificacion es cara.

"Este fragmento tiene fuente?" -- El LLM debe leerlo.
"La referencia temporal de este fragmento es apropiada?" -- El LLM debe leerlo.
"El formato de este fragmento es correcto?" -- El lenguaje natural no tiene formato, asi que la pregunta misma no tiene sentido.

Esta es la realidad de la ingenieria de contexto actual.
Incluso la verificacion mas simple se realiza con la herramienta mas cara.
Una tarea que podria resolverse con comparacion de cadenas se maneja con un motor de inferencia.

---

## Prerrequisitos para la verificacion

Para que la verificacion mecanica exista, se necesitan tres cosas.

**Una especificacion.** El formato que la informacion debe seguir debe estar definido. Que campos son requeridos, que valores estan permitidos, que referencias son validas. Sin especificacion, las violaciones no pueden definirse.

**Formalizacion.** La informacion debe expresarse en el formato que la especificacion requiere. No como oraciones en lenguaje natural, sino codificada en la estructura que la especificacion exige. La informacion que no esta formalizada no puede ser inspeccionada.

**El poder de rechazar.** Debe ser posible rechazar efectivamente la informacion que no se ajusta. Si inspeccionas pero siempre apruebas, no es verificacion. La informacion invalida debe impedirse de entrar al contexto.

Estas tres cosas se dan por sentadas en los lenguajes de programacion.
Hay una especificacion llamada gramatica, un formato llamado codigo y un poder de rechazo llamado compilador.

En el lenguaje natural, las tres estan ausentes.
La gramatica no es una especificacion de formato sino una convencion.
Las oraciones no son formatos estructurados sino texto libre.
El concepto de "lenguaje natural invalido" no existe, asi que no hay nada que rechazar.

Para introducir la verificacion mecanica en la ingenieria de contexto,
la representacion de la informacion misma debe cambiar.

---

## Resumen

En el pipeline de contexto actual, la informacion entra al contexto sin inspeccion.
Porque el lenguaje natural no tiene el concepto de "oracion invalida."

La verificacion mecanica no comprueba la verdad del contenido sino la conformidad con una especificacion de formato.
Completitud estructural, validez de identificadores, conformidad de tipos, presencia de metadatos, integridad referencial.
Determinista, barata, y no lee el significado.

En el pipeline, las verificaciones baratas deben ir primero.
Si la verificacion mecanica filtra los errores de formato,
los juicios semanticos caros tienen menos que procesar.

El lenguaje natural no tiene especificacion, asi que esta verificacion es imposible.
Toda verificacion se convierte en semantica, y toda verificacion es cara.

Para que la verificacion mecanica sea posible,
debe haber una especificacion, formalizacion y el poder de rechazar.
La representacion de la informacion misma debe cambiar.
