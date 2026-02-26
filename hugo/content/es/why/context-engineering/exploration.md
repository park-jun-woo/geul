---
title: "Por que la exploracion es necesaria"
weight: 7
date: 2026-02-26T12:00:07+09:00
lastmod: 2026-02-26T12:00:07+09:00
tags: ["exploracion", "busqueda", "escala"]
summary: "Cuando el indice supera la ventana, el paradigma de busqueda alcanza su limite"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Cuando el indice supera la ventana, el paradigma de busqueda alcanza su limite.

---

## La busqueda ha tenido exito

Discutimos los limites de RAG.
La imprecision de la similitud de embedding, la arbitrariedad de la division en fragmentos, la imposibilidad del juicio de calidad.

Pero esa discusion era sobre la calidad de la busqueda.
"Como debemos buscar con mayor precision?"

Ahora hay que hacer una pregunta diferente.
Supongamos que la busqueda es perfecta.
Supongamos que devuelve solo informacion precisamente relevante para la consulta.

Aun asi hay casos en que no funciona.

---

## El problema de la escala

Una base de conocimiento interna tiene 1.000 declaraciones.
Hay un indice. Pon el indice en el contexto. Consulta. Recupera resultados.
Funciona.

Las declaraciones crecen a 100.000.
El indice se agranda. Aun cabe en la ventana. Funciona.

Las declaraciones crecen a 10 millones.
El indice mismo supera la ventana.

Esto no es un problema de calidad de busqueda.
No importa cuan precisa sea la busqueda,
si el indice que debe consultarse para buscar no cabe en la ventana,
la busqueda ni siquiera puede comenzar.

Y el conocimiento crece.
Los documentos corporativos aumentan cada dia.
Lo que un agente ha aprendido sigue acumulandose.
El conocimiento del mundo no se reduce.

Una ventana mas grande resuelve esto?
Si 128K se convierte en 1M y luego en 10M?
Si el conocimiento llega a 100M, el mismo problema se repite.
La ventana siempre es finita, y el conocimiento siempre crece.
Este desequilibrio es permanente.

---

## La diferencia entre busqueda y exploracion

La busqueda obtiene resultados con una sola consulta.

Consulta: "Beneficio operativo de Samsung Electronics Q3 2024"
-> Resultado: 9,18 billones de won.

Un intento. Listo.

La exploracion llega a los resultados a traves de multiples pasos.

Paso 1: Ver el mapa de conocimiento de nivel superior. "Corporaciones," "Industrias," "Macroeconomia," "Tecnologia"...
-> Seleccionar "Corporaciones."

Paso 2: Ver el mapa de corporaciones. "Samsung Electronics," "SK Hynix," "Hyundai Motor"...
-> Seleccionar "Samsung Electronics."

Paso 3: Ver el mapa de Samsung Electronics. "Finanzas," "Recursos Humanos," "Tecnologia," "Legal"...
-> Seleccionar "Finanzas."

Paso 4: Ver el mapa de finanzas. "Resultados trimestrales," "Resultados anuales," "Planes de inversion"...
-> Seleccionar "Resultados trimestrales."

Paso 5: Recuperar "Q3 2024" de los resultados trimestrales.
-> Beneficio operativo: 9,18 billones de won.

El resultado es el mismo.
El proceso es diferente.

La busqueda es preguntar "Tienes esto?"
La exploracion es rastrear "Donde podria estar?"

La busqueda requiere que el indice sea visible para quien consulta. El indice completo debe ser accesible.
La exploracion solo necesita ver la capa actual del mapa. En cada paso, solo una capa entra a la ventana.

---

## La analogia de la biblioteca

Visitas una biblioteca de barrio.
Tiene 3.000 libros.
Le preguntas al bibliotecario: "Tienen una biografia de Yi Sun-sin?"
El bibliotecario recuerda: "Esta al final del estante 3."
Busqueda. Funciona.

Visitas la Biblioteca Nacional.
Tiene 10 millones de volumenes.
Le preguntas al bibliotecario: "Tienen una biografia de Yi Sun-sin?"
El bibliotecario tampoco lo sabe. Nadie memoriza 10 millones de volumenes.

En cambio, hay un sistema de clasificacion.

Consultas el directorio de la planta baja. -> La seccion de "Historia" esta en el 3er piso.
Subes al 3er piso. -> "Historia de Corea" esta en el ala este.
Vas al ala este. -> "Dinastia Joseon" esta en la fila D.
Vas a la fila D. -> "Personajes" esta en la 3a seccion de la fila D.
Buscas en la 3a seccion. -> Hay una biografia de Yi Sun-sin.

La capacidad de memoria del bibliotecario no ha cambiado.
La escala de la biblioteca ha cambiado.
El metodo paso de preguntar al bibliotecario (busqueda) a recorrer el sistema de clasificacion (exploracion).

Aqui esta la clave.
En cada paso, el tamano de lo que debe verse cabe dentro de la capacidad de memoria del bibliotecario.
El directorio de la planta baja. El mapa de zonas del 3er piso. La lista de filas del ala este. La lista de secciones de la fila D.
Todo cabe en una sola mirada.

El catalogo completo de todos los fondos no cabe en una sola mirada.
Pero el mapa de cada piso si.

Asi es como la exploracion difiere de la busqueda.
No necesitas ver el todo de una vez.
Solo necesitas juzgar la siguiente direccion desde donde estas ahora.

---

## Mapas de mapas

En terminos tecnicos, esta es una estructura jerarquica de mapas.

**Mapa de nivel 1**: la clasificacion de nivel superior de todo el conocimiento.
"Esta base de conocimiento contiene informacion sobre corporaciones, industrias, macroeconomia y tecnologia."
Decenas de elementos. Cabe en la ventana.

**Mapa de nivel 2**: las subcategorias de cada clasificacion de nivel superior.
"La categoria de corporaciones contiene Samsung Electronics, SK Hynix, Hyundai Motor..."
De decenas a cientos de elementos. Cabe en la ventana.

**Mapa de nivel 3**: las categorias detalladas de cada subcategoria.
"Samsung Electronics contiene Finanzas, Recursos Humanos, Tecnologia, Legal..."
Decenas de elementos. Cabe en la ventana.

**Declaraciones reales**: la informacion concreta a la que apunta el mapa del nivel mas bajo.
"El beneficio operativo de Samsung Electronics en el Q3 2024 fue de 9,18 billones de won."

Si el tamano de cada capa cabe dentro de la ventana,
la exploracion es posible independientemente de la escala total del conocimiento.

Incluso con 10 millones de declaraciones,
si cada capa tiene 100 elementos, se alcanza el objetivo en 5 pasos de exploracion.
100 -> 100 -> 100 -> 100 -> 100 = cobertura de hasta 10 mil millones.
En cada paso, solo 100 elementos entran a la ventana.

Es la misma forma en que un B-tree encuentra datos en el disco.
No carga todos los datos en memoria.
Lee solo el nodo actual del arbol y avanza al siguiente.
Datos de cualquier escala pueden explorarse independientemente del tamano de la memoria.

La ventana de contexto es la memoria.
La base de conocimiento es el disco.
El mapa es un nodo del B-tree.

---

## El agente camina

En la exploracion de multiples pasos, quien selecciona la direccion en cada paso?

El agente.

Pon el mapa de nivel 1 en el contexto.
El agente lo lee, lo compara con la consulta y selecciona la direccion "Corporaciones."

Solicita el mapa de nivel 2.
El mapa de subcategorias de corporaciones entra al contexto.
El agente lo lee y selecciona la direccion "Samsung Electronics."

Solicita el mapa de nivel 3.
El agente selecciona "Finanzas."

Este es el uso de herramientas del agente.
Leer un mapa es una llamada a herramienta.
Seleccionar una direccion es un juicio.
Solicitar el siguiente mapa es la siguiente llamada a herramienta.

En la busqueda, el agente consulta una vez y recibe un resultado. Pasivo.
En la exploracion, el agente hace multiples juicios y selecciona direcciones. Activo.

Aqui es donde la ingenieria de contexto se encuentra con el diseno de agentes.
Lo que entra al contexto se determina paso a paso a traves del juicio del agente.
La construccion del contexto pasa de ensamblaje estatico a exploracion dinamica.

---

## Este problema apenas se discute hoy

Mirando las discusiones en la comunidad de RAG,
la mayor parte de la energia se enfoca en la calidad de la busqueda.

Mejores modelos de embedding.
Mejores estrategias de fragmentacion.
Arquitecturas de reranker.
Busqueda hibrida.
Graph RAG.

Todo importante.
Todo sobre "como obtener mejores resultados de una sola busqueda."

"Que pasa si una sola busqueda no es suficiente?" apenas se discute.

El momento en que el indice supera la ventana.
El momento en que los resultados son demasiados para caber.
El momento en que la escala del conocimiento rompe la premisa del paradigma de busqueda mismo.

Ese momento esta llegando.
El conocimiento crece y la ventana es finita.

La mayoria de las soluciones actuales son evasion.
Recuperar solo los top k. Descartar el resto.
Agrandar la ventana. Los costos aumentan.
Particionar el conocimiento. Separar almacenes vectoriales por dominio.

Todas encuentran el mismo problema de nuevo cuando la escala crece mas.

---

## Prerrequisitos para la exploracion

Para que la exploracion funcione, el conocimiento debe estar en una estructura explorable.

**Debe existir una jerarquia.** Si el conocimiento esta dispuesto de forma plana, la exploracion es imposible. Un almacen de vectores de embedding es plano. Todos los fragmentos estan al mismo nivel. No hay jerarquia, asi que el concepto de "profundizar" no existe.

**Cada capa debe caber en la ventana.** Si un solo mapa supera la ventana, la exploracion falla. El numero de opciones en cada nivel de la jerarquia debe ser de tamano apropiado. Esto es un problema de diseno de clasificacion.

**Los caminos deben ser diversos.** Debe ser posible llegar a la misma informacion por multiples caminos. A traves de "Samsung Electronics -> Finanzas -> Beneficio operativo" o a traves de "Industria semiconductora -> Principales empresas -> Samsung Electronics -> Resultados." Porque el camino natural varia segun la pregunta. Si el criterio de clasificacion esta fijado en uno solo, se ajusta a algunas preguntas y a otras no.

Una estructura de carpetas tiene jerarquia pero solo un camino.
Un archivo pertenece a una sola carpeta.
Solo existe el camino "Samsung Electronics/Finanzas/Beneficio operativo."
Cuando llega una pregunta sobre "la industria semiconductora," la exploracion natural a traves de esta estructura de carpetas es imposible.

Un grafo tiene tanto jerarquia como caminos diversos.
Un solo nodo puede estar conectado a multiples nodos padre.
El nodo de Samsung Electronics puede alcanzarse por un camino de "Corporaciones," un camino de "Industria semiconductora" o un camino de "Empresas cotizadas en KOSPI."
Independientemente del contexto del que provenga una pregunta, existe un camino natural.

---

## Este es un problema sin resolver

Hay algo que debe decirse con honestidad.

La necesidad de la exploracion en multiples pasos es clara.
Pero aun no existe un sistema estandar que lo implemente de forma efectiva.

Como se genera automaticamente la jerarquia de mapas?
Como se determina el tamano apropiado de cada capa?
Que pasa cuando el agente selecciona la direccion equivocada?
Que pasa con la latencia a medida que aumenta la profundidad de exploracion?

Estas son preguntas abiertas.

Pero el hecho de que un problema no este resuelto
no significa que el problema no exista.

El conocimiento esta creciendo.
La ventana es finita.
El punto donde la busqueda sola no es suficiente esta llegando.

La exploracion debe estar lista como respuesta para ese punto.
Si no esta lista,
las unicas opciones que quedan son agrandar la ventana o descartar conocimiento.

---

## Resumen

La busqueda devuelve resultados con una sola consulta.
Cuando la escala del conocimiento crece lo suficiente, esto no es suficiente.
Porque el indice mismo supera la ventana.

La exploracion sigue mapas jerarquicos, seleccionando direcciones mientras desciende.
Lo que debe verse en cada paso cabe dentro de la ventana.
Cada paso es finito independientemente de la escala total.
De la misma forma que un B-tree encuentra datos sin cargar todo el disco en memoria.

El agente juzga la direccion en cada paso.
La construccion del contexto pasa de ensamblaje estatico a exploracion dinamica.
Aqui es donde la ingenieria de contexto se encuentra con el diseno de agentes.

Para que la exploracion funcione, el conocimiento debe ser jerarquico, cada capa debe ser finita y los caminos deben ser diversos.
Una estructura de carpetas tiene solo un camino. Un grafo tiene caminos diversos.

Este sigue siendo un problema sin resolver y sin solucion estandar.
Pero mientras el conocimiento crece y la ventana es finita, es un problema que debe resolverse.
