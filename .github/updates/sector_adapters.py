"""Parse official technology briefs and industrial publications without fetching URLs."""
from __future__ import annotations

from datetime import date as calendar_date
import re
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit

from bs4 import BeautifulSoup


def _soup(text: str) -> BeautifulSoup:
    soup = BeautifulSoup(text, 'html.parser')
    for node in list(soup.select('script,style,nav,header,footer,template,[hidden],[aria-hidden="true"]')):
        if node.name:
            node.decompose()
    for node in list(soup.select('[style]')):
        if node.attrs and re.search(r'display\s*:\s*none|visibility\s*:\s*hidden', node.get('style', ''), re.I):
            node.decompose()
    return soup


def _text(node) -> str:
    return ' '.join(node.get_text(' ', strip=True).split()) if node else ''


def _date(value: str) -> str:
    match = re.search(r'(20\d{2})\s*[년./-]\s*(\d{1,2})(?:\s*[월./-]\s*(\d{1,2}))?', value)
    if not match:
        return ''
    year, month = int(match[1]), int(match[2])
    day = int(match[3]) if match[3] else None
    try:
        calendar_date(year, month, day or 1)
    except ValueError:
        return ''
    return f'{year:04d}-{month:02d}' + (f'-{day:02d}' if day else '')


def _url(source: dict, value: str, base: str | None = None) -> str:
    result = urljoin(base or source['url'], value)
    parts = urlsplit(result)
    if parts.scheme != 'https' or parts.hostname not in source['hosts'] or parts.username or parts.password:
        return ''
    return result


def _series(source: dict, title: str) -> str:
    label = source.get('series', '')
    return label + ' · ' + title if label and label not in title else title


def discover(source: dict, text: str) -> list[dict]:
    """Read source dates and stable publisher IDs from already downloaded HTML."""
    soup = _soup(text)
    items = []
    adapter = source['adapter']
    if adapter == 'sector_spri':
        for link in soup.select('a[href*="/posts/view/"]'):
            match = re.search(r'/posts/view/(\d+)', link.get('href', ''))
            card = link.find_parent('li')
            if not match or card is None:
                continue
            title_node = card.select_one('.text_box .data')
            title = _text(title_node) or (card.select_one('img[alt]').get('alt') if card.select_one('img[alt]') else '')
            if not title:
                continue
            query = parse_qs(urlsplit(source['url']).query)
            code = query.get('code', [''])[0]
            url = _url(source, '/posts/view/' + match[1] + ('?' + urlencode({'code': code}) if code else ''))
            items.append({'url': url, 'title': _series(source, title), 'date': _date(title), 'description': ''})
    elif adapter == 'sector_kistep':
        for link in soup.select('strong.title a[href]'):
            parts = urlsplit(link.get('href', ''))
            query = parse_qs(parts.query)
            identity = query.get('list_no', [''])[0]
            board = query.get('bid', [''])[0]
            card = link.find_parent('li')
            if not identity.isdigit() or board != '0031' or card is None:
                continue
            url = _url(source, '/board.es?' + urlencode({'mid': 'a10306040000', 'bid': board, 'list_no': identity, 'act': 'view'}))
            date = ''
            for row in card.select('.basic_info li'):
                if _text(row.select_one('.label')) == '등록일':
                    date = _date(_text(row.select_one('.txt')))
            pdf = card.select_one('a[href*="/boardDownload.es?"]')
            items.append({'url': url, 'title': _text(link), 'date': date, 'description': '',
                          'pdf_url': _url(source, pdf['href']) if pdf else ''})
    elif adapter == 'sector_kari':
        for card in soup.select('.bod-program-list ul.pdf > li'):
            title = _text(card.select_one('.desc > strong'))
            download = card.select_one('.desc a.down[href]')
            if not title or not download:
                continue
            url = _url(source, download['href'])
            if not re.fullmatch(r'/attach/[a-f0-9]+/[a-f0-9]+', urlsplit(url).path):
                continue
            date = ''
            for row in card.select('.desc > ul > li'):
                if _text(row.select_one('em')) == '작성일':
                    date = _date(_text(row))
            contents = _text(card.select_one('.desc.ty2'))
            # These are printed contents, not the site's generated summary modal.
            items.append({'url': url, 'title': title, 'date': date,
                          'description': ('목차: ' + contents)[:600] if contents else '',
                          'source_page': source['url'], 'kind': '기관 발간물 첨부파일'})
    else:
        raise ValueError('Unknown sector adapter: ' + str(adapter))
    seen, result = set(), []
    for item in items:
        if item['url'] and item['url'] not in seen:
            seen.add(item['url'])
            result.append(item)
    return result


def detail(source: dict, text: str, url: str) -> dict:
    """Read the publisher's visible introduction, not generated site summaries."""
    soup = _soup(text)
    adapter = source['adapter']
    if adapter == 'sector_spri':
        top = soup.select_one('.view_top_box')
        title = _text(top.select_one('h3.title')) if top else ''
        date = _date(_text(top.select_one('.data.sty2'))) if top else ''
        topics = [_text(node) for node in soup.select('.txt_box .info_list.sty3, .txt_box .txt_list .info_list')]
        description = '목차: ' + ' '.join(topics) if topics else ''
        download = soup.select_one('.view_top_box button[onclick*="file_down"]')
        match = re.search(r"file_down\(['\"](\d+)['\"]\)", download.get('onclick', '')) if download else None
        return {'title': _series(source, title) if title else '', 'date': date,
                'description': description[:600],
                'pdf_url': _url(source, '/download/' + match[1]) if match else ''}
    if adapter == 'sector_kistep':
        article = soup.select_one('article.board_view')
        if article is None:
            return {}
        pdf = article.select_one('a[href*="/boardDownload.es?"]')
        return {'title': _text(article.select_one('.publication_info h2.title')),
                'date': _date(_text(article.select_one('.publication_info li.date span'))),
                'description': _text(article.select_one('.contents'))[:600],
                'pdf_url': _url(source, pdf['href'], url) if pdf else ''}
    if adapter == 'sector_kari':
        return {}  # The official card already contains the available metadata.
    raise ValueError('Unknown sector adapter: ' + str(adapter))
