"""Apply shared type and directional icons to each generated page."""
import re
from pathlib import Path

PATHS = {
    '→': 'M4 12h15m-6-6 6 6-6 6',
    '←': 'M20 12H5m6-6-6 6 6 6',
    '↑': 'M12 20V5m-6 6 6-6 6 6',
    '↓': 'M12 4v15m-6-6 6 6 6-6',
    '↗': 'M5 19 18 6M7 6h11v11',
    '⌄': 'm6 9 6 6 6-6',
    '☰': 'M4 6h16M4 12h16M4 18h16',
    '×': 'm6 6 12 12M18 6 6 18',
}

def icon(symbol):
    return f'<svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="{PATHS[symbol]}"/></svg>'

def decorate_control(match):
    parts = re.split('(<[^>]+>)', match.group())
    for i in range(0, len(parts), 2):
        parts[i] = re.sub('[→←↑↓↗⌄☰×]', lambda m: icon(m.group()), parts[i])
    return ''.join(parts)

def apply(directory):
    root = Path(__file__).parent
    css = (root/'type-system.css').read_text()
    js = (root/'title-effects.js').read_text()
    for page in directory.glob('*.html'):
        markup = page.read_text()
        if 'class="hero original-hero' in markup:
            markup = re.sub(r'<img src="assets/([^".]+)\.(jpeg|webp)"', r'<img data-motion="assets/\1-motion.webp" src="assets/\1.\2"', markup, count=1)
        markup = re.sub(r'<(?:a|button)\b[^>]*>.*?</(?:a|button)>', decorate_control, markup, flags=re.S)
        if page.name in ('index.html', 'contacto.html'):
            markup = markup.replace('</style>', css + '\n</style>')
            markup = markup.replace('</body>', '<script>' + js + '</script></body>')
        page.write_text(markup)
    with (directory/'style.css').open('a') as target:
        target.write('\n' + css)
    script = directory/'script.js'
    source = script.read_text().replace("button.textContent = open ? '×' : '☰';", "button.innerHTML = open ? '" + icon('×') + "' : '" + icon('☰') + "';")
    source = source.replace('<span aria-hidden="true">×</span>', icon('×'))
    script.write_text(source + '\n' + js)
