// 일반 floating tree 비교 기준: 각 곱과 각 pairwise 덧셈에서 E8M7 RNE.
// 이 독립 모듈은 MAX-EX의 '곱을 넓게 보관하고 마지막에 한 번 반올림'과
// 비교할 연구용 baseline이다. 기존 Q8.8 Transformer나 Nexys bitstream에
// 연결하지 않는다. Python model/e8m7_maxex.py의 rounded_product_tree_dot와
// 비트 단위로 같도록 정의하며 특정 제품의 BF16 명령을 복제했다고 주장하지 않는다.
//
// E8M7 word = sign[15], exponent[14:7], fraction[6:0], bias=127.
// 정상수는 (128+fraction)*2^(exp-127-7), subnormal은 fraction*2^(-126-7).
// NaN은 7fc0으로 통일하고 Inf*0, 서로 반대인 Inf 합은 NaN이다.
// 입력 zero의 곱과 정확한 합의 zero는 +0; 음수 nonzero의 underflow만 -0.
// 이는 현재 Python Fraction 기준의 zero 정책이며 IEEE -0 보존과 구분한다.
//
// G512 같은 전체 exponent 범위의 거대 정렬기는 사용하지 않는다. 덧셈은
// 8bit significand + guard/round/sticky 3bit만 정렬한다. sticky는 버린 모든
// bit의 OR이며, RNE가 '정확한 midpoint인가, 조금 더 큰가'를 판단하게 한다.
// 32bit 지역 임시 변수는 정수 bit 연산·공통 pack 함수의 편의 폭이며 lane 합을
// 넓은 common-exponent accumulator에 모으는 MAX-EX 구조가 아니다.
module e8m7_pairwise_tree_mac #(
    parameter integer LANES = 16
) (
    input wire [15:0] a [0:LANES-1],
    input wire [15:0] b [0:LANES-1],
    output wire [15:0] result
);
    localparam integer LEVELS = (LANES <= 1) ? 0 : $clog2(LANES);
    localparam integer LEAVES = 1 << LEVELS;
    // heap 순서: root=1, 자식=2*i/2*i+1, product 잎=LEAVES+i.
    // 3/5/17처럼 홀수 lane은 남는 잎을 +0으로 채워 Python balanced_tree와
    // 같은 인접쌍·같은 단계 순서로 합한다. 반올림 때문에 합 순서도 명세이다.
    wire [15:0] tree [0:2*LEAVES-1];
    assign tree[0] = 16'h0000;

    // 양의 정수를 2^shift로 나누어 nearest, ties-to-even으로 반올림한다.
    // quotient의 마지막 bit가 1인 정확한 midpoint만 올린다. shift가 폭보다
    // 크면 guard가 없으므로 0; 매우 작은 subnormal product도 안전하게 처리한다.
    function automatic [31:0] rne_right32;
        input [31:0] magnitude;
        input integer shift;
        reg [31:0] quotient;
        reg guard_bit, sticky_bit;
        integer bit_index;
        begin
            quotient = 0;
            guard_bit = 0;
            sticky_bit = 0;
            if (shift <= 0) begin
                quotient = magnitude << (-shift);
            end else begin
                if (shift < 32) quotient = magnitude >> shift;
                for (bit_index=0; bit_index<32; bit_index=bit_index+1) begin
                    if (bit_index == shift-1) guard_bit = magnitude[bit_index];
                    if (bit_index < shift-1) sticky_bit = sticky_bit | magnitude[bit_index];
                end
                if (guard_bit && (sticky_bit || quotient[0])) quotient = quotient + 1;
            end
            rne_right32 = quotient;
        end
    endfunction

    // 작은 피연산자의 significand를 공통 exponent로 오른쪽 정렬한다.
    // 나간 bit를 단순히 버리면 midpoint와 midpoint+epsilon을 구분하지 못한다.
    // OR된 sticky를 마지막 bit에 jam하여 그 정보만 보존한다. 11bit이면
    // 8bit significand와 guard/round/sticky에 충분하며 최대 shift는 exponent 차다.
    function automatic [10:0] shift_right_jam11;
        input [10:0] value;
        input integer shift;
        reg [10:0] shifted;
        reg sticky;
        integer bit_index;
        begin
            sticky = 0;
            shifted = value;
            if (shift > 0) begin
                shifted = (shift < 11) ? (value >> shift) : 11'b0;
                for (bit_index=0; bit_index<11; bit_index=bit_index+1)
                    if (bit_index < shift) sticky = sticky | value[bit_index];
                shifted[0] = shifted[0] | sticky;
            end
            shift_right_jam11 = shifted;
        end
    endfunction

    // 실제 유한 값 sign * magnitude * 2^binary_scale를 E8M7로 RNE한다.
    // product는 정확한 16bit 곱을, adder는 이미 sticky-jam된 12bit 합을 준다.
    // highest bit로 정상수 exponent를 찾고, subnormal은 고정 quantum 2^-133에
    // 맞춘다. RNE carry로 255->256이 되면 exponent를 한 단계 올린다.
    function automatic [15:0] pack_finite;
        input sign_bit;
        input [31:0] magnitude;
        input integer binary_scale;
        integer top_bit, bit_index, exponent_value, packed_exponent;
        reg [31:0] rounded;
        begin
            top_bit = -1;
            rounded = 0;
            packed_exponent = 0;
            for (bit_index=0; bit_index<32; bit_index=bit_index+1)
                if (magnitude[bit_index]) top_bit = bit_index;
            if (top_bit < 0) begin
                // 정확한 입력 zero 또는 정확한 상쇄는 Fraction(0)과 같은 +0.
                pack_finite = 16'h0000;
            end else begin
                exponent_value = top_bit + binary_scale;
                if (exponent_value > 127) begin
                    pack_finite = {sign_bit,8'hff,7'b0};
                end else if (exponent_value >= -126) begin
                    rounded = rne_right32(magnitude, top_bit-7);
                    if (rounded >= 256) begin
                        rounded = rounded >> 1;
                        exponent_value = exponent_value + 1;
                    end
                    if (exponent_value > 127) pack_finite = {sign_bit,8'hff,7'b0};
                    else begin
                        packed_exponent = exponent_value + 127;
                        pack_finite = {sign_bit,packed_exponent[7:0],rounded[6:0]};
                    end
                end else begin
                    rounded = rne_right32(magnitude, -133-binary_scale);
                    if (rounded >= 128) pack_finite = {sign_bit,8'h01,7'b0};
                    else pack_finite = {sign_bit,8'h00,rounded[6:0]};
                end
            end
        end
    endfunction

    // Transformer VMM의 한 lane에 해당하는 scalar 곱이다. MAX-EX와 달리
    // 이 곱 자체를 바로 E8M7로 저장하여 fraction 7bit로 돌아간다.
    function automatic [15:0] multiply_rne;
        input [15:0] left_word, right_word;
        reg sign_bit, left_nan, right_nan, left_inf, right_inf;
        reg [7:0] left_mantissa, right_mantissa;
        reg [15:0] product;
        integer left_exponent, right_exponent;
        begin
            sign_bit = left_word[15] ^ right_word[15];
            left_nan = (left_word[14:7]==8'hff) && (left_word[6:0]!=0);
            right_nan = (right_word[14:7]==8'hff) && (right_word[6:0]!=0);
            left_inf = (left_word[14:7]==8'hff) && (left_word[6:0]==0);
            right_inf = (right_word[14:7]==8'hff) && (right_word[6:0]==0);
            left_mantissa = {left_word[14:7]!=0,left_word[6:0]};
            right_mantissa = {right_word[14:7]!=0,right_word[6:0]};
            left_exponent = (left_word[14:7]==0) ? -126 : int'(left_word[14:7])-127;
            right_exponent = (right_word[14:7]==0) ? -126 : int'(right_word[14:7])-127;
            product = left_mantissa * right_mantissa;
            if (left_nan || right_nan || (left_inf && right_word[14:0]==0)
                    || (right_inf && left_word[14:0]==0)) multiply_rne = 16'h7fc0;
            else if (left_inf || right_inf) multiply_rne = {sign_bit,8'hff,7'b0};
            else multiply_rne = pack_finite(sign_bit,{16'b0,product},left_exponent+right_exponent-14);
        end
    endfunction

    // 일반 floating adder: exponent 비교 -> 작은 significand sticky 정렬 ->
    // 부호에 따라 합/차 -> normalize/RNE. 합은 carry 1bit를 포함한 12bit이다.
    // subtract에서 깊은 상쇄는 exponent가 같거나 1차이인 경우이며, 이때
    // 3개의 추가 bit 안에 원래 유효 bit가 모두 남아 정규화 전에 정보가 사라지지 않는다.
    function automatic [15:0] add_rne;
        input [15:0] left_word, right_word;
        reg left_nan, right_nan, left_inf, right_inf, result_sign;
        reg [7:0] left_mantissa, right_mantissa;
        reg [10:0] left_aligned, right_aligned;
        reg [11:0] sum_magnitude;
        integer left_exponent, right_exponent, common_exponent;
        begin
            left_nan = (left_word[14:7]==8'hff) && (left_word[6:0]!=0);
            right_nan = (right_word[14:7]==8'hff) && (right_word[6:0]!=0);
            left_inf = (left_word[14:7]==8'hff) && (left_word[6:0]==0);
            right_inf = (right_word[14:7]==8'hff) && (right_word[6:0]==0);
            left_mantissa = {left_word[14:7]!=0,left_word[6:0]};
            right_mantissa = {right_word[14:7]!=0,right_word[6:0]};
            left_exponent = (left_word[14:7]==0) ? -126 : int'(left_word[14:7])-127;
            right_exponent = (right_word[14:7]==0) ? -126 : int'(right_word[14:7])-127;
            common_exponent = (left_exponent >= right_exponent) ? left_exponent : right_exponent;
            left_aligned = shift_right_jam11({left_mantissa,3'b0},common_exponent-left_exponent);
            right_aligned = shift_right_jam11({right_mantissa,3'b0},common_exponent-right_exponent);
            result_sign = left_word[15];
            sum_magnitude = 0;
            if (left_word[15]==right_word[15])
                sum_magnitude = {1'b0,left_aligned} + {1'b0,right_aligned};
            else if (left_aligned >= right_aligned)
                sum_magnitude = {1'b0,left_aligned} - {1'b0,right_aligned};
            else begin
                sum_magnitude = {1'b0,right_aligned} - {1'b0,left_aligned};
                result_sign = right_word[15];
            end
            if (left_nan || right_nan || (left_inf && right_inf && left_word[15]!=right_word[15]))
                add_rne = 16'h7fc0;
            else if (left_inf) add_rne = {left_word[15],8'hff,7'b0};
            else if (right_inf) add_rne = {right_word[15],8'hff,7'b0};
            else if (left_mantissa==0 && right_mantissa==0) add_rne = 16'h0000;
            else if (left_mantissa==0) add_rne = right_word;
            else if (right_mantissa==0) add_rne = left_word;
            else add_rne = pack_finite(result_sign,{20'b0,sum_magnitude},common_exponent-10);
        end
    endfunction

    genvar lane, node;
    generate
        for (lane=0; lane<LEAVES; lane=lane+1) begin: product_leaves
            if (lane<LANES) assign tree[LEAVES+lane] = multiply_rne(a[lane],b[lane]);
            else assign tree[LEAVES+lane] = 16'h0000;
        end
        for (node=1; node<LEAVES; node=node+1) begin: rounded_adders
            assign tree[node] = add_rne(tree[2*node],tree[2*node+1]);
        end
    endgenerate
    assign result = tree[1];

    // 잘못된 parameter만 simulation에서 즉시 알린다. 합성 datapath는 바꾸지 않는다.
    // synthesis translate_off
    initial if (LANES<1) $fatal(1,"LANES는 1 이상이어야 합니다.");
    // synthesis translate_on
endmodule
