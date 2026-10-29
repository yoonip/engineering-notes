"""Parse official paper/course notices without requesting pages or evaluating research."""
from __future__ import annotations

import re
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup


def _text(node) -> str:
    return ' '.join(node.get_text(' ', strip=True).split()) if node else ''


def _allowed(source: dict, url: str) -> bool:
    parts = urlsplit(url)
    return parts.scheme == 'https' and parts.hostname in source['hosts'] and not parts.username and not parts.password


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
    for heading in soup.find_all('h3'):
        if '수업내용/목표' not in _text(heading):
            continue
        paragraphs = []
        for sibling in heading.next_siblings:
            if getattr(sibling, 'name', None) in ('h2', 'h3'):
                break
            if getattr(sibling, 'name', None) in ('p', 'div', 'ul', 'ol'):
                paragraphs.append(_text(sibling))
        description = ' '.join(paragraphs).strip()
        break
    return {'title': title, 'description': description, 'date': '', 'kind': '강좌 안내'}
