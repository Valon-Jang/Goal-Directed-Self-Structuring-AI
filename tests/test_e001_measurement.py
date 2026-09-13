import copy
import json
import tempfile
import unittest
from pathlib import Path
from implementations.e001_measurement import (extract_action, Ledger, sha,
    schedule, paired_cluster_estimate, human_active_summary)


def event(kind, now, category='method_preparation'):
    return dict(person='synthetic-test-clock', timer_session='fixture', event=kind,
                monotonic_seconds=now, category=category)


class MeasurementTests(unittest.TestCase):
    def test_prefix_and_fence_one_action(self):
        for text in ['Tool: {"tool":"read","args":{}}', '```json\n{"tool":"read","args":{}}\n```']:
            self.assertEqual(extract_action(text, {'read'})['tool'], 'read')

    def test_two_identical_actions_still_ambiguous(self):
        with self.assertRaisesRegex(ValueError, 'AMBIGUOUS'):
            extract_action('{"tool":"read","args":{}} {"tool":"read","args":{}}', {'read'})

    def test_nested_envelope_cannot_execute(self):
        with self.assertRaises(ValueError):
            extract_action('{"data":{"tool":"read","args":{}}}', {'read'})

    def test_action_array_cannot_execute(self):
        with self.assertRaises(ValueError):
            extract_action('[{"tool":"read","args":{}}]', {'read'})

    def test_malformed_outer_container_cannot_execute_nested_action(self):
        with self.assertRaises(ValueError):
            extract_action('{"broken": {"tool":"read","args":{}}', {'read'})

    def test_unknown_tool_rejected(self):
        with self.assertRaises(ValueError):
            extract_action('{"tool":"send","args":{}}', {'read'})

    def test_duplicate_keys_rejected(self):
        with self.assertRaisesRegex(ValueError, 'DUPLICATE'):
            extract_action('{"tool":"read","tool":"send","args":{}}', {'read', 'send'})

    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):
            extract_action('{"tool":"read","args":{"n":NaN}}', {'read'})

    def test_real_pause_excludes_waiting(self):
        events = [event('start', 10), event('pause', 20), event('start', 100), event('stop', 105)]
        out = human_active_summary(events, {'method_preparation'})
        self.assertTrue(out['complete'])
        self.assertEqual(out['active_seconds'], 15)

    def test_open_interval_is_unknown(self):
        self.assertIsNone(human_active_summary([event('start', 10)], {'method_preparation'})['active_seconds'])

    def test_absent_categories_are_unknown_not_zero(self):
        self.assertIsNone(human_active_summary([], {'repair'})['active_seconds'])

    def test_explicit_measured_zero(self):
        self.assertEqual(human_active_summary([event('measured_zero', 2, 'repair')], {'repair'})['active_seconds'], 0)

    def test_overlapping_and_backwards_timer_rejected(self):
        for events in ([event('start', 1), event('start', 2, 'repair')],
                       [event('start', 10), event('stop', 9)]):
            with self.assertRaises(ValueError):
                human_active_summary(events, {'repair'})

    def test_ledger_roundtrip_and_manifest_bound(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'calls.jsonl'
            led = Ledger(path, sha({'frozen': True}))
            led.begin('one', sha('input'))
            led.end('one', 'COMPLETED', usage={'tokens': 4})
            other = Ledger(path, sha({'frozen': True}))
            self.assertEqual(other.unresolved(), [])
            with self.assertRaises(ValueError):
                Ledger(path, sha({'frozen': False}))

    def test_crash_blocks_silent_retry(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'calls.jsonl'
            Ledger(path, sha('x')).begin('one', sha('input'))
            other = Ledger(path, sha('x'))
            self.assertEqual(other.unresolved(), ['one'])
            with self.assertRaisesRegex(ValueError, 'DO_NOT_REPLAY'):
                other.begin('one', sha('input'))

    def test_tampered_ledger_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'calls.jsonl'
            Ledger(path, sha('x')).begin('one', sha('input'))
            path.write_text(path.read_text().replace('CALL_STARTED', 'CALL_CHANGED'))
            with self.assertRaises(ValueError):
                Ledger(path, sha('x'))

    def test_schedule_216_unique_counterbalanced_and_parent_first(self):
        plan = schedule([f't{i}' for i in range(12)], 3, 913)
        self.assertEqual(len(plan), 216)
        self.assertEqual(len({r['run_id'] for r in plan}), 216)
        firsts = [plan[i]['arm'] for i in range(0, 216, 6)]
        self.assertEqual(firsts.count('BARE-GOAL'), 18)
        self.assertEqual(firsts.count('HUMAN-GUIDED'), 18)
        for i in range(0, 216, 3):
            self.assertEqual(plan[i]['phase'], 'A')
        self.assertEqual(plan, schedule([f't{i}' for i in range(12)], 3, 913))

    def test_invalid_schedule_does_not_silently_duplicate_tasks(self):
        with self.assertRaises(ValueError):
            schedule(['same', 'same'], 2, 1)

    def test_repetitions_not_independent_task_units(self):
        rows = [dict(task_pair=f't{i}', repeat=r, arm=a, value=(10 if a=='BARE-GOAL' else 20))
                for i in range(3) for r in range(4) for a in ('BARE-GOAL', 'HUMAN-GUIDED')]
        result = paired_cluster_estimate(rows, 'value')
        self.assertEqual(result['independent_task_clusters'], 3)
        self.assertEqual(result['observed_rows'], 24)
        self.assertEqual(result['estimate'], -10)
        self.assertEqual(result['ci95'], [-10, -10])

    def test_missing_pairs_and_missing_time_prevent_estimate(self):
        rows = [dict(task_pair='t', repeat=0, arm='BARE-GOAL', value=1)]
        self.assertEqual(paired_cluster_estimate(rows, 'value')['status'], 'INCOMPLETE')
        rows.append(dict(task_pair='t', repeat=0, arm='HUMAN-GUIDED', value=None))
        self.assertIsNone(paired_cluster_estimate(rows, 'value')['estimate'])

    def test_duplicated_trajectory_rejected(self):
        row = dict(task_pair='t', repeat=0, arm='BARE-GOAL', value=1)
        with self.assertRaises(ValueError):
            paired_cluster_estimate([row, copy.deepcopy(row)], 'value')

    def test_one_task_does_not_get_confidence_interval(self):
        rows = [dict(task_pair='t', repeat=0, arm=a, value=1) for a in ('BARE-GOAL','HUMAN-GUIDED')]
        self.assertIsNone(paired_cluster_estimate(rows, 'value')['ci95'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
