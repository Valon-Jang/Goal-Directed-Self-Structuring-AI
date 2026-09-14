# GDSSA laboratory — current entry point

Owner: Valon-Jang. Research workspace: Goal-Directed-Self-Structuring-AI. Updated: 2026-09-13.

## Scope amendment authorized by the owner

Research is NOT restricted to Qwen, open-weight models, small models, a specific company, model-only prompts or the current architecture. The current assistant itself, its actual decisions/tool use, produced artifacts and persistent operating structures may be studied. Choose the research question first, then an adequate subject and execution surface. Cheap CPU Qwen remains a valid instrument for appropriate questions, not a mandatory default. Do not claim models or tools are available until actually verified.

Self-study must remain honestly labelled: the researcher is not an independent evaluator of itself, same-conversation roles are not separate blinded model sessions, and deterministic tests of an assistant-authored artifact are not repeated model trials. Preserve these distinctions while continuing useful research. Goals and authorization remain human-governed; permissions and budgets are not enlarged by this scope amendment.

## Current evidence

- E001 E0: 36 original instrumentation tests; no model comparison.
- E001 E0.1: 15 completed actual Qwen3-0.6B calls, 3 developmental task episodes, 0/3 accepted. See evidence/E001/E01_RESULT.json and experiments/E001/E01_FINDINGS.md.
- E002: current-assistant open-label artifact transfer study; 96 post-freeze case instances x 3 SOFTWARE conditions = 288 invocations. Adapted reuse: 72 correct completed outputs, 24 correct ambiguity blocks, zero silent errors. All 95 regression tests passed. See evidence/E002/RESULT.json and FINDINGS.md. Main source frozen at 5fd5052b7aa30cc979775d78d5f994734f4fbbca; remote run 34758574472.

Never compare E001's 0/3 model episodes with E002's 72/72 resolvable artifact instances as a model ranking or intelligence gain. E002's same-seed local replay is a reproducibility check, not another independent study.

## Active research route

Branch: research/e002-assistant-transfer-v01, built on the E001 research branch. The original theory and E001 code/results are preserved. Main is not automatically promoted. RESEARCH_CHARTER.md supplies the north star; this index supersedes its historical E0.1-only next-action paragraph, not its safety/evidence rules.

Current next candidate: E003 intervention-selection study — can the assistant determine whether to reuse, minimally adapt, replace or ask for missing authority from the goal and evidence, rather than being assigned the correct method? Read evidence/E002/FINDINGS.md before designing the task/evaluator separation. This next study is PLANNED, not executed.

Still pending independently: E001-E0.2's 24 diagnostic model trajectories; authentic human method provenance and whole-human-time collection; the 216-trajectory primary BARE-GOAL/HUMAN-GUIDED pilot. No completed result may be inferred for those lanes.

## Execution

Researcher workflow: retrieve current evidence -> pick one consequential uncertainty -> freeze a fair bounded test -> execute within real capabilities -> preserve negative results and limitations -> update this entry point. No unattended loop or scheduled work has been installed. No extra user testing should be requested when the available tools can resolve the question directly.

The public repository contains generic code and synthetic evidence only. A persistent original evidence ZIP is kept in the owner's project Drive with a verified checksum; private routing is not published. No private repository, customer, company or credential data is eligible for public copy.

Before repeating connector operations, consult docs/OPERATIONAL_NOTES.md for exact failures and supported alternatives. Before applying any artifact in operational work, verify its declared scope and current evidence; research PASS is not production deployment approval.
