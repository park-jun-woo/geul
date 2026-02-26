---
title: "Pourquoi 16 bits ?"
weight: 16
date: 2026-02-26T12:00:04+09:00
lastmod: 2026-02-26T12:00:04+09:00
tags: ["16-bit", "binaire", "flux"]
summary: "Un seul mot traverse trois mondes"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Un seul mot traverse trois mondes

---

## Trois mondes

Il existe trois mondes en informatique.

**Le monde des reseaux.**
Les donnees circulent sous forme de flux d'octets.
Les octets arrivent par les sockets TCP, et les octets en repartent.
Le vocabulaire de l'ingenieur reseau : paquets, en-tetes et charges utiles.

**Le monde du stockage.**
Les donnees sont persistees sous forme de formats de fichiers.
Ecrites sur disque, lues depuis le disque.
Le vocabulaire de l'ingenieur stockage : blocs, decalages et alignement.

**Le monde de l'IA.**
Les donnees sont traitees sous forme de sequences de tokens.
Les LLM recoivent des tokens en entree et produisent des tokens en sortie.
Le vocabulaire de l'ingenieur IA : embeddings, attention et contexte.

Ces trois mondes parlent des langues differentes.
Et entre eux, une traduction est toujours necessaire.

---

## Le cout de la traduction

Suivons le chemin que parcourent les donnees dans un systeme d'IA moderne.

Le savoir est stocke dans un fichier. En JSON ou en texte brut.

Pour le transmettre a une IA :

1. Ouvrir le fichier et lire le texte.
2. Analyser le texte. S'il s'agit de JSON, interpreter la structure et extraire les champs.
3. Injecter le texte extrait dans un tokeniseur.
4. Le tokeniseur convertit le texte en une sequence d'identifiants de tokens.
5. La sequence de tokens est injectee dans le LLM.

Lorsque l'IA genere une reponse :

6. Le LLM produit une sequence de tokens.
7. Decoder les tokens en texte.
8. Serialiser le texte dans un format structure.
9. Ecrire les donnees serialisees dans un fichier.

Une simple operation de "lecture et ecriture" necessite neuf etapes.

Chaque etape coute du temps.
Chaque etape coute de la memoire.
Chaque etape risque une perte d'information.

Les etapes 3 et 4 -- le processus de tokenisation -- sont notoirement problematiques.
Parce que les frontieres de mots du langage naturel ne s'alignent pas avec les frontieres de tokens du tokeniseur,
un nom propre comme "Yi Sun-sin" peut etre decoupe en fragments arbitraires,
ou une unite semantique unique se retrouve dispersee sur plusieurs tokens.

Tel est le prix de trois mondes qui parlent des langues differentes.

---

## Et si une seule unite traversait les trois mondes ?

Dans ce langage, un mot fait 16 bits (2 octets).

Un seul mot de 16 bits est simultanement trois choses.

**Une unite du flux d'octets.**
Les mots de 16 bits arrivent en flux continu sur le reseau.
Big Endian. Alignes sur des frontieres de 2 octets. Aucune analyse supplementaire n'est necessaire.
Il suffit de les lire dans l'ordre d'arrivee.

**Une unite du format de fichier.**
Ecrivez le flux directement sur le disque, et voila votre fichier.
Lisez les octets directement depuis le disque et envoyez-les sur le reseau, et voila votre flux.
Pas de serialisation. Pas de deserialisation.

**Une unite du token LLM.**
16 bits = 65 536 symboles distincts.
Les tailles de vocabulaire des LLM modernes vont generalement de 50 000 a 100 000.
Les modeles de la famille GPT utilisent environ 50 000 ; les modeles specialises pour le coreen environ 100 000.
65 536 se situe exactement au centre de cette plage.
Un mot de 16 bits devient un token LLM.

Trois mondes partageant la meme unite.
La traduction disparait.

---

## Zero conversion, zero perte, zero surcharge

Voyons ce que cela signifie concretement.

**Approche conventionnelle : 9 etapes**

```
[Fichier] -> Lire -> Analyser -> Extraire le texte -> Tokeniser -> [LLM]
[LLM] -> Decoder -> Serialiser -> Ecrire -> [Fichier]
```

**Approche flux binaire : 1 etape**

```
[Fichier/Flux] -> [LLM]
[LLM] -> [Fichier/Flux]
```

Lire un fichier, et c'est deja une sequence de tokens.
Ecrire la sequence de tokens produite par le LLM, et c'est deja un fichier.
Prendre un flux du reseau et l'injecter directement dans le LLM.

Zero conversion. Zero analyse. Zero tokenisation.
Zero perte. Zero surcharge.

---

## Pourquoi pas 8 bits ?

8 bits donnent 256 symboles distincts.

256 symboles sont bien trop peu pour representer le monde.
Assignez l'alphabet, les chiffres et la ponctuation de base, et la moitie de l'espace est deja epuisee.

Si vous utilisez 8 bits comme unite fondamentale,
la plupart des tokens significatifs necessitent 2 octets ou plus.
Cela impose un encodage a longueur variable,
et la longueur variable rend l'analyse complexe.

Adequat comme unite de flux d'octets,
mais insuffisant comme unite de token.

---

## Pourquoi pas 32 bits ?

32 bits donnent environ 4,3 milliards de symboles distincts.

La puissance d'expression est plus que suffisante -- bien au-dela du necessaire.
Mais le probleme est l'efficacite.

Le paquet le plus frequent dans ce format est le Tiny Verb Edge, a 2 mots.
A 16 bits par mot, cela fait 4 octets. A 32 bits par mot, cela devient 8 octets.
Le paquet le plus courant double de taille.

Du point de vue du LLM, il y a aussi un probleme.
Si un seul token fait 32 bits, seule la moitie des tokens tient dans la meme fenetre de contexte.
Etant donne que la longueur de contexte des LLM est une ressource rare aujourd'hui,
l'espace qu'un token occupe devient inefficace par rapport a l'information qu'il porte.

Un mot de 32 bits est surdimensionne comme token pour ce langage.

---

## Pourquoi pas une longueur variable ?

UTF-8 est un encodage a longueur variable.
La longueur d'un caractere varie de 1 a 4 octets selon le caractere.

Cela offre des avantages en efficacite de stockage,
mais introduit une faiblesse fatale en efficacite de traitement.

Pour trouver le n-ieme caractere, il faut compter depuis le debut.
L'acces aleatoire est impossible.
Le traitement parallele SIMD devient difficile.

Ce langage utilise des mots fixes de 16 bits comme unite fondamentale.
La position du n-ieme mot est toujours n * 2 octets.
L'acces aleatoire est O(1).
SIMD peut comparer plusieurs mots en une seule instruction.
Les GPU peuvent analyser des milliards de mots en parallele.

Pourtant, au niveau du paquet, la longueur variable reste autorisee.
Un Tiny Verb Edge fait 2 mots ; un Event6 Edge peut aller jusqu'a 8 mots.
L'unite de mot est fixe, mais l'unite de paquet est flexible.

L'efficacite de traitement de la largeur fixe combinee a l'expressivite de la longueur variable.
Le mot de 16 bits realise les deux simultanement.

---

## Le chemin prouve par Unicode

Unicode est la norme d'encodage la plus reussie que l'humanite ait jamais creee.

L'unite de base d'UTF-16 est 16 bits (2 octets).
Elle represente les 65 536 caracteres du Plan Multilingue de Base (BMP) en un seul mot,
et s'etend aux caracteres au-dela grace aux paires de substitution (2 mots = 4 octets).

Nous suivons simplement cette structure eprouvee.

Representer 65 536 primitives semantiques de base en un seul mot,
et etendre les paquets composes sur plusieurs mots.

Tout comme Unicode exprime chaque caractere du monde
sur la base de "un caractere = 2 octets",
ce langage exprime chaque element du raisonnement de l'IA
sur la base de "un mot = 2 octets".

---

## Retrocompatibilite et extension ascendante

Un autre atout de 16 bits est l'alignement.

16 est un multiple de 8, un diviseur de 32, un diviseur de 64 et un diviseur de 128.

Cela signifie que l'alignement ne se brise jamais, quelle que soit la direction dans laquelle on etend.

Que se passe-t-il si l'architecture transformer change a l'avenir
et que les tokens deviennent 32 bits ?
Deux mots de 16 bits forment un token. Aucun probleme d'alignement.

Et 64 bits ?
Quatre mots de 16 bits forment un token. Toujours aucun probleme d'alignement.

Inversement, que se passe-t-il si un systeme embarque 8 bits traite ce format ?
Il suffit de lire chaque mot de 16 bits comme un octet de poids fort et un octet de poids faible.

La retrocompatibilite doit etre maintenue de maniere absolue.
Le mot de 16 bits la garantit au niveau physique.

Nous ne pouvons pas predire la taille de mot des intelligences futures,
mais l'alignement multiple de 16 bits garantit la compatibilite avec toute taille.

---

## La triple structure

Resumons.

Un seul mot de 16 bits est simultanement trois choses.

| Monde | Role d'un mot |
|-------|---------------------|
| Reseau | Unite du flux d'octets |
| Stockage | Unite du format de fichier |
| IA | Unite du token LLM |

Une seule unite traverse les trois mondes.

Stocker un flux tel quel, et c'est un fichier.
Lire un fichier tel quel, et ce sont des tokens.
Envoyer des tokens tels quels, et c'est un flux.

Aucune conversion.
Aucune traduction.
Aucune perte.

Voila pourquoi 16 bits.
Ni 8 bits, ni 32 bits, ni longueur variable.
Le nombre qui se situe precisement a l'intersection des trois mondes.

16.
