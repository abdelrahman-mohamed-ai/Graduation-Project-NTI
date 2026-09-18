'use strict';
window.EG = {
  esc(value) { return String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); },
  icons() { window.lucide?.createIcons(); },
  debounce(fn, delay=250) { let timer; return (...args) => { clearTimeout(timer); timer=setTimeout(()=>fn(...args), delay); }; },
  async api(url, options={}) {
    const headers = {'X-CSRF-Token':document.querySelector('meta[name="csrf-token"]').content, ...options.headers};
    if (options.body && !(options.body instanceof FormData)) { headers['Content-Type']='application/json'; options.body=JSON.stringify(options.body); }
    const response=await fetch(url,{...options,headers});
    const data=await response.json().catch(()=>({error:'The server returned an unreadable response. Please try again.'}));
    if(!response.ok){const error=new Error(data.error || 'Request failed.');error.fields=data.errors || {};throw error;}
    return data;
  },
  toast(message,error=false) { const el=document.createElement('div');el.className='toast'+(error?' error':'');el.textContent=message;document.querySelector('#toast-region').append(el);setTimeout(()=>el.remove(),6500); },
  badge(level) { const icon={High:'triangle-alert',Medium:'circle-alert',Low:'shield-check'}[level]||'circle';return `<span class="badge ${EG.esc((level||'').toLowerCase())}"><i data-lucide="${icon}"></i>${EG.esc((level||'Not analyzed').toUpperCase())}</span>`; },
  date(value) { return value ? new Date(value).toLocaleDateString(I18N.language==='ar'?'ar-EG':'en-GB',{month:'short',day:'numeric',year:'numeric'}) : 'Not analyzed'; },
  chart(id, config) { const el=document.getElementById(id);if(!el||!window.Chart)return;Chart.getChart(el)?.destroy();return I18N.registerChart(new Chart(el,config),config); },
  chartOptions(horizontal=false) { return {responsive:true,maintainAspectRatio:false,animation:{duration:window.matchMedia('(prefers-reduced-motion: reduce)').matches?0:600},plugins:{legend:{display:false},tooltip:{backgroundColor:'#242840',padding:11,cornerRadius:7,titleFont:{size:11},bodyFont:{size:10}}},scales:{x:{grid:{display:horizontal,color:'#f0f2f7'},border:{display:false},ticks:{font:{size:11},color:'#6e7b91',maxTicksLimit:6}},y:{grid:{display:!horizontal,color:'#f0f2f7'},border:{display:false},ticks:{font:{size:11},color:'#6e7b91'}}}, ...(horizontal?{indexAxis:'y'}:{})}; }
};
EG.icons();
if(window.Chart){Chart.defaults.font.family='Inter, system-ui, sans-serif';Chart.defaults.color='#959eb0';}
function syncNavigation(){const mobile=innerWidth<=760,open=document.body.classList.contains('sidebar-open');document.querySelector('#sidebar').inert=mobile&&!open;document.querySelector('#menu-toggle').setAttribute('aria-expanded',mobile?open:!document.body.classList.contains('sidebar-collapsed'));}
document.querySelector('#menu-toggle')?.addEventListener('click',()=>{if(innerWidth<=760){document.body.classList.toggle('sidebar-open');}else{document.body.classList.toggle('sidebar-collapsed');}syncNavigation();if(innerWidth<=760&&document.body.classList.contains('sidebar-open'))document.querySelector('#sidebar a').focus();});
function closeNavigation(){document.body.classList.remove('sidebar-open');syncNavigation();}
document.querySelector('#collapse-sidebar')?.addEventListener('click',()=>{if(innerWidth<=760){closeNavigation();document.querySelector('#menu-toggle').focus();}else document.body.classList.toggle('sidebar-collapsed');syncNavigation();});
document.querySelector('#sidebar-backdrop')?.addEventListener('click',closeNavigation);
window.addEventListener('resize',syncNavigation);syncNavigation();
document.addEventListener('keydown',event=>{if(event.key==='Escape'){const wasOpen=document.body.classList.contains('sidebar-open');closeNavigation();if(wasOpen)document.querySelector('#menu-toggle').focus();document.querySelector('#global-results').hidden=true;}if(event.key==='Tab'&&innerWidth<=760&&document.body.classList.contains('sidebar-open')){const links=[...document.querySelectorAll('#sidebar a,#sidebar button')],first=links[0],last=links[links.length-1];if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}}if(event.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){event.preventDefault();document.querySelector('#global-search').focus();}});
const globalInput=document.querySelector('#global-search'),globalResults=document.querySelector('#global-results');
let globalSequence=0;
globalInput?.addEventListener('input',EG.debounce(async()=>{const seq=++globalSequence,q=globalInput.value.trim();if(!q){globalResults.hidden=true;globalInput.setAttribute('aria-expanded','false');return;}try{const d=await EG.api('/api/students/search?q='+encodeURIComponent(q));if(seq!==globalSequence)return;globalResults.innerHTML=d.students.length?d.students.map(s=>`<a class="search-result" href="/students/${encodeURIComponent(s.student_uid)}"><span><strong><span data-i18n-skip>${EG.esc(s.student_name||s.student_uid)}</span></strong><small><span data-i18n-skip>${EG.esc(s.student_uid)}</span> · ${EG.esc(s.course_name)}</small></span>${EG.badge(s.risk_level)}</a>`).join(''):'<div class="search-empty">No matching students. Try another ID or name.</div>';globalResults.hidden=false;globalInput.setAttribute('aria-expanded','true');EG.icons();}catch(e){EG.toast(e.message,true);}}));
globalInput?.addEventListener('keydown',e=>{if(e.key==='ArrowDown'){e.preventDefault();globalResults.querySelector('a')?.focus();}});
globalResults?.addEventListener('keydown',e=>{const links=[...globalResults.querySelectorAll('a')],i=links.indexOf(document.activeElement);if(e.key==='ArrowDown'){e.preventDefault();links[(i+1)%links.length]?.focus();}if(e.key==='ArrowUp'){e.preventDefault();if(i===0)globalInput.focus();else links[i-1]?.focus();}});
document.addEventListener('click',e=>{if(!e.target.closest('.global-search')){globalResults.hidden=true;globalInput.setAttribute('aria-expanded','false');}});
document.querySelector('#notifications')?.addEventListener('click',async()=>{const dialog=document.querySelector('#notification-dialog');dialog.showModal();try{const d=await EG.api('/api/dashboard');document.querySelector('#notification-content').textContent=`${d.review} students are near the high-risk decision threshold and flagged for manual review. This flag is distinct from the ${d.counts.High} students in the high-risk band.`;}catch(e){document.querySelector('#notification-content').textContent=e.message;}});
document.querySelectorAll('[data-close-dialog]').forEach(b=>b.addEventListener('click',()=>b.closest('dialog').close()));
// Accessible dashboard explanations: pointer, keyboard and touch all reveal the same exported values.
document.querySelectorAll('.tooltip-anchor').forEach(anchor=>{
  const trigger=anchor.querySelector('.tooltip-trigger'),tip=anchor.querySelector('[role="tooltip"]');
  const toggle=show=>{tip.hidden=!show;trigger.setAttribute('aria-expanded',show);if(show){const anchorBox=trigger.getBoundingClientRect();tip.style.position='fixed';tip.style.right='auto';tip.style.left=Math.max(16,Math.min(anchorBox.left,innerWidth-tip.offsetWidth-16))+'px';tip.style.top=(anchorBox.bottom+tip.offsetHeight+12>innerHeight?Math.max(12,anchorBox.top-tip.offsetHeight-9):anchorBox.bottom+9)+'px';}};
  anchor.addEventListener('mouseenter',()=>toggle(true));anchor.addEventListener('mouseleave',()=>{if(!anchor.contains(document.activeElement))toggle(false);});
  trigger.addEventListener('focus',()=>toggle(true));trigger.addEventListener('blur',()=>toggle(false));trigger.addEventListener('click',()=>toggle(true));
  trigger.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();e.stopPropagation();toggle(false);}});
  document.addEventListener('click',e=>{if(!anchor.contains(e.target))toggle(false);});
  window.addEventListener('scroll',()=>toggle(false),{passive:true});window.addEventListener('resize',()=>toggle(false));
});
