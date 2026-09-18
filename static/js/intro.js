'use strict';
(() => {
  const intro=document.getElementById('app-intro');
  const key='eduguard.intro.seen';
  let seen=false;
  try {seen=sessionStorage.getItem(key)==='1';sessionStorage.setItem(key,'1');} catch (_) { /* Storage restrictions must never block entry. */ }
  if(seen){intro.remove();return;}
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  intro.hidden=false;
  let closed=false;
  function finish(){if(closed)return;closed=true;intro.classList.add('intro-exit');setTimeout(()=>intro.remove(),reduced.matches?100:300);}
  document.getElementById('intro-skip').addEventListener('click',finish);
  // Keyboard users may move directly into the application; no focus trap or forced focus.
  document.addEventListener('focusin',event=>{if(!intro.contains(event.target))finish();},{once:true});
  const timer=setTimeout(finish,reduced.matches?350:2000);
  reduced.addEventListener('change',()=>{if(reduced.matches){clearTimeout(timer);finish();}},{once:true});
})();
