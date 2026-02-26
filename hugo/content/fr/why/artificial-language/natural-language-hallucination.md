---
title: "Pourquoi le langage naturel cree-t-il des hallucinations ?"
weight: 8
date: 2026-02-26T12:00:16+09:00
lastmod: 2026-02-26T12:00:16+09:00
tags: ["langage naturel", "hallucination", "ambiguite"]
summary: "L'hallucination n'est pas un bug du LLM — c'est une inevitabilite structurelle causee par quatre defauts du langage naturel : ambiguite, absence de source, de confiance et de contexte temporel. Des modeles plus grands n'y remedient pas."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## L'hallucination n'est pas un bug. C'est une inevitabilite structurelle tant que nous utilisons le langage naturel.

---

## Le miracle du langage naturel

Il y a 100 000 ans, le langage parle est apparu. Les relations sociales que les primates pouvaient maintenir par le toilettage mutuel etaient limitees a environ 150 individus. Le langage a brise ce plafond. Des qu'une personne pouvait parler a plusieurs en meme temps, une nouvelle echelle de societe --- la tribu --- est devenue possible.

Il y a 10 000 ans, l'agriculture a cree des surplus alimentaires, et les gens se sont rassembles en un lieu pour former des villes. Il y a 5 000 ans, quelqu'un en Mesopotamie a presse des marques en forme de coins dans une tablette d'argile humide. C'etait pour enregistrer les inventaires de cereales. La naissance de l'ecriture. La parole s'evanouit, mais les enregistrements perdurent. Une fois que les enregistrements perdurent, la bureaucratie est devenue possible, le droit est devenu possible, l'Etat est devenu possible.

Le langage parle a cree la tribu. L'ecriture a cree l'Etat.

Le langage naturel est la plus grande technologie que l'humanite ait jamais creee. Ni la decouverte du feu, ni l'invention de la roue, ni l'invention du semiconducteur. Ce qui les a tous rendus possibles, c'est le langage naturel. Parce que le langage naturel existait, le savoir pouvait etre transmis, la cooperation pouvait avoir lieu, et les pensees des morts pouvaient etre heritees par les vivants. Pendant des dizaines de milliers d'annees, le langage naturel a ete le medium de toute la civilisation humaine.

Et maintenant, ce grand langage naturel est devenu le goulot d'etranglement de l'ere de l'IA.

---

## Le malentendu qu'on appelle hallucination

Quand l'IA dit quelque chose de faux, nous appelons cela "hallucination".

Ce nom porte des implications.
L'implication que l'hallucination est anormale.
L'implication qu'elle peut etre corrigee.
L'implication qu'un meilleur modele la resoudra.

C'est un malentendu.

L'hallucination n'est pas un bug des LLM.
L'hallucination est une inevitabilite structurelle qui ne peut etre evitee
tant que le langage naturel est utilise comme langage de raisonnement de l'IA.

Peu importe combien vous agrandissez le modele,
peu importe combien vous elargissez les donnees,
peu importe a quel point le RLHF est raffine,
tant que le langage naturel est en entree et le langage naturel en sortie,
l'hallucination ne disparaitra pas.

Laissez-moi expliquer pourquoi.

---

## Les quatre defauts structurels du langage naturel

Le langage naturel a evolue pour la communication entre humains.
Les quatre caracteristiques qu'il a acquises dans ce processus
deviennent des defauts fatals dans le raisonnement de l'IA.

---

### Defaut 1 : L'ambiguite

"He went to the bank."

Est-ce que "bank" designe une institution financiere ou une berge de riviere ?
Qui est "he" ?
Quand y est-il alle ?

Les humains resolvent cela avec le contexte.
Le fil de la conversation, l'expression faciale du locuteur, les connaissances de fond partagees.

L'IA n'a que le texte.
Le texte seul ne peut pas resoudre entierement l'ambiguite.
Si elle ne peut pas etre resolue, l'IA devine.
Les suppositions sont parfois fausses.
Quand une supposition erronee est produite avec assurance, c'est l'hallucination.

---

### Defaut 2 : L'absence de source

"Yi Sun-sin a vaincu 133 navires avec seulement 12."

Cette phrase n'a pas de source.

Qui a fait cette affirmation ?
Quels documents historiques la soutiennent ?
Y a-t-il un desaccord savant sur ces chiffres ?

Le langage naturel n'a pas de place structurelle pour les metadonnees.
Pour inclure des sources, il faut rallonger la phrase,
et la rallonger obscurcit le propos.
Ainsi, dans la plupart des phrases en langage naturel, les sources sont omises. Ce probleme est approfondi dans [Pourquoi des affirmations, pas des faits ?](/fr/why/claims-not-facts/).

Les LLM sont entraines sur des milliards de telles phrases.
Les affirmations aux sources omises se melangent
en une immense soupe statistique.

Retracer la base du chiffre "12" dans cette soupe
est impossible en principe.
Puisque la base ne peut pas etre retracee, des chiffres sans fondement peuvent aussi etre fabriques.
C'est l'hallucination.

---

### Defaut 3 : L'absence de confiance

"La Terre est ronde."
"L'energie sombre constitue 68% de l'univers."
"Il pleuvra demain."

Les niveaux de confiance de ces trois phrases sont completement differents.

La premiere est un consensus ecrasant.
La deuxieme est la meilleure estimation actuelle, mais la theorie peut changer.
La troisieme est une prediction probabiliste.

Pourtant, en langage naturel, les trois ont des structures grammaticales identiques.
Sujet + predicat. Phrase declarative. Point.

Le langage naturel ne peut pas exprimer structurellement "a quel point est-ce certain".
Il existe des dispositifs adverbiaux comme "peut-etre", "presque certainement", "pourrait",
mais ils sont optionnels, imprecis et generalement omis.

Les LLM apprennent toutes les phrases a des niveaux de confiance identiques.
Il n'y a aucun moyen pour le modele de distinguer interieurement la difference de confiance
entre "la Terre est ronde" et "l'energie sombre est de 68%".

Ainsi, il enonce des estimations comme des faits,
enonce des hypotheses comme des vues etablies,
et enonce des choses incertaines avec certitude.
C'est l'hallucination.

---

### Defaut 4 : L'absence de contexte temporel

"Le PDG de Tesla est Elon Musk."

En date de quand ?

En 2024, c'est correct.
En 2030, qui sait.
Si la date de redaction n'est pas specifiee,
la periode de validite de cette phrase ne peut pas etre determinee.

La plupart des phrases en langage naturel omettent le contexte temporel.
Le "present" peut signifier "en ce moment"
ou il peut signifier "en general".

Les LLM apprennent les articles de 2020 et les articles de 2024 comme les memes donnees.
Puisque l'information temporelle n'est pas preservee structurellement,
ils enoncent des faits passes comme s'ils etaient presents,
ou melangent des informations de periodes differentes.
C'est l'hallucination.

---

## La confluence des quatre defauts

L'hallucination s'intensifie de maniere explosive quand ces quatre defauts convergent.

Analysons une seule sortie de LLM.

> "Yi Sun-sin a detruit 330 navires japonais avec 12 vaisseaux,
> et est mort plus tard a la bataille de Noryang, laissant les derniers mots 'N'annoncez pas ma mort.'"

Dans cette phrase :

**Ambiguite :** Que signifie precisement "detruit" ? Coule ? Mis en deroute ? Partiellement endommage ?

**Absence de source :** Quelle est la base des chiffres 12 et 330 ? Differents documents historiques citent des chiffres differents --- lequel a ete suivi ?

**Absence de confiance :** "N'annoncez pas ma mort" est-il un dernier testament historiquement confirme, ou une tradition orale ulterieure ? Les niveaux de confiance des deux sont differents, pourtant ils sont listes dans la meme phrase declarative.

**Absence de contexte temporel :** A quel point du consensus academique dans le temps cette information se refere-t-elle ?

Le LLM comble toute cette ambiguite avec "la sequence de tokens la plus plausible".
La plausibilite n'est pas l'exactitude.
L'ecart entre les deux est l'hallucination.

---

## Pourquoi des modeles plus grands ne peuvent pas resoudre cela

"L'hallucination ne diminuera-t-elle pas quand GPT-5 sortira ?"

Elle diminuera. Mais elle ne disparaitra pas.

Des modeles plus grands apprennent des motifs plus sophistiques a partir de plus de donnees.
Donc la precision de la "plausibilite" augmente.

Mais le probleme fondamental ne change pas.

Tant que l'entree est en langage naturel, l'ambiguite demeure.
Tant que les donnees d'entrainement sont en langage naturel, les sources restent perdues.
Tant que la sortie est en langage naturel, la confiance n'est pas exprimee.
Tant que l'information temporelle est absente de la structure, le temps reste brouille.

Meme si vous agrandissez le modele par 100,
les defauts structurels du langage naturel ne croissent pas par 100 ---
mais ils n'atteignent pas zero non plus.

Ce n'est pas un probleme de resolution. C'est un probleme de medium.

Peu importe combien vous augmentez la resolution d'une photographie en noir et blanc, la couleur n'apparait pas.
Peu importe combien vous augmentez la precision du langage naturel,
la source, la confiance et le contexte temporel n'apparaissent pas dans la structure.

Si vous voulez de la couleur, il faut de la pellicule couleur.
Si vous voulez eliminer l'hallucination, il faut un langage different.

---

## Conditions pour une solution structurelle

Pour resoudre ces quatre defauts, la structure du langage elle-meme doit etre differente.

**Ambiguite --> Structuration explicite.**
Quand "He went to the bank" est converti en langage structure,
"he" est resolu en un SIDX d'entite specifique,
et "bank" est resolu en le SIDX d'une institution financiere ou d'une berge de riviere.
Si cela ne peut pas etre resolu, "non resolu" est explicitement declare.
Soit resoudre l'ambiguite, soit enregistrer le fait qu'elle est ambigue.

**Absence de source --> Source integree.**
Chaque narration inclut structurellement une entite source.
"Qui a fait cette affirmation" fait partie de la narration.
Ce n'est pas optionnel. Si le champ est vide, il est marque comme vide.

**Absence de confiance --> Confiance integree.**
Chaque arete de verbe a un champ de confiance.
"Certain", "estime", "hypothetique"
sont specifies structurellement comme modificateurs de verbe.

**Absence de contexte temporel --> Contexte temporel integre.**
Chaque narration inclut un contexte temporel.
"En date de quand est cette narration" est toujours specifie.

Ce qui est omis en langage naturel
existe comme partie de la structure dans un langage structure.

Quand l'omission est impossible, l'espace pour l'hallucination se reduit. [Pourquoi la clarification est necessaire](/fr/why/clarification/) explique ce principe.
Quand on ne peut pas parler sans base, les declarations sans fondement ne sont pas produites.

---

## La fin de l'hallucination reside dans le remplacement du langage

Examinons les approches actuelles pour reduire l'hallucination.

**RAG (Retrieval-Augmented Generation) :** Recupere des documents externes et les fournit comme contexte. Efficace, mais les documents recuperes sont aussi en langage naturel, donc les problemes d'ambiguite, d'absence de sources et d'absence de confiance suivent sans changement. [Pourquoi RAG ne suffit pas](/fr/why/rag-not-enough/) explore cette limitation en detail.

**RLHF :** Entraine le modele a dire "je ne sais pas" quand il est incertain. Reduit la frequence de l'hallucination, mais ne resout pas le probleme fondamental que le langage naturel n'a pas de structure de confiance.

**Chain-of-Thought :** Enregistre le processus de raisonnement en langage naturel. La direction est bonne, mais le medium de l'enregistrement est le langage naturel, donc il herite des memes defauts.

Toutes ces approches tentent d'attenuer l'hallucination dans le cadre du langage naturel.
Elles fonctionnent. Mais elles ne sont pas fondamentales.

La solution fondamentale est de retirer le langage naturel de l'interieur de l'IA.

L'interface avec les utilisateurs reste en langage naturel.
Les humains continuent de parler en langage naturel et de recevoir des reponses en langage naturel.

Mais le langage dans lequel l'IA raisonne, enregistre et verifie interieurement
doit etre autre chose que le langage naturel.

Un langage ou la source est dans la structure.
Un langage ou la confiance est dans la structure.
Un langage ou le contexte temporel est dans la structure.
Un langage ou l'ambiguite est traitee explicitement.

Le langage parle a cree la tribu.
L'ecriture a cree l'Etat.
Que creera le troisieme langage ?

La fin de l'hallucination ne reside pas dans des modeles plus grands
mais dans un meilleur langage.

---

## Resume

L'hallucination nait des quatre defauts structurels du langage naturel.

1. **Ambiguite :** Irresolvable sans contexte. L'IA devine, et les suppositions sont fausses.
2. **Absence de source :** La base des affirmations est perdue. Des combinaisons sans fondement sont fabriquees.
3. **Absence de confiance :** Les faits et les estimations sont exprimes dans une grammaire identique. L'IA ne peut pas les distinguer.
4. **Absence de contexte temporel :** Les informations de differentes periodes sont brouillees.

Des modeles plus grands reduisent l'hallucination mais ne peuvent pas l'eliminer.
Sans changer le medium, les defauts structurels demeurent.

Peu importe combien vous augmentez la resolution d'une pellicule noir et blanc, la couleur n'apparait pas.
Si vous voulez de la couleur, vous devez changer de pellicule.
