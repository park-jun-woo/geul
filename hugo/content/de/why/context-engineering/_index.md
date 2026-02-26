---
title: "Kontext-Engineering"
date: 2026-02-26T12:00:00+09:00
image: "/images/og-default.webp"
summary: "Warum besserer Kontext bessere Prompts schlägt: RAG-Einschränkungen, mechanische Verifizierung, Konsistenzprüfung und semantische Filterung für KI-Systeme."
---

## Unterthemen

### Warum ist die Ära des Prompt-Engineerings vorbei?
Wenn Modelle intelligent genug sind, spielt es weniger eine Rolle, „wie man es sagt". „Was man zeigt" bestimmt die Ausgabequalität. Das Kontextfenster ist endlich, und was man hineinstellt, entscheidet das Ergebnis.

### Warum ist Klarheit notwendig?
Natürliche Sprache wird unvermeidlich länger, um Mehrdeutigkeit aufzulösen. Eine strukturell eindeutige Darstellung hat keine Auflösungskosten. Kompression entsteht als Nebenprodukt der Klarheit.

### Warum reicht RAG nicht aus?
Embedding-Ähnlichkeit garantiert keine Relevanz. Semantisch strukturbasiertes Retrieval ist erforderlich. Um Kandidaten aus einer Milliarde Erinnerungen in Millisekunden einzugrenzen, muss Information semantisch indexiert sein.

### Warum ist mechanische Verifikation notwendig?
Natürliche Sprache hat kein Konzept eines „ungültigen Satzes". Wie ein Go-Compiler muss Information, die den Spezifikationen nicht entspricht, vor dem Eintritt in den Kontext abgelehnt werden. Die günstigste und deterministischste Prüfung kommt zuerst.

### Warum sind Filter notwendig?
Wenn Verifikation die strukturelle Eignung beurteilt, beurteilen Filter die semantische Qualität. Relevanz, Vertrauen, Aktualität. Nur was für diese Inferenz gerade jetzt benötigt wird, passiert den Filter.

### Warum sind Konsistenzprüfungen notwendig?
Einzeln gute Informationen können sich widersprechen, wenn sie kombiniert werden. Wenn Fakten aus 2020 und 2024 gleichzeitig in den Kontext gelangen, wird das LLM verwirrt. Kohärenz auf Mengenebene muss gewährleistet sein.

### Warum ist Exploration notwendig?
Suche liefert Ergebnisse mit einer einzelnen Anfrage. Wenn Wissen groß genug wird, funktioniert das nicht mehr — der Index selbst übersteigt das Fenster. Ein Agent muss hierarchische Karten navigieren und Richtungen wählen. Wenn eine Bibliothek wächst, wechselt man vom Fragen des Bibliothekars zum Durchlaufen des Klassifikationssystems.
