# Experiments

## Experiment 0 — Concept sanity checks

Purpose: verify that the distinction between BARE-GOAL and HUMAN-GUIDED can be implemented without changing model, tools, evidence, or success criteria.

Required controls:

- same model and reasoning level;
- same task inputs;
- same tools and permissions;
- same time / cost ceilings;
- same success evidence;
- only the method-design responsibility differs.

## Experiment 1 — BARE-GOAL vs HUMAN-GUIDED

Primary hypothesis:

> For sufficiently capable models and observable tasks, BARE-GOAL can match or exceed HUMAN-GUIDED while requiring less human intervention.

Measure:

- real-world task success;
- semantic correctness;
- format / policy compliance separately;
- human intervention count;
- human intervention minutes;
- unnecessary questions;
- total model/tool cost;
- elapsed time;
- retries and rework;
- number of structure/tool changes;
- reusable capabilities created;
- performance on a related second task.

## Experiment 2 — Evidence quality

Hold the model and goal fixed while varying access to observable evidence.

Question:

> Does self-structuring fail primarily because of reasoning limits, or because the system cannot observe reality well enough to evaluate goal distance?

## Experiment 3 — Model capability crossover

Run the same matched tasks across model capability tiers.

Question:

> At what capability level does procedural human guidance shift from useful scaffold to unnecessary or harmful constraint?

## Experiment 4 — Persistent capability reuse

Allow verified capabilities and operational lessons from task A to persist into task B while keeping private task facts isolated.

Question:

> Does accumulated capability reduce human intervention without increasing failure or hidden coupling?

## Experiment 5 — Restructuring control

Compare:

- unrestricted replanning within authority boundaries;
- bounded restructure budget;
- fixed initial workflow.

Question:

> When does self-structuring improve adaptation, and when does it become architecture thrashing?

## Experimental discipline

Negative and null results are first-class evidence. A failed hypothesis should change the architecture rather than be hidden by redefining success after the run.
