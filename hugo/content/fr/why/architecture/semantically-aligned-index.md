---
title: "Pourquoi un index semantiquement aligne ?"
weight: 15
date: 2026-02-26T12:00:03+09:00
lastmod: 2026-02-26T12:00:03+09:00
tags: ["SIDX", "alignement semantique", "index"]
summary: "Quand le sens est grave dans les bits, la recherche devient raisonnement"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Ce qui se passe quand un identifiant est un savoir, pas une adresse

---

## Une adresse ne sait rien

Pour trouver Yi Sun-sin dans une base de donnees, il faut un identifiant.

Dans Wikidata, l'identifiant de Yi Sun-sin est `Q8492`.

Ce numero pointe vers Yi Sun-sin.
Mais la chaine `Q8492` elle-meme ne sait rien.

Elle ne sait pas s'il s'agit d'une personne ou d'un batiment.
Elle ne sait pas s'il s'agit d'un Coreen ou d'un citoyen francais.
Elle ne sait pas s'il s'agit d'un personnage du XVIe siecle ou du XXIe siecle.
Elle ne sait pas s'il est vivant ou mort.

`Q8492` est une adresse.
Un facteur qui livre le courrier n'a aucune idee de ce qui est ecrit dans l'enveloppe.
Il regarde simplement l'adresse sur l'enveloppe et livre.

UUID, c'est pareil. `550e8400-e29b-41d4-a716-446655440000`.
128 bits de nombres aleatoires. Unique seulement pour eviter les collisions --
cela ne dit rien sur ce a quoi il fait reference.

Depuis cinquante ans, les identifiants de bases de donnees fonctionnent ainsi.
Un identifiant est une adresse, et pour apprendre quoi que ce soit, il faut suivre cette adresse et lire les donnees.

---

## Il faut suivre pour savoir

Pourquoi est-ce un probleme ?

Supposons que vous vouliez trouver "un philosophe masculin de nationalite allemande ne au XIXe siecle".

Dans une base de donnees traditionnelle, voici comment cela se passe :

```
1. Filtrer la table des personnes ou gender = 'male'
2. JOIN avec la table des nationalites et filtrer country = 'Germany'
3. JOIN avec la table des dates de naissance et filtrer year BETWEEN 1800 AND 1899
4. JOIN avec la table des professions et filtrer occupation = 'philosopher'
```

Quatre operations JOIN.
Chaque JOIN compare les lignes de deux tables.
Si les tables sont grandes, on parcourt un index ; s'il n'y a pas d'index, on fait un balayage complet.
Avec un milliard d'enregistrements, ce processus prend des secondes a des dizaines de secondes.

Pourquoi est-ce si complexe ?

Parce que l'identifiant ne sait rien.
En regardant `Q8492`, on ne peut pas dire s'il s'agit d'un Allemand ou d'un Coreen,
il faut donc aller dans une autre table pour recuperer cette information.

Pour chaque question, il faut suivre l'adresse de l'identifiant.
C'est le cout que les bases de donnees paient depuis cinquante ans.

---

## Et si l'identifiant savait deja ?

Inversons la premisse.

Et si l'identifiant lui-meme contenait les informations essentielles ?

Et si, simplement en regardant l'identifiant,
on pouvait dire s'il fait reference a un humain, de quel pays il vient,
a quelle epoque il appartient et comment il est classifie ?

Pour trouver "un philosophe allemand masculin du XIXe siecle",
les JOIN deviennent inutiles.

En parcourant un milliard d'identifiants,
on peut instantanement determiner si chacun correspond en examinant ses bits.

C'est l'idee centrale de l'index semantiquement aligne.

---

## Aligner le sens dans l'identifiant

SIDX (Semantically-Aligned Index) est un identifiant de 64 bits.

Ces 64 bits ne sont pas des nombres aleatoires.
Un sens est attribue a la position de chaque bit.

Les bits de poids fort contiennent l'information la plus importante.
Quel type d'entite est-ce ? Une personne, un lieu, un evenement, un concept ?

Les bits suivants contiennent des informations de classification.
S'il s'agit d'une personne, quelle epoque ? Quelle region ?

Les bits de poids faible portent des informations de plus en plus specifiques.

Le principe cle est le suivant :

> L'ordre des bits est l'ordre d'importance de l'information.

La classification la plus fondamentale en haut,
les distinctions les plus fines en bas.

Ce n'est pas un simple tri.
C'est une philosophie de conception.

---

## D'un milliard a dix mille, en un seul passage

La puissance pratique de SIDX se revele dans les chiffres.

WMS contient un milliard d'entites.
Le SIDX de chaque entite fait 64 bits.
Taille totale : 1 milliard x 8 octets = 8 Go.

Ces 8 Go tiennent entierement en memoire.

Vous voulez trouver "les entites qui sont humaines et originaires d'Asie de l'Est".
Les bits de poids fort contiennent un drapeau "humain" et un code "Asie de l'Est",
donc on peut filtrer avec un seul masque de bits.

```
mask   = 0xFF00_0000_0000_0000  (8 bits de poids fort : type + region)
target = 0x8100_0000_0000_0000  (humain + Asie de l'Est)

for each sidx in 1_billion:
    if (sidx & mask) == target:
        add to candidates
```

Cette operation se parallelise avec SIMD.
Avec AVX-512, on compare 8 SIDX simultanement en une seule instruction.
Balayage d'un milliard d'entrees : environ 12 millisecondes.

Sur un GPU ? Moins d'une milliseconde.

Un milliard d'enregistrements reduits a dix mille.
Filtrer les dix mille restants en detail est instantane.

Zero JOIN.
Zero parcours d'arbre d'index.
Juste un AND au niveau des bits.

---

## Pourquoi 64 bits suffisent

Au debut, je pensais qu'un espace plus grand etait necessaire.

32 octets (256 bits). Un vecteur FP16 a 32 dimensions.
J'ai essaye d'incorporer chaque attribut cle d'une entite dans l'identifiant.
S'il s'agit d'un humain, son genre, sa nationalite, son epoque, sa profession, sa region, s'il est vivant, son chemin de classification...

Mais ensuite j'ai realise quelque chose.

**L'identifiant n'a pas besoin de tout savoir.**

Il lui suffit de reduire un milliard d'enregistrements a dix mille.
WMS s'occupe du reste.

Pensez-y comme a un point de controle.
A un peage autoroutier, pour determiner que
"ce vehicule se dirige vers la province de Gyeonggi" a partir de la plaque d'immatriculation,
vous n'avez pas besoin de savoir ce qui est charge dans le coffre.

64 bits suffisent.
Utilisez les bits de poids fort pour capturer le type et la classification generale,
et les bits de poids faible pour une classification plus fine.
64 bits sont amplement suffisants pour reduire un milliard d'enregistrements a dix mille.

Et 64 bits = quatre mots de 16 bits.
Ils circulent naturellement dans un flux.
Un identifiant de 32 octets alourdirait un flux,
mais un SIDX de 64 bits est leger et rapide.

---

## Degradation gracieuse : le sens survit meme quand les bits sont tronques

Un autre atout de l'alignement semantique est ses caracteristiques de degradation.

Parce que les bits de SIDX sont ordonnes du plus important au moins important,
meme si les bits de poids faible sont endommages ou tronques,
l'information essentielle dans les bits de poids fort est preservee.

```
64 bits complets :  "Yi Sun-sin, commandant naval du Joseon du XVIe siecle"
48 bits :           "Officier militaire du Joseon du XVIe siecle"
32 bits :           "Humain d'Asie de l'Est du XVIe siecle"
16 bits :           "Humain"
8 bits :            "Entite physique"
```

A mesure que l'information est tronquee, la specificite est perdue,
mais la classification la plus fondamentale survit jusqu'au bout.

C'est une implementation au niveau des bits du principe de "degradation gracieuse".

Meme si une interruption reseau ne livre que des donnees partielles,
le systeme sait "je ne sais pas exactement qui c'est, mais c'est au moins une histoire a propos d'un humain"
et peut continuer a raisonner.

Un contour flou vaut mieux que le silence total.
Une comprehension partielle vaut mieux qu'un echec complet.

---

## Une requete devient un identifiant

La possibilite la plus fascinante qu'ouvre l'indexation semantiquement alignee
est celle-ci : une requete en langage naturel peut etre convertie en un SIDX temporaire.

Un utilisateur demande : "Qui etait le general qui a vaincu la marine japonaise pendant la guerre d'Imjin ?"

L'encodeur analyse cette question.
Humain. Asie de l'Est. XVIe siecle. Domaine militaire.
L'assemblage de ces attributs en bits produit un SIDX temporaire.

Ce SIDX temporaire balaye les milliards de SIDX dans WMS.
Les entites dont les motifs de bits sont les plus similaires emergent comme candidats.
Yi Sun-sin, Won Gyun, Gwon Yul, Yi Eok-gi...

Le croisement d'informations detaillees avec ces candidats donne la reponse finale.

Cela unifie la recherche et la liaison d'entites en un seul mecanisme.
Pas besoin d'un moteur de recherche separe.
Pas besoin d'un pipeline NER (Named Entity Recognition) separe.
Une seule comparaison SIDX suffit.

---

## Pourquoi pas un B-Tree ?

Les bases de donnees traditionnelles utilisent des index B-Tree.

Les B-Tree excellent a trouver une valeur specifique dans des donnees triees en O(log n).
Pour "trouver Q8492", ils sont optimaux.

Mais pour "trouver toutes les entites qui sont humaines et originaires d'Asie de l'Est", ils sont faibles.
Les recherches a conditions composees necessitent l'intersection de plusieurs index,
et le cout de l'intersection croit fortement avec l'echelle des donnees.

Le balayage exhaustif SIDX + SIMD adopte une approche fondamentalement differente.

Si un B-Tree est un annuaire telephonique qui repond rapidement a "qui habite a cette adresse",
un balayage SIDX est un profilage qui repond rapidement a "qui a ces caracteristiques".

La nature de la question differe, et la structure de donnees optimale aussi.

| Type de requete | B-Tree | Balayage SIDX |
|-----------|--------|-----------|
| Recherche par identifiant specifique | O(log n), optimal | Inutile (utiliser un hash) |
| Filtrage par conditions composees | Necessite des JOIN, lent | Un seul AND de bits, rapide |
| Recherche d'entites similaires | Impossible | Possible par similarite vectorielle |
| Insertion | O(log n), reequilibrage | O(1), ajout |
| Complexite d'implementation | Elevee | Faible |

WMS n'utilise pas de B-Tree.
Il charge un milliard de SIDX en memoire
et effectue un balayage exhaustif avec des masques de bits SIMD.

Simple. Force brute. Rapide.

---

## La sagesse de Huffman

La structure d'allocation de bits de SIDX suit le principe du codage de Huffman.

Dans le codage de Huffman, les symboles frequents recoivent des codes plus courts,
et les symboles rares recoivent des codes plus longs.

Dans SIDX, l'information de classification la plus frequemment necessaire occupe les bits de poids fort,
et les details rarement necessaires occupent les bits de poids faible.

Le meme principe gouverne les prefixes de type de paquet de ce langage.
Le Tiny Verb Edge, de frequence maximale, obtient le prefixe le plus court.
L'Event6 Edge, de faible frequence, obtient un prefixe plus long.

La sagesse de Huffman traverse chaque couche de cette conception.
Pas un seul bit n'est gaspille.
Le cout le plus faible pour la chose la plus importante.

---

## Resume

Un identifiant traditionnel est une adresse. Une adresse ne sait rien.

1. Quand l'identifiant ne porte pas de sens, il faut suivre les donnees a chaque fois. C'est un JOIN.
2. Quatre JOIN sur un milliard d'enregistrements, c'est lent.
3. SIDX encode le sens directement dans l'identifiant par l'alignement semantique.
4. Un seul AND de masque de bits reduit un milliard d'enregistrements a dix mille. Zero JOIN.
5. 64 bits suffisent. L'identifiant n'a pas besoin de tout savoir -- il lui suffit de reduire les candidats.
6. Parce que l'information la plus importante occupe les bits de poids fort, le sens essentiel survit meme quand les bits sont tronques.
7. Convertir une requete en langage naturel en un SIDX temporaire transforme la recherche en une operation vectorielle.

Au moment ou un identifiant cesse d'etre une adresse et devient un savoir,
les regles de la base de donnees changent.
