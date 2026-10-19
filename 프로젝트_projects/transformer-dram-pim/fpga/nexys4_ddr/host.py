"""Nexys 4 DDR에서 token ID→65 logits를 받아 Python Q8.8 기준과 대조하는 PC측 도구.

Python은 문자열/직렬 통신/다음 문자 선택을 담당하고, FPGA는 Transformer 계산을
담당한다. --offline은 Python 기준 결과만 표시하며 FPGA 측정이라고 기록하지 않는다.
실기기 실행에는 pyserial과 연결된 보드 COM 포트, 성공한 bitstream이 필요하다.
"""
from __future__ import annotations
import argparse
import json
import struct
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
# UART 라이브러리를 프로젝트 내부에도 설치해 두었다. 사용자 Python의 전역 환경을 바꾸지 않는다.
if (ROOT/'tools/vendor/serial').is_dir(): sys.path.insert(0,str(ROOT/'tools/vendor'))
from model.gpt_q88 import load_checkpoint, forward_q88_step, new_kv_cache

MAX_CONTEXT=8


def read_exact(serial_port, length: int) -> bytes:
    """serial.read가 적게 반환하는 상황을 고려해 frame 전체를 모은다."""
    result=bytearray()
    while len(result)<length:
        chunk=serial_port.read(length-len(result))
        if not chunk: raise TimeoutError(f'UART 응답이 부족합니다: {len(result)}/{length} bytes')
        result.extend(chunk)
    return bytes(result)


def read_frame(serial_port) -> dict:
    """GP header와 16-bit little-endian 점수를 복원한다. 부호/순서를 바꾸지 않는다."""
    header=read_exact(serial_port,5)
    if header[:2]!=b'GP': raise ValueError(f'UART header 불일치: {header.hex()}')
    status,count,words=header[2:]
    if words not in (0,65): raise ValueError(f'예상하지 못한 logit 개수: {words}')
    data=read_exact(serial_port,2*words)
    logits=list(struct.unpack('<'+'h'*words,data))
    return {'status':status,'token_count':count,'logits':logits}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',help='예: COM5. --offline일 때는 사용하지 않는다.')
    parser.add_argument('--baud',type=int,default=115200,choices=[57600,115200],
                        help='실제 bitstream과 맞출 PC baud: 기본8=115200, 32저속구성=57600')
    parser.add_argument('--offline',action='store_true')
    parser.add_argument('--prompt',default='RO')
    parser.add_argument('--tokens',type=int,default=2,help='greedy로 새로 선택할 문자 개수')
    parser.add_argument('--context-limit',type=int,default=MAX_CONTEXT,choices=range(1,33),
        help='사용하는 bitstream의 MAX_CONTEXT와 같아야 합니다. 기본8; 더 큰 값은 해당 빌드 검증 필요')
    parser.add_argument('--checkpoint',type=Path,default=ROOT/'output/tiny_gpt_full_ops_qat/tiny_gpt_qat_q88.json')
    parser.add_argument('--output',type=Path,default=ROOT/'build/reports/nexys_host_result.json')
    args=parser.parse_args()
    if not args.offline and not args.port: parser.error('--port COM번호 또는 --offline을 지정하세요.')
    model=load_checkpoint(args.checkpoint)
    stoi={ch:i for i,ch in enumerate(model['vocab'])}
    if not args.prompt or any(ch not in stoi for ch in args.prompt):
        parser.error('65개 학습 어휘에 있는 문자를 사용하세요. 예: RO, ROMEO:')
    # 마지막으로 선택한 문자 자체의 logits는 다음 생성이 필요할 때만 계산한다.
    if args.tokens<1 or len(args.prompt)+args.tokens-1>args.context_limit:
        parser.error(f'보드의 context{args.context_limit} 한도: prompt길이 + 생성문자수 - 1 <= {args.context_limit}')
    serial_port=None
    if not args.offline:
        try: import serial
        except ImportError: raise SystemExit('실기기 UART에는 pyserial이 필요합니다: python -m pip install pyserial')
        # UART divider가 실제 FPGA clock에 연결되므로 보드 profile과 baud를 맞춘다.
        # --offline에서는 serial 포트를 열지 않는다. baud 선택만으로 FPGA clock은 바뀌지 않는다.
        serial_port=serial.Serial(args.port,args.baud,timeout=20,write_timeout=5)
    try:
        if serial_port:
            serial_port.reset_input_buffer()
            serial_port.write(b'\xff')
            reset_reply=read_frame(serial_port)
            if reset_reply!={'status':1,'token_count':0,'logits':[]}:
                raise ValueError(f'cache reset 응답 불일치: {reset_reply}')
        cache=new_kv_cache(model)
        transactions=[]
        text=args.prompt
        def process(token_id: int) -> list[int]:
            expected=forward_q88_step(model,token_id,cache)
            if serial_port:
                serial_port.write(bytes([token_id]))
                frame=read_frame(serial_port)
                if frame['status']!=0: raise RuntimeError(f'FPGA 상태 오류: 0x{frame["status"]:02x}')
                if frame['token_count']!=cache['position']: raise ValueError('보드 token count가 기준과 다릅니다.')
                actual=frame['logits']
                if actual!=expected:
                    differences=[i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b]
                    raise AssertionError(f'FPGA/reference logit 불일치: indices={differences[:8]}')
            else: actual=expected
            top=sorted(range(len(actual)),key=lambda i:actual[i],reverse=True)[:5]
            transactions.append({'token_id':token_id,'token_count':cache['position'],'logits_raw_q88':actual,
                'top5':[{'id':i,'character':model['vocab'][i],'raw_q88':actual[i],'real_logit':actual[i]/256.0} for i in top]})
            return actual
        for char in args.prompt: logits=process(stoi[char])
        for step in range(args.tokens):
            chosen=max(range(65),key=lambda i:logits[i])
            text+=model['vocab'][chosen]
            if step+1<args.tokens: logits=process(chosen)
        report={'mode':'fpga_uart' if serial_port else 'python_reference_only',
            'hardware_measured':bool(serial_port),'prompt':args.prompt,'generated_text':text,
            'max_context':args.context_limit,'transactions':transactions,
            'host_baud':args.baud,'port':args.port if serial_port else None,
            'exact_compared_logits':len(transactions)*65 if serial_port else 0}
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'mode':report['mode'],'generated_text':text,
            'transactions':len(transactions),'hardware_measured':report['hardware_measured']},ensure_ascii=True))
        return 0
    finally:
        if serial_port: serial_port.close()


if __name__=='__main__': raise SystemExit(main())
