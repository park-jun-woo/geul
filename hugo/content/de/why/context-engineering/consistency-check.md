---
title: "Warum Konsistenzpruefungen notwendig sind"
weight: 6
date: 2026-02-26T12:00:08+09:00
lastmod: 2026-02-26T12:00:08+09:00
tags: ["Konsistenz", "Widerspruch", "Kohaerenz"]
summary: "Einzeln korrekte Informationen koennen gemeinsam falsch sein"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Einzeln korrekte Informationen koennen gemeinsam falsch sein.

---

## Verifikation bestanden. Filterung bestanden.

Mechanische Verifikation hat Formatfehler herausgefiltert.
Filterung hat nach Relevanz, Vertrauenswuerdigkeit und Aktualitaet ausgewaehlt.

30 Informationen bleiben uebrig.
Alle gueltig, alle relevant, alle vertrauenswuerdig, alle aktuell.

Gibt man diese 30 in den Kontext?

Nein.
Eine Sache muss noch geprueft werden.
Widersprechen sich diese 30 gegenseitig?

---

## Widerspruch ist keine Eigenschaft einzelner Informationen

Betrachten Sie diese zwei Aussagen.

- Quelle: Samsung Electronics IR-Offenlegung, Oktober 2024. "Samsung Electronics CEO: Jun Young-hyun."
- Quelle: Samsung Electronics IR-Offenlegung, Maerz 2024. "Samsung Electronics CEO: Kyung Kye-hyun."

Einzeln betrachtet sind beide gueltig.
Das Format ist korrekt, die Quelle ist vorhanden, die Zeit ist vorhanden, und sie sind vertrauenswuerdig.
Sie bestehen die Verifikation. Sie bestehen die Filterung.

Aber wenn beide in denselben Kontext gelangen, gibt es ein Problem.
Ist Samsung Electronics' CEO Jun Young-hyun oder Kyung Kye-hyun?

Keine der beiden Aussagen ist falsch.
Im Maerz war Kyung Kye-hyun korrekt. Im Oktober ist Jun Young-hyun korrekt.
Einzeln sind beide richtig.
Aber wenn sie im Kontext koexistieren, wird das LLM verwirrt.

Das ist das Konsistenzproblem.
Es entsteht nicht aus einzelnen Informationen, sondern aus der Menge der Informationen.
Verifikation untersucht einzelne Informationen. Filterung untersucht einzelne Informationen.
Konsistenz untersucht den Raum zwischen Informationen.

---

## Arten von Widerspruechen

Widersprueche im Kontext lassen sich in mehrere Typen einteilen.

### Zeitlicher Widerspruch

Der haeufigste.

Dieselbe Eigenschaft derselben Entitaet hat sich im Laufe der Zeit geaendert,
und Werte aus verschiedenen Zeitpunkten koexistieren im Kontext.

"Tesla CEO: Elon Musk" und
"Tesla-Aktienkurs: 194 $" stehen im selben Kontext,
aber die CEO-Information ist von 2024 und der Aktienkurs von Juni 2023.
Das LLM koennte sie als Informationen vom selben Zeitpunkt behandeln.

Subtilere Faelle treten ebenfalls auf.
"Suedkoreas Leitzins: 3,50 %" ist von Januar 2024, und
"Suedkoreas Verbraucherpreisinflation: 2,0 %" ist von Oktober 2024.
Beide sind gueltig und beide betreffen die koreanische Wirtschaft,
aber dazwischen liegen 9 Monate.
Ob diese Luecke die Inferenz beeinflusst, haengt vom Kontext ab.

### Quellen-Widerspruch

Verschiedene Quellen praesentieren verschiedene Werte fuer denselben Sachverhalt.

- Quelle A: "2024 globale KI-Marktgroesse: 184 Milliarden Dollar."
- Quelle B: "2024 globale KI-Marktgroesse: 214 Milliarden Dollar."

Keine kann eindeutig als "falsch" deklariert werden.
Die Marktdefinition kann sich unterscheiden. Die Messmethoden koennen sich unterscheiden.
Aber wenn beide im Kontext stehen,
muss das LLM eine waehlen, beide vermischen oder verwirrt werden.

### Inferenzieller Widerspruch

Keine direkt widerspruechlichen Werte,
aber logisch unvereinbar, wenn sie nebeneinander stehen.

"Unternehmen A Marktanteil: 60 %."
"Unternehmen B Marktanteil: 55 %."

Einzeln gueltig. Aber zusammen ergeben sie 115 %.
Addiert man die uebrigen Wettbewerber, uebersteigt man 100 %.
Eine der Angaben stammt aus einer anderen Zeit, verwendet eine andere Marktdefinition oder ist falsch.

Diese Art von Widerspruch laesst sich nicht finden, indem man einzelne Aussagen betrachtet.
Man muss die Menge untersuchen.

---

## LLMs koennen schlecht mit Widerspruechen umgehen

Theoretisch sollte das LLM in der Lage sein, Widersprueche zu erkennen und aufzuloesen.
"Diese beiden Informationen unterscheiden sich zeitlich, also antworte ich auf Basis der aktuelleren."

In der Praxis passiert das nicht.

**LLMs neigen dazu, Informationen im Kontext zu vertrauen.**
Das Einfuegen in den Kontext ist selbst ein Signal, das sagt "beziehe dich darauf."
Wenn zwei widerspruechliche Informationen vorhanden sind,
neigt das LLM dazu, beide zu referenzieren, statt eine zu ignorieren.
Das Ergebnis ist eine Vermischung oder Verwirrung.

**Widerspruchserkennung erfordert Schlussfolgern.**
Zu wissen, dass "CEO: Jun Young-hyun" und "CEO: Kyung Kye-hyun" sich widersprechen,
erfordert das Hintergrundwissen, dass es zu einem bestimmten Zeitpunkt nur einen CEO gibt.
Zu pruefen, ob Marktanteile in der Summe 100 % uebersteigen, erfordert Arithmetik.
Das haengt von der Schlussfolgerfaehigkeit des LLM ab.

**Aufloesung ist noch schwieriger.**
Selbst wenn ein Widerspruch erkannt wird, muss beurteilt werden, welche Seite man waehlt.
Die aktuellere? Die vertrauenswuerdigere Quelle? Die, die von mehr Quellen gestuetzt wird?
Wenn diese Beurteilung dem LLM ueberlassen wird, ist Konsistenz nicht garantiert.
Fuer denselben Widerspruch waehlt es mal A und mal B.

Fazit: Widersprueche zu behandeln, nachdem sie in den Kontext gelangt sind,
ist teuer und das Ergebnis ist unsicher.
Widersprueche muessen vor dem Eintritt in den Kontext aufgeloest werden.

---

## Warum Konsistenzpruefung in natuerlicher Sprache schwer ist

Nehmen wir an, man prueft die Konsistenz von 30 natuerlichsprachlichen Chunks.

Zunaechst muss man feststellen, ob sie dasselbe Thema behandeln.
Ob "Samsung Electronics", "Samsung Electronics" und "Samsung" dieselbe Entitaet bezeichnen.
In natuerlicher Sprache ist das unsicher.
Ob "Samsung" Samsung Electronics, Samsung C&T oder Samsung Life bedeutet, erfordert das Lesen des Kontexts.

Dann muss man feststellen, ob sie dieselbe Eigenschaft beschreiben.
Ob "Umsatz", "Umsatz", "Gesamtumsatz" und "Bruttoumsatz" dasselbe sind.
Ob "operativer Gewinn", "operativer Gewinn" und "operative Marge" gleich oder verschieden sind.

Dann muss man die Zeitangaben extrahieren.
Wann ist "letztes Quartal"? Wann ist "kuerzlich"? Wann ist "dieses Jahr"?

Erst nach all dem kann man schliesslich vergleichen, ob zwei Aussagen sich widersprechen.

Bei 30 Aussagen gibt es 435 Vergleichspaare.
Jedes Paar muss den obigen Prozess durchlaufen.
Alles LLM-Schlussfolgern.
Alles teuer.
Alles probabilistisch.

---

## Konsistenzpruefung in strukturierten Darstellungen

In einer strukturierten Darstellung ist die Situation anders.

**Entitaetsidentifikation ist deterministisch.**
Die Entitaet "Samsung Electronics" hat einen eindeutigen Bezeichner.
"Samsung Electronics" zeigt auf denselben Bezeichner.
Kein Schlussfolgern noetig, um die Identitaet festzustellen.

**Eigenschaften sind explizit.**
"Umsatz" ist eine typisierte Eigenschaft.
"Operative Marge" ist eine andere Eigenschaft.
Ob zwei Eigenschaften gleich oder verschieden sind, wird durch Feldvergleich bestaetigt.

**Zeit ist ein Feld.**
Es gibt einen Wert wie "2024-Q3."
Kein Interpretieren von "letztes Quartal" noetig.
Ob zwei Aussagen dieselbe Zeit teilen, ist ein Wertvergleich.

Wenn diese drei Dinge deterministisch sind, werden Widerspruchserkennungsmuster mechanisierbar.

Gleiche Entitaet + gleiche Eigenschaft + gleiche Zeit + verschiedener Wert = Widerspruch.
Gleiche Entitaet + gleiche Eigenschaft + verschiedene Zeit + verschiedener Wert = Aenderung. Kein Widerspruch.
Verschiedene Entitaet + gleiche Eigenschaft + gleiche Zeit + Summe der Werte > 100 % = inferenzieller Widerspruch.

Kein LLM dafuer noetig.
Feldvergleich und Arithmetik.

Nicht alle Widersprueche lassen sich erkennen.
Ob "der KI-Markt waechst" und "KI-Investitionen sinken" sich widersprechen,
erfordert nach wie vor semantische Beurteilung.
Aber wenn mechanisch erkennbare Widersprueche zuerst gefangen werden,
bleiben nur Faelle uebrig, die semantische Beurteilung erfordern.
Wieder: Guenstiges kommt zuerst.

---

## Aufloesungsstrategien fuer Konsistenzpruefungen

Nach der Erkennung eines Widerspruchs muss er aufgeloest werden.

Aufloesungsstrategien variieren je nach Kontext, aber in einer strukturierten Darstellung koennen sie als Politik deklariert werden.

**Aktuellstes zuerst.** Wenn dieselbe Eigenschaft derselben Entitaet in Konflikt steht, die mit dem aktuelleren Zeitstempel waehlen. Geeignet fuer sich aendernde Werte wie CEO, Aktienkurs, Bevoelkerung.

**Hoechstes Vertrauen zuerst.** Die mit hoeherer Konfidenz waehlen. Oder wenn eine Quellenhierarchie definiert ist, die hoeherrangige Quelle waehlen. Primaerquelle > Sekundaerquelle > inoffizielle Quelle.

**Beide praesentieren.** Den Widerspruch nicht aufloesen. Beide in den Kontext geben, aber den Widerspruch explizit kennzeichnen. "Quelle A sagt 184 Milliarden Dollar; Quelle B sagt 214 Milliarden Dollar. Vermutlich aufgrund von Definitionsunterschieden." Das LLM mit dem Bewusstsein des Widerspruchs schlussfolgern lassen.

**Beide ausschliessen.** Wenn der Widerspruch nicht aufgeloest werden kann, beide Seiten ausschliessen. Keine Information ist besser als falsche Information.

In einer natuerlichsprachlichen Pipeline werden diese Strategien als natuerliche Sprache im Prompt formuliert.
"Bitte priorisieren Sie die aktuellste Information."
Ob das LLM dies konsistent befolgt, ist wiederum eine Frage der Wahrscheinlichkeit.

In einer strukturierten Darstellung werden diese Strategien als Politik deklariert.
"Bei Konflikt gleiche-Entitaet + gleiche-Eigenschaft: aktuellster Zeitstempel zuerst. Bei gleichem Zeitstempel: hoechste Konfidenz zuerst. Bei gleicher Konfidenz: beide praesentieren."
Die Maschine fuehrt es aus. Keine Wahrscheinlichkeit.

---

## Position in der Pipeline

Konsistenzpruefung kommt nach der Filterung.

Verifikation -> Filterung -> Konsistenz.

Warum diese Reihenfolge?

Verifikation filtert Formatfehler heraus.
Filterung entfernt unnoetige Informationen.
Konsistenzpruefung muss nur verarbeiten, was Verifikation und Filterung bestanden hat.

Konsistenzpruefung vergleicht Paare.
Bei n Aussagen gibt es n(n-1)/2 Paare.
1.000 ergibt rund 500.000 Paare. 30 ergibt 435.

Wenn Verifikation und Filterung 1.000 auf 30 reduzieren,
sinken die Kosten der Konsistenzpruefung von 500.000 auf 435 -- ein Tausendstel.

Reihenfolge ist wichtig.

---

## Zusammenfassung

Informationen, die einzeln gueltig, relevant und vertrauenswuerdig sind,
koennen sich als Menge widersprechen.

Es gibt drei Arten von Widerspruechen.
Zeitlicher Widerspruch -- Werte aus verschiedenen Zeitpunkten koexistieren.
Quellen-Widerspruch -- verschiedene Quellen praesentieren verschiedene Werte.
Inferenzieller Widerspruch -- einzeln gueltig, aber logisch unvereinbar in Kombination.

LLMs koennen schlecht mit Widerspruechen umgehen.
Sie neigen dazu, Informationen im Kontext zu vertrauen,
Widerspruchserkennung erfordert Schlussfolgern,
und Konsistenz der Aufloesung ist nicht garantiert.

In natuerlicher Sprache ist Konsistenzpruefung durchweg LLM-Schlussfolgern.
Entitaetsidentitaet, Eigenschaftsidentitaet, Zeitextraktion, Wertvergleich -- alles probabilistisch und teuer.

In einer strukturierten Darstellung existieren Entitaetsbezeichner, Eigenschaftstypen und Zeitfelder,
sodass sich ein Grossteil der Widerspruchserkennung in Feldvergleich und Arithmetik umwandelt.
Aufloesungsstrategien werden ebenfalls als Politik deklariert.

Konsistenzpruefung kommt in der Pipeline nach der Filterung.
Verifikation und Filterung muessen die Menge reduzieren, damit die Zahl der Vergleichspaare sinkt.
Guenstiges kommt zuerst, und kollektive Pruefungen kommen nach den individuellen.
