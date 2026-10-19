"""UART 기반 반복 검증: sequence, timeout, 결과 판정, CSV/JSONL 증거 저장."""
import argparse
import csv
import json
import time
import statistics
from pathlib import Path
import serial


def expected_signature():
    x=0x12345678
    for i in range(256):
        x ^= (i+0x9e3779b9)&0xffffffff
        x=((x<<5)|(x>>27))&0xffffffff
        x=(x+0x7f4a7c15)&0xffffffff
    return x


def validate_response(obj, board, sequence):
    if obj.get('board') != board or obj.get('seq') != sequence:
        return False  # 이전 명령의 늦은 응답을 현재 성공으로 오판하지 않는다.
    for field in ['seq','words','errors','signature','elapsed_us']:
        if type(obj.get(field)) is not int or obj[field] < 0:
            raise ValueError('invalid integer field: '+field)
    if obj.get('version') != 1 or obj['words'] != 1024:
        raise ValueError('firmware version or test length mismatch')
    if obj['errors'] or obj['signature'] != expected_signature():
        raise RuntimeError('device validation FAIL: '+json.dumps(obj))
    return True


def request_run(port, board, sequence, timeout=2.0, retries=1):
    command=f'RUN,{sequence}\n'.encode('ascii')
    for attempt in range(retries+1):
        port.write(command); port.flush()
        deadline=time.monotonic()+timeout
        pending=bytearray()
        while time.monotonic()<deadline:
            pending.extend(port.read(256))
            if len(pending)>4096: raise ValueError('RX frame too large')
            while b'\n' in pending:
                raw,_,tail=pending.partition(b'\n'); pending=bytearray(tail)
                try: obj=json.loads(raw)
                except (ValueError,UnicodeDecodeError): continue # boot log 등 비JSON 행.
                if not isinstance(obj,dict): continue
                if 'error' in obj or 'fatal' in obj: raise RuntimeError(str(obj))
                if validate_response(obj,board,sequence):
                    obj['attempt']=attempt+1
                    return obj
        # 다음 시도에도 같은 sequence를 사용. 펌웨어는 직전 결과를 캐시한다.
    raise TimeoutError(f'no valid response: board={board}, seq={sequence}')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--port',required=True)
    ap.add_argument('--board',choices=['ESP32','STM32F767ZI'],required=True)
    ap.add_argument('--runs',type=int,default=100)
    ap.add_argument('--out',type=Path,default=Path('validation_results'))
    args=ap.parse_args()
    if not 1<=args.runs<=100000: raise ValueError('runs out of range')
    args.out.mkdir(parents=True,exist_ok=True)
    rows=[]
    with serial.Serial(args.port,115200,timeout=0.1) as port:
        port.dtr=False; port.rts=False
        time.sleep(2)  # serial open으로 reset된 ESP32의 boot 완료를 기다림.
        port.reset_input_buffer()
        with (args.out/'raw.jsonl').open('w',encoding='utf-8') as raw_file:
            for seq in range(args.runs):
                obj=request_run(port,args.board,seq)
                obj['host_unix_time']=time.time()
                raw_file.write(json.dumps(obj)+'\n'); raw_file.flush()
                rows.append({k:obj[k] for k in
                             ['seq','errors','signature','elapsed_us','attempt']})
    with (args.out/'summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    times=[r['elapsed_us'] for r in rows]
    print(json.dumps({'runs':len(rows),'passed':len(rows),
                      'median_us':statistics.median(times),'min_us':min(times),
                      'max_us':max(times)},indent=2))


if __name__=='__main__': main()
