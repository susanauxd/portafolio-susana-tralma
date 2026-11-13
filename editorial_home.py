"""Self-contained editorial homepage with embedded case cover images."""
from pathlib import Path
import html
from project_menu import CASES

def render(projects):
 root=Path(__file__).parent
 cards=[]
 markers=[]
 for i,(slug,name,meta,description,im) in enumerate(projects,1):
  image=f'assets/{im}.webp'
  name = 'Clínica Essana' if slug == 'essana-web' else name
  discipline = 'Diseño gráfico' if slug == 'essana' else 'UI' if slug == 'essana-web' else 'UX/UI'
  markers.append(f'<button type="button" class="project-marker" data-slide="{i-1}" aria-controls="project-slider"><span>{i} / {html.escape(name)}</span><small>{discipline}</small></button>')
  cards.append(f'''<article class="folio-slide" aria-label="{i} de {len(projects)}: {html.escape(name)}"><a class="folio-card" href="{slug}.html" aria-label="Ver {html.escape(name)}: {CASES[slug][1]}"><div class="folio-card-head"><span>{html.escape(name)}</span><span>{discipline}</span></div><img src="{image}" alt="Portada del proyecto {html.escape(name)}" width="1600" height="1000"><div class="folio-card-foot"><h2>{CASES[slug][1]}</h2><span>Ver ↗</span></div></a></article>''')
 output=(root/'editorial-home.html').read_text().replace('{{PROJECTS}}',''.join(cards)).replace('{{MARKERS}}',''.join(markers))
 (root/'dist/index.html').write_text(output)
 start = output.index('<main id="contenido">') + len('<main id="contenido">')
 contact = output[:start] + (root/'editorial-contact.html').read_text() + output[output.index('</main>'):]
 contact = contact.replace('class="portfolio-home"', 'class="portfolio-home contact-view"').replace('<title>Susana Tralma — Diseñadora Gráfica y UX/UI</title>', '<title>Contacto · Susana Tralma</title>').replace('<a href="contacto.html">Contacto</a>', '<a href="contacto.html" aria-current="page">Contacto</a>')
 (root/'dist/contacto.html').write_text(contact)
