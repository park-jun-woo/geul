---
title: "Por qué los lenguajes de programación no son suficientes"
weight: 10
date: 2026-02-26T12:00:19+09:00
lastmod: 2026-02-26T12:00:19+09:00
tags: ["lenguaje de programación", "descripción", "representación del conocimiento"]
summary: "Los lenguajes de programación describen procedimientos. No pueden describir el mundo. JSON ofrece estructura pero no significado. Incluso LISP solo toma prestada la sintaxis."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Los lenguajes de programación describen procedimientos. No pueden describir el mundo.

---

## Los lenguajes de programación son uno de los mayores inventos de la humanidad

Los lenguajes de programación son inequívocos.
`x = 3 + 4` da 7 sin importar cuándo ni dónde se ejecute.
No hay margen para la interpretación.

Los lenguajes de programación son verificables.
Los errores de sintaxis se detectan antes de la compilación.
Los errores de tipo se detectan antes de la ejecución.
Cuando se ejecutan las pruebas, el resultado es o aprobado o fallido.

Los lenguajes de programación son Turing-completos.
Pueden expresar todo lo que sea computable.
Con suficiente tiempo y memoria, cualquier procedimiento puede describirse.

Todo lo que esta serie identificó como limitaciones del lenguaje natural — ambigüedad, imposibilidad de verificación, falta de estructura — los lenguajes de programación lo han resuelto.

Entonces, ¿por qué no usar un lenguaje de programación para representar el contexto de una IA?

No funciona.

---

## Los lenguajes de programación describen procedimientos

El siguiente es código Python válido.

```python
def calculate_revenue(units_sold, unit_price):
    return units_sold * unit_price
```

Este código es claro, verificable y ejecutable.
Pero ¿qué expresa?

"Multiplicar las unidades vendidas por el precio unitario para obtener los ingresos."

Esto es un procedimiento. Un método. El CÓMO.
Describe qué hacer cuando llega la entrada.

Ahora intentemos expresar lo siguiente.

"Los ingresos de Samsung Electronics en el tercer trimestre de 2024 fueron de 79 billones de wones."

Esto no es un procedimiento. Es un hecho. El QUÉ.
No se ejecuta nada. Describe el estado del mundo.

¿Cómo se expresa esto en Python?

```python
samsung_revenue_2024_q3 = 79_000_000_000_000
```

Se asigna un número a una variable.
Funciona. Pero esto no es descripción. Es almacenamiento.
Este código no sabe:

- Qué tipo de entidad es "Samsung Electronics".
- Qué significa "ingresos". ¿Es un indicador financiero? ¿Una magnitud física?
- Si "T3 2024" es un tiempo, una versión o una etiqueta.
- Cuál es la fuente de la cifra de 79 billones de wones.
- Cuán seguro es este valor.

El nombre de la variable `samsung_revenue_2024_q3` permite a un humano adivinar el significado.
Para la máquina, es una cadena de caracteres arbitraria.
Cámbialo a `xyzzy_42` y el resultado de ejecución será idéntico.

En los lenguajes de programación, los nombres de variables no tienen significado.
El significado vive fuera del código, en la mente del programador.

---

## Más sofisticación no ayuda

¿Y si creamos una clase?

```python
class FinancialReport:
    def __init__(self, company, metric, period, value, currency):
        self.company = company
        self.metric = metric
        self.period = period
        self.value = value
        self.currency = currency

report = FinancialReport("삼성전자", "매출", "2024-Q3", 79_000_000_000_000, "KRW")
```

Mejor. Hay estructura.
Pero los problemas persisten.

`company` es la cadena "삼성전자" (Samsung Electronics).
"Samsung Electronics", "SEC" y "005930" se refieren a la misma empresa.
¿Lo sabe el código? No.
Solo puede comparar si las cadenas son iguales o no.

`metric` es la cadena "매출" (ingresos).
¿Son "매출", "매출액" y "revenue" lo mismo o cosas distintas?
El código no lo sabe. Las cadenas son diferentes, así que son cosas diferentes.

¿Y si definimos un esquema?
Gestionar la lista de empresas con Enums, gestionar la lista de indicadores.
Claro. Funciona.

Entonces intentemos expresar lo siguiente.

"Yi Sun-sin fue un gran hombre."

```python
opinion = Opinion("이순신", "was", "위대했다")
```

¿Qué es esto?
Una cadena "이순신" (Yi Sun-sin) unida a una cadena "위대했다" (fue grande).
No expresa "Yi Sun-sin fue grande".
Almacena "이순신" y "위대했다".

El código no conoce el significado de "위대했다" (fue grande).
Si "위대했다" (fue grande) y "훌륭했다" (fue admirable) son similares,
si "비겁했다" (fue cobarde) es lo opuesto —
el código no puede saberlo.

Los hechos estructurados como los datos financieros son más o menos manejables.
Las evaluaciones, el contexto, las relaciones y las descripciones abstractas quedan fuera del alcance expresivo de los lenguajes de programación.

---

## El código no sabe lo que hace

```python
def process(data):
    result = []
    for item in data:
        if item["value"] > threshold:
            result.append(transform(item))
    return result
```

Este código se ejecuta perfectamente.
Pero ¿qué hace?

¿Filtra datos de ingresos?
¿Selecciona expedientes de pacientes?
¿Depura datos de sensores?

El código en sí no lo sabe.
`data`, `value`, `threshold`, `transform` — todos nombres abstractos.
Si este código pertenece a un sistema financiero o médico
depende del contexto fuera del código.

Se pueden escribir comentarios.
Pero los comentarios son lenguaje natural. Las máquinas no los entienden.
Si un comentario contradice el código, el compilador no se da cuenta.
Los comentarios son para humanos, no para máquinas.

Cuando una IA recibe código como contexto, este problema se manifiesta directamente.
Como el código no tiene identidad propia,
la IA debe reconstruir esa identidad mediante inferencia cada vez.
Al ser inferencia, tiene un coste computacional y puede equivocarse.

---

## La razón fundamental

Que los lenguajes de programación no puedan describir el mundo no es un defecto de diseño.
El propósito es diferente.

El propósito de un lenguaje de programación es dar instrucciones procedimentales a una máquina.
"Cuando llegue esta entrada, ejecuta esta operación."
La semántica de un lenguaje de programación es la semántica de la ejecución.
Cada construcción se interpreta como "qué hace la máquina".

`x = 3` es la instrucción "almacena 3 en la posición de memoria llamada x".
`if x > 0` es la instrucción "si x es mayor que 0, ejecuta el siguiente bloque".
`return x` es la instrucción "devuelve el valor de x al llamador".

Todo verbos. Todo acciones. Todo procedimientos.

"Samsung Electronics es una empresa coreana" no es un verbo.
No es una acción. No es un procedimiento.
Describe en qué estado se encuentra el mundo.

Los lenguajes de programación no tienen lugar para esto.
Se puede almacenar en una variable, pero eso es almacenamiento, no descripción.
El significado del valor almacenado no es competencia del código.

---

## ¿Y JSON, YAML, XML?

Si no lenguajes de programación, ¿qué hay de los formatos de datos?

```json
{
  "company": "삼성전자",
  "metric": "매출",
  "period": "2024-Q3",
  "value": 79000000000000,
  "currency": "KRW"
}
```

Hay estructura. Los campos son explícitos.
Pero no hay significado.

Si "company" significa una corporación, JSON no lo sabe.
Si "삼성전자" es lo mismo que "Samsung Electronics" en otro lugar, JSON no lo sabe.
Si este objeto JSON y aquel objeto JSON describen la misma entidad, JSON no lo sabe.

JSON proporciona estructura, pero no significado.
Son pares clave-valor, no entidad-relación-atributo.

Definir esquemas mejora las cosas.
JSON Schema, Protocol Buffers, GraphQL.
Se definen los tipos de campo, la obligatoriedad y las referencias.

Pero todas estas son estructuras diseñadas para sistemas específicos.
No son representación de conocimiento de propósito general.
Un esquema de datos financieros no puede expresar la valoración de un personaje histórico.
Un esquema de datos médicos no puede expresar relaciones de competencia entre empresas.

Un esquema independiente para cada dominio.
Una herramienta independiente para cada esquema.
Sin interoperabilidad entre esquemas.

Esta limitación se analiza con más detalle en [Por qué MD/JSON/XML no funcionan](/es/why/not-md-json-xml/).

---

## ¿Y LISP?

Algunos lectores habrán pensado en un contraejemplo.

LISP.

```lisp
(is 삼성전자 (company korea))
(revenue 삼성전자 2024-Q3 79000000000000)
(great 이순신)
```

Las S-expressions son estructuras de árbol,
y el código es datos y los datos son código.
Homoiconicidad (homoiconicity).

De hecho, la IA temprana estaba enteramente basada en LISP.
SHRDLU, CYC, sistemas expertos.
El conocimiento se representaba en LISP y los motores de inferencia se ejecutaban sobre él.
Parece una contraprueba histórica de que "los lenguajes de programación no pueden describir el mundo".

Pero el contraejemplo falla por tres razones.

### Lo que LISP sabe frente a lo que el programador decidió

En `(is 삼성전자 company)`, LISP no sabe
que `is` significa la relación "es un".
El programador lo decidió así.

Sustituye `is` por `zzz` y a LISP le da igual.
`(zzz 삼성전자 company)` es una expresión perfectamente válida para LISP.

LISP proporciona estructura. Un árbol llamado S-expression.
Pero el significado dentro de esa estructura lo asignó el programador, no el lenguaje.
Esto es fundamentalmente lo mismo que JSON sin conocer el significado de sus claves.

Proporcionar estructura e incorporar significado son cosas distintas.

### Los 30 años de CYC

El intento más ambicioso fue CYC.

Comenzó en 1984.
Intentó representar conocimiento general usando LISP.
Millones de reglas fueron introducidas a mano.

Lo que 30 años demostraron no fue la viabilidad, sino las limitaciones.

Las ontologías debían diseñarse manualmente para cada dominio.
La interoperabilidad entre dominios no funcionaba.
No podía seguir el ritmo de la flexibilidad del lenguaje natural.
A medida que crecía la escala, mantener la consistencia se volvía casi imposible.

Que la representación del conocimiento "se pueda hacer" en LISP es cierto.
Que "funcione bien" es lo que 30 años de resultados refutan.

### Si no vas a usar eval, no hay razón para usar LISP

El problema más fundamental.

El poder de LISP es `eval`.
Como el código es datos, los datos pueden ejecutarse.
Metaprogramación, macros, generación de código en tiempo de ejecución.
Esto es lo que hace que LISP sea LISP.

Pero ¿qué pasa cuando haces `eval` de `(is 삼성전자 company)`?

Se convierte en una llamada a función que pasa `삼성전자` y `company` como argumentos a una función llamada `is`.
No descripción — ejecución.

Para usarlo como representación de conocimiento, no debes evaluar.
Si no vas a evaluar, no estás usando la semántica de LISP.
Solo estás tomando prestada la sintaxis de las S-expressions.

Eso no es "describir el mundo en LISP".
Es "almacenar datos usando la notación de paréntesis de LISP".

La semántica de LISP como lenguaje de programación — la semántica de la ejecución —
sigue diseñada para describir procedimientos.
Tomar prestada la sintaxis no cambia la semántica.

---

## Qué necesita un lenguaje para describir el mundo

Los lenguajes de programación describen procedimientos.
Los formatos de datos proporcionan estructura pero no significado.
Incluso LISP solo toma prestada la sintaxis sin la semántica de la descripción.

¿Qué necesita un lenguaje para describir el mundo?

**Identidad de entidad.** "Samsung Electronics" debe tener un identificador único. La máquina debe saber que es lo mismo que "삼성전자". No comparación de cadenas, sino equivalencia de identidad.

**Expresión de relaciones.** En "Samsung Electronics es una empresa coreana", debe ser posible expresar la relación "empresa coreana". No asignación de variables, sino descripción de relaciones.

**Descripciones autocontenidas.** De qué trata la descripción, quién la dijo, a partir de cuándo y cuán segura es — todo debe estar incluido en la propia descripción. Dentro del código, no fuera.

**Independencia de dominio.** Datos financieros, hechos históricos, evaluaciones subjetivas, relaciones abstractas — todo debe poder expresarse en el mismo formato. No un esquema independiente para cada dominio, sino una estructura universal.

Los lenguajes de programación carecen de estas cuatro propiedades.
Porque los lenguajes de programación no fueron creados para esto.
Fueron creados para describir procedimientos.

El lenguaje natural puede hacer las cuatro cosas. De forma ambigua.
Lo que se necesita es una combinación del alcance expresivo del lenguaje natural y la precisión de los lenguajes de programación.

---

## Resumen

Los lenguajes de programación son inequívocos, verificables y Turing-completos.
Pero no pueden describir el mundo.

Los lenguajes de programación describen procedimientos.
"Cuando llegue esta entrada, haz esto." Todo verbos, todo acciones.
"Samsung Electronics es una empresa coreana" no es una acción.
Los lenguajes de programación no tienen lugar para ello.

El código no conoce su propia identidad.
A qué dominio pertenece, qué propósito cumple —
nada de esto queda registrado dentro del código.

Los formatos de datos como JSON y YAML proporcionan estructura pero no significado.
LISP puede tomar prestada la sintaxis, pero no tiene semántica de descripción.
CYC dedicó 30 años a intentar representar conocimiento basándose en LISP, y lo que demostró fue la limitación.

Describir el mundo requiere identidad de entidad, expresión de relaciones, descripciones autocontenidas e independencia de dominio.
Los lenguajes de programación no fueron creados para esto.
El lenguaje natural puede hacerlo, pero de forma ambigua.
Lo que se necesita está en algún punto entre ambos.
