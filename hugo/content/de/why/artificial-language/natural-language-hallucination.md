---
title: "Warum erzeugt natuerliche Sprache Halluzinationen?"
weight: 8
date: 2026-02-26T12:00:16+09:00
lastmod: 2026-02-26T12:00:16+09:00
tags: ["natuerliche Sprache", "Halluzination", "Mehrdeutigkeit"]
summary: "Halluzination ist kein LLM-Bug — sie ist eine strukturelle Unvermeidlichkeit aus vier Maengeln natuerlicher Sprache: Mehrdeutigkeit, fehlende Quelle, fehlende Konfidenz und fehlender Zeitkontext. Groessere Modelle loesen das nicht."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Halluzination ist kein Bug. Sie ist eine strukturelle Unvermeidlichkeit, solange wir natuerliche Sprache verwenden.

---

## Das Wunder der natuerlichen Sprache

Vor 100.000 Jahren erschien die gesprochene Sprache. Die sozialen Beziehungen, die Primaten durch gegenseitiges Lausen aufrechterhalten konnten, waren auf etwa 150 Individuen beschraenkt. Sprache durchbrach diese Grenze. Sobald eine Person gleichzeitig zu vielen sprechen konnte, wurde eine neue Gesellschaftsgroesse moeglich --- der Stamm.

Vor 10.000 Jahren schuf die Landwirtschaft Nahrungsueberschuesse, und Menschen versammelten sich an einem Ort, um Staedte zu bilden. Vor 5.000 Jahren drueckte jemand in Mesopotamien keilfoermige Zeichen in eine feuchte Tontafel. Es ging um die Erfassung von Getreideinventaren. Die Geburt der Schrift. Gesprochenes verfliegt, aber Aufzeichnungen bestehen. Sobald Aufzeichnungen bestanden, wurde Buerokratie moeglich, Recht wurde moeglich, der Staat wurde moeglich.

Gesprochene Sprache schuf den Stamm. Schrift schuf den Staat.

Natuerliche Sprache ist die groesste Technologie, die die Menschheit je geschaffen hat. Nicht die Entdeckung des Feuers, nicht die Erfindung des Rads, nicht die Erfindung des Halbleiters. Was all das ermoeglicht hat, war natuerliche Sprache. Weil natuerliche Sprache existierte, konnte Wissen uebertragen werden, konnte Kooperation stattfinden, und die Gedanken der Toten konnten von den Lebenden geerbt werden. Zehntausende Jahre lang war natuerliche Sprache das Medium der gesamten menschlichen Zivilisation.

Und jetzt ist diese grosse natuerliche Sprache zum Flaschenhals des KI-Zeitalters geworden.

---

## Das Missverstaendnis namens Halluzination

Wenn KI etwas Falsches sagt, nennen wir es "Halluzination".

Dieser Name traegt Implikationen.
Die Implikation, dass Halluzination abnormal ist.
Die Implikation, dass sie behoben werden kann.
Die Implikation, dass ein besseres Modell sie loesen wird.

Das ist ein Missverstaendnis.

Halluzination ist kein Bug von LLMs.
Halluzination ist eine strukturelle Unvermeidlichkeit, die nicht vermieden werden kann,
solange natuerliche Sprache als Denksprache der KI verwendet wird.

Egal wie sehr man das Modell skaliert,
egal wie sehr man die Daten erweitert,
egal wie verfeinert das RLHF ist,
solange natuerliche Sprache Eingabe und natuerliche Sprache Ausgabe ist,
wird Halluzination nicht verschwinden.

Lassen Sie mich erklaeren warum.

---

## Die vier strukturellen Maengel der natuerlichen Sprache

Natuerliche Sprache hat sich fuer die Kommunikation zwischen Menschen entwickelt.
Die vier Eigenschaften, die sie dabei erwarb,
werden zu fatalen Maengeln beim KI-Denken.

---

### Mangel 1: Mehrdeutigkeit

"He went to the bank."

Ist "bank" ein Finanzinstitut oder ein Flussufer?
Wer ist "he"?
Wann ist er gegangen?

Menschen loesen das mit Kontext.
Der Gespraechsverlauf, der Gesichtsausdruck des Sprechers, gemeinsames Hintergrundwissen.

KI hat nur Text.
Text allein kann Mehrdeutigkeit nicht vollstaendig aufloesen.
Wenn sie nicht aufgeloest werden kann, raet die KI.
Vermutungen sind manchmal falsch.
Wenn eine falsche Vermutung mit Zuversicht ausgegeben wird, ist das Halluzination.

---

### Mangel 2: Fehlende Quelle

"Yi Sun-sin besiegte 133 Schiffe mit nur 12."

Dieser Satz hat keine Quelle.

Wer hat diese Behauptung aufgestellt?
Welche historischen Aufzeichnungen stuetzen sie?
Gibt es gelehrte Meinungsverschiedenheiten ueber diese Zahlen?

Natuerliche Sprache hat keinen strukturellen Platz fuer Metadaten.
Um Quellen einzubeziehen, muss man den Satz verlaengern,
und Verlaengerung verdunkelt den Punkt.
Deshalb werden in den meisten natuerlichsprachlichen Saetzen Quellen weggelassen. Dieses Problem wird in [Warum Behauptungen, nicht Fakten?](/de/why/claims-not-facts/) ausfuehrlicher behandelt.

LLMs werden auf Milliarden solcher Saetze trainiert.
Behauptungen mit weggelassenen Quellen vermischen sich
in einer riesigen statistischen Suppe.

Die Grundlage fuer die Zahl "12" in dieser Suppe zurueckzuverfolgen
ist prinzipiell unmoeglich.
Da die Grundlage nicht zurueckverfolgt werden kann, koennen auch grundlose Zahlen fabriziert werden.
Das ist Halluzination.

---

### Mangel 3: Fehlende Konfidenz

"Die Erde ist rund."
"Dunkle Energie macht 68% des Universums aus."
"Morgen wird es regnen."

Die Konfidenzniveaus dieser drei Saetze sind voellig verschieden.

Der erste ist ein ueberwältigender Konsens.
Der zweite ist die aktuelle beste Schaetzung, aber die Theorie koennte sich aendern.
Der dritte ist eine probabilistische Vorhersage.

Doch in natuerlicher Sprache haben alle drei identische grammatische Strukturen.
Subjekt + Praedikat. Aussagesatz. Punkt.

Natuerliche Sprache kann nicht strukturell ausdruecken "wie sicher ist das".
Es gibt adverbiale Mittel wie "vielleicht", "fast sicher", "koennte",
aber sie sind optional, ungenau und werden meist weggelassen.

LLMs lernen alle Saetze auf identischem Konfidenzniveau.
Es gibt fuer das Modell keine Moeglichkeit, den Konfidenzunterschied
zwischen "die Erde ist rund" und "dunkle Energie ist 68%" intern zu unterscheiden.

So werden Schaetzungen als Fakten dargestellt,
Hypothesen als etablierte Sichtweisen,
und unsichere Dinge mit Sicherheit behauptet.
Das ist Halluzination.

---

### Mangel 4: Fehlender zeitlicher Kontext

"Der CEO von Tesla ist Elon Musk."

Stand wann?

Im Jahr 2024 ist das korrekt.
Im Jahr 2030, wer weiss.
Wenn der Zeitpunkt des Schreibens nicht angegeben ist,
kann die Gueltigkeitsdauer dieses Satzes nicht bestimmt werden.

Die meisten natuerlichsprachlichen Saetze lassen den zeitlichen Kontext weg.
Das "Praesens" kann "genau jetzt" bedeuten
oder "im Allgemeinen".

LLMs lernen Artikel von 2020 und Artikel von 2024 als dieselben Daten.
Da zeitliche Information nicht strukturell bewahrt wird,
stellen sie vergangene Fakten als gegenwaertig dar
oder mischen Informationen aus verschiedenen Zeitraeumen.
Das ist Halluzination.

---

## Die Zusammenfuehrung der vier Maengel

Halluzination eskaliert explosionsartig, wenn diese vier Maengel zusammentreffen.

Analysieren wir eine einzelne LLM-Ausgabe.

> "Yi Sun-sin vernichtete 330 japanische Schiffe mit 12 Schiffen,
> und starb spaeter in der Schlacht von Noryang mit den letzten Worten 'Verkuendet nicht meinen Tod.'"

In diesem Satz:

**Mehrdeutigkeit:** Was bedeutet "vernichtete" genau? Versenkt? In die Flucht geschlagen? Teilweise beschaedigt?

**Fehlende Quelle:** Was ist die Grundlage fuer die Zahlen 12 und 330? Verschiedene historische Aufzeichnungen nennen verschiedene Zahlen --- welcher wurde gefolgt?

**Fehlende Konfidenz:** Ist "Verkuendet nicht meinen Tod" ein historisch bestaetigtes letztes Testament, oder spaetere muendliche Ueberlieferung? Die Konfidenzniveaus beider sind verschieden, doch sie stehen im selben Aussagesatz.

**Fehlender zeitlicher Kontext:** Welchen Zeitpunkt des akademischen Konsenses spiegelt diese Information wider?

Das LLM fuellt all diese Mehrdeutigkeit mit "der plausibelsten Token-Sequenz".
Plausibilitaet ist nicht Genauigkeit.
Die Luecke zwischen beiden ist Halluzination.

---

## Warum groessere Modelle das nicht loesen koennen

"Wird Halluzination nicht abnehmen, wenn GPT-5 herauskommt?"

Sie wird abnehmen. Aber sie wird nicht verschwinden.

Groessere Modelle lernen komplexere Muster aus mehr Daten.
Die Genauigkeit der "Plausibilitaet" steigt also.

Aber das fundamentale Problem aendert sich nicht.

Solange die Eingabe natuerliche Sprache ist, bleibt Mehrdeutigkeit.
Solange Trainingsdaten natuerliche Sprache sind, bleiben Quellen verloren.
Solange die Ausgabe natuerliche Sprache ist, wird Konfidenz nicht ausgedrueckt.
Solange zeitliche Information in der Struktur fehlt, bleibt die Zeit durcheinander.

Selbst wenn man das Modell um das 100-fache skaliert,
wachsen die strukturellen Maengel der natuerlichen Sprache nicht um das 100-fache ---
aber sie erreichen auch nicht null.

Das ist kein Problem der Aufloesung. Es ist ein Problem des Mediums.

Egal wie sehr man die Aufloesung eines Schwarz-Weiss-Fotos erhoeht, Farbe erscheint nicht.
Egal wie sehr man die Praezision der natuerlichen Sprache erhoeht,
Quelle, Konfidenz und zeitlicher Kontext erscheinen nicht in der Struktur.

Wenn man Farbe will, braucht man Farbfilm.
Wenn man Halluzination eliminieren will, braucht man eine andere Sprache.

---

## Bedingungen fuer eine strukturelle Loesung

Um diese vier Maengel zu loesen, muss die Struktur der Sprache selbst anders sein.

**Mehrdeutigkeit --> Explizite Strukturierung.**
Wenn "He went to the bank" in eine strukturierte Sprache umgewandelt wird,
wird "he" zu einem bestimmten Entitaets-SIDX aufgeloest,
und "bank" wird zum SIDX entweder eines Finanzinstituts oder eines Flussufers aufgeloest.
Wenn es nicht aufgeloest werden kann, wird "ungeloest" explizit angegeben.
Entweder die Mehrdeutigkeit aufloesen oder die Tatsache aufzeichnen, dass sie mehrdeutig ist.

**Fehlende Quelle --> Eingebettete Quelle.**
Jede Narration schliesst strukturell eine Quell-Entitaet ein.
"Wer hat diese Behauptung aufgestellt" ist Teil der Narration.
Es ist nicht optional. Wenn das Feld leer ist, wird es als leer markiert.

**Fehlende Konfidenz --> Eingebettete Konfidenz.**
Jede Verb-Kante hat ein Konfidenzfeld.
"Sicher", "geschaetzt", "hypothetisch"
werden strukturell als Verb-Modifikatoren angegeben.

**Fehlender zeitlicher Kontext --> Eingebetteter zeitlicher Kontext.**
Jede Narration schliesst einen Zeitkontext ein.
"Stand wann ist diese Narration" wird immer angegeben.

Was in natuerlicher Sprache weggelassen wird,
existiert als Teil der Struktur in einer strukturierten Sprache.

Wenn Weglassen unmoeglich ist, schrumpft der Raum fuer Halluzination. [Warum Klaerung notwendig ist](/de/why/clarification/) erlaeutert dieses Prinzip.
Wenn man nicht ohne Grundlage sprechen kann, werden grundlose Aussagen nicht produziert.

---

## Das Ende der Halluzination liegt im Ersetzen der Sprache

Betrachten wir aktuelle Ansaetze zur Reduktion von Halluzination.

**RAG (Retrieval-Augmented Generation):** Ruft externe Dokumente ab und stellt sie als Kontext bereit. Wirksam, aber die abgerufenen Dokumente sind ebenfalls natuerliche Sprache, also folgen die Probleme von Mehrdeutigkeit, fehlenden Quellen und fehlender Konfidenz unveraendert. [Warum RAG nicht ausreicht](/de/why/rag-not-enough/) untersucht diese Einschraenkung im Detail.

**RLHF:** Trainiert das Modell, "ich weiss nicht" zu sagen, wenn es unsicher ist. Reduziert die Haeufigkeit von Halluzination, loest aber nicht das fundamentale Problem, dass natuerliche Sprache keine Konfidenzstruktur hat.

**Chain-of-Thought:** Zeichnet den Denkprozess in natuerlicher Sprache auf. Die Richtung ist richtig, aber das Medium der Aufzeichnung ist natuerliche Sprache, also erbt es dieselben Maengel.

Alle diese Ansaetze versuchen, Halluzination im Rahmen der natuerlichen Sprache abzumildern.
Sie funktionieren. Aber sie sind nicht fundamental.

Die fundamentale Loesung ist, natuerliche Sprache aus dem Inneren der KI zu entfernen.

Die Schnittstelle zu den Nutzern bleibt in natuerlicher Sprache.
Menschen sprechen weiterhin in natuerlicher Sprache und erhalten Antworten in natuerlicher Sprache.

Aber die Sprache, in der KI intern denkt, aufzeichnet und verifiziert,
muss etwas anderes als natuerliche Sprache sein.

Eine Sprache, in der die Quelle in der Struktur ist.
Eine Sprache, in der die Konfidenz in der Struktur ist.
Eine Sprache, in der der zeitliche Kontext in der Struktur ist.
Eine Sprache, in der Mehrdeutigkeit explizit behandelt wird.

Gesprochene Sprache schuf den Stamm.
Schrift schuf den Staat.
Was wird die dritte Sprache schaffen?

Das Ende der Halluzination liegt nicht in groesseren Modellen,
sondern in einer besseren Sprache.

---

## Zusammenfassung

Halluzination entsteht aus den vier strukturellen Maengeln der natuerlichen Sprache.

1. **Mehrdeutigkeit:** Ohne Kontext nicht aufloesbar. KI raet, und Vermutungen sind falsch.
2. **Fehlende Quelle:** Die Grundlage von Behauptungen geht verloren. Grundlose Kombinationen werden fabriziert.
3. **Fehlende Konfidenz:** Fakten und Schaetzungen werden in identischer Grammatik ausgedrueckt. KI kann sie nicht unterscheiden.
4. **Fehlender zeitlicher Kontext:** Informationen aus verschiedenen Zeitraeumen werden durcheinander gebracht.

Groessere Modelle reduzieren Halluzination, koennen sie aber nicht eliminieren.
Ohne das Medium zu aendern, bleiben die strukturellen Maengel.

Egal wie sehr man die Aufloesung von Schwarz-Weiss-Film erhoeht, Farbe erscheint nicht.
Wenn man Farbe will, muss man den Film wechseln.
