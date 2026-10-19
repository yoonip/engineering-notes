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
// DRAM bank 가까이에 배치된 VMM(Vector-Matrix Multiply) 연산 모델
//
// Transformer에서 Q/K/V 투영, 어텐션 점수(QK^T), 문맥(V 가중합), FFN 선형층은
// 모두 행렬곱으로 표현된다. 실제 PIM 칩에서는 메모리 뱅크 안팎의 MAC 배열이
// 이 일을 맡지만, 이 모듈은 특정 DRAM 공정이나 배선 구조를 흉내 내지 않고
// “가중치와 곱셈 누산기가 뱅크 가까이에 있다”는 데이터 배치 가정을 표현한다.
//
// 이번 구현에서 제안서의 adder tree는 추가 PU가 아니다. 각 출력 원소를 만드는
// MAC 안에서 K개의 곱을 더하는 균형 트리이다. 비 VMM PU는 별도 모듈에서
// Softmax, residual add, LayerNorm, ReLU를 담당한다.
//
// 수 표현은 signed Q8.8 (16비트, 소수부 8비트)로 고정했다. 각 입력 곱은
// Q16.16이므로, 먼저 넓은 정수로 모두 더한 뒤 마지막에만 8 비트를 오른쪽으로
// 이동해 Q8.8로 되돌린다. 따라서 항마다 먼저 잘라내는 누산 방식보다 중간
// 반올림 오차가 작다. 기존 기준 모델과의 호환성을 위해 최종 이동은 산술
// 오른쪽 이동(절삭)이며, 포화는 마지막에 한 번 적용한다.
//
// K가 2의 거듭제곱이 아니어도 균형 트리를 만들 수 있도록 빈 잎을 0으로 채운다.
// 트리 깊이는 ceil(log2(K))이며 이는 조합 논리의 구조적 깊이에 관한 설명이다.
// 이 모듈 자체에는 레지스터가 없으므로 클록 주기나 실제 칩 지연을 뜻하지 않는다.
// -----------------------------------------------------------------------------
module dram_pim_vmm_bank #(
    // ROWS는 결과를 동시에 계산할 행 수입니다. full context에서 는 token 수, 새 token 계산에서는 1입니다.
    parameter integer ROWS = 4,
    // K는 내적 길이입니다. Q 투영에서는 D_MODEL, 한 head QK에서 는 HEAD_DIM입니다.
    parameter integer K = 4,
    // COLS는 결과 열 수입니다. Q 투영에서는 D_MODEL, LM head에서 는 VOCAB_SIZE입니다.
    parameter integer COLS = 4
) (
    // A 행렬[ROWS,K]의 활성값. Transformer에서는 token hidden, attention 확률, FFN 중간값 등에 해당합니다.
    // Python에서 는 list[list[int]]의 a이며 원소[r,k]는(r*K+k)*16에서 시작합니다.
    input  wire [ROWS*K*16-1:0] activation_flat,
    // B 행렬[K,COLS]. Q/K/V 투영에서는 학습 가중치, QK^T에서 는 전치된 K,
    // attention context에서 는 V입니다. 이름이 weight라도 모든 사용처가 학습 가중치는 아닙니다.
    input  wire [K*COLS*16-1:0] weight_flat,
    // C=A@B의 Q8.8 결과[ROWS,COLS]. Python gpt_q88.qmat(a,b)의 반환 행렬입니다.
    output wire [ROWS*COLS*16-1:0] result_flat
);

    // 두 벡터를 묶어 둘 때 필요한 최소 2의 거듭제곱 크기다.
    // K=1이면 $clog2(1)=0이 고 트리는 잎 하나만 가진다.
    localparam integer TREE_LEVELS = (K <= 1) ? 0 : $clog2(K);
    localparam integer PAD_K = 1 << TREE_LEVELS;

    // signed 16x16 곱은 signed 32 비트에 들어간다. K개를 더할 때 생길 수 있는
    // 추가 carry를 보존하기 위해 log2(K) 비트를 더 확보한다.
    localparam integer ACC_W = 32 + TREE_LEVELS;
    localparam integer NODES_PER_DOT = 2 * PAD_K;
    localparam integer DOTS = ROWS * COLS;

    // 힙 형태의 완전 이진 트리로 저장한다. dot별 시작 주소 다음의 인덱스 1이
    // 뿌리(root), 2*i와 2*i+1이 각각 왼쪽/오른쪽 자식이다. 인덱스 0은 미사용이다.
    wire signed [ACC_W-1:0] tree_node [0:DOTS*NODES_PER_DOT-1];
    wire [DOTS*16-1:0] result_bits;
    assign result_flat = result_bits;

    // 원래 Q8.8 입력 둘을 곱하면 Q16.16 값이 된다. 함수의 반환 폭은 누산 폭에
    // 맞추고, signed 대입을 이용해 곱의 부호 비트를 상위까지 확장한다.
    // Python의 int(a_raw)*int(b_raw)입니다. 16×16→32 비트 곱은 아직/256 하지 않습니다.
    // activation=256, weight=128이면 product=32768(Q16.16)이고 최종 >>8 뒤 128=0.5가 됩니다.
    function automatic signed [ACC_W-1:0] q88_product(
        input [15:0] activation_bits,
        input [15:0] weight_bits
    );
        reg signed [15:0] activation_value;
        reg signed [15:0] weight_value;
        reg signed [31:0] product_value;
        begin
            activation_value = $signed(activation_bits);
            weight_value = $signed(weight_bits);
            product_value = activation_value * weight_value;
            q88_product = product_value;
        end
    endfunction

    // Q8.8로 돌아온 결과를 16 비트 signed 범위에 포화한다. 포화는 큰 양수나
    // 음수가 16 비트로 잘려 부호가 뒤집히는 일을 막는다.
    // Python sat16(value)=max(-32768,min(32767,value))에 대응합니다.
    // 63:0 입력은 비교에서 중간 합의 큰 값/부호를 잃지 않기 위한 충분한 폭입니다.
    function automatic signed [15:0] saturate_q88(
        input signed [63:0] value
    );
        begin
            if (value > 64'sd32767)
                saturate_q88 = 16'sd32767;
            else if (value < -64'sd32768)
                saturate_q88 = -16'sd32768;
            else
                saturate_q88 = value[15:0];
        end
    endfunction

    // genvar는 합성/엘라보레이션 때 정해지는 회로 생성 인덱스입니다. CPU 실행 때 도는 루프가 아닙니다.
    // 각 (row,col)의 dot product 회로가 따로 생겨 병렬도는 높지만 LUT/DSP와 배선 사용량이 커집니다.
    genvar row_index;
    genvar col_index;
    genvar leaf_index;
    genvar node_index;
    generate
        for (row_index = 0; row_index < ROWS; row_index = row_index + 1) begin : gen_rows
            for (col_index = 0; col_index < COLS; col_index = col_index + 1) begin : gen_cols
                // (행,열)마다 하나의 dot-product 트리를 만든다. Transformer에서
                // 예를 들어 Q[t,d]를 만들 때 activation은 입력의 t행, weight는
                // 투영행렬의 d열이며, K개 곱이 바로 이 트리의 잎으로 들어간다.
                localparam integer DOT_INDEX = row_index * COLS + col_index;
                localparam integer BASE = DOT_INDEX * NODES_PER_DOT;

                for (leaf_index = 0; leaf_index < PAD_K; leaf_index = leaf_index + 1) begin : gen_leaves
                    if (leaf_index < K) begin : gen_real_product
                        // 행 우선(row-major) 주소 계산: A[row,k], W[k,col].
                        // weight_flat은 현재 계산 동안 해당 뱅크에 상주한다고 가정한다.
                        assign tree_node[BASE + PAD_K + leaf_index] = q88_product(
                            activation_flat[(row_index*K + leaf_index)*16 +: 16],
                            weight_flat[(leaf_index*COLS + col_index)*16 +: 16]
                        );
                    end else begin : gen_zero_padding
                        // K가 2의 거듭제곱이 아니면 남는 잎을 0으로 만들어
                        // 임의의 가짜 연산 없이도 균형 트리 구조를 유지한다.
                        assign tree_node[BASE + PAD_K + leaf_index] = {ACC_W{1'b0}};
                    end
                end

                for (node_index = 1; node_index < PAD_K; node_index = node_index + 1) begin : gen_tree_levels
                    // 한 단계의 두 부분합을 더한다. 동일 층의 노드들이 병렬로
                    // 계산되므로, K항을 순차적으로 누산하는 구조보다 논리 깊이가
                    // 선형 K가 아니라 log2(K)에 비례한다.
                    assign tree_node[BASE + node_index] =
                        tree_node[BASE + 2*node_index] +
                        tree_node[BASE + 2*node_index + 1];
                end

                // 트리 뿌리는 정확한 Q16.16 누산 결과다. 마지막에만 소수부 8 비트를
                // 버려 Q8.8로 맞춘 뒤 포화한다. 이 결과가 다음 Transformer 단계의
                // 활성값으로 쓰인다.
                // Python 한 원소: sat16(sum(a[r][k]*b[k][c] for k in range(K)) >> 8).
                // 부호 있는 >>>8은 음수에서도 부호를 보존하며 -257>>>8=-2입니다. 이는 0을 향한 /256 절삭(-1)과 다릅니다.
                // 곱마다 절삭하지 않고 넓은 합을 완성한 후 한 번만 이동합니다. 예:큰 양수·음수가 상쇄될 때 정밀도를 지킵니다.
                assign result_bits[DOT_INDEX*16 +: 16] = saturate_q88(
                    $signed(tree_node[BASE + 1]) >>> 8
                );
            end
        end
    endgenerate
endmodule
