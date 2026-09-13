"""Controller-only arithmetic oracle. Does not import E002, choices or executor."""
import copy
from fractions import Fraction


def expected(case, documents):
    p=case['policy']; metric=p['metric']
    if metric is None:
        if case['documents']:
            metric=documents[case['documents'][0]['id']]['metric']
        else:
            return {'status':'ASK','key':'metric_definition','rows':None}
    if p['checked_unit']=='carton' and p.get('units_per_carton') is None:
        return {'status':'ASK','key':'units_per_carton','rows':None}
    lots={}
    if metric=='distinct_unit_percent':
        register={}
        for u in case['unit_register']:
            if u['unit_id'] in register and register[u['unit_id']]!=u['lot']:raise ValueError('UNIT_LOT_CONFLICT')
            register[u['unit_id']]=u['lot']
        bad={e['unit_id'] for e in case['defect_events']}
        if not bad<=register.keys():raise ValueError('UNINSPECTED_DEFECT')
        for uid,lot in register.items():
            v=lots.setdefault(lot,[0,0,[]]);v[0]+=1;v[1]+=int(uid in bad)
    else:
        rs=copy.deepcopy(case['payload']['rows']);rename=p.get('column_map',{})
        rs=[{rename.get(k,k):v for k,v in r.items()} for r in rs]
        ids={r['inspection'] for r in rs}
        for identity in sorted(ids):
            candidates=[r for r in rs if r['inspection']==identity]
            if p['selection']=='EFFECTIVE_V2':
                candidates=[r for r in candidates if r['approved'] and r['effective_day']<=case['payload']['as_of_day']]
            if not candidates:continue
            current_version=max(r['version'] for r in candidates)
            current=[r for r in candidates if r['version']==current_version]
            r=current[0]
            if any(q!=r for q in current):raise ValueError('CURRENT_CONFLICT')
            if p['selection']=='EFFECTIVE_V2' and r['withdrawn']:continue
            n=r['checked'];f=r['failed']
            if p['checked_unit']=='carton':n*=p['units_per_carton'][identity]
            if type(n) is not int or type(f) is not int or not 0<=f<=n:raise ValueError('COUNTS')
            v=lots.setdefault(r['lot'],[0,0,[]]);v[0]+=n;v[1]+=f
            if n:v[2].append(Fraction(f,n))
    out=[]
    for lot,(n,f,rates) in sorted(lots.items()):
        if metric=='macro_percent':ratio=sum(rates,Fraction(0))/len(rates) if rates else None
        else:ratio=Fraction(f,n) if n else None
        scale=1000000 if metric=='pooled_ppm' else 100
        value=None if ratio is None else round(float(ratio*scale),6)
        out.append({'lot':lot,'checked':n,'failed':f,'value':value})
    return {'status':'COMPLETE','metric':metric,'rows':out}


def ambiguity_witnesses(cases,documents):
    """Alternative synthetic worlds, NOT supplied facts or human responses."""
    by={c['id']:c for c in cases};out={}
    for key,field,values in [('SJ04','units_per_carton',[{'x':5},{'x':10}]),('SJ10','metric',['pooled_percent','macro_percent'])]:
        alternatives=[]
        for value in values:
            c=copy.deepcopy(by[key]);c['policy'][field]=value
            alternatives.append({'hypothetical_fact':value,'output':expected(c,documents)})
        out[key]={'alternatives':alternatives,'answers_differ':alternatives[0]['output']!=alternatives[1]['output']}
    return out
