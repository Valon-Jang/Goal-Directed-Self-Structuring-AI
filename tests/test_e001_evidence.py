"""Recompute derived evidence; these tests add no real model or human trials."""
import hashlib
import json
import unittest
from pathlib import Path
from implementations.e001_stagnation import scan

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'evidence' / 'E001'


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.result = json.loads((EVIDENCE/'E01_RESULT.json').read_text())
        self.observed = json.loads((EVIDENCE/'E01_OBSERVATIONS.json').read_text())
        self.replay = json.loads((EVIDENCE/'E01_STAGNATION_REPLAY.json').read_text())

    def test_observation_commitments_match(self):
        actual = hashlib.sha256((EVIDENCE/'E01_OBSERVATIONS.json').read_bytes()).hexdigest()
        self.assertEqual(self.result['normalized_observations_sha256'], actual)
        self.assertEqual(self.replay['source_observations_sha256'], actual)

    def test_reported_token_sums_recompute(self):
        calls = [u for seq in self.result['calls_and_tokens'].values() for u in seq]
        self.assertEqual(len(calls), self.result['real_model_calls_attempted'])
        for key, value in self.result['token_totals'].items():
            self.assertEqual(sum(c[key] for c in calls), value)

    def test_posthoc_sensor_reproduces_exact_results(self):
        for family, ids in self.observed['trace_observation_ids'].items():
            trace = [self.observed['observation_pool'][i] for i in ids]
            actual = scan(trace, self.observed['input_hashes'][family], self.replay['threshold'])
            self.assertEqual(actual, self.replay['results'][family])

    def test_source_pins_are_recoverable_from_tested_commit(self):
        # Tested source is intentionally not changed by the evidence-only addition.
        for name, expected in self.result['source_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), expected, name)

    def test_workflow_success_does_not_turn_task_failures_into_success(self):
        self.assertEqual(sum(c['accepted'] for c in self.result['cases']), self.result['accepted_task_episodes'])
        self.assertEqual(self.result['accepted_task_episodes'], 0)
        self.assertEqual(self.result['primary_comparative_trials_completed'], 0)
        self.assertIsNone(self.result['human_total_active_seconds'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
