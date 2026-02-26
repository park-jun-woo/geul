---
title: "Why Embedding Vectors Are Not Enough"
weight: 11
date: 2026-02-26T12:00:18+09:00
lastmod: 2026-02-26T12:00:18+09:00
tags: ["embedding", "vector", "whitebox"]
summary: "Rearranging embedding vectors breaks the model. Avoiding breakage means rebuilding the model from scratch. What we need is not transparency inside the black box, but a transparent layer outside it."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Vectors are great for computation, but impossible to interpret. You cannot make the inside of a black box transparent.

---

## Embedding vectors are a remarkable technology

"King - Man + Woman = Queen."

When word2vec demonstrated this, the world was astonished.
Represent words as vectors with hundreds of dimensions,
and semantic relationships emerge as vector arithmetic.

Embedding vectors are the foundation of LLMs.
Everything in a transformer is vector computation.
Tokens become vectors.
Attention computes similarity between vectors.
Outputs are converted from vectors back to tokens.

Similar meanings are nearby vectors.
Different meanings are distant vectors.
Search is vector similarity computation.
Classification is boundary-setting in vector space.

Without embedding vectors, today's AI would not exist.

So why not just use embedding vectors to represent knowledge?
Align vectors directly, structure them, make them interpretable.

It does not work.
The surest way to know this is to try.

---

## AILEV: We tried

The GEUL project originally started under the name AILEV.

AI Language Embedding Vector.

The name itself declared the purpose:
an AI language that directly manipulates embedding vectors.

The concept was this:

Represent meaning with 512-dimensional vectors.
Assign roles to segments of the vector.
The first 128 dimensions for entities, the next 128 for relations, the next 128 for properties, the rest for metadata.
Just as RGBA decomposes color into four channels, decompose meaning into dimensional segments.

Train BERT to convert natural language into these structured vectors.
When "Seoul is the capital of Korea" is input,
the entity segment produces the Seoul vector, the relation segment produces the capital vector, the property segment produces the Korea vector.

Since they are vectors, computation is possible.
Similarity search is possible.
Reduce dimensions and you get graceful degradation.
Going from 512 to 256 dimensions loses precision but preserves core meaning.

It was elegant. In theory.

---

## Why it fails

### Arbitrarily rearranging vectors breaks the model

The embedding vectors of an LLM are the product of training.

After reading billions of texts,
the model self-optimizes its internal representations.
What each dimension means is something the model decided.
Not something a human decided.

What happens if you declare "the first 128 dimensions are for entities"?

In the vector space the model learned,
entity information does not reside in the first 128 dimensions.
It is distributed across all 768 dimensions.
Relation information, property information, tense information — all mixed together.

This is not a design mistake but the nature of learning.
Backpropagation finds
the vector arrangement optimal for the task.
It does not find an interpretable arrangement.
Optimal and interpretable are not the same thing.

If you forcibly rearrange vectors — "entities here, relations there" —
the statistical relationships the model learned break.
Performance degrades.

### Rearranging without breaking means rebuilding the model

Then why not train from scratch with the constraint "the first 128 dimensions are for entities"?

You can. In theory.
But this is not aligning embedding vectors.
It is designing a new model architecture.

You need training data. Billions of tokens.
You need training infrastructure. Thousands of GPUs.
You need training time. Months.
And there is no guarantee the resulting model will perform as well as existing LLMs.

The effort is too large.

The problem of "align vectors to make them interpretable"
has transformed into "rebuild an LLM from scratch."
This is not solving the problem but expanding it.

### Interpretation is impossible

Suppose you did manage to create a structured vector.
A 512-dimensional vector.
Say the first 128 dimensions are for entities.

The entity segment reads `[0.23, -0.47, 0.81, 0.12, ...]`.

How do you know whether this is "Samsung Electronics" or "Hyundai Motor"?

You have to find the nearest vector.
You have to compute similarity in a vector database.
And you get a probabilistic answer: "probably Samsung Electronics."

"Probably."

Vectors are inherently continuous.
Between the vectors for Samsung Electronics and SK Hynix,
infinitely many intermediate vectors exist.
Nobody knows what those intermediate vectors mean.

This is not a technical limitation but a mathematical truth.
Representing discrete meanings in continuous space
makes boundaries ambiguous.
Ambiguity was [the problem with natural language](/why/natural-language-hallucination/).
We switched to vectors, and the ambiguity returned.

Only the form changed.
In natural language, the ambiguity of words.
In vectors, the ambiguity of coordinates.

---

## The whitebox principle

Here the fundamental design issue reveals itself.

Embedding vectors are a black box.
Looking at a 768-dimensional real-valued vector, no one can tell
what information is encoded where.
The model itself cannot explain it.

This is not an inconvenient trait but an ontological property.
This is precisely why vectors work.
Because they arrange information in ways humans did not design,
they work better than anything humans would have designed.
Uninterpretability is not a bug but a feature.

Yet knowledge used as AI context demands the opposite.

You need to know the source.
You need to know the timestamp.
You need to know the confidence level.
You need to know what the statement is about.
You need to know whether two statements refer to the same entity.

Every requirement is "need to know." Every requirement demands interpretability.

Satisfying whitebox demands with a black-box vector
is a contradiction.

---

## The logic of the pivot

The pivot from AILEV to GEUL was not a retreat.
It was a redefinition of the problem.

**Original problem:** LLMs are black boxes. Let us make the inside transparent.
Then let us make embedding vectors interpretable by aligning them.
But touching the vectors breaks the model.
Avoiding breakage means rebuilding the model.
Dead end.

**Redefined problem:** There is no need to make the inside of the black box transparent. Let us build a transparent layer on the outside.
Leave the LLM's internals untouched.
Outside the LLM, create an interpretable representation system.
The LLM can read and write that system. Because it is tokens.
An artificial language.

Not vectors but language.
Not continuous but discrete.
Not uninterpretable but interpretation as the sole purpose.
Not inside the model but outside the model.

AILEV's "Embedding Vector" was dropped,
and GEUL — meaning "writing" — took its place. This is why.

---

## Vectors for computation, language for representation

This is not a rejection of embedding vectors.

Vectors are optimized for computation.
Similarity search, clustering, classification, retrieval.
Language cannot replace what vectors do.

Language is optimized for representation.
Entity identity, relational description, embedded metadata, interpretability.
Vectors cannot replace what language does.

They are tools at different layers.

Inside the LLM, vectors operate. A black box. As it should be.
Outside the LLM, language operates. A white box. As it should be.

The problem started when these two layers were confused.
We tried to make vectors do the job of language.
We tried to assign a black box the role of a white box.

Each has its place.

---

## Summary

Embedding vectors are the foundation of LLMs and a remarkable technology.
Yet as a means of knowledge representation, they have fundamental limits.

GEUL started as AILEV (AI Language Embedding Vector).
The goal was to directly align vectors and make them interpretable.
It failed. For two reasons.

Arbitrarily aligning vectors breaks the relationships the model learned.
Aligning without breaking means rebuilding the model from scratch. The effort is too large.

And even if it succeeded, vectors cannot be interpreted.
In continuous space, the boundaries of discrete meaning are ambiguous.
You cannot assign a black box the role of a white box.

The logic of the pivot:
We tried to make the inside of the black box transparent.
Touching the inside breaks it.
Instead, leave the inside alone and build a transparent layer on the outside.
Not vectors but language. Not inside the model but outside the model.

Vectors for computation, language for representation.
Each has its place.
