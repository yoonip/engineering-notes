"""공식 모델 발표와 기관 보고서의 새 소개를 날짜별로 게시합니다.

공식 한국어 소개를 발췌하거나 공개된 주제를 한국어로 안내합니다.
LLM·번역 API를 호출하지 않으며 기존 분석 본문은 수정하지 않습니다.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import hashlib
import html
from http.client import HTTPException
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, build_opener
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'news'))
from collect_news import FeedError, RestrictedRedirect, safe_url, md_text, md_url
import model_adapters
import report_adapters

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
KST = timezone(timedelta(hours=9))
AGENT = 'EngineeringNotesUpdates/1.0 (+https://github.com/yoonip/engineering-notes)'
MAX_BYTES = 3_000_000
GROUPS = {
    'models': ('AI모델동향_ai-model-updates', '모델 발표'),
    'reports': ('미래경제보고서_future-economic-reports', '보고서 소식'),
}
TOPICS = [
    (r'reasoning|inference|추론|推理', '추론'),
    (r'coding|code generation|software engineering|코딩|코드|编程', '코딩'),
    (r'agent|tool use|tool calling|에이전트|도구 사용|智能体', '에이전트·도구 사용'),
    (r'computer use|browser|컴퓨터 사용|브라우저', '컴퓨터·브라우저 사용'),
    (r'world model|world simulation|월드 모델|세계 모형|시뮬레이션', '세계 모형·시뮬레이션'),
    (r'context|long.horizon|long.running|문맥|컨텍스트|장기 작업|上下文', '긴 문맥·장기 작업'),
    (r'multimodal|vision|image|video|다중모달|멀티모달|이미지|영상|多模态', '이미지·영상 처리'),
    (r'audio|speech|음성|语音', '음성 처리'),
    (r'cyber|security|보안|安全', '보안'),
    (r'benchmark|evaluation|벤치마크|평가|评估', '평가'),
    (r'pricing|cost|efficien|latency|가격|비용|효율|지연', '비용·실행 효율'),
    (r'econom|growth|inflation|경제|성장률|물가', '경제·경기'),
    (r'energy|electric|climate|에너지|전력|탄소', '에너지·전력'),
    (r'semiconductor|chip|반도체', '반도체'),
    (r'robot|mobility|로봇|모빌리티', '로봇·모빌리티'),
]


def clean(value: str) -> str:
    soup = BeautifulSoup(str(value)[:40_000], 'html.parser')
    for node in soup.select('script,style,noscript,template'):
        node.decompose()
    return ' '.join(soup.get_text(' ', strip=True).split())


def canonical(url: str, keep_fragment: bool = False) -> str:
    parts = urlsplit(html.unescape(url))
    path = re.sub(r';jsessionid=[^/?;]+', '', parts.path, flags=re.I).rstrip('/') or '/'
    # 실제 같은 발표의 언어 경로만 통합합니다. pub_no·idx 같은 발행물 ID는 보존합니다.
    if parts.hostname in ('openai.com', 'www.openai.com'):
        path = re.sub(r'^/ko-KR(?=/)', '', path)
    query = sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                   if not k.lower().startswith(('utm_', 'fbclid', 'gclid')))
    return urlunsplit(('https', parts.netloc.lower(), path, urlencode(query), parts.fragment if keep_fragment else ''))


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def publication_key(group: str, url: str, keep_fragment: bool = False) -> str:
    parts = urlsplit(canonical(url, keep_fragment))
    if group == 'models' and parts.hostname in ('blog.google', 'deepmind.google'):
        slug = parts.path.rsplit('/', 1)[-1]
        # 공식 한국어 경로의 -kr만 뺀 동일한 전체 slug를 묶습니다. 모델명 유사도로 합치지 않습니다.
        if parts.path.startswith('/intl/ko-kr/') and slug.endswith('-kr'):
            slug = slug[:-3]
        return group + ':google-announcement:' + slug
    return group + ':' + canonical(url, keep_fragment)


def fingerprint(item: dict) -> str:
    # 등록일·조회수·수집일·모델 다운로드 수·revision만의 변화는 새 내용이 아닙니다.
    return digest([re.sub(r'\s+', ' ', item.get(k, '')).strip() for k in ('title', 'description', 'pdf_url')])


def date_time(value: str) -> datetime | None:
    value = value.strip()
    if not value or re.fullmatch(r'\d{4}-\d{2}', value):
        return None
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        try:
            result = parsedate_to_datetime(value)
        except (ValueError, TypeError, OverflowError):
            return None
    if result.tzinfo is None:
        result = result.replace(tzinfo=KST)
    return result.astimezone(timezone.utc)


def parse_feed(text: str) -> list[dict]:
    if '\0' in text or re.search(r'<!\s*(?:DOCTYPE|ENTITY)\b', text, re.I):
        raise ValueError('invalid_feed')
    root = ET.fromstring(text)
    local = lambda tag: tag.rsplit('}', 1)[-1]
    if local(root.tag) not in ('rss', 'RDF', 'feed'):
        raise ValueError('invalid_feed')
    result = []
    for node in root.iter():
        if local(node.tag) not in ('item', 'entry'):
            continue
        fields = {local(child.tag): child for child in node}
        value = lambda name: ''.join(fields[name].itertext()).strip() if name in fields else ''
        link = value('link')
        if 'link' in fields and fields['link'].get('href'):
            link = fields['link'].get('href')
        raw_date = value('pubDate') or value('published') or value('date')
        parsed_date = date_time(raw_date)
        display_date = raw_date if re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?', raw_date) else (parsed_date.isoformat() if parsed_date else '')
        result.append({'title': clean(value('title')), 'url': link,
                       'description': clean(value('description') or value('summary'))[:3000],
                       'date': display_date,
                       'categories': [''.join(child.itertext()).strip() for child in node if local(child.tag) == 'category']})
    return result[:1500]


def generic_detail(text: str, url: str) -> dict:
    soup = BeautifulSoup(text, 'html.parser')
    meta = {node.get('property') or node.get('name'): node.get('content', '')
            for node in soup.select('meta[content]')}
    result = {'title': clean(meta.get('og:title', '')),
              'description': clean(meta.get('og:description') or meta.get('description', '')),
              'date': meta.get('article:published_time', '')}
    canonical_node = soup.select_one('link[rel="canonical"]')
    if canonical_node:
        result['canonical_url'] = urljoin(url, canonical_node.get('href', ''))
    for node in soup.select('script[type="application/ld+json"]'):
        try:
            data = json.loads(node.string or node.get_text())
        except (ValueError, TypeError):
            continue
        stack = data if isinstance(data, list) else [data]
        for obj in stack:
            if not isinstance(obj, dict):
                continue
            stack.extend(obj.get('@graph', []))
            kind = obj.get('@type', '')
            if not any(k in str(kind) for k in ('Article', 'Report')):
                continue
            for name, field in (('title', 'headline'), ('description', 'description'), ('date', 'datePublished')):
                if not result.get(name) and isinstance(obj.get(field), str):
                    result[name] = clean(obj[field])
    return {k: v for k, v in result.items() if v}


class FetchFailure(Exception):
    pass


class Client:
    def __init__(self, request_state: dict):
        self.state = request_state

    def fetch(self, url: str, hosts: list[str]) -> tuple[str | None, str]:
        if not safe_url(url, hosts):
            raise FetchFailure('unsafe_url')
        key = canonical(url)
        previous = self.state.get(key, {})
        headers = {'User-Agent': AGENT, 'Accept-Encoding': 'identity'}
        for header, request_header in (('ETag', 'If-None-Match'), ('Last-Modified', 'If-Modified-Since')):
            if previous.get(header):
                headers[request_header] = previous[header]
        try:
            opener = build_opener(RestrictedRedirect(hosts))
            with opener.open(Request(url, headers=headers), timeout=22) as response:
                if not safe_url(response.url, hosts):
                    raise FetchFailure('unsafe_redirect')
                data = response.read(MAX_BYTES + 1)
                if len(data) > MAX_BYTES:
                    raise FetchFailure('too_large')
                charset = response.headers.get_content_charset() or 'utf-8'
                text = data.decode(charset, errors='replace')
                self.state[key] = {h: response.headers[h] for h in ('ETag', 'Last-Modified')
                                   if response.headers.get(h) and len(response.headers[h]) < 1000}
                return text, response.url
        except HTTPError as exc:
            if exc.code == 304:
                return None, url
            raise FetchFailure('http_' + str(exc.code)) from None
        except FeedError as exc:
            raise FetchFailure(str(exc)) from None
        except (URLError, TimeoutError, OSError, HTTPException):
            raise FetchFailure('network_error') from None


def allowed_by_robots(client: Client, source: dict, state: dict, now: datetime, url: str | None = None) -> bool:
    url = url or source['url']
    origin = urlunsplit((*urlsplit(url)[:2], '/robots.txt', '', ''))
    day = now.date().isoformat()
    cache = state.setdefault('robots', {}).get(origin, {})
    if cache.get('day') != day:
        try:
            text, _ = client.fetch(origin, source['hosts'])
            if text is not None:
                # HTML 오류 페이지를 robots 규칙으로 해석하지 않습니다.
                rules = text[:100_000] if re.search(r'^\s*user-agent:', text, re.I | re.M) else ''
                cache = {'rules': rules, 'day': day}
            else:
                cache = dict(cache, day=day)
        except FetchFailure as exc:
            if str(exc) in ('http_404', 'http_410'):
                cache = {'rules': '', 'day': day}
            else:
                raise
        state['robots'][origin] = cache
    parser = RobotFileParser()
    parser.parse(cache.get('rules', '').splitlines())
    return parser.can_fetch(AGENT, url)


def short_korean(text: str, title: str) -> str:
    text = clean(text)
    if len(re.findall(r'[가-힣]', text)) < 12 or text == title:
        return ''
    # 짧은 원문 소개만 발췌합니다. 완결 문장이 없으면 생략 부호를 명시합니다.
    # 원제와 함께 긴 원문을 재출간하지 않도록 발췌 분량을 제한합니다.
    words = text.split()
    budget = max(5, 25 - len(title.split()))
    if len(words) > budget:
        text = ' '.join(words[:budget]) + '…'
    if len(text) <= 230:
        return text
    chunk = text[:230]
    endings = [m.end() for m in re.finditer(r'(?:습니다|입니다|한다|이다|했다|된다)[.!?]?(?:\s|$)', chunk)]
    return chunk[:endings[-1]].strip() if endings else chunk.rsplit(' ', 1)[0] + '…'


def overview(item: dict, source: dict) -> tuple[str, str]:
    native = short_korean(item.get('description', ''), item['title'])
    if native:
        return native, '공식 한국어 소개 발췌'
    text = item['title'] + ' ' + item.get('description', '')
    topics = [label for pattern, label in TOPICS if re.search(pattern, text, re.I)][:5]
    if item.get('kind') == 'weights':
        first = source['name'] + '의 공식 모델 배포물 등록 소식입니다.'
    elif source['group'] == 'models':
        first = source['name'] + '의 모델 관련 공식 발표입니다.'
    else:
        first = source['name'] + '에서 발행한 보고서입니다.'
    if topics:
        first += ' 공개 제목·소개에서 ' + '·'.join(topics) + ' 주제를 다룹니다.'
    return first, '제목·공개 정보에 따른 한국어 안내'


def validate_item(item: dict, source: dict) -> dict | None:
    item = dict(item)
    item['title'] = clean(item.get('title', ''))[:500]
    item['description'] = clean(item.get('description', ''))[:600]
    item['date'] = str(item.get('date') or '').strip()[:100]
    item['url'] = urljoin(source['url'], item.get('url', ''))
    if not item['title'] or not safe_url(item['url'], source['hosts']):
        return None
    if item.get('pdf_url'):
        item['pdf_url'] = urljoin(item['url'], item['pdf_url'])
        if not safe_url(item['pdf_url'], source['hosts']):
            item.pop('pdf_url')
    return item


def load_config() -> dict:
    sources = []
    for name in ('model_sources.json', 'report_sources.json'):
        sources.extend(json.loads((HERE / name).read_text(encoding='utf-8'))['sources'])
    assert len({s['id'] for s in sources}) == len(sources)
    for source in sources:
        source['keep_fragment'] = source.get('preserve_fragment', False)
        source['homepage'] = source.get('homepage', urlunsplit((*urlsplit(source['url'])[:2], '/', '', '')))
        if source.get('adapter') == 'deepseek_updates':
            source['detail'] = False  # 날짜별 절의 소개가 이미 목록에 있습니다.
        if source.get('format') == 'feed':
            source['detail'] = False  # 충분한 피드 소개는 다시 기사 본문을 요청하지 않습니다.
            source['detail_if_empty'] = True
        if source['group'] not in GROUPS or not safe_url(source['url'], source['hosts']):
            raise ValueError('Invalid source configuration: ' + source['id'])
    return {'sources': sources, 'initial_days': 45, 'initial_per_source': 3}


def covered_urls(repo: Path) -> set[str]:
    """기존에 해설한 정확한 공식 원문을 새 소식으로 재게시하지 않습니다."""
    result = set()
    for group, (folder, _) in GROUPS.items():
        for path in (repo / folder).rglob('*.md'):
            if '새소식_updates' in path.parts:
                continue
            for url in re.findall(r'\]\(<?(https://[^\s)>]+)', path.read_text(encoding='utf-8')):
                result.add(publication_key(group, url, True))
    return result


def outside_window(value: str, cutoff: datetime, now: datetime) -> tuple[bool, bool]:
    """월 단위 발행일은 월끼리 비교하고 공개 표시에 임의의 날짜를 넣지 않습니다."""
    if re.fullmatch(r'\d{4}-\d{2}', value):
        return value < cutoff.strftime('%Y-%m'), value > now.strftime('%Y-%m')
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return value < cutoff.astimezone(KST).date().isoformat(), value > (now.astimezone(KST).date() + timedelta(days=1)).isoformat()
    parsed = date_time(value)
    return (parsed < cutoff, parsed > now + timedelta(days=1)) if parsed else (False, False)


def write_if_changed(path: Path, text: str) -> bool:
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError('Symlink output path is not allowed')
    if path.exists() and path.read_text(encoding='utf-8') == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(text, encoding='utf-8', newline='\n')
    temporary.replace(path)
    return True


def render(items: list[dict], group: str, stamp: str, prefix: str) -> str:
    label = GROUPS[group][1]
    lines = ['# ' + label, '', '반영: ' + stamp + ' KST', '',
             f'[카테고리 목차]({prefix}../README.md) · [날짜별 소식]({prefix}날짜별/README.md)', '']
    for item in sorted(items, key=lambda item: (item.get('date', ''), item['key']), reverse=True):
        lines += ['## ' + md_text(item['title']), '']
        if item.get('update'):
            lines += ['기존 발표의 소개 내용이 갱신되었습니다.', '']
        if item['summary_mode'] == '공식 한국어 소개 발췌':
            lines += ['> ' + md_text(item['summary_ko']), '']
        else:
            lines += [md_text(item['summary_ko']), '']
        date_label = '배포 저장소 등록일' if item.get('published_kind') == 'repository_created' else ('발표일' if group == 'models' else '공식 페이지 표기일')
        date = item.get('date') or '원문에 미표기'
        if 'T' in date and date_time(date):
            date = date_time(date).astimezone(KST).strftime('%Y-%m-%d %H:%M KST')
        lines += [f"출처: [{md_text(item['source_name'])}](<{md_url(item['homepage'])}>) · "
                  f"[원문](<{md_url(item['url'])}>) · {date_label}: {md_text(date)}", '']
        if item.get('pdf_url'):
            lines += [f"[발행 기관의 PDF](<{md_url(item['pdf_url'])}>)", '']
        lines += ['개요: ' + item['summary_mode'], '']
    lines += ['공식 한국어 소개는 짧게 발췌하며, 다른 언어의 자료는 제목과 공개 정보의 주제를 한국어로 안내합니다. '
              '원문 전체를 번역하거나 새로운 분석을 작성한 글과는 구분합니다.', '']
    return '\n'.join(lines)


def publish(repo: Path, state: dict, accepted: list[dict], now: datetime) -> list[str]:
    changed = []
    day = now.astimezone(KST).date().isoformat()
    stamp = now.astimezone(KST).strftime('%Y-%m-%d %H:%M')
    for group, (category, _) in GROUPS.items():
        updates = [item for item in accepted if item['group'] == group]
        if not updates:
            continue
        base = repo / category / '새소식_updates'
        dated = base / '날짜별' / (day + '.md')
        # 당일 기록만 합치며 이전 날짜 문서는 다시 쓰지 않습니다.
        days = state.setdefault('days', {}).setdefault(group, {})
        todays = {item['key']: item for item in days.get(day, [])}
        for item in updates:
            todays[item['key']] = item
        days[day] = sorted(todays.values(), key=lambda item: item['key'])
        for path, content in ((dated, render(list(todays.values()), group, stamp, '../')),
                              (base / 'README.md', render(list(todays.values()), group, stamp, ''))):
            if write_if_changed(path, content):
                changed.append(path.relative_to(repo).as_posix())
        dates = ['# 날짜별 ' + GROUPS[group][1], '', '[최근 소식](../README.md)', '']
        dates += [f'- [{date}]({date}.md)' for date in sorted(days, reverse=True)]
        index_path = base / '날짜별' / 'README.md'
        if write_if_changed(index_path, '\n'.join(dates) + '\n'):
            changed.append(index_path.relative_to(repo).as_posix())
    return changed


def run(config: dict, state_path: Path, repo: Path, now: datetime, fetcher=None) -> dict:
    original = state_path.read_text(encoding='utf-8') if state_path.exists() else ''
    state = json.loads(original) if original else {'schema': 1, 'requests': {}, 'sources': {}, 'seen': {}, 'aliases': {}, 'robots': {}}
    if state.get('schema') != 1:
        raise ValueError('Unsupported state schema')
    client = Client(state['requests'])
    fetch = fetcher or client.fetch
    covered = covered_urls(repo)
    accepted, reports = [], []
    started = now.isoformat()
    for source in config['sources']:
        source_state = state['sources'].get(source['id'], {})
        report = {'id': source['id'], 'status': 'ok', 'new': 0, 'updated': 0}
        reports.append(report)
        adapter = model_adapters if source['group'] == 'models' else report_adapters
        try:
            if fetcher is None and not allowed_by_robots(client, source, state, now):
                raise FetchFailure('robots_disallowed')
            text, final_url = fetch(source['url'], source['hosts'])
            if text is None:
                candidates = source_state.get('candidates', [])
                if not source_state:
                    state['requests'].pop(canonical(source['url']), None)
                    raise FetchFailure('empty_cache_on_304')
                report['status'] = 'unchanged'
            else:
                candidates = parse_feed(text) if source.get('format') == 'feed' else adapter.discover(source, text)
                if not candidates and source.get('adapter') == 'huggingface_models':
                    models = json.loads(text)
                    if isinstance(models, list) and models and all(isinstance(row, dict) and
                        row.get('id', '').startswith(source['organization'] + '/') for row in models):
                        report['status'] = 'no_eligible_items'
                        source_state.update(initialized=True, candidates=[], since=source_state.get('since', started))
                        state['sources'][source['id']] = source_state
                        continue
                if not candidates:
                    raise FetchFailure('parse_empty')
                candidates = [item for item in (validate_item(item, source) for item in candidates) if item]
                if not candidates:
                    raise FetchFailure('parse_empty')
                source_state['candidates'] = candidates
            initial = not source_state.get('initialized')
            posted = 0
            # 모든 목록 항목을 관측합니다. 첫 실행 제한 이후 구판을 조금씩 게시하지 않습니다.
            for item in candidates:
                if source['group'] == 'models' and hasattr(adapter, 'eligible') and not adapter.eligible(source, item):
                    continue
                observation_key = source['id'] + ':' + canonical(item['url'], source.get('keep_fragment', False))
                identity = publication_key(source['group'], item['url'], source.get('keep_fragment', False))
                identity = state['aliases'].get(identity, identity)
                observed = state['seen'].get(observation_key)
                marker = fingerprint(item)
                if observed and observed.get('list_fingerprint') == marker and observed.get('status') != 'pending':
                    continue
                if identity in covered:
                    state['seen'][observation_key] = {'list_fingerprint': marker, 'status': 'existing_analysis'}
                    continue
                list_cutoff = now - timedelta(days=config.get('initial_days', 45)) if initial else date_time(source_state.get('since', started))
                if observed and observed.get('status') == 'pending' and observed.get('cutoff'):
                    list_cutoff = date_time(observed['cutoff'])
                list_older, list_future = outside_window(item.get('date', ''), list_cutoff, now)
                if list_future:
                    continue
                if list_older and not state['seen'].get(identity):
                    state['seen'][observation_key] = {'list_fingerprint': marker, 'status': 'older_material'}
                    continue
                if initial and posted >= config.get('initial_per_source', 3):
                    state['seen'][observation_key] = {'list_fingerprint': marker, 'status': 'bootstrap_skipped'}
                    continue
                try:
                    full = dict(item)
                    if source.get('detail', True) or (source.get('detail_if_empty') and len(full.get('description', '')) < 60):
                        detail_url = item.get('detail_url') or item['url']
                        if fetcher is None and not allowed_by_robots(client, source, state, now, detail_url):
                            raise FetchFailure('robots_disallowed')
                        detail_text, detail_final = fetch(detail_url, source['hosts'])
                        if detail_text is None:
                            values = state.get('details', {}).get(canonical(detail_url))
                            if values is None:
                                # 부분 실패 뒤의 캐시 표식만 남아 있으면 다음에는 본문을 요청합니다.
                                state['requests'].pop(canonical(detail_url), None)
                                raise FetchFailure('detail_304_without_body')
                        else:
                            values = generic_detail(detail_text, detail_final)
                            values.update(adapter.detail(source, detail_text, detail_final))
                            if values.get('description'):
                                values['description'] = clean(values['description'])[:600]
                            state.setdefault('details', {})[canonical(detail_url)] = values
                        # 메타 제목이 일반 사이트명인 경우 어댑터가 반환한 원문 제목을 우선합니다.
                        full.update({k: v for k, v in values.items() if v})
                        proposed = full.pop('canonical_url', detail_final)
                        if values.get('canonical'):
                            proposed = values['canonical']
                        if source.get('keep_fragment'):
                            proposed = item['url']
                        if safe_url(proposed, source['hosts']):
                            full['url'] = proposed
                    full = validate_item(full, source)
                    if full is None:
                        raise FetchFailure('invalid_detail')
                except (FetchFailure, ValueError, TypeError, KeyError) as exc:
                    if source.get('format') == 'feed' and not source.get('detail', True) and item.get('description') and item.get('date'):
                        # RSS 자체에 날짜·소개가 있으면 차단된 웹 본문 없이 그 공개 소개를 씁니다.
                        full = dict(item)
                        report['feed_only'] = report.get('feed_only', 0) + 1
                    else:
                        retry_cutoff = (observed or {}).get('cutoff') or (
                            now - timedelta(days=config.get('initial_days', 45)) if initial
                            else date_time(source_state.get('since', started))).isoformat()
                        state['seen'][observation_key] = {'list_fingerprint': marker, 'status': 'pending', 'cutoff': retry_cutoff,
                                                         'bootstrap_initial': (observed or {}).get('bootstrap_initial', initial)}
                        report.setdefault('detail_errors', []).append({'url': item['url'], 'error': str(exc) if isinstance(exc, FetchFailure) else type(exc).__name__})
                        continue
                actual = publication_key(source['group'], full['url'], source.get('keep_fragment', False))
                state['aliases'][identity] = actual
                previous = state['seen'].get(actual)
                full_fingerprint = fingerprint(full)
                if actual in covered or (previous and (previous.get('fingerprint') == full_fingerprint or
                    (previous.get('language') == 'ko' and source.get('language') != 'ko'))):
                    state['seen'][observation_key] = {'list_fingerprint': marker, 'status': 'unchanged'}
                    continue
                cutoff = now - timedelta(days=config.get('initial_days', 45)) if initial else date_time(source_state.get('since', started))
                if observed and observed.get('status') == 'pending' and observed.get('cutoff'):
                    cutoff = date_time(observed['cutoff'])
                older, future = outside_window(full.get('date', ''), cutoff, now)
                if future:
                    report.setdefault('future_items', []).append(full['url'])
                    continue
                # 미표기 발행일을 첫 발견일로 대신하지 않습니다.
                bootstrap = initial or bool((observed or {}).get('bootstrap_initial'))
                if (bootstrap and not full.get('date')) or (older and previous is None):
                    state['seen'][observation_key] = {'list_fingerprint': marker, 'status': 'older_material'}
                    continue
                summary, mode = overview(full, source)
                display = {key: value for key, value in full.items()
                           if key in ('title', 'url', 'date', 'pdf_url', 'kind', 'published_kind')}
                display.update(key=actual, group=source['group'], source_name=source['name'], homepage=source.get('homepage', source['url']),
                               summary_ko=summary, summary_mode=mode, update=bool(previous), first_seen=now.isoformat())
                accepted.append(display)
                state['seen'][actual] = {'fingerprint': full_fingerprint, 'url': full['url'],
                                        'language': source.get('language', ''),
                                        'first_seen': previous.get('first_seen', started) if previous else started}
                state['seen'][observation_key] = {'list_fingerprint': marker, 'status': 'posted'}
                report['updated' if previous else 'new'] += 1
                posted += 1
            source_state.update(initialized=True, since=source_state.get('since', started))
            state['sources'][source['id']] = source_state
        except (FetchFailure, ValueError, TypeError, KeyError, ET.ParseError) as exc:
            report['status'] = str(exc) if isinstance(exc, FetchFailure) else 'parse_error'
            # 본문을 해석하지 못한 응답의 ETag로 304 상태에 고착되지 않게 합니다.
            state['requests'].pop(canonical(source['url']), None)
    if not any(report['status'] in ('ok', 'unchanged', 'no_eligible_items') for report in reports):
        raise RuntimeError('All official sources failed; existing publications are unchanged.')
    # 한 실행의 같은 원문은 하나로 남깁니다. 한국어 원문 소개를 우선합니다.
    unique = {}
    for item in accepted:
        old_item = unique.get(item['key'])
        if not old_item or item['summary_mode'] == '공식 한국어 소개 발췌':
            unique[item['key']] = item
    changed = publish(repo, state, list(unique.values()), now)
    serialized = json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    if serialized != original:
        write_if_changed(state_path, serialized)
    return {'checked_at': now.isoformat(), 'sources': reports, 'changed_files': changed,
            'new_or_updated': len(unique), 'state_changed': serialized != original}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--state', type=Path, default=HERE / 'state.json')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = run(load_config(), args.state, args.repo, datetime.now(timezone.utc))
    if args.report:
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
