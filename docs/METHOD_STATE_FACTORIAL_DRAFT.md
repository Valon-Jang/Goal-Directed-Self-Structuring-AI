# Method guidance x maintained state — prospective design candidate

Date: 2026-09-13. Status: **DRAFT / NOT FROZEN / NOT EXECUTED**. This document does not modify E001's treatments, estimands, thresholds, run counts or current instrumentation sequence. It is not a completed preregistration.

Canonical shared argument: [Where structure belongs](https://github.com/Valon-Jang/Root-Engineering/blob/main/docs/STRUCTURE_ALLOCATION_ARGUMENT.md).

Governing documents: [Continuing research charter](../RESEARCH_CHARTER.md) and [E001 protocol](../experiments/E001/PROTOCOL.md). The objective remains a useful conditional delegation policy, not a predetermined BARE victory or a statistically significant interaction at any cost.

## 1. Question and scope

Does agent-maintained, source-backed current state improve accepted task outcomes and total workload differently when initial method design is delegated to the AI versus supplied by a human?

This is separate from the stronger hypothesis that model capability changes the optimal amount of guidance/state. A single-model factorial cannot identify that capability derivative.

Use synthetic procurement / part-qualification episodes inspired by Atlas: configuration scope, quote fields with partial supersession, validation readiness, customer authority, temporary permissions, lot restrictions and expiry. This is domain-specific synthetic research, not a real customer validation project. Do not publish actual company data.

Atlas is an existing developmental example, not a fresh holdout. Its Native arm used native project memory, so it cannot be relabeled the no-maintained-state cell of this design. Existing Qwen interface studies and GDSSA single-arm instrumentation runs also cannot retrospectively fill the cells.

## 2. Define the treatments before using the matrix

| Maintained derived state | AI chooses initial method | Human-authored advisory initial method |
|---|---|---|
| No maintained canonical Root | A | B |
| Maintained source-backed Root with selective retrieval | C | D |

'No maintained Root' does **not** mean no facts, no source documents or arbitrary amnesia. All arms receive the same goal contract, chronological updates, raw source archive, transcript-access policy, ordinary tools, permissions and context limits. A/B reconstruct from the common sources without a maintained derived current-state representation. C/D may maintain that representation and retrieve it selectively, while retaining access to the same originals.

Host-native or cross-chat memory must be disabled or equivalently controlled and documented in every cell. If this cannot be verified, name and report the actual baseline instead of claiming a clean absence-of-state intervention.

The S intervention is a specified system policy involving maintenance and retrieval, not merely a disk-location change. Its write/update costs are part of the treatment. If multiple implementation details differ, estimate the package effect and use a later mechanism ablation before attributing it solely to selective retrieval.

### Guidance is not continuing human memory

Follow E001: a genuine HUMAN-GUIDED initial method is independently human-authored, reviewed for competence and fact parity, and advisory. Both columns retain identical adaptation freedom. A static plan does not continuously supply missing facts or memory. Do not justify the predicted interaction by assuming that it does.

Any ongoing human coaching or state repair is a separate intervention. Ordinary factual responses and required approvals use the same policy in all cells and their actual active time is counted.

An AI-authored guide may support a separately named `AI-PROCEDURAL-PROXY` instrument study. It is not HUMAN-GUIDED, even if AI is asked to imitate an expert. Missing human participation is a gate for the human-method claim, not a reason to fabricate provenance or stop all instrumentation research.

### State construction must not hide superior expertise

Use the same evaluated model for agent-created state, with a declared state schema/interface and matched tool documentation. Do not give C/D a manually curated gold state or hidden authority oracle. Any common interface instructions are supplied to all arms; arm-specific maintenance instructions are logged as part of the state package.

Include state setup, schema preparation, update attempts, repairs, validation and reads in the cost ledger. Independently created state artifacts are isolated per trajectory; no cell reads another cell's state, decisions or responses. Exact source values must remain accessible, but access to sources is not proof that the model selected the authoritative ones.

## 3. Outcomes and estimands

Primary outcome: accepted end-to-end task rate under the same semantic, evidence and authority criteria. Report paired differences in total active human labor and machine use across **all assigned trajectories**, with failures and their costs retained. Do not compare only the successful survivors. Promotion remains subject to declared outcome quality and authority requirements.

Record semantic correctness, source coverage, source applicability, source-value fidelity, output format and effect authorization separately. A correct deterministic solver result based on an obsolete or inapplicable source is an end-to-end failure. A schema failure is not automatically evidence that the underlying semantic choice was wrong.

For a prespecified higher-is-better outcome scale:

```text
state effect without guide = C - A
state effect with guide    = D - B
proposed contrast I        = (C - A) - (D - B)
```

I > 0 is the proposed stronger hypothesis: state helps more without initial guidance. With guide=1 coding, this is a negative conventional state-by-guide interaction. It describes partial substitution on this scale, not automatically statistical complementarity.

I=0 does not imply no state benefit. For example, illustrative rates A=.60, B=.65, C=.80, D=.85 give equal +.20 state benefits and zero interaction. A reverse interaction is also plausible if guidance improves how state is used. The argument must survive accurate reporting of main effects, reverse effects and uncertainty rather than requiring one preferred sign.

Interactions depend on scale. Predeclare accepted-rate difference as the pilot's primary outcome contrast and treat logit/relative-scale alternatives as sensitivity analyses, not opportunities to select a favorable result. Costs use their own lower-is-better scale and are not silently combined with acceptance into a score.

## 4. Outcome observation and failure handling

Reuse E001's existing observability design instead of adding a new named framework. Each episode needs an outcome contract with:

- target output/effect, applicable scope and observation time;
- authoritative source/version/field rules and required evidence coverage;
- frozen independent evaluator or declared independent review rubric;
- acceptance criteria, explicit uncertainty statuses and action permissions.

Use hidden deterministic gold for these synthetic tasks, generated and checked independently of the evaluated agent. The worker cannot read the evaluator, gold state, answer keys or competing transcripts. A final response must identify supported current facts, justified decisions and unresolved conflicts rather than obtaining credit for a plausible explanation.

Test the evaluator with deliberate wrong source, wrong scope, stale value, invented/omitted record, unsupported approval and false-completion mutations. Submission receipt is not acceptance feedback. Do not reveal hidden answers through an unbounded iterative grading oracle.

Absent or delayed outcome evidence means UNVERIFIED or BLOCKED, not success. Safe reversible evidence gathering may continue within existing authority. Unsupported consequential action remains prohibited. Real deployments without a deterministic oracle require independent outcome observation and disclosed uncertainty; fixture scores cannot substitute for that evidence.

## 5. Task construction and isolation

Build new semantic variants after development: change which fields are superseded, whether newer rows are applicable, delegated authority scope, future-effective approvals, evidence readiness and interactions among these conditions. Shuffling row order or identifiers alone is insufficient novelty.

Balance cases where the older source remains authoritative with cases where a newer correction genuinely supersedes it. Include cases with no conflict, resolvable conflict and unresolved conflict. Include negative transfer from stale retained decisions and cases where no structured state is worth maintaining.

The whole source/update/query episode is the unit of task independence. Repeated seeds and multiple questions within one episode are dependent measurements, not new task families. Use independent environments and conversations for every cell/repetition. Counterbalance/randomize arm order and block on task family and human guide author where applicable.

Publish developmental fixtures as developmental. Freeze prompts, interfaces, model/backend identity, budget ceilings, state policy, scoring and analysis before obtaining a new evaluation slice. Keep held-out payloads and keys outside the agent-visible repository. Once evaluation feedback informs a change, retire that slice from future holdout status.

## 6. Costs and break-even

Count common goal preparation separately, human method preparation, state preparation/maintenance, human factual responses, review, approval, repair and final acceptance. Distinguish active human time from model waiting and total wall time. Missing times remain null.

Machine accounting includes input/output/cached tokens where observable, all failed attempts, tool/runtime use, state writes/reads and deterministic zero-model outcomes. Do not label a zero-model case a successful reasoning call.

Report first-use and recurring-use results separately. The Atlas calculation `Root-Native=109.5U-158.5Q` describes only its observed UI thinking-time proxy under a stationary-mean extrapolation. Its Q/U threshold is not this study's business break-even or a predetermined success target.

Estimate a task-cluster quality/labor/cost frontier. A fixed pilot of a few tasks cannot establish a narrow noninferiority margin or a robust interaction; use a separate pilot for variance and practical-effect sizing, then freeze a confirmatory plan before new data. Do not repeatedly extend a sample until the desired interaction appears.

## 7. Mechanism and model follow-ups

A mechanism study may compare raw-history access, generated lossy-summary replacement and source-backed selective retrieval under the same method condition. This directly targets the historical HC ambiguity; it must not be called a retrospective explanation already proved by Exp3.

A cross-model study requires actual recorded backend/model identities, comparable tool/input contracts, measured base-task capability and enough non-ceiling tasks. Merely rerunning twelve familiar cases on a differently named frontier model does not isolate a capability slope. Family, training, serving, context limits and instruction-following are competing explanations. Separate fixed-task capability moderation from changes caused by deploying longer or more volatile tasks.

No new paid service/GPU or permission expansion is authorized by this draft. Continue the existing bounded instrument and source-applicability work under the charter; do not replace it simply to fill this matrix.

## 8. Readiness and execution status

Before freezing this candidate, resolve the state policy and enforceability of no-maintained-Root; establish source/fact parity; pass interface and evaluator negative tests; obtain real human method provenance where needed; record the exact accessible model/configuration; choose pilot size and stop limits; and verify complete labor/cost logging and isolation.

**Actual new factorial trajectories executed for this document: 0.** No model efficacy result is claimed. The draft does not relabel any existing trajectory, change E001, start a background job, or require the user to run commands.

Immediate useful action from the audit is documentary: make the common argument, evidence limitations and existing observability contract discoverable; preserve negative findings; then choose the next bounded experiment by the current weakest evidenced boundary.
