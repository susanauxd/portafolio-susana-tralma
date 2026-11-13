"""Services navigation shared by the landing page and project pages."""
from html import escape

SERVICES = (
    ('identidad-visual', 'Identidad visual'),
    ('prototipado-ui', 'Prototipado UI'),
    ('analisis-ux', 'Análisis de UX'),
)

def render(prefix=''):
    links = ''.join(
        f'<a href="{prefix}#{slug}">{escape(label)}</a>'
        for slug, label in (('servicios', 'Ver servicios'), *SERVICES)
    )
    return (
        '<details class="services-menu"><summary>Servicios</summary>'
        f'<div class="services-links">{links}</div></details>'
    )
