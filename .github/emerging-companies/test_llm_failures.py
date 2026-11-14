"""Regression checks for proposal filenames and source/model failure outcomes."""
import copy
import os
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

    def test_invented_url_path_and_english_topic_stay_rejected(self):
        for changed in ({'homepage_url':'https://invented.example/'},{'topic':'센서/설계'},{'topic':'robot-automation'}):
            with self.subTest(changed=changed):
                proposal=dict(self.proposal,**changed)
                rows,errors=llm.propose_candidates(self.discovered,set(),fetcher=self.source_fetch,completion=Mock(return_value=proposal),limit=1)
                self.assertEqual(rows,[])
                self.assertEqual(len(errors),1)
                self.assertEqual(errors[0]['kind'],'proposal_rejected')
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
