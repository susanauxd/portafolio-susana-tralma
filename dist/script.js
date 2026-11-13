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

// Full-size sources load on demand. Ordinary image links work without JavaScript.
function enableImageViewer() {
  const links = [...document.querySelectorAll('figure a[href]')].filter(
    link => /\.(?:webp|png|jpe?g)$/i.test(link.pathname)
  );
  if (!links.length || !window.HTMLDialogElement) return;
  const viewer = document.createElement('dialog');
  viewer.className = 'media-viewer detail-viewer';
  viewer.setAttribute('aria-labelledby', 'media-title');
  viewer.innerHTML = `
    <div class="media-toolbar">
      <h2 id="media-title">Vista ampliada</h2>
      <div class="zoom-controls" role="group" aria-label="Ampliación">
        <button type="button" data-step="-1" aria-label="Reducir imagen">−</button>
        <output aria-live="polite"></output>
        <button type="button" data-step="1" aria-label="Aumentar imagen">+</button>
        <button type="button" class="zoom-fit">Ajustar</button>
      </div>
      <button type="button" class="media-close" autofocus>Cerrar ×</button>
    </div>
    <div class="media-canvas" tabindex="0" role="region" aria-label="Detalle de imagen. Usa las flechas para recorrerla.">
      <img alt="" draggable="false">
    </div>
    <p class="media-description"></p>`;
  document.body.append(viewer);
  const canvas = viewer.querySelector('.media-canvas');
  const picture = canvas.querySelector('img');
  const caption = viewer.querySelector('.media-description');
  const percent = viewer.querySelector('output');
  const smaller = viewer.querySelector('[data-step="-1"]');
  const larger = viewer.querySelector('[data-step="1"]');
  const fit = viewer.querySelector('.zoom-fit');
  let scale = 1, fitted = false, trigger, drag, fallback;
  const fitScale = () => Math.min(1, canvas.clientWidth / picture.naturalWidth,
                                      canvas.clientHeight / picture.naturalHeight);
  function magnify(value, anchorX = canvas.clientWidth / 2, anchorY = canvas.clientHeight / 2) {
    if (!picture.naturalWidth) return;
    const imageBox = picture.getBoundingClientRect();
    const viewport = canvas.getBoundingClientRect();
    const fx = (viewport.left + anchorX - imageBox.left) / imageBox.width;
    const fy = (viewport.top + anchorY - imageBox.top) / imageBox.height;
    scale = Math.min(4, Math.max(fitScale(), value));
    picture.style.width = Math.round(picture.naturalWidth * scale) + 'px';
    canvas.scrollLeft = Math.max(0, picture.offsetWidth * fx - anchorX);
    canvas.scrollTop = Math.max(0, picture.offsetHeight * fy - anchorY);
    percent.value = Math.round(scale * 100) + ' %';
    smaller.disabled = scale <= fitScale() + .001;
    larger.disabled = scale >= 4;
    fit.textContent = Math.abs(scale - fitScale()) < .001 && fitScale() < .999 ? 'Ver al 100 %' : 'Ajustar';
  }
  const stops = [.125,.25,.5,.75,1,1.5,2,3,4];
  function step(up) {
    fitted = false;
    magnify(up ? (stops.find(n => n > scale + .001) || 4)
               : ([...stops].reverse().find(n => n < scale - .001) || fitScale()));
  }
  function toggleFit() {
    fitted = fit.textContent !== 'Ver al 100 %';
    magnify(fitted ? fitScale() : 1);
  }
  smaller.onclick = () => step(false);
  larger.onclick = () => step(true);
  fit.onclick = toggleFit;
  viewer.querySelector('.media-close').onclick = () => viewer.close();
  picture.onload = () => {
    if (!viewer.open) return;
    magnify(fitted ? fitScale() : 1);
    canvas.scrollTo(0, 0);
  };
  picture.onerror = () => {
    if (fallback && picture.src !== fallback) { picture.src = fallback; return; }
    caption.textContent = 'La imagen no se pudo cargar. Cierra el visor y vuelve a intentarlo.';
  };
  for (const link of links) {
    const source = link.closest('figure').querySelector('img');
    if (!source) continue;
    link.setAttribute('aria-haspopup','dialog');
    link.setAttribute('aria-label','Ampliar: ' + source.alt);
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      trigger = link;
      fallback = new URL(source.getAttribute('src'), document.baseURI).href;
      fitted = !!link.closest('.original-hero');
      picture.alt = source.alt;
      caption.textContent = source.alt;
      picture.style.removeProperty('width');
      percent.value = '…';
      viewer.showModal();
      document.documentElement.classList.add('viewer-open');
      picture.src = link.href;
    });
  }
  viewer.addEventListener('keydown', e => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (['+','=','-','0'].includes(e.key)) {
      e.preventDefault();
      if (e.key === '0') { fitted = true; magnify(fitScale()); }
      else step(e.key !== '-');
    }
  });
  canvas.addEventListener('dblclick', e => {
    const r = canvas.getBoundingClientRect();
    fitted = scale >= 2;
    magnify(fitted ? fitScale() : Math.max(1, scale * 2), e.clientX-r.left, e.clientY-r.top);
  });
  canvas.addEventListener('pointerdown', e => {
    if (e.pointerType !== 'mouse' || e.button !== 0 || e.target !== picture) return;
    drag = {x:e.clientX, y:e.clientY, left:canvas.scrollLeft, top:canvas.scrollTop};
    canvas.setPointerCapture(e.pointerId);
    canvas.classList.add('panning');
  });
  canvas.addEventListener('pointermove', e => {
    if (drag) canvas.scrollTo(drag.left + drag.x - e.clientX, drag.top + drag.y - e.clientY);
  });
  canvas.addEventListener('lostpointercapture', () => {drag = null; canvas.classList.remove('panning');});
  new ResizeObserver(() => {
    if (viewer.open && picture.complete && picture.naturalWidth) magnify(fitted ? fitScale() : scale);
  }).observe(canvas);
  viewer.addEventListener('close', () => {
    document.documentElement.classList.remove('viewer-open');
    picture.removeAttribute('src');
    trigger?.focus({preventScroll:true});
  });
}
enableImageViewer();

// Titles stay visible before the observer runs, including with JavaScript disabled.
if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const titles = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('type-arrive');
        titles.unobserve(entry.target);
      }
    }
  });
  document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(title => titles.observe(title));
}
document.addEventListener('click', event => {
  for (const menu of document.querySelectorAll('.projects-menu[open]')) {
    if (!menu.contains(event.target) || event.target.closest('a')) menu.open = false;
  }
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') {
    const menu = document.querySelector('.projects-menu[open]');
    if (menu) { menu.open = false; menu.querySelector('summary').focus(); }
  }
});

// Load each short motion study only when its cover becomes visible.
const coverMotionPreference = matchMedia('(prefers-reduced-motion: reduce)');
if ('IntersectionObserver' in window) {
  const covers = document.querySelectorAll('.original-hero img[data-motion]');
  const originals = new Map(Array.from(covers, image => [image, image.getAttribute('src')]));
  const observer = new IntersectionObserver(entries => {
    for (const {target, isIntersecting} of entries) {
      if (isIntersecting && !coverMotionPreference.matches) {
        observer.unobserve(target);
        const clip = new Image();
        clip.onload = () => {
          if (coverMotionPreference.matches) return;
          target.src = clip.src;
          setTimeout(() => target.setAttribute('src', originals.get(target)), 3350);
        };
        clip.src = target.dataset.motion;
      }
    }
  }, {threshold:.25});
  function setMotion() {
    observer.disconnect();
    for (const image of covers) {
      if (coverMotionPreference.matches) image.setAttribute('src', originals.get(image));
      else observer.observe(image);
    }
  }
  setMotion();
  coverMotionPreference.addEventListener('change', setMotion);
}
