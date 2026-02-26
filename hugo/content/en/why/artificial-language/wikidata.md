---
title: "Why Wikidata"
weight: 13
date: 2026-02-26T12:00:17+09:00
lastmod: 2026-02-26T12:00:17+09:00
tags: ["Wikidata", "Ontology", "SIDX"]
summary: "GEUL does not reject Wikidata. It transforms the classification system and frequency statistics of 100 million entities into SIDX codebooks. Grammar is built on top of a dictionary."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## GEUL does not reject Wikidata. It stands on top of it.

---

## You cannot build a language without a dictionary

Every language needs a vocabulary.

Korean has the Korean dictionary.
English has the English dictionary.
Programming languages have standard libraries.

The same is true for an artificial language.
A list of entities, a list of relations, a list of properties.
What code represents "Samsung Electronics" in this language?
What code represents the relation "capital"?
You need a vocabulary before you can write a sentence.

How do you build this vocabulary?
There are two approaches.

Build it from scratch.
Or use what already exists.

---

## Building from scratch: the lesson of CYC

The CYC project began in 1984.

Its goal was to formalize and store general common-sense knowledge.
The ontology was designed from the ground up.
Concepts were defined, relations were defined, rules were defined.
Experts entered them by hand.

Thirty years passed.
Millions of rules were entered.

Yet it was nowhere near enough to cover the world's knowledge.
A separate ontology had to be designed for each domain.
Maintaining consistency across domains proved difficult.
Every time a new concept emerged, the ontology had to be revised.
Revisions frequently conflicted with existing rules.

What CYC demonstrated was not its potential but its limits.
Having a small team of experts design the world's ontology
becomes unmaintainable at scale.

---

## What already exists: Wikidata

Wikidata launched in 2012.

A structured knowledge base operated by the Wikimedia Foundation.
Anyone can edit it.
As of 2024, it contains over 100 million entities.
More than 10,000 properties.
Billions of statements.
Labels in over 300 languages.

The scale that CYC could not achieve in 30 years with an expert team,
Wikidata achieved in 10 years with a community.

Consider what Wikidata provides.

**Entity identifiers.** Q-IDs. Samsung Electronics is Q20718. Seoul is Q8684. Yi Sun-sin is Q217300. Globally unique identifiers. Language-independent.

**Property identifiers.** P-IDs. "Headquarters location" is P159. "Inception" is P571. "Population" is P1082. Relations and properties are uniquely identified.

**Hierarchical structure.** P31 (instance of) and P279 (subclass of) form a type hierarchy. "Seoul → city → human settlement → geographic entity." The world's classification system is expressed through these two properties.

**Multilingual labels.** The Korean label for Q20718 is "삼성전자," the English label is "Samsung Electronics," the Japanese label is "サムスン電子." One identifier, different names for each language.

**Community validation.** Millions of editors. Vandalism detection. Source requirements. Not perfect, but more scalable than a small team of experts.

There is no reason to build this from scratch.

---

## GEUL's vocabulary comes from Wikidata

GEUL's SIDX (Semantic-aligned Index) is a 64-bit semantically aligned identifier.
Meaning is encoded in the bits themselves.
Just by examining the upper bits, you can tell whether something is a person, a place, or an organization.

The SIDX codebook — which bit pattern maps to which meaning — is extracted from Wikidata.

The process works as follows.

**Step 1: Type extraction.**
Extract all Q-IDs used as objects of P31 (instance of) from Wikidata.
This produces the list of "types."
"Human (Q5)," "city (Q515)," "country (Q6256)," "enterprise (Q4830453)"...
Count how many times each type is used — the number of instances.

**Step 2: Hierarchy construction.**
Extract P279 (subclass of) relations between types.
"City → human settlement → geographic entity → entity."
This forms the tree structure of types.
Identify root nodes, leaf nodes, and intermediate nodes.
Detect and handle multiple inheritance — cases where a single type belongs to multiple parent types.

**Step 3: Bit assignment.**
The tree structure determines the prefix relationships of bit patterns.
Subtypes under the same parent share the same prefix.
"City" and "town" share the prefix of "human settlement."

Instance counts influence bit length.
Frequently used types receive more efficient codes.
The same principle as Huffman coding: shorter codes for higher frequencies.

---

## What Wikidata provides

In this process, Wikidata provides three things.

**A classification system.**
An answer to "What kinds of things exist in the world?"
CYC had an expert team design this.
GEUL extracts it from Wikidata.
A classification system built by millions of editors over 10 years,
transformed into a bit tree.

**Frequency statistics.**
An answer to "How many of each kind exist in the world?"
If there are 9 million human entities and 1 million asteroids,
the type "human" should receive a more efficient code than "asteroid."
Real-world usage frequency drives code design.

**Identifier mapping.**
A mapping between Wikidata's Q-IDs and GEUL's SIDX.
Which bit pattern in SIDX corresponds to Q20718 (Samsung Electronics)?
With this mapping, Wikidata knowledge can be converted to GEUL,
and GEUL statements can be converted back to Wikidata.

---

## What Wikidata does not provide

Wikidata is a dictionary. A dictionary is not a language.

A dictionary provides a list of words.
A language provides grammar for composing sentences from words.

What Wikidata does not provide is what GEUL adds.

**From facts to claims.**
The basic unit of Wikidata is a fact.
"The population of Seoul is 9.74 million."
It is either true or false.

The basic unit of GEUL is a claim.
"According to A, the population of Seoul is approximately 9.74 million. (confidence 0.9, as of 2023)"
Who is asserting it, with what level of certainty, and as of when — all of this is embedded in the statement.
This difference is discussed in detail in [Why claims, not facts](/why/claims-not-facts/).

**Verb qualifiers.**
Wikidata has no place to express the nuances of verbs.
In "Yi Sun-sin won the Battle of Myeongnyang,"
where are tense, aspect, evidentiality, mood, and confidence?
In Wikidata, these are partially expressed through qualifiers,
but there is no systematic verb qualification system.

GEUL has a 28-bit verb qualifier system.
Thirteen dimensions — tense, aspect, polarity, evidentiality, mood, volitionality, confidence, and more — are structurally embedded in every statement.

**16-bit compression.**
Wikidata's representation was not designed for context windows.
JSON-LD, RDF, SPARQL.
Machine-readable, but not token-efficient.

GEUL is designed in 16-bit word units.
One-to-one mapping with LLM tokens.
A representation system built on the premise of finite context windows.
This was already discussed in [Why not MD/JSON/XML](/why/not-md-json-xml/).

**Context pipeline.**
Wikidata is a repository. GEUL is part of a pipeline.
Clarification, validation, filtering, consistency checking, exploration — everything discussed in this series operates on GEUL's structured representation.
Wikidata does not have this pipeline.
Nor does it need one. Wikidata's purpose is different.

---

## The relationship between a dictionary and a language

To summarize:

Wikidata is the world's vocabulary.
Which entities exist,
which relations exist,
which types exist and how they are classified.
Millions of people built this over 10 years.

GEUL builds grammar on top of this vocabulary.
The vocabulary's classification system → SIDX's bit tree.
The vocabulary's frequency statistics → bit assignment priorities.
The vocabulary's identifiers → mapping to SIDX.

And it adds what the vocabulary lacks.
Claim structure. Verb qualification. Token-level compression. Context pipeline.

Could GEUL be built without Wikidata?
It could. You would design the ontology from scratch, as CYC did.
But that was attempted 30 years ago, and the results speak for themselves.

Because Wikidata exists, GEUL does not design an ontology.
It transforms an existing consensus.

---

## Summary

An artificial language needs a vocabulary.
Building one from scratch was attempted by CYC, and 30 years proved the limits of that approach.

Wikidata is the world's vocabulary, with over 100 million entities, more than 10,000 properties, and billions of statements.
Millions of editors built it over 10 years.

GEUL's SIDX codebook is extracted from Wikidata.
P31 instance frequencies determine bit assignments,
and the P279 hierarchy forms the skeleton of the bit tree.

Wikidata is a dictionary; GEUL is a language.
A dictionary provides words; a language provides grammar.
GEUL builds claim structure, verb qualification, 16-bit compression, and a context pipeline on top of Wikidata's vocabulary.

GEUL does not reject Wikidata.
It stands on top of it.
