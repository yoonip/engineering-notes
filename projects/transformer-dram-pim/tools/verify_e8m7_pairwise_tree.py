#!/usr/bin/env python3
"""곱·각 pairwise 합에서 RNE하는 독립 E8M7 baseline의 실제 RTL 검증."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import re
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model.e8m7_maxex import (CANONICAL_NAN, decode_fields, decode_e8m7_fraction,
    fraction_to_e8m7, rounded_product_words, rounded_product_tree_dot,
    maxex_dot, exact_dot_e8m7)
from tools.verify_e8m7_maxex import make_vectors, resolve_executable, write_words
from tools.verify_e8m7_maxex_registered import make_schedule, lane_tag_vector


# 독립 adder 정답: 특수값을 먼저 처리한 뒤 정확한 Fraction 합을 한 번 RNE.
# RTL의 GRS 구현과 다른 계산 경로를 사용하므로 같은 실수를 공유하지 않게 한다.
def add_word(left: int,right: int)->int:
    a,b=decode_fields(left),decode_fields(right)
    if a.kind=='nan' or b.kind=='nan':return CANONICAL_NAN
    if a.kind=='inf' and b.kind=='inf' and a.sign!=b.sign:return CANONICAL_NAN
    if a.kind=='inf':return (a.sign<<15)|0x7f80
    if b.kind=='inf':return (b.sign<<15)|0x7f80
    return fraction_to_e8m7(decode_e8m7_fraction(left)+decode_e8m7_fraction(right))


# heap 잎과 모든 내부 adder를 같은 인접쌍 순서로 계산한다. 최종 word와 Python의
# 공개 rounded_product_tree_dot 결과도 별도로 일치시켜 참조 구성 실수를 검사한다.
def expected_tree(vector:dict)->list[int]:
    products=list(rounded_product_words(vector['a_words'],vector['b_words']))
    leaves=1<<(len(products)-1).bit_length()
    nodes=[0]*(2*leaves)
    nodes[leaves:leaves+len(products)]=products
    for node in range(leaves-1,0,-1):nodes[node]=add_word(nodes[node*2],nodes[node*2+1])
    assert nodes[1]==rounded_product_tree_dot(vector['a_words'],vector['b_words'])
    return nodes[1:]


# MAX-EX 검증과 같은 경계·같은 결정론적 입력을 쓴다. MAX-EX와 다른 word는
# baseline의 반올림 손실이지 RTL 실패가 아니다. tree 순서를 바꾸지 않는다.
def vectors_for(lanes:int,count:int,seed:int)->list[dict]:
    vectors=make_vectors(lanes,count,seed)
    if lanes>=3:
        vectors.append({'name':'pairwise_half_ulp_then_cancel',
            'a_words':[0x3f80,0x3b80,0xbf80]+[0]*(lanes-3),
            'b_words':[0x3f80]*3+[0]*(lanes-3)})
    return vectors


# 모든 16bit 입력 word ×1을 검사한다. exponent 255의 NaN과 zero도 제외하지 않는다.
# 이것은 scalar 단항 항등/정규화 조사이며 모든 두 입력 쌍의 전수검사가 아니다.
# 추가로 128×128 정상 significand 곱, exponent 차·부호·subnormal의 고정 경계와
# seeded random 쌍을 섞어 guard/round/sticky와 중간 overflow를 검사한다.
def scalar_pairs(seed:int,count:int,exhaustive:bool)->list[tuple[int,int]]:
    pairs=[(word,0x3f80) for word in range(65536)] if exhaustive else []
    specials=[0,0x8000,1,0x8001,0x007f,0x807f,0x0080,0x8080,0x3f80,0xbf80,
              0x3f81,0x3fff,0x4000,0x7f7f,0xff7f,0x7f80,0xff80,0x7fc1,0xff81]
    pairs.extend((a,b) for a in specials for b in specials)
    if exhaustive:
        pairs.extend((0x3f80+a,0x3f80+b) for a in range(128) for b in range(128))
    for exponent in (0,1,2,126,127,128,253,254):
        for gap in range(15):
            other=max(0,exponent-gap)
            for ma in (0,1,63,64,126,127):
                for mb in (0,1,63,64,126,127):
                    for signs in range(4):
                        pairs.append(((exponent<<7)|ma|((signs&1)<<15),
                                      (other<<7)|mb|((signs>>1)<<15)))
    rng=random.Random(seed)
    pairs.extend((rng.randrange(65536),rng.randrange(65536)) for _ in range(count))
    return pairs


# 각 compile/simulation의 명령·실제 종료코드·stdout/stderr를 보존한다. 실패/timeout도
# JSON을 남기며, 실패한 도구의 결과를 다음 성공 출력으로 덮지 않는다.
def run_tool(arguments:list[str],folder:Path,label:str,timeout:int)->dict:
    started=time.perf_counter();timed_out=False
    try:
        completed=subprocess.run(arguments,cwd=folder,capture_output=True,timeout=timeout)
        code=completed.returncode;raw=completed.stdout+completed.stderr
    except subprocess.TimeoutExpired as error:
        timed_out=True;code=None;raw=(error.stdout or b'')+(error.stderr or b'')
    text=raw.decode('utf-8',errors='replace');log=folder/(label+'.log')
    log.write_text(text,encoding='utf-8')
    return {'command':arguments,'returncode':code,'timed_out':timed_out,
        'wall_seconds':round(time.perf_counter()-started,6),
        'log':log.relative_to(ROOT).as_posix(),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),
        'stdout':text}


def require_tool(record:dict)->str:
    assert record['returncode']==0 and not record['timed_out'],record['log']
    return record['stdout']


# Python에서도 이전 수락 입력을 한 cycle 보관해 TB와 별도의 protocol 정답을 만든다.
# reset은 아직 출력하지 않은 pending 입력을 취소하며 reset+valid에서 입력을 받지 않는다.
def schedule_oracle(schedule:list[dict],vectors:list[dict],lanes:int)->tuple[list[dict],dict]:
    pending=None;expected=[];burst=0
    counts={'accepted':0,'cancelled':0,'resets':0,'exact':0,'lane_checks':0,'maximum_burst':0}
    for row in schedule:
        if not row['reset_n']:
            expected.append({'valid':0,'word':0});counts['resets']+=1
            counts['cancelled']+=pending is not None;pending=None;burst=0
        else:
            expected.append({'valid':int(pending is not None),'word':pending})
            counts['exact']+=pending is not None
            if row['input_valid']:
                vector=vectors[row['vector_index']]
                pending=rounded_product_tree_dot(vector['a_words'],vector['b_words'])
                counts['accepted']+=1;counts['lane_checks']+=2*lanes;burst+=1
                counts['maximum_burst']=max(counts['maximum_burst'],burst)
            else:pending=None;burst=0
    assert pending is None and counts['accepted']==counts['exact']+counts['cancelled']
    return expected,counts


def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lanes',nargs='+',type=int,default=[1,3,5,16,17],help='odd padding과 scalar lane 포함')
    parser.add_argument('--random-cases',type=int,default=256,help='lane별 결정론적 random 내적 수')
    parser.add_argument('--registered-lanes',nargs='+',type=int,default=[3,16],help='등록 경계 시험 lane 수(2 이상)')
    parser.add_argument('--registered-random-cases',type=int,default=128)
    parser.add_argument('--scalar-random-cases',type=int,default=4096)
    parser.add_argument('--skip-scalar-exhaustive',action='store_true',help='확대 재검사에서 65536 단항/16384 곱 조사만 생략')
    parser.add_argument('--seed',type=int,default=20261005)
    parser.add_argument('--timeout',type=int,default=300,help='각 tool 단계의 벽시계 초')
    parser.add_argument('--iverilog');parser.add_argument('--vvp')
    parser.add_argument('--output',type=Path,default=ROOT/'build/reports/e8m7_pairwise_verification.json')
    args=parser.parse_args()
    if any(x<1 for x in args.lanes) or any(x<2 for x in args.registered_lanes):parser.error('lane parameter 범위 오류')
    if min(args.random_cases,args.registered_random_cases,args.scalar_random_cases)<0 or args.timeout<1:parser.error('case/timeout 범위 오류')
    compiler=resolve_executable('iverilog',args.iverilog);runtime=resolve_executable('vvp',args.vvp)
    kernel=ROOT/'rtl/e8m7_pairwise_tree_mac.sv';wrapper=ROOT/'rtl/e8m7_pairwise_registered_top.sv'
    bench=ROOT/'tb/tb_e8m7_pairwise_tree.sv';work=ROOT/'build/e8m7_pairwise'/args.output.stem
    source_files=[kernel,wrapper,bench,Path(__file__),ROOT/'model/e8m7_maxex.py',
        ROOT/'tools/verify_e8m7_maxex.py',ROOT/'tools/verify_e8m7_maxex_registered.py']
    report={'passed':False,'mode':'independent_e8m7_pairwise_tree_rtl_verification',
        'definition_ko':'각 8x8 곱과 균형 트리 매 덧셈을 E8M7 RNE, 표준 8+GRS sticky 정렬',
        'reference':'model.e8m7_maxex.rounded_product_tree_dot','seed':args.seed,
        'gpt_q88_connected':False,'physical_board_measured':False,'sdf_annotated':False,
        'guard512_alignment_used':False,'latency_clocks':1,
        'structural_bit_widths':{'input_significand':8,'exact_product':16,
            'adder_significand':8,'guard_round_sticky':3,'aligned_operand':11,'carry_sum':12},
        'coverage_ko':'scalar 항등 word 전수와 고정/seeded 경계. 모든 두 입력 조합·모든 lane tuple의 전수 시험 아님.',
        'source_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
        'kernel_configurations':[],'registered_configurations':[],'vectors':{},'registered_schedules':{},
        'scalar_exhaustive_identity_inputs':0 if args.skip_scalar_exhaustive else 65536,
        'scalar_exhaustive_normal_significand_products':0 if args.skip_scalar_exhaustive else 16384,
        'total_kernel_words':0,'total_tree_node_comparisons':0,'total_scalar_mul_comparisons':0,
        'total_scalar_add_comparisons':0,'total_registered_words':0,'total_registered_cycles':0,
        'total_packed_lane_word_checks':0,'started_at':datetime.now(timezone.utc).isoformat()}
    try:
        pairs=scalar_pairs(args.seed,args.scalar_random_cases,not args.skip_scalar_exhaustive)
        for config_index,lanes in enumerate(args.lanes):
            folder=work/f'kernel_lanes{lanes}';folder.mkdir(parents=True,exist_ok=True)
            vectors=vectors_for(lanes,args.random_cases,args.seed);nodes=[expected_tree(v) for v in vectors]
            cfg={'lanes':lanes,'cases':len(vectors)};report['kernel_configurations'].append(cfg)
            report['vectors'][str(lanes)]=vectors
            write_words(folder/'a.mem',[w for v in vectors for w in v['a_words']])
            write_words(folder/'b.mem',[w for v in vectors for w in v['b_words']])
            write_words(folder/'expected.mem',[v[0] for v in nodes]);write_words(folder/'tree.mem',[w for row in nodes for w in row])
            scalar=pairs if config_index==0 else []
            if scalar:
                write_words(folder/'scalar_a.mem',[a for a,b in scalar]);write_words(folder/'scalar_b.mem',[b for a,b in scalar])
                write_words(folder/'scalar_mul.mem',[rounded_product_words([a],[b])[0] for a,b in scalar])
                write_words(folder/'scalar_add.mem',[add_word(a,b) for a,b in scalar])
            command=[compiler,'-g2012','-s','tb_e8m7_pairwise_tree',f'-Ptb_e8m7_pairwise_tree.LANES={lanes}',
                f'-Ptb_e8m7_pairwise_tree.CASES={len(vectors)}',f'-Ptb_e8m7_pairwise_tree.SCALAR_CASES={len(scalar)}',
                '-o','simulation.vvp',str(kernel),str(wrapper),str(bench)]
            cfg['compile']=run_tool(command,folder,'compile',args.timeout);require_tool(cfg['compile'])
            cfg['simulation']=run_tool([runtime,'simulation.vvp'],folder,'simulation',args.timeout)
            output=require_tool(cfg['simulation']);rows=re.findall(r'^PAIRWISE case=(\d+) result=([0-9a-f]{4}) nodes=(\d+)\s*$',output,re.M)
            assert len(rows)==len(vectors)
            for i,(index,word,count) in enumerate(rows):
                assert int(index)==i and int(word,16)==nodes[i][0] and int(count)==len(nodes[i])
            scalar_rows=re.findall(r'^SCALAR case=(\d+) mul=([0-9a-f]{4}) add=([0-9a-f]{4})\s*$',output,re.M)
            assert len(scalar_rows)==len(scalar)
            assert f'PAIRWISE PASS lanes={lanes} cases={len(vectors)} scalar={len(scalar)}' in output
            cfg.update({'passed':True,'tree_nodes_checked':sum(map(len,nodes)),'scalar_mul_checked':len(scalar),
                'scalar_add_checked':len(scalar),'exact_python_matches':len(rows)})
            # 수치 방식 차이는 따로 세며 baseline의 버그로 처리하지 않는다.
            cfg['maxex_guard16_different']=sum(nodes[i][0]!=maxex_dot(v['a_words'],v['b_words'],16) for i,v in enumerate(vectors))
            cfg['maxex_guard32_different']=sum(nodes[i][0]!=maxex_dot(v['a_words'],v['b_words'],32) for i,v in enumerate(vectors))
            cfg['exact_dot_different']=sum(nodes[i][0]!=exact_dot_e8m7(v['a_words'],v['b_words']) for i,v in enumerate(vectors))
            # 발표에서 반올림 위치의 차이를 설명할 수 있도록 결정된 고정 반례의
            # 실제 baseline 정답과 MAX-EX/이상적 dot word를 모두 적는다.
            cfg['defined_difference_examples']=[{'name':v['name'],'pairwise_word':nodes[i][0],
                'maxex_guard16_word':maxex_dot(v['a_words'],v['b_words'],16),
                'maxex_guard32_word':maxex_dot(v['a_words'],v['b_words'],32),
                'exact_dot_word':exact_dot_e8m7(v['a_words'],v['b_words'])}
                for i,v in enumerate(vectors) if v['name'] in
                ('pairwise_half_ulp_then_cancel','extreme_finite_cancellation_loses_unit',
                 'negative_half_subnormal_tie_to_negative_zero')]
            cfg['memory_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.mem')}
            report['total_kernel_words']+=len(rows);report['total_tree_node_comparisons']+=cfg['tree_nodes_checked']
            report['total_scalar_mul_comparisons']+=len(scalar);report['total_scalar_add_comparisons']+=len(scalar)
            print(f'kernel LANES{lanes}: {len(rows)}word/{cfg["tree_nodes_checked"]}nodes/{len(scalar)}scalar PASS',flush=True)
        for lanes in args.registered_lanes:
            folder=work/f'registered_lanes{lanes}';folder.mkdir(parents=True,exist_ok=True)
            vectors=[lane_tag_vector(lanes)]+vectors_for(lanes,args.registered_random_cases,args.seed)
            schedule=make_schedule(vectors);expected,counts=schedule_oracle(schedule,vectors,lanes)
            cfg={'lanes':lanes,'cycles':len(schedule),**counts};report['registered_configurations'].append(cfg)
            report['registered_schedules'][str(lanes)]={'vectors':vectors,'schedule':schedule}
            inputs=[vectors[r['vector_index']] for r in schedule]
            write_words(folder/'a.mem',[w for v in inputs for w in v['a_words']]);write_words(folder/'b.mem',[w for v in inputs for w in v['b_words']])
            write_words(folder/'expected.mem',[rounded_product_tree_dot(v['a_words'],v['b_words']) for v in inputs])
            (folder/'controls.mem').write_text(''.join(f'{2*r["reset_n"]+r["input_valid"]:x}\n' for r in schedule),encoding='ascii')
            command=[compiler,'-g2012','-s','tb_e8m7_pairwise_tree',f'-Ptb_e8m7_pairwise_tree.LANES={lanes}',
                f'-Ptb_e8m7_pairwise_tree.CASES={len(schedule)}','-Ptb_e8m7_pairwise_tree.REGISTERED=1',
                '-o','simulation.vvp',str(kernel),str(wrapper),str(bench)]
            cfg['compile']=run_tool(command,folder,'compile',args.timeout);require_tool(cfg['compile'])
            cfg['simulation']=run_tool([runtime,'simulation.vvp'],folder,'simulation',args.timeout)
            output=require_tool(cfg['simulation']);rows=re.findall(r'^PAIRWISE_REG cycle=(\d+) valid=(\d+) result=([0-9a-f]{4}) exact=(\d+)\s*$',output,re.M)
            assert len(rows)==len(schedule)
            for i,(cycle,valid,word,count) in enumerate(rows):
                assert int(cycle)==i and int(valid)==expected[i]['valid']
                if expected[i]['word'] is not None:assert int(word,16)==expected[i]['word']
            wanted=(f'PAIRWISE_REG PASS lanes={lanes} cycles={len(schedule)} exact={counts["exact"]} '
                f'accepted={counts["accepted"]} cancelled={counts["cancelled"]} resets={counts["resets"]} '
                f'lane_checks={counts["lane_checks"]} maximum_burst={counts["maximum_burst"]}')
            assert wanted in output
            cfg.update({'passed':True,'one_clock_latency_checked':True,'continuous_valid_checked':True,
                'bubble_checked':True,'pending_cancelled_by_reset':True,'packed_lane_register_order_checked':True,
                'memory_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.mem')}})
            report['total_registered_words']+=counts['exact'];report['total_registered_cycles']+=len(schedule)
            report['total_packed_lane_word_checks']+=counts['lane_checks']
            print(f'registered LANES{lanes}: {counts["exact"]}word/{len(schedule)}cycles PASS',flush=True)
        report['passed']=True
    except Exception as error:
        report['failure_ko']=f'{type(error).__name__}: {error}'
        print(report['failure_ko'],file=sys.stderr)
    finally:
        # 실패한 실행의 명령/정답 mem/로그를 보존하면서 JSON만 사람이 읽는 요약으로
        # 만든다. 거대한 stdout 원문은 log로 남겨 JSON의 수십만 줄 복제를 피한다.
        for cfg in report['kernel_configurations']+report['registered_configurations']:
            for stage in ('compile','simulation'):
                if stage in cfg:cfg[stage].pop('stdout',None)
        report['finished_at']=datetime.now(timezone.utc).isoformat()
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return 0 if report['passed'] else 1


if __name__=='__main__':
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
    raise SystemExit(main())
