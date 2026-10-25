"""Extract factual curriculum tables from TU's 2026 public guidebook (stdlib only)."""
from html.parser import HTMLParser
from pathlib import Path
import argparse, hashlib, json, re

COLLEGES = ['보건복지교육대학', '뷰티예술대학', '건축·디자인대학', 'ICT융합대학']
SOURCE = 'https://www.tu.ac.kr/web/module-guidebook.html'
class Node:
    def __init__(self, tag='', attrs=(), parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []
    def walk(self):
        yield self
        for item in self.children:
            if isinstance(item, Node): yield from item.walk()
    def has(self, cls): return cls in self.attrs.get('class', '').split()
    def find(self, cls): return next((n for n in self.walk() if n.has(cls)), None)
    def text(self, skip=()):
        return ''.join(x if isinstance(x,str) else '' if any(x.has(c) for c in skip) else x.text(skip) for x in self.children)
class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.root=Node(); self.current=self.root
    def handle_starttag(self, tag, attrs):
        node=Node(tag,attrs,self.current);self.current.children.append(node)
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}: self.current=node
    def handle_endtag(self, tag):
        node=self.current
        while node.parent and node.tag!=tag:node=node.parent
        if node.parent:self.current=node.parent
    def handle_data(self,data):self.current.children.append(data)
def clean(text):return re.sub(r'\s+',' ',text).strip()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('html');parser.add_argument('--out',default='research/data/tu-2026');args=parser.parse_args()
    raw=Path(args.html).read_bytes();tree=Tree();tree.feed(raw.decode('utf-8'))
    nodes=list(tree.root.walk());ids={n.attrs['id']:n for n in nodes if 'id' in n.attrs}
    colleges=[];departments=[];modules=[];courses=[];issues=[]
    for ci,college in enumerate(COLLEGES,1):
        college_id=f'TU2026-C{ci:02}'
        colleges.append(dict(collegeId=college_id,college=college,sourceUrl=SOURCE))
        section=next(n for n in nodes if n.has('w-col') and n.attrs.get('data-c')==college)
        for di,dep in enumerate([n for n in section.walk() if n.has('w-dept')],1):
            name=clean(next(n for n in dep.walk() if n.tag=='h3').text());dep_id=f'{college_id}-D{di:02}'
            departments.append(dict(departmentId=dep_id,collegeId=college_id,college=college,department=name,idKind='local-not-official',sourceUrl=SOURCE))
            for link in (n for n in dep.walk() if n.has('w-item')):
                mid=link.attrs['href'].lstrip('#');article=ids[mid];hero=article.find('hero')
                title=clean(next(n for n in hero.walk() if n.tag=='h1').text());stats=article.find('stats');stat=next(n for n in stats.walk() if n.has('stat'))
                credits=float(clean(stat.find('num').text()));roadmap=article.find('timeline')
                if not roadmap:issues.append(dict(moduleId=mid,issue='missing-roadmap'));continue
                years=[clean(n.text()) for n in roadmap.children if isinstance(n,Node) and n.has('yearhead')]
                cols=[n for n in roadmap.children if isinstance(n,Node) and n.has('semcol')]
                entries=[]
                for si,sem in enumerate(cols):
                    year=years[si//2] if si//2<len(years) else None;semester=clean(sem.find('semlabel').text())
                    for course in (n for n in sem.walk() if n.has('course')):
                        label=clean(course.text(skip=('meta','tag')));meta=clean(course.find('meta').text()) if course.find('meta') else ''
                        cm=re.search(r'(\d+(?:\.\d+)?)\s*학점',meta);hours=re.search(r'(\d+(?:\.\d+)?)\s*시수',meta)
                        row=dict(courseRowId=f'{mid}-R{len(entries)+1:02}',moduleId=mid,departmentId=dep_id,collegeId=college_id,
                            college=college,department=name,module=title,courseNameRaw=label,
                            credits=float(cm.group(1)) if cm else None,hours=float(hours.group(1)) if hours else None,
                            yearRaw=year,year=int(re.search(r'\d+',year).group()) if year and re.search(r'\d+',year) else None,
                            semester=int(re.search(r'\d+',semester).group()) if re.search(r'\d+',semester) else None,
                            choiceGroup=bool(course.find('tag') or re.search(r'택\s*\d|중\s*\d|선택',label)),
                            teachingMode='practice' if course.has('practice') else 'mixed' if course.has('mixed') else 'theory',
                            idKind='local-module-roadmap-row-not-official-course-code',sourceUrl=SOURCE+'#'+mid)
                        entries.append(row)
                total=sum(c['credits'] or 0 for c in entries);complete=bool(entries) and all(c['credits'] is not None and c['year'] is not None and c['semester'] in (1,2) for c in entries)
                eligible=complete and abs(total-credits)<0.001
                module=dict(moduleId=mid,collegeId=college_id,departmentId=dep_id,college=college,department=name,
                    module=title,moduleType=link.attrs.get('data-t'),publishedCredits=credits,roadmapCredits=total,
                    roadmapRowCount=len(entries),matchingEligible=eligible,
                    selectionPolicy='all-roadmap-slots; choice-group counts as one slot; no official graduation audit',
                    sourceUrl=SOURCE+'#'+mid)
                modules.append(module);courses.extend(entries)
                if not eligible:issues.append(dict(moduleId=mid,issue='roadmap-incomplete-or-credit-mismatch',publishedCredits=credits,roadmapCredits=total))
    assert len({m['moduleId'] for m in modules})==len(modules),'duplicate module IDs'
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    result=dict(version='tu-2026-four-colleges-v1',retrievedOn='2026-10-25',sourceUrl=SOURCE,sourceHtmlSha256=hashlib.sha256(raw).hexdigest(),
        notes=['Names, credits, schedule and anchor IDs are source facts. Local keys are not official university codes.','Module descriptions and career recommendation prose are not reproduced.','Choice rows preserve source wording; full degree audit rules are not inferred.'],
        colleges=colleges,departments=departments,modules=modules,moduleCourses=courses,issues=issues)
    (out/'curriculum.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(colleges=len(colleges),departments=len(departments),modules=len(modules),courseRows=len(courses),eligibleModules=sum(m['matchingEligible'] for m in modules),issues=issues,
        byCollege={c:dict(departments=sum(d['college']==c for d in departments),modules=sum(m['college']==c for m in modules)) for c in COLLEGES}),ensure_ascii=False))
if __name__=='__main__':main()
