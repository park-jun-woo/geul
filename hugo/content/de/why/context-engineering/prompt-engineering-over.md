---
title: "Warum das Zeitalter des Prompt Engineering vorbei ist"
weight: 1
date: 2026-02-26T12:00:12+09:00
lastmod: 2026-02-26T12:00:12+09:00
tags: ["Prompt", "Kontext", "Engineering"]
summary: "Von wie man es sagt zu was man zeigt -- das Spiel hat sich geaendert"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Warum das Zeitalter des Prompt Engineering vorbei ist

### Von "wie man es sagt" zu "was man zeigt" -- das Spiel hat sich geaendert.

---

### Prompt Engineering als Beruf

Im Jahr 2023 erschien ein neuer Beruf.

Prompt Engineer.

"Denken Sie Schritt fuer Schritt."
"Sie sind ein Experte mit 20 Jahren Erfahrung."
"Lassen Sie mich Ihnen erst ein paar Beispiele zeigen."

Saetze wie diese wurden Know-how im Wert von Zehntausenden Dollar. Dieselbe Frage produzierte dramatisch unterschiedliche Antworten von der KI, je nach Formulierung.

Prompt Engineering funktionierte tatsaechlich.
Eine einzige Chain-of-Thought-Zeile erhoehte die Mathematikergebnisse um 20%.
Ein einziger Satz, der eine Rolle zuwies, veraenderte die Expertise-Tiefe.
Drei Few-Shot-Beispiele gaben vollstaendige Kontrolle ueber das Ausgabeformat.

Das war kein Hype. Es war real.
Warum endet es also?

---

### Warum es funktionierte: Weil die Modelle dumm genug waren

Betrachten Sie von Grundprinzipien aus, warum Prompt Engineering funktionierte. Es ist einfach.

Fruehe LLMs waren schlecht darin, die Absicht des Nutzers zu erfassen.
Sagen Sie "zusammenfassen" und sie schrieben um.
Sagen Sie "vergleichen" und sie listeten auf.

Weil das Modell die Absicht falsch las,
wurde die Faehigkeit, die Absicht praezise zu uebermitteln, wertvoll.
Prompt Engineering war im Wesentlichen "Dolmetschen" --
menschliche Absicht in eine Form uebersetzen, die das LLM verstehen konnte.

Damit Dolmetschen wertvoll ist, muss eine Sprachbarriere existieren.

---

### Was sich aenderte: Die Modelle wurden intelligent

Von GPT-3.5 zu GPT-4. Von Claude 2 zu Claude 3.5.
Mit jeder Generation verbesserte sich die Faehigkeit der Modelle, Absichten zu erfassen, dramatisch.

Sagen Sie "zusammenfassen" und sie fassen zusammen.
Sagen Sie "vergleichen" und sie vergleichen.
Selbst ohne die Anweisung "Schritt fuer Schritt denken" zerlegen sie komplexe Probleme von selbst in Schritte.

Die Sprachbarriere wurde niedriger.
Der Wert des Dolmetschens schrumpfte.

Prompt-Techniken, die 2023 dramatische Unterschiede erzeugten,
erzeugen 2025 nur noch marginale Unterschiede.
Wenn das Modell intelligent genug ist, spielt die Formulierung immer weniger eine Rolle.

Was zaehlt stattdessen?

---

### Das Kontextfenster: Ein Gesetz der Physik

LLMs haben eine physikalische Beschraenkung.

Das Kontextfenster.

Ob 128K Tokens oder 1M Tokens, es ist endlich.
Nur Informationen, die in diesen endlichen Raum passen, beeinflussen das Denken.
Informationen ausserhalb des Fensters, egal wie wichtig, koennten genauso gut nicht existieren.

Das ist unabhaengig von der Modellgroesse.
Selbst mit einer Billion Parameter ist das Kontextfenster endlich.
Selbst mit Trainingsdaten, die das gesamte Internet umfassen, ist das Kontextfenster endlich.

Egal wie intelligent das Modell ist,
wenn falsche Informationen in den Kontext gelangen, produziert es falsche Antworten.
Wenn irrelevante Informationen den Kontext fuellen, verpasst es das Wesentliche.
Wenn noetige Informationen im Kontext fehlen, ist es so gut wie unbekannt.

Prompt Engineering war ein Problem von "wie man es sagt".
Das neue Spiel ist ein Problem von "was man zeigt".

Das ist Context Engineering.

---

### Analogie: Die Pruefung mit offenen Buechern

Hier ist eine Analogie fuer den Unterschied zwischen Prompt Engineering und Context Engineering.

Prompt Engineering ist das gute Formulieren von Pruefungsfragen.
Statt "waehlen Sie die richtige Antwort unten"
schreiben Sie "leiten Sie Schritt fuer Schritt die Antwort ab, die alle folgenden Bedingungen erfuellt" --
und der Student gibt eine bessere Antwort.

Context Engineering ist die Frage, welche Buecher man zur Pruefung mit offenen Buechern mitbringt.
Egal wie gut die Pruefungsfragen formuliert sind,
wenn der Student die falschen Buecher mitgebracht hat, kann er nicht antworten.
Die Anzahl der Buecher, die man mitbringen kann, ist begrenzt.
Welche Buecher man mitbringt, bestimmt die Note.

Als das Modell dumm war, zaehlt das Fragenformat (Prompt).
Wenn das Modell intelligent ist, zaehlt das Referenzmaterial (Kontext).

---

### Das Agenten-Zeitalter beschleunigt den Wandel

Dieser Wandel wird durch das Aufkommen von Agenten beschleunigt.

Prompt Engineering wird jedes Mal von Menschen geschrieben.
Menschen schreiben die Frage, Menschen erklaeren den Kontext, Menschen spezifizieren das Format.

Agenten sind anders.
Agenten denken selbstaendig, rufen Tools auf und arbeiten mit anderen Agenten zusammen.
Bei jedem Schritt muessen sie den Kontext selbst zusammenstellen.

Ein Agent hat eine externe API aufgerufen und Daten erhalten.
Diese Daten muessen fuer die naechste Denkrunde in den Kontext.
Welche Teile kommen rein und welche bleiben draussen?
Welche vorherigen Denkergebnisse werden behalten und welche verworfen?
Kann man Informationen, die ein anderer Agent geschickt hat, vertrauen?

Ein Mensch kann nicht jedes Mal all diese Entscheidungen treffen.
Damit Agenten autonom operieren koennen,
muss die Kontextzusammenstellung automatisiert werden.

Prompt Engineering war eine menschliche Faehigkeit.
Context Engineering muss eine Systemfaehigkeit sein.

---

### Prompt Engineering verschwindet nicht

Vermeiden wir ein Missverstaendnis.

Ich sage nicht, dass Prompt Engineering bedeutungslos wird.
System Prompts sind weiterhin wichtig.
Die Spezifikation des Ausgabeformats ist weiterhin noetig.
Das Erklaeren von Rollen und Einschraenkungen ist weiterhin effektiv.

Was schrumpft, ist der Anteil, den Prompt Engineering haelt.

Wenn 2023 70% der Ausgabequalitaet vom Prompt bestimmt wurden,
werden 2025 30% vom Prompt und 70% vom Kontext bestimmt.

Das Verhaeltnis hat sich umgekehrt.

Und dieser Trend kehrt sich nicht um.
Modelle werden weiter intelligenter,
und je intelligenter sie werden, desto weniger zaehlt die Formulierung
und desto mehr zaehlt der Kontext.

---

### Aber Context Engineering hat keine Infrastruktur

Hier liegt der Kern.

Prompt Engineering hatte Werkzeuge.
Prompt-Vorlagen, Prompt-Bibliotheken, Prompt-Test-Frameworks.
Ein ganzes Oekosystem zur systematischen Verwaltung von "wie man es sagt" wurde aufgebaut.

Context Engineering hat das noch nicht.

Schauen Sie sich an, wie Kontext in der Praxis derzeit gehandhabt wird.

RAG-Pipeline-Chunk-Groessen werden per Hand eingestellt.
Hintergrundinformationen werden per Hand in System Prompts geschrieben.
Was im Gedaechtnis eines Agenten gespeichert wird, wird per Hand entworfen.
Welche Suchergebnisse in den Kontext kommen, wird per Hand entschieden.

Alles ist manuell.

Und der Rohstoff fuer all diese manuelle Arbeit ist natuerliche Sprache.
Natuerlichsprachliche Dokumente werden in natuerlicher Sprache zerschnitten und in einen natuerlichsprachlichen Kontext eingefuegt.

Natuerliche Sprache hat eine niedrige Informationsdichte.
Keine Quellen. Keine Konfidenzniveaus. Keine Zeitstempel.
Unnoetige Tokens werden verbraucht, um dieselbe Bedeutung zu vermitteln.
Es gibt keine Moeglichkeit, die Qualitaetsbeurteilung zu automatisieren.

Das aehnelt der Aera vor dem Prompt Engineering.
Prompt Engineering war anfangs auch manuell.
Es beruhte auf individueller Intuition und Erfahrung.
Dann erschienen Werkzeuge und Methodologien und es wurde systematisiert.

Context Engineering befindet sich derzeit in dieser vorherigen Phase.
Das Problem wurde erkannt, aber die Infrastruktur existiert nicht.

---

### Was die Infrastruktur braucht

Damit Context Engineering von manueller Arbeit zu einem System wird,
ist mindestens Folgendes erforderlich.

**Kompression.** Ein Weg, mehr Bedeutung in dasselbe Fenster zu packen.
Den grammatischen Klebstoff natuerlicher Sprache entfernen und nur Bedeutung belassen,
und die effektive Fenstergroesse vervielfacht sich -- ohne das Modell zu aendern.

**Indexierung.** Ein Weg, die richtige Information praezise zu finden.
Suche basierend auf semantischer Struktur, nicht auf Embedding-Aehnlichkeit.
Eine Suche, bei der "Apple Umsatz" nicht "Apfel Naehrwerte" liefert.

**Validierung.** Ein Weg, Informationen, die nicht der Spezifikation entsprechen, mechanisch abzuweisen.
So wie ein Go-Compiler unbenutzte Variablen als Fehler erkennt,
sollten Behauptungen ohne Quellen und Fakten ohne Zeitstempel herausgefiltert werden, bevor sie in den Kontext gelangen.
Die guenstigsten und deterministischsten Pruefungen muessen zuerst kommen.

**Filterung.** Ein Weg, semantische Qualitaet zu beurteilen.
Wenn Validierung die Form betrachtet, betrachtet Filterung den Inhalt.
Relevanz, Zuverlaessigkeit, Aktualitaet. Wird diese Information wirklich fuer diese Denkrunde benoetigt?

**Konsistenz.** Ein Weg, die interne Kohaerenz des ausgewaehlten Informationssatzes zu garantieren.
Einzeln gute Informationen koennen sich bei Kombination widersprechen.
Wenn der CEO von 2020 und der CEO von 2024 gleichzeitig in den Kontext gelangen,
wird das LLM verwirrt.

**Komposition.** Ein Weg, Platzierung und Struktur innerhalb des Fensters zu optimieren.
Dieselbe Information erhaelt unterschiedliche Aufmerksamkeitsgewichte je nach Platzierung.
Vorne oder hinten? Wie ist sie gruppiert?

**Akkumulation.** Ein Weg fuer das System, mit der Zeit zu lernen und zu wachsen.
Caching ist die Wiederverwendung einzelner Ergebnisse.
Akkumulation ist zu lernen, welche Kontextzusammenstellungen gute Ergebnisse erzielten,
und die Wissensbasis selbst wachsen zu lassen.

Diese sieben sind der vollstaendige Stack der Context-Engineering-Infrastruktur.

---

### Es geht nicht um ein bestimmtes Werkzeug

Seien wir ehrlich.

Wer diese Infrastruktur baut, ist eine offene Frage.
Ein Werkzeug koennte alles loesen,
oder mehrere Werkzeuge koennten je eine Schicht uebernehmen.

Aber dass Infrastruktur benoetigt wird, ist keine offene Frage.

Dass das Kontextfenster endlich ist, ist eine physikalische Tatsache.
Selbst wenn das Fenster um das 10-fache waechst, wachsen die Informationen der Welt schneller.
Dass natuerliche Sprache eine niedrige Informationsdichte hat, ist eine strukturelle Tatsache.
Dass Agenten automatisiertes Kontextmanagement brauchen, um autonom zu operieren, ist eine logische Notwendigkeit.

So wie Prompt Engineering Werkzeuge brauchte,
braucht Context Engineering Werkzeuge.
Aber diesmal ist die Art der Werkzeuge anders.

Prompt-Engineering-Werkzeuge waren naeher an Texteditoren.
Context-Engineering-Werkzeuge sind naeher an Compilern.

Informationen komprimieren, indexieren, validieren, filtern,
Konsistenz pruefen, Platzierung optimieren und Ergebnisse akkumulieren.
Das ist kein Editieren. Das ist Engineering.

Deshalb heisst es Context "Engineering".

---

### Zusammenfassung

Prompt Engineering war wertvoll, als Modelle dumm waren.
Weil Modelle die Absicht nicht lesen konnten, zaehlt die Faehigkeit, die Absicht gut zu vermitteln.

Als die Modelle intelligenter wurden, aenderte sich das Spiel.
Von "wie man es sagt" zu "was man zeigt".
Vom Prompt zum Kontext.

Das Aufkommen von Agenten beschleunigt diesen Wandel.
Menschen koennen nicht jedes Mal den Kontext zusammenstellen.
Das System muss es selbst tun.

Aber derzeit hat Context Engineering keine Infrastruktur.
Natuerliche Sprache wird per Hand geschnitten und eingefuegt.

Die benoetigte Infrastruktur hat sieben Schichten:
Kompression, Indexierung, Validierung, Filterung, Konsistenz, Komposition, Akkumulation.

Es ist nicht das Zeitalter des Prompt Engineering, das endet.
Es ist das Zeitalter, in dem Prompt Engineering allein ausreichte.
