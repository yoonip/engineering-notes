"""공식 문서의 장단점·대안·선택 조건을 근거와 함께 표시합니다."""
from __future__ import annotations

import re
from urllib.error import HTTPError
from urllib.parse import urlsplit

import guides

PATTERNS = {
    'advantages': r'\badvantages?\b|strengths?|benefits?|why\s+(?:use|choose)|장점|강점|优点',
    'limitations': r'\bdisadvantages?\b|limitations?|drawbacks?|caveats?|trade.?offs?|known.issues?|non.goals?|제약|한계|단점|注意',
    'comparison': r'comparisons?|alternatives?|versus|\bvs\.?\b|why.not|비교|대안|对比',
    'selection': r'when.to.use|when.not.to.use|which.*choose|who.*for|use.cases?|선택|활용|적합',
}


def select(parsed: list[dict], kind: str) -> list[dict]:
    found, scopes, source = [], [], None
    opposite = {'advantages': 'limitations', 'limitations': 'advantages'}.get(kind)
    for section in parsed:
        if section.get('source_url') != source:
            scopes.clear()
            source = section.get('source_url')
        while scopes and section['level'] <= scopes[-1][0]:
            scopes.pop()
        matches = bool(re.search(PATTERNS[kind], section['heading'], re.I))
        conflicts = bool(opposite and re.search(PATTERNS[opposite], section['heading'], re.I))
        if matches or conflicts:
            # 혼합 제목과 반대 범주의 하위 절은 장점·제약을 확정하는 근거에서 제외합니다.
            scopes.append((section['level'], matches and not conflicts, section['heading']))
        if scopes and scopes[-1][1]:
            found.append(dict(section, scope_heading=scopes[-1][2]))
    return found


def evidence(parsed: list[dict], kind: str, translations) -> list[dict]:
    result, budget = [], 60
    for section in select(parsed, kind):
        for paragraph in section['paragraphs']:
            words = len(paragraph.split())
            if 3 <= words <= min(budget, 45) and len(paragraph) < 700:
                translated = guides.korean_text(paragraph, translations)
                result.append({'text': translated['text'], 'original': paragraph,
                               'method': translated['method'], 'source_url': section['source_url'],
                               'section': section['heading']})
                budget -= words
                if len(result) >= 2 or budget < 3:
                    return result
    return result


def documented_conditions(parsed: list[dict], translations) -> list[dict]:
    result = []
    candidates = guides.select_sections(parsed, 'installation') + select(parsed, 'limitations')
    seen = set()
    for section in candidates:
        for text in section['paragraphs']:
            if text in seen or re.search(r'requires? no|does not require|no .{0,15}required', text, re.I):
                continue
            if 3 <= len(text.split()) <= 45 and re.search(r'\brequires?\b|\bonly\b|does not|not supported|\bmust\b|cannot|\bneeds?\b|\bminimum\b|not included|\blimited\b|필요|지원하지|제한', text, re.I):
                seen.add(text)
                translated = guides.korean_text(text, translations)
                result.append({'text': translated['text'], 'original': text, 'method': translated['method'],
                               'section': section['heading'], 'source_url': section['source_url']})
                if len(result) == 2:
                    return result
    return result


def competitor_names(parsed: list[dict], own_name: str) -> list[str]:
    names, seen = [], {own_name.casefold()}
    for section in select(parsed, 'comparison'):
        if re.search(r'reproduc|dependencies|prerequisites?|requirements?|installation|setup', section['heading'], re.I):
            continue
        for link in section.get('links', []):
            context = link.get('context', '')
            # 대안 목록의 하위 연동·의존성 절에는 부모 제목의 분류를 상속하지 않습니다.
            explicit = bool(re.search(r'alternatives?|대안', section['heading'], re.I))
            explicit = explicit or bool(re.search(r'compar(?:e|ed|ison).*with|versus|\bvs\b|differs? from|instead of|replace|대안|비교', context, re.I))
            if link.get('kind') == 'table':
                explicit = any(link['label'] in ' '.join(table['header']) or
                    (re.search(r'tool|project|framework|alternative|도구|프로젝트', table['header'][0], re.I)
                     and any(link['label'] in row[0] for row in table['rows'])) for table in section.get('tables', []))
            if not explicit or re.search(r'\binstall\b|\bdependenc|\brequires?\b', context, re.I):
                continue
            url = urlsplit(link['url'])
            if url.scheme != 'https' or url.hostname != 'github.com' or url.query:
                continue
            match = re.fullmatch(r'/([A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+)/?', url.path)
            if match and match[1].casefold() not in seen:
                seen.add(match[1].casefold())
                names.append(match[1])
                if len(names) == 2:
                    return names
    return names


def comparison_table(parsed: list[dict], translations) -> dict | None:
    for section in select(parsed, 'comparison'):
        for table in section.get('tables', []):
            header, rows = table['header'], table['rows'][:3]
            if len(header) > 5 or sum(len(cell.split()) for row in [header] + rows for cell in row) > 80:
                continue
            translated = [[guides.korean_text(guides.plain(cell), translations)['text'] or guides.plain(cell)
                           for cell in row] for row in [header] + rows]
            return {'header': translated[0], 'rows': translated[1:], 'original': [header] + rows,
                    'source_url': section['source_url'], 'section': section['heading']}
    return None


def parsed_documents(readme: dict) -> list[dict]:
    parsed = []
    for document in [readme] + readme.get('documents', []):
        for section in guides.sections(document['text']):
            section['source_url'] = document['source_url']
            parsed.append(section)
    return parsed


def brief(parsed: list[dict], kind: str, translations) -> list[dict]:
    items = guides.excerpts(parsed, kind)
    for item in items:
        item.update(guides.korean_text(item['original'], translations))
    return items


def build(repo: dict, readme: dict, reviewed: dict, translations, getter, repository_loader, token: str) -> dict:
    manual = reviewed.get(repo['full_name'].casefold(), {})
    if manual.get('repository_id') == repo['id'] and manual.get('readme_sha') == readme.get('sha'):
        return dict(manual, method='공식 문서의 기능·조건에 근거한 비교', origin='reviewed', source_url=readme['source_url'])
    parsed = parsed_documents(readme)
    result = {'method': '제작자 문서의 해당 구간 발췌·CPU 번역', 'origin': 'extracted',
              'checked_at': readme['fetched_at'][:10], 'source_url': readme['source_url'],
              'repository_id': repo['id'], 'readme_sha': readme['sha'],
              'advantages': evidence(parsed, 'advantages', translations),
              'limitations': evidence(parsed, 'limitations', translations),
              'comparison': evidence(parsed, 'comparison', translations),
              'selection': evidence(parsed, 'selection', translations),
              'table': comparison_table(parsed, translations), 'official_competitors': []}
    if not result['advantages']:
        result['advantages'] = [dict(item, section=item['heading']) for item in brief(parsed, 'features', translations)]
        result['advantages_basis'] = '공식 문서에 명시된 지원 기능입니다.'
    if not result['limitations']:
        result['limitations'] = documented_conditions(parsed, translations)
    seen_ids = {repo['id']}
    for slug in competitor_names(parsed, repo['full_name']):
        try:
            other = repository_loader(slug, token)
            other_readme = guides.fetch_readme(other, token, getter)
        except HTTPError as exc:
            if exc.code == 404:
                continue
            raise
        if other['id'] in seen_ids or other_readme['status'] != 'ok':
            continue
        seen_ids.add(other['id'])
        other_parsed = parsed_documents(other_readme)
        result['official_competitors'].append({
            'name': other['full_name'], 'url': other['html_url'], 'id': other['id'],
            'readme_url': other_readme['source_url'], 'readme_sha': other_readme['sha'],
            'commit': other_readme['commit'], 'language': other.get('language'),
            'license': (other.get('license') or {}).get('spdx_id'),
            'features': brief(other_parsed, 'features', translations),
            'requirements': brief(other_parsed, 'installation', translations)})
    # 대응 항목은 양쪽 문서의 실제 기능·설치 조건입니다. 성능 우열 점수를 만들지 않습니다.
    if result['official_competitors']:
        result['own_features'] = brief(parsed, 'features', translations)
        result['own_requirements'] = brief(parsed, 'installation', translations)
    return result


def source_links(urls: list[str]) -> str:
    return ' · '.join('[근거 ' + str(index) + '](' + url + ')' for index, url in enumerate(dict.fromkeys(urls), 1))


def render(assessment: dict, clean) -> list[str]:
    lines = []
    for key, title, manual_key in [('advantages', '장점', 'advantages_ko'),
                                   ('limitations', '제약과 확인할 점', 'limitations_ko')]:
        lines.extend(['### ' + title, ''])
        if assessment.get(manual_key):
            for item in assessment[manual_key]:
                lines.extend(['- ' + clean(item['text']) + ' ' + source_links(item['source_urls'])])
            lines.append('')
        elif assessment.get(key):
            lines.extend([assessment.get('advantages_basis', '제작자 문서의 설명입니다.') if key == 'advantages' else '제작자 문서의 설명입니다.', ''])
            for item in assessment[key]:
                text = item.get('text') or item['original']
                lines.extend([clean(text) + ' ' + source_links([item['source_url']]), '',
                              '원문 (' + clean(item['section']) + '): ' + clean(item['original']), ''])
        else:
            lines.extend(['공식 문서에서 이 항목을 뒷받침할 별도 설명을 찾지 못했습니다. '
                          + source_links([assessment['source_url']]), ''])
    lines.extend(['### 비슷한 도구와의 차이', ''])
    if assessment.get('alternatives'):
        lines.extend(['| 비교 도구 | 차이 | 공식 근거 |', '| --- | --- | --- |'])
        for alternative in assessment['alternatives']:
            lines.append('| [' + clean(alternative['name']) + '](' + alternative['url'] + ') | '
                         + clean(alternative['difference_ko']) + ' | ' + source_links(alternative['source_urls']) + ' |')
        lines.append('')
    else:
        if assessment.get('comparison') or assessment.get('table'):
            lines.extend(['아래 비교는 제작자가 공개한 설명이며 독립 성능시험 결과와는 구분합니다.', ''])
        for item in assessment.get('comparison', []):
            lines.extend([clean(item.get('text') or item['original']) + ' ' + source_links([item['source_url']]), '',
                          '원문 (' + clean(item['section']) + '): ' + clean(item['original']), ''])
        table = assessment.get('table')
        if table:
            lines.append('| ' + ' | '.join(clean(cell) for cell in table['header']) + ' |')
            lines.append('| ' + ' | '.join('---' for _ in table['header']) + ' |')
            lines.extend('| ' + ' | '.join(clean(cell) for cell in row) + ' |' for row in table['rows'])
            lines.extend(['', source_links([table['source_url']]), ''])
        if assessment.get('official_competitors'):
            lines.extend(['대응하는 공식 문서의 기능과 실행 조건:', '',
                          '| 프로젝트 | 문서상 기능 | 실행 조건 |', '| --- | --- | --- |'])
            for name, features, requirements, url in [( '현재 프로젝트', assessment['own_features'], assessment['own_requirements'], assessment['source_url'])] + [
                    (other['name'], other['features'], other['requirements'], other['readme_url'])
                    for other in assessment['official_competitors']]:
                feature_text = ' '.join(item.get('text') or item['original'] for item in features)
                condition_text = ' '.join(item.get('text') or item['original'] for item in requirements)
                lines.append('| [' + clean(name) + '](' + url + ') | ' + clean(feature_text or '별도 구간 없음')
                             + ' | ' + clean(condition_text or '별도 구간 없음') + ' |')
            lines.append('')
        if not any(assessment.get(key) for key in ('comparison', 'table', 'official_competitors')):
            lines.extend(['공식 문서에 구체적인 비교 근거가 없어 임의의 경쟁 도구나 우열을 붙이지 않았습니다. '
                          + source_links([assessment['source_url']]), ''])
    lines.extend(['### 선택하기 좋은 상황', ''])
    if assessment.get('choose_ko'):
        for item in assessment['choose_ko']:
            lines.append('- ' + clean(item['text']) + ' ' + source_links(item['source_urls']))
        lines.append('')
    elif assessment.get('selection'):
        lines.extend(['제작자가 설명한 사용 대상·선택 조건:', ''])
        for item in assessment['selection']:
            lines.extend([clean(item.get('text') or item['original']) + ' ' + source_links([item['source_url']]), '',
                          '원문 (' + clean(item['section']) + '): ' + clean(item['original']), ''])
    else:
        lines.extend(['제작자가 별도의 선택 조건을 제시하지 않았습니다. 앞의 기능·설치 환경·제약을 필요한 작업과 대조해 판단하실 수 있습니다. '
                      + source_links([assessment['source_url']]), ''])
    lines.extend(['비교 기준: ' + clean(assessment['method']) + ' · 문서 확인: ' + clean(assessment['checked_at']), ''])
    return lines
