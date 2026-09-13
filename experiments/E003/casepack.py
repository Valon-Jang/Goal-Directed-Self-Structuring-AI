"""Public, self-authored diagnostic vignettes; no expected routes or outputs."""
import copy, json
from pathlib import Path


def make_cases():
    rows = [
        dict(inspection='a',version=1,lot='L1',checked=10,failed=8),
        dict(inspection='a',version=2,lot='L1',checked=20,failed=2),
        dict(inspection='b',version=3,lot='L1',checked=100,failed=30),
        dict(inspection='b',version=1,lot='L1',checked=50,failed=4),
        dict(inspection='c',version=1,lot='L2',checked=3,failed=1)]
    rows += [copy.deepcopy(rows[1])]
    base = {'contract':'LEGACY_V1','as_of_day':100,'rows':rows}
    def case(n,goal,**policy):
        return {'id':f'SJ{n:02}', 'goal':goal,
                'policy':{'authority':'Task owner approved definition; source rows do not change it.',
                          'selection':'LEGACY_V1','metric':'pooled_percent','checked_unit':'unit',**policy},
                'payload':copy.deepcopy(base),'documents':[]}
    cases=[]
    c=case(1,'Report current lot defective-unit percentage. A cosmetic report title changed.')
    c['payload']['report_title']='Quality board 2027 skin';cases.append(c)
    c=case(2,'Report currently approved/effective lot defective-unit percentage; apply withdrawals.',selection='EFFECTIVE_V2')
    c['payload']['contract']='EFFECTIVE_V2'
    for r in c['payload']['rows']:r.update(approved=True,effective_day=80,withdrawn=False)
    a=next(r for r in c['payload']['rows'] if r['inspection']=='a' and r['version']==2)
    c['payload']['rows'] += [dict(a,version=9,failed=19,approved=False),dict(a,version=8,failed=18,effective_day=101)]
    cases.append(c)
    c=case(3,'Report defective units per checked unit, not per carton.',checked_unit='carton',units_per_carton={'a':12,'b':5,'c':4})
    c['payload']['rows']=[dict(inspection=k,version=1,lot='L1',checked=n,failed=f) for k,n,f in [('a',2,2),('b',3,3),('c',1,1)]];cases.append(c)
    c=case(4,'Report defective units per checked unit. Carton capacity is not present in any available source.',checked_unit='carton',units_per_carton=None)
    c['payload']['rows']=[dict(inspection='x',version=1,lot='L1',checked=10,failed=2)];cases.append(c)
    c=case(5,'Report the same current lot defective-unit percentage after export column renaming.',column_map={'sample_key':'inspection','rev':'version','batch':'lot','n_checked':'checked','n_failed':'failed'})
    inverse={v:k for k,v in c['policy']['column_map'].items()}
    c['payload']['rows']=[{inverse[k]:v for k,v in r.items()} for r in rows];cases.append(c)
    cases.append(case(6,'Report defective-unit parts per million (PPM), rounded to six decimals; tolerance 0.000001 ppm.',metric='pooled_ppm'))
    cases.append(case(7,'Report the arithmetic mean of CURRENT inspection-level defective-unit percentages per lot; each inspection has equal weight. Do not pool checked quantities.',metric='macro_percent'))
    c=case(8,'Report DISTINCT defective inspected units / DISTINCT inspected units per lot. Multiple defect events on one unit count once.',metric='distinct_unit_percent')
    c['unit_register']=[{'unit_id':str(i),'lot':'L1'} for i in range(8)]
    c['defect_events']=[{'unit_id':'0','kind':'dent'},{'unit_id':'0','kind':'scratch'},{'unit_id':'1','kind':'dent'},{'unit_id':'1','kind':'dent'}]
    c['payload']['rows']=[dict(inspection='summary',version=1,lot='L1',checked=8,failed=4)]
    c['policy']['legacy_failed_meaning']='defect EVENTS, not defective units';cases.append(c)
    c=case(9,'Produce the approved metric for this report. Its exact definition is in the listed document.',metric=None)
    c['documents']=[{'id':'metric-definition','path':'experiments/E003/sources/metric-definition.json','title':'Owner-approved metric definition'}];cases.append(c)
    c=case(10,'Produce the owner-approved defect rate. Two current definitions have equal authority; no priority or revocation is available.',metric=None)
    c['policy']['competing_definitions']=['pooled_percent','macro_percent'];cases.append(c)
    c=copy.deepcopy(cases[1]);c['id']='SJ11'
    c['goal']='Report approved/effective current records using the owner policy. The export cache contract tag predates that policy.'
    c['payload']['contract']='LEGACY_V1';c['policy']['cache_tag_authority']='obsolete_hint_only';cases.append(c)
    c=case(12,'Report the current lot rate. Zero inspected units is valid; return a null rate, not a guess or a question.')
    c['payload']['rows']=[dict(inspection='zero',version=1,lot='L0',checked=0,failed=0)];cases.append(c)
    return cases


if __name__=='__main__':
    root=Path(__file__).parent
    (root/'cases.json').write_text(json.dumps(make_cases(),ensure_ascii=False,indent=2)+'\n')
    (root/'sources').mkdir(exist_ok=True)
    (root/'sources/metric-definition.json').write_text(json.dumps({'id':'metric-definition','authority':'task_owner','status':'approved','metric':'macro_percent','zero_rule':'exclude_zero_checked_inspections; null if no eligible rate'},indent=2)+'\n')
    print('Created 12 public vignettes. No oracle execution.')
