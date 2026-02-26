---
title: "Por que las verificaciones de consistencia son necesarias"
weight: 6
date: 2026-02-26T12:00:08+09:00
lastmod: 2026-02-26T12:00:08+09:00
tags: ["consistencia", "contradiccion", "coherencia"]
summary: "La informacion individualmente correcta puede ser colectivamente erronea"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## La informacion individualmente correcta puede ser colectivamente erronea.

---

## La verificacion paso. El filtrado paso.

La verificacion mecanica filtro los errores de formato.
El filtrado selecciono segun relevancia, confiabilidad y actualidad.

Quedan 30 piezas de informacion.
Todas validas, todas relevantes, todas confiables, todas actuales.

Pones estas 30 en el contexto?

No.
Hay una cosa mas que verificar.
Estas 30 se contradicen entre si?

---

## La contradiccion no es una propiedad de la informacion individual

Considera estas dos declaraciones.

- Fuente: divulgacion IR de Samsung Electronics, octubre 2024. "CEO de Samsung Electronics: Jun Young-hyun."
- Fuente: divulgacion IR de Samsung Electronics, marzo 2024. "CEO de Samsung Electronics: Kyung Kye-hyun."

Individualmente, ambas son validas.
El formato es correcto, la fuente esta presente, el tiempo esta presente, y son confiables.
Pasan la verificacion. Pasan el filtrado.

Pero cuando ambas entran al mismo contexto, hay un problema.
El CEO de Samsung Electronics es Jun Young-hyun o Kyung Kye-hyun?

Ninguna declaracion es incorrecta.
En marzo, Kyung Kye-hyun era correcto. En octubre, Jun Young-hyun es correcto.
Individualmente, ambas son correctas.
Pero cuando coexisten en el contexto, el LLM se confunde.

Este es el problema de la consistencia.
Surge no de la informacion individual sino del conjunto de informacion.
La verificacion examina la informacion individual. El filtrado examina la informacion individual.
La consistencia examina el espacio entre las piezas de informacion.

---

## Tipos de contradiccion

Las contradicciones en el contexto se clasifican en varios tipos.

### Contradiccion temporal

La mas comun.

La misma propiedad de la misma entidad ha cambiado a lo largo del tiempo,
y valores de diferentes momentos coexisten en el contexto.

"CEO de Tesla: Elon Musk" y
"Precio de la accion de Tesla: $194" estan en el mismo contexto,
pero la informacion del CEO es de 2024 y el precio de la accion es de junio de 2023.
El LLM puede tratarlos como informacion del mismo momento.

Tambien surgen casos mas sutiles.
"Tasa de interes base de Corea del Sur: 3,50%" es de enero de 2024, y
"Inflacion del precio al consumidor de Corea del Sur: 2,0%" es de octubre de 2024.
Ambas son validas y ambas se refieren a la economia coreana,
pero hay una brecha de 9 meses.
Si esta brecha afecta la inferencia depende del contexto.

### Contradiccion entre fuentes

Diferentes fuentes presentan valores distintos para el mismo hecho.

- Fuente A: "Tamano del mercado global de IA en 2024: $184 mil millones."
- Fuente B: "Tamano del mercado global de IA en 2024: $214 mil millones."

Ninguna puede declararse definitivamente "incorrecta."
La definicion del alcance del mercado puede diferir. Los metodos de medicion pueden diferir.
Pero si ambas estan en el contexto,
el LLM debe elegir una, combinar ambas o confundirse.

### Contradiccion inferencial

No son valores directamente contradictorios,
pero son logicamente incompatibles cuando se colocan juntos.

"Cuota de mercado de la Empresa A: 60%."
"Cuota de mercado de la Empresa B: 55%."

Cada una es valida. Pero suman 115%.
Agregando los competidores restantes se superaria el 100%.
Una de ellas es de un momento diferente, usa una definicion de mercado diferente, o es incorrecta.

Este tipo de contradiccion no puede encontrarse mirando declaraciones individuales.
Se debe examinar el conjunto.

---

## Los LLM no manejan bien las contradicciones

En teoria, el LLM deberia poder detectar y resolver contradicciones.
"Estas dos piezas de informacion difieren en el tiempo, asi que respondere basandome en la mas reciente."

En la practica, eso no es lo que ocurre.

**Los LLM tienden a confiar en la informacion del contexto.**
El acto de poner algo en el contexto es en si mismo una senal que dice "consulta esto."
Cuando dos piezas de informacion contradictoria estan presentes,
el LLM tiende a referenciar ambas en lugar de ignorar una.
El resultado es una mezcla o confusion.

**La deteccion de contradicciones requiere razonamiento.**
Saber que "CEO: Jun Young-hyun" y "CEO: Kyung Kye-hyun" se contradicen
requiere el conocimiento de fondo de que solo hay un CEO en un momento dado.
Verificar si las cuotas de mercado suman mas del 100% requiere aritmetica.
Esto depende de la capacidad de razonamiento del LLM.

**La resolucion es aun mas dificil.**
Incluso si se detecta una contradiccion, hay que juzgar que lado elegir.
El mas reciente? La fuente mas confiable? El que tiene mas fuentes de apoyo?
Si este juicio se deja al LLM, la consistencia no esta garantizada.
Para la misma contradiccion, a veces elige A y a veces B.

En conclusion, manejar las contradicciones despues de que entran al contexto
es caro y el resultado es incierto.
Las contradicciones deben resolverse antes de entrar al contexto.

---

## Por que la verificacion de consistencia es dificil en lenguaje natural

Supongamos que estas verificando la consistencia de 30 fragmentos de lenguaje natural.

Primero, debes determinar si tratan del mismo tema.
Si "Samsung Electronics," "Samsung Electronics" y "Samsung" se refieren a la misma entidad.
En lenguaje natural, esto es incierto.
Si "Samsung" significa Samsung Electronics, Samsung C&T o Samsung Life requiere leer el contexto.

Luego, debes determinar si describen la misma propiedad.
Si "ingresos," "ingresos," "ingresos totales" e "ingresos brutos" son lo mismo.
Si "beneficio operativo," "beneficio operativo" y "margen operativo" son lo mismo o diferente.

Luego, debes extraer las referencias temporales.
Cuando es "el trimestre pasado"? Cuando es "recientemente"? Cuando es "este ano"?

Solo despues de todo esto puedes finalmente comparar si dos declaraciones se contradicen.

Con 30 declaraciones, hay 435 pares de comparacion.
Cada par debe pasar por el proceso anterior.
Todo razonamiento del LLM.
Todo caro.
Todo probabilistico.

---

## Verificacion de consistencia en representaciones estructuradas

En una representacion estructurada, la situacion es diferente.

**La identificacion de entidades es determinista.**
La entidad "Samsung Electronics" tiene un identificador unico.
"Samsung Electronics" apunta al mismo identificador.
No se necesita razonamiento para determinar la identidad.

**Las propiedades son explicitas.**
"Ingresos" es una propiedad tipada.
"Margen operativo" es una propiedad diferente.
Si dos propiedades son iguales o diferentes se confirma por comparacion de campos.

**El tiempo es un campo.**
Hay un valor como "2024-Q3."
No es necesario interpretar "el trimestre pasado."
Si dos declaraciones comparten el mismo tiempo es una comparacion de valores.

Cuando estas tres cosas son deterministas, los patrones de deteccion de contradicciones se vuelven mecanizables.

Misma entidad + misma propiedad + mismo tiempo + valor diferente = contradiccion.
Misma entidad + misma propiedad + tiempo diferente + valor diferente = cambio. No es contradiccion.
Entidad diferente + misma propiedad + mismo tiempo + suma de valores > 100% = contradiccion inferencial.

No se necesita un LLM para esto.
Comparacion de campos y aritmetica.

No todas las contradicciones pueden detectarse.
Si "el mercado de IA esta creciendo" y "la inversion en IA esta declinando" se contradicen
aun requiere juicio semantico.
Pero si las contradicciones detectables mecanicamente se capturan primero,
solo quedan los casos que requieren juicio semantico.
Una vez mas, lo barato va primero.

---

## Estrategias de resolucion para verificaciones de consistencia

Despues de detectar una contradiccion, debe resolverse.

Las estrategias de resolucion varian segun el contexto, pero en una representacion estructurada pueden declararse como politica.

**Lo mas reciente primero.** Cuando la misma propiedad de la misma entidad entra en conflicto, elegir la de marca temporal mas reciente. Adecuada para valores cambiantes como CEO, precio de acciones, poblacion.

**Mayor confianza primero.** Elegir la de mayor confianza. O si hay una jerarquia de fuentes definida, elegir la fuente de mayor rango. Fuente primaria > fuente secundaria > fuente no oficial.

**Presentar ambas.** No resolver la contradiccion. Poner ambas en el contexto, pero marcar la contradiccion explicitamente. "La fuente A dice $184 mil millones; la fuente B dice $214 mil millones. Probablemente se debe a diferencias de definicion." Dejar que el LLM razone con conciencia de la contradiccion.

**Excluir ambas.** Si la contradiccion no puede resolverse, excluir ambos lados. Ninguna informacion es mejor que informacion incorrecta.

En un pipeline de lenguaje natural, estas estrategias se escriben en lenguaje natural en el prompt.
"Por favor, priorice la informacion mas reciente."
Si el LLM sigue esto de forma consistente es, de nuevo, cuestion de probabilidad.

En una representacion estructurada, estas estrategias se declaran como politica.
"En conflicto de misma-entidad + misma-propiedad: marca temporal mas reciente primero. Si las marcas temporales son iguales: mayor confianza primero. Si la confianza es igual: presentar ambas."
La maquina lo ejecuta. No es probabilidad.

---

## Posicion en el pipeline

La verificacion de consistencia viene despues del filtrado.

Verificacion -> Filtrado -> Consistencia.

Por que este orden?

La verificacion filtra los errores de formato.
El filtrado elimina la informacion innecesaria.
La verificacion de consistencia solo necesita procesar lo que paso la verificacion y el filtrado.

La verificacion de consistencia compara pares.
Para n declaraciones, hay n(n-1)/2 pares.
1.000 produce aproximadamente 500.000 pares. 30 produce 435.

Si la verificacion y el filtrado reducen 1.000 a 30,
el costo de la verificacion de consistencia cae de 500.000 a 435 -- una milesima parte.

El orden importa.

---

## Resumen

La informacion que es individualmente valida, relevante y confiable
puede contradecirse cuando se reune como conjunto.

Hay tres tipos de contradiccion.
Contradiccion temporal -- valores de diferentes momentos coexisten.
Contradiccion entre fuentes -- diferentes fuentes presentan valores distintos.
Contradiccion inferencial -- individualmente validas, pero logicamente incompatibles al combinarse.

Los LLM no manejan bien las contradicciones.
Tienden a confiar en la informacion del contexto,
la deteccion de contradicciones requiere razonamiento,
y la consistencia de la resolucion no esta garantizada.

En lenguaje natural, la verificacion de consistencia es razonamiento del LLM de principio a fin.
Identidad de entidades, identidad de propiedades, extraccion temporal, comparacion de valores -- todo probabilistico y caro.

En una representacion estructurada, existen identificadores de entidades, tipos de propiedades y campos de tiempo,
asi que gran parte de la deteccion de contradicciones se convierte en comparacion de campos y aritmetica.
Las estrategias de resolucion tambien se declaran como politica.

La verificacion de consistencia viene despues del filtrado en el pipeline.
La verificacion y el filtrado deben reducir el conjunto para que el numero de pares de comparacion disminuya.
Lo barato va primero, y las verificaciones colectivas vienen despues de que las individuales se completan.
