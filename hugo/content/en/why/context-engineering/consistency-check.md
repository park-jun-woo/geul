---
title: "Why Consistency Checks Are Necessary"
weight: 6
date: 2026-02-26T12:00:08+09:00
lastmod: 2026-02-26T12:00:08+09:00
tags: ["consistency", "contradiction", "coherence"]
summary: "Individually correct information can be collectively wrong"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Individually correct information can be collectively wrong.

---

## Verification Passed. Filtering Passed.

Mechanical verification filtered out format errors.
Filtering selected based on relevance, trustworthiness, and recency.

30 pieces of information remain.
All valid, all relevant, all trustworthy, all current.

Do you put these 30 into the context?

No.
One more thing must be checked.
Do these 30 contradict each other?

---

## Contradiction Is Not a Property of Individual Information

Consider these two statements.

- Source: Samsung Electronics IR disclosure, October 2024. "Samsung Electronics CEO: Jun Young-hyun."
- Source: Samsung Electronics IR disclosure, March 2024. "Samsung Electronics CEO: Kyung Kye-hyun."

Individually, both are valid.
The format is correct, the source is present, the time is present, and they are trustworthy.
They pass verification. They pass filtering.

But when both enter the same context, there is a problem.
Is Samsung Electronics' CEO Jun Young-hyun or Kyung Kye-hyun?

Neither statement is wrong.
In March, Kyung Kye-hyun was correct. In October, Jun Young-hyun is correct.
Individually, both are right.
But when they coexist in the context, the LLM gets confused.

This is the consistency problem.
It arises not from individual information but from the set of information.
Verification examines individual information. Filtering examines individual information.
Consistency examines the space between pieces of information.

---

## Types of Contradiction

Contradictions in the context fall into several types.

### Temporal Contradiction

The most common.

The same property of the same entity has changed over time,
and values from different points in time coexist in the context.

"Tesla CEO: Elon Musk" and
"Tesla stock price: $194" are in the same context,
but the CEO information is as of 2024 and the stock price is from June 2023.
The LLM may treat them as information from the same point in time.

More subtle cases also arise.
"South Korea's base interest rate: 3.50%" is as of January 2024, and
"South Korea's consumer price inflation: 2.0%" is as of October 2024.
Both are valid and both relate to the Korean economy,
but there is a 9-month gap.
Whether this gap affects the inference depends on the context.

### Source-to-Source Contradiction

Different sources present different values for the same fact.

- Source A: "2024 global AI market size: $184 billion."
- Source B: "2024 global AI market size: $214 billion."

Neither can be declared definitively "wrong."
The market scope definition may differ. The measurement methods may differ.
But if both are in the context,
the LLM must pick one, blend both, or get confused.

### Inferential Contradiction

Not directly contradicting values,
but logically incompatible when placed together.

"Company A's market share: 60%."
"Company B's market share: 55%."

Each is valid. But they add up to 115%.
Adding the remaining competitors would exceed 100%.
One of them is from a different time, uses a different market definition, or is wrong.

This kind of contradiction cannot be found by looking at individual statements.
You must examine the set.

---

## LLMs Do Not Handle Contradictions Well

In theory, the LLM should be able to detect and resolve contradictions.
"These two pieces of information differ in time, so I will answer based on the more recent one."

In practice, that is not what happens.

**LLMs tend to trust information in the context.**
The act of putting something in the context is itself a signal that says "refer to this."
When two contradictory pieces of information are present,
the LLM tends to reference both rather than ignore one.
The result is a blend or confusion.

**Contradiction detection requires reasoning.**
Knowing that "CEO: Jun Young-hyun" and "CEO: Kyung Kye-hyun" contradict each other
requires the background knowledge that there is only one CEO at a given time.
Checking whether market share sums exceed 100% requires arithmetic.
This depends on the LLM's reasoning capability.

**Resolution is even harder.**
Even if a contradiction is detected, a judgment must be made on which side to choose.
The more recent one? The more trustworthy source? The one supported by more sources?
If this judgment is left to the LLM, consistency is not guaranteed.
For the same contradiction, it picks A sometimes and B other times.

In conclusion, handling contradictions after they enter the context
is expensive and the outcome is uncertain.
Contradictions must be resolved before entering the context.

---

## Why Consistency Checking Is Hard in Natural Language

Suppose you are checking the consistency of 30 natural language chunks.

First, you must determine whether they are about the same subject.
Whether "Samsung Electronics," "Samsung Electronics," and "Samsung" refer to the same entity.
In natural language, this is uncertain.
Whether "Samsung" means Samsung Electronics, Samsung C&T, or Samsung Life requires reading the context.

Next, you must determine whether they describe the same property.
Whether "revenue," "revenue," "total revenue," and "gross revenue" are the same thing.
Whether "operating profit," "operating profit," and "operating margin" are the same or different.

Next, you must extract the time references.
When is "last quarter"? When is "recently"? When is "this year"?

Only after all of this can you finally compare whether two statements contradict each other.

With 30 statements, there are 435 comparison pairs.
Each pair must go through the above process.
All LLM reasoning.
All expensive.
All probabilistic.

---

## Consistency Checking in Structured Representations

In a structured representation, the situation is different.

**Entity identification is deterministic.**
The entity "Samsung Electronics" has a unique identifier.
"Samsung Electronics" points to the same identifier.
No reasoning is needed to determine identity.

**Properties are explicit.**
"Revenue" is a typed property.
"Operating margin" is a different property.
Whether two properties are the same or different is confirmed by field comparison.

**Time is a field.**
There is a value like "2024-Q3."
No need to interpret "last quarter."
Whether two statements share the same time is one value comparison.

When these three things are deterministic, contradiction detection patterns become mechanizable.

Same entity + same property + same time + different value = contradiction.
Same entity + same property + different time + different value = change. Not a contradiction.
Different entity + same property + same time + sum of values > 100% = inferential contradiction.

No LLM needed for this.
Field comparison and arithmetic.

Not all contradictions can be caught.
Whether "the AI market is growing" and "AI investment is declining" contradict each other
still requires semantic judgment.
But if mechanically detectable contradictions are caught first,
only cases requiring semantic judgment remain.
Once again, cheap comes first.

---

## Resolution Strategies for Consistency Checks

After detecting a contradiction, it must be resolved.

Resolution strategies vary by context, but in a structured representation they can be declared as policy.

**Most recent first.** When the same property of the same entity conflicts, pick the one with the more recent timestamp. Suitable for changing values like CEO, stock price, population.

**Highest trust first.** Pick the one with higher confidence. Or if a source hierarchy is defined, pick the higher-ranked source. Primary source > secondary source > unofficial source.

**Present both.** Do not resolve the contradiction. Put both in the context, but mark the contradiction explicitly. "Source A says $184 billion; Source B says $214 billion. Likely due to definitional differences." Let the LLM reason with awareness of the contradiction.

**Exclude both.** If the contradiction cannot be resolved, exclude both sides. No information is better than wrong information.

In a natural language pipeline, these strategies are written in natural language in the prompt.
"Please prioritize the most recent information."
Whether the LLM follows this consistently is, again, a matter of probability.

In a structured representation, these strategies are declared as policy.
"On same-entity + same-property conflict: most recent timestamp first. If timestamps are equal: highest confidence first. If confidence is equal: present both."
The machine executes it. Not probability.

---

## Position in the Pipeline

Consistency checking comes after filtering.

Verification -> Filtering -> Consistency.

Why this order?

Verification filters out format errors.
Filtering removes unnecessary information.
Consistency checking only needs to process what passed verification and filtering.

Consistency checking compares pairs.
For n statements, there are n(n-1)/2 pairs.
1,000 yields roughly 500,000 pairs. 30 yields 435.

If verification and filtering reduce 1,000 to 30,
the cost of consistency checking drops from 500,000 to 435 -- one-thousandth.

Order matters.

---

## Summary

Information that is individually valid, relevant, and trustworthy
can contradict each other when gathered as a set.

There are three types of contradiction.
Temporal contradiction -- values from different points in time coexist.
Source-to-source contradiction -- different sources present different values.
Inferential contradiction -- individually valid, but logically incompatible when combined.

LLMs do not handle contradictions well.
They tend to trust information in the context,
contradiction detection requires reasoning,
and consistency of resolution is not guaranteed.

In natural language, consistency checking is LLM reasoning throughout.
Entity identity, property identity, time extraction, value comparison -- all probabilistic and expensive.

In a structured representation, entity identifiers, property types, and time fields exist,
so much of contradiction detection converts to field comparison and arithmetic.
Resolution strategies are also declared as policy.

Consistency checking comes after filtering in the pipeline.
Verification and filtering must reduce the set for the number of comparison pairs to shrink.
Cheap comes first, and collective checks come after individual checks are done.
