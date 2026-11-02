"""Parse official paper/course notices without requesting pages or evaluating research."""
from __future__ import annotations

import re
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup, Comment, NavigableString


def _text(node) -> str:
    return ' '.join(node.get_text(' ', strip=True).split()) if node else ''


def _allowed(source: dict, url: str) -> bool:
    parts = urlsplit(url)
    return parts.scheme == 'https' and parts.hostname in source['hosts'] and not parts.username and not parts.password


def _following_intro(heading) -> str:
    """Read visible text up to the next section, including boundaries inside a div."""
    pieces = []
    for sibling in heading.next_siblings:
        if not getattr(sibling, 'name', None):
            continue
        for node in (sibling, *sibling.descendants):
            if getattr(node, 'name', None) in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'article'):
                return ' '.join(''.join(pieces).split())
            if getattr(node, 'name', None) in ('p', 'div', 'li', 'br', 'ul', 'ol'):
                pieces.append(' ')
            if isinstance(node, NavigableString) and not isinstance(node, Comment):
                pieces.append(str(node))
    return ' '.join(''.join(pieces).split())


def prepare_item(source: dict, item: dict) -> dict:
    """Normalize arXiv identity; a cross-listing is not a second paper."""
    result = dict(item)
    if source.get('adapter') == 'arxiv':
        match = re.search(r'/abs/((?:\d{4}\.\d{4,5}|[a-z-]+/\d{7}))(?:v(\d+))?', result.get('url', ''), re.I)
        if not match:
            return result
        paper_id = match[1]
        description = result.get('description', '')
        version = re.search(r'arXiv:' + re.escape(paper_id) + r'v(\d+)', description)
        result['paper_id'] = paper_id
        result['version'] = version[1] if version else (match[2] or '')
        result['url'] = 'https://arxiv.org/abs/' + paper_id
        result['description'] = re.sub(r'^\s*arXiv:[\w./-]+\s+Announce\s+Type:\s*[^:]+?\s+Abstract:\s*', '', description, flags=re.I)
        result['kind'] = '프리프린트 초록'
        result['published_kind'] = 'arxiv_announcement'
    elif source.get('adapter') == 'mit_research':
        result['kind'] = '대학 연구 소개'
    elif source.get('adapter') in ('ocw_notices', 'mit_learning'):
        result['kind'] = '공개 학습 자료 안내'
    return result


def eligible(source: dict, item: dict) -> bool:
    """Apply documented subject filters without inventing significance or citation ranks."""
    if not _allowed(source, item.get('url', '')):
        return False
    title = item.get('title', '')
    if not title:
        return False
    patterns = source.get('title_patterns', [])
    if patterns and not any(re.search(pattern, title, re.I) for pattern in patterns):
        return False
    adapter = source.get('adapter')
    if adapter == 'arxiv':
        return bool(re.fullmatch(r'/abs/(?:\d{4}\.\d{4,5}|[a-z-]+/\d{7})(?:v\d+)?', urlsplit(item['url']).path, re.I))
    if adapter == 'mit_research':
        text = title + ' ' + item.get('description', '')[:1000]
        if re.search(r'\b(?:award|prize|appointed|elected|commencement|obituary|memoriam)\b', title, re.I):
            return False
        return bool(re.search(r'\b(?:research|researchers?|paper|study|scientists?|experiment|findings|journal|Nature|Science)\b', text, re.I))
    if adapter in ('ocw_notices', 'mit_learning'):
        if re.search(r'\b(?:award|anniversary|donation|fundraising|newsletter)\b', title, re.I):
            return False
        if re.search(r'\b(?:book|textbook|curriculum|tutorial|lecture|seminar)\b', title, re.I):
            return True
        if re.search(r'\b(?:inspired|confidence|journey|doors|learner)\b', title, re.I):
            return False
        return bool(re.search(r'\b(?:courses?|resources?|learning materials?)\b', title, re.I))
    return adapter == 'kmooc'


def discover(source: dict, text: str) -> list[dict]:
    """Read K-MOOC's server-rendered homepage cards; no hidden API is used."""
    if source.get('adapter') != 'kmooc':
        raise ValueError('Unknown HTML scholar adapter: ' + str(source.get('adapter')))
    soup = BeautifulSoup(text, 'html.parser')
    result = {}
    for card in soup.select('li.card_item'):
        anchor = card.select_one('a[href]')
        if not anchor:
            continue
        path = anchor.get('href', '')
        if not re.fullmatch(r'/view/course/detail/\d+', path):
            continue
        url = urljoin(source['url'], path)
        title = _text(card.select_one('strong.title'))
        if not title or not _allowed(source, url):
            continue
        # 운영기간은 게시일이 아닙니다. 발행일을 만들어 넣지 않습니다.
        period = _text(card.select_one('.date'))
        result[url] = {'title': title, 'url': url, 'date': '', 'description': '',
                       'kind': '강좌 안내', 'course_period': period,
                       'institution': _text(card.select_one('.institution'))}
    return list(result.values())


def detail(source: dict, text: str, url: str) -> dict:
    """Extract the course author's introduction; periods remain separate metadata."""
    if source.get('adapter') != 'kmooc':
        return {}
    if not _allowed(source, url):
        raise ValueError('Unexpected course host')
    soup = BeautifulSoup(text, 'html.parser')
    for node in soup.select('script,style,noscript,template'):
        node.decompose()
    title = _text(soup.find('title')).split('| K-MOOC', 1)[0].strip()
    description = ''
    # 현재 강좌의 .introduce/h6와 이전 h3 양식을 모두 읽습니다.
    # 일정·평가기준·추천 강좌까지 소개문에 섞지 않습니다.
    headings = soup.select('.introduce h6') + soup.find_all('h3')
    for heading in headings:
        if _text(heading) not in ('수업내용/목표', '강좌소개', 'Course Introduction'):
            continue
        description = _following_intro(heading)
        if description:
            break
    intro = soup.select_one('.introduce')
    if not description and intro:
        for row in intro.select('tr'):
            cells = row.find_all(['th', 'td'], recursive=False)
            if len(cells) >= 2 and _text(cells[0]) in ('학습목표', 'Learning Objectives'):
                description = ' '.join(_text(cell) for cell in cells[1:])
                break
    if not description and intro:
        # 제목 대신 이미지로 구획을 표시하는 강좌의 첫 설명 문단입니다.
        # 뒤의 주차표·평가기준으로 넘어가지 않습니다.
        for node in intro.children:
            if getattr(node, 'name', None) in ('table', 'article', 'h3', 'h4', 'h5', 'h6'):
                break
            if getattr(node, 'name', None) == 'p' and len(_text(node)) >= 60:
                description = _text(node)
                break
    return {'title': title, 'description': description, 'date': '', 'kind': '강좌 안내'}
