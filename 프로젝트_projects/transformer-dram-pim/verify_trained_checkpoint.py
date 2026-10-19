#!/usr/bin/env python3
# 학습 Q8.8 memory 이미지를 SV testbench에 넣고 모든 logit을 Python oracle과 exact 비교한다.
# prompt는 Python이 ID로 바꾸며 SV $readmemh는 같은 bit pattern을 읽는다. core 지원 옵션을 학습 정의와 맞춘다.
"""학습해 내보낸 Q8.8 checkpoint를 실제 SystemVerilog GPT top에 넣어 검증한다."""

from __future__ import annotations

import re
import os
import shutil
import subprocess
import sys
from pathlib import Path

from model.gpt_q88 import forward_q88, load_checkpoint, write_mem_files

ROOT = Path(__file__).resolve().parent
RTL = ROOT / "rtl"
BUILD = ROOT / "build" / "checkpoint_verify"
DEFAULT_CHECKPOINT = ROOT / "output" / "tiny_gpt_full_ops_qat" / "tiny_gpt_qat_q88.json"


# Icarus compile/vvp 실행 경로를 찾는다. 도구 발견 자체가 FPGA 검증 성공은 아니다.
def tool(name: str) -> str:
    found = shutil.which(name)
    if found:
        return found
    fallback = Path(f"C:/iverilog/bin/{name}.exe")
    if fallback.exists():
        return str(fallback)
    suite_root = Path(os.environ.get(
        "OSS_CAD_SUITE", Path.home() / "Documents" / "ChatGPT" / "oss-cad-suite"
    ))
    suite_tool = suite_root / "bin" / f"{name}.exe"
    if suite_tool.exists():
        return str(suite_tool)
    raise FileNotFoundError(f"{name} 실행 파일이 없습니다. Icarus Verilog를 설치하세요.")


# checkpoint memory/ID/context/core 설정의 TB와 가정 MAC/traffic 정답을 만든다.
def generate_testbench(
    model: dict, prompt: str, destination: Path, sequential: bool = False,
    mem_dir: str = "output/tiny_gpt_demo/mem",
) -> tuple[list[int], dict[str, int]]:
    # model config의 shape/수치 규칙. config와 weight가 같아야 같은 모델이다.
    cfg = model["config"]
    # embedding/layer/LM raw 숫자. inference 중 새 학습을 하지 않는다.
    weights = model["weights"]
    # ID 순서 문자 목록. score index/선택 ID와 출력 문자의 대응표다.
    vocab = model["vocab"]
    # prompt 문자->ID 사전. 어휘 밖 문자는 unknown ID로 바뀐다.
    encoder = {char: index for index, char in enumerate(vocab)}
    ids = [encoder.get(char, model.get("unknown_token_id", 0)) for char in prompt]
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if not ids:
        raise ValueError("prompt는 비어 있을 수 없습니다.")
    ids = ids[-int(cfg["context_length"]):]
    t = len(ids)
    # Value projection. attention 확률로 가중 합산할 내용이다.
    v = int(cfg["vocab_size"])
    d = int(cfg["d_model"])
    heads = int(cfg["heads"])
    f = int(cfg["d_ff"])
    layers = int(cfg["layers"])
    token_bits = max(1, (v - 1).bit_length())
    scale = int(cfg["score_scale_q8"])
    mem_dir = Path(mem_dir).as_posix()
    # 생성 SV source 문장 목록. list 안 문자열은 실제 별도 HDL 코드다.
    lines = [
        "`timescale 1ns/1ps",
        "module tb_trained_checkpoint;",
        f"localparam integer T={t}, V={v}, D={d}, H={heads}, F={f}, L={layers}, TOKEN_BITS={token_bits};",
        f"localparam integer CONTEXT={int(cfg['context_length'])}, SCORE_SCALE={scale};",
        "reg [T*TOKEN_BITS-1:0] token_ids_flat;",
        "reg [V*D*16-1:0] token_embedding_flat;",
        "reg [T*D*16-1:0] position_embedding_flat;",
        "reg [L*D*D*16-1:0] wq_layers_flat, wk_layers_flat, wv_layers_flat, wo_layers_flat;",
        "reg [L*D*F*16-1:0] w1_layers_flat;",
        "reg [L*F*D*16-1:0] w2_layers_flat;",
        "reg [D*V*16-1:0] lm_head_flat;",
        "reg [15:0] token_emb_mem [0:V*D-1];",
        "reg [15:0] position_mem [0:CONTEXT*D-1];",
        "reg [15:0] lm_head_mem [0:D*V-1];",
        "wire [T*D*16-1:0] embedding_sum_flat, hidden_flat;",
        "wire [T*V*16-1:0] logits_flat;",
        "wire [31:0] cpu_words, pim_words, macs, pu_ops;",
        "integer i, token, channel, vocabulary_id;",
    ]
    if sequential:
        lines.extend([
            "reg clk, reset_n, start;",
            "wire busy, done;",
            "wire [31:0] cycle_count, sequential_macs;",
            "always #5 clk = ~clk;",
        ])
    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for layer in range(layers):
        for name, count in (("wq", d*d), ("wk", d*d), ("wv", d*d), ("wo", d*d),
                            ("w1", d*f), ("w2", f*d)):
            lines.append(f"reg [15:0] {name}_{layer}_mem [0:{count-1}];")
    core_module = (
        "transformer_gpt_language_model_seq" if sequential
        else "transformer_gpt_language_model_comb"
    )
    lines.extend([
        f"{core_module} #(",
        "  .TOKENS(T), .VOCAB_SIZE(V), .D_MODEL(D), .HEADS(H), .D_FF(F), .LAYERS(L),",
        "  .SCORE_SCALE_Q8(SCORE_SCALE), .TOKEN_BITS(TOKEN_BITS)",
        ") dut (",
    ])
    if sequential:
        lines.extend([
            "  .clk(clk), .reset_n(reset_n), .start(start),",
        ])
    lines.extend([
        "  .token_ids_flat(token_ids_flat), .token_embedding_flat(token_embedding_flat),",
        "  .position_embedding_flat(position_embedding_flat),",
        "  .wq_layers_flat(wq_layers_flat), .wk_layers_flat(wk_layers_flat),",
        "  .wv_layers_flat(wv_layers_flat), .wo_layers_flat(wo_layers_flat),",
        "  .w1_layers_flat(w1_layers_flat), .w2_layers_flat(w2_layers_flat),",
        "  .lm_head_flat(lm_head_flat), .embedding_sum_flat(embedding_sum_flat),",
        "  .hidden_flat(hidden_flat), .logits_flat(logits_flat),",
    ])
    if sequential:
        lines.extend([
            "  .busy(busy), .done(done), .cycle_count(cycle_count), .mac_count(sequential_macs)",
        ])
    else:
        lines.extend([
            "  .cpu_boundary_words(cpu_words), .pim_boundary_words(pim_words),",
            "  .mac_count(macs), .nonvmm_vector_ops(pu_ops)",
        ])
    lines.extend([
        ");",
        "initial begin",
    ])
    if sequential:
        lines.extend([
            "  clk = 1'b0; reset_n = 1'b0; start = 1'b0;",
        ])
    lines.extend([
        f'  $readmemh("{mem_dir}/token_embedding.mem", token_emb_mem);',
        f'  $readmemh("{mem_dir}/position_embedding.mem", position_mem);',
        f'  $readmemh("{mem_dir}/lm_head.mem", lm_head_mem);',
    ])
    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for layer in range(layers):
        for name, _ in (("wq", d*d), ("wk", d*d), ("wv", d*d), ("wo", d*d),
                        ("w1", d*f), ("w2", f*d)):
            lines.append(f'  $readmemh("{mem_dir}/layer_{layer}_{name}.mem", {name}_{layer}_mem);')
    lines.extend([
        f"  token_ids_flat = {{T*TOKEN_BITS{{1'b0}}}};",
        f"  for (i=0; i<V*D; i=i+1) token_embedding_flat[i*16 +: 16] = token_emb_mem[i];",
        f"  for (i=0; i<T*D; i=i+1) position_embedding_flat[i*16 +: 16] = position_mem[i];",
        f"  for (i=0; i<D*V; i=i+1) lm_head_flat[i*16 +: 16] = lm_head_mem[i];",
    ])
    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for layer in range(layers):
        for name, count in (("wq", d*d), ("wk", d*d), ("wv", d*d), ("wo", d*d),
                            ("w1", d*f), ("w2", f*d)):
            lines.append(
                f"  for (i=0; i<{count}; i=i+1) {name}_layers_flat[({layer}*{count}+i)*16 +: 16] = {name}_{layer}_mem[i];"
            )
    for index, token_id in enumerate(ids):
        lines.append(f"  token_ids_flat[{index}*TOKEN_BITS +: TOKEN_BITS] = {token_bits}'d{token_id};")
    if sequential:
        lines.extend([
            "  #1; @(negedge clk); reset_n = 1'b1;",
            "  @(negedge clk); start = 1'b1;",
            "  @(negedge clk); start = 1'b0;",
            "  i = 0;",
            "  while ((done !== 1'b1) && (i < 100000)) begin @(negedge clk); i = i + 1; end",
            '  if (done !== 1\'b1) $fatal(1, "sequential checkpoint timeout");',
            '  if (sequential_macs !== 32\'d' + str(
                layers * (4*t*d*d + 2*t*t*d + 2*t*d*f) + t*d*v
            ) + ') $fatal(1, "sequential MAC count mismatch: %0d", sequential_macs);',
            '  $display("CKPT_SEQ cycles=%0d macs=%0d", cycle_count, sequential_macs);',
        ])
    else:
        lines.append("  #1;")
    lines.extend([
        "  for (token=0; token<T; token=token+1) begin",
        "    $write(\"CKPT_LOGITS token=%0d\", token);",
        "    for (vocabulary_id=0; vocabulary_id<V; vocabulary_id=vocabulary_id+1)",
        "      $write(\" %0d\", $signed(logits_flat[(token*V+vocabulary_id)*16 +: 16]));",
        "    $write(\"\\n\");",
        "  end",
    ])
    if sequential:
        lines.append('  $display("CKPT_RESULT cycles=%0d mac=%0d", cycle_count, sequential_macs);')
    else:
        lines.append('  $display("CKPT_RESULT cpu=%0d pim=%0d mac=%0d pu=%0d", cpu_words, pim_words, macs, pu_ops);')
    lines.extend(["  $finish;", "end", "endmodule"])
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")

    core_cpu = layers * (24*t*d + 4*t*f + 4*t*t)
    expected_stats = {
        "cpu": core_cpu + 3*t*d + t*d + d*v + t*v,
        "pim": (t*token_bits + 15)//16 + t*v,
        "mac": layers * (4*t*d*d + 2*t*t*d + 2*t*d*f) + t*d*v,
        "pu": layers*t*(heads+5) + t,
    }
    return ids, expected_stats


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    # 정수 inference JSON config/vocab/weight. 저장한 숫자를 읽고 새 학습을 하지 않는다.
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    # 입력 문자열->ID. prompt 마지막 score가 첫 생성 token을 예측한다.
    parser.add_argument("--prompt", default="ROMEO:")
    # 비교/검증 JSON 저장 경로. 실패 조건은 정상 결과로 기록하지 않아야 한다.
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "reports" / "trained_rtl_logits.json")
    # 같은 context를 shared-MAC seq RTL로 검증. 기본 comb과 수학 결과는 같아야 한다.
    parser.add_argument("--sequential", action="store_true",
                        help="cycle-accurate resource-shared RTL top으로 검증")
    args = parser.parse_args()
    model = load_checkpoint(args.checkpoint)
    memory_path = args.checkpoint.resolve().parent / "mem"
    if not memory_path.exists():
        write_mem_files(model, memory_path)
    try:
        memory_dir = memory_path.relative_to(ROOT).as_posix()
    except ValueError as error:
        raise ValueError("Icarus $readmemh 검증용 checkpoint는 저장소 내부 경로를 사용해야 합니다.") from error
    BUILD.mkdir(parents=True, exist_ok=True)
    tb = BUILD / ("tb_trained_checkpoint_seq.sv" if args.sequential else "tb_trained_checkpoint.sv")
    ids, expected_stats = generate_testbench(model, args.prompt, tb, args.sequential, memory_dir)
    actual_ids, expected_logits = forward_q88(model, ids)
    compiler = tool("iverilog")
    simulator = tool("vvp")
    image = BUILD / ("trained_checkpoint_seq.vvp" if args.sequential else "trained_checkpoint.vvp")
    source_files = ["rtl/dram_pim_pu_synth.sv"]
    if args.sequential:
        source_files.append("rtl/transformer_gpt_language_model_seq.sv")
    else:
        source_files.extend([
            "rtl/dram_pim_vmm_bank.sv",
            "rtl/transformer_decoder_mha_pim_comb.sv",
            "rtl/transformer_gpt_decoder_stack_comb.sv",
            "rtl/transformer_gpt_language_model_comb.sv",
        ])
    source_files.append(str(tb.relative_to(ROOT)).replace("\\", "/"))
    # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
    # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
    compile_proc = subprocess.run(
        [compiler, "-g2012", "-s", "tb_trained_checkpoint", "-o", str(image), *source_files],
        cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True,
    )
    if compile_proc.stdout:
        print(compile_proc.stdout, end="")
    if compile_proc.stderr:
        print(compile_proc.stderr, end="", file=sys.stderr)
    if compile_proc.returncode:
        return compile_proc.returncode
    print("학습 checkpoint RTL 시뮬레이션 중...", flush=True)
    # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
    # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
    simulation = subprocess.run(
        [simulator, str(image)], cwd=ROOT, text=True,
        encoding="utf-8", errors="replace", capture_output=True,
    )
    print(simulation.stdout, end="")
    if simulation.stderr:
        print(simulation.stderr, end="", file=sys.stderr)
    if simulation.returncode:
        return simulation.returncode

    # SV의 실제 raw 후보 점수들. 소수 오차 허용 없이 정수 그대로 비교한다.
    actual_logits: dict[int, list[int]] = {}
    actual_stats: dict[str, int] | None = None
    sequential_stats: dict[str, int] | None = None
    for line in simulation.stdout.splitlines():
        match = re.fullmatch(r"CKPT_LOGITS token=(\d+) (-?\d+(?: -?\d+)*)", line.strip())
        if match:
            actual_logits[int(match.group(1))] = [int(value) for value in match.group(2).split()]
        match = re.fullmatch(r"CKPT_RESULT cpu=(\d+) pim=(\d+) mac=(\d+) pu=(\d+)", line.strip())
        if match:
            actual_stats = dict(zip(("cpu", "pim", "mac", "pu"), map(int, match.groups())))
        match = re.fullmatch(r"CKPT_RESULT cycles=(\d+) mac=(\d+)", line.strip())
        if match:
            sequential_stats = dict(zip(("cycles", "mac"), map(int, match.groups())))

    # 위치별 oracle 점수 사전. parsed 실제 위치/숫자와 완전히 비교한다.
    expected_map = {index: row for index, row in enumerate(expected_logits)}
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if actual_logits != expected_map:
        raise AssertionError(f"학습 Q8.8 checkpoint RTL과 Python 결과 불일치\nRTL={actual_logits}\nPython={expected_map}")
    if args.sequential:
        # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
        if sequential_stats is None or sequential_stats["cycles"] <= 0 or sequential_stats["mac"] != expected_stats["mac"]:
            raise AssertionError(f"순차 RTL counter 오류: {sequential_stats}, 기대 MAC={expected_stats['mac']}")
        actual_stats = sequential_stats
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    elif actual_stats != expected_stats:
        raise AssertionError(f"RTL 계수와 Python 예상값 불일치: {actual_stats} != {expected_stats}")
    report = {
        "prompt": args.prompt,
        "token_ids": ids,
        "rtl_logits_q88": [actual_logits[index] for index in range(len(actual_logits))],
        "q88_python_logits": expected_logits,
        "counts": actual_stats,
        "all_logits_exact_match": True,
        "rtl_kind": "resource_shared_sequential" if args.sequential else "combinational_functional",
        "note_ko": "float 학습 checkpoint를 Q8.8로 내보낸 뒤, 같은 가중치를 SystemVerilog token embedding·multi-head decoder·LM head에 넣어 정수 logits가 정확히 일치함을 확인했다.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(__import__("json").dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: 학습 가중치로 계산한 logits {sum(len(row) for row in expected_logits)}개가 RTL과 Python에서 정확히 일치합니다.")
    print(f"결과 JSON: {args.output}")
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    raise SystemExit(main())
