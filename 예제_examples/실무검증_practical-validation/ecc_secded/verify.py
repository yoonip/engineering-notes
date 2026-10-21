"""Use a literal generator codebook and radius-one oracle to verify the SECDED codec."""
import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import platform
import sys

sys.dont_write_bytecode = True  # 검사 중 공개 코드 폴더에 __pycache__를 만들지 않습니다.
from codec import decode, encode, MUTATIONS

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, value):
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n").encode("utf-8"))


class ContractError(ValueError):
    pass


class Checks:
    def __init__(self):
        self.counts = Counter()
        self.last = None

    def check(self, group, actual, expected, context=None):
        self.last = {"group":group,"context":context,"actual":actual,"expected":expected}
        if actual != expected:
            raise ContractError("comparison failed: "+group)
        self.counts[group] += 1  # 성공한 비교만 세며 -O로 사라지는 assert를 사용하지 않습니다.


def reference_codebook(basis):
    result = []
    for data in range(256):
        word = 0
        for bit in range(8):
            if data & (1 << bit):
                word ^= basis[bit]  # 구현의 위치별 parity 계산 대신 고정 generator 기저를 XOR합니다.
        result.append(word)
    return result


def radius_oracle(codebook):
    lookup = {}
    for data, word in enumerate(codebook):
        for position in range(14):
            received = word if position == 0 else word ^ (1 << (position-1))
            if received in lookup:
                raise ContractError("radius-one neighborhoods overlap")
            lookup[received] = ("clean" if position == 0 else "corrected", data, word, position or None)
    return lookup


def core_fields(result):
    return (result.status, result.data, result.corrected_word, result.corrected_position)


def verify(checks, fixture, mutation):
    basis = [int(word,16) for word in fixture["basis_words_hex"]]
    codebook = reference_codebook(basis)
    checks.check("codebook_unique", len(set(codebook)), 256)
    distance = min((left^right).bit_count() for left,right in combinations(codebook,2))
    checks.check("codebook_distance", distance, 4)
    lookup = radius_oracle(codebook)
    checks.check("radius_neighborhoods", len(lookup), 3584)
    for item in fixture["encoded_literals"]:
        checks.check("literal_encoding", codebook[item["data"]], int(item["word_hex"],16),item["data"])
    for data, expected in enumerate(codebook):
        checks.check("encoder_256",encode(data,mutation),expected,{"data":data})
        checks.check("clean_256",core_fields(decode(expected,mutation)),("clean",data,expected,None),{"data":data})
    for received in range(8192):
        expected = lookup.get(received,("uncorrectable",None,None,None))
        checks.check("decoder_all_8192",core_fields(decode(received,mutation)),expected,{"received":received})
    for data, word in enumerate(codebook):
        for position in range(1,14):
            received = word ^ (1 << (position-1))
            result = decode(received,mutation)
            expected = {"status":"corrected","data":data,"corrected_word":word,
                "corrected_position":position,"syndrome":position if position <= 12 else 0,"overall_bad":True}
            checks.check("single_3328",asdict(result),expected,{"data":data,"position":position})
        for left,right in combinations(range(1,14),2):
            received = word ^ (1 << (left-1)) ^ (1 << (right-1))
            syndrome = (left if left<=12 else 0) ^ (right if right<=12 else 0)
            expected = {"status":"uncorrectable","data":None,"corrected_word":None,
                "corrected_position":None,"syndrome":syndrome,"overall_bad":False}
            checks.check("double_19968",asdict(decode(received,mutation)),expected,{"data":data,"positions":[left,right]})
    outside = []
    for item in fixture["outside_guarantee"]:
        mask = sum(1 << (position-1) for position in item["flips"])
        received = codebook[item["data"]] ^ mask
        checks.check("outside_input_literal",received,int(item["received_hex"],16),item["name"])
        result = asdict(decode(received,mutation))
        checks.check("outside_result_literal",result,item["expected"],item["name"])
        outside.append({"name":item["name"],"original_data":item["data"],"flips":item["flips"],
            "received":received,"observed":result,"original_data_recovered":result["data"]==item["data"]})
    for name, function, maximum in (("encode",encode,255),("decode",decode,8191)):
        for value in (True,False,-1,maximum+1,1.0,None,"1",[],{}):
            try:
                function(value,mutation)
                rejected = False
            except ValueError:
                rejected = True
            checks.check("invalid_inputs",rejected,True,{"function":name,"input":value})
    # 완전한 다른 위치의 codeword를 받는 주소 오배달은 자료 parity만으로 구별하지 못합니다.
    wrong_address = asdict(decode(codebook[1],mutation))
    checks.check("wrong_address_limit",wrong_address,{"status":"clean","data":1,"corrected_word":4103,
        "corrected_position":None,"syndrome":0,"overall_bad":False})
    return {"minimum_code_distance":distance,"valid_codewords":len(codebook),"radius_one_words":len(lookup),
        "outside_guarantee":outside,"wrong_address_limit":{"wanted_data":0,"received_data":1,"observed":wrong_address}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",required=True,type=Path)
    parser.add_argument("--mutation",choices=MUTATIONS,default="none")
    args = parser.parse_args()
    if args.out.exists():
        parser.error("--out must be a new directory")
    args.out.mkdir(parents=True)
    fixture = json.loads((HERE/"fixtures.json").read_text(encoding="utf-8"))
    inputs = {"fixture":fixture,"payloads":list(range(256)),"single_positions":list(range(1,14)),
        "double_position_pairs":list(combinations(range(1,14),2)),"all_received_words":8192}
    save_json(args.out/"input_manifest.json",inputs)
    checks = Checks()
    report = {"scope":fixture["scope"],"environment":{"python":sys.version,"platform":platform.platform(),
        "executable":sys.executable,"optimize":sys.flags.optimize,"argv":sys.argv},"mutation":args.mutation,
        "source_sha256":{name:digest(HERE/name) for name in ("codec.py","verify.py","fixtures.json")},
        "input_sha256":digest(args.out/"input_manifest.json")}
    try:
        report["observations"] = verify(checks,fixture,args.mutation)
        report["status"], code = "PASS", 0
    except Exception as error:
        report.update(status="FAIL",error=type(error).__name__+": "+str(error),failed_comparison=checks.last)
        code = 1
    report["checks_passed"] = dict(checks.counts)
    report["check_count"] = sum(checks.counts.values())
    save_json(args.out/"report.json",report)
    print(json.dumps({"status":report["status"],"mutation":args.mutation,"checks":report["check_count"],
        "error":report.get("error")},ensure_ascii=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
