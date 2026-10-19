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
// 합성을 위해 기능별로 나눈 비 VMM Processing Unit (PU)
//
// 이전 범용 PU 하나에는 Softmax, LayerNorm, 덧셈, ReLU가 모두 들어 있었다. RTL
// 시뮬레이션에는 편하지만 각 인스턴스가 모든 함수를 갖고 있어 합성 시 불필요한
// divider/LUT까지 복제될 수 있다. 여기서는 동작 종류를 모듈 경계에서 고정해
// 실제 사용하는 함수만 회로에 포함한다. 수치 의미는 legacy PU와 같은 Q8.8 규칙이다.
// -----------------------------------------------------------------------------

// [포화 덧셈 PU] Python [sat16(a[i]+b[i]) for i in ...]. Transformer residual와 bias 덧셈에 해당합니다.
// 하나의 입력이 Q8.8이면 다른 입력도 같은 scale이어야 덧셈이 의미 있습니다.
module dram_pim_add_pu #(
    parameter integer VEC_LEN = 4
) (
    // a_flat은 원소 VEC_LEN개를 16 비트씩 포장한 Q8.8 입력입니다. a_flat[i*16 +:16]이 Python a[i]입니다.
    input wire [VEC_LEN*16-1:0] a_flat,
    // b_flat은 residual/bias 덧셈의 두 번째 입력이며 a와 같은 Q8.8 scale을 사용합니다.
    input wire [VEC_LEN*16-1:0] b_flat,
    // y_flat은 조합 결과이며 reg라는문법만으로 저장 레지스터가 되지는 않습니다. always @*이면조합 회로입니다.
    output reg  [VEC_LEN*16-1:0] y_flat
);
    // 두 signed 16 비트의 합은 최소 17 비트로 받아야 합니다. 이 함수의 33 비트 입력은 넓은 비교를 위한 여유입니다.
    // Python int는 폭이 자동 확장되지만 하드웨어 bit width는 선언한 범위까지만 보존됩니다.
    function automatic signed [15:0] sat16(input signed [32:0] value);
        begin
            if (value > 33'sd32767) sat16 = 16'sd32767;
            else if (value < -33'sd32768) sat16 = -16'sd32768;
            else sat16 = value[15:0];
        end
    endfunction

    integer i;
    reg signed [15:0] a_value;
    reg signed [15:0] b_value;
    always @* begin
        y_flat = {VEC_LEN*16{1'b0}};
        a_value = 0;
        b_value = 0;
        for (i = 0; i < VEC_LEN; i = i + 1) begin
            a_value = $signed(a_flat[i*16 +: 16]);
            b_value = $signed(b_flat[i*16 +: 16]);
            y_flat[i*16 +: 16] = sat16($signed(a_value) + $signed(b_value));
        end
    end
endmodule

// [ReLU PU] Python [max(0,x) for x in values]. FFN의 비선형 단계입니다.
// GELU full-ops checkpoint에서 는 GELU 경로가 쓰이고 이 모듈은 기존 ReLU 비교 구성에 쓰입니다.
module dram_pim_relu_pu #(
    parameter integer VEC_LEN = 4
) (
    // a_flat은 원소 VEC_LEN개를 16 비트씩 포장한 Q8.8 입력입니다. a_flat[i*16 +:16]이 Python a[i]입니다.
    input wire [VEC_LEN*16-1:0] a_flat,
    // y_flat은 조합 결과이며 reg라는문법만으로 저장 레지스터가 되지는 않습니다. always @*이면조합 회로입니다.
    output reg  [VEC_LEN*16-1:0] y_flat
);
    integer i;
    reg signed [15:0] a_value;
    always @* begin
        y_flat = {VEC_LEN*16{1'b0}};
        a_value = 0;
        for (i = 0; i < VEC_LEN; i = i + 1) begin
            a_value = $signed(a_flat[i*16 +: 16]);
            y_flat[i*16 +: 16] = (a_value < 0) ? 16'sd0 : a_value;
        end
    end
endmodule

// GELU PU: GELU(x)=x*Phi(x)를 Q8.8 table + 선형 보간으로 근사합니다.
// -8..8 범위를 0.25 간격으로 나눈 65 개 상수는 model/gpt_q88.py의
// GELU_LUT_Q8과 같습니다. 작은 음수는 약간 음수로, 큰 음수는 0에 가까이,
// 양수는 입력을 통과시키는 GELU의 모양을 보존합니다. 표 밖은 x<=-8에서 0,
// x>=8에서 x를 반환합니다. 점별 계산은 software와 RTL에서 같은 integer rule입니다.
// [GELU PU] Python model.gpt_q88.gelu_q8를 원소마다 적용합니다.
// GELU는 음수를 모두 0으로 만드는 ReLU와 달리 작은 음수를 약하게 통과시키는 FFN 활성화입니다.
// 실수 erf/tanh를 FPGA에서 직접 구하는 대신 고정 65 개 표와 선형 보간을 씁니다.
module dram_pim_gelu_pu #(
    parameter integer VEC_LEN = 4
) (
    // a_flat은 원소 VEC_LEN개를 16 비트씩 포장한 Q8.8 입력입니다. a_flat[i*16 +:16]이 Python a[i]입니다.
    input wire [VEC_LEN*16-1:0] a_flat,
    // y_flat은 조합 결과이며 reg라는문법만으로 저장 레지스터가 되지는 않습니다. always @*이면조합 회로입니다.
    output reg  [VEC_LEN*16-1:0] y_flat
);
    // GELU_LUT_Q8[index]에 대응하는 case 조회표입니다. index 0은 x=-8, index32는 0, index64는 8입니다.
    // 이 상수는 학습 가중치가 아니라 선택한 활성화 근사 함수의 값입니다.
    function automatic integer gelu_table(input integer index);
        begin
            case (index)
                0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19: gelu_table = 0;
                20: gelu_table = -1; 21: gelu_table = -2; 22: gelu_table = -4;
                23: gelu_table = -7; 24: gelu_table = -12; 25: gelu_table = -18;
                26: gelu_table = -26; 27: gelu_table = -34; 28: gelu_table = -41;
                29: gelu_table = -44; 30: gelu_table = -39; 31: gelu_table = -26;
                32: gelu_table = 0; 33: gelu_table = 38; 34: gelu_table = 89;
                35: gelu_table = 148; 36: gelu_table = 215; 37: gelu_table = 286;
                38: gelu_table = 358; 39: gelu_table = 430; 40: gelu_table = 500;
                41: gelu_table = 569; 42: gelu_table = 636; 43: gelu_table = 702;
                44: gelu_table = 767; 45: gelu_table = 832; 46: gelu_table = 896;
                47: gelu_table = 960; 48: gelu_table = 1024; 49: gelu_table = 1088;
                50: gelu_table = 1152; 51: gelu_table = 1216; 52: gelu_table = 1280;
                53: gelu_table = 1344; 54: gelu_table = 1408; 55: gelu_table = 1472;
                56: gelu_table = 1536; 57: gelu_table = 1600; 58: gelu_table = 1664;
                59: gelu_table = 1728; 60: gelu_table = 1792; 61: gelu_table = 1856;
                62: gelu_table = 1920; 63: gelu_table = 1984; 64: gelu_table = 2048;
                default: gelu_table = 0;
            endcase
        end
    endfunction

    // 입력 raw를 2048만큼 이동해 양수 offset을 만든 뒤 64(raw 0.25)로 나눠 구간과 나머지를 구합니다.
    // lower+(upper-lower)*remainder/64가 선형 보간입니다. 음수 차이에 signed /가 적용되어
    // Python trunc_div(difference*remainder,64)를 써야 정확하게 일치합니다.
    function automatic signed [15:0] gelu_q8(input signed [15:0] value);
        integer offset;
        integer table_index;
        integer remainder_value;
        integer lower_value;
        integer upper_value;
        integer interpolated;
        begin
            if (value <= -16'sd2048) gelu_q8 = 16'sd0;
            else if (value >= 16'sd2048) gelu_q8 = value;
            else begin
                offset = $signed(value) + 2048;
                table_index = offset / 64;
                remainder_value = offset % 64;
                lower_value = gelu_table(table_index);
                upper_value = gelu_table(table_index + 1);
                // signed integer division은 0을 향한 절삭이며 Python trunc_div와 같다.
                interpolated = lower_value + ((upper_value-lower_value)*remainder_value)/64;
                if (interpolated > 32767) gelu_q8 = 16'sd32767;
                else if (interpolated < -32768) gelu_q8 = -16'sd32768;
                else gelu_q8 = interpolated[15:0];
            end
        end
    endfunction

    integer i;
    reg signed [15:0] value;
    always @* begin
        y_flat = {VEC_LEN*16{1'b0}};
        value = 16'sd0;
        for (i = 0; i < VEC_LEN; i = i + 1) begin
            value = $signed(a_flat[i*16 +: 16]);
            y_flat[i*16 +: 16] = gelu_q8(value);
        end
    end
endmodule

// [Softmax PU] Python model.gpt_q88.softmax_q8(logits,valid). 점수→attention 가중치를 계산합니다.
// 임의의 vocabulary sampling Softmax와 혼동하지 마세요. 여기 출력은 이전 token의 V를 섞는 가중치입니다.
// 현재 분모 16 비트 구조는 최대 256*VEC_LEN<65536 조건이 필요합니다. VEC_LEN32는 안전하며
// VEC_LEN256 동점에서는 합 65536이 16 비트로 잘리므로 그 크기로 확장하기 전 divider 폭을 늘려야 합니다.
module dram_pim_softmax_pu #(
    parameter integer VEC_LEN = 4
) (
    // a_flat은 원소 VEC_LEN개를 16 비트씩 포장한 Q8.8 입력입니다. a_flat[i*16 +:16]이 Python a[i]입니다.
    input wire [VEC_LEN*16-1:0] a_flat,
    // valid_mask의 각 1 비트는한 score 원소의유효성. 미래 token 또는미채움 cache 원소는 0으로 가립니다.
    input wire [VEC_LEN-1:0] valid_mask,
    // y_flat은 조합 결과이며 reg라는문법만으로 저장 레지스터가 되지는 않습니다. always @*이면조합 회로입니다.
    output reg  [VEC_LEN*16-1:0] y_flat
);
    // Softmax 확률은 0~256 Q8.8이 고, 분모는 최대 VEC_LEN*256이 다.
    // 분모를 16 비트로 제한하고 17 단계 restoring divider를 사용한다.
    // 분자 최대 256*256=65536이므로 17비트, 현재 32 token 분모 최대 8192이므로 16 비트면 충분합니다.
    // Python exp_raw*256//exp_total. unsigned 양수 divider이므로 버림이 확률의 Q8.8 양자화입니다.
    // 단계 17은 조합 depth이며 17 clock latency를 의미하지 않습니다.
    function automatic [16:0] udiv17by16(
        input [16:0] numerator,
        input [15:0] denominator
    );
        reg [16:0] remainder_value;
        reg [16:0] denominator_wide;
        reg [16:0] quotient_value;
        integer bit_index;
        begin
            remainder_value = 17'd0;
            denominator_wide = {1'b0, denominator};
            quotient_value = 17'd0;
            if (denominator != 0) begin
                for (bit_index = 16; bit_index >= 0; bit_index = bit_index - 1) begin
                    remainder_value = (remainder_value << 1) | numerator[bit_index];
                    if (remainder_value >= denominator_wide) begin
                        remainder_value = remainder_value - denominator_wide;
                        quotient_value[bit_index] = 1'b1;
                    end
                end
            end
            udiv17by16 = quotient_value;
        end
    endfunction

    // delta=max를 뺀 score_raw. maximum 항은 delta0→exp_raw 256이 고 점수 차이 0.5는 약 155입니다.
    // 전체 exp값의 같은 scale이 분자/분모에서 약분되며 결과에 256을 곱해 확률 raw를 돌려줍니다.
    function automatic integer exp_q8(input integer delta);
        integer idx;
        begin
            idx = ((-delta) + 64) / 128;
            case (idx)
                0: exp_q8 = 256; 1: exp_q8 = 155; 2: exp_q8 = 94;
                3: exp_q8 = 57;  4: exp_q8 = 35;  5: exp_q8 = 21;
                6: exp_q8 = 13;  7: exp_q8 = 8;   8: exp_q8 = 5;
                9: exp_q8 = 3;   10: exp_q8 = 2;
                // Python 기준 모델과 같이 LUT 인덱스 10 아래로 saturate한다.
                // delta가 더 작더라도 최소 exp 근사값 2를 유지해야 긴 context의
                // attention 확률이 RTL/Python에서 같은 정수값이 된다.
                default: exp_q8 = 2;
            endcase
        end
    endfunction

    integer i;
    integer maximum;
    integer delta;
    integer exp_value;
    integer exp_total;
    reg signed [15:0] value;
    reg [VEC_LEN*9-1:0] unused_width_anchor;
    // Python exponents list에 해당하는 조합 임시배열. masked 항은 0, unmasked 항은 2~256입니다.
    // 이미 계산한 지수값을 보존해 확률을 만드는 loop에서 같은 LUT 계산을 다시 쓰지 않습니다.
    reg [15:0] exponentials [0:VEC_LEN-1];

    always @* begin
        y_flat = {VEC_LEN*16{1'b0}};
        maximum = -2147483647;
        delta = 0;
        exp_value = 0;
        exp_total = 0;
        value = 0;
        unused_width_anchor = 0;
        for (i = 0; i < VEC_LEN; i = i + 1) begin
            exponentials[i] = 0;
            value = $signed(a_flat[i*16 +: 16]);
            if (valid_mask[i] && ($signed(value) > maximum)) maximum = value;
        end
        if (maximum != -2147483647) begin
            for (i = 0; i < VEC_LEN; i = i + 1) begin
                value = $signed(a_flat[i*16 +: 16]);
                if (valid_mask[i]) begin
                    delta = $signed(value) - maximum;
                    exponentials[i] = exp_q8(delta);
                    exp_total = exp_total + exponentials[i];
                end
            end
            if (exp_total > 0) begin
                for (i = 0; i < VEC_LEN; i = i + 1)
                    if (valid_mask[i])
                        y_flat[i*16 +: 16] = udiv17by16(
                            exponentials[i] * 17'd256,
                            exp_total[15:0]
                        );
            end
        end
    end
endmodule

// [LayerNorm PU] Python model.gpt_q88.layernorm_q8. 한 token의 hidden 채널들을 정규화합니다.
// 이 PU에는 학습 gamma/beta가 없습니다. full-ops cache top은 PU 출력 뒤 별도 곱·덧셈으로 affine을 적용합니다.
// 정규화로 채널값의 scale을 안정시켜 다음 QKV/FFN 가중치 곱셈을 지나치게 크게 만들지 않도록 합니다.
module dram_pim_layernorm_pu #(
    parameter integer VEC_LEN = 4
) (
    // a_flat은 원소 VEC_LEN개를 16 비트씩 포장한 Q8.8 입력입니다. a_flat[i*16 +:16]이 Python a[i]입니다.
    input wire [VEC_LEN*16-1:0] a_flat,
    // y_flat은 조합 결과이며 reg라는문법만으로 저장 레지스터가 되지는 않습니다. always @*이면조합 회로입니다.
    output reg  [VEC_LEN*16-1:0] y_flat
);
    // LayerNorm 분산의 상한을 고려해 25 비트 restoring divider를 사용한다.
    // Q8.8 입력의 평균 제곱 편차를 최대 signed 16-bit 범위에서 계산해도
    // variance_raw는 25 비트에 들어간다. 1/sqrt는 기존 RTL의 floor 정수 결과와 같다.
    // LayerNorm inverse-std에 쓰는 floor(2^24/variance_raw).2^24는 25 비트가 필요합니다.
    // 분자·분모 25비트/나머지 26 비트로 비교·빼기 과정의 carry를 보존합니다.
    function automatic [24:0] udiv25by25(
        input [24:0] numerator,
        input [24:0] denominator
    );
        reg [25:0] remainder_value;
        reg [25:0] denominator_wide;
        reg [24:0] quotient_value;
        integer bit_index;
        begin
            remainder_value = 26'd0;
            denominator_wide = {1'b0, denominator};
            quotient_value = 25'd0;
            if (denominator != 0) begin
                for (bit_index = 24; bit_index >= 0; bit_index = bit_index - 1) begin
                    remainder_value = (remainder_value << 1) | numerator[bit_index];
                    if (remainder_value >= denominator_wide) begin
                        remainder_value = remainder_value - denominator_wide;
                        quotient_value[bit_index] = 1'b1;
                    end
                end
            end
            udiv25by25 = quotient_value;
        end
    endfunction

    // 26 비트 양수의 제곱근을 13회, 항상 같은 횟수로 계산한다. restoring sqrt는
    // 입력 두 비트를 한 번에 소비하고 제곱근 한 비트를 결정해 floor(sqrt(n))을 얻는다.
    // Python math.isqrt(n). 26 비트 입력을 13 개의 2 비트 묶음으로 읽고 결과 13 비트를 계산합니다.
    // 제곱근과 divider을 한 조합 경로에 붙이면 깊이가 커집니다. 기존 Vivado timing 실패의 개선 대상으로
    // 레지스터 삽입 또는 반복형 다중클록 연산이 필요한 이유가 여기에 있습니다.
    function automatic [12:0] isqrt26_fixed13(input [25:0] number);
        reg [26:0] remainder_value;
        reg [12:0] partial_root;
        reg [26:0] trial;
        integer step;
        begin
            remainder_value = 27'd0;
            partial_root = 13'd0;
            trial = 27'd0;
            for (step = 0; step < 13; step = step + 1) begin
                remainder_value = (remainder_value << 2) |
                    ((number >> (24 - 2*step)) & 26'd3);
                trial = (partial_root << 2) | 27'd1;
                if (remainder_value >= trial) begin
                    remainder_value = remainder_value - trial;
                    partial_root = (partial_root << 1) | 13'd1;
                end else begin
                    partial_root = partial_root << 1;
                end
            end
            isqrt26_fixed13 = partial_root;
        end
    endfunction

    // 정규화 편차×역표준편차의 64 비트 중간값을>>>8 후 signed 16 비트로 포화합니다. Python sat16과 같습니다.
    function automatic signed [15:0] sat16(input signed [63:0] value);
        begin
            if (value > 64'sd32767) sat16 = 16'sd32767;
            else if (value < -64'sd32768) sat16 = -16'sd32768;
            else sat16 = value[15:0];
        end
    endfunction

    integer i;
    integer sum_value;
    integer mean_value;
    integer centered_value;
    integer variance_value;
    integer inv_std_value;
    reg signed [15:0] value;
    reg signed [63:0] centered_wide;
    reg signed [63:0] square_sum;
    reg signed [63:0] norm_product;
    reg [24:0] radicand;

    always @* begin
        y_flat = {VEC_LEN*16{1'b0}};
        sum_value = 0;
        mean_value = 0;
        centered_value = 0;
        variance_value = 1;
        inv_std_value = 4096;
        square_sum = 0;
        centered_wide = 0;
        norm_product = 0;
        radicand = 0;
        value = 0;

        for (i = 0; i < VEC_LEN; i = i + 1)
            sum_value = sum_value + $signed(a_flat[i*16 +: 16]);
        // 평균은 signed 32 비트 / 상수 VEC_LEN. 음수 평균은 0 방향 절삭으로 Python trunc_div를 사용합니다.
        mean_value = sum_value / VEC_LEN;

        for (i = 0; i < VEC_LEN; i = i + 1) begin
            value = $signed(a_flat[i*16 +: 16]);
            centered_value = $signed(value) - mean_value;
            centered_wide = centered_value;
            square_sum = square_sum + centered_wide * centered_wide;
        end
        // raw 제곱합(Q16.16)을 평균낸 뒤 Q8.8 분산으로 축소하고 epsilon=1/256을 더합니다.
        // 현재 이 PU는 gamma/beta를 포함하지 않으며 cache top의 S_NORM1/S_NORM2가 뒤에 적용합니다.
        variance_value = (square_sum / VEC_LEN) / 256 + 1;
        if (variance_value > 1) begin
            radicand = udiv25by25(25'd16777216, variance_value[24:0]);
            inv_std_value = isqrt26_fixed13({1'b0, radicand});
        end

        for (i = 0; i < VEC_LEN; i = i + 1) begin
            value = $signed(a_flat[i*16 +: 16]);
            centered_value = $signed(value) - mean_value;
            centered_wide = centered_value;
            norm_product = centered_wide * inv_std_value;
            y_flat[i*16 +: 16] = sat16(norm_product >>> 8);
        end
    end
endmodule
