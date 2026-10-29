"""Parse official tool releases and vendor introductions without network calls."""
from __future__ import annotations

from datetime import datetime
import json
import re
from urllib.parse import urlsplit

from bs4 import BeautifulSoup


PREVIEW = re.compile(r'\b(?:alpha|beta|candidate|nightly|preview|snapshot)\b|(?:[-_.]|\d)rc\d|\d+\.\d+(?:\.\d+)?(?:a|b|rc)\d+', re.I)
PYTHON_VERSION = re.compile(r'^Python\s+\d+\.\d+', re.I)


def _text(value: str) -> str:
    soup = BeautifulSoup(value[:40_000], 'html.parser')
    for node in soup.select('script,style,noscript,template'):
        node.decompose()
    return ' '.join(soup.get_text(' ', strip=True).split())


def _allowed(source: dict, url: str) -> bool:
    try:
        parsed = urlsplit(url)
        return (parsed.scheme == 'https' and parsed.hostname in source['hosts']
                and not parsed.username and not parsed.password and parsed.port in (None, 443))
    except (ValueError, TypeError):
        return False


def _published(value: str) -> str:
    """Use a real publication timestamp, never repository creation/update time."""
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, TypeError, AttributeError):
        return ''
    return parsed.isoformat() if parsed.tzinfo is not None else ''


def _release_intro(body: str) -> str:
    """Retain a short publisher paragraph, excluding images and full changelogs."""
    body = re.sub(r'<!--.*?-->', '', body or '', flags=re.S)
    body = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', body)
    body = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', body)
    paragraphs = re.split(r'\n\s*\n', body)
    for paragraph in paragraphs:
        stripped = paragraph.strip()
        if not stripped or stripped.startswith(('#', '* ', '- ', '|', '```', '>')):
            continue
        cleaned = _text(stripped)
        if len(cleaned) >= 20:
            return cleaned[:600]
    return ''


def eligible(source: dict, item: dict) -> bool:
    """Limit the Python source to stable releases and omit event-only vendor posts."""
    if not _allowed(source, item.get('url', '')):
        return False
    title = item.get('title', '')
    if not title:
        return False
    if source.get('adapter') == 'python_releases':
        categories = [str(value).casefold() for value in item.get('categories', [])]
        return (bool(PYTHON_VERSION.search(title))
                and ('releases' in categories or bool(re.search(r'are out|is (?:now )?available|is here|released', title, re.I)))
                and not PREVIEW.search(title))
    if source.get('adapter') == 'github_releases':
        return not PREVIEW.search(title)
    if source['group'] == 'products':
        return not re.search(r'\b(?:register now|join us at|webinar|career fair|hiring)\b|채용|등록하세요', title, re.I)
    return True


def discover(source: dict, text: str) -> list[dict]:
    """Read the official repository's public Releases API response."""
    if source.get('adapter') != 'github_releases':
        raise ValueError('Unknown vendor list adapter: ' + str(source.get('adapter')))
    records = json.loads(text)
    if not isinstance(records, list):
        raise ValueError('GitHub releases response is not an array')
    repository = source['repository']
    expected_path = '/' + repository + '/releases/tag/'
    items, seen = [], set()
    for record in records:
        if not isinstance(record, dict) or record.get('draft') or record.get('prerelease'):
            continue
        url = record.get('html_url', '')
        parsed = urlsplit(url)
        title = _text(record.get('name') or record.get('tag_name') or '')
        tag = record.get('tag_name', '')
        date = _published(record.get('published_at', ''))
        if (not _allowed(source, url) or parsed.hostname != 'github.com'
                or not parsed.path.startswith(expected_path) or PREVIEW.search(tag)
                or not title or not date or url in seen):
            continue
        item = {'url': url, 'title': title, 'date': date,
                'description': _release_intro(record.get('body') or ''),
                'source_item_id': str(record.get('id', '')), 'kind': '공식 안정판 릴리스',
                'published_kind': 'official_release'}
        if eligible(source, item):
            items.append(item)
            seen.add(url)
    return items


def detail(source: dict, text: str, url: str) -> dict:
    """Read KISA's notice overview; RSS and API sources need no full article copy."""
    if source.get('adapter') != 'kisa_notice':
        return {}
    soup = BeautifulSoup(text, 'html.parser')
    board = soup.select_one('section#View .board')
    if board is None:
        raise ValueError('KISA notice body is missing')
    title_node, date_node = board.select_one('.b_title h2'), board.select_one('.b_title span')
    title = title_node.get_text(' ', strip=True) if title_node else ''
    date_match = re.search(r'\b\d{4}-\d{2}-\d{2}\b', date_node.get_text() if date_node else '')
    description = ''
    content = board.select_one('.content_html')
    if content:
        for node in content.select('script,style,noscript,template'):
            node.decompose()
        for paragraph in content.find_all('p'):
            value = ' '.join(paragraph.get_text(' ', strip=True).split())
            if re.match(r'^[□■]\s*개요', value):
                description = re.sub(r'^[□■]\s*개요\s*(?:o\s*)?', '', value)[:600]
                break
    return {key: value for key, value in {'title': title, 'date': date_match[0] if date_match else '',
            'description': description}.items() if value}
