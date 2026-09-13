# E0.1 — actual model transport works; task execution does not yet work

Recorded 2026-09-13. Source: completed GitHub Actions run 34756883943, job 103722672201, code commit 9d2eac8c9b9458418cef1eb98224629b6fb98cee. Read E01_RESULT.json and E01_OBSERVATIONS.json under evidence/E001 for normalized measurements and tool traces. Original full call ledger was hashed by the runner but is not archived here; do not claim byte-identical raw-ledger preservation.

## What was executed

A checksum-pinned public Qwen3-0.6B Q8_0 model ran in llama.cpp b10344 on CPU. Three fresh inference processes received the same existing BARE-GOAL interface on three public developmental task families. No human method was supplied. Each task had at most six calls, one neutral formatting recovery, a 60-second request limit and a 180-second process watchdog. A separate outer command and CI job bounded overall execution. This observed run did not exercise a hung-model timeout; that mechanism still needs an injected fault probe.

All 58 instrumentation tests passed before model acquisition. Fifteen actual inference requests returned fifteen responses; twelve passed the action-envelope parser, seven tool invocations returned success, five returned SQL errors. Three response-format failures occurred. No task was accepted: 0/3. There were no observed authority-denied attempts. Total measured tokens: 14,465 prompt + 520 completion = 14,985; cached tokens reported zero. There were no hosted model-inference API calls or charges; full CPU resource cost is unmeasured, not zero.

## Failure observations

**State:** queried nonexistent `your_table` five times, receiving `no such table` each time, and exhausted the six-call cap without an output. Schema names were available in the common input. This is observed non-recovery, not evidence that more iterations would cure it.

**Quality:** issued the same global-MAX-version query five times and kept receiving the same duplicated input rows. It never aggregated and submitted the required summary. Successful tool execution therefore did not imply goal progress. Its first query included the literal key `params?`; the adapter ignored this unknown key. That is a concrete interface-contract weakness, not proof of the cause of all failures.

**Approval:** listed input schema and then submitted empty arguments without producing a draft or asking for `responsible_team`. The receipt was SUBMITTED but the independent grader rejected it. Zero questions were not successful autonomy.

The precise causes of the three rejected response envelopes were not preserved in the terminal report; raw rejected text was hashed rather than retained. Do not invent their content or infer a root cause from counts alone.

## A problem found in the benchmark itself

The current quality generator gives every inspection the same final version number. It tests duplicates and replacement rows, but on this dimension a global MAX-version query and a per-inspection MAX query select the same latest-version number. A development variant with staggered final versions is necessary to discriminate that error. Further cases should vary meaning, not only shuffle rows. Preserve the current baseline instead of silently modifying it and reusing the old score.

## Immediate learning and bounded response

The next candidate is a no-progress sensor, not another mandatory chain of reasoning. `implementations/e001_stagnation.py` detects three consecutive exact read-only action/response pairs under an unchanged controller-state fingerprint. It is OBSERVE_ONLY and never declares task success or impossibility.

Post-hoc replay detected a signal after the third state tool event and fourth quality event; respectively two and one later baseline tool events remained. This is not measured runtime, token or monetary saving: an intervening policy could alter later model behavior. The approval failure requires a different signal and was not classified as stagnation. The threshold was selected after observing these failures, so this slice is development data and cannot validate a promotion claim.

## Next bounded experiment — E0.2 prospective plan

Highest-value uncertainty: is the new path feeding and interpreting tool contracts correctly enough to evaluate model behavior, and can its repetition/termination signals distinguish failure from legitimate information gathering?

First add a transport conformance suite: assert actual rendered prompt includes complete goal, all tool schemas and input table names; record a hash and safe diagnostic of rejected action envelopes without storing private reasoning; reject unknown arguments explicitly; exercise owned-process timeout and cleanup with a deliberately hanging test process. This is common infrastructure, not BARE-specific procedural guidance.

Next use new developmental cases with staggered per-record versions, changed policies and unique identifiers. Hold model, method freedom, tools, permissions and budgets fixed while comparing the current interface with an explicit JSON argument schema. Do not change model size, inference settings, schema and stopping policy in one comparison and attribute improvements to one factor. Six cases (two per family), two schema conditions, two seeds = 24 planned trajectories; this is a diagnostic design, not executed evidence. Do not run the unchanged 216-trajectory main pilot against the present floor-level behavior.

Keep the no-progress sensor observational in that comparison. A prospective stopping-policy test comes separately and must include tasks where repeated reads or changed source state legitimately matter. If a stronger model is tested, freeze the interface and vary only the model family/size as a separate diagnostic; choose the smallest actually adequate model after evidence, not before.

The human comparison continues on its own lane. Genuine human-written methods, measured preparation/review/repair time, scoped permissions and sealed evaluation inputs remain required. Current real-model calls do not satisfy any of those human-provenance requirements.

## Claim boundary

This establishes a working acquisition/inference/tool/measurement route and records specific failure modes on three public tiny-model tasks. It does not establish BARE-GOAL inferiority to HUMAN-GUIDED, frontier-model limitations, overall GDSSA impossibility, successful reuse, reduced human labor or business ROI. The research objective remains open to alternative architectures and future models.
