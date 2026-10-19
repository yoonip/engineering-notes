// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// -----------------------------------------------------------------------------
// 외부 트랜잭션 인터페이스: 기능 datapath + 단계 스케줄러
//
// start가 들어오면 현재 입력과 가중치로 기능 결과를 계산해 pending 레지스터에
// 보관하고, 공유 FSM이 Transformer 작업량에 해당하는 서비스 주기를 세는 동안
// 결과를 외부에 노출하지 않는다. 마지막 단계가 끝날 때 y_flat을 갱신하고 done을
// 한 클록 올린다. 현재 datapath의 내부 곱셈/Softmax 계산 자체는 조합식이므로,
// 실제 각 단계마다 값이 순차적으로 흘러가는 cycle-accurate 설계는 아니다.
// 실제 FPGA/칩 타이밍이라고 오해하지 않도록 이 구조를 명시한다.
// -----------------------------------------------------------------------------
// [학습용 상세 해설 2026-10-04]
// 위치: 최초 단일-head 기능 core를 start/busy/done transaction으로 감싼 wrapper.
// Python 대응: model/reference.py:transformer_block이 result_comb에 해당한다.
// start에서 조합 결과를 pending register에 저장하고 scheduler 서비스 주기 뒤 공개한다.
// scheduler 대기만으로 내부 dot product가 시간 분할되지 않는다. 실제 shared-MAC/KV
// 설계를 공부하려면 transformer_gpt_kvcache_seq를 읽는다. Python에는 물리 clock FSM이 없다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module transformer_decoder_pim #(
    // context 토큰 수 T. attention 점수는 T*T개이며 문자열 byte 수와 항상 같지는 않다.
    parameter integer TOKENS = 4,
    // 토큰마다 hidden 숫자 수 D. embedding/residual 폭이며 모든 head 채널 수 합이 D다.
    parameter integer D_MODEL = 4,
    // FFN 중간 채널 수 F. W1=D*F, W2=F*D이고 폭을 키우면 연산/저장 비용도 커진다.
    parameter integer D_FF = 8,
    // scaled QK 점수에 쓰는 1/sqrt(D_MODEL)의 Q8.8 근삿값을 top까지 노출한다.
    // D_MODEL=4의 기본값은 128(0.5)이며, 다른 모델 폭에서는 호출자가 갱신한다.
    // round(256/sqrt(head_dim)) 정수. QK의 차원 효과를 완화하며 head_dim=4일 때 128=0.5다.
    parameter integer SCORE_SCALE_Q8 = 128,
    // 최초 scheduler의 가정 PU 서비스 주기. 실제 원본 조합 PU의 지연 클록을 측정한 숫자는 아니다.
    parameter integer PU_VECTOR_CYCLES = 8
) (
    // clk/rst_n/start는 트랜잭션 외부 제어다. reset은 active-low이며,
    // start는 idle 상태에서만 새 입력 계산을 받아들인다.
    // 클록 입력. 순차 회로는 상승 에지에서 계산 결과를 register에 저장한다. comb wrapper에서는 비교용으로만 남는다.
    input  wire clk,
    // 0일 때 초기화하는 active-low reset. scheduler와 결과 register의 시작 상태를 맞춘다.
    input  wire rst_n,
    // 계산 요청. 순차 core는 idle에서만 수락하므로 ready/busy 확인 후 한 클록 펄스를 준다.
    input  wire start,
    // start 순간에 고정되는 입력 hidden state와 학습 가중치 행렬들이다.
    // 각 원소는 signed Q8.8이며 row-major 순서로 묶는다.
    // [토큰][hidden 채널] 입력 숫자 표현. embedding이 끝난 행렬이고 원문 문자열이 아니며 Python x/state에 해당한다.
    input  wire [TOKENS*D_MODEL*16-1:0] x_flat,
    // [입력 채널][출력 채널] Query 가중치. Python qmat(x,wq)가 찾을 정보의 특징 Q를 만든다.
    input  wire [D_MODEL*D_MODEL*16-1:0] wq_flat,
    // [입력 채널][출력 채널] Key 가중치. Python qmat(x,wk)가 비교할 검색 대상 특징 K를 만든다.
    input  wire [D_MODEL*D_MODEL*16-1:0] wk_flat,
    // [입력 채널][출력 채널] Value 가중치. Python qmat(x,wv)가 attention 비중으로 합칠 내용 V를 만든다.
    input  wire [D_MODEL*D_MODEL*16-1:0] wv_flat,
    // [D_MODEL][D_MODEL] attention 출력 투영. Python qmat(context,wo)가 head 내용을 전체 hidden 채널에 섞는다.
    input  wire [D_MODEL*D_MODEL*16-1:0] wo_flat,
    // [D_MODEL][D_FF] FFN 확장 가중치. token마다 특징 폭을 늘린 뒤 비선형 활성화한다.
    input  wire [D_MODEL*D_FF*16-1:0] w1_flat,
    // [D_FF][D_MODEL] FFN 축소 가중치. 활성화 결과를 residual에 더할 원래 hidden 폭으로 되돌린다.
    input  wire [D_FF*D_MODEL*16-1:0] w2_flat,
    // busy 중 새 start는 무시한다. done은 마지막 단계에서 한 clock 동안 올라간다.
    // 계산 중 또는 결과 소비 대기 상태. 1이면 새 start를 수락하지 않는다.
    output wire busy,
    // 계산 완료 한 클록 pulse. KV 결과를 지속해서 읽으려면 result_valid도 확인한다.
    output wire done,
    // decoder block/stack 최종 hidden [토큰][채널]. 문자가 아니라 LM head로 전달하는 내부 표현이다.
    output reg  [TOKENS*D_MODEL*16-1:0] y_flat,
    // 미융합 CPU 비교 가정의 경계 이동 단어 수. word=16bit=2byte이며 실측 DRAM 트래픽은 아니다.
    output wire [31:0] cpu_boundary_words,
    // 중간값을 메모리 가까이 유지한다는 PIM 비교 가정의 경계 이동 단어 수. 실제 칩 계측값은 아니다.
    output wire [31:0] pim_boundary_words,
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    output wire [31:0] mac_count,
    // Softmax/Residual/Norm/활성화의 vector 단계 수. 개별 산술 덧셈 개수와 다르다.
    output wire [31:0] nonvmm_vector_ops,
    // scheduler의 가정 서비스 주기. 실제 pipeline clock latency를 검증한 수치로 쓰면 안 된다.
    output wire [31:0] modeled_latency_cycles,
    // 가정 scheduler의 현재 구간 번호. 파형에서 작업 흐름을 확인하는 디버그 출력이다.
    output wire [3:0] scheduler_stage
);

    // 원본 single-head core의 즉시 조합 출력. pending 저장 전에 모든 stage 수학이 연결돼 있다.
    wire [TOKENS*D_MODEL*16-1:0] result_comb;
    // 원본 scheduler가 마지막 서비스 구간임을 알리는 신호. 이때 pending을 출력으로 복사한다.
    wire scheduler_final_cycle;
    // 요청 순간 계산된 전체 결과를 scheduler 종료까지 보관하는 transaction register.
    reg [TOKENS*D_MODEL*16-1:0] result_pending;

    transformer_decoder_pim_comb #(
        .TOKENS(TOKENS),
        .D_MODEL(D_MODEL),
        .D_FF(D_FF),
        .SCORE_SCALE_Q8(SCORE_SCALE_Q8)
    // Python transformer_block의 전체 조합 core. scheduler는 결과 공개 시점만 관리한다.
    ) u_datapath (
        .x_flat(x_flat),
        .wq_flat(wq_flat),
        .wk_flat(wk_flat),
        .wv_flat(wv_flat),
        .wo_flat(wo_flat),
        .w1_flat(w1_flat),
        .w2_flat(w2_flat),
        .y_flat(result_comb),
        .cpu_boundary_words(cpu_boundary_words),
        .pim_boundary_words(pim_boundary_words),
        .mac_count(mac_count),
        .nonvmm_vector_ops(nonvmm_vector_ops)
    );

    dram_pim_scheduler #(
        .TOKENS(TOKENS),
        .D_MODEL(D_MODEL),
        .D_FF(D_FF),
        .PU_STAGE_CYCLES(PU_VECTOR_CYCLES)
    // 가정 서비스 주기 제어. 원본 조합 core 내부에 실제 pipeline register를 삽입하는 회로가 아니다.
    ) u_scheduler (
        .clk(clk), .rst_n(rst_n), .start(start),
        .busy(busy), .done(done), .stage(scheduler_stage),
        .final_cycle(scheduler_final_cycle),
        .modeled_latency_cycles(modeled_latency_cycles)
    );

    // 비동기 active-low reset에서 출력과 보류 결과를 0으로 초기화한다.
    // 트랜잭션 수락 때 결과를 저장하고, 스케줄러가 최종 완료를 알릴 때만 갱신한다.
    // posedge clk에서 RHS를 이전 register 값으로 계산하고 <= nonblocking으로 동시에 갱신한다.
    // negedge reset_n/rst_n은 비동기 reset이다. 물리 board에서는 reset 해제를 동기화해야 한다.
    // Python 대입과 달리 <= 새 값은 같은 always의 아래 줄에서 즉시 읽히지 않는다.
    // 그래서 residual 저장/Norm 계산, 마지막 layer 저장/다음 layer 복사를 상태로 나눈다.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            y_flat <= {TOKENS*D_MODEL*16{1'b0}};
            result_pending <= {TOKENS*D_MODEL*16{1'b0}};
        end else begin
            if (start && !busy)
                result_pending <= result_comb;
            if (scheduler_final_cycle)
                y_flat <= result_pending;
        end
    end
endmodule
