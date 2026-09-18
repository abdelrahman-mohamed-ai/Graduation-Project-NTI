'use strict';
(() => {
  const catalog = JSON.parse(document.getElementById('i18n-catalog').textContent);
  const lookup = new Map(Object.entries(catalog).map(([k,v])=>[k.toLowerCase(),v]));
  const escaped = s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
  const phrases = new RegExp('(?<![\\w])(?:'+Object.keys(catalog).sort((a,b)=>b.length-a.length).map(escaped).join('|')+')(?![\\w])','gi');
  const originals = new WeakMap(), attributes = new WeakMap(), charts = new Map();
  const skip = 'script,style,[data-i18n-skip],.student-initial';
  let language=document.documentElement.lang, observer;
  function t(value, locale=language) {
    if (typeof value!=='string'||locale!=='ar'||!value.trim()) return value;
    const trimmed=value.trim();
    let translated=lookup.get(trimmed.toLowerCase());
    if(translated===undefined)translated=trimmed.replace(phrases,match=>lookup.get(match.toLowerCase()));
    return value.slice(0,value.length-value.trimStart().length)+translated+value.slice(value.trimEnd().length);
  }
  function visit(root) {
    if(root.nodeType===3){
      if(!root.parentElement||root.parentElement.closest(skip))return;
      let record=originals.get(root);
      if(!record||root.nodeValue!==record.last){
        let source=root.nodeValue;
        const comment=root.previousSibling;
        if(!record&&comment?.nodeType===8&&comment.data.startsWith('i18n:')){
          source=new TextDecoder().decode(Uint8Array.from(atob(comment.data.slice(5)),c=>c.charCodeAt(0)));
        }
        record={source,last:root.nodeValue};originals.set(root,record);
      }
      record.last=t(record.source);if(root.nodeValue!==record.last)root.nodeValue=record.last;
      return;
    }
    if(root.nodeType!==1||root.closest(skip))return;
    if(root.matches('time[data-i18n-date]')){
      const date=new Date(root.getAttribute('datetime'));
      const label=Number.isNaN(date.getTime())?t('Not analyzed'):date.toLocaleDateString(language==='ar'?'ar-EG':'en-GB',{month:'short',day:'numeric',year:'numeric'});
      if(root.textContent!==label)root.textContent=label;
      return;
    }
    if(root.tagName==='OPTION'&&!root.hasAttribute('value'))root.setAttribute('value',root.textContent);
    let attrs=attributes.get(root);
    if(!attrs){attrs=Object.fromEntries(Object.entries(JSON.parse(root.getAttribute('data-i18n-attrs')||'{}')).map(([key,source])=>[key,{source,last:root.getAttribute(key)}]));attributes.set(root,attrs);}
    for(const key of ['title','placeholder','aria-label','alt']){
      if(root.hasAttribute(key)){const current=root.getAttribute(key);if(!(key in attrs)||current!==attrs[key].last)attrs[key]={source:current,last:current};const value=t(attrs[key].source);attrs[key].last=value;if(current!==value)root.setAttribute(key,value);}
    }
    for(const child of root.childNodes)visit(child);
  }
  function observe(){observer.observe(document.documentElement,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['placeholder','title','aria-label','alt']});}
  function refresh(){observer?.disconnect();visit(document.documentElement);observe();}
  function localizeChart(chart, source) {
    chart.data.labels=source.labels.map(label=>Array.isArray(label)?label.map(x=>t(x)):t(label));
    chart.data.datasets.forEach((set,i)=>{if(source.datasets[i]!==undefined)set.label=t(source.datasets[i]);});
    const plugins=chart.options.plugins;
    for(const key of ['legend','tooltip']){if(plugins[key]){plugins[key].rtl=language==='ar';plugins[key].textDirection=language==='ar'?'rtl':'ltr';}}
    chart.options.font={family:language==='ar'?'"Noto Sans Arabic", Tahoma, sans-serif':'Inter, system-ui, sans-serif'};
    if(chart.options.scales?.y&&chart.options.indexAxis==='y')chart.options.scales.y.position=language==='ar'?'right':'left';
    chart.update('none');
  }
  function registerChart(chart, config){
    if(!chart)return chart;
    const source={labels:[...(config.data.labels||[])],datasets:config.data.datasets.map(d=>d.label)};
    charts.set(chart,source);
    const callbacks=chart.options.plugins?.tooltip?.callbacks;
    if(callbacks)for(const key of ['title','label','afterLabel','footer']){
      const original=callbacks[key];if(typeof original==='function')callbacks[key]=function(...args){const value=original.apply(this,args);return Array.isArray(value)?value.map(x=>t(x)):t(value);};
    }
    localizeChart(chart,source);return chart;
  }
  function setLanguage(next){
    if(!['en','ar'].includes(next))return;
    language=next;document.documentElement.lang=next;document.documentElement.dir=next==='ar'?'rtl':'ltr';
    document.cookie='eduguard_language='+next+';path=/;max-age=31536000;SameSite=Lax'+(location.protocol==='https:'?';Secure':'');
    // Remove a previous server-language override so refresh follows the new selection.
    const url=new URL(location.href);url.searchParams.delete('lang');history.replaceState(null,'',url);
    refresh();document.querySelectorAll('[data-language]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.language===next)));
    for(const [chart,source] of charts){if(chart.ctx)localizeChart(chart,source);else charts.delete(chart);}
    document.dispatchEvent(new CustomEvent('languagechange',{detail:{language:next}}));
  }
  window.I18N={t,refresh,registerChart,setLanguage,get language(){return language;}};
  observer=new MutationObserver(records=>{observer.disconnect();for(const record of records){if(record.type==='childList')record.addedNodes.forEach(visit);else visit(record.target);}observe();});
  document.querySelectorAll('[data-language]').forEach(button=>button.addEventListener('click',()=>setLanguage(button.dataset.language)));
  refresh();
})();
