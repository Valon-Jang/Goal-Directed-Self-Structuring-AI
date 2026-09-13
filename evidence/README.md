# Evidence

This directory is for observed results, not persuasive summaries.

## Evidence classes

- experiment inputs and configuration;
- exact model / tool / environment versions where relevant;
- raw or minimally transformed results;
- evaluator outputs;
- failure cases;
- cost and latency measurements;
- human intervention records;
- replication results;
- falsification evidence.

## Evidence policy

- Preserve negative results.
- Separate observation from interpretation.
- Do not promote a capability based only on the same component's self-evaluation.
- Record benchmark changes that affect comparability.
- Do not silently remove failed runs because a later version performs better.
- Treat provider/runtime-specific behavior as scoped evidence, not universal fact.

## Current evidence state

At repository initialization, GDSSA is a conceptual hypothesis with experiment designs but without a completed controlled benchmark.

The absence of evidence is explicit. The theory should become narrower or change if experiments fail.
