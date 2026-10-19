// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// -----------------------------------------------------------------------------
// 여러 block을 직렬로 잇는 GPT-style decoder core
//
// 각 block의 출력 activation이 다음 block의 입력이 된다. 이는 각 층을 같은
// 입력에서 따로 계산하는 테스트가 아니라 실제 Transformer의 residual stream을
// 따라가는 구조다. 레이어별 가중치는 서로 독립된 packed bus에서 전달되므로 학습된
// 모델의 층마다 다른 행렬을 넣을 수 있다.
//
// 현재 top은 토큰 표현 X를 받아 decoder blocks를 수행하는 기능 코어다. 토크나이저,
// token/position embedding lookup, vocabulary LM head와 sampling은 top 바깥의
// software/model adapter가 담당한다. top 전체는 조합식 연산 코어이며 cycle-accurate
// 메모리 인터페이스는 아니다. 외부 FSM/DRAM traffic model은 분리해서 검증한다.
// -----------------------------------------------------------------------------
// [학습용 상세 해설 2026-10-04]
// 위치: decoder block을 여러 층으로 연결한 기능 stack. 문자열 처리/LM head는 바깥이다.
// Python 대응: model/gpt_core_reference.py:decoder_stack의 for weights ...:
// state = decoder_block(state,weights). generate는 반복을 L개 실제 core 연결로 펼친다.
// state[0..L]는 배선이지 clocked state register가 아니다. [0]=입력, [L]=최종 출력이다.
// 여러 조합 층이 직렬로 연결되어 물리 임계 경로가 길어질 수 있다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module transformer_gpt_decoder_stack_comb #(
    // context 토큰 수 T. attention 점수는 T*T개이며 문자열 byte 수와 항상 같지는 않다.
    parameter integer TOKENS = 4,
    // 토큰마다 hidden 숫자 수 D. embedding/residual 폭이며 모든 head 채널 수 합이 D다.
    parameter integer D_MODEL = 8,
    // attention 관점 수 H. head_dim=D_MODEL/HEADS이며 서로 다른 채널로 독립 점수/확률을 만든다.
    parameter integer HEADS = 2,
    // FFN 중간 채널 수 F. W1=D*F, W2=F*D이고 폭을 키우면 연산/저장 비용도 커진다.
    parameter integer D_FF = 16,
    // decoder block 반복 층 수 L. 앞 층 출력이 다음 층 입력이며 층마다 별도 weight다.
    parameter integer LAYERS = 2,
    // 이 값은 256/sqrt(D_MODEL/HEADS)의 Q8.8 정수 근사값이다.
    // round(256/sqrt(head_dim)) 정수. QK의 차원 효과를 완화하며 head_dim=4일 때 128=0.5다.
    parameter integer SCORE_SCALE_Q8 = 128
) (
    // [토큰][hidden 채널] 입력 숫자 표현. embedding이 끝난 행렬이고 원문 문자열이 아니며 Python x/state에 해당한다.
    input  wire [TOKENS*D_MODEL*16-1:0] x_flat,
    // [layer][입력 채널][출력 채널] Query 가중치. layer 0 원소가 낮은 bit에 놓이며 Python layer['wq'] 방향이다.
    input  wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wq_layers_flat,
    // [layer][입력 채널][출력 채널] Key 가중치. 층마다 다른 학습 행렬로 검색 대상 특징을 만든다.
    input  wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wk_layers_flat,
    // [layer][입력 채널][출력 채널] Value 가중치. 현재 층의 입력 hidden에서 꺼낼 내용을 만든다.
    input  wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wv_layers_flat,
    // [layer][D_MODEL][D_MODEL] 출력 투영. head별 context를 연결한 뒤 전체 특징으로 섞는다.
    input  wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wo_layers_flat,
    // [layer][D_MODEL][D_FF] FFN 확장 행렬. Python layer['w1']와 row-major 방향이 같다.
    input  wire [LAYERS*D_MODEL*D_FF*16-1:0] w1_layers_flat,
    // [layer][D_FF][D_MODEL] FFN 축소 행렬. Python layer['w2']와 row-major 방향이 같다.
    input  wire [LAYERS*D_FF*D_MODEL*16-1:0] w2_layers_flat,
    // decoder block/stack 최종 hidden [토큰][채널]. 문자가 아니라 LM head로 전달하는 내부 표현이다.
    output wire [TOKENS*D_MODEL*16-1:0] y_flat,
    // 미융합 CPU 비교 가정의 경계 이동 단어 수. word=16bit=2byte이며 실측 DRAM 트래픽은 아니다.
    output wire [31:0] cpu_boundary_words,
    // 중간값을 메모리 가까이 유지한다는 PIM 비교 가정의 경계 이동 단어 수. 실제 칩 계측값은 아니다.
    output wire [31:0] pim_boundary_words,
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    output wire [31:0] mac_count,
    // Softmax/Residual/Norm/활성화의 vector 단계 수. 개별 산술 덧셈 개수와 다르다.
    output wire [31:0] nonvmm_vector_ops
);
    // [token][D_MODEL] tensor의 총 bit 수 T*D*16. vector 원소 수와 bit 수를 구분한다.
    localparam integer TD_BITS = TOKENS * D_MODEL * 16;
    // 한 layer Q/K/V/Wo 행렬의 bit 수 D*D*16.
    localparam integer QQ_BITS = D_MODEL * D_MODEL * 16;
    // 한 layer FFN 확장 행렬의 bit 수 D*F*16.
    localparam integer W1_BITS = D_MODEL * D_FF * 16;
    // 한 layer FFN 축소 행렬의 bit 수 F*D*16.
    localparam integer W2_BITS = D_FF * D_MODEL * 16;

    // state[0]은 입력, state[n+1]은 n번째 decoder block의 출력이다.
    // 각 decoder 층 사이 [0..LAYERS] 연결 배선. clocked FSM state가 아니라 Python state 갱신을 층 연결로 펼친 tensor다.
    wire [TD_BITS-1:0] state [0:LAYERS];
    assign state[0] = x_flat;
    assign y_flat = state[LAYERS];

    genvar layer_index;
    // generate는 실행 중 반복이 아니라 elaboration 때 고정 개수 회로를 만드는 문법이다.
    // head/token/layer 숫자를 늘리면 물리 복제 회로와 조합 경로 크기가 바뀐다.
    generate
        for (layer_index = 0; layer_index < LAYERS; layer_index = layer_index + 1) begin : gen_decoder_layers
            transformer_decoder_mha_pim_comb #(
                .TOKENS(TOKENS),
                .D_MODEL(D_MODEL),
                .HEADS(HEADS),
                .D_FF(D_FF),
                .SCORE_SCALE_Q8(SCORE_SCALE_Q8)
            // Python state=decoder_block(state,weights) 한 반복. 현재 layer의 weight를 연결한다.
            ) u_decoder_block (
                .x_flat(state[layer_index]),
                .wq_flat(wq_layers_flat[layer_index*QQ_BITS +: QQ_BITS]),
                .wk_flat(wk_layers_flat[layer_index*QQ_BITS +: QQ_BITS]),
                .wv_flat(wv_layers_flat[layer_index*QQ_BITS +: QQ_BITS]),
                .wo_flat(wo_layers_flat[layer_index*QQ_BITS +: QQ_BITS]),
                .w1_flat(w1_layers_flat[layer_index*W1_BITS +: W1_BITS]),
                .w2_flat(w2_layers_flat[layer_index*W2_BITS +: W2_BITS]),
                .y_flat(state[layer_index+1]),
                // 계층별 내부 카운터는 top에서 수식으로 합산한다.
                .cpu_boundary_words(),
                .pim_boundary_words(),
                .mac_count(),
                .nonvmm_vector_ops()
            );
        end
    endgenerate

    // MAC 작업량은 layer마다 같은 크기의 파라미터 수식을 LAYERS배 한다.
    // CPU 비교는 층 사이 activation 이동까지 포함한 미융합 기준이다. PIM 비교는
    // 첫 입력과 최종 출력만 메모리 계층 경계를 통과하고, 중간값이 메모리 근처에
    // 남는다고 가정한다. 가중치 최초 적재와 DRAM command는 별도 simulator가 센다.
    // 미융합 CPU 비교 가정의 경계 이동 단어 수. word=16bit=2byte이며 실측 DRAM 트래픽은 아니다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign cpu_boundary_words = LAYERS *
        (24*TOKENS*D_MODEL + 4*TOKENS*D_FF + 4*TOKENS*TOKENS);
    // 중간값을 메모리 가까이 유지한다는 PIM 비교 가정의 경계 이동 단어 수. 실제 칩 계측값은 아니다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign pim_boundary_words = 2*TOKENS*D_MODEL;
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign mac_count = LAYERS *
        (4*TOKENS*D_MODEL*D_MODEL +
         2*TOKENS*TOKENS*D_MODEL +
         2*TOKENS*D_MODEL*D_FF);
    // Softmax/Residual/Norm/활성화의 vector 단계 수. 개별 산술 덧셈 개수와 다르다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign nonvmm_vector_ops = LAYERS * TOKENS * (HEADS+5);

    // elaboration/simulation 설정 검사. 양의 차원/head 나눗셈 조건이 깨진 회로는 오류를 알린다.
    // 매 token에서 모델 shape를 검사하는 동적 FPGA 기능은 아니다.
    initial begin
        if (LAYERS < 1) $error("LAYERS must be at least 1");
    end
endmodule
