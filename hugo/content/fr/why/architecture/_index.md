---
title: "Architecture"
date: 2026-02-26T12:00:00+09:00
image: "/images/og-default.webp"
summary: "Comment GEUL est construit : indexation sémantiquement alignée, unités de mots de 16 bits, mémoire structurée et représentation des connaissances basée sur des affirmations."
---

## Sous-themes

### Pourquoi 16 bits
Toutes les donnees dans GEUL sont en unites de 16 bits (1 mot). C'est l'unite minimale qui combine l'efficacite du code machine avec le sens du langage humain en un seul mot.

### Pourquoi mettre en cache le raisonnement sous forme de code
Jeter les resultats a chaque fois qu'une IA raisonne est un gaspillage de calcul. Enregistrer le raisonnement dans un langage structure permet la reutilisation et l'accumulation.

### Pourquoi des affirmations, pas des faits
Les phrases en langage naturel ressemblent a des faits mais sont en realite les affirmations de quelqu'un. Integrer structurellement la source, le moment et le degre de confiance reduit la marge d'hallucination.

### Pourquoi un index semantiquement aligne
SIDX est un identifiant de 64 bits qui encode le sens dans les bits eux-memes. Le type peut etre determine uniquement par les bits superieurs, et moins les bits sont remplis, plus l'expression est abstraite.

### Pourquoi la memoire structuree est necessaire
La fenetre de contexte d'un LLM est finie. Pour faire tenir une experience infinie dans une fenetre finie, la memoire doit etre structuree.
