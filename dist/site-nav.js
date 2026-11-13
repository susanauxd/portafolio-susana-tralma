(() => {
  const header = document.querySelector('.portfolio-nav');
  const nav = header.querySelector('nav');
  const toggle = header.querySelector('.menu-toggle');
  const projects = nav.querySelector('details');
  function setOpen(open) {
    nav.classList.toggle('open',open);
    toggle.setAttribute('aria-expanded',String(open));
    if (!open) projects.open=false;
  }
  toggle.addEventListener('click',()=>setOpen(!nav.classList.contains('open')));
  document.addEventListener('click',e=>{
    if (!header.contains(e.target) || e.target.closest('a')) setOpen(false);
    else if (!projects.contains(e.target)) projects.open=false;
  });
  header.addEventListener('focusout',e=>{if (!header.contains(e.relatedTarget)) setOpen(false);});
  document.addEventListener('keydown',e=>{
    if (e.key!=='Escape') return;
    if (projects.open) {projects.open=false;projects.querySelector('summary').focus();}
    else if(nav.classList.contains('open')) {setOpen(false);toggle.focus();}
  });
  matchMedia('(min-width:801px)').addEventListener('change',()=>setOpen(false));
  function scrollState(){header.classList.toggle('has-scroll',scrollY>0);}
  addEventListener('scroll',scrollState,{passive:true});
  scrollState();
})();
