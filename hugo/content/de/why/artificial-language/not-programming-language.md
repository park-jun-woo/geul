---
title: "Warum Programmiersprachen nicht ausreichen"
weight: 10
date: 2026-02-26T12:00:19+09:00
lastmod: 2026-02-26T12:00:19+09:00
tags: ["Programmiersprache", "Beschreibung", "Wissensrepräsentation"]
summary: "Programmiersprachen beschreiben Prozeduren. Sie können die Welt nicht beschreiben. JSON liefert Struktur, aber keine Bedeutung. Selbst LISP leiht sich nur die Syntax."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Programmiersprachen beschreiben Prozeduren. Sie können die Welt nicht beschreiben.

---

## Programmiersprachen gehören zu den größten Erfindungen der Menschheit

Programmiersprachen sind eindeutig.
`x = 3 + 4` ergibt 7, egal wann und wo es ausgeführt wird.
Es gibt keinen Spielraum für Interpretation.

Programmiersprachen sind verifizierbar.
Syntaxfehler werden vor der Kompilierung erkannt.
Typfehler werden vor der Ausführung erkannt.
Wenn Tests laufen, ist das Ergebnis entweder bestanden oder durchgefallen.

Programmiersprachen sind Turing-vollständig.
Sie können alles Berechenbare ausdrücken.
Mit genügend Zeit und Speicher lässt sich jede Prozedur beschreiben.

Alles, was diese Serie als Einschränkungen natürlicher Sprache identifiziert hat — Mehrdeutigkeit, fehlende Verifizierbarkeit, fehlende Struktur — haben Programmiersprachen gelöst.

Warum also nicht eine Programmiersprache verwenden, um den Kontext einer KI darzustellen?

Es funktioniert nicht.

---

## Programmiersprachen beschreiben Prozeduren

Der folgende Python-Code ist gültig.

```python
def calculate_revenue(units_sold, unit_price):
    return units_sold * unit_price
```

Dieser Code ist klar, verifizierbar und ausführbar.
Aber was drückt er aus?

„Multipliziere die verkaufte Stückzahl mit dem Stückpreis, um den Umsatz zu erhalten."

Das ist eine Prozedur. Eine Methode. Das WIE.
Er beschreibt, was zu tun ist, wenn eine Eingabe eintrifft.

Versuchen wir nun, Folgendes auszudrücken.

„Der Umsatz von Samsung Electronics im dritten Quartal 2024 betrug 79 Billionen Won."

Das ist keine Prozedur. Es ist eine Tatsache. Das WAS.
Nichts wird ausgeführt. Es beschreibt den Zustand der Welt.

Wie drückt man das in Python aus?

```python
samsung_revenue_2024_q3 = 79_000_000_000_000
```

Eine Zahl wird einer Variablen zugewiesen.
Es funktioniert. Aber das ist keine Beschreibung. Das ist Speicherung.
Dieser Code weiß nicht:

- Was für eine Art von Entität „Samsung Electronics" ist.
- Was „Umsatz" bedeutet. Ist es eine Finanzkennzahl? Eine physikalische Größe?
- Ob „Q3 2024" eine Zeit, eine Version oder ein Label ist.
- Was die Quelle der Zahl von 79 Billionen Won ist.
- Wie sicher dieser Wert ist.

Der Variablenname `samsung_revenue_2024_q3` lässt einen Menschen die Bedeutung erraten.
Für die Maschine ist es eine beliebige Zeichenkette.
Benennt man sie in `xyzzy_42` um, bleibt das Ausführungsergebnis dasselbe.

In Programmiersprachen tragen Variablennamen keine Bedeutung.
Die Bedeutung lebt außerhalb des Codes, im Kopf des Programmierers.

---

## Mehr Raffinesse hilft nicht

Und wenn man eine Klasse erstellt?

```python
class FinancialReport:
    def __init__(self, company, metric, period, value, currency):
        self.company = company
        self.metric = metric
        self.period = period
        self.value = value
        self.currency = currency

report = FinancialReport("삼성전자", "매출", "2024-Q3", 79_000_000_000_000, "KRW")
```

Besser. Es gibt jetzt Struktur.
Aber die Probleme bleiben.

`company` ist die Zeichenkette „삼성전자" (Samsung Electronics).
„Samsung Electronics", „SEC" und „005930" beziehen sich alle auf dasselbe Unternehmen.
Weiß der Code das? Nein.
Er kann nur vergleichen, ob Zeichenketten gleich sind oder nicht.

`metric` ist die Zeichenkette „매출" (Umsatz).
Sind „매출", „매출액" und „revenue" dasselbe oder verschiedene Dinge?
Der Code weiß es nicht. Die Zeichenketten sind verschieden, also sind es verschiedene Dinge.

Und wenn man ein Schema definiert?
Unternehmenslisten mit Enums verwalten, Kennzahlenlisten verwalten.
Klar. Es funktioniert.

Dann versuchen wir, Folgendes auszudrücken.

„Yi Sun-sin war großartig."

```python
opinion = Opinion("이순신", "was", "위대했다")
```

Was ist das?
Eine Zeichenkette „이순신" (Yi Sun-sin) verbunden mit einer Zeichenkette „위대했다" (war großartig).
Das drückt nicht „Yi Sun-sin war großartig" aus.
Es speichert „이순신" und „위대했다".

Der Code kennt die Bedeutung von „위대했다" (war großartig) nicht.
Ob „위대했다" (war großartig) und „훌륭했다" (war bewundernswert) ähnlich sind,
ob „비겁했다" (war feige) das Gegenteil ist —
der Code kann es nicht wissen.

Strukturierte Fakten wie Finanzdaten sind einigermaßen handhabbar.
Bewertungen, Kontext, Beziehungen, abstrakte Beschreibungen liegen jenseits der Ausdrucksfähigkeit von Programmiersprachen.

---

## Code weiß nicht, was er tut

```python
def process(data):
    result = []
    for item in data:
        if item["value"] > threshold:
            result.append(transform(item))
    return result
```

Dieser Code wird einwandfrei ausgeführt.
Aber was tut er?

Filtert er Umsatzdaten?
Sichtet er Patientenakten?
Bereinigt er Sensordaten?

Der Code selbst weiß es nicht.
`data`, `value`, `threshold`, `transform` — alles abstrakte Namen.
Ob dieser Code zu einem Finanzsystem oder einem medizinischen System gehört,
hängt vom Kontext außerhalb des Codes ab.

Man kann Kommentare schreiben.
Aber Kommentare sind natürliche Sprache. Maschinen verstehen sie nicht.
Wenn ein Kommentar dem Code widerspricht, bemerkt der Compiler es nicht.
Kommentare sind für Menschen, nicht für Maschinen.

Wenn eine KI Code als Kontext erhält, tritt dieses Problem unmittelbar zutage.
Da Code keine Selbstidentität besitzt,
muss die KI seine Identität jedes Mal durch Inferenz rekonstruieren.
Da es Inferenz ist, kostet es Rechenleistung und kann falsch sein.

---

## Der grundlegende Grund

Dass Programmiersprachen die Welt nicht beschreiben können, ist kein Designfehler.
Der Zweck ist ein anderer.

Der Zweck einer Programmiersprache ist es, einer Maschine Prozeduren anzuweisen.
„Wenn diese Eingabe eintrifft, führe diese Operation aus."
Die Semantik einer Programmiersprache ist die Semantik der Ausführung.
Jedes Konstrukt wird als „was tut die Maschine" interpretiert.

`x = 3` ist die Anweisung „speichere 3 an der Speicherstelle x".
`if x > 0` ist die Anweisung „wenn x größer als 0 ist, führe den nächsten Block aus".
`return x` ist die Anweisung „gib den Wert von x an den Aufrufer zurück".

Alles Verben. Alles Handlungen. Alles Prozeduren.

„Samsung Electronics ist ein koreanisches Unternehmen" ist kein Verb.
Keine Handlung. Keine Prozedur.
Es beschreibt, in welchem Zustand die Welt ist.

Programmiersprachen haben dafür keinen Platz.
Man kann es in einer Variablen speichern, aber das ist Speicherung, nicht Beschreibung.
Die Bedeutung des gespeicherten Werts liegt nicht in der Zuständigkeit des Codes.

---

## Was ist mit JSON, YAML, XML?

Wenn nicht Programmiersprachen, dann Datenformate?

```json
{
  "company": "삼성전자",
  "metric": "매출",
  "period": "2024-Q3",
  "value": 79000000000000,
  "currency": "KRW"
}
```

Es gibt Struktur. Die Felder sind explizit.
Aber es gibt keine Bedeutung.

Ob „company" ein Unternehmen bedeutet — JSON weiß es nicht.
Ob „삼성전자" dasselbe wie „Samsung Electronics" anderswo ist — JSON weiß es nicht.
Ob dieses JSON-Objekt und jenes JSON-Objekt dieselbe Entität beschreiben — JSON weiß es nicht.

JSON liefert Struktur, aber keine Bedeutung.
Es sind Schlüssel-Wert-Paare, nicht Entität-Beziehung-Attribut.

Schemata zu definieren hilft.
JSON Schema, Protocol Buffers, GraphQL.
Feldtypen werden definiert, Pflichtfelder werden definiert, Referenzen werden definiert.

Aber das sind alles Strukturen, die für spezifische Systeme entworfen wurden.
Sie sind keine universelle Wissensrepräsentation.
Ein Finanzdaten-Schema kann die Bewertung einer historischen Persönlichkeit nicht ausdrücken.
Ein Medizindaten-Schema kann die Wettbewerbsbeziehungen zwischen Unternehmen nicht ausdrücken.

Ein separates Schema für jede Domäne.
Ein separates Werkzeug für jedes Schema.
Keine Interoperabilität zwischen Schemata.

Diese Einschränkung wird ausführlicher in [Warum MD/JSON/XML nicht funktionieren](/de/why/not-md-json-xml/) behandelt.

---

## Was ist mit LISP?

Einige Leser haben möglicherweise an ein Gegenbeispiel gedacht.

LISP.

```lisp
(is 삼성전자 (company korea))
(revenue 삼성전자 2024-Q3 79000000000000)
(great 이순신)
```

S-Ausdrücke sind Baumstrukturen,
und Code ist Daten und Daten sind Code.
Homoikonizität (homoiconicity).

Tatsächlich basierte die frühe KI vollständig auf LISP.
SHRDLU, CYC, Expertensysteme.
Wissen wurde in LISP dargestellt, und Inferenzmaschinen liefen darauf.
Es scheint ein historischer Gegenbeweis zu sein, dass „Programmiersprachen die Welt nicht beschreiben können".

Aber das Gegenbeispiel scheitert aus drei Gründen.

### Was LISP weiß und was der Programmierer festgelegt hat

In `(is 삼성전자 company)` weiß LISP nicht,
dass `is` die Beziehung „ist ein" bedeutet.
Der Programmierer hat das festgelegt.

Ersetze `is` durch `zzz` und LISP ist es egal.
`(zzz 삼성전자 company)` ist für LISP ein vollkommen gültiger Ausdruck.

LISP liefert Struktur. Einen Baum namens S-Ausdruck.
Aber die Bedeutung innerhalb dieser Struktur wurde vom Programmierer zugewiesen, nicht von der Sprache.
Das ist grundsätzlich dasselbe, wie wenn JSON die Bedeutung seiner Schlüssel nicht kennt.

Struktur bereitstellen und Bedeutung einbetten sind zwei verschiedene Dinge.

### 30 Jahre CYC

Der ambitionierteste Versuch war CYC.

Gestartet 1984.
Er versuchte, allgemeines Wissen mit LISP darzustellen.
Millionen von Regeln wurden manuell eingegeben.

Was 30 Jahre bewiesen haben, war nicht die Machbarkeit, sondern die Grenzen.

Ontologien mussten für jede Domäne manuell entworfen werden.
Domänenübergreifende Interoperabilität funktionierte nicht.
Mit der Flexibilität natürlicher Sprache konnte es nicht Schritt halten.
Je größer der Umfang wurde, desto unmöglicher wurde es, Konsistenz zu wahren.

Dass Wissensrepräsentation in LISP „gemacht werden kann", stimmt.
Dass es „gut funktioniert", ist das, was 30 Jahre Ergebnisse widerlegen.

### Wenn man eval nicht verwenden will, gibt es keinen Grund, LISP zu benutzen

Das grundlegendste Problem.

Die Stärke von LISP ist `eval`.
Da Code Daten sind, können Daten ausgeführt werden.
Metaprogrammierung, Makros, Code-Generierung zur Laufzeit.
Das ist es, was LISP zu LISP macht.

Aber was passiert, wenn man `eval` auf `(is 삼성전자 company)` anwendet?

Es wird ein Funktionsaufruf, der `삼성전자` und `company` als Argumente an eine Funktion namens `is` übergibt.
Nicht Beschreibung — Ausführung.

Für die Verwendung als Wissensrepräsentation darf man nicht evaluieren.
Wenn man nicht evaluiert, nutzt man die Semantik von LISP nicht.
Man leiht sich nur die Syntax der S-Ausdrücke.

Das ist nicht „die Welt in LISP beschreiben".
Das ist „Daten mit der Klammernotation von LISP speichern".

Die Semantik von LISP als Programmiersprache — die Semantik der Ausführung —
ist weiterhin dafür ausgelegt, Prozeduren zu beschreiben.
Sich die Syntax zu leihen, ändert die Semantik nicht.

---

## Was eine Sprache zur Beschreibung der Welt braucht

Programmiersprachen beschreiben Prozeduren.
Datenformate liefern Struktur, aber keine Bedeutung.
Selbst LISP leiht sich nur Syntax ohne die Semantik der Beschreibung.

Was braucht eine Sprache zur Beschreibung der Welt?

**Identität von Entitäten.** „Samsung Electronics" muss einen eindeutigen Bezeichner haben. Die Maschine muss wissen, dass es dasselbe ist wie „삼성전자". Nicht Zeichenkettenvergleich, sondern Identitätsäquivalenz.

**Ausdruck von Beziehungen.** In „Samsung Electronics ist ein koreanisches Unternehmen" muss die Beziehung „koreanisches Unternehmen" ausgedrückt werden können. Nicht Variablenzuweisung, sondern Beschreibung von Beziehungen.

**Selbstbeschreibende Beschreibungen.** Wovon die Beschreibung handelt, wer sie gemacht hat, zu welchem Zeitpunkt und wie sicher sie ist — alles muss in der Beschreibung selbst enthalten sein. Im Code, nicht außerhalb.

**Domänenunabhängigkeit.** Finanzdaten, historische Fakten, subjektive Bewertungen, abstrakte Beziehungen — alles muss im selben Format ausdrückbar sein. Nicht ein separates Schema für jede Domäne, sondern eine universelle Struktur.

Programmiersprachen besitzen keine dieser vier Eigenschaften.
Denn Programmiersprachen wurden nicht dafür gebaut.
Sie wurden gebaut, um Prozeduren zu beschreiben.

Natürliche Sprache kann alle vier Dinge. Mehrdeutig.
Was gebraucht wird, ist eine Verbindung der Ausdrucksbandbreite natürlicher Sprache mit der Präzision von Programmiersprachen.

---

## Zusammenfassung

Programmiersprachen sind eindeutig, verifizierbar und Turing-vollständig.
Aber sie können die Welt nicht beschreiben.

Programmiersprachen beschreiben Prozeduren.
„Wenn diese Eingabe eintrifft, tue dies." Alles Verben, alles Handlungen.
„Samsung Electronics ist ein koreanisches Unternehmen" ist keine Handlung.
Programmiersprachen haben keinen Platz dafür.

Code kennt seine eigene Identität nicht.
Zu welcher Domäne er gehört, welchem Zweck er dient —
nichts davon ist im Code festgehalten.

Datenformate wie JSON und YAML liefern Struktur, aber keine Bedeutung.
LISP kann sich Syntax leihen, hat aber keine Semantik der Beschreibung.
CYC hat 30 Jahre lang LISP-basierte Wissensrepräsentation versucht, und was es bewiesen hat, waren die Grenzen.

Die Welt zu beschreiben erfordert Identität von Entitäten, Ausdruck von Beziehungen, selbstbeschreibende Beschreibungen und Domänenunabhängigkeit.
Programmiersprachen wurden nicht dafür gebaut.
Natürliche Sprache kann es, aber mehrdeutig.
Was gebraucht wird, liegt irgendwo dazwischen.
