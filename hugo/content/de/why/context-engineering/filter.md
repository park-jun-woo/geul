---
title: "Warum Filter notwendig sind"
weight: 5
date: 2026-02-26T12:00:09+09:00
lastmod: 2026-02-26T12:00:09+09:00
tags: ["Filter", "Relevanz", "Vertrauen"]
summary: "Gueltige Informationen sind nicht immer benoetigte Informationen"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Gueltige Informationen sind nicht immer benoetigte Informationen.

---

## Sie haben 1.000 Informationen, die die Verifikation bestanden haben

Nehmen wir an, die mechanische Verifikation hat funktioniert.

Das Format ist korrekt,
erforderliche Felder existieren,
Bezeichner sind gueltig,
Typen sind angemessen,
und die referentielle Integritaet ist gewahrt -- 1.000 Aussagen bleiben uebrig.

Alle sind gueltige Informationen.
Sie entsprechen der Spezifikation. Es gibt keinen Grund, sie abzulehnen.

Aber das Kontextfenster kann nur 300 aufnehmen.

Welche 300 nimmt man?

Das ist das Problem der Filterung.

---

## Verifikation und Filterung stellen unterschiedliche Fragen

Was Verifikation fragt: "Ist diese Information gueltig?"
Was Filterung fragt: "Wird diese Information gerade gebraucht?"

Verifikation betrachtet die Eigenschaften der Information selbst.
Ist das Format korrekt? Sind die Felder vorhanden? Sind die Referenzen gueltig?
Es spielt keine Rolle, wovon die Information handelt oder welchem Zweck sie dient.

Filterung betrachtet die Beziehung zwischen Information und Situation.
Ist sie fuer diese bestimmte Inferenz gerade relevant?
Ist diese Information vertrauenswuerdig?
Ist sie hinreichend aktuell?

Verifikation ist ohne Kontext moeglich. Man braucht nur die Spezifikation.
Filterung ist ohne Kontext unmoeglich. Man muss wissen, "was gerade gebraucht wird."

Verifikation ist deterministisch. Gueltig oder ungueltig.
Filterung ist Beurteilung. Relevanz hat Abstufungen, Vertrauenswuerdigkeit hat Schwellenwerte, Aktualitaet hat Kontext.

Verifikation ist guenstig.
Filterung ist vergleichsweise teuer.

Deshalb kommt Verifikation zuerst und Filterung danach.
Wenn Verifikation zuerst filtert, beurteilt die Filterung eine kleinere Menge.
Die Kosten der teuren Beurteilung sinken.

---

## Drei Dinge, die Filterung beurteilt

Filterung betrachtet hauptsaechlich drei Dinge.

### Relevanz: Wird es fuer diese Inferenz gebraucht?

Der Benutzer hat nach "Samsung Electronics' operativem Gewinn Q3 2024" gefragt.

Unter den gueltigen Aussagen, die die Verifikation bestanden haben:

- Samsung Electronics' operativer Gewinn Q3 2024 betrug 9,18 Billionen Won.
- Samsung Electronics' Umsatz Q3 2024 betrug 79 Billionen Won.
- Samsung Electronics' operativer Gewinn Q3 2023 betrug 2,43 Billionen Won.
- Samsung Electronics' Halbleiter-Investitionsplan belaeuft sich auf 53 Billionen Won (Stand 2025).
- Samsung Electronics' Hauptsitz ist in Suwon.

Alle gueltig. Alle ueber Samsung Electronics.
Gibt man alle in den Kontext?

Der Hauptsitzstandort ist irrelevant.
Der Investitionsplan hat geringe Relevanz.
Der operative Gewinn von 2023 koennte fuer Vergleiche nuetzlich sein.
Umsatz ist eng mit dem operativen Gewinn verknuepft.

In natuerlichsprachlichem RAG wird diese Beurteilung an die Embedding-Aehnlichkeit delegiert.
Sortiert nach Vektorabstand zu "Samsung Electronics operativer Gewinn."
Aber wie bereits eroertert: aehnlich ist nicht relevant.

In einer strukturierten Darstellung hat die Relevanzbeurteilung andere Eingaben.
Auf welche Entitaet zeigt die Aussage? Samsung Electronics.
Welche Eigenschaft? Operativer Gewinn.
Welche Zeit? Q3 2024.

Wenn Entitaet, Eigenschaft und Zeit als Felder existieren,
kann man "gleiche Entitaet, gleiche Eigenschaft, gleiche Zeit" praezise finden.
Und man kann bewusst "gleiche Entitaet, gleiche Eigenschaft, andere Zeit" einschliessen oder ausschliessen.
Feldabgleich, nicht Vektorabstand.

Relevanz ist nach wie vor eine Beurteilung. Nicht deterministisch.
Aber ob die Eingabe fuer diese Beurteilung Vektorabstand oder strukturierte Felder ist, macht einen Unterschied in der Genauigkeit.

### Vertrauenswuerdigkeit: Kann man dieser Information glauben?

Zwei Aussagen existieren zum gleichen Inhalt.

- Quelle: Samsung Electronics IR-Offenlegung. Konfidenz: 1,0. "Operativer Gewinn Q3 2024: 9,18 Billionen Won."
- Quelle: anonymer Blog. Konfidenz: 0,3. "Operativer Gewinn Q3 2024: circa 10 Billionen Won."

Welche kommt in den Kontext?

Offensichtlich die erste.

Aber damit diese Beurteilung "offensichtlich" ist,
muessen Quelle und Konfidenz in lesbarer Form vorliegen.

In natuerlichsprachlichen Chunks ist die Quelle irgendwo im Text vergraben oder fehlt.
Konfidenz wurde noch nie ausgedrueckt.
Um zwei Chunks zu vergleichen und zu beurteilen, welcher vertrauenswuerdiger ist,
muss ein LLM lesen und schlussfolgern.

In einer strukturierten Darstellung sind Quelle und Konfidenz Felder.
"Konfidenz unter 0,5 ausschliessen" ist ein Vergleich.
"Nur Primaerquellen einschliessen" ist Feldabgleich.

Die Kosten der Vertrauenswuerdigkeitsfilterung verschieben sich von LLM-Inferenz zu Feldvergleich.

### Aktualitaet: Ist diese Information hinreichend aktuell?

"Wer ist der CEO von Samsung Electronics?"

- Zeit: Maerz 2024. "Samsung Electronics CEO: Kyung Kye-hyun."
- Zeit: Dezember 2022. "Samsung Electronics Co-CEOs: Han Jong-hee, Kyung Kye-hyun."

Beide sind gueltig. Korrektes Format, Quellen vorhanden.
Aber die aktuellste wird gebraucht.

In natuerlicher Sprache kann die Zeit im Text erwaehnt sein oder auch nicht.
Wenn "letztes Jahr" steht, muss man auch berechnen, wann "letztes Jahr" war.

In einer strukturierten Darstellung ist Zeit ein Feld.
Ein ISO-8601-Datum.
"Nur die aktuellste Aussage einschliessen" ist eine Sortieroperation.

Wichtiger noch: Das Kriterium fuer Aktualitaet haengt vom Kontext ab.
Wenn jemand nach dem CEO fragt, wird der aktuellste Eintrag gebraucht.
Wenn jemand nach allen frueheren CEOs fragt, wird jeder Eintrag gebraucht.
Wenn jemand nach Umsatztrends fragt, werden die letzten 8 Quartale gebraucht.

Wenn Zeit als Feld existiert, koennen diese Bedingungen als Abfrage formuliert werden.
Wenn Zeit in natuerlicher Sprache vergraben ist, muss sie jedes Mal extrahiert werden.

---

## Warum Filterung keine mechanische Verifikation ist

Hier gibt es eine wichtige Unterscheidung.

Von den drei Kriterien der Filterung -- Relevanz, Vertrauenswuerdigkeit, Aktualitaet --
koennen Vertrauenswuerdigkeit und Aktualitaet in einer strukturierten Darstellung weitgehend mechanisch verarbeitet werden.
Feldvergleich, Wertsortierung, Bereichsfilterung.

Warum nennt man das dann "Filterung" und nicht "Verifikation"?

Verifikation betrachtet nur Eigenschaften der Information selbst.
"Hat diese Aussage ein Zeitfeld?" Vorhanden oder fehlend. Kein Kontext noetig.

Filterung betrachtet die Beziehung zwischen Information und Situation.
"Ist die Zeit dieser Aussage fuer diese Frage angemessen?" Man muss wissen, was die Frage ist, um zu antworten.

Beide untersuchen dasselbe Zeitfeld,
aber Verifikation prueft "Existenz"
und Filterung beurteilt "Angemessenheit."

Existenz braucht keinen Kontext.
Angemessenheit braucht Kontext.

Dieser Unterschied ist der Grund, warum die Pipeline die beiden Stufen trennt.

---

## Die Kostenstruktur der Filterung

Filterung ist teurer als Verifikation. Aber wie teuer, haengt von der Darstellung ab.

**Filterung in einer natuerlichsprachlichen Pipeline:**
Relevanzbeurteilung -- LLM-Inferenz oder Embedding-Aehnlichkeitsberechnung.
Vertrauenswuerdigkeitsbeurteilung -- LLM extrahiert Quelleninformationen aus Text und bewertet.
Aktualitaetsbeurteilung -- LLM extrahiert Zeitinformationen aus Text und vergleicht.
Alles Schlussfolgern. Alles teuer.

**Filterung in einer strukturierten Darstellung:**
Relevanzbeurteilung -- Entitaets-/Eigenschafts-Feldabgleich + kontextbasierte Beurteilung.
Vertrauenswuerdigkeitsbeurteilung -- Konfidenzfeldvergleich. Quellenfeldabgleich.
Aktualitaetsbeurteilung -- Zeitfeldsortierung. Bereichsvergleich.
Vertrauenswuerdigkeit und Aktualitaet sind Feldoperationen. Nur Relevanz erfordert Beurteilung.

Mit anderen Worten: Strukturierung wandelt zwei der drei Filterkriterien in mechanische Operationen um.
Was bleibt, ist allein die Relevanz.
Selbst die Relevanz verengt sich von "ist dieser Textblock aehnlich zur Frage" zu "ist diese Eigenschaft dieser Entitaet relevant fuer die Frage", was die Beurteilung klarer macht.

Die Gesamtkosten der Filterung sinken erheblich.

---

## Was passiert ohne Filterung

Wenn man verifiziert, aber alles ohne Filterung in den Kontext gibt.

Alle 1.000 gueltigen Informationen gehen hinein.
Davon werden nur 30 gerade gebraucht.

Das LLM liest alle 1.000.
Lesen kostet Geld.
970 unnoetige Informationen zerstreuen die Aufmerksamkeit.
Studien zeigen, dass mehr irrelevante Informationen im Kontext die Wahrscheinlichkeit von Halluzinationen erhoehen.
Die Schlussfolgerungsqualitaet bei den 30, die tatsaechlich zaehlen, verschlechtert sich.

Auch das Fenster wird verschwendet.
Von dem Platz, den 1.000 Eintraege belegen, sind 970 Eintraege Verschwendung.
Dieser Platz haette andere, relevantere Informationen aufnehmen koennen.

Filterung bedeutet, ein endliches Fenster endlich zu verwalten.
Wenn Verifikation bestaetigt "ist es qualifiziert einzutreten",
beurteilt Filterung "hat es einen Grund einzutreten."

Qualifikation ist eine Frage des Formats. Grund ist eine Frage des Kontexts.
Beides ist notwendig.

---

## Filterung ist Politik

Ein weiterer wichtiger Punkt.

Die Kriterien fuer Filterung sind nicht festgelegt.
Sie variieren mit dem Kontext.

Filterung fuer einen medizinischen Beratungsagenten:
Vertrauenswuerdigkeitsschwelle ist hoch. Konfidenz unter 0,9 ausschliessen.
Aktualitaetsstandard ist streng. Medizinische Informationen aelter als 3 Jahre ausschliessen.
Quellen ausschliessen, die nicht peer-reviewed Zeitschriften sind.

Filterung fuer einen Smalltalk-Agenten:
Vertrauenswuerdigkeitsschwelle ist niedrig. Ungefaehre Informationen sind akzeptabel.
Aktualitaetsstandard ist flexibel. Aeltere Informationen koennen je nach Kontext einbezogen werden.
Quellenbeschraenkungen sind locker.

Dieselbe Information wird bei einem Agenten durchgelassen und bei einem anderen abgelehnt.
Die Information hat sich nicht geaendert. Die Politik ist verschieden.

Das bedeutet, Filterung ist nicht nur ein technisches Problem,
sondern ein Designproblem.
"Was in den Kontext kommt" ist dieselbe Frage wie
"nach welchen Standards soll dieser Agent arbeiten."

In einer strukturierten Darstellung wird diese Politik deklarativ ausgedrueckt.
"confidence >= 0.9, time >= 2022, source_type = peer-reviewed."
Eine Abfragezeile.

In natuerlicher Sprache wird diese Politik als natuerliche Sprache im Prompt formuliert.
"Bitte beziehen Sie sich nur auf vertrauenswuerdige, aktuelle Informationen."
Ob das LLM dies konsistent befolgt, ist eine Frage der Wahrscheinlichkeit.

---

## Zusammenfassung

Nicht alle Informationen, die die Verifikation bestehen, werden gebraucht.
Ein endliches Kontextfenster sollte nur enthalten, was fuer die aktuelle Inferenz benoetigt wird.

Filterung beurteilt drei Dinge.
Relevanz -- wird diese Information fuer die aktuelle Frage gebraucht?
Vertrauenswuerdigkeit -- kann man dieser Information glauben?
Aktualitaet -- ist diese Information hinreichend aktuell?

Verifikation und Filterung stellen unterschiedliche Fragen.
Verifikation fragt "ist es gueltig?"; Filterung fragt "wird es gebraucht?"
Verifikation ist ohne Kontext moeglich; Filterung erfordert Kontext.
Verifikation kommt zuerst; Filterung kommt danach.

In einer strukturierten Darstellung werden zwei der drei Filterkriterien -- Vertrauenswuerdigkeit und Aktualitaet -- in Feldoperationen umgewandelt. Was bleibt, ist allein die Relevanz, und selbst die wird durch strukturellen Feldabgleich klarer.

Filterung ist Politik.
Dieselbe Information wird je nach Kontext eingeschlossen oder ausgeschlossen.
In einer strukturierten Darstellung wird diese Politik als Abfrage deklariert.
In natuerlicher Sprache wird diese Politik im Prompt als Hoffnung formuliert.
