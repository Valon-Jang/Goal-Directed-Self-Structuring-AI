"""Post-hoc replay sensor, NOT an autonomous stopping policy or efficacy result.

An unchanged input fingerprint plus repeated *exact* read-only action/response
is a candidate no-progress signal. Timing fields are not business observations.
Changes in source, permission, capsule or other controller state must change
state_sha256. The caller must not use this heuristic to declare impossibility.
"""
from __future__ import annotations
import hashlib
import json

READ_ONLY = {'list_inputs', 'read', 'query', 'run_capability'}


def scan(trace: list[dict], state_sha256: str, threshold: int = 3) -> dict:
    if threshold < 2 or len(state_sha256) != 64:
        raise ValueError('Invalid threshold or state fingerprint')
    last, count = None, 0
    for index, event in enumerate(trace):
        action = event['action']
        if action.get('tool') not in READ_ONLY:
            last, count = None, 0
            continue
        state = event.get('state_sha256', state_sha256)
        payload = [state, action, event['response']]
        current = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
        count = count + 1 if current == last else 1
        last = current
        if count >= threshold:
            return {'candidate_detected': True, 'first_signal_after_tool_events': index + 1,
                    'remaining_baseline_tool_events': len(trace) - index - 1,
                    'observation_sha256': current, 'policy': 'OBSERVE_ONLY',
                    'evidence_class': 'POST_HOC_REPLAY', 'prospective_savings': None}
    return {'candidate_detected': False, 'first_signal_after_tool_events': None,
            'remaining_baseline_tool_events': 0, 'policy': 'OBSERVE_ONLY',
            'evidence_class': 'POST_HOC_REPLAY', 'prospective_savings': None}
