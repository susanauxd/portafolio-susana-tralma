from pathlib import Path
import re
from project_menu import render as project_menu


FOOTER = '''<footer class="portfolio-footer">
<div class="footer-inner">
<div class="footer-info"><div><strong class="footer-name">SUSANA TRALMA</strong>
<p>Diseñadora gráfica - UX/UI</p></div>
<div class="footer-socials" role="group" aria-label="Contacto y redes profesionales">
<a href="mailto:susanauxd@gmail.com">susanauxd@gmail.com</a>
<a href="https://github.com/susanauxd" target="_blank" rel="noopener noreferrer">GitHub ↗</a>
<a href="https://www.behance.net/susanatralma" target="_blank" rel="noopener noreferrer">Behance ↗</a>
<a href="https://www.linkedin.com/in/susana-tralma/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>
</div></div>
<p class="footer-credit">Hecho con <svg role="img" aria-label="amor" focusable="false" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21s-9-5.5-9-12a5 5 0 0 1 9-3 5 5 0 0 1 9 3c0 6.5-9 12-9 12z"/></svg> por Susana Tralma 2026</p>
</div></footer>'''


def apply(directory):
    css = (Path(__file__).parent/'button-system.css').read_text()
    header_template = (Path(__file__).parent/'site-header.html').read_text().strip()
    for page in directory.glob('*.html'):
        markup = re.sub(r'<footer\b[^>]*>.*?</footer>', '', page.read_text(), flags=re.S)
        header = header_template.replace('{{PORTFOLIO_MENU}}', project_menu(page.name))
        for target in ('sobre-mi.html', 'contacto.html'):
            if target == page.name:
                header = header.replace(f'href="{target}"', f'href="{target}" aria-current="page"')
        markup = markup.replace('{{SITE_HEADER}}', header).replace('</head>', '<link rel="stylesheet" href="site-nav.css"></head>').replace('</body>', '<script src="site-nav.js"></script></body>')
        if page.name in ('index.html', 'sobre-mi.html', 'proyectos.html'):
            markup = markup.replace('</head>', '<link rel="stylesheet" href="glass.css"></head>')
        if page.name in ('sobre-mi.html', 'proyectos.html'):
            markup = markup.replace('<body>', '<body class="portfolio-interior">')
            markup = markup.replace('</head>', '<link rel="stylesheet" href="portfolio-interior.css"></head>')
        if page.name in ('index.html', 'contacto.html'):
            markup = markup.replace('</style>', css + '</style>')
        markup = markup.replace('</main>', '</main>' + FOOTER, 1)
        page.write_text(markup)
    stylesheet = directory/'style.css'
    stylesheet.write_text(stylesheet.read_text() + '\n' + css)
