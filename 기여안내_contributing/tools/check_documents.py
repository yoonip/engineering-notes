"""Check local Markdown destinations and machine-readable document paths."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys

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
    """Read inline destinations including balanced parentheses in filenames."""
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


def check():
    paths = [p for p in ROOT.rglob('*.md') if '.git' not in p.parts]
    errors, links = [], 0
    for path in paths:
        text = without_fences(path.read_text(encoding='utf-8-sig'))
        for target in destinations(text):
            if not target or target.startswith(('#', '//')):
                continue
            parsed = urlsplit(target)
            if parsed.scheme:
                continue
            links += 1
            dest = (path.parent / unquote(parsed.path)).resolve()
            if not dest.is_relative_to(ROOT) or not dest.exists():
                errors.append({'file': path.relative_to(ROOT).as_posix(), 'target': target})
        prose = re.sub(r'`[^`]*`', '', text)
        if re.search(r'\*\*\S[^\n]*?\S\*\*', prose):
            errors.append({'file': path.relative_to(ROOT).as_posix(), 'error': 'bold prose'})
    records = 0
    for file in [ROOT / 'catalog.json', *(ROOT / '참고자료_references').glob('*.json')]:
        data = json.loads(file.read_text(encoding='utf-8'))
        for item in data.get('areas', []) + data.get('articles', []):
            records += 1
            if not (ROOT / item['path']).is_file():
                errors.append({'file': file.relative_to(ROOT).as_posix(), 'target': item['path']})
    return {'markdown_files': len(paths), 'local_links': links,
            'catalog_and_source_paths': records, 'errors': errors}


if __name__ == '__main__':
    result = check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(bool(result['errors']))
