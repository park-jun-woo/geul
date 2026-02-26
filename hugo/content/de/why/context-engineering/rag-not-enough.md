---
title: "Warum RAG nicht ausreicht"
weight: 2
date: 2026-02-26T12:00:11+09:00
lastmod: 2026-02-26T12:00:11+09:00
tags: ["RAG", "Suche", "Embedding"]
summary: "Relevant aussehen und relevant sein sind nicht dasselbe"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Relevant aussehen und relevant sein sind nicht dasselbe.

---

## RAG ist der aktuelle Standard

Stand 2024 ist RAG die verbreitetste Methode, mit der Unternehmen LLMs produktiv einsetzen.

Retrieval-Augmented Generation.
Externe Dokumente durchsuchen, in den Kontext stopfen und das Modell auf dieser Grundlage antworten lassen.

RAG funktioniert.
Es ermoeglicht LLMs, auf interne Dokumente zuzugreifen, auf die sie nie trainiert wurden.
Es ermoeglicht ihnen, aktuelle Informationen widerzuspiegeln.
Es reduziert Halluzinationen erheblich.

Ohne RAG waere die Einfuehrung von LLMs in Unternehmen deutlich langsamer verlaufen.
RAG ist eine Technologie, die Respekt verdient.

Aber RAG hat fundamentale Grenzen.
Diese Grenzen lassen sich nicht durch besseres RAG loesen.
Sie ergeben sich aus der Grundannahme von RAG selbst.

---

## Wie RAG funktioniert

Der Kern von RAG besteht aus drei Schritten.

**Schritt 1: Dokumente in Chunks aufteilen.**
PDFs, Wikis, interne Dokumente werden in feste Groessen unterteilt (typischerweise 200--500 Token).

**Schritt 2: Jeden Chunk in einen Embedding-Vektor umwandeln.**
Ein reellwertiger Vektor mit Hunderten bis Tausenden von Dimensionen.
Die "Bedeutung" des Textes, abgebildet auf einen einzelnen Punkt im Vektorraum.

**Schritt 3: Bei einer Anfrage aehnliche Vektoren finden.**
Die Anfrage wird ebenfalls in einen Vektor umgewandelt.
Die 5--20 Chunks mit der hoechsten Kosinus-Aehnlichkeit werden ausgewaehlt und in den Kontext eingefuegt.

Einfach und elegant.
Und hier liegen drei fundamentale Probleme.

---

## Problem 1: Aehnlich ist nicht relevant

Embedding-Aehnlichkeit misst, "ob zwei Texte aehnliche Woerter in aehnlichen Kontexten verwenden."

Das ist keine Relevanz.

Beispiel.

Anfrage: "Wie hoch war Apples Umsatz in Q3 2024?"

Chunks, die die Embedding-Suche zurueckgeben koennte:
- "Apples Umsatz in Q3 2024 betrug 94,9 Milliarden Dollar." -- Relevant
- "Apples Umsatz in Q3 2023 betrug 81,8 Milliarden Dollar." -- Aehnlich, aber anderer Zeitraum
- "Samsung Electronics' Umsatz in Q3 2024 betrug 79 Billionen Won." -- Aehnlich, aber anderes Unternehmen
- "Ein Apfelkuchen hat etwa 296 kcal." -- Wort-Ueberschneidung

Die Embedding-Aehnlichkeit kann diese vier nicht unterscheiden.
Im Vektorraum gruppiert sich "Apple Umsatz" um eine einzige Region.
Ob 2023 oder 2024, Apple oder Samsung --
der Vektorabstand trennt sie nicht zuverlaessig.

Ein Reranker verbessert die Sache.
Aber ein Reranker liest und beurteilt ebenfalls natuerlichsprachlichen Text,
also bleibt das fundamentale Mehrdeutigkeitsproblem bestehen.

Semantisch-strukturbasierte Suche ist anders.
Wenn "Apple" als Entitaet einen eindeutigen Bezeichner hat,
wird es nie mit "Apfel" der Frucht verwechselt.
Wenn "Q3 2024" ein Zeitfeld ist,
wird es mechanisch von "Q3 2023" unterschieden.

Keine Aehnlichkeitsberechnung noetig.
Stimmt es ueberein oder nicht? Ja oder nein.

---

## Problem 2: Chunks sind keine Bedeutungseinheiten

Schauen Sie sich den ersten Schritt von RAG noch einmal an.
"Dokumente in Chunks aufteilen."

Dieses "Aufteilen" ist das Problem.

Wenn man ein Dokument in 500-Token-Einheiten aufteilt,
wird die Bedeutung mittendrin abgeschnitten.
Ein Absatz erstreckt sich ueber zwei Chunks.
Praemisse und Schlussfolgerung eines Arguments werden getrennt.

"Yi Sun-sin trat mit nur 12 Schiffen gegen 133 Schiffe in der Schlacht von Myeongnyang an" steht in Chunk A,
und "Historiker bezweifeln diese Zahlen" steht in Chunk B.
Wenn fuer eine Anfrage nur Chunk A abgerufen wird,
gelangt die Vertrauensinformation bereits verloren in den Kontext.

Chunks groesser machen? Sie verbrauchen mehr vom Fenster.
Chunks kleiner machen? Mehr Kontext wird abgeschnitten.
Ueberlappung hinzufuegen? Man verschwendet das Fenster mit Duplikaten.

Wie man es auch einstellt, das fundamentale Problem bleibt dasselbe.
Natuerlichsprachlichen Text nach Token-Anzahl aufzuteilen
ist dasselbe wie Bedeutung nach Token-Anzahl aufzuteilen.
Bedeutung hat eine inherente Groesse,
und sie nach einer unzusammenaengenden Einheit zu teilen verursacht Probleme.

In einer strukturierten Darstellung sind Bedeutungseinheiten explizit.
Eine Praedikation ist eine Kante.
Eine Kante wird nicht geteilt.
Die Suche operiert auf Kantenebene.
Es gibt kein Abschneiden mitten in der Bedeutung.

---

## Problem 3: Die Qualitaet der Suchergebnisse ist unbekannt

RAG hat 5 Chunks zurueckgegeben.
Bevor man diese 5 in den Kontext gibt, gibt es Fragen zu stellen.

Was ist die Quelle dieser Information?
Was ist das Bezugsdatum?
Wie sicher ist sie?
Widersprechen sich diese 5 gegenseitig?

In natuerlichsprachlichen Chunks kann man das nicht wissen.

Die Quelle kann irgendwo im Chunk als natuerliche Sprache erwaehnt sein oder auch nicht.
Der Zeitbezug kann irgendwo im Dokument stehen, oder er ging beim Aufteilen des Chunks verloren.
Konfidenz hat in natuerlicher Sprache kein strukturelles Feld, daher fehlt sie fast immer.
Widerspruchspruefung erfordert, alle 5 Chunks zu lesen und darueber zu schlussfolgern.

Letztlich muss man die Qualitaetsbeurteilung an das LLM delegieren.
Man nutzt RAG, um LLM-Aufrufkosten zu senken,
ruft aber das LLM auf, um RAG-Ergebnisse zu ueberpruefen.

In einer strukturierten Darstellung sind Quelle, Zeit und Konfidenz Felder.
"Aussagen ohne Quelle ausschliessen" ist eine Abfragezeile.
"Informationen vor 2023 ausschliessen" ist ein Feldvergleich.
"Konfidenz unter 0,5 ausschliessen" ist ein numerischer Vergleich.
Kein LLM-Aufruf noetig.

---

## Die fundamentale Praemisse von RAG

Die Wurzel dieser drei Probleme ist eine Sache.

RAG durchsucht natuerliche Sprache als natuerliche Sprache.

Die Dokumente sind natuerliche Sprache.
Die Chunks sind natuerliche Sprache.
Die Embeddings sind statistische Approximationen natuerlicher Sprache.
Die Suchergebnisse sind natuerliche Sprache.
Was in den Kontext gelangt, ist natuerliche Sprache.

Die Mehrdeutigkeit natuerlicher Sprache durchdringt die gesamte Pipeline.

Die Suche ist ungenau, weil man mehrdeutigen Inhalt in seiner mehrdeutigen Form durchsucht.
Kontext geht verloren, weil man mehrdeutigen Inhalt nach einer bedeutungsfremden Groesse aufteilt.
Verifikation ist unmoeglich, weil man aus mehrdeutigem Inhalt keine Qualitaetsinformationen extrahieren kann.

Die meisten Versuche, RAG zu verbessern, operieren innerhalb dieser Praemisse.

Ein besseres Embedding-Modell verwenden. -- Die statistische Approximation wird verfeinert, das ist alles.
Eine bessere Chunking-Strategie verwenden. -- Die Schnittpositionen verbessern sich, das ist alles.
Einen Reranker hinzufuegen. -- Man liest die natuerliche Sprache noch einmal, das ist alles.
Hybride Suche verwenden. -- Man mischt Schluesselwoerter und Aehnlichkeit, das ist alles.

Alles funktioniert.
Alles bleibt im Rahmen der natuerlichen Sprache.
Nichts davon ist fundamental.

---

## Bedingungen fuer eine fundamentale Alternative

Um ueber die Grenzen von RAG hinauszugehen, muss sich die Praemisse aendern.
Nicht natuerliche Sprache als natuerliche Sprache durchsuchen,
sondern strukturierte Darstellungen strukturell durchsuchen.

Diese Alternative muss drei Bedingungen erfuellen.

**Suche nach Uebereinstimmung, nicht nach Aehnlichkeit.**
Nicht "Dinge finden, die aehnlich aussehen",
sondern "Dinge finden, die uebereinstimmen."
Stimmt der Bezeichner ueberein? Liegt es im Zeitbereich?
Ja oder nein. Keine Wahrscheinlichkeit.

**Die Bedeutungseinheit ist die Sucheinheit.**
Nicht nach Token-Anzahl aufteilen,
sondern nach Praedikation speichern und nach Praedikation suchen.
Kein Abschneiden mitten in der Bedeutung.

**Metadaten sind in die Struktur eingebettet.**
Kein LLM-Aufruf noetig, um die Qualitaet der Suchergebnisse zu beurteilen.
Quelle, Zeit und Konfidenz sind Felder,
sodass mechanische Filterung moeglich ist.

Wenn diese drei Bedingungen erfuellt sind,
verschiebt sich die Suche von "plausible Kandidaten erraten"
zu "Uebereinstimmungen bestaetigen."

---

## RAG ist eine Uebergangstechnologie

Das soll RAG nicht herabsetzen.

RAG war die beste Antwort in einer Welt, in der natuerliche Sprache alles war.
Als Dokumente natuerliche Sprache waren, Wissen in natuerlicher Sprache gespeichert wurde
und LLMs Werkzeuge waren, die natuerliche Sprache verarbeiten,
war es naheliegend, natuerliche Sprache mit natuerlicher Sprache zu durchsuchen.

Und RAG funktioniert.
Ein LLM mit RAG ist weit genauer als eines ohne.
Das ist eine Tatsache.

Aber wenn sich die Praemisse "eine Welt, in der natuerliche Sprache alles ist" aendert,
aendert sich auch RAGs Position.

Wenn strukturierte Darstellungen existieren,
wird RAG zum Frontend, das "natuerlichsprachliche Eingaben nimmt und einen strukturierten Speicher durchsucht."
Natuerliche Sprache -> strukturierte Abfrage -> strukturelle Suche -> strukturierte Ergebnisse -> Kontext.

RAG verschwindet nicht.
Sein Backend aendert sich.
Von Embedding-Aehnlichkeitssuche zu semantisch-strukturbasierter Suche.

---

## Zusammenfassung

RAG ist der aktuelle Standard fuer Context Engineering.
Und es hat drei fundamentale Grenzen.

1. **Aehnlich ≠ relevant.** Embedding-Aehnlichkeit garantiert keine Relevanz. "Sieht aehnlich aus" und "ist relevant" sind verschieden.
2. **Chunk ≠ Bedeutung.** Aufteilen nach Token-Anzahl schneidet mitten durch die Bedeutung. Praemissen und Schlussfolgerungen werden getrennt. Vertrauensinformationen gehen verloren.
3. **Qualitaetsbeurteilung ist unmoeglich.** Quelle, Zeit und Konfidenz abgerufener Chunks koennen nicht mechanisch bestimmt werden. Ihre Beurteilung erfordert einen LLM-Aufruf.

Die Wurzel der drei Probleme ist eine Sache.
Natuerliche Sprache als natuerliche Sprache durchsuchen.

Die fundamentale Alternative ist, die Praemisse zu aendern.
Uebereinstimmung, nicht Aehnlichkeit.
Praedikation, nicht Token-Chunks.
Eingebettete Metadaten, nicht externe Beurteilung.

RAG ist eine Uebergangstechnologie.
Es war die beste Antwort in einer Welt, in der natuerliche Sprache alles war.
Wenn sich diese Praemisse aendert, aendert sich RAGs Backend.
