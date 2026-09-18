'use strict';
(async()=>{try{
 const d=await EG.api('/api/dashboard');
 document.querySelectorAll('[data-kpi]').forEach(el=>{const key=el.dataset.kpi,value=d.counts[key]??d[key];el.classList.remove('skeleton');if(value===null){el.textContent='—';return;}const start=performance.now();const tick=now=>{const p=matchMedia('(prefers-reduced-motion: reduce)').matches?1:Math.min((now-start)/750,1);const n=value*(1-Math.pow(1-p,3));el.textContent=key==='average'?n.toFixed(1)+'%':Math.round(n).toLocaleString();if(p<1)requestAnimationFrame(tick);};requestAnimationFrame(tick);});
 const levels=['High','Medium','Low'],colors=['#dd8790','#e4c17d','#73b9a3'];
 EG.chart('risk-donut',{type:'doughnut',data:{labels:levels.map(x=>x+' risk'),datasets:[{data:levels.map(x=>d.counts[x]),backgroundColor:colors,borderWidth:5,borderColor:'#fff',hoverOffset:5,borderRadius:5}]},options:{responsive:true,maintainAspectRatio:false,cutout:'79%',plugins:{legend:{display:false}}}});
 document.querySelector('#cohort-total').textContent=d.analyzed.toLocaleString();
 document.querySelector('#risk-legend').innerHTML=levels.map((x,i)=>`<div><span class="legend-dot" style="--legend-color:${colors[i]}"></span>${x}<b>${d.counts[x]}</b></div>`).join('');
 const courses=d.courses.slice(0,6);const opt=EG.chartOptions(true);opt.scales.x.max=100;opt.scales.x.ticks.callback=v=>v+'%';opt.scales.y.ticks.font.size=11;
 EG.chart('course-chart',{type:'bar',data:{labels:courses.map(c=>c.course),datasets:[{data:courses.map(c=>c.average),backgroundColor:['#948bd5','#a19bdc','#afa8e2','#bbb6e9','#c6c2ed','#d1cef2'],borderRadius:4,barThickness:15}]},options:{...opt,plugins:{...opt.plugins,tooltip:{callbacks:{title:items=>courses[items[0].dataIndex].course,label:item=>`Average risk: ${item.raw}% · ${courses[item.dataIndex].count} students`}}}}});
 const barOptions=EG.chartOptions();barOptions.scales.y.ticks.precision=0;
 EG.chart('level-chart',{type:'bar',data:{labels:levels,datasets:[{data:levels.map(l=>d.counts[l]),backgroundColor:colors,borderRadius:5,maxBarThickness:45}]},options:barOptions});
 EG.chart('histogram-chart',{type:'bar',data:{labels:d.histogram.map((_,i)=>`${i*10}–${(i+1)*10}%`),datasets:[{data:d.histogram,backgroundColor:'#a9a1dd',borderRadius:3}]},options:barOptions});
 const max=d.importance[0]?.value||1;document.querySelector('#importance-bars').innerHTML=d.importance.slice(0,5).map(f=>`<div class="importance-item"><div><span>${EG.esc(f.label)}</span><b>${(f.value*100).toFixed(1)}%</b></div><div class="importance-track"><span style="width:${f.value/max*100}%"></span></div></div>`).join('');
 }catch(e){document.querySelectorAll('[data-kpi]').forEach(el=>{el.classList.remove('skeleton');el.textContent='—';});EG.toast('Dashboard could not load: '+e.message,true);}})();
