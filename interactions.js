const filters=document.querySelector('.project-filters');
if(filters){
 const names={todos:'Todos',ux:'UX',ui:'UI','diseno-grafico':'Diseño gráfico'};
 function filterProjects(){
  const requested=location.hash.slice(1);
  const selected=Object.hasOwn(names,requested)?requested:'todos';
  let count=0;
  document.querySelectorAll('.cards .card').forEach(card=>{
   card.hidden=selected!=='todos'&&!card.dataset.disciplines.split(' ').includes(selected);
   if(!card.hidden)count++;
  });
  filters.querySelectorAll('a').forEach(a=>{
   if(a.dataset.filter===selected)a.setAttribute('aria-current','true');
   else a.removeAttribute('aria-current');
  });
  document.querySelector('.filter-status').textContent=count
   ? names[selected]+' · '+count+(count===1?' proyecto':' proyectos')
   : 'No hay proyectos en esta categoría.';
  try { sessionStorage.setItem('portfolio-category',selected); } catch {}
 }
 addEventListener('hashchange',filterProjects);
 filterProjects();
}

// Keep the header offset in one place and track the section at the reading position.
const header = document.querySelector('header');
function headerSize(){document.documentElement.style.setProperty('--header-height', header.offsetHeight+'px')}
headerSize();
if ('ResizeObserver' in window) new ResizeObserver(headerSize).observe(header);
const storySections = [...document.querySelectorAll('.original-story > section')];
const storyLinks = [...document.querySelectorAll('.story-index a')];
let sectionFrame;
function markReadingSection(){
 sectionFrame = null;
 const line = header.offsetHeight + 40;
 const current = storySections.find(section => {
  const r = section.getBoundingClientRect(); return r.top <= line && r.bottom > line;
 });
 storyLinks.forEach(link => {
  if(current && link.hash === '#'+current.id) link.setAttribute('aria-current','location');
  else link.removeAttribute('aria-current');
 });
}
addEventListener('scroll',()=>{if(!sectionFrame)sectionFrame=requestAnimationFrame(markReadingSection)}, {passive:true});
addEventListener('resize',markReadingSection);
markReadingSection();
// Native anchors keep history; move keyboard focus to the destination heading.
document.querySelectorAll('.story-index a,.skip').forEach(link=>link.addEventListener('click',()=>{
 const destination=document.getElementById(link.hash.slice(1));
 if(destination){destination.setAttribute('tabindex','-1');destination.focus({preventScroll:true})}
}));
// Returning to the list retains the category chosen by the reader.
try {
 const category=sessionStorage.getItem('portfolio-category');
 if(['ux','ui','diseno-grafico'].includes(category)) {
  document.querySelectorAll('.breadcrumb,.story-back a').forEach(link=>{
   if(link.getAttribute('href')==='proyectos.html')link.href='proyectos.html#'+category;
  });
 }
} catch {}

// Brief feedback after a filter change, without delaying or hiding the results.
const motionPreference=matchMedia('(prefers-reduced-motion: reduce)');
const filterAnimations=new Set();
if(filters){
 addEventListener('hashchange',()=>{
  filterAnimations.forEach(animation=>animation.cancel());filterAnimations.clear();
  if(motionPreference.matches)return;
  const results=document.querySelector('.cards');
  if(!results?.animate)return;
  const animation=results.animate([{opacity:.75,transform:'translateY(4px)'},{opacity:1,transform:'none'}],{duration:180,easing:'cubic-bezier(.2,.7,.2,1)'});
  filterAnimations.add(animation);
  animation.finished.then(()=>filterAnimations.delete(animation)).catch(()=>{});
 });
}
motionPreference.addEventListener('change',()=>{if(motionPreference.matches){filterAnimations.forEach(animation=>animation.cancel());filterAnimations.clear()}});
