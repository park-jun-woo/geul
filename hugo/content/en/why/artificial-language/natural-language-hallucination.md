---
title: "Why Does Natural Language Create Hallucinations?"
weight: 8
date: 2026-02-26T12:00:16+09:00
lastmod: 2026-02-26T12:00:16+09:00
tags: ["natural language", "hallucination", "ambiguity"]
summary: "Hallucination is not an LLM bug — it is a structural inevitability of natural language. Four flaws — ambiguity, absent sources, absent confidence, absent time — make it unfixable by scaling alone."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Hallucination is not a bug. It is a structural inevitability as long as we use natural language.

---

## The Miracle of Natural Language

100,000 years ago, spoken language appeared. The social relationships that primates could maintain by grooming each other were limited to about 150 individuals. Language shattered that ceiling. Once one person could speak to many at the same time, a new scale of society --- the tribe --- became possible.

10,000 years ago, agriculture created food surpluses, and people gathered in one place to form cities. 5,000 years ago, someone in Mesopotamia pressed wedge-shaped marks into a wet clay tablet. It was to record grain inventories. The birth of writing. Speech vanishes, but records endure. Once records endured, bureaucracy became possible, law became possible, the state became possible.

Spoken language created the tribe. Writing created the state.

Natural language is the greatest technology humanity has ever created. Not the discovery of fire, not the invention of the wheel, not the invention of the semiconductor. What made all of those possible was natural language. Because natural language existed, knowledge could be transmitted, cooperation could happen, and the thoughts of the dead could be inherited by the living. For tens of thousands of years, natural language was the medium of all human civilization.

And now, that great natural language has become the bottleneck of the AI era.

---

## The Misunderstanding Called Hallucination

When AI says something false, we call it "hallucination."

This name carries implications.
The implication that hallucination is abnormal.
The implication that it can be fixed.
The implication that a better model will solve it.

This is a misunderstanding.

Hallucination is not a bug of LLMs.
Hallucination is a structural inevitability that cannot be avoided
as long as natural language is used as AI's language of reasoning.

No matter how much you scale the model,
no matter how much you expand the data,
no matter how refined the RLHF,
as long as natural language is input and natural language is output,
hallucination will not disappear.

Let me explain why.

---

## The Four Structural Flaws of Natural Language

Natural language evolved for communication between humans.
The four characteristics it acquired in the process
become fatal flaws in AI reasoning.

---

### Flaw 1: Ambiguity

"He went to the bank."

Is "bank" a financial institution or a riverbank?
Who is "he"?
When did he go?

Humans resolve this with context.
The flow of conversation, the speaker's facial expression, shared background knowledge.

AI has only text.
Text alone cannot fully resolve ambiguity.
If it cannot be resolved, AI guesses.
Guesses are sometimes wrong.
When a wrong guess is output with confidence, that is hallucination.

---

### Flaw 2: Absence of Source

"Yi Sun-sin defeated 133 ships with just 12."

This sentence has no source.

Who made this claim?
What historical records support it?
Is there scholarly disagreement on these numbers?

Natural language has no structural place for metadata.
To include sources, you have to lengthen the sentence,
and lengthening it obscures the point.
So in most natural language sentences, sources are omitted. This problem is explored further in [Why Claims, Not Facts](/why/claims-not-facts/).

LLMs are trained on billions of such sentences.
Claims with omitted sources get mixed together
into one massive statistical soup.

Tracing the basis for the number "12" inside that soup
is impossible in principle.
Since the basis cannot be traced, baseless numbers can also be fabricated.
That is hallucination.

---

### Flaw 3: Absence of Confidence

"The Earth is round."
"Dark energy makes up 68% of the universe."
"It will rain tomorrow."

The confidence levels of these three sentences are completely different.

The first is an overwhelming consensus.
The second is the current best estimate, but the theory may change.
The third is a probabilistic prediction.

Yet in natural language, all three have identical grammatical structures.
Subject + predicate. Declarative sentence. Period.

Natural language cannot structurally express "how certain is this."
There are adverbial devices like "perhaps," "almost certainly," "might,"
but they are optional, imprecise, and usually omitted.

LLMs learn all sentences at identical confidence levels.
There is no way for the model to internally distinguish the confidence difference
between "the Earth is round" and "dark energy is 68%."

So it states estimates as facts,
states hypotheses as established views,
and states uncertain things with certainty.
That is hallucination.

---

### Flaw 4: Absence of Temporal Context

"The CEO of Tesla is Elon Musk."

As of when?

In 2024, this is correct.
In 2030, who knows.
If the time of writing is not specified,
the validity period of this sentence cannot be determined.

Most natural language sentences omit temporal context.
The "present tense" can mean "right now"
or it can mean "generally."

LLMs learn articles from 2020 and articles from 2024 as the same data.
Since temporal information is not structurally preserved,
they state past facts as if they were present,
or mix information from different time periods.
That is hallucination.

---

## The Confluence of the Four Flaws

Hallucination escalates explosively when these four flaws converge.

Let us analyze a single LLM output.

> "Yi Sun-sin destroyed 330 Japanese ships with 12 vessels,
> and later died at the Battle of Noryang, leaving the last words 'Do not announce my death.'"

In this sentence:

**Ambiguity:** What does "destroyed" precisely mean? Sunk? Routed? Partially damaged?

**Absence of source:** What is the basis for the numbers 12 and 330? Different historical records cite different figures --- which one was followed?

**Absence of confidence:** Is "Do not announce my death" a historically confirmed last testament, or later oral tradition? The confidence levels of the two are different, yet they are listed in the same declarative sentence.

**Absence of temporal context:** Which point in time of academic consensus does this information reflect?

The LLM fills all this ambiguity with "the most plausible token sequence."
Plausibility is not accuracy.
The gap between the two is hallucination.

---

## Why Bigger Models Cannot Solve This

"Won't hallucination decrease when GPT-5 comes out?"

It will decrease. But it will not disappear.

Bigger models learn more sophisticated patterns from more data.
So the accuracy of "plausibility" goes up.

But the fundamental problem does not change.

As long as the input is natural language, ambiguity remains.
As long as training data is natural language, sources remain lost.
As long as the output is natural language, confidence is not expressed.
As long as temporal information is absent from the structure, time remains scrambled.

Even if you scale the model by 100x,
the structural flaws of natural language do not grow 100x ---
but they do not reach zero either.

This is not a problem of resolution. It is a problem of medium.

No matter how much you increase the resolution of a black-and-white photograph, color does not appear.
No matter how much you increase the precision of natural language,
source, confidence, and temporal context do not appear in the structure.

If you want color, you need color film.
If you want to eliminate hallucination, you need a different language.

---

## Conditions for a Structural Solution

To solve these four flaws, the structure of the language itself must be different.

**Ambiguity --> Explicit structuring.**
When "He went to the bank" is converted into a structured language,
"he" is resolved to a specific entity SIDX,
and "bank" is resolved to the SIDX of either a financial institution or a riverbank.
If it cannot be resolved, "unresolved" is explicitly stated.
Either resolve the ambiguity, or record the fact that it is ambiguous.

**Absence of source --> Embedded source.**
Every narration structurally includes a source entity.
"Who made this claim" is part of the narration.
It is not optional. If the field is empty, it is marked as empty.

**Absence of confidence --> Embedded confidence.**
Every verb edge has a confidence field.
"Certain," "estimated," "hypothetical"
are structurally specified as verb modifiers.

**Absence of temporal context --> Embedded temporal context.**
Every narration includes a time context.
"As of when is this narration" is always specified.

What is omitted in natural language
exists as part of the structure in a structured language.

When omission is impossible, the room for hallucination shrinks. [Why Clarification Is Necessary](/why/clarification/) explains this principle.
When you cannot speak without basis, baseless statements are not produced.

---

## The End of Hallucination Lies in Replacing the Language

Let us look at current approaches to reducing hallucination.

**RAG (Retrieval-Augmented Generation):** Retrieves external documents and provides them as context. Effective, but the retrieved documents are also natural language, so the problems of ambiguity, absent sources, and absent confidence follow along unchanged. [Why RAG Is Not Enough](/why/rag-not-enough/) explores this limitation in detail.

**RLHF:** Trains the model to say "I don't know" when uncertain. Reduces the frequency of hallucination, but does not solve the fundamental problem that natural language lacks a confidence structure.

**Chain-of-Thought:** Records the reasoning process in natural language. The direction is right, but the medium of the record is natural language, so it inherits the same flaws.

All of these approaches attempt to mitigate hallucination within the framework of natural language.
They work. But they are not fundamental.

The fundamental solution is to remove natural language from inside AI.

The interface with users stays in natural language.
Humans continue to speak in natural language and receive answers in natural language.

But the language in which AI reasons, records, and verifies internally
must be something other than natural language.

A language where source is in the structure.
A language where confidence is in the structure.
A language where temporal context is in the structure.
A language where ambiguity is explicitly handled.

Spoken language created the tribe.
Writing created the state.
What will the third language create?

The end of hallucination lies not in bigger models
but in a better language.

---

## Summary

Hallucination is born from the four structural flaws of natural language.

1. **Ambiguity:** Irresolvable without context. AI guesses, and guesses are wrong.
2. **Absence of source:** The basis of claims is lost. Baseless combinations are fabricated.
3. **Absence of confidence:** Facts and estimates are expressed in identical grammar. AI cannot distinguish them.
4. **Absence of temporal context:** Information from different time periods is scrambled.

Bigger models reduce hallucination but cannot eliminate it.
Without changing the medium, the structural flaws remain.

No matter how much you increase the resolution of black-and-white film, color does not appear.
If you want color, you must change the film.
