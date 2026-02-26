---
title: "Ingeniería de Contexto"
date: 2026-02-26T12:00:00+09:00
image: "/images/og-default.webp"
summary: "Por qué un mejor contexto supera a mejores prompts: limitaciones de RAG, verificación mecánica, comprobación de consistencia y filtrado semántico para sistemas de IA."
---

## Subtemas

### ¿Por qué terminó la era de la ingeniería de prompts?
Cuando los modelos son suficientemente inteligentes, "cómo lo dices" importa menos. "Lo que muestras" determina la calidad del resultado. La ventana de contexto es finita, y lo que pones en ella es lo que cuenta.

### ¿Por qué es necesaria la clarificación?
El lenguaje natural inevitablemente se alarga para resolver la ambigüedad. Una representación estructuralmente inequívoca no tiene costo de resolución. La compresión surge como subproducto de la clarificación.

### ¿Por qué RAG no es suficiente?
La similitud de embeddings no garantiza relevancia. Se necesita recuperación basada en estructura semántica. Para reducir candidatos entre mil millones de recuerdos en milisegundos, la información debe estar indexada semánticamente.

### ¿Por qué es necesaria la verificación mecánica?
El lenguaje natural no tiene el concepto de "oración inválida". Como un compilador de Go, la información que no cumple las especificaciones debe ser rechazada antes de entrar al contexto. La verificación más barata y determinista va primero.

### ¿Por qué son necesarios los filtros?
Si la verificación juzga la aptitud estructural, los filtros juzgan la calidad semántica. Relevancia, confianza, actualidad. Solo lo que se necesita para esta inferencia ahora mismo pasa el filtro.

### ¿Por qué son necesarias las verificaciones de consistencia?
Información individualmente buena puede contradecirse al combinarse. Cuando hechos de 2020 y 2024 entran simultáneamente al contexto, el LLM se confunde. Se debe garantizar la coherencia a nivel de conjunto.

### ¿Por qué es necesaria la exploración?
La búsqueda devuelve resultados con una sola consulta. Cuando el conocimiento crece lo suficiente, esto no funciona: el índice mismo excede la ventana. Un agente debe navegar mapas jerárquicos, eligiendo direcciones. A medida que una biblioteca crece, pasas de preguntar al bibliotecario a recorrer el sistema de clasificación.
