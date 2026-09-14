"""Open-label E002 controller; fixture executions are not model trials."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
import platform
import random
import statistics
import time
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from .capability import CONDITIONS, BASE_SQL

SCENARIOS = ('legacy', 'effective_plain', 'draft', 'future', 'withdrawn', 'conflict', 'missing', 'mixed')


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def make_case(scenario, seed, instance):
    if scenario not in SCENARIOS:
        raise ValueError('UNKNOWN_SCENARIO')
    rng = random.Random(f'{seed}:{scenario}:{instance}')
    prefix = hashlib.sha256(f'{seed}:{scenario}:{instance}'.encode()).hexdigest()[:12]
    day = rng.randint(30, 200)
    rows, latest = [], []
    for i in range(rng.randint(7, 12)):
        last_version = 1 + i % 4
        for version in range(1, last_version + 1):
            checked = rng.randint(10, 400)
            row = {'inspection': f'{prefix}-i{i}', 'version': version,
                   'lot': f'{prefix}-L{i % 3}', 'checked': checked,
                   'failed': rng.randint(0, checked // 3), 'approved': True,
                   'effective_day': day - 10 + version, 'withdrawn': False}
            rows.append(row)
        latest.append(row)
        rows.append(copy.deepcopy(row))
    if scenario in ('draft', 'mixed'):
        r = dict(latest[0], version=latest[0]['version'] + 1, approved=False,
                 checked=latest[0]['checked'] + 997)
        rows.append(r)
    if scenario in ('future', 'mixed'):
        rows.append(dict(latest[1], version=latest[1]['version'] + 1,
                         effective_day=day + 30, checked=latest[1]['checked'] + 499))
    if scenario in ('withdrawn', 'mixed'):
        rows.append(dict(latest[2], version=latest[2]['version'] + 1, withdrawn=True))
    if scenario == 'conflict':
        rows.append(dict(latest[0], failed=latest[0]['failed'] + 1))
    if scenario == 'missing':
        # Invalidate all copies of the current fact, not just one transport copy.
        for r in rows:
            if r['inspection'] == latest[1]['inspection'] and r['version'] == latest[1]['version']:
                r['checked'] = None
    if scenario == 'mixed':
        rows.append(dict(latest[3], version=latest[3]['version'] + 1, lot=f'{prefix}-L4'))
        rows.append(dict(latest[4], version=latest[4]['version'] + 1, checked=0, failed=0))
    rng.shuffle(rows)
    contract = 'LEGACY_V1' if scenario in ('legacy', 'conflict', 'missing') else 'EFFECTIVE_V2'
    return {'case_id': f'{scenario}:{prefix}', 'scenario': scenario, 'contract': contract,
            'as_of_day': day, 'rows': rows}


def oracle(case):
    """Independent Python/Decimal calculation; never calls capability normalization or SQL.

    This oracle covers the declared generated distribution. Adversarial schema
    tests separately exercise capability validation, not an all-input oracle.
    """
    effective = case['contract'] == 'EFFECTIVE_V2'
    eligible = [r for r in case['rows'] if not effective or (r['approved'] and r['effective_day'] <= case['as_of_day'])]
    totals = {}
    for identity in sorted({r['inspection'] for r in eligible}):
        versions = sorted((r for r in eligible if r['inspection'] == identity), key=lambda r: r['version'], reverse=True)
        top = [r for r in versions if r['version'] == versions[0]['version']]
        facts = {(r['lot'], r['checked'], r['failed'], r['withdrawn'] if effective else False) for r in top}
        if len(facts) != 1:
            return {'status': 'BLOCKED', 'rows': None}
        lot, checked, failed, withdrawn = next(iter(facts))
        if withdrawn:
            continue
        if type(checked) is not int or type(failed) is not int or not 0 <= failed <= checked:
            return {'status': 'BLOCKED', 'rows': None}
        a, b = totals.get(lot, (0, 0))
        totals[lot] = (a + checked, b + failed)
    output = []
    for lot, (checked, failed) in sorted(totals.items()):
        pct = None if checked == 0 else float((Decimal(100) * failed / checked).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))
        output.append({'lot': lot, 'checked': checked, 'failed': failed, 'defect_percent': pct})
    return {'status': 'COMPLETE', 'rows': output}


def matches(actual, expected):
    if actual.get('status') != expected['status']:
        return False
    if expected['status'] != 'COMPLETE':
        return actual.get('rows') is None
    rows = actual.get('rows')
    if not isinstance(rows, list) or len(rows) != len(expected['rows']):
        return False
    keyed = {}
    for r in rows:
        if not isinstance(r, dict) or set(r) != {'lot', 'checked', 'failed', 'defect_percent'}:
            return False
        if type(r['lot']) is not str or r['lot'] in keyed or any(type(r[k]) is not int for k in ('checked', 'failed')):
            return False
        keyed[r['lot']] = r
    for e in expected['rows']:
        r = keyed.get(e['lot'])
        if r is None or any(r[k] != e[k] for k in ('checked', 'failed')):
            return False
        a, b = r['defect_percent'], e['defect_percent']
        if b is None:
            if a is not None:
                return False
        elif type(a) not in (float, int) or not abs(a - b) <= 0.000001:
            return False
    return True


def run(seed, count, conditions=None):
    active = CONDITIONS if conditions is None else {n: CONDITIONS[n] for n in conditions}
    records, input_ids, by_scenario = [], [], {}
    for scenario in SCENARIOS:
        by_scenario[scenario] = {}
        for instance in range(count):
            case = make_case(scenario, seed, instance)
            before = sha(case)
            expected = oracle(case)
            input_ids.append(before)
            # Rotate software timing order. This is not LLM randomization.
            names = list(active)
            names = names[instance % len(names):] + names[:instance % len(names)]
            for name in names:
                data = copy.deepcopy(case)
                start = time.perf_counter()
                try:
                    actual = active[name](data)
                except Exception as error:
                    actual = {'status': 'EXCEPTION', 'rows': None, 'reason': type(error).__name__}
                elapsed = time.perf_counter() - start
                correct = matches(actual, expected)
                record = {'case_id': case['case_id'], 'scenario': scenario, 'condition': name,
                          'expected_status': expected['status'], 'actual_status': actual['status'],
                          'correct': correct,
                          'silent_error': actual['status'] == 'COMPLETE' and not correct,
                          'unnecessary_refusal': expected['status'] == 'COMPLETE' and actual['status'] in ('BLOCKED', 'DECLINED'),
                          'input_unchanged': sha(data) == before,
                          'input_sha256': before, 'expected_sha256': sha(expected),
                          'actual_sha256': sha(actual), 'wall_seconds': elapsed}
                records.append(record)
                bucket = by_scenario[scenario].setdefault(name, {'correct_complete': 0, 'silent_errors': 0, 'blocked': 0, 'declined': 0, 'unnecessary_refusals': 0, 'correct_handling': 0, 'exceptions': 0, 'input_mutations': 0})
                bucket['correct_complete'] += int(correct and actual['status'] == 'COMPLETE')
                bucket['silent_errors'] += int(record['silent_error'])
                bucket['blocked'] += int(actual['status'] == 'BLOCKED')
                bucket['declined'] += int(actual['status'] == 'DECLINED')
                bucket['unnecessary_refusals'] += int(record['unnecessary_refusal'])
                bucket['correct_handling'] += int(correct)
                bucket['exceptions'] += int(actual['status'] == 'EXCEPTION')
                bucket['input_mutations'] += int(not record['input_unchanged'])
    summary = {}
    for name in active:
        summary[name] = {key: sum(by_scenario[s][name][key] for s in SCENARIOS) for key in by_scenario[SCENARIOS[0]][name]}
        summary[name]['artifact_wall_median_seconds'] = statistics.median(r['wall_seconds'] for r in records if r['condition'] == name)
    deterministic_records = [{k: v for k, v in r.items() if k != 'wall_seconds'} for r in records]
    sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob('*.py'))}
    return {'schema': 'GDSSA_E002_V1', 'evidence_class': 'CURRENT_ASSISTANT_OPEN_LABEL_ARTIFACT_STUDY',
            'seed': seed, 'instances_per_scenario': count, 'case_instances': len(input_ids),
            'artifact_invocations': len(records), 'source_sha256': sources,
            'historical_query_sha256': hashlib.sha256(BASE_SQL.encode()).hexdigest(),
            'input_suite_sha256': sha(input_ids), 'deterministic_records_sha256': sha(deterministic_records),
            'summary': summary, 'by_scenario': by_scenario, 'records': records,
            'independent_model_trials': 0, 'human_guided_trials': 0, 'human_total_active_seconds': None,
            'interactive_model_inference_tokens': None, 'interactive_model_cost_usd': None,
            'new_external_model_api_calls': 0, 'total_compute_cost_usd': None,
            'independent_or_blinded_evaluation': False, 'python': platform.python_version(),
            'sqlite': __import__('sqlite3').sqlite_version,
            'source_commit': os.environ.get('GITHUB_SHA'), 'workflow_run_id': os.environ.get('GITHUB_RUN_ID')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--count', type=int, default=12)
    parser.add_argument('--conditions', nargs='+', choices=tuple(CONDITIONS))
    parser.add_argument('--out', default='e002-result.json')
    args = parser.parse_args()
    if not 1 <= args.count <= 12:
        parser.error('count must be in 1..12')
    report = run(args.seed, args.count, args.conditions)
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    print('E002_REPORT_BEGIN')
    print(json.dumps({k: v for k, v in report.items() if k != 'records'}, ensure_ascii=False, indent=2))
    print('E002_REPORT_END')
