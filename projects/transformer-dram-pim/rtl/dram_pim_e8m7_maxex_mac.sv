`timescale 1ns/1ps
// =============================================================================
// 원 연구계획서 그림 5의 MAX-EX(최대 지수 선행 정렬) 내적을 실행하는 독립 회로.
//
// 이 모듈은 이미 배선한 Q8.8 GPT top에 연결하지 않는다. 별도 PIM VMM 연구용
// E8M7 내적이다. Python model/e8m7_maxex.py의 maxex_dot와 비트 단위로 대조한다.
// 계산: a[0]*b[0] + ... + a[LANES-1]*b[LANES-1]. Transformer에서 Q/K/V나 FFN
// 행렬곱의 한 출력 원소에 해당한다. DRAM PHY나 실제 메모리 bank는 포함하지 않는다.
//
// E8M7 word = [sign 1][exponent 8, bias 127][fraction 7]. 정상수의 magnitude는
// (128+fraction)*2^(exponent-127-7), subnormal은 fraction*2^(-126-7)이다.
// 두 8-bit significand를 정확히 곱해 16-bit P를 얻고 E=e_a+e_b라 하면,
// product의 실제 값은 (-1)^sign * P * 2^(E-14)이다. 곱을 E8M7로 먼저 반올림하지
// 않으므로 곱의 16-bit significand가 살아 있다.
//
// 1) 모든 유한 nonzero 곱의 E 중 MAXEX를 균형 비교 트리로 한 번 구한다.
// 2) 각 P를 GUARD_BITS만큼 확장한 뒤 MAXEX-E만큼 논리 right shift한다.
//    작은 항의 magnitude를 먼저 절삭하고 그 뒤 부호를 적용한다. 음수에 산술
//    right shift를 직접 적용하면 -1이 생길 수 있어 이 정의와 달라진다.
// 3) 넓은 signed 균형 adder tree로 합산한다. 마지막에만 normalize하고 E8M7
//    round-to-nearest ties-to-even(RNE)으로 반올림한다.
//
// 이 방식은 좁은 alignment에서 작은 항을 잃을 수 있다. 특히 큰 항끼리 상쇄한
// 뒤 작은 항이 남는 경우 GUARD16과 GUARD32의 결과가 다를 수 있다. 정확한 실수
// dot product나 모든 IEEE floating 누산과 같다고 주장하지 않는다. 실제로 같아야
// 하는 것은 위 규칙과 Python MAX-EX reference의 16-bit 결과다.
//
// 특수값: NaN 또는 Inf*0 → canonical qNaN 7fc0. +Inf와 -Inf가 모두 있으면
// 7fc0, 한 부호의 Inf만 있으면 그 Inf. 유한 합의 완전 상쇄/모든 zero는 +0.
// 유한 음수의 최종 underflow는 -0, overflow는 부호 있는 Inf로 반올림한다.
//
// 전체 모듈은 조합 회로다. 클록/ready/valid가 없다. 테스트벤치의 #1은 신호
// 안정화를 기다리는 simulation delay이고 물리적으로 1ns에 계산된다는 뜻이 아니다.
// 실제 pipeline/clock·setup/hold는 외부 등록 wrapper의 Vivado 결과로 판단한다.
// =============================================================================
module dram_pim_e8m7_maxex_mac #(
    parameter integer LANES = 16,
    // 공통 지수로 옮길 때 아래쪽에 보존하는 추가 bit 수. 소수 정밀도 여유이며
    // E8M7 저장 형식의 fraction 7비트 자체를 바꾸는 parameter는 아니다.
    parameter integer GUARD_BITS = 16
) (
    // 배열 lane i는 Python a_words[i], b_words[i]에 대응한다. 서로 다른 lane의
    // E8M7 곱을 하나의 dot product로 합친다. packed bus wrapper는 i*16+:16을
    // 이 배열 원소에 연결하면 된다.
    input wire [15:0] a [0:LANES-1],
    input wire [15:0] b [0:LANES-1],
    output wire [15:0] result
);
    localparam integer TREE_LEVELS = (LANES <= 1) ? 0 : $clog2(LANES);
    localparam integer PAD_LANES = 1 << TREE_LEVELS;
    // 각 magnitude는 최대 (65535<<G), LANES개 합에는 ceil(log2(LANES)) 추가
    // bit와 signed 부호 bit가 필요하다. 중간 덧셈도 모두 이 폭을 유지한다.
    localparam integer ACC_WIDTH = 16 + GUARD_BITS + TREE_LEVELS + 1;
    // 유한 product exponent는 -252..254. -512는 모든 실제 exponent보다 작고
    // signed10bit에 들어가는 안전한 zero/padding sentinel이다.
    localparam signed [9:0] ZERO_EXPONENT = -10'sd512;

    wire signed [9:0] max_nodes [0:2*PAD_LANES-1];
    wire signed [ACC_WIDTH-1:0] sum_nodes [0:2*PAD_LANES-1];
    wire invalid_nodes [0:2*PAD_LANES-1];
    wire positive_inf_nodes [0:2*PAD_LANES-1];
    wire negative_inf_nodes [0:2*PAD_LANES-1];

    // e는 significand를 정수8bit로 해석할 때 쓰는 unbiased exponent다.
    // exponent field0은 hidden1이 없지만 e=-126으로 정상 최소 지수와 동일하다.
    function automatic signed [9:0] unbiased_exponent(input [15:0] word);
        integer exponent_field;
        begin
            exponent_field = word[14:7];
            unbiased_exponent = (exponent_field == 0) ? -126 : exponent_field - 127;
        end
    endfunction

    // unsigned magnitude를 정렬한 후 마지막에 signed 부호를 붙인다.
    // Python: magnitude=(product<<G)>>max(0,max_exponent-exponent).
    // 논리 shift에서 버린 bit는 이 단계에서 보정하지 않는다. 이후 RNE는 남아
    // 있는 accumulator를 E8M7로 저장할 때만 적용한다.
    function automatic signed [ACC_WIDTH-1:0] align_product(
        input [15:0] product,
        input signed [9:0] exponent,
        input signed [9:0] maximum_exponent,
        input sign_bit
    );
        reg [ACC_WIDTH-1:0] magnitude;
        integer gap;
        begin
            magnitude = {{(ACC_WIDTH-16){1'b0}}, product};
            magnitude = magnitude << GUARD_BITS;
            gap = $signed(maximum_exponent) - $signed(exponent);
            if (product == 0 || exponent == ZERO_EXPONENT || gap >= ACC_WIDTH)
                magnitude = 0;
            else if (gap > 0)
                magnitude = magnitude >> gap;
            align_product = sign_bit ? -$signed(magnitude) : $signed(magnitude);
        end
    endfunction

    // magnitude/2^shift를 ties-to-even으로 반올림한다. shift<=0은 exact left shift.
    // half_bit는 정확한 반 bit, sticky는 그 아래의 하나라도1인지 나타낸다.
    // half_bit=1이고 sticky=1이면 반보다 큼, sticky=0이면 retained LSB가 홀수일
    // 때만 올려 최종 결과를 짝수로 만든다. shift가 폭보다 커도 bit index를
    // 범위 밖에서 읽지 않고 zero/underflow를 정확히 처리한다.
    function automatic [ACC_WIDTH:0] rounded_shift(
        input [ACC_WIDTH-1:0] magnitude,
        input integer shift
    );
        reg [ACC_WIDTH:0] retained;
        reg half_bit;
        reg sticky;
        integer bit_index;
        begin
            retained = {1'b0, magnitude};
            half_bit = 1'b0;
            sticky = 1'b0;
            if (shift <= 0) begin
                retained = retained << (-shift);
            end else begin
                retained = retained >> shift;
                if (shift <= ACC_WIDTH)
                    half_bit = magnitude[shift-1];
                for (bit_index = 0; bit_index < ACC_WIDTH; bit_index = bit_index + 1)
                    if (bit_index < shift-1 && magnitude[bit_index]) sticky = 1'b1;
                if (half_bit && (sticky || retained[0])) retained = retained + 1'b1;
            end
            rounded_shift = retained;
        end
    endfunction

    // accumulator의 실제 값 = acc * 2^(MAXEX-14-G). 최상위1 위치를 찾아 정상수
    // 8-bit significand로 맞춘다. 정상수보다 작은 값은 subnormal unit2^-133에
    // 맞춰 반올림한다. Python fraction_to_e8m7(reconstructed)에 대응한다.
    function automatic [15:0] normalize_accumulator(
        input signed [ACC_WIDTH-1:0] accumulator,
        input signed [9:0] maximum_exponent
    );
        reg sign_bit;
        reg [ACC_WIDTH-1:0] magnitude;
        reg [ACC_WIDTH:0] rounded;
        reg [7:0] exponent_field;
        integer highest_bit;
        integer bit_index;
        integer output_exponent;
        integer shift;
        begin
            normalize_accumulator = 16'h0000;
            sign_bit = accumulator[ACC_WIDTH-1];
            magnitude = sign_bit ? -accumulator : accumulator;
            highest_bit = -1;
            rounded = 0;
            exponent_field = 0;
            shift = 0;
            output_exponent = 0;
            if (accumulator != 0) begin
                for (bit_index = 0; bit_index < ACC_WIDTH; bit_index = bit_index + 1)
                    if (magnitude[bit_index]) highest_bit = bit_index;
                output_exponent = $signed(maximum_exponent) - 14 - GUARD_BITS + highest_bit;
                if (output_exponent >= -126) begin
                    rounded = rounded_shift(magnitude, highest_bit - 7);
                    // 반올림으로1.1111111→10.0000000이 되면 지수를1 올린다.
                    if (rounded >= 256) begin
                        rounded = 128;
                        output_exponent = output_exponent + 1;
                    end
                    if (output_exponent > 127)
                        normalize_accumulator = {sign_bit, 8'hff, 7'h00};
                    else begin
                        exponent_field = output_exponent + 127;
                        normalize_accumulator = {sign_bit, exponent_field, rounded[6:0]};
                    end
                end else begin
                    // subnormal raw fraction n은 실제 n*2^-133이다.
                    shift = GUARD_BITS - 119 - $signed(maximum_exponent);
                    rounded = rounded_shift(magnitude, shift);
                    if (rounded >= 128)
                        normalize_accumulator = {sign_bit, 8'h01, 7'h00};
                    else
                        normalize_accumulator = {sign_bit, 8'h00, rounded[6:0]};
                end
            end
        end
    endfunction

    // Heap 모양의 균형 트리: root1, 왼쪽2*i, 오른쪽2*i+1, leaf PAD_LANES+i.
    // LANES3이면4개의 leaf를 만들고 마지막을zero로 채운다. max tree와 sum tree가
    // 동일한 padding 규칙을 써 odd lane에서도 실제 항을 빠뜨리지 않는다.
    genvar lane;
    genvar node;
    generate
        for (lane = 0; lane < PAD_LANES; lane = lane + 1) begin : gen_lanes
            if (lane < LANES) begin : gen_real_lane
                wire a_nan = (a[lane][14:7] == 8'hff) && (a[lane][6:0] != 0);
                wire b_nan = (b[lane][14:7] == 8'hff) && (b[lane][6:0] != 0);
                wire a_inf = (a[lane][14:7] == 8'hff) && (a[lane][6:0] == 0);
                wire b_inf = (b[lane][14:7] == 8'hff) && (b[lane][6:0] == 0);
                wire a_zero = (a[lane][14:0] == 0);
                wire b_zero = (b[lane][14:0] == 0);
                wire product_sign = a[lane][15] ^ b[lane][15];
                wire invalid = a_nan || b_nan || (a_inf && b_zero) || (b_inf && a_zero);
                wire product_inf = (a_inf || b_inf) && !invalid;
                wire finite_nonzero = !invalid && !product_inf && !a_zero && !b_zero;
                wire [7:0] a_mantissa = {(a[lane][14:7] != 0), a[lane][6:0]};
                wire [7:0] b_mantissa = {(b[lane][14:7] != 0), b[lane][6:0]};
                wire [15:0] product_magnitude = a_mantissa * b_mantissa;
                wire signed [9:0] product_exponent = unbiased_exponent(a[lane]) + unbiased_exponent(b[lane]);

                assign max_nodes[PAD_LANES+lane] = finite_nonzero ? product_exponent : ZERO_EXPONENT;
                assign sum_nodes[PAD_LANES+lane] = finite_nonzero
                    ? align_product(product_magnitude, product_exponent, max_nodes[1], product_sign)
                    : {ACC_WIDTH{1'b0}};
                assign invalid_nodes[PAD_LANES+lane] = invalid;
                assign positive_inf_nodes[PAD_LANES+lane] = product_inf && !product_sign;
                assign negative_inf_nodes[PAD_LANES+lane] = product_inf && product_sign;
            end else begin : gen_padding
                assign max_nodes[PAD_LANES+lane] = ZERO_EXPONENT;
                assign sum_nodes[PAD_LANES+lane] = {ACC_WIDTH{1'b0}};
                assign invalid_nodes[PAD_LANES+lane] = 1'b0;
                assign positive_inf_nodes[PAD_LANES+lane] = 1'b0;
                assign negative_inf_nodes[PAD_LANES+lane] = 1'b0;
            end
        end
        for (node = 1; node < PAD_LANES; node = node + 1) begin : gen_tree
            assign max_nodes[node] = ($signed(max_nodes[2*node]) >= $signed(max_nodes[2*node+1]))
                ? max_nodes[2*node] : max_nodes[2*node+1];
            assign sum_nodes[node] = sum_nodes[2*node] + sum_nodes[2*node+1];
            assign invalid_nodes[node] = invalid_nodes[2*node] || invalid_nodes[2*node+1];
            assign positive_inf_nodes[node] = positive_inf_nodes[2*node] || positive_inf_nodes[2*node+1];
            assign negative_inf_nodes[node] = negative_inf_nodes[2*node] || negative_inf_nodes[2*node+1];
        end
    endgenerate

    // 특수값의 우선순위는 IEEE 계열의 불능 연산/상반된 infinity 규칙을 명시적으로
    // 정했다. NaN payload는 보존하지 않고 항상 qNaN7fc0으로 정규화한다.
    assign result = (invalid_nodes[1] || (positive_inf_nodes[1] && negative_inf_nodes[1]))
        ? 16'h7fc0 : positive_inf_nodes[1] ? 16'h7f80 : negative_inf_nodes[1] ? 16'hff80
        : normalize_accumulator(sum_nodes[1], max_nodes[1]);

    // synthesis translate_off
    initial begin
        // GUARD512는 유한 product의 최대 지수 차506보다 넓어 alignment bit를
        // 모두 보존하는 별도 software/RTL 기준시험에 사용한다. 실제 FPGA OOC
        // 실험은 GUARD16/32이며512의 FPGA 자원·timing을 측정한 것은 아니다.
        // 이 상한 변경은 simulation parameter 검사뿐이고16/32 datapath는 같다.
        if (LANES < 1 || GUARD_BITS < 0 || GUARD_BITS > 512)
            $fatal(1, "LANES>=1 and 0<=GUARD_BITS<=512 required");
    end
    // synthesis translate_on
endmodule
