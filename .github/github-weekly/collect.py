"""GitHub 주간 Trending과 공식 저장소 정보를 읽어 주차별 소개를 보관합니다."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from bs4 import BeautifulSoup
import guides
import comparisons
import source_checks

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUTPUT = ROOT / '인기GitHub프로젝트_github-weekly'
KST = timezone(timedelta(hours=9))
TRENDING = 'https://github.com/trending?since=weekly'
SLUG = re.compile(r'[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+\Z')


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old, new = urlsplit(req.full_url), urlsplit(newurl)
        if new.scheme != 'https' or new.hostname != old.hostname or new.port not in (None, 443):
            raise ValueError('Cross-host or insecure redirect refused')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def clean(text: str) -> str:
    """외부 설명이 Markdown 링크·HTML·표 구문으로 실행되지 않게 표시합니다."""
    text = html.escape(' '.join(str(text).split()), quote=False)
    return re.sub(r'([\\`*_|\[\]#])', r'\\\1', text)


def get(url: str, token: str = '') -> tuple[bytes, str]:
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname not in ('github.com', 'api.github.com'):
        raise ValueError('Unexpected request host')
    headers = {'User-Agent': 'engineering-notes-weekly/1.0', 'Accept': 'text/html'}
    if url.startswith('https://api.github.com/'):
        headers.update({'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'})
        if token:
            headers['Authorization'] = 'Bearer ' + token
    for attempt in range(3):
        try:
            with build_opener(SafeRedirect()).open(Request(url, headers=headers), timeout=45) as response:
                final = response.url
                # 인증 헤더를 별도 호스트로 보내거나 외부 다운로드를 실행하지 않습니다.
                if not final.startswith(('https://github.com/', 'https://api.github.com/')):
                    raise ValueError('Unexpected response host')
                data = response.read(5_000_001)
                if len(data) > 5_000_000:
                    raise ValueError('Response exceeds size limit')
                return data, final
        except HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
        except (URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(2 ** attempt)
    raise RuntimeError('Request failed')


def parse_trending(document: bytes, count: int = 10) -> list[dict]:
    soup = BeautifulSoup(document, 'html.parser')
    rows, seen = [], set()
    articles = soup.select('article.Box-row')
    if len(articles) < count:
        raise ValueError('Trending layout changed or fewer than ten repositories were returned')
    for article in articles[:count]:
        link = article.select_one('h2 a[href]')
        slug = link['href'].strip('/') if link else ''
        if not SLUG.fullmatch(slug) or slug.casefold() in seen:
            raise ValueError('Invalid or duplicate repository in Trending')
        metric = re.search(r'([\d,]+)\s+stars?\s+this\s+week', article.get_text(' ', strip=True), re.I)
        if not metric:
            raise ValueError('Weekly stars metric missing: ' + slug)
        seen.add(slug.casefold())
        rows.append({'rank': len(rows) + 1, 'requested_full_name': slug,
                     'weekly_stars': int(metric.group(1).replace(',', ''))})
    return rows


def repository(slug: str, token: str) -> dict:
    if not SLUG.fullmatch(slug):
        raise ValueError('Invalid repository name')
    payload, _ = get('https://api.github.com/repos/' + slug, token)
    data = json.loads(payload)
    canonical = data['full_name']
    if not SLUG.fullmatch(canonical) or data['html_url'].casefold() != ('https://github.com/' + canonical).casefold():
        raise ValueError('Invalid canonical GitHub URL')
    return {key: data.get(key) for key in ('id', 'full_name', 'html_url', 'description', 'language',
            'stargazers_count', 'forks_count', 'topics', 'archived', 'disabled', 'license', 'default_branch')} | {
                'metadata_url': 'https://api.github.com/repos/' + canonical}


class Introductions:
    def __init__(self, reviewed: dict, cache: dict):
        self.reviewed = {name.casefold(): item for name, item in reviewed.items()}
        self.cache = cache
        self.translator = None

    def translate(self, source: str) -> dict:
        key = digest(source)
        if key in self.cache:
            return self.cache[key]
        # 공개 번역 모델은 GitHub runner CPU에서 실행하며 유료 API를 호출하지 않습니다.
        import argostranslate.package
        import argostranslate.translate
        if self.translator is None:
            installed = argostranslate.package.get_installed_packages()
            pair = [p for p in installed if p.from_code == 'en' and p.to_code == 'ko']
            if pair and any(p.package_version != '1.1' for p in pair):
                raise ValueError('Unexpected installed Argos en-ko model version')
            if not pair:
                argostranslate.package.update_package_index()
                package = next(p for p in argostranslate.package.get_available_packages()
                               if p.from_code == 'en' and p.to_code == 'ko' and p.package_version == '1.1')
                argostranslate.package.install_from_path(package.download())
            self.translator = argostranslate.translate.get_translation_from_codes('en', 'ko')
        translated = self.translator.translate(source)
        if not translated.strip() or not re.search(r'[가-힣]', translated):
            raise ValueError('Korean translation unavailable')
        result = {'source': source, 'text': translated, 'method': 'Argos Translate en→ko 1.1'}
        self.cache[key] = result
        return result

    def for_repo(self, repo: dict, readme_sha: str | None = None) -> dict:
        item = self.reviewed.get(repo['full_name'].casefold())
        if item and item.get('repository_id') == repo['id'] and item.get('description_sha256') == digest(repo.get('description') or '') and (readme_sha is None or item.get('readme_sha') == readme_sha):
            return {'text': item['summary_ko'], 'detail': item.get('detail_ko', ''),
                    'method': 'README 해설 (' + item['reviewed_at'] + ' 확인)',
                    'source_url': item.get('source_url', repo['html_url'] + '#readme')}
        about = (repo.get('description') or '').strip()
        if re.search(r'[가-힣]', about):
            return {'text': about, 'detail': '', 'method': '저장소의 한국어 소개',
                    'source_url': repo['html_url']}
        if not about:
            return {'text': f"{repo.get('language') or '여러 언어'} 기반 프로젝트입니다. 사용 목적과 실행 방법은 공식 README에서 확인하실 수 있습니다.",
                    'detail': '', 'method': 'GitHub 공개 메타데이터', 'source_url': repo['html_url'] + '#readme'}
        # 영어 설명만 번역합니다. 다른 언어를 영어라고 가정해 오역하지 않습니다.
        if re.search(r'[\u4e00-\u9fff\u3040-\u30ff]', about):
            return {'text': f"{repo.get('language') or '여러 언어'} 기반 프로젝트이며, 공식 소개와 사용 예시는 아래 원문에서 읽으실 수 있습니다.",
                    'detail': '', 'method': 'GitHub 공개 메타데이터·원문 병기', 'source_url': repo['html_url']}
        translation = self.translate(about)
        return {'text': translation['text'], 'detail': '', 'method': translation['method'] + ' 기계번역',
                'source_url': repo['html_url']}


def week_start(now: datetime) -> datetime:
    now = now.astimezone(KST)
    return (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)


def label(start: datetime) -> str:
    return f'{start.year}년 {start.month}월 {(start.day - 1) // 7 + 1}주차'


def render_entry(item: dict, numbered: bool = True) -> str:
    repo, intro = item['repository'], item['introduction']
    prefix = str(item['rank']) + '. ' if numbered else ''
    license_id = (repo.get('license') or {}).get('spdx_id')
    if license_id in (None, 'NOASSERTION', 'OTHER'):
        license_id = '공식 라이선스 파일 확인'
    lines = [f"## {prefix}{repo['full_name']}", '', clean(intro['text']), '']
    if intro.get('detail'):
        lines.extend([clean(intro['detail']), ''])
    if item.get('guide'):
        lines.extend(guides.render_guide(item['guide'], clean))
    lines.extend(['### 저장소 정보', ''])
    lines.extend([f"- [저장소]({repo['html_url']}) · [README]({repo['html_url']}#readme) · [소개 근거]({intro['source_url']})",
                  f"- 주요 언어: {clean(repo.get('language') or '미표기')} · 라이선스: {clean(license_id)}",
                  f"- 누적 별: {repo['stargazers_count']:,}개 · 포크: {repo['forks_count']:,}개",
                  '- 소개 방식: ' + clean(intro['method'])])
    if numbered:
        lines.append(f"- Trending 주간 표시: +{item['weekly_stars']:,} stars this week")
    if repo.get('archived') or repo.get('disabled'):
        lines.append('- 저장소 상태: ' + ('보관됨' if repo.get('archived') else '사용 제한됨'))
    about = repo.get('description')
    if about:
        lines.extend(['', '원문 소개: ' + clean(about)])
    return '\n'.join(lines) + '\n'


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def update_index(output: Path) -> None:
    files = sorted((output / '주간기록').glob('*/*/*.json'), reverse=True)
    lines = ['# 주간 프로젝트 기록 | Weekly project archive', '',
             '발행 주의 월요일을 기준으로 월과 주차를 표시합니다. 매주 수집 당시의 주간 Trending을 보관합니다.', '']
    month = None
    for path in files:
        data = json.loads(path.read_text(encoding='utf-8'))
        current = data['week_start'][:7]
        if month != current:
            month = current
            lines.extend(['## ' + month, ''])
        relative = path.with_suffix('.md').relative_to(output / '주간기록').as_posix()
        lines.append(f"- [{data['label']}]({relative}) — {data['collected_at'][:10]} 수집")
    lines.extend(['', '[프로젝트 소개로 돌아가기](../README.md)', ''])
    (output / '주간기록' / 'README.md').write_text('\n'.join(lines), encoding='utf-8')


def collect(output: Path, now: datetime, token: str, reviewed: dict, cache_path: Path, details: dict | None = None, assessments: dict | None = None) -> dict:
    start = week_start(now)
    target = output / '주간기록' / f'{start.year:04d}' / f'{start.month:02d}' / start.strftime('%Y-%m-%d')
    # 발행된 같은 주는 그대로 두므로 재실행으로 과거 순위가 바뀌지 않습니다.
    if target.with_suffix('.json').exists():
        if not target.with_suffix('.md').exists():
            data = json.loads(target.with_suffix('.json').read_text(encoding='utf-8'))
            target.with_suffix('.md').write_text(render_archive(data), encoding='utf-8')
            update_index(output)
            return {'status': 'recovered', 'week_start': start.date().isoformat()}
        return {'status': 'already_published', 'week_start': start.date().isoformat()}
    raw, final_url = get(TRENDING)
    rows = parse_trending(raw)
    cache = json.loads(cache_path.read_text(encoding='utf-8')) if cache_path.exists() else {}
    introductions = Introductions(reviewed, cache)
    identities = set()
    for row in rows:
        repo = repository(row['requested_full_name'], token)
        if repo['id'] in identities:
            raise ValueError('Redirected duplicate repository')
        identities.add(repo['id'])
        row['repository'] = repo
        if details is not None:
            readme = guides.fetch_readme(repo, token, get)
            row['introduction'] = introductions.for_repo(repo, readme_sha=readme['sha'])
            detail_map = {k.casefold(): v for k, v in details.items()}
            manual = detail_map.get(repo['full_name'].casefold(), {})
            if manual.get('repository_id') != repo['id'] or manual.get('readme_sha') != readme['sha']:
                readme['documents'] = guides.linked_documents(repo, readme, token, get)
            row['readme'] = {key: value for key, value in readme.items() if key not in ('text', 'documents')}
            row['readme']['documents'] = [{k: v for k, v in document.items() if k != 'text'}
                                        for document in readme.get('documents', [])]
            row['guide'] = guides.make_guide(repo, readme, detail_map, introductions)
            if assessments is not None:
                row['guide']['assessment'] = comparisons.build(repo, readme,
                    {k.casefold(): v for k, v in assessments.items()}, introductions, get, repository, token)
            row['guide']['source_checks'] = source_checks.verify(row['guide'], readme, get, token)
        else:
            row['introduction'] = introductions.for_repo(repo)
    stamp = now.astimezone(KST).isoformat(timespec='seconds')
    data = {'schema_version': 1, 'label': label(start), 'week_start': start.date().isoformat(),
            'collected_at': stamp, 'source_url': final_url, 'source_sha256': hashlib.sha256(raw).hexdigest(),
            'selection': 'GitHub Trending, all languages, since=weekly, first 10 in displayed order',
            'run_url': os.environ.get('GITHUB_SERVER_URL', 'https://github.com') + '/' + os.environ['GITHUB_REPOSITORY'] + '/actions/runs/' + os.environ['GITHUB_RUN_ID'] if os.environ.get('GITHUB_RUN_ID') else None,
            'items': rows}
    # 모든 원본 조회와 소개 생성이 성공한 뒤에만 새 주를 발행합니다.
    write_json(target.with_suffix('.json'), data)
    target.with_suffix('.md').write_text(render_archive(data), encoding='utf-8')
    write_json(cache_path, cache)
    update_index(output)
    return {'status': 'published', 'week_start': data['week_start'], 'count': len(rows), 'collected_at': stamp}


def render_archive(data: dict) -> str:
    title = '# ' + data['label'] + ' 인기 GitHub 프로젝트\n\n'
    title += f"수집 시각: {data['collected_at']} (한국 표준시)\n\n[GitHub 주간 Trending]({data['source_url']})의 당시 표시 순서입니다. `stars this week`는 GitHub가 제공한 주간 값이며, 달력 주간의 직접 집계나 품질 순위가 아닙니다. 누적 별·포크는 저장소 API를 읽은 시점의 값입니다.\n\n"
    body = title + '\n'.join(render_entry(item) for item in data['items'])
    return body + '\n[주간 기록 목록](../../README.md) · [선정·수집 기준](../../../선정과업데이트_방법.md)\n'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    reviewed = json.loads((HERE / 'reviewed.json').read_text(encoding='utf-8'))
    details = json.loads((HERE / 'details.json').read_text(encoding='utf-8'))
    assessments = json.loads((HERE / 'comparisons.json').read_text(encoding='utf-8'))
    result = collect(args.output, datetime.now(KST), os.environ.get('GITHUB_TOKEN', ''), reviewed, HERE / 'translations.json', details, assessments)
    if args.report:
        write_json(args.report, result)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
