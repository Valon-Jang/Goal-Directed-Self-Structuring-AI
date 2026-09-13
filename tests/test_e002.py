import copy
import math
import unittest
from experiments.E002.capability import adapted_reuse, blind_reuse, contract_gated_reuse
from experiments.E002.study import make_case, matches, oracle, run, sha


def row(identity='A', version=1, checked=10, failed=1, **changes):
    r = {'inspection': identity, 'version': version, 'lot': 'X', 'checked': checked,
         'failed': failed, 'approved': True, 'effective_day': 10, 'withdrawn': False}
    r.update(changes)
    return r


def case(rows, contract='EFFECTIVE_V2', day=20):
    return {'rows': rows, 'contract': contract, 'as_of_day': day}


class E002Tests(unittest.TestCase):
    def test_01_hand_computed_weighted_denominator(self):
        c = case([row(checked=10, failed=5), row('B', checked=90, failed=9)])
        expected = {'status': 'COMPLETE', 'rows': [{'lot': 'X', 'checked': 100, 'failed': 14, 'defect_percent': 14.0}]}
        self.assertEqual(oracle(c), expected)
        self.assertTrue(matches(adapted_reuse(c), expected))
        wrong = copy.deepcopy(expected)
        wrong['rows'][0]['defect_percent'] = 30.0  # Mean of 50% and 10%.
        self.assertFalse(matches(wrong, expected))

    def test_02_heterogeneous_versions_discriminate_global_max(self):
        c = case([row(version=2, checked=20, failed=2), row('B', version=1, checked=30, failed=3)])
        self.assertEqual(oracle(c)['rows'][0]['checked'], 50)
        wrong = case([c['rows'][0]])
        self.assertFalse(matches(adapted_reuse(wrong), oracle(c)))

    def test_03_identical_duplicates_are_invariant(self):
        c = case([row(), row('B')])
        self.assertEqual(adapted_reuse(c), adapted_reuse(case(c['rows'] * 3)))

    def test_04_old_conflict_does_not_block_current(self):
        c = case([row(), row(failed=2), row(version=2, checked=20, failed=3)])
        self.assertEqual(adapted_reuse(c)['status'], 'COMPLETE')

    def test_05_future_invalid_count_is_not_current(self):
        c = case([row(), row(version=2, checked=None, effective_day=21)])
        self.assertEqual(adapted_reuse(c)['rows'][0]['checked'], 10)

    def test_06_draft_does_not_override(self):
        c = case([row(), row(version=2, checked=50, approved=False)])
        self.assertEqual(adapted_reuse(c)['rows'][0]['checked'], 10)

    def test_07_withdrawn_current_removes_inspection(self):
        c = case([row(), row(version=2, withdrawn=True), row('B')])
        self.assertEqual(adapted_reuse(c)['rows'][0]['checked'], 10)

    def test_08_selected_conflict_blocks_without_rows(self):
        c = case([row(), row(failed=2)])
        a = adapted_reuse(c)
        self.assertEqual(a['status'], 'BLOCKED')
        self.assertIsNone(a['rows'])
        self.assertTrue(matches(a, oracle(c)))

    def test_09_missing_current_count_blocks(self):
        self.assertEqual(adapted_reuse(case([row(checked=None)]))['status'], 'BLOCKED')

    def test_10_zero_denominator_is_null(self):
        c = case([row(checked=0, failed=0)])
        self.assertTrue(matches(adapted_reuse(c), oracle(c)))
        self.assertIsNone(adapted_reuse(c)['rows'][0]['defect_percent'])

    def test_11_effective_date_boundary_inclusive(self):
        c = case([row(), row(version=2, checked=20, effective_day=20)])
        self.assertEqual(adapted_reuse(c)['rows'][0]['checked'], 20)

    def test_12_unknown_contract_not_guessed(self):
        self.assertEqual(adapted_reuse(case([row()], 'UNKNOWN'))['status'], 'DECLINED')

    def test_13_invalid_counts_are_not_coerced(self):
        for value in (None, True, '10', -1, float('nan'), float('inf'), 10**10):
            with self.subTest(value=value):
                self.assertEqual(adapted_reuse(case([row(checked=value)]))['status'], 'BLOCKED')

    def test_14_invalid_flags_are_not_coerced(self):
        for field, value in [('approved', 1), ('withdrawn', 'false'), ('effective_day', '10')]:
            self.assertEqual(adapted_reuse(case([row(**{field: value})]))['status'], 'BLOCKED')

    def test_15_undeclared_column_blocks(self):
        self.assertEqual(adapted_reuse(case([row(unit='kg')]))['status'], 'BLOCKED')

    def test_16_invalid_version_and_identity_block(self):
        for data in (row(identity=''), row(version=True), row(version=0), row(lot=None)):
            self.assertEqual(adapted_reuse(case([data]))['status'], 'BLOCKED')

    def test_17_grader_rejects_duplicate_omitted_and_extra_rows(self):
        e = oracle(case([row()]))
        for rows in ([], e['rows'] * 2, [dict(e['rows'][0], extra=1)]):
            self.assertFalse(matches({'status': 'COMPLETE', 'rows': rows}, e))

    def test_18_grader_rejects_nan_boolean_string_pct(self):
        e = oracle(case([row()]))
        for value in (float('nan'), float('inf'), True, '10.0'):
            a = copy.deepcopy(e)
            a['rows'][0]['defect_percent'] = value
            self.assertFalse(matches(a, e))

    def test_19_gate_refusal_is_not_completion(self):
        c = case([row()])
        self.assertFalse(matches(contract_gated_reuse(c), oracle(c)))

    def test_20_synthetic_seed_changes_quantities_not_just_order(self):
        a, b = make_case('legacy', 12, 0), make_case('legacy', 13, 0)
        self.assertNotEqual(sorted(r['checked'] for r in a['rows']), sorted(r['checked'] for r in b['rows']))
        self.assertGreater(len({r['version'] for r in a['rows']}), 1)

    def test_21_resolved_and_ambiguous_expected_counts(self):
        r = run(913, 1)
        self.assertEqual(r['case_instances'], 8)
        self.assertEqual(r['artifact_invocations'], 24)
        self.assertEqual(r['summary']['ADAPTED_REUSE']['correct_complete'], 6)
        self.assertEqual(r['summary']['ADAPTED_REUSE']['blocked'], 2)
        self.assertEqual(r['summary']['ADAPTED_REUSE']['silent_errors'], 0)
        self.assertEqual(r['independent_model_trials'], 0)
        self.assertIsNone(r['human_total_active_seconds'])

    def test_22_input_remains_unchanged(self):
        c = make_case('mixed', 913, 0)
        before = sha(c)
        for f in (adapted_reuse, blind_reuse, contract_gated_reuse):
            f(c)
            self.assertEqual(sha(c), before)

    def test_23_postgresql_or_alternate_schema_not_invented(self):
        c = case([{'inspection_id': 'A', 'version': 1, 'lot': 'X', 'checked': 10, 'failed': 1}])
        self.assertEqual(adapted_reuse(c)['status'], 'BLOCKED')

    def test_24_new_lot_and_empty_input(self):
        self.assertTrue(matches(adapted_reuse(case([])), oracle(case([]))))
        c = case([row(), row(version=2, lot='Y')])
        self.assertEqual(adapted_reuse(c)['rows'][0]['lot'], 'Y')

    def test_25_draft_withdrawal_does_not_remove_valid_inspection(self):
        c = case([row(), row(version=2, approved=False, withdrawn=True)])
        self.assertEqual(adapted_reuse(c)['rows'][0]['checked'], 10)

    def test_26_refusal_cannot_smuggle_business_rows(self):
        self.assertFalse(matches({'status': 'BLOCKED', 'rows': []}, {'status': 'BLOCKED', 'rows': None}))


if __name__ == '__main__':
    unittest.main(verbosity=2)
