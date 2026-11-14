"""Regression checks for proposal filenames and source/model failure outcomes."""
import copy
import io
import json
import os
import re
import unittest
from unittest.mock import Mock, patch

import llm_research as llm
import test_pipeline as fixtures


class FilenameTopicTests(unittest.TestCase):
    def test_short_korean_and_ordinary_spaces_are_safe(self):
        for value,expected in (('센서','센서'),('로봇 작업 자동화','로봇_작업_자동화'),('  센서  데이터 분석  ','센서_데이터_분석'),('가'*60,'가'*60)):
            with self.subTest(value=value):self.assertEqual(llm.filename_topic(value),expected)

    def test_paths_controls_english_only_and_length_are_rejected(self):
        for value in ('센서/설계','센서\\설계','../센서','센서:설계','센서\n설계','센서\t설계','sensor-only','가','가'*61):
            with self.subTest(value=value),self.assertRaises(ValueError):llm.filename_topic(value)


class ProposalRegressionTests(unittest.TestCase):
    def setUp(self):
        self.discovered=[{'url':'https://institution.example/company-story','title':'Institution company story'}]
        self.homepage='https://robot.example/'
        self.proposal={'is_company_candidate':True,'id':'Example-Robot','company':'Example Robot',
                       'topic':'로봇 작업 자동화','sector':'로봇','homepage_url':self.homepage}

    def source_fetch(self,url,allowed):
        return {'url':url,'sha256':'a'*64,
                'text':'<main><h1>Company introduction</h1><p>'+('Public company source text. '*30)+'</p><a href="'+self.homepage+'">Company website</a></main>'}

    def test_short_and_spaced_topics_create_candidates_using_linked_url(self):
        for value,expected in (('센서','센서'),('로봇 작업 자동화','로봇_작업_자동화')):
            with self.subTest(topic=value):
                proposal=dict(self.proposal,topic=value)
                rows,errors=llm.propose_candidates(self.discovered,set(),fetcher=self.source_fetch,completion=Mock(return_value=proposal),limit=1)
                self.assertEqual(errors,[])
                self.assertEqual(len(rows),1)
                self.assertEqual(rows[0]['topic'],expected)
                self.assertEqual(rows[0]['sources'][1]['url'],self.homepage)
                self.assertEqual(rows[0]['allowed_hosts'],['institution.example','robot.example'])

    def test_unlinked_url_and_invalid_model_fields_have_distinct_outcomes(self):
        cases=(({'homepage_url':'https://invented.example/'},'proposal_rejected'),
               ({'topic':'센서/설계'},'model_format_error'),
               ({'topic':'robot collaboration in manufacturing'},'model_format_error'),
               ({'id':'Example Robot'},'model_format_error'),
               ({'sector':[]},'model_format_error'),
               ({'sector':'robotics'},'model_format_error'))
        for changed,kind in cases:
            with self.subTest(changed=changed):
                proposal=dict(self.proposal,**changed)
                rows,errors=llm.propose_candidates(self.discovered,set(),fetcher=self.source_fetch,completion=Mock(return_value=proposal),limit=1)
                self.assertEqual(rows,[])
                self.assertEqual(len(errors),1)
                self.assertEqual(errors[0]['kind'],kind)
                self.assertEqual(errors[0]['stage'],'validating_proposal')

    def test_proposal_source_and_model_timeouts_keep_distinct_stages(self):
        source_error=Mock(side_effect=TimeoutError('source timed out'))
        completion=Mock(return_value=self.proposal)
        rows,errors=llm.propose_candidates(self.discovered,set(),fetcher=source_error,completion=completion,limit=1)
        self.assertEqual(rows,[])
        self.assertEqual((errors[0]['kind'],errors[0]['stage']),('source_unavailable','fetching_source'))
        completion.assert_not_called()
        rows,errors=llm.propose_candidates(self.discovered,set(),fetcher=self.source_fetch,completion=Mock(side_effect=TimeoutError('model timed out')),limit=1)
        self.assertEqual(rows,[])
        self.assertEqual((errors[0]['kind'],errors[0]['stage']),('runtime_error','proposing'))

    def test_malformed_cached_candidate_is_an_internal_error(self):
        fetcher=Mock()
        completion=Mock()
        rows,errors=llm.propose_candidates([{'title':'Missing cached URL'}],set(),
            fetcher=fetcher,completion=completion,limit=1)
        self.assertEqual(rows,[])
        self.assertEqual(len(errors),1)
        self.assertEqual((errors[0]['kind'],errors[0]['stage']),('internal_error','fetching_source'))
        fetcher.assert_not_called()
        completion.assert_not_called()


class LocalCompletionContractTests(unittest.TestCase):
    endpoint='http://127.0.0.1:8080/v1/chat/completions'

    def test_malformed_envelope_invalid_json_and_truncation_are_model_output_errors(self):
        cases=(b'not JSON',b'{"choices":[]}',
               json.dumps({'choices':[{'message':{'content':'{"invalid":'},'finish_reason':'stop'}]}).encode(),
               json.dumps({'choices':[{'message':{'content':'{}'},'finish_reason':'length'}]}).encode())
        for raw in cases:
            with self.subTest(raw=raw),patch.object(llm,'urlopen',return_value=io.BytesIO(raw)):
                with self.assertRaises(llm.ModelOutputError):
                    llm.local_completion('한국어 JSON을 반환합니다.',{},llm.PROPOSAL_SCHEMA,endpoint=self.endpoint)

    def test_serialized_proposal_contract_blocks_observed_english_title(self):
        proposal={'is_company_candidate':True,'id':'Example-Robot','company':'Example Robot',
                  'topic':'로봇 작업 자동화','sector':'로봇','homepage_url':'https://robot.example/'}
        raw=json.dumps({'choices':[{'message':{'content':json.dumps(proposal,ensure_ascii=False)},'finish_reason':'stop'}]}).encode()
        with patch.object(llm,'urlopen',return_value=io.BytesIO(raw)) as request:
            result=llm.local_completion('한국어 JSON을 반환합니다.',{'source_text':'Untrusted source text'},llm.PROPOSAL_SCHEMA,endpoint=self.endpoint)
        self.assertEqual(result,proposal)
        sent=request.call_args.args[0]
        self.assertEqual(sent.full_url,self.endpoint)
        body=json.loads(sent.data)
        schema=body['response_format']['json_schema']['schema']
        topic_pattern=schema['properties']['topic']['pattern']
        self.assertIsNotNone(re.fullmatch(topic_pattern,proposal['topic']))
        self.assertIsNone(re.fullmatch(topic_pattern,'robot collaboration in manufacturing'))
        self.assertIsNone(re.fullmatch(schema['properties']['id']['pattern'],'Example Robot'))
        self.assertFalse(body['chat_template_kwargs']['enable_thinking'])
        self.assertTrue(body['messages'][0]['content'].endswith('/no_think'))


class ResearchFailureTests(unittest.TestCase):
    def setUp(self):
        # Compose the existing fixture without importing its TestCase into discovery.
        fixture=fixtures.GroundingTests('test_exact_evidence_is_required')
        fixture.setUp()
        self.documents=copy.deepcopy(fixture.documents)
        self.draft=copy.deepcopy(fixture.draft)
        self.candidate={'id':'Example','company':'Example','topic':'센서데이터수집기','sector':'센서',
                        'allowed_hosts':['example.com','institution.example'],
                        'sources':[{'url':doc['url'],'title':doc['title']} for doc in self.documents]}

    def source_fetch(self,url,allowed):
        doc=next(doc for doc in self.documents if doc['url']==url)
        return {'url':url,'sha256':doc['reviewed_sha256'],'text':'<main>'+doc['text']+'</main>'}

    def test_generation_and_review_timeouts_are_runtime_errors(self):
        for stage,outputs in (('generating',[TimeoutError('model timed out')]),('second_model_review',[self.draft,TimeoutError('review timed out')])):
            with self.subTest(stage=stage),patch.object(llm,'render') as render:
                with self.assertRaises(llm.ResearchUnavailable) as caught:
                    llm.research(self.candidate,fetcher=self.source_fetch,completion=Mock(side_effect=outputs),checked_on='2026-11-15')
                self.assertEqual(caught.exception.audit['status'],'runtime_error')
                self.assertEqual(caught.exception.audit['stage'],stage)
                render.assert_not_called()

    def test_invalid_model_endpoint_is_runtime_configuration_failure(self):
        with patch.dict(os.environ,{'LOCAL_MODEL_ENDPOINT':'https://remote.example/completions'}), \
             patch.object(llm,'urlopen') as request,patch.object(llm,'render') as render:
            with self.assertRaises(llm.ResearchUnavailable) as caught:
                llm.research(self.candidate,fetcher=self.source_fetch,checked_on='2026-11-15')
        self.assertEqual(caught.exception.audit['status'],'runtime_error')
        self.assertEqual(caught.exception.audit['stage'],'generating')
        self.assertIn('fixed loopback',str(caught.exception))
        request.assert_not_called()
        render.assert_not_called()

    def test_source_timeout_is_source_unavailable_without_model_call(self):
        completion=Mock()
        with self.assertRaises(llm.ResearchRejected) as caught:
            llm.research(self.candidate,fetcher=Mock(side_effect=TimeoutError('source timed out')),completion=completion,checked_on='2026-11-15')
        self.assertEqual(caught.exception.audit['status'],'source_unavailable')
        self.assertEqual(caught.exception.audit['stage'],'fetching_sources')
        completion.assert_not_called()

    def test_generation_and_review_format_failures_are_not_content_rejections(self):
        for stage,outputs in (('generating',[llm.ModelOutputError('Invalid structured model response envelope')]),
                              ('second_model_review',[self.draft,llm.ModelOutputError('Model returned invalid JSON')])):
            with self.subTest(stage=stage),patch.object(llm,'render') as render:
                with self.assertRaises(llm.ResearchUnavailable) as caught:
                    llm.research(self.candidate,fetcher=self.source_fetch,completion=Mock(side_effect=outputs),checked_on='2026-11-15')
                self.assertEqual(caught.exception.audit['status'],'model_format_error')
                self.assertEqual(caught.exception.audit['stage'],stage)
                render.assert_not_called()

    def test_english_prose_wrong_field_type_and_missing_keys_are_format_errors(self):
        english=copy.deepcopy(self.draft)
        english['summary']='Robot collaboration in manufacturing.'
        wrong_type=copy.deepcopy(self.draft)
        wrong_type['facts'][0]['label']=42
        missing_key=copy.deepcopy(self.draft)
        del missing_key['business_analysis']
        for draft in (english,wrong_type,missing_key):
            with self.subTest(draft=draft),patch.object(llm,'render') as render:
                completion=Mock(return_value=draft)
                with self.assertRaises(llm.ResearchUnavailable) as caught:
                    llm.research(self.candidate,fetcher=self.source_fetch,completion=completion,checked_on='2026-11-15')
                self.assertEqual(caught.exception.audit['status'],'model_format_error')
                self.assertEqual(caught.exception.audit['stage'],'deterministic_evidence_checks')
                completion.assert_called_once()
                render.assert_not_called()

    def test_evidence_mismatch_remains_rejected_without_article(self):
        draft=copy.deepcopy(self.draft)
        draft['facts'][0]['evidence'][0]['quote']='This quotation was invented and is not present.'
        completion=Mock(return_value=draft)
        with patch.object(llm,'render') as render:
            with self.assertRaises(llm.ResearchRejected) as caught:
                llm.research(self.candidate,fetcher=self.source_fetch,completion=completion,checked_on='2026-11-15')
            self.assertEqual(caught.exception.audit['status'],'rejected')
            self.assertEqual(caught.exception.audit['stage'],'deterministic_evidence_checks')
            self.assertIn('quote is not present',str(caught.exception))
            completion.assert_called_once()
            render.assert_not_called()

    def test_unexpected_program_error_is_not_a_content_rejection(self):
        with self.assertRaises(llm.ResearchUnavailable) as caught:
            llm.research(self.candidate,fetcher=self.source_fetch,completion=Mock(side_effect=RuntimeError('unexpected worker failure')),checked_on='2026-11-15')
        self.assertEqual(caught.exception.audit['status'],'internal_error')
        self.assertEqual(caught.exception.audit['stage'],'generating')


if __name__=='__main__':unittest.main()
