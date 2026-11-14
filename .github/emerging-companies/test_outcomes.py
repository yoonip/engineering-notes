"""Regression checks for publication holds versus actual execution failures."""
import contextlib
from datetime import datetime, timedelta
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).parent))
import pipeline as p
import llm_research as llm


class RunOutcomeTests(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root=Path(self.temporary.name)/'root'
        self.output=Path(self.temporary.name)/'output'
        self.day=datetime.now(p.KST).strftime('%Y-%m-%d')
        self.candidate={'id':'Example','company':'Example','sources':[]}
        self.write(p.CONTROL+'/sources.json',{'sources':[{
            'url':'https://institution.example/feed','allowed_hosts':['institution.example']}]})
        self.write(p.CONTROL+'/state.json',{'schema_version':1,'published_ids':[],'source_candidates':[]})
        self.write(p.CONTROL+'/research_candidates.json',{'companies':[self.candidate]})
        self.write(p.CATEGORY+'/기업목록_companies.json',{'entries':[]})

    def write(self,path,value):
        target=self.root/path
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(value),encoding='utf-8')

    def run_pipeline(self,*,research=None,proposals=None,fetch_error=None,limit=1):
        kwargs={'side_effect':fetch_error} if fetch_error else {'return_value':{'text':'source'}}
        with patch.object(p,'fetch',**kwargs),patch.object(p,'extract_candidates',return_value=[]), \
             patch.object(p,'load_ready',return_value=[]),patch.object(p,'verify_reviewed_sources'), \
             patch.object(p,'prepare_publications',return_value=[]) as prepare, \
             patch.object(llm,'research',side_effect=research) as runner, \
             patch.object(llm,'propose_candidates',return_value=proposals or ([],[])) as proposer, \
             patch.dict(os.environ,{'GITHUB_STEP_SUMMARY':str(self.output/'summary.md')}), \
             contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            exit_code=p.main(['--root',str(self.root),'--output',str(self.output),
                '--auto-research','--publish-ready','--limit',str(limit)])
        result=json.loads((self.output/'result.json').read_text(encoding='utf-8'))
        state=json.loads((self.output/p.CONTROL/'state.json').read_text(encoding='utf-8'))
        manifest=json.loads((self.output/'manifest.json').read_text(encoding='utf-8'))
        self.proposer=proposer
        self.assertIn(p.CONTROL+'/state.json',manifest['paths'])
        self.assertEqual(state['last_status'],result['status'])
        return exit_code,result,state,runner,prepare

    def test_all_candidates_in_cooldown_is_successful_state_only_run(self):
        self.write(p.CONTROL+'/state.json',{'published_ids':[],'source_candidates':[],
            'auto_attempts':{'Example':{'last_attempt_on':self.day,'status':'rejected'}}})
        code,result,state,runner,prepare=self.run_pipeline()
        self.assertEqual(code,0)
        self.assertEqual(result['status'],'no_eligible_candidates')
        self.assertEqual(result['publication_outcome'],'state_only')
        self.assertEqual(result['attempted_analyses'],0)
        runner.assert_not_called();prepare.assert_not_called()

    def test_quality_rejection_keeps_audit_and_succeeds_without_article(self):
        rejection=llm.ResearchRejected('Evidence quote missing',{'status':'rejected','stage':'evidence'})
        code,result,state,runner,prepare=self.run_pipeline(research=rejection)
        self.assertEqual(code,0)
        self.assertEqual(result['status'],'no_publishable_analysis')
        self.assertEqual(state['auto_attempts']['Example']['status'],'rejected')
        self.assertTrue((self.output/'audits/Example.rejected.json').is_file())
        self.assertEqual(result['prepared_analyses'],0)
        prepare.assert_not_called()

    def test_model_outage_is_failure_with_short_retry_and_no_article(self):
        outage=RuntimeError('Local inference server unavailable')
        outage.audit={'status':'runtime_error','stage':'generating'}
        code,result,state,runner,prepare=self.run_pipeline(research=outage)
        self.assertEqual(code,1)
        self.assertEqual(result['status'],'operational_failure')
        self.assertEqual(state['auto_attempts']['Example']['status'],'runtime_error')
        self.assertTrue((self.output/'audits/Example.runtime_error.json').is_file())
        prepare.assert_not_called()

    def test_unusable_model_output_is_failure_and_not_quality_hold(self):
        failure=RuntimeError('Model output has no usable Korean topic')
        failure.audit={'status':'model_format_error','stage':'generating'}
        code,result,state,runner,prepare=self.run_pipeline(research=failure)
        self.assertEqual(code,1)
        self.assertEqual(result['status'],'operational_failure')
        self.assertEqual(result['execution_outcome'],'failed')
        self.assertEqual(result['operational_error_count'],1)
        self.assertEqual(state['auto_attempts']['Example']['status'],'model_format_error')
        self.assertTrue((self.output/'audits/Example.model_format_error.json').is_file())
        prepare.assert_not_called()

    def test_all_proposal_format_errors_are_not_successful_empty_run(self):
        self.write(p.CONTROL+'/research_candidates.json',{'companies':[]})
        code,result,*_=self.run_pipeline(proposals=([],[{
            'kind':'model_format_error','stage':'validating_proposal','reason':'invalid topic'}]))
        self.assertEqual(code,1)
        self.assertEqual(result['status'],'operational_failure')
        self.assertEqual(result['operational_error_count'],1)

    def test_all_discovery_sources_down_is_failure_even_with_cached_candidates(self):
        self.write(p.CONTROL+'/research_candidates.json',{'companies':[]})
        self.write(p.CONTROL+'/state.json',{'source_candidates':[{
            'url':'https://institution.example/old','title':'Old source'}]})
        code,result,state,runner,prepare=self.run_pipeline(fetch_error=TimeoutError('source timeout'))
        self.assertEqual(code,1)
        self.assertEqual(result['status'],'discovery_failed')
        self.assertEqual(result['successful_source_checks'],0)
        self.assertEqual(result['prepared_analyses'],0)

    def test_proposal_model_error_is_failure_not_content_rejection(self):
        self.write(p.CONTROL+'/research_candidates.json',{'companies':[]})
        code,result,*_=self.run_pipeline(proposals=([],[{'kind':'runtime_error','reason':'connection refused'}]))
        self.assertEqual(code,1)
        self.assertEqual(result['status'],'operational_failure')

    def test_unexpected_research_bug_is_not_hidden(self):
        code,result,state,*_=self.run_pipeline(research=KeyError('missing field'))
        self.assertEqual(code,1)
        self.assertEqual(result['status'],'operational_failure')
        self.assertEqual(state['auto_attempts']['Example']['status'],'internal_error')

    def test_only_accepted_records_are_prepared_when_another_is_rejected(self):
        self.write(p.CONTROL+'/research_candidates.json',{'companies':[
            self.candidate,{'id':'Accepted','company':'Accepted','sources':[]}]})
        record={'id':'Accepted','company':'Accepted','sources':[]}
        reject=llm.ResearchRejected('evidence missing',{'status':'rejected'})
        code,result,state,runner,prepare=self.run_pipeline(limit=2,research=[reject,(record,{'status':'passed_model_review'})])
        self.assertEqual(code,0)
        self.assertEqual(result['prepared_analyses'],1)
        self.assertEqual(result['attempted_analyses'],2)
        self.assertEqual(result['publication_outcome'],'articles_prepared')
        self.assertEqual(state['published_ids'],['Accepted'])
        self.assertEqual(prepare.call_args.args[2],[record])

    def test_accepted_article_with_other_model_failure_is_explicit_partial_success(self):
        self.write(p.CONTROL+'/research_candidates.json',{'companies':[
            self.candidate,{'id':'Accepted','company':'Accepted','sources':[]}]})
        record={'id':'Accepted','company':'Accepted','sources':[]}
        failure=RuntimeError('Malformed model output')
        failure.audit={'status':'model_format_error','stage':'generating'}
        code,result,state,runner,prepare=self.run_pipeline(limit=2,research=[failure,(record,{'status':'passed_model_review'})])
        self.assertEqual(code,0)
        self.assertEqual(result['prepared_analyses'],1)
        self.assertEqual(result['operational_error_count'],1)
        self.assertEqual(result['execution_outcome'],'partial_success')
        self.assertEqual(state['last_execution_outcome'],'partial_success')
        self.assertEqual(state['last_operational_error_count'],1)
        self.assertEqual(state['published_ids'],['Accepted'])
        self.assertEqual(prepare.call_args.args[2],[record])
        self.assertIn('실행 오류: 1건',(self.output/'summary.md').read_text(encoding='utf-8'))

    def test_transient_retry_is_next_day_while_quality_retry_waits_week(self):
        yesterday=(datetime.strptime(self.day,'%Y-%m-%d')-timedelta(days=1)).strftime('%Y-%m-%d')
        for status in ('runtime_error','model_format_error','source_unavailable','internal_error'):
            self.assertTrue(p.retry_due({'last_attempt_on':yesterday,'status':status},self.day))
            self.assertFalse(p.retry_due({'last_attempt_on':self.day,'status':status},self.day))
        self.assertFalse(p.retry_due({'last_attempt_on':yesterday,'status':'rejected'},self.day))

    def test_old_size_limit_rejection_retries_same_day_after_cap_change(self):
        attempt={'last_attempt_on':self.day,'status':'rejected','reason':'Source exceeds byte limit'}
        with patch.object(p,'MAX_BYTES',2_000_000):
            # Legacy entries without a recorded limit were checked under one megabyte.
            self.assertTrue(p.retry_due(attempt,self.day))
            self.assertTrue(p.retry_due(dict(attempt,source_byte_limit=1_000_000),self.day))

    def test_size_rejection_under_current_cap_does_not_retry_same_day(self):
        with patch.object(p,'MAX_BYTES',2_000_000):
            attempt={'last_attempt_on':self.day,'status':'source_unavailable',
                     'reason':'Source exceeds byte limit','source_byte_limit':2_000_000}
            self.assertFalse(p.retry_due(attempt,self.day))
            # Reducing the cap also does not make the same document newly eligible.
            self.assertFalse(p.retry_due(dict(attempt,source_byte_limit=3_000_000),self.day))

    def test_cap_change_does_not_bypass_other_quality_rejection(self):
        with patch.object(p,'MAX_BYTES',2_000_000):
            for reason in ('Evidence quote missing','Second model pass rejected the draft',
                           'Source exceeds byte limit and evidence is missing'):
                attempt={'last_attempt_on':self.day,'status':'rejected',
                         'reason':reason,'source_byte_limit':1_000_000}
                with self.subTest(reason=reason):self.assertFalse(p.retry_due(attempt,self.day))

    def test_source_limit_failure_retains_audit_and_current_limit_for_short_retry(self):
        failure=llm.ResearchRejected('Source exceeds byte limit',{
            'status':'source_unavailable','stage':'fetching_sources','reason':'Source exceeds byte limit'})
        with patch.object(p,'MAX_BYTES',2_000_000):
            code,result,state,runner,prepare=self.run_pipeline(research=failure)
            self.assertEqual(code,0)
            self.assertEqual(result['status'],'no_publishable_analysis')
            attempt=state['auto_attempts']['Example']
            self.assertEqual(attempt['status'],'source_unavailable')
            self.assertEqual(attempt['source_byte_limit'],2_000_000)
            self.assertFalse(p.retry_due(attempt,self.day))
            tomorrow=(datetime.strptime(self.day,'%Y-%m-%d')+timedelta(days=1)).strftime('%Y-%m-%d')
            self.assertTrue(p.retry_due(attempt,tomorrow))
        audit=json.loads((self.output/'audits/Example.source_unavailable.json').read_text(encoding='utf-8'))
        self.assertEqual(audit,failure.audit)
        self.assertEqual(result['prepared_analyses'],0)
        prepare.assert_not_called()

    def test_dynamic_proposal_exclusion_uses_current_retry_policy(self):
        self.write(p.CONTROL+'/research_candidates.json',{'companies':[]})
        self.write(p.CONTROL+'/state.json',{'published_ids':[],'source_candidates':[],
            'auto_attempts':{
                'OldSize':{'last_attempt_on':self.day,'status':'rejected',
                           'reason':'Source exceeds byte limit','source_byte_limit':1_000_000},
                'CurrentSize':{'last_attempt_on':self.day,'status':'source_unavailable',
                               'reason':'Source exceeds byte limit','source_byte_limit':2_000_000},
                'Quality':{'last_attempt_on':self.day,'status':'rejected','reason':'Evidence quote missing'}}})
        with patch.object(p,'MAX_BYTES',2_000_000):
            code,result,*_=self.run_pipeline()
        self.assertEqual(code,0)
        self.proposer.assert_called_once()
        excluded=self.proposer.call_args.args[1]
        self.assertNotIn('oldsize',excluded)
        self.assertIn('currentsize',excluded)
        self.assertIn('quality',excluded)


if __name__=='__main__':unittest.main()
