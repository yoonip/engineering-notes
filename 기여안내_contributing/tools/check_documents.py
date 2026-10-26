"""Check local Markdown destinations and machine-readable document paths."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import html
import json
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[2]


def without_fences(text):
    result = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            value = marker.group(1)
            if fence is None:
                fence = value[0], len(value)
            elif value[0] == fence[0] and len(value) >= fence[1]:
                fence = None
        elif fence is None:
            result.append(line)
    return '\n'.join(result)


def destinations(text):
    """Read inline destinations, excluding text inside Markdown code spans."""
    # Code spans: https://spec.commonmark.org/0.31.2/#code-spans
    # Matching backtick runs delimit code spans; unmatched runs remain literal.
    spans = []
    cursor = 0
    while cursor < len(text):
        opener = re.search(r'`+', text[cursor:])
        if opener is None:
            break
        start = cursor + opener.start()
        end = cursor + opener.end()
        escaped = start
        while escaped and text[escaped - 1] == '\\':
            escaped -= 1
        if (start - escaped) % 2:
            cursor = end
            continue
        paragraph_end = re.search(r'\n[ \t]*\n', text[end:])
        limit = end + paragraph_end.start() if paragraph_end else len(text)
        closer = re.search(r'(?<!`)' + re.escape(opener.group()) + r'(?!`)', text[end:limit])
        if closer is None:
            cursor = end
            continue
        stop = end + closer.end()
        spans.append((start, stop))
        cursor = stop
    if spans:
        pieces = []
        cursor = 0
        for start, stop in spans:
            pieces.append(text[cursor:start])
            pieces.append(re.sub(r'[^\n]', ' ', text[start:stop]))
            cursor = stop
        pieces.append(text[cursor:])
        text = ''.join(pieces)
    for match in re.finditer(r'\]\(', text):
        start = match.end()
        if start < len(text) and text[start] == '<':
            end = text.find('>', start + 1)
            if end != -1:
                yield text[start + 1:end]
            continue
        depth, cursor = 0, start
        while cursor < len(text):
            char = text[cursor]
            if char == '\\':
                cursor += 2
                continue
            if char == '(':
                depth += 1
            elif char == ')':
                if depth == 0:
                    yield re.split(r'\s+"', text[start:cursor], maxsplit=1)[0]
                    break
                depth -= 1
            elif char == '\n':
                break
            cursor += 1


def heading_ids(text):
    """Collect GitHub-style heading slugs and explicit HTML anchors."""
    # Rules: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#section-links
    ids = set(re.findall(r'<[^>]*\b(?:id|name)=["\']([^"\']+)["\']', text, re.I))
    generated = set()
    duplicates = {}
    for line in text.splitlines():
        match = re.match(r'^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$', line)
        if not match:
            continue
        title = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', match.group(1))
        title = re.sub(r'(?<!\w)(\*{1,3}|_{1,3})(.+?)\1(?!\w)', r'\2', title)
        title = html.unescape(re.sub(r'<[^>]+>', '', title)).lower()
        slug = ''.join(char for char in title if char.isalnum() or char in '-_ ' or unicodedata.category(char).startswith('M')).replace(' ', '-')
        count = duplicates.get(slug, 0)
        candidate = slug if count == 0 else f'{slug}-{count}'
        while candidate in generated:
            count += 1
            candidate = f'{slug}-{count}'
        duplicates[slug] = count + 1
        generated.add(candidate)
        ids.add(candidate)
    return ids


def check():
    paths = [p for p in ROOT.rglob('*.md') if '.git' not in p.parts]
    texts = {path.resolve(): without_fences(path.read_text(encoding='utf-8-sig')) for path in paths}
    anchors = {path: heading_ids(text) for path, text in texts.items()}
    errors, links = [], 0
    for path in paths:
        text = texts[path.resolve()]
        for target in destinations(text):
            if not target or target.startswith('//'):
                continue
            parsed = urlsplit(target)
            if parsed.scheme:
                continue
            links += 1
            if parsed.path.startswith('/'):
                dest = (ROOT / unquote(parsed.path).lstrip('/')).resolve()
            else:
                dest = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
            if not dest.is_relative_to(ROOT) or not dest.exists():
                errors.append({'file': path.relative_to(ROOT).as_posix(), 'target': target})
            elif parsed.fragment and dest in anchors and unquote(parsed.fragment) not in anchors[dest]:
                errors.append({'file': path.relative_to(ROOT).as_posix(), 'target': target, 'error': 'missing heading anchor'})
        prose = re.sub(r'`[^`]*`', '', text)
        if re.search(r'\*\*\S[^\n]*?\S\*\*', prose):
            errors.append({'file': path.relative_to(ROOT).as_posix(), 'error': 'bold prose'})
    records = 0
    for file in [ROOT / 'catalog.json', *(ROOT / '참고자료_references').glob('*.json')]:
        data = json.loads(file.read_text(encoding='utf-8'))
        for item in data.get('areas', []) + data.get('articles', []) + [p for p in data.get('providers', []) if 'path' in p]:
            records += 1
            if not (ROOT / item['path']).is_file():
                errors.append({'file': file.relative_to(ROOT).as_posix(), 'target': item['path']})
    return {'markdown_files': len(paths), 'local_links': links,
            'catalog_and_source_paths': records, 'errors': errors}


if __name__ == '__main__':
    result = check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(bool(result['errors']))
