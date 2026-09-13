import copy
import unittest
from implementations.e001_stagnation import scan


def event(sql='SELECT 1', value=1):
    return {'action': {'tool': 'query', 'args': {'sql': sql}}, 'response': {'ok': True, 'value': value}}


class StagnationTests(unittest.TestCase):
    def test_three_equal_observations_signal_only(self):
        result = scan([event()] * 5, 'a' * 64)
        self.assertEqual(result['first_signal_after_tool_events'], 3)
        self.assertEqual(result['remaining_baseline_tool_events'], 2)
        self.assertEqual(result['policy'], 'OBSERVE_ONLY')
        self.assertIsNone(result['prospective_savings'])

    def test_changed_response_breaks_run(self):
        self.assertFalse(scan([event(), event(value=2), event()], 'a' * 64)['candidate_detected'])

    def test_changed_state_breaks_run(self):
        trace = [event(), event(), event()]
        trace[2]['state_sha256'] = 'b' * 64
        self.assertFalse(scan(trace, 'a' * 64)['candidate_detected'])

    def test_distinct_action_does_not_collapse(self):
        self.assertFalse(scan([event(), event('SELECT 2'), event()], 'a' * 64)['candidate_detected'])

    def test_human_response_breaks_run(self):
        question = {'action': {'tool': 'ask_human', 'args': {}}, 'response': {'ok': True}}
        self.assertFalse(scan([event(), event(), question, event()], 'a' * 64)['candidate_detected'])

    def test_replay_is_nonmutating(self):
        trace = [event(), event(), event()]
        original = copy.deepcopy(trace)
        scan(trace, 'a' * 64)
        self.assertEqual(trace, original)

if __name__ == '__main__':
    unittest.main(verbosity=2)
