# E001 — BARE-GOAL vs HUMAN-GUIDED

Version: 0.1-design, 2026-09-13. Status: PROTOCOL + EXPERIMENT-0 IMPLEMENTATION; NOT AN EFFICACY RESULT.

`ARE-GOAL` in the initiating request is treated as an alias of the repository's existing `BARE-GOAL`, not a new acronym. This experiment is about responsibility for method design, not model training or the separate Qwen reasoning-guide study. The research objective and this protocol were designed by the AI at the user's request. That does not make an AI-authored treatment plan a human-authored plan.

## 1. Research objective

Determine the task conditions under which assigning initial method design to AI preserves acceptable outcomes while reducing the human work required to obtain, review, repair and reuse those outcomes. Produce a delegation policy, not a claim that goal-only always wins.

The first operational target is a low-risk, observable, synthetic recurring operations workflow: produce accurate current-state exception lists, reconciled quality summaries and approval queues. No actual customer records, external messages, purchases or production changes are involved.

Deliverables: a falsifiable protocol; a runnable controlled environment; traceable measurements; a negative/null-results record; and evidence sufficient to decide the next experiment. A file count, attractive architecture, or generated report is not business success.

## 2. Primary estimand and decision thresholds

Primary estimand: the paired difference in total active human labor between the two initial-method assignments, subject to acceptable task outcomes. Estimate on an intention-to-treat basis. All failed runs remain in the denominator and their costs remain in the numerator.

Proposed decision thresholds, selected before model trials and NOT empirical findings:

- Outcome noninferiority: lower 95% confidence bound for BARE minus GUIDED accepted-task rate above -5 percentage points.
- Human labor: at least 30% lower mean total active human minutes, with uncertainty reported; a promotion claim additionally requires a confidence interval excluding no improvement.
- Safety: no unauthorized side effects or acceptance of unsupported critical human-only facts. A single observed violation blocks promotion; zero observed violations is not a safety guarantee.
- Cost: report machine-only and human-inclusive costs separately. A cost ratio above 1.25 is an investigation trigger, not a hidden weighted penalty. A promotion recommendation requires a stated labor-rate scenario under which total cost does not increase.
- Reuse: measure benefit on related task B relative to a cold-start B in the SAME arm, and include A's capability-development cost. A capability file by itself earns no reuse credit.

These thresholds are decision preferences. A 12-task pilot cannot reliably establish narrow noninferiority margins or general business ROI. The pilot estimates variance and failure types. A confirmatory sample size and immutable analysis plan must be set from a separate pilot before collecting confirmatory data. No post-hoc threshold adjustment is allowed.

Do not combine success, minutes, dollars, question counts and safety into an uncalibrated single score. Report the outcome/labor/cost frontier and conditional recommendations: delegate; supply factual context; supply human method; or retain human execution/approval.

## 3. Treatment definition

### Common to both arms

Exactly the same goal contract, task data, observable evidence, action interface, permissions, model snapshot, inference settings, resource ceilings, human-fact service, evaluator and initial capability registry. Model context begins fresh on each run. The model cannot read evaluator code, answer keys, the other arm's transcript, research notes or developer fixtures. It has no host shell or network tool. Both arms may query, calculate, ask, submit and create/reuse a declarative SQL capability.

The common contract describes desired outputs, business rules, sources, boundaries and available tools. It must not prescribe decomposition, tool sequence, a reasoning architecture, or an implementation plan. Interface documentation is common infrastructure, not an arm-specific workflow.

### BARE-GOAL

Only the common contract and ordinary input sources are supplied. AI chooses the working method. No mandatory multi-agent design, reflection loop, planner, or capability creation is imposed.

### HUMAN-GUIDED

Same common material, plus an independently human-authored initial method plan. The plan may specify decomposition, tool suggestions, checks and implementation hints. It must not contain extra facts, answer keys, additional permissions or a superior starting codebase. Any legitimate extra fact discovered during plan review must enter BOTH arms before freezing.

In the primary experiment the human plan is advisory: both arms retain identical adaptation freedom. Record plan adherence and substantial departures, but do not penalize departure from a suggested method. Otherwise the comparison would partly measure enforced rigidity rather than human guidance. A strict-human-workflow condition is a separate future ablation, not silently mixed into this one.

Guide length is not padded or made artificially bad. Prompt-length and preparation overhead are part of the treatment cost. Do not give BARE a secretly richer scaffold to compensate. A neutral-length control can be a later diagnostic.

## 4. Human provenance and timing

A HUMAN-GUIDED plan needs a pseudonymous author identifier, relevant experience, a declaration that the method was written by that human without AI composition, an exact text hash, development-material hash, preparation active seconds and a timing method. Never fabricate these fields. An AI-generated plan is `AI-PROCEDURAL-PROXY`; a human-reviewed AI plan is `HUMAN-APPROVED-AI-PLAN`. Neither supports the primary human-method claim.

Guide authors see development examples and the common task-family contract, not held-out instances or their answers. Before freezing, a reviewer checks that the guide is competent and does not introduce private facts or changed goals. For the pilot a single documented author can be used, but inference is limited to that author. Confirmation should use multiple authors with task/author blocking; repeating one author's guide does not sample more humans.

Human-time ledger categories:

1. goal/context preparation (common setup, shown separately and allocated equally when applicable);
2. method preparation (treatment-specific, including discarded drafts);
3. factual responses and values/authority decisions;
4. operating/review/approval time;
5. diagnosis, repair and rework;
6. final acceptance review.

Use active start/pause/stop timing; waiting for a model is wall time, not active labor. The CLI's measured time-to-enter-a-response is explicitly `wall_response_seconds`, not automatically active time. Missing measurements are null, never zero. A human-fact oracle is scripted in Experiment 0 only; it supplies no measured human labor. Human labor and human-inclusive cost are not inferable from token counts or number of questions.

Report first-use setup and recurring use separately. Amortize setup over predeclared N=1, 10 and 100 uses, without presenting those hypothetical reuse counts as observed deployments. Researcher benchmark-development time is not operational treatment labor, but remains a separate disclosed cost category.

## 5. Benchmark scope

Three families in v0.1:

- `state`: reconcile versioned records; latest version is authoritative even when rows are out of order; cancelled/completed work is excluded; report overdue open work with source evidence.
- `quality`: reject duplicate/replaced inspection rows; use the current record and the correct denominator; report lot-level checked/failed quantities and defect rate.
- `approval`: identify unsigned, above-threshold requests for the currently responsible team; already-approved or already-sent records must not be acted on; the responsible team is a human-only fact that must not be guessed.

Each family has four synthetic variants: 12 development/test instances. Each can generate an independently changed B with different identifiers, amounts, dates, policy threshold and row order. These PUBLIC examples are development fixtures, NOT a held-out test set and NOT evidence that tasks represent all office work.

Pilot target AFTER gates: 12 fresh held-out A/B task pairs, three repetitions, two arms. Per A run evaluate B in warm and cold fresh contexts: 12 x 3 x 2 x (A + B-warm + B-cold) = 216 planned model trajectories. This is an initial measurement plan, not a claim that 216 runs have occurred. Three repetitions reduce stochastic noise, not increase independent task sample size from 12 to 36.

Generate held-out data only after prompts/guides/config/evaluator freeze. Store the held-out seed, task payloads and answer keys outside the model-visible repository/workspace, publish only their commitments until the study closes. Task-family generator publicity is disclosed; never call development fixtures contamination-free. Exact held-out data must not be accessible through the model tools.

## 6. Controlled execution

Unit: (task-pair, repetition, author/block, arm). Counterbalance arm order within task/repetition; randomize B-warm/B-cold order. Use independent inference conversations and environment instances. No cross-arm or cross-task raw transcript sharing. A common model version alias must be resolved to a recorded backend snapshot; record inference options and any provider fingerprint. Same alias alone is not proof of identical backend weights.

Freeze manifest includes model/backend identity, inference config, common-contract and guide hashes, input/evaluator/harness hashes, tool manifest, budget ceilings, seed policy and human-fact policy. The worker receives only task inputs and interface material. The research controller has evaluator access but is never the evaluated agent.

The v0.1 executable deliberately implements offline tooling and preflight gates first. Live inference integration must prove trace capture, backend identity, independent contexts and hard budgets before it can emit primary results. Missing runtime identity, unverified human provenance, unreviewed fact parity, or missing human timing produces BLOCKED, not a guessed score.

Budgets are equal upper bounds, not instructions to spend all resources. Include initialization, planning, queries, failures, reparsing, retries, generated capabilities and validation. Timeouts and exhausted budgets are failed trials with recorded censored time, not removed observations. Do not silently retry failed provider calls outside the ledger. Provider caching and concurrency must be equalized or reported.

## 7. Metrics and grader

Outcome: accepted iff exact normalized business output matches the oracle, required evidence is supported, and authority constraints are respected. Separately record semantic field correctness, format errors and policy violations. Output ordering is not significant; duplicate rows and invented/omitted rows are significant. Numeric tolerances are explicit, not judged by a language model's impression.

Questions: count events and label required human-only fact, retrievable-data question, method delegation, approval request, or redundant question. Lower is not always better. Correctly asking an essential question is successful uncertainty management; guessing the fact is an unsupported result even if the guess happens to match the answer key.

Rework: failed submissions, corrected artifacts, tool errors, model retries, human repair minutes and time to first acceptable outcome. Initial construction is not all rework. Preserve all attempts and report first-pass and eventual acceptance separately.

Cost: raw input/output/cached/reasoning tokens where supported; model-call count; tool/runtime charges; one-time capability-building cost; human labor. Unknown price or usage remains null. Cost per accepted task uses total costs of ALL runs divided by accepted tasks; if no successes, report undefined/infinite as appropriate, not zero. Subscription marginal cash and allocated capacity cost are different accounting views.

Wall time and active human time are distinct. Report medians and tail behavior as descriptive statistics without replacing paired inference with cherry-picked best runs.

The deterministic grader is authored before held-out model runs. Golden answers are independently calculated in Python; SQL reference queries are used only as test fixtures to validate the tooling. Wrong-result mutations must fail. The agent's `submit` action returns receipt only; it does not reveal the hidden expected answer or an unbounded grading oracle. Visible query errors may support repair; hidden evaluation occurs after the run.

## 8. Capability reuse experiment

A capsule contains name, purpose, parameterized read-only SQL, schema/assumption metadata and a content hash. The code is optional: neither arm is required to build one. Registry entries start CANDIDATE; saving a file does not mark it VERIFIED. A new B run receives only capsule artifacts, not A's answers, business facts or transcript. B-cold has no A artifacts. Both B variants can query, ask and build with the same remaining per-run limits.

Record capsule lineage, actual invocation, exact byte hash, parameters, accepted B outcome and cold/warm costs. Unchanged exact-hash successful execution is strict reuse. Edited code is adapted reuse and its editing cost counts; rebuilding without use of a prior capsule is not reuse. Report negative transfer when warm does worse. A changed B policy and identifiers test stale constants. Distinguish a documented SQL capability from a proven general reusable product.

Net value at observed transfer count k: B-cold cost minus B-warm cost, summed over transfers, minus capability setup cost. Also show counterfactual N scenarios clearly labelled. Do not claim compounded returns from a single B. Verified trust is scoped to tested schema/policy conditions, never permanent production certification.

## 9. Analysis and claim boundaries

Use paired task-cluster estimates: average repeated runs within each task/arm, then resample paired task clusters for uncertainty. Report family-stratified estimates and all exclusions declared before evaluation. With a single author, do not generalize across authors. For confirmation incorporate task and author dependence. Retain unsuccessful runs, mixed outcomes and missingness.

Possible outcomes: BARE matches quality with less human labor; GUIDED materially improves success; BARE is cheaper only after reuse; guidance helps weak-evidence tasks; no meaningful difference; inconclusive. Report them without rescuing a preferred story. Single-model results cannot establish model-capability crossover; synthetic SQL tasks cannot establish organization-wide transformation, arbitrary self-modification, or human job replacement.

Experiment 0 selftests establish only that controls, scoring, isolation and accounting behave as specified. A reference solver is not an AI participant; fixture success rates are not BARE/HUMAN performance. No primary model efficacy claim is permitted while real-model trajectories or measured human plans are absent.

## 10. Go/no-go sequence

E0: implement paired fixture controls, independent graders, input isolation, query boundaries, trace ledger, capability round-trip and negative tests. Execute and save exact software hashes and test output.

E1 readiness: receive genuine human-authored plan(s); pass fact-parity review; freeze a single accessible model/runtime identity and hard budgets; validate adapter in an isolated non-primary smoke test; establish active-human-time capture; seal held-out cases. No need to redefine the research objective at this stage.

E1 pilot: run the planned paired experiment, retain failures, analyze with task clusters, and record which boundaries explain wins/losses. E2 confirmation: preregister sample size and policy before new data. Later vary evidence quality and model capability independently; do not change both and attribute effects to one.

## Sources and lineage

Repository baseline (2026-09-13): README sections 11–13; docs/RESEARCH_SCOPE.md; experiments/README.md. This specification extends those hypotheses without replacing them with results.

External methodological context, checked 2026-09-13:

- Kapoor et al., *AI Agents That Matter*, https://arxiv.org/abs/2407.01502 — evaluate accuracy with cost, prevent holdout leakage, document reproducible comparisons.
- Wang et al., *How Do AI Agents Do Human Work? Comparing AI and Human Workflows Across Diverse Occupations*, https://arxiv.org/abs/2510.22780 — workflow-level outcome differences motivate observation beyond speed. Not direct evidence for the present two-arm causal hypothesis.

These sources motivate measurement choices; they do not validate E001. No claim of academic priority is made.
