---
title: "Pourquoi les verifications de coherence sont necessaires"
weight: 6
date: 2026-02-26T12:00:08+09:00
lastmod: 2026-02-26T12:00:08+09:00
tags: ["coherence", "contradiction", "consistance"]
summary: "Des informations individuellement correctes peuvent etre collectivement fausses"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Des informations individuellement correctes peuvent etre collectivement fausses.

---

## La verification est passee. Le filtrage est passe.

La verification mecanique a filtre les erreurs de format.
Le filtrage a selectionne selon la pertinence, la fiabilite et la recence.

30 informations subsistent.
Toutes valides, toutes pertinentes, toutes fiables, toutes actuelles.

Mettez-vous ces 30 dans le contexte ?

Non.
Une chose de plus doit etre verifiee.
Ces 30 se contredisent-elles ?

---

## La contradiction n'est pas une propriete de l'information individuelle

Considerez ces deux enonces.

- Source : publication IR de Samsung Electronics, octobre 2024. "PDG de Samsung Electronics : Jun Young-hyun."
- Source : publication IR de Samsung Electronics, mars 2024. "PDG de Samsung Electronics : Kyung Kye-hyun."

Individuellement, les deux sont valides.
Le format est correct, la source est presente, le temps est present, et ils sont fiables.
Ils passent la verification. Ils passent le filtrage.

Mais quand les deux entrent dans le meme contexte, il y a un probleme.
Le PDG de Samsung Electronics est-il Jun Young-hyun ou Kyung Kye-hyun ?

Aucun des deux enonces n'est faux.
En mars, Kyung Kye-hyun etait correct. En octobre, Jun Young-hyun est correct.
Individuellement, les deux ont raison.
Mais quand ils coexistent dans le contexte, le LLM est confus.

C'est le probleme de coherence.
Il nait non pas de l'information individuelle mais de l'ensemble des informations.
La verification examine l'information individuelle. Le filtrage examine l'information individuelle.
La coherence examine l'espace entre les informations.

---

## Types de contradiction

Les contradictions dans le contexte se repartissent en plusieurs types.

### Contradiction temporelle

La plus courante.

La meme propriete de la meme entite a change au fil du temps,
et des valeurs de differents moments coexistent dans le contexte.

"PDG de Tesla : Elon Musk" et
"Cours de l'action Tesla : 194 $" sont dans le meme contexte,
mais l'information sur le PDG date de 2024 et le cours de l'action date de juin 2023.
Le LLM peut les traiter comme des informations du meme moment.

Des cas plus subtils apparaissent aussi.
"Taux directeur de la Coree du Sud : 3,50 %" date de janvier 2024, et
"Inflation des prix a la consommation en Coree du Sud : 2,0 %" date d'octobre 2024.
Les deux sont valides et les deux concernent l'economie coreenne,
mais il y a un ecart de 9 mois.
Si cet ecart affecte l'inference depend du contexte.

### Contradiction entre sources

Des sources differentes presentent des valeurs differentes pour le meme fait.

- Source A : "Taille du marche mondial de l'IA en 2024 : 184 milliards de dollars."
- Source B : "Taille du marche mondial de l'IA en 2024 : 214 milliards de dollars."

Aucune ne peut etre definitivement declaree "fausse."
Le perimetre du marche peut differer. Les methodes de mesure peuvent differer.
Mais si les deux sont dans le contexte,
le LLM doit en choisir une, les fusionner, ou etre confus.

### Contradiction inferentielle

Pas de valeurs directement contradictoires,
mais logiquement incompatibles quand elles sont placees ensemble.

"Part de marche de l'entreprise A : 60 %."
"Part de marche de l'entreprise B : 55 %."

Chacune est valide. Mais leur somme fait 115 %.
En ajoutant les concurrents restants, on depasserait 100 %.
L'une d'elles provient d'un moment different, utilise une definition de marche differente, ou est fausse.

Ce type de contradiction ne peut pas etre trouve en examinant les enonces individuellement.
Il faut examiner l'ensemble.

---

## Les LLM ne gerent pas bien les contradictions

En theorie, le LLM devrait pouvoir detecter et resoudre les contradictions.
"Ces deux informations different dans le temps, donc je vais repondre sur la base de la plus recente."

En pratique, ce n'est pas ce qui se passe.

**Les LLM tendent a faire confiance aux informations dans le contexte.**
Le fait de mettre quelque chose dans le contexte est en soi un signal qui dit "referez-vous a ceci."
Quand deux informations contradictoires sont presentes,
le LLM tend a referencer les deux plutot qu'a en ignorer une.
Le resultat est un melange ou une confusion.

**La detection des contradictions necessite du raisonnement.**
Savoir que "PDG : Jun Young-hyun" et "PDG : Kyung Kye-hyun" se contredisent
exige la connaissance prealable qu'il n'y a qu'un seul PDG a un moment donne.
Verifier si la somme des parts de marche depasse 100 % exige de l'arithmetique.
Cela depend de la capacite de raisonnement du LLM.

**La resolution est encore plus difficile.**
Meme si une contradiction est detectee, il faut juger quel cote choisir.
Le plus recent ? La source la plus fiable ? Celui soutenu par le plus de sources ?
Si ce jugement est laisse au LLM, la coherence n'est pas garantie.
Pour la meme contradiction, il choisit A parfois et B d'autres fois.

En conclusion, traiter les contradictions apres qu'elles sont entrees dans le contexte
est couteux et le resultat est incertain.
Les contradictions doivent etre resolues avant d'entrer dans le contexte.

---

## Pourquoi la verification de coherence est difficile en langage naturel

Supposons que vous verifiez la coherence de 30 fragments en langage naturel.

D'abord, il faut determiner s'ils portent sur le meme sujet.
Si "Samsung Electronics", "Samsung Electronics" et "Samsung" font reference a la meme entite.
En langage naturel, c'est incertain.
Si "Samsung" designe Samsung Electronics, Samsung C&T ou Samsung Life necessite de lire le contexte.

Ensuite, il faut determiner s'ils decrivent la meme propriete.
Si "chiffre d'affaires", "revenu", "chiffre d'affaires total" et "revenu brut" sont la meme chose.
Si "benefice d'exploitation", "resultat operationnel" et "marge operationnelle" sont identiques ou differents.

Ensuite, il faut extraire les references temporelles.
Quand est "le trimestre dernier" ? Quand est "recemment" ? Quand est "cette annee" ?

Ce n'est qu'apres tout cela qu'on peut enfin comparer si deux enonces se contredisent.

Avec 30 enonces, il y a 435 paires de comparaison.
Chaque paire doit passer par le processus ci-dessus.
Tout est raisonnement LLM.
Tout est couteux.
Tout est probabiliste.

---

## Verification de coherence dans les representations structurees

Dans une representation structuree, la situation est differente.

**L'identification d'entite est deterministe.**
L'entite "Samsung Electronics" a un identifiant unique.
"Samsung Electronics" pointe vers le meme identifiant.
Pas besoin de raisonnement pour determiner l'identite.

**Les proprietes sont explicites.**
"Chiffre d'affaires" est une propriete typee.
"Marge operationnelle" est une propriete differente.
Si deux proprietes sont identiques ou differentes est confirme par comparaison de champs.

**Le temps est un champ.**
Il y a une valeur comme "2024-Q3."
Pas besoin d'interpreter "le trimestre dernier."
Si deux enonces partagent le meme temps est une comparaison de valeur.

Quand ces trois choses sont deterministes, les patterns de detection de contradiction deviennent mecanisables.

Meme entite + meme propriete + meme temps + valeur differente = contradiction.
Meme entite + meme propriete + temps different + valeur differente = changement. Pas une contradiction.
Entite differente + meme propriete + meme temps + somme des valeurs > 100 % = contradiction inferentielle.

Pas besoin de LLM pour cela.
Comparaison de champs et arithmetique.

Toutes les contradictions ne peuvent pas etre attrapees.
Si "le marche de l'IA est en croissance" et "l'investissement dans l'IA est en baisse" se contredisent
necessite toujours un jugement semantique.
Mais si les contradictions mecaniquement detectables sont attrapees d'abord,
seuls les cas necessitant un jugement semantique restent.
Encore une fois, le bon marche d'abord.

---

## Strategies de resolution pour les verifications de coherence

Apres avoir detecte une contradiction, il faut la resoudre.

Les strategies de resolution varient selon le contexte, mais dans une representation structuree elles peuvent etre declarees comme politique.

**Le plus recent d'abord.** Quand la meme propriete de la meme entite entre en conflit, prendre celle avec l'horodatage le plus recent. Adapte aux valeurs changeantes comme le PDG, le cours de l'action, la population.

**La plus haute confiance d'abord.** Prendre celle avec la confiance la plus elevee. Ou si une hierarchie de sources est definie, prendre la source de rang superieur. Source primaire > source secondaire > source non officielle.

**Presenter les deux.** Ne pas resoudre la contradiction. Mettre les deux dans le contexte, mais marquer la contradiction explicitement. "La source A dit 184 milliards de dollars ; la source B dit 214 milliards de dollars. Probablement du a des differences de definition." Laisser le LLM raisonner en connaissance de la contradiction.

**Exclure les deux.** Si la contradiction ne peut pas etre resolue, exclure les deux cotes. Pas d'information vaut mieux qu'une mauvaise information.

Dans un pipeline en langage naturel, ces strategies sont ecrites en langage naturel dans le prompt.
"Veuillez privilegier les informations les plus recentes."
Que le LLM suive cela de maniere constante est, encore une fois, une question de probabilite.

Dans une representation structuree, ces strategies sont declarees comme politique.
"En cas de conflit meme-entite + meme-propriete : horodatage le plus recent d'abord. Si les horodatages sont egaux : confiance la plus elevee d'abord. Si la confiance est egale : presenter les deux."
La machine l'execute. Pas de probabilite.

---

## Position dans le pipeline

La verification de coherence vient apres le filtrage.

Verification -> Filtrage -> Coherence.

Pourquoi cet ordre ?

La verification filtre les erreurs de format.
Le filtrage supprime les informations inutiles.
La verification de coherence n'a besoin de traiter que ce qui a passe la verification et le filtrage.

La verification de coherence compare des paires.
Pour n enonces, il y a n(n-1)/2 paires.
1 000 donne environ 500 000 paires. 30 donne 435.

Si la verification et le filtrage reduisent 1 000 a 30,
le cout de la verification de coherence passe de 500 000 a 435 -- un millieme.

L'ordre compte.

---

## Resume

Des informations individuellement valides, pertinentes et fiables
peuvent se contredire quand elles sont rassemblees en ensemble.

Il y a trois types de contradiction.
Contradiction temporelle -- des valeurs de differents moments coexistent.
Contradiction entre sources -- des sources differentes presentent des valeurs differentes.
Contradiction inferentielle -- individuellement valides, mais logiquement incompatibles quand elles sont combinees.

Les LLM ne gerent pas bien les contradictions.
Ils tendent a faire confiance aux informations dans le contexte,
la detection des contradictions necessite du raisonnement,
et la coherence de la resolution n'est pas garantie.

En langage naturel, la verification de coherence est du raisonnement LLM de bout en bout.
Identite d'entite, identite de propriete, extraction temporelle, comparaison de valeurs -- tout est probabiliste et couteux.

Dans une representation structuree, les identifiants d'entite, les types de propriete et les champs temporels existent,
donc une grande partie de la detection de contradiction se convertit en comparaison de champs et en arithmetique.
Les strategies de resolution sont aussi declarees comme politique.

La verification de coherence vient apres le filtrage dans le pipeline.
La verification et le filtrage doivent reduire l'ensemble pour que le nombre de paires de comparaison diminue.
Le bon marche d'abord, et les verifications collectives viennent apres que les verifications individuelles sont faites.
