# E003 — Structural decisions and the limits of a curated test

2026-09-13. Executed source: 0baf08f99360e3af76f757faa2fe1364069c0560. Remote run 34760858279, job 103733323075. RESULT.json contains the verified summary; the full 16-file evidence archive contains actual choices and observed outputs, not only hashes.

## Structural judgment before execution

The proposed reuse/adapt/replace/ask menu mixed unlike decisions. Reuse, adaptation and replacement describe changes to a calculation. Reading and asking acquire evidence. Approval and dispatch govern side effects. A case can require reuse AND a question, or unchanged calculation AND a pending approval. We separated these descriptive axes without imposing a fixed reasoning loop or adding more agents.

A second correction: a valid existing outcome can already satisfy the goal. Merely invoking more tools is not progress. When only the source data changed, rerunning a compatible calculation can be sufficient; rebuilding its code is a different and potentially unnecessary intervention.

These are design deductions, not claims of academic novelty or empirical proof that this decomposition is universally best.

## Actual subject choices and execution

The current assistant inspected twelve synthetic cases and recorded twelve explicit initial choices. One case selected an indexed authority document; its read returned the approved equal-inspection weighting rule. A separate commit fixed that case's final calculation choice while preserving the other eleven. Numerical execution/evaluation followed the commits. The environment replayed the selected operation and did not choose or repair a solution using case labels.

Result: ten fully completed goals; one correct request for an absent metric definition; one correctly prepared report with dispatch approval pending. Eleven correct reports existed because the approval-pending case had completed its calculation. No wrong report, unauthorized dispatch attempt, unhandled execution error or source mutation was observed. One current result was reused without recalculation. One permitted dispatch produced an in-memory simulated receipt; no external message was sent.

All 111 software-control tests passed: 95 inherited and 16 new. These are not 111 subject decisions. Original E002 capability bytes remained unchanged, SHA-256 c805556842624ee18b306ae8561a559777f1cea401524118cc277cde19dd645e.

## Six contrasted boundaries

| Boundary | First case | Contrasting case | Observed choice/outcome |
|---|---|---|---|
| Presentation | Ordinary metadata | Changed title/theme/display version | Reused pooled calculation in both; 4.040404% in both |
| Metric meaning | Pooled failed/checked | Equal mean per inspection, same columns | Reused pooling vs replaced aggregation while retaining selection; 5.434783% vs 25.595238% |
| Unit conversion | Factor 4 for every record | Factors 4 and 20 across records | Reused ratio unchanged vs normalized inputs and reused pooling; 5.154639% vs 2.022472% |
| Missing definition | Indexed approved document exists | No authority source available | Read document and calculated 17.142857% vs requested metric_definition without inventing output |
| Existing outcome | Current source/policy fingerprints | Older source fingerprint | Reused approved output vs reran existing calculation; both current answers 1.785714% |
| Action authority | Dispatch not authorized | Dispatch explicitly authorized | Same 2.884615% report; requested approval vs simulated receipt |

This illustrates why neither surface similarity nor the mere presence of a change is a sufficient intervention rule. A display version can change without a mathematical change; columns can stay identical while the metric changes substantially. Reuse may happen at several levels: the final result, the entire calculation, the current-record selector, or the core aggregation after input normalization.

## A more precise unit-invariance deduction

Let n_i>0 be checked counts, f_i failed counts, s_i>0 a common conversion factor applied to both counts within record i, r_i=f_i/n_i, and p_i=n_i/sum(n_i). For a pooled FRACTION (multiply by 100 for a percentage):

R_raw = E_p[r], and R_converted = E_p[s*r]/E_p[s].

Therefore R_converted - R_raw = Cov_p(s,r)/E_p[s].

A common scale factor across records is sufficient for invariance, but not necessary: covariance can also be zero with different factors. Thus do not turn the two unit examples into a blanket 'mixed units always change the answer' rule. More importantly, preserving a percentage does not preserve requested absolute counts. The selected invariance must match the actual goal outputs. This identity is elementary algebra, not a newly discovered general theorem or an empirically established universal agent policy.

## Structural implication, with scope

A useful candidate is to revalidate the part of a dependency chain affected by changed evidence, rather than choosing between 'keep everything' and 'rebuild everything'. In these cases, the affected part was sometimes input normalization, sometimes aggregation meaning, sometimes the result's source binding, and sometimes only dispatch authority. The smallest justified change is not necessarily the fewest lines, cheapest unmeasured action, or always an input adapter.

The current observation supports feasible behavior on these curated examples. It does NOT establish that an autonomous system discovers the right dependency chain, chooses the cost-optimal intervention, or reduces human labor in real workflows.

## Critique of this experiment itself

E003 is still too helpful to the subject to demonstrate general structural judgment. The input explicitly declares POOLED versus EQUAL_INSPECTION_MEAN, supplies truthful unit factors and permission flags, and directly indexes the relevant authority document. The same assistant designed those distinctions, wrote the evaluator, and knew the paired-case mechanism. The provided execution primitives already cover the intended operations. Registering and freezing before outcomes reduces retrospective editing; it does not eliminate common-author bias, known-case contamination or menu assistance.

The assistant is a real interactive decision maker here, unlike E002's assigned software policies, but there are no fresh independent model sessions. Twelve decisions in one conversation are dependent observations. Do not publish 'structural intelligence 100%' or compare the result with the earlier small-Qwen smoke. Numerical wall times cover deterministic artifact execution, not assistant reasoning or the whole workflow. Human review time remains unmeasured.

The executor and oracle are sufficient for the fixed valid-input slice; they are not hardened general validators. Conflicting document precedence, invalid metric-source metadata, zero-denominator business policy, large/hostile inputs and forged authority are outside this slice. A truthful 'approved' flag is not cryptographic authentication. No production capability promotion is warranted.

## Evidence and preservation

Remote completion status and full decoded job logs were read. Downloaded ZIP: 26,064 bytes, SHA-256 c1ad75a30866f3f4ba8435a760764af9e81889a1312437c83b4dacd3d6887297. All manifested archive files matched. Local source equality and same-choice/same-input replay reproduced stable record SHA-256 0a8b44c1b3a7e1a7b72db63c5d83a25d4df90cccfc640eb6c56f346544aab854 on a different Python/SQLite version. Replay is not new independent evidence. The owner-project Drive copy was re-fetched and byte-compared; its private routing is kept outside this public repository.

## Next priority — E004 evidence discovery, not more easy repetitions

Planned, not executed: test whether the assistant identifies the relevant relationship from ordinary evidence rather than receiving semantic answer labels. Preserve the same goal, information content, tools and permissions while comparing a normalized evidence representation with a distributed document representation. Do not secretly remove facts from only one condition. Include old and current rules, irrelevant document changes, compatible pre-existing outputs, units whose common scaling preserves the requested ratio, and one case that genuinely needs unavailable authority.

Commit the assistant's chosen evidence acquisition before retrieval, then the selected intervention before outcome evaluation. Track unsupported assumptions, necessary versus redundant evidence reads, correct completion, legitimate pending states and changed dependency components. Do not require an elaborate planner or one preferred algorithm. An independent challenge author and separated fresh contexts are needed before making comparative reliability claims; absent that, keep the next cycle explicitly developmental.

The original E001 human-method comparison and its timing/provenance requirements are still pending. E003 is not a substitute for that research question. The next research milestone is less pre-arranged evidence structure, not a larger count of successful unit tests.
