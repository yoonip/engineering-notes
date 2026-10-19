// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// 순차형 synthesis top과 정확히 같은 dimensions를 가진 end-to-end comb 비교 top.
// clock/control ports는 interface 비교를 위해 있지만 comb 기능 블록은 사용하지 않는다.
// [학습용 상세 해설 2026-10-04]
// 위치: 순차 wrapper와 같은 차원의 조합 언어 모델 합성 비교 기준.
// Python 대응: model/gpt_language_model_reference.py:language_model_logits.
// clk/reset_n은 comb 연산에 사용되지 않는다. busy=0,done=start,cycle_count=0은
// transaction FSM이 없는 비교 표시다. FPGA가 모든 계산을 0ns에 끝낸다는 뜻은 아니다.
// 실제 gate/배선 지연은 synthesis/place/route timing으로 따로 확인해야 한다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module gpt_comb_synth_top (
    // 클록 입력. 순차 회로는 상승 에지에서 계산 결과를 register에 저장한다. comb wrapper에서는 비교용으로만 남는다.
    input wire clk,
    // 순차 wrapper와 port를 비교하기 위해 둔 reset 입력. 이 comb core에는 저장 상태가 없어 reset_n을 사용하지 않는다.
    input wire reset_n,
    // comb 비교 wrapper의 표시 입력. 수학 core는 start와 무관하게 계산하고 이 입력은 done에 바로 연결된다.
    input wire start,
    // token t의 ID는 [t*TOKEN_BITS +: TOKEN_BITS]. Python token_ids[t]를 낮은 token 순서부터 묶는다.
    input wire [3*3-1:0] token_ids_flat,
    // [어휘 ID][hidden 채널] 학습 표. Python weights['token_embedding'][token_id][channel]을 row-major로 묶는다.
    input wire [8*4*16-1:0] token_embedding_flat,
    // [위치][hidden 채널] 학습 표. 순서를 나타내기 위해 embedding에 더하는 weights['position_embedding'][position][channel]이다.
    input wire [3*4*16-1:0] position_embedding_flat,
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
    // embedding+position 중간 결과 [토큰][채널]. 문자열 ID가 처음 숫자 특징으로 변한 위치를 확인하는 출력이다.
    output wire [3*4*16-1:0] embedding_sum_flat,
    // 마지막 decoder의 hidden 특징. raw/256으로 읽으며 개별 채널에 고정된 자연어 단어 뜻이 있지는 않다.
    output wire [3*4*16-1:0] hidden_flat,
    // 다음 어휘 후보별 Q8.8 점수. 확률이 아니며 argmax/sampling으로 고른 ID를 vocab[id]로 문자로 바꾼다.
    output wire [3*8*16-1:0] logits_flat,
    // comb 비교 wrapper에는 FSM이 없어 항상 0. 별도 거래 수락/결과 대기 프로토콜이 없는 기능 모델이다.
    output wire busy,
    // start를 그대로 반영하는 comb 비교 표시. 실제 clocked 완료 pulse/valid handshake가 아니다.
    output wire done,
    // 최근 거래의 클록 수. 초 단위 시간=cycle_count*클록 주기다. KV의 output 대기 시간도 늘릴 수 있다.
    output wire [31:0] cycle_count,
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    output wire [31:0] mac_count
);
    // 하위 core의 비교용 CPU traffic 가정 값을 받는 내부 배선.
    wire [31:0] cpu_words;
    // 하위 core의 비교용 PIM traffic 가정 값을 받는 내부 배선.
    wire [31:0] pim_words;
    // 하위 core의 non-VMM vector 호출 횟수 수식을 받는 내부 배선.
    wire [31:0] pu_ops;

    transformer_gpt_language_model_comb #(
        .TOKENS(3), .VOCAB_SIZE(8), .D_MODEL(4), .HEADS(2),
        .D_FF(8), .LAYERS(2), .SCORE_SCALE_Q8(181), .TOKEN_BITS(3)
    // 고정 차원 wrapper의 하위 회로. 수학을 추가하지 않고 파라미터와 신호를 전달한다.
    ) u_core (
        .token_ids_flat(token_ids_flat),
        .token_embedding_flat(token_embedding_flat),
        .position_embedding_flat(position_embedding_flat),
        .wq_layers_flat(wq_layers_flat), .wk_layers_flat(wk_layers_flat),
        .wv_layers_flat(wv_layers_flat), .wo_layers_flat(wo_layers_flat),
        .w1_layers_flat(w1_layers_flat), .w2_layers_flat(w2_layers_flat),
        .lm_head_flat(lm_head_flat), .embedding_sum_flat(embedding_sum_flat),
        .hidden_flat(hidden_flat), .logits_flat(logits_flat),
        .cpu_boundary_words(cpu_words), .pim_boundary_words(pim_words),
        .mac_count(mac_count), .nonvmm_vector_ops(pu_ops)
    );
    // 계산/결과 대기를 상태 비교로 표시. comb top의 상수 0은 transaction FSM이 없는 비교 표현이다.
    assign busy = 1'b0;
    // start를 done에 바로 연결하는 comb 비교 interface이며 계산 지연 0ns를 뜻하지 않는다.
    assign done = start;
    // clocked 연산 counter가 없는 comb 비교값. 실제 gate 지연은 timing report로 확인한다.
    assign cycle_count = 32'd0;
endmodule
