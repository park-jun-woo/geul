---
title: "Por que MD/JSON/XML no funcionan"
weight: 9
date: 2026-02-26T12:00:15+09:00
lastmod: 2026-02-26T12:00:15+09:00
tags: ["formato", "JSON", "XML"]
summary: "Los formatos existentes no pueden transportar significado"
author: "박준우"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Los formatos estructurados ya existen. Entonces, por que se necesita un nuevo lenguaje?

---

## La objecion mas comun

Cuando alguien se encuentra por primera vez con la idea de un lenguaje de razonamiento de IA, lo primero que dice es:

"Los formatos estructurados ya existen, no?"

Tienen razon. Existen. Muchos de ellos.

Existe Markdown.
Existe JSON.
Existe XML.
YAML, TOML, Protocol Buffers, MessagePack, CSV...

El mundo rebosa de formatos de datos.
Entonces, por que la IA sigue pensando en lenguaje natural?

Para responder esta pregunta, debemos senalar exactamente que hace bien cada formato
y que no puede hacer.

---

## Markdown: la memoria actual de los agentes de IA

A partir de 2026, el formato mas ampliamente usado por los agentes de IA es Markdown.

Claude Code recuerda en archivos `.md`.
Los agentes basados en GPT tambien dejan notas en Markdown.
CLAUDE.md, memory.md, notes.md.
La memoria a largo plazo de la IA se sostiene sobre Markdown en este mismo momento.

Por que Markdown? La razon es simple.
Los LLM leen y escriben bien en Markdown.
Markdown es abundante en los datos de entrenamiento,
y su estructura es lo suficientemente simple para generar y parsear facilmente.

Pero Markdown es **un formato de documento destinado a que los humanos lean.**

```markdown
# Estado del Proyecto
## Estrategia de Cache
- Mascara de bits SIMD adoptada (decidido 1/28)
- Aceleracion GPU en revision
## Sin resolver
- Metodo de generacion de consultas TBD
```

Como interpreta esto una maquina?

Hay un encabezado de seccion llamado "Estrategia de Cache."
Debajo, hay un item "Mascara de bits SIMD adoptada."
Hay una fecha "(1/28)" entre parentesis.

Una maquina no puede entender esto estructuralmente.
Puede decir por `##` que "Estrategia de Cache" es un encabezado de seccion,
pero la relacion semantica de que es "un subtema de arquitectura" no existe en Markdown.
Un humano sabe que "1/28" es una fecha, pero una maquina tiene que adivinar.
28 de enero, o un veintiocho-avo?

En ultima instancia, para "entender" Markdown, un LLM debe realizar interpretacion de lenguaje natural.
Markdown es lenguaje natural con indentacion superpuesta ---
no son datos estructurados.

---

## JSON: estructura sin significado

JSON va un paso mas alla que Markdown.

```json
{
  "entity": "Yi Sun-sin",
  "birth": "1545",
  "death": "1598",
  "occupation": "naval_commander"
}
```

Hay estructura. Los pares clave-valor son explicitos.
Una maquina puede parsearlo. Los campos son accesibles.

Pero hay un problema.

**JSON no sabe que significa la clave "entity".**

La persona que creo este JSON sabe que "entity" significa "un objeto."
En el JSON de otra persona, el mismo concepto podria ser "name", "subject" o "item."

```json
{"name": "Yi Sun-sin"}
{"subject": "Yi Sun-sin"}
{"item": "Yi Sun-sin"}
{"entity": "Yi Sun-sin"}
```

Cuatro JSON expresan lo mismo,
pero una maquina no puede saber que son lo mismo.

JSON carece de **semantica compartida.**
Hay estructura, pero no hay acuerdo sobre lo que esa estructura significa.

Cada proyecto crea su propio esquema.
Cada API usa sus propios nombres de campo.
Conectar el esquema A con el esquema B requiere otra capa de transformacion.

Esto es la Torre de Babel.
La estructura existe, pero nadie entiende la estructura del otro.

---

## XML: el impuesto de la verbosidad

XML intento resolver el problema de JSON.

Namespaces, definiciones de esquema (XSD), definiciones de tipo de documento (DTD).
Proporciona meta-estructuras que definen el significado de las estructuras.

```xml
<entity xmlns="http://example.org/schema">
  <name>Yi Sun-sin</name>
  <birth>
    <year>1545</year>
    <calendar>lunar</calendar>
  </birth>
  <death>
    <year>1598</year>
    <cause>killed_in_action</cause>
  </death>
</entity>
```

El significado puede definirse. La estructura puede imponerse con esquemas.
Es mas riguroso que JSON.

Pero XML tiene un problema fatal.

**Es verboso.**

En el XML anterior, la informacion real es "Yi Sun-sin, 1545, 1598, killed_in_action."
Todo lo demas son etiquetas. Las etiquetas de apertura y cierre superan en numero a la informacion.

Por que es esto un problema para la IA?

La ventana de contexto de un LLM es finita.
Si transmitir la misma informacion requiere 3x los tokens,
la cantidad de informacion que cabe en el contexto se reduce a un tercio.

XML es verboso para que los humanos puedan leerlo facilmente.
Un lenguaje de razonamiento de IA no debe tener este desperdicio.
Para un LLM, la etiqueta `<name>` es desperdicio.

Y XML es un diseno de principios de los 2000.
Se creo en una era cuando los LLM no existian, para humanos y software tradicional.
Nunca se diseno como un lenguaje de razonamiento de IA.

---

## La limitacion compartida

Markdown, JSON, XML.
Cada uno de los tres formatos tiene sus fortalezas, pero comparten limitaciones comunes.

**Son basados en texto.**
Todos se serializan en cadenas.
Una maquina debe parsearlos para procesarlos.
El parseo es un costo.

Un lenguaje de razonamiento ideal es un flujo binario.
Una secuencia de palabras de 16 bits. No se necesita parseo.
Interpretable en el instante en que se lee.

**Fueron disenados antes de la era LLM.**
Markdown es de 2004. JSON es de 2001. XML es de 1998.
Se disenaron en una era cuando el concepto de LLM no existia,
para humanos o software tradicional.

Un lenguaje de razonamiento de IA debe disenarse en la era LLM, para LLM.
El principio de diseno "1 palabra = 1 token"
presupone la existencia de LLM.

**Su sistema semantico unificado esta ausente o es incompleto.**
Markdown no tiene sistema semantico en absoluto.
JSON tiene estructura pero no significado.
XML puede definir esquemas pero no estan unificados.

Un indice semanticamente alineado es un ID de significado unificado globalmente.
Donde sea que se use, el mismo SIDX significa lo mismo.
No se necesita conversion. El consenso esta integrado.

---

## Resumen

| Formato | Estructura | Significado | Amigable con LLM | Binario | Soporte de afirmaciones | Modificadores verbales |
|--------|-----------|---------|---------------|--------|---------------|----------------|
| Markdown | Debil | Ninguno | Alto | No | Ninguno | Ninguno |
| JSON | Si | Ninguno | Medio | No | Ninguno | Ninguno |
| XML | Si | Parcial | Bajo | No | Ninguno | Ninguno |
| **Lenguaje de razonamiento ideal** | **Si** | **Si** | **Alto** | **Si** | **Si** | **Si** |

Un nuevo formato se necesita no porque los formatos existentes sean malos.
Es porque los formatos existentes fueron hechos en una era diferente, para un proposito diferente.

Markdown fue hecho para documentos que los humanos leen.
JSON fue hecho para intercambio de datos en APIs web.
XML fue hecho para serializacion de proposito general de documentos y datos.

Un formato para registrar y acumular el razonamiento de la IA. Eso aun no existe.

Cuando el proposito es diferente, la herramienta debe ser diferente.
