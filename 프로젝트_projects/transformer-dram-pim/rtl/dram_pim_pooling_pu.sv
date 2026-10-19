`timescale 1ns/1ps
// =============================================================================
// 독립 Q8.8 pooling PU: 유효한 window 값의 최대값 또는 평균을 구한다.
//
// PU(Processing Unit)는 데이터를 연산하는 블록이다. 원 제안이 Transformer
// 이외의 일반 ML 연산까지 지원하려고 한 목표에 맞춰 pooling을 별도로 제공한다.
// 표준 GPT decoder에는 pooling 단계가 없으므로 현재 GPT/QAT/Nexys bitstream에
// 이 모듈을 연결하지 않는다. 이름의 dram_pim은 제안된 bank 측 연산 후보라는
// 의미이며 실제 DRAM 칩 내부에 이 RTL을 탑재했다는 뜻이 아니다.
//
// Python model/pooling_q88.py의 pool_q88/pool_details와 같은 계산이다.
// - 입력/출력: signed 16bit Q8.8. raw 정수 x는 실수 x/256을 뜻한다.
// - operation_avg=0: max pooling. operation_avg=1: average pooling.
// - valid_mask[i]=0인 lane은 padding/무효 값이다. max/sum/count 모두 제외한다.
// - 유효 값이 하나도 없으면 결과와 valid_count 모두 0이다.
// - 평균은 넓은 signed 합을 실제 유효 개수로 나누며 0 방향으로 절삭한다.
//   예: raw [-1,-2]의 평균 -1.5 raw는 -1이 된다. 바닥 내림 -2가 아니다.
// - max에서 같은 값이 만나면 왼쪽 가지를 선택한다. index는 출력하지 않는다.
//
// lane i는 values_packed[16*i +: 16]이다. lane0이 가장 낮은 16bit다.
// Python 리스트 순서는 lane0, lane1, ...이며 .mem 문자열은 역순으로 적는다.
// WINDOW가 2의 거듭제곱이 아니면 다음 거듭제곱까지 무효 leaf를 채운다.
// =============================================================================
module dram_pim_pooling_pu #(
    parameter integer WINDOW = 16
) (
    input wire [WINDOW*16-1:0] values_packed,
    input wire [WINDOW-1:0] valid_mask,
    input wire operation_avg,
    output wire signed [15:0] result,
    // WINDOW=1이면 clog2(2)=1이므로 포트 폭이 0이 되지 않는다.
    output wire [$clog2(WINDOW+1)-1:0] valid_count
);
    localparam integer TREE_LEVELS = $clog2(WINDOW);
    localparam integer LEAVES = 1 << TREE_LEVELS;
    localparam integer COUNT_WIDTH = $clog2(WINDOW+1);
    // 입력 최솟값 -32768을 WINDOW개 합해도 넘치지 않는 폭이다.
    // 예: WINDOW16은 20bit이고 -32768*16=-524288을 정확히 표현한다.
    // 합산 전에 값을 16bit로 자르지 않으므로 평균 계산에 wraparound가 없다.
    localparam integer SUM_WIDTH = 16 + TREE_LEVELS;

    // heap식 배열: root=1, 자식=2*n 및 2*n+1, leaf=LEAVES+i.
    // 직렬 for 누산 대신 각 단계의 두 자식을 병렬로 합치는 균형 tree다.
    // count tree도 같은 유효성 규칙을 쓰므로 masked padding으로 평균 분모가
    // 커지지 않는다. max tree는 count=0 가지를 제외하여 음수 입력에 0이
    // 잘못 최대값으로 선택되는 문제를 피한다.
    wire signed [SUM_WIDTH-1:0] sum_tree [1:2*LEAVES-1];
    wire [COUNT_WIDTH-1:0] count_tree [1:2*LEAVES-1];
    wire signed [15:0] max_tree [1:2*LEAVES-1];
    genvar lane;
    generate
        for (lane=0; lane<LEAVES; lane=lane+1) begin : g_leaf
            if (lane<WINDOW) begin : g_real
                wire signed [15:0] lane_value;
                assign lane_value = values_packed[16*lane +: 16];
                // signed sign extension을 명시한다. 음수 raw의 상위 bit를 0으로
                // 채우면 양수로 바뀌므로 합을 넓힐 때 부호 bit를 반복한다.
                assign sum_tree[LEAVES+lane] = valid_mask[lane]
                    ? {{(SUM_WIDTH-16){lane_value[15]}}, lane_value} : {SUM_WIDTH{1'b0}};
                assign count_tree[LEAVES+lane] = valid_mask[lane]
                    ? {{(COUNT_WIDTH-1){1'b0}}, 1'b1} : {COUNT_WIDTH{1'b0}};
                assign max_tree[LEAVES+lane] = valid_mask[lane] ? lane_value : 16'sd0;
            end else begin : g_padding
                // 홀수 WINDOW 등에서 추가한 leaf는 원래 입력이 아니다.
                // count=0으로 설정하여 어떤 pooling 연산에도 참여시키지 않는다.
                assign sum_tree[LEAVES+lane] = {SUM_WIDTH{1'b0}};
                assign count_tree[LEAVES+lane] = {COUNT_WIDTH{1'b0}};
                assign max_tree[LEAVES+lane] = 16'sd0;
            end
        end
    endgenerate

    genvar node;
    generate
        for (node=1; node<LEAVES; node=node+1) begin : g_reduce
            assign sum_tree[node] = sum_tree[2*node] + sum_tree[2*node+1];
            assign count_tree[node] = count_tree[2*node] + count_tree[2*node+1];
            assign max_tree[node] = (count_tree[2*node] == 0)
                ? max_tree[2*node+1]
                : ((count_tree[2*node+1] == 0) ? max_tree[2*node]
                : ((max_tree[2*node] >= max_tree[2*node+1])
                   ? max_tree[2*node] : max_tree[2*node+1]));
        end
    endgenerate

    wire signed [SUM_WIDTH-1:0] positive_divisor;
    wire signed [SUM_WIDTH-1:0] average_wide;
    // unsigned count를 signed 양수 wire로 넓혀 두 operand의 부호를 일치시킨다.
    // empty에서는 sum=0이고 분모를 1로 대체하여 내부의 0/0도 발생시키지 않는다.
    // 중요: 나눗셈을 unsigned concat이 있는 ?: 조건식 안에 넣으면 expression
    // context가 unsigned가 되어 음수 평균이 틀릴 수 있다. signed wire 두 개의
    // 직접 나눗셈으로 분리한다. 실제 WINDOW3의 -32768 평균 시험에서 확인한
    // 이 오류와 수정 전 로그는 별도 build/pooling_pu/history_*에 보존한다.
    // SystemVerilog signed 정수 나눗셈은 음수 결과도 0 방향으로 절삭한다.
    assign positive_divisor = (count_tree[1] != 0)
        ? {{(SUM_WIDTH-COUNT_WIDTH){1'b0}}, count_tree[1]}
        : {{(SUM_WIDTH-1){1'b0}}, 1'b1};
    assign average_wide = sum_tree[1] / positive_divisor;
    assign valid_count = count_tree[1];
    // 유효 값의 산술 평균은 입력 최소/최대 범위 안에 있으므로 16bit에 맞는다.
    // 고정소수점의 소수 bit는 그대로 8개다. 추가 *256 또는 >>8은 필요 없다.
    assign result = (count_tree[1] == 0) ? 16'sd0
        : (operation_avg ? average_wide[15:0] : max_tree[1]);

`ifndef SYNTHESIS
    initial begin
        if (WINDOW < 1) $fatal(1, "pooling WINDOW must be >=1");
    end
`endif
endmodule
