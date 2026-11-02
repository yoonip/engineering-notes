"""공식 링크·앵커·명령·발췌 문장의 원문 존재를 확인합니다. 의미나 실행 성공은 증명하지 않습니다."""
from __future__ import annotations

import base64
import hashlib
import html
from html.parser import HTMLParser
import json
import re
from urllib.parse import quote, unquote, urlsplit
from bs4 import BeautifulSoup

import guides

LIMIT = 1_000_000
AUTOMATIC = '공식 README 구간 추출·한국어 번역'
BLOB = re.compile(r'^/([^/]+/[^/]+)/blob/([^/]+)/(.+)$')


def _reference(url: str):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Source URL must use HTTPS: ' + str(url))
    if parsed.hostname.lower() != 'github.com':
        return None
    match = BLOB.fullmatch(parsed.path)
    if not match:
        return None
    repository, commit, path = match.groups()
    if not re.fullmatch(r'[a-fA-F0-9]{40}', commit):
        raise ValueError('GitHub source must use a fixed commit: ' + url)
    path = unquote(path)
    if parsed.query or parsed.port not in (None, 443) or any(p in ('', '.', '..') for p in path.split('/')):
        raise ValueError('Invalid GitHub document path: ' + url)
    canonical = 'https://github.com/' + repository + '/blob/' + commit + '/' + quote(path, safe='/')
    return canonical, repository, commit, path, unquote(parsed.fragment)


def _blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def _outside_code(text: str) -> str:
    outside, fence = [], None
    for line in text.splitlines():
        stripped = line.strip()
        if fence:
            if re.fullmatch(re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*', stripped):
                fence = None
        else:
            match = re.match(r'^(`{3,}|~{3,})(.*)$', stripped)
            if match:
                fence = match[1]
            else:
                outside.append(line)
    return '\n'.join(outside)


def _anchor_sections(parsed: list[dict]) -> dict[str, int]:
    result, counts = {}, {}
    for index, section in enumerate(parsed):
        if not section['level']:
            continue
        slug = re.sub(r'[^\w\- ]', '', html.unescape(section['heading']).lower()).replace(' ', '-')
        number = counts.get(slug, 0)
        candidate = slug + ('-' + str(number) if number else '')
        while candidate in result:
            number += 1
            candidate = slug + '-' + str(number)
        counts[slug] = number + 1
        result[candidate] = index
    for index, section in enumerate(parsed):
        class AnchorParser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                for name, value in attrs:
                    if name in ('id', 'name') and value:
                        result[value] = index
        AnchorParser(convert_charrefs=True).feed(_outside_code(section['raw']))
    return result


def _anchors(text: str) -> set[str]:
    return set(_anchor_sections(guides.sections(text)))


def _command_sections(document: dict, block: dict) -> list[dict]:
    parsed = guides.sections(document['text'])
    allowed = set(range(len(parsed)))
    fragment = unquote(urlsplit(block['source_url']).fragment)
    if fragment:
        start = _anchor_sections(parsed)[fragment]
        end = next((i for i in range(start + 1, len(parsed)) if parsed[i]['level'] <= parsed[start]['level']), len(parsed))
        allowed &= set(range(start, end))
    if block.get('heading') or block.get('heading_path'):
        candidates, parents = set(), []
        for index, section in enumerate(parsed):
            while parents and section['level'] <= parents[-1]['level']:
                parents.pop()
            path = [item['heading'] for item in parents if item['level']] + [section['heading']]
            matches = path == block['heading_path'] if block.get('heading_path') else section['heading'] == block['heading']
            if matches:
                candidates.add(index)
            parents.append(section)
        allowed &= candidates
    return [section for index, section in enumerate(parsed) if index in allowed]


def _command_units(parsed: list[dict]) -> set[str]:
    units = set()
    for section in parsed:
        for block in section['codes']:
            units.update(line.strip() for line in block['code'].splitlines() if line.strip())
        outside = _outside_code(section['raw'])
        for value in re.findall(r'(?<!`)`(?!`)([^`\n]+)`(?!`)', outside):
            units.add(html.unescape(value).strip())
        for element in BeautifulSoup(outside, 'html.parser').find_all('code'):
            units.update(line.strip() for line in element.get_text().splitlines() if line.strip())
    return units


def verify(guide: dict, readme: dict, getter, token: str = '') -> dict:
    """collect.get과 같은 getter로 필요한 고정판 문서만 읽고 실패 시 게시를 중단합니다."""
    cache, checked, unchecked, command_checks, excerpt_checks = {}, {}, set(), [], []

    def remember(document):
        url = document.get('source_url', '')
        reference = _reference(url)
        if reference is None:
            raise ValueError('Cached document needs a pinned GitHub URL: ' + url)
        raw = document.get('text', '').encode('utf-8')
        sha = document.get('sha')
        if len(raw) > LIMIT or not sha or _blob_sha(raw) != sha:
            raise ValueError('Source content size or SHA mismatch: ' + url)
        cache[reference[0]] = dict(document, sha=sha)

    for document in [readme] + readme.get('documents', []):
        if document.get('status', 'ok') == 'ok':
            remember(document)

    def source(url):
        if not isinstance(url, str) or not url:
            raise ValueError('Source URL is missing')
        reference = _reference(url)
        if reference is None:
            unchecked.add(url)
            return None
        canonical, repository, commit, path, fragment = reference
        if canonical not in cache:
            api = 'https://api.github.com/repos/' + repository + '/contents/' + quote(path, safe='/') + '?ref=' + commit
            try:
                response, _ = getter(api, token)
                data = json.loads(response)
                if data.get('encoding') != 'base64' or not isinstance(data.get('content'), str):
                    raise ValueError('Expected base64 document content')
                encoded = ''.join(data['content'].split())
                if len(encoded) > (LIMIT + 2) // 3 * 4:
                    raise ValueError('Document exceeds content limit')
                raw = base64.b64decode(encoded, validate=True)
                remember({'source_url': canonical, 'text': raw.decode('utf-8'), 'sha': data.get('sha')})
            except Exception as exc:
                raise ValueError('Cannot verify source document: ' + url) from exc
        document = cache[canonical]
        if fragment and fragment not in _anchors(document['text']):
            raise ValueError('Source anchor is missing: ' + url)
        checked[canonical] = {'url': canonical, 'sha': document['sha'], 'commit': commit,
                              'bytes': len(document['text'].encode('utf-8'))}
        return document

    for item in guide.get('sources', []):
        source(item.get('url', ''))
    for item in guide.get('source_refs', []):
        source(item if isinstance(item, str) else item.get('url', item.get('source_url', '')))
    if guide.get('readme_url'):
        source(guide['readme_url'])
    automatic = guide.get('method') == AUTOMATIC
    for name in ('install_code', 'example_code'):
        block = guide.get(name)
        if block is None:
            continue
        code = block.get('code', '')
        if not code.strip():
            raise ValueError('Command block is empty: ' + name)
        document = source(block.get('source_url', ''))
        if document is None:
            raise ValueError('Command requires a pinned GitHub source: ' + name)
        parsed = _command_sections(document, block)
        if automatic or block.get('language', '').lower() in ('python', 'py', 'javascript', 'js', 'typescript', 'ts', 'c', 'cpp', 'java'):
            wanted = code.splitlines()
            valid = any(any(lines[index:index + len(wanted)] == wanted
                            for index in range(len(lines) - len(wanted) + 1))
                        for section in parsed for item in section['codes']
                        for lines in [item['code'].splitlines()])
            mode = 'contiguous_fenced_excerpt'
        else:
            units = _command_units(parsed)
            valid = all(line.strip() in units for line in code.splitlines() if line.strip())
            mode = 'manual_exact_command_units_inline_table_or_fence'
        if not valid:
            raise ValueError('Command does not match its source: ' + name)
        command_checks.append({'field': name, 'mode': mode, 'source_url': block['source_url'],
                               'nonempty_lines': sum(bool(line.strip()) for line in code.splitlines())})

    def walk(value, automatic_item=False):
        if isinstance(value, dict):
            original = value.get('original')
            if isinstance(original, str):
                document = source(value.get('source_url', ''))
                if document is None:
                    raise ValueError('Excerpt requires a pinned GitHub source')
                heading = value.get('heading') or value.get('section')
                matching = [section for section in guides.sections(document['text'])
                            if not heading or section['heading'] == heading]
                if not original.strip() or not any(original in section['paragraphs'] for section in matching):
                    raise ValueError('Original excerpt does not match its source paragraph or section')
                excerpt_checks.append({'source_url': value['source_url'], 'section': heading,
                                       'mode': 'parsed_paragraph_presence'})
            for key, item in value.items():
                if key == 'source_urls' and isinstance(item, list):
                    for url in item:
                        source(url)
                elif key == 'source_url' and (automatic_item or 'original' in value):
                    source(item)
                elif key == 'readme_url':
                    source(item)
                else:
                    walk(item, automatic_item)
        elif isinstance(value, list):
            for item in value:
                walk(item, automatic_item)

    if automatic:
        for field in ('features', 'audience', 'installation', 'examples'):
            walk(guide.get(field, []), True)
    assessment = guide.get('assessment', {})
    walk(assessment, assessment.get('origin') == 'extracted')
    return {'documents_checked': len(checked), 'commands_checked': len(command_checks),
            'sources': [checked[key] for key in sorted(checked)], 'command_checks': command_checks,
            'excerpts_checked': len(excerpt_checks), 'excerpt_checks': excerpt_checks,
            'unchecked_urls': sorted(unchecked),
            'scope': '고정판 문서·앵커·명령·발췌 문장의 원문 존재만 확인합니다. 외부 링크 도달 여부, 번역·해석의 정확성, 명령 실행 결과는 검증하지 않습니다.'}
