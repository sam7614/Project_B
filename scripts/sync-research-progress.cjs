'use strict';
// Build the shared schedule snapshot after reviewing evidence; never infer completion from dates.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..'),read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const source=read('research/progress-source.json'),manifest=read('research/versions/manifest.json');
if(source.basedOnReportVersion!==manifest.currentVersion)throw Error('Review progress-source.json against the new report version before publishing');
if(!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+09:00$/.test(source.reviewedAt))throw Error('reviewedAt must be an explicit Korean-time review timestamp');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8'),match=html.match(/const phases=([\s\S]*?);\s*phases\.forEach/);
if(!match)throw Error('Schedule phases not found');
const phases=vm.runInNewContext('('+match[1]+')'),ids=new Set(phases.flatMap(p=>p.items.map(i=>i.id)));
const allowed=new Set(['planned','in_progress','blocked','complete','unverified']);
const check=item=>{if(!allowed.has(item.status)||typeof item.note!=='string')throw Error('Invalid progress item');if(item.status==='complete'&&!item.evidence?.length)throw Error('Completion requires evidence');for(const e of item.evidence||[]){if(!e.label||!e.url||!(/^(research\/[a-zA-Z0-9/._-]+\.(md|json)|https:\/\/(docs\.google\.com|github\.com|project-b-lemon\.vercel\.app|micro-degree-student\.vercel\.app)\/[^\s]+)$/.test(e.url)))throw Error('Invalid evidence link');if(e.url.startsWith('research/')&&!fs.existsSync(path.join(root,e.url)))throw Error('Missing evidence file '+e.url);}};
for(const[id,item]of Object.entries(source.tasks)){if(!ids.has(id))throw Error('Unknown schedule task '+id);check(item);}
source.deliverables.forEach(check);
if(!allowed.has(source.reportStatus))throw Error('Explicit reportStatus required');
const date=source.reviewedAt.slice(0,10),tasks={};for(const p of phases)for(const i of p.items)tasks[i.id]=source.tasks[i.id]||{status:i.date<date?'unverified':'planned',note:i.date<date?'실제 완료 증빙을 아직 대조하지 않았습니다.':'계획 일정입니다. 실제 수행 후 근거와 상태를 갱신합니다.',evidence:[]};
const snapshot=manifest.snapshots.find(s=>s.version===manifest.currentVersion);if(!snapshot)throw Error('Current report snapshot missing');
const output={schemaVersion:1,reviewedAt:source.reviewedAt,report:{version:manifest.currentVersion,status:source.reportStatus,note:source.reportNote,url:source.reportUrl,snapshot:snapshot.path},dailyReportUrl:source.dailyReportUrl,scope:source.scope,actualParticipants:source.actualParticipants,deliverables:source.deliverables,tasks};
fs.writeFileSync(path.join(root,'research/progress.json'),JSON.stringify(output,null,2)+'\n');
console.log('Shared research progress: '+ids.size+' tasks / '+source.deliverables.length+' deliverables / '+manifest.currentVersion);
