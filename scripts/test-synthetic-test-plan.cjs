'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict'),{test}=require('node:test'),{validate}=require('./validate-synthetic-test-plan.cjs');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8')),base=read('research/data/synthetic-advising-test-plan-v1.json'),corpus=read('research/data/synthetic-expert-scenarios-v1.json'),reqs=read('research/data/synthetic-expert-requirements-v1.json');
test('prepared matrix preserves actual0/executed0',()=>assert.deepEqual(validate(base,corpus,reqs),{preparedCases:16,requirements:8,actualParticipants:0,productCasesExecuted:0,scope:'document traceability only'}));
for(const [name,mutate] of [
 ['reject simulated participation as actual',p=>p.actualParticipants=9],
 ['reject unexecuted plan labelled passed',p=>p.cases[0].status='passed'],
 ['reject missing negative coverage',p=>p.cases[1].polarity='positive'],
 ['reject invented response reference',p=>p.cases[0].segments=['SYN-E99-Q01']],
 ['reject cross-theme attribution',p=>p.cases[0].segments=['SYN-E07-Q06']],
 ['reject duplicate case identifiers',p=>p.cases[1].id=p.cases[0].id],
 ['reject unsupported product task',p=>p.cases[0].tasks=['T99']]
])test(name,()=>{const p=structuredClone(base);mutate(p);assert.throws(()=>validate(p,corpus,reqs));});
