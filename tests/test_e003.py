import copy,json,unittest
from pathlib import Path
from experiments.E003.actions import execute
from experiments.E003.casepack import make_cases
from experiments.E003.oracle import expected,ambiguity_witnesses
from experiments.E003.evaluate import grade,check_freeze
from experiments.E003.witnesses import build

class E003Tests(unittest.TestCase):
    def setUp(self):self.cases={c['id']:c for c in make_cases()}
    def test_01_input_pins(self):check_freeze(Path('experiments/E003'))
    def test_02_unweighted_hand_value(self):
        out=expected(self.cases['SJ07'],{})
        self.assertEqual(out['rows'][0]['value'],20.0)
    def test_03_pooled_hand_value(self):
        out=expected(self.cases['SJ01'],{})
        self.assertEqual(out['rows'][0]['checked'],120)
        self.assertEqual(out['rows'][0]['failed'],32)
        self.assertAlmostEqual(out['rows'][0]['value'],26.666667,places=6)
    def test_04_carton_counts(self):
        out=execute(self.cases['SJ03'],{'route':'e002','operations':['normalize_cartons']})
        self.assertEqual(out['rows'][0]['checked'],43)
        self.assertEqual(out['rows'][0]['failed'],6)
    def test_05_ppm_rounding_sensitive(self):
        self.assertEqual(execute(self.cases['SJ06'],{'route':'e002','output':'ppm_from_counts'})['rows'][1]['value'],333333.333333)
    def test_06_zero_is_not_missing(self):
        self.assertIsNone(execute(self.cases['SJ12'],{'route':'e002'})['rows'][0]['value'])
    def test_07_missing_unit_is_not_zero(self):
        self.assertEqual(expected(self.cases['SJ04'],{})['status'],'ASK')
    def test_08_conflicting_metric_has_no_chosen_truth(self):
        self.assertEqual(expected(self.cases['SJ10'],{})['status'],'ASK')
    def test_09_two_worlds_differ(self):
        self.assertTrue(all(v['answers_differ'] for v in ambiguity_witnesses(list(self.cases.values()),{}).values()))
    def test_10_loss_witnesses(self):
        w=build()
        for k in ['aggregation_information_loss','identity_information_loss']:
            self.assertTrue(w[k]['same_old_output']);self.assertTrue(w[k]['different_required_output'])
    def test_11_grader_rejects_extra_duplicate_boolean_nan(self):
        wanted=expected(self.cases['SJ01'],{})
        for value in [float('nan'),True,'26.666667']:
            bad=copy.deepcopy(wanted);bad['rows'][0]['value']=value
            self.assertFalse(grade(bad,wanted))
        bad=copy.deepcopy(wanted);bad['rows'].append(bad['rows'][0]);self.assertFalse(grade(bad,wanted))
    def test_12_source_mutation_absent(self):
        c=self.cases['SJ05'];before=copy.deepcopy(c)
        execute(c,{'route':'e002','operations':['rename_columns']});self.assertEqual(c,before)
    def test_13_asking_cannot_smuggle_result(self):
        wanted=expected(self.cases['SJ04'],{})
        bad={'status':'ASK','key':'units_per_carton','question':'capacity?','rows':[{'guessed':1}]}
        self.assertFalse(grade(bad,wanted))
    def test_14_unknown_operation_and_route_rejected(self):
        for ch in [{'route':'external_send'},{'route':'e002','operations':['rewrite_authority']}]:
            with self.assertRaises(ValueError):execute(self.cases['SJ01'],ch)
    def test_15_multiple_routes_not_one_preferred_label(self):
        c=self.cases['SJ01'];wanted=expected(c,{})
        self.assertTrue(grade(execute(c,{'route':'e002'}),wanted))
        self.assertTrue(grade(execute(c,{'route':'e002','operations':['bind_authoritative_contract']}),wanted))
    def test_16_unit_id_duplicates_are_not_defective_units(self):
        out=execute(self.cases['SJ08'],{'route':'distinct_units'})
        self.assertEqual(out['rows'][0]['failed'],2);self.assertEqual(out['rows'][0]['value'],25.0)

if __name__=='__main__':unittest.main()
