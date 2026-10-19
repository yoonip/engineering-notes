// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// Yosys generic synthesis harness for the advanced token-stream design.
// Dimensions are intentionally small but nontrivial and all model inputs remain
// ports, so synthesis cannot fold away the MAC, layer cache, affine, bias or GELU.
// [학습용 상세 해설 2026-10-04]
// 위치: V=8,D=4,H=2,F=8,L=2,cache=4의 full-ops KV-cache 합성 재현 wrapper.
// Python 대응: model/gpt_q88.py:forward_q88_step에 같은 shape/연산 설정 모델을 넣은 동작.
// bias/affine/GELU를 켜고 weight input을 유지해 해당 연산이 최적화로 사라지는 것을 줄인다.
// dut (.*)는 이름이 같은 port를 자동 연결하는 SV 문법이다. 전체 input을 실제 보드
// pin으로 연결하는 설계가 아니며 물리 host/메모리 shell은 별도로 필요하다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module gpt_kvcache_synth_top (
    // 클록 입력. 순차 회로는 상승 에지에서 계산 결과를 register에 저장한다. comb wrapper에서는 비교용으로만 남는다.
    input wire clk,
    // 0일 때 초기화하는 active-low reset. 상태/위치/완료 신호를 시작 값으로 만들고 KV 문맥을 새로 시작한다.
    input wire reset_n,
    // 계산 요청. 순차 core는 idle에서만 수락하므로 ready/busy 확인 후 한 클록 펄스를 준다.
    input wire start,
    // 결과 소비 확인. result_valid 이후 모든 logit을 읽은 host가 1을 주어 다음 토큰 수락을 허용한다.
    input wire result_ready,
    // 문자 자체가 아닌 어휘표 정수 번호. Python encode[char]로 만든 ID이고 Q8.8 실수가 아니다.
    input wire [2:0] token_id,
    // [어휘 ID][hidden 채널] 학습 표. Python weights['token_embedding'][token_id][channel]을 row-major로 묶는다.
    input wire [8*4*16-1:0] token_embedding_flat,
    // [위치][hidden 채널] 학습 표. 순서를 나타내기 위해 embedding에 더하는 weights['position_embedding'][position][channel]이다.
    input wire [4*4*16-1:0] position_embedding_flat,
    // [layer][입력 채널][출력 채널] Query 가중치. layer 0 원소가 낮은 bit에 놓이며 Python layer['wq'] 방향이다.
    input wire [2*4*4*16-1:0] wq_layers_flat,
    // [layer][입력 채널][출력 채널] Key 가중치. 층마다 다른 학습 행렬로 검색 대상 특징을 만든다.
    input wire [2*4*4*16-1:0] wk_layers_flat,
    // [layer][입력 채널][출력 채널] Value 가중치. 현재 층의 입력 hidden에서 꺼낼 내용을 만든다.
    input wire [2*4*4*16-1:0] wv_layers_flat,
    // [layer][D_MODEL][D_MODEL] 출력 투영. head별 context를 연결한 뒤 전체 특징으로 섞는다.
    input wire [2*4*4*16-1:0] wo_layers_flat,
    // [layer][D_MODEL][D_FF] FFN 확장 행렬. Python layer['w1']와 row-major 방향이 같다.
    input wire [2*4*8*16-1:0] w1_layers_flat,
    // [layer][D_FF][D_MODEL] FFN 축소 행렬. Python layer['w2']와 row-major 방향이 같다.
    input wire [2*8*4*16-1:0] w2_layers_flat,
    // [hidden 채널][어휘 ID] 출력 행렬. 마지막 hidden을 다음 문자 후보별 logit 점수로 바꾼다.
    input wire [4*8*16-1:0] lm_head_flat,
    // [layer][D_MODEL] Q linear bias. 내적 >>8/포화 후 더하는 Python layer.get('bq')이다.
    input wire [2*4*16-1:0] wq_bias_flat,
    // [layer][D_MODEL] K linear bias. ENABLE_BIAS=1일 때 선택하며 Python layer.get('bk')와 같다.
    input wire [2*4*16-1:0] wk_bias_flat,
    // [layer][D_MODEL] V linear bias. Python qmat_bias([state],layer['wv'],layer.get('bv'))의 bv다.
    input wire [2*4*16-1:0] wv_bias_flat,
    // [layer][D_MODEL] attention output bias. Python layer.get('bo')와 같다.
    input wire [2*4*16-1:0] wo_bias_flat,
    // [layer][D_FF] FFN 확장 bias. 길이는 D_MODEL이 아니라 확장 폭 D_FF다.
    input wire [2*8*16-1:0] w1_bias_flat,
    // [layer][D_MODEL] FFN 축소 bias. Python layer.get('b2')를 linear 포화 후 더한다.
    input wire [2*4*16-1:0] w2_bias_flat,
    // [어휘 ID] LM head bias. Python weights.get('lm_bias')이며 문자 후보 점수 각각에 더한다.
    input wire [8*16-1:0] lm_bias_flat,
    // [layer][D_MODEL] 첫 LayerNorm 학습 scale gamma. Q8.8 256=배율 1.0이다.
    input wire [2*4*16-1:0] ln1_gamma_flat,
    // [layer][D_MODEL] 첫 LayerNorm 학습 이동량 beta. gamma 곱셈 >>8/포화 후 더한다.
    input wire [2*4*16-1:0] ln1_beta_flat,
    // [layer][D_MODEL] 두 번째 LayerNorm gamma. Python layernorm_q8_affine(...,ln2_gamma,...)이다.
    input wire [2*4*16-1:0] ln2_gamma_flat,
    // [layer][D_MODEL] 두 번째 LayerNorm beta. ENABLE_NORM_AFFINE=0이면 gamma/beta를 쓰지 않는다.
    input wire [2*4*16-1:0] ln2_beta_flat,
    // 마지막 decoder의 hidden 특징. raw/256으로 읽으며 개별 채널에 고정된 자연어 단어 뜻이 있지는 않다.
    output wire [4*16-1:0] hidden_flat,
    // 다음 어휘 후보별 Q8.8 점수. 확률이 아니며 argmax/sampling으로 고른 ID를 vocab[id]로 문자로 바꾼다.
    output wire [8*16-1:0] logits_flat,
    // 새 입력 수락 가능. 1인 idle에서 start/token_id를 제공한다.
    output wire input_ready,
    // 계산 중 또는 결과 소비 대기 상태. 1이면 새 start를 수락하지 않는다.
    output wire busy,
    // 계산 완료 한 클록 pulse. KV 결과를 지속해서 읽으려면 result_valid도 확인한다.
    output wire done,
    // hidden/logits가 유효함을 유지하는 신호. result_ready handshake까지 데이터가 고정된다.
    output wire result_valid,
    // 잘못된 어휘 ID/꽉 찬 문맥을 거절하는 한 클록 알림. 잘못된 입력을 정상 결과로 오해하지 않게 한다.
    output wire error,
    // 완료한 토큰 수. 다음 입력의 absolute position 및 layer별 KV cache 유효 길이이며 Q8.8 숫자가 아니다.
    output wire [31:0] token_count,
    // 최근 거래의 클록 수. 초 단위 시간=cycle_count*클록 주기다. KV의 output 대기 시간도 늘릴 수 있다.
    output wire [31:0] cycle_count,
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    output wire [31:0] mac_count
);
    transformer_gpt_kvcache_seq #(
        .VOCAB_SIZE(8), .D_MODEL(4), .HEADS(2), .D_FF(8), .LAYERS(2),
        .MAX_TOKENS(4), .TOKEN_BITS(3), .SCORE_SCALE_Q8(181),
        .ENABLE_BIAS(1), .ENABLE_NORM_AFFINE(1), .ENABLE_GELU(1)
    ) dut (.*);
endmodule
