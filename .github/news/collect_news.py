"""공식 RSS/Atom의 제목과 원문 링크를 읽어 최신 뉴스 목록을 만듭니다.

Python 3.12 표준 라이브러리만 사용합니다. 기사 페이지나 본문은 요청하지 않습니다.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import html
from html.parser import HTMLParser
from http.client import HTTPException
import ipaddress
import json
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import xml.etree.ElementTree as ET

KST = timezone(timedelta(hours=9), name='KST')
MAX_BYTES = 2_000_000
TIMEOUT = 20
USER_AGENT = 'EngineeringNotesNews/1.0 (+https://github.com/yoonip/engineering-notes)'
GROUPS = {'world': '세계 뉴스', 'korea': '한국 뉴스'}
REASONS = {
    'ok': '정상', 'no_recent_items': '최근 24시간 기사 없음',
    'unchanged': '변경 없음',
    'http_error': 'HTTP 응답 오류', 'network_error': '연결 오류',
    'invalid_feed': '피드 형식 오류', 'unsafe_redirect': '허용되지 않은 이동 주소',
    'too_large': '피드 크기 초과',
}


class FeedError(Exception):
    """외부 응답 본문 대신 정해진 오류 코드만 기록합니다."""


def safe_url(value: str, hosts: list[str]) -> bool:
    """설정에 명시한 공개 HTTPS 호스트만 허용합니다."""
    try:
        parts = urlsplit(value)
        host = (parts.hostname or '').lower()
        if parts.scheme != 'https' or parts.username or parts.password or parts.port not in (None, 443):
            return False
        if not host or any(ord(c) < 33 for c in value) or '\\' in value:
            return False
        try:
            ipaddress.ip_address(host)
            return False
        except ValueError:
            pass
        return any(host == allowed or host.endswith('.' + allowed) for allowed in hosts)
    except (ValueError, TypeError):
        return False


class RestrictedRedirect(HTTPRedirectHandler):
    def __init__(self, hosts: list[str]):
        super().__init__()
        self.hosts = hosts

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not safe_url(newurl, self.hosts):
            raise FeedError('unsafe_redirect')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def load_config(path: Path) -> dict:
    config = json.loads(path.read_text(encoding='utf-8'))
    if config.get('schema_version') != 1 or config.get('lookback_hours') != 24:
        raise ValueError('지원하지 않는 설정 형식 또는 수집 기간입니다.')
    if not 1 <= config['items_per_source'] <= 12:
        raise ValueError('매체별 기사 수는 1~12건이어야 합니다.')
    sources = config['sources']
    if not sources or len(sources) > 30 or len({s['id'] for s in sources}) != len(sources):
        raise ValueError('매체 목록이 비어 있거나 ID가 중복됩니다.')
    for source in sources:
        if not re.fullmatch(r'[a-z0-9-]+', source['id']) or source['group'] not in GROUPS:
            raise ValueError('매체 ID 또는 분류가 올바르지 않습니다.')
        if not safe_url(source['feed_url'], source['feed_hosts']):
            raise ValueError('피드 URL이 허용된 HTTPS 주소가 아닙니다.')
        if not source['article_hosts'] or not source['policy_url'].startswith('https://'):
            raise ValueError('기사 호스트와 이용 조건 출처가 필요합니다.')
    return config


def date_value(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.strip()
    try:
        result = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        try:
            result = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except (TypeError, ValueError, OverflowError):
            return None
    # 채널 갱신일이나 수집 시각을 기사 발행 시각으로 대신 쓰지 않습니다.
    if result.tzinfo is None:
        return None
    try:
        return result.astimezone(timezone.utc)
    except (ValueError, OverflowError):
        return None


def local_name(tag: str) -> str:
    return tag.rsplit('}', 1)[-1]


def field(node: ET.Element, names: tuple[str, ...]) -> str | None:
    for name in names:
        for child in node:
            if local_name(child.tag) == name and child.text and child.text.strip():
                return child.text.strip()
    return None


def article_link(node: ET.Element) -> str:
    for child in node:
        if local_name(child.tag) == 'link':
            if child.get('href') and child.get('rel', 'alternate') == 'alternate':
                return child.get('href', '').strip()
            if child.text and not child.get('href'):
                return child.text.strip()
    return ''


def clean_title(value: str | None) -> str:
    if not value:
        return ''
    # XML 파서가 이미 엔티티를 처리합니다. 제목을 번역하거나 요약하지 않습니다.
    title = ' '.join(value.split())
    if len(title) > 500 or any(ord(c) < 32 for c in title):
        return ''
    return title


def url_key(value: str) -> str:
    """중복 판별에만 추적 매개변수를 뺍니다. 게시 링크는 원본 그대로입니다."""
    parts = urlsplit(value)
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
             if not k.lower().startswith(('utm_', 'fbclid', 'gclid'))]
    return urlunsplit((parts.scheme, parts.netloc.lower(), parts.path, urlencode(query), ''))


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.hidden = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        elif tag in ('p', 'br', 'div'):
            self.parts.append(' ')

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.hidden:
            self.hidden -= 1
        elif tag in ('p', 'div'):
            self.parts.append(' ')

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def plain_description(value: str) -> str:
    parser = PlainText()
    parser.feed(value[:20_000])
    return ' '.join(''.join(parser.parts).split())


def brief_description(value: str) -> str:
    text = plain_description(value)
    text = re.sub(r'^\([^)]*=연합뉴스\)\s*[^=]{0,100}=\s*', '', text)
    # 피드가 제공한 첫 완결 문장만 사용하며 잘린 문장을 사실 요약으로 꾸미지 않습니다.
    sentences = re.split(r'(?<=[.!?。])\s+(?=[A-Z가-힣“\"\'])', text)
    first = sentences[0].strip() if sentences else ''
    if len(first) < 12 or len(first) > 700 or re.search(r'(?i)read more|continue reading', first):
        return ''
    return first


def parse_feed(data: bytes, source: dict, now: datetime) -> tuple[list[dict], dict]:
    if len(data) > MAX_BYTES:
        raise FeedError('too_large')
    # UTF-16 등으로 선언을 숨기는 입력도 DTD 검사 뒤 파싱되도록 합니다.
    if b'\x00' in data or re.search(br'<!\s*(DOCTYPE|ENTITY)\b', data, re.I):
        raise FeedError('invalid_feed')
    try:
        root = ET.fromstring(data)
    except (ET.ParseError, LookupError, ValueError):
        raise FeedError('invalid_feed') from None
    if local_name(root.tag) not in ('rss', 'RDF', 'feed'):
        raise FeedError('invalid_feed')
    nodes = [node for node in root.iter() if local_name(node.tag) in ('item', 'entry')]
    stats = {'scanned': len(nodes), 'old': 0, 'future': 0, 'invalid': 0, 'duplicates': 0}
    items, seen = [], set()
    cutoff = now - timedelta(hours=24)
    for node in nodes[:1000]:
        title = clean_title(field(node, ('title',)))
        link = article_link(node)
        published = date_value(field(node, ('pubDate', 'published', 'date')))
        if not title or not safe_url(link, source['article_hosts']) or published is None:
            stats['invalid'] += 1
            continue
        if published > now:
            stats['future'] += 1
            continue
        if published < cutoff:
            stats['old'] += 1
            continue
        key = url_key(link)
        if key in seen:
            stats['duplicates'] += 1
            continue
        seen.add(key)
        # 원 피드의 항목 순서를 유지합니다. 별도의 중요도 점수를 만들지 않습니다.
        entry = {'title': title, 'url': link, 'published_at': published.isoformat()}
        credit = clean_title(field(node, ('creator', 'publisher', 'author')))
        if credit:
            entry['credit'] = credit
        if source.get('news_mode'):
            description = field(node, ('description', 'summary')) or ''
            if credit in source.get('excluded_creators', []):
                continue
            wire = source.get('exclude_credit_pattern')
            if wire and re.search(wire, credit + ' ' + plain_description(description), re.I):
                continue
            if source.get('summary_mode') != 'link_only':
                excerpt = brief_description(description)
                if excerpt:
                    entry['excerpt'] = excerpt
            entry['feed_rank'] = nodes.index(node)
        items.append(entry)
    return items, stats


def fetch_source(source: dict, now: datetime) -> dict:
    report = {'source': source, 'state': 'network_error', 'items': [], 'stats': {}}
    opener = build_opener(RestrictedRedirect(source['feed_hosts']))
    request = Request(source['feed_url'], headers={
        'User-Agent': USER_AGENT, 'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml',
        'Accept-Encoding': 'identity',
    })
    for header in ('ETag', 'Last-Modified'):
        value = source.get('conditional', {}).get(header)
        if isinstance(value, str) and len(value) <= 1000 and '\r' not in value and '\n' not in value:
            request.add_header('If-None-Match' if header == 'ETag' else 'If-Modified-Since', value)
    for attempt in range(2):
        try:
            with opener.open(request, timeout=TIMEOUT) as response:
                if not safe_url(response.url, source['feed_hosts']):
                    raise FeedError('unsafe_redirect')
                data = response.read(MAX_BYTES + 1)
                report['conditional'] = {h: response.headers[h] for h in ('ETag', 'Last-Modified')
                                         if response.headers.get(h)} if hasattr(response, 'headers') else {}
            report['items'], report['stats'] = parse_feed(data, source, now)
            report['state'] = 'ok' if report['items'] else 'no_recent_items'
            report.pop('http_status', None)
            break
        except FeedError as exc:
            report['state'] = str(exc)
            break
        except HTTPError as exc:
            if exc.code == 304:
                report.update(state='unchanged', conditional=source.get('conditional', {}))
                break
            report.update(state='http_error', http_status=exc.code)
            if exc.code not in (429, 500, 502, 503, 504):
                break
        except (URLError, TimeoutError, OSError, HTTPException):
            report['state'] = 'network_error'
        if attempt == 0:
            time.sleep(1)
    return report


def choose_items(reports: list[dict], limit: int) -> dict[str, list[dict]]:
    chosen, seen = {}, set()
    for report in reports:
        selected = []
        for item in report['items']:
            key = url_key(item['url'])
            if key in seen:
                continue
            seen.add(key)
            selected.append(item)
            if len(selected) == limit:
                break
        chosen[report['source']['id']] = selected
    return chosen


def publishable(reports: list[dict], selected: dict[str, list[dict]]) -> bool:
    counts = {group: 0 for group in GROUPS}
    for report in reports:
        if selected.get(report['source']['id']):
            counts[report['source']['group']] += 1
    return counts['world'] >= 2 and counts['korea'] >= 1


def md_text(value: str) -> str:
    # RSS 제목이 Markdown 링크·HTML·강조 문법으로 실행되지 않도록 이스케이프합니다.
    value = html.escape(value, quote=False)
    return re.sub(r'([\\`*_{}\[\]()#!|])', r'\\\1', value)


def md_url(value: str) -> str:
    # 꺾쇠 URL 문법에 영향을 주는 문자만 퍼센트 인코딩합니다.
    return value.replace('<', '%3C').replace('>', '%3E')


def render(reports: list[dict], selected: dict[str, list[dict]], now: datetime) -> str:
    fetched = now.astimezone(KST).strftime('%Y-%m-%d %H:%M')
    lines = ['# 오늘의 뉴스 | Daily news', '', f'수집 시각: {fetched} KST(한국 표준시)', '',
        '매체별 공식 피드에서 최근 24시간에 발행된 기사 중 앞에 실린 기사를 연결합니다. '
        '제목과 링크는 원문을 유지하며, 기사 발행 시각은 한국 표준시로 표시합니다.', '',
        '[뉴스 안내](README.md) · [매체와 수집 기준](매체와수집기준_sources.md)', '']
    for group, label in GROUPS.items():
        lines += ['## ' + label, '']
        for report in reports:
            source = report['source']
            if source['group'] != group:
                continue
            lines += [f"### [{md_text(source['name'])}]({source['homepage']})", '']
            entries = selected[source['id']]
            if not entries:
                reason = REASONS[report['state']] if report['state'] != 'ok' else '다른 피드와 같은 기사'
                lines += [f'이번 수집: {reason}', '']
                continue
            for item in entries:
                published = datetime.fromisoformat(item['published_at']).astimezone(KST).strftime('%m-%d %H:%M')
                credit = ' · 작성·제공: ' + md_text(item['credit']) if item.get('credit') else ''
                lines.append(f"- [{md_text(item['title'])}](<{md_url(item['url'])}>) · {published} KST{credit}")
            lines.append('')
    lines += ['## 수집 상태', '', '| 매체 | 상태 | 연결한 기사 |', '| --- | --- | ---: |']
    for report in reports:
        source = report['source']
        state = REASONS[report['state']]
        if report.get('http_status'):
            state += f" ({report['http_status']})"
        lines.append(f"| {md_text(source['name'])} | {state} | {len(selected[source['id']])} |")
    lines += ['', '기사 내용과 정정 사항은 각 매체의 원문에서 확인하실 수 있습니다. '
        '이 목록은 매체의 보도를 연결하며, 별도의 사실 확인이나 중요도 순위를 뜻하지 않습니다.', '']
    return '\n'.join(lines)


def run(config: dict, output: Path, now: datetime, fetcher=fetch_source) -> tuple[int, dict]:
    if now.tzinfo is None:
        raise ValueError('수집 시각에 시간대가 필요합니다.')
    now = now.astimezone(timezone.utc)
    with ThreadPoolExecutor(max_workers=4) as pool:
        reports = list(pool.map(lambda source: fetcher(source, now), config['sources']))
    selected = choose_items(reports, config['items_per_source'])
    allowed = publishable(reports, selected)
    summary = {'collected_at': now.isoformat(), 'published': allowed, 'sources': []}
    for report in reports:
        source_id = report['source']['id']
        summary['sources'].append({'id': source_id, 'state': report['state'],
            'selected': len(selected[source_id]), 'stats': report.get('stats', {}),
            'http_status': report.get('http_status')})
    # 전체/한쪽 지역의 장애 때 기존 정상 목록을 빈 뉴스로 덮어쓰지 않습니다.
    if allowed:
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_suffix(output.suffix + '.tmp')
        temporary.write_text(render(reports, selected, now), encoding='utf-8', newline='\n')
        temporary.replace(output)
    return (0 if allowed else 1), summary


def main() -> int:
    from news_pipeline import main as publish_main
    return publish_main()


if __name__ == '__main__':
    raise SystemExit(main())
