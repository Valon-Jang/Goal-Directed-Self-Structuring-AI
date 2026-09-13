"""E001 measurement primitives. No provider credentials or model method scaffold.

Timers measure only explicitly recorded human activity. Deterministic tests do
not count as human participants. The ledger is single-controller, append-only;
a crash with an open call blocks automatic replay. Bootstrap CIs describe paired
task clusters, not a confirmatory decision or many independent repeated trials.
"""
from __future__ import annotations
import copy
import hashlib
import json
import math
import os
import random
import time
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def extract_action(text: str, allowed: set[str]) -> dict:
    """Accept one top-level canonical action, possibly fenced or prefixed.

    Skip parsed nested content as a unit: never execute an action inside a data
    envelope or list. Reject multiple objects even when identical. Tool argument
    semantics are enforced by Environment, not inferred by this parser.
    """
    if not isinstance(text, str) or len(text) > 64000:
        raise ValueError('INVALID_ACTION_TEXT')
    decoder = json.JSONDecoder(object_pairs_hook=_pairs,
                               parse_constant=lambda _: (_ for _ in ()).throw(ValueError('NONFINITE_JSON')))
    i, objects = 0, []
    while i < len(text):
        if text[i] not in '{[':
            i += 1
            continue
        try:
            obj, end = decoder.raw_decode(text, i)
        except json.JSONDecodeError:
            # Never scavenge a nested action out of a malformed outer object.
            raise ValueError('MALFORMED_JSON_CONTAINER')
        if not isinstance(obj, dict) or set(obj) != {'tool', 'args'}:
            raise ValueError('NONCANONICAL_ACTION_CONTAINER')
        if not isinstance(obj['tool'], str) or obj['tool'] not in allowed or not isinstance(obj['args'], dict):
            raise ValueError('INVALID_ACTION_SCHEMA')
        objects.append(obj)
        i = end
    if len(objects) != 1:
        raise ValueError('ACTION_AMBIGUOUS' if objects else 'ACTION_NOT_FOUND')
    return objects[0]


CATEGORIES = {'goal_context', 'method_preparation', 'human_fact_response',
              'operation_review', 'repair', 'final_acceptance'}


def human_active_summary(events: list[dict], required_categories: set[str]) -> dict:
    """Events use monotonic seconds in one timer_session per uninterrupted clock.

    A category with no work needs a measured_zero event, not omission. Overlapping
    activity for one person is rejected, preventing double counting. Waiting is
    recorded by paused intervals. A missing stop yields null, not estimated time.
    """
    totals, covered, active, previous = defaultdict(float), set(), {}, {}
    for e in events:
        key = (e['person'], e['timer_session'])
        category, op, now = e['category'], e['event'], e['monotonic_seconds']
        if category not in CATEGORIES or not isinstance(now, (int, float)) or isinstance(now, bool) or not math.isfinite(now) or now < 0:
            raise ValueError('INVALID_TIMER_EVENT')
        if key in previous and now < previous[key]:
            raise ValueError('NONMONOTONIC_TIMER')
        previous[key] = now
        if op == 'start':
            if key in active:
                raise ValueError('OVERLAPPING_HUMAN_ACTIVITY')
            active[key] = (category, now)
        elif op in {'pause', 'stop'}:
            if key not in active or active[key][0] != category:
                raise ValueError('TIMER_NOT_RUNNING')
            _, began = active.pop(key)
            totals[category] += now - began
            covered.add(category)
        elif op == 'measured_zero':
            if key in active:
                raise ValueError('TIMER_IS_RUNNING')
            covered.add(category)
        else:
            raise ValueError('UNKNOWN_TIMER_OPERATION')
    missing = sorted(required_categories - covered)
    complete = not active and not missing
    return {'complete': complete, 'active_seconds': sum(totals.values()) if complete else None,
            'by_category_seconds': dict(totals), 'missing_categories': missing,
            'open_intervals': len(active), 'timer_method': 'active_start_pause_stop'}


class Ledger:
    """Single-writer durable JSONL with a hash chain; NOT tamper-proof storage."""
    def __init__(self, path: str | Path, manifest_sha256: str):
        if len(manifest_sha256) != 64 or any(c not in '0123456789abcdef' for c in manifest_sha256):
            raise ValueError('INVALID_MANIFEST_HASH')
        self.path, self.manifest = Path(path), manifest_sha256
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.rows = []
        if self.path.exists():
            for line in self.path.read_text(encoding='utf-8').splitlines():
                row = json.loads(line)
                check = dict(row)
                stored = check.pop('sha256')
                prior = self.rows[-1]['sha256'] if self.rows else '0' * 64
                if stored != sha(check) or row['previous'] != prior or row['manifest'] != self.manifest:
                    raise ValueError('LEDGER_INTEGRITY_OR_MANIFEST_MISMATCH')
                self.rows.append(row)

    def append(self, event: str, **data) -> dict:
        entry = {'event': event, 'manifest': self.manifest,
                 'sequence': len(self.rows), 'previous': self.rows[-1]['sha256'] if self.rows else '0' * 64,
                 'data': copy.deepcopy(data)}
        entry['sha256'] = sha(entry)
        with self.path.open('a', encoding='utf-8') as file:
            file.write(canonical(entry) + '\n')
            file.flush()
            os.fsync(file.fileno())
        self.rows.append(entry)
        return entry

    def begin(self, call_id: str, payload_sha256: str):
        events = [r for r in self.rows if r['data'].get('call_id') == call_id]
        if events:
            raise ValueError('CALL_ALREADY_EXISTS_DO_NOT_REPLAY')
        self.append('CALL_STARTED', call_id=call_id, payload_sha256=payload_sha256)

    def end(self, call_id: str, status: str, **data):
        matching = [r for r in self.rows if r['data'].get('call_id') == call_id]
        if len(matching) != 1 or matching[0]['event'] != 'CALL_STARTED':
            raise ValueError('CALL_NOT_OPEN')
        if status not in {'COMPLETED', 'FAILED', 'TIMEOUT'}:
            raise ValueError('INVALID_CALL_STATUS')
        self.append('CALL_' + status, call_id=call_id, **data)

    def unresolved(self) -> list[str]:
        started = {r['data']['call_id'] for r in self.rows if r['event'] == 'CALL_STARTED'}
        ended = {r['data']['call_id'] for r in self.rows if r['event'] in {'CALL_COMPLETED', 'CALL_FAILED', 'CALL_TIMEOUT'}}
        return sorted(started - ended)


def schedule(task_ids: list[str], repeats: int, seed: int) -> list[dict]:
    if not task_ids or len(set(task_ids)) != len(task_ids) or repeats < 1:
        raise ValueError('INVALID_SCHEDULE_INPUT')
    rng, out = random.Random(seed), []
    blocks = [(task, rep) for task in task_ids for rep in range(repeats)]
    rng.shuffle(blocks)
    first = [i % 2 for i in range(len(blocks))]
    rng.shuffle(first)
    warm_order = [i % 2 for i in range(len(blocks) * 2)]
    rng.shuffle(warm_order)
    for b, (task, rep) in enumerate(blocks):
        arms = ['BARE-GOAL', 'HUMAN-GUIDED']
        if first[b]:
            arms.reverse()
        for j, arm in enumerate(arms):
            phases = ['A', 'B-warm', 'B-cold']
            if warm_order[b*2+j]:
                phases = ['A', 'B-cold', 'B-warm']
            for phase in phases:
                out.append({'task_pair': task, 'repeat': rep, 'arm': arm, 'phase': phase,
                            'run_id': f'{task}/{rep}/{arm}/{phase}'})
    return out


def paired_cluster_estimate(rows: list[dict], metric: str, seed: int = 913,
                            resamples: int = 2000) -> dict:
    """Use rows for one phase and one author block; missing pairs invalidate CI."""
    groups = defaultdict(dict)
    signatures = set()
    for row in rows:
        signature = (row['task_pair'], row['repeat'], row['arm'])
        if signature in signatures:
            raise ValueError('DUPLICATE_TRIAL')
        signatures.add(signature)
        value = row.get(metric)
        if value is None or not isinstance(value, (float, int)) or not math.isfinite(value):
            return {'status': 'INCOMPLETE', 'estimate': None, 'ci95': None}
        groups[row['task_pair']].setdefault(row['arm'], {})[row['repeat']] = value
    deltas = []
    for arms in groups.values():
        if set(arms) != {'BARE-GOAL', 'HUMAN-GUIDED'} or arms['BARE-GOAL'].keys() != arms['HUMAN-GUIDED'].keys():
            return {'status': 'INCOMPLETE', 'estimate': None, 'ci95': None}
        deltas.append(mean(arms['BARE-GOAL'].values()) - mean(arms['HUMAN-GUIDED'].values()))
    if not deltas:
        return {'status': 'INCOMPLETE', 'estimate': None, 'ci95': None}
    ci = None
    if len(deltas) >= 2 and resamples >= 100:
        rng = random.Random(seed)
        boot = sorted(mean(rng.choices(deltas, k=len(deltas))) for _ in range(resamples))
        ci = [boot[int(.025*(resamples-1))], boot[int(.975*(resamples-1))]]
    return {'status': 'DESCRIPTIVE_PAIRED_TASK_CLUSTER', 'estimate': mean(deltas), 'ci95': ci,
            'independent_task_clusters': len(deltas), 'observed_rows': len(rows),
            'promotion_verdict': 'NOT_IMPLEMENTED_NO_AUTOMATIC_PROMOTION'}
