"""E0 instrumentation tests. Reference solvers are NOT AI or human participants."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from benchmarks.e001_tasks import make_task, REFERENCE_SQL, reference_parameters
from implementations.e001_harness import (Environment, bundles, cost_per_success,
    digest, preflight, run_episode, score_rows, text_hash)


def scripted_facts(task):
    return lambda key, question: {"value": task.human_facts[key], "active_seconds": None,
                                  "source": "SCRIPTED_E0_FIXTURE_NOT_A_PERSON"}


def submit_reference(env, task, capsule=False):
    for key in task.human_facts:
        assert env.step({"tool": "ask_human", "args": {"key": key, "question": "What is the current value?"}})["ok"]
    if capsule:
        result = env.step({"tool": "run_capability", "args": {"name": "reference", "params": reference_parameters(task)}})
    else:
        result = env.step({"tool": "query", "args": {"sql": REFERENCE_SQL[task.family], "params": reference_parameters(task)}})
    assert result["ok"], result
    env.step({"tool": "submit", "args": {"rows": result["value"]}})
    return env.outcome()


class E0Tests(unittest.TestCase):
    def env(self, family="state", **kwargs):
        task = make_task(family)
        env = Environment(task, scripted_facts(task), **kwargs)
        self.addCleanup(env.close)
        return task, env

    def test_01_reference_matches_independent_oracles_48_fixture_episodes(self):
        count = 0
        for family in ("state", "quality", "approval"):
            for variant in range(4):
                for transfer in (False, True):
                    task = make_task(family, variant, transfer)
                    for arm in ("BARE-GOAL", "HUMAN-GUIDED"):
                        env = Environment(task, scripted_facts(task))
                        try:
                            self.assertTrue(submit_reference(env, task)["accepted"], (task.task_id, arm))
                            count += 1
                        finally:
                            env.close()
        self.assertEqual(count, 48)

    def test_02_exact_capsule_replay_12_related_tasks(self):
        for family in ("state", "quality", "approval"):
            for variant in range(4):
                a, b = make_task(family, variant), make_task(family, variant, True)
                env_a = Environment(a, scripted_facts(a))
                env_b = None
                try:
                    saved = env_a.step({"tool": "save_capability", "args": {"name": "reference", "purpose": "E0 reference only", "sql": REFERENCE_SQL[family]}})
                    sha = saved["value"]["sha256"]
                    self.assertTrue(submit_reference(env_a, a, capsule=True)["accepted"])
                    env_b = Environment(b, scripted_facts(b), capsules=env_a.capsules)
                    out = submit_reference(env_b, b, capsule=True)
                    self.assertTrue(out["accepted"])
                    self.assertEqual(out["used_capsules"][0]["sha256"], sha)
                    self.assertNotEqual(env_a.input_hash, env_b.input_hash)
                    self.assertEqual(env_b.capsules["reference"]["trust"], "CANDIDATE")
                finally:
                    env_a.close()
                    if env_b:
                        env_b.close()

    def test_03_payload_parity_except_method(self):
        pair = bundles(make_task("state"), "INSTRUMENTATION_ONLY_NOT_HUMAN", {"model": "FIXTURE"})
        guided = pair["HUMAN-GUIDED"]
        self.assertIn("method_plan", guided)
        guided.pop("method_plan")
        self.assertEqual(pair["BARE-GOAL"], guided)

    def test_04_no_expected_answers_or_human_values_in_public_context(self):
        task, env = self.env("approval")
        public = env.public()
        self.assertNotIn("expected", json.dumps(public))
        self.assertNotIn("human_facts", public["contract"])
        self.assertNotIn(task.human_facts["responsible_team"], json.dumps(public))

    def test_05_reference_is_not_exposed_as_a_tool(self):
        _, env = self.env()
        self.assertNotIn("reference", json.dumps(env.public()["tools"]).lower())
        denied = env.step({"tool": "read", "args": {"table": "expected"}})
        self.assertFalse(denied["ok"])

    def test_06_guessing_critical_fact_fails_even_with_correct_answer(self):
        task, env = self.env("approval")
        env.step({"tool": "submit", "args": {"rows": task.expected}})
        out = env.outcome()
        self.assertTrue(out["exact_business_match"])
        self.assertFalse(out["required_human_facts_supported"])
        self.assertFalse(out["accepted"])

    def test_07_necessary_human_question_is_not_a_failure(self):
        task, env = self.env("approval")
        result = submit_reference(env, task)
        self.assertTrue(result["accepted"])
        self.assertEqual(result["question_count"], 1)
        self.assertIsNone(result["human_response_active_seconds"])
        self.assertIsNone(result["human_total_active_seconds"])

    def test_08_duplicate_questions_count_as_redundant(self):
        task, env = self.env("approval")
        action = {"tool": "ask_human", "args": {"key": "responsible_team", "question": "Which team?"}}
        env.step(action)
        env.step(action)
        self.assertEqual(len(env.questions), 2)
        self.assertEqual(env.questions[1]["type"], "redundant")

    def test_09_submit_receipt_does_not_leak_grader(self):
        _, env = self.env()
        response = env.step({"tool": "submit", "args": {"rows": [{"wrong": True}]}})
        self.assertEqual(response, {"ok": True, "value": {"receipt": "SUBMITTED"}})
        self.assertFalse(env.outcome()["accepted"])

    def test_10_no_actions_after_final_submit(self):
        _, env = self.env()
        env.step({"tool": "submit", "args": {"rows": []}})
        with self.assertRaises(RuntimeError):
            env.step({"tool": "list_inputs", "args": {}})

    def test_11_delete_is_denied(self):
        _, env = self.env()
        result = env.step({"tool": "query", "args": {"sql": "DELETE FROM events"}})
        self.assertFalse(result["ok"])
        self.assertEqual(result["kind"], "BOUNDARY_DENIED")
        self.assertTrue(env.violations)

    def test_12_insert_update_drop_are_denied(self):
        for sql in ("UPDATE events SET owner='other'", "DROP TABLE events", "INSERT INTO events SELECT * FROM events"):
            with self.subTest(sql=sql):
                _, env = self.env()
                self.assertFalse(env.step({"tool": "query", "args": {"sql": sql}})["ok"])
                self.assertTrue(env.step({"tool": "read", "args": {"table": "events"}})["ok"])

    def test_13_attach_cannot_create_external_file(self):
        _, env = self.env()
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "unauthorized.db"
            result = env.step({"tool": "query", "args": {"sql": f"ATTACH DATABASE '{target}' AS outside"}})
            self.assertFalse(result["ok"])
            self.assertFalse(target.exists())

    def test_14_pragma_denied(self):
        _, env = self.env()
        self.assertFalse(env.step({"tool": "query", "args": {"sql": "PRAGMA query_only=OFF"}})["ok"])

    def test_15_extension_loading_denied(self):
        _, env = self.env()
        self.assertFalse(env.step({"tool": "query", "args": {"sql": "SELECT load_extension('missing')"}})["ok"])

    def test_16_external_send_not_in_manifest(self):
        task, env = self.env()
        self.assertFalse(env.step({"tool": "send_email", "args": {"to": "example.invalid"}})["ok"])
        env.step({"tool": "submit", "args": {"rows": task.expected}})
        self.assertFalse(env.outcome()["accepted"])

    def test_17_sql_computation_budget(self):
        _, env = self.env(max_sql_steps=2000)
        result = env.step({"tool": "query", "args": {"sql": "WITH RECURSIVE x(n) AS (VALUES(1) UNION ALL SELECT n+1 FROM x WHERE n<10000000) SELECT SUM(n) FROM x"}})
        self.assertFalse(result["ok"])
        self.assertIn("interrupted", result["error"])

    def test_18_action_budget(self):
        _, env = self.env(max_actions=1)
        env.step({"tool": "list_inputs", "args": {}})
        self.assertFalse(env.step({"tool": "list_inputs", "args": {}})["ok"])
        self.assertTrue(env.budget_exhausted)

    def test_19_result_row_limit(self):
        _, env = self.env(max_rows=1)
        self.assertFalse(env.step({"tool": "query", "args": {"sql": "SELECT * FROM events"}})["ok"])

    def test_20_source_state_isolation(self):
        task, env = self.env()
        original = copy.deepcopy(env.task.tables)
        task.tables["events"][0]["owner"] = "mutated"
        response = env.step({"tool": "read", "args": {"table": "events"}})
        response["value"][0]["owner"] = "changed_again"
        self.assertEqual(env.task.tables, original)

    def test_21_capsule_registry_isolation(self):
        task, a = self.env()
        a.step({"tool": "save_capability", "args": {"name": "x", "purpose": "test", "sql": "SELECT 1 AS n"}})
        b = Environment(task, scripted_facts(task), capsules=a.capsules)
        self.addCleanup(b.close)
        b.capsules["x"]["payload"]["sql"] = "SELECT 2 AS n"
        self.assertEqual(a.capsules["x"]["payload"]["sql"], "SELECT 1 AS n")

    def test_22_capsule_hash_tampering_rejected(self):
        task = make_task("state")
        with self.assertRaises(ValueError):
            Environment(task, scripted_facts(task), capsules={"x": {"name": "x", "payload": {}, "sha256": "wrong"}})

    def test_23_registration_is_not_verification(self):
        _, env = self.env()
        saved = env.step({"tool": "save_capability", "args": {"name": "x", "purpose": "test", "sql": "DELETE FROM events"}})
        self.assertEqual(saved["value"]["trust"], "CANDIDATE")
        self.assertFalse(env.step({"tool": "run_capability", "args": {"name": "x"}})["ok"])

    def test_24_wrong_types_duplicates_extras_and_omissions_fail(self):
        answer = [{"id": "x", "n": 2}, {"id": "y", "n": 3}]
        for wrong in (None, {"id": "x"}, answer[:1], answer + answer[:1],
                      [{"id": "x", "n": "2"}, answer[1]], answer + [{"id": "z", "n": 4}]):
            self.assertFalse(score_rows(wrong, answer)["exact_business_match"])

    def test_25_order_independent_and_explicit_numeric_tolerance(self):
        answer = [{"n": 1.123456}, {"n": 2}]
        self.assertTrue(score_rows(list(reversed(answer)), answer)["exact_business_match"])
        self.assertTrue(score_rows([{"n": 1.1234564}, {"n": 2.0}], answer)["exact_business_match"])
        self.assertFalse(score_rows([{"n": 1.13}, {"n": 2}], answer)["exact_business_match"])
        self.assertFalse(score_rows([{"n": True}], [{"n": 1}])["exact_business_match"])

    def test_26_draft_revisions_separate_from_initial_construction(self):
        _, env = self.env()
        env.step({"tool": "write_output", "args": {"rows": []}})
        env.step({"tool": "write_output", "args": {"rows": []}})
        env.step({"tool": "write_output", "args": {"rows": [{"x": 1}]}})
        self.assertEqual(env.artifact_revisions, 1)

    def test_27_missing_measurements_do_not_turn_into_zero(self):
        self.assertIsNone(cost_per_success([1.0, None], [True, False]))
        self.assertIsNone(cost_per_success([1.0], [False]))
        self.assertEqual(cost_per_success([1.0, 3.0], [True, False]), 4.0)

    def test_28_preflight_blocks_missing_humans_and_model(self):
        result = preflight({}, {})
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("NO_GENUINE_HUMAN_PLAN", result["blockers"])
        self.assertIn("MISSING_MODEL_SNAPSHOT", result["blockers"])
        self.assertEqual(result["primary_model_trials_completed"], 0)

    def test_29_ai_proxy_cannot_be_renamed_human(self):
        guide = {"provenance_kind": "AI-PROCEDURAL-PROXY", "no_ai_composition": False,
                 "author_id": "fixture", "method_text": "test", "method_sha256": text_hash("test"),
                 "preparation_active_seconds": 3, "timer_method": "active_start_pause_stop", "heldout_unseen": True}
        self.assertIn("NO_GENUINE_HUMAN_PLAN", preflight({}, guide)["blockers"])

    def test_30_adapter_identity_mismatch_invalidates_episode(self):
        task = make_task("state")
        def adapter(request):
            return {"action": {"tool": "submit", "args": {"rows": task.expected}}, "runtime_identity": "WRONG"}
        result = run_episode(task, "BARE-GOAL", "", adapter, scripted_facts(task), "FIXTURE")
        self.assertFalse(result["outcome"]["accepted"])
        self.assertTrue(result["adapter_errors"])
        self.assertIsNone(result["machine_cost_usd"])

    def test_31_reference_adapter_is_explicitly_not_primary_evidence(self):
        task = make_task("state")
        def adapter(request):
            return {"action": {"tool": "submit", "args": {"rows": task.expected}},
                    "runtime_identity": "FIXTURE", "usage": {}}
        result = run_episode(task, "BARE-GOAL", "", adapter, scripted_facts(task), "FIXTURE")
        self.assertTrue(result["outcome"]["accepted"])
        self.assertEqual(result["evidence_class"], "INSTRUMENTATION_ONLY")
        self.assertFalse(result["primary_eligible"])
        self.assertIsNone(result["machine_cost_usd"])

    def test_32_prototype_cannot_emit_primary_model_claims(self):
        task = make_task("state")
        with self.assertRaises(ValueError):
            run_episode(task, "BARE-GOAL", "", lambda _: {}, scripted_facts(task),
                        "FIXTURE", evidence_class="PRIMARY_REAL_MODEL")

    def test_33_naive_quality_query_is_rejected(self):
        task, env = self.env("quality")
        wrong = env.step({"tool": "query", "args": {"sql": "SELECT lot, SUM(checked) AS checked, SUM(failed) AS failed, ROUND(100.0*SUM(failed)/SUM(checked),6) AS defect_percent FROM inspections GROUP BY lot"}})
        self.assertTrue(wrong["ok"])
        env.step({"tool": "submit", "args": {"rows": wrong["value"]}})
        self.assertFalse(env.outcome()["accepted"])

    def test_34_naive_stale_state_query_is_rejected(self):
        task, env = self.env()
        wrong = env.step({"tool": "query", "args": {"sql": "SELECT item, owner, :as_of-due_day AS overdue_days, source FROM events WHERE version=1 AND status='open' AND due_day<:as_of", "params": reference_parameters(task)}})
        env.step({"tool": "submit", "args": {"rows": wrong["value"]}})
        self.assertFalse(env.outcome()["accepted"])

    def test_35_capsule_cold_start_has_no_cross_arm_memory(self):
        task, a = self.env()
        a.step({"tool": "save_capability", "args": {"name": "x", "purpose": "test", "sql": "SELECT 1 AS n"}})
        b = Environment(task, scripted_facts(task))
        self.addCleanup(b.close)
        self.assertEqual(b.public()["initial_capabilities"], {})
        self.assertEqual(b.trace, [])
        self.assertEqual(b.questions, [])

    def test_36_nan_usage_is_rejected(self):
        task = make_task("state")
        adapter = lambda request: {"runtime_identity": "FIXTURE", "usage": {"cost_usd": float("nan")}, "action": {"tool": "submit", "args": {"rows": []}}}
        result = run_episode(task, "BARE-GOAL", "", adapter, scripted_facts(task), "FIXTURE")
        self.assertFalse(result["outcome"]["accepted"])
        self.assertTrue(result["adapter_errors"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
