"""Essana web: literal narrative and original interface artwork from the supplied PDF."""
import html,json
from pathlib import Path
from PIL import Image
COPY={
'objective':'Este es un proyecto conceptual de diseño de interfaz digital para la plataforma web y aplicación móvil.',
'clinic':'Clínica Essana es un centro de salud integral que combina medicina, tecnología y empatía para acompañar a las personas en su bienestar físico y emocional. Especializada en control de peso, metabolismo y salud femenina, se destaca por un enfoque humano, ético y multidisciplinario.',
'usability':'Moderna, limpia, pensada en la usabilidad.'}
def render(page):
 def p(key):return '<p>'+html.escape(COPY[key])+'</p>'
 def fig(name,alt):
  src='assets/essana-web-'+name+'.webp'
  phone=' phone-silhouette' if name in {'feature','onboarding','agenda','progress'} else ''
  w,h=Image.open(Path(__file__).parent/'dist'/src).size
  return f'<figure><a class="essana-artwork image-surface{phone}" href="{src}" target="_blank" rel="noopener" aria-label="Ampliar: {html.escape(alt)}"><img src="{src}" width="{w}" height="{h}" alt="{html.escape(alt)}" loading="lazy"></a><figcaption><a class="textlink" href="{src}" target="_blank" rel="noopener">Ampliar imagen ↗</a></figcaption></figure>'
 sections=[
 ('acerca','CONTEXTO','Acerca del proyecto','<div class="story-split"><div><h3>Objetivo</h3>'+p('objective')+'<h3>Clínica Essana</h3>'+p('clinic')+'</div>'+fig('context','Aplicación de la identidad de Clínica Essana en publicidad exterior')+'</div>'),
 ('tipografia','','Tipografía',fig('type','Poppins es una tipografía con formas limpias y modernas, legible y con capacidad de combinar con otras tipografías. Poppins: Bold, Medium, Regular.')),
 ('color','COLOR','Legibilidad y contraste',fig('color','Color: #F4F4F4, #DDD6FF, #6941C6 y #1D2939')),
 ('diseno','DISEÑO',COPY['usability'],fig('landing','Interfaz web de Clínica Essana')+fig('feature','Pantalla de bienvenida de la aplicación de Clínica Essana')),
 ('administrador','','Administrador de datos','<p>Solicitud de citas · Anuncios · Evaluaciones</p>'+fig('dashboard','Administrador de datos: citas, anuncios y evaluaciones')+fig('registration','Registro de cuenta de Clínica Essana')),
 ('medicos','DISEÑO','Propuesta versión desktop',fig('desktop','Interfaz de Clínica Essana en escritorio')),
 ('app','DISEÑO','Propuesta versión App móvil','<div class="web-phones"><div><h3>Onboarding</h3>'+fig('onboarding','App: Onboarding')+'</div><div><h3>Agenda</h3>'+fig('agenda','App: Agenda y reservas')+'</div><div><h3>Progreso</h3>'+fig('progress','App: Progreso y resumen del día')+'</div></div>')]
 body='<section class="hero original-hero essana-web-hero"><div class="wrap"><a class="breadcrumb" href="proyectos.html#ui">← Volver a proyectos</a><div class="story-split"><div><p class="eyebrow">2025 / Proyecto conceptual</p><h1>Clínica Essana</h1><p class="sub">Tu bienestar evoluciona</p></div>'+fig('cover','Clínica Essana: proyecto conceptual web y app, 2025')+'</div></div></section><div class="original-story essana-web-story">'
 for key,label,title,content in sections:
  eyebrow=f'<p class="eyebrow">{label}</p>' if label else ''
  body+=f'<section id="{key}" class="story-section"><div class="wrap">{eyebrow}<h2>{title}</h2>{content}</div></section>'
 body+='</div><div class="wrap story-back"><a class="textlink" href="proyectos.html#ui">← Volver a proyectos</a></div>'
 page('essana-web.html','Clínica Essana · Web y app',body,'proyectos.html')
