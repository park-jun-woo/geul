---
title: "Why MD/JSON/XML Won't Work"
weight: 9
date: 2026-02-26T12:00:15+09:00
lastmod: 2026-02-26T12:00:15+09:00
tags: ["format", "JSON", "XML"]
summary: "Existing formats cannot carry meaning"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Structured formats already exist. So why is a new language needed?

---

## The Most Common Objection

When someone first encounters the idea of an AI reasoning language, the first thing they say is:

"Structured formats already exist, don't they?"

They are right. They exist. Many of them.

There is Markdown.
There is JSON.
There is XML.
YAML, TOML, Protocol Buffers, MessagePack, CSV...

The world overflows with data formats.
So why is AI still thinking in natural language?

To answer this question, we must pinpoint exactly what each format does well
and what it cannot do.

---

## Markdown: The Current Memory of AI Agents

As of 2026, the format most widely used by AI agents is Markdown.

Claude Code remembers in `.md` files.
GPT-based agents also leave notes in Markdown.
CLAUDE.md, memory.md, notes.md.
AI's long-term memory stands on Markdown at this very moment.

Why Markdown? The reason is simple.
LLMs read and write Markdown well.
Markdown is abundant in training data,
and its structure is simple enough for easy generation and parsing.

But Markdown is **a document format meant for humans to read.**

```markdown
# Project Status
## Cache Strategy
- SIMD bitmask adopted (decided 1/28)
- GPU acceleration under review
## Unresolved
- Query generation method TBD
```

How does a machine interpret this?

There is a section heading called "Cache Strategy."
Under it, there is an item "SIMD bitmask adopted."
There is a date "(1/28)" in parentheses.

A machine cannot understand this structurally.
It can tell from `##` that "Cache Strategy" is a section heading,
but the semantic relationship that it is "a subtopic of architecture" does not exist in Markdown.
A human knows "1/28" is a date, but a machine has to guess.
January 28th, or one twenty-eighth?

Ultimately, to "understand" Markdown, an LLM must perform natural language interpretation.
Markdown is natural language with indentation layered on top ---
it is not structured data.

---

## JSON: Structure Without Meaning

JSON goes one step further than Markdown.

```json
{
  "entity": "Yi Sun-sin",
  "birth": "1545",
  "death": "1598",
  "occupation": "naval_commander"
}
```

There is structure. Key-value pairs are explicit.
A machine can parse it. Fields are accessible.

But there is a problem.

**JSON does not know what the key "entity" means.**

The person who created this JSON knows that "entity" means "an object."
In another person's JSON, the same concept might be "name," "subject," or "item."

```json
{"name": "Yi Sun-sin"}
{"subject": "Yi Sun-sin"}
{"item": "Yi Sun-sin"}
{"entity": "Yi Sun-sin"}
```

Four JSONs express the same thing,
but a machine cannot know they are the same.

JSON lacks **shared semantics.**
There is structure, but there is no agreement on what that structure means.

Every project creates its own schema.
Every API uses its own field names.
Connecting schema A to schema B requires yet another transformation layer.

This is the Tower of Babel.
Structure exists, but no one understands each other's structure.

---

## XML: The Tax of Verbosity

XML tried to solve JSON's problem.

Namespaces, schema definitions (XSD), document type definitions (DTD).
It provides meta-structures that define the meaning of structures.

```xml
<entity xmlns="http://example.org/schema">
  <name>Yi Sun-sin</name>
  <birth>
    <year>1545</year>
    <calendar>lunar</calendar>
  </birth>
  <death>
    <year>1598</year>
    <cause>killed_in_action</cause>
  </death>
</entity>
```

Meaning can be defined. Structure can be enforced with schemas.
It is more rigorous than JSON.

But XML has a fatal problem.

**It is verbose.**

In the XML above, the actual information is "Yi Sun-sin, 1545, 1598, killed_in_action."
Everything else is tags. Opening and closing tags outnumber the information.

Why is this a problem for AI?

The context window of an LLM is finite.
If conveying the same information requires 3x the tokens,
the amount of information that fits in the context shrinks to one-third.

XML is verbose so that humans can read it easily.
An AI reasoning language must not have this waste.
For an LLM, the `<name>` tag is waste.

And XML is a design from the early 2000s.
It was created in an era when LLMs did not exist, for humans and traditional software.
It was never designed as an AI reasoning language.

---

## The Shared Limitation

Markdown, JSON, XML.
Each of the three formats has its strengths, but they share common limitations.

**They are text-based.**
All of them serialize into strings.
A machine must parse them to process them.
Parsing is a cost.

An ideal reasoning language is a binary stream.
A sequence of 16-bit words. No parsing needed.
Interpretable the instant it is read.

**They were designed before the LLM era.**
Markdown is from 2004. JSON is from 2001. XML is from 1998.
They were designed in an era when the concept of LLMs did not exist,
for humans or traditional software.

An AI reasoning language must be designed in the LLM era, for LLMs.
The design principle "1 word = 1 token"
presupposes the existence of LLMs.

**Their unified semantic system is absent or incomplete.**
Markdown has no semantic system at all.
JSON has structure but no meaning.
XML can define schemas but they are not unified.

A semantically-aligned index is a globally unified meaning ID.
Wherever it is used, the same SIDX means the same thing.
No conversion needed. Consensus is built in.

---

## Summary

| Format | Structure | Meaning | LLM-Friendly | Binary | Claim Support | Verb Modifiers |
|--------|-----------|---------|---------------|--------|---------------|----------------|
| Markdown | Weak | None | High | No | None | None |
| JSON | Yes | None | Medium | No | None | None |
| XML | Yes | Partial | Low | No | None | None |
| **Ideal Reasoning Language** | **Yes** | **Yes** | **High** | **Yes** | **Yes** | **Yes** |

A new format is needed not because existing formats are bad.
It is because existing formats were made in a different era, for a different purpose.

Markdown was made for documents that humans read.
JSON was made for data exchange in web APIs.
XML was made for general-purpose serialization of documents and data.

A format for recording and accumulating AI's reasoning. That does not yet exist.

When the purpose is different, the tool must be different.
