"""Execute committed decisions; no case-ID router, oracle or model API."""
import copy
from collections import defaultdict
from decimal import Decimal, localcontext
from experiments.E002.capability import adapted_reuse, _select


def rate(f,n,scale=100):
    if n==0:return None
    with localcontext() as ctx:
        ctx.prec=40
        return float((Decimal(f)*scale/Decimal(n)).quantize(Decimal('0.000001')))


def execute(case,choice):
    c=copy.deepcopy(case);p=c['payload'];route=choice['route']
    if route=='ask':
        return {'status':'ASK','key':choice['key'],'question':choice['question'],'rows':None}
    if route=='read_document':
        return {'status':'READ_REQUIRED','document_id':choice['document_id'],'rows':None}
    for op in choice.get('operations',[]):
        if op=='rename_columns':
            mapping=c['policy']['column_map']
            if len(set(mapping.values()))!=len(mapping):raise ValueError('NON_BIJECTIVE_MAP')
            p['rows']=[{mapping.get(k,k):v for k,v in r.items()} for r in p['rows']]
        elif op=='normalize_cartons':
            for r in p['rows']:
                factor=c['policy']['units_per_carton'][r['inspection']]
                if type(factor) is not int or factor<=0:raise ValueError('INVALID_UNIT_FACTOR')
                r['checked']*=factor
        elif op=='bind_authoritative_contract':p['contract']=c['policy']['selection']
        else:raise ValueError('UNKNOWN_OPERATION')
    if route=='e002':
        response=adapted_reuse(p)
        if response['status']!='COMPLETE':return response
        ppm=choice.get('output')=='ppm_from_counts'
        rows=[{'lot':r['lot'],'checked':r['checked'],'failed':r['failed'],
               'value':rate(r['failed'],r['checked'],1000000) if ppm else r['defect_percent']} for r in response['rows']]
        metric='pooled_ppm' if ppm else 'pooled_percent'
    elif route=='macro':
        groups=defaultdict(list)
        for r in _select(p,p['contract']=='EFFECTIVE_V2'):groups[r['lot']].append(r)
        rows=[]
        with localcontext() as ctx:
            ctx.prec=40
            for lot,rs in groups.items():
                ratios=[Decimal(r['failed'])/Decimal(r['checked']) for r in rs if r['checked']]
                val=float((sum(ratios)/len(ratios)*100).quantize(Decimal('0.000001'))) if ratios else None
                rows.append({'lot':lot,'checked':sum(r['checked'] for r in rs),'failed':sum(r['failed'] for r in rs),'value':val})
        metric='macro_percent'
    elif route=='distinct_units':
        groups=defaultdict(set);registry={}
        for r in c['unit_register']:
            if r['unit_id'] in registry and registry[r['unit_id']]!=r['lot']:raise ValueError('CONFLICTING_UNIT_LOT')
            registry[r['unit_id']]=r['lot'];groups[r['lot']].add(r['unit_id'])
        defective=set(e['unit_id'] for e in c['defect_events'])
        if not defective<=registry.keys():raise ValueError('DEFECT_NOT_INSPECTED')
        rows=[{'lot':lot,'checked':len(ids),'failed':len(ids & defective),'value':rate(len(ids & defective),len(ids))} for lot,ids in groups.items()]
        metric='distinct_unit_percent'
    else:raise ValueError('UNKNOWN_ROUTE')
    return {'status':'COMPLETE','metric':metric,'rows':sorted(rows,key=lambda r:r['lot'])}
