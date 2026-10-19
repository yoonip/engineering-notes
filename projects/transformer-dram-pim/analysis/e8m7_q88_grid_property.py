"""Q8.8에서 E8M7로 변환한 입력의 제한된 격자를 확인한다.

G16 무손실의 충분조건을 확인하는 별도 수치 조사다. 일반 E8M7 분포나
전체 부동소수점 GPT 정확도를 보장하지 않으며 기본670표본 실험과 분리한다.
"""
from fractions import Fraction
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import platform
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model.e8m7_maxex import fraction_to_e8m7,decode_e8m7_fraction,decode_fields,maxex_dot_details


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'build/reports/e8m7_q88_grid_property.json')
    parser.add_argument('--samples',type=int,default=128)
    parser.add_argument('--seed',type=int,default=20261005)
    parser.add_argument('--lanes',type=int,default=16)
    args=parser.parse_args()
    if args.samples<1 or args.lanes<1:
        parser.error('--samples와 --lanes는 1 이상이어야 합니다.')
    before=time.perf_counter()
    exponents=[]
    max_abs=Fraction(0)
    checked_inputs=0
    # 16bit signed raw의 전체 범위다. Fraction(raw,256)가 원래 Q8.8의 정확한 값이다.
    for raw in range(-32768,32768):
        word=fraction_to_e8m7(Fraction(raw,256))
        value=decode_e8m7_fraction(word)
        assert (value*256).denominator==1
        assert abs(value)<=128
        max_abs=max(max_abs,abs(value))
        checked_inputs+=1
        if value:
            exponents.append(decode_fields(word).unbiased_exponent)
    # 양쪽 벡터를 Q8.8 grid에서 가져온 조건의 내적만 검사한다.
    rng=random.Random(args.seed)
    exact_matches=0
    # 표본 내용 자체의 digest도 남긴다. 같은 seed와 lane 길이가 같은 벡터를
    # 만들었는지 확인하는 용도이며 합성 회로나 GPT checkpoint hash는 아니다.
    samples_digest=hashlib.sha256()
    for _ in range(args.samples):
        a=[fraction_to_e8m7(Fraction(rng.randrange(-32768,32768),256)) for _ in range(args.lanes)]
        b=[fraction_to_e8m7(Fraction(rng.randrange(-32768,32768),256)) for _ in range(args.lanes)]
        details=maxex_dot_details(a,b,16)
        assert details.reconstructed==details.exact
        exact_matches+=1
        samples_digest.update(json.dumps([a,b],separators=(',',':')).encode('ascii')+b'\n')
    source_hashes={file:hashlib.sha256((ROOT/file).read_bytes()).hexdigest() for file in
                   ('model/e8m7_maxex.py','analysis/e8m7_q88_grid_property.py')}
    result={'passed':True,'mode':'q88_converted_e8m7_grid_property',
            'all_signed_q88_inputs_checked':checked_inputs,
            'signed_q88_raw_minimum':-32768,'signed_q88_raw_maximum':32767,
            'input_exhaustive':True,'input_exponent_range':[min(exponents),max(exponents)],
            'maximum_abs_encoded_value':str(max_abs),'encoded_values_are_multiples_of':'1/256',
            'product_grid':'1/65536','maximum_product_exponent':14,
            'guard16_common_unit_maximum':'1/65536','random_dot_samples':args.samples,
            'seed':args.seed,'lanes':args.lanes,'guard_bits':16,'unrounded_exact_matches':exact_matches,
            'random_dot_vectors_sha256':samples_digest.hexdigest(),
            'wall_seconds':round(time.perf_counter()-before,6),
            'python_version':platform.python_version(),
            'execution_argv':[sys.executable,str(Path(__file__).resolve()),*sys.argv[1:]],
            'connected_to_q88_transformer':False,'physical_board_measured':False,
            'description_ko':'Q8.8 값을 E8M7로 먼저 RNE한 제한된 입력 분포의 격자 성질. 원 Q8.8 값의 표현 오차나 일반 E8M7 분포의 정렬 무손실 보장이 아닙니다.',
            'source_sha256':source_hashes}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
