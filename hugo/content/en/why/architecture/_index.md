---
title: "Architecture"
date: 2026-02-26T12:00:00+09:00
image: "/images/og-default.webp"
summary: "How GEUL is built: semantically-aligned indexing, 16-bit word units, structured memory, and claims-based knowledge representation."
---

## Subtopics

### Why 16-Bit
All data in GEUL is in 16-bit (1-word) units. It is the minimum unit that combines the efficiency of machine code with the meaning of human language in a single word.

### Why Cache Reasoning as Code
Discarding results every time an AI reasons is a waste of computation. Recording reasoning in a structured language enables reuse and accumulation.

### Why Claims, Not Facts
Natural language sentences look like facts but are actually someone's claims. Structurally embedding source, timestamp, and confidence reduces the room for hallucination.

### Why a Semantically Aligned Index
SIDX is a 64-bit identifier that encodes meaning in the bits themselves. The type can be determined from the upper bits alone, and the fewer bits filled, the more abstract the expression becomes.

### Why Structured Memory Is Necessary
The context window of an LLM is finite. To fit infinite experience into a finite window, memory must be structured.
