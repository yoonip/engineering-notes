// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// resource-shared 순차 core의 재현용 소형 합성 wrapper.
// comb 합성 top과 같은 T=3,D=4,H=2,F=8,L=2 dimensions를 사용해 generic cell 수를
// 비교할 수 있게 한다. 이는 특정 FPGA part에 대응하는 LUT/FF 수가 아니다.
// [학습용 상세 해설 2026-10-04]
// 위치: T=3,V=8,D=4,H=2,F=8,L=2의 shared-MAC 합성 wrapper.
// Python 대응: gpt_language_model_reference:language_model_logits 결과를
// transformer_gpt_language_model_seq의 FSM으로 시간 분할 계산한다.
// .port(signal)은 하위 회로로 전달하는 배선이며 알고리즘은 core에 있다.
// generic synthesis cell 수는 Vivado vendor LUT/FF 자원 수와 다른 수치다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module gpt_seq_synth_top (
    // 클록 입력. 순차 회로는 상승 에지에서 계산 결과를 register에 저장한다. comb wrapper에서는 비교용으로만 남는다.
    input wire clk,
    // 0일 때 초기화하는 active-low reset. 상태/위치/완료 신호를 시작 값으로 만들고 KV 문맥을 새로 시작한다.
    input wire reset_n,
    // 계산 요청. 순차 core는 idle에서만 수락하므로 ready/busy 확인 후 한 클록 펄스를 준다.
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
    // 계산 중 또는 결과 소비 대기 상태. 1이면 새 start를 수락하지 않는다.
    output wire busy,
    // 계산 완료 한 클록 pulse. KV 결과를 지속해서 읽으려면 result_valid도 확인한다.
    output wire done,
    // 최근 거래의 클록 수. 초 단위 시간=cycle_count*클록 주기다. KV의 output 대기 시간도 늘릴 수 있다.
    output wire [31:0] cycle_count,
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    output wire [31:0] mac_count
);
    transformer_gpt_language_model_seq #(
        .TOKENS(3), .VOCAB_SIZE(8), .D_MODEL(4), .HEADS(2),
        .D_FF(8), .LAYERS(2), .SCORE_SCALE_Q8(181), .TOKEN_BITS(3)
    // 고정 차원 wrapper의 하위 회로. 수학을 추가하지 않고 파라미터와 신호를 전달한다.
    ) u_core (
        .clk(clk), .reset_n(reset_n), .start(start),
        .token_ids_flat(token_ids_flat),
        .token_embedding_flat(token_embedding_flat),
        .position_embedding_flat(position_embedding_flat),
        .wq_layers_flat(wq_layers_flat), .wk_layers_flat(wk_layers_flat),
        .wv_layers_flat(wv_layers_flat), .wo_layers_flat(wo_layers_flat),
        .w1_layers_flat(w1_layers_flat), .w2_layers_flat(w2_layers_flat),
        .lm_head_flat(lm_head_flat), .embedding_sum_flat(embedding_sum_flat),
        .hidden_flat(hidden_flat), .logits_flat(logits_flat),
        .busy(busy), .done(done), .cycle_count(cycle_count), .mac_count(mac_count)
    );
endmodule
