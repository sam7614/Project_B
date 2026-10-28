'use strict';
// Read the same Markdown manuscripts tracked in Git and deployed by Vercel.
window.ResearchRepository = (() => {
  const escape = value => String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let selected='overview', generation=0;
  const sourceLink = path => 'https://github.com/sam7614/Project_B/blob/main/'+path.split('/').map(encodeURIComponent).join('/');
  async function index(){
    const response=await fetch('research/index.json',{cache:'no-store'});
    if(!response.ok)throw new Error('문서 목록을 읽지 못했습니다. 배포 상태를 확인하고 다시 시도하세요.');
    const value=await response.json();
    if(value.version!==1||!Array.isArray(value.documents)||value.documents.some(d=>typeof d.id!=='string'||typeof d.title!=='string'||typeof d.group!=='string'||!/^research\/0[1-6]-[a-z-]+\/[a-zA-Z0-9-]+\.md$/.test(d.path)))throw new Error('연구 문서 목록의 형식을 확인하세요.');
    return value.documents;
  }
  async function read(document){const response=await fetch(document.path,{cache:'no-store'});if(!response.ok)throw new Error('본문을 읽지 못했습니다. 문서 경로 또는 배포 상태를 확인하세요.');return response.text();}
  function body(markdown){const match=markdown.match(/<!-- report-body:start -->([\s\S]*?)<!-- report-body:end -->/);return match?match[1].trim():'';}
  function format(markdown,current,documents){
    const inline=line=>escape(line).replace(/\[([^\]]+)\]\(([A-Za-z0-9-]+\.md)\)/g,(match,label,file)=>{
      const target=documents.find(d=>d.path===current.path.slice(0,current.path.lastIndexOf('/')+1)+file);
      return target?`<button class="text-button" data-document="${escape(target.id)}">${label}</button>`:match;
    }).replace(/\[([^\]]+)\]\((https:\/\/(?:docs\.google\.com|drive\.google\.com|github\.com)\/[^\s)]+)\)/g,(_,label,url)=>`<a href="${url}" target="_blank" rel="noopener noreferrer">${label} ↗</a>`);
    const lines=markdown.split(/\r?\n/),consumed=new Set();
    return lines.map((line,i)=>{
      if(consumed.has(i)||/^<!-- report-body:(start|end) -->$/.test(line))return '';
      if(line.startsWith('|')&&/^\|\s*:?-{3,}/.test(lines[i+1]||'')){
        const cells=row=>row.trim().replace(/^\||\|$/g,'').split('|').map(v=>v.trim());
        const heads=cells(line),rows=[];consumed.add(i+1);
        for(let j=i+2;j<lines.length&&lines[j].startsWith('|');j++){rows.push(cells(lines[j]));consumed.add(j);}
        return `<div role="region" aria-label="연구 자료 표" tabindex="0" style="max-width:100%;overflow-x:auto"><table style="border-collapse:collapse;width:100%;min-width:560px"><thead><tr>${heads.map(v=>`<th scope="col" style="padding:10px;border:1px solid #cbd5e1;text-align:left">${inline(v)}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${heads.map((_,k)=>`<td style="padding:10px;border:1px solid #cbd5e1;vertical-align:top">${inline(row[k]||'')}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
      }
      const figure=line.match(/^!\[([^\]]*)\]\((research\/figures\/[a-zA-Z0-9._-]+\.(?:png|svg))\)$/);
      if(figure)return `<figure><a href="${escape(figure[2])}" target="_blank" rel="noopener noreferrer"><img src="${escape(figure[2])}" alt="${escape(figure[1])}" style="max-width:100%;height:auto" loading="lazy"></a><figcaption>${escape(figure[1])}</figcaption></figure>`;
      const heading=line.match(/^(#{1,3}) (.*)$/);
      if(heading){const level=Math.min(heading[1].length+1,4);return `<h${level}>${escape(heading[2])}</h${level}>`;}
      if(line.startsWith('- [ ] '))return `<p>☐ ${escape(line.slice(6))}</p>`;
      if(line.startsWith('- [x] '))return `<p>☑ ${escape(line.slice(6))}</p>`;
      if(line.startsWith('- '))return `<p>• ${inline(line.slice(2))}</p>`;
      return line.trim()?`<p>${inline(line)}</p>`:'';
    }).join('');
  }
  async function section(id){const documents=await index(),document=documents.find(d=>d.id===id);if(!document)throw new Error('연결된 저장소 문서가 없습니다.');return {document,text:body(await read(document))};}
  async function render(root){
    const ticket=++generation;
    root.innerHTML='<div class="banner">저장소 연구 문서를 읽고 있습니다…</div>';
    try{
      const documents=await index();if(!root.isConnected||ticket!==generation)return;
      const current=documents.find(d=>d.id===selected)||documents[0];selected=current.id;
      const markdown=await read(current);if(!root.isConnected||ticket!==generation)return;
      let previous='';const outline=documents.map(d=>{const label=d.group!==previous?`<div class="outline-group">${escape(d.group)}</div>`:'';previous=d.group;return label+`<button class="${d.id===selected?'active':''}" data-document="${escape(d.id)}" ${d.id===selected?'aria-current="true"':''}>${escape(d.title.replace(d.group+' · ',''))}</button>`;}).join('');
      root.innerHTML=`<div class="page-heading"><div><div class="eyebrow">REPOSITORY / MANUSCRIPTS</div><h1>저장소 연구 문서</h1><p>6개 장 · 기준 본문 17개 · 연구 문서 ${documents.length}개 · main 배포본</p></div><a class="button" href="https://github.com/sam7614/Project_B/tree/main/research" target="_blank" rel="noopener noreferrer">GitHub 연구 폴더 ↗</a></div><div class="banner">이 문서가 저장소의 기준본입니다. 작업 브랜치에서 수정하고 검토 후 main에 반영하면 배포된 내용이 여기에 표시됩니다. 브라우저 초안 편집은 자동으로 GitHub에 반영되지 않습니다.</div><div class="report-layout"><nav class="panel outline" aria-label="저장소 연구 목차">${outline}</nav><article class="panel repository-document"><div class="actions no-print"><a class="button" href="${escape(sourceLink(current.path))}" target="_blank" rel="noopener noreferrer">GitHub 원본 보기 ↗</a><a class="button" href="${escape(current.path)}" download>문서 받기 ↓</a><button class="button" id="reloadRepository">최신 배포본 다시 읽기</button></div><p class="entry-meta">${escape(current.path)}</p>${format(markdown,current,documents)}</article></div>`;
      root.onclick=e=>{const button=e.target.closest('[data-document]');if(button){selected=button.dataset.document;render(root);}};
      root.querySelector('#reloadRepository').onclick=()=>render(root);
    }catch(error){if(!root.isConnected||ticket!==generation)return;root.innerHTML=`<div class="banner error" role="alert">${escape(error.message)}</div><button class="button" id="retryRepository">다시 시도</button>`;root.querySelector('#retryRepository').onclick=()=>render(root);}
  }
  return {render,section};
})();
