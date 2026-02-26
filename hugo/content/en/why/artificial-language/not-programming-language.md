---
title: "Why Programming Languages Are Not Enough"
weight: 10
date: 2026-02-26T12:00:19+09:00
lastmod: 2026-02-26T12:00:19+09:00
tags: ["programming language", "description", "knowledge representation"]
summary: "Programming languages describe procedures. They cannot describe the world. JSON provides structure but no meaning. Even LISP merely borrows syntax."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Programming languages describe procedures. They cannot describe the world.

---

## Programming languages are among humanity's greatest inventions

Programming languages are unambiguous.
`x = 3 + 4` yields 7 no matter when or where it runs.
There is no room for interpretation.

Programming languages are verifiable.
Syntax errors are caught before compilation.
Type errors are caught before execution.
When tests run, the result is either pass or fail.

Programming languages are Turing-complete.
They can express anything that is computable.
Given enough time and memory, any procedure can be described.

Everything this series identified as limitations of natural language — ambiguity, unverifiability, lack of structure — programming languages have solved.

So why not use a programming language to represent an AI's context?

It doesn't work.

---

## Programming languages describe procedures

The following is valid Python code.

```python
def calculate_revenue(units_sold, unit_price):
    return units_sold * unit_price
```

This code is clear, verifiable, and executable.
But what does it express?

"Multiply the number of units sold by the unit price to get revenue."

This is a procedure. A method. HOW.
It describes what to do when input arrives.

Now try to express the following.

"Samsung Electronics' revenue in Q3 2024 was 79 trillion won."

This is not a procedure. It is a fact. WHAT.
Nothing is executed. It describes the state of the world.

How do you express this in Python?

```python
samsung_revenue_2024_q3 = 79_000_000_000_000
```

A number is assigned to a variable.
It works. But this is not description. It is storage.
This code does not know:

- What kind of entity "Samsung Electronics" is.
- What "revenue" means. Is it a financial metric? A physical quantity?
- Whether "Q3 2024" is a time, a version, or a label.
- What the source of the 79 trillion won figure is.
- How certain this value is.

The variable name `samsung_revenue_2024_q3` lets a human guess the meaning.
To the machine, it is an arbitrary string.
Rename it to `xyzzy_42` and the execution result is the same.

In programming languages, variable names carry no meaning.
The meaning lives outside the code, in the programmer's head.

---

## More sophistication doesn't help

Why not create a class?

```python
class FinancialReport:
    def __init__(self, company, metric, period, value, currency):
        self.company = company
        self.metric = metric
        self.period = period
        self.value = value
        self.currency = currency

report = FinancialReport("삼성전자", "매출", "2024-Q3", 79_000_000_000_000, "KRW")
```

Better. There is structure now.
But problems remain.

`company` is the string "삼성전자" (Samsung Electronics).
"Samsung Electronics," "SEC," and "005930" all refer to the same company.
Does the code know this? No.
It can only compare whether strings are equal or not.

`metric` is the string "매출" (revenue).
Are "매출," "매출액," and "revenue" the same thing or different?
The code doesn't know. The strings differ, so they are different.

Why not define a schema?
Manage company lists with Enums, manage metric lists.
Sure. It works.

Then try to express the following.

"Yi Sun-sin was great."

```python
opinion = Opinion("이순신", "was", "위대했다")
```

What is this?
A string "이순신" (Yi Sun-sin) bound to a string "위대했다" (was great).
It does not express "Yi Sun-sin was great."
It stores "이순신" and "위대했다."

The code does not know the meaning of "위대했다" (was great).
Whether "위대했다" (was great) and "훌륭했다" (was admirable) are similar,
whether "비겁했다" (was cowardly) is the opposite —
the code cannot tell.

Structured facts like financial data are somewhat manageable.
Evaluations, context, relationships, abstract descriptions lie beyond the expressive range of programming languages.

---

## Code doesn't know what it does

```python
def process(data):
    result = []
    for item in data:
        if item["value"] > threshold:
            result.append(transform(item))
    return result
```

This code executes perfectly.
But what does it do?

Is it filtering revenue data?
Screening patient records?
Cleaning sensor data?

The code itself doesn't know.
`data`, `value`, `threshold`, `transform` — all abstract names.
Whether this code belongs to a financial system or a medical system
depends on context outside the code.

You can write comments.
But comments are natural language. Machines don't understand them.
If a comment contradicts the code, the compiler doesn't notice.
Comments are for humans, not machines.

When an AI receives code as context, this problem manifests directly.
Because code has no self-identity,
the AI must reconstruct its identity through inference every time.
Since it's inference, it costs compute and can be wrong.

---

## The fundamental reason

That programming languages cannot describe the world is not a design flaw.
The purpose is different.

The purpose of a programming language is to instruct a machine on procedures.
"When this input arrives, perform this operation."
The semantics of a programming language are the semantics of execution.
Every construct is interpreted as "what does the machine do."

`x = 3` is the instruction "store 3 in the memory location named x."
`if x > 0` is the instruction "if x is greater than 0, execute the next block."
`return x` is the instruction "return the value of x to the caller."

All verbs. All actions. All procedures.

"Samsung Electronics is a Korean company" is not a verb.
Not an action. Not a procedure.
It describes the state of the world.

Programming languages have no place for this.
You can store it in a variable, but that is storage, not description.
The meaning of the stored value is not the code's concern.

---

## What about JSON, YAML, XML?

If not programming languages, what about data formats?

```json
{
  "company": "삼성전자",
  "metric": "매출",
  "period": "2024-Q3",
  "value": 79000000000000,
  "currency": "KRW"
}
```

There is structure. Fields are explicit.
But there is no meaning.

JSON doesn't know whether "company" means a corporation.
JSON doesn't know whether "삼성전자" is the same as "Samsung Electronics" elsewhere.
JSON doesn't know whether this JSON object and that JSON object describe the same entity.

JSON provides structure but not meaning.
It is key-value pairs, not entity-relationship-attribute.

Defining schemas helps.
JSON Schema, Protocol Buffers, GraphQL.
Field types are defined, required fields are defined, references are defined.

But these are all structures designed for specific systems.
They are not general-purpose knowledge representation.
A financial data schema cannot express the evaluation of a historical figure.
A medical data schema cannot express competitive relationships between companies.

A separate schema for each domain.
A separate tool for each schema.
No interoperability between schemas.

This limitation is discussed in more detail in [Why MD/JSON/XML Won't Work](/why/not-md-json-xml/).

---

## What about LISP?

Some readers may have thought of a counterexample.

LISP.

```lisp
(is 삼성전자 (company korea))
(revenue 삼성전자 2024-Q3 79000000000000)
(great 이순신)
```

S-expressions are tree structures,
and code is data and data is code.
Homoiconicity.

In fact, early AI was entirely LISP-based.
SHRDLU, CYC, expert systems.
Knowledge was represented in LISP, and inference engines ran on it.
It seems like a historical counterproof to "programming languages cannot describe the world."

But the counterexample fails for three reasons.

### What LISP knows vs. what the programmer decided

In `(is 삼성전자 company)`, LISP does not know
that `is` means the relation "is a."
The programmer decided that.

Replace `is` with `zzz` and LISP doesn't care.
`(zzz 삼성전자 company)` is a perfectly valid expression to LISP.

LISP provides structure. A tree called S-expression.
But the meaning within that structure was assigned by the programmer, not the language.
This is fundamentally the same as JSON not knowing the meaning of its keys.

Providing structure and embedding meaning are different things.

### CYC's 30 years

The most ambitious attempt at this was CYC.

Started in 1984.
It tried to represent general knowledge using LISP.
Millions of rules were entered by hand.

What 30 years proved was not feasibility but limitations.

Ontologies had to be manually designed for each domain.
Cross-domain interoperability didn't work.
It couldn't keep up with the flexibility of natural language.
As scale grew, maintaining consistency became nearly impossible.

That knowledge representation "can be done" in LISP is true.
That it "works well" is what 30 years of results refute.

### If you're not going to eval, there's no reason to use LISP

The most fundamental problem.

LISP's power is `eval`.
Because code is data, data can be executed.
Metaprogramming, macros, runtime code generation.
This is what makes LISP LISP.

But what happens when you `eval` `(is 삼성전자 company)`?

It becomes a function call passing `삼성전자` and `company` as arguments to a function named `is`.
Not description — execution.

To use it for knowledge representation, you must not eval.
If you're not going to eval, you're not using LISP's semantics.
You're merely borrowing the syntax of S-expressions.

That is not "describing the world in LISP."
It is "storing data using LISP's parenthetical notation."

LISP's semantics as a programming language — the semantics of execution —
are still designed for describing procedures.
Borrowing the syntax does not change the semantics.

---

## What a language for describing the world requires

Programming languages describe procedures.
Data formats provide structure but no meaning.
Even LISP merely borrows syntax without the semantics of description.

What does a language for describing the world need?

**Entity identity.** "Samsung Electronics" must have a unique identifier. The machine must know it is the same as "삼성전자." Not string comparison, but identity equivalence.

**Expression of relationships.** In "Samsung Electronics is a Korean company," it must be possible to express the relationship "Korean company." Not variable assignment, but description of relationships.

**Self-describing descriptions.** What the description is about, who said it, as of when, and how certain — all must be included in the description itself. Inside the code, not outside.

**Domain independence.** Financial data, historical facts, subjective evaluations, abstract relationships — all must be expressible in the same format. Not a separate schema for each domain, but one universal structure.

Programming languages possess none of these four properties.
Because programming languages were not built for this.
They were built to describe procedures.

Natural language can do all four. Ambiguously.
What is needed is a combination of natural language's expressive range and programming language's precision.

---

## Summary

Programming languages are unambiguous, verifiable, and Turing-complete.
But they cannot describe the world.

Programming languages describe procedures.
"When this input arrives, do this." All verbs, all actions.
"Samsung Electronics is a Korean company" is not an action.
Programming languages have no place for it.

Code doesn't know its own identity.
What domain it belongs to, what purpose it serves —
none of this is recorded within the code.

Data formats like JSON and YAML provide structure but no meaning.
LISP can borrow syntax, but it has no semantics of description.
CYC spent 30 years attempting LISP-based knowledge representation, and what it proved was the limitation.

Describing the world requires entity identity, expression of relationships, self-describing descriptions, and domain independence.
Programming languages were not built for this.
Natural language can do it, but ambiguously.
What is needed lies somewhere between the two.
