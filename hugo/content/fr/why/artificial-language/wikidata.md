---
title: "Pourquoi Wikidata"
weight: 13
date: 2026-02-26T12:00:17+09:00
lastmod: 2026-02-26T12:00:17+09:00
tags: ["Wikidata", "Ontologie", "SIDX"]
summary: "GEUL ne rejette pas Wikidata. Il transforme le systeme de classification et les statistiques de frequence de 100 millions d'entites en livres de codes SIDX. La grammaire est construite par-dessus un dictionnaire."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## GEUL ne rejette pas Wikidata. Il se dresse dessus.

---

## On ne peut pas creer une langue sans dictionnaire

Toute langue a besoin d'un vocabulaire.

Le coreen a le dictionnaire coreen.
L'anglais a le dictionnaire anglais.
Les langages de programmation ont des bibliotheques standard.

Il en va de meme pour une langue artificielle.
Une liste d'entites, une liste de relations, une liste de proprietes.
Quel code represente « Samsung Electronics » dans cette langue ?
Quel code represente la relation « capitale » ?
Il faut un vocabulaire avant de pouvoir ecrire une phrase.

Comment construire ce vocabulaire ?
Il y a deux approches.

Le construire a partir de zero.
Ou utiliser ce qui existe deja.

---

## Construire a partir de zero : la lecon de CYC

Le projet CYC a debute en 1984.

Son objectif etait de formaliser et stocker le savoir de sens commun general.
L'ontologie a ete concue a partir de zero.
Des concepts ont ete definis, des relations ont ete definies, des regles ont ete definies.
Les experts les ont saisis manuellement.

Trente ans ont passe.
Des millions de regles ont ete saisies.

Pourtant, cela etait loin de suffire a couvrir la connaissance du monde.
Il fallait concevoir une ontologie separee pour chaque domaine.
Maintenir la coherence entre les domaines s'est avere difficile.
Chaque fois qu'un nouveau concept apparaissait, l'ontologie devait etre revisee.
Les revisions entraient frequemment en conflit avec les regles existantes.

Ce que CYC a demontre, ce n'est pas son potentiel mais ses limites.
Confier a une petite equipe d'experts la conception de l'ontologie du monde
devient impossible a maintenir a grande echelle.

---

## Ce qui existe deja : Wikidata

Wikidata a ete lance en 2012.

Une base de connaissances structuree geree par la Fondation Wikimedia.
N'importe qui peut la modifier.
En 2024, elle contient plus de 100 millions d'entites.
Plus de 10 000 proprietes.
Des milliards de declarations.
Des libelles dans plus de 300 langues.

L'echelle que CYC n'a pas pu atteindre en 30 ans avec une equipe d'experts,
Wikidata l'a atteinte en 10 ans grace a une communaute.

Voyons ce que Wikidata fournit.

**Identifiants d'entites.** Q-ID. Samsung Electronics est Q20718. Seoul est Q8684. Yi Sun-sin est Q217300. Des identifiants uniques au niveau mondial. Independants de la langue.

**Identifiants de proprietes.** P-ID. « Lieu du siege social » est P159. « Date de creation » est P571. « Population » est P1082. Les relations et proprietes sont identifiees de maniere unique.

**Structure hierarchique.** P31 (instance of) et P279 (subclass of) forment une hierarchie de types. « Seoul → ville → etablissement humain → entite geographique. » Le systeme de classification du monde est exprime a travers ces deux proprietes.

**Libelles multilingues.** Le libelle coreen de Q20718 est « 삼성전자 », le libelle anglais est « Samsung Electronics », le libelle japonais est « サムスン電子 ». Un identifiant, des noms differents pour chaque langue.

**Validation communautaire.** Des millions d'editeurs. Detection du vandalisme. Exigence de sources. Pas parfait, mais plus evolutif qu'une petite equipe d'experts.

Il n'y a aucune raison de construire tout cela a partir de zero.

---

## Le vocabulaire de GEUL provient de Wikidata

Le SIDX (Semantic-aligned Index) de GEUL est un identifiant semantiquement aligne de 64 bits.
La signification est encodee dans les bits eux-memes.
En examinant simplement les bits de poids fort, on peut savoir si quelque chose est une personne, un lieu ou une organisation.

Le livre de codes du SIDX — quel motif de bits correspond a quelle signification — est extrait de Wikidata.

Le processus est le suivant.

**Etape 1 : Extraction des types.**
On extrait tous les Q-ID utilises comme objets de P31 (instance of) dans Wikidata.
Cela produit la liste des « types ».
« Humain (Q5) », « ville (Q515) », « pays (Q6256) », « entreprise (Q4830453) »...
On compte combien de fois chaque type est utilise — le nombre d'instances.

**Etape 2 : Construction de la hierarchie.**
On extrait les relations P279 (subclass of) entre les types.
« Ville → etablissement humain → entite geographique → entite. »
Cela forme la structure arborescente des types.
On identifie les noeuds racine, les noeuds feuille et les noeuds intermediaires.
On detecte et traite l'heritage multiple — les cas ou un type appartient a plusieurs types parents.

**Etape 3 : Attribution des bits.**
La structure de l'arbre determine les relations de prefixe des motifs de bits.
Les sous-types sous le meme parent partagent le meme prefixe.
« Ville » et « bourg » partagent le prefixe d'« etablissement humain ».

Le nombre d'instances influence la longueur en bits.
Les types frequemment utilises recoivent des codes plus efficaces.
Le meme principe que le codage de Huffman : des codes plus courts pour les frequences plus elevees.

---

## Ce que Wikidata fournit

Dans ce processus, Wikidata fournit trois choses.

**Un systeme de classification.**
Une reponse a « Quels types de choses existent dans le monde ? »
CYC confiait cela a une equipe d'experts.
GEUL l'extrait de Wikidata.
Un systeme de classification construit par des millions d'editeurs pendant 10 ans,
transforme en arbre de bits.

**Des statistiques de frequence.**
Une reponse a « Combien de chaque type existe dans le monde ? »
S'il y a 9 millions d'entites humaines et 1 million d'asteroides,
le type « humain » devrait recevoir un code plus efficace qu'« asteroide ».
La frequence d'utilisation reelle determine la conception des codes.

**Un mappage d'identifiants.**
Un mappage entre les Q-ID de Wikidata et les SIDX de GEUL.
Quel motif de bits dans le SIDX correspond a Q20718 (Samsung Electronics) ?
Avec ce mappage, les connaissances de Wikidata peuvent etre converties en GEUL,
et les declarations GEUL peuvent etre reconverties en Wikidata.

---

## Ce que Wikidata ne fournit pas

Wikidata est un dictionnaire. Un dictionnaire n'est pas une langue.

Un dictionnaire fournit une liste de mots.
Une langue fournit la grammaire pour composer des phrases a partir de mots.

Ce que Wikidata ne fournit pas, c'est ce que GEUL ajoute.

**Des faits aux affirmations.**
L'unite de base de Wikidata est un fait (Fact).
« La population de Seoul est de 9,74 millions. »
C'est soit vrai, soit faux.

L'unite de base de GEUL est une affirmation (Claim).
« Selon A, la population de Seoul est d'environ 9,74 millions. (confiance 0,9, en date de 2023) »
Qui affirme, avec quel niveau de certitude, et en date de quand — tout cela est integre dans la declaration.
Cette difference est traitee en detail dans [Pourquoi des affirmations, pas des faits](/fr/why/claims-not-facts/).

**Qualificateurs verbaux.**
Wikidata n'a pas de place pour exprimer les nuances des verbes.
Dans « Yi Sun-sin a remporte la bataille de Myeongnyang »,
ou se trouvent le temps, l'aspect, l'evidentialite, le mode et la confiance ?
Dans Wikidata, ceux-ci sont partiellement exprimes par des qualificateurs,
mais il n'existe pas de systeme systematique de qualification verbale.

GEUL possede un systeme de qualificateurs verbaux de 28 bits.
Treize dimensions — temps, aspect, polarite, evidentialite, mode, volitivite, confiance, et d'autres — sont structurellement integrees dans chaque declaration.

**Compression 16 bits.**
La representation de Wikidata n'a pas ete concue pour les fenetres de contexte.
JSON-LD, RDF, SPARQL.
Lisibles par les machines, mais pas efficaces en tokens.

GEUL est concu en unites de mots de 16 bits.
Correspondance un-pour-un avec les tokens des LLM.
Un systeme de representation construit sur la premisse de fenetres de contexte finies.
Cela a deja ete traite dans [Pourquoi pas MD/JSON/XML](/fr/why/not-md-json-xml/).

**Pipeline de contexte.**
Wikidata est un entrepot. GEUL fait partie d'un pipeline.
Clarification, validation, filtrage, verification de coherence, exploration — tout ce qui a ete discute dans cette serie fonctionne sur la representation structuree de GEUL.
Wikidata ne dispose pas de ce pipeline.
Et n'en a pas besoin. L'objectif de Wikidata est different.

---

## La relation entre un dictionnaire et une langue

En resume :

Wikidata est le vocabulaire du monde.
Quelles entites existent,
quelles relations existent,
quels types existent et comment ils sont classes.
Des millions de personnes l'ont construit pendant 10 ans.

GEUL construit la grammaire par-dessus ce vocabulaire.
Le systeme de classification du vocabulaire → l'arbre de bits du SIDX.
Les statistiques de frequence du vocabulaire → les priorites d'attribution des bits.
Les identifiants du vocabulaire → le mappage avec le SIDX.

Et il ajoute ce qui manque au vocabulaire.
Structure des affirmations. Qualification verbale. Compression au niveau des tokens. Pipeline de contexte.

Pourrait-on construire GEUL sans Wikidata ?
Oui. En concevant l'ontologie a partir de zero, comme CYC.
Mais cela a ete tente il y a 30 ans, et les resultats parlent d'eux-memes.

Parce que Wikidata existe, GEUL ne concoit pas d'ontologie.
Il transforme un consensus existant.

---

## Resume

Une langue artificielle a besoin d'un vocabulaire.
En construire un a partir de zero est ce qu'a tente CYC, et 30 ans ont prouve les limites de cette approche.

Wikidata est le vocabulaire du monde, avec plus de 100 millions d'entites, plus de 10 000 proprietes et des milliards de declarations.
Des millions d'editeurs l'ont construit pendant 10 ans.

Le livre de codes SIDX de GEUL est extrait de Wikidata.
Les frequences d'instances de P31 determinent l'attribution des bits,
et la hierarchie de P279 forme le squelette de l'arbre de bits.

Wikidata est un dictionnaire ; GEUL est une langue.
Un dictionnaire fournit des mots ; une langue fournit la grammaire.
GEUL construit la structure des affirmations, la qualification verbale, la compression 16 bits et un pipeline de contexte par-dessus le vocabulaire de Wikidata.

GEUL ne rejette pas Wikidata.
Il se dresse dessus.
