"""Exercise runtime download failure paths with mock responses, without network access."""
import hashlib
import http.client
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

import prepare_runtime as runtime


class Response:
    def __init__(self,chunks,declared_size=None):
        self.chunks=iter(chunks)
        self.headers={} if declared_size is None else {'Content-Length':str(declared_size)}

    def __enter__(self):return self

    def __exit__(self,*args):return False

    def read(self,size):
        chunk=next(self.chunks,b'')
        if isinstance(chunk,Exception):raise chunk
        return chunk


class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.target=Path(self.folder.name)/'artifact.bin'
        self.data=b'checksum-pinned public artifact'
        self.expected=hashlib.sha256(self.data).hexdigest()
        self.part=self.target.with_suffix('.bin.part')
        self.url='https://example.com/artifact.bin'

    def run_download(self):
        runtime.download(self.url,self.target,self.expected,100)

    def assert_clean(self):
        self.assertFalse(self.part.exists())

    def test_pinned_existing_artifact_avoids_network(self):
        self.target.write_bytes(self.data)
        with patch.object(runtime.urllib.request,'urlopen') as request:
            self.run_download()
        request.assert_not_called()
        self.assertEqual(self.target.read_bytes(),self.data)

    def test_http_504_then_success_restarts_and_checks_artifact(self):
        error=urllib.error.HTTPError(self.url,504,'Gateway Timeout',{},None)
        with patch.object(runtime.urllib.request,'urlopen',side_effect=[error,Response([self.data])]) as request,patch.object(runtime.time,'sleep') as sleep:
            self.run_download()
        self.assertEqual(request.call_count,2)
        sleep.assert_called_once_with(2)
        self.assertEqual(self.target.read_bytes(),self.data)
        self.assert_clean()

    def test_429_and_503_retries_are_bounded(self):
        errors=[urllib.error.HTTPError(self.url,code,'temporarily unavailable',{},None) for code in (429,503)]
        with patch.object(runtime.urllib.request,'urlopen',side_effect=errors+[Response([self.data])]) as request,patch.object(runtime.time,'sleep') as sleep:
            self.run_download()
        self.assertEqual(request.call_count,3)
        self.assertEqual([call.args[0] for call in sleep.call_args_list],[2,4])
        self.assertEqual(self.target.read_bytes(),self.data)
        self.assert_clean()

    def test_transport_failures_retry(self):
        for error in (urllib.error.URLError('temporary resolution error'),TimeoutError('timed out'),ConnectionResetError('connection reset')):
            with self.subTest(error=type(error).__name__):
                self.target.unlink(missing_ok=True)
                with patch.object(runtime.urllib.request,'urlopen',side_effect=[error,Response([self.data])]) as request,patch.object(runtime.time,'sleep') as sleep:
                    self.run_download()
                self.assertEqual(request.call_count,2)
                sleep.assert_called_once_with(2)
                self.assertEqual(self.target.read_bytes(),self.data)
                self.assert_clean()

    def test_interrupted_read_discards_partial_content_before_retry(self):
        broken=Response([b'partial',http.client.IncompleteRead(b'',20)])
        with patch.object(runtime.urllib.request,'urlopen',side_effect=[broken,Response([self.data])]) as request,patch.object(runtime.time,'sleep'):
            self.run_download()
        self.assertEqual(request.call_count,2)
        self.assertEqual(self.target.read_bytes(),self.data)
        self.assert_clean()

    def test_premature_eof_against_content_length_retries(self):
        broken=Response([b'partial'],declared_size=len(self.data))
        with patch.object(runtime.urllib.request,'urlopen',side_effect=[broken,Response([self.data],declared_size=len(self.data))]) as request,patch.object(runtime.time,'sleep'):
            self.run_download()
        self.assertEqual(request.call_count,2)
        self.assertEqual(self.target.read_bytes(),self.data)
        self.assert_clean()

    def test_permanent_http_error_is_not_retried(self):
        error=urllib.error.HTTPError(self.url,404,'Not Found',{},None)
        with patch.object(runtime.urllib.request,'urlopen',side_effect=error) as request,patch.object(runtime.time,'sleep') as sleep:
            with self.assertRaises(urllib.error.HTTPError):self.run_download()
        request.assert_called_once()
        sleep.assert_not_called()
        self.assertFalse(self.target.exists())
        self.assert_clean()

    def test_exhausted_retries_preserve_original_failure_and_existing_file(self):
        self.target.write_bytes(b'previous invalid cached bytes')
        error=urllib.error.HTTPError(self.url,504,'Gateway Timeout',{},None)
        with patch.object(runtime.urllib.request,'urlopen',side_effect=error) as request,patch.object(runtime.time,'sleep') as sleep:
            with self.assertRaises(urllib.error.HTTPError) as caught:self.run_download()
        self.assertIs(caught.exception,error)
        self.assertEqual(request.call_count,runtime.DOWNLOAD_ATTEMPTS)
        self.assertEqual(sleep.call_count,runtime.DOWNLOAD_ATTEMPTS-1)
        self.assertEqual(self.target.read_bytes(),b'previous invalid cached bytes')
        self.assert_clean()

    def test_checksum_mismatch_is_not_retried(self):
        with patch.object(runtime.urllib.request,'urlopen',return_value=Response([b'different artifact'])) as request,patch.object(runtime.time,'sleep') as sleep:
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):self.run_download()
        request.assert_called_once()
        sleep.assert_not_called()
        self.assertFalse(self.target.exists())
        self.assert_clean()

    def test_actual_size_violation_is_not_retried(self):
        with patch.object(runtime.urllib.request,'urlopen',return_value=Response([b'x'*101])) as request,patch.object(runtime.time,'sleep') as sleep:
            with self.assertRaisesRegex(ValueError,'size budget'):self.run_download()
        request.assert_called_once()
        sleep.assert_not_called()
        self.assertFalse(self.target.exists())
        self.assert_clean()

    def test_declared_size_violation_is_not_retried(self):
        with patch.object(runtime.urllib.request,'urlopen',return_value=Response([],declared_size=101)) as request,patch.object(runtime.time,'sleep') as sleep:
            with self.assertRaisesRegex(ValueError,'size budget'):self.run_download()
        request.assert_called_once()
        sleep.assert_not_called()
        self.assertFalse(self.target.exists())
        self.assert_clean()


if __name__=='__main__':unittest.main()
