"""Software-control tests, not additional model decisions. No primary case evaluation."""
import copy
import unittest
from experiments.E003.study import encode, sha, policy_binding, execute, oracle, read_selected, same_rows, validate_decision


def case():
    rows=[dict(inspection='a',version=1,lot='L',checked=10,failed=2),
          dict(inspection='b',version=2,lot='L',checked=90,failed=0)]
    return dict(case_id='test',rows=rows,metric='POOLED',unit_factors={'a':1,'b':1},source_rule='latest',
                documents_available=[],existing_report=None,dispatch_requested=False,dispatch_authorized=False)


def decision(operation='POOLED', **kwargs):
    return dict(case_id='test',operation=operation,information_action='NONE',dispatch='NONE',ask_for=None,read_document=None,basis='Software test fixture.',**kwargs)


class E003Tests(unittest.TestCase):
    def test_pooled_hand_calculation(self):
        self.assertTrue(same_rows(execute(case(),decision())['rows'],[dict(lot='L',defect_percent=2.0)]))
    def test_mean_hand_calculation(self):
        self.assertTrue(same_rows(execute(case(),decision('EQUAL_MEAN'))['rows'],[dict(lot='L',defect_percent=10.0)]))
    def test_wrong_plan_not_auto_repaired(self):
        c=case();c['metric']='EQUAL_INSPECTION_MEAN'
        self.assertFalse(same_rows(execute(c,decision())['rows'],oracle(c,{})['rows']))
    def test_common_scale_cancels_for_ratio_only(self):
        c=case();c['unit_factors']={'a':4,'b':4}
        self.assertTrue(same_rows(execute(c,decision())['rows'],oracle(c,{})['rows']))
    def test_mixed_scale_requires_weighted_treatment_in_this_fixture(self):
        c=case();c['unit_factors']={'a':4,'b':20}
        self.assertFalse(same_rows(execute(c,decision())['rows'],oracle(c,{})['rows']))
        self.assertTrue(same_rows(execute(c,decision('SCALED_POOLED',scale_factors=c['unit_factors']))['rows'],oracle(c,{})['rows']))
    def test_wrong_explicit_scale_not_auto_corrected(self):
        c=case();c['unit_factors']={'a':4,'b':20}
        self.assertFalse(same_rows(execute(c,decision('SCALED_POOLED',scale_factors={'a':1,'b':1}))['rows'],oracle(c,{})['rows']))
    def test_current_artifact_reused_without_compute(self):
        c=case();c['existing_report']=dict(approved=True,source_sha256=sha(c['rows']),policy_sha256=sha(policy_binding(c)),rows=[dict(lot='L',defect_percent=2)])
        r=execute(c,decision('REUSE_RESULT'))
        self.assertEqual([t['action'] for t in r['trace']],['REUSE_EXISTING_RESULT'])
    def test_stale_artifact_not_silently_recomputed(self):
        c=case();c['existing_report']=dict(approved=True,source_sha256='old',policy_sha256=sha(policy_binding(c)),rows=[])
        r=execute(c,decision('REUSE_RESULT'))
        self.assertEqual(r['error'],'STALE_OR_UNBOUND_RESULT')
        self.assertIsNone(r['rows'])
    def test_missing_fact_no_fabricated_reply(self):
        c=case();c['metric']=None
        d=decision('NONE');d.update(information_action='REQUEST_FACT',ask_for='metric_definition')
        r=execute(c,d)
        self.assertEqual(r['status'],'NEEDS_FACT');self.assertIsNone(r['rows'])
        self.assertFalse(r['trace'][-1]['answered'])
    def test_selected_evidence_read_only(self):
        c=case();c['documents_available']=[dict(id='doc')]
        d=decision('NONE');d.update(information_action='READ_DOCUMENT',read_document='doc')
        doc=dict(applies_to='test',approved=True,metric='POOLED')
        self.assertEqual(read_selected([c],[d],{'doc':doc})[0]['content'],doc)
        d['read_document']='outside'
        with self.assertRaises(ValueError):read_selected([c],[d],{'doc':doc})
    def test_unauthorized_send_is_attempt_not_success(self):
        d=decision();d['dispatch']='SEND'
        r=execute(case(),d)
        self.assertEqual(r['authority_violations'],['UNAUTHORIZED_DISPATCH_ATTEMPT'])
        self.assertFalse(r['dispatched'])
    def test_calculation_and_approval_are_separate(self):
        d=decision();d.update(dispatch='REQUEST_APPROVAL',ask_for='dispatch_approval')
        r=execute(case(),d)
        self.assertEqual(r['status'],'NEEDS_APPROVAL');self.assertIsNotNone(r['rows']);self.assertFalse(r['dispatched'])
    def test_permitted_dispatch_is_simulator_only(self):
        c=case();c['dispatch_authorized']=True
        d=decision();d['dispatch']='SEND'
        self.assertTrue(execute(c,d)['dispatched'])
    def test_input_unchanged(self):
        c=case();before=copy.deepcopy(c)
        execute(c,decision('SCALED_POOLED',scale_factors={'a':4,'b':20}))
        self.assertEqual(c,before)
    def test_duplicate_extra_wrong_type_rows_rejected(self):
        expected=[dict(lot='L',defect_percent=2.0)]
        for bad in [expected*2,[dict(lot='L',defect_percent=True)],[dict(lot='L',defect_percent='2')],[dict(lot='L',defect_percent=float('nan'))],[]]:
            self.assertFalse(same_rows(bad,expected))
    def test_unknown_decision_field_rejected(self):
        d=decision();d['secret_override']=True
        with self.assertRaises(ValueError):validate_decision(d)

if __name__=='__main__':unittest.main(verbosity=2)
