"""공식 README의 기능·대상·설치·예시 구간을 골라 한국어 안내로 연결합니다.

문서는 데이터로만 읽습니다. 추출한 명령·스크립트·모델은 실행하지 않습니다.
"""
from __future__ import annotations

import base64
from datetime import datetime, timezone
import json
import posixpath
import re
from urllib.error import HTTPError
from urllib.parse import quote, unquote, urlsplit


def fetch_readme(repo: dict, token: str, getter) -> dict:
    """기본 브랜치의 커밋을 고정하고 그 판본의 README를 읽습니다."""
    base = 'https://api.github.com/repos/' + repo['full_name']
    ref, _ = getter(base + '/git/ref/heads/' + quote(repo['default_branch'], safe=''), token)
    commit = json.loads(ref)['object']['sha']
    if not re.fullmatch(r'[a-f0-9]{40}', commit):
        raise ValueError('Invalid README commit')
    try:
        response, _ = getter(base + '/readme?ref=' + commit, token)
    except HTTPError as exc:
        if exc.code == 404:
            return {'status': 'not_found', 'commit': commit, 'text': '', 'sha': None,
                    'source_url': repo['html_url'] + '/tree/' + commit, 'fetched_at': datetime.now(timezone.utc).isoformat()}
        raise
    data = json.loads(response)
    if data.get('encoding') != 'base64' or not data.get('content'):
        raise ValueError('README content unavailable or too large')
    raw = base64.b64decode(data['content'])
    if len(raw) > 1_000_000:
        raise ValueError('README exceeds content limit')
    path = data['path']
    return {'status': 'ok', 'text': raw.decode('utf-8'), 'sha': data['sha'], 'commit': commit,
            'path': path, 'source_url': repo['html_url'] + '/blob/' + commit + '/' + quote(path, safe='/'),
            'fetched_at': datetime.now(timezone.utc).isoformat()}


def linked_documents(repo: dict, readme: dict, token: str, getter) -> list[dict]:
    """README가 연결한 같은 저장소의 설치·사용 Markdown 문서를 최대 두 개 읽습니다."""
    result, seen = [], set()
    for label, target in re.findall(r'(?<!!)\[([^\]\n]+)\]\(([^\s)]+)\)', readme['text']):
        if not re.search(r'install|quick.?start|getting.?started|usage|examples?|comparisons?|alternatives?|설치|사용|비교', label + ' ' + target, re.I):
            continue
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or parsed.path.startswith('/'):
            continue
        path = posixpath.normpath(posixpath.join(posixpath.dirname(readme.get('path', 'README.md')), unquote(parsed.path)))
        if path.startswith('../') or path == '..' or not path.lower().endswith('.md') or path == readme.get('path') or path in seen:
            continue
        seen.add(path)
        url = 'https://api.github.com/repos/' + repo['full_name'] + '/contents/' + quote(path, safe='/') + '?ref=' + readme['commit']
        try:
            response, _ = getter(url, token)
            data = json.loads(response)
            if data.get('encoding') != 'base64' or not data.get('content'):
                continue
            raw = base64.b64decode(data['content'])
            if len(raw) > 1_000_000:
                continue
        except HTTPError as exc:
            if exc.code == 404:
                continue
            raise
        result.append({'text': raw.decode('utf-8'), 'sha': data['sha'], 'path': path,
                       'source_url': repo['html_url'] + '/blob/' + readme['commit'] + '/' + quote(path, safe='/')})
        if len(result) == 2:
            break
    return result


def plain(text: str) -> str:
    """번역할 짧은 설명에서 링크 문법과 장식만 제거합니다."""
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'^\s*(?:>\s*)?(?:[-+*]\s+|\d+[.)]\s+)?', '', text)
    return ' '.join(text.replace('**', '').replace('`', '').split())


def sections(markdown: str) -> list[dict]:
    """ATX·Setext 제목과 코드 펜스를 구분하고 코드 안의 #을 제목으로 읽지 않습니다."""
    def section(heading, level):
        return {'heading': heading, 'level': level, 'paragraphs': [], 'codes': [], 'links': [], 'tables': [], '_rows': []}

    result = [section('Introduction', 0)]
    paragraph, code, fence, language, context = [], [], None, '', ''

    def flush():
        if paragraph:
            text = plain(' '.join(paragraph))
            if text:
                result[-1]['paragraphs'].append(text)
            paragraph.clear()

    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if fence:
            if re.fullmatch(re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*', stripped):
                result[-1]['codes'].append({'language': language, 'code': '\n'.join(code), 'context': context})
                code, fence = [], None
            else:
                code.append(line)
            continue
        match = re.match(r'^(`{3,}|~{3,})([\w+.-]*)\s*$', stripped)
        if match:
            flush()
            fence, language = match.groups()
            context = result[-1]['paragraphs'][-1] if result[-1]['paragraphs'] else ''
            continue
        if result[-1]['_rows'] and result[-1]['_rows'][-1] and not stripped.startswith('|'):
            result[-1]['_rows'].append('')
        heading = re.match(r'^ {0,3}(#{1,6})\s+(.+?)\s*#*$', line)
        if heading:
            flush()
            result.append(section(plain(heading[2]), len(heading[1])))
        elif stripped and index + 1 < len(lines) and re.fullmatch(r'(?:={3,}|-{3,})\s*', lines[index + 1].strip()):
            flush()
            level = 1 if lines[index + 1].lstrip().startswith('=') else 2
            result.append(section(plain(line), level))
        elif re.fullmatch(r'(?:={3,}|-{3,})\s*', stripped):
            flush()
        elif not stripped:
            flush()
        elif stripped.startswith('|'):
            flush()
            result[-1]['_rows'].append(stripped)
        elif not stripped.startswith(('<', '[!')):
            paragraph.append(line)
        for label, url in re.findall(r'(?<!!)\[([^\]\n]+)\]\((https://[^\s)]+)\)', line):
            result[-1]['links'].append({'label': label, 'url': url, 'context': plain(line),
                                       'kind': 'table' if stripped.startswith('|') else 'text'})
    flush()
    # 닫히지 않은 코드 블록은 설치 예시로 재게시하지 않습니다.
    for item in result:
        rows = item.pop('_rows')
        for index in range(len(rows) - 1):
            header = [cell.strip() for cell in re.split(r'(?<!\\)\|', rows[index].strip('|'))]
            separator = [cell.strip() for cell in rows[index + 1].strip('|').split('|')]
            if len(header) < 2 or len(header) != len(separator) or not all(re.fullmatch(r':?-{3,}:?', cell) for cell in separator):
                continue
            data = []
            for row in rows[index + 2:]:
                cells = [cell.strip() for cell in re.split(r'(?<!\\)\|', row.strip('|'))]
                if len(cells) != len(header) or all(re.fullmatch(r':?-{3,}:?', cell) for cell in cells):
                    break
                data.append(cells)
            if data:
                item['tables'].append({'header': header, 'rows': data})
    return result


PATTERNS = {
    'features': r'features?|what.*does|what.*get|capabilit|overview|功能|특징|기능',
    'audience': r'who.*for|use.?cases?|when.*use|대상|활용|适用',
    'installation': r'install|quick.?start|getting.?started|setup|requirements?|prerequisites?|설치|시작|安装',
    'examples': r'usage|examples?|how.*use|workflow|사용|예시|用法|示例',
}


def select_sections(parsed: list[dict], kind: str) -> list[dict]:
    """일치 제목의 하위 절만 포함하고 다음 동급 제목을 넘어가지 않습니다."""
    selected, active_level = [], None
    for section in parsed:
        matches = re.search(PATTERNS[kind], section['heading'], re.I)
        if re.search(r'uninstall|remov|changelog|release.notes|security.policy', section['heading'], re.I):
            matches = None
            active_level = None
        if matches:
            active_level = min(active_level, section['level']) if active_level is not None else section['level']
        elif active_level is not None and section['level'] <= active_level:
            active_level = None
        if active_level is not None:
            selected.append(section)
    return selected


def excerpts(parsed: list[dict], kind: str) -> list[dict]:
    """원문 문장을 잘라 명령의 뜻이 달라지지 않도록 완전한 짧은 항목만 고릅니다."""
    selected = select_sections(parsed, kind)
    if kind == 'features' and not selected:
        selected = parsed[:2]
    result, budget = [], 40 if kind == 'features' else 25
    for section in selected:
        for text in section['paragraphs']:
            words = len(text.split())
            minimum = 1 if kind == 'installation' else 3
            if minimum <= words <= min(budget, 65) and len(text) <= 650 and not text.lower().startswith(('copyright', 'license')):
                result.append({'heading': section['heading'], 'original': text,
                               'source_url': section.get('source_url')})
                budget -= words
                if len(result) == 2 or budget < minimum:
                    return result
    return result


def code_example(parsed: list[dict], kind: str) -> dict | None:
    for section in select_sections(parsed, kind):
        if kind == 'installation' and re.search(r'prerequisites?|requirements?', section['heading'], re.I):
            continue
        for block in section['codes']:
            text = block['code'].strip('\n')
            # 짧은 명령·예시를 통째로 남기며 긴 설치 스크립트를 임의로 자르지 않습니다.
            if text and len(text) <= 1200 and len(text.splitlines()) <= 14 and len(text.split()) <= 35:
                return dict(block, code=text, heading=section['heading'], source_url=section.get('source_url'))
    return None


def korean_text(source: str, introductions) -> dict:
    if re.search(r'[가-힣]', source):
        return {'text': source, 'method': '공식 한국어 원문'}
    if re.search(r'[\u4e00-\u9fff\u3040-\u30ff]', source):
        return {'text': '', 'method': '원문 병기'}
    try:
        translated = introductions.translate(source)
    except ValueError as exc:
        # Python·Node.js 같은 짧은 환경 표기가 그대로 남는 경우 원문으로 표시합니다.
        if str(exc) == 'Korean translation unavailable' and len(source.split()) <= 4:
            return {'text': source, 'method': '짧은 원문 표기'}
        raise
    return {'text': translated['text'], 'method': translated['method'] + ' 기계번역'}


def make_guide(repo: dict, readme: dict, details: dict, introductions) -> dict:
    reviewed = details.get(repo['full_name'].casefold())
    if reviewed and reviewed.get('repository_id') == repo['id'] and reviewed.get('readme_sha') == readme['sha']:
        return dict(reviewed, method='공식 문서 한국어 해설', readme_url=readme['source_url'])
    parsed = []
    for document in [readme] + readme.get('documents', []):
        for section in sections(document['text']):
            section['source_url'] = document['source_url']
            parsed.append(section)
    guide = {'method': '공식 README 구간 추출·한국어 번역', 'readme_url': readme['source_url'],
             'checked_at': readme['fetched_at'][:10], 'readme_sha': readme['sha'], 'repository_id': repo['id']}
    for kind in PATTERNS:
        items = excerpts(parsed, kind)
        for item in items:
            item.update(korean_text(item['original'], introductions))
        guide[kind] = items
    guide['install_code'] = code_example(parsed, 'installation')
    guide['example_code'] = code_example(parsed, 'examples')
    for name in ('install_code', 'example_code'):
        block = guide[name]
        if block and block.get('context') and len(block['context'].split()) <= 35:
            block['context_translation'] = korean_text(block['context'], introductions)
    guide['sources'] = [{'title': '공식 README (' + readme['commit'][:12] + ')', 'url': readme['source_url']}]
    guide['sources'] += [{'title': document['path'], 'url': document['source_url']} for document in readme.get('documents', [])]
    return guide


def render_guide(guide: dict, clean) -> list[str]:
    """기능·사용·비교 항목을 모든 프로젝트에 같은 순서로 표시합니다."""
    lines = []
    headings = [('features', '어떤 일을 하나요', 'features_ko'),
                ('audience', '누구에게 유용한가요', 'audience_ko'),
                ('installation', '설치 방법', 'install_steps_ko'),
                ('examples', '사용 예시', 'example_steps_ko')]
    for kind, title, manual in headings:
        lines.extend(['### ' + title, ''])
        if kind == 'installation' and guide.get('prerequisites_ko'):
            lines.append('준비 사항: ' + clean(' '.join(guide['prerequisites_ko'])))
            lines.append('')
        if guide.get(manual):
            for text in guide[manual]:
                lines.append('- ' + clean(text))
            lines.append('')
        elif guide.get(kind):
            for item in guide[kind]:
                if item.get('text'):
                    lines.extend([clean(item['text']), ''])
                lines.extend(['원문 (' + clean(item['heading']) + '): ' + clean(item['original']), ''])
        else:
            fallbacks = {'features': '프로젝트의 기능은 위 소개와 공식 README에서 확인하실 수 있습니다.',
                         'audience': '공식 README에서 별도의 대상 사용자 설명을 찾지 못했습니다. 위 기능과 사용 예시를 기준으로 용도를 확인하실 수 있습니다.',
                         'installation': '공식 README에 짧게 옮길 수 있는 설치 절차가 없습니다. 연결된 원문의 설치·배포 안내를 확인해 주세요.',
                         'examples': '공식 README에서 짧게 옮길 수 있는 사용 예시를 찾지 못했습니다. 아래 원문에서 프로젝트의 현재 사용법을 확인해 주세요.'}
            lines.extend([fallbacks[kind], ''])
        block = guide.get('install_code' if kind == 'installation' else 'example_code' if kind == 'examples' else '_none')
        if block:
            code = block['code']
            fence = '`' * max(3, max((len(m[0]) for m in re.finditer(r'`+', code)), default=0) + 1)
            language = block.get('language', '')
            language = language if re.fullmatch(r'[A-Za-z0-9_+.-]{0,25}', language) else ''
            section = ' — ' + clean(block['heading']) if block.get('heading') else ''
            lines.extend(['공식 문서의 명령·예시' + section + ':', ''])
            if block.get('context_translation', {}).get('text'):
                lines.extend([clean(block['context_translation']['text']), ''])
            lines.extend([fence + language, code, fence, ''])
            if block.get('source_url'):
                lines.extend(['[명령·예시 원문](' + block['source_url'] + ')', ''])
    if guide.get('assessment'):
        import comparisons
        lines.extend(comparisons.render(guide['assessment'], clean))
    lines.extend(['### 출처와 확인 범위', '',
                  '소개 방식: ' + clean(guide['method']) + ' · 문서 확인: ' + clean(guide['checked_at']), ''])
    for source in guide.get('sources', []):
        lines.append('- [' + clean(source['title']) + '](' + source['url'] + ')')
    lines.append('')
    return lines
