'use strict';
(() => {
  if(!window.EG || !window.Chart)return;
  const compact=matchMedia('(max-width: 760px)');
  const create=EG.chart;
  function tune(chart){
    if(!chart?.ctx)return;
    const options=chart.config.options;
    const horizontal=options.indexAxis==='y';
    if(horizontal&&options.scales?.y){
      const ticks=options.scales.y.ticks ||= {};
      ticks.font={...(ticks.font||{}),size:compact.matches?11:12};
      ticks.callback=function(value){
        const label=String(this.getLabelForValue(value));
        if(!compact.matches||label.length<=19)return label;
        const words=label.split(' '),lines=[''];
        for(const word of words){const i=lines.length-1;if(lines[i]&&(lines[i]+' '+word).length>19)lines.push(word);else lines[i]+=(lines[i]?' ':'')+word;}
        return lines.length>2?[lines[0],lines[1]+'…']:lines;
      };
    }
    if(options.plugins?.legend){const labels=options.plugins.legend.labels ||= {};labels.font={...(labels.font||{}),size:compact.matches?11:12};labels.padding=compact.matches?12:20;}
    chart.update('none');
  }
  EG.chart=(...args)=>{const chart=create(...args);tune(chart);return chart;};
  compact.addEventListener('change',()=>Object.values(Chart.instances).forEach(tune));
})();
