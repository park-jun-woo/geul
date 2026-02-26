---
title: "Pourquoi l'ere du prompt engineering est terminee"
weight: 1
date: 2026-02-26T12:00:12+09:00
lastmod: 2026-02-26T12:00:12+09:00
tags: ["prompt", "contexte", "ingenierie"]
summary: "De comment le dire a ce qu'on montre -- le jeu a change"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Pourquoi l'ere du prompt engineering est terminee

### De "comment le dire" a "ce qu'on montre" -- le jeu a change.

---

### Le prompt engineering comme profession

En 2023, une nouvelle profession est apparue.

Prompt engineer.

"Pensez etape par etape."
"Vous etes un expert avec 20 ans d'experience."
"Laissez-moi d'abord vous montrer quelques exemples."

Des phrases comme celles-ci sont devenues un savoir-faire valant des dizaines de milliers de dollars. La meme question produisait des reponses dramatiquement differentes de l'IA selon la formulation.

Le prompt engineering fonctionnait reellement.
Une seule ligne de Chain-of-Thought augmentait les scores en mathematiques de 20%.
Une seule phrase attribuant un role changeait la profondeur de l'expertise.
Trois exemples few-shot donnaient un controle total sur le format de sortie.

Ce n'etait pas du battage mediatique. C'etait reel.
Alors pourquoi cela prend-il fin ?

---

### Pourquoi ca fonctionnait : Parce que les modeles etaient assez betes

Regardez pourquoi le prompt engineering fonctionnait a partir des premiers principes. C'est simple.

Les premiers LLM avaient du mal a saisir l'intention de l'utilisateur.
Dites "resumez" et ils reecrivaient.
Dites "comparez" et ils listaient.

Parce que le modele lisait mal l'intention,
la competence de transmettre l'intention avec precision est devenue precieuse.
Le prompt engineering etait essentiellement de l'"interpretation" --
traduire l'intention humaine dans une forme que le LLM pouvait comprendre.

Pour que l'interpretation ait de la valeur, il faut une barriere linguistique.

---

### Ce qui a change : Les modeles sont devenus intelligents

De GPT-3.5 a GPT-4. De Claude 2 a Claude 3.5.
A chaque generation, la capacite des modeles a saisir l'intention s'est amelioree de maniere spectaculaire.

Dites "resumez" et ils resument.
Dites "comparez" et ils comparent.
Meme sans qu'on leur dise de "penser etape par etape", ils decomposent les problemes complexes en etapes par eux-memes.

La barriere linguistique s'est abaissee.
La valeur de l'interpretation a diminue.

Les techniques de prompt qui produisaient des differences spectaculaires en 2023
ne produisent que des differences marginales en 2025.
Quand le modele est assez intelligent, la formulation compte de moins en moins.

Alors qu'est-ce qui compte a la place ?

---

### La fenetre de contexte : Une loi de la physique

Les LLM ont une contrainte physique.

La fenetre de contexte.

Que ce soit 128K tokens ou 1M tokens, elle est finie.
Seules les informations qui tiennent dans cet espace fini influencent le raisonnement.
Les informations en dehors de la fenetre, aussi importantes soient-elles, pourraient tout aussi bien ne pas exister.

C'est independant de la taille du modele.
Meme avec un billion de parametres, la fenetre de contexte est finie.
Meme avec des donnees d'entrainement couvrant tout l'internet, la fenetre de contexte est finie.

Aussi intelligent que soit le modele,
si de mauvaises informations entrent dans le contexte, il produit de mauvaises reponses.
Si des informations non pertinentes remplissent le contexte, il passe a cote de l'essentiel.
Si les informations necessaires manquent du contexte, c'est comme si elles n'existaient pas.

Le prompt engineering etait un probleme de "comment le dire".
Le nouveau jeu est un probleme de "ce qu'on montre".

C'est le context engineering.

---

### Analogie : L'examen a livre ouvert

Voici une analogie pour la difference entre prompt engineering et context engineering.

Le prompt engineering, c'est bien rediger les questions d'examen.
Au lieu de "choisissez la bonne reponse ci-dessous",
ecrivez "derivez etape par etape la reponse qui satisfait toutes les conditions suivantes" --
et l'etudiant donne une meilleure reponse.

Le context engineering, c'est la question de quels livres vous apportez a un examen a livre ouvert.
Peu importe la qualite de la redaction des questions,
si l'etudiant a apporte les mauvais livres, il ne peut pas repondre.
Le nombre de livres que vous pouvez apporter est limite.
Les livres que vous apportez determinent votre note.

Quand le modele etait bete, le format de la question (prompt) comptait.
Quand le modele est intelligent, le materiel de reference (contexte) compte.

---

### L'ere des agents accelere le changement

Ce changement s'accelere avec l'emergence des agents.

Le prompt engineering est ecrit par des humains a chaque fois.
Les humains ecrivent la question, les humains expliquent le contexte, les humains specifient le format.

Les agents sont differents.
Les agents raisonnent par eux-memes, appellent des outils et collaborent avec d'autres agents.
A chaque etape, ils doivent composer le contexte eux-memes.

Un agent a appele une API externe et a recu des donnees.
Ces donnees doivent aller dans le contexte pour le prochain cycle de raisonnement.
Quelles parties entrent et quelles parties sont laissees de cote ?
Quels resultats de raisonnement precedents sont conserves et lesquels sont ecartes ?
Les informations envoyees par un autre agent sont-elles fiables ?

Un humain ne peut pas prendre toutes ces decisions a chaque fois.
Pour que les agents operent de maniere autonome,
la composition du contexte doit etre automatisee.

Le prompt engineering etait une competence humaine.
Le context engineering doit etre une capacite systeme.

---

### Le prompt engineering ne disparait pas

Evitons un malentendu.

Je ne dis pas que le prompt engineering devient insignifiant.
Les system prompts sont toujours importants.
La specification du format de sortie est toujours necessaire.
La declaration de roles et de contraintes est toujours efficace.

Ce qui diminue, c'est la part que detient le prompt engineering.

Si 70% de la qualite de sortie etait determinee par le prompt en 2023,
en 2025, 30% est determine par le prompt et 70% par le contexte.

Le ratio s'est inverse.

Et cette tendance ne s'inversera pas.
Les modeles continueront a devenir plus intelligents,
et plus ils le deviennent, moins la formulation compte
et plus le contexte compte.

---

### Mais le context engineering n'a pas d'infrastructure

Voici le noeud du probleme.

Le prompt engineering avait des outils.
Des templates de prompts, des bibliotheques de prompts, des frameworks de test de prompts.
Tout un ecosysteme pour gerer systematiquement "comment le dire" a ete construit.

Le context engineering n'a pas encore cela.

Regardez comment le contexte est gere en pratique actuellement.

Les tailles de chunks des pipelines RAG sont ajustees a la main.
Les informations de fond sont ecrites dans les system prompts a la main.
Ce qu'il faut stocker dans la memoire d'un agent est concu a la main.
Quels resultats de recherche mettre dans le contexte est decide a la main.

Tout est manuel.

Et la matiere premiere de tout ce travail manuel est le langage naturel.
Des documents en langage naturel sont decoupes en langage naturel et colles dans un contexte en langage naturel.

Le langage naturel a une faible densite d'information.
Pas de sources. Pas de niveaux de confiance. Pas d'horodatages.
Des tokens inutiles sont consommes pour transmettre le meme sens.
Il n'y a aucun moyen d'automatiser le jugement de qualite.

Cela ressemble a l'ere pre-prompt-engineering.
Le prompt engineering etait aussi manuel au debut.
Il reposait sur l'intuition et l'experience individuelles.
Puis des outils et des methodologies sont apparus et il s'est systematise.

Le context engineering en est a ce stade anterieur actuellement.
Le probleme a ete reconnu, mais l'infrastructure n'existe pas.

---

### Ce dont l'infrastructure a besoin

Pour que le context engineering passe du travail manuel a un systeme,
il faut au minimum les elements suivants.

**Compression.** Un moyen de faire tenir plus de sens dans la meme fenetre.
Enlevez la colle grammaticale du langage naturel et ne gardez que le sens,
et la taille effective de la fenetre se multiplie -- sans changer le modele.

**Indexation.** Un moyen de trouver la bonne information avec precision.
Une recherche basee sur la structure semantique, pas sur la similarite d'embeddings.
Une recherche ou chercher "chiffre d'affaires Apple" ne ramene pas "valeurs nutritives de la pomme".

**Validation.** Un moyen de rejeter mecaniquement les informations qui ne respectent pas la specification.
Tout comme un compilateur Go signale les variables inutilisees comme des erreurs,
les affirmations sans sources et les faits sans horodatages devraient etre filtres avant d'entrer dans le contexte.
Les verifications les moins couteuses et les plus deterministes doivent venir en premier.

**Filtrage.** Un moyen de juger la qualite semantique.
Si la validation regarde la forme, le filtrage regarde le contenu.
Pertinence, fiabilite, fraicheur. Cette information est-elle vraiment necessaire pour ce cycle de raisonnement ?

**Coherence.** Un moyen de garantir la coherence interne de l'ensemble d'informations selectionne.
Des informations individuellement bonnes peuvent se contredire quand elles sont combinees.
Si le PDG de 2020 et le PDG de 2024 entrent simultanement dans le contexte,
le LLM est perdu.

**Composition.** Un moyen d'optimiser le placement et la structure dans la fenetre.
La meme information recoit des poids d'attention differents selon l'endroit ou elle est placee.
Au debut ou a la fin ? Comment est-elle regroupee ?

**Accumulation.** Un moyen pour le systeme d'apprendre et de croitre au fil du temps.
Le cache est la reutilisation de resultats individuels.
L'accumulation, c'est apprendre quelles compositions de contexte ont produit de bons resultats,
et faire croitre la base de connaissances elle-meme.

Ces sept elements constituent la pile complete de l'infrastructure de context engineering.

---

### Ce n'est pas une question d'outil particulier

Soyons francs.

Qui construit cette infrastructure est une question ouverte.
Un seul outil pourrait tout resoudre,
ou plusieurs outils pourraient chacun gerer une couche.

Mais le fait que l'infrastructure est necessaire n'est pas une question ouverte.

Que la fenetre de contexte est finie est un fait physique.
Meme si la fenetre grandit de 10x, l'information mondiale grandit plus vite.
Que le langage naturel a une faible densite d'information est un fait structurel.
Que les agents ont besoin d'une gestion automatisee du contexte pour operer de maniere autonome est une necessite logique.

Tout comme le prompt engineering avait besoin d'outils,
le context engineering a besoin d'outils.
Mais cette fois, la nature des outils est differente.

Les outils de prompt engineering etaient plus proches des editeurs de texte.
Les outils de context engineering sont plus proches des compilateurs.

Compresser l'information, l'indexer, la valider, la filtrer,
verifier la coherence, optimiser le placement et accumuler les resultats.
Ce n'est pas de l'edition. C'est de l'ingenierie.

C'est pourquoi on parle de context "engineering".

---

### Resume

Le prompt engineering avait de la valeur quand les modeles etaient betes.
Parce que les modeles ne lisaient pas l'intention, la competence de bien transmettre l'intention comptait.

A mesure que les modeles sont devenus plus intelligents, le jeu a change.
De "comment le dire" a "ce qu'on montre".
Du prompt au contexte.

L'emergence des agents accelere ce changement.
Les humains ne peuvent pas assembler le contexte a chaque fois.
Le systeme doit le faire par lui-meme.

Mais actuellement, le context engineering n'a pas d'infrastructure.
Le langage naturel est decoupe et colle a la main.

L'infrastructure requise comporte sept couches :
compression, indexation, validation, filtrage, coherence, composition, accumulation.

Ce n'est pas l'ere du prompt engineering qui se termine.
C'est l'ere ou le prompt engineering seul suffisait.
