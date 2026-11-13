"""Project names and descriptions used in navigation and on the homepage."""
from html import escape

CASES = {
    'regcheq': ('Regcheq', 'Refactorización de UI kit y sistema de diseño', 'UI'),
    'komatsu': ('Komatsu', 'Evaluación de una interfaz minera', 'UX'),
    'cademsmart': ('Cademsmart', 'Migración de plataforma y rediseño móvil', 'UI'),
    'claro': ('Claro Chile', 'Rediseño de la app de prepago', 'UX'),
    'essana': ('Clínica Essana', 'Identidad visual y manual de marca', 'Diseño gráfico'),
    'essana-web': ('Clínica Essana', 'Diseño de sitio web y aplicación', 'UI'),
}


def render(current_page):
    items = []
    for number, (slug, (name, description, discipline)) in enumerate(CASES.items(), 1):
        active = ' aria-current="page"' if current_page == slug + '.html' else ''
        items.append(
            f'<li><a href="{slug}.html"{active}><span class="case-number" aria-hidden="true">{number}</span>'
            f'<span class="case-copy"><strong>{escape(name)}</strong><small>{escape(description)}</small></span><span class="discipline-badge">{discipline}</span></a></li>'
        )
    return '<details class="case-menu"><summary>Portafolio</summary><ol class="case-index">' + ''.join(items) + '</ol></details>'
