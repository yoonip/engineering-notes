#!/usr/bin/env python3
# prompt->score->greedy 선택->재입력의 SV 생성 반복을 Python oracle과 검증하는 host/TB 도구다.
# 기본은 전체 context seq, --kvcache-rtl은 layer별 K/V를 보존하는 incremental core다.
# 같은 score면 낮은 ID를 선택하는 argmax는 core 바깥 TB 역할이다. 실제 UART board 측정은 별도다.
"""학습 checkpoint로 sequential SystemVerilog autoregressive generation을 검증한다.

기본 RTL 경로는 거래마다 전체 context를 재계산한다. --kvcache-rtl 경로는
RTL 내부에 layer별 K/V를 보존하고 현재 token만 incremental 처리한다.
두 경우 모두 유효 prefix의 마지막 logits를 검사한 뒤 core 바깥 testbench가
greedy argmax로 다음 ID를 고르며, Python 정수 기준과 실제 회로 결과를 대조한다.
"""

from __future__ import annotations

import argparse
import json
import re
import os
import shutil
import sys
from pathlib import Path

from model.gpt_q88 import forward_q88, load_checkpoint, write_mem_files
# $finish가 출력하는 한글 파일 경로도 원본 bytes에서 UTF-8/CP949를 판별한다.
# logits·hidden·생성 ID·cycle 비교는 기존 숫자 검사식 그대로 실행한다.
from tools.console_text import run_console

ROOT = Path(__file__).resolve().parent
DEFAULT_CHECKPOINT = ROOT / "output" / "tiny_gpt_full_ops_qat" / "tiny_gpt_qat_q88.json"
BUILD = ROOT / "build" / "generation_verify"


# PATH/프로젝트 설치 후보에서 실행파일을 찾고 없으면 명시적으로 실패한다.
def find_tool(name: str) -> str:
    found = shutil.which(name)
    if found:
        return found
    for candidate in (Path(f"C:/iverilog/bin/{name}.exe"),
                      Path.home() / "Documents" / "ChatGPT" / "oss-cad-suite" / "bin" / f"{name}.exe"):
        if candidate.exists():
            return str(candidate)
    raise FileNotFoundError(f"{name}를 찾지 못했습니다. Icarus Verilog가 필요합니다.")


# 음수를 올바른 SV signed16 literal 문자열로 만들어 oracle 검사식의 부호를 보존한다.
def _signed16(value: int) -> str:
    return f"16'sd{value}" if value >= 0 else f"-16'sd{-value}"


# 동일 입력/weight와 oracle 검사식의 실제 SV testbench 문자열을 만든다.
# 문자열 내부는 별도 HDL 코드이며 Python #주석 작업에서 이 생성 결과는 변하지 않는다.
def create_testbench(model: dict, prompt_ids: list[int], new_tokens: int,
                     destination: Path, mem_dir: str) -> tuple[list[int], list[list[int]]]:
    # model config의 shape/수치 규칙. config와 weight가 같아야 같은 모델이다.
    cfg = model["config"]
    # ID 순서 문자 목록. score index/선택 ID와 출력 문자의 대응표다.
    vocab = model["vocab"]
    # embedding/layer/LM raw 숫자. inference 중 새 학습을 하지 않는다.
    weights = model["weights"]
    vocab_size = int(cfg["vocab_size"])
    context = int(cfg["context_length"])
    total = len(prompt_ids) + new_tokens
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if not prompt_ids:
        raise ValueError("prompt는 비어 있을 수 없습니다.")
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if total > context:
        raise ValueError(f"prompt token 수 + 생성 token 수({total})가 context_length({context})를 넘습니다.")
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if new_tokens < 1:
        raise ValueError("--tokens는 1 이상이어야 합니다.")

    # 정수 기준 모델에서 매 prefix의 전체 logits와 greedy 선택 token을 만든다.
    # TB는 같은 prefix를 sequential RTL에 공급한 다음 매 vocab logit을 검사한다.
    # prefix마다 Python greedy argmax ID. SV도 동일 tie 규칙이어야 한다.
    expected_tokens: list[int] = []
    # oracle의 모든 후보 점수. 선택 ID만 우연히 같은 경우를 넘어서 검증한다.
    expected_logits: list[list[int]] = []
    prefix = list(prompt_ids)
    for _ in range(new_tokens):
        _, all_logits = forward_q88(model, prefix)
        row = all_logits[-1]
        expected_logits.append(row)
        # 마지막 score로 고른 다음 문자 번호. vocab[next_id]가 실제 문자다.
        next_id = max(range(vocab_size), key=lambda index: row[index])
        expected_tokens.append(next_id)
        prefix.append(next_id)

    d_model = int(cfg["d_model"])
    heads = int(cfg["heads"])
    d_ff = int(cfg["d_ff"])
    layers = int(cfg["layers"])
    token_bits = max(1, (vocab_size - 1).bit_length())
    # 1/sqrt(head_dim)의 Q8.8 배율. raw128=0.5이며 clock 주기가 아니다.
    score_scale = int(cfg["score_scale_q8"])
    mem_dir = Path(mem_dir).as_posix()

    # 생성 SV source 문장 목록. list 안 문자열은 실제 별도 HDL 코드다.
    lines = [
        "`timescale 1ns/1ps",
        "module tb_trained_generation;",
        f"localparam integer T={total}, V={vocab_size}, D={d_model}, H={heads}, F={d_ff}, L={layers}, TOKEN_BITS={token_bits};",
        f"localparam integer CONTEXT={context}, SCORE_SCALE={score_scale};",
        "reg clk, reset_n, start;",
        "wire busy, done;",
        "wire [31:0] cycle_count, mac_count;",
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
        "reg [TOKEN_BITS-1:0] generated_ids [0:T-1];",
        "wire [T*D*16-1:0] embedding_sum_flat, hidden_flat;",
        "wire [T*V*16-1:0] logits_flat;",
        "integer i, layer_id, prefix_len, step_id, active_row, best_id, total_cycles;",
        "integer candidate, check_vocab;",
        "reg signed [15:0] best_logit;",
        "always #5 clk = ~clk;",
        "transformer_gpt_language_model_seq #( .TOKENS(T), .VOCAB_SIZE(V), .D_MODEL(D), .HEADS(H), .D_FF(F), .LAYERS(L), .SCORE_SCALE_Q8(SCORE_SCALE), .TOKEN_BITS(TOKEN_BITS) ) dut (",
        "  .clk(clk), .reset_n(reset_n), .start(start), .token_ids_flat(token_ids_flat),",
        "  .token_embedding_flat(token_embedding_flat), .position_embedding_flat(position_embedding_flat),",
        "  .wq_layers_flat(wq_layers_flat), .wk_layers_flat(wk_layers_flat), .wv_layers_flat(wv_layers_flat), .wo_layers_flat(wo_layers_flat),",
        "  .w1_layers_flat(w1_layers_flat), .w2_layers_flat(w2_layers_flat), .lm_head_flat(lm_head_flat),",
        "  .embedding_sum_flat(embedding_sum_flat), .hidden_flat(hidden_flat), .logits_flat(logits_flat),",
        "  .busy(busy), .done(done), .cycle_count(cycle_count), .mac_count(mac_count)",
        ");",
        "initial begin",
        "  clk=0; reset_n=0; start=0; total_cycles=0; token_ids_flat=0;",
        f'  $readmemh("{mem_dir}/token_embedding.mem", token_emb_mem);',
        f'  $readmemh("{mem_dir}/position_embedding.mem", position_mem);',
        f'  $readmemh("{mem_dir}/lm_head.mem", lm_head_mem);',
    ]
    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for layer in range(layers):
        for name, count in (("wq", d_model*d_model), ("wk", d_model*d_model),
                            ("wv", d_model*d_model), ("wo", d_model*d_model),
                            ("w1", d_model*d_ff), ("w2", d_ff*d_model)):
            lines.append(f"  reg [15:0] {name}_{layer}_mem [0:{count-1}];")
    # Verilog에서는 블록 안 reg 선언이 tool별로 제한될 수 있어 배열 선언은
    # 위의 initial 블록보다 앞에 있어야 한다. 아래 조립 단계에서 위치를 옮긴다.
    declarations = lines[-layers*6:] if layers else []
    if declarations:
        del lines[-layers*6:]
        insert_at = lines.index("integer candidate, check_vocab;") + 1
        lines[insert_at:insert_at] = declarations

    lines.extend([
        "  for (i=0; i<V*D; i=i+1) token_embedding_flat[i*16 +: 16]=token_emb_mem[i];",
        "  for (i=0; i<T*D; i=i+1) position_embedding_flat[i*16 +: 16]=position_mem[i];",
        "  for (i=0; i<D*V; i=i+1) lm_head_flat[i*16 +: 16]=lm_head_mem[i];",
    ])
    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for layer in range(layers):
        for name, count in (("wq", d_model*d_model), ("wk", d_model*d_model),
                            ("wv", d_model*d_model), ("wo", d_model*d_model),
                            ("w1", d_model*d_ff), ("w2", d_ff*d_model)):
            lines.append(f'  $readmemh("{mem_dir}/layer_{layer}_{name}.mem", {name}_{layer}_mem);')
            lines.append(f"  for (i=0; i<{count}; i=i+1) {name}_layers_flat[({layer}*{count}+i)*16 +: 16]={name}_{layer}_mem[i];")
    lines.extend([
        "  for (i=0; i<T; i=i+1) generated_ids[i]=0;",
    ])
    for index, token_id in enumerate(prompt_ids):
        lines.append(f"  generated_ids[{index}]={token_id};")
    lines.extend([
        "  #1; @(negedge clk); reset_n=1;",
        f"  prefix_len={len(prompt_ids)};",
        f"  for (step_id=0; step_id<{new_tokens}; step_id=step_id+1) begin",
        "    for (i=0; i<T; i=i+1) begin",
        "      if (i<prefix_len) token_ids_flat[i*TOKEN_BITS +: TOKEN_BITS]=generated_ids[i];",
        "      else token_ids_flat[i*TOKEN_BITS +: TOKEN_BITS]=0;",
        "    end",
        "    @(negedge clk); start=1;",
        "    @(negedge clk); start=0;",
        "    i=0; while ((done !== 1'b1) && (i < 300000)) begin @(negedge clk); i=i+1; end",
        '    if (done !== 1\'b1) $fatal(1, "generation transaction timeout at step %0d", step_id);',
        "    total_cycles=total_cycles+cycle_count; active_row=prefix_len-1;",
    ])
    for step_index, row in enumerate(expected_logits):
        lines.append(f"    if (step_id=={step_index}) begin")
        for vocab_id, expected in enumerate(row):
            lines.append(
                f"      if ($signed(logits_flat[(active_row*V+{vocab_id})*16 +: 16]) !== {_signed16(expected)}) "
                f"$fatal(1, \"logit mismatch step={step_index} vocab={vocab_id}: got %0d expected {expected}\", $signed(logits_flat[(active_row*V+{vocab_id})*16 +: 16]));"
            )
        lines.append("    end")
    lines.extend([
        "    best_id=0; best_logit=$signed(logits_flat[(active_row*V)*16 +: 16]);",
        "    for (candidate=1; candidate<V; candidate=candidate+1) begin",
        "      if ($signed(logits_flat[(active_row*V+candidate)*16 +: 16]) > best_logit) begin",
        "        best_logit=$signed(logits_flat[(active_row*V+candidate)*16 +: 16]); best_id=candidate;",
        "      end",
        "    end",
        "    case (step_id)",
    ])
    for step_index, expected_id in enumerate(expected_tokens):
        lines.append(f'      {step_index}: if (best_id != {expected_id}) $fatal(1, "next-token mismatch step=%0d got=%0d expected={expected_id}", step_id, best_id);')
    lines.extend([
        "      default: $fatal(1, \"unexpected generation step\");",
        "    endcase",
        '    $display("GEN_STEP step=%0d cycles=%0d macs=%0d token=%0d", step_id, cycle_count, mac_count, best_id);',
        "    generated_ids[prefix_len]=best_id; prefix_len=prefix_len+1;",
        "  end",
        '  $display("GEN_TOTAL cycles=%0d", total_cycles);',
        '  $write("GEN_TEXT "); for (i=0; i<prefix_len; i=i+1) $write("%0d ", generated_ids[i]); $write("\\n");',
        '  $display("PASS: sequential RTL generated token IDs and logits match Q8.8 reference");',
        "  $finish;",
        "end",
        "endmodule",
    ])
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return expected_tokens, expected_logits


# prompt부터 KV RTL을 incremental 실행하는 TB를 만든다. 매 hidden/logit/argmax를 oracle에 대조한다.
def create_kvcache_testbench(model: dict, prompt_ids: list[int], new_tokens: int,
                             destination: Path, mem_dir: str):
    """진짜 token-stream/KV-cache RTL을 prompt부터 차례로 검증하는 bench를 만든다."""
    cfg, vocab, weights = model["config"], model["vocab"], model["weights"]
    vocab_size = int(cfg["vocab_size"])
    context = int(cfg["context_length"])
    d_model, heads, d_ff, layers = (int(cfg[name]) for name in
                                    ("d_model", "heads", "d_ff", "layers"))
    token_bits = max(1, (vocab_size - 1).bit_length())
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if not prompt_ids or len(prompt_ids) + new_tokens - 1 > context:
        raise ValueError("prompt token 수 + 생성 token 수 - 1은 context_length 이하여야 합니다.")

    # 매 step마다 reference의 마지막 위치 hidden/logits와 다음 greedy token을 저장한다.
    # 입력 stream은 prompt 전체와 마지막 출력용 token 직전까지의 generated token이다.
    # prefix마다 Python greedy argmax ID. SV도 동일 tie 규칙이어야 한다.
    expected_tokens: list[int] = []
    # oracle의 모든 후보 점수. 선택 ID만 우연히 같은 경우를 넘어서 검증한다.
    expected_logits: list[list[int]] = []
    expected_hidden: list[list[int]] = []
    prefix = list(prompt_ids)
    input_ids = list(prompt_ids)
    for generation_index in range(new_tokens):
        hidden, logits = forward_q88(model, prefix)
        expected_hidden.append(hidden[-1])
        expected_logits.append(logits[-1])
        # 마지막 score로 고른 다음 문자 번호. vocab[next_id]가 실제 문자다.
        next_id = max(range(vocab_size), key=lambda index: logits[-1][index])
        expected_tokens.append(next_id)
        if generation_index + 1 < new_tokens:
            prefix.append(next_id)
            input_ids.append(next_id)

    input_hidden: list[list[int]] = []
    input_logits: list[list[int]] = []
    seen: list[int] = []
    for token_id in input_ids:
        seen.append(token_id)
        hidden, logits = forward_q88(model, seen)
        input_hidden.append(hidden[-1])
        input_logits.append(logits[-1])
    # 위 생성 reference와 transaction별 마지막 위치 reference가 서로 독립적으로
    # 계산되며, 같은 prefix를 가리켜야 한다.
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if input_logits[-new_tokens:] != expected_logits or input_hidden[-new_tokens:] != expected_hidden:
        raise AssertionError("testbench vector construction lost a generation prefix")

    mem_dir = Path(mem_dir).as_posix()
    token_count = len(input_ids)
    # 생성 SV source 문장 목록. list 안 문자열은 실제 별도 HDL 코드다.
    lines = [
        "`timescale 1ns/1ps", "module tb_trained_kvcache;",
        f"localparam integer V={vocab_size}, D={d_model}, H={heads}, F={d_ff}, L={layers}, C={context}, TOKEN_BITS={token_bits}, N={token_count};",
        f"localparam integer SCALE={int(cfg['score_scale_q8'])};",
        f"localparam integer BIAS_EN={int(bool(cfg.get('linear_bias', False)))}, AFFINE_EN={int(bool(cfg.get('layernorm_affine', False)))}, GELU_EN={int(cfg.get('activation', 'relu') == 'gelu')};",
        "reg clk, reset_n, start; reg [TOKEN_BITS-1:0] token_id;",
        "reg [TOKEN_BITS-1:0] input_ids [0:N-1];",
        "reg [V*D*16-1:0] token_embedding_flat; reg [C*D*16-1:0] position_embedding_flat;",
        "reg [L*D*D*16-1:0] wq_layers_flat, wk_layers_flat, wv_layers_flat, wo_layers_flat;",
        "reg [L*D*F*16-1:0] w1_layers_flat; reg [L*F*D*16-1:0] w2_layers_flat;",
        "reg [D*V*16-1:0] lm_head_flat;",
        "reg [L*D*16-1:0] wq_bias_flat, wk_bias_flat, wv_bias_flat, wo_bias_flat, w2_bias_flat;",
        "reg [L*F*16-1:0] w1_bias_flat; reg [V*16-1:0] lm_bias_flat;",
        "reg [L*D*16-1:0] ln1_gamma_flat, ln1_beta_flat, ln2_gamma_flat, ln2_beta_flat;",
        "reg [15:0] token_emb_mem [0:V*D-1]; reg [15:0] position_mem [0:C*D-1]; reg [15:0] lm_mem [0:D*V-1];",
        "wire [D*16-1:0] hidden_flat; wire [V*16-1:0] logits_flat;",
        "wire input_ready, busy, done, result_valid, error; wire [31:0] token_count, cycle_count, mac_count;",
        "integer i, step_id, wait_cycles, total_cycles, total_macs, best_id, candidate; reg signed [15:0] best_logit;",
        "always #5 clk=~clk;",
    ]
    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for layer in range(layers):
        for name, count in (("wq", d_model*d_model), ("wk", d_model*d_model),
                            ("wv", d_model*d_model), ("wo", d_model*d_model),
                            ("w1", d_model*d_ff), ("w2", d_ff*d_model)):
            lines.append(f"reg [15:0] {name}_{layer}_mem [0:{count-1}];")
    lines.extend([
        "transformer_gpt_kvcache_seq #( .VOCAB_SIZE(V), .D_MODEL(D), .HEADS(H), .D_FF(F), .LAYERS(L), .MAX_TOKENS(C), .TOKEN_BITS(TOKEN_BITS), .SCORE_SCALE_Q8(SCALE), .ENABLE_BIAS(BIAS_EN), .ENABLE_NORM_AFFINE(AFFINE_EN), .ENABLE_GELU(GELU_EN) ) dut (",
        " .clk(clk), .reset_n(reset_n), .start(start), .result_ready(1'b1), .input_ready(input_ready), .token_id(token_id),",
        " .token_embedding_flat(token_embedding_flat), .position_embedding_flat(position_embedding_flat),",
        " .wq_layers_flat(wq_layers_flat), .wk_layers_flat(wk_layers_flat), .wv_layers_flat(wv_layers_flat), .wo_layers_flat(wo_layers_flat),",
        " .w1_layers_flat(w1_layers_flat), .w2_layers_flat(w2_layers_flat), .lm_head_flat(lm_head_flat),",
        " .wq_bias_flat(wq_bias_flat), .wk_bias_flat(wk_bias_flat), .wv_bias_flat(wv_bias_flat), .wo_bias_flat(wo_bias_flat),",
        " .w1_bias_flat(w1_bias_flat), .w2_bias_flat(w2_bias_flat), .lm_bias_flat(lm_bias_flat),",
        " .ln1_gamma_flat(ln1_gamma_flat), .ln1_beta_flat(ln1_beta_flat), .ln2_gamma_flat(ln2_gamma_flat), .ln2_beta_flat(ln2_beta_flat),",
        " .hidden_flat(hidden_flat), .logits_flat(logits_flat), .busy(busy), .done(done), .result_valid(result_valid), .error(error),",
        " .token_count(token_count), .cycle_count(cycle_count), .mac_count(mac_count));",
        "initial begin clk=0; reset_n=0; start=0; token_id=0; total_cycles=0; total_macs=0;",
        " wq_bias_flat=0; wk_bias_flat=0; wv_bias_flat=0; wo_bias_flat=0; w1_bias_flat=0; w2_bias_flat=0; lm_bias_flat=0;",
        " ln1_gamma_flat=0; ln1_beta_flat=0; ln2_gamma_flat=0; ln2_beta_flat=0;",
        f' $readmemh("{mem_dir}/token_embedding.mem", token_emb_mem);',
        f' $readmemh("{mem_dir}/position_embedding.mem", position_mem);',
        f' $readmemh("{mem_dir}/lm_head.mem", lm_mem);',
        " for (i=0;i<V*D;i=i+1) token_embedding_flat[i*16 +:16]=token_emb_mem[i];",
        " for (i=0;i<C*D;i=i+1) position_embedding_flat[i*16 +:16]=position_mem[i];",
        " for (i=0;i<D*V;i=i+1) lm_head_flat[i*16 +:16]=lm_mem[i];",
    ])
    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for layer in range(layers):
        for name, count in (("wq", d_model*d_model), ("wk", d_model*d_model),
                            ("wv", d_model*d_model), ("wo", d_model*d_model),
                            ("w1", d_model*d_ff), ("w2", d_ff*d_model)):
            lines.append(f' $readmemh("{mem_dir}/layer_{layer}_{name}.mem", {name}_{layer}_mem);')
            lines.append(f" for (i=0;i<{count};i=i+1) {name}_layers_flat[({layer}*{count}+i)*16 +:16]={name}_{layer}_mem[i];")
        layer_weights = weights["layers"][layer]
        fields = (
            ("bq", "wq_bias_flat", d_model, [0]*d_model),
            ("bk", "wk_bias_flat", d_model, [0]*d_model),
            ("bv", "wv_bias_flat", d_model, [0]*d_model),
            ("bo", "wo_bias_flat", d_model, [0]*d_model),
            ("b1", "w1_bias_flat", d_ff, [0]*d_ff),
            ("b2", "w2_bias_flat", d_model, [0]*d_model),
            ("ln1_gamma", "ln1_gamma_flat", d_model, [256]*d_model),
            ("ln1_beta", "ln1_beta_flat", d_model, [0]*d_model),
            ("ln2_gamma", "ln2_gamma_flat", d_model, [256]*d_model),
            ("ln2_beta", "ln2_beta_flat", d_model, [0]*d_model),
        )
        for field, bus, width, default in fields:
            vector = layer_weights.get(field, default)
            # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
            if len(vector) != width:
                raise ValueError(f"{field} vector width mismatch in layer {layer}")
            for channel, value in enumerate(vector):
                lines.append(f" {bus}[({layer}*{width}+{channel})*16 +:16]={_signed16(int(value))};")
    lm_bias = weights.get("lm_bias", [0]*vocab_size)
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if len(lm_bias) != vocab_size:
        raise ValueError("lm_bias vector width mismatch")
    for vocab_id, value in enumerate(lm_bias):
        lines.append(f" lm_bias_flat[{vocab_id}*16 +:16]={_signed16(int(value))};")
    for index, token in enumerate(input_ids):
        lines.append(f" input_ids[{index}]={token_bits}'d{token};")
    lines.extend([" #1; @(negedge clk); reset_n=1;",
                  " for (step_id=0;step_id<N;step_id=step_id+1) begin",
                  "  wait_cycles=0; while ((input_ready!==1'b1)&&(wait_cycles<5)) begin @(negedge clk); wait_cycles=wait_cycles+1; end",
                  '  if(input_ready!==1\'b1) $fatal(1,"KV-cache input not ready before token");',
                  "  token_id=input_ids[step_id]; @(negedge clk); start=1; @(negedge clk); start=0;",
                  "  wait_cycles=0; while ((done!==1'b1)&&(wait_cycles<200000)) begin @(negedge clk); wait_cycles=wait_cycles+1; end",
                  '  if(done!==1\'b1 || result_valid!==1\'b1 || error!==1\'b0) $fatal(1,"KV-cache RTL timeout/error/invalid output step=%0d",step_id);',
                  "  total_cycles=total_cycles+cycle_count; total_macs=total_macs+mac_count;"])
    for step_index, (hidden, logits) in enumerate(zip(input_hidden, input_logits)):
        lines.append(f"  if(step_id=={step_index}) begin")
        for channel, expected in enumerate(hidden):
            lines.append(f'   if($signed(hidden_flat[{channel}*16 +:16]) !== {_signed16(expected)}) $fatal(1,"hidden mismatch step={step_index} channel={channel}");')
        for vocab_id, expected in enumerate(logits):
            lines.append(f'   if($signed(logits_flat[{vocab_id}*16 +:16]) !== {_signed16(expected)}) $fatal(1,"logit mismatch step={step_index} vocab={vocab_id}");')
        lines.append("  end")
    first_generation_step = len(prompt_ids) - 1
    lines.extend([
        "  best_id=-1;",
        f"  if(step_id >= {first_generation_step}) begin",
        "   best_id=0; best_logit=$signed(logits_flat[0 +:16]);",
        "   for(candidate=1;candidate<V;candidate=candidate+1) if($signed(logits_flat[candidate*16 +:16])>best_logit) begin best_logit=$signed(logits_flat[candidate*16 +:16]); best_id=candidate; end",
        "   case(step_id-" + str(first_generation_step) + ")",
    ])
    for generation_index, expected_id in enumerate(expected_tokens):
        lines.append(f'    {generation_index}: if(best_id!={expected_id}) $fatal(1,"generated token mismatch step=%0d got=%0d expected={expected_id}",step_id,best_id);')
    lines.extend([
        "    default: $fatal(1,\"unexpected generation index\"); endcase",
        "  end",
        '  $display("KCACHE_TX step=%0d cycles=%0d macs=%0d token=%0d count=%0d",step_id,cycle_count,mac_count,best_id,token_count);',
        " end",
        ' $display("KCACHE_TOTAL cycles=%0d macs=%0d",total_cycles,total_macs);',
        ' $display("PASS: true RTL K/V cache equals full-context Q8.8 reference"); $finish; end endmodule',
    ])
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return expected_tokens, input_ids, input_hidden, input_logits


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    # 정수 inference JSON config/vocab/weight. 저장한 숫자를 읽고 새 학습을 하지 않는다.
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    # 입력 문자열->ID. prompt 마지막 score가 첫 생성 token을 예측한다.
    parser.add_argument("--prompt", default="ROMEO:")
    # generation에서는 새 token 수, DRAM 모델에서는 context token 수. 파일 목적에 따라 의미가 다르다.
    parser.add_argument("--tokens", type=int, default=3)
    # incremental KV RTL의 token별 검증. 기본 context 재계산과 다르다.
    parser.add_argument("--kvcache-rtl", action="store_true",
                        help="매 token incremental layer-wise KV-cache RTL로 검증")
    # 비교/검증 JSON 저장 경로. 실패 조건은 정상 결과로 기록하지 않아야 한다.
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    model = load_checkpoint(args.checkpoint)
    memory_path = args.checkpoint.resolve().parent / "mem"
    if not memory_path.exists():
        write_mem_files(model, memory_path)
    try:
        memory_dir = memory_path.relative_to(ROOT).as_posix()
    except ValueError as error:
        raise ValueError("Icarus $readmemh 검증용 checkpoint는 저장소 내부 경로를 사용해야 합니다.") from error
    # prompt 문자->ID 사전. 어휘 밖 문자는 unknown ID로 바뀐다.
    encoder = {char: index for index, char in enumerate(model["vocab"])}
    prompt_ids = [encoder.get(char, model.get("unknown_token_id", 0)) for char in args.prompt]
    prompt_ids = prompt_ids[-int(model["config"]["context_length"]):]
    BUILD.mkdir(parents=True, exist_ok=True)
    if args.kvcache_rtl:
        default_output = ROOT / "build" / "reports" / "trained_kvcache_rtl_generation.json"
        tb = BUILD / "tb_trained_kvcache.sv"
        expected_tokens, input_ids, expected_hidden, expected_logits = create_kvcache_testbench(
            model, prompt_ids, args.tokens, tb, memory_dir)
        expected_transaction_count = len(input_ids)
        top = "tb_trained_kvcache"
        core_source = ROOT / "rtl" / "transformer_gpt_kvcache_seq.sv"
        image = BUILD / "trained_kvcache.vvp"
    else:
        # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
        if (bool(model["config"].get("linear_bias", False)) or
                bool(model["config"].get("layernorm_affine", False)) or
                model["config"].get("activation", "relu") == "gelu"):
            raise ValueError("bias/affine/GELU checkpoint는 --kvcache-rtl을 사용하세요.")
        default_output = ROOT / "build" / "reports" / "trained_sequential_generation.json"
        tb = BUILD / "tb_trained_generation.sv"
        expected_tokens, expected_logits = create_testbench(model, prompt_ids, args.tokens, tb, memory_dir)
        expected_transaction_count = args.tokens
        top = "tb_trained_generation"
        core_source = ROOT / "rtl" / "transformer_gpt_language_model_seq.sv"
        image = BUILD / "trained_generation.vvp"
    output_path = args.output or default_output
    compiler, simulator = find_tool("iverilog"), find_tool("vvp")
    # 컴파일할 RTL/core/TB 목록. top을 지정하여 의도한 회로를 검사한다.
    sources = [
        ROOT / "rtl" / "dram_pim_pu_synth.sv",
        core_source,
        tb,
    ]
    # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
    # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
    compile_result = run_console(
        [compiler, "-g2012", "-s", top, "-o", str(image), *map(str, sources)],
        cwd=ROOT, capture_output=True,
    )
    if compile_result.stdout:
        print(compile_result.stdout, end="")
    if compile_result.stderr:
        print(compile_result.stderr, end="", file=sys.stderr)
    if compile_result.returncode:
        return compile_result.returncode
    # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
    # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
    simulation = run_console(
        [simulator, str(image)], cwd=ROOT, capture_output=True,
    )
    print(simulation.stdout, end="")
    if simulation.stderr:
        print(simulation.stderr, end="", file=sys.stderr)
    if simulation.returncode:
        return simulation.returncode

    steps = []
    line_pattern = (r"KCACHE_TX step=(\d+) cycles=(\d+) macs=(\d+) token=(-?\d+) count=(\d+)"
                    if args.kvcache_rtl else
                    r"GEN_STEP step=(\d+) cycles=(\d+) macs=(\d+) token=(\d+)")
    for line in simulation.stdout.splitlines():
        match = re.fullmatch(line_pattern, line.strip())
        if match:
            names = (("step", "cycles", "macs", "token_id", "token_count")
                     if args.kvcache_rtl else ("step", "cycles", "macs", "token_id"))
            steps.append(dict(zip(names, map(int, match.groups()))))
    # 시뮬레이터에서 실제 선택한 ID들. oracle과 다르면 실패한다.
    actual_tokens = ([step["token_id"] for step in steps if step["token_id"] >= 0]
                     if args.kvcache_rtl else [step["token_id"] for step in steps])
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if actual_tokens != expected_tokens:
        raise AssertionError(f"RTL generation token mismatch: {actual_tokens} != {expected_tokens}")
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if len(steps) != expected_transaction_count:
        raise AssertionError(f"RTL transaction count mismatch: {len(steps)} != {expected_transaction_count}")

    # 기존 token_id는 '이 거래의 점수로 선택한 다음 ID'이며 prefill에서는 -1이다.
    # 이를 입력 ID로 오해하지 않도록 실제 입력과 선택값을 별도 필드로 명시한다.
    # -1은 FPGA에 전송한 ID가 아니라 아직 생성 선택을 하지 않았다는 로그 표식이다.
    if args.kvcache_rtl:
        for step, input_id in zip(steps, input_ids):
            step['input_token_id'] = input_id
            step['input_character'] = model['vocab'][input_id]
            step['generated_token_id'] = step['token_id'] if step['token_id'] >= 0 else None

    simulation_log = output_path.with_suffix('.simulation.log')
    simulation_log.parent.mkdir(parents=True, exist_ok=True)
    simulation_log.write_text(simulation.stdout + simulation.stderr, encoding='utf-8')

    result = {
        "prompt": args.prompt,
        "prompt_token_ids": prompt_ids,
        "generated_token_ids": actual_tokens,
        "generated_text": "".join(model["vocab"][token_id] for token_id in actual_tokens),
        "tokens_generated": len(actual_tokens),
        "transaction_count": len(steps),
        "total_cycles": sum(step["cycles"] for step in steps),
        "total_macs": sum(step["macs"] for step in steps),
        "per_step": steps,
        "passed": True,
        "exact_logit_comparisons": len(expected_logits) * int(model['config']['vocab_size']),
        "exact_hidden_comparisons": (len(steps) * int(model['config']['d_model']) if args.kvcache_rtl else 0),
        "physical_board_measured": False,
        "simulation_log": str(simulation_log),
        "logit_comparison": ("매 token transaction에서 hidden vector와 전체 vocabulary Q8.8 logits를 full-context Python 기준과 exact 비교"
                             if args.kvcache_rtl else
                             "매 생성 단계의 유효 마지막 token에서 모든 vocabulary Q8.8 logits를 Python 기준과 exact 비교"),
        "architecture_note_ko": ("RTL 내부에 layer별 K/V cache가 있으며 입력 token 하나를 처리할 때 과거 K/V를 재사용한다. 본 시험은 prompt부터 token을 흘려 넣고 생성 argmax 결과도 확인했다."
                                 if args.kvcache_rtl else
                                 "순차 RTL top을 transaction마다 호출하고 host/testbench가 argmax token을 되돌려 준다. 이 경로는 매번 context를 재계산하며 RTL 내부 KV cache는 없다."),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: {len(expected_logits) * int(model['config']['vocab_size'])}개 단계별 logits와 {len(actual_tokens)}개 생성 token이 정확히 일치합니다.")
    print(f"결과 JSON: {output_path}")
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    raise SystemExit(main())
