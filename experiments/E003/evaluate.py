"""Controller-only evaluation of outputs, not a preferred intervention label."""
import copy, hashlib, json, math, platform, sqlite3, time
from collections import Counter
from pathlib import Path
from experiments.E003.oracle import expected, ambiguity_witnesses
from experiments.E003.actions import execute


def encoded(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def sha(x):return hashlib.sha256(encoded(x)).hexdigest()


def grade(actual,wanted):
    if not isinstance(actual,dict) or actual.get('status')!=wanted['status']:return False
    if wanted['status']=='ASK':
        return (actual.get('key')==wanted['key'] and actual.get('rows') is None
                and isinstance(actual.get('question'),str) and bool(actual['question'].strip()))
    if set(actual)!={'status','metric','rows'} or actual['metric']!=wanted['metric']:return False
    rows=actual.get('rows')
    if not isinstance(rows,list) or len(rows)!=len(wanted['rows']):return False
    if any(not isinstance(r,dict) or set(r)!={'lot','checked','failed','value'} for r in rows):return False
    if len({r['lot'] for r in rows})!=len(rows):return False
    for a,b in zip(sorted(rows,key=lambda r:r['lot']),wanted['rows']):
        if a['lot']!=b['lot']:return False
        if any(type(a[k]) is not int or a[k]!=b[k] for k in ['checked','failed']):return False
        if b['value'] is None:
            if a['value'] is not None:return False
        elif (type(a['value']) not in [int,float] or not math.isfinite(a['value']) or abs(a['value']-b['value'])>1e-6):return False
    return True


def check_freeze(root):
    m=json.loads((root/'INPUT_FREEZE.json').read_text())
    repo=root.parents[1]
    for name,pin in m['source_hashes'].items():
        if hashlib.sha256((repo/name).read_bytes()).hexdigest()!=pin:raise ValueError('INPUT_ORACLE_PIN_MISMATCH:'+name)
    return m


def run(root,out):
    check_freeze(root)
    cases=json.loads((root/'cases.json').read_text())
    initial=json.loads((root/'INITIAL_CHOICES.json').read_text())
    observation=json.loads((root/'SOURCE_OBSERVATION.json').read_text())
    choices={c['id']:c for c in initial['choices']}
    if len(choices)!=12 or set(choices)!={c['id'] for c in cases}:raise ValueError('CHOICE_COVERAGE')
    docbytes=(root/'sources/metric-definition.json').read_bytes()
    if hashlib.sha256(docbytes).hexdigest()!=observation['document_sha256']:raise ValueError('DOC_PIN')
    doc=json.loads(docbytes)
    if doc!=observation['observation']:raise ValueError('OBSERVATION_MISMATCH')
    if choices[observation['case_id']]['route']!='read_document':raise ValueError('UNREQUESTED_READ')
    choices[observation['case_id']]=observation['followup_choice']
    documents={doc['id']:doc};records=[]
    for c in cases:
        before=sha(c);started=time.perf_counter();error=None
        try:actual=execute(c,choices[c['id']])
        except Exception as exc:actual=None;error=type(exc).__name__+': '+str(exc)
        elapsed=time.perf_counter()-started
        wanted=expected(c,documents)
        mutated=sha(c)!=before
        records.append({'id':c['id'],'choice':choices[c['id']],'input_sha256':before,
                        'output':actual,'expected':wanted,'correct_handling':grade(actual,wanted) and not mutated,
                        'input_mutation':mutated,'exception':error,'artifact_seconds':elapsed})
    # These deliberately wrong substitutes are sensitivity checks, NOT assistant decisions.
    by={c['id']:c for c in cases};want={r['id']:r['expected'] for r in records};mutants={}
    bad=execute(by['SJ06'],{'route':'e002'})
    bad['metric']='pooled_ppm'
    for r in bad['rows']:r['value']=round(r['value']*10000,6) if r['value'] is not None else None
    mutants['scale_rounded_percent']=not grade(bad,want['SJ06'])
    for label,cid,ch in [('pooled_for_macro','SJ07',{'route':'e002'}),('events_for_units','SJ08',{'route':'e002'}),('obsolete_contract','SJ11',{'route':'e002'}),('unnecessary_human_question','SJ09',{'route':'ask','key':'metric_definition','question':'Which metric?'})]:
        mutants[label]=not grade(execute(by[cid],ch),want[cid])
    guessed=copy.deepcopy(by['SJ04']);guessed['policy']['units_per_carton']={'x':10}
    mutants['guess_carton_capacity']=not grade(execute(guessed,{'route':'e002','operations':['normalize_cartons']}),want['SJ04'])
    summary={'case_decisions':12,'followup_decisions':1,'single_interactive_contexts':1,
             'correct_completed':sum(r['correct_handling'] and r['output']['status']=='COMPLETE' for r in records),
             'correctly_pending_human_fact':sum(r['correct_handling'] and r['output']['status']=='ASK' for r in records),
             'incorrect_or_unresolved':sum(not r['correct_handling'] for r in records),
             'input_mutations':sum(r['input_mutation'] for r in records),'exceptions':sum(r['exception'] is not None for r in records),
             'synthetic_document_reads':1,'proposed_human_questions':sum(ch['route']=='ask' for ch in choices.values()),
             'actual_human_responses':0,'independent_model_trials':0,
             'new_external_model_api_calls':0,'human_total_active_seconds':None,'interactive_model_tokens':None,'total_cost':None,
             'final_intervention_counts':dict(Counter(c['intervention'] for c in choices.values()))}
    result={'schema':'GDSSA_E003_OUTPUT_STUDY_V1','evidence_class':'OPEN_LABEL_CURRENT_ASSISTANT_DECISION_AND_ARTIFACT_STUDY',
            'summary':summary,'records':records,'negative_control_rejections':mutants,
            'ambiguity_witnesses':ambiguity_witnesses(cases,documents),'python':platform.python_version(),'sqlite':sqlite3.sqlite_version,
            'decision_sha256':sha(initial),'observation_sha256':sha(observation),'casepack_sha256':sha(cases),
            'deterministic_outputs_sha256':sha([{k:v for k,v in r.items() if k!='artifact_seconds'} for r in records]),
            'claim_boundary':'One same-context, self-authored diagnostic session, not independent model efficacy, causal human-method comparison or cost improvement.'}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'summary':summary,'negative_control_rejections':mutants,'output_commitment':result['deterministic_outputs_sha256']},indent=2))
    return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
    r=run(Path(__file__).parent,Path(a.out))
    raise SystemExit(int(r['summary']['incorrect_or_unresolved']>0))
