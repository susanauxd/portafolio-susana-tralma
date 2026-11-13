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
