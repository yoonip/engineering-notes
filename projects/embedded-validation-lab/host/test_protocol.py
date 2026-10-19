"""장치 없는 host unit test. 실제 UART/SRAM 측정의 성공 결과와 구분한다."""
import json
import unittest
from run_validation import validate_response, request_run, expected_signature

def response(seq=7):
    return {'board':'ESP32','seq':seq,'version':1,'words':1024,'errors':0,
            'signature':expected_signature(),'elapsed_us':10}

class FakeSerial:
    def __init__(self,chunks): self.chunks=list(chunks); self.writes=[]
    def write(self,b): self.writes.append(b)
    def flush(self): pass
    def read(self,n): return self.chunks.pop(0) if self.chunks else b''

class ProtocolTests(unittest.TestCase):
    def test_success(self): self.assertTrue(validate_response(response(),'ESP32',7))
    def test_stale(self): self.assertFalse(validate_response(response(6),'ESP32',7))
    def test_board(self): self.assertFalse(validate_response(response(),'STM32F767ZI',7))
    def test_error(self):
        obj=response();obj['errors']=1
        with self.assertRaises(RuntimeError): validate_response(obj,'ESP32',7)
    def test_signature(self):
        obj=response();obj['signature']^=1
        with self.assertRaises(RuntimeError): validate_response(obj,'ESP32',7)
    def test_field_type(self):
        obj=response();obj['elapsed_us']=True
        with self.assertRaises(ValueError): validate_response(obj,'ESP32',7)
    def test_negative(self):
        obj=response();obj['elapsed_us']=-1
        with self.assertRaises(ValueError): validate_response(obj,'ESP32',7)
    def test_fragments_and_boot_log(self):
        line=json.dumps(response()).encode()+b'\n'
        fake=FakeSerial([b'boot log\n',line[:10],line[10:]])
        self.assertEqual(request_run(fake,'ESP32',7)['seq'],7)
    def test_timeout(self):
        fake=FakeSerial([])
        with self.assertRaises(TimeoutError):request_run(fake,'ESP32',7,timeout=.01,retries=1)
        self.assertEqual(fake.writes,[b'RUN,7\n',b'RUN,7\n'])
    def test_stale_then_correct(self):
        fake=FakeSerial([(json.dumps(response(6))+'\n'+json.dumps(response(7))+'\n').encode()])
        self.assertEqual(request_run(fake,'ESP32',7)['seq'],7)

if __name__=='__main__': unittest.main()
