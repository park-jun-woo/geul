---
title: "Why Exploration Is Necessary"
weight: 7
date: 2026-02-26T12:00:07+09:00
lastmod: 2026-02-26T12:00:07+09:00
tags: ["exploration", "search", "scale"]
summary: "When the index exceeds the window, the search paradigm itself hits its limit"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## When the index exceeds the window, the search paradigm itself hits its limit.

---

## Search Has Succeeded

We discussed the limits of RAG.
The inaccuracy of embedding similarity, the arbitrariness of chunk splitting, the impossibility of quality judgment.

But that discussion was about the quality of search.
"How should we search more accurately?"

Now a different question must be asked.
Assume search is perfect.
Assume it returns only information precisely relevant to the query.

There are still cases where it does not work.

---

## The Problem of Scale

An internal knowledge base has 1,000 statements.
There is an index. Put the index in the context. Query. Retrieve results.
It works.

Statements grow to 100,000.
The index gets larger. It still fits in the window. It works.

Statements grow to 10 million.
The index itself exceeds the window.

This is not a problem of search quality.
No matter how accurate the search is,
if the index that must be consulted to search does not fit in the window,
the search cannot even begin.

And knowledge grows.
Corporate documents increase every day.
What an agent has learned keeps accumulating.
The world's knowledge does not shrink.

Does a bigger window solve this?
If 128K becomes 1M becomes 10M?
If knowledge reaches 100M, the same problem repeats.
The window is always finite, and knowledge always grows.
This imbalance is permanent.

---

## The Difference Between Search and Exploration

Search obtains results with a single query.

Query: "Samsung Electronics Q3 2024 operating profit"
-> Result: 9.18 trillion won.

One shot. Done.

Exploration reaches results through multiple steps.

Step 1: View the top-level knowledge map. "Corporations," "Industries," "Macroeconomics," "Technology"...
-> Select "Corporations."

Step 2: View the corporations map. "Samsung Electronics," "SK Hynix," "Hyundai Motor"...
-> Select "Samsung Electronics."

Step 3: View the Samsung Electronics map. "Finance," "HR," "Technology," "Legal"...
-> Select "Finance."

Step 4: View the finance map. "Quarterly results," "Annual results," "Investment plans"...
-> Select "Quarterly results."

Step 5: Retrieve "Q3 2024" from the quarterly results.
-> Operating profit: 9.18 trillion won.

The result is the same.
The process is different.

Search is asking "Do you have this?"
Exploration is tracking down "Where might it be?"

Search requires the index to be visible to the querier. The entire index must be accessible.
Exploration only needs to see the current layer of the map. At each step, only one layer enters the window.

---

## The Library Analogy

You visit a neighborhood library.
It has 3,000 books.
You ask the librarian: "Do you have a biography of Yi Sun-sin?"
The librarian remembers: "It's at the end of shelf 3."
Search. It works.

You visit the National Library.
It holds 10 million volumes.
You ask the librarian: "Do you have a biography of Yi Sun-sin?"
The librarian does not know either. Nobody memorizes 10 million volumes.

Instead, there is a classification system.

You check the first-floor directory. -> The "History" section is on the 3rd floor.
You go to the 3rd floor. -> "Korean History" is in the east wing.
You go to the east wing. -> "Joseon Dynasty" is in row D.
You go to row D. -> "Figures" is in the 3rd section of row D.
You search the 3rd section. -> There is a biography of Yi Sun-sin.

The librarian's memory capacity has not changed.
The library's scale has changed.
The method shifted from asking the librarian (search) to walking the classification system (exploration).

Here is the key.
At each step, the size of what must be viewed fits within the librarian's memory capacity.
The first-floor directory. The 3rd-floor zone map. The list of rows in the east wing. The list of sections in row D.
All fit in a single glance.

The complete catalog of all holdings does not fit in a single glance.
But the map of each floor does.

This is how exploration differs from search.
You do not need to see the whole at once.
You only need to judge the next direction from where you currently stand.

---

## Maps of Maps

In technical terms, this is a hierarchical structure of maps.

**Level 1 map**: the top-level classification of all knowledge.
"This knowledge base contains information on corporations, industries, macroeconomics, and technology."
Dozens of items. Fits in the window.

**Level 2 map**: the subcategories of each top-level classification.
"The corporations category contains Samsung Electronics, SK Hynix, Hyundai Motor..."
Dozens to hundreds of items. Fits in the window.

**Level 3 map**: the detailed categories of each subcategory.
"Samsung Electronics contains Finance, HR, Technology, Legal..."
Dozens of items. Fits in the window.

**Actual statements**: the concrete information pointed to by the lowest-level map.
"Samsung Electronics' Q3 2024 operating profit was 9.18 trillion won."

If each layer's size fits within the window,
exploration is possible regardless of the total scale of knowledge.

Even with 10 million statements,
if each layer has 100 items, you reach the target in 5 exploration steps.
100 -> 100 -> 100 -> 100 -> 100 = coverage up to 10 billion.
At each step, only 100 items enter the window.

This is the same way a B-tree finds data on disk.
It does not load all the data into memory.
It reads only the current node of the tree and moves to the next.
Data of any scale can be explored regardless of memory size.

The context window is memory.
The knowledge base is disk.
The map is a B-tree node.

---

## The Agent Walks

In multi-step exploration, who selects the direction at each step?

The agent.

Put the level 1 map in the context.
The agent reads it, compares it to the query, and selects the "Corporations" direction.

Request the level 2 map.
The subcategory map of corporations enters the context.
The agent reads it and selects the "Samsung Electronics" direction.

Request the level 3 map.
The agent selects "Finance."

This is the agent's tool use.
Reading a map is a tool call.
Selecting a direction is a judgment.
Requesting the next map is the next tool call.

In search, the agent queries once and receives a result. Passive.
In exploration, the agent makes multiple judgments and selects directions. Active.

This is where context engineering meets agent design.
What goes into the context is determined step by step through the agent's judgment.
Context construction shifts from static assembly to dynamic exploration.

---

## This Problem Is Barely Discussed Today

Looking at discussions in the RAG community,
most energy is focused on search quality.

Better embedding models.
Better chunking strategies.
Reranker architectures.
Hybrid search.
Graph RAG.

All important.
All about "how to get better results from a single search."

"What if a single search is not enough?" is barely discussed.

The point when the index exceeds the window.
The point when results are too numerous to fit.
The point when the scale of knowledge breaks the premise of the search paradigm itself.

That point is coming.
Knowledge grows and the window is finite.

Most current solutions are avoidance.
Retrieve only the top k. Discard the rest.
Enlarge the window. Costs increase.
Partition the knowledge. Separate vector stores per domain.

All of them encounter the same problem again when the scale grows further.

---

## Prerequisites for Exploration

For exploration to work, knowledge must be in an explorable structure.

**Hierarchy must exist.** If knowledge is laid out flat, exploration is impossible. An embedding vector store is flat. All chunks are at the same level. There is no hierarchy, so the concept of "going deeper" does not exist.

**Each layer must fit in the window.** If a single map exceeds the window, exploration fails. The number of choices at each level of the hierarchy must be of appropriate size. This is a classification design problem.

**Paths must be diverse.** It must be possible to reach the same information through multiple paths. Via "Samsung Electronics -> Finance -> Operating profit" or via "Semiconductor industry -> Major companies -> Samsung Electronics -> Results." Because the natural path varies depending on the question. If the classification criterion is fixed to one, it fits some questions and not others.

A folder structure has hierarchy but only one path.
A file belongs to only one folder.
Only the path "Samsung Electronics/Finance/Operating profit" exists.
When a question about "the semiconductor industry" comes in, natural exploration through this folder structure is impossible.

A graph has both hierarchy and diverse paths.
A single node can be connected to multiple parent nodes.
The Samsung Electronics node can be reached via a "Corporations" path, a "Semiconductor industry" path, or a "KOSPI-listed companies" path.
Regardless of the context from which a question originates, a natural path exists.

---

## This Is an Unsolved Problem

There is something that must be said honestly.

The need for multi-step exploration is clear.
But there is no standard system that implements this effectively yet.

How do you automatically generate the hierarchy of maps?
How do you determine the appropriate size of each layer?
What happens when the agent selects the wrong direction?
What happens to latency as exploration depth increases?

These are open questions.

But the fact that a problem is unsolved
does not mean the problem does not exist.

Knowledge is growing.
The window is finite.
The point where search alone is not enough is coming.

Exploration must be ready as an answer for that point.
If it is not ready,
the only choices left are to enlarge the window or to discard knowledge.

---

## Summary

Search returns results with a single query.
When the scale of knowledge grows large enough, this is not sufficient.
Because the index itself exceeds the window.

Exploration follows hierarchical maps, selecting directions as it descends.
What must be viewed at each step fits within the window.
Each step is finite regardless of total scale.
Just as a B-tree finds data without loading the entire disk into memory.

The agent judges the direction at each step.
Context construction shifts from static assembly to dynamic exploration.
This is where context engineering meets agent design.

For exploration to work, knowledge must be hierarchical, each layer must be finite, and paths must be diverse.
A folder structure has only one path. A graph has diverse paths.

This is still an unsolved problem with no standard solution.
But as long as knowledge grows and the window is finite, it is a problem that must be solved.
