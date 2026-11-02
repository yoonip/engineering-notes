import copy
import importlib.util
import json
from pathlib import Path
import socket
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).parent))
import pipeline as p
import llm_research as llm
import publish


class SourceSecurityTests(unittest.TestCase):
    def test_private_and_credential_urls_are_rejected(self):
        for url in ('http://example.com/','https://127.0.0.1/','https://10.0.0.1/','https://[::1]/','https://user:pass@example.com/','https://example.com:8080/','https://metadata.google.internal/'):
            with self.subTest(url=url),self.assertRaises(ValueError): p.canonical_url(url)

    def test_private_dns_and_cross_domain_redirect_are_rejected(self):
        with patch.object(socket,'getaddrinfo',return_value=[(2,1,6,'',('127.0.0.1',443))]):
            with self.assertRaises(ValueError): p.validate_destination('https://public.example/',{'public.example'})
        with self.assertRaises(ValueError): p.validate_destination('https://other.example/',{'public.example'})

    def test_feed_deduplicates_and_rejects_external_entities(self):
        source={'kind':'rss','allowed_hosts':['news.example'],'label':'Institution','url':'https://news.example/feed'}
        xml='<rss><channel><item><title>A</title><link>https://news.example/a</link></item><item><title>A2</title><link>https://news.example/a#x</link></item></channel></rss>'
        rows=p.extract_candidates({'url':source['url'],'text':xml},source)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['status'],'unreviewed_source_candidate')
        with self.assertRaises(ValueError): p.extract_candidates({'url':source['url'],'text':'<!DOCTYPE rss><rss/>'},source)

    def test_source_text_prefers_main_and_removes_script(self):
        parser=p.PageParser(); parser.feed('<nav>noise</nav><main><h1>Product</h1><script>danger</script><p>Evidence text</p></main><footer>tail</footer>')
        self.assertEqual(parser.main_text,['Product','Evidence text'])

    def test_path_and_scope_guards(self):
        folder=Path(__file__).parent/'test-root'
        with self.assertRaises(ValueError): p.within(folder,'../outside.md')
        self.assertFalse(publish.allowed('README.md'))
        self.assertFalse(publish.allowed('.github/workflows/evil.yml'))
        self.assertFalse(publish.allowed(p.CATEGORY+'/자동분석_auto-research/../../README.md'))
        self.assertTrue(publish.allowed(p.CATEGORY+'/자동분석_auto-research/2026-11-02/기업_Example.md'))

    def test_company_name_and_domain_deduplication(self):
        entries=[{'id':'Example-Company','company':'Example Company','sources':[{'url':'https://www.example.com/product'},{'url':'https://www.ycombinator.com/companies/example'}]}]
        names,hosts=p.identity_sets(entries)
        self.assertTrue(p.is_duplicate({'id':'New-ID','company':'EXAMPLE COMPANY','sources':[]},names,hosts))
        self.assertTrue(p.is_duplicate({'id':'Other','company':'Other','sources':[{'url':'https://example.com/about'}]},names,hosts))
        self.assertFalse(p.is_duplicate({'id':'Another','company':'Another','sources':[{'url':'https://www.ycombinator.com/companies/another'}]},names,hosts))


class GroundingTests(unittest.TestCase):
    def setUp(self):
        self.documents=[{'source_id':'S1','title':'Official product','url':'https://example.com/product','text':'The company makes a test sensor for factory data collection. '+('source context '*40),'reviewed_sha256':'a'*64},
            {'source_id':'S2','title':'Institution','url':'https://institution.example/company','text':'The project is a pilot rather than a full commercial deployment. '+('institution context '*40),'reviewed_sha256':'b'*64}]
        prose='공개 자료가 설명하는 제품과 시험 범위는 제한된 작업에서 센서 데이터를 기록하는 방식입니다. 원문이 밝힌 기능을 전체 산업에서 검증된 성능으로 해석하지 않습니다.'
        self.draft={'eligible':True,'eligibility_reason':'파일럿 단계의 기술기업이라는 근거를 확인합니다.','summary':'현장의 데이터 수집을 다루는 전문 기술기업입니다.',
            'facts':[{'label':'기술과 제품','explanation':prose,'evidence':[{'source_id':'S1' if i%2==0 else 'S2','quote':'The company makes a test sensor' if i%2==0 else 'The project is a pilot'}]} for i in range(4)],
            'unknowns':['현재 확정 매출은 확인하지 못했습니다.','고객의 재구매 실적은 확인하지 못했습니다.'],
            'business_analysis':'사업 구조에 대한 분석으로는 수집 장비와 운영 지원을 결합할 수 있습니다. 계약 단가와 비용 구조는 원문에 공개되지 않았으므로 추정하지 않습니다.',
            'risks':'경쟁 대안은 고객이 기존 도구와 자체 인력으로 처리하는 방식입니다. 제품의 작동뿐 아니라 설치와 유지에 필요한 노력을 비교해야 합니다.',
            'learning':'Python으로 공개된 센서 기록을 읽고 누락과 시간 간격을 확인하는 실험을 제안합니다. 실제 제품의 성능 재현과 구분합니다.',
            'next_checks':'다음에는 실제 고객의 사용 범위와 반복 운전의 결과를 확인해야 합니다.'}

    def test_exact_evidence_is_required(self):
        llm.validate_draft(self.draft,self.documents)
        bad=copy.deepcopy(self.draft);bad['facts'][0]['evidence'][0]['quote']='This is an invented quote that does not exist.'
        with self.assertRaises(ValueError): llm.validate_draft(bad,self.documents)

    def test_unknown_numbers_urls_and_missing_source_are_rejected(self):
        for mutate in ('number','url','source'):
            bad=copy.deepcopy(self.draft)
            if mutate=='number':bad['facts'][0]['explanation']+=' 매출은 123456달러입니다.'
            if mutate=='url':bad['risks']+=' https://bad.example/'
            if mutate=='source':
                for fact in bad['facts']:fact['evidence']=copy.deepcopy(self.draft['facts'][0]['evidence'])
            with self.subTest(mutate=mutate),self.assertRaises(ValueError):llm.validate_draft(bad,self.documents)

    def test_inference_endpoint_is_loopback_only(self):
        with self.assertRaises(ValueError):llm.local_completion('x',{},llm.REVIEW_SCHEMA,endpoint='https://api.example/completions')

    def test_second_pass_rejection_prevents_article(self):
        candidate={'id':'Example','company':'Example','topic':'센서데이터수집기','sector':'센서','allowed_hosts':['example.com','institution.example'],
            'sources':[{'url':'https://example.com/product','title':'Product'},{'url':'https://institution.example/company','title':'Institution'}]}
        def source_fetch(url,allowed):
            doc=next(s for s in self.documents if s['url']==url)
            return {'url':url,'sha256':doc['reviewed_sha256'],'text':'<main>'+doc['text']+'</main>'}
        results=iter([self.draft,{'approved':False,'issues':['Unsupported generalization']}])
        with self.assertRaisesRegex(ValueError,'Second model'):
            llm.research(candidate,fetcher=source_fetch,completion=lambda *args:next(results),checked_on='2026-11-02')

    def test_changed_reviewed_source_blocks_publication(self):
        records=[{'id':'Example','sources':[{'url':'https://example.com/','reviewed_sha256':'a'*64}]}]
        with self.assertRaisesRegex(ValueError,'Source changed'):
            p.verify_reviewed_sources(records,fetcher=lambda *args:{'sha256':'b'*64})

    def test_number_in_unrelated_source_text_does_not_ground_a_claim(self):
        documents=copy.deepcopy(self.documents);documents[0]['text']+=' 123456'
        draft=copy.deepcopy(self.draft);draft['facts'][0]['explanation']+=' 매출은 123456달러입니다.'
        with self.assertRaises(ValueError):llm.validate_draft(draft,documents)

    def test_rejection_audit_keeps_draft_but_not_source_full_text(self):
        candidate={'id':'Example','company':'Example','topic':'센서데이터수집기','sector':'센서','allowed_hosts':['example.com','institution.example'],
            'sources':[{'url':'https://example.com/product','title':'Product'},{'url':'https://institution.example/company','title':'Institution'}]}
        def source_fetch(url,allowed):
            doc=next(s for s in self.documents if s['url']==url)
            return {'url':url,'sha256':doc['reviewed_sha256'],'text':'<main>'+doc['text']+'</main>'}
        bad=copy.deepcopy(self.draft);bad['facts'][0]['evidence'][0]['quote']='A fabricated quotation which does not exist.'
        with self.assertRaises(llm.ResearchRejected) as error:
            llm.research(candidate,fetcher=source_fetch,completion=lambda *args:bad,checked_on='2026-11-02')
        self.assertIn('draft',error.exception.audit)
        self.assertEqual(error.exception.audit['stage'],'deterministic_evidence_checks')
        self.assertNotIn('text',error.exception.audit['sources'][0])

    def test_auto_render_is_explicitly_not_human_reviewed(self):
        draft=copy.deepcopy(self.draft)
        draft['facts'].extend(copy.deepcopy(draft['facts'][:2]))
        draft['learning']+=' 첫 결과물에는 표본 번호와 기록 시각, 장치 설정, 누락 여부를 함께 남겨야 합니다. 작업을 반복해 값이 얼마나 달라지는지 비교하고, 환경을 바꿨을 때 오류가 생기는 조건을 따로 기록할 수 있습니다. 데이터를 공개할 때에는 이용 조건과 개인 정보가 포함되는지 확인하는 과정도 필요합니다. 센서를 직접 연결하기 전에 공개된 기록으로 같은 분석을 수행하면 측정과 해석의 차이를 익힐 수 있습니다.'
        body=llm.render({'topic':'센서데이터수집기','company':'Example'},draft,self.documents,'2026-11-02')
        self.assertIn('사람이 원문 전체를 대조한 글',body)
        self.assertIn('(../../README.md)',body)


if __name__=='__main__':unittest.main()
