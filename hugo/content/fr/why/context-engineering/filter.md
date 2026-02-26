---
title: "Pourquoi les filtres sont necessaires"
weight: 5
date: 2026-02-26T12:00:09+09:00
lastmod: 2026-02-26T12:00:09+09:00
tags: ["filtre", "pertinence", "confiance"]
summary: "Une information valide n'est pas toujours une information necessaire"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Une information valide n'est pas toujours une information necessaire.

---

## Vous avez 1 000 informations qui ont passe la verification

Supposons que la verification mecanique ait fonctionne.

Le format est correct,
les champs obligatoires existent,
les identifiants sont valides,
les types sont appropries,
et l'integrite referentielle est respectee -- 1 000 enonces subsistent.

Tous sont des informations valides.
Ils sont conformes a la specification. Il n'y a aucune raison de les rejeter.

Mais la fenetre de contexte ne peut en contenir que 300.

Lesquels 300 mettez-vous ?

C'est le probleme du filtrage.

---

## Verification et filtrage posent des questions differentes

Ce que la verification demande : "Cette information est-elle valide ?"
Ce que le filtrage demande : "Cette information est-elle necessaire maintenant ?"

La verification examine les proprietes de l'information elle-meme.
Le format est-il correct ? Les champs sont-ils presents ? Les references sont-elles valides ?
Elle ne se soucie pas du sujet de l'information ni de l'usage qu'on en fera.

Le filtrage examine la relation entre l'information et la situation.
Est-elle pertinente pour cette inference particuliere en ce moment ?
Cette information est-elle fiable ?
Est-elle suffisamment recente ?

La verification est possible sans contexte. On n'a besoin que de la specification.
Le filtrage est impossible sans contexte. Il faut savoir "ce qui est necessaire maintenant."

La verification est deterministe. Valide ou invalide.
Le filtrage est un jugement. La pertinence a des degres, la fiabilite a des seuils, la recence depend du contexte.

La verification est bon marche.
Le filtrage est relativement couteux.

C'est pourquoi la verification vient d'abord et le filtrage vient apres.
Si la verification filtre en premier, le filtrage juge un ensemble plus petit.
Le cout du jugement couteux diminue.

---

## Trois choses que le filtrage juge

Le filtrage examine trois elements principaux.

### Pertinence : est-ce necessaire pour cette inference ?

L'utilisateur a demande "le benefice d'exploitation de Samsung Electronics au T3 2024."

Parmi les enonces valides ayant passe la verification :

- Le benefice d'exploitation de Samsung Electronics au T3 2024 etait de 9 180 milliards de wons.
- Le chiffre d'affaires de Samsung Electronics au T3 2024 etait de 79 000 milliards de wons.
- Le benefice d'exploitation de Samsung Electronics au T3 2023 etait de 2 430 milliards de wons.
- Le plan d'investissement de Samsung Electronics dans les semi-conducteurs est de 53 000 milliards de wons en 2025.
- Le siege de Samsung Electronics est a Suwon.

Tous valides. Tous concernent Samsung Electronics.
Les mettez-vous tous dans le contexte ?

L'emplacement du siege est non pertinent.
Le plan d'investissement a une faible pertinence.
Le benefice d'exploitation de 2023 peut etre utile pour la comparaison.
Le chiffre d'affaires est etroitement lie au benefice d'exploitation.

Dans le RAG en langage naturel, ce jugement est delegue a la similarite d'embedding.
Classe par distance vectorielle a "benefice d'exploitation Samsung Electronics."
Mais comme deja discute, similaire n'est pas pertinent.

Dans une representation structuree, le jugement de pertinence a des entrees differentes.
Vers quelle entite l'enonce pointe-t-il ? Samsung Electronics.
Quelle propriete ? Benefice d'exploitation.
Quel moment ? T3 2024.

Si l'entite, la propriete et le temps existent comme champs,
on peut trouver "meme entite, meme propriete, meme moment" avec precision.
Et on peut intentionnellement inclure ou exclure "meme entite, meme propriete, moment different."
Correspondance de champs, pas distance vectorielle.

La pertinence reste un jugement. Pas deterministe.
Mais que l'entree de ce jugement soit la distance vectorielle ou des champs structures fait une difference en precision.

### Fiabilite : peut-on croire cette information ?

Deux enonces existent sur le meme sujet.

- Source : publication IR de Samsung Electronics. Confiance : 1,0. "Benefice d'exploitation T3 2024 : 9 180 milliards de wons."
- Source : blog anonyme. Confiance : 0,3. "Benefice d'exploitation T3 2024 : environ 10 000 milliards de wons."

Lequel va dans le contexte ?

Evidemment le premier.

Mais pour que ce jugement soit "evident",
la source et la confiance doivent exister sous une forme lisible.

Dans les fragments en langage naturel, la source est enfouie quelque part dans le texte ou absente.
La confiance n'a jamais ete exprimee.
Pour comparer deux fragments et juger lequel est plus fiable,
un LLM doit lire et raisonner.

Dans une representation structuree, la source et la confiance sont des champs.
"Exclure la confiance inferieure a 0,5" est une comparaison.
"Inclure uniquement les sources primaires" est une correspondance de champ.

Le cout du filtrage par fiabilite passe de l'inference LLM a la comparaison de champs.

### Recence : cette information est-elle suffisamment actuelle ?

"Qui est le PDG de Samsung Electronics ?"

- Temps : mars 2024. "PDG de Samsung Electronics : Kyung Kye-hyun."
- Temps : decembre 2022. "Co-PDG de Samsung Electronics : Han Jong-hee, Kyung Kye-hyun."

Les deux sont valides. Format correct, sources presentes.
Mais c'est le plus recent qui est necessaire.

En langage naturel, le temps peut ou non etre mentionne dans le texte.
S'il est ecrit "l'annee derniere," il faut aussi calculer quand etait "l'annee derniere."

Dans une representation structuree, le temps est un champ.
Une date ISO 8601.
"Inclure uniquement l'enonce le plus recent" est une operation de tri.

Plus important, le critere de recence depend du contexte.
Si on demande le PDG, l'entree la plus recente est necessaire.
Si on demande tous les PDG passes, chaque entree est necessaire.
Si on demande les tendances de chiffre d'affaires, les 8 derniers trimestres sont necessaires.

Si le temps existe comme champ, ces conditions peuvent s'exprimer comme une requete.
Si le temps est enfoui dans le langage naturel, il faut l'extraire a chaque fois.

---

## Pourquoi le filtrage n'est pas de la verification mecanique

Il y a une distinction importante ici.

Parmi les trois criteres du filtrage -- pertinence, fiabilite, recence --
la fiabilite et la recence peuvent etre largement traitees mecaniquement dans une representation structuree.
Comparaison de champs, tri de valeurs, filtrage par plage.

Alors pourquoi appeler cela "filtrage" et non "verification" ?

La verification ne regarde que les proprietes de l'information elle-meme.
"Cet enonce a-t-il un champ temporel ?" Present ou absent. Pas besoin de contexte.

Le filtrage regarde la relation entre l'information et la situation.
"Le temps de cet enonce est-il approprie pour cette question ?" Il faut connaitre la question pour repondre.

Les deux examinent le meme champ temporel,
mais la verification verifie "l'existence"
et le filtrage juge "l'adequation."

L'existence n'a pas besoin de contexte.
L'adequation a besoin de contexte.

Cette difference est la raison pour laquelle le pipeline separe les deux etapes.

---

## La structure de cout du filtrage

Le filtrage est plus couteux que la verification. Mais a quel point depend de la representation.

**Filtrage dans un pipeline en langage naturel :**
Jugement de pertinence -- inference LLM ou calcul de similarite d'embedding.
Jugement de fiabilite -- le LLM extrait l'information de source du texte et evalue.
Jugement de recence -- le LLM extrait l'information temporelle du texte et compare.
Tout est raisonnement. Tout est couteux.

**Filtrage dans une representation structuree :**
Jugement de pertinence -- correspondance de champs entite/propriete + jugement base sur le contexte.
Jugement de fiabilite -- comparaison du champ confiance. Correspondance du champ source.
Jugement de recence -- tri du champ temporel. Comparaison de plage.
La fiabilite et la recence sont des operations sur champs. Seule la pertinence necessite un jugement.

Autrement dit, la structuration convertit deux des trois criteres de filtrage en operations mecaniques.
Ce qui reste est la pertinence seule.
Meme la pertinence passe de "ce bloc de texte est-il similaire a la question" a "cette propriete de cette entite est-elle pertinente pour la question," rendant le jugement plus clair.

Le cout total du filtrage baisse significativement.

---

## Ce qui se passe sans filtrage

Si on verifie mais qu'on met tout dans le contexte sans filtrer.

Les 1 000 informations valides entrent.
De celles-ci, seules 30 sont necessaires maintenant.

Le LLM lit les 1 000.
La lecture coute de l'argent.
970 informations inutiles dispersent l'attention.
La recherche montre que plus il y a d'informations non pertinentes dans le contexte, plus la probabilite d'hallucination augmente.
La qualite du raisonnement sur les 30 qui comptent reellement se degrade.

La fenetre est aussi gaspillee.
Sur l'espace que 1 000 elements occupent, l'equivalent de 970 elements est du gaspillage.
Cet espace aurait pu contenir d'autres informations plus pertinentes.

Le filtrage consiste a gerer une fenetre finie de maniere finie.
Si la verification confirme "est-ce qualifie pour entrer",
le filtrage juge "y a-t-il une raison d'entrer."

La qualification est une question de format. La raison est une question de contexte.
Les deux sont necessaires.

---

## Le filtrage est une politique

Un point important de plus.

Les criteres de filtrage ne sont pas fixes.
Ils varient selon le contexte.

Filtrage pour un agent de consultation medicale :
Le seuil de fiabilite est eleve. Exclure la confiance inferieure a 0,9.
Le critere de recence est strict. Exclure les informations medicales de plus de 3 ans.
Exclure les sources qui ne sont pas des revues a comite de lecture.

Filtrage pour un agent de conversation informelle :
Le seuil de fiabilite est bas. L'information approximative est acceptable.
Le critere de recence est flexible. Des informations plus anciennes peuvent etre incluses selon le contexte.
Les contraintes sur les sources sont laches.

La meme information passe dans un agent et est rejetee dans un autre.
L'information n'a pas change. La politique est differente.

Cela signifie que le filtrage n'est pas simplement un probleme technique
mais un probleme de conception.
"Ce qui entre dans le contexte" est la meme question que
"quels standards voulons-nous que cet agent respecte."

Dans une representation structuree, cette politique s'exprime de maniere declarative.
"confidence >= 0.9, time >= 2022, source_type = peer-reviewed."
Une ligne de requete.

En langage naturel, cette politique est ecrite en langage naturel dans le prompt.
"Veuillez ne vous referer qu'a des informations fiables et recentes."
Que le LLM suive cela de maniere constante est une question de probabilite.

---

## Resume

Toute information qui passe la verification n'est pas necessaire.
Une fenetre de contexte finie ne devrait contenir que ce qui est necessaire pour l'inference en cours.

Le filtrage juge trois choses.
Pertinence -- cette information est-elle necessaire pour la question actuelle ?
Fiabilite -- peut-on croire cette information ?
Recence -- cette information est-elle suffisamment actuelle ?

Verification et filtrage posent des questions differentes.
La verification demande "est-ce valide ?" ; le filtrage demande "est-ce necessaire ?"
La verification est possible sans contexte ; le filtrage necessite un contexte.
La verification vient d'abord ; le filtrage vient apres.

Dans une representation structuree, deux des trois criteres de filtrage -- fiabilite et recence -- sont convertis en operations sur champs. Ce qui reste est la pertinence seule, et meme celle-ci devient plus claire grace a la correspondance structurelle de champs.

Le filtrage est une politique.
La meme information est incluse ou exclue selon le contexte.
Dans une representation structuree, cette politique est declaree comme une requete.
En langage naturel, cette politique est ecrite dans le prompt comme un espoir.
