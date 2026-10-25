'use strict';
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const dir = path.resolve(process.argv[2] || '.synthetic-data');
const read = name => JSON.parse(fs.readFileSync(path.join(dir,name),'utf8'));
const manifest = read('manifest.json');
const rows = read('students.json');
const demo = read('demo-students.json');
assert.equal(rows.length,manifest.count);
assert.equal(new Set(rows.map(r=>r.id)).size,rows.length);
assert.equal(manifest.empiricalParticipants,0);
for (const row of rows) {
  assert.equal(row.synthetic,true);
  assert.match(row.id,/^SYN-\d{7}$/);
  assert.match(row.email,/@example\.invalid$/);
  assert.equal(row.phone,'연락처 없음 (합성)');
  assert(row.gpa >= 0 && row.gpa <= 4.5);
  assert(row.creditsEarned >= 0 && row.creditsEarned <= row.totalCredits);
  assert(row.moduleCreditsEarned <= row.moduleCreditsRequired);
  assert.equal(row.progress,Math.round(row.moduleCreditsEarned / row.moduleCreditsRequired * 100));
  assert.equal(row.generalProgress,Math.round(row.creditsEarned / row.totalCredits * 100));
  for (const key of ['progress','attendance','midtermScore','finalScore','assignmentScore','projectScore','participationScore','socialScore']) assert(row[key]>=0&&row[key]<=100);
  for (const consultation of row.consultations) { assert(consultation.synthetic); assert(consultation.date <= manifest.referenceDate); }
  assert.equal(row.missingFields.includes('reflection'),row.reflection === null);
  assert.equal(row.missingFields.includes('careerGoal'),row.careerGoal === '');
}
assert.equal(demo.length,256);
assert.equal(new Set(demo.map(r=>`${r.grade}|${r.module}|${r.scenario}`)).size,256);
assert.equal(new Set(demo.map(r=>r.scenario)).size,16);
for (const [name,meta] of Object.entries(manifest.files)) {
  const bytes=fs.readFileSync(path.join(dir,name));
  assert.equal(bytes.length,meta.bytes);
  assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),meta.sha256);
}
assert.equal(read('negative-cases.json').cases.length,6);
console.log(JSON.stringify({result:'PASS',synthetic:true,records:rows.length,demo:demo.length,scenarioGradeModuleCombinations:256,negativeFixtures:6,scope:'data constraints and provenance only; not app behavior, fidelity to real learners, fairness or efficacy'}));
