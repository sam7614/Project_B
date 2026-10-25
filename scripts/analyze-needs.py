"""Development-only paired needs summary. No empirical inference or student-grade proxy."""
from pathlib import Path
import argparse,csv,json,math,statistics,hashlib

def analyze(rows):
    required={'respondent_id','role','item_id','importance','current','synthetic'}
    groups={};seen=set();roles=set();identifiers=set()
    for n,r in enumerate(rows,2):
        if not required.issubset(r):raise ValueError('Missing required CSV headers')
        if r['synthetic'].lower()!='true':raise ValueError('This development adapter accepts synthetic fixtures only')
        if not r['respondent_id'].startswith('SYN-Q-')or not r['item_id'].strip():raise ValueError(f'Invalid synthetic keys at row{n}')
        if r['role']not in ('student','faculty','developer-test'):raise ValueError('Unknown role')
        key=(r['respondent_id'],r['item_id']);roles.add(r['role']);identifiers.add(r['respondent_id'])
        if key in seen:raise ValueError('Duplicate respondent/item pair')
        seen.add(key);g=groups.setdefault(r['item_id'],{'pairs':[],'excluded':0})
        if r['importance']==''or r['current']=='':g['excluded']+=1;continue
        a,b=float(r['importance']),float(r['current'])
        if not all(math.isfinite(x)and 1<=x<=5 and x.is_integer()for x in (a,b)):raise ValueError('Scores must be integers1..5')
        g['pairs'].append((a,b))
    if len(roles)!=1:raise ValueError('Analyze each role separately; mixed roles are not pooled')
    if not groups:raise ValueError('Empty input')
    items=[]
    for k,g in sorted(groups.items()):
        pairs=g['pairs'];n=len(pairs)
        if n<2:raise ValueError(f'{k}: at least2 complete pairs needed for this calculation fixture')
        a=statistics.mean(x for x,y in pairs);b=statistics.mean(y for x,y in pairs);diffs=[x-y for x,y in pairs];gap=statistics.mean(diffs);sd=statistics.stdev(diffs)
        items.append(dict(item_id=k,n=n,excluded_missing_pairs=g['excluded'],mean_importance=a,mean_current=b,mean_gap=gap,borich_mwds=a*gap,paired_t=gap/(sd/math.sqrt(n))if sd else None,df=n-1,p_value=None,inference_status='not-run; statistic-only development fixture'if sd else 'zero difference variance; no finite paired_t',difference_sd=sd))
    x=statistics.mean(i['mean_importance']for i in items);y=statistics.mean(i['mean_gap']for i in items)
    for i in items:
        i['lf_quadrant']=('H'if i['mean_importance']>x else 'L')+('H'if i['mean_gap']>y else 'L');i['lf_boundary']=math.isclose(i['mean_importance'],x,abs_tol=1e-10)or math.isclose(i['mean_gap'],y,abs_tol=1e-10)
        i['borich_rank']=1+sum(j['borich_mwds']>i['borich_mwds']for j in items)
    h=sum(i['lf_quadrant']=='HH'and not i['lf_boundary']for i in items)
    cutoff=sorted((i['borich_mwds']for i in items),reverse=True)[h-1]if h else None
    for i in items:i['candidate_overlap']=bool(h and i['lf_quadrant']=='HH'and not i['lf_boundary']and i['borich_mwds']>=cutoff)
    return dict(version='needs-readiness-v1',purpose='synthetic calculation fixture only; not empirical needs or feature prioritization',real_participants=0,synthetic_case_ids=len(identifiers),role=next(iter(roles)),lf_axis_order='importance, importance-minus-current',lf_thresholds=dict(mean_importance=x,mean_gap=y),hh_count=h,borich_cutoff=cutoff,items=items)

def main():
    p=argparse.ArgumentParser();p.add_argument('csv_path');p.add_argument('--out',default='.synthetic-data/needs-readiness');args=p.parse_args()
    source=Path(args.csv_path);rows=list(csv.DictReader(source.read_text(encoding='utf-8-sig').splitlines()));result=analyze(rows);result['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);(out/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with(out/'items.csv').open('w',encoding='utf-8-sig',newline='')as f:
        w=csv.DictWriter(f,fieldnames=list(result['items'][0]));w.writeheader();w.writerows(result['items'])
    print(json.dumps({'items':len(result['items']),'real_participants':0,'p_values':'not computed','output':str(out)}))
if __name__=='__main__':main()
