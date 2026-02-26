---
title: "Why RAG Is Not Enough"
weight: 2
date: 2026-02-26T12:00:11+09:00
lastmod: 2026-02-26T12:00:11+09:00
tags: ["RAG", "search", "embedding"]
summary: "Looking relevant and being relevant are not the same thing"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Looking relevant and being relevant are not the same thing.

---

## RAG Is the Current Standard

As of 2024, RAG is the most common way enterprises put LLMs to work.

Retrieval-Augmented Generation.
Search external documents, stuff them into the context, and have the model answer based on that.

RAG works.
It lets LLMs reference internal documents they were never trained on.
It lets them reflect up-to-date information.
It significantly reduces hallucinations.

Without RAG, enterprise adoption of LLMs would have been far slower.
RAG is a technology that deserves respect.

But RAG has fundamental limitations.
These limitations are not solved by building better RAG.
They stem from the very premise of RAG itself.

---

## How RAG Works

The core of RAG is three steps.

**Step 1: Split documents into chunks.**
PDFs, wikis, internal docs are divided into fixed sizes (typically 200--500 tokens).

**Step 2: Convert each chunk into an embedding vector.**
A real-valued vector of hundreds to thousands of dimensions.
The "meaning" of the text mapped to a single point in vector space.

**Step 3: When a query comes in, find similar vectors.**
The query is also converted into a vector.
The top 5--20 chunks with the highest cosine similarity are selected and inserted into the context.

Simple and elegant.
And here lie three fundamental problems.

---

## Problem 1: Similar Is Not Relevant

Embedding similarity measures "whether two texts use similar words in similar contexts."

This is not relevance.

Example.

Query: "What was Apple's Q3 2024 revenue?"

Chunks embedding search might return:
- "Apple's Q3 2024 revenue was $94.9 billion." -- Relevant
- "Apple's Q3 2023 revenue was $81.8 billion." -- Similar but different time period
- "Samsung Electronics' Q3 2024 revenue was 79 trillion won." -- Similar but different company
- "An apple pie has about 296 kcal." -- Keyword overlap

Embedding similarity cannot distinguish these four.
In vector space, "Apple revenue" clusters around a single region.
Whether it's 2023 or 2024, Apple or Samsung --
vector distance does not reliably separate them.

Adding a reranker improves things.
But a reranker also reads and judges natural language text,
so the fundamental ambiguity problem remains.

Semantic-structure-based search is different.
If "Apple" the entity has a unique identifier,
it is never confused with "apple" the fruit.
If "Q3 2024" is a time field,
it is mechanically distinguished from "Q3 2023."

No need to compute similarity.
Does it match or not? Yes or no.

---

## Problem 2: Chunks Are Not Units of Meaning

Look at the first step of RAG again.
"Split documents into chunks."

That "split" is the problem.

When you split a document into 500-token units,
meaning is cut in the middle.
A paragraph spans two chunks.
The premise and conclusion of an argument are separated.

"Yi Sun-sin faced 133 ships with only 12 at the Battle of Myeongnyang" is in Chunk A,
and "scholars dispute these figures" is in Chunk B.
If only Chunk A is retrieved for a query,
the confidence information enters the context already lost.

Make chunks bigger? They consume more of the window.
Make chunks smaller? More context gets cut.
Add overlap? You waste the window on duplicates.

No matter how you adjust, the fundamental problem is the same.
Splitting natural language text by token count
is the same as splitting meaning by token count.
Meaning has an inherent size,
and dividing it by an unrelated unit causes problems.

In a structured representation, units of meaning are explicit.
One predication is one edge.
An edge is not split.
Search operates at the edge level.
There is no cutting in the middle of meaning.

---

## Problem 3: The Quality of Retrieved Results Is Unknown

RAG returned 5 chunks.
Before putting these 5 into the context, there are questions to ask.

What is the source of this information?
What is the reference date?
How certain is it?
Do these 5 contradict each other?

In natural language chunks, you cannot know these things.

The source may or may not be mentioned somewhere in the chunk as natural language.
The time reference may be somewhere in the document, or it may have been lost when the chunk was split.
Confidence has no structural slot in natural language, so it is almost always absent.
Contradiction checking requires reading all 5 chunks and reasoning over them.

In the end, you have to delegate quality judgment to the LLM.
You use RAG to reduce LLM call costs,
but you call the LLM to verify RAG results.

In a structured representation, source, time, and confidence are fields.
"Exclude statements without a source" is one query line.
"Exclude information before 2023" is one field comparison.
"Exclude confidence below 0.5" is one numeric comparison.
No LLM call needed.

---

## The Fundamental Premise of RAG

The root of these three problems is one thing.

RAG searches natural language as natural language.

The documents are natural language.
The chunks are natural language.
The embeddings are statistical approximations of natural language.
The search results are natural language.
What enters the context is natural language.

The ambiguity of natural language permeates the entire pipeline.

Search is inaccurate because you search ambiguous content in its ambiguous form.
Context is lost because you split ambiguous content by a size unrelated to meaning.
Verification is impossible because you cannot extract quality information from ambiguous content.

Most attempts to improve RAG operate within this premise.

Use a better embedding model. -- The statistical approximation becomes more refined, that's all.
Use a better chunking strategy. -- The split positions improve, that's all.
Add a reranker. -- You read the natural language one more time, that's all.
Use hybrid search. -- You mix keywords and similarity, that's all.

All of them work.
All of them remain within the frame of natural language.
None of them are fundamental.

---

## Conditions for a Fundamental Alternative

To go beyond the limits of RAG, the premise must change.
Not searching natural language as natural language,
but searching structured representations structurally.

This alternative must satisfy three conditions.

**Search by match, not by similarity.**
Not finding "things that look similar"
but finding "things that match."
Does the identifier match? Is it within the time range?
Yes or no. Not a probability.

**The unit of meaning is the unit of search.**
Not splitting by token count
but storing by predication and searching by predication.
No cutting in the middle of meaning.

**Metadata is embedded in the structure.**
No need to call an LLM to judge the quality of search results.
Source, time, and confidence are fields,
so mechanical filtering is possible.

When these three conditions are met,
search shifts from "guessing plausible candidates"
to "confirming what matches."

---

## RAG Is a Transitional Technology

This is not to disparage RAG.

RAG was the best answer in a world where natural language was all there was.
When documents were natural language, knowledge was stored in natural language,
and LLMs were tools that process natural language,
searching natural language with natural language was the obvious choice.

And RAG does work.
An LLM with RAG is far more accurate than one without.
This is a fact.

But if the premise of "a world where natural language is all there is" changes,
RAG's position changes too.

If structured representations exist,
RAG becomes the front end that "takes natural language input and searches a structured store."
Natural language -> structured query -> structural search -> structured results -> context.

RAG does not disappear.
Its backend changes.
From embedding similarity search to semantic-structure-based search.

---

## Summary

RAG is the current standard for context engineering.
And it has three fundamental limitations.

1. **Similar ≠ relevant.** Embedding similarity does not guarantee relevance. "Looks similar" and "is relevant" are different.
2. **Chunk ≠ meaning.** Splitting by token count cuts in the middle of meaning. Premises and conclusions are separated. Confidence information is lost.
3. **Quality judgment is impossible.** The source, time, and confidence of retrieved chunks cannot be determined mechanically. Judging them requires an LLM call.

The root of the three problems is one thing.
Searching natural language as natural language.

The fundamental alternative is to change the premise.
Match, not similarity.
Predication, not token chunks.
Embedded metadata, not external judgment.

RAG is a transitional technology.
It was the best answer in a world where natural language was all there was.
When that premise changes, RAG's backend changes.
