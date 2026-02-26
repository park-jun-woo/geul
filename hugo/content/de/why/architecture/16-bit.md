---
title: "Warum 16-Bit?"
weight: 16
date: 2026-02-26T12:00:04+09:00
lastmod: 2026-02-26T12:00:04+09:00
tags: ["16-Bit", "binaer", "Stream"]
summary: "Ein einziges Wort durchdringt drei Welten"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Ein einziges Wort durchdringt drei Welten

---

## Drei Welten

Es gibt drei Welten in der Informatik.

**Die Welt der Netzwerke.**
Daten fliessen als Byte-Streams.
Bytes kommen ueber TCP-Sockets herein, und Bytes gehen hinaus.
Das Vokabular des Netzwerkingenieurs: Pakete, Header und Nutzlasten.

**Die Welt der Speicherung.**
Daten werden in Dateiformaten persistiert.
Auf die Festplatte geschrieben, von der Festplatte gelesen.
Das Vokabular des Speicheringenieurs: Bloecke, Offsets und Alignment.

**Die Welt der KI.**
Daten werden als Token-Sequenzen verarbeitet.
LLMs nehmen Tokens auf und produzieren Tokens.
Das Vokabular des KI-Ingenieurs: Embeddings, Attention und Kontext.

Diese drei Welten sprechen unterschiedliche Sprachen.
Und zwischen ihnen ist immer eine Uebersetzung erforderlich.

---

## Die Kosten der Uebersetzung

Verfolgen wir den Weg, den Daten in einem modernen KI-System zuruecklegen.

Wissen ist in einer Datei gespeichert. Als JSON oder Klartext.

Um dies an eine KI zu uebermitteln:

1. Die Datei oeffnen und den Text lesen.
2. Den Text parsen. Wenn es JSON ist, die Struktur interpretieren und Felder extrahieren.
3. Den extrahierten Text in einen Tokenizer einspeisen.
4. Der Tokenizer wandelt den Text in eine Sequenz von Token-IDs um.
5. Die Token-Sequenz wird in das LLM eingespeist.

Wenn die KI eine Antwort generiert:

6. Das LLM gibt eine Token-Sequenz aus.
7. Die Tokens zurueck in Text dekodieren.
8. Den Text in ein strukturiertes Format serialisieren.
9. Die serialisierten Daten in eine Datei schreiben.

Eine einfache "Lese- und Schreib"-Operation erfordert neun Schritte.

Jeder Schritt kostet Zeit.
Jeder Schritt kostet Speicher.
Jeder Schritt birgt das Risiko eines Informationsverlusts.

Die Schritte 3 und 4 -- der Tokenisierungsprozess -- sind notorisch problematisch.
Weil die Wortgrenzen natuerlicher Sprache nicht mit den Token-Grenzen des Tokenizers uebereinstimmen,
kann ein Eigenname wie "Yi Sun-sin" in willkuerliche Fragmente zerteilt werden,
oder eine einzelne semantische Einheit wird ueber mehrere Tokens verstreut.

Dies ist der Preis dafuer, dass drei Welten unterschiedliche Sprachen sprechen.

---

## Was waere, wenn eine einzige Einheit alle drei Welten durchdringen wuerde?

In dieser Sprache ist ein Wort 16 Bit (2 Bytes).

Ein einziges 16-Bit-Wort ist gleichzeitig drei Dinge.

**Eine Einheit des Byte-Streams.**
16-Bit-Woerter kommen in einem kontinuierlichen Fluss ueber das Netzwerk.
Big Endian. Auf 2-Byte-Grenzen ausgerichtet. Kein zusaetzliches Parsen erforderlich.
Einfach in der Reihenfolge lesen, in der sie ankommen.

**Eine Einheit des Dateiformats.**
Den Stream direkt auf die Festplatte schreiben, und das ist die Datei.
Die Bytes direkt von der Festplatte lesen und ueber das Netzwerk senden, und das ist der Stream.
Keine Serialisierung. Keine Deserialisierung.

**Eine Einheit des LLM-Tokens.**
16 Bit = 65.536 verschiedene Symbole.
Moderne LLM-Vokabulargroessen liegen generell zwischen 50.000 und 100.000.
Modelle der GPT-Familie verwenden etwa 50.000; koreanisch-spezialisierte Modelle etwa 100.000.
65.536 liegt genau in der Mitte dieses Bereichs.
Ein 16-Bit-Wort wird ein LLM-Token.

Drei Welten teilen dieselbe Einheit.
Die Uebersetzung verschwindet.

---

## Null Konvertierung, null Verlust, null Overhead

Sehen wir, was das konkret bedeutet.

**Konventioneller Ansatz: 9 Schritte**

```
[Datei] -> Lesen -> Parsen -> Text extrahieren -> Tokenisieren -> [LLM]
[LLM] -> Dekodieren -> Serialisieren -> Schreiben -> [Datei]
```

**Binaer-Stream-Ansatz: 1 Schritt**

```
[Datei/Stream] -> [LLM]
[LLM] -> [Datei/Stream]
```

Eine Datei lesen, und es ist bereits eine Token-Sequenz.
Die vom LLM erzeugte Token-Sequenz ausgeben, und es ist bereits eine Datei.
Einen Stream aus dem Netzwerk nehmen und direkt in das LLM einspeisen.

Null Konvertierung. Null Parsen. Null Tokenisierung.
Null Verlust. Null Overhead.

---

## Warum nicht 8-Bit?

8 Bit ergeben 256 verschiedene Symbole.

256 Symbole sind bei weitem zu wenig, um die Welt darzustellen.
Weist man das Alphabet, Ziffern und grundlegende Satzzeichen zu, ist die Haelfte des Raums bereits verbraucht.

Wenn man 8 Bit als grundlegende Einheit verwendet,
erfordern die meisten bedeutungsvollen Tokens 2 oder mehr Bytes.
Das erzwingt eine Kodierung variabler Laenge,
und variable Laenge macht das Parsen komplex.

Als Byte-Stream-Einheit ausreichend,
aber als Token-Einheit unzureichend.

---

## Warum nicht 32-Bit?

32 Bit ergeben etwa 4,3 Milliarden verschiedene Symbole.

Die Ausdruckskraft ist mehr als ausreichend -- weit mehr als noetig.
Aber das Problem ist die Effizienz.

Das am haeufigsten vorkommende Paket in diesem Format ist der Tiny Verb Edge mit 2 Woertern.
Bei 16 Bit pro Wort sind das 4 Bytes. Bei 32 Bit pro Wort werden es 8 Bytes.
Das haeufigste Paket verdoppelt sich in der Groesse.

Aus Sicht des LLM gibt es ebenfalls ein Problem.
Wenn ein einzelner Token 32 Bit hat, passt nur die Haelfte der Tokens in dasselbe Kontextfenster.
Angesichts der Tatsache, dass die LLM-Kontextlaenge heute eine knappe Ressource ist,
wird der Platz, den ein Token einnimmt, im Verhaeltnis zur getragenen Information ineffizient.

Ein 32-Bit-Wort ist als Token fuer diese Sprache ueberdimensioniert.

---

## Warum nicht variable Laenge?

UTF-8 ist eine Kodierung variabler Laenge.
Die Zeichenlaenge reicht von 1 Byte bis 4 Bytes je nach Zeichen.

Dies bietet Vorteile bei der Speichereffizienz,
fuehrt aber eine fatale Schwaeche bei der Verarbeitungseffizienz ein.

Um das n-te Zeichen zu finden, muss man vom Anfang zaehlen.
Wahlfreier Zugriff ist unmoeglich.
Parallele SIMD-Verarbeitung wird schwierig.

Diese Sprache verwendet 16-Bit-Woerter fester Breite als grundlegende Einheit.
Die Position des n-ten Wortes ist immer n * 2 Bytes.
Wahlfreier Zugriff ist O(1).
SIMD kann mehrere Woerter in einer einzigen Instruktion vergleichen.
GPUs koennen Milliarden von Woertern parallel scannen.

Dennoch ist auf Paketebene variable Laenge weiterhin erlaubt.
Ein Tiny Verb Edge hat 2 Woerter; ein Event6 Edge kann bis zu 8 Woerter haben.
Die Wort-Einheit ist fest, aber die Paket-Einheit ist flexibel.

Die Verarbeitungseffizienz fester Breite kombiniert mit der Ausdruckskraft variabler Laenge.
Das 16-Bit-Wort erreicht beides gleichzeitig.

---

## Der Weg, den Unicode bewiesen hat

Unicode ist der erfolgreichste Kodierungsstandard, den die Menschheit je geschaffen hat.

Die Grundeinheit von UTF-16 ist 16 Bit (2 Bytes).
Sie stellt die 65.536 Zeichen der Basic Multilingual Plane (BMP) in einem einzigen Wort dar
und erweitert auf Zeichen darueber hinaus durch Surrogatpaare (2 Woerter = 4 Bytes).

Wir folgen einfach dieser bewaehrten Struktur.

65.536 grundlegende semantische Primitive in einem einzigen Wort darstellen
und zusammengesetzte Pakete ueber mehrere Woerter erweitern.

So wie Unicode jedes Zeichen der Welt
auf der Grundeinheit "ein Zeichen = 2 Bytes" ausdrueckt,
drueckt diese Sprache jedes Element des KI-Denkens
auf der Grundeinheit "ein Wort = 2 Bytes" aus.

---

## Abwaertskompatibilitaet und Aufwaertserweiterung

Eine weitere Staerke von 16 Bit ist das Alignment.

16 ist ein Vielfaches von 8, ein Teiler von 32, ein Teiler von 64 und ein Teiler von 128.

Das bedeutet, dass das Alignment niemals bricht, egal in welche Richtung man erweitert.

Was wenn sich die Transformer-Architektur in Zukunft aendert
und Tokens 32 Bit werden?
Zwei 16-Bit-Woerter ergeben einen Token. Keine Alignment-Probleme.

Was ist mit 64 Bit?
Vier 16-Bit-Woerter ergeben einen Token. Immer noch keine Alignment-Probleme.

Umgekehrt: Was wenn ein eingebettetes 8-Bit-System dieses Format verarbeitet?
Einfach jedes 16-Bit-Wort als High-Byte und Low-Byte lesen.

Abwaertskompatibilitaet muss absolut aufrechterhalten werden.
Das 16-Bit-Wort garantiert dies auf physischer Ebene.

Wir koennen die Wortgroesse zukuenftiger Intelligenzen nicht vorhersagen,
aber das Vielfach-Alignment von 16 Bit garantiert Kompatibilitaet mit jeder Groesse.

---

## Die Dreifachstruktur

Fassen wir zusammen.

Ein einziges 16-Bit-Wort ist gleichzeitig drei Dinge.

| Welt | Rolle eines Wortes |
|-------|---------------------|
| Netzwerk | Einheit des Byte-Streams |
| Speicher | Einheit des Dateiformats |
| KI | Einheit des LLM-Tokens |

Eine einzige Einheit durchdringt alle drei Welten.

Einen Stream unveraendert speichern, und es ist eine Datei.
Eine Datei unveraendert lesen, und es sind Tokens.
Tokens unveraendert senden, und es ist ein Stream.

Keine Konvertierung.
Keine Uebersetzung.
Kein Verlust.

Deshalb 16-Bit.
Nicht 8-Bit, nicht 32-Bit, nicht variable Laenge.
Die Zahl, die praezise an der Schnittstelle dreier Welten liegt.

16.
