#!/usr/bin/env python3
# 6개 shape/seed로 streaming KV RTL의 hidden/logit을 Python oracle과 대조한다.
# random seed를 고정해 재현하며 head/layer/FFN/선택 연산을 바꿔 한 예제만 맞는 오류를 찾는다.
# 문자열로 만드는 SV는 실제 HDL testbench다. 이 주석 작업은 생성 문자열을 변경하지 않는다.
"""여러 model shape와 seed에서 K/V-cache RTL을 Python 정수 기준과 대조한다.

각 case는 가중치·embedding을 seed로 생성하고, 같은 입력 token을 한 개씩
SystemVerilog streaming top에 넣는다. 매 입력 위치에서 hidden과 vocabulary
logits를 Python full-context Q8.8 결과와 비교한다. 이는 선택한 작은 설정의
parameter sweep이지 모든 가능한 parameter 조합의 증명은 아니다.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RTL = ROOT / "rtl"
OUT = ROOT / "build" / "reports" / "rtl_parameter_sweep"

# 서로 다른 head 수, layer 수, odd/even FFN 폭, context, vocabulary,
# 선택 연산 조합을 포함한 작고 재현 가능한 smoke-sweep 구성이다.
CASES = [
    {"d_model": 4, "heads": 1, "d_ff": 5, "layers": 1, "vocab": 5,
     "tokens": 3, "bias": 0, "affine": 0, "gelu": 0, "seed": 7301},
    {"d_model": 4, "heads": 2, "d_ff": 7, "layers": 2, "vocab": 7,
     "tokens": 4, "bias": 1, "affine": 1, "gelu": 1, "seed": 7302},
    {"d_model": 6, "heads": 3, "d_ff": 5, "layers": 1, "vocab": 6,
     "tokens": 3, "bias": 1, "affine": 0, "gelu": 1, "seed": 7303},
    {"d_model": 8, "heads": 4, "d_ff": 12, "layers": 2, "vocab": 9,
     "tokens": 5, "bias": 0, "affine": 1, "gelu": 0, "seed": 7304},
    {"d_model": 8, "heads": 2, "d_ff": 3, "layers": 2, "vocab": 5,
     "tokens": 3, "bias": 1, "affine": 1, "gelu": 1, "seed": 7305},
    {"d_model": 4, "heads": 4, "d_ff": 9, "layers": 1, "vocab": 8,
     "tokens": 2, "bias": 1, "affine": 0, "gelu": 0, "seed": 7306},
]


# PATH/프로젝트 설치 후보에서 실행파일을 찾고 없으면 명시적으로 실패한다.
def find_tool(name: str, fallback: str) -> str:
    found = shutil.which(name)
    if found:
        return found
    path = Path(fallback)
    if path.exists():
        return str(path)
    suite = Path(os.environ.get("OSS_CAD_SUITE", Path.home() / "Documents" / "ChatGPT" / "oss-cad-suite"))
    candidate = suite / "bin" / f"{name}.exe"
    if candidate.exists():
        return str(candidate)
    raise FileNotFoundError(f"{name} 실행 파일을 찾을 수 없습니다. README의 도구 설정을 확인하세요.")


# 고정 seed 소형 Q8.8 matrix fixture. diagonal 옵션은 연산이 사라지지 않는 주대각 성분을 준다.
def matrix(rng: random.Random, rows: int, cols: int, diagonal: bool = True) -> list[list[int]]:
    values = []
    for row in range(rows):
        current = []
        for col in range(cols):
            if diagonal and row == col:
                current.append(192 + rng.randint(-32, 32))
            else:
                current.append(rng.randint(-24, 24))
        values.append(current)
    return values


# sweep shape/bias/affine/GELU 설정으로 weight/embedding/ID를 seed 고정 생성한다.
def make_model(case: dict[str, int]) -> tuple[dict[str, Any], list[int]]:
    rng = random.Random(case["seed"])
    d, f, layers, vocab, tokens = (case[k] for k in ("d_model", "d_ff", "layers", "vocab", "tokens"))
    data: dict[str, Any] = {
        "config": {
            "d_model": d, "heads": case["heads"], "d_ff": f,
            "context_length": tokens, "score_scale_q8": round(256 / math.sqrt(d // case["heads"])),
            "activation": "gelu" if case["gelu"] else "relu",
        },
        "vocab": [chr(65 + index) for index in range(vocab)],
        "weights": {
            "token_embedding": [[rng.randint(-80, 80) for _ in range(d)] for _ in range(vocab)],
            "position_embedding": [[rng.randint(-35, 35) for _ in range(d)] for _ in range(tokens)],
            "lm_head": matrix(rng, d, vocab, diagonal=False),
            "layers": [],
        },
    }
    if case["bias"]:
        data["weights"]["lm_bias"] = [rng.randint(-12, 12) for _ in range(vocab)]
    for _ in range(layers):
        layer: dict[str, Any] = {
            "wq": matrix(rng, d, d), "wk": matrix(rng, d, d),
            "wv": matrix(rng, d, d), "wo": matrix(rng, d, d),
            "w1": matrix(rng, d, f), "w2": matrix(rng, f, d),
        }
        if case["bias"]:
            layer.update({
                "bq": [rng.randint(-10, 10) for _ in range(d)],
                "bk": [rng.randint(-10, 10) for _ in range(d)],
                "bv": [rng.randint(-10, 10) for _ in range(d)],
                "bo": [rng.randint(-10, 10) for _ in range(d)],
                "b1": [rng.randint(-10, 10) for _ in range(f)],
                "b2": [rng.randint(-10, 10) for _ in range(d)],
            })
        if case["affine"]:
            layer.update({
                "ln1_gamma": [256 + rng.randint(-16, 16) for _ in range(d)],
                "ln1_beta": [rng.randint(-12, 12) for _ in range(d)],
                "ln2_gamma": [256 + rng.randint(-16, 16) for _ in range(d)],
                "ln2_beta": [rng.randint(-12, 12) for _ in range(d)],
            })
        data["weights"]["layers"].append(layer)
    ids = [rng.randrange(vocab) for _ in range(tokens)]
    return data, ids


# 중첩 row/layer list를 row-major 원소로 펼친다. SV word0은 최하위16bit다.
def flatten(value: Any) -> list[int]:
    if isinstance(value, list):
        result: list[int] = []
        for item in value:
            result.extend(flatten(item) if isinstance(item, list) else [int(item)])
        return result
    raise TypeError("packed RTL input은 list형이어야 합니다.")


# raw&0xffff를 index*16에 배치한 SV hex 대입 문자열. 값0이 bus 하위 bit다.
def packed_assignment(name: str, width: int, values: list[int]) -> str:
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if len(values) * 16 != width:
        raise ValueError(f"{name}: 예상 폭 {width}, 실제 원소 수 {len(values)}")
    packed = sum((int(value) & 0xFFFF) << (16 * index) for index, value in enumerate(values))
    return f"        {name} = {width}'h{packed:x};"


# 동일 입력/weight와 oracle 검사식의 실제 SV testbench 문자열을 만든다.
# 문자열 내부는 별도 HDL 코드이며 Python #주석 작업에서 이 생성 결과는 변하지 않는다.
def create_testbench(case: dict[str, int], model: dict[str, Any], ids: list[int], expected: list[tuple[list[int], list[int]]]) -> str:
    d, f, layers, vocab, tokens = (case[k] for k in ("d_model", "d_ff", "layers", "vocab", "tokens"))
    bits = max(1, math.ceil(math.log2(vocab)))
    # embedding/layer/LM raw 숫자. inference 중 새 학습을 하지 않는다.
    weights = model["weights"]
    arrays: dict[str, list[int]] = {
        "token_embedding_flat": flatten(weights["token_embedding"]),
        "position_embedding_flat": flatten(weights["position_embedding"]),
        "wq_layers_flat": flatten([layer["wq"] for layer in weights["layers"]]),
        "wk_layers_flat": flatten([layer["wk"] for layer in weights["layers"]]),
        "wv_layers_flat": flatten([layer["wv"] for layer in weights["layers"]]),
        "wo_layers_flat": flatten([layer["wo"] for layer in weights["layers"]]),
        "w1_layers_flat": flatten([layer["w1"] for layer in weights["layers"]]),
        "w2_layers_flat": flatten([layer["w2"] for layer in weights["layers"]]),
        "lm_head_flat": flatten(weights["lm_head"]),
    }
    for bus, key, length in (
        ("wq_bias_flat", "bq", layers*d), ("wk_bias_flat", "bk", layers*d),
        ("wv_bias_flat", "bv", layers*d), ("wo_bias_flat", "bo", layers*d),
        ("w1_bias_flat", "b1", layers*f), ("w2_bias_flat", "b2", layers*d),
        ("ln1_gamma_flat", "ln1_gamma", layers*d), ("ln1_beta_flat", "ln1_beta", layers*d),
        ("ln2_gamma_flat", "ln2_gamma", layers*d), ("ln2_beta_flat", "ln2_beta", layers*d),
    ):
        arrays[bus] = flatten([layer.get(key, [0] * (f if key == "b1" else d))
                               for layer in weights["layers"]])
        # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
        if len(arrays[bus]) != length:
            raise AssertionError(f"{bus} 폭 구성 오류")
    arrays["lm_bias_flat"] = flatten(weights.get("lm_bias", [0] * vocab))
    widths = {
        "token_embedding_flat": vocab*d*16, "position_embedding_flat": tokens*d*16,
        "wq_layers_flat": layers*d*d*16, "wk_layers_flat": layers*d*d*16,
        "wv_layers_flat": layers*d*d*16, "wo_layers_flat": layers*d*d*16,
        "w1_layers_flat": layers*d*f*16, "w2_layers_flat": layers*f*d*16,
        "lm_head_flat": d*vocab*16, "wq_bias_flat": layers*d*16,
        "wk_bias_flat": layers*d*16, "wv_bias_flat": layers*d*16,
        "wo_bias_flat": layers*d*16, "w1_bias_flat": layers*f*16,
        "w2_bias_flat": layers*d*16, "lm_bias_flat": vocab*16,
        "ln1_gamma_flat": layers*d*16, "ln1_beta_flat": layers*d*16,
        "ln2_gamma_flat": layers*d*16, "ln2_beta_flat": layers*d*16,
    }
    assignments = "\n".join(packed_assignment(name, widths[name], value) for name, value in arrays.items())
    declarations = "\n".join(f"    reg [{width-1}:0] {name};" for name, width in widths.items())
    expected_comments = "\n".join(
        f"        // 기대값 token {index}: hidden={hid}, logits={log}"
        for index, (hid, log) in enumerate(expected)
    )
    token_cases = "\n".join(
        f"                {index}: token_id = {bits}'d{token};"
        for index, token in enumerate(ids)
    )
    return f'''`timescale 1ns/1ps
module tb_sweep_case;
    localparam integer D={d}, F={f}, L={layers}, V={vocab}, T={tokens}, H={case["heads"]};
    localparam integer B={bits}, SCALE={model["config"]["score_scale_q8"]};
    reg clk, reset_n, start, result_ready;
    reg [B-1:0] token_id;
    wire input_ready, busy, done, result_valid, error;
    wire [D*16-1:0] hidden_flat;
    wire [V*16-1:0] logits_flat;
    wire [31:0] token_count, cycle_count, mac_count;
{declarations}
    integer timeout_count, token_index, channel_index;
    transformer_gpt_kvcache_seq #(
        .VOCAB_SIZE(V), .D_MODEL(D), .HEADS(H), .D_FF(F), .LAYERS(L),
        .MAX_TOKENS(T), .TOKEN_BITS(B), .SCORE_SCALE_Q8(SCALE),
        .ENABLE_BIAS({case["bias"]}), .ENABLE_NORM_AFFINE({case["affine"]}),
        .ENABLE_GELU({case["gelu"]})
    ) dut (
        .clk(clk), .reset_n(reset_n), .start(start), .input_ready(input_ready),
        .token_id(token_id), .token_embedding_flat(token_embedding_flat),
        .position_embedding_flat(position_embedding_flat), .wq_layers_flat(wq_layers_flat),
        .wk_layers_flat(wk_layers_flat), .wv_layers_flat(wv_layers_flat),
        .wo_layers_flat(wo_layers_flat), .w1_layers_flat(w1_layers_flat),
        .w2_layers_flat(w2_layers_flat), .lm_head_flat(lm_head_flat),
        .wq_bias_flat(wq_bias_flat), .wk_bias_flat(wk_bias_flat),
        .wv_bias_flat(wv_bias_flat), .wo_bias_flat(wo_bias_flat),
        .w1_bias_flat(w1_bias_flat), .w2_bias_flat(w2_bias_flat), .lm_bias_flat(lm_bias_flat),
        .ln1_gamma_flat(ln1_gamma_flat), .ln1_beta_flat(ln1_beta_flat),
        .ln2_gamma_flat(ln2_gamma_flat), .ln2_beta_flat(ln2_beta_flat),
        .result_ready(result_ready), .hidden_flat(hidden_flat), .logits_flat(logits_flat),
        .busy(busy), .done(done), .result_valid(result_valid), .error(error),
        .token_count(token_count), .cycle_count(cycle_count), .mac_count(mac_count)
    );
    always #5 clk = ~clk;
    initial begin
        clk=0; reset_n=0; start=0; result_ready=1; token_id=0;
{assignments}
        #12; reset_n=1;
        {expected_comments}
        for (token_index=0; token_index<T; token_index=token_index+1) begin
            @(negedge clk);
            timeout_count=0;
            while (input_ready !== 1'b1 && timeout_count < 10) begin
                @(negedge clk); timeout_count=timeout_count+1;
            end
            if (input_ready !== 1'b1) $fatal(1, "input_ready timeout before token %0d", token_index);
            case (token_index)
{token_cases}
            endcase
            start=1; @(negedge clk); start=0;
            timeout_count=0;
            while (done !== 1'b1 && timeout_count < 200000) begin
                @(negedge clk); timeout_count=timeout_count+1;
            end
            if (done !== 1'b1 || result_valid !== 1'b1 || error !== 1'b0)
                $fatal(1, "stream failed token=%0d done=%b valid=%b error=%b", token_index, done, result_valid, error);
            $write("SWEEP token=%0d hidden", token_index);
            for (channel_index=0; channel_index<D; channel_index=channel_index+1)
                $write(" %0d", $signed(hidden_flat[channel_index*16 +: 16]));
            $write(" logits");
            for (channel_index=0; channel_index<V; channel_index=channel_index+1)
                $write(" %0d", $signed(logits_flat[channel_index*16 +: 16]));
            $write("\\n");
        end
        $display("PASS sweep tokens=%0d model=%0d heads=%0d layers=%0d", T, D, H, L);
        $finish;
    end
endmodule
'''


# 한 sweep case compile/simulate 후 모든 실제값과 oracle를 비교하고 입력/model/TB hash를 기록한다.
def run_case(index: int, case: dict[str, int], compiler: str, simulator: str) -> dict[str, Any]:
    # Import at runtime so this script can also be run as a file from the repo root.
    sys.path.insert(0, str(ROOT))
    from model.gpt_q88 import forward_q88

    model, ids = make_model(case)
    # Python oracle 정답. 실제 RTL 숫자와 전체 비교한다.
    expected = []
    for position in range(len(ids)):
        hidden, logits = forward_q88(model, ids[:position + 1])
        expected.append((hidden[-1], logits[-1]))
    folder = OUT / f"case_{index:02d}_seed_{case['seed']}"
    folder.mkdir(parents=True, exist_ok=True)
    tb = create_testbench(case, model, ids, expected)
    tb_path = folder / "tb_sweep_case.sv"
    tb_path.write_text(tb, encoding="utf-8")
    executable = folder / "sweep_case.vvp"
    # 컴파일할 RTL/core/TB 목록. top을 지정하여 의도한 회로를 검사한다.
    sources = [RTL / "dram_pim_pu_synth.sv", RTL / "dram_pim_vmm_bank.sv",
               RTL / "transformer_gpt_kvcache_seq.sv", tb_path]
    # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
    # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
    compiled = subprocess.run([compiler, "-g2012", "-s", "tb_sweep_case", "-o", str(executable),
                               *map(str, sources)], cwd=ROOT, text=True, encoding="utf-8",
                              errors="replace", capture_output=True)
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if compiled.returncode:
        raise RuntimeError(f"case {index} compile failed:\n{compiled.stderr[-5000:]}")
    # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
    # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
    simulation = subprocess.run([simulator, str(executable)], cwd=ROOT, text=True,
                                encoding="utf-8", errors="replace", capture_output=True,
                                timeout=60)
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if simulation.returncode:
        raise RuntimeError(f"case {index} simulation failed:\n{simulation.stdout}\n{simulation.stderr}")
    observed: list[tuple[list[int], list[int]]] = []
    for line in simulation.stdout.splitlines():
        if not line.startswith("SWEEP token="):
            continue
        parts = line.split()
        # SWEEP token=N hidden h0 ... logits l0 ...
        try:
            hidden_at, logits_at = parts.index("hidden"), parts.index("logits")
            observed.append((list(map(int, parts[hidden_at+1:logits_at])),
                             list(map(int, parts[logits_at+1:]))))
        except (ValueError, IndexError) as error:
            raise RuntimeError(f"case {index} output parse failed: {line}") from error
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if observed != expected:
        raise AssertionError(f"case {index}, seed {case['seed']} mismatch\nexpected={expected}\nobserved={observed}")
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if f"PASS sweep tokens={case['tokens']}" not in simulation.stdout:
        raise AssertionError(f"case {index} lacks PASS marker")
    serialized_model = json.dumps(model, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "case": index, "seed": case["seed"], "config": case,
        "input_token_ids": ids, "positions_checked": len(ids),
        "hidden_vectors_exact": sum(len(row[0]) for row in observed),
        "logits_exact": sum(len(row[1]) for row in observed),
        "model_sha256": hashlib.sha256(serialized_model).hexdigest(),
        "testbench_sha256": hashlib.sha256(tb.encode("utf-8")).hexdigest(),
        "status": "passed",
    }


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    compiler = find_tool("iverilog", "C:/iverilog/bin/iverilog.exe")
    simulator = find_tool("vvp", "C:/iverilog/bin/vvp.exe")
    OUT.mkdir(parents=True, exist_ok=True)
    results = [run_case(index, case, compiler, simulator) for index, case in enumerate(CASES, 1)]
    report = {
        "title_ko": "SystemVerilog K/V-cache parameter 및 seed sweep",
        "claim_boundary_ko": "선택한 6개 소형 설정, 6개 seed의 exact simulation 결과다. 가능한 모든 parameter 조합이나 FPGA timing을 증명하지 않는다.",
        "cases_passed": len(results),
        "positions_checked": sum(item["positions_checked"] for item in results),
        "hidden_vectors_exact": sum(item["hidden_vectors_exact"] for item in results),
        "logits_exact": sum(item["logits_exact"] for item in results),
        "results": results,
    }
    report_path = OUT / "rtl_parameter_sweep.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("cases_passed", "positions_checked", "hidden_vectors_exact", "logits_exact")}, ensure_ascii=False))
    print(f"결과: {report_path}")
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"실패: {error}", file=sys.stderr)
        raise SystemExit(1)
