"""새 기사와 실질적인 후속 내용만 날짜별 뉴스에 반영합니다."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import re
import sys

from archive_news import publish_bundle
import collect_news as core

ROOT = Path(__file__).resolve().parents[2]
GROUP_PATHS = {'world': '세계주요뉴스_world', 'korea': '국내주요뉴스_korea'}
IMPORTANT = re.compile(
    r'속보|긴급|전쟁|휴전|종전|침공|대선|총선|정상회담|탄핵|비상계엄|대법원|헌법재판|'
    r'기준금리|경제성장률|물가|수출|수입|반도체|에너지|대규모|지진|태풍|홍수|산불|'
    r'사망|참사|감염|백신|노벨|우주|국가대표|월드컵|올림픽|우승|'
    r'\b(?:war|ceasefire|election|earthquake|flood|hurricane|outbreak|inflation|'
    r'interest rate|central bank|summit|missile|nuclear|breakthrough|world cup|olympic)\b', re.I)


def normalized(text: str) -> str:
    text = re.sub(r'\[(?:속보|종합|단독)[^\]]*\]|\((?:종합|종합\d보|\d보)\)', '', text)
    return re.sub(r'[^\w가-힣]', '', text.casefold())


def fingerprint(item: dict) -> str:
    return hashlib.sha256(normalized(item['title'] + ' ' + item.get('excerpt', '')).encode()).hexdigest()


def observed_key(url: str) -> str:
    return hashlib.sha256(core.url_key(url).encode()).hexdigest()


def facts(text: str) -> tuple:
    numbers = tuple(re.findall(r'\d+(?:[.,]\d+)*', text))
    flags = tuple(word for word in ('부인', '철회', '결렬', '타결', '승인', '사망', '오늘', '내일',
        'denies', 'withdraws', 'agrees', 'killed', 'rejects') if word in text.casefold())
    return numbers, flags


def substantive(old: dict, new: dict) -> bool:
    if normalized(old['title']) == normalized(new['title']) and not new.get('excerpt'):
        return False
    old_text, new_text = old['title'] + ' ' + old.get('excerpt', ''), new['title'] + ' ' + new.get('excerpt', '')
    if normalized(old_text) == normalized(new_text):
        return False
    if facts(old_text) != facts(new_text):
        return True
    if old.get('excerpt') and new.get('excerpt'):
        return normalized(old['excerpt']) != normalized(new['excerpt'])
    return SequenceMatcher(None, normalized(old['title']), normalized(new['title'])).ratio() < 0.78


def near_duplicate(old: dict, new: dict) -> bool:
    if old['group'] != new['group'] or facts(old['title'] + old.get('excerpt', '')) != facts(new['title'] + new.get('excerpt', '')):
        return False
    if normalized(old['title']) == normalized(new['title']):
        return not substantive(old, new)
    title_ratio = SequenceMatcher(None, normalized(old['title']), normalized(new['title'])).ratio()
    return title_ratio > 0.92 and normalized(old.get('excerpt', '')) == normalized(new.get('excerpt', ''))


def priority(item: dict, source: dict, now: datetime) -> float:
    age = max(0, (now - datetime.fromisoformat(item['published_at'])).total_seconds() / 3600)
    routine = 18 if re.search(r'위로연|참전유공자|체험행사|축제|방문.*협력|\[특징주\]|할인행사', item['title']) else 0
    return (source.get('priority', 20) - routine + min(20, 4 * len(set(IMPORTANT.findall(item['title'] + ' ' + item.get('excerpt', '')))))
            + max(0, 12 - age) - min(item.get('feed_rank', 0), 30) * 0.15)


def load_state(path: Path) -> dict:
    if not path.exists():
        return {'schema_version': 1, 'articles': {}, 'feeds': {}}
    state = json.loads(path.read_text(encoding='utf-8'))
    if state.get('schema_version') != 1 or not isinstance(state.get('articles'), dict):
        raise ValueError('뉴스 상태 파일 형식이 올바르지 않습니다.')
    return state


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def pick_candidates(reports: list[dict], state: dict, now: datetime, limit: int = 10) -> list[dict]:
    candidates = {}
    for report in reports:
        source = report['source']
        for item in report['items']:
            posted = state['articles'].get(core.url_key(item['url']))
            if posted and not substantive(posted, item):
                continue
            candidate = dict(item, source_id=source['id'], source_name=source['name'], group=source['group'],
                summary_mode=source.get('summary_mode', 'link_only'), homepage=source['homepage'],
                license_url=source.get('license_url'), source_kind=source.get('kind', 'news'),
                score=priority(item, source, now))
            key = core.url_key(candidate['url'])
            if key not in candidates or candidates[key]['score'] < candidate['score']:
                candidates[key] = candidate
    accepted, per_group, per_source = [], {}, {}
    recent = [a for a in state['articles'].values()
              if datetime.fromisoformat(a['seen_at']) >= now - timedelta(days=3)]
    for key, item in sorted(candidates.items(), key=lambda pair: pair[1]['score'], reverse=True):
        old = state['articles'].get(key)
        if not old and state.get('observed', {}).get(observed_key(item['url']), {}).get('fingerprint') == fingerprint(item):
            continue
        if old and not substantive(old, item):
            continue
        if not old and any(near_duplicate(previous, item) for previous in recent + accepted):
            continue
        group, source_id = item['group'], item['source_id']
        if per_group.get(group, 0) >= limit or per_source.get(source_id, 0) >= 3:
            continue
        item['key'], item['seen_at'] = key, now.isoformat()
        item['update'] = old is not None
        item['history'] = list(old.get('history', [])) if old else []
        if old:
            item['history'].append({'title': old['title'], 'seen_at': old['seen_at']})
        item['history'] = item['history'][-6:]
        accepted.append(item)
        per_group[group] = per_group.get(group, 0) + 1
        per_source[source_id] = per_source.get(source_id, 0) + 1
    return accepted


def render_group(items: list[dict], group: str, now: datetime) -> str:
    title = '세계 주요뉴스' if group == 'world' else '국내 주요뉴스'
    root_url = 'https://github.com/yoonip/engineering-notes/tree/main/'
    group_url = root_url + '뉴스_news/' + GROUP_PATHS[group]
    lines = ['# ' + title, '', '갱신: ' + now.astimezone(core.KST).strftime('%Y-%m-%d %H:%M') + ' KST', '',
        f'[뉴스](<{root_url}뉴스_news>) · [날짜별 뉴스](<{group_url}/날짜별>)', '']
    main = [a for a in items if a.get('summary_mode') != 'link_only']
    links = [a for a in items if a.get('summary_mode') == 'link_only']
    for item in sorted(main, key=lambda i: (i['score'], i['seen_at']), reverse=True):
        lines += ['## ' + core.md_text(item['title']), '']
        if item.get('update'):
            lines += ['후속 내용이 반영된 기사입니다.', '']
        if item.get('excerpt'):
            lines += ['> ' + core.md_text(item['excerpt']), '']
        published = datetime.fromisoformat(item['published_at']).astimezone(core.KST).strftime('%Y-%m-%d %H:%M')
        credit = ' · 작성·제공: ' + core.md_text(item['credit']) if item.get('credit') else ''
        origin = '기관 발표 · ' if item.get('source_kind') == 'institution' else ''
        lines += [f"{origin}출처: [{core.md_text(item['source_name'])}](<{item['homepage']}>) · "
                  f"[원문](<{core.md_url(item['url'])}>) · {published} KST{credit}", '']
    if links:
        lines += ['## 다른 매체의 원문', '']
        for item in sorted(links, key=lambda i: i['score'], reverse=True):
            lines.append(f"- [{core.md_text(item['title'])}](<{core.md_url(item['url'])}>) · {core.md_text(item['source_name'])}")
        lines.append('')
    lines += ['기사 개요는 각 매체가 공식 피드로 제공한 내용을 기준으로 합니다. 본문의 상세 내용과 정정 사항은 원문에서 확인하실 수 있습니다.', '']
    if group == 'world':
        lines += ['[CNN](https://www.cnn.com/) · [BBC News](https://www.bbc.com/news) · [ABC News](https://abcnews.com/) · [Reuters](https://www.reuters.com/) · [AP News](https://apnews.com/)', '']
    else:
        lines += ['[KBS 뉴스](https://news.kbs.co.kr/) · [YTN](https://www.ytn.co.kr/) · [조선일보](https://www.chosun.com/) · [중앙일보](https://www.joongang.co.kr/)', '']
    return '\n'.join(lines)


def run(config: dict, state_path: Path, news_root: Path, now: datetime, translator=None, fetcher=core.fetch_source) -> dict:
    # translator는 호출하지 않습니다. 외부 AI가 주입되어도 공식 원문만 게시합니다.
    state = load_state(state_path)
    sources = [dict(s, conditional=state['feeds'].get(s['id'], {})) for s in config['sources']]
    with ThreadPoolExecutor(max_workers=4) as pool:
        reports = list(pool.map(lambda s: fetcher(s, now), sources))
    result = {'checked_at': now.isoformat(), 'changed': False,
              'sources': [{'id': r['source']['id'], 'state': r['state'], 'stats': r.get('stats', {})} for r in reports]}
    if not any(r['state'] in ('ok', 'unchanged', 'no_recent_items') for r in reports):
        raise RuntimeError('모든 피드 확인에 실패해 이전 뉴스를 유지합니다.')
    candidates = pick_candidates(reports, state, now, config.get('new_items_per_group', 10))
    before_metadata = json.dumps([state.get('observed', {}), state['feeds']], sort_keys=True)
    observed = state.setdefault('observed', {})
    for report in reports:
        if report.get('conditional'):
            state['feeds'][report['source']['id']] = report['conditional']
        for item in report['items']:
            posted = state['articles'].get(core.url_key(item['url']))
            if posted and not substantive(posted, item):
                continue
            key = observed_key(item['url'])
            value = fingerprint(item)
            if observed.get(key, {}).get('fingerprint') != value:
                observed[key] = {'fingerprint': value, 'at': now.isoformat()}
    state['observed'] = {k: v for k, v in observed.items() if datetime.fromisoformat(v['at']) >= now - timedelta(days=3)}
    metadata_changed = before_metadata != json.dumps([state['observed'], state['feeds']], sort_keys=True)
    if not candidates:
        result['new_articles'] = result['updated_articles'] = 0
        if metadata_changed:
            save_state(state_path, state)
        return result
    day = now.astimezone(core.KST).date()
    for item in candidates:
        item['day'] = day.isoformat()
        state['articles'][item['key']] = item
    for report in reports:
        if report.get('conditional'):
            state['feeds'][report['source']['id']] = report['conditional']
    # 이전 날짜는 보존하고 당일에는 새 기사와 같은 URL의 실질적인 변경만 반영합니다.
    for group, folder in GROUP_PATHS.items():
        if not any(a['group'] == group for a in candidates):
            continue
        todays = [a for a in state['articles'].values() if a['group'] == group and a['day'] == day.isoformat()]
        if todays:
            publish_bundle(news_root / folder / 'README.md', render_group(todays, group, now), now)
    # 제목과 짧은 표시 내용만 유지하며 원문 본문이나 RSS 전체는 저장하지 않습니다.
    state['articles'] = {k: a for k, a in state['articles'].items() if datetime.fromisoformat(a['seen_at']) >= now - timedelta(days=14)}
    save_state(state_path, state)
    result.update(changed=True, new_articles=sum(not a['update'] for a in candidates), updated_articles=sum(a['update'] for a in candidates))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', type=Path, default=Path(__file__).with_name('state.json'))
    parser.add_argument('--news-root', type=Path, default=ROOT / '뉴스_news')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = run(core.load_config(Path(__file__).with_name('sources.json')), args.state, args.news_root, datetime.now(timezone.utc))
    if args.report:
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
