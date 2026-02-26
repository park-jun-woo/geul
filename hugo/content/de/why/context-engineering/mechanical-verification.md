---
title: "Warum mechanische Verifikation notwendig ist"
weight: 4
date: 2026-02-26T12:00:10+09:00
lastmod: 2026-02-26T12:00:10+09:00
tags: ["Verifikation", "Spezifikation", "Compiler"]
summary: "Natuerliche Sprache kennt das Konzept eines ungueltigen Satzes nicht"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Natuerliche Sprache kennt das Konzept eines "ungueltigen Satzes" nicht.

---

## Niemand prueft, was in den Kontext gelangt

Schauen Sie sich an, wie Informationen in aktuellen LLM-Pipelines in den Kontext gelangen.

RAG liefert Chunks.
Ein Agent empfaengt API-Antworten.
Vorherige Gespraeche sammeln sich im Verlauf.
Ein Benutzer laedt ein Dokument hoch.

All das gelangt in das Kontextfenster.
Ohne Pruefung.

Warum gibt es keine Pruefung?
Weil natuerliche Sprache kein Konzept von "ungueltig" hat.

---

## Natuerliche Sprache akzeptiert jede Zeichenkette

In der Programmierung gibt es so etwas wie einen Syntaxfehler.

```python
def calculate(x, y
    return x + y
```

Die Klammer ist nicht geschlossen. Es wird vor der Ausfuehrung abgelehnt.
Code kann eindeutig als "dies ist kein gueltiger Code" deklariert werden, bevor er ausgefuehrt, bevor er ueberhaupt gelesen wird.

Natuerliche Sprache hat so etwas nicht.

"Er ging zur Bank."
Grammatisch einwandfrei.
Man kann nicht erkennen, wer ging, welche Bank oder warum,
aber nichts verstoesst gegen die Grammatikregeln der natuerlichen Sprache.

"Verkaufsbericht fuer den 45. des 13. Monats, 2024."
Es gibt keinen 13. Monat und keinen 45. Tag.
Dennoch verstoesst nichts gegen die Grammatikregeln der natuerlichen Sprache.
Es ist ein grammatisch gueltiger Satz.

"Quelle: unbekannt. Konfidenz: unbekannt. Datum: unbekannt. Samsung Electronics' Marktkapitalisierung betraegt 1.200 Billionen Won."
Die Quelle ist unbekannt, die Konfidenz ist unbekannt, das Bezugsdatum ist unbekannt.
Dennoch verstoesst nichts gegen die Grammatikregeln der natuerlichen Sprache.

Natuerliche Sprache akzeptiert alles.
Ein ungueltiger natuerlichsprachlicher Satz existiert strukturell nicht.
Daher gibt es kein mechanisches Kriterium fuer das "Ablehnen" von Informationen, die in natuerlicher Sprache ausgedrueckt sind.

---

## Was es fuer mechanische Verifikation braucht

Schauen Sie sich den Go-Compiler an.

Go verweigert die Kompilierung, wenn es einen ungenutzten Import gibt.
Selbst wenn der Code einwandfrei funktioniert.
Selbst wenn an der Logik nichts falsch ist.
Er verweigert allein deshalb, weil eine Import-Zeile ungenutzt ist.

Das ist mechanische Verifikation.

Mechanische Verifikation hat drei Eigenschaften.

**Sie ist deterministisch.** Das Ergebnis ist Ja oder Nein. Keine Wahrscheinlichkeit. Es gibt kein "es ist wahrscheinlich in Ordnung." Gueltig oder ungueltig.

**Sie ist guenstig.** Kein LLM-Aufruf noetig. Zeichenkettenvergleich, Feldexistenzpruefung, Wertebereichspruefung. CPU-Operationen im Nanosekundenbereich.

**Sie liest keine Bedeutung.** Sie beurteilt nicht, ob der Inhalt wahr oder falsch ist. Sie prueft nur, ob das Format der Spezifikation entspricht. Sie weiss nicht, ob "Samsung Electronics' Marktkapitalisierung betraegt 1.200 Billionen Won" stimmt. Aber sie weiss, ob das Quellenfeld leer ist.

Damit diese drei Dinge moeglich sind, gibt es eine Voraussetzung.
Informationen muessen eine Spezifikation haben.

Wenn es eine Spezifikation gibt, sind Verstoesse definiert.
Wenn Verstoesse definiert sind, ist Ablehnung moeglich.
Wenn Ablehnung moeglich ist, existiert Verifikation.

Natuerliche Sprache hat keine Spezifikation, also gibt es keine Verstoesse.
Keine Verstoesse bedeutet keine Ablehnung.
Keine Ablehnung bedeutet keine Verifikation.

---

## Warum Vor-Kontext-Verifikation noetig ist

Das Kontextfenster ist endlich.

Ob 128K Token oder 1M Token, es ist endlich.
Die Qualitaet der Informationen, die in einen endlichen Raum gelangen, bestimmt die Qualitaet der Ausgabe.

Doch in aktuellen Pipelines
findet die Qualitaetsbeurteilung erst statt, nachdem Informationen in den Kontext gelangt sind.
Man erwartet, dass das LLM sie liest, beurteilt und selbst zu dem Schluss kommt: "Diese Information ist schwer vertrauenswuerdig."

Das ist in dreifacher Hinsicht falsch.

**Es ist teuer.** Man nutzt LLM-Inferenzkosten fuer Formatpruefungen. Man laesst ein Modell mit Milliarden Parametern laufen, um Chunks ohne Quelle herauszufiltern. Man nutzt probabilistisches Schlussfolgern fuer eine Aufgabe, die das Pruefen eines einzelnen Feldes erfordert.

**Es ist unzuverlaessig.** Es gibt keine Garantie, dass das LLM Informationen ohne Quelle immer ignoriert. Tatsaechlich neigt das LLM dazu, Informationen zu verwenden, sobald sie im Kontext stehen. Vom Modell zu erwarten, dass es etwas ignoriert, das man in den Kontext gelegt hat, ist ein Widerspruch.

**Es ist zu spaet.** Der Fensterplatz ist bereits verbraucht. Wenn 5 Chunks ohne Quelle jeweils 200 Token belegen, sind 1.000 Token verschwendet. Selbst wenn sie herausgefiltert werden, ist dieser Platz bereits belegt.

Mechanische Verifikation kommt vor all dem.
Bevor etwas in den Kontext gelangt.
Bevor das LLM es liest.
Bevor das Fenster verbraucht wird.

---

## Was wird verifiziert

Mechanische Verifikation prueft nicht die Wahrheit des Inhalts, sondern die Konformitaet mit einer Formatspezifikation.

Konkret folgendes:

**Strukturelle Vollstaendigkeit.** Existieren die erforderlichen Felder? Hat die Kante ein Subjekt und ein Objekt? Fehlt etwas?

**Bezeichner-Gueltigkeit.** Existiert der referenzierte Knoten? Zeigt das, was als "Samsung Electronics" geschrieben ist, tatsaechlich auf eine definierte Entitaet? Haengt die Referenz ins Leere?

**Typkonformitaet.** Steht ein Datum im Datumsfeld? Steht eine Zahl im Zahlenfeld? "Der 45. des 13. Monats, 2024" wird hier abgefangen.

**Metadaten-Vorhandensein.** Gibt es ein Quellenfeld? Gibt es ein Zeitfeld? Ist die Konfidenz angegeben? Wenn nicht: ablehnen, als fehlend markieren oder einen Standardwert zuweisen.

**Referentielle Integritaet.** Existiert der Knoten, auf den die Kante zeigt, tatsaechlich? Wird auf einen geloeschten Knoten verwiesen?

Diese Pruefungen haben eines gemeinsam.
Alle koennen durchgefuehrt werden, ohne den Inhalt zu lesen.
Man weiss nicht, ob "Samsung Electronics' Marktkapitalisierung betraegt 1.200 Billionen Won" stimmt.
Aber man weiss, ob fuer diese Aussage eine Quelle angegeben ist.
Man weiss, ob fuer diese Aussage eine Zeit erfasst ist.
Man weiss, ob das Format dieser Aussage der Spezifikation entspricht.

---

## Guenstig kommt zuerst

In einer Context-Engineering-Pipeline haben Pruefungen eine Reihenfolge.

**Mechanische Verifikation**: Spezifikationskonformitaet. Kosten nahe null. Deterministisch.
**Semantische Filterung**: Relevanz-, Vertrauenswuerdigkeits-, Nuetzlichkeitsbeurteilung. Hohe Kosten. Probabilistisch.
**Konsistenzpruefung**: Widersprueche zwischen ausgewaehlten Informationen. Noch hoehere Kosten. Erfordert Schlussfolgern.

Wenn man sie von guenstigsten zu teuersten anordnet,
hat die teure Pruefung weniger zu verarbeiten.

Wenn mechanische Verifikation 30 % der Aussagen ohne Quelle herausfiltert,
muss die semantische Filterung nur noch 70 % verarbeiten.
Wenn die semantische Filterung das Irrelevante entfernt,
verarbeitet die Konsistenzpruefung eine noch kleinere Menge.

Das ist dasselbe Prinzip wie bei der Datenbankabfrageoptimierung.
Index-filterbare Bedingungen in der WHERE-Klausel zuerst anwenden.
Full-Scan-Bedingungen danach.
Wenn Guenstiges zuerst kommt, sinkt die Last fuer den teuren Teil.

Umgekehrt:
Wenn man die teure Pruefung zuerst und die guenstige danach durchfuehrt,
entdeckt man Formatfehler erst, nachdem man die Kosten bereits aufgewendet hat.
Man analysiert die Bedeutung einer Aussage, die auf einen nicht existierenden Knoten verweist,
nur um danach festzustellen, dass die Referenz ungueltig ist.

---

## Diese Reihenfolge ist in einer natuerlichsprachlichen Pipeline unmoeglich

Natuerliche Sprache hat keine Spezifikation, also ist mechanische Verifikation unmoeglich.
Da mechanische Verifikation unmoeglich ist, existiert die guenstigste Pruefung nicht.

Folglich ist jede Pruefung eine semantische Pruefung.
Jede Pruefung erfordert ein LLM.
Jede Pruefung ist teuer.

"Hat dieser Chunk eine Quelle?" -- Das LLM muss ihn lesen.
"Ist der Zeitbezug dieses Chunks angemessen?" -- Das LLM muss ihn lesen.
"Ist das Format dieses Chunks korrekt?" -- Natuerliche Sprache hat kein Format, also ergibt die Frage keinen Sinn.

Das ist die Realitaet des aktuellen Context Engineering.
Selbst die einfachste Pruefung wird mit dem teuersten Werkzeug durchgefuehrt.
Eine Aufgabe, die mit einem Zeichenkettenvergleich enden koennte, wird von einer Inferenz-Engine bearbeitet.

---

## Voraussetzungen fuer Verifikation

Damit mechanische Verifikation existieren kann, werden drei Dinge benoetigt.

**Eine Spezifikation.** Das Format, dem Informationen folgen muessen, muss definiert sein. Welche Felder erforderlich sind, welche Werte erlaubt sind, welche Referenzen gueltig sind. Ohne Spezifikation koennen Verstoesse nicht definiert werden.

**Formalisierung.** Informationen muessen in dem Format ausgedrueckt werden, das die Spezifikation verlangt. Nicht als natuerlichsprachliche Saetze, sondern kodiert in der Struktur, die die Spezifikation fordert. Informationen, die nicht formalisiert sind, koennen nicht geprueft werden.

**Die Macht der Ablehnung.** Es muss moeglich sein, Informationen, die nicht konform sind, tatsaechlich abzulehnen. Wenn man prueft, aber immer durchlaesst, ist es keine Verifikation. Ungueltige Informationen muessen daran gehindert werden, in den Kontext zu gelangen.

Diese drei Dinge sind in Programmiersprachen selbstverstaendlich.
Es gibt eine Spezifikation namens Grammatik, ein Format namens Code und eine Ablehnungsmacht namens Compiler.

In natuerlicher Sprache fehlen alle drei.
Grammatik ist keine Formatspezifikation, sondern eine Konvention.
Saetze sind keine strukturierten Formate, sondern Freitext.
Das Konzept "ungueltiger natuerlicher Sprache" existiert nicht, also gibt es nichts abzulehnen.

Um mechanische Verifikation in Context Engineering einzufuehren,
muss sich die Darstellung von Informationen selbst aendern.

---

## Zusammenfassung

In der aktuellen Kontext-Pipeline gelangen Informationen ohne Pruefung in den Kontext.
Weil natuerliche Sprache kein Konzept eines "ungueltigen Satzes" kennt.

Mechanische Verifikation prueft nicht die Wahrheit des Inhalts, sondern die Konformitaet mit einer Formatspezifikation.
Strukturelle Vollstaendigkeit, Bezeichner-Gueltigkeit, Typkonformitaet, Metadaten-Vorhandensein, referentielle Integritaet.
Deterministisch, guenstig, und sie liest keine Bedeutung.

In der Pipeline muessen guenstige Pruefungen zuerst kommen.
Wenn mechanische Verifikation Formatfehler herausfiltert,
haben die teuren semantischen Beurteilungen weniger zu verarbeiten.

Natuerliche Sprache hat keine Spezifikation, also ist diese Pruefung unmoeglich.
Jede Pruefung wird zur semantischen Pruefung, und jede Pruefung ist teuer.

Damit mechanische Verifikation moeglich ist,
braucht es eine Spezifikation, Formalisierung und die Macht der Ablehnung.
Die Darstellung von Informationen selbst muss sich aendern.
