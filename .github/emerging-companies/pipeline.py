"""Collect primary-source candidates and publish only explicitly reviewed analyses.

Deterministic discovery and local-model analysis are separate paths. The optional
local CPU engine is explicitly configured; no paid API or retired GitHub Models
endpoint is silently substituted. Automatic review is not human fact-checking.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone, timedelta
import hashlib
from html.parser import HTMLParser
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import sys
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

CATEGORY = '신생기업과기술사업_emerging-companies'
CONTROL = '.github/emerging-companies'
MAX_BYTES = 1_000_000
MAX_CANDIDATES = 1000
KST = timezone(timedelta(hours=9))
USER_AGENT = 'engineering-notes-primary-source-research/1.0'
ROBOTS_CACHE = {}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_url(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Only credential-free HTTPS URLs are allowed')
    if parsed.port not in (None, 443):
        raise ValueError('Non-standard ports are not allowed')
    hostname = parsed.hostname.encode('idna').decode('ascii').lower()
    if hostname in {'localhost', 'metadata.google.internal'} or hostname.endswith(('.local', '.internal')):
        raise ValueError('Internal host is not allowed')
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        pass
    else:
        if not address.is_global:
            raise ValueError('Non-public address is not allowed')
    return urlunsplit(('https', hostname, parsed.path or '/', parsed.query, ''))


def validate_destination(url: str, allowed_hosts: set[str]) -> str:
    clean = canonical_url(url)
    host = urlsplit(clean).hostname
    if host not in allowed_hosts:
        raise ValueError('Host is outside this source allowlist')
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(row[4][0]).is_global for row in addresses):
        raise ValueError('DNS includes a non-public address')
    return clean


class CheckedRedirect(HTTPRedirectHandler):
    def __init__(self, allowed_hosts: set[str]):
        self.allowed_hosts = allowed_hosts

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_destination(newurl, self.allowed_hosts)
        if urlsplit(newurl).path!='/robots.txt' and not robots_allowed(newurl,self.allowed_hosts):
            raise ValueError('Redirect target robots.txt disallows collection')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _fetch_raw(url: str, allowed_hosts: set[str]) -> dict:
    clean = validate_destination(url, allowed_hosts)
    request = Request(clean, headers={'User-Agent': USER_AGENT, 'Accept': 'text/html,application/rss+xml,application/atom+xml,application/xml'})
    opener = build_opener(CheckedRedirect(allowed_hosts))
    with opener.open(request, timeout=18) as response:
        content_type = response.headers.get_content_type()
        if content_type not in {'text/html', 'application/xhtml+xml', 'application/rss+xml', 'application/atom+xml', 'application/xml', 'text/xml', 'text/plain'}:
            raise ValueError('Unsupported source content type')
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError('Source exceeds byte limit')
        encoding = response.headers.get_content_charset() or 'utf-8'
        return {'url': canonical_url(response.geturl()), 'sha256': digest(raw),
                'content_type': content_type, 'text': raw.decode(encoding, errors='replace')}


def robots_allowed(url: str, allowed_hosts: set[str]) -> bool:
    clean=canonical_url(url)
    host=urlsplit(clean).hostname
    if host not in ROBOTS_CACHE:
        robot_url='https://'+host+'/robots.txt'
        try:
            raw=_fetch_raw(robot_url,allowed_hosts)
        except HTTPError as exc:
            if exc.code in (401,403): ROBOTS_CACHE[host]=False
            elif exc.code==404: ROBOTS_CACHE[host]=True
            else: raise ValueError('robots.txt could not be checked') from None
        else:
            parser=RobotFileParser(); parser.set_url(robot_url);parser.parse(raw['text'].splitlines())
            ROBOTS_CACHE[host]=parser
    decision=ROBOTS_CACHE[host]
    return decision if isinstance(decision,bool) else decision.can_fetch(USER_AGENT,clean)


def fetch(url: str, allowed_hosts: set[str]) -> dict:
    validate_destination(url,allowed_hosts)
    if not robots_allowed(url,allowed_hosts):
        raise ValueError('robots.txt disallows this source')
    return _fetch_raw(url,allowed_hosts)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.text = []
        self.title = []
        self.skip = 0
        self.in_title = False
        self.current_link = None
        self.main_depth = 0
        self.main_text = []
        self.after_h1 = False
        self.h1_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {'main', 'article'}: self.main_depth += 1
        if tag == 'h1': self.after_h1 = True
        if tag in {'script', 'style', 'noscript'}:
            self.skip += 1
        if tag == 'title': self.in_title = True
        if tag == 'a' and attrs.get('href'):
            self.current_link = [attrs['href'], []]

    def handle_endtag(self, tag):
        if tag in {'main', 'article'} and self.main_depth: self.main_depth -= 1
        if tag in {'script', 'style', 'noscript'} and self.skip:
            self.skip -= 1
        if tag == 'title': self.in_title = False
        if tag == 'a' and self.current_link is not None:
            self.links.append((self.current_link[0], ' '.join(self.current_link[1]).strip()))
            self.current_link = None

    def handle_data(self, text):
        if self.skip: return
        clean = ' '.join(text.split())
        if not clean: return
        self.text.append(clean)
        if self.main_depth: self.main_text.append(clean)
        if self.after_h1: self.h1_text.append(clean)
        if self.in_title: self.title.append(clean)
        if self.current_link is not None: self.current_link[1].append(clean)


def extract_candidates(document: dict, source: dict) -> list[dict]:
    candidates = []
    if source['kind'] == 'rss':
        if '<!DOCTYPE' in document['text'].upper() or '<!ENTITY' in document['text'].upper():
            raise ValueError('DTD/entities are not allowed in source feeds')
        tree = ET.fromstring(document['text'])
        for item in tree.findall('.//item'):
            url = (item.findtext('link') or '').strip()
            title = (item.findtext('title') or '').strip()
            if url and title: candidates.append({'url': url, 'title': title})
    else:
        parser = PageParser()
        parser.feed(document['text'])
        pattern = re.compile(source['candidate_path_pattern'])
        for url, label in parser.links:
            url = urljoin(document['url'], url)
            if pattern.search(urlsplit(url).path) and label:
                candidates.append({'url': url, 'title': label[:240]})
    unique = {}
    allowed = set(source['allowed_hosts'])
    for candidate in candidates:
        try:
            url = canonical_url(candidate['url'])
        except ValueError:
            continue
        if urlsplit(url).hostname not in allowed: continue
        unique.setdefault(url, {'url': url, 'title': candidate['title'][:240],
            'discovery_source': source['url'], 'status': 'unreviewed_source_candidate',
            'source_kind': source['label']})
    return list(unique.values())[:60]


def json_load(path: Path, default=None):
    if not path.exists():
        if default is not None: return default
        raise ValueError('Required repository file is missing: ' + path.name)
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def within(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ValueError('Invalid relative path')
    candidate = (root / relative).resolve()
    if Path(relative).is_absolute() or not candidate.is_relative_to(root.resolve()):
        raise ValueError('Path escapes allowed root')
    return candidate


def load_ready(root: Path, known_ids: set[str], published: set[str], limit: int) -> list[dict]:
    ready = []
    queue = root / CONTROL / 'reviewed'
    for file in sorted(queue.glob('*.json')):
        record = json_load(file)
        ident = record.get('id', '')
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]{1,80}', ident):
            raise ValueError('Invalid reviewed company identifier')
        if ident.casefold() in known_ids or ident in published: continue
        required = ('company', 'sector', 'problem', 'stage_summary', 'checked_on', 'reviewed_by', 'reviewed_on', 'markdown', 'markdown_sha256', 'sources')
        if any(not record.get(k) for k in required) or record.get('status') != 'reviewed':
            raise ValueError('Incomplete reviewed record: ' + ident)
        for key in ('checked_on', 'reviewed_on'):
            datetime.strptime(record[key], '%Y-%m-%d')
        manuscript = within(queue, record['markdown'])
        if manuscript.suffix != '.md' or not manuscript.is_file():
            raise ValueError('Reviewed manuscript is missing')
        data = manuscript.read_bytes()
        if digest(data) != record['markdown_sha256']:
            raise ValueError('Manuscript changed after review: ' + ident)
        body = data.decode('utf-8')
        if len(body) < 1500 or '**' in body or record['checked_on'] not in body:
            raise ValueError('Reviewed manuscript does not meet format requirements')
        target_name = record.get('filename', '')
        if '/' in target_name or '\\' in target_name or not re.fullmatch(r'[가-힣A-Za-z0-9·_-]+\.md', target_name):
            raise ValueError('Invalid manuscript output name')
        if ident.lower() not in target_name.lower() or not re.search('[가-힣]',target_name):
            raise ValueError('Output name must include Korean subject and company id')
        sources = record['sources']
        if len(sources) < 2 or len({canonical_url(s['url']) for s in sources}) < 2:
            raise ValueError('At least two primary sources are required')
        for source in sources:
            canonical_url(source['url'])
            if not source.get('title') or not re.fullmatch('[a-f0-9]{64}', source.get('reviewed_sha256','')):
                raise ValueError('Source review identity is missing')
            if source['url'] not in body:
                raise ValueError('Source is not cited by manuscript')
        item = dict(record, body=body, queue_record=file.relative_to(root).as_posix())
        ready.append(item)
        known_ids.add(ident.casefold())
        if len(ready) >= limit: break
    return ready


def verify_reviewed_sources(records: list[dict], fetcher=fetch):
    """A stale or unreachable reviewed source cannot silently authorize publication."""
    for record in records:
        for source in record['sources']:
            host = urlsplit(canonical_url(source['url'])).hostname
            snapshot = fetcher(source['url'], {host})
            if snapshot['sha256'] != source['reviewed_sha256']:
                raise ValueError('Source changed since review: ' + record['id'])


def append_before(text: str, marker: str, addition: str) -> str:
    if marker in text: return text.replace(marker, addition + '\n' + marker, 1)
    return text.rstrip() + '\n\n' + addition + '\n'


def prepare_publications(root: Path, output: Path, records: list[dict], day: str) -> list[str]:
    category = root / CATEGORY
    index = json_load(category/'기업목록_companies.json')
    readme = (category/'README.md').read_text(encoding='utf-8')
    sources = (category/'출처_sources.md').read_text(encoding='utf-8')
    log = (category/'조사기록_research-log.md').read_text(encoding='utf-8')
    paths = []
    tables=[]
    source_blocks=[]
    log_items=[]
    for r in records:
        automatic=r.get('entry_type')=='automated_analysis'
        rel=('자동분석_auto-research/'+day+'/' if automatic else '기업분석_companies/')+r['filename']
        destination=within(output/CATEGORY,rel)
        if (category/rel).exists(): raise ValueError('Refusing to replace an existing company analysis')
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(r['body'].encode('utf-8'))
        paths.append(CATEGORY+'/'+rel)
        index['entries'].append({k:r[k] for k in ('id','company','sector','checked_on','problem','stage_summary')} | {
            'entry_type':'automated_analysis' if automatic else 'company_analysis','path':rel,
            'sources':[{'title':s['title'],'url':s['url']} for s in r['sources']]})
        safe=lambda s: str(s).replace('|','·').replace('\n',' ')
        tables.append(f"| [{safe(r['company'])}]({rel}) | {safe(r['problem'])} | {safe(r['stage_summary'])} |")
        source_blocks.append(f"## {r['company']}\n\n[기술·사업 본문]({rel})\n\n"+'\n'.join(f"- [{s['title']}]({s['url']})" for s in r['sources']))
        log_items.append(f"- [{r['company']}]({rel}): {r['problem']}입니다.")
    index['updated_on']=day
    is_auto=any(r.get('entry_type')=='automated_analysis' for r in records)
    heading='자동 분석 · 사람 검토 전' if is_auto else '추가 분석'
    note='공개 원문을 로컬 모델로 분석하고 별도 모델 검토·형식 검사를 수행했습니다. 사람의 원문 대조나 독립 기관 검증과 구분합니다.\n\n' if is_auto else ''
    block=f'### {day} {heading}\n\n'+note+'| 기업과 본문 | 해결하려는 문제 | 공개된 현재 단계 |\n| --- | --- | --- |\n'+ '\n'.join(tables)+'\n'
    readme=append_before(readme,'## 창업 관점에서 읽는 경로',block)
    sources=append_before(sources,'[기업 목록으로]', '\n\n'.join(source_blocks))
    method='별도 모델 검토와 형식 검사를 통과한 자동 분석입니다. 사람의 원문 대조·독립 성능 검증과 구분하며 정확성을 보증하지 않습니다.' if is_auto else '사전에 원문과 본문을 대조한 분석입니다.'
    log=append_before(log,'[기업 목록으로]',f'## {day} · {heading}\n\n'+'\n'.join(log_items)+'\n\n'+method+' 직접 장비 실행·재무 실사를 수행한 기록은 아닙니다.\n')
    for filename,text in (('README.md',readme),('출처_sources.md',sources),('조사기록_research-log.md',log)):
        p=output/CATEGORY/filename
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(text.encode('utf-8'))
        paths.append(CATEGORY+'/'+filename)
    write_json(output/CATEGORY/'기업목록_companies.json',index)
    paths.append(CATEGORY+'/기업목록_companies.json')
    return paths


SHARED_HOSTS={'github.com','huggingface.co','arxiv.org','www.prnewswire.com','www.businesswire.com',
    'www.ycombinator.com','ycombinator.com','news.mit.edu','d2sf.naver.com','www.linkedin.com','linkedin.com',
    'developer.nvidia.com','nvidia.github.io','www.ces2026-humanoidmaxalliance.com','eopla.net','surge.peakxv.com'}


def normalized_company(value):
    return re.sub(r'[^a-z0-9가-힣]','',str(value).casefold())


def identity_sets(entries):
    names=set();hosts=set()
    for row in entries:
        names.update(normalized_company(row.get(k,'')) for k in ('id','company'))
        for source in row.get('sources',[]):
            try: host=urlsplit(canonical_url(source['url'])).hostname.removeprefix('www.')
            except (ValueError,KeyError): continue
            if host in {h.removeprefix('www.') for h in SHARED_HOSTS} or host.endswith(('.edu','.gov')):continue
            hosts.add(host)
    names.discard('')
    return names,hosts


def is_duplicate(candidate,names,hosts):
    if any(normalized_company(candidate.get(k,'')) in names for k in ('id','company')):return True
    candidate_hosts=[]
    for source in candidate.get('sources',[]):
        host=urlsplit(canonical_url(source['url'])).hostname.removeprefix('www.')
        if host in {h.removeprefix('www.') for h in SHARED_HOSTS} or host.endswith(('.edu','.gov')):continue
        candidate_hosts.append(host)
    return bool(set(candidate_hosts)&hosts)


def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--output',type=Path,default=Path('research-output'))
    parser.add_argument('--publish-ready',action='store_true')
    parser.add_argument('--limit',type=int,default=3,choices=(1,2,3))
    parser.add_argument('--auto-research',action='store_true')
    args=parser.parse_args(argv)
    root=args.root.resolve()
    output=args.output.resolve()
    output.mkdir(parents=True,exist_ok=True)
    config=json_load(root/CONTROL/'sources.json')
    state=json_load(root/CONTROL/'state.json',{'schema_version':1,'published_ids':[],'source_candidates':[]})
    day=datetime.now(KST).strftime('%Y-%m-%d')
    candidates={row['url']:row for row in state.get('source_candidates',[])}
    source_errors=[]
    new_count=0
    for source in config['sources']:
        try:
            doc=fetch(source['url'],set(source['allowed_hosts']))
            rows=extract_candidates(doc,source)
            for row in rows:
                if row['url'] not in candidates:
                    candidates[row['url']]=dict(row,first_seen_on=day,last_seen_on=day)
                    new_count+=1
                else: candidates[row['url']]['last_seen_on']=day
        except Exception as exc:
            source_errors.append({'source':source['url'],'error':type(exc).__name__})
    if not candidates and not args.auto_research:
        write_json(output/'result.json',{'status':'discovery_failed','source_errors':source_errors,'published':0})
        raise RuntimeError('No usable source candidates; see sanitized result artifact')
    existing_entries=json_load(root/CATEGORY/'기업목록_companies.json')['entries']
    known={r['id'].casefold() for r in existing_entries}
    known_names,known_hosts=identity_sets(existing_entries)
    records=load_ready(root,known,set(state.get('published_ids',[])),args.limit)
    verify_reviewed_sources(records)
    research_errors=[]
    if args.auto_research and len(records)<args.limit:
        from llm_research import research,propose_candidates
        registry=json_load(root/CONTROL/'research_candidates.json',{'companies':[]})
        attempts=state.setdefault('auto_attempts',{})
        def eligible(c):
            if c.get('id','').casefold() in known or is_duplicate(c,known_names,known_hosts):return False
            last=attempts.get(c.get('id'),{}).get('last_attempt_on')
            return not last or (datetime.strptime(day,'%Y-%m-%d')-datetime.strptime(last,'%Y-%m-%d')).days>=7
        available=[c for c in registry['companies'] if eligible(c)]
        automatic=[]
        dynamic_added=False
        attempted=0
        while len(automatic)+len(records)<args.limit and attempted<args.limit+2:
            if not available and not dynamic_added:
                discovered=sorted(candidates.values(),key=lambda r:(r.get('first_seen_on',''),r['url']),reverse=True)
                proposals,proposal_errors=propose_candidates(discovered,set(known)|{k.casefold() for k,v in attempts.items() if v.get('last_attempt_on')==day},limit=args.limit-len(records)-len(automatic))
                available.extend(c for c in proposals if eligible(c))
                research_errors.extend(proposal_errors)
                dynamic_added=True
            if not available: break
            candidate=available.pop(0)
            if not eligible(candidate):continue
            attempted+=1
            prior=attempts.get(candidate['id'],{}).get('attempts',0)
            try:
                record,audit=research(candidate,checked_on=day)
                automatic.append(record)
                known.add(record['id'].casefold())
                new_names,new_hosts=identity_sets([record]);known_names.update(new_names);known_hosts.update(new_hosts)
                attempts[candidate['id']]={'attempts':prior+1,'last_attempt_on':day,'status':'passed_model_review'}
                write_json(output/'audits'/(record['id']+'.json'),audit)
            except Exception as exc:
                attempts[candidate['id']]={'attempts':prior+1,'last_attempt_on':day,'status':'rejected','reason':str(exc)[:220]}
                research_errors.append({'company_id':candidate.get('id'),'error':type(exc).__name__,'reason':str(exc)[:220]})
                if getattr(exc,'audit',None):
                    write_json(output/'audits'/(candidate['id']+'.rejected.json'),exc.audit)
        records.extend(automatic)
    status='ready_to_publish' if records else 'needs_review'
    paths=[]
    if records and args.publish_ready:
        paths=prepare_publications(root,output,records,day)
        state['published_ids']=sorted(set(state.get('published_ids',[]))|{r['id'] for r in records})
        status='prepared_reviewed_publications'
    state['source_candidates']=sorted(candidates.values(),key=lambda r:(r.get('last_seen_on',''),r['url']),reverse=True)[:MAX_CANDIDATES]
    state['last_checked_on']=day
    state['last_status']=status
    write_json(output/CONTROL/'state.json',state)
    paths.append(CONTROL+'/state.json')
    result={'status':status,'new_source_candidates':new_count,'source_candidates':len(candidates),
            'reviewed_ready':len(records),'prepared_analyses':len(records) if args.publish_ready else 0,
            'source_errors':source_errors,'research_errors':research_errors,'checked_on':day,
            'human_reviewed':False if args.auto_research else None,
            'limitation':'Local-model source-grounded analysis uses a separate model review, not human fact-checking or independent validation. Insufficient drafts are not published.' if args.auto_research else 'This keyless workflow discovers sources and publishes previously reviewed analyses. It does not generate or claim autonomous new research.'}
    write_json(output/'result.json',result)
    base_hashes={path:digest((root/path).read_bytes()) if (root/path).is_file() else None for path in paths}
    write_json(output/'manifest.json',{'paths':paths,'base_sha256':base_hashes})
    summary=os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary,'a',encoding='utf-8') as f:
            f.write(f"## 신생기업 자료 확인\n\n- 상태: `{status}`\n- 새 원문 후보: {new_count}\n- 본문 준비: {result['prepared_analyses']}\n- 자동 분석 여부: {args.auto_research}\n\n{result['limitation']}\n")
    print(json.dumps({k:v for k,v in result.items() if k!='source_errors'},ensure_ascii=False))
    if args.auto_research and not records:
        print('No automatic draft passed the evidence and review gates',file=sys.stderr)
        return 2
    return 0


if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as exc:
        print('Pipeline stopped: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
