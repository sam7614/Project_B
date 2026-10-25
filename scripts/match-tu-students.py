"""Match synthetic students to source curriculum; write Google-Sheets-ready tables."""
from pathlib import Path
import argparse, collections, hashlib, json, random

FIELDS=['active','synthetic','id','name','department','grade','module','moduleCreditsEarned','moduleCreditsRequired','creditsEarned','totalCredits','gpa','attendance','status','careerGoal','midtermScore','finalScore','assignmentScore','projectScore','participationScore','socialScore','lastConsultation','scenario','reflection','planChangeReason','prerequisiteMet','plannedSemesterCredits','selectedModules','college','departmentId','moduleId','curriculumVersion','gradedCredits']
def main():
    p=argparse.ArgumentParser();p.add_argument('snapshot');p.add_argument('--catalog',default='research/data/tu-2026/curriculum.json');p.add_argument('--out',default='.synthetic-data/tu-matched');args=p.parse_args()
    catalog=json.loads(Path(args.catalog).read_text(encoding='utf-8'));snapshot=json.loads(Path(args.snapshot).read_text(encoding='utf-8'));students=snapshot['students'];assert len(students)==1000
    rng=random.Random(20261025);out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    tables={};tables['Colleges']={'headers':['collegeId','college','sourceUrl'],'rows':catalog['colleges']}
    tables['Departments']={'headers':['departmentId','collegeId','department','sourceUrl'],'rows':catalog['departments']}
    tables['Modules']={'headers':['moduleId','departmentId','module','moduleType','publishedCredits','roadmapCredits','matchingEligible','sourceUrl'],'rows':catalog['modules']}
    tables['ModuleCourses']={'headers':['courseRowId','moduleId','courseNameRaw','credits','hours','year','semester','choiceGroup','teachingMode','sourceUrl'],'rows':catalog['moduleCourses']}
    enrollments=[];student_rows=[];summaries=[]
    for i,old in enumerate(students):
        college=catalog['colleges'][i%4];local=i//4;depts=[d for d in catalog['departments'] if d['collegeId']==college['collegeId']];dep=depts[local%len(depts)]
        pool=[m for m in catalog['modules'] if m['departmentId']==dep['departmentId'] and m['matchingEligible']];assert pool
        module=pool[(local//len(depts))%len(pool)];courses=[c for c in catalog['moduleCourses'] if c['moduleId']==module['moduleId']]
        sid=old['id'];grade=old['grade'];earned=0;weighted=0;graded=0;records=[]
        for course in courses:
            if course['year']>grade: status='planned'
            elif course['year']==grade and course['semester']==2:status='in-progress' if rng.random()<0.85 else 'planned'
            else:status=rng.choices(['completed','failed','in-progress'],[0.85,0.1,0.05])[0]
            point=rng.choice([2.0,2.5,3.0,3.5,4.0,4.5]) if status=='completed' else 0 if status=='failed' else None
            cr=course['credits'];e=cr if status=='completed' else 0;g=cr if status in ('completed','failed') else 0;earned+=e;graded+=g;weighted+=g*(point or 0)
            n=len(enrollments)+2
            enrollments.append(dict(studentId=sid,courseRowId=course['courseRowId'],moduleId=module['moduleId'],courseNameRaw=course['courseNameRaw'],credits=cr,year=course['year'],semester=course['semester'],status=status,gradePoint=point,
                earnedCredits=f'=IF(H{n}="completed",E{n},0)',weightedPoints=f'=IF(OR(H{n}="completed",H{n}="failed"),E{n}*IF(I{n}="",0,I{n}),0)',gradedCredits=f'=IF(OR(H{n}="completed",H{n}="failed"),E{n},0)',synthetic=True))
            records.append(dict(courseRowId=course['courseRowId'],status=status,gradePoint=point))
        row={k:old.get(k) for k in FIELDS};row.update(active=True,synthetic=True,college=college['college'],department=dep['department'],departmentId=dep['departmentId'],module=module['module'],moduleId=module['moduleId'],moduleCreditsRequired=module['publishedCredits'],curriculumVersion=catalog['version'],careerGoal='[합성] '+dep['department']+' 관련 진로 탐색',selectedModules=module['module'])
        row.update(moduleCreditsEarned=earned,creditsEarned=earned,totalCredits=module['publishedCredits'],gpa=round(weighted/graded,2) if graded else 0,gradedCredits=graded)
        summaries.append({**old,**row,'progress':round(earned/module['publishedCredits']*100),'generalProgress':round(earned/module['publishedCredits']*100),'courseRecords':records})
        student_rows.append(row)
    n=len(enrollments)+1
    for i,row in enumerate(student_rows,2):
        row['moduleCreditsEarned']=f'=SUMIF(StudentCourses!$A$2:$A${n},C{i},StudentCourses!$J$2:$J${n})'
        row['creditsEarned']=f'=H{i}';row['totalCredits']=f'=I{i}'
        row['gradedCredits']=f'=SUMIF(StudentCourses!$A$2:$A${n},C{i},StudentCourses!$L$2:$L${n})'
        row['gpa']=f'=IF(AG{i}=0,0,ROUND(SUMIF(StudentCourses!$A$2:$A${n},C{i},StudentCourses!$K$2:$K${n})/AG{i},2))'
    tables['StudentCourses']={'headers':['studentId','courseRowId','moduleId','courseNameRaw','credits','year','semester','status','gradePoint','earnedCredits','weightedPoints','gradedCredits','synthetic'],'rows':enrollments}
    tables['Students']={'headers':FIELDS,'rows':student_rows}
    formula_fields={'StudentCourses':['earnedCredits','weightedPoints','gradedCredits'],'Students':['moduleCreditsEarned','creditsEarned','totalCredits','gpa','gradedCredits']}
    for name,table in tables.items():
        table['formulaFields']=formula_fields.get(name,[]);(out/f'{name}.json').write_text(json.dumps(table,ensure_ascii=False)+'\n',encoding='utf-8')
    (out/'student-summaries.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest=dict(version='tu-matched-synthetic-v1',seed=20261025,asOf='2026-10-25',studentCount=len(students),empiricalParticipants=0,studentCourseRows=len(enrollments),moduleCoverage=len({s['moduleId'] for s in summaries}),
        byCollege=dict(collections.Counter(s['college'] for s in summaries)),byDepartment=dict(collections.Counter(s['department'] for s in summaries)),sourceUrl=catalog['sourceUrl'],sourceHtmlSha256=catalog['sourceHtmlSha256'],
        limits=['One primary module per synthetic student; not a full university transcript or graduation audit.','Total credits/GPA refer only to represented module-course records.','Choice-group rows are a single requirement slot; no official course code or graduation selection policy is invented.','Offering year/semester are source facts; enrollments/status/grade points are simulated; 4.5 grade scale is a simulation assumption.'])
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(manifest,ensure_ascii=False))
if __name__=='__main__':main()
