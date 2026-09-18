'use strict';
const datasetWidthToggle=document.querySelector('#dataset-width-toggle');
if(datasetWidthToggle){
 const syncWidth=()=>{const wide=document.body.classList.contains('sidebar-collapsed');datasetWidthToggle.setAttribute('aria-pressed',wide);datasetWidthToggle.querySelector('span').textContent=wide?'Restore navigation':'Expand reading area';if(innerWidth>760)document.querySelector('#menu-toggle')?.setAttribute('aria-expanded',!wide);};
 datasetWidthToggle.addEventListener('click',()=>document.body.classList.toggle('sidebar-collapsed'));
 new MutationObserver(syncWidth).observe(document.body,{attributes:true,attributeFilter:['class']});syncWidth();
}
(()=>{const outcome=document.querySelector('#outcome-data');if(outcome){const d=JSON.parse(outcome.textContent);EG.chart('outcome-chart',{type:'doughnut',data:{labels:Object.keys(d),datasets:[{data:Object.values(d),backgroundColor:Object.keys(d).map(k=>({Graduate:'#85bda8',Dropout:'#d99aa6',Enrolled:'#a69bdd'}[k])),borderWidth:5,borderColor:'#fff',borderRadius:4}]},options:{responsive:true,maintainAspectRatio:false,cutout:'67%',plugins:{legend:{position:'bottom',labels:{usePointStyle:true,pointStyle:'circle',boxWidth:8,font:{size:13},padding:22}}}}});}
const featureSearch=document.querySelector('#feature-search');
if(featureSearch){
 const cards=[...document.querySelectorAll('[data-feature-group]')],allButton=document.querySelector('#feature-all'),rows=[...document.querySelectorAll('#dictionary-rows tr')];let selectedGroup='';
 const filter=()=>{let count=0;const query=featureSearch.value.trim().toLowerCase();for(const row of rows){row.hidden=!(row.textContent.toLowerCase().includes(query)&&(!selectedGroup||row.dataset.group===selectedGroup));if(!row.hidden)count++;}
 cards.forEach(card=>{const selected=card.dataset.featureGroup===selectedGroup;card.classList.toggle('active',selected);card.setAttribute('aria-pressed',selected);});allButton.classList.toggle('active',!selectedGroup);allButton.setAttribute('aria-pressed',!selectedGroup);
 document.querySelector('#feature-result-count').textContent=`${count} of ${rows.length} fields${selectedGroup?' · '+(cards.find(card=>card.dataset.featureGroup===selectedGroup)?.querySelector('b').textContent||selectedGroup):''}`;
 document.querySelector('#dictionary-empty').hidden=count!==0;
 };
 cards.forEach(card=>card.addEventListener('click',()=>{selectedGroup=selectedGroup===card.dataset.featureGroup?'':card.dataset.featureGroup;filter();}));
 allButton.addEventListener('click',()=>{selectedGroup='';filter();});featureSearch.addEventListener('input',filter);
 document.querySelector('#reset-feature-filters').addEventListener('click',()=>{selectedGroup='';featureSearch.value='';filter();featureSearch.focus();});filter();
}
const importance=document.querySelector('#model-importance-data');if(importance){const d=JSON.parse(importance.textContent);const options=EG.chartOptions(true);options.scales.x.ticks.callback=v=>(v*100).toFixed(0)+'%';EG.chart('model-importance',{type:'bar',data:{labels:d.map(f=>f.label),datasets:[{data:d.map(f=>f.value),backgroundColor:'#aea3d9',borderRadius:4,barThickness:15}]},options:{...options,plugins:{...options.plugins,tooltip:{callbacks:{title:items=>d[items[0].dataIndex].label,label:item=>`Aggregated importance: ${(item.raw*100).toFixed(2)}%`}}}}});}
const filters=document.querySelector('#report-filters');if(filters){let seq=0;const update=async()=>{const current=++seq;const query=new URLSearchParams(new FormData(filters));for(const[k,v]of [...query])if(!v)query.delete(k);document.querySelectorAll('[data-export]').forEach(a=>{const p=new URLSearchParams(query);if(a.dataset.export==='high')p.set('risk','High');a.href=(a.dataset.export==='summary'?'/exports/summary.csv':'/exports/students.csv')+'?'+p;});try{const d=await EG.api('/api/students?per_page=1&'+query);if(current!==seq)return;document.querySelector('#report-count').textContent=d.total?`${d.total.toLocaleString()} matching students. Exports contain the latest saved analysis for each student.`:'No matching students. Adjust filters to create a populated report.';}catch(e){document.querySelector('#report-count').textContent=e.message;}};filters.addEventListener('change',update);filters.addEventListener('reset',()=>setTimeout(update,0));update();}
})();
