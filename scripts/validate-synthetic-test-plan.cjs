'use strict';
const fs=require('node:fs');
function validate(plan,corpus,requirements){
  const fail=m=>{throw Error(m)};
  if(plan.synthetic!==true||plan.actualParticipants!==0||plan.productExecution!=='not_run')fail('Evidence boundary: preparation only');
  const answers=new Map(corpus.profiles.flatMap(p=>p.answers.map(a=>[a.segmentId,a]))),reqs=new Map(requirements.requirements.map(r=>[r.id,r])),ids=new Set();
  if(plan.cases.length!==16)fail('Expected sixteen prepared cases');
  for(const c of plan.cases){
    if(ids.has(c.id))fail('Duplicate case');ids.add(c.id);
    const r=reqs.get(c.requirement);if(!r)fail('Unknown requirement');
    if(!['positive','negative'].includes(c.polarity)||c.status!=='not_run'||!c.input||!c.expected||!c.evidenceToCapture)fail('Missing preparation or execution boundary');
    if(!c.tasks.length||c.tasks.some(t=>!/^T0[1-8]$/.test(t)))fail('Unknown task');
    if(!c.segments.length||c.segments.some(s=>!answers.has(s)||!r.evidence.includes(s)||!answers.get(s).codes.includes(r.theme)))fail('Broken response/theme trace');
  }
  for(const r of reqs.keys())for(const polarity of ['positive','negative'])if(!plan.cases.some(c=>c.requirement===r&&c.polarity===polarity))fail('Missing polarity coverage');
  return {preparedCases:16,requirements:8,actualParticipants:0,productCasesExecuted:0,scope:'document traceability only'};
}
function read(path){return JSON.parse(fs.readFileSync(path,'utf8'));}
if(require.main===module){console.log(JSON.stringify(validate(read('research/data/synthetic-advising-test-plan-v1.json'),read('research/data/synthetic-expert-scenarios-v1.json'),read('research/data/synthetic-expert-requirements-v1.json'))));}
module.exports={validate};
