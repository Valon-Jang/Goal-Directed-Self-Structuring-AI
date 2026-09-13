# Benchmarks

GDSSA benchmarks should evaluate **goal achievement under different allocations of method-design responsibility**.

## Benchmark requirements

A valid benchmark case should have:

- a real or faithfully simulated goal;
- observable success evidence;
- bounded authority and cost;
- at least one plausible alternative path;
- enough uncertainty that method design matters;
- a way to distinguish semantic success from format compliance;
- a measurable human-intervention burden.

## Primary metrics

### Outcome

- success / failure;
- degree of goal attainment;
- quality / correctness;
- policy and safety compliance.

### Human burden

- number of human interventions;
- minutes of human attention;
- number of human-designed method steps;
- number of questions that could have been resolved without the human.

### System cost

- model tokens / API cost;
- tool cost;
- elapsed time;
- retries;
- unnecessary capability creation;
- architecture changes.

### Learning / reuse

- verified capabilities created;
- capability reuse rate;
- improvement on related later tasks;
- regression or hidden coupling caused by persistent learning.

## Candidate aggregate metric

A useful summary metric may be:

```text
Goal Progress
---------------------------------------
Human Intervention + Cost + Risk Penalty
```

This is only a research direction. The denominator weights must not be chosen after seeing results.

## First benchmark family

Start with bounded knowledge-work tasks where results are independently checkable, for example:

- structured data comparison and report generation;
- multi-source research with explicit evidence requirements;
- small software changes with tests;
- workflow redesign with measurable baseline and post-change time;
- repeated office processes with deterministic checks.

Avoid using open-ended strategic judgment as the first benchmark because success evidence would be too subjective.
