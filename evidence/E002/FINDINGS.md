# E002 findings — preserve a useful implementation, revalidate its assumptions

## What changed in research scope

The owner explicitly instructed that research is not Qwen-only and may study the current assistant. E002 therefore uses the current assistant as researcher/engineer and its selected and adapted artifacts as the directly measured objects. This is a different research lane from repeating calls to a small public model. Model choice follows the scientific question; availability of a cheap model does not define the question.

## Observed result

The preregistered 96 generated instances were created after code commit 5fd5052b7aa30cc979775d78d5f994734f4fbbca. GitHub run 34758574472 completed 288 software-condition invocations. All 95 regression tests passed, including 26 new E002 tests and preservation of the exact E001 historical quality SQL.

| Software condition | Correct data outputs | Incorrect data outputs | Correct ambiguity blocks | Resolvable tasks declined |
|---|---:|---:|---:|---:|
| BLIND_REUSE | 24 | 72 | 0 | 0 |
| CONTRACT_GATED_REUSE | 12 | 0 | 24 | 60 |
| ADAPTED_REUSE | 72 | 0 | 24 | 0 |

Each condition received the same 96 instances. Seventy-two were resolvable; twenty-four deliberately contained conflicting current evidence or missing counts. Thus ADAPTED_REUSE completed 72 tasks and correctly blocked 24; it did not complete 96 tasks. No condition mutated the supplied input object or raised an exception on this fixed slice.

BLIND_REUSE continued to execute valid SQL despite draft, future-effective, withdrawn, conflicting and missing-current-fact cases. A code-execution success signal alone could not distinguish those wrong outcomes. CONTRACT_GATED_REUSE avoided silent errors but gave up 60 resolvable new-policy cases. ADAPTED_REUSE projected approved/effective/non-withdrawn unambiguous current facts into the old calculation's input contract, preserving the original SQL text exactly.

## What the experiment supports

For these two declared contracts and this synthetic distribution, a separately tested eligibility/conflict adapter can extend reuse without rewriting the core aggregation. A conservative applicability gate alone has a measurable completion-coverage cost. Correct refusal must remain separate from completed work, and testing only exceptions would miss every blind-reuse failure in this suite.

Design implication, not a novelty claim: retain a capability together with its applicability assumptions and supporting evidence, rather than treating the existence of its code or past PASS as sufficient authority. A useful reuse choice is not merely KEEP versus REBUILD: REUSE_UNCHANGED, ADAPT_BOUNDARY, REBUILD and DECLINE need to be distinguishable. E002 does not establish that the current assistant can reliably select among these without explicit experimental treatment assignments.

## Limits and self-evaluation boundary

These are deterministic artifact tests, not 96 independent current-assistant solves or 288 model decisions. The current assistant authored the task families, oracle and adapter in the same interactive context. The historical query was prior assistant-authored reference SQL, not a learned Qwen capability. Its E001 source remains intact.

Scenario families were known during design; only concrete quantities, IDs, version distributions, dates and ordering were generated after freeze. This is not independent held-out evidence. The deliberately failure-rich mix cannot estimate natural workplace error incidence. The architecture's mechanism is being validated against its declared scope, not proved superior by a neutral population sample.

The adapter was anticipated and authored before the initial two-condition development probe. That chronology differs from a literal 'discover failure first, then invent adapter' narrative; DEVELOPMENT.json records it. No first main-slice failure was hidden and no post-slice solver repair was made.

Human involvement in this task consisted of the user's research direction; active time spent reading/reviewing these outputs was not measured. Do not turn absence of extra user messages into zero total human labor. Current-assistant inference tokens, full backend identity and total cost were not exposed. Sub-millisecond artifact timing is not an AI workflow speed claim.

## Evidence recovery

RESULT.json is a normalized verified summary. The original GitHub artifact has four files: actual generated input/oracle data, invocation results and commitments, source hashes and tests. The ZIP was downloaded and its SHA-256 and all four file hashes were checked against the job log. Running the same frozen code and seed locally on Python 3.13.5 / SQLite 3.46.1 reproduced the hosted Python 3.12.3 / SQLite 3.45.1 input-suite and deterministic-record commitments. This is a reproducibility check, not extra independent sample size.

A byte-identical owner Drive archive was also uploaded, re-fetched and SHA-256 verified, so preservation does not depend solely on the configured 90-day Actions artifact. Private archive routing is in the owner's project context, not this public repository. No sharing permissions were expanded.

## Next question — E003 candidate, not executed

Can an assistant discover the relevant assumptions and choose the smallest warranted intervention without the researcher already assigning the software condition? This is closer to the original GDSSA question than another 96 arithmetic fixtures.

Proposed decision task: give the assistant a goal, available capabilities and authoritative task evidence, but not a procedural treatment label. Require a committed choice among unchanged reuse, boundary adapter, replacement, or a specific missing-authority question. Include cases where an irrelevant metadata change should NOT trigger rebuilding; a hidden denominator/unit change DOES require a new treatment; and unresolved authority must not be guessed. Capture the chosen intervention and actual executed outcome separately. The evaluator must support more than one valid route when appropriate, rather than rewarding a preferred action label.

First small study candidate: 12 task vignettes across these boundaries. Record the assistant's actual policy choices and downstream artifacts. Interactive self-study remains open-label unless an independent execution surface and separated evaluator are verified. A later cross-model comparison must give each model the same data/tools/permissions and report backend identity. Do not use invented human-authored methods as a control.

E001-E0.2's Qwen interface-conformance study stays pending; authentic BARE-GOAL/HUMAN-GUIDED comparison stays pending. They are not silently redefined by E002, and no win against HUMAN-GUIDED has been established.
