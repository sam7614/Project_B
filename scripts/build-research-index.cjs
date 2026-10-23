// Rebuild the public document index; manuscript content stays in Markdown files.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const context = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(root, 'research-schema.js'), 'utf8'), context);
const sections = context.window.ResearchSchema.sections;
const folders = ['01-overview','02-methods','03-results','04-discussion','05-summaries','06-references'];
const groups = [...new Set(sections.map(s => s.group))];
const documents = sections.map(s => {
  const folder = folders[groups.indexOf(s.group)];
  const file = `research/${folder}/${s.id}.md`;
  const content = fs.readFileSync(path.join(root, file), 'utf8');
  if (!content.includes('<!-- report-body:start -->') || !content.includes('<!-- report-body:end -->')) {
    throw new Error(`Missing report body markers: ${file}`);
  }
  return { id:s.id, group:s.group, title:s.title, path:file };
});
for (const [i, folder] of folders.entries()) {
  for (const [name, title] of [['README','장 안내'],['evidence','근거 자료 목록'],['tasks','남은 과제']]) {
    const file = `research/${folder}/${name}.md`;
    if (!fs.existsSync(path.join(root, file))) throw new Error(`Missing file: ${file}`);
    documents.push({id:`${folder}-${name}`,group:groups[i],title:`${groups[i]} · ${title}`,path:file});
  }
}
documents.sort((a,b)=>groups.indexOf(a.group)-groups.indexOf(b.group));
fs.writeFileSync(path.join(root, 'research', 'index.json'), JSON.stringify({version:1,documents},null,2)+'\n');
console.log(`Research index: ${documents.length} documents / ${groups.length} chapters`);
