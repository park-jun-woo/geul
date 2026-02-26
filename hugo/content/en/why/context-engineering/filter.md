---
title: "Why Filters Are Necessary"
weight: 5
date: 2026-02-26T12:00:09+09:00
lastmod: 2026-02-26T12:00:09+09:00
tags: ["filter", "relevance", "trust"]
summary: "Valid information is not always needed information"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Valid information is not always needed information.

---

## You Have 1,000 Pieces of Information That Passed Verification

Suppose mechanical verification worked.

The format is correct,
required fields exist,
identifiers are valid,
types are appropriate,
and referential integrity holds -- 1,000 statements remain.

All of them are valid information.
They conform to the specification. There is no reason to reject them.

But the context window can only hold 300.

Which 300 do you put in?

This is the problem of filtering.

---

## Verification and Filtering Ask Different Questions

What verification asks: "Is this information valid?"
What filtering asks: "Is this information needed right now?"

Verification looks at the properties of the information itself.
Is the format correct? Are the fields present? Are references valid?
It does not care what the information is about or what purpose it will serve.

Filtering looks at the relationship between information and situation.
Is it relevant to this particular inference right now?
Can this information be trusted?
Is it sufficiently recent?

Verification is possible without context. You only need the specification.
Filtering is impossible without context. You need to know "what is needed right now."

Verification is deterministic. Valid or invalid.
Filtering is judgment. Relevance has degrees, trustworthiness has thresholds, recency has context.

Verification is cheap.
Filtering is relatively expensive.

That is why verification comes first and filtering comes after.
If verification filters first, then filtering judges a smaller set.
The cost of expensive judgment decreases.

---

## Three Things Filtering Judges

Filtering looks at three main things.

### Relevance: Is It Needed for This Inference?

The user asked about "Samsung Electronics' Q3 2024 operating profit."

Among the valid statements that passed verification:

- Samsung Electronics' Q3 2024 operating profit was 9.18 trillion won.
- Samsung Electronics' Q3 2024 revenue was 79 trillion won.
- Samsung Electronics' Q3 2023 operating profit was 2.43 trillion won.
- Samsung Electronics' semiconductor capex plan is 53 trillion won as of 2025.
- Samsung Electronics' headquarters is in Suwon.

All valid. All about Samsung Electronics.
Do you put all of them in the context?

The headquarters location is irrelevant.
The capex plan has low relevance.
The 2023 operating profit may be useful for comparison.
Revenue is closely related to operating profit.

In natural language RAG, this judgment is delegated to embedding similarity.
Ranked by vector distance to "Samsung Electronics operating profit."
But as already discussed, similar is not relevant.

In a structured representation, relevance judgment has different inputs.
What entity does the statement point to? Samsung Electronics.
What property? Operating profit.
What time? Q3 2024.

If entity, property, and time exist as fields,
you can find "same entity, same property, same time" precisely.
And you can intentionally include or exclude "same entity, same property, different time."
Field matching, not vector distance.

Relevance is still a judgment. Not deterministic.
But whether the input to that judgment is vector distance or structured fields makes a difference in accuracy.

### Trustworthiness: Can This Information Be Believed?

Two statements exist about the same content.

- Source: Samsung Electronics IR disclosure. Confidence: 1.0. "Q3 2024 operating profit: 9.18 trillion won."
- Source: anonymous blog. Confidence: 0.3. "Q3 2024 operating profit: approximately 10 trillion won."

Which one goes into the context?

Obviously the former.

But for this judgment to be "obvious,"
the source and confidence must exist in a readable form.

In natural language chunks, the source is buried somewhere in the text or absent.
Confidence has never been expressed.
To compare two chunks and judge which is more trustworthy,
an LLM must read and reason.

In a structured representation, source and confidence are fields.
"Exclude confidence below 0.5" is one comparison.
"Include only primary sources" is field matching.

The cost of trustworthiness filtering shifts from LLM inference to field comparison.

### Recency: Is This Information Sufficiently Current?

"Who is the CEO of Samsung Electronics?"

- Time: March 2024. "Samsung Electronics CEO: Kyung Kye-hyun."
- Time: December 2022. "Samsung Electronics co-CEOs: Han Jong-hee, Kyung Kye-hyun."

Both are valid. Correct format, sources present.
But the most recent one is needed.

In natural language, time may or may not be mentioned in the text.
If it says "as of last year," you also have to calculate when "last year" was.

In a structured representation, time is a field.
An ISO 8601 date.
"Include only the most recent statement" is one sort operation.

More importantly, the criterion for recency depends on context.
If someone asks for the CEO, the most recent entry is needed.
If someone asks for all past CEOs, every entry is needed.
If someone asks for revenue trends, the last 8 quarters are needed.

If time exists as a field, these conditions can be expressed as a query.
If time is buried in natural language, it must be extracted every time.

---

## Why Filtering Is Not Mechanical Verification

There is an important distinction here.

Of filtering's three criteria -- relevance, trustworthiness, recency --
trustworthiness and recency can be largely processed mechanically in a structured representation.
Field comparison, value sorting, range filtering.

Then why call this "filtering" and not "verification"?

Verification looks only at properties of the information itself.
"Does this statement have a time field?" Present or absent. No context needed.

Filtering looks at the relationship between information and situation.
"Is the time of this statement appropriate for this question?" You must know what the question is to answer.

Both examine the same time field,
but verification checks "existence"
and filtering judges "appropriateness."

Existence needs no context.
Appropriateness needs context.

This difference is why the pipeline separates the two stages.

---

## The Cost Structure of Filtering

Filtering is more expensive than verification. But how expensive depends on the representation.

**Filtering in a natural language pipeline:**
Relevance judgment -- LLM inference or embedding similarity computation.
Trustworthiness judgment -- LLM extracts source information from text and evaluates.
Recency judgment -- LLM extracts time information from text and compares.
All reasoning. All expensive.

**Filtering in a structured representation:**
Relevance judgment -- entity/property field matching + context-based judgment.
Trustworthiness judgment -- confidence field comparison. Source field matching.
Recency judgment -- time field sorting. Range comparison.
Trustworthiness and recency are field operations. Only relevance requires judgment.

In other words, structuring converts two of the three filtering criteria into mechanical operations.
What remains is relevance alone.
Even relevance narrows from "is this blob of text similar to the question" to "is this entity's this property relevant to the question," making the judgment clearer.

The total cost of filtering drops significantly.

---

## What Happens Without Filtering

If you verify but put everything into the context without filtering.

All 1,000 valid pieces of information go in.
Of those, only 30 are needed right now.

The LLM reads all 1,000.
Reading costs money.
970 unnecessary pieces of information scatter attention.
Research shows that more irrelevant information in the context increases the likelihood of hallucination.
Reasoning quality on the 30 that actually matter degrades.

The window is also wasted.
Out of the space 1,000 items occupy, 970 items' worth is waste.
That space could have held other, more relevant information.

Filtering is about managing a finite window finitely.
If verification confirms "does it qualify to enter,"
filtering judges "does it have a reason to enter."

Qualification is a matter of format. Reason is a matter of context.
Both are necessary.

---

## Filtering Is Policy

One more important point.

The criteria for filtering are not fixed.
They vary with context.

Filtering for a medical consultation agent:
Trustworthiness threshold is high. Exclude confidence below 0.9.
Recency standard is strict. Exclude medical information older than 3 years.
Exclude sources that are not peer-reviewed journals.

Filtering for a casual conversation agent:
Trustworthiness threshold is low. Approximate information is acceptable.
Recency standard is flexible. Older information may be included depending on context.
Source constraints are loose.

The same information passes in one agent and is rejected in another.
The information has not changed. The policy is different.

This means filtering is not merely a technical problem
but a design problem.
"What goes into the context" is the same question as
"what standards do we want this agent to operate by."

In a structured representation, this policy is expressed declaratively.
"confidence >= 0.9, time >= 2022, source_type = peer-reviewed."
One query line.

In natural language, this policy is written as natural language in a prompt.
"Please only refer to trustworthy recent information."
Whether the LLM follows this consistently is a matter of probability.

---

## Summary

Not all information that passes verification is needed.
A finite context window should contain only what is needed for the current inference.

Filtering judges three things.
Relevance -- is this information needed for the current question?
Trustworthiness -- can this information be believed?
Recency -- is this information sufficiently current?

Verification and filtering ask different questions.
Verification asks "is it valid?"; filtering asks "is it needed?"
Verification is possible without context; filtering requires context.
Verification comes first; filtering comes after.

In a structured representation, two of filtering's three criteria -- trustworthiness and recency -- are converted to field operations. What remains is relevance alone, and even that becomes clearer through structural field matching.

Filtering is policy.
The same information is included or excluded depending on context.
In a structured representation, this policy is declared as a query.
In natural language, this policy is written in the prompt as a hope.
