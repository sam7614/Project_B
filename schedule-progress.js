'use strict';
window.ScheduleProgress=(()=>{
  const labels={planned:'예정',in_progress:'진행 중',blocked:'선행 조건 필요',complete:'완료',unverified:'증빙 확인 필요'};
  let data=null,error='',busy=false;
  const escape=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const safeUrl=url=>typeof url==='string'&&/^(research\/[a-zA-Z0-9/._-]+\.(md|json)|https:\/\/(docs\.google\.com|github\.com|project-b-lemon\.vercel\.app|micro-degree-student\.vercel\.app)\/[^\s]+)$/.test(url);
  const link=e=>safeUrl(e.url)?`<a href="${escape(e.url)}" target="_blank" rel="noopener noreferrer">${escape(e.label)} ↗</a>`:'';
  function task(id){return data?.tasks[id]||null;}
  function status(id){return task(id)?.status||'unverified';}
  function details(id){const t=task(id);return `<div class="task-progress"><span class="progress-tag ${status(id)}">${data?labels[status(id)]:'공유 상태 확인 중'}</span><p>${escape(t?.note||'완료 여부는 공유 증빙을 읽은 뒤 표시합니다.')}</p><div class="evidence-links">${(t?.evidence||[]).map(link).join(' ')}</div></div>`;}
  function panel(){const root=document.querySelector('#sharedProgress');
    if(!data){root.innerHTML=`<h2>공유 연구 현황</h2><p role="status">${escape(error||'원고 버전과 과업별 증빙 상태를 읽고 있습니다.')}</p><button class="btn" id="refreshProgress">다시 확인</button>`;}
    else{const all=Object.values(data.tasks),counts=Object.keys(labels).map(s=>`${labels[s]} ${all.filter(t=>t.status===s).length}`).join(' · ');
      root.innerHTML=`<div class="shared-heading"><div><div class="eyebrow">공유 연구 현황 · 보고서 ${escape(data.report.version)}</div><h2>보고서 집필 ${labels[data.report.status]||'진행 중'}</h2></div><button class="btn" id="refreshProgress">최신 상태 확인</button></div><p>${escape(data.report.note)}</p><p class="source">최종 증빙 확인: ${escape(new Intl.DateTimeFormat('ko-KR',{timeZone:'Asia/Seoul',dateStyle:'long',timeStyle:'short'}).format(new Date(data.reviewedAt)))} (한국시간) · 실제 참여자 ${escape(data.actualParticipants)}명</p><div class="evidence-links">${link({label:'구글독스 최종보고서',url:data.report.url})} ${link({label:'수행보고',url:data.dailyReportUrl})} ${link({label:'전체 원고 스냅샷',url:data.report.snapshot})} ${link({label:'버전 변경 이력',url:'research/01-overview/report-versions.md'})}</div><p class="source">${escape(counts)}</p><div class="deliverables">${data.deliverables.map(d=>`<article><span class="progress-tag ${escape(d.status)}">${labels[d.status]}</span><h3>${escape(d.title)}</h3><p>${escape(d.note)}</p><div class="evidence-links">${(d.evidence||[]).map(link).join(' ')}</div></article>`).join('')}</div><p class="source">${escape(data.scope)} 발행된 공유 자료를 페이지 진입·다시 활성화·60초마다 확인합니다.</p>${error?`<p class="sync-error" role="status">${escape(error)} 마지막으로 읽은 공유 상태를 표시합니다.</p>`:''}`;
    }
    root.querySelector('#refreshProgress').onclick=()=>refresh();
  }
  let onChange=()=>{};
  async function refresh(){if(busy)return;busy=true;try{
      const r=await fetch('research/progress.json',{cache:'no-store'});if(!r.ok)throw Error('공유 현황 파일을 읽지 못했습니다.');const next=await r.json();
      if(next.schemaVersion!==1||!next.report||!safeUrl(next.report.url)||!safeUrl(next.report.snapshot)||!safeUrl(next.dailyReportUrl)||!Number.isFinite(Date.parse(next.reviewedAt))||!Number.isInteger(next.actualParticipants)||!Array.isArray(next.deliverables)||!next.tasks||Object.values(next.tasks).concat(next.deliverables).some(t=>!labels[t.status]||typeof t.note!=='string'||!Array.isArray(t.evidence)||t.evidence.some(e=>!safeUrl(e.url))))throw Error('공유 현황 형식을 확인할 수 없습니다.');
      if(window.ScheduleProgress.taskIds?.some(id=>!next.tasks[id]))throw Error('공유 현황의 일부 일정이 누락되었습니다.');
      data=next;error='';
    }catch(e){error=e.message||'최신 상태를 확인하지 못했습니다.';}finally{busy=false;panel();onChange();}
  }
  function start(callback,ids){onChange=callback;window.ScheduleProgress.taskIds=ids;panel();refresh();setInterval(()=>{if(!document.hidden)refresh();},60000);document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh();});}
  return {task,status,details,start,ready:()=>Boolean(data)};
})();
