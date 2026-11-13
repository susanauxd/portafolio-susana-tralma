"""Separate case narratives from artwork while preserving each section's reading order."""
import re
from itertools import cycle, groupby
from lxml import html
from project_menu import CASES


def content_blocks(element):
    for node in element:
        classes = set(node.get('class', '').split())
        if node.tag in ('figure', 'video') or classes & {'compare', 'essana-gallery', 'web-phones'}:
            yield 'media', node
        elif node.tag == 'div' and 'note' not in classes:
            yield from content_blocks(node)
        else:
            yield 'copy', node


def render_section(match):
    section = html.fragment_fromstring(match.group())
    wrapper = section[0]
    groups = [(kind, list(items)) for kind, items in groupby(content_blocks(wrapper), key=lambda pair: pair[0])]
    section.remove(wrapper)
    for kind, items in groups:
        band = html.Element('div', {'class': f'case-band case-{kind}'})
        for _, element in items:
            band.append(element)
        section.append(band)
    return html.tostring(section, encoding='unicode', method='html')


def regcheq_heading(band):
    heading = band.find('h3')
    if heading is None:
        return
    title = heading.text_content().strip().rstrip(':')
    label = title
    intro = next(iter(band.xpath('./p[not(@class)]')), None)
    if title.startswith('Auditoría'):
        band.remove(band.find('h2'))
        label = 'Proceso'
    elif title.startswith('Arquitectura'):
        title = 'Creación del archivo en Figma aplicando Diseño Atómico asistido IA'
    elif title.startswith('Automatización'):
        title = 'Para mitigar las limitaciones de tiempo, como soporte de validación bajo presión, manteniendo siempre la revisión humana.'
    elif title.startswith('Implementación'):
        title = 'REDISEÑAR Y OPTIMIZAR LAS PANTALLAS DE PRODUCTOS DIGITALES'
    else:
        label = None
    if intro is not None and label is not None:
        band.remove(intro)
    if label and band.find('p[@class="eyebrow"]') is None:
        kicker = html.Element('p', {'class': 'eyebrow'})
        kicker.text = label
        band.insert(0, kicker)
    heading.clear()
    heading.tag = 'h2'
    heading.text = title


def keep_heading_ending(heading):
    words = heading.text_content().rsplit(None, 2)
    if len(words) == 3:
        heading.text = words[0] + ' '
        tail = html.Element('span', {'class': 'text-tail'})
        tail.text = ' '.join(words[1:])
        heading.append(tail)


def render_regcheq_section(match):
    section = html.fragment_fromstring(match.group())
    wrapper = section[0]
    blocks = list(content_blocks(wrapper))
    section.remove(wrapper)
    chapter = html.Element('div', {'class': 'case-band case-copy'})
    section.append(chapter)
    for kind, node in blocks:
        if kind == 'media':
            media = html.Element('div', {'class': 'case-band case-media'})
            section.append(media)
            if node.tag == 'figure':
                row = html.Element('div', {'class': 'regcheq-row'})
                copy = html.Element('div', {'class': 'regcheq-copy'})
                copy.extend(chapter.findall('ul'))
                row.extend([copy, node])
                media.append(row)
            else:
                media.append(node)
        elif node.get('class') == 'note':
            section[-1].append(node)
        else:
            if section[-1] is not chapter:
                chapter = html.Element('div', {'class': 'case-band case-copy'})
                section.append(chapter)
            chapter.append(node)
    for band in section.xpath('./div[@class="case-band case-copy"]'):
        regcheq_heading(band)
        for heading in band.findall('h2'):
            keep_heading_ending(heading)
    return html.tostring(section, encoding='unicode', method='html')


def render_komatsu_section(match):
    section = html.fragment_fromstring(render_section(match))
    chapter = section[0]
    keep_heading_ending(chapter.find('h2'))
    if section.get('id') in ('paso-0', 'paso-2'):
        media = section[1]
        row = html.Element('div', {'class': 'regcheq-row'})
        copy = html.Element('div', {'class': 'regcheq-copy'})
        copy.extend(chapter.find('h2').itersiblings())
        row.extend([copy, media.find('figure')])
        media.append(row)
    if len(section[-1]) == 1 and section[-1][0].get('class') == 'note':
        note_band = section[-1]
        section[-2].append(note_band[0])
        section.remove(note_band)
    return html.tostring(section, encoding='unicode', method='html')


def render_cademsmart_section(match):
    section = html.fragment_fromstring(match.group())
    wrapper = section[0]
    section.remove(wrapper)
    chapter = html.Element('div', {'class': 'case-band case-copy'})
    section.append(chapter)
    for node in list(wrapper):
        if 'story-step' in node.classes:
            node = node[0]
            chapter = html.Element('div', {'class': 'case-band case-copy'})
            section.append(chapter)
        if 'story-split' in node.classes:
            media = html.Element('div', {'class': 'case-band case-media'})
            row = html.Element('div', {'class': 'regcheq-row'})
            copy = next(column for column in node if column.find('figure') is None)
            figure = node.find('.//figure')
            copy.set('class', 'regcheq-copy')
            if chapter.find('h2') is None and len(copy) and copy[0].tag == 'h3':
                label = html.Element('p', {'class': 'eyebrow'})
                label.text = 'USUARIOS'
                chapter.extend([label, copy[0]])
            row.extend([copy, figure])
            media.append(row)
            section.append(media)
        elif 'compare' in node.classes:
            media = html.Element('div', {'class': 'case-band case-media'})
            media.append(node)
            section.append(media)
        elif 'note' in node.classes:
            note = html.Element('div', {'class': 'case-band case-copy'})
            note.append(node)
            section.append(note)
        else:
            chapter.append(node)
    for heading in section.xpath('./div[@class="case-band case-copy"]/h2'):
        keep_heading_ending(heading)
    return html.tostring(section, encoding='unicode', method='html')


def render_essana_web_section(match):
    section = html.fragment_fromstring(match.group())
    wrapper = section[0]
    section.remove(wrapper)
    def kind(node):
        if node.tag == 'figure' or set(node.classes) & {'story-split', 'web-phones'}:
            return 'media'
        return 'copy'
    for category, nodes in groupby(list(wrapper), key=kind):
        band = html.Element('div', {'class': f'case-band case-{category}'})
        for node in nodes:
            if 'story-split' in node.classes:
                node[0].set('class', 'regcheq-copy')
            band.append(node)
        section.append(band)
    return html.tostring(section, encoding='unicode', method='html')


def render_hero(match):
    hero = html.fragment_fromstring(match.group())
    for caption in hero.xpath('.//figure/figcaption'):
        if caption.text_content().strip() == 'Ampliar imagen':
            caption.getparent().remove(caption)
    facts_band = html.Element('div', {'class': 'case-facts'})
    for facts in hero.xpath('.//dl[@class="facts"]'):
        facts_band.append(facts)
    markup = html.tostring(hero, encoding='unicode', method='html')
    if len(facts_band):
        markup += html.tostring(facts_band, encoding='unicode', method='html')
    return markup


def apply(directory):
    for slug in CASES:
        path = directory / f'{slug}.html'
        renderer = {'regcheq': render_regcheq_section, 'komatsu': render_komatsu_section, 'cademsmart': render_cademsmart_section, 'essana-web': render_essana_web_section}.get(slug, render_section)
        page = path.read_text()
        if slug != 'claro':
            page = re.sub(r'<section\b[^>]*class="story-section[^"]*"[^>]*>.*?</section>', renderer,
                      page, flags=re.S)
        page = re.sub(r'<section class="hero original-hero[^"]*">.*?</section>', render_hero,
                      page, count=1, flags=re.S)
        if slug in ('regcheq', 'komatsu', 'cademsmart', 'essana-web', 'essana'):
            tones = cycle(('lavender', 'cyan', 'violet'))
            page = re.sub(r'class="case-band case-copy"',
                          lambda _: f'class="case-band case-copy" data-tone="{next(tones)}"', page)
            page = page.replace('</head>', '<link rel="stylesheet" href="glass.css"></head>')
            page = page.replace('<main ', f'<main class="{slug}-case" ', 1)
        page = page.replace('</head>', '<link rel="stylesheet" href="case-layout.css"></head>')
        if slug == 'claro':
            page = page.replace('</body>', '<script src="claro-card-heights.js" defer></script></body>')
            page = page.replace('<main ', '<main class="claro-case" ', 1).replace('</head>', '<link rel="stylesheet" href="glass.css"></head>')
        path.write_text(page)
