const track = document.querySelector('.folio-track');
function setupGallery() {
const originals = [...track.children];
const count = originals.length;
function copies() {
  return originals.map(original => {
    const copy = original.cloneNode(true);
    copy.setAttribute('aria-hidden','true');
    copy.querySelector('a').tabIndex = -1;
    return copy;
  });
}
track.prepend(...copies());
track.append(...copies());
const cards = [...track.children];
const rail = document.querySelector('.project-rail');
const markers = [...rail.children];
const previous = document.querySelector('#prev');
const next = document.querySelector('#next');
const reducedMotion = matchMedia('(prefers-reduced-motion:reduce)');
let selected = -1;
function targetLeft(i) {
  const card = cards[i];
  return track.scrollLeft + card.getBoundingClientRect().left - (track.clientWidth - card.offsetWidth) / 2;
}
let physical = count;
let target = null;
function select(index, relative = false) {
  const logical = (index % count + count) % count;
  const candidates = [logical, logical+count, logical+2*count];
  target = relative ? (target ?? physical) + index : candidates.reduce((a,b)=>Math.abs(targetLeft(a)-track.scrollLeft)<Math.abs(targetLeft(b)-track.scrollLeft)?a:b);
  target = Math.max(1,Math.min(cards.length-2,target));
  track.scrollTo({left:targetLeft(target),behavior:reducedMotion.matches?'instant':'smooth'});
}
function refresh() {
  let active = 0, nearest = Infinity;
  cards.forEach((card,i) => {
    const delta = (targetLeft(i)-track.scrollLeft)/card.offsetWidth;
    const distance = Math.abs(delta);
    if (distance < nearest) { nearest=distance; active=i; }
    card.style.setProperty('--size',String(1-.13*Math.min(1,distance)));
    card.style.setProperty('--tilt',Math.max(-12,Math.min(12,-delta*11))+'deg');
  });
  physical=active;
  active%=count;
  if (active===selected) return;
  selected=active;
  markers.forEach((button,i)=>button.setAttribute('aria-current',String(i===active)));

  const marker=markers[active];
  rail.scrollTo({left:rail.scrollLeft+marker.getBoundingClientRect().left-rail.getBoundingClientRect().left-(rail.clientWidth-marker.offsetWidth)/2,behavior:'instant'});
  document.querySelector('#gallery-status').textContent=cards[active].getAttribute('aria-label');
}
markers.forEach((button,i)=>button.addEventListener('click',()=>select(i)));
previous.onclick=()=>select(-1,true);
next.onclick=()=>select(1,true);
let endTimer;
function settle(){
  refresh();
  const middle=count+selected;
  if(physical!==middle) track.scrollTo({left:targetLeft(middle),behavior:'instant'});
  target=null;
}
track.addEventListener('scroll',()=>{
  refresh();
  clearTimeout(endTimer);
  endTimer=setTimeout(settle,140);
},{passive:true});
document.querySelector('.gallery-stage').addEventListener('keydown',e=>{
  if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();select(e.key==='ArrowLeft'?-1:1,true);}
  if(e.key==='Home'||e.key==='End'){e.preventDefault();select(e.key==='Home'?0:count-1);}
});
let lastWheel=0;
track.addEventListener('wheel',e=>{
  if(e.ctrlKey || Math.abs(e.deltaX)>=Math.abs(e.deltaY))return;
  const dir=Math.sign(e.deltaY);

  e.preventDefault();
  const now=performance.now();
  if(now-lastWheel>260)select(dir,true);
  lastWheel=now;
},{passive:false});
track.scrollTo({left:targetLeft(count),behavior:'instant'});
refresh();
addEventListener('resize',()=>{track.scrollTo({left:targetLeft(count+selected),behavior:'instant'});refresh();});
}
if(track) setupGallery();
