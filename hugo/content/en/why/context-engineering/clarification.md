---
title: "Why Clarification Is Necessary"
weight: 3
date: 2026-02-26T12:00:13+09:00
lastmod: 2026-02-26T12:00:13+09:00
tags: ["clarification", "input", "output"]
summary: "Clear input produces clear output"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Natural language inevitably grows longer to resolve ambiguity. In a clear structure, that cost disappears.

---

## The Cost of Ambiguity

"He went to the bank."

7 tokens. Short. Looks efficient.

But this sentence is unusable.
It cannot be put into AI's reasoning context.
Because it is ambiguous.

Who is "he"?
Is "bank" a financial institution or a riverbank?
When did he go?
Why did he go?

Reasoning from this sentence produces four branches of uncertainty.
Uncertainty propagates through every subsequent step of reasoning.
When propagated uncertainty is output as if it were certainty, that is hallucination.

So natural language tries to resolve ambiguity.
The only way to resolve it is to use more words.

---

## The Cost of Resolution

Let us look at an unambiguous version of the sentence.

"Kim Cheolsu, section chief of the finance team at Samsung Electronics,
visited the Gangnam branch of Shinhan Bank
on Monday, January 15, 2024,
to open a corporate account."

Now there is no ambiguity.
The subject is specified. The location is specified.
The timestamp is stated. The purpose is stated.

But 7 tokens have become 40.

The additional 33 tokens are entirely the cost of disambiguation.
They are not new information.
Specifying "he" as "Kim Cheolsu, section chief of the finance team at Samsung Electronics"
did not add meaning — it removed ambiguity.

In natural language, clarity is not free.
To become clear, you must become long.
This is a structural property of natural language.

---

## Why Natural Language Inevitably Gets Longer

Natural language evolved for communication between humans.
In human communication, ambiguity is a feature.

"He went to the bank, I hear."

If the speaker and listener share the same context,
they already know who "he" is and which "bank" it is.
7 tokens is enough.
Ambiguity is a compression mechanism. It omits by relying on shared context.

The problem arises on the decompression side.

To convey the message to someone who does not share the context,
everything that was omitted must be restored.
Restoration makes it longer.

In natural language, clarity and brevity are a trade-off.
Clear means long. Short means ambiguous.
You cannot have both at once.

This is the fundamental constraint of natural language.

---

## AI Has No Shared Context

In conversation between humans, ambiguity is efficient.
Decades of shared experience, cultural background, and conversational flow
automatically resolve ambiguity.

AI does not have this.

The text inside AI's context window is all there is.
Context outside the text does not exist.

Put "He went to the bank" into the context,
and AI begins reasoning with four branches of uncertainty.
It picks the "most plausible" interpretation
and accepts the risk of being wrong.

That is why natural language is disadvantageous for AI context.

Write clearly and the token count balloons, wasting window space.
Write briefly and the ambiguity becomes raw material for hallucination.

As long as you use natural language, there is no escape from this dilemma.

---

## Structural Clarity as a Solution

To solve this dilemma,
you must break the trade-off between clarity and brevity.

In natural language, this is impossible.
Resolving ambiguity requires adding words.

But in a structurally clear representation, it is possible.

In natural language, specifying "Kim Cheolsu" requires writing "Kim Cheolsu, section chief of the finance team at Samsung Electronics."
In a structured representation, a single unique identifier does the job.
The identifier is inherently unique.
The modifier "finance team at Samsung Electronics" is unnecessary.
Modifiers are disambiguation devices for humans —
they are unnecessary for machines.

In natural language, resolving whether "bank" means a financial institution or a riverbank
requires writing "Shinhan Bank, Gangnam branch."
In a structured representation, the entity's identifier points to the financial institution.
Ambiguity is blocked at the source by the structure.

In natural language, specifying a timestamp requires writing "Monday, January 15, 2024."
In a structured representation, a value goes into the time field.
Because the field exists, omission is impossible.
Because the value is typed, there is no interpretive ambiguity.

In structural clarity,
the cost of disambiguation converges to zero.
Identifiers are unambiguous, so modifiers are unnecessary.
Fields exist, so omission is impossible.
Values are typed, so interpretation is deterministic.

---

## Compression Is a Byproduct of Clarification

Here is where something interesting happens.

Making it clear makes it shorter.

In natural language, clarity makes things longer.
In structured representation, clarity makes things shorter.

Why?

Because most of what makes natural language sentences long
is the cost of disambiguation.

In "Kim Cheolsu, section chief of the finance team at Samsung Electronics,"
"finance team at Samsung Electronics" and "section chief" are not information — they are identification devices.
They are modifiers to narrow down who "he" is.
With a unique identifier, all of these modifiers vanish.

In "Monday, January 15, 2024," the word "Monday" is redundant.
January 15 already determines the day of the week.
Yet in natural language, such redundancy is conventionally added for clarity.
In a typed time field, such redundancy is structurally impossible.

As a result of structural clarification,
the expression becomes shorter than natural language.

This is not intentional compression.
It is the result of disambiguation cost disappearing.

---

## The Paradox of a Single Sentence

There is something to be honest about here.

For a single sentence, a structured representation can be longer than natural language.

"Yi Sun-sin was great."

In natural language, this is done in 7 tokens.
Convert it to a structured representation —
entity node, attribute node, verb edge, tense, confidence field —
and the structural overhead can be larger than the sentence itself.

This is true.
There is a fixed cost to embedding clarity into structure.

But as the number of statements grows, a reversal occurs.

If there are 100 statements about Yi Sun-sin,
natural language writes "Yi Sun-sin" 100 times.
In a structured representation, you define the Yi Sun-sin node once
and 100 edges reference it.

If 50 statements come from the same source,
natural language either cites the source every time or omits it and becomes ambiguous.
In a structured representation, the metadata is bound once.

As statements accumulate, node sharing rates rise.
As node sharing rates rise, the gains from structural clarity grow.

In practice, the reversal begins at roughly 20 statements.
In context engineering, it is rare for the information placed in the window
to be fewer than 20 statements.

In practical terms, structured representation is always clear and always shorter.

---

## The Chain Reaction That Clarity Creates

Clarification does not only produce compression.

**Indexing becomes possible.**
When there are unambiguous identifiers, precise search becomes possible.
Searching for "Apple revenue" does not pull up "apple nutrition facts."
If the identifier encodes meaning, a single bitmask narrows the candidates.

**Validation becomes possible.**
When the structure is typed, "is this a valid expression?" can be judged mechanically.
In natural language, the concept of an "invalid sentence" does not exist.
In a clear structure, if a required field is empty, it is invalid.

**Consistency checking becomes possible.**
When statements about the same entity are unambiguous,
"do these two statements contradict each other?" can be judged mechanically.
In natural language, determining whether "the CEO is A" and "the CEO is B" are contradictory
requires AI to read both sentences and reason.
In a clear structure — same entity, same relation, different values — it is auto-detected.

Clarity is the precondition for the entire context engineering pipeline.
Indexing, validation, filtering, consistency checking —
none of them work if the information is not clear.

Clarification is not one stage of the pipeline.
It is the condition that makes the pipeline possible.

---

## Summary

In natural language, clarity and brevity are a trade-off.
Clear means long. Short means ambiguous.

AI has no shared context.
Natural language ambiguity becomes raw material for hallucination.
Resolving ambiguity inflates token counts and wastes the window.

A structurally clear representation breaks this trade-off.
Unique identifiers block ambiguity at the source.
Typed fields make omission impossible.
When disambiguation cost disappears, compression follows as a byproduct.

Clarification is the precondition for context engineering.
If information is not clear, indexing, validation, and consistency checking do not work.

Compression is not the goal.
Clarification is the goal.
Compression follows.
