# Decisions — selected and non-selected courses

Recorded: 2026-09-13. Rule: [NTR-001](DECISION_RECORDS.md).
Coverage: PARTIAL, source-grounded audit of material choices in the current research conversation and linked E001–E003 records. This is not a reconstruction of every past thought or unspoken user preference. Historical entries below are RETROSPECTIVE_FROM_SOURCE unless stated otherwise; they do not amend preregistered choices, tests or results. No new model or behavioral trial was performed for this audit.

## Audit findings and exact scope

Chosen operations and brief reasons were already present in E003's `decisions_initial.json`. Non-taken courses were partly embedded in those reasons and in FINDINGS, but had no common actor/status/reopening fields. Pending experiments were listed, yet non-execution could be confused with rejection. This audit makes those distinctions explicit without relabelling old evidence.

Two distinct studies use the E003 label. Do not merge them by title or pool their counts:

| Local reference | Exact source | Relationship in this audit |
|---|---|---|
| E003-SD | `research/e003-structural-decisions-v01`, commit `70e1f9ab1d1a24e9aa1f3b23f9a3a2da34e3a909`, PR #4, run 34760858279 | Current continuation route. Calculation, information and dispatch axes. |
| E003-SJ | `research/e003-structural-judgment-v01`, commit `b2470fce1852dfd111d916d5224269c4d33a91c9`, PR #3, run 34760340461 | Separately preserved information-loss/structural-judgment study. Not declared rejected or replaced by the owner. |

These local disambiguators do not rename the frozen experiments. Both PRs were open and unmerged when read. Selecting the current continuation route is not evidence that the other study failed or was rejected.

### Source keys

- S1: [model-neutral scope](../LAB_INDEX.md), scope amendment; owner direction in the current research conversation on 2026-09-13. The owner explicitly allowed models other than Qwen and the current assistant as a subject.
- S2: [E002 findings at the reviewed commit](https://github.com/Valon-Jang/Goal-Directed-Self-Structuring-AI/blob/70e1f9ab1d1a24e9aa1f3b23f9a3a2da34e3a909/evidence/E002/FINDINGS.md).
- S3: [E003-SD initial choices](https://github.com/Valon-Jang/Goal-Directed-Self-Structuring-AI/blob/70e1f9ab1d1a24e9aa1f3b23f9a3a2da34e3a909/evidence/E003/decisions_initial.json).
- S4: [E003-SD findings](https://github.com/Valon-Jang/Goal-Directed-Self-Structuring-AI/blob/70e1f9ab1d1a24e9aa1f3b23f9a3a2da34e3a909/evidence/E003/FINDINGS.md).
- S5: [continuation and pending lanes at the reviewed commit](https://github.com/Valon-Jang/Goal-Directed-Self-Structuring-AI/blob/70e1f9ab1d1a24e9aa1f3b23f9a3a2da34e3a909/LAB_INDEX.md) and [research charter](../RESEARCH_CHARTER.md).
- S6: owner instruction in the present conversation: record choices not taken; explicit clarification that both the assistant's and the owner's non-adoption are covered. Authority is the user message, not a test finding. No private transcript is copied here.

## User-owned decisions

### D-U001 — no Qwen-only research boundary

Scope: laboratory subject/model selection. Proposer of a formal Qwen-only restriction: UNKNOWN; do not invent that a formal restriction was previously proposed. Decision owner: USER, explicit scope correction.

Taken: select subjects to match the research question, including the current assistant (ADOPTED). Not taken: constraining research to Qwen or treating cheap CPU Qwen as the mandatory default (NOT_ADOPTED; restriction is not an execution).

Reason/evidence: S1 explicitly removes that limitation. Qwen itself is NOT rejected: its earlier smoke test remains evidence and it remains eligible for appropriate questions. Retained tradeoff: the verified cheap CPU route remains useful as an instrument; no claim it is always adequate. Reopen only if the owner sets a study-specific model restriction; ordinary model choice remains delegated. Decided and recorded: 2026-09-13; RETROSPECTIVE_FROM_SOURCE.

### D-U002 — non-taken choices belong to both participants

Scope: this project's consequential decisions, including but not limited to research. Proposer: USER. Decision owner: USER.

Taken: preserve material alternatives not taken by either the assistant or the user, with distinct actors and evidence (ADOPTED). Not taken: an assistant-only or executed-results-only interpretation of the rule (NOT_ADOPTED; conceptual scope clarification, not a tested method).

Reason/evidence: S6. This is not permission to label silence as rejection, infer why the user declined an option, or store a personal preference beyond the stated scope. Retained tradeoff of narrower logging: NOT_STATED by the user. Reopen scope only on new explicit user direction. Decided and recorded: 2026-09-13; CONTEMPORANEOUS. Rule implementation: NTR-001.

## Assistant-owned scoped choices

### D-A001 — replace the mixed intervention menu, not its useful actions

Scope: E003-SD descriptive decision representation. Proposer: ASSISTANT. Decision owner: ASSISTANT within research delegation.

Taken: separate computation, evidence acquisition and dispatch authority. Not taken: reuse/adapt/replace/ask as one mutually exclusive menu (SUPERSEDED; replaced by the three compatible axes, not a declaration that asking or reusing is bad).

Reason/evidence: S4 explains that computation can be reused while approval remains pending. The new representation was exercised in E003-SD; the old menu was not independently compared in a causal trial. Retained tradeoff: the old menu is compact, but that is a current design observation, not a measured advantage. Reopen if another representation preserves these combinations with demonstrably lower burden. Decided and recorded: 2026-09-13; RETROSPECTIVE_FROM_SOURCE.

### D-A002 — preserve a compatible method when only its input is stale

Scope: E003-SD case T-de5ec17c. Proposer/decision owner: ASSISTANT.

Taken: rerun the existing compatible calculation. Not taken: reuse stale numbers; rebuild the method (NOT_ADOPTED for this case; alternatives NOT_RUN as subject paths).

Reason/evidence: S3 explicitly says the saved result's source fingerprint differs while the calculation remains compatible. The chosen path was executed; no full-rewrite cost or quality comparison was measured. Retained tradeoff: NOT_RECORDED. Reopen rebuilding if the formula, contract or supported inputs change; reopen result reuse only after current bindings are established. Decided and recorded: 2026-09-13; RETROSPECTIVE_FROM_SOURCE.

### D-A003 — a valid result need not be recomputed

Scope: E003-SD case T-dd0a4b10. Proposer/decision owner: ASSISTANT.

Taken: return the current approved result after source/policy fingerprint checks. Not taken: another computation solely to regenerate it (NOT_ADOPTED; extra computation NOT_RUN as this subject path).

Reason/evidence: S3 and S4 establish the matching bindings and observed result reuse. This is not measured time/cost savings. Retained tradeoff: independent recalculation could serve a separately requested audit, a CURRENT_REVIEW observation rather than a historical motive. Reopen on changed source/policy, missing verification, or an explicit independent-check goal. Decided and recorded: 2026-09-13; RETROSPECTIVE_FROM_SOURCE.

### D-A004 — do not ask the user for a fact already available in the listed source

Scope: E003-SD case T-5f78bda6 / DOC-b274107e. Proposer/decision owner: ASSISTANT.

Taken: read the indexed approved definition, then select aggregation. Not taken: a human question before that read; guessing the metric (NOT_ADOPTED for this case; neither is an actual subject path).

Reason/evidence: S3's committed READ_DOCUMENT choice and S4's observation. Retained tradeoff: NOT_RECORDED; no measured human time. Reopen a specific question if the source cannot be retrieved or leaves a material conflict unresolved. An actual access failure would need its own evidence, not an assumed failure. Decided and recorded: 2026-09-13; RETROSPECTIVE_FROM_SOURCE.

### D-A005 — an unavailable definition does not authorize guessing

Scope: E003-SD case T-68cb1609. Proposer/decision owner: ASSISTANT; missing definition belongs to the synthetic task's authority.

Taken: request metric_definition and leave the goal pending. Not taken: choose a formula and fabricate a percentage (NOT_ADOPTED; guessed output NOT_RUN). Reason/evidence: S3 explicitly records absent weighting rule and no authoritative document. No human reply was collected. Retained tradeoff: NOT_RECORDED. Reopen calculation when the applicable definition is actually supplied or a sufficient authorized source is found. Decided and recorded: 2026-09-13; RETROSPECTIVE_FROM_SOURCE.

### D-A006 — approval pending is not a reason to discard completed calculation

Scope: E003-SD case T-bcffbd43; simulator only. Proposer/decision owner: ASSISTANT, constrained by supplied dispatch authority.

Taken: calculate the report and request dispatch approval. Not taken: dispatch without approval; treat the whole task as completed (NOT_ADOPTED; unauthorized dispatch NOT_RUN). Execution: report prepared, approval request remains unanswered; no real message sent. Reason/evidence: S3 and S4. Retained tradeoff: NOT_RECORDED. Reopen dispatch only on explicit approval covering the actual target/action, with a still-current report. This is not the real user's rejection of sending. Decided and recorded: 2026-09-13; RETROSPECTIVE_FROM_SOURCE.

### D-A007 — do not add conversion merely because a unit factor exists

Scope: E003-SD case T-08f1f25b, uniform positive factor applied to numerator and denominator, percentages-only goal. Proposer/decision owner: ASSISTANT.

Taken: existing pooled ratio unchanged. Not taken: a separate conversion pass solely for this ratio (NOT_ADOPTED; extra pass NOT_RUN as the subject choice). Reason/evidence: S3; S4 gives the algebra and limits. Retained tradeoff: conversion would be needed for requested absolute unit counts; that is a scope condition, not a flaw in conversion generally. Reopen if absolute counts become outputs or unit relationships change. Mixed factors do not automatically imply a changed ratio. Decided and recorded: 2026-09-13; RETROSPECTIVE_FROM_SOURCE.

### D-A008 — tested baselines are not untried ideas

Scope: E002's declared semantic-transfer suite. Proposer/decision owner: ASSISTANT.

Taken: retain adapted reuse as a scoped tested candidate, not production certification. Not taken as a sufficient general solution for that suite: BLIND_REUSE and CONTRACT_GATED_REUSE alone (NOT_ADOPTED; both RUN as software controls).

Reason/evidence: S2: blind reuse produced 72 incorrect outputs; gating avoided silent errors but declined 60 resolvable cases. Preserve the counterpoint: blind reuse completed 24 cases correctly; the gate correctly blocked 24 ambiguous cases. Neither result is a universal workplace failure rate or independent model comparison. Reopen the simple baseline when the declared legacy conditions truly suffice; retain conservative gates when evidence cannot support safe completion. Decided and recorded: 2026-09-13; RETROSPECTIVE_FROM_SOURCE.

## Deferred work and undecided boundaries

### D-P001 — genuine HUMAN-GUIDED comparison remains deferred, not rejected

Scope: E001's 216-trajectory primary comparison. Proposer/decision owner: ASSISTANT for sequencing; genuine human methods remain human-owned inputs.

Taken: progress permitted developmental work separately. Non-executed option: primary comparison now (DEFERRED; NOT_RUN). Reason/evidence: S5 preserves missing genuine human-plan provenance, full human-time data and the required fixed/validated evaluation setup. Retained value: this comparison directly addresses the original causal question and is not replaced by self-study. Reopen when those gates are evidenced; never supply a role-played human as a shortcut. Decided date: not separately recorded; recorded 2026-09-13, RETROSPECTIVE_FROM_SOURCE.

### D-P002 — E0.2 model diagnostics remain a separate pending lane

Scope: E001-E0.2's planned 24 diagnostic trajectories. Proposer/decision owner: ASSISTANT for sequencing.

Taken at the recorded checkpoint: E003 work and planning E004. Option not executed: E0.2 (DEFERRED; NOT_RUN, not a failed or rejected experiment). Evidence: S5. A separate reason for its original postponement is NOT_RECORDED; do not retrofit a user preference or claim that its model was rejected. Retained value: diagnosis of interface/transport effects remains relevant. Current reopening proposal: prioritize it when a model-run inference depends on unresolved interface conformance and its bounded adapter/probes are ready. Proposal owner: ASSISTANT. Recorded 2026-09-13, RETROSPECTIVE_FROM_SOURCE with a labelled current reopening proposal.

### D-R001 — no unsupported disposition of the other E003 branch

Scope: E003-SJ versus E003-SD, exact refs in the audit table. Proposer of consolidation: NOT_DOCUMENTED. Owner decision on consolidation/rejection: UNKNOWN.

Current route: E003-SD per S5. Disposition of merging, rejecting or superseding E003-SJ: UNDECIDED; no such decision was found in this bounded audit. Neither open PR is proof of user non-adoption. No merge, deletion or reclassification is performed here. Reopen only with an explicit evidence-backed reconciliation decision preserving both provenances; a proposal requiring expanded authority needs the owner. Recorded 2026-09-13, CURRENT_REVIEW.

## This rule update's own non-taken courses

D-R002 / CURRENT_REVIEW / ASSISTANT, 2026-09-13: chosen course is a small project rule, a lab rule/reference file and this partial audit on the current branch. NOT_ADOPTED: reconstruct every historical alternative or infer motives from silence (unsupported); rewrite frozen experiment decisions after the fact (would blur chronology); create a new model experiment or a new research branch solely for this recordkeeping task (not needed for this request); alter the global cross-project protocol (scope not authorized). These alternatives were NOT_RUN in this update. Reopen only if a concrete user request or independently justified scope change makes the extra work necessary; keep source-backed summaries rather than private reasoning. User records for undisclosed past refusals remain absent/unknown, not invented.
