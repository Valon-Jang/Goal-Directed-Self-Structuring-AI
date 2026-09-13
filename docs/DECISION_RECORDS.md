# Decision records — choices taken and not taken

Rule ID: NTR-001. Version: 1.0. Effective: 2026-09-13.
Authority: the owner explicitly required retention of choices not taken and clarified that this includes both the assistant's choices and the owner's non-adoption of proposals. This is a recordkeeping rule, not permission to infer the owner's intentions or a requirement to force every task through a decision tree.

## Scope and trigger

For consequential goals, methods, models, tools, architecture, evidence acquisition, permissions and research claims, retain the chosen course together with material alternatives actually proposed, compared, declined or deferred. The proposer and the decision owner may each be USER or ASSISTANT and need not be the same person. A user proposal not taken by the assistant is covered too; the assistant may decline or defer only within its delegated authority and cannot silently overrule a user decision.

Record an explicit user rejection, cancellation or postponement promptly. Consolidate other consequential choices at the next research checkpoint. Include a proposal still awaiting a decision when losing that fact could cause repetition or unauthorized execution. Do not enumerate imaginary alternatives, retain every passing thought, or create a new file for every turn. No minimum number of alternatives is required. State PARTIAL or NO_DOCUMENTED_ALTERNATIVES when coverage is incomplete; absence of a record is not proof no alternative existed.

The primary record belongs beside the decision's authoritative project/experiment record. In this laboratory use [DECISIONS.md](DECISIONS.md) for cross-cutting choices and explicit user direction, and the experiment's existing decision file or a linked addendum for detailed case choices. Do not copy private project context into this public repository. Operational failure fingerprints stay in their existing operational records and are linked, not duplicated.

## Two states that must remain separate

| Decision status | Meaning |
|---|---|
| ADOPTED | Explicitly selected in the stated scope; execution may still be pending. |
| NOT_ADOPTED | A documented choice not to use this option in this scope. Not an assertion that it is generally inferior. |
| DEFERRED | A documented postponement, with the blocking dependency or priority and a reopening condition. |
| UNDECIDED | Proposed, but no supported adoption/non-adoption decision is available. Silence and topic changes stay here. |
| SUPERSEDED | A previous decision has an explicit replacement; preserve both and their linkage. |

Record execution independently as NOT_RUN, RUN, or UNKNOWN. For a RUN, identify whether it was an actual subject action, a scripted control, an artifact test or a replay, and link the observed outcome. Rejected-by-choice, not-yet-tested and experimentally failed are different facts. A missing measurement stays unknown, not zero.

Do not treat mutually compatible actions as competitors: computation changes, information acquisition and permission/dispatch may be selected together. Selecting one option rules out another only within an explicitly exclusive choice and the stated scope.

## Compact record

A record may be a short table row or a small section. Preserve these fields without requiring empty boilerplate:

- Stable decision ID; project/experiment/case and exact version or source scope.
- Proposer (if known), decision owner, and decision authority; use UNKNOWN rather than inventing an actor.
- What was taken and what was not taken or remains undecided, with separate option statuses.
- The publicly explainable reason and supporting source; a reason not supplied by the user is NOT_STATED, not an inferred personal preference. A structural deduction is labelled as such rather than as an observed trial.
- Execution status and evidence scope. Keep a tested control's outcome separate from the subject's actual behavior.
- A material advantage or tradeoff of the non-taken option when supported. Do not rewrite every alternative as obviously bad; when absent, say NOT_RECORDED instead of fabricating a historical motivation.
- Reopening trigger and who may reopen/authorize it; triggers such as a changed goal, new evidence, a different backend or permission approval must be specific enough to check. A proposed trigger is not a scheduled task or an actual approval.
- Decision date when known, record date, and provenance mode: CONTEMPORANEOUS, RETROSPECTIVE_FROM_SOURCE, or CURRENT_REVIEW. A retrospective addendum does not alter a prior freeze or pretend the record existed earlier.

Example shape:

    ID / scope / proposer / decision owner
    Taken: ...
    Not taken: ... [decision status; execution status]
    Reason and evidence: ...
    Retained tradeoff: ... or NOT_RECORDED
    Reopen when / authority: ...
    Decided / recorded / provenance: ...

## Use on the next decision

Read matching prior records before repeating a material recommendation or repeating a known excluded route. Match the actual scope, goal, constraints and evidence, not just an option's name. If conditions have not changed, respect the recorded choice instead of repeatedly pitching it or silently executing it. If conditions have changed, cite the previous record, state what changed and open a new linked review; do not erase the earlier decision. User-owned boundaries still require user authorization to change. Record a changed user decision without turning the old one into a timeless personal trait.

A user selecting a broader research scope does not reject every model inside it. No response is not rejection. An open/unmerged PR is not evidence the owner rejected its research. A missing capability or authorization is not the owner's dislike of it. A tested but non-adopted baseline must remain accessible for reproducibility.

## Audit and acceptance

Before marking a consequential decision record complete, check the actor, scope, status, evidence, timing and reopening condition. Verify that historical reasons are source-backed, unknown motives remain unknown, tests are not relabelled as real decisions, and original results/freeze files remain unchanged. Store concise decision summaries only: no private chain-of-thought, hidden reasoning, full dialogue dumps, credentials or unsupported psychological profiles.

This rule adds no new model benchmark, unattended loop, spending, permission expansion or global cross-project protocol change. Its project-wide human/assistant scope is owner-confirmed; this file is the laboratory implementation of that rule.
