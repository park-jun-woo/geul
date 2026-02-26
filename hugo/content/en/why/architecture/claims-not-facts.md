---
title: "Why Claims, Not Facts?"
weight: 14
date: 2026-02-26T12:00:06+09:00
lastmod: 2026-02-26T12:00:06+09:00
tags: ["claims", "facts", "confidence"]
summary: "Truth vanishes faster than the speed of light"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Truth Vanishes Faster Than the Speed of Light

---

## This Very Moment Is Already the Past

Right now, as you read this sentence,
the moment this sentence was written is already in the past.

The light that reached your eyes traveled from the screen,
taking several nanoseconds to reach your retina.
The signal from your retina takes tens of milliseconds to travel through the optic nerve to your brain.
Your brain takes hundreds of milliseconds to interpret that signal as a "sentence."

By the moment you feel that you have "read" this sentence,
the moment when this sentence existed on the screen
is already hundreds of millions of nanoseconds in the past.

This is not a metaphor.
This is physics.

---

## Truth Is Inaccessible

In the physical world, an "event" is a point in spacetime.

The moment an event occurs, it emits information.
Photons, sound waves, gravitational waves, chemical traces.
This information propagates at or below the speed of light.

But the event itself?
The complete state at the exact moment and location where it occurred?

It vanishes into the past faster than the speed of light.

0.001 seconds after the event, it is already in the past.
No observer can access the event "itself."
What reaches us is always
the traces the event left behind.

Reflected photons.
Recorded text.
Relayed rumors.
Measured data.

All fragments.
Fragments of truth. Not truth itself.

---

## The Brain Does Not Store Facts

Neuroscience has revealed an uncomfortable truth.

Human memory is not recording. It is reconstruction.

When you remember "I saw a red car yesterday,"
there is no photograph of a "red car" stored in your brain.

What actually happens is this:

1. Photons reach the retina.
2. Cone cells in the retina convert specific wavelengths into signals.
3. The visual cortex assembles these signals into patterns.
4. The hippocampus encodes these patterns along with context.
5. During sleep, these codes are reorganized and compressed.

The memory "I saw a red car" is
a product reassembled at the moment of retrieval
from fragments scattered across multiple brain regions.

That is why memories change.
Each time you recall the same event, it is reconstructed slightly differently.
New experiences contaminate old memories.
You can even remember things that never happened.

What the brain stores is not "facts."
What the brain stores is
"this is how it felt, this is how it looked, this is how I interpreted it" ---
claims.

---

## All Knowledge Is Claims

Extend this principle from individual memory to civilizational knowledge,
and the same structure repeats.

**History:**
"Yi Sun-sin died in the Battle of Noryang in 1598."

Is this a fact?

What we have:
There are records in the Annals of the Joseon Dynasty.
There are records in the Complete Works of Admiral Yi.
There are Japanese records.
There are centuries of scholarly interpretation.

All of them are claims.
Claims narrated by different sources, at different times, from different perspectives.

"Yi Sun-sin died in 1598" is not a fact ---
it is a consensus of these claims.
A consensus of very high confidence, but still a consensus.

**Science:**
"The speed of light is 299,792,458 m/s."

Is this a fact?

What we have:
Countless experiments have measured this value.
Current physical theory predicts this value.
The International Bureau of Weights and Measures has adopted this value as a definition.

All of them are claims.
Claims that passed through the limits of measurement instruments, assumptions of theories, and consensus procedures.
The probability that a more precise measurement tomorrow will revise this value
is extremely low, but in principle, it is not zero.

**News:**
"The stock market dropped 3% today."

Is this a fact?

It is a number recorded by the exchange's system.
Under the premise that the system operated correctly.
Depending on which reference point defines "3%."

It looks like a fact, but strictly speaking, it is a claim
recorded by a specific system under specific conditions.

---

## The Hierarchy of Truth

A proper knowledge system must reflect this epistemological reality in its design.

If truth is inaccessible,
then all we can handle are claims about truth.

On top of a collection of claims,
we can compute consensus and confidence.

This can be structured into four layers.

**L3 --- Narration/Observation:**
"This reporter, at this time, from this perspective, reported this."
The most primitive data. Subjective and individual.
The primary data that a knowledge system directly handles.

**L2 --- Consensus/Established View:**
"Synthesizing multiple narrations, this is the most plausible account."
The result of aggregating multiple L3 claims.
Probabilistic and provisional.

**L1 --- Rules/Laws:**
"In this world, this rule operates."
Laws of physics, game rules, social norms.
If broken, the system enters a state of contradiction.

**L0 --- Mathematics/Logic:**
1+1=2. The rules of logical operations.
This alone is uniquely not a claim.
This is the operating rule of the engine. Not data.

The key is this:

> The starting point is always L3 --- claims.
> The remaining layers are derivatives computed on top of claims.

---

## Why Do Existing Systems Store Facts?

Look at Wikidata.

```
Q8492 (Yi Sun-sin)
  - instance of: human
  - occupation: naval commander
  - date of death: 1598-12-16
```

There is no "who made this claim."
There is no "how confident is this."
There is no "are there conflicting claims."

The assertion that Yi Sun-sin's date of death is December 16, 1598
is the result of consensus among multiple historical records and scholars,
yet Wikidata stores it as if it were a universal truth.

In most cases, this is not a problem.
Because the confidence of the consensus is sufficiently high.

But consider these situations:

Two news outlets publish conflicting reports about the same event.
A historian presents a new interpretation that contradicts the established view.
A scientific paper fails to reproduce existing experimental results.

In a system that stores "facts," this is an error.
One of them is wrong. It must be corrected.

In a system that stores "claims," this is normal.
Different sources, from different perspectives, made different claims.
Both claims are recorded.
Consensus and confidence are computed on top of them.

Reality is not clean.
Contradiction is part of reality.
A system that treats contradiction as error cannot contain reality.

---

## The Physical Origin of Hallucination

Let us revisit the hallucination problem of LLMs from this perspective.

LLMs are trained on billions of sentences.
Each sentence is a claim written by someone in some context.

But LLMs learn these not as "claims"
but as "facts about the world."

Sources disappear.
Context disappears.
Confidence disappears.
Perspectives disappear.

What remains is only statistical patterns.

So an LLM cannot distinguish between
"Yi Sun-sin died in 1598" and
"Yi Sun-sin was fond of four-character idioms."
Both sentences can appear with high probability in the training data,
and without source information, there is no way to know
that one is an established historical narration and
the other is a nonexistent claim.

This is the physical origin of hallucination.

When fragments of truth lose their sources and get mixed together,
nonexistent "facts" are fabricated.

The solution is clear.
Treat fragments as fragments.
Record claims as claims.
Structurally preserve sources, context, and confidence.

---

## A Structural Solution

A proper knowledge system must treat every narration as a claim.

When a natural language sentence is converted into a structured representation, it must include:

**Who made the claim** --- Source entity
**When was it claimed** --- Temporal context
**In which world is this claim** --- World context
**From which perspective** --- POV (Point of View)
**How confident is it** --- Confidence level

This is not optional.
The structure of such a system demands this information.
If a field is empty, it is explicitly marked as empty.

When "Yi Sun-sin was great" is converted into a structured representation:

```
[Entity: Yi Sun-sin]
[Verb: be great (evaluative verb)]
[POV: Speaker (current conversation participant)]
[Time: Present moment]
[Confidence: Not specified]
[Source: Speaker's direct utterance]
[World: Real world]
```

Even for the identical natural language sentence "Yi Sun-sin was great,"
the representation is entirely different depending on whether
it is narrated by a history textbook,
spoken as an individual's personal impression,
or uttered by a character in a novel.

Ambiguity is structurally eliminated.
Claims are recorded as claims.
Fragments of truth are preserved as fragments.

---

## The Map Is Not the Territory

The Polish-American scholar Alfred Korzybski said:

> "The map is not the territory."

What we need is a language for drawing maps.
An engine that collects maps and reverse-engineers the territory.

A map is not a perfect replica of the territory.
A map is a representation drawn by someone, for some purpose, at some scale.
There can be dozens of maps of the same city.
Tourist maps, topographic maps, transit maps, population density maps.
All of them are different claims about the same territory.

No map is the territory itself.
But by overlaying multiple maps, our understanding of the territory deepens.

This is how a claim-based knowledge system handles the world.
It records countless claims in structured form,
discovers consensus and patterns on top of them,
and builds an increasingly precise understanding of the territory.

But it never asserts, "This is the territory itself."

---

## Summary

Truth is physically inaccessible.

1. Events vanish into the past the moment they occur. Faster than the speed of light.
2. All that remains are fragments of truth. Photons, records, testimonies.
3. Even the brain does not store facts. It stores claims reconstructed from fragments.
4. Therefore, the primary data of a knowledge system cannot be facts. It must be claims.
5. If you treat claims as facts, contradiction becomes error. If you treat them as claims, contradiction becomes data.
6. LLM hallucination is the result of claims losing their sources.
7. Such a system structurally embeds source, time, perspective, and confidence into every narration.

We do not handle truth.
We handle sentences about truth.
This is not humility. This is physics.
