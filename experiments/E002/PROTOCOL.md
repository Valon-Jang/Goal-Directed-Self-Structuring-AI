# E002 — Current-assistant capability transfer under semantic change

Status at registration: PLANNED / NOT EXECUTED. Date: 2026-09-13.

## Mandate and why this experiment

The user explicitly permits any suitable model, including the current assistant, as a research subject. Qwen is one previously observed instrument, not the research boundary. Research targets include models, the current assistant's tool use and generated artifacts, capability acquisition, evaluation and retained operating structures. Existing authority, privacy and cost limits remain unchanged.

E001-E0.1 established a small-model execution route, not an adequate model choice for all future research. E001-E0.2's interface study and the authentic HUMAN-GUIDED comparison remain open, unexecuted work; E002 neither replaces their definitions nor claims their results. E002 uses the current assistant's existing generated SQL as a historical artifact and asks a different question: when is retaining working code unsafe even if column names still fit?

## Objective

Determine whether a reusable quality-summary capability needs an explicit applicability contract when the meaning of 'current inspection' changes. Test whether a small adapter can preserve the historical SQL while refusing ambiguous evidence. Do not assume that more instructions, more model calls, more code or a particular model is the solution.

## Subject and evidence unit

Subject: the current interactive ChatGPT assistant's engineering activity and the artifacts it selects, adapts and tests. Runtime-facing model identity: GPT-6 Astra Pro; exact backend snapshot, inference token accounting and independent-session replay are unavailable in this interactive study. No API identity equivalence is asserted.

The historical artifact is REFERENCE_SQL['quality'] from benchmarks/e001_tasks.py at repository commit 902f10de6d0ca3571b36aa726d8714b55b7e0aaf. It was assistant-authored fixture code, NOT a capability learned by the Qwen subject; E0.1 generated zero capabilities. Its text must remain byte-identical.

This is an OPEN-LABEL, SINGLE-ASSISTANT DEVELOPMENTAL ENGINEERING CASE STUDY with deterministic artifact tests. The researcher also authors the generator and evaluator; procedural separation is not independent or blinded evaluation. Repeated data fixtures are NOT separate model decisions or AI participants. No BARE-GOAL/HUMAN-GUIDED effect, model ranking, human-time saving or autonomous-intelligence gain may be inferred.

## Common task contract

Produce per-lot total checked units, total failed units and six-decimal defect percentage from the current inspection facts. Duplicate transport rows count once. Numeric versions are local to each inspection, not global. Output order is irrelevant; missing and duplicate business rows matter. Zero checked units yields null percentage.

Contract LEGACY_V1: highest numeric version per inspection is current.

Contract EFFECTIVE_V2: only approved rows effective on or before as_of_day are eligible. Select highest eligible version per inspection. A selected withdrawn row removes that inspection; an ineligible future/draft row does not remove its older eligible record. Identical duplicates are harmless. Conflicting facts at the selected version, missing/invalid counts, invalid flags, non-finite numbers or undeclared schema/authority semantics require explicit refusal, not an invented answer. Unresolved legacy conflicts are also refused by safe implementations.

A valid data result is status=COMPLETE plus exact expected rows. Ambiguous data requires status=BLOCKED with no business rows. Unsupported contracts may be DECLINED with no rows. Safe refusal is reported separately and is not completed-work throughput. No external approval or business action is permitted.

## Three SOFTWARE conditions, not three model arms

1. BLIND_REUSE: execute the historical SQL without interpreting new semantic metadata. This is an intentional stress control and may violate the new business contract.
2. CONTRACT_GATED_REUSE: validate original scope and data preconditions; use the exact SQL only on LEGACY_V1, otherwise decline. Tests the price of conservative scope restriction.
3. ADAPTED_REUSE: current assistant may implement one generic eligibility/conflict adapter, then call the exact historical SQL. No row-specific answers, case names or evaluator access in capability code.

All get the same case data, metadata, compute surface and authority. These policies are designed treatments, not evidence that the assistant spontaneously chooses one. Original SQL preservation versus complete rewrite is documented, but no rewrite-cost benefit is claimed without a measured cold-construction comparison.

## Staged execution and fixed evaluation plan

A. Publish this protocol before running probes. Keep the historical query immutable.
B. Run one development fixture per scenario. Observe blind/gated outcomes; design the adapter without changing the contract. Log implementation failures. At most one bounded repair wave after an observed implementation failure; after a further failure retain partial results and replan rather than cycling until green.
C. Freeze capability and evaluator/source hashes in a GitHub commit BEFORE generating the main instance slice. New instance identifiers, quantities, record counts, versions, times and ordering are derived from a disclosed seed after the freeze. Scenario families are known to the author; these are post-freeze development instances, NOT sealed independent held-out evidence.
D. Fixed main slice: 8 scenarios x 12 instances = 96 case instances; evaluate all three software conditions = 288 deterministic invocations. Do not tune on this slice and call it fresh validation. If code changes afterward, retain the first result and identify a new run.

Scenarios: legacy-compatible heterogeneous versions; effective-policy with no invalid newer rows; newer unapproved rows; newer future-effective rows; withdrawn current records; same-version conflicting facts; missing selected counts; mixed valid changes across multiple lots. Include duplicate transport rows, unequal sample sizes and different latest version numbers. The independent Python oracle must not call capability code or reuse its normalization helper. Hand-derived oracle examples and negative/mutation controls must test the grader and demonstrate that global-MAX and average-percentage mistakes are detectable.

## Metrics and decision

Report per condition/scenario: correct COMPLETE outputs, incorrect COMPLETE outputs (silent errors), safe BLOCKED/DECLINED outcomes, incorrect refusals on resolvable cases, total contract-conformant handling, exceptions and input mutation. Report artifact execution wall time as local software timing only, not total research time or model latency. Record code hashes, query hash, suite/input/output commitments and actual invocation counts. No zero substitution for unmeasured human time, inference tokens or total compute cost.

Promotion candidate requires zero silent errors, correct completion of all resolvable fixed-slice cases, correct blocking of ambiguous cases, immutable source inputs and retained baseline SQL. A pass supports only the tested contract and generated distribution; it does not certify arbitrary data, concurrency, authority authenticity, permissions, mixed units, arbitrary future schemas or operational deployment. Failure of any required condition remains visible.

## Sources and preservation

Methodological background, not evidence for our result: OpenAI Evaluation best practices, https://developers.openai.com/api/docs/guides/evaluation-best-practices (accessed 2026-09-13), separates objective, data, metrics, comparison and continued evaluation. Study-specific design and hypotheses are our own.

Only synthetic data, code, observations and evidence commitments are public. No private reasoning, account secrets, real participant identities or company/customer material. No paid model service, unattended loop, permission expansion or production promotion. Preserve E001 artifacts and historical results. End with a verified checkpoint, limits and the next highest-value uncertainty.
