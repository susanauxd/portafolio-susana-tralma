"""Reserve media geometry and expose an accessible viewer without changing case copy."""
import re
from pathlib import Path
from PIL import Image

def link_detail(figure, root):
 markup=figure.group()
 image=re.search(r'<img\b[^>]* src="([^"]+)"[^>]*>',markup)
 if not image:
  return markup
 preview=Path(image[1])
 detail=next((p for p in (root/'assets/detail').glob(preview.stem+'.*') if p.suffix in ('.png','.webp','.jpg','.jpeg')),None)
 target=detail.relative_to(root).as_posix() if detail else image[1]
 markup=markup.replace('href="'+image[1]+'"','href="'+target+'"')
 if '<a ' not in markup:
  markup=markup.replace(image[0],'<a href="'+target+'" class="case-image-open">'+image[0]+'</a>')
 if not re.search(r'<figcaption[^>]*>.*?<a ',markup,re.S):
  action='<a class="textlink figure-enlarge" href="'+target+'">Ampliar imagen</a>'
  if '</figcaption>' in markup:
   markup=markup.replace('</figcaption>',action+'</figcaption>')
  else:
   markup=markup.replace('</figure>','<figcaption>'+action+'</figcaption></figure>')
 return markup

def apply(directory):
 root=Path(directory)
 for file in root.glob('*.html'):
  s=file.read_text()
  def size(m):
   tag=m.group(0);src=re.search(r'\bsrc="([^"]+)"',tag)
   if not src:return tag
   p=root/src[1]
   if not p.is_file():return tag
   with Image.open(p) as im:w,h=im.size
   tag=re.sub(r'\s(?:width|height)="[^"]*"','',tag)
   ratio=f'--media-ratio:{w}/{h}'
   if 'style="' in tag:
    tag=tag.replace('style="','style="'+ratio+';',1)
   else:
    tag=tag[:-1]+f' style="{ratio}">'
   return tag[:-1]+f' width="{w}" height="{h}" decoding="async">'
  s=re.sub(r'<img\b[^>]*>',size,s)
  s=s.replace('<main id="contenido">','<main id="contenido" tabindex="-1">')
  # Keep the original crop container and image; make its existing surface operable.
  s=re.sub(r'<span class="image-surface([^\"]*)"([^>]*)>(<img[^>]*src="([^"]+)"[^>]*>)</span>',lambda m:f'<a class="image-surface{m[1]}"{m[2]} href="{m[4]}" aria-label="Ampliar imagen">{m[3]}</a>',s)
  if 'class="hero original-hero' in s:
   s=re.sub(r'<figure\b[^>]*>.*?</figure>',lambda m:link_detail(m,root),s,flags=re.S)
  file.write_text(s)
