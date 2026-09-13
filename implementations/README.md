# Implementations

No general GDSSA implementation is claimed yet.

This directory is reserved for reference implementations that earn their status through experiments.

## Minimum implementation contract

A future GDSSA prototype should separate:

1. **Goal Contract** — goal, boundaries, authority, reality facts, success evidence.
2. **Goal-Directed Core** — unknown discovery, evidence acquisition, path comparison, structure design.
3. **Capability Layer** — tools, APIs, Skills, code, reusable functions.
4. **Knowledge / Persistence Layer** — verified facts, decisions, operational learning, capability trust state.
5. **Execution Layer** — bounded actions against the real or simulated environment.
6. **Observation Layer** — independent collection of outcome evidence.
7. **Evaluation Layer** — comparison between current reality and success criteria.
8. **Authority Gate** — permissions, budgets, irreversible actions, promotion to production.

## Design rule

Do not implement a large framework before the benchmark proves that the missing capability requires one.

Prefer the smallest sufficient structure:

```text
direct model call
→ model + tools
→ model + persistent state
→ model + capability builder
→ multi-agent / distributed structure only when evidence justifies it
```

## Non-goals for the first prototype

- unrestricted self-modification;
- silent permission expansion;
- autonomous production deployment;
- a custom foundation model;
- a large UI platform;
- a fixed multi-agent topology.

The first prototype should make the experimental comparison easy, not attempt to be a commercial product.
