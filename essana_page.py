"""Essana: original narrative and artwork, arranged using the shared portfolio grid."""
import html,json,re
from pathlib import Path

def render(page):
 source=json.loads((Path(__file__).parent/'essana-copy.json').read_text())
 copy=source['copy'];groups=source['groups']
 def text(i):return re.sub(r'\s+',' ',copy[i]).strip()
 def esc(value):return html.escape(value)
 title=text(1).removeprefix('Diseño ')
 paragraphs=copy[2].split('Para su construcción')
 body='<section class="hero original-hero essana-hero"><div class="wrap"><a class="breadcrumb" href="proyectos.html#diseno-grafico">← Volver a proyectos</a><div class="story-split"><div><p class="eyebrow">'+esc(text(0))+' / Diseño</p><h1>'+esc(title)+'</h1><p class="sub">'+esc(re.sub(r'\s+',' ',paragraphs[0]).strip())+'</p><p>'+esc('Para su construcción '+paragraphs[1].strip())+'</p></div><figure><img src="assets/essana-hero.webp" alt="Manual de marca de Clínica Essana." width="1800" height="1200"></figure></div><dl class="facts">'
 # Keep exactly the words in the supplied PDF.
 for a,b in [(3,4),(5,6),(7,8)]:
  body+='<div><dt>'+esc(text(a))+'</dt><dd>'+esc(text(b))+'</dd></div>'
 body+='</dl></div></section><div class="original-story essana-story">'
 headings = {
  'introduccion': ('IDENTIDAD VISUAL', 'Páginas de Introducción'),
  'historia': ('IDENTIDAD VISUAL', 'El Comienzo de una Visión'),
  'tipografia': ('ESTILOS', 'Tipografía y color'),
  'comunicacion': ('Comunicación de ecosistema', 'Construir consistencia en entornos digitales y físicos'),
  'papeleria': ('COMUNICACIÓN', 'Papelería Corporativa'),
  'publicidad': ('COMUNICACIÓN', 'Afiche Corporativo R.S.E.'),
 }
 for key,_,xrefs,labels in groups:
  if key=='introduccion':
   body+='<section class="story-section essana-video-section" aria-label="Video de presentación de Essana"><div class="wrap"><video class="essana-project-video" controls playsinline preload="metadata" width="1920" height="1080" aria-label="Video de presentación de Essana"><source src="assets/essana-presentacion.mp4" type="video/mp4"><a href="assets/essana-presentacion.mp4">Abrir video de presentación</a></video></div></section>'
   body+='<section id="manual-interactivo" class="story-section essana-video-section"><div class="wrap"><p class="eyebrow">IDENTIDAD VISUAL</p><h2>Vista Previa Animada</h2><video class="essana-project-video" controls playsinline preload="metadata" width="2264" height="1028" aria-label="Video del manual interactivo de Essana"><source src="assets/essana-manual-interactivo.mp4" type="video/mp4"><a href="assets/essana-manual-interactivo.mp4">Abrir video del manual interactivo</a></video></div></section>'
  eyebrow, title = headings[key]
  body+='<section id="'+key+'" class="story-section"><div class="wrap"><p class="eyebrow">'+esc(eyebrow)+'</p><h2>'+esc(title)+'</h2><div class="essana-gallery">'
  for i,label in enumerate(labels,1):
   src='assets/essana-'+key+'-'+str(i)+'.jpeg'
   body+='<figure><a class="essana-artwork image-surface" href="'+src+'" target="_blank" rel="noopener" aria-label="Ampliar: '+esc(label)+'"><img src="'+src+'" alt="'+esc(label)+' — lámina original del manual de marca Essana." loading="lazy" width="1193" height="596"></a><figcaption><a class="textlink" href="'+src+'" target="_blank" rel="noopener">Ampliar imagen ↗</a></figcaption></figure>'
  body+='</div></div></section>'
 body+='</div><div class="wrap story-back"><a class="textlink" href="proyectos.html#diseno-grafico">← Volver a proyectos</a></div>'
 page('essana.html','Essana · Manual de Marca e identidad Corporativa',body,'proyectos.html')
