"""Original portfolio narrative. Text is transcribed from the user's PDF exports."""
import json,html
from pathlib import Path

def render(page,cards):
 data=json.loads((Path(__file__).parent/'original-copy.json').read_text())
 rectangular=json.loads((Path(__file__).parent/'rectangular-images.json').read_text())
 def text(n,i):
  t=data[n][i]
  for a,b in [('U X/UI','UX/UI'),('K omatsu','Komatsu'),('R ealización','Realización'),('R ediseño','Rediseño'),('Automati zación','Automatización'),('Im plementación','Implementación'),('N egociación','Negociación'),('1 0 Operadores','10 Operadores')]:t=t.replace(a,b)
  return t
 def p(n,*ids):return ''.join('<p>'+html.escape(text(n,i))+'</p>' for i in ids)
 def ul(n,*ids):return '<ul>'+''.join('<li>'+html.escape(text(n,i))+'</li>' for i in ids)+'</ul>'
 def h(n,i):return '<h3>'+html.escape(text(n,i))+'</h3>'
 def pic(src,caption=''):
  photo = src in {'reg-hero','reg-context','reg-audit','reg-ai','reg-dashboard','reg-handoff','cad-hero','cad-mobile','cad-research','cad-strategy','cad-test','cad-final','kom-hero','blog-original'}
  edge = ''
  filename = rectangular.get(src, src+'.webp')
  # Display only the rectangular screenshot area; preserve all source redactions.
  crops = {
   'reg-before1': (944,706,8,39,936,689),
   'reg-after1': (944,706,10,36,934,688),
   'reg-before2': (944,641,8,98,936,616),
   'reg-after2': (944,708,12,99,936,693),
   'reg-tokens': (944,536,8,8,935,528),
   'reg-foundations': (941,519,8,8,932,510),
   'kom-before1': (943,670,8,14,935,655),
   'kom-after1': (944,673,8,16,936,657),
   'kom-before2': (873,825,10,10,862,794),
   'kom-after2': (799,825,10,10,789,815),
   'kom-flow': (2122,1134,16,16,2106,1118),
   'kom-eval1': (943,690,8,8,935,682),
   'kom-eval2': (946,374,3,3,943,371),
  }
  style = ''
  if src in crops:
   iw,ih,x,y,r,b = crops[src]; w,h=r-x,b-y
   edge=' cropped-source'
   style=f' style="aspect-ratio:{w}/{h};--source-width:{iw/w*100:.6f}%;--source-height:{ih/h*100:.6f}%;--source-left:{-x/w*100:.6f}%;--source-top:{-y/h*100:.6f}%"'

  return f'<figure><span class="image-surface{edge}"{style}><img src="assets/{filename}" alt="{html.escape(caption or {'reg-hero':'Imagen de portada del proyecto Regcheq','cad-hero':'Imagen de portada del proyecto Cademsmart','kom-hero':'Imagen de portada del proyecto Komatsu','reg-handoff':'Traspaso del sistema de diseño al equipo','reg-dashboard':'Imagen conceptual del dashboard de Regcheq','kom-ranking-detail':'Detalle del ranking y barra de índice de efectividad','blog-original':'Imagen de portada del artículo'}.get(src,src.replace('-', ' ')))}" loading="lazy"></span>'+(f'<figcaption>{html.escape(caption)}</figcaption>' if caption else '')+'</figure>'
 def duo(a,b):return '<div class="compare">'+a+b+'</div>'
 def split(copy,images):return '<div class="story-split"><div>'+copy+'</div><div>'+images+'</div></div>'
 def story(slug,n,hero,sections,labels=None):
  body='<section class="hero original-hero"><div class="wrap"><a class="breadcrumb" href="proyectos.html">← Volver a proyectos</a><div class="story-split"><div><p class="eyebrow">'+text(n,1)+' / '+text(n,2)+'</p><h1>'+text(n,3)+'</h1><p class="sub">'+text(n,4)+'</p></div>'+pic(hero)+'</div><dl class="facts"><div><dt>Rol</dt><dd>'+text(n,6)+'</dd></div><div><dt>Responsabilidades</dt><dd>'+text(n,8)+'</dd></div><div><dt>Plataforma</dt><dd>'+text(n,10)+'</dd></div></dl></div></section>'
  body+='<div class="original-story">'
  for i,(title,content) in enumerate(sections):
   label = (labels or {}).get(title, 'Proceso')
   body+=f'<section id="paso-{i}" class="story-section"><div class="wrap"><p class="eyebrow">{html.escape(label)}</p><h2>{html.escape(title)}</h2>{content}</div></section>'

  body+='</div><aside class="case-confidentiality"><p>'+html.escape(text('Cademsmart',82))+'</p></aside>'
  if slug == 'regcheq':
   body+='<div class="project-directory"><a class="textlink" href="proyectos.html">Ver todos los proyectos ↗</a></div>'
  elif slug == 'cademsmart':
   body+='<div class="project-directory"><a class="textlink" href="proyectos.html">← Volver a proyectos</a></div>'
  else:
   body+='<div class="wrap story-back"><a class="textlink" href="proyectos.html">← Volver a proyectos</a></div>'
  page(slug+'.html',text(n,2),body,'proyectos.html')
 n='Regcheq'
 context=text(n,13);intro,rest=context.split('El Reto Operativo:');points=[]
 for label in ['Urgencia:','Autonomía Total:','Puente Técnico:','Design Ops + IA:']:rest=rest.replace(label,'\n'+label)
 context='<p>'+html.escape(intro.strip())+'</p><ul>'+''.join('<li>'+html.escape(x.strip())+'</li>' for x in rest.split('\n') if x.strip())+'</ul>'
 story('regcheq',n,'reg-hero',[
 (text(n,12),context+pic('reg-context',text(n,14))),
 (text(n,16),split(h(n,17)+ul(n,18,19),pic('reg-audit',text(n,20)))+
 '<div class="story-step">'+split(h(n,21)+p(n,22)+ul(n,23,24,25)+'<ul><li>'+html.escape(text(n,26).replace(' Algunos Tokens de color',''))+'</li></ul>',duo(pic('reg-tokens','Algunos Tokens de color'),pic('reg-foundations',text(n,27))))+'</div>'+
 '<div class="story-step">'+split(h(n,28)+p(n,29)+ul(n,30,31,32),pic('reg-ai',text(n,33)))+'</div>'+
 '<div class="story-step">'+split(h(n,34)+ul(n,35,36,37),pic('reg-dashboard'))+'</div>'+
 '<div class="story-step">'+h(n,39)+p(n,40)+ul(n,41,42)+duo(pic('reg-before1','Antes con UI Kit'),pic('reg-after1','Después con componentes de Sistema de Diseño'))+duo(pic('reg-before2','Antes con UI Kit'),pic('reg-after2','Después con componentes de Sistema de Diseño'))+'</div>'+
 '<div class="story-step">'+split(h(n,47)+ul(n,48,49),pic('reg-handoff'))+'</div>')])
 n='Cademsmart'
 strategy_points = """<ul>
<li><strong>Conecté empatía con negocio:</strong> Crucé las frustraciones reales de los auditores en terreno con las metas operativas de la empresa para resolver dolores reales con valor comercial.</li>
<li><strong>2. Co-creé con el equipo de TI:</strong> Trabajé codo a codo con los desarrolladores para transformar la falta de señal en bodegas en un reto de diseño: una arquitectura <em>offline</em> que protegiera el trabajo del usuario.</li>
<li><strong>3. Equilibré impacto y viabilidad:</strong> Filtré las prioridades para encontrar el balance perfecto: soluciones viables de construir que generaran el mayor beneficio tanto para el auditor como para el negocio.</li>
</ul>"""
 validation_points = """<ul>
<li><strong>Validé con usuarios reales:</strong> Realicé pruebas de usabilidad cualitativas con el equipo interno y los auditores en terreno para evaluar el nuevo diseño en Android frente al sistema anterior de las máquinas Zebra.</li>
<li><strong>Evalué la fluidez del flujo:</strong> Aseguré que los auditores completaran tareas críticas (rutas, inventario y reportes) de forma fluida y sin bloqueos mentales.</li>
<li><strong>Aplané la curva de aprendizaje:</strong> Garanticé que la transición tecnológica de Windows a Android fuera amigable para reducir drásticamente los tiempos de capacitación del personal.</li>
</ul>"""
 delivery_points = """<ul>
<li><strong>Ajusté con feedback real:</strong> Iteré los prototipos finales de alta fidelidad incorporando directamente los aprendizajes de los test de usabilidad guerrilla.</li>
<li><strong>Lideré el traspaso técnico (<em>Handoff</em>):</strong> Presenté y entregué formalmente las propuestas finales a los equipos Comercial y de TI para asegurar una implementación sin fricciones.</li>
<li><strong>Guié el desarrollo en Android:</strong> Estructuré la documentación técnica necesaria para guiar con total claridad al equipo de desarrollo dentro del ecosistema de la empresa.</li>
</ul>"""
 story('cademsmart',n,'cad-hero',[
 ('Cambio de sistema operativo e interfaz',p(n,13)+duo(pic('cad-zebra','Computadora móvil de Zebra Technologies'),pic('cad-mobile','Computadoras móviles de Zebra'))),
 ('Auditoría y flujos',split(ul(n,19,20),pic('cad-flow',text(n,46)))+'<div class="story-step">'+split(pic('cad-research',text(n,52)),'<h3>Observación contextual</h3>'+p(n,48)+ul(n,49,50,51))+'</div>'),
 ('ALINEAR Y DEFINIR OPORTUNIDADES DE MEJORA CLAVES',split(strategy_points+'<p>'+html.escape(text(n,55).split(' De este proceso estratégico')[0])+'</p>' ,pic('cad-strategy',text(n,62)))),
 ('ALINEAR Y DEFINIR OPORTUNIDADES DE MEJORA',split(p(n,66,67)+ul(n,68),pic('cad-wireframe',text(n,69)))),
 ('Validación con usuarios',split(validation_points,pic('cad-test',text(n,77)))),
 ('Iteraciones y entrega',split(delivery_points,pic('cad-final',text(n,81))))], labels={
  'Auditoría y flujos': 'INVESTIGACIÓN',
  'ALINEAR Y DEFINIR OPORTUNIDADES DE MEJORA': 'DISEÑO E IDEACIÓN',
  'Validación con usuarios': 'Pruebas de usabilidad',
  'Iteraciones y entrega': 'prototipo',
 })
 n='Komatsu(1)'
 wireflow_ideas = text(n,55).strip().split('. ')
 wireflow_list = '<ul class="wireflow-ideas">' + ''.join(
  '<li>' + html.escape(idea.rstrip('.') + '.') + '</li>' for idea in wireflow_ideas
 ) + '</ul>'
 story('komatsu',n,'kom-hero',[
 (text(n,12),split(ul(n,13,14,15),pic('kom-research','Investigación: referencias y recursos del proyecto.'))),
 ('Visualizar la estructura',split(p(n,49)+'<p>'+html.escape(text(n,50)+' '+text(n,51))+'</p>',pic('kom-map',text(n,52)))),
 (text(n,54),split(wireflow_list,pic('kom-flow',text(n,56)))),
 ('Oportunidades de mejora',p(n,59)+duo(pic('kom-eval1','Tabla de evaluación'),pic('kom-eval2','Tabla de evaluación'))),
 ('PROPUESTAS DESDE LAS OPORTUNIDADES',p(n,63)+duo('<div><h3>Antes</h3>'+pic('kom-before1','Imagen de referencia. Los datos se ocultaron por temas de confidencialidad.')+'</div>','<div><h3>Propuesta</h3>'+pic('kom-after1','Imagen de referencia. Los datos se ocultaron por temas de confidencialidad.')+'</div>')),
 ('Visualizar datos',p(n,69)+pic('kom-ranking-detail')+duo('<div><h3>Antes</h3>'+pic('kom-before2','*Imagen de referencia. Los datos se ocultaron por temas de confidencialidad.')+'</div>','<div><h3>Propuesta</h3>'+pic('kom-after2','Imagen de referencia. Los datos se ocultaron por temas de confidencialidad.')+'</div>'))], labels={
  'Visualizar la estructura': text(n,48),
  'Oportunidades de mejora': text(n,58),
  'PROPUESTAS DESDE LAS OPORTUNIDADES': text(n,62).rstrip(':'),
  'Visualizar datos': text(n,68).rstrip(':'),
 })
 # Original home narrative, with the same project images and sequence.
 n='Inicio'
 page('index.html','Inicio','<section class="hero original-home"><div class="wrap creative-hero"><div class="creative-copy"><p class="eyebrow">Hola, soy Susana</p><h1>Diseño para hacer más claro lo complejo y visibilizar el valor.</h1><p class="sub">'+text(n,2)+'</p><div class="actions"><a class="btn" href="contacto.html">Hablemos ↗</a></div></div></div></section><section class="section"><div class="wrap"><h2>'+text(n,4)+'</h2>'+p(n,5)+'<a class="textlink" href="sobre-mi.html">Sobre mí ↗</a></div></section><section class="section gray"><div class="wrap"><h2>Proyectos</h2>'+cards()+'</div></section><section class="section"><div class="wrap"><h2>'+text(n,9)+'</h2>'+p(n,10)+'<a class="textlink" href="sobre-mi.html">Sobre mí ↗</a></div></section>')
 n='Sobre mi'
 from about_page import render as render_about
 render_about(page)
 n='Blog'
 title = 'Análisis de UX'
 feature = split('<h2>'+title+'</h2><p>Cómo recorrer una interfaz, detectar dónde se atasca una tarea y decidir qué conviene mejorar primero.</p>', pic('blog-original'))
 page('blog.html','Blog',
  '<section class="hero"><div class="wrap"><h1>Blog</h1>'
  '<p class="sub">Aquí compartiré lo que voy aprendiendo al diseñar interfaces, probar su usabilidad y trabajar con sistemas de diseño.</p></div></section>'
  '<section class="section"><div class="wrap">'+feature+'</div></section>'
  '<section class="section gray" id="articulos"><div class="wrap"><div class="section-head"><h2>Artículos</h2></div>'
  '<article><h3>'+title+'</h3><p>Qué observar en un flujo de usuario y cómo documentar los problemas con ejemplos.</p></article>'
  '<article style="margin-top:2rem"><h3>'+text(n,18)+'</h3><p>'+' '.join(text(n,i) for i in [19,20])+'</p></article></div></section>')

