"""E002 software conditions. No oracle, network, model API or external writes."""
from __future__ import annotations
import copy
import sqlite3

# Exact historical text: benchmarks/e001_tasks.py at 902f10de.
BASE_SQL = """WITH latest AS (
      SELECT DISTINCT i.inspection, i.version, i.lot, i.checked, i.failed FROM inspections i
      WHERE i.version=(SELECT MAX(x.version) FROM inspections x WHERE x.inspection=i.inspection))
      SELECT lot, SUM(checked) AS checked, SUM(failed) AS failed,
      ROUND(100.0*SUM(failed)/SUM(checked),6) AS defect_percent FROM latest GROUP BY lot"""
BASE_KEYS = {'inspection', 'version', 'lot', 'checked', 'failed'}
EXTRA_KEYS = {'approved', 'effective_day', 'withdrawn'}


def result(status, rows=None, reason=None):
    return {'status': status, 'rows': rows, 'reason': reason}


def query(rows):
    """Run the frozen query on a disposable in-memory database; inputs unchanged."""
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    try:
        conn.execute('CREATE TABLE inspections(inspection TEXT, version INTEGER, lot TEXT, checked INTEGER, failed INTEGER)')
        conn.executemany('INSERT INTO inspections VALUES(?,?,?,?,?)',
                         [(r.get('inspection'), r.get('version'), r.get('lot'), r.get('checked'), r.get('failed')) for r in rows])
        conn.execute('PRAGMA query_only=ON')
        return [dict(r) for r in conn.execute(BASE_SQL)]
    finally:
        conn.close()


def blind_reuse(case):
    # Intentionally unsafe scientific control, never a recommended production path.
    return result('COMPLETE', query(case['rows']))


def _select(case, effective):
    rows = case.get('rows')
    if not isinstance(rows, list) or len(rows) > 10000:
        raise ValueError('INVALID_ROWS')
    if effective and type(case.get('as_of_day')) is not int:
        raise ValueError('INVALID_AS_OF')
    grouped = {}
    for r in rows:
        if not isinstance(r, dict) or not BASE_KEYS <= set(r) or set(r) - BASE_KEYS - EXTRA_KEYS:
            raise ValueError('UNDECLARED_SCHEMA')
        if any(type(r[k]) is not str or not 0 < len(r[k]) <= 128 for k in ('inspection', 'lot')):
            raise ValueError('INVALID_ID')
        if type(r['version']) is not int or not 1 <= r['version'] <= 1000000:
            raise ValueError('INVALID_VERSION')
        if effective:
            if not EXTRA_KEYS <= set(r) or type(r['approved']) is not bool or type(r['withdrawn']) is not bool or type(r['effective_day']) is not int:
                raise ValueError('INVALID_ELIGIBILITY')
            if not r['approved'] or r['effective_day'] > case['as_of_day']:
                continue
        grouped.setdefault(r['inspection'], []).append(r)
    chosen = []
    for group in grouped.values():
        maximum = max(r['version'] for r in group)
        candidates = [r for r in group if r['version'] == maximum]
        keys = sorted(BASE_KEYS | ({'withdrawn'} if effective else set()))
        # Equality of relevant business facts, not row order or number of copies.
        first = candidates[0]
        if any(any(type(r[k]) is not type(first[k]) or r[k] != first[k] for k in keys) for r in candidates[1:]):
            raise ValueError('CONFLICTING_CURRENT_FACTS')
        if effective and first['withdrawn']:
            continue
        if any(type(first[k]) is not int or not 0 <= first[k] <= 1000000000 for k in ('checked', 'failed')) or first['failed'] > first['checked']:
            raise ValueError('INVALID_CURRENT_COUNTS')
        chosen.append({k: copy.deepcopy(first[k]) for k in BASE_KEYS})
    return chosen


def contract_gated_reuse(case):
    if case.get('contract') != 'LEGACY_V1':
        return result('DECLINED', reason='OUTSIDE_LEGACY_SCOPE')
    try:
        _select(case, False)  # Validate first; do not change the historical SQL input.
        return result('COMPLETE', query(case['rows']))
    except (ValueError, TypeError, KeyError) as error:
        return result('BLOCKED', reason=str(error))


def adapted_reuse(case):
    contract = case.get('contract')
    if contract not in {'LEGACY_V1', 'EFFECTIVE_V2'}:
        return result('DECLINED', reason='UNKNOWN_CONTRACT')
    try:
        selected = _select(case, contract == 'EFFECTIVE_V2')
        return result('COMPLETE', query(selected))
    except (ValueError, TypeError, KeyError) as error:
        return result('BLOCKED', reason=str(error))


CONDITIONS = {'BLIND_REUSE': blind_reuse, 'CONTRACT_GATED_REUSE': contract_gated_reuse,
              'ADAPTED_REUSE': adapted_reuse}
