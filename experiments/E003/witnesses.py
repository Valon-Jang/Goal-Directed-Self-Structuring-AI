"""Executable information-loss counterexamples; not additional model trials."""
import copy,json
from pathlib import Path
from experiments.E002.capability import adapted_reuse
from experiments.E003.casepack import make_cases
from experiments.E003.oracle import expected,ambiguity_witnesses


def build():
    cases=make_cases();macro=copy.deepcopy(cases[6]);variants=[]
    for counts in [[(10,0),(90,10)],[(50,5),(50,5)]]:
        c=copy.deepcopy(macro)
        c['payload']['rows']=[dict(inspection=str(i),version=1,lot='L',checked=n,failed=f) for i,(n,f) in enumerate(counts)]
        variants.append({'input':c['payload']['rows'],'old_output':adapted_reuse(c['payload']),'new_target':expected(c,{})})
    unit=copy.deepcopy(cases[7]);other=copy.deepcopy(unit)
    other['defect_events']=[{'unit_id':str(i),'kind':'dent'} for i in range(4)]
    units=[{'old_output':adapted_reuse(c['payload']),'new_target':expected(c,{}),'events':c['defect_events']} for c in [unit,other]]
    return {'schema':'GDSSA_E003_STRUCTURAL_WITNESSES_V1',
            'aggregation_information_loss':{'worlds':variants,'same_old_output':variants[0]['old_output']==variants[1]['old_output'],'different_required_output':variants[0]['new_target']!=variants[1]['new_target']},
            'identity_information_loss':{'worlds':units,'same_old_output':units[0]['old_output']==units[1]['old_output'],'different_required_output':units[0]['new_target']!=units[1]['new_target']},
            'missing_authority':ambiguity_witnesses(cases,{}),
            'interpretation':'For each demonstrated pair, no output-only mapping from that identical old output can guarantee both distinct new targets. Return to available upstream records; ask for missing facts only when no authorized evidence resolves them.',
            'extra_model_decisions':0,'causal_improvement_claim':False}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
    data=build();Path(a.out).write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:{x:v[x] for x in ['same_old_output','different_required_output']} for k,v in data.items() if k.endswith('information_loss')},indent=2))
