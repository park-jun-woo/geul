---
title: "Architektur"
date: 2026-02-26T12:00:00+09:00
image: "/images/og-default.webp"
summary: "Wie GEUL aufgebaut ist: semantisch ausgerichtete Indizierung, 16-Bit-Worteinheiten, strukturierter Speicher und anspruchsbasierte Wissensrepräsentation."
---

## Unterthemen

### Warum 16-Bit
Alle Daten in GEUL sind in 16-Bit-Einheiten (1 Wort). Es ist die minimale Einheit, die die Effizienz von Maschinencode mit der Bedeutung menschlicher Sprache in einem einzigen Wort vereint.

### Warum Schlussfolgerungen als Code zwischenspeichern
Ergebnisse jedes Mal zu verwerfen, wenn eine KI schlussfolgert, ist Rechenverschwendung. Schlussfolgerungen in einer strukturierten Sprache aufzuzeichnen ermoglicht Wiederverwendung und Akkumulation.

### Warum Behauptungen, nicht Fakten
Satze in naturlicher Sprache sehen wie Fakten aus, sind aber tatsachlich Behauptungen von jemandem. Die strukturelle Einbettung von Quelle, Zeitpunkt und Konfidenz verringert den Spielraum fur Halluzinationen.

### Warum ein semantisch ausgerichteter Index
SIDX ist ein 64-Bit-Bezeichner, der Bedeutung in den Bits selbst kodiert. Der Typ kann allein aus den oberen Bits bestimmt werden, und je weniger Bits gefullt sind, desto abstrakter wird der Ausdruck.

### Warum strukturierter Speicher notwendig ist
Das Kontextfenster eines LLM ist endlich. Um unendliche Erfahrung in ein endliches Fenster zu packen, muss der Speicher strukturiert sein.
