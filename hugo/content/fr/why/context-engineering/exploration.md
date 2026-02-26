---
title: "Pourquoi l'exploration est necessaire"
weight: 7
date: 2026-02-26T12:00:07+09:00
lastmod: 2026-02-26T12:00:07+09:00
tags: ["exploration", "recherche", "echelle"]
summary: "Quand l'index depasse la fenetre, le paradigme de recherche lui-meme atteint sa limite"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Quand l'index depasse la fenetre, le paradigme de recherche lui-meme atteint sa limite.

---

## La recherche a reussi

Nous avons discute des limites de RAG.
L'imprecision de la similarite d'embedding, l'arbitraire du decoupage en fragments, l'impossibilite du jugement de qualite.

Mais cette discussion portait sur la qualite de la recherche.
"Comment rechercher de maniere plus precise ?"

Maintenant une question differente doit etre posee.
Supposons que la recherche soit parfaite.
Supposons qu'elle ne retourne que des informations precisement pertinentes pour la requete.

Il y a encore des cas ou cela ne fonctionne pas.

---

## Le probleme d'echelle

Une base de connaissances interne a 1 000 enonces.
Il y a un index. Mettez l'index dans le contexte. Interrogez. Recuperez les resultats.
Ca fonctionne.

Les enonces passent a 100 000.
L'index grossit. Il tient encore dans la fenetre. Ca fonctionne.

Les enonces passent a 10 millions.
L'index lui-meme depasse la fenetre.

Ce n'est pas un probleme de qualite de recherche.
Aussi precise que soit la recherche,
si l'index qu'il faut consulter pour chercher ne tient pas dans la fenetre,
la recherche ne peut meme pas commencer.

Et la connaissance croit.
Les documents d'entreprise augmentent chaque jour.
Ce qu'un agent a appris ne cesse de s'accumuler.
La connaissance du monde ne retrecit pas.

Une fenetre plus grande resout-elle le probleme ?
Si 128K devient 1M puis 10M ?
Si la connaissance atteint 100M, le meme probleme se repete.
La fenetre est toujours finie, et la connaissance croit toujours.
Ce desequilibre est permanent.

---

## La difference entre recherche et exploration

La recherche obtient des resultats avec une seule requete.

Requete : "Benefice d'exploitation Samsung Electronics T3 2024"
-> Resultat : 9 180 milliards de wons.

Un seul coup. Termine.

L'exploration atteint les resultats en plusieurs etapes.

Etape 1 : Voir la carte de connaissance de niveau superieur. "Entreprises", "Industries", "Macroeconomie", "Technologie"...
-> Selectionner "Entreprises."

Etape 2 : Voir la carte des entreprises. "Samsung Electronics", "SK Hynix", "Hyundai Motor"...
-> Selectionner "Samsung Electronics."

Etape 3 : Voir la carte Samsung Electronics. "Finance", "RH", "Technologie", "Juridique"...
-> Selectionner "Finance."

Etape 4 : Voir la carte finance. "Resultats trimestriels", "Resultats annuels", "Plans d'investissement"...
-> Selectionner "Resultats trimestriels."

Etape 5 : Recuperer "T3 2024" des resultats trimestriels.
-> Benefice d'exploitation : 9 180 milliards de wons.

Le resultat est le meme.
Le processus est different.

La recherche demande "Avez-vous ceci ?"
L'exploration traque "Ou cela pourrait-il etre ?"

La recherche exige que l'index soit visible pour celui qui interroge. L'index entier doit etre accessible.
L'exploration n'a besoin de voir que la couche actuelle de la carte. A chaque etape, une seule couche entre dans la fenetre.

---

## L'analogie de la bibliotheque

Vous visitez une bibliotheque de quartier.
Elle a 3 000 livres.
Vous demandez au bibliothecaire : "Avez-vous une biographie de Yi Sun-sin ?"
Le bibliothecaire se souvient : "C'est au bout de l'etagere 3."
Recherche. Ca fonctionne.

Vous visitez la Bibliotheque nationale.
Elle contient 10 millions de volumes.
Vous demandez au bibliothecaire : "Avez-vous une biographie de Yi Sun-sin ?"
Le bibliothecaire ne sait pas non plus. Personne ne memorise 10 millions de volumes.

A la place, il y a un systeme de classification.

Vous consultez le repertoire du rez-de-chaussee. -> La section "Histoire" est au 3e etage.
Vous montez au 3e etage. -> "Histoire de Coree" est dans l'aile est.
Vous allez dans l'aile est. -> "Dynastie Joseon" est dans la rangee D.
Vous allez a la rangee D. -> "Personnages" est dans la 3e section de la rangee D.
Vous cherchez dans la 3e section. -> Il y a une biographie de Yi Sun-sin.

La capacite de memoire du bibliothecaire n'a pas change.
L'echelle de la bibliotheque a change.
La methode est passee de demander au bibliothecaire (recherche) a parcourir le systeme de classification (exploration).

Voici le point cle.
A chaque etape, la taille de ce qui doit etre consulte tient dans la capacite de memoire du bibliothecaire.
Le repertoire du rez-de-chaussee. Le plan des zones du 3e etage. La liste des rangees de l'aile est. La liste des sections de la rangee D.
Tout tient en un seul coup d'oeil.

Le catalogue complet de toutes les collections ne tient pas en un seul coup d'oeil.
Mais la carte de chaque etage, si.

C'est en cela que l'exploration differe de la recherche.
Il n'est pas necessaire de tout voir d'un coup.
Il suffit de juger la prochaine direction depuis l'endroit ou l'on se trouve.

---

## Des cartes de cartes

En termes techniques, c'est une structure hierarchique de cartes.

**Carte de niveau 1** : la classification de niveau superieur de toute la connaissance.
"Cette base de connaissances contient des informations sur les entreprises, les industries, la macroeconomie et la technologie."
Des dizaines d'elements. Tient dans la fenetre.

**Carte de niveau 2** : les sous-categories de chaque classification de niveau superieur.
"La categorie entreprises contient Samsung Electronics, SK Hynix, Hyundai Motor..."
Des dizaines a des centaines d'elements. Tient dans la fenetre.

**Carte de niveau 3** : les categories detaillees de chaque sous-categorie.
"Samsung Electronics contient Finance, RH, Technologie, Juridique..."
Des dizaines d'elements. Tient dans la fenetre.

**Enonces reels** : les informations concretes pointees par la carte de niveau le plus bas.
"Le benefice d'exploitation de Samsung Electronics au T3 2024 etait de 9 180 milliards de wons."

Si la taille de chaque couche tient dans la fenetre,
l'exploration est possible quelle que soit l'echelle totale de la connaissance.

Meme avec 10 millions d'enonces,
si chaque couche a 100 elements, on atteint la cible en 5 etapes d'exploration.
100 -> 100 -> 100 -> 100 -> 100 = couverture jusqu'a 10 milliards.
A chaque etape, seuls 100 elements entrent dans la fenetre.

C'est de la meme maniere qu'un B-tree trouve des donnees sur le disque.
Il ne charge pas toutes les donnees en memoire.
Il lit uniquement le noeud courant de l'arbre et passe au suivant.
Des donnees de n'importe quelle echelle peuvent etre explorees independamment de la taille de la memoire.

La fenetre de contexte est la memoire.
La base de connaissances est le disque.
La carte est un noeud B-tree.

---

## L'agent marche

Dans l'exploration en plusieurs etapes, qui selectionne la direction a chaque etape ?

L'agent.

Mettez la carte de niveau 1 dans le contexte.
L'agent la lit, la compare a la requete, et selectionne la direction "Entreprises."

Demandez la carte de niveau 2.
La carte de sous-categories des entreprises entre dans le contexte.
L'agent la lit et selectionne la direction "Samsung Electronics."

Demandez la carte de niveau 3.
L'agent selectionne "Finance."

C'est l'utilisation d'outils par l'agent.
Lire une carte est un appel d'outil.
Selectionner une direction est un jugement.
Demander la carte suivante est le prochain appel d'outil.

Dans la recherche, l'agent interroge une fois et recoit un resultat. Passif.
Dans l'exploration, l'agent fait plusieurs jugements et selectionne des directions. Actif.

C'est la ou le context engineering rencontre la conception d'agents.
Ce qui entre dans le contexte est determine etape par etape par le jugement de l'agent.
La construction du contexte passe de l'assemblage statique a l'exploration dynamique.

---

## Ce probleme est a peine discute aujourd'hui

En regardant les discussions dans la communaute RAG,
la plupart de l'energie est concentree sur la qualite de la recherche.

De meilleurs modeles d'embedding.
De meilleures strategies de decoupage.
Des architectures de reranker.
La recherche hybride.
Graph RAG.

Tout est important.
Tout porte sur "comment obtenir de meilleurs resultats d'une seule recherche."

"Et si une seule recherche ne suffit pas ?" est a peine discute.

Le moment ou l'index depasse la fenetre.
Le moment ou les resultats sont trop nombreux pour tenir.
Le moment ou l'echelle de la connaissance brise la premisse meme du paradigme de recherche.

Ce moment arrive.
La connaissance croit et la fenetre est finie.

La plupart des solutions actuelles sont de l'evitement.
Ne recuperer que les top k. Ignorer le reste.
Agrandir la fenetre. Les couts augmentent.
Partitionner la connaissance. Separer les magasins de vecteurs par domaine.

Toutes rencontrent le meme probleme quand l'echelle augmente encore.

---

## Prerequis pour l'exploration

Pour que l'exploration fonctionne, la connaissance doit etre dans une structure explorable.

**Une hierarchie doit exister.** Si la connaissance est disposee a plat, l'exploration est impossible. Un magasin de vecteurs d'embedding est plat. Tous les fragments sont au meme niveau. Il n'y a pas de hierarchie, donc le concept de "descendre plus profond" n'existe pas.

**Chaque couche doit tenir dans la fenetre.** Si une seule carte depasse la fenetre, l'exploration echoue. Le nombre de choix a chaque niveau de la hierarchie doit etre de taille appropriee. C'est un probleme de conception de classification.

**Les chemins doivent etre divers.** Il doit etre possible d'atteindre la meme information par plusieurs chemins. Via "Samsung Electronics -> Finance -> Benefice d'exploitation" ou via "Industrie des semi-conducteurs -> Entreprises majeures -> Samsung Electronics -> Resultats." Parce que le chemin naturel varie selon la question. Si le critere de classification est fixe a un seul, il convient a certaines questions et pas a d'autres.

Une structure de dossiers a une hierarchie mais un seul chemin.
Un fichier n'appartient qu'a un seul dossier.
Seul le chemin "Samsung Electronics/Finance/Benefice d'exploitation" existe.
Quand une question sur "l'industrie des semi-conducteurs" arrive, l'exploration naturelle a travers cette structure de dossiers est impossible.

Un graphe a a la fois une hierarchie et des chemins divers.
Un seul noeud peut etre connecte a plusieurs noeuds parents.
Le noeud Samsung Electronics peut etre atteint via un chemin "Entreprises", un chemin "Industrie des semi-conducteurs", ou un chemin "Entreprises cotees au KOSPI."
Quel que soit le contexte d'ou vient la question, un chemin naturel existe.

---

## C'est un probleme non resolu

Il y a quelque chose qui doit etre dit honnetement.

Le besoin d'exploration en plusieurs etapes est clair.
Mais il n'y a pas encore de systeme standard qui l'implemente efficacement.

Comment genere-t-on automatiquement la hierarchie des cartes ?
Comment determine-t-on la taille appropriee de chaque couche ?
Que se passe-t-il quand l'agent selectionne la mauvaise direction ?
Que devient la latence a mesure que la profondeur d'exploration augmente ?

Ce sont des questions ouvertes.

Mais le fait qu'un probleme soit non resolu
ne signifie pas que le probleme n'existe pas.

La connaissance croit.
La fenetre est finie.
Le moment ou la recherche seule ne suffit plus arrive.

L'exploration doit etre prete comme reponse pour ce moment.
Si elle n'est pas prete,
les seuls choix qui restent sont d'agrandir la fenetre ou d'abandonner de la connaissance.

---

## Resume

La recherche retourne des resultats avec une seule requete.
Quand l'echelle de la connaissance devient suffisamment grande, cela ne suffit pas.
Parce que l'index lui-meme depasse la fenetre.

L'exploration suit des cartes hierarchiques, selectionnant des directions en descendant.
Ce qui doit etre consulte a chaque etape tient dans la fenetre.
Chaque etape est finie quelle que soit l'echelle totale.
Tout comme un B-tree trouve des donnees sans charger le disque entier en memoire.

L'agent juge la direction a chaque etape.
La construction du contexte passe de l'assemblage statique a l'exploration dynamique.
C'est la ou le context engineering rencontre la conception d'agents.

Pour que l'exploration fonctionne, la connaissance doit etre hierarchique, chaque couche doit etre finie, et les chemins doivent etre divers.
Une structure de dossiers n'a qu'un seul chemin. Un graphe a des chemins divers.

C'est encore un probleme non resolu sans solution standard.
Mais tant que la connaissance croit et que la fenetre est finie, c'est un probleme qui doit etre resolu.
