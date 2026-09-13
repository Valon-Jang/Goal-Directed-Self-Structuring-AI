# Goal-Directed Self-Structuring AI

## From Prompt Engineering to Goal Engineering

**Research status:** Conceptual hypothesis v0.1  
**Date:** 2026-09-13  
**Public research note:** This document records an independently derived operating model. It does **not** claim academic priority, novelty against all prior work, or experimental validation yet.

> **Human owns the goal. AI owns the path. Reality decides whether it worked.**

---

## Abstract

Most human-AI workflows still leave the human responsible for designing the method.

The human decides what to ask, what questions the AI should ask back, what tools should be used, what sequence should be followed, and often what architecture should be built. Even advanced agentic systems frequently begin from a human-specified workflow or from a large set of procedural instructions.

This research explores a different operating model:

> **The human provides the goal. The AI becomes responsible for discovering what must be known, designing the structure required to reach the goal, acquiring or building the necessary capabilities, executing, observing the result, and repeatedly restructuring its approach so that the system moves closer to the goal.**

The human no longer acts as the primary method designer. The human becomes the **Goal Owner, Reality Authority, Observer-Advisor, and Approver for consequential actions**.

This is called **Goal-Directed Self-Structuring AI (GDSSA)**.

The corresponding human skill shifts from **Prompt Engineering** toward **Goal Engineering**.

---

# 1. The Core Inversion

Traditional interaction:

```text
Human decides method
        ↓
Human writes instructions
        ↓
AI executes / answers
        ↓
Human notices gaps
        ↓
Human writes better instructions
```

Socratic interaction improves this by letting the AI ask the human for missing requirements:

```text
Human expresses intent
        ↓
AI asks questions
        ↓
Human supplies answers
        ↓
AI builds the requested result
```

GDSSA moves the responsibility boundary one level further:

```text
Human supplies GOAL
        ↓
AI determines what it must know
        ↓
AI infers / retrieves / measures / experiments
        ↓
AI asks the human only for irreducible human ground truth
        ↓
AI designs the required structure
        ↓
AI acquires / builds capabilities
        ↓
AI executes
        ↓
AI observes outcome
        ↓
AI evaluates distance to goal
        ↓
AI restructures and tries again
```

The important transition is not "better prompting."

It is:

> **Method-design responsibility moves from the human to the AI.**

---

# 2. New Human-AI Role Boundary

## Human

The human primarily owns:

- the goal;
- real-world facts that cannot be independently obtained;
- values and priorities;
- authority and permissions;
- approval for consequential or irreversible actions;
- observations from real deployment;
- strategic correction when the goal itself should change.

The human is **not expected to specify the implementation path**.

The human does not need to say:

- which program to build;
- which architecture to use;
- which questions the AI should ask;
- which tool should be chosen;
- which subproblems should be decomposed;
- what order those subproblems should be solved in.

Those become AI responsibilities unless the human intentionally constrains them.

## AI

The AI owns:

- decomposition of the goal;
- discovery of unknowns;
- evidence collection;
- selection of what can be inferred versus what must be measured;
- architecture and workflow design;
- tool and capability selection;
- capability acquisition or construction;
- execution;
- verification;
- failure diagnosis;
- comparison of alternative paths;
- observation of outcomes;
- replanning and restructuring;
- proposing changes to the goal when evidence shows the original goal is malformed or internally inconsistent.

---

# 3. Questioning Becomes an AI Action, Not the Workflow

A key ancestor of this idea was Socratic questioning:

> Instead of forcing the human to know every implementation requirement, the AI should discover which questions are necessary.

GDSSA generalizes that principle.

For every unknown, the AI should decide:

```text
Can I infer it reliably?
    → infer

Can I retrieve evidence?
    → retrieve

Can I measure it with a tool?
    → measure

Can I run a bounded experiment?
    → experiment

Do I lack a required capability?
    → acquire/build capability

Is this fact only available from the human?
    → ask the human
```

Therefore the design principle becomes:

> **Ask the human only when the missing information is both irreducibly human and capable of changing the next decision.**

Questions are no longer a default interaction pattern. They are one possible information-acquisition action inside a larger goal-directed loop.

---

# 4. Goal Engineering

Prompt Engineering asks:

> What should I tell the model so that it produces the result I want?

Goal Engineering asks:

> What goal, boundaries, reality constraints, permissions, and success evidence must exist so that the AI can determine the path itself?

A minimal Goal Contract may contain:

```text
GOAL
- desired real-world outcome

BOUNDARIES
- prohibited actions
- budget / time / security constraints

AUTHORITY
- what the AI may do autonomously
- what requires approval

REALITY
- human-only facts not externally recoverable

SUCCESS EVIDENCE
- observations that prove meaningful progress or completion
```

Everything else should be discovered or designed by the AI when possible.

The quality of the human-AI system therefore depends less on detailed prompts and increasingly on:

- goal quality;
- evidence quality;
- observation quality;
- capability access;
- evaluation quality;
- persistence of validated knowledge;
- safety boundaries.

---

# 5. Self-Structuring

"Self-structuring" does not mean unrestricted self-modification.

It means that the AI is allowed to decide what working structure is necessary to reach the goal.

Possible structures include:

- a simple direct answer;
- a temporary plan;
- a new Skill;
- a deterministic script;
- a reusable Capability;
- an external API connection;
- an evaluation harness;
- a persistent knowledge structure;
- multiple specialized agents;
- a workflow redesign;
- elimination of an unnecessary process;
- no new software at all.

The AI should not be rewarded for constructing complexity.

A strong system should prefer:

> **the smallest sufficient structure that moves the real outcome toward the goal.**

---

# 6. The Goal-Distance Loop

The system should not consider itself complete merely because a requested artifact was produced.

The completion question becomes:

> **Did the system measurably move closer to the goal?**

A generic loop is:

```text
Goal
  ↓
Current reality
  ↓
Estimate distance / failure gap
  ↓
Choose highest-value next intervention
  ↓
Acquire required knowledge or capability
  ↓
Execute
  ↓
Observe real outcome
  ↓
Evaluate
  ↓
Persist useful learning
  ↓
Restructure if needed
  └──────────────→ repeat
```

The loop can stop when:

- success evidence is satisfied;
- marginal improvement is no longer worth the cost;
- a human authority boundary is reached;
- the goal is impossible under current constraints;
- the goal itself must be revised.

---

# 7. Architecture Sketch

```text
                   HUMAN
       Goal / Values / Reality / Approval
                     │
                     ▼
              GOAL CONTRACT
                     │
                     ▼
       ┌─────────────────────────┐
       │ Goal-Directed AI Core   │
       │                         │
       │ Unknown Discovery       │
       │ Evidence Acquisition    │
       │ Structure Design        │
       │ Path Comparison         │
       └──────────┬──────────────┘
                  │
         ┌────────┴────────┐
         ▼                 ▼
  Capability Layer      Knowledge Layer
  Tool/API/Skill/Code    Facts/Decisions/Learning
         │                 │
         └────────┬────────┘
                  ▼
               EXECUTE
                  │
                  ▼
               OBSERVE
                  │
                  ▼
               EVALUATE
                  │
          Goal distance reduced?
            │             │
           yes            no
            │             │
        continue/stop ← restructure
```

This architecture deliberately separates **AI reasoning freedom** from **external action authority**. The AI may redesign the path, while permissions, budgets, irreversible actions, and security boundaries remain enforceable outside the model.

---

# 8. Relationship to AX AI

This concept emerged while designing an AI whose purpose is not merely to use AI tools, but to perform AX itself.

The AX architecture was:

```text
AX Scout
  → discover high-value transformation opportunities

AX Builder
  → acquire or build required capabilities

AX Operator
  → use those capabilities to perform real work

Evaluation / Learning Loop
  → observe outcomes and improve the system
```

GDSSA generalizes the same principle beyond AX.

The user no longer needs to say:

> "Find AX opportunities, ask me ten questions, build these three tools, then automate them."

The user can instead say:

> **"Goal: reduce this team's recurring workload by 50% without lowering quality."**

The AI must then determine what should be measured, what should be eliminated, what should be automated, what capability is missing, and how success should be verified.

---

# 9. Relationship to Root Engineering

Goal-directed autonomy becomes more valuable when models improve, but it also increases the need for durable validated state.

The model may change. The path may change. The tools may change. The architecture may change.

What should persist is:

- the goal;
- verified facts;
- decisions and constraints;
- capabilities and their trust state;
- evidence;
- successful and failed operational experience;
- important unresolved questions.

This makes Goal-Directed Self-Structuring AI complementary to [Root Engineering](https://github.com/Valon-Jang/Root-Engineering):

> **The AI may continuously redesign the path. The Root preserves what must survive those redesigns.**

---

# 10. What This Is Not

## Not merely autonomous agents

An autonomous agent may execute a predefined task loop.

GDSSA specifically places **workflow and architecture design responsibility** inside the AI's mandate and judges success against real goal progress rather than task completion alone.

## Not merely Socratic prompting

Socratic prompting improves requirement discovery through questions.

GDSSA treats questions as only one evidence-acquisition mechanism. The AI should infer, retrieve, measure, experiment, or build capabilities before asking the human when possible.

## Not unrestricted self-modification

The AI may redesign its working structure but should not silently expand permissions, rewrite safety boundaries, or promote unverified capabilities into production.

## Not "human out of the loop"

The human remains essential as Goal Owner, Reality Authority, and authority holder.

The shift is from **method operator** to **observer/advisor/approver**.

## Not one-shot delegation

A single generated answer is insufficient when the real-world outcome can be observed.

The system is expected to repeatedly compare reality with the goal and adapt.

---

# 11. Research Hypotheses

### H1 — Goal-only delegation can outperform instruction-heavy collaboration

For sufficiently capable models, a system given a good goal contract and access to evidence/tools will outperform a workflow in which the human prescribes detailed implementation steps.

### H2 — Better models increase the value of less procedural instruction

As model capability rises, detailed procedural scaffolding increasingly becomes a ceiling rather than an advantage unless it enforces a real external constraint.

### H3 — The optimal human role shifts upward

Human contribution will increasingly move from task decomposition and prompt design toward goal selection, real-world observation, value judgment, authority, and strategic correction.

### H4 — Persistent capability and operational memory create compounding returns

A goal-directed AI that retains verified capabilities and operational experience should require less human intervention over time.

### H5 — The correct metric is goal progress per human intervention

Useful evaluation should measure not only model accuracy but also:

```text
real outcome improvement
-------------------------
human intervention + cost + risk
```

---

# 12. Failure Modes

This model can fail badly if the goal is weak.

Important risks include:

- **Goal ambiguity** — the AI optimizes an interpretation the human did not intend.
- **Proxy capture** — measurable indicators improve while the real objective worsens.
- **Architecture thrashing** — the AI repeatedly redesigns instead of exploiting a good structure.
- **Capability sprawl** — unnecessary tools accumulate.
- **Silent authority expansion** — convenience is mistaken for permission.
- **Evidence failure** — the system cannot observe the real outcome and optimizes internal artifacts instead.
- **Cost blindness** — technically better paths cost more than the value they create.
- **Over-questioning** — the system pushes method design back onto the human.
- **Under-questioning** — the system guesses human-only values or facts.
- **Self-confirming evaluation** — the same component builds and judges its own work without independent evidence.

These failures imply that the highest-value engineering may not be more reasoning instructions. It may be better **goal contracts, evidence access, independent verification, permissions, and durable learning**.

---

# 13. Initial Experimental Design

A first benchmark should compare two modes on the same real task.

## BARE-GOAL

Give the AI:

- goal;
- boundaries;
- available environment;
- success evidence.

Do not prescribe the method.

## HUMAN-GUIDED

Give the same AI the human-designed decomposition, questions, suggested tools, and workflow.

Measure:

- final real-world success;
- human intervention count;
- human intervention minutes;
- number of unnecessary questions;
- execution cost;
- time to acceptable outcome;
- number of architecture/tool changes;
- error/rework rate;
- reusable capabilities created;
- performance on a second related task.

The interesting result is not whether BARE-GOAL always wins.

The research question is:

> **At what model capability, task type, and evidence quality does human procedural guidance stop helping and start constraining the system?**

---

# 14. Longer-Term Direction

If the hypothesis holds, human-AI interaction may evolve through the following stages:

```text
Commanding AI
    ↓
Prompting AI
    ↓
AI asking the human
    ↓
AI discovering what it needs to know
    ↓
AI acquiring what it needs to do
    ↓
AI designing the structure required by the goal
    ↓
Human governing goals, reality, authority, and values
```

The endpoint is not an AI that "does whatever it wants."

It is a system where:

> **Humans govern the destination and boundaries. AI increasingly owns the path.**

---

# 15. Working Definition

> **Goal-Directed Self-Structuring AI is an operating model in which the human supplies the desired outcome, irreducible real-world facts, values, and authority boundaries, while the AI assumes responsibility for discovering unknowns, designing and revising the working structure, acquiring capabilities, executing, observing results, and iteratively reducing the distance between current reality and the goal.**

Short form:

> **Human owns the goal. AI owns the path. Reality decides whether it worked.**

---

## Research lineage

This idea grew from several earlier directions:

1. **Socratic requirement discovery** — let AI discover the questions the human does not know to ask.
2. **Question-Driven Deepening** — ask only what can materially change the next decision.
3. **Root Engineering** — preserve durable validated knowledge outside replaceable model/runtime context.
4. **AX Scout / Builder / Operator** — let AI discover transformation opportunities, acquire capabilities, and perform the transformed work.
5. **Future-Improving Architecture** — persist goals/evidence/capabilities while allowing stronger future models to redesign the path.

GDSSA is the generalization:

> Instead of asking how the human should operate AI, ask how the AI should structure itself to achieve a human-governed goal.

---

## Repository map

```text
README.md                  # current theory / working definition
docs/                      # scope, terminology, related-work positioning
experiments/               # controlled experiment designs and runs
benchmarks/                # reusable evaluation tasks and metrics
implementations/           # reference implementations and prototypes
evidence/                  # observed results and falsification evidence
history/                   # superseded hypotheses that remain informative
```

The repository starts as a theory and experiment-design project. Implementation claims must be earned by evidence; the folder structure does not imply that a working autonomous GDSSA system already exists.

---

## Provenance

The concept was first written publicly on 2026-09-13 inside `Valon-Jang/Root-Engineering` as an independently derived research hypothesis, then promoted into this standalone repository after reviewing the existing research-repository topology. The original Root Engineering location is retained as a lineage pointer, not as the canonical GDSSA research source.