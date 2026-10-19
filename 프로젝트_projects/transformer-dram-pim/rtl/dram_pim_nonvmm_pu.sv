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
// DRAM 뱅크 가까이에 두는 비 VMM(행렬곱 이외의 벡터 연산) PU 모델
//
// Transformer에는 행렬곱 외에도 Softmax, LayerNorm, residual 덧셈, ReLU가
// 반복해서 나온다. 이 모듈이 제안서에서 말한 “새로운 PU”에 해당한다. VMM의
// 곱셈 누산기(adder tree)는 별도 dram_pim_vmm_bank 모듈 안에 있다. 따라서
// PU와 adder tree는 서로 다른 연산 경로이며, 이 모듈은 MAC 트리를 대신하지 않는다.
//
// 실제 DRAM 다이 안에 회로를 넣은 결과가 아니라, 뱅크 가까이에 PU가 있다고
// 가정하고 입력·출력 의미와 Transformer 연산 분담을 검증하는 RTL 모델이다.
// 모든 수는 signed Q8.8이며, 예를 들어 정수 256은 실수 1.0을 뜻한다.
// -----------------------------------------------------------------------------
module dram_pim_nonvmm_pu #(
    parameter integer VEC_LEN = 4,
    parameter integer OP_RELU = 0,
    parameter integer OP_ADD = 1,
    parameter integer OP_SOFTMAX = 2,
    parameter integer OP_LAYERNORM = 3
) (
    // 2 비트 연산 선택. 0=ReLU,1=포화 덧셈,2=masked Softmax,3=LayerNorm.
    // 이 legacy 모듈은 하나의 런타임 opcode로 여러 기능 중 하나를 선택합니다.
    input  wire [1:0]                  op,
    // Q8.8 입력 벡터입니다. Softmax이면 attention score, LayerNorm이면 한 token의 D개 hidden 채널입니다.
    input  wire [VEC_LEN*16-1:0]       a_flat,
    // ADD에만 쓰는 두 번째 벡터입니다. 다른 연산에서는 연결되어 있어도 결과 계산에 쓰이지 않습니다.
    input  wire [VEC_LEN*16-1:0]       b_flat,
    // Softmax에서 만 쓰는 원소별 유효 비트. valid_mask[i]=0이면 해당 위치의 확률은 0입니다.
    // causal mask와 미채움 cache를 표현합니다. LayerNorm의 채널 선택용 mask는 아닙니다.
    input  wire [VEC_LEN-1:0]          valid_mask,
    // 선택된 연산의 Q8.8 출력. 조합 출력으로 clk/start/done이 없습니다. 입력이 바뀌면 출력도 변합니다.
    output reg  [VEC_LEN*16-1:0]       y_flat
);

    // 결과가 Q8.8의 signed 16 비트 범위를 넘으면 가장 가까운 표현 가능 값에
    // 고정한다. 단순히 하위 16 비트만 자르면 큰 양수가 음수처럼 보이는 문제가 생긴다.
    // Python model.reference.sat16 및 model.gpt_q88.sat16. 양자화 격자를 유지하고 wrap-around를 막습니다.
    function automatic signed [15:0] sat16(input signed [63:0] value);
        begin
            if (value > 64'sd32767)
                sat16 = 16'sd32767;
            else if (value < -64'sd32768)
                sat16 = -16'sd32768;
            else
                sat16 = value[15:0];
        end
    endfunction

    // 가변 분모 정수 나눗셈을 32 단계 restoring divider로 직접 정의한다. 입력의
    // 최상위 비트부터 나머지에 한 비트씩 넣고, 분모 이상이면 빼서 quotient bit를
    // 세운다. 반복 횟수가 항상 32 회이므로 합성기가 종료 조건이 다른 가변 while
    // 회로를 만들지 않는다. 기능은 unsigned 정수 나눗셈의 버림 결과와 같다.
    // 일반 `/` 연산자를 쓰면 일부 합성 흐름에서 각 PU마다 불필요하게 큰 divider가
    // 만들어지므로, 폭과 구조를 직접 제한하기 위해 이 함수를 사용한다.
    // Python numerator//denominator와 같습니다(둘 다 비음수일 때). denominator=0에서 는 방어적으로 0을 반환합니다.
    // 32 회 for가 32클록을 뜻하지 않습니다. 클록 없는 함수이므로 32단 비교·빼기 연결이 조합 경로가 될 수 있습니다.
    function automatic [31:0] udiv32_fixed(
        input [31:0] numerator,
        input [31:0] denominator
    );
        reg [32:0] remainder_value;
        reg [32:0] denominator_wide;
        reg [31:0] quotient_value;
        integer bit_index;
        begin
            remainder_value = 33'd0;
            denominator_wide = {1'b0, denominator};
            quotient_value = 32'd0;
            if (denominator != 0) begin
                for (bit_index = 31; bit_index >= 0; bit_index = bit_index - 1) begin
                    remainder_value = (remainder_value << 1) | numerator[bit_index];
                    if (remainder_value >= denominator_wide) begin
                        remainder_value = remainder_value - denominator_wide;
                        quotient_value[bit_index] = 1'b1;
                    end
                end
            end
            udiv32_fixed = quotient_value;
        end
    endfunction

    // Softmax의 exp(score - max)를 흉내 내는 작은 조회표(LUT)다. 최댓값을 빼면
    // delta는 0 이하이고 exp(delta)는 0~1 범위가 된다. delta를 0.5 간격으로
    // 묶어 표를 작게 유지한다. 회로 면적을 줄이는 대신 정확도가 조금 낮아지는
    // 연구용 근사이며, 표준 Softmax와 같은 정밀도라고 주장하지 않는다.
    // Python softmax_q8의 exponents lookup입니다. 입력 delta 자체가 raw 정수이므로 128은 실제 0.5입니다.
    // 64를 더해 가장 가까운 0.5 간격으로 고른 뒤 idx10 이상은 표 마지막값 2로 제한합니다.
    // 지수 최소값 2는 실제 exp의 정확한 꼬리가 아닙니다. 수치 근사 오차와 기능 일치 검증을 구분해야 합니다.
    function automatic integer exp_q8(input integer delta);
        integer idx;
        begin
            idx = ((-delta) + 64) / 128;
            case (idx)
                0: exp_q8 = 256;
                1: exp_q8 = 155;
                2: exp_q8 = 94;
                3: exp_q8 = 57;
                4: exp_q8 = 35;
                5: exp_q8 = 21;
                6: exp_q8 = 13;
                7: exp_q8 = 8;
                8: exp_q8 = 5;
                9: exp_q8 = 3;
                10: exp_q8 = 2;
                // LUT 범위 아래에서는 마지막 entry(2)로 saturate한다.
                default: exp_q8 = 2;
            endcase
        end
    endfunction

    // 32 비트 정수의 제곱근을 restoring 알고리즘으로 구한다. 매 반복에서 입력의
    // 2 비트 묶음을 나머지에 넣고 다음 제곱근 비트를 결정한다. 항상 16 번 반복하므로
    // 데이터에 따라 종료 시점이 달라지는 while loop가 없다. 합성기는 이를 고정된
    // 조합 회로로 펼칠 수 있다. 다만 아직 single-cycle 조합 경로이므로 pipeline
    // 단계와 실제 timing closure를 뜻하지 않는다.
    // Python math.isqrt(number)의 정확한 바닥 정수 제곱근입니다.
    // 각 반복은 입력 2 비트를 소비하고 결과 제곱근 1 비트를 결정합니다. 32 비트 입력을 16 쌍 처리합니다.
    function automatic [31:0] isqrt_fixed16(input [31:0] number);
        reg [31:0] remainder;
        reg [31:0] partial_root;
        reg [31:0] trial;
        integer step;
        begin
            remainder = 32'd0;
            partial_root = 32'd0;
            trial = 32'd0;
            for (step = 0; step < 16; step = step + 1) begin
                remainder = (remainder << 2) |
                    ((number >> (30 - 2*step)) & 32'd3);
                trial = (partial_root << 2) | 32'd1;
                if (remainder >= trial) begin
                    remainder = remainder - trial;
                    partial_root = (partial_root << 1) | 32'd1;
                end else begin
                    partial_root = partial_root << 1;
                end
            end
            isqrt_fixed16 = partial_root;
        end
    endfunction

    // LayerNorm에서 필요한 1/sqrt(분산)을 정수 연산으로 근사한다. 분산이 Q8.8일
    // 때 floor(sqrt(2^24 / variance_raw))가 Q8.8 역표준편차다. 가변 나눗셈은
    // udiv32_fixed에 전달해 정수 divider의 폭과 고정 구조를 명시한다.
    // Python: 4096 if variance_raw<=1 else math.isqrt(16777216//variance_raw).
    // 16777216=2^24. var_raw=256*variance이 고 inv_std_raw=256/sqrt(variance)이므로
    // inv_std_raw^2=2^24/var_raw가 됩니다. epsilon raw 1일 때 최대값 4096은 실제 16입니다.
    function automatic integer inv_sqrt_q8(input integer variance_raw);
        integer n;
        integer radicand;
        begin
            if (variance_raw <= 1) begin
            inv_sqrt_q8 = 4096; // epsilon 제한에서 반환할 최대 근사값: Q8.8의 16.0
            end else begin
                radicand = udiv32_fixed(32'd16777216, variance_raw);
                n = isqrt_fixed16(radicand);
                inv_sqrt_q8 = n;
            end
        end
    endfunction

    // integer는 SV에서 32 비트 signed입니다. 평균/합/인덱스 임시값에 쓰고, 제곱합은 64 비트로 넓힙니다.
    // 현재 VEC_LEN4~32 범위에서는 합 폭이 충분합니다. 임의로 수백만 채널로 확장할 때는 폭 검토가 필요합니다.
    integer i;
    integer max_value;
    integer exp_value;
    integer exp_sum;
    integer sum_value;
    integer mean_value;
    integer variance_value;
    integer inv_std_value;
    integer centered_value;
    reg signed [15:0] a_value;
    reg signed [15:0] b_value;
    integer delta_value;
    reg signed [63:0] square_sum;
    reg signed [63:0] centered_wide;
    reg signed [63:0] square_wide;
    reg signed [63:0] norm_product;

    // 조합 출력과 모든 임시값을 먼저 초기화합니다. 분기에서 대입이 빠져 이전 값을 기억하는 latch 생성을 막습니다.
    // case는 Python if op==... 분기에 대응하지만 하드웨어에서는 연산 회로와 선택 mux를 나타냅니다.
    always @* begin
        y_flat = {VEC_LEN*16{1'b0}};
        max_value = -2147483647;
        exp_sum = 0;
        sum_value = 0;
        mean_value = 0;
        variance_value = 1; // Q8.8 기준 epsilon 1/256: 분산이 0이어도 나눗셈이 안전하다.
        inv_std_value = 0;
        centered_value = 0;
        square_sum = 0;
        centered_wide = 0;
        square_wide = 0;
        norm_product = 0;
        a_value = 0;
        b_value = 0;
        delta_value = 0;
        exp_value = 0;

        case (op)
            // Transformer의 residual 경로: 서브레이어 입력과 출력 벡터를 원소별로
            // 더해 원래 표현 정보를 보존한다. 포화 함수가 수치 범위를 지킨다.
            OP_ADD: begin
                for (i = 0; i < VEC_LEN; i = i + 1) begin
                    a_value = $signed(a_flat[i*16 +: 16]);
                    b_value = $signed(b_flat[i*16 +: 16]);
                    y_flat[i*16 +: 16] = sat16($signed(a_value) + $signed(b_value));
                end
            end

            // FFN 첫 번째 선형층 다음의 활성화 함수다. 음수 출력을 0으로 만들어
            // 선형층만 이어 붙였을 때 생기는 선형성 한계를 깨뜨린다.
            OP_RELU: begin
                for (i = 0; i < VEC_LEN; i = i + 1) begin
                    a_value = $signed(a_flat[i*16 +: 16]);
                    y_flat[i*16 +: 16] = (a_value < 0) ? 16'sd0 : a_value;
                end
            end

            // 어텐션 점수를 확률 가중치로 바꾼다. valid_mask=0인 위치는 causal
            // mask가 가린 미래 토큰이므로 최댓값, 지수 합, 확률 출력 모두에서 제외한다.
            OP_SOFTMAX: begin
                for (i = 0; i < VEC_LEN; i = i + 1) begin
                    a_value = $signed(a_flat[i*16 +: 16]);
                    // 먼저 가장 큰 점수를 빼면 exp의 입력이 0 이하가 되어 overflow를
                    // 줄이고, Softmax 결과를 바꾸지 않으면서 계산 범위를 제한한다.
                    if (valid_mask[i] && ($signed(a_value) > max_value))
                        max_value = a_value;
                end
                // 유효 토큰이 하나도 없으면 max_value가 초기값 그대로 남으므로
                // 나눗셈을 건너뛰고 이미 설정한 0 벡터를 반환한다.
                if (max_value != -2147483647) begin
                    for (i = 0; i < VEC_LEN; i = i + 1) begin
                        a_value = $signed(a_flat[i*16 +: 16]);
                        if (valid_mask[i]) begin
                            delta_value = a_value - max_value;
                            exp_value = exp_q8(delta_value);
                            exp_sum = exp_sum + exp_value;
                        end
                    end
                    // 분자와 분모는 동일한 LUT 값의 스케일을 쓰므로 나눗셈 후
                    // Q8.8 확률로 저장한다. 잘린 하위 비트 때문에 합이 정확히 256이
                    // 되지 않을 수 있으며, 검증에서는 작은 오차 범위를 허용한다.
                    if (exp_sum > 0) begin
                        for (i = 0; i < VEC_LEN; i = i + 1) begin
                            a_value = $signed(a_flat[i*16 +: 16]);
                            if (valid_mask[i]) begin
                                delta_value = a_value - max_value;
                                exp_value = exp_q8(delta_value);
                                y_flat[i*16 +: 16] = udiv32_fixed(exp_value * 256, exp_sum);
                            end
                        end
                    end
                end
            end

            // 토큰 하나의 hidden channel을 정규화한다. 평균을 빼고, 분산의 역제곱근을
            // 곱한다. 실제 Transformer가 기대하는 LayerNorm을 기능 수준에서 모델링한다.
            OP_LAYERNORM: begin
                for (i = 0; i < VEC_LEN; i = i + 1)
                    sum_value = sum_value + $signed(a_flat[i*16 +: 16]);
                // SV signed /는 0을 향해 절삭합니다. Python 음수 //는 아래 정수로 내리므로
                // 직접 //를 쓰면 다를 수 있습니다. model.gpt_q88.trunc_div(sum(values),len(values))가 정확한 대응입니다.
                mean_value = sum_value / VEC_LEN;

                for (i = 0; i < VEC_LEN; i = i + 1) begin
                    a_value = $signed(a_flat[i*16 +: 16]);
                    centered_value = $signed(a_value) - mean_value;
                    centered_wide = centered_value;
                    square_wide = centered_wide * centered_wide;
                    square_sum = square_sum + square_wide;
                end
                // 편차 제곱의 합은 Q16.16이 다. 평균을 낸 다음 8 비트 스케일을
                // 되돌려 분산을 Q8.8로 맞춘다.
                // 정수 계산 순서를 유지합니다: 편차(raw)^2 합→원소 수로 나눔→256으로 나눔→epsilon raw 1 추가.
                // 실수 식 variance+epsilon을 한 번에 반올림한 계산과 같은 비트결과를 보장하지 않습니다.
                variance_value = (square_sum / VEC_LEN) / 256 + 1;
                inv_std_value = inv_sqrt_q8(variance_value);

                for (i = 0; i < VEC_LEN; i = i + 1) begin
                    a_value = $signed(a_flat[i*16 +: 16]);
                    centered_value = $signed(a_value) - mean_value;
                    centered_wide = centered_value;
                    norm_product = centered_wide * inv_std_value;
                    y_flat[i*16 +: 16] = sat16(norm_product >>> 8);
                end
            end

            // 예약하지 않은 op에는 0을 반환한다. 알 수 없는 제어값이 X로 퍼져
            // 디버깅을 어렵게 만드는 것을 줄이는 결정적 기본 동작이다.
            default: begin
                y_flat = {VEC_LEN*16{1'b0}};
            end
        endcase
    end
endmodule
