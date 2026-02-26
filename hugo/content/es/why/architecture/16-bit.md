---
title: "Por que 16 bits?"
weight: 16
date: 2026-02-26T12:00:04+09:00
lastmod: 2026-02-26T12:00:04+09:00
tags: ["16-bit", "binario", "flujo"]
summary: "Una sola palabra penetra tres mundos"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Una sola palabra penetra tres mundos

---

## Tres mundos

Existen tres mundos en la informatica.

**El mundo de las redes.**
Los datos fluyen como flujos de bytes.
Los bytes entran por sockets TCP y los bytes salen.
El vocabulario del ingeniero de redes son paquetes, encabezados y cargas utiles.

**El mundo del almacenamiento.**
Los datos se persisten en formatos de archivo.
Se escriben en disco, se leen del disco.
El vocabulario del ingeniero de almacenamiento son bloques, offsets y alineacion.

**El mundo de la IA.**
Los datos se procesan como secuencias de tokens.
Los LLM reciben tokens y producen tokens.
El vocabulario del ingeniero de IA son embeddings, atencion y contexto.

Estos tres mundos hablan idiomas diferentes.
Y entre ellos, siempre se requiere traduccion.

---

## El costo de la traduccion

Sigamos el camino que recorren los datos en un sistema de IA moderno.

El conocimiento se almacena en un archivo. Como JSON o texto plano.

Para entregarselo a una IA:

1. Abrir el archivo y leer el texto.
2. Parsear el texto. Si es JSON, interpretar la estructura y extraer campos.
3. Introducir el texto extraido en un tokenizador.
4. El tokenizador convierte el texto en una secuencia de IDs de tokens.
5. La secuencia de tokens se alimenta al LLM.

Cuando la IA genera una respuesta:

6. El LLM produce una secuencia de tokens.
7. Decodificar los tokens de vuelta a texto.
8. Serializar el texto en un formato estructurado.
9. Escribir los datos serializados en un archivo.

Una simple operacion de "leer y escribir" requiere nueve pasos.

Cada paso cuesta tiempo.
Cada paso cuesta memoria.
Cada paso arriesga perdida de informacion.

Los pasos 3 y 4 -- el proceso de tokenizacion -- son notoriamente problematicos.
Porque los limites de las palabras en lenguaje natural no se alinean con los limites de los tokens del tokenizador,
un nombre propio como "Yi Sun-sin" puede dividirse en fragmentos arbitrarios,
o una sola unidad semantica se dispersa entre multiples tokens.

Este es el precio de que tres mundos hablen idiomas diferentes.

---

## Y si una sola unidad penetrara los tres mundos?

En este lenguaje, una palabra son 16 bits (2 bytes).

Una sola palabra de 16 bits es simultaneamente tres cosas.

**Una unidad del flujo de bytes.**
Las palabras de 16 bits llegan en un flujo continuo por la red.
Big Endian. Alineadas en limites de 2 bytes. No se necesita parseo adicional.
Simplemente se leen en el orden en que llegan.

**Una unidad del formato de archivo.**
Escribe el flujo directamente en disco y eso es tu archivo.
Lee los bytes directamente del disco y envialos por la red, y eso es tu flujo.
Sin serializacion. Sin deserializacion.

**Una unidad del token del LLM.**
16 bits = 65,536 simbolos distintos.
Los tamanos de vocabulario de los LLM modernos generalmente van de 50,000 a 100,000.
Los modelos de la familia GPT usan aproximadamente 50,000; los modelos especializados en coreano alrededor de 100,000.
65,536 se situa justo en el centro de ese rango.
Una palabra de 16 bits se convierte en un token del LLM.

Tres mundos compartiendo la misma unidad.
La traduccion desaparece.

---

## Cero conversion, cero perdida, cero sobrecarga

Veamos que significa esto concretamente.

**Enfoque convencional: 9 pasos**

```
[Archivo] -> Leer -> Parsear -> Extraer texto -> Tokenizar -> [LLM]
[LLM] -> Decodificar -> Serializar -> Escribir -> [Archivo]
```

**Enfoque de flujo binario: 1 paso**

```
[Archivo/Flujo] -> [LLM]
[LLM] -> [Archivo/Flujo]
```

Lee un archivo y ya es una secuencia de tokens.
Escribe la secuencia de tokens que produce el LLM y ya es un archivo.
Toma un flujo de la red y alimentalo directamente al LLM.

Cero conversion. Cero parseo. Cero tokenizacion.
Cero perdida. Cero sobrecarga.

---

## Por que no 8 bits?

8 bits te dan 256 simbolos distintos.

256 simbolos son demasiado pocos para representar el mundo.
Asigna el alfabeto, los digitos y la puntuacion basica, y ya se fue la mitad del espacio.

Si usas 8 bits como tu unidad fundamental,
la mayoria de los tokens significativos terminan requiriendo 2 o mas bytes.
Eso fuerza una codificacion de longitud variable,
y la longitud variable hace el parseo complejo.

Adecuado como unidad de flujo de bytes,
pero insuficiente como unidad de token.

---

## Por que no 32 bits?

32 bits te dan aproximadamente 4,300 millones de simbolos distintos.

El poder expresivo es mas que suficiente -- vastamente mas de lo necesario.
Pero el problema es la eficiencia.

El paquete mas frecuente en este formato es el Tiny Verb Edge, de 2 palabras.
A 16 bits por palabra, eso son 4 bytes. A 32 bits por palabra, se convierte en 8 bytes.
El paquete mas comun duplica su tamano.

Desde la perspectiva del LLM, tambien hay un problema.
Si un solo token es de 32 bits, solo cabe la mitad de tokens en la misma ventana de contexto.
Dado que la longitud de contexto del LLM es un recurso escaso hoy en dia,
el espacio que ocupa un token se vuelve ineficiente en relacion con la informacion que transporta.

Una palabra de 32 bits es excesiva como token para este lenguaje.

---

## Por que no longitud variable?

UTF-8 es una codificacion de longitud variable.
La longitud de un caracter varia de 1 byte a 4 bytes dependiendo del caracter.

Esto ofrece ventajas en eficiencia de almacenamiento,
pero introduce una debilidad fatal en eficiencia de procesamiento.

Para encontrar el n-esimo caracter, hay que contar desde el principio.
El acceso aleatorio es imposible.
El procesamiento paralelo con SIMD se vuelve dificil.

Este lenguaje usa palabras de 16 bits de ancho fijo como su unidad fundamental.
La posicion de la n-esima palabra es siempre n * 2 bytes.
El acceso aleatorio es O(1).
SIMD puede comparar multiples palabras en una sola instruccion.
Las GPU pueden escanear miles de millones de palabras en paralelo.

Sin embargo, a nivel de paquete, la longitud variable sigue siendo permitida.
Un Tiny Verb Edge tiene 2 palabras; un Event6 Edge puede tener hasta 8 palabras.
La unidad de palabra es fija, pero la unidad de paquete es flexible.

La eficiencia de procesamiento del ancho fijo combinada con la expresividad de la longitud variable.
La palabra de 16 bits logra ambas simultaneamente.

---

## El camino que Unicode demostro

Unicode es el estandar de codificacion mas exitoso que la humanidad ha creado jamas.

La unidad basica de UTF-16 es 16 bits (2 bytes).
Representa los 65,536 caracteres del Plano Multilingue Basico (BMP) en una sola palabra,
y se extiende a caracteres mas alla usando pares sustitutos (2 palabras = 4 bytes).

Simplemente seguimos esta estructura probada.

Representar 65,536 primitivos semanticos basicos en una sola palabra,
y extender paquetes compuestos a traves de multiples palabras.

Asi como Unicode expresa cada caracter del mundo
sobre la unidad basica de "un caracter = 2 bytes",
este lenguaje expresa cada elemento del razonamiento de IA
sobre la unidad basica de "una palabra = 2 bytes".

---

## Compatibilidad hacia atras y extension hacia arriba

Otra fortaleza de 16 bits es la alineacion.

16 es multiplo de 8, divisor de 32, divisor de 64 y divisor de 128.

Esto significa que la alineacion nunca se rompe, sin importar en que direccion te extiendas.

Y si la arquitectura transformer cambia en el futuro
y los tokens se convierten en 32 bits?
Dos palabras de 16 bits hacen un token. Sin problemas de alineacion.

Y 64 bits?
Cuatro palabras de 16 bits hacen un token. Sigue sin problemas de alineacion.

A la inversa, que pasa si un sistema embebido de 8 bits procesa este formato?
Simplemente lee cada palabra de 16 bits como un byte alto y un byte bajo.

La compatibilidad hacia atras debe mantenerse absolutamente.
La palabra de 16 bits garantiza esto a nivel fisico.

No podemos predecir el tamano de palabra de las inteligencias futuras,
pero la alineacion multiple de 16 bits garantiza compatibilidad con cualquier tamano.

---

## La estructura triple

Resumamos.

Una sola palabra de 16 bits es simultaneamente tres cosas.

| Mundo | Rol de una palabra |
|-------|---------------------|
| Red | Unidad del flujo de bytes |
| Almacenamiento | Unidad del formato de archivo |
| IA | Unidad del token del LLM |

Una sola unidad penetra los tres mundos.

Almacena un flujo tal cual y es un archivo.
Lee un archivo tal cual y son tokens.
Envia tokens tal cual y es un flujo.

Sin conversion.
Sin traduccion.
Sin perdida.

Es por esto que 16 bits.
No 8 bits, no 32 bits, no longitud variable.
El numero que se situa precisamente en la interseccion de tres mundos.

16.
