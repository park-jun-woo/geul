---
title: "Pourquoi RAG ne suffit pas"
weight: 2
date: 2026-02-26T12:00:11+09:00
lastmod: 2026-02-26T12:00:11+09:00
tags: ["RAG", "recherche", "embedding"]
summary: "Paraitre pertinent et etre pertinent ne sont pas la meme chose"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Paraitre pertinent et etre pertinent ne sont pas la meme chose.

---

## RAG est le standard actuel

En 2024, RAG est la methode la plus courante pour deployer les LLM en entreprise.

Retrieval-Augmented Generation.
Rechercher des documents externes, les injecter dans le contexte, et faire repondre le modele sur cette base.

RAG fonctionne.
Il permet aux LLM de referencer des documents internes sur lesquels ils n'ont jamais ete entraines.
Il leur permet de refleter des informations a jour.
Il reduit significativement les hallucinations.

Sans RAG, l'adoption des LLM en entreprise aurait ete bien plus lente.
RAG est une technologie qui merite le respect.

Mais RAG a des limites fondamentales.
Ces limites ne se resolvent pas en construisant un meilleur RAG.
Elles decoulent de la premisse meme de RAG.

---

## Comment RAG fonctionne

Le coeur de RAG tient en trois etapes.

**Etape 1 : Decouper les documents en fragments.**
Les PDF, wikis, documents internes sont divises en tailles fixes (generalement 200 a 500 tokens).

**Etape 2 : Convertir chaque fragment en vecteur d'embedding.**
Un vecteur reel de plusieurs centaines a milliers de dimensions.
Le "sens" du texte projete en un seul point dans l'espace vectoriel.

**Etape 3 : Quand une requete arrive, trouver les vecteurs similaires.**
La requete est aussi convertie en vecteur.
Les 5 a 20 fragments ayant la plus haute similarite cosine sont selectionnes et inseres dans le contexte.

Simple et elegant.
Et c'est la que se trouvent trois problemes fondamentaux.

---

## Probleme 1 : Similaire n'est pas pertinent

La similarite d'embedding mesure "si deux textes utilisent des mots similaires dans des contextes similaires."

Ce n'est pas la pertinence.

Exemple.

Requete : "Quel etait le chiffre d'affaires d'Apple au T3 2024 ?"

Les fragments que la recherche d'embedding pourrait retourner :
- "Le chiffre d'affaires d'Apple au T3 2024 etait de 94,9 milliards de dollars." -- Pertinent
- "Le chiffre d'affaires d'Apple au T3 2023 etait de 81,8 milliards de dollars." -- Similaire mais periode differente
- "Le chiffre d'affaires de Samsung Electronics au T3 2024 etait de 79 000 milliards de wons." -- Similaire mais entreprise differente
- "Une tarte aux pommes contient environ 296 kcal." -- Chevauchement de mots-cles

La similarite d'embedding ne peut pas distinguer ces quatre cas.
Dans l'espace vectoriel, "chiffre d'affaires Apple" se regroupe autour d'une seule region.
Que ce soit 2023 ou 2024, Apple ou Samsung --
la distance vectorielle ne les separe pas de maniere fiable.

Ajouter un reranker ameliore les choses.
Mais un reranker lit et juge aussi du texte en langage naturel,
donc le probleme fondamental d'ambiguite demeure.

La recherche basee sur la structure semantique est differente.
Si "Apple" l'entite a un identifiant unique,
elle n'est jamais confondue avec "apple" le fruit.
Si "T3 2024" est un champ temporel,
il est mecaniquement distingue de "T3 2023."

Pas besoin de calculer la similarite.
Ca correspond ou pas ? Oui ou non.

---

## Probleme 2 : Les fragments ne sont pas des unites de sens

Revenons a la premiere etape de RAG.
"Decouper les documents en fragments."

Ce "decoupage" est le probleme.

Quand vous decoupez un document en unites de 500 tokens,
le sens est coupe au milieu.
Un paragraphe s'etend sur deux fragments.
La premisse et la conclusion d'un argument sont separees.

"Yi Sun-sin a affronte 133 navires avec seulement 12 a la bataille de Myeongnyang" est dans le Fragment A,
et "les historiens contestent ces chiffres" est dans le Fragment B.
Si seul le Fragment A est recupere pour une requete,
l'information de fiabilite entre dans le contexte deja perdue.

Augmenter la taille des fragments ? Ils consomment plus de la fenetre.
Reduire la taille des fragments ? Plus de contexte est coupe.
Ajouter du chevauchement ? Vous gaspillez la fenetre sur des doublons.

Quel que soit l'ajustement, le probleme fondamental est le meme.
Decouper du texte en langage naturel par nombre de tokens
revient a decouper le sens par nombre de tokens.
Le sens a une taille inherente,
et le diviser par une unite sans rapport cause des problemes.

Dans une representation structuree, les unites de sens sont explicites.
Une predication est une arete.
Une arete n'est pas coupee.
La recherche opere au niveau de l'arete.
Il n'y a pas de coupure au milieu du sens.

---

## Probleme 3 : La qualite des resultats recuperes est inconnue

RAG a retourne 5 fragments.
Avant de mettre ces 5 dans le contexte, il y a des questions a poser.

Quelle est la source de cette information ?
Quelle est la date de reference ?
Quel est le degre de certitude ?
Ces 5 se contredisent-ils ?

Dans des fragments en langage naturel, on ne peut pas le savoir.

La source peut etre mentionnee quelque part dans le fragment en langage naturel, ou pas.
La reference temporelle peut etre quelque part dans le document, ou elle a pu etre perdue lors du decoupage.
La confiance n'a pas de champ structurel en langage naturel, donc elle est presque toujours absente.
La verification des contradictions exige de lire les 5 fragments et de raisonner dessus.

Au final, il faut deleguer le jugement de qualite au LLM.
On utilise RAG pour reduire les couts d'appel au LLM,
mais on appelle le LLM pour verifier les resultats de RAG.

Dans une representation structuree, la source, le temps et la confiance sont des champs.
"Exclure les enonces sans source" tient en une ligne de requete.
"Exclure les informations anterieures a 2023" est une comparaison de champ.
"Exclure la confiance inferieure a 0,5" est une comparaison numerique.
Pas besoin d'appel au LLM.

---

## La premisse fondamentale de RAG

La racine de ces trois problemes est une seule chose.

RAG recherche du langage naturel comme du langage naturel.

Les documents sont du langage naturel.
Les fragments sont du langage naturel.
Les embeddings sont des approximations statistiques du langage naturel.
Les resultats de recherche sont du langage naturel.
Ce qui entre dans le contexte est du langage naturel.

L'ambiguite du langage naturel impregne tout le pipeline.

La recherche est imprecise parce qu'on cherche du contenu ambigu sous sa forme ambigue.
Le contexte est perdu parce qu'on decoupe du contenu ambigu par une taille sans rapport avec le sens.
La verification est impossible parce qu'on ne peut pas extraire d'information de qualite d'un contenu ambigu.

La plupart des tentatives d'ameliorer RAG operent dans cette premisse.

Utiliser un meilleur modele d'embedding. -- L'approximation statistique devient plus raffinee, c'est tout.
Utiliser une meilleure strategie de decoupage. -- Les positions de coupure s'ameliorent, c'est tout.
Ajouter un reranker. -- On relit le langage naturel une fois de plus, c'est tout.
Utiliser la recherche hybride. -- On melange mots-cles et similarite, c'est tout.

Tous fonctionnent.
Tous restent dans le cadre du langage naturel.
Aucun n'est fondamental.

---

## Conditions pour une alternative fondamentale

Pour depasser les limites de RAG, la premisse doit changer.
Ne pas rechercher du langage naturel comme du langage naturel,
mais rechercher des representations structurees de maniere structurelle.

Cette alternative doit satisfaire trois conditions.

**Recherche par correspondance, pas par similarite.**
Ne pas trouver "des choses qui se ressemblent"
mais trouver "des choses qui correspondent."
L'identifiant correspond-il ? Est-ce dans la plage temporelle ?
Oui ou non. Pas une probabilite.

**L'unite de sens est l'unite de recherche.**
Ne pas decouper par nombre de tokens
mais stocker par predication et rechercher par predication.
Pas de coupure au milieu du sens.

**Les metadonnees sont integrees dans la structure.**
Pas besoin d'appeler un LLM pour juger la qualite des resultats de recherche.
La source, le temps et la confiance sont des champs,
donc le filtrage mecanique est possible.

Quand ces trois conditions sont remplies,
la recherche passe de "deviner des candidats plausibles"
a "confirmer ce qui correspond."

---

## RAG est une technologie de transition

Ce n'est pas pour denigrer RAG.

RAG etait la meilleure reponse dans un monde ou le langage naturel etait tout ce qui existait.
Quand les documents etaient du langage naturel, les connaissances stockees en langage naturel,
et les LLM des outils qui traitent le langage naturel,
rechercher du langage naturel avec du langage naturel etait le choix evident.

Et RAG fonctionne.
Un LLM avec RAG est bien plus precis qu'un LLM sans.
C'est un fait.

Mais si la premisse d'"un monde ou le langage naturel est tout ce qui existe" change,
la position de RAG change aussi.

Si des representations structurees existent,
RAG devient le front-end qui "prend du langage naturel en entree et recherche dans un magasin structure."
Langage naturel -> requete structuree -> recherche structurelle -> resultats structures -> contexte.

RAG ne disparait pas.
Son backend change.
De la recherche par similarite d'embedding a la recherche basee sur la structure semantique.

---

## Resume

RAG est le standard actuel du context engineering.
Et il a trois limites fondamentales.

1. **Similaire ≠ pertinent.** La similarite d'embedding ne garantit pas la pertinence. "Ca se ressemble" et "c'est pertinent" sont differents.
2. **Fragment ≠ sens.** Le decoupage par nombre de tokens coupe au milieu du sens. Les premisses et les conclusions sont separees. L'information de fiabilite est perdue.
3. **Le jugement de qualite est impossible.** La source, le temps et la confiance des fragments recuperes ne peuvent pas etre determines mecaniquement. Les juger necessite un appel au LLM.

La racine des trois problemes est une seule chose.
Rechercher du langage naturel comme du langage naturel.

L'alternative fondamentale est de changer la premisse.
Correspondance, pas similarite.
Predication, pas fragments de tokens.
Metadonnees integrees, pas jugement externe.

RAG est une technologie de transition.
C'etait la meilleure reponse dans un monde ou le langage naturel etait tout ce qui existait.
Quand cette premisse change, le backend de RAG change.
