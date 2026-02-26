---
title: "Pourquoi les vecteurs d'embedding ne suffisent pas"
weight: 11
date: 2026-02-26T12:00:18+09:00
lastmod: 2026-02-26T12:00:18+09:00
tags: ["embedding", "vecteur", "boîte blanche"]
summary: "Réarranger les vecteurs d'embedding casse le modèle. Éviter la casse revient à reconstruire le modèle de zéro. Ce qu'il faut, ce n'est pas de la transparence à l'intérieur de la boîte noire, mais une couche transparente à l'extérieur."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Les vecteurs sont bons pour le calcul, mais impossibles à interpréter. On ne peut pas rendre l'intérieur d'une boîte noire transparent.

---

## Les vecteurs d'embedding sont une technologie remarquable

« Roi - Homme + Femme = Reine. »

Quand word2vec a démontré cela, le monde a été stupéfait.
Représentez les mots comme des vecteurs à des centaines de dimensions,
et les relations sémantiques apparaissent sous forme d'opérations vectorielles.

Les vecteurs d'embedding sont le fondement des LLM.
Tout dans un transformer est du calcul vectoriel.
Les tokens deviennent des vecteurs.
L'attention calcule la similarité entre les vecteurs.
Les sorties sont converties des vecteurs en tokens.

Des significations proches sont des vecteurs proches.
Des significations différentes sont des vecteurs éloignés.
La recherche est un calcul de similarité vectorielle.
La classification est la définition de frontières dans l'espace vectoriel.

Sans vecteurs d'embedding, l'IA actuelle n'existerait pas.

Alors, pourquoi ne pas utiliser les vecteurs d'embedding pour représenter la connaissance ?
Les aligner directement, les structurer, les rendre interprétables.

Cela ne marche pas.
Le moyen le plus sûr de le savoir est d'essayer.

---

## AILEV : nous avons essayé

Le projet GEUL a commencé sous le nom d'AILEV.

AI Language Embedding Vector.

Le nom lui-même énonçait l'objectif :
un langage d'IA manipulant directement les vecteurs d'embedding.

Le concept était le suivant :

Représenter le sens avec des vecteurs à 512 dimensions.
Attribuer des rôles à des segments du vecteur.
Les 128 premières dimensions pour les entités, les 128 suivantes pour les relations, les 128 suivantes pour les propriétés, le reste pour les métadonnées.
Tout comme RGBA décompose la couleur en quatre canaux, décomposer le sens en segments dimensionnels.

Entraîner BERT à convertir le langage naturel en ces vecteurs structurés.
Lorsqu'on saisit « Séoul est la capitale de la Corée »,
le segment des entités produit le vecteur de Séoul, le segment des relations le vecteur de capitale, le segment des propriétés le vecteur de Corée.

Puisque ce sont des vecteurs, le calcul est possible.
La recherche par similarité est possible.
La réduction dimensionnelle offre une dégradation élégante.
De 512 à 256 dimensions, la précision diminue mais le sens essentiel est préservé.

C'était élégant. En théorie.

---

## Pourquoi cela échoue

### Réarranger arbitrairement les vecteurs casse le modèle

Les vecteurs d'embedding d'un LLM sont le produit de l'entraînement.

Après avoir lu des milliards de textes,
le modèle optimise lui-même ses représentations internes.
Ce que chaque dimension signifie est une décision du modèle.
Pas d'un humain.

Que se passe-t-il si l'on déclare « les 128 premières dimensions sont pour les entités » ?

Dans l'espace vectoriel appris par le modèle,
l'information sur les entités ne réside pas dans les 128 premières dimensions.
Elle est distribuée sur les 768 dimensions.
L'information sur les relations, les propriétés, les temps verbaux — tout est mélangé.

Ce n'est pas une erreur de conception, mais la nature de l'apprentissage.
La rétropropagation trouve
l'arrangement vectoriel optimal pour la tâche.
Pas un arrangement interprétable.
Optimal et interprétable ne sont pas la même chose.

Si l'on réarrange les vecteurs de force — « les entités ici, les relations là » —
les relations statistiques apprises par le modèle se brisent.
Les performances se dégradent.

### Réarranger sans casser revient à reconstruire le modèle

Alors, pourquoi ne pas entraîner dès le départ avec la contrainte « les 128 premières dimensions sont pour les entités » ?

C'est possible. En théorie.
Mais ce n'est pas aligner des vecteurs d'embedding.
C'est concevoir une nouvelle architecture de modèle.

Il faut des données d'entraînement. Des milliards de tokens.
Il faut une infrastructure. Des milliers de GPU.
Il faut du temps. Des mois.
Et rien ne garantit que le modèle résultant fonctionnera aussi bien que les LLM existants.

L'effort est trop considérable.

Le problème d'« aligner les vecteurs pour les rendre interprétables »
s'est transformé en « reconstruire un LLM de zéro ».
Ce n'est pas résoudre le problème, c'est l'amplifier.

### L'interprétation est impossible

Supposons qu'on ait réussi à créer un vecteur structuré.
Un vecteur à 512 dimensions.
Disons que les 128 premières dimensions sont pour les entités.

Le segment des entités vaut `[0.23, -0.47, 0.81, 0.12, ...]`.

Comment savoir s'il s'agit de « Samsung Electronics » ou de « Hyundai Motor » ?

Il faut trouver le vecteur le plus proche.
Il faut calculer la similarité dans une base de données vectorielle.
Et l'on obtient une réponse probabiliste : « probablement Samsung Electronics ».

« Probablement. »

Les vecteurs sont intrinsèquement continus.
Entre les vecteurs de Samsung Electronics et SK Hynix,
il existe une infinité de vecteurs intermédiaires.
Ce que ces vecteurs intermédiaires signifient, personne ne le sait.

Ce n'est pas une limitation technique, c'est une vérité mathématique.
Représenter des significations discrètes dans un espace continu
rend les frontières floues.
L'ambiguïté était [le problème du langage naturel](/fr/why/natural-language-hallucination/).
On est passé aux vecteurs, et l'ambiguïté est revenue.

Seule la forme a changé.
Dans le langage naturel, l'ambiguïté des mots.
Dans les vecteurs, l'ambiguïté des coordonnées.

---

## Le principe de la boîte blanche

C'est ici que le problème fondamental de conception se révèle.

Les vecteurs d'embedding sont une boîte noire.
En regardant un vecteur à 768 dimensions de nombres réels,
personne ne peut dire quelle information est encodée et où.
Le modèle lui-même ne peut pas l'expliquer.

Ce n'est pas un trait gênant, c'est une propriété ontologique.
C'est précisément la raison pour laquelle les vecteurs fonctionnent.
Parce qu'ils organisent l'information de manières que les humains n'ont pas conçues,
ils fonctionnent mieux que tout ce que les humains auraient pu concevoir.
L'impossibilité d'interprétation n'est pas un défaut, c'est une fonctionnalité.

Or, la connaissance utilisée comme contexte de l'IA exige l'inverse.

Il faut connaître la source.
Il faut connaître le moment.
Il faut connaître le degré de confiance.
Il faut savoir de quoi parle l'énoncé.
Il faut savoir si deux énoncés se réfèrent à la même entité.

Chaque exigence est « il faut savoir ». Chaque exigence demande l'interprétabilité.

Satisfaire les exigences de la boîte blanche avec un vecteur de boîte noire
est une contradiction.

---

## La logique du tournant

Le passage d'AILEV à GEUL n'a pas été un recul.
Ce fut une redéfinition du problème.

**Problème initial :** Les LLM sont des boîtes noires. Rendons l'intérieur transparent.
→ Rendons les vecteurs d'embedding interprétables en les alignant.
→ Toucher aux vecteurs casse le modèle.
→ Éviter la casse revient à reconstruire le modèle.
→ Impasse.

**Problème redéfini :** Il n'est pas nécessaire de rendre l'intérieur de la boîte noire transparent. Construisons une couche transparente à l'extérieur.
→ On ne touche pas à l'intérieur du LLM.
→ À l'extérieur du LLM, on crée un système de représentation interprétable.
→ Le LLM peut lire et écrire ce système. Parce que ce sont des tokens.
→ Un langage artificiel.

Pas des vecteurs, mais un langage.
Pas continu, mais discret.
Pas ininterprétable, mais avec l'interprétation comme unique but.
Pas à l'intérieur du modèle, mais à l'extérieur.

Le « Embedding Vector » d'AILEV a été retiré,
et GEUL — signifiant « écriture » — a pris sa place. Voilà pourquoi.

---

## Les vecteurs pour le calcul, le langage pour la représentation

Ceci ne rejette pas les vecteurs d'embedding.

Les vecteurs sont optimisés pour le calcul.
Recherche par similarité, regroupement, classification, récupération.
Le langage ne peut pas remplacer ce que font les vecteurs.

Le langage est optimisé pour la représentation.
Identité des entités, description des relations, métadonnées intégrées, interprétabilité.
Les vecteurs ne peuvent pas remplacer ce que fait le langage.

Ce sont des outils à des niveaux différents.

À l'intérieur du LLM, les vecteurs opèrent. Une boîte noire. C'est ainsi que cela doit être.
À l'extérieur du LLM, le langage opère. Une boîte blanche. C'est ainsi que cela doit être.

Le problème a commencé quand ces deux niveaux ont été confondus.
On a essayé de faire aux vecteurs le travail du langage.
On a essayé d'attribuer à une boîte noire le rôle d'une boîte blanche.

Chacun a sa place.

---

## Résumé

Les vecteurs d'embedding sont le fondement des LLM et une technologie remarquable.
Cependant, comme moyen de représentation des connaissances, ils ont des limites fondamentales.

GEUL a commencé sous le nom d'AILEV (AI Language Embedding Vector).
L'objectif était d'aligner directement les vecteurs et de les rendre interprétables.
Échec. Pour deux raisons.

Aligner arbitrairement les vecteurs brise les relations apprises par le modèle.
Aligner sans casser revient à reconstruire le modèle de zéro. L'effort est trop considérable.

Et même en cas de succès, les vecteurs ne sont pas interprétables.
Dans un espace continu, les frontières du sens discret sont floues.
On ne peut pas attribuer à une boîte noire le rôle d'une boîte blanche.

La logique du tournant :
On a essayé de rendre l'intérieur de la boîte noire transparent.
Toucher l'intérieur le casse.
Au lieu de cela, laisser l'intérieur intact et construire une couche transparente à l'extérieur.
Pas des vecteurs, mais un langage. Pas à l'intérieur du modèle, mais à l'extérieur.

Les vecteurs pour le calcul, le langage pour la représentation.
Chacun a sa place.
