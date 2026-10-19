// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// Yosys/FPGA 합성 실험을 반복할 수 있도록 작은 GPT core 구성을 고정한 top.
// 3-token context, D=4, 2 heads, 2 layers, FFN=8이다. 소비자용 GPT 크기가 아니라
// multi-head와 multi-layer의 합성 가능성을 확인하는 최소 재현 구성이다.
// [학습용 상세 해설 2026-10-04]
// 위치: T=3,D=4,H=2,F=8,L=2를 고정한 decoder-stack 합성 재현 wrapper.
// Python 대응: model/gpt_core_reference.py:sample_input/sample_weights/decoder_stack.
// 새 수학을 추가하지 않고 하위 core의 차원/port를 고정한다. weight를 input으로 남겨
// 상수 최적화로 연산이 사라지는 것을 줄인다. 이를 실제 FPGA pin으로 모두 빼는 구성이
// 아니므로 물리 보드용 weight memory와 외부 interface shell이 별도로 필요하다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module gpt_stack_synth_top (
    // [토큰][hidden 채널] 입력 숫자 표현. embedding이 끝난 행렬이고 원문 문자열이 아니며 Python x/state에 해당한다.
    input  wire [3*4*16-1:0] x_flat,
    // [layer][입력 채널][출력 채널] Query 가중치. layer 0 원소가 낮은 bit에 놓이며 Python layer['wq'] 방향이다.
    input  wire [2*4*4*16-1:0] wq_layers_flat,
    // [layer][입력 채널][출력 채널] Key 가중치. 층마다 다른 학습 행렬로 검색 대상 특징을 만든다.
    input  wire [2*4*4*16-1:0] wk_layers_flat,
    // [layer][입력 채널][출력 채널] Value 가중치. 현재 층의 입력 hidden에서 꺼낼 내용을 만든다.
    input  wire [2*4*4*16-1:0] wv_layers_flat,
    // [layer][D_MODEL][D_MODEL] 출력 투영. head별 context를 연결한 뒤 전체 특징으로 섞는다.
    input  wire [2*4*4*16-1:0] wo_layers_flat,
    // [layer][D_MODEL][D_FF] FFN 확장 행렬. Python layer['w1']와 row-major 방향이 같다.
    input  wire [2*4*8*16-1:0] w1_layers_flat,
    // [layer][D_FF][D_MODEL] FFN 축소 행렬. Python layer['w2']와 row-major 방향이 같다.
    input  wire [2*8*4*16-1:0] w2_layers_flat,
    // decoder block/stack 최종 hidden [토큰][채널]. 문자가 아니라 LM head로 전달하는 내부 표현이다.
    output wire [3*4*16-1:0] y_flat,
    // 미융합 CPU 비교 가정의 경계 이동 단어 수. word=16bit=2byte이며 실측 DRAM 트래픽은 아니다.
    output wire [31:0] cpu_boundary_words,
    // 중간값을 메모리 가까이 유지한다는 PIM 비교 가정의 경계 이동 단어 수. 실제 칩 계측값은 아니다.
    output wire [31:0] pim_boundary_words,
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    output wire [31:0] mac_count,
    // Softmax/Residual/Norm/활성화의 vector 단계 수. 개별 산술 덧셈 개수와 다르다.
    output wire [31:0] nonvmm_vector_ops
);
    transformer_gpt_decoder_stack_comb #(
        .TOKENS(3), .D_MODEL(4), .HEADS(2), .D_FF(8), .LAYERS(2),
        .SCORE_SCALE_Q8(181)
    // 고정 차원 wrapper의 하위 회로. 수학을 추가하지 않고 파라미터와 신호를 전달한다.
    ) u_core (
        .x_flat(x_flat),
        .wq_layers_flat(wq_layers_flat), .wk_layers_flat(wk_layers_flat),
        .wv_layers_flat(wv_layers_flat), .wo_layers_flat(wo_layers_flat),
        .w1_layers_flat(w1_layers_flat), .w2_layers_flat(w2_layers_flat),
        .y_flat(y_flat), .cpu_boundary_words(cpu_boundary_words),
        .pim_boundary_words(pim_boundary_words), .mac_count(mac_count),
        .nonvmm_vector_ops(nonvmm_vector_ops)
    );
endmodule
