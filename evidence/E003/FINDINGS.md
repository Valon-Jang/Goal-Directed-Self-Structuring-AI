# E003 — Structural judgment: preserve sufficient information, not merely old code

Recorded 2026-09-13. Read RESULT.json for exact provenance and the recovered full evidence archive. Source fixed at 66e47a77245e82f49093d5106f8469b8018a92a7; GitHub run 34760340461 / job 103731958738. This is a current-assistant open-label development study, not a blinded model benchmark.

## What was actually studied

E002 assigned software policies to inputs. E003 instead recorded the current assistant's intervention choices before executing and grading them. Twelve synthetic vignettes were authored and committed by input/oracle hashes, the assistant wrote twelve case decisions, one synthetic document was read for a follow-up decision, and executable choices were fixed before the first output evaluation. Short justifications are public decision summaries, not private reasoning.

The separate oracle uses Fraction-based arithmetic and does not import the execution choices or E002 capability. However, the same assistant authored it and the tasks. This separation prevents certain code-coupling errors; it does not remove design exposure, prove evaluator independence or turn the cases into a held-out test.

## Observed outcomes

Ten business outputs were completed correctly. Two cases correctly remained pending an unavailable fact or unresolved authority; no actual human response was simulated or obtained. There were no observed incorrect completions, exceptions or input mutations on the fixed slice. The first local execution required no post-score repair. Hosted replay matched its deterministic output commitment.

| Case | Committed intervention | Measured result |
|---|---|---|
| SJ01 | Existing capability unchanged | Cosmetic report-title change did not trigger rebuilding. Correct pooled lot rates. |
| SJ02 | Existing capability unchanged | The capability already supported approved/effective records. No new eligibility algorithm was needed. |
| SJ03 | Input unit conversion | Known carton capacities gave 43 checked units and 6 failed units: 13.953488%. |
| SJ04 | Specific authority question | Missing carton capacity was not guessed. No business output. |
| SJ05 | Input field mapping | Explicit bijective column renaming preserved the original calculation. |
| SJ06 | Output conversion from retained counts | Exact counts produced 333333.333333 ppm for 1/3, rather than scaling a rounded percentage. |
| SJ07 | Replace aggregation only | Equal inspection weighting gave 20% for L1 instead of the pooled 26.666667%. Record selection was retained. |
| SJ08 | Replace aggregation using unit identity | Four defect events on two of eight inspected units gave 25%, not 50%. |
| SJ09 | Read listed source, then replace aggregation | The approved synthetic definition selected equal inspection weighting; no unnecessary human question was used. |
| SJ10 | Specific authority question | Equally authoritative conflicting metric definitions were left unresolved. No definition was invented. |
| SJ11 | Rebind existing supported policy | Current owner policy overrode an obsolete export-cache hint without rewriting the supported algorithm. |
| SJ12 | Existing capability unchanged | A valid zero denominator returned null, not an invented value or an unnecessary question. |

Final intervention footprint: 3 unchanged uses; 4 input/output/policy-binding adaptations; 3 aggregation replacements; 2 authority questions. The source lookup is an intermediate action in one of the replacement cases, not a thirteenth independent task. These counts describe the choices and do not measure their labor cost or prove global minimality.

All 111 hosted regression tests passed: 95 inherited and 16 new. Six deliberately wrong substitutions were rejected: scaling a rounded percentage for high-precision ppm, pooled for macro averaging, events for distinct units, obsolete policy binding, asking instead of using available documentation, and guessing carton capacity. These substitutions are sensitivity controls, not six additional actual assistant decisions.

## Structural conclusion from the implemented cases

The meaningful decision is not simply KEEP versus REBUILD. Identify what information the new goal needs and where that information still exists.

An output boundary can be enough when the existing result preserves the needed counts. An input boundary can be enough when an explicit field mapping or conversion preserves meaning. A changed metric may require returning before a lossy aggregation, while leaving unrelated selection and validation intact. If authorized available evidence cannot distinguish possibilities that require different answers, another computation cannot manufacture the missing fact.

The existing capability's coverage also matters: SJ02 needed a function already implemented in E002, not new code. A changed business rule does not always imply new development. Conversely, SJ11 shows that an implementation's stale contract label is not itself authoritative evidence of which business rule applies.

These are scoped design implications. The assistant did not establish an optimal intervention search algorithm, a universal routing policy, or general autonomous understanding of source authority.

## An exact boundary for output-only adaptation

For deterministic functions on an explicitly allowed input domain, let F(x) be the information retained by an old capability, and G(x) the uniquely required new answer. An output-only mapping H with G(x)=H(F(x)) can exist only if:

    F(x1) = F(x2) implies G(x1) = G(x2).

Necessity: one identical input to H cannot guarantee two distinct outputs. Sufficiency as a set-theoretic statement: when G is constant on each set of inputs sharing F's output, define H on that output as their common G value. This does not establish an efficient implementation, access rights, or lowest cost. If a task allows several acceptable answers, the corresponding condition is that every indistinguishable input group has at least one common acceptable output, not exact equality of one preferred answer.

A single verified violating pair is enough to disprove universal output-only sufficiency on that domain. Failure to find such a pair in a finite sample is not a proof of sufficiency. This is an elementary logical characterization applied to this design problem; no academic novelty or priority claim is made.

### Executed aggregation-loss witness

Two source datasets have the same old output: 100 checked, 10 failed, pooled rate 10%.

- Dataset A: one inspection has 0/10 failures; another has 10/90. The equally weighted mean of their rates is 5.555556%.
- Dataset B: two inspections each have 5/50 failures. Their equally weighted mean is 10%.

The pooled output is identical, but the requested new metric differs. No output-only correction of those same totals can guarantee both answers. The necessary information is still available upstream at inspection granularity, so that is where the calculation must change. Rebuilding the whole workflow is unnecessary; pretending the old aggregate is sufficient is incorrect.

### Executed identity-loss witness

Eight inspected units and four defect events may mean four events on two units (25% distinct defective units), or four events on four units (50%). The old event-count summary is identical. The unit identities resolve the new target; the summary alone does not.

### Precision and authority are different boundaries

For 1/3, the existing six-decimal percentage is 33.333333. Scaling it by 10000 yields 333333.33 ppm, missing the requested 333333.333333 ppm by 0.003333 ppm. Exact failed/checked counts were retained, so recomputing from those counts at the output boundary succeeds without replacing record selection or pooled counting.

For the missing-capacity case, 5 units/carton and 10 units/carton are both consistent with the supplied evidence but imply 4% and 2%. For the unresolved-definition case, the same rows imply 26.666667% pooled or 20% equally weighted for L1. These are hypothetical witness worlds, not newly discovered real facts or participant answers. Unlike the lossy-output examples, no provided authoritative source resolves them, so the selected questions remain necessary within the declared task.

Witnesses were developed after the main choice/output check. Their role is analytic falsification of specific reuse assumptions, not extra prospective model evidence.

## Evidence and limitations

The actual inputs, frozen source, choices, source observation, full expected and actual output payloads, witnesses and test results are recoverable in the original six-file Actions artifact. Its ZIP and reported member hashes were checked after download. The owner Drive copy was re-fetched and is byte-identical, so archival preservation is not limited to Actions' configured 90 days. Private Drive routing is deliberately not published here.

Important limits: one interactive context; self-authored task families; explicit goal/policy cues; same-author oracle and source document; no independent model reset or blind scoring; no authentic HUMAN-GUIDED control. The apparent completeness of the choices on twelve deliberately clear vignettes does not show how the assistant behaves when semantics are unstated, metadata is misleading, or sources are independently authored. No cross-model ranking, lower human labor, lower total cost, broad safety certification, or operational promotion follows.

The method of measuring choices before outcomes is now exercised. The remaining question is not whether to rerun more copies of these easy cases, but whether the same judgment survives weaker and contradictory evidence without either guessing or refusing everything.

## Next highest-value uncertainty — E004 candidate, not executed

Test authority and information sufficiency when high-level labels disagree with authorized evidence. Include two matched kinds of case: a harmless representation change that should not force replacement, and an identical-looking interface hiding a metric or unit change that does. Include missing facts resolvable by a listed source and genuinely unresolved equal-authority evidence. Require observable source selection and a committed output or specific question; score supported outcome validity and unnecessary intervention separately rather than rewarding a preferred route name.

Before attributing accuracy to the model, improve separation of case authorship and subject execution. Independently authored tasks and fresh subject contexts are preferred when an actual authorized surface is available; otherwise retain the open-label designation. Do not simulate independence by assigning researcher/subject role names inside one conversation. No E004 cases or outcomes have been collected here.

E001-E0.2's planned 24 model diagnostics and the authentic 216-trajectory BARE-GOAL/HUMAN-GUIDED pilot remain pending independently. E003 does not redefine or complete them.
