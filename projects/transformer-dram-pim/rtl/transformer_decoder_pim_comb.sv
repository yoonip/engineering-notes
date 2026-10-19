// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// -----------------------------------------------------------------------------
// 작은 인과적 Transformer decoder block의 기능 RTL
//
// 이 모듈은 입력 hidden-state 행렬에 디코더 블록의 수학적 연산 순서를 적용한다.
// 각 행렬곱은 dram_pim_vmm_bank의 뱅크 근접 MAC/adder tree로 보내고, Softmax,
// residual, LayerNorm, ReLU는 dram_pim_nonvmm_pu로 보낸다. 따라서 제안서의 핵심인
// “메모리 가까운 VMM + 별도 비 VMM PU”의 역할 분리를 실제 모듈 연결로 보여준다.
//
// 각 16비트 값은 signed Q8.8이고 텐서는 행 우선(row-major)으로 납작하게 전달한다.
// 1개의 attention head, 작은 T=4/D=4 예시를 기본으로 한다. 실제 대규모 언어모델,
// 토크나이저, 임베딩 조회, 여러 층의 KV cache 및 vocab 출력층은 포함하지 않는다.
// -----------------------------------------------------------------------------
// [학습용 상세 해설 2026-10-04]
// 위치: attention+FFN 한 블록을 표현하는 단일-head 조합 기능 core.
// Python 대응: model/reference.py:transformer_block의 qmat/softmax_q8/layernorm_q8 순서다.
// Q=찾을 정보 특징, K=비교 대상 특징, V=합칠 내용이다. QK^T는 관련 점수이며 Softmax는
// 관련성 비중, probability*V는 내용 합산, Wo는 출력 특징 혼합이다.
// residual은 입력을 더해 정보를 보존한다. post-norm은 덧셈 후 정규화하는 모델 정의다.
// W1/ReLU/W2 FFN은 attention과 달리 각 token에 독립적인 특징 변환이다. 출력은 hidden이다.
// comb에는 clk가 없다. 조합 for가 여러 회로를 펼치므로 한 반복이 한 클록을 뜻하지 않는다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module transformer_decoder_pim_comb #(
    // context 토큰 수 T. attention 점수는 T*T개이며 문자열 byte 수와 항상 같지는 않다.
    parameter integer TOKENS = 4,
    // 토큰마다 hidden 숫자 수 D. embedding/residual 폭이며 모든 head 채널 수 합이 D다.
    parameter integer D_MODEL = 4,
    // FFN 중간 채널 수 F. W1=D*F, W2=F*D이고 폭을 키우면 연산/저장 비용도 커진다.
    parameter integer D_FF = 8,
    // QK 점수에 곱하는 1/sqrt(D_MODEL)의 Q8.8 근사값이다.
    // 기본값 128은 D_MODEL=4일 때의 0.5를 뜻한다. 다른 차원을 쓸 경우
    // 소프트웨어에서 반올림한 계수를 명시적으로 넣어야 한다.
    // round(256/sqrt(head_dim)) 정수. QK의 차원 효과를 완화하며 head_dim=4일 때 128=0.5다.
    parameter integer SCORE_SCALE_Q8 = 128,
    // non-VMM PU 연산 선택 번호. 음수 특징을 0으로 만드는 ReLU 코드이며 학습 weight가 아니다.
    parameter integer PU_RELU = 0,
    // non-VMM PU 포화 덧셈 선택 번호. Transformer residual connection에 사용한다.
    parameter integer PU_ADD = 1,
    // 마스킹된 attention score를 Q8.8 확률 근사로 바꾸는 non-VMM PU 선택 번호.
    parameter integer PU_SOFTMAX = 2,
    // 토큰 한 개의 채널 평균/분산을 정규화하는 non-VMM PU 선택 번호.
    parameter integer PU_LAYERNORM = 3
) (
    // x_flat은 이미 임베딩/위치 정보가 합쳐진 토큰별 hidden-state다.
    // 가중치 행렬은 한 dot-product 계산 동안 뱅크 가까이에 상주한다고 가정한다.
    // [토큰][hidden 채널] 입력 숫자 표현. embedding이 끝난 행렬이고 원문 문자열이 아니며 Python x/state에 해당한다.
    input  wire [TOKENS*D_MODEL*16-1:0] x_flat,
    // Q/K/V와 어텐션 출력 투영에 쓰는 D_MODEL×D_MODEL 행렬들이다.
    // [입력 채널][출력 채널] Query 가중치. Python qmat(x,wq)가 찾을 정보의 특징 Q를 만든다.
    input  wire [D_MODEL*D_MODEL*16-1:0] wq_flat,
    // [입력 채널][출력 채널] Key 가중치. Python qmat(x,wk)가 비교할 검색 대상 특징 K를 만든다.
    input  wire [D_MODEL*D_MODEL*16-1:0] wk_flat,
    // [입력 채널][출력 채널] Value 가중치. Python qmat(x,wv)가 attention 비중으로 합칠 내용 V를 만든다.
    input  wire [D_MODEL*D_MODEL*16-1:0] wv_flat,
    // [D_MODEL][D_MODEL] attention 출력 투영. Python qmat(context,wo)가 head 내용을 전체 hidden 채널에 섞는다.
    input  wire [D_MODEL*D_MODEL*16-1:0] wo_flat,
    // FFN은 D_MODEL→D_FF→D_MODEL로 채널 폭을 넓혔다가 되돌린다.
    // [D_MODEL][D_FF] FFN 확장 가중치. token마다 특징 폭을 늘린 뒤 비선형 활성화한다.
    input  wire [D_MODEL*D_FF*16-1:0] w1_flat,
    // [D_FF][D_MODEL] FFN 축소 가중치. 활성화 결과를 residual에 더할 원래 hidden 폭으로 되돌린다.
    input  wire [D_FF*D_MODEL*16-1:0] w2_flat,
    // y_flat은 마지막 residual과 LayerNorm을 통과한 최종 토큰 표현 행렬이다.
    // decoder block/stack 최종 hidden [토큰][채널]. 문자가 아니라 LM head로 전달하는 내부 표현이다.
    output reg  [TOKENS*D_MODEL*16-1:0] y_flat,
    // 아래 값은 버스 측정치가 아니라 공개한 traffic/work 가정에서 계산한 카운터다.
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
    // 한 head attention 점수/확률 [query token][key token]의 bit 수 T*T*16.
    localparam integer TT_BITS = TOKENS * TOKENS * 16;
    // FFN 확장 tensor [token][D_FF]의 bit 수 T*F*16.
    localparam integer TF_BITS = TOKENS * D_FF * 16;
    // 전치 K [channel][token] bit 수 D*T*16. TD와 크기는 같지만 주소 축이 다르다.
    localparam integer KT_BITS = D_MODEL * TOKENS * 16;

    // Q=X*Wq 결과. 현재 query가 찾을 특징이며 Python q다.
    wire [TD_BITS-1:0] q_flat;
    // K=X*Wk 결과. 다른 query가 비교할 대상 특징이며 Python k다.
    wire [TD_BITS-1:0] k_flat;
    // V=X*Wv 결과. 관련성 비중으로 합칠 token 내용이며 Python v다.
    wire [TD_BITS-1:0] v_flat;
    // K [T,D]를 [D,T]로 전치한 word 배선. QK 내적 축을 일치시킨다.
    reg  [KT_BITS-1:0] k_transposed_flat;
    // QK^T raw 내적을 Q8.8로 줄인 점수. scale 적용 전이며 확률은 아니다.
    wire [TT_BITS-1:0] score_raw_flat;
    // head dimension scale 적용 attention score. Softmax 입력이고 확률이 아니다.
    reg  [TT_BITS-1:0] scores_flat;
    // [query][key] causal valid bit 행렬. key<=query만 1이어서 미래 문자 유출을 방지한다.
    reg  [TOKENS*TOKENS-1:0] softmax_mask_flat;
    // causal Softmax Q8.8 확률 근사. 이후 V 내용을 가중 합산한다.
    wire [TT_BITS-1:0] probs_flat;
    // probability*V 결과. 각 token/head가 관련된 과거 내용을 모은 vector다.
    wire [TD_BITS-1:0] context_flat;
    // context*Wo 결과. 입력 hidden과 더할 attention 출력 투영.
    wire [TD_BITS-1:0] attn_proj_flat;
    // x+attention 첫 포화 residual. 원래 특징을 함께 보존한다.
    wire [TD_BITS-1:0] residual1_flat;
    // 첫 residual의 LayerNorm 결과. FFN 입력이자 두 번째 residual 경로다.
    wire [TD_BITS-1:0] norm1_flat;
    // W1 선형 확장 출력. 아직 ReLU 이전 값이며 relu_flat에서 비선형을 적용한다.
    wire [TF_BITS-1:0] ff1_flat;
    // FFN 확장값의 max(0,x). 소형 comb 모델의 비선형 출력.
    wire [TF_BITS-1:0] relu_flat;
    // 활성화한 FFN 특징*W2의 축소 출력. norm1과 residual 덧셈한다.
    wire [TD_BITS-1:0] ff2_flat;
    // norm1+ff2의 두 번째 포화 residual.
    wire [TD_BITS-1:0] residual2_flat;
    // 두 번째 residual의 LayerNorm. 다음 층 입력 또는 최종 hidden이다.
    wire [TD_BITS-1:0] norm2_flat;

    // Q8.8 중간 행렬을 16비트 범위로 제한해 다음 블록에 전달한다.
    // Python 대응: model/reference.py 또는 model/gpt_q88.py:sat16 = max(-32768,min(32767,value)).
    // 범위 밖 숫자가 16비트에서 반대 부호로 뒤집히는 wrap-around를 막는 saturation(포화) 함수다.
    // raw -32768..32767은 /256하면 -128..127.99609375이다. 소수 비트 >>8 이동은 호출부가 수행한다.
    // automatic은 임시 지역값이 독립적인 SV 함수 선언이며 CPU가 Python 함수를 실행하는 회로는 아니다.
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

    // K는 [token, channel]로 계산되지만 QK^T를 만들 때에는 [channel, token]이
    // 필요하다. 이 함수는 실제 행렬 전치이며, causal mask와 함께 어텐션 점수
    // Q[t,:] dot K[u,:]의 올바른 축을 연결한다.
    // Python 대응: [list(column) for column in zip(*k)]의 [T,D] -> [D,T] 전치.
    // 숫자 scale을 바꾸지 않고 word 위치를 r*D+c -> c*T+r로 배선하여 Q@K.T의 내적 축을 맞춘다.
    // +:16은 시작 bit에서 증가 방향으로 16개 bit를 선택하는 indexed part-select 문법이다.
    function automatic [KT_BITS-1:0] transpose_k(input [TD_BITS-1:0] k);
        reg [KT_BITS-1:0] result;
        integer r;
        integer c;
        begin
            result = {KT_BITS{1'b0}};
            for (r = 0; r < TOKENS; r = r + 1)
                for (c = 0; c < D_MODEL; c = c + 1)
                    result[(c*TOKENS+r)*16 +: 16] = k[(r*D_MODEL+c)*16 +: 16];
            transpose_k = result;
        end
    endfunction

    // Transformer의 scaled dot-product attention에서 사용하는 1/sqrt(D) 계수를
    // 각 QK^T 점수에 곱한다. 계수를 파라미터화해 D에 따라 사용자가 맞는 값을 넣는다.
    // Python 대응: sat16((raw*SCORE_SCALE_Q8)>>8). raw는 QK 내적을 Q8.8로 줄인 값이다.
    // Q8.8*Q8.8 곱은 소수 bit 16개이므로 >>>8로 8개를 버려 Q8.8로 복귀한다.
    // $signed는 packed bit를 음수 가능한 수로 읽고 >>>는 sign bit를 채우는 산술 우측 이동이다.
    // head_dim을 바꾸면 scale도 round(256/sqrt(head_dim))로 변경해 학습/RTL을 일치시킨다.
    function automatic [TT_BITS-1:0] scale_scores(input [TT_BITS-1:0] raw_scores);
        reg [TT_BITS-1:0] result;
        reg signed [15:0] raw_value;
        integer index;
        begin
            result = {TT_BITS{1'b0}};
            for (index = 0; index < TOKENS*TOKENS; index = index + 1) begin
                raw_value = $signed(raw_scores[index*16 +: 16]);
                // 점수와 계수는 모두 Q8.8이다. 곱 결과 Q16.16에서 소수 비트
                // 8개를 이동해 다시 Q8.8로 맞춘다.
                result[index*16 +: 16] = sat16(($signed(raw_value) * SCORE_SCALE_Q8) >>> 8);
            end
            scale_scores = result;
        end
    endfunction

    // 각 VMM 인스턴스는 하나의 뱅크 근처 연산 자리로 본다. 가중치는 연산 중
    // 이미 그 위치에 상주하므로 입력 활성값만 MAC 트리로 흘러간다.
    // Q/K/V 투영은 세 개의 서로 다른 학습 가중치 행렬을 사용하는 계산이다.
    // Q=X*Wq: 찾을 정보의 Query 특징 투영.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_MODEL), .COLS(D_MODEL)) u_q_vmm (
        .activation_flat(x_flat), .weight_flat(wq_flat), .result_flat(q_flat)
    );
    // K=X*Wk: 검색 대상으로 비교할 Key 특징 투영.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_MODEL), .COLS(D_MODEL)) u_k_vmm (
        .activation_flat(x_flat), .weight_flat(wk_flat), .result_flat(k_flat)
    );
    // V=X*Wv: 관련성 확률로 합칠 Value 내용 투영.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_MODEL), .COLS(D_MODEL)) u_v_vmm (
        .activation_flat(x_flat), .weight_flat(wv_flat), .result_flat(v_flat)
    );
    // Q*K^T: query-key 관계 점수. 뒤에 scale/causal Softmax를 적용한다.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_MODEL), .COLS(TOKENS)) u_score_vmm (
        .activation_flat(q_flat), .weight_flat(k_transposed_flat), .result_flat(score_raw_flat)
    );
    // probability*V: 관련성 비중으로 token 내용 vector를 합친다.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(TOKENS), .COLS(D_MODEL)) u_context_vmm (
        .activation_flat(probs_flat), .weight_flat(v_flat), .result_flat(context_flat)
    );
    // context*Wo: attention 내용의 학습 특징 혼합.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_MODEL), .COLS(D_MODEL)) u_output_vmm (
        .activation_flat(context_flat), .weight_flat(wo_flat), .result_flat(attn_proj_flat)
    );
    // norm1*W1: D -> F FFN 확장 선형층.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_MODEL), .COLS(D_FF)) u_ffn1_vmm (
        .activation_flat(norm1_flat), .weight_flat(w1_flat), .result_flat(ff1_flat)
    );
    // activated*W2: F -> D FFN 축소 선형층.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_FF), .COLS(D_MODEL)) u_ffn2_vmm (
        .activation_flat(relu_flat), .weight_flat(w2_flat), .result_flat(ff2_flat)
    );

    integer r;
    integer c;
    // 조합 계산/배선 블록. for는 합성시 고정 개수의 회로로 펼쳐지며 한 반복=한 clock이 아니다.
    // 모든 output 원소에 값을 정의해 이전 값을 유지하는 latch가 생기지 않게 한다.
    always @* begin
        // K를 전치하고 어텐션 점수를 scaling한 뒤, causal mask를 만든다.
        // c<=r만 허용하므로 token r은 자기 자신과 이전 토큰까지만 볼 수 있다.
        k_transposed_flat = transpose_k(k_flat);
        scores_flat = scale_scores(score_raw_flat);
        softmax_mask_flat = {TOKENS*TOKENS{1'b0}};
        for (r = 0; r < TOKENS; r = r + 1)
            for (c = 0; c < TOKENS; c = c + 1)
                softmax_mask_flat[r*TOKENS+c] = (c <= r);
        y_flat = norm2_flat;
    end

    genvar row;
    // 토큰 행마다 필요한 비 VMM PU를 둔다. Softmax는 각 토큰의 어텐션 점수 벡터에,
    // LayerNorm/Residual/ReLU는 각 토큰의 채널 벡터에 적용한다.
    // generate는 실행 중 반복이 아니라 elaboration 때 고정 개수 회로를 만드는 문법이다.
    // head/token/layer 숫자를 늘리면 물리 복제 회로와 조합 경로 크기가 바뀐다.
    generate
        for (row = 0; row < TOKENS; row = row + 1) begin : gen_token_pus
            // Python softmax_q8(scores,causal_valid). 미래 위치 기여를 0으로 하고 유효 점수를 비중으로 바꾼다.
            dram_pim_nonvmm_pu #(.VEC_LEN(TOKENS)) u_softmax (
                .op(PU_SOFTMAX[1:0]),
                .a_flat(scores_flat[row*TOKENS*16 +: TOKENS*16]),
                .b_flat({TOKENS*16{1'b0}}),
                .valid_mask(softmax_mask_flat[row*TOKENS +: TOKENS]),
                .y_flat(probs_flat[row*TOKENS*16 +: TOKENS*16])
            );

            // Python sat16(x+attention). attention 처리 전 특징을 보존하는 첫 residual.
            dram_pim_nonvmm_pu #(.VEC_LEN(D_MODEL)) u_residual1 (
                .op(PU_ADD[1:0]),
                .a_flat(x_flat[row*D_MODEL*16 +: D_MODEL*16]),
                .b_flat(attn_proj_flat[row*D_MODEL*16 +: D_MODEL*16]),
                .valid_mask({D_MODEL{1'b1}}),
                .y_flat(residual1_flat[row*D_MODEL*16 +: D_MODEL*16])
            );
            // Python layernorm_q8(residual1). token별 channel 평균/분산 정규화.
            dram_pim_nonvmm_pu #(.VEC_LEN(D_MODEL)) u_layernorm1 (
                .op(PU_LAYERNORM[1:0]),
                .a_flat(residual1_flat[row*D_MODEL*16 +: D_MODEL*16]),
                .b_flat({D_MODEL*16{1'b0}}),
                .valid_mask({D_MODEL{1'b1}}),
                .y_flat(norm1_flat[row*D_MODEL*16 +: D_MODEL*16])
            );

            // Python max(0,ff1_value). 음수를 0으로 만드는 FFN 비선형.
            dram_pim_nonvmm_pu #(.VEC_LEN(D_FF)) u_relu (
                .op(PU_RELU[1:0]),
                .a_flat(ff1_flat[row*D_FF*16 +: D_FF*16]),
                .b_flat({D_FF*16{1'b0}}),
                .valid_mask({D_FF{1'b1}}),
                .y_flat(relu_flat[row*D_FF*16 +: D_FF*16])
            );

            // Python sat16(norm1+ff2). FFN 전 특징을 보존하는 두 번째 residual.
            dram_pim_nonvmm_pu #(.VEC_LEN(D_MODEL)) u_residual2 (
                .op(PU_ADD[1:0]),
                .a_flat(norm1_flat[row*D_MODEL*16 +: D_MODEL*16]),
                .b_flat(ff2_flat[row*D_MODEL*16 +: D_MODEL*16]),
                .valid_mask({D_MODEL{1'b1}}),
                .y_flat(residual2_flat[row*D_MODEL*16 +: D_MODEL*16])
            );
            // Python layernorm_q8(residual2). block을 마무리하는 post-norm.
            dram_pim_nonvmm_pu #(.VEC_LEN(D_MODEL)) u_layernorm2 (
                .op(PU_LAYERNORM[1:0]),
                .a_flat(residual2_flat[row*D_MODEL*16 +: D_MODEL*16]),
                .b_flat({D_MODEL*16{1'b0}}),
                .valid_mask({D_MODEL{1'b1}}),
                .y_flat(norm2_flat[row*D_MODEL*16 +: D_MODEL*16])
            );
        end
    endgenerate

    // 데이터 이동량 비교용 간단한 경계 모델이다. CPU 기준은 각 활성화 연산마다
    // 입력 피연산자와 출력 텐서를 경계 밖으로 보내는 unfused 실행을 가정한다.
    // PIM 기준은 입력과 최종 결과만 경계를 넘고 중간값/가중치는 뱅크 가까이에
    // 머문다고 가정한다. 가중치 최초 적재, 명령 바이트, 캐시, 버스 경합은 제외한다.
    // 따라서 이 카운터는 하드웨어 실측이나 GPU 최적화 구현과의 성능 비교가 아니다.
    // 미융합 CPU 비교 가정의 경계 이동 단어 수. word=16bit=2byte이며 실측 DRAM 트래픽은 아니다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign cpu_boundary_words =
        24*TOKENS*D_MODEL + 4*TOKENS*D_FF + 4*TOKENS*TOKENS;
    // 중간값을 메모리 가까이 유지한다는 PIM 비교 가정의 경계 이동 단어 수. 실제 칩 계측값은 아니다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign pim_boundary_words = 2*TOKENS*D_MODEL;
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign mac_count =
        4*TOKENS*D_MODEL*D_MODEL +
        2*TOKENS*TOKENS*D_MODEL +
        2*TOKENS*D_MODEL*D_FF;
    // Softmax/Residual/Norm/활성화의 vector 단계 수. 개별 산술 덧셈 개수와 다르다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign nonvmm_vector_ops = 6*TOKENS;
endmodule
