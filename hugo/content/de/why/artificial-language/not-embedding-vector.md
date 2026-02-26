---
title: "Warum Embedding-Vektoren nicht ausreichen"
weight: 11
date: 2026-02-26T12:00:18+09:00
lastmod: 2026-02-26T12:00:18+09:00
tags: ["Embedding", "Vektor", "Whitebox"]
summary: "Das Umordnen von Embedding-Vektoren zerstört das Modell. Die Zerstörung zu vermeiden bedeutet, das Modell von Grund auf neu zu bauen. Was wir brauchen, ist nicht Transparenz innerhalb der Blackbox, sondern eine transparente Schicht außerhalb."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Vektoren eignen sich hervorragend für Berechnungen, lassen sich aber nicht interpretieren. Man kann das Innere einer Blackbox nicht transparent machen.

---

## Embedding-Vektoren sind eine bemerkenswerte Technologie

„König - Mann + Frau = Königin."

Als word2vec dies zeigte, staunte die Welt.
Stellt man Wörter als Vektoren mit Hunderten von Dimensionen dar,
treten semantische Beziehungen als Vektoroperationen zutage.

Embedding-Vektoren sind das Fundament von LLMs.
Alles in einem Transformer ist Vektorberechnung.
Tokens werden zu Vektoren.
Attention berechnet die Ähnlichkeit zwischen Vektoren.
Ausgaben werden von Vektoren zurück in Tokens umgewandelt.

Ähnliche Bedeutungen sind nahe Vektoren.
Unterschiedliche Bedeutungen sind entfernte Vektoren.
Suche ist Vektorähnlichkeitsberechnung.
Klassifikation ist das Setzen von Grenzen im Vektorraum.

Ohne Embedding-Vektoren würde die heutige KI nicht existieren.

Warum also nicht einfach Embedding-Vektoren zur Wissensdarstellung verwenden?
Sie direkt ausrichten, strukturieren, interpretierbar machen.

Das funktioniert nicht.
Der sicherste Weg, dies zu erfahren, ist es auszuprobieren.

---

## AILEV: Wir haben es versucht

Das GEUL-Projekt begann ursprünglich unter dem Namen AILEV.

AI Language Embedding Vector.

Der Name selbst erklärte das Ziel:
eine KI-Sprache, die Embedding-Vektoren direkt manipuliert.

Das Konzept war Folgendes:

Bedeutung mit 512-dimensionalen Vektoren darstellen.
Segmenten des Vektors Rollen zuweisen.
Die ersten 128 Dimensionen für Entitäten, die nächsten 128 für Relationen, die nächsten 128 für Eigenschaften, der Rest für Metadaten.
So wie RGBA Farbe in vier Kanäle zerlegt, Bedeutung in dimensionale Segmente zerlegen.

BERT trainieren, um natürliche Sprache in diese strukturierten Vektoren umzuwandeln.
Bei der Eingabe „Seoul ist die Hauptstadt von Korea"
erzeugt das Entitätssegment den Seoul-Vektor, das Relationssegment den Hauptstadt-Vektor, das Eigenschaftssegment den Korea-Vektor.

Da es Vektoren sind, ist Berechnung möglich.
Ähnlichkeitssuche ist möglich.
Dimensionsreduktion ermöglicht elegante Degradation.
Von 512 auf 256 Dimensionen sinkt die Präzision, aber die Kernbedeutung bleibt erhalten.

Es war elegant. In der Theorie.

---

## Warum es scheitert

### Willkürliches Umordnen von Vektoren zerstört das Modell

Die Embedding-Vektoren eines LLM sind das Produkt des Trainings.

Nach dem Lesen von Milliarden Texten
optimiert das Modell seine internen Repräsentationen selbst.
Was jede Dimension bedeutet, hat das Modell entschieden.
Nicht ein Mensch.

Was passiert, wenn man festlegt: „Die ersten 128 Dimensionen sind für Entitäten"?

Im Vektorraum, den das Modell gelernt hat,
befinden sich Entitätsinformationen nicht in den ersten 128 Dimensionen.
Sie sind über alle 768 Dimensionen verteilt.
Relationsinformationen, Eigenschaftsinformationen, Tempusinformationen — alles vermischt.

Dies ist kein Designfehler, sondern die Natur des Lernens.
Backpropagation findet
die für die Aufgabe optimale Vektoranordnung.
Nicht eine interpretierbare Anordnung.
Optimal und interpretierbar sind nicht dasselbe.

Ordnet man Vektoren zwangsweise um — „Entitäten hier, Relationen dort" —
brechen die statistischen Beziehungen, die das Modell gelernt hat.
Die Leistung sinkt.

### Umordnen ohne Zerstörung bedeutet, das Modell neu zu bauen

Warum dann nicht von Anfang an mit der Einschränkung „die ersten 128 Dimensionen sind für Entitäten" trainieren?

Möglich. In der Theorie.
Aber das ist nicht das Ausrichten von Embedding-Vektoren.
Es ist das Entwerfen einer neuen Modellarchitektur.

Man braucht Trainingsdaten. Milliarden Tokens.
Man braucht Infrastruktur. Tausende GPUs.
Man braucht Zeit. Monate.
Und es gibt keine Garantie, dass das resultierende Modell so gut funktioniert wie bestehende LLMs.

Der Aufwand ist zu groß.

Das Problem „Vektoren ausrichten, um sie interpretierbar zu machen"
hat sich in „ein LLM von Grund auf neu bauen" verwandelt.
Das ist nicht die Lösung des Problems, sondern seine Vergrößerung.

### Interpretation ist unmöglich

Angenommen, es gelänge, einen strukturierten Vektor zu erstellen.
Ein 512-dimensionaler Vektor.
Sagen wir, die ersten 128 Dimensionen sind für Entitäten.

Das Entitätssegment hat den Wert `[0.23, -0.47, 0.81, 0.12, ...]`.

Wie weiß man, ob das „Samsung Electronics" oder „Hyundai Motor" ist?

Man muss den nächsten Vektor finden.
Man muss die Ähnlichkeit in einer Vektordatenbank berechnen.
Und man erhält eine probabilistische Antwort: „wahrscheinlich Samsung Electronics."

„Wahrscheinlich."

Vektoren sind von Natur aus kontinuierlich.
Zwischen den Vektoren von Samsung Electronics und SK Hynix
existieren unendlich viele Zwischenvektoren.
Was diese Zwischenvektoren bedeuten, weiß niemand.

Dies ist keine technische Einschränkung, sondern eine mathematische Wahrheit.
Diskrete Bedeutungen in einem kontinuierlichen Raum darzustellen
macht Grenzen unscharf.
Mehrdeutigkeit war [das Problem der natürlichen Sprache](/de/why/natural-language-hallucination/).
Man wechselte zu Vektoren, und die Mehrdeutigkeit kehrte zurück.

Nur die Form änderte sich.
In der natürlichen Sprache die Mehrdeutigkeit der Wörter.
In Vektoren die Mehrdeutigkeit der Koordinaten.

---

## Das Whitebox-Prinzip

Hier offenbart sich das grundlegende Designproblem.

Embedding-Vektoren sind eine Blackbox.
Betrachtet man einen 768-dimensionalen Vektor reeller Zahlen,
kann niemand erkennen, welche Information wo codiert ist.
Das Modell selbst kann es nicht erklären.

Dies ist keine unangenehme Eigenschaft, sondern ein ontologisches Merkmal.
Genau deshalb funktionieren Vektoren.
Weil sie Informationen auf eine Weise anordnen, die Menschen nicht entworfen haben,
funktionieren sie besser als alles, was Menschen entworfen hätten.
Nicht-Interpretierbarkeit ist kein Bug, sondern ein Feature.

Doch Wissen, das als KI-Kontext dient, verlangt das Gegenteil.

Man muss die Quelle kennen.
Man muss den Zeitpunkt kennen.
Man muss den Konfidenzgrad kennen.
Man muss wissen, worüber die Aussage handelt.
Man muss wissen, ob sich zwei Aussagen auf dieselbe Entität beziehen.

Jede Anforderung ist „muss wissen". Jede Anforderung verlangt Interpretierbarkeit.

Whitebox-Anforderungen mit einem Blackbox-Vektor zu erfüllen
ist ein Widerspruch.

---

## Die Logik der Wende

Die Wende von AILEV zu GEUL war kein Rückzug.
Es war eine Neudefinition des Problems.

**Ursprüngliches Problem:** LLMs sind Blackboxen. Machen wir das Innere transparent.
→ Machen wir Embedding-Vektoren durch Ausrichtung interpretierbar.
→ Ändert man die Vektoren, bricht das Modell.
→ Vermeidet man den Bruch, muss man das Modell neu bauen.
→ Sackgasse.

**Neudefiniertes Problem:** Das Innere der Blackbox muss nicht transparent werden. Bauen wir eine transparente Schicht außen.
→ Das Innere des LLM wird nicht angefasst.
→ Außerhalb des LLM wird ein interpretierbares Darstellungssystem geschaffen.
→ Das LLM kann dieses System lesen und schreiben. Denn es sind Tokens.
→ Eine künstliche Sprache.

Nicht Vektoren, sondern Sprache.
Nicht kontinuierlich, sondern diskret.
Nicht uninterpretierbar, sondern Interpretation als einziger Zweck.
Nicht innerhalb des Modells, sondern außerhalb.

Das „Embedding Vector" aus AILEV wurde gestrichen,
und GEUL — was „Schrift" bedeutet — trat an seine Stelle. Das ist der Grund.

---

## Vektoren für Berechnung, Sprache für Darstellung

Dies ist keine Ablehnung von Embedding-Vektoren.

Vektoren sind für Berechnungen optimiert.
Ähnlichkeitssuche, Clustering, Klassifikation, Retrieval.
Sprache kann nicht ersetzen, was Vektoren leisten.

Sprache ist für Darstellung optimiert.
Entitätsidentität, Relationsbeschreibung, eingebettete Metadaten, Interpretierbarkeit.
Vektoren können nicht ersetzen, was Sprache leistet.

Es sind Werkzeuge auf verschiedenen Ebenen.

Innerhalb des LLM arbeiten Vektoren. Eine Blackbox. So soll es sein.
Außerhalb des LLM arbeitet Sprache. Eine Whitebox. So soll es sein.

Das Problem begann mit der Verwechslung dieser beiden Ebenen.
Man versuchte, Vektoren die Arbeit der Sprache tun zu lassen.
Man versuchte, einer Blackbox die Rolle einer Whitebox zuzuweisen.

Jedes hat seinen Platz.

---

## Zusammenfassung

Embedding-Vektoren sind das Fundament von LLMs und eine bemerkenswerte Technologie.
Als Mittel der Wissensdarstellung haben sie jedoch fundamentale Grenzen.

GEUL begann als AILEV (AI Language Embedding Vector).
Das Ziel war, Vektoren direkt auszurichten und interpretierbar zu machen.
Es scheiterte. Aus zwei Gründen.

Willkürliches Ausrichten von Vektoren zerstört die Beziehungen, die das Modell gelernt hat.
Ausrichten ohne Zerstörung bedeutet, das Modell von Grund auf neu zu bauen. Der Aufwand ist zu groß.

Und selbst bei Erfolg können Vektoren nicht interpretiert werden.
Im kontinuierlichen Raum sind die Grenzen diskreter Bedeutung unscharf.
Man kann einer Blackbox nicht die Rolle einer Whitebox zuweisen.

Die Logik der Wende:
Man versuchte, das Innere der Blackbox transparent zu machen.
Das Innere anfassen heißt es zerstören.
Stattdessen das Innere unberührt lassen und eine transparente Schicht außen bauen.
Nicht Vektoren, sondern Sprache. Nicht innerhalb des Modells, sondern außerhalb.

Vektoren für Berechnung, Sprache für Darstellung.
Jedes hat seinen Platz.
