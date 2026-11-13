"""Claro case study: source wording retained, PDF line wraps normalized for HTML."""
import html,json,re
from pathlib import Path

def render(page):
 data=json.loads((Path(__file__).parent/'claro-copy.json').read_text())
 def txt(i):return re.sub(r'\s+',' ',data[i]).strip()
 def e(t):return html.escape(t)
 def p(t):return '<p>'+e(t)+'</p>'
 def items(values,ordered=False):
  tag='ol' if ordered else 'ul'
  return '<'+tag+'>'+''.join('<li>'+e(t)+'</li>' for t in values)+'</'+tag+'>'
 def fig(name,alt,zoom=False):
  src='assets/claro-'+name+'.webp'
  return '<figure><a class="claro-image-link image-surface" href="'+src+'" target="_blank" rel="noopener" aria-label="'+e('Ampliar: '+alt)+'"><img src="'+src+'" alt="'+e(alt)+'" loading="lazy"></a>'+('<figcaption><a class="textlink" href="'+src+'" target="_blank" rel="noopener">Ampliar imagen ↗</a></figcaption>' if zoom else '')+'</figure>'
 def split(a,b):return '<div class="story-split"><div>'+a+'</div><div>'+b+'</div></div>'
 def compare(before,after,after_label='Después'):
  return '<div class="compare claro-compare"><div><h3>Antes</h3>'+before+'</div><div><h3>'+after_label+'</h3>'+after+'</div></div>'
 def card(content):
  return '<div class="regcheq-copy">'+content+'</div>'
 def row(copy,media):
  return '<div class="claro-row">'+card('<div class="claro-card-content">'+copy+'</div>')+media+'</div>'
 sections=[]
 def section(key,label,title,tone,media='',intro=''):
  kicker='<p class="eyebrow">'+e(label)+'</p>' if label else ''
  chapter=f'<div class="case-band case-copy" data-tone="{tone}">'+kicker+'<h2>'+e(title)+'</h2>'+intro+'</div>'
  panel='<div class="case-band case-media">'+media+'</div>' if media else ''
  sections.append(f'<section id="{key}" class="story-section">{chapter}{panel}</section>')
 heuristics=items(re.sub(r'\s*\n\s*(?=[a-záéíóú])', ' ', data[11]).splitlines(),True)
 section('heuristicas','INVESTIGACIÓN','EVALUACIÓN DE USABILIDAD','lavender',
  row('<h3>'+e(txt(10))+'</h3>'+heuristics,fig('heuristics','Pantallas de Claro anotadas con los hallazgos de la evaluación heurística.',True)))
 findings=data[21].splitlines()[0]
 map_items=['Gran cantidad de tipos de bolsas prepago.','Acceso poco accesible a la tienda','Organización de categorías de beneficios desordenada.','Filtro de beneficios incompleta.']
 section('mapa','ANÁLISIS','MAPEANDO LA EXPERIENCIA','cyan',
  row('<h3>'+e(findings)+'</h3>'+items(map_items,True),fig('map','Mapa de navegación del cliente prepago.',True)),p(txt(20)))
 intro,task=txt(24).split('La tarea')
 section('test',txt(22),txt(23),'lavender',
  card('<h3>Hallazgos:</h3>'+items([
   'Se observa que los usuarios tuvieron dificultad para encontrar el nombre de la bolsa video.',
   'Se observa que para lograr llegar a la bolsa video el usuario debe revisar cada una de las bolsas.',
   'Se observa que el usuario no visualiza una opción clara para iniciar su recorrido en la búsqueda.',
   'Se observa que el usuario identifica la opción del menú compras a las bolsas prepago y éstas actualmente no se encuentran allí.'],True))+fig('tests-white','Resultados de Tree testing y Card Sorting.',True),p(intro.strip())+p('La tarea'+task))
 section('lean',txt(26),txt(27),'lavender',row(p(txt(28))+p(txt(29)),fig('lean','Lean UX Canvas del proyecto Claro.',True)))
 ui=['Mejora de elementos de estilos de interfaz como reducción de colores de un mismo tono','Unidad en iconografía','Familia tipográfica y orden de jerarquías','Diagramación de contenido y sus elementos coherentes (bordes, radios, tamaños, botones)']
 ux=['Cambios en categorías de visualización de bolsas prepago.','Accesos directos claros a beneficios.','Opciones de manejo para el usuario como botones touch en filtros.','Filtros más completos en beneficios, categorías.','Visualización de opciones que simplifican pantallas de interacciones.','Creación de tags para beneficios.']
 section('oportunidades',txt(30),txt(31),'cyan',media='<div class="claro-opportunity-cards">'+card('<h3>UI</h3>'+items(ui))+card('<h3>UX</h3>'+items(ux))+'</div>',intro=p(txt(32)))
 section('estilos',txt(37),'Tipografía','violet','<div class="claro-specimens">'+fig('type-sample',txt(39),True)+fig('type-scale',txt(40)+'. '+'. '.join(txt(i) for i in range(41,51)),True)+'</div>')
 section('color',txt(37),'Color','violet','<div class="claro-specimens">'+fig('color-sample','Muestra de color de Claro',True)+fig('color-palette',txt(51),True)+'</div>')
 section('disenos','PROPUESTA','Inicio','lavender',row(
  p('Propuesta de diseño escalable con patrones visuales claros, pensada para disminuir la tasa de abandono en las transacciones más críticas y entregar claridad al usuario agregando también nuevos componentes.'),
  fig('home-comparison','Pantalla de inicio de Claro: antes a la izquierda y después a la derecha.',True)))
 section('flujo-antes','PROPUESTAS','FLUJO RECARGA BOLSAS','violet',
  compare(fig('purchase-before','Antes: flujo de compra de bolsas prepago.',True),fig('purchase-after','Después: flujo de compra de bolsas prepago.',True),'Después'))
 section('beneficios-antes','PROPUESTAS','Flujo cupones','lavender',
  compare(fig('benefits-flow-before','Antes: flujo de beneficios y cupones.',True),fig('benefits-flow-after','Después: flujo de beneficios y cupones.',True),'Después'))
 section('prototipo','Prototipo','Recorrido por la propuesta de rediseño','lavender',row(
  p('Este video muestra la navegación del prototipo de la app Claro y permite observar cómo se conectan sus pantallas e interacciones dentro de la propuesta de rediseño.'),
  '<video class="claro-prototype-video" controls playsinline preload="metadata" width="1184" height="1848" aria-label="Video del prototipo de la app Claro"><source src="assets/claro-prototipo.mp4" type="video/mp4"><a href="assets/claro-prototipo.mp4">Abrir video del prototipo</a></video>'))
 title=txt(1).removeprefix('caso de estudio ')
 body='<section class="hero original-hero claro-hero"><div class="wrap"><a class="breadcrumb" href="proyectos.html">← Volver a proyectos</a>'+split('<p class="eyebrow">'+e(txt(0))+' / caso de estudio</p><h1>'+e(title)+'</h1><p class="sub">'+e(txt(2))+'</p>',fig('hero','Portada del proyecto: rediseño de la app Claro Chile.'))+'<dl class="facts">'
 for label,value in [(txt(3),txt(4)),(txt(5),txt(6)),(txt(7),txt(8))]:
  body+='<div><dt>'+e(label)+'</dt><dd>'+e(value)+'</dd></div>'
 body+='</dl></div></section><div class="original-story claro-story">'
 body+=''.join(sections)
 body+='</div><div class="wrap story-back"><a class="textlink" href="proyectos.html">← Volver a proyectos</a></div>'
 page('claro.html','Claro Chile · Rediseño App',body,'proyectos.html')
