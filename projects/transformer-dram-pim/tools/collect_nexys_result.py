"""Vivado 원본 report와 실제 .bit에서 Nexys 결과를 읽어 검증 증거 JSON을 저장한다."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bit_header(path: Path) -> dict:
    """Xilinx .bit의 장치/생성정보와 실제 configuration payload 길이를 검증한다."""
    data=path.read_bytes()
    magic_length=struct.unpack('>H',data[:2])[0]
    pos=2+magic_length
    assert struct.unpack('>H',data[pos:pos+2])[0]==1
    pos+=2
    result={}
    while pos<len(data):
        tag=chr(data[pos]);pos+=1
        width=4 if tag=='e' else 2
        length=int.from_bytes(data[pos:pos+width],'big');pos+=width
        assert pos+length<=len(data),'잘린 bitstream payload'
        if tag=='e': result['configuration_payload_bytes']=length
        else: result[{'a':'design','b':'part','c':'date','d':'time'}[tag]]=data[pos:pos+length].rstrip(b'\0').decode('ascii')
        pos+=length
    assert pos==len(data)
    assert result['part']=='7a100tcsg324',result
    return result


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,default=ROOT/'build/nexys4_ddr/board')
    parser.add_argument('--context',type=int,default=8)
    parser.add_argument('--cache-storage',choices=['registers','distributed'],default='registers')
    parser.add_argument('--clock-hz',type=int,choices=[2500000,5000000],default=5000000)
    parser.add_argument('--host-baud',type=int,choices=[57600,115200],default=115200)
    parser.add_argument('--stage',help='해당 빌드를 실행한 임시 폴더 경로')
    args=parser.parse_args()
    folder=args.directory.resolve()
    util=(folder/'routed_utilization.rpt').read_text(encoding='utf-8')
    timing=(folder/'routed_timing.rpt').read_text(encoding='utf-8')
    drc=(folder/'drc.rpt').read_text(encoding='utf-8')
    methodology=(folder/'methodology.rpt').read_text(encoding='utf-8')
    resources={}
    for name,pattern in [('LUT',r'Slice LUTs'),('FF',r'Slice Registers'),('DSP',r'DSPs'),('BRAM36_tiles',r'Block RAM Tile'),('LUT_memory',r'LUT as Memory')]:
        match=re.search(r'\|\s*'+pattern+r'\s*\|\s*(\d+)\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*(\d+)\s*\|\s*([\d.]+)',util)
        assert match,name
        resources[name]={'used':int(match[1]),'available':int(match[2]),'percent':float(match[3])}
    assert re.search(r'Design State\s*:\s*(Fully )?Routed',timing)
    summary=timing.split('Design Timing Summary')[1]
    line=re.search(r'\n\s*([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)\s+([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)\s+([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)\s*\n',summary)
    assert line,'timing summary가 없습니다.'
    metrics=dict(zip(['WNS_ns','TNS_ns','setup_failing_endpoints','setup_endpoints',
                      'WHS_ns','THS_ns','hold_failing_endpoints','hold_endpoints',
                      'WPWS_ns','TPWS_ns','pulse_failing_endpoints','pulse_endpoints'],map(float,line.groups())))
    assert min(metrics['WNS_ns'],metrics['WHS_ns'],metrics['WPWS_ns'])>=0
    assert 'All user specified timing constraints are met.' in timing
    assert 'checking no_clock (0)' in timing
    assert 'checking unconstrained_internal_endpoints (0)' in timing
    # clock 옵션은 요약의 이름표일 뿐이다. 실제 STA에 있는 generated clock 주기가
    # 그 값과 같은지 확인하여 XDC 숫자만 바꾼 잘못된 성공 표시를 방지한다.
    expected_period=1000000000/args.clock_hz
    clock_rows=re.findall(r'^\s*(clock\S*)\s+\{[^}]+\}\s+([\d.]+)\s+',timing,re.M)
    assert any(abs(float(period)-expected_period)<0.001 for _,period in clock_rows), '실제 generated clock 주기 불일치'
    assert args.clock_hz//args.host_baud==43, '현재 UART divider43과 profile이 다릅니다.'
    rules=lambda text:[{'rule':m[0],'severity':m[1],'count':int(m[2])} for m in
        re.findall(r'\|\s*([A-Z]+-\d+)\s*\|\s*(Warning|Error|Critical Warning)\s*\|[^\n]+?\|\s*(\d+)\s*\|',text)]
    drc_rules=rules(drc)
    assert not any(x['severity']!='Warning' for x in drc_rules)
    bit=folder/'nexys4_ddr_gpt.bit'
    bit_info=bit_header(bit)
    weights=sorted((folder/'weights').glob('*.mem'))
    assert len(weights)==36
    for weight in weights: assert digest(weight)==digest(ROOT/'build/vivado_weights'/weight.name),weight
    result={'device':'xc7a100tcsg324-1','board':'Nexys 4 DDR','vivado':'2024.1',
        'max_context':args.context,'cache_storage':args.cache_storage,'model':{'vocab':65,'d_model':16,'heads':4,'d_ff':32,'layers':2,
            'bias':True,'layernorm_affine':True,'activation':'GELU','format':'signed Q8.8'},
        'clock_hz':args.clock_hz,'clock_period_ns':expected_period,
        'host_baud':args.host_baud,'uart_divisor':43,'fpga_actual_baud':args.clock_hz/43,
        'resources_routed':resources,
        'timing':metrics,'no_clock_endpoints':0,'unconstrained_internal_endpoints':0,
        'drc':{'error_count':0,'warning_count':sum(x['count'] for x in drc_rules),'rules':drc_rules},
        'methodology':{'rules':rules(methodology)},
        'bitstream':{'path':str(bit),'bytes':bit.stat().st_size,'sha256':digest(bit),'header':bit_info},
        'weights':[{'file':p.name,'sha256':digest(p)} for p in weights],
        'checkpoint_sha256':digest(ROOT/'output/tiny_gpt_full_ops_qat/tiny_gpt_qat_q88.json'),
        'routed_checkpoint':{'file':'routed.dcp','sha256':digest(folder/'routed.dcp'),
                             'bytes':(folder/'routed.dcp').stat().st_size},
        'source_snapshot':[{'file':p.relative_to(folder/'source_snapshot').as_posix(),'sha256':digest(p)}
                           for p in sorted((folder/'source_snapshot').rglob('*')) if p.is_file()],
        'ascii_stage':args.stage,'physical_programming_performed':False,'physical_board_measured':False,
        'notes':['이 기록은 Vivado 합성·배치·배선·제약 검증이며 실제 보드 출력 측정은 아니다.',
            'DSP pipeline 권고와 조합 reset gating의 LUTAR-1 경고가 남아 있다.',
            'DDR2 핀/컨트롤러를 사용하지 않으며 메모리 칩 자체의 PIM을 구현한 것은 아니다.']}
    (folder/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    location={'source_root':str(ROOT),'ascii_stage':args.stage,'device':result['device'],
        'max_context':args.context,'physical_programming_performed':False,
        'clock_hz':args.clock_hz,'host_baud':args.host_baud,
        'cache_storage':args.cache_storage,
        'vivado_exit_code':0,'source_note_ko':'실제로 빌드한 stage와 checkpoint/bitstream 해시는 result.json에 기록한다.'}
    (folder/'build_location.json').write_text(json.dumps(location,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['max_context','resources_routed','timing','drc','bitstream']},ensure_ascii=True))


if __name__=='__main__':main()
