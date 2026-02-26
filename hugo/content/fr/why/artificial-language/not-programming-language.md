---
title: "Pourquoi les langages de programmation ne suffisent pas"
weight: 10
date: 2026-02-26T12:00:19+09:00
lastmod: 2026-02-26T12:00:19+09:00
tags: ["langage de programmation", "description", "représentation des connaissances"]
summary: "Les langages de programmation décrivent des procédures. Ils ne peuvent pas décrire le monde. JSON fournit une structure mais pas de sens. Même LISP ne fait qu'emprunter la syntaxe."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Les langages de programmation décrivent des procédures. Ils ne peuvent pas décrire le monde.

---

## Les langages de programmation comptent parmi les plus grandes inventions de l'humanité

Les langages de programmation sont non ambigus.
`x = 3 + 4` donne 7, peu importe quand et où on l'exécute.
Il n'y a aucune place pour l'interprétation.

Les langages de programmation sont vérifiables.
Les erreurs de syntaxe sont détectées avant la compilation.
Les erreurs de type sont détectées avant l'exécution.
Quand les tests s'exécutent, le résultat est soit réussite, soit échec.

Les langages de programmation sont Turing-complets.
Ils peuvent exprimer tout ce qui est calculable.
Avec suffisamment de temps et de mémoire, toute procédure peut être décrite.

Tout ce que cette série a identifié comme limites du langage naturel — ambiguïté, impossibilité de vérification, absence de structure — les langages de programmation l'ont résolu.

Alors pourquoi ne pas utiliser un langage de programmation pour représenter le contexte d'une IA ?

Cela ne fonctionne pas.

---

## Les langages de programmation décrivent des procédures

Le code Python suivant est valide.

```python
def calculate_revenue(units_sold, unit_price):
    return units_sold * unit_price
```

Ce code est clair, vérifiable et exécutable.
Mais qu'exprime-t-il ?

« Multiplier le nombre d'unités vendues par le prix unitaire pour obtenir le chiffre d'affaires. »

C'est une procédure. Une méthode. Le COMMENT.
Il décrit ce qu'il faut faire quand une entrée arrive.

Essayons maintenant d'exprimer ceci.

« Le chiffre d'affaires de Samsung Electronics au troisième trimestre 2024 était de 79 000 milliards de wons. »

Ce n'est pas une procédure. C'est un fait. Le QUOI.
Rien n'est exécuté. Cela décrit l'état du monde.

Comment l'exprimer en Python ?

```python
samsung_revenue_2024_q3 = 79_000_000_000_000
```

Un nombre est affecté à une variable.
Ça fonctionne. Mais ce n'est pas une description. C'est du stockage.
Ce code ne sait pas :

- Quel type d'entité est « Samsung Electronics ».
- Ce que signifie « chiffre d'affaires ». Est-ce un indicateur financier ? Une grandeur physique ?
- Si « Q3 2024 » est un temps, une version ou un libellé.
- Quelle est la source du chiffre de 79 000 milliards de wons.
- À quel point cette valeur est certaine.

Le nom de variable `samsung_revenue_2024_q3` permet à un humain de deviner le sens.
Pour la machine, c'est une chaîne de caractères arbitraire.
Renommez-la `xyzzy_42` et le résultat d'exécution sera identique.

Dans les langages de programmation, les noms de variables ne portent pas de sens.
Le sens vit en dehors du code, dans la tête du programmeur.

---

## Plus de sophistication n'y change rien

Et si l'on créait une classe ?

```python
class FinancialReport:
    def __init__(self, company, metric, period, value, currency):
        self.company = company
        self.metric = metric
        self.period = period
        self.value = value
        self.currency = currency

report = FinancialReport("삼성전자", "매출", "2024-Q3", 79_000_000_000_000, "KRW")
```

Mieux. Il y a une structure.
Mais les problèmes demeurent.

`company` est la chaîne « 삼성전자 » (Samsung Electronics).
« Samsung Electronics », « SEC » et « 005930 » désignent la même entreprise.
Le code le sait-il ? Non.
Il ne peut que comparer si les chaînes sont égales ou non.

`metric` est la chaîne « 매출 » (chiffre d'affaires).
« 매출 », « 매출액 » et « revenue » sont-ils la même chose ou des choses différentes ?
Le code ne le sait pas. Les chaînes sont différentes, donc ce sont des choses différentes.

Et si l'on définissait un schéma ?
Gérer la liste des entreprises avec des Enums, gérer la liste des indicateurs.
Bien sûr. Ça fonctionne.

Alors essayons d'exprimer ceci.

« Yi Sun-sin était grand. »

```python
opinion = Opinion("이순신", "was", "위대했다")
```

Qu'est-ce que c'est ?
Une chaîne « 이순신 » (Yi Sun-sin) liée à une chaîne « 위대했다 » (était grand).
Cela n'exprime pas « Yi Sun-sin était grand ».
Cela stocke « 이순신 » et « 위대했다 ».

Le code ne connaît pas le sens de « 위대했다 » (était grand).
Si « 위대했다 » (était grand) et « 훌륭했다 » (était admirable) sont similaires,
si « 비겁했다 » (était lâche) est le contraire —
le code ne peut pas le déterminer.

Les faits structurés comme les données financières sont plus ou moins gérables.
Les évaluations, le contexte, les relations, les descriptions abstraites dépassent la portée expressive des langages de programmation.

---

## Le code ne sait pas ce qu'il fait

```python
def process(data):
    result = []
    for item in data:
        if item["value"] > threshold:
            result.append(transform(item))
    return result
```

Ce code s'exécute parfaitement.
Mais que fait-il ?

Filtre-t-il des données de chiffre d'affaires ?
Trie-t-il des dossiers de patients ?
Nettoie-t-il des données de capteurs ?

Le code lui-même ne le sait pas.
`data`, `value`, `threshold`, `transform` — tous des noms abstraits.
Que ce code appartienne à un système financier ou médical
dépend du contexte extérieur au code.

On peut écrire des commentaires.
Mais les commentaires sont en langage naturel. Les machines ne les comprennent pas.
Si un commentaire contredit le code, le compilateur ne s'en aperçoit pas.
Les commentaires sont pour les humains, pas pour les machines.

Quand une IA reçoit du code en tant que contexte, ce problème se manifeste directement.
Comme le code n'a pas d'identité propre,
l'IA doit reconstruire cette identité par inférence à chaque fois.
Comme c'est de l'inférence, cela coûte du calcul et peut se tromper.

---

## La raison fondamentale

Que les langages de programmation ne puissent pas décrire le monde n'est pas un défaut de conception.
L'objectif est différent.

L'objectif d'un langage de programmation est d'instruire une machine sur des procédures.
« Quand cette entrée arrive, effectue cette opération. »
La sémantique d'un langage de programmation est la sémantique de l'exécution.
Chaque construction est interprétée comme « que fait la machine ».

`x = 3` est l'instruction « stocker 3 dans l'emplacement mémoire nommé x ».
`if x > 0` est l'instruction « si x est supérieur à 0, exécuter le bloc suivant ».
`return x` est l'instruction « renvoyer la valeur de x à l'appelant ».

Que des verbes. Que des actions. Que des procédures.

« Samsung Electronics est une entreprise coréenne » n'est pas un verbe.
Pas une action. Pas une procédure.
C'est une description de l'état du monde.

Les langages de programmation n'ont pas de place pour cela.
On peut le stocker dans une variable, mais c'est du stockage, pas de la description.
Le sens de la valeur stockée n'est pas du ressort du code.

---

## Et JSON, YAML, XML ?

Si pas les langages de programmation, alors les formats de données ?

```json
{
  "company": "삼성전자",
  "metric": "매출",
  "period": "2024-Q3",
  "value": 79000000000000,
  "currency": "KRW"
}
```

Il y a une structure. Les champs sont explicites.
Mais il n'y a pas de sens.

Si « company » signifie une entreprise, JSON ne le sait pas.
Si « 삼성전자 » est identique à « Samsung Electronics » ailleurs, JSON ne le sait pas.
Si cet objet JSON et celui-là décrivent la même entité, JSON ne le sait pas.

JSON fournit une structure mais pas de sens.
Ce sont des paires clé-valeur, pas entité-relation-attribut.

Définir des schémas améliore les choses.
JSON Schema, Protocol Buffers, GraphQL.
Les types de champs sont définis, le caractère obligatoire est défini, les références sont définies.

Mais ce sont toutes des structures conçues pour des systèmes spécifiques.
Ce n'est pas de la représentation universelle des connaissances.
Un schéma de données financières ne peut pas exprimer l'évaluation d'un personnage historique.
Un schéma de données médicales ne peut pas exprimer les relations concurrentielles entre entreprises.

Un schéma distinct pour chaque domaine.
Un outil distinct pour chaque schéma.
Aucune interopérabilité entre les schémas.

Cette limite est examinée plus en détail dans [Pourquoi MD/JSON/XML ne conviennent pas](/fr/why/not-md-json-xml/).

---

## Et LISP ?

Certains lecteurs ont sans doute pensé à un contre-exemple.

LISP.

```lisp
(is 삼성전자 (company korea))
(revenue 삼성전자 2024-Q3 79000000000000)
(great 이순신)
```

Les S-expressions sont des structures arborescentes,
et le code est données, les données sont code.
Homoïconicité (homoiconicity).

En fait, l'IA primitive était entièrement fondée sur LISP.
SHRDLU, CYC, systèmes experts.
Les connaissances étaient représentées en LISP, et les moteurs d'inférence tournaient dessus.
On dirait une réfutation historique de « les langages de programmation ne peuvent pas décrire le monde ».

Mais le contre-exemple échoue pour trois raisons.

### Ce que LISP sait vs. ce que le programmeur a décidé

Dans `(is 삼성전자 company)`, LISP ne sait pas
que `is` signifie la relation « est un ».
C'est le programmeur qui l'a décidé.

Remplacez `is` par `zzz` et LISP s'en moque.
`(zzz 삼성전자 company)` est une expression parfaitement valide pour LISP.

LISP fournit une structure. Un arbre appelé S-expression.
Mais le sens contenu dans cette structure a été attribué par le programmeur, pas par le langage.
C'est fondamentalement la même chose que JSON ne connaissant pas le sens de ses clés.

Fournir une structure et intégrer du sens sont deux choses différentes.

### Les 30 ans de CYC

La tentative la plus ambitieuse fut CYC.

Démarré en 1984.
Il a tenté de représenter des connaissances générales en LISP.
Des millions de règles ont été saisies manuellement.

Ce que 30 ans ont prouvé, ce n'est pas la faisabilité mais les limites.

Les ontologies devaient être conçues manuellement pour chaque domaine.
L'interopérabilité entre domaines ne fonctionnait pas.
Il ne pouvait pas suivre la flexibilité du langage naturel.
À mesure que l'échelle grandissait, maintenir la cohérence devenait quasi impossible.

Que la représentation des connaissances « peut se faire » en LISP est vrai.
Que cela « fonctionne bien » est ce que 30 ans de résultats réfutent.

### Si on ne va pas utiliser eval, il n'y a aucune raison d'utiliser LISP

Le problème le plus fondamental.

La puissance de LISP est `eval`.
Puisque le code est données, les données peuvent être exécutées.
Métaprogrammation, macros, génération de code à l'exécution.
C'est ce qui fait de LISP, LISP.

Mais que se passe-t-il quand on fait `eval` de `(is 삼성전자 company)` ?

Cela devient un appel de fonction passant `삼성전자` et `company` comme arguments à une fonction nommée `is`.
Pas de la description — de l'exécution.

Pour l'utiliser comme représentation des connaissances, il ne faut pas évaluer.
Si on n'évalue pas, on n'utilise pas la sémantique de LISP.
On ne fait qu'emprunter la syntaxe des S-expressions.

Ce n'est pas « décrire le monde en LISP ».
C'est « stocker des données avec la notation parenthésée de LISP ».

La sémantique de LISP en tant que langage de programmation — la sémantique de l'exécution —
reste conçue pour décrire des procédures.
Emprunter la syntaxe ne change pas la sémantique.

---

## Ce dont un langage pour décrire le monde a besoin

Les langages de programmation décrivent des procédures.
Les formats de données fournissent une structure mais pas de sens.
Même LISP ne fait qu'emprunter la syntaxe sans la sémantique de la description.

De quoi un langage pour décrire le monde a-t-il besoin ?

**Identité des entités.** « Samsung Electronics » doit avoir un identifiant unique. La machine doit savoir que c'est la même chose que « 삼성전자 ». Pas une comparaison de chaînes, mais une équivalence d'identité.

**Expression des relations.** Dans « Samsung Electronics est une entreprise coréenne », il doit être possible d'exprimer la relation « entreprise coréenne ». Pas une affectation de variable, mais une description de relations.

**Descriptions auto-descriptives.** Ce dont la description parle, qui l'a formulée, à quelle date, et à quel degré de certitude — tout doit être inclus dans la description elle-même. À l'intérieur du code, pas à l'extérieur.

**Indépendance du domaine.** Données financières, faits historiques, évaluations subjectives, relations abstraites — tout doit pouvoir s'exprimer dans le même format. Pas un schéma distinct pour chaque domaine, mais une structure universelle.

Les langages de programmation ne possèdent aucune de ces quatre propriétés.
Parce que les langages de programmation n'ont pas été conçus pour cela.
Ils ont été conçus pour décrire des procédures.

Le langage naturel peut faire ces quatre choses. De manière ambiguë.
Ce qu'il faut, c'est la combinaison de la portée expressive du langage naturel et de la précision des langages de programmation.

---

## Résumé

Les langages de programmation sont non ambigus, vérifiables et Turing-complets.
Mais ils ne peuvent pas décrire le monde.

Les langages de programmation décrivent des procédures.
« Quand cette entrée arrive, fais ceci. » Que des verbes, que des actions.
« Samsung Electronics est une entreprise coréenne » n'est pas une action.
Les langages de programmation n'ont pas de place pour cela.

Le code ne connaît pas sa propre identité.
À quel domaine il appartient, quel objectif il remplit —
rien de tout cela n'est enregistré dans le code.

Les formats de données comme JSON et YAML fournissent une structure mais pas de sens.
LISP peut emprunter la syntaxe, mais n'a pas de sémantique de description.
CYC a consacré 30 ans à la représentation des connaissances fondée sur LISP, et ce qu'il a prouvé, c'est la limite.

Décrire le monde nécessite l'identité des entités, l'expression des relations, des descriptions auto-descriptives et l'indépendance du domaine.
Les langages de programmation n'ont pas été conçus pour cela.
Le langage naturel en est capable, mais de manière ambiguë.
Ce qu'il faut se trouve quelque part entre les deux.
