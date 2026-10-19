// [코드 읽기 안내] 이 파일의 16 비트 원소는 signed Q8.8 raw 값입니다.
// raw/256이 실제 수입니다. 256→1.0, -128→-0.5이며 범위는 -128~127.99609375입니다.
// *_flat은 여러 원소를 한 긴 비트벡터에 포장한 것입니다. i*16 +:16은 i번째 원소이며
// Python list[i]에 대응합니다. 비트 조각은 signed 속성을 잃을 수 있어 $signed로 해석합니다.
// function은 Python 함수처럼 읽을 수 있지만 합성 시 조합 회로가 됩니다. 함수 호출을
// 여러 번 쓰면 회로가 복제될 수도 있습니다. automatic은 호출별 임시 변수 공간을 뜻합니다.
// always @*의 blocking 대입(=)은 현재 입력에서 바로 결과를 만드는 조합 연산을 기술합니다.
// posedge 블록의 nonblocking 대입(<=)은 다음 레지스터 값을 예약합니다. 모든 우변은
// 그 클록 직전 상태를 기준으로 읽습니다. Python 순차 대입과 다른 가장 중요한 부분입니다.
// for/generate의 고정 반복은 합성할 때 회로를 펼치는 표현입니다. 시뮬레이터에서 반복문이
// 끝났다고 FPGA의 물리 지연이 0인 것은 아닙니다. 실제 경로 지연은 Vivado timing으로 봅니다.
// `timescale 1 ns/1ps는 시뮬레이션 시간 단위/해상도이며 FPGA 클록 주파수를 설정하지 않습니다.
`timescale 1ns/1ps
// -----------------------------------------------------------------------------
// Transformer 디코더 블록의 단계별 작업을 순서대로 발행하는 공유 스케줄러
//
// VMM(MAC 트리)과 비 VMM PU(Softmax/LayerNorm/residual/ReLU)가 언제 실행되는지
// 하나의 FSM으로 나타낸다. 이 순서는 Transformer 연산 의존관계를 반영한다.
// stage_cycles() 값은 연구자가 정한 “한 MAC=1 서비스 주기, PU=지정 주기” 모델이다.
// 합성 후의 클록 주기, DRAM 명령 타이밍, 실제 뱅크 충돌을 측정한 값은 아니다.
// -----------------------------------------------------------------------------
module dram_pim_scheduler #(
    parameter integer TOKENS = 4,
    parameter integer D_MODEL = 4,
    parameter integer D_FF = 8,
    parameter integer PU_STAGE_CYCLES = 8
) (
    // 스케줄러 상태/remaining 레지스터를 갱신하는 클록. posedge에서 만 단계가 바뀝니다.
    input  wire clk,
    // active-low 비동기 초기화.0을 주면클록없이즉시 busy/done/state/remaining을 초기화합니다.
    input  wire rst_n,
    // idle에서 작업을 시작하는 제어.입력활성값/가중치 자체를여기서저장하지는않습니다.
    input  wire start,
    // stage service countdown이 진행 중임을 알립니다. 물리 연산기의 valid나 DRAM busy 실측이 아닙니다.
    output reg  busy,
    // 전체단계가 끝난때한 클록동안 1인완료 pulse. Python blocking return과 달리외부소비자가동시에관찰해야합니다.
    output reg  done,
    // 현재단계의 4 비트번호. 숫자의크기는출력정확도나성능이아니라 FSM 분기를 구별하는 코드입니다.
    output reg  [3:0] stage,
    // 마지막 LayerNorm stage의 마지막 service clock임을 표시.상위모듈은이때조합최종 결과를등록합니다.
    output wire final_cycle,
    // 정한 MAC/PU 서비스가정으로 계산한 cycle 수. FPGA 실제시계주파수나 DRAM latency 측정이아닙니다.
    output wire [31:0] modeled_latency_cycles
);
    // 단계 번호는 4 비트 FSM 상태다. QKV 투영부터 시작해 어텐션, residual,
    // 정규화, FFN을 순서대로 거친 뒤 마지막 LayerNorm에서 완료한다.
    localparam [3:0] ST_IDLE       = 4'd0;
    localparam [3:0] ST_QKV         = 4'd1;
    localparam [3:0] ST_SCORE       = 4'd2;
    localparam [3:0] ST_SOFTMAX     = 4'd3;
    localparam [3:0] ST_CONTEXT     = 4'd4;
    localparam [3:0] ST_OUTPUT      = 4'd5;
    localparam [3:0] ST_RESIDUAL1   = 4'd6;
    localparam [3:0] ST_LAYERNORM1  = 4'd7;
    localparam [3:0] ST_FFN1        = 4'd8;
    localparam [3:0] ST_RELU        = 4'd9;
    localparam [3:0] ST_FFN2        = 4'd10;
    localparam [3:0] ST_RESIDUAL2   = 4'd11;
    localparam [3:0] ST_LAYERNORM2  = 4'd12;

    // Python의 remaining countdown에해당하는 32 비트레지스터.파라미터기반 stage_cycles 값을로드하고
    // 매 클록 1씩줄입니다.0/1판정을써마지막 service clock에서 다음단계로 진행합니다.
    reg [31:0] remaining;

    // 현재 작은 설정에서는 행렬곱의 MAC 수를 서비스 주기로 사용한다.
    // 실제 구현에서 MAC 병렬도 P를 정하면 각 VMM 단계 주기는 MAC 수/P에 가까워지고,
    // 여기에 메모리 접근, 파이프라인 채움, 충돌 대기를 더해야 한다.
    // Python교육표현: stage_work={QKV:3*T*D*D,...}; remaining=stage_work[stage].
    // MAC 수식은행렬출력원소 수×내적길이입니다.여기선 1MAC=1cycle이라는연구가정입니다.
    // analysis.dram_pim_model.simulate_pim_compute는 bank/parallelism 가정이추가된별도모델입니다.
    function automatic [31:0] stage_cycles(input [3:0] selected_stage);
        begin
            case (selected_stage)
                ST_QKV:        stage_cycles = 3*TOKENS*D_MODEL*D_MODEL;
                ST_SCORE:      stage_cycles = TOKENS*TOKENS*D_MODEL;
                ST_SOFTMAX:    stage_cycles = PU_STAGE_CYCLES;
                ST_CONTEXT:    stage_cycles = TOKENS*TOKENS*D_MODEL;
                ST_OUTPUT:     stage_cycles = TOKENS*D_MODEL*D_MODEL;
                ST_RESIDUAL1:  stage_cycles = PU_STAGE_CYCLES;
                ST_LAYERNORM1: stage_cycles = PU_STAGE_CYCLES;
                ST_FFN1:       stage_cycles = TOKENS*D_MODEL*D_FF;
                ST_RELU:       stage_cycles = PU_STAGE_CYCLES;
                ST_FFN2:       stage_cycles = TOKENS*D_FF*D_MODEL;
                ST_RESIDUAL2:  stage_cycles = PU_STAGE_CYCLES;
                ST_LAYERNORM2: stage_cycles = PU_STAGE_CYCLES;
                default:       stage_cycles = 0;
            endcase
        end
    endfunction

    // 블록 전체의 산술량을 같은 가정으로 계산한 예상 주기다.
    // 테스트벤치는 FSM이 이 모델 수치와 일치하는지 확인한다.
    assign modeled_latency_cycles =
        4*TOKENS*D_MODEL*D_MODEL +
        2*TOKENS*TOKENS*D_MODEL +
        2*TOKENS*D_MODEL*D_FF +
        6*PU_STAGE_CYCLES;
    // 최종 결과를 내보낼 시점이다. top-level은 이 신호에서 결과 레지스터를 갱신한다.
    assign final_cycle = busy && (stage == ST_LAYERNORM2) && (remaining <= 1);

    // FSM(Finite State Machine)은현재 state와 입력으로 다음 state를 정하는작은제어회로입니다.
    // 여기 nonblocking <=는한 클록의모든레지스터가동시에갱신되도록예약합니다.
    // done<=0을 매 clock 기본으로두고완료때만 1로 덮어 pulse를 만듭니다.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            busy <= 1'b0;
            done <= 1'b0;
            stage <= ST_IDLE;
            remaining <= 0;
        end else begin
            done <= 1'b0;
            if (!busy) begin
                if (start) begin
                    busy <= 1'b1;
                    stage <= ST_QKV;
                    // start를 받은 clock은 QKV 서비스시작설정입니다.테스트벤치는이후 done까지 count해서모델식과비교합니다.
                    remaining <= stage_cycles(ST_QKV);
                end
            end else if (remaining <= 1) begin
                // 단계의 남은 서비스 주기가 끝나면 다음 Transformer 연산 단계로 이동한다.
                // final stage가 끝나면 busy를 내리고 done을 한 클록 동안 올린다.
                if (stage == ST_LAYERNORM2) begin
                    busy <= 1'b0;
                    done <= 1'b1;
                    stage <= ST_IDLE;
                    remaining <= 0;
                end else begin
                    // 단계 번호를연속으로정했으므로+1이 다음연산단계입니다.이때 새 remaining은 이전 stage+1의 값입니다.
                    // <=는즉시값을 바꾸지않으므로 stage_cycles(stage)는아직이전단계가된다는점에주의합니다.
                    stage <= stage + 1'b1;
                    remaining <= stage_cycles(stage + 1'b1);
                end
            end else begin
                remaining <= remaining - 1'b1;
            end
        end
    end
endmodule
