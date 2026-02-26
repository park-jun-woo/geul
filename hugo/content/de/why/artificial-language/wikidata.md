---
title: "Warum Wikidata"
weight: 13
date: 2026-02-26T12:00:17+09:00
lastmod: 2026-02-26T12:00:17+09:00
tags: ["Wikidata", "Ontologie", "SIDX"]
summary: "GEUL lehnt Wikidata nicht ab. Es wandelt das Klassifikationssystem und die Haeufigkeitsstatistiken von 100 Millionen Entitaeten in SIDX-Codebuecher um. Grammatik wird auf einem Woerterbuch aufgebaut."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## GEUL lehnt Wikidata nicht ab. Es steht darauf.

---

## Ohne Woerterbuch laesst sich keine Sprache erschaffen

Jede Sprache braucht einen Wortschatz.

Koreanisch hat das koreanische Woerterbuch.
Englisch hat das englische Woerterbuch.
Programmiersprachen haben Standardbibliotheken.

Dasselbe gilt fuer eine kuenstliche Sprache.
Eine Liste von Entitaeten, eine Liste von Relationen, eine Liste von Eigenschaften.
Welcher Code steht fuer „Samsung Electronics" in dieser Sprache?
Welcher Code steht fuer die Relation „Hauptstadt"?
Man braucht einen Wortschatz, bevor man einen Satz schreiben kann.

Wie baut man diesen Wortschatz auf?
Es gibt zwei Wege.

Ihn von Grund auf neu erstellen.
Oder das verwenden, was bereits existiert.

---

## Von Grund auf neu: die Lehre aus CYC

Das CYC-Projekt begann 1984.

Sein Ziel war es, allgemeines Alltagswissen zu formalisieren und zu speichern.
Die Ontologie wurde von Grund auf entworfen.
Konzepte wurden definiert, Relationen wurden definiert, Regeln wurden definiert.
Experten gaben sie haendisch ein.

Dreissig Jahre vergingen.
Millionen von Regeln wurden eingegeben.

Doch es reichte bei Weitem nicht aus, um das Wissen der Welt abzudecken.
Fuer jede Domaene musste eine eigene Ontologie entworfen werden.
Die Konsistenz zwischen den Domaenen aufrechtzuerhalten erwies sich als schwierig.
Bei jedem neuen Konzept musste die Ontologie ueberarbeitet werden.
Ueberarbeitungen standen haeufig im Widerspruch zu bestehenden Regeln.

Was CYC bewies, war nicht sein Potenzial, sondern seine Grenzen.
Die Weltontologie von einem kleinen Expertenteam entwerfen zu lassen,
wird im grossen Massstab unwartbar.

---

## Was bereits existiert: Wikidata

Wikidata wurde 2012 gestartet.

Eine strukturierte Wissensbasis, betrieben von der Wikimedia Foundation.
Jeder kann sie bearbeiten.
Stand 2024 enthaelt sie ueber 100 Millionen Entitaeten.
Mehr als 10.000 Eigenschaften.
Milliarden von Aussagen.
Bezeichnungen in ueber 300 Sprachen.

Den Umfang, den CYC in 30 Jahren mit einem Expertenteam nicht erreichen konnte,
erreichte Wikidata in 10 Jahren mit einer Community.

Betrachten wir, was Wikidata bietet.

**Entitaetsidentifikatoren.** Q-IDs. Samsung Electronics ist Q20718. Seoul ist Q8684. Yi Sun-sin ist Q217300. Weltweit eindeutige Identifikatoren. Sprachunabhaengig.

**Eigenschaftsidentifikatoren.** P-IDs. „Hauptsitz" ist P159. „Gruendungsdatum" ist P571. „Bevoelkerung" ist P1082. Relationen und Eigenschaften werden eindeutig identifiziert.

**Hierarchische Struktur.** P31 (instance of) und P279 (subclass of) bilden eine Typhierarchie. „Seoul → Stadt → menschliche Siedlung → geographische Entitaet." Das Klassifikationssystem der Welt wird durch diese beiden Eigenschaften ausgedrueckt.

**Mehrsprachige Bezeichnungen.** Die koreanische Bezeichnung fuer Q20718 ist „삼성전자", die englische „Samsung Electronics", die japanische „サムスン電子". Ein Identifikator, verschiedene Namen fuer jede Sprache.

**Community-Validierung.** Millionen von Editoren. Vandalismuserkennung. Quellenanforderungen. Nicht perfekt, aber skalierbarer als ein kleines Expertenteam.

Es gibt keinen Grund, dies von Grund auf neu zu bauen.

---

## GEULs Wortschatz kommt aus Wikidata

GEULs SIDX (Semantic-aligned Index) ist ein 64-Bit semantisch ausgerichteter Identifikator.
Die Bedeutung ist in den Bits selbst kodiert.
Allein durch die Untersuchung der oberen Bits laesst sich erkennen, ob etwas eine Person, ein Ort oder eine Organisation ist.

Das SIDX-Codebuch — welches Bitmuster welcher Bedeutung entspricht — wird aus Wikidata extrahiert.

Der Prozess laeuft folgendermassen ab.

**Schritt 1: Typextraktion.**
Alle Q-IDs, die als Objekte von P31 (instance of) in Wikidata verwendet werden, werden extrahiert.
Dies ergibt die Liste der „Typen".
„Mensch (Q5)", „Stadt (Q515)", „Staat (Q6256)", „Unternehmen (Q4830453)"...
Es wird gezaehlt, wie oft jeder Typ verwendet wird — die Anzahl der Instanzen.

**Schritt 2: Hierarchieaufbau.**
Die P279-Relationen (subclass of) zwischen Typen werden extrahiert.
„Stadt → menschliche Siedlung → geographische Entitaet → Entitaet."
Dies bildet die Baumstruktur der Typen.
Wurzelknoten, Blattknoten und Zwischenknoten werden identifiziert.
Mehrfachvererbung — Faelle, in denen ein Typ zu mehreren Elterntypen gehoert — wird erkannt und behandelt.

**Schritt 3: Bitzuweisung.**
Die Baumstruktur bestimmt die Praefixbeziehungen der Bitmuster.
Untertypen unter demselben Elterntyp teilen dasselbe Praefix.
„Stadt" und „Dorf" teilen das Praefix von „menschliche Siedlung".

Die Instanzanzahl beeinflusst die Bitlaenge.
Haeufig verwendete Typen erhalten effizientere Codes.
Dasselbe Prinzip wie bei der Huffman-Kodierung: kuerzere Codes fuer hoehere Haeufigkeiten.

---

## Was Wikidata liefert

In diesem Prozess liefert Wikidata drei Dinge.

**Ein Klassifikationssystem.**
Eine Antwort auf „Welche Arten von Dingen gibt es auf der Welt?"
CYC liess dies von einem Expertenteam entwerfen.
GEUL extrahiert es aus Wikidata.
Ein Klassifikationssystem, das Millionen von Editoren ueber 10 Jahre aufgebaut haben,
umgewandelt in einen Bitbaum.

**Haeufigkeitsstatistiken.**
Eine Antwort auf „Wie viele von jeder Art gibt es auf der Welt?"
Wenn es 9 Millionen menschliche Entitaeten und 1 Million Asteroiden gibt,
sollte der Typ „Mensch" einen effizienteren Code erhalten als „Asteroid".
Die tatsaechliche Nutzungshaeufigkeit bestimmt das Codedesign.

**Identifikatorzuordnung.**
Eine Zuordnung zwischen Wikidatas Q-IDs und GEULs SIDX.
Welches Bitmuster im SIDX entspricht Q20718 (Samsung Electronics)?
Mit dieser Zuordnung kann Wikidata-Wissen in GEUL konvertiert werden
und GEUL-Aussagen koennen zurueck in Wikidata konvertiert werden.

---

## Was Wikidata nicht liefert

Wikidata ist ein Woerterbuch. Ein Woerterbuch ist keine Sprache.

Ein Woerterbuch liefert eine Liste von Woertern.
Eine Sprache liefert die Grammatik, um aus Woertern Saetze zu bilden.

Was Wikidata nicht liefert, ist das, was GEUL hinzufuegt.

**Von Fakten zu Behauptungen.**
Die Grundeinheit von Wikidata ist eine Tatsache (Fact).
„Die Bevoelkerung von Seoul betraegt 9,74 Millionen."
Sie ist entweder wahr oder falsch.

Die Grundeinheit von GEUL ist eine Behauptung (Claim).
„Laut A betraegt die Bevoelkerung von Seoul etwa 9,74 Millionen. (Konfidenz 0,9, Stand 2023)"
Wer behauptet, mit welcher Sicherheit, und zu welchem Zeitpunkt — all das ist in der Aussage eingebettet.
Dieser Unterschied wird ausfuehrlich in [Warum Behauptungen, nicht Fakten](/de/why/claims-not-facts/) behandelt.

**Verbqualifikatoren.**
Wikidata hat keinen Platz, um die Nuancen von Verben auszudruecken.
In „Yi Sun-sin gewann die Schlacht von Myeongnyang" —
wo befinden sich Tempus, Aspekt, Evidentialitaet, Modus und Konfidenz?
In Wikidata werden diese teilweise durch Qualifier ausgedrueckt,
aber ein systematisches Verbqualifikationssystem gibt es nicht.

GEUL hat ein 28-Bit-Verbqualifikatorsystem.
Dreizehn Dimensionen — Tempus, Aspekt, Polaritaet, Evidentialitaet, Modus, Volitivitaet, Konfidenz und weitere — sind strukturell in jede Aussage eingebettet.

**16-Bit-Komprimierung.**
Wikidatas Darstellung wurde nicht fuer Kontextfenster entworfen.
JSON-LD, RDF, SPARQL.
Maschinenlesbar, aber nicht tokeneffizient.

GEUL ist in 16-Bit-Worteinheiten konzipiert.
Eins-zu-eins-Zuordnung mit LLM-Tokens.
Ein Darstellungssystem, das auf der Praemisse endlicher Kontextfenster aufgebaut ist.
Dies wurde bereits in [Warum nicht MD/JSON/XML](/de/why/not-md-json-xml/) behandelt.

**Kontextpipeline.**
Wikidata ist ein Speicher. GEUL ist Teil einer Pipeline.
Klaerung, Validierung, Filterung, Konsistenzpruefung, Exploration — alles, was in dieser Serie diskutiert wurde, arbeitet auf GEULs strukturierter Darstellung.
Wikidata hat diese Pipeline nicht.
Und braucht sie auch nicht. Wikidatas Zweck ist ein anderer.

---

## Das Verhaeltnis zwischen Woerterbuch und Sprache

Zusammengefasst:

Wikidata ist der Wortschatz der Welt.
Welche Entitaeten existieren,
welche Relationen existieren,
welche Typen existieren und wie sie klassifiziert sind.
Millionen von Menschen haben dies ueber 10 Jahre aufgebaut.

GEUL baut Grammatik auf diesen Wortschatz auf.
Das Klassifikationssystem des Wortschatzes → der Bitbaum des SIDX.
Die Haeufigkeitsstatistiken des Wortschatzes → die Prioritaeten der Bitzuweisung.
Die Identifikatoren des Wortschatzes → die Zuordnung zum SIDX.

Und es fuegt hinzu, was dem Wortschatz fehlt.
Behauptungsstruktur. Verbqualifikation. Komprimierung auf Tokenebene. Kontextpipeline.

Koennte GEUL ohne Wikidata gebaut werden?
Ja. Man wuerde die Ontologie von Grund auf entwerfen, wie CYC.
Aber das wurde vor 30 Jahren versucht, und die Ergebnisse sprechen fuer sich.

Weil Wikidata existiert, entwirft GEUL keine Ontologie.
Es wandelt einen bestehenden Konsens um.

---

## Zusammenfassung

Eine kuenstliche Sprache braucht einen Wortschatz.
Einen von Grund auf neu zu bauen, hat CYC versucht, und 30 Jahre haben die Grenzen dieses Ansatzes bewiesen.

Wikidata ist der Wortschatz der Welt — mit ueber 100 Millionen Entitaeten, mehr als 10.000 Eigenschaften und Milliarden von Aussagen.
Millionen von Editoren haben ihn ueber 10 Jahre aufgebaut.

GEULs SIDX-Codebuch wird aus Wikidata extrahiert.
Die Instanzhaeufigkeiten von P31 bestimmen die Bitzuweisung,
und die P279-Hierarchie bildet das Geruest des Bitbaums.

Wikidata ist ein Woerterbuch; GEUL ist eine Sprache.
Ein Woerterbuch liefert Woerter; eine Sprache liefert Grammatik.
GEUL baut Behauptungsstruktur, Verbqualifikation, 16-Bit-Komprimierung und eine Kontextpipeline auf dem Wortschatz von Wikidata auf.

GEUL lehnt Wikidata nicht ab.
Es steht darauf.
