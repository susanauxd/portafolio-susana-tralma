"""Improve paragraph endings without rewriting or replacing any source text."""
import re
from html import unescape
from pathlib import Path

PLAIN_BLOCK = re.compile(r'(<(?P<tag>p|li|dd|figcaption)\b[^>]*>)(?P<copy>[^<]+)(</(?P=tag)>)')
PLAIN_NOTE = re.compile(r'(<div class="note">)([^<]+)(</div>)')

def protect_tail(copy):
    # Short endings stay together when there is room; CSS allows them to wrap
    # inside their own box on narrow screens or with enlarged text.
    match = re.search(r'(?P<tail>\S+\s+\S+)(?P<trailing>\s*)$', copy)
    if not match or len(copy.split()) < 5:
        return copy
    tail = match.group('tail')
    if len(unescape(tail)) > 32:
        return copy
    return copy[:match.start('tail')] + '<span class="text-tail">' + tail + '</span>' + match.group('trailing')

def apply(directory):
    for path in Path(directory).glob('*.html'):
        markup = path.read_text()
        markup = PLAIN_BLOCK.sub(lambda m: m.group(1)+protect_tail(m.group('copy'))+m.group(4), markup)
        markup = PLAIN_NOTE.sub(lambda m: m.group(1)+protect_tail(m.group(2))+m.group(3), markup)
        path.write_text(markup)
