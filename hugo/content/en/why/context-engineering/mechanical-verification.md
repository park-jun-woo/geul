---
title: "Why Mechanical Verification Is Necessary"
weight: 4
date: 2026-02-26T12:00:10+09:00
lastmod: 2026-02-26T12:00:10+09:00
tags: ["verification", "specification", "compiler"]
summary: "Natural language has no concept of an invalid sentence"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Natural language has no concept of an "invalid sentence."

---

## Nobody Inspects What Enters the Context

Look at how information enters the context in current LLM pipelines.

RAG returns chunks.
An agent receives API responses.
Previous conversations accumulate in the history.
A user uploads a document.

These go into the context window.
Without inspection.

Why is there no inspection?
Because natural language has no concept of "invalid."

---

## Natural Language Accepts Every String

In programming, there is such a thing as a syntax error.

```python
def calculate(x, y
    return x + y
```

The parenthesis is unclosed. It is rejected before execution.
Code can be definitively declared "this is not valid code" before it is run, before it is even read.

Natural language has no such thing.

"He went to the bank."
Grammatically perfect.
You cannot tell who went, which bank, or why,
but nothing violates the grammar rules of natural language.

"Sales report for the 45th of the 13th month, 2024."
There is no 13th month and no 45th day.
Yet nothing violates the grammar rules of natural language.
It is a grammatically valid sentence.

"Source: unknown. Confidence: unknown. Date: unknown. Samsung Electronics' market cap is 1,200 trillion won."
The source is unknown, the confidence is unknown, the reference date is unknown.
Yet nothing violates the grammar rules of natural language.

Natural language accepts everything.
An invalid natural language sentence structurally does not exist.
Therefore, there is no mechanical criterion for "rejecting" information expressed in natural language.

---

## What It Takes for Mechanical Verification

Look at the Go compiler.

Go refuses to compile if there is an unused import.
Even if the code works perfectly.
Even if there is nothing wrong with the logic.
It refuses solely because one import line is unused.

This is mechanical verification.

Mechanical verification has three characteristics.

**It is deterministic.** The result is yes or no. Not a probability. There is no "it's probably fine." Valid or invalid.

**It is cheap.** No LLM call needed. String comparison, field existence check, value range check. CPU operations on the nanosecond scale.

**It does not read meaning.** It does not judge whether the content is true or false. It only checks whether the format conforms to the specification. It does not know whether "Samsung Electronics' market cap is 1,200 trillion won" is true. But it knows whether the source field is empty.

For these three things to be possible, there is one prerequisite.
Information must have a specification.

If there is a specification, violations are defined.
If violations are defined, rejection is possible.
If rejection is possible, verification exists.

Natural language has no specification, so there are no violations.
No violations means no rejection.
No rejection means no verification.

---

## Why Pre-Context Verification Is Needed

The context window is finite.

Whether it is 128K tokens or 1M tokens, it is finite.
The quality of information entering a finite space determines the quality of the output.

Yet in current pipelines,
quality judgment happens only after information enters the context.
You expect the LLM to read it, judge it, and conclude on its own that "this information is hard to trust."

This is wrong in three ways.

**It is expensive.** You are using LLM inference costs to do format checking. You run a model with billions of parameters to filter out chunks with no source. You use probabilistic reasoning for a task that requires checking a single field.

**It is unreliable.** There is no guarantee the LLM will always ignore information without a source. In fact, once something is in the context, the LLM is more likely to use it. Expecting the model to ignore something you put in the context is a contradiction.

**It is late.** The window space is already consumed. If 5 chunks without sources take up 200 tokens each, 1,000 tokens are wasted. Even if they are filtered out, that space is already spent.

Mechanical verification comes before all of this.
Before entering the context.
Before the LLM reads it.
Before the window is consumed.

---

## What Gets Verified

Mechanical verification checks not the truth of content but conformance to a format specification.

Specifically, these things:

**Structural completeness.** Do required fields exist? Does the edge have a subject and object? Is anything missing?

**Identifier validity.** Does the referenced node exist? Does what is written as "Samsung Electronics" actually point to a defined entity? Is the reference dangling?

**Type conformance.** Is there a date in the date field? Is there a number in the number field? "The 45th of the 13th month, 2024" gets caught here.

**Metadata presence.** Is there a source field? Is there a time field? Is confidence specified? If not, reject, mark as absent, or assign a default.

**Referential integrity.** Does the node pointed to by the edge actually exist? Is it referencing a deleted node?

These checks share one thing in common.
All of them can be performed without reading the content.
You do not know whether "Samsung Electronics' market cap is 1,200 trillion won" is true.
But you know whether a source is specified for this statement.
You know whether a time is recorded for this statement.
You know whether the format of this statement conforms to the specification.

---

## Cheap Comes First

In a context engineering pipeline, inspections have an order.

**Mechanical verification**: specification conformance. Cost near zero. Deterministic.
**Semantic filtering**: relevance, trustworthiness, usefulness judgment. High cost. Probabilistic.
**Consistency checking**: contradictions among selected pieces of information. Even higher cost. Requires reasoning.

If you arrange them from cheapest to most expensive,
the expensive checks have less to process.

If mechanical verification filters out 30% of statements lacking a source,
semantic filtering only needs to process 70%.
If semantic filtering removes the irrelevant,
consistency checking handles an even smaller set.

This is the same principle as database query optimization.
Apply index-filterable conditions in the WHERE clause first.
Full-scan conditions come later.
If cheap comes first, the burden on the expensive part decreases.

Conversely,
if you run the expensive check first and the cheap check later,
you discover format errors only after you have already spent the cost.
You analyze the meaning of a statement that references a nonexistent node,
only to discover afterward that the reference is invalid.

---

## This Order Is Impossible in a Natural Language Pipeline

Natural language has no specification, so mechanical verification is impossible.
Since mechanical verification is impossible, the cheapest check does not exist.

Consequently, every check is a semantic check.
Every check requires an LLM.
Every check is expensive.

"Does this chunk have a source?" -- The LLM must read it.
"Is the time reference of this chunk appropriate?" -- The LLM must read it.
"Is the format of this chunk correct?" -- Natural language has no format, so the question itself does not hold.

This is the reality of current context engineering.
Even the simplest check is performed with the most expensive tool.
A task that could end with string comparison is handled by an inference engine.

---

## Prerequisites for Verification

For mechanical verification to exist, three things are needed.

**A specification.** The format that information must follow must be defined. Which fields are required, which values are allowed, which references are valid. Without a specification, violations cannot be defined.

**Formalization.** Information must be expressed in the format the specification requires. Not as natural language sentences, but encoded in the structure the specification demands. Information that is not formalized cannot be inspected.

**The power to reject.** It must be possible to actually reject information that does not conform. If you inspect but always pass, it is not verification. Invalid information must be prevented from entering the context.

These three things are taken for granted in programming languages.
There is a specification called grammar, a format called code, and a power to reject called the compiler.

In natural language, all three are absent.
Grammar is not a format specification but a convention.
Sentences are not structured formats but free text.
The concept of "invalid natural language" does not exist, so there is nothing to reject.

To introduce mechanical verification into context engineering,
the representation of information itself must change.

---

## Summary

In the current context pipeline, information enters the context without inspection.
Because natural language has no concept of an "invalid sentence."

Mechanical verification checks not the truth of content but conformance to a format specification.
Structural completeness, identifier validity, type conformance, metadata presence, referential integrity.
Deterministic, cheap, and it does not read meaning.

In the pipeline, cheap checks must come first.
If mechanical verification filters out format errors,
the expensive semantic judgments have less to process.

Natural language has no specification, so this check is impossible.
Every check becomes a semantic check, and every check is expensive.

For mechanical verification to be possible,
there must be a specification, formalization, and the power to reject.
The representation of information itself must change.
