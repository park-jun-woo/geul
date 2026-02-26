---
title: "Warum Exploration notwendig ist"
weight: 7
date: 2026-02-26T12:00:07+09:00
lastmod: 2026-02-26T12:00:07+09:00
tags: ["Exploration", "Suche", "Skalierung"]
summary: "Wenn der Index das Fenster uebersteigt, stoesst das Suchparadigma selbst an seine Grenzen"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Wenn der Index das Fenster uebersteigt, stoesst das Suchparadigma selbst an seine Grenzen.

---

## Suche war erfolgreich

Wir haben die Grenzen von RAG besprochen.
Die Ungenauigkeit von Embedding-Aehnlichkeit, die Willkuerlichkeit des Chunk-Splittings, die Unmoeglickeit der Qualitaetsbeurteilung.

Aber diese Diskussion betraf die Qualitaet der Suche.
"Wie sollten wir genauer suchen?"

Jetzt muss eine andere Frage gestellt werden.
Nehmen wir an, die Suche ist perfekt.
Nehmen wir an, sie liefert ausschliesslich Informationen, die praezise zur Anfrage passen.

Es gibt trotzdem Faelle, in denen das nicht funktioniert.

---

## Das Problem der Skalierung

Eine interne Wissensbasis hat 1.000 Aussagen.
Es gibt einen Index. Man gibt den Index in den Kontext. Abfrage. Ergebnisse abrufen.
Es funktioniert.

Die Aussagen wachsen auf 100.000.
Der Index wird groesser. Er passt noch ins Fenster. Es funktioniert.

Die Aussagen wachsen auf 10 Millionen.
Der Index selbst uebersteigt das Fenster.

Das ist kein Problem der Suchqualitaet.
Egal wie genau die Suche ist --
wenn der Index, der fuer die Suche konsultiert werden muss, nicht ins Fenster passt,
kann die Suche nicht einmal beginnen.

Und Wissen waechst.
Unternehmensdokumente nehmen taeglich zu.
Was ein Agent gelernt hat, akkumuliert sich weiter.
Das Wissen der Welt schrumpft nicht.

Loest ein groesseres Fenster das Problem?
Wenn 128K zu 1M wird zu 10M?
Wenn das Wissen 100M erreicht, wiederholt sich dasselbe Problem.
Das Fenster ist immer endlich, und Wissen waechst immer.
Dieses Ungleichgewicht ist permanent.

---

## Der Unterschied zwischen Suche und Exploration

Suche liefert Ergebnisse mit einer einzelnen Abfrage.

Abfrage: "Samsung Electronics operativer Gewinn Q3 2024"
-> Ergebnis: 9,18 Billionen Won.

Ein Schuss. Erledigt.

Exploration erreicht Ergebnisse durch mehrere Schritte.

Schritt 1: Die uebergeordnete Wissenskarte betrachten. "Konzerne", "Branchen", "Makrooekonomie", "Technologie"...
-> "Konzerne" waehlen.

Schritt 2: Die Konzernkarte betrachten. "Samsung Electronics", "SK Hynix", "Hyundai Motor"...
-> "Samsung Electronics" waehlen.

Schritt 3: Die Samsung-Electronics-Karte betrachten. "Finanzen", "Personal", "Technologie", "Recht"...
-> "Finanzen" waehlen.

Schritt 4: Die Finanzkarte betrachten. "Quartalsergebnisse", "Jahresergebnisse", "Investitionsplaene"...
-> "Quartalsergebnisse" waehlen.

Schritt 5: "Q3 2024" aus den Quartalsergebnissen abrufen.
-> Operativer Gewinn: 9,18 Billionen Won.

Das Ergebnis ist dasselbe.
Der Prozess ist anders.

Suche fragt "Hast du das?"
Exploration verfolgt "Wo koennte es sein?"

Suche erfordert, dass der Index fuer den Suchenden sichtbar ist. Der gesamte Index muss zugaenglich sein.
Exploration muss nur die aktuelle Ebene der Karte sehen. Bei jedem Schritt gelangt nur eine Ebene ins Fenster.

---

## Die Bibliotheksanalogie

Sie besuchen eine Stadtteilbibliothek.
Sie hat 3.000 Buecher.
Sie fragen den Bibliothekar: "Haben Sie eine Biografie von Yi Sun-sin?"
Der Bibliothekar erinnert sich: "Die steht am Ende von Regal 3."
Suche. Es funktioniert.

Sie besuchen die Nationalbibliothek.
Sie umfasst 10 Millionen Baende.
Sie fragen den Bibliothekar: "Haben Sie eine Biografie von Yi Sun-sin?"
Der Bibliothekar weiss es auch nicht. Niemand merkt sich 10 Millionen Baende.

Stattdessen gibt es ein Klassifikationssystem.

Sie pruefen das Erdgeschoss-Verzeichnis. -> Die Abteilung "Geschichte" ist im 3. Stock.
Sie gehen in den 3. Stock. -> "Koreanische Geschichte" ist im Ostfluegel.
Sie gehen in den Ostfluegel. -> "Joseon-Dynastie" ist in Reihe D.
Sie gehen zu Reihe D. -> "Persoenlichkeiten" ist im 3. Abschnitt von Reihe D.
Sie durchsuchen den 3. Abschnitt. -> Es gibt eine Biografie von Yi Sun-sin.

Die Gedaechtniskapazitaet des Bibliothekars hat sich nicht geaendert.
Der Umfang der Bibliothek hat sich geaendert.
Die Methode wechselte vom Fragen des Bibliothekars (Suche) zum Durchlaufen des Klassifikationssystems (Exploration).

Hier ist der Schluesselpunkt.
Bei jedem Schritt passt die Groesse des Betrachteten in die Gedaechtniskapazitaet des Bibliothekars.
Das Erdgeschoss-Verzeichnis. Die Zonenkarte des 3. Stocks. Die Reihenliste des Ostfluegels. Die Abschnittsliste von Reihe D.
Alles passt in einen einzigen Blick.

Der vollstaendige Katalog aller Bestaende passt nicht in einen einzigen Blick.
Aber die Karte jeder Etage schon.

So unterscheidet sich Exploration von Suche.
Man muss nicht das Ganze auf einmal sehen.
Man muss nur die naechste Richtung vom aktuellen Standort aus beurteilen.

---

## Karten von Karten

In technischen Begriffen ist das eine hierarchische Kartenstruktur.

**Ebene-1-Karte**: die uebergeordnete Klassifikation des gesamten Wissens.
"Diese Wissensbasis enthaelt Informationen zu Konzernen, Branchen, Makrooekonomie und Technologie."
Dutzende Eintraege. Passt ins Fenster.

**Ebene-2-Karte**: die Unterkategorien jeder uebergeordneten Klassifikation.
"Die Kategorie Konzerne enthaelt Samsung Electronics, SK Hynix, Hyundai Motor..."
Dutzende bis Hunderte Eintraege. Passt ins Fenster.

**Ebene-3-Karte**: die Detailkategorien jeder Unterkategorie.
"Samsung Electronics enthaelt Finanzen, Personal, Technologie, Recht..."
Dutzende Eintraege. Passt ins Fenster.

**Tatsaechliche Aussagen**: die konkreten Informationen, auf die die unterste Kartenebene zeigt.
"Samsung Electronics' operativer Gewinn Q3 2024 betrug 9,18 Billionen Won."

Wenn die Groesse jeder Ebene ins Fenster passt,
ist Exploration unabhaengig vom Gesamtumfang des Wissens moeglich.

Selbst bei 10 Millionen Aussagen:
Wenn jede Ebene 100 Eintraege hat, erreicht man das Ziel in 5 Explorationsschritten.
100 -> 100 -> 100 -> 100 -> 100 = Abdeckung bis 10 Milliarden.
Bei jedem Schritt gelangen nur 100 Eintraege ins Fenster.

Das ist dasselbe Prinzip, nach dem ein B-tree Daten auf der Festplatte findet.
Er laedt nicht alle Daten in den Speicher.
Er liest nur den aktuellen Knoten des Baums und geht zum naechsten.
Daten jeder Groessenordnung koennen unabhaengig von der Speichergroesse durchsucht werden.

Das Kontextfenster ist der Arbeitsspeicher.
Die Wissensbasis ist die Festplatte.
Die Karte ist ein B-tree-Knoten.

---

## Der Agent geht

Bei mehrstufiger Exploration -- wer waehlt die Richtung bei jedem Schritt?

Der Agent.

Man gibt die Ebene-1-Karte in den Kontext.
Der Agent liest sie, vergleicht sie mit der Anfrage und waehlt die Richtung "Konzerne."

Die Ebene-2-Karte anfordern.
Die Unterkategoriekarte der Konzerne gelangt in den Kontext.
Der Agent liest sie und waehlt die Richtung "Samsung Electronics."

Die Ebene-3-Karte anfordern.
Der Agent waehlt "Finanzen."

Das ist der Werkzeugeinsatz des Agenten.
Eine Karte lesen ist ein Werkzeugaufruf.
Eine Richtung waehlen ist eine Beurteilung.
Die naechste Karte anfordern ist der naechste Werkzeugaufruf.

Bei der Suche fragt der Agent einmal ab und erhaelt ein Ergebnis. Passiv.
Bei der Exploration trifft der Agent mehrere Beurteilungen und waehlt Richtungen. Aktiv.

Hier treffen Context Engineering und Agent-Design aufeinander.
Was in den Kontext kommt, wird Schritt fuer Schritt durch die Beurteilung des Agenten bestimmt.
Kontextkonstruktion wechselt von statischer Zusammenstellung zu dynamischer Exploration.

---

## Dieses Problem wird heute kaum diskutiert

Wenn man Diskussionen in der RAG-Community betrachtet,
konzentriert sich die meiste Energie auf die Suchqualitaet.

Bessere Embedding-Modelle.
Bessere Chunking-Strategien.
Reranker-Architekturen.
Hybride Suche.
Graph RAG.

Alles wichtig.
Alles dreht sich um "wie bekommt man bessere Ergebnisse aus einer einzelnen Suche."

"Was, wenn eine einzelne Suche nicht ausreicht?" wird kaum diskutiert.

Der Punkt, an dem der Index das Fenster uebersteigt.
Der Punkt, an dem Ergebnisse zu zahlreich sind, um hineinzupassen.
Der Punkt, an dem der Umfang des Wissens die Praemisse des Suchparadigmas selbst durchbricht.

Dieser Punkt kommt.
Wissen waechst und das Fenster ist endlich.

Die meisten aktuellen Loesungen weichen aus.
Nur die Top k abrufen. Den Rest verwerfen.
Das Fenster vergroessern. Kosten steigen.
Das Wissen partitionieren. Separate Vektorspeicher pro Domaene.

Alle stossen auf dasselbe Problem, wenn der Umfang weiter waechst.

---

## Voraussetzungen fuer Exploration

Damit Exploration funktioniert, muss Wissen in einer explorierbaren Struktur vorliegen.

**Hierarchie muss existieren.** Wenn Wissen flach ausgelegt ist, ist Exploration unmoeglich. Ein Embedding-Vektorspeicher ist flach. Alle Chunks liegen auf derselben Ebene. Es gibt keine Hierarchie, also existiert das Konzept "tiefer gehen" nicht.

**Jede Ebene muss ins Fenster passen.** Wenn eine einzelne Karte das Fenster uebersteigt, scheitert die Exploration. Die Anzahl der Wahlmoeglichkeiten auf jeder Hierarchieebene muss eine angemessene Groesse haben. Das ist ein Klassifikations-Designproblem.

**Pfade muessen vielfaeltig sein.** Es muss moeglich sein, dieselbe Information ueber mehrere Pfade zu erreichen. Ueber "Samsung Electronics -> Finanzen -> Operativer Gewinn" oder ueber "Halbleiterbranche -> Grosse Unternehmen -> Samsung Electronics -> Ergebnisse." Denn der natuerliche Pfad variiert je nach Frage. Wenn das Klassifikationskriterium auf eines festgelegt ist, passt es zu manchen Fragen und zu anderen nicht.

Eine Ordnerstruktur hat Hierarchie, aber nur einen Pfad.
Eine Datei gehoert zu nur einem Ordner.
Nur der Pfad "Samsung Electronics/Finanzen/Operativer Gewinn" existiert.
Wenn eine Frage zur "Halbleiterbranche" kommt, ist natuerliche Exploration durch diese Ordnerstruktur unmoeglich.

Ein Graph hat sowohl Hierarchie als auch vielfaeltige Pfade.
Ein einzelner Knoten kann mit mehreren uebergeordneten Knoten verbunden sein.
Der Samsung-Electronics-Knoten kann ueber einen "Konzerne"-Pfad, einen "Halbleiterbranche"-Pfad oder einen "KOSPI-gelistete Unternehmen"-Pfad erreicht werden.
Unabhaengig vom Kontext, aus dem eine Frage stammt, existiert ein natuerlicher Pfad.

---

## Das ist ein ungeloestes Problem

Etwas muss ehrlich gesagt werden.

Die Notwendigkeit mehrstufiger Exploration ist klar.
Aber es gibt noch kein Standardsystem, das dies effektiv implementiert.

Wie generiert man die Hierarchie der Karten automatisch?
Wie bestimmt man die angemessene Groesse jeder Ebene?
Was passiert, wenn der Agent die falsche Richtung waehlt?
Was passiert mit der Latenz, wenn die Explorationstiefe zunimmt?

Das sind offene Fragen.

Aber die Tatsache, dass ein Problem ungeloest ist,
bedeutet nicht, dass das Problem nicht existiert.

Wissen waechst.
Das Fenster ist endlich.
Der Punkt, an dem Suche allein nicht ausreicht, kommt.

Exploration muss als Antwort fuer diesen Punkt bereitstehen.
Wenn sie nicht bereitsteht,
bleiben nur die Moeglichkeiten, das Fenster zu vergroessern oder Wissen zu verwerfen.

---

## Zusammenfassung

Suche liefert Ergebnisse mit einer einzelnen Abfrage.
Wenn der Umfang des Wissens gross genug wird, reicht das nicht aus.
Weil der Index selbst das Fenster uebersteigt.

Exploration folgt hierarchischen Karten und waehlt Richtungen beim Abstieg.
Was bei jedem Schritt betrachtet werden muss, passt ins Fenster.
Jeder Schritt ist endlich, unabhaengig vom Gesamtumfang.
Genau wie ein B-tree Daten findet, ohne die gesamte Festplatte in den Speicher zu laden.

Der Agent beurteilt die Richtung bei jedem Schritt.
Kontextkonstruktion wechselt von statischer Zusammenstellung zu dynamischer Exploration.
Hier treffen Context Engineering und Agent-Design aufeinander.

Damit Exploration funktioniert, muss Wissen hierarchisch sein, jede Ebene muss endlich sein und Pfade muessen vielfaeltig sein.
Eine Ordnerstruktur hat nur einen Pfad. Ein Graph hat vielfaeltige Pfade.

Das ist nach wie vor ein ungeloestes Problem ohne Standardloesung.
Aber solange Wissen waechst und das Fenster endlich ist, ist es ein Problem, das geloest werden muss.
