---
title: "Pourquoi la verification mecanique est necessaire"
weight: 4
date: 2026-02-26T12:00:10+09:00
lastmod: 2026-02-26T12:00:10+09:00
tags: ["verification", "specification", "compilateur"]
summary: "Le langage naturel n'a pas de concept de phrase invalide"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Le langage naturel n'a pas de concept de "phrase invalide."

---

## Personne n'inspecte ce qui entre dans le contexte

Regardez comment l'information entre dans le contexte des pipelines LLM actuels.

RAG retourne des fragments.
Un agent recoit des reponses d'API.
Les conversations precedentes s'accumulent dans l'historique.
Un utilisateur televerse un document.

Tout cela entre dans la fenetre de contexte.
Sans inspection.

Pourquoi n'y a-t-il pas d'inspection ?
Parce que le langage naturel n'a pas de concept d'"invalide."

---

## Le langage naturel accepte toute chaine de caracteres

En programmation, il existe les erreurs de syntaxe.

```python
def calculate(x, y
    return x + y
```

La parenthese n'est pas fermee. Le code est rejete avant l'execution.
On peut definitivement declarer "ceci n'est pas du code valide" avant qu'il ne soit execute, avant meme qu'il ne soit lu.

Le langage naturel n'a rien de tel.

"Il est alle a la banque."
Grammaticalement parfait.
On ne peut pas savoir qui y est alle, quelle banque, ni pourquoi,
mais rien ne viole les regles grammaticales du langage naturel.

"Rapport des ventes du 45e jour du 13e mois 2024."
Il n'y a pas de 13e mois ni de 45e jour.
Pourtant rien ne viole les regles grammaticales du langage naturel.
C'est une phrase grammaticalement valide.

"Source : inconnue. Confiance : inconnue. Date : inconnue. La capitalisation boursiere de Samsung Electronics est de 1 200 000 milliards de wons."
La source est inconnue, la confiance est inconnue, la date de reference est inconnue.
Pourtant rien ne viole les regles grammaticales du langage naturel.

Le langage naturel accepte tout.
Une phrase invalide en langage naturel n'existe structurellement pas.
Par consequent, il n'y a pas de critere mecanique pour "rejeter" une information exprimee en langage naturel.

---

## Ce qu'il faut pour la verification mecanique

Regardez le compilateur Go.

Go refuse de compiler s'il y a un import inutilise.
Meme si le code fonctionne parfaitement.
Meme si la logique est sans defaut.
Il refuse uniquement parce qu'une ligne d'import est inutilisee.

C'est la verification mecanique.

La verification mecanique a trois caracteristiques.

**Elle est deterministe.** Le resultat est oui ou non. Pas une probabilite. Il n'y a pas de "ca devrait aller." Valide ou invalide.

**Elle est bon marche.** Pas besoin d'appel au LLM. Comparaison de chaines, verification d'existence de champ, verification de plage de valeurs. Operations CPU a l'echelle de la nanoseconde.

**Elle ne lit pas le sens.** Elle ne juge pas si le contenu est vrai ou faux. Elle verifie uniquement si le format est conforme a la specification. Elle ne sait pas si "la capitalisation boursiere de Samsung Electronics est de 1 200 000 milliards de wons" est vrai. Mais elle sait si le champ source est vide.

Pour que ces trois choses soient possibles, il y a un prerequis.
L'information doit avoir une specification.

S'il y a une specification, les violations sont definies.
Si les violations sont definies, le rejet est possible.
Si le rejet est possible, la verification existe.

Le langage naturel n'a pas de specification, donc il n'y a pas de violations.
Pas de violations signifie pas de rejet.
Pas de rejet signifie pas de verification.

---

## Pourquoi la verification pre-contexte est necessaire

La fenetre de contexte est finie.

Que ce soit 128K tokens ou 1M tokens, elle est finie.
La qualite de l'information entrant dans un espace fini determine la qualite de la sortie.

Pourtant dans les pipelines actuels,
le jugement de qualite n'intervient qu'apres que l'information est entree dans le contexte.
On attend du LLM qu'il la lise, la juge, et conclue de lui-meme que "cette information est peu fiable."

C'est faux pour trois raisons.

**C'est couteux.** On utilise les couts d'inference du LLM pour faire de la verification de format. On execute un modele a des milliards de parametres pour filtrer des fragments sans source. On utilise du raisonnement probabiliste pour une tache qui exige de verifier un seul champ.

**C'est peu fiable.** Il n'y a aucune garantie que le LLM ignorera toujours une information sans source. En fait, une fois que quelque chose est dans le contexte, le LLM est plus susceptible de l'utiliser. Attendre du modele qu'il ignore quelque chose qu'on a mis dans le contexte est une contradiction.

**C'est trop tard.** L'espace de la fenetre est deja consomme. Si 5 fragments sans source occupent 200 tokens chacun, 1 000 tokens sont gaspilles. Meme s'ils sont filtres ensuite, cet espace est deja depense.

La verification mecanique vient avant tout cela.
Avant d'entrer dans le contexte.
Avant que le LLM ne lise.
Avant que la fenetre ne soit consommee.

---

## Ce qui est verifie

La verification mecanique ne verifie pas la veracite du contenu mais la conformite a une specification de format.

Concretement, ces choses :

**Completude structurelle.** Les champs obligatoires existent-ils ? L'arete a-t-elle un sujet et un objet ? Manque-t-il quelque chose ?

**Validite des identifiants.** Le noeud reference existe-t-il ? Ce qui est ecrit "Samsung Electronics" pointe-t-il reellement vers une entite definie ? La reference est-elle pendante ?

**Conformite de type.** Y a-t-il une date dans le champ date ? Y a-t-il un nombre dans le champ nombre ? "Le 45e jour du 13e mois 2024" est attrape ici.

**Presence des metadonnees.** Y a-t-il un champ source ? Y a-t-il un champ temporel ? La confiance est-elle specifiee ? Sinon, rejeter, marquer comme absent, ou assigner une valeur par defaut.

**Integrite referentielle.** Le noeud pointe par l'arete existe-t-il reellement ? Fait-elle reference a un noeud supprime ?

Ces verifications ont un point commun.
Toutes peuvent etre effectuees sans lire le contenu.
On ne sait pas si "la capitalisation boursiere de Samsung Electronics est de 1 200 000 milliards de wons" est vrai.
Mais on sait si une source est specifiee pour cet enonce.
On sait si un temps est enregistre pour cet enonce.
On sait si le format de cet enonce est conforme a la specification.

---

## Le bon marche d'abord

Dans un pipeline de context engineering, les inspections ont un ordre.

**Verification mecanique** : conformite a la specification. Cout quasi nul. Deterministe.
**Filtrage semantique** : jugement de pertinence, fiabilite, utilite. Cout eleve. Probabiliste.
**Verification de coherence** : contradictions entre les informations selectionnees. Cout encore plus eleve. Necessite du raisonnement.

Si on les ordonne du moins cher au plus cher,
les verifications couteuses ont moins a traiter.

Si la verification mecanique filtre 30% des enonces sans source,
le filtrage semantique n'a besoin de traiter que 70%.
Si le filtrage semantique supprime les elements non pertinents,
la verification de coherence traite un ensemble encore plus petit.

C'est le meme principe que l'optimisation de requetes en base de donnees.
Appliquer les conditions filtrables par index dans la clause WHERE en premier.
Les conditions de scan complet viennent apres.
Si le bon marche vient d'abord, la charge sur la partie couteuse diminue.

A l'inverse,
si on execute la verification couteuse d'abord et la verification bon marche apres,
on decouvre les erreurs de format seulement apres avoir deja depense le cout.
On analyse le sens d'un enonce qui reference un noeud inexistant,
pour decouvrir ensuite que la reference est invalide.

---

## Cet ordre est impossible dans un pipeline en langage naturel

Le langage naturel n'a pas de specification, donc la verification mecanique est impossible.
Puisque la verification mecanique est impossible, la verification la moins chere n'existe pas.

Par consequent, chaque verification est une verification semantique.
Chaque verification necessite un LLM.
Chaque verification est couteuse.

"Ce fragment a-t-il une source ?" -- Le LLM doit le lire.
"La reference temporelle de ce fragment est-elle appropriee ?" -- Le LLM doit le lire.
"Le format de ce fragment est-il correct ?" -- Le langage naturel n'a pas de format, donc la question elle-meme ne tient pas.

C'est la realite du context engineering actuel.
Meme la verification la plus simple est effectuee avec l'outil le plus couteux.
Une tache qui pourrait se terminer par une comparaison de chaines est traitee par un moteur d'inference.

---

## Prerequis pour la verification

Pour que la verification mecanique existe, trois choses sont necessaires.

**Une specification.** Le format que l'information doit suivre doit etre defini. Quels champs sont obligatoires, quelles valeurs sont autorisees, quelles references sont valides. Sans specification, les violations ne peuvent pas etre definies.

**Une formalisation.** L'information doit etre exprimee dans le format exige par la specification. Pas sous forme de phrases en langage naturel, mais encodee dans la structure que la specification impose. Une information non formalisee ne peut pas etre inspectee.

**Le pouvoir de rejeter.** Il doit etre possible de reellement rejeter une information non conforme. Si on inspecte mais qu'on laisse toujours passer, ce n'est pas de la verification. L'information invalide doit etre empechee d'entrer dans le contexte.

Ces trois choses sont tenues pour acquises dans les langages de programmation.
Il y a une specification appelee grammaire, un format appele code, et un pouvoir de rejet appele compilateur.

En langage naturel, les trois sont absents.
La grammaire n'est pas une specification de format mais une convention.
Les phrases ne sont pas des formats structures mais du texte libre.
Le concept de "langage naturel invalide" n'existe pas, donc il n'y a rien a rejeter.

Pour introduire la verification mecanique dans le context engineering,
la representation de l'information elle-meme doit changer.

---

## Resume

Dans le pipeline de contexte actuel, l'information entre dans le contexte sans inspection.
Parce que le langage naturel n'a pas de concept de "phrase invalide."

La verification mecanique ne verifie pas la veracite du contenu mais la conformite a une specification de format.
Completude structurelle, validite des identifiants, conformite de type, presence des metadonnees, integrite referentielle.
Deterministe, bon marche, et elle ne lit pas le sens.

Dans le pipeline, les verifications bon marche doivent venir en premier.
Si la verification mecanique filtre les erreurs de format,
les jugements semantiques couteux ont moins a traiter.

Le langage naturel n'a pas de specification, donc cette verification est impossible.
Chaque verification devient une verification semantique, et chaque verification est couteuse.

Pour que la verification mecanique soit possible,
il faut une specification, une formalisation, et le pouvoir de rejeter.
La representation de l'information elle-meme doit changer.
