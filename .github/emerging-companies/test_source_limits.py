"""Bound public HTML acquisition without relaxing content or destination policies."""
from email.message import Message
import hashlib
import io
import unittest
from unittest.mock import Mock, patch

import pipeline as p


class SourceResponse(io.BytesIO):
    def __init__(self,data,content_type='text/html; charset=utf-8'):
        super().__init__(data)
        self.headers=Message()
        self.headers['Content-Type']=content_type
        self.read_limits=[]

    def geturl(self):return 'https://company.example/product'

    def read(self,size=-1):
        self.read_limits.append(size)
        return super().read(size)


class SourceLimitTests(unittest.TestCase):
    url='https://company.example/product'
    hosts={'company.example'}

    def fetch_response(self,response):
        opener=Mock()
        opener.open.return_value=response
        with patch.object(p,'validate_destination',return_value=self.url),patch.object(p,'build_opener',return_value=opener):
            return p._fetch_raw(self.url,self.hosts)

    def test_observed_1690744_byte_homepage_fits_source_budget(self):
        body=b'<main>'+b'x'*(1_690_744-13)+b'</main>'
        self.assertEqual(len(body),1_690_744)
        response=SourceResponse(body)
        result=self.fetch_response(response)
        self.assertEqual(len(result['text'].encode('utf-8')),len(body))
        self.assertEqual(result['sha256'],hashlib.sha256(body).hexdigest())
        self.assertEqual(result['content_type'],'text/html')
        self.assertEqual(result['url'],self.url)

    def test_exact_two_megabyte_boundary_is_accepted(self):
        body=b'x'*2_000_000
        result=self.fetch_response(SourceResponse(body))
        self.assertEqual(len(result['text']),len(body))
        self.assertEqual(result['sha256'],hashlib.sha256(body).hexdigest())

    def test_over_budget_response_stops_after_bounded_read(self):
        response=SourceResponse(b'x'*2_000_010)
        with self.assertRaisesRegex(ValueError,'Source exceeds byte limit'):
            self.fetch_response(response)
        self.assertEqual(response.read_limits,[2_000_001])

    def test_non_document_content_is_rejected_before_body_read(self):
        for content_type in ('application/pdf','application/octet-stream','image/png'):
            with self.subTest(content_type=content_type):
                response=SourceResponse(b'not an allowed HTML document',content_type)
                with self.assertRaisesRegex(ValueError,'Unsupported source content type'):
                    self.fetch_response(response)
                self.assertEqual(response.read_limits,[])

    def test_destination_denial_still_prevents_opening_connection(self):
        with patch.object(p,'validate_destination',side_effect=ValueError('Host is outside this source allowlist')),patch.object(p,'build_opener') as opener:
            with self.assertRaisesRegex(ValueError,'outside this source allowlist'):
                p._fetch_raw('https://unlisted.example/',self.hosts)
        opener.assert_not_called()

    def test_robots_denial_still_prevents_document_fetch(self):
        with patch.object(p,'validate_destination',return_value=self.url),patch.object(p,'robots_allowed',return_value=False),patch.object(p,'_fetch_raw') as fetch_raw:
            with self.assertRaisesRegex(ValueError,'robots.txt disallows this source'):
                p.fetch(self.url,self.hosts)
        fetch_raw.assert_not_called()


if __name__=='__main__':unittest.main()
