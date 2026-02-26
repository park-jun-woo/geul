---
title: "Por que la era de la ingenieria de prompts termino"
weight: 1
date: 2026-02-26T12:00:12+09:00
lastmod: 2026-02-26T12:00:12+09:00
tags: ["prompt", "contexto", "ingenieria"]
summary: "De como lo dices a que le muestras — el juego ha cambiado"
author: "박준우"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Por que la era de la ingenieria de prompts termino

### De "como lo dices" a "que le muestras" — el juego ha cambiado.

---

### La ingenieria de prompts como profesion

En 2023, aparecio una nueva profesion.

Ingeniero de prompts.

"Piensa paso a paso."
"Eres un experto con 20 anos de experiencia."
"Dejame mostrarte algunos ejemplos primero."

Frases como estas se convirtieron en conocimiento valorado en decenas de miles de dolares. La misma pregunta producia respuestas dramaticamente diferentes de la IA dependiendo de como la formularas.

La ingenieria de prompts genuinamente funcionaba.
Una sola linea de Chain-of-Thought elevaba las puntuaciones de matematicas un 20%.
Una sola frase asignando un rol cambiaba la profundidad del conocimiento experto.
Tres ejemplos few-shot daban control completo sobre el formato de salida.

Esto no era exageracion. Era real.
Entonces, por que esta terminando?

---

### Por que funcionaba: porque los modelos eran suficientemente tontos

Mira por que funcionaba la ingenieria de prompts desde primeros principios. Es simple.

Los primeros LLM eran malos captando la intencion del usuario.
Decir "resume" y reescribian en su lugar.
Decir "compara" y listaban en su lugar.

Porque el modelo malinterpretaba la intencion,
la habilidad de transmitir la intencion precisamente se volvio valiosa.
La ingenieria de prompts era esencialmente "interpretacion" —
traducir la intencion humana a una forma que el LLM pudiera entender.

Para que la interpretacion sea valiosa, debe haber una barrera idiomatica.

---

### Lo que cambio: los modelos se volvieron inteligentes

De GPT-3.5 a GPT-4. De Claude 2 a Claude 3.5.
Con cada generacion, la capacidad de los modelos para captar la intencion mejoro dramaticamente.

Decir "resume" y resumen.
Decir "compara" y comparan.
Incluso sin que les digan "piensa paso a paso", descomponen problemas complejos en pasos por su cuenta.

La barrera idiomatica se redujo.
El valor de la interpretacion se encogio.

Las tecnicas de prompt que producian diferencias dramaticas en 2023
producen solo diferencias marginales en 2025.
Cuando el modelo es suficientemente inteligente, la formulacion importa cada vez menos.

Entonces, que importa en su lugar?

---

### La ventana de contexto: una ley de la fisica

Los LLM tienen una restriccion fisica.

La ventana de contexto.

Sean 128K tokens o 1M tokens, es finita.
Solo la informacion que cabe dentro de este espacio finito influye en el razonamiento.
La informacion fuera de la ventana, sin importar cuan importante sea, podria no existir.

Esto es independiente del tamano del modelo.
Incluso con un billon de parametros, la ventana de contexto es finita.
Incluso con datos de entrenamiento que abarcan todo internet, la ventana de contexto es finita.

No importa cuan inteligente sea el modelo,
si informacion incorrecta entra en el contexto, produce respuestas incorrectas.
Si informacion irrelevante llena el contexto, se pierde lo que importa.
Si la informacion necesaria falta en el contexto, es como si fuera desconocida.

La ingenieria de prompts era un problema de "como lo dices."
El nuevo juego es un problema de "que le muestras."

Esto es ingenieria de contexto.

---

### Analogia: el examen a libro abierto

Aqui hay una analogia para la diferencia entre ingenieria de prompts e ingenieria de contexto.

La ingenieria de prompts es escribir bien las preguntas del examen.
En lugar de "elige la respuesta correcta a continuacion",
escribe "deriva la respuesta paso a paso que satisfaga todas las siguientes condiciones" —
y el estudiante da una mejor respuesta.

La ingenieria de contexto es la pregunta de que libros traes a un examen a libro abierto.
No importa cuan bien esten escritas las preguntas del examen,
si el estudiante trajo los libros equivocados, no puede responder.
El numero de libros que puedes traer es limitado.
Que libros traes determina tu calificacion.

Cuando el modelo era tonto, el formato de la pregunta (prompt) importaba.
Cuando el modelo es inteligente, el material de referencia (contexto) importa.

---

### La era de los agentes acelera el cambio

Este cambio se esta acelerando con la aparicion de los agentes.

La ingenieria de prompts es escrita por humanos cada vez.
Los humanos escriben la pregunta, los humanos explican el contexto, los humanos especifican el formato.

Los agentes son diferentes.
Los agentes razonan por su cuenta, llaman herramientas y colaboran con otros agentes.
En cada paso, deben componer el contexto ellos mismos.

Un agente llamo a una API externa y recibio datos.
Estos datos necesitan ir al contexto para la siguiente ronda de razonamiento.
Que partes entran y cuales se quedan fuera?
Que resultados de razonamiento previos se mantienen y cuales se descartan?
Se puede confiar en la informacion enviada por otro agente?

Un humano no puede tomar todas estas decisiones cada vez.
Para que los agentes operen de forma autonoma,
la composicion del contexto debe automatizarse.

La ingenieria de prompts era una habilidad humana.
La ingenieria de contexto debe ser una capacidad del sistema.

---

### La ingenieria de prompts no esta desapareciendo

Permitan prevenir un malentendido.

No estoy diciendo que la ingenieria de prompts se esta volviendo insignificante.
Los system prompts siguen siendo importantes.
La especificacion de formato de salida sigue siendo necesaria.
Declarar roles y restricciones sigue siendo efectivo.

Lo que se esta reduciendo es la proporcion que la ingenieria de prompts ocupa.

Si el 70% de la calidad de la salida estaba determinado por el prompt en 2023,
en 2025, el 30% esta determinado por el prompt y el 70% por el contexto.

La proporcion se invirtio.

Y esta tendencia no se esta revirtiendo.
Los modelos seguiran haciendose mas inteligentes,
y cuanto mas inteligentes se vuelvan, menos importa la formulacion
y mas importa el contexto.

---

### Pero la ingenieria de contexto no tiene infraestructura

Aqui esta el punto crucial.

La ingenieria de prompts tenia herramientas.
Plantillas de prompts, bibliotecas de prompts, frameworks de prueba de prompts.
Se construyo todo un ecosistema para gestionar sistematicamente "como lo dices."

La ingenieria de contexto aun no tiene esto.

Mira como se maneja el contexto en la practica ahora mismo.

Los tamanos de chunk del pipeline RAG se ajustan a mano.
La informacion de fondo se escribe en system prompts a mano.
Que almacenar en la memoria de un agente se disena a mano.
Que resultados de busqueda poner en el contexto se decide a mano.

Todo es manual.

Y la materia prima de todo ese trabajo manual es lenguaje natural.
Documentos en lenguaje natural se cortan en lenguaje natural y se pegan en un contexto en lenguaje natural.

El lenguaje natural tiene baja densidad de informacion.
Sin fuentes. Sin niveles de confianza. Sin marcas de tiempo.
Se consumen tokens innecesarios para transmitir el mismo significado.
No hay forma de automatizar el juicio de calidad.

Esto se parece a la era pre-ingenieria-de-prompts.
La ingenieria de prompts tambien era manual al principio.
Se basaba en la intuicion y experiencia individual.
Luego surgieron herramientas y metodologias y se sistematizo.

La ingenieria de contexto esta en esa etapa previa ahora mismo.
El problema se ha reconocido, pero la infraestructura no existe.

---

### Lo que la infraestructura necesita

Para que la ingenieria de contexto pase de trabajo manual a sistema,
como minimo se requiere lo siguiente.

**Compresion.** Una forma de meter mas significado en la misma ventana.
Elimina el pegamento gramatical del lenguaje natural y deja solo el significado,
y el tamano efectivo de la ventana se multiplica — sin cambiar el modelo.

**Indexacion.** Una forma de encontrar la informacion correcta con precision.
Busqueda basada en estructura semantica, no similaridad de embeddings.
Una busqueda donde buscar "ingresos de Apple" no traiga "informacion nutricional de la manzana."

**Validacion.** Una forma de rechazar mecanicamente informacion que no cumple la especificacion.
Asi como un compilador de Go detecta variables no usadas como errores,
las afirmaciones sin fuentes y los hechos sin marcas de tiempo deberian filtrarse antes de entrar al contexto.
Las verificaciones mas baratas y deterministicas deben ir primero.

**Filtrado.** Una forma de juzgar la calidad semantica.
Si la validacion mira la forma, el filtrado mira el contenido.
Relevancia, fiabilidad, frescura. Es esta informacion verdaderamente necesaria para esta ronda de razonamiento?

**Consistencia.** Una forma de garantizar la coherencia interna del conjunto de informacion seleccionado.
Piezas de informacion individualmente buenas pueden contradecirse cuando se combinan.
Si el CEO de 2020 y el CEO de 2024 entran al contexto simultaneamente,
el LLM se confunde.

**Composicion.** Una forma de optimizar la colocacion y estructura dentro de la ventana.
La misma informacion recibe diferentes pesos de atencion dependiendo de donde se coloque.
Al frente o atras? Como se agrupa?

**Acumulacion.** Una forma de que el sistema aprenda y crezca con el tiempo.
El caching es la reutilizacion de resultados individuales.
La acumulacion es aprender que composiciones de contexto produjeron buenos resultados,
y hacer crecer la base de conocimiento misma.

Estas siete son la pila completa de infraestructura de ingenieria de contexto.

---

### Esto no se trata de ninguna herramienta en particular

Permitan ser franco.

Quien construye esta infraestructura es una pregunta abierta.
Una herramienta podria resolverlo todo,
o multiples herramientas podrian manejar cada capa.

Pero el hecho de que se necesita infraestructura no es una pregunta abierta.

Que la ventana de contexto es finita es un hecho fisico.
Incluso si la ventana crece 10x, la informacion del mundo crece mas rapido.
Que el lenguaje natural tiene baja densidad de informacion es un hecho estructural.
Que los agentes necesitan gestion de contexto automatizada para operar autonomamente es una necesidad logica.

Asi como la ingenieria de prompts necesitaba herramientas,
la ingenieria de contexto necesita herramientas.
Pero esta vez, la naturaleza de las herramientas es diferente.

Las herramientas de ingenieria de prompts se parecian mas a editores de texto.
Las herramientas de ingenieria de contexto se parecen mas a compiladores.

Comprimir informacion, indexarla, validarla, filtrarla,
verificar consistencia, optimizar colocacion y acumular resultados.
Esto no es edicion. Esto es ingenieria.

Por eso se llama ingenieria de "contexto."

---

### Resumen

La ingenieria de prompts era valiosa cuando los modelos eran tontos.
Porque los modelos no podian leer la intencion, la habilidad de transmitir bien la intencion importaba.

A medida que los modelos se volvieron mas inteligentes, el juego cambio.
De "como lo dices" a "que le muestras."
Del prompt al contexto.

La aparicion de agentes acelera este cambio.
Los humanos no pueden ensamblar el contexto cada vez.
El sistema debe hacerlo por su cuenta.

Pero ahora mismo, la ingenieria de contexto no tiene infraestructura.
El lenguaje natural se esta cortando y pegando a mano.

La infraestructura requerida tiene siete capas:
compresion, indexacion, validacion, filtrado, consistencia, composicion, acumulacion.

No es la era de la ingenieria de prompts la que esta terminando.
Es la era en que la ingenieria de prompts sola era suficiente.
