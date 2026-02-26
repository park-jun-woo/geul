---
title: "Why a Semantically-Aligned Index?"
weight: 15
date: 2026-02-26T12:00:03+09:00
lastmod: 2026-02-26T12:00:03+09:00
tags: ["SIDX", "semantic alignment", "index"]
summary: "When meaning is engraved in bits, search becomes reasoning"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## What Happens When an ID Is Knowledge, Not an Address

---

## An Address Knows Nothing

To find Yi Sun-sin in a database, you need an ID.

In Wikidata, Yi Sun-sin's ID is `Q8492`.

This number points to Yi Sun-sin.
But the string `Q8492` itself knows nothing.

It does not know whether this is a person or a building.
It does not know whether this is a Korean or a French citizen.
It does not know whether this is a 16th-century figure or a 21st-century one.
It does not know whether they are alive or dead.

`Q8492` is an address.
A letter carrier delivering mail has no idea what is written inside the envelope.
They simply look at the address on the envelope and deliver.

UUID is the same. `550e8400-e29b-41d4-a716-446655440000`.
128 bits of random numbers. Unique only to avoid collisions --
it tells you nothing about what it refers to.

For the past fifty years, database IDs have worked this way.
An ID is an address, and to learn anything, you must follow that address and read the data.

---

## You Have to Follow It to Know

Why is this a problem?

Suppose you want to find "a male philosopher of German nationality born in the 19th century."

In a traditional database, this is how it works:

```
1. Filter persons table where gender = 'male'
2. JOIN with nationalities table and filter country = 'Germany'
3. JOIN with birth_dates table and filter year BETWEEN 1800 AND 1899
4. JOIN with occupations table and filter occupation = 'philosopher'
```

Four JOIN operations.
Each JOIN compares rows across two tables.
If the tables are large, it traverses an index; if there is no index, it performs a full scan.
With a billion records, this process takes seconds to tens of seconds.

Why is it so complex?

Because the ID knows nothing.
Looking at `Q8492`, you cannot tell whether this is a German or a Korean,
so you must go to another table to retrieve that information.

For every question, you must follow where the ID points.
This is the cost databases have been paying for fifty years.

---

## What If the ID Already Knew?

Let us flip the premise.

What if the ID itself contained the essential information?

What if, simply by looking at the ID,
you could tell whether it refers to a human, which country they are from,
which era they belong to, and how they are classified?

To find "a 19th-century German male philosopher,"
JOINs become unnecessary.

Scanning through a billion IDs,
you can instantly determine whether each one matches by examining its bits.

This is the core idea behind the Semantically-Aligned Index.

---

## Aligning Meaning into the ID

SIDX (Semantically-Aligned Index) is a 64-bit identifier.

These 64 bits are not random numbers.
Meaning is assigned to the position of each bit.

The upper bits hold the most important information.
What kind of entity is this? A person, a place, an event, a concept?

The next bits hold classification information.
If it is a person, which era? Which region?

Lower bits carry increasingly specific information.

The key principle is this:

> The order of the bits is the order of information importance.

The most fundamental classification at the top,
the most granular distinctions at the bottom.

This is not mere sorting.
This is a design philosophy.

---

## From a Billion to Ten Thousand, in One Pass

The practical power of SIDX shows itself in the numbers.

WMS holds one billion entities.
Each entity's SIDX is 64 bits.
Total size: 1 billion x 8 bytes = 8 GB.

This 8 GB fits entirely in memory.

You want to find "entities that are human and originate from East Asia."
The upper bits contain a "human" flag and an "East Asia" code,
so you can filter with a single bitmask.

```
mask   = 0xFF00_0000_0000_0000  (upper 8 bits: type + region)
target = 0x8100_0000_0000_0000  (human + East Asia)

for each sidx in 1_billion:
    if (sidx & mask) == target:
        add to candidates
```

This operation parallelizes with SIMD.
With AVX-512, you compare 8 SIDXs simultaneously in a single instruction.
Scanning 1 billion entries: approximately 12 milliseconds.

On a GPU? Under 1 millisecond.

A billion records narrowed to ten thousand.
Filtering the remaining ten thousand in detail is instantaneous.

Zero JOINs.
Zero index tree traversals.
Just one bitwise AND.

---

## Why 64 Bits Is Enough

At first, I thought a larger space was needed.

32 bytes (256 bits). A 32-dimensional FP16 vector.
I tried to cram every key attribute of an entity into the ID.
Whether they are human, their gender, nationality, era, occupation, region, living status, classification path...

But then I realized something.

**The ID does not need to know everything.**

It only needs to narrow a billion records down to ten thousand.
WMS handles the rest.

Think of it as a checkpoint.
At a highway tollgate, to determine that
"this vehicle is heading toward Gyeonggi Province" from the license plate,
you do not need to know what is loaded in the trunk.

64 bits is enough.
Use the upper bits to capture type and broad classification,
and the lower bits for finer classification.
64 bits is more than sufficient to narrow a billion records to ten thousand.

And 64 bits = four 16-bit words.
They flow naturally within a stream.
A 32-byte ID would make a stream heavy,
but a 64-bit SIDX is light and fast.

---

## Graceful Degradation: Meaning Survives Even When Bits Are Truncated

Another strength of semantic alignment is its degradation characteristics.

Because SIDX bits are ordered from most to least important,
even if lower bits are damaged or truncated,
the core information in the upper bits is preserved.

```
Full 64 bits:  "Yi Sun-sin, 16th-century Joseon naval commander"
48 bits:       "16th-century Joseon military officer"
32 bits:       "16th-century East Asian human"
16 bits:       "Human"
8 bits:        "Physical entity"
```

As information is truncated, specificity is lost,
but the most fundamental classification survives to the very end.

This is a bit-level implementation of the "graceful degradation" principle.

Even if a network interruption delivers only partial data,
the system knows "I do not know exactly who this is, but it is at least a story about a human"
and can continue reasoning.

A blurry outline is better than total silence.
Partial understanding is better than complete failure.

---

## A Query Becomes an ID

The most intriguing possibility that semantically-aligned indexing opens up
is this: a natural language query can be converted into a temporary SIDX.

A user asks: "Who was the general that defeated the Japanese navy during the Imjin War?"

The encoder analyzes this question.
Human. East Asia. 16th century. Military-related.
Assembling these attributes into bits produces a temporary SIDX.

This temporary SIDX scans the billion SIDXs in WMS.
Entities whose bit patterns are most similar rise as candidates.
Yi Sun-sin, Won Gyun, Gwon Yul, Yi Eok-gi...

Cross-referencing detailed information against these candidates yields the final answer.

This unifies search and entity linking into a single mechanism.
No separate search engine required.
No separate NER (Named Entity Recognition) pipeline required.
A single SIDX comparison is all it takes.

---

## Why Not a B-Tree?

Traditional databases use B-Tree indexes.

B-Trees excel at finding a specific value in sorted data in O(log n).
For "find Q8492," they are optimal.

But for "find all entities that are human and originate from East Asia," they are weak.
Compound condition searches require intersecting multiple indexes,
and the cost of intersection grows sharply with data scale.

SIDX + SIMD exhaustive scanning takes a fundamentally different approach.

If a B-Tree is a phone book that quickly answers "who lives at this address,"
an SIDX scan is profiling that quickly answers "who has these characteristics."

The nature of the question differs, and so does the optimal data structure.

| Query Type | B-Tree | SIDX Scan |
|-----------|--------|-----------|
| Lookup by specific ID | O(log n), optimal | Unnecessary (use a hash) |
| Compound condition filtering | Requires JOINs, slow | One bitwise AND, fast |
| Similar entity search | Not possible | Possible via vector similarity |
| Insertion | O(log n), rebalancing | O(1), append |
| Implementation complexity | High | Low |

WMS does not use B-Trees.
It loads a billion SIDXs into memory
and performs an exhaustive scan with SIMD bitmasks.

Simple. Brute-force. Fast.

---

## Huffman's Wisdom

The bit allocation structure of SIDX follows the principle of Huffman coding.

In Huffman coding, frequently occurring symbols receive shorter codes,
and rarely occurring symbols receive longer codes.

In SIDX, the most frequently needed classification information occupies the upper bits,
and rarely needed details occupy the lower bits.

The same principle governs the packet type prefixes of this language.
The highest-frequency Tiny Verb Edge gets the shortest prefix.
The low-frequency Event6 Edge gets a longer prefix.

Huffman's wisdom runs through every layer of this design.
Not a single bit is wasted.
The lowest cost for the most important thing.

---

## Summary

A traditional ID is an address. An address knows nothing.

1. When the ID does not carry meaning, you must follow it to the data every time. That is a JOIN.
2. Four JOINs across a billion records is slow.
3. SIDX encodes meaning directly into the ID through semantic alignment.
4. A single bitmask AND narrows a billion records to ten thousand. Zero JOINs.
5. 64 bits is enough. The ID does not need to know everything -- it only needs to narrow the candidates.
6. Because the most important information occupies the upper bits, the core meaning survives even when bits are truncated.
7. Converting a natural language query into a temporary SIDX turns search into a vector operation.

The moment an ID stops being an address and becomes knowledge,
the rules of the database change.
