// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// -----------------------------------------------------------------------------
// 여러 attention head를 갖는 causal Transformer decoder block
//
// 이 모듈은 현재 연구 패키지의 1-head 블록을 GPT 계열 decoder block의
// multi-head 형태로 확장한다. 텐서는 [token][channel] 순서로 평탄화하고,
// 한 원소는 signed Q8.8(16비트)로 표현한다.
//
// 데이터 흐름:
//   X -> Q/K/V 전체 채널 투영 -> head별 QK^T -> 1/sqrt(head_dim) -> causal
//   Softmax -> head별 확률*V -> head 결과 채널 결합 -> Wo -> residual/LN
//   -> FFN(ReLU) -> residual/LN
//
// 각 head는 전체 hidden vector의 서로 다른 head_dim 채널을 사용한다. 점수 행렬은
// head마다 독립적으로 계산되므로 head마다 다른 토큰 관계를 학습할 수 있다.
// HEADS=1이면 기존 한-head 구조의 일반화이며, D_MODEL은 HEADS로 나누어져야 한다.
//
// 입력 임베딩, 위치 임베딩, 토큰 어휘층, 체크포인트 로더, bias와 학습형 LayerNorm
// gamma/beta는 이 행렬 연산 코어 바깥의 별도 시스템 계층이다. 이 제한은 의도적으로
// 숨기지 않는다. 이 코어는 decoder block의 attention/FFN 경로를 검증한다.
// 내부 PU의 나눗셈 및 역제곱근은 기능 모델이므로, 합성 report를 실리콘 면적/속도로
// 해석할 수 없다. 실제 ASIC/FPGA 성능 주장은 별도 timing/board 검증이 필요하다.
// -----------------------------------------------------------------------------
// [학습용 상세 해설 2026-10-04]
// 위치: 한 decoder block을 H개 attention head로 확장한 조합 기능 core.
// Python 대응: model/gpt_core_reference.py:decoder_block의 qh/kh/vh, probabilities,
// all_context_rows, residual1/norm1/ff1/relu/ff2/residual2를 module 연결로 표현한다.
// head마다 hidden 전체를 복제하지 않고 Q/K/V의 서로 다른 HEAD_DIM 채널을 골라 쓴다.
// 각 head의 T*T 점수/Softmax는 독립이다. context를 channel 축으로 합쳐 Wo에 보낸다.
// 이 core는 bias 없는 post-norm/ReLU 검증 정의다. 학습 full-ops의 bias/gamma/beta/GELU
// 지원 경로는 transformer_gpt_kvcache_seq에 구현되어 있다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module transformer_decoder_mha_pim_comb #(
    // context 토큰 수 T. attention 점수는 T*T개이며 문자열 byte 수와 항상 같지는 않다.
    parameter integer TOKENS = 4,
    // 토큰마다 hidden 숫자 수 D. embedding/residual 폭이며 모든 head 채널 수 합이 D다.
    parameter integer D_MODEL = 8,
    // attention 관점 수 H. head_dim=D_MODEL/HEADS이며 서로 다른 채널로 독립 점수/확률을 만든다.
    parameter integer HEADS = 2,
    // FFN 중간 채널 수 F. W1=D*F, W2=F*D이고 폭을 키우면 연산/저장 비용도 커진다.
    parameter integer D_FF = 16,
    // Q8.8 표현의 round(256/sqrt(D_MODEL/HEADS)). head_dim=4이면 128이다.
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
    // decoder block/stack 최종 hidden [토큰][채널]. 문자가 아니라 LM head로 전달하는 내부 표현이다.
    output reg  [TOKENS*D_MODEL*16-1:0] y_flat,
    // 미융합 CPU 비교 가정의 경계 이동 단어 수. word=16bit=2byte이며 실측 DRAM 트래픽은 아니다.
    output wire [31:0] cpu_boundary_words,
    // 중간값을 메모리 가까이 유지한다는 PIM 비교 가정의 경계 이동 단어 수. 실제 칩 계측값은 아니다.
    output wire [31:0] pim_boundary_words,
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    output wire [31:0] mac_count,
    // Softmax/Residual/Norm/활성화의 vector 단계 수. 개별 산술 덧셈 개수와 다르다.
    output wire [31:0] nonvmm_vector_ops
);
    // 한 head의 채널 수 D/H. QK 내적 길이이자 연결 전 context 폭이다.
    localparam integer HEAD_DIM = D_MODEL / HEADS;
    // [token][D_MODEL] tensor의 총 bit 수 T*D*16. vector 원소 수와 bit 수를 구분한다.
    localparam integer TD_BITS = TOKENS * D_MODEL * 16;
    // [token][head channel] tensor의 bit 수 T*HEAD_DIM*16.
    localparam integer TH_BITS = TOKENS * HEAD_DIM * 16;
    // 한 head attention 점수/확률 [query token][key token]의 bit 수 T*T*16.
    localparam integer TT_BITS = TOKENS * TOKENS * 16;
    // FFN 확장 tensor [token][D_FF]의 bit 수 T*F*16.
    localparam integer TF_BITS = TOKENS * D_FF * 16;
    // 모든 head 점수/확률을 연결한 bit 수 H*T*T*16.
    localparam integer HTT_BITS = HEADS * TT_BITS;

    // Q=X*Wq 결과. 현재 query가 찾을 특징이며 Python q다.
    wire [TD_BITS-1:0] q_flat;
    // K=X*Wk 결과. 다른 query가 비교할 대상 특징이며 Python k다.
    wire [TD_BITS-1:0] k_flat;
    // V=X*Wv 결과. 관련성 비중으로 합칠 token 내용이며 Python v다.
    wire [TD_BITS-1:0] v_flat;
    // 선언만 남은 전체 head raw score 집계 배선. 현재 실행 경로는 head별 score_raw_head를 사용한다.
    wire [HTT_BITS-1:0] score_raw_all_flat;
    // [head][query][key] 순서의 모든 attention 확률 bus.
    wire [HTT_BITS-1:0] probs_all_flat;
    // head context를 hidden channel 축으로 연결한 [T,D] tensor. Python all_context_rows와 같다.
    reg  [TD_BITS-1:0] context_concat_flat;
    // head 연결 context*Wo의 전체 attention 출력.
    wire [TD_BITS-1:0] attention_projected_flat;
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

    // head별 배열은 각 head가 독립 점수/확률/문맥 행렬을 갖도록 한다.
    // Q=X*Wq 결과. 현재 query가 찾을 특징이며 Python q다.
    wire [TH_BITS-1:0] q_head [0:HEADS-1];
    // K=X*Wk 결과. 다른 query가 비교할 대상 특징이며 Python k다.
    wire [TH_BITS-1:0] k_head [0:HEADS-1];
    // V=X*Wv 결과. 관련성 비중으로 합칠 token 내용이며 Python v다.
    wire [TH_BITS-1:0] v_head [0:HEADS-1];
    // head K를 channel/token 축 교환한 QK^T 피연산자.
    wire [HEAD_DIM*TOKENS*16-1:0] kt_head [0:HEADS-1];
    // QK^T raw 내적을 Q8.8로 줄인 점수. scale 적용 전이며 확률은 아니다.
    wire [TT_BITS-1:0] score_raw_head [0:HEADS-1];
    // causal Softmax가 만든 Q8.8 확률 근사. 미래 token의 기여는 0이다.
    wire [TT_BITS-1:0] prob_head [0:HEADS-1];
    // probability*V 결과. 각 token/head가 관련된 과거 내용을 모은 vector다.
    wire [TH_BITS-1:0] context_head [0:HEADS-1];

    // Python 대응: model/reference.py 또는 model/gpt_q88.py:sat16 = max(-32768,min(32767,value)).
    // 범위 밖 숫자가 16비트에서 반대 부호로 뒤집히는 wrap-around를 막는 saturation(포화) 함수다.
    // raw -32768..32767은 /256하면 -128..127.99609375이다. 소수 비트 >>8 이동은 호출부가 수행한다.
    // automatic은 임시 지역값이 독립적인 SV 함수 선언이며 CPU가 Python 함수를 실행하는 회로는 아니다.
    function automatic signed [15:0] sat16(input signed [63:0] value);
        begin
            if (value > 64'sd32767) sat16 = 16'sd32767;
            else if (value < -64'sd32768) sat16 = -16'sd32768;
            else sat16 = value[15:0];
        end
    endfunction

    // Full-width Q/K/V 결과에서 특정 head 채널만 골라 head-local 텐서로 바꾼다.
    // head h는 [h*HEAD_DIM, (h+1)*HEAD_DIM) 채널을 받는다.
    // Python 대응: [row[h*HEAD_DIM:(h+1)*HEAD_DIM] for row in q] (k/v도 같다).
    // 각 token의 연속 hidden channel 중 한 head 조각만 골라 [T,D] -> [T,HEAD_DIM]으로 묶는다.
    // scale/부호를 바꾸지 않는다. Q/K/V의 같은 channel 영역을 선택해야 같은 head로 비교한다.
    function automatic [TH_BITS-1:0] select_head(
        input [TD_BITS-1:0] full_tensor,
        input integer head_number
    );
        reg [TH_BITS-1:0] result;
        // 현재 embedding/Softmax/Norm 대상 token 위치. 한 vector PU를 여러 token에 재사용하는 주소다.
        integer token_index;
        integer channel_index;
        begin
            result = {TH_BITS{1'b0}};
            for (token_index = 0; token_index < TOKENS; token_index = token_index + 1)
                for (channel_index = 0; channel_index < HEAD_DIM; channel_index = channel_index + 1)
                    result[(token_index*HEAD_DIM+channel_index)*16 +: 16] =
                        full_tensor[(token_index*D_MODEL + head_number*HEAD_DIM + channel_index)*16 +: 16];
            select_head = result;
        end
    endfunction

    // [token][head channel]을 [head channel][token]으로 전치해 QK^T의
    // 두 번째 피연산자로 전달한다.
    // Python 대응: head별 kh를 전치해 Qh@Kh.T 계산에 사용하는 축 교환이다.
    // [T,HEAD_DIM] -> [HEAD_DIM,T] 배선이며 다른 head channel을 섞지 않는다.
    function automatic [HEAD_DIM*TOKENS*16-1:0] transpose_head(
        input [TH_BITS-1:0] tensor
    );
        reg [HEAD_DIM*TOKENS*16-1:0] result;
        // 현재 embedding/Softmax/Norm 대상 token 위치. 한 vector PU를 여러 token에 재사용하는 주소다.
        integer token_index;
        integer channel_index;
        begin
            result = {(HEAD_DIM*TOKENS*16){1'b0}};
            for (token_index = 0; token_index < TOKENS; token_index = token_index + 1)
                for (channel_index = 0; channel_index < HEAD_DIM; channel_index = channel_index + 1)
                    result[(channel_index*TOKENS+token_index)*16 +: 16] =
                        tensor[(token_index*HEAD_DIM+channel_index)*16 +: 16];
            transpose_head = result;
        end
    endfunction

    // QK^T의 각 원소에 head dimension 기준 1/sqrt(HEAD_DIM)을 곱한다.
    // 곱은 Q16.16이므로 오른쪽 8비트를 이동해 Q8.8로 돌아온다.
    // Python 대응: sat16((raw*SCORE_SCALE_Q8)>>8). raw는 QK 내적을 Q8.8로 줄인 값이다.
    // Q8.8*Q8.8 곱은 소수 bit 16개이므로 >>>8로 8개를 버려 Q8.8로 복귀한다.
    // $signed는 packed bit를 음수 가능한 수로 읽고 >>>는 sign bit를 채우는 산술 우측 이동이다.
    // head_dim을 바꾸면 scale도 round(256/sqrt(head_dim))로 변경해 학습/RTL을 일치시킨다.
    function automatic [TT_BITS-1:0] scale_scores(
        input [TT_BITS-1:0] raw_scores
    );
        reg [TT_BITS-1:0] result;
        reg signed [15:0] raw_value;
        integer index;
        begin
            result = {TT_BITS{1'b0}};
            for (index = 0; index < TOKENS*TOKENS; index = index + 1) begin
                raw_value = $signed(raw_scores[index*16 +: 16]);
                result[index*16 +: 16] = sat16(($signed(raw_value) * SCORE_SCALE_Q8) >>> 8);
            end
            scale_scores = result;
        end
    endfunction

    // Q/K/V는 각각 D_MODEL×D_MODEL 투영이다. 이후 head split만 달라지고, 학습된
    // 전체 projection matrix를 그대로 사용한다. 나머지 행렬곱은 같은 bank-local
    // balanced-adder-tree VMM을 재사용한다.
    // Python q=qmat(x,wq). head들이 분할할 전체 D 채널 Query projection.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_MODEL), .COLS(D_MODEL)) u_q_projection (
        .activation_flat(x_flat), .weight_flat(wq_flat), .result_flat(q_flat)
    );
    // Python k=qmat(x,wk). Q와 같은 head 분할 위치의 Key projection.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_MODEL), .COLS(D_MODEL)) u_k_projection (
        .activation_flat(x_flat), .weight_flat(wk_flat), .result_flat(k_flat)
    );
    // Python v=qmat(x,wv). attention으로 합칠 내용 projection.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_MODEL), .COLS(D_MODEL)) u_v_projection (
        .activation_flat(x_flat), .weight_flat(wv_flat), .result_flat(v_flat)
    );

    genvar head_index;
    // generate는 실행 중 반복이 아니라 elaboration 때 고정 개수 회로를 만드는 문법이다.
    // head/token/layer 숫자를 늘리면 물리 복제 회로와 조합 경로 크기가 바뀐다.
    generate
        for (head_index = 0; head_index < HEADS; head_index = head_index + 1) begin : gen_heads
            assign q_head[head_index] = select_head(q_flat, head_index);
            assign k_head[head_index] = select_head(k_flat, head_index);
            assign v_head[head_index] = select_head(v_flat, head_index);
            assign kt_head[head_index] = transpose_head(k_head[head_index]);

            // Python 한 head sum(qh[token][d]*kh[other][d]). HEAD_DIM을 내적 축으로 한다.
            dram_pim_vmm_bank #(.ROWS(TOKENS), .K(HEAD_DIM), .COLS(TOKENS)) u_qk_vmm (
                .activation_flat(q_head[head_index]),
                .weight_flat(kt_head[head_index]),
                .result_flat(score_raw_head[head_index])
            );

            // probability*V: 관련성 비중으로 token 내용 vector를 합친다.
            dram_pim_vmm_bank #(.ROWS(TOKENS), .K(TOKENS), .COLS(HEAD_DIM)) u_context_vmm (
                .activation_flat(prob_head[head_index]),
                .weight_flat(v_head[head_index]),
                .result_flat(context_head[head_index])
            );

            genvar token_index;
            for (token_index = 0; token_index < TOKENS; token_index = token_index + 1) begin : gen_head_softmax
                // 토큰 i는 자기 자신과 이전 토큰까지만 볼 수 있다. mask의 하위
                // i+1 비트를 1로 설정하여 미래 정보가 Softmax에 들어오지 못하게 한다.
                localparam [TOKENS-1:0] CAUSAL_MASK = ({{(TOKENS-1){1'b0}}, 1'b1} << (token_index+1)) - 1'b1;
                wire [TT_BITS-1:0] scaled_scores;
                assign scaled_scores = scale_scores(score_raw_head[head_index]);
                // Python softmax_q8(scores,causal_valid). 미래 위치 기여를 0으로 하고 유효 점수를 비중으로 바꾼다.
                dram_pim_softmax_pu #(.VEC_LEN(TOKENS)) u_softmax (
                    .a_flat(scaled_scores[token_index*TOKENS*16 +: TOKENS*16]),
                    .valid_mask(CAUSAL_MASK),
                    .y_flat(probs_all_flat[(head_index*TOKENS*TOKENS + token_index*TOKENS)*16 +: TOKENS*16])
                );
            end

            assign prob_head[head_index] = probs_all_flat[head_index*TT_BITS +: TT_BITS];
        end
    endgenerate

    // 모든 head의 문맥을 channel 축으로 연결(concatenate)한다. head 0이 앞의
    // HEAD_DIM 채널, head 1이 그 다음 채널을 차지하며 총 D_MODEL 채널이 된다.
    integer h;
    integer t;
    integer d;
    // 조합 계산/배선 블록. for는 합성시 고정 개수의 회로로 펼쳐지며 한 반복=한 clock이 아니다.
    // 모든 output 원소에 값을 정의해 이전 값을 유지하는 latch가 생기지 않게 한다.
    always @* begin
        context_concat_flat = {TD_BITS{1'b0}};
        for (h = 0; h < HEADS; h = h + 1) begin
            for (t = 0; t < TOKENS; t = t + 1)
                for (d = 0; d < HEAD_DIM; d = d + 1)
                    context_concat_flat[(t*D_MODEL + h*HEAD_DIM+d)*16 +: 16] =
                        context_head[h][(t*HEAD_DIM+d)*16 +: 16];
        end
        y_flat = norm2_flat;
    end

    // 결합한 head 결과에 출력 투영을 적용한다. 그 뒤 residual/LN, FFN, residual/LN을
    // 거쳐 한 decoder block을 완성한다.
    // Python attention=qmat(all_context_rows,wo). 모든 head의 context를 섞는다.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_MODEL), .COLS(D_MODEL)) u_output_projection (
        .activation_flat(context_concat_flat), .weight_flat(wo_flat), .result_flat(attention_projected_flat)
    );
    // Python ff1=qmat(norm1,w1). token별 D -> F 특징 확장.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_MODEL), .COLS(D_FF)) u_ffn_expand (
        .activation_flat(norm1_flat), .weight_flat(w1_flat), .result_flat(ff1_flat)
    );
    // Python ff2=qmat(relu,w2). token별 F -> D 특징 축소.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_FF), .COLS(D_MODEL)) u_ffn_contract (
        .activation_flat(relu_flat), .weight_flat(w2_flat), .result_flat(ff2_flat)
    );

    genvar row_index;
    // generate는 실행 중 반복이 아니라 elaboration 때 고정 개수 회로를 만드는 문법이다.
    // head/token/layer 숫자를 늘리면 물리 복제 회로와 조합 경로 크기가 바뀐다.
    generate
        for (row_index = 0; row_index < TOKENS; row_index = row_index + 1) begin : gen_block_pus
            // Python sat16(x+attention). attention 처리 전 특징을 보존하는 첫 residual.
            dram_pim_add_pu #(.VEC_LEN(D_MODEL)) u_residual1 (
                .a_flat(x_flat[row_index*D_MODEL*16 +: D_MODEL*16]),
                .b_flat(attention_projected_flat[row_index*D_MODEL*16 +: D_MODEL*16]),
                .y_flat(residual1_flat[row_index*D_MODEL*16 +: D_MODEL*16])
            );
            // Python layernorm_q8(residual1). token별 channel 평균/분산 정규화.
            dram_pim_layernorm_pu #(.VEC_LEN(D_MODEL)) u_layernorm1 (
                .a_flat(residual1_flat[row_index*D_MODEL*16 +: D_MODEL*16]),
                .y_flat(norm1_flat[row_index*D_MODEL*16 +: D_MODEL*16])
            );
            // Python max(0,ff1_value). 음수를 0으로 만드는 FFN 비선형.
            dram_pim_relu_pu #(.VEC_LEN(D_FF)) u_relu (
                .a_flat(ff1_flat[row_index*D_FF*16 +: D_FF*16]),
                .y_flat(relu_flat[row_index*D_FF*16 +: D_FF*16])
            );
            // Python sat16(norm1+ff2). FFN 전 특징을 보존하는 두 번째 residual.
            dram_pim_add_pu #(.VEC_LEN(D_MODEL)) u_residual2 (
                .a_flat(norm1_flat[row_index*D_MODEL*16 +: D_MODEL*16]),
                .b_flat(ff2_flat[row_index*D_MODEL*16 +: D_MODEL*16]),
                .y_flat(residual2_flat[row_index*D_MODEL*16 +: D_MODEL*16])
            );
            // Python layernorm_q8(residual2). block을 마무리하는 post-norm.
            dram_pim_layernorm_pu #(.VEC_LEN(D_MODEL)) u_layernorm2 (
                .a_flat(residual2_flat[row_index*D_MODEL*16 +: D_MODEL*16]),
                .y_flat(norm2_flat[row_index*D_MODEL*16 +: D_MODEL*16])
            );
        end
    endgenerate

    // 단순화한 외부 경계 카운터. 이 수치는 메모리 트래픽을 실제 계측한 값이 아니며,
    // 블록 사이의 activation 왕복을 줄이는 가정만 보인다. 파라미터 변경 시 MAC 수는
    // head 개수와 무관하게 동일한데, 전체 head_dim의 합이 D_MODEL이기 때문이다.
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
    // head별 Softmax T*HEADS와 기타 다섯 개 벡터 단계 T*5를 각각 계산한다.
    // Softmax/Residual/Norm/활성화의 vector 단계 수. 개별 산술 덧셈 개수와 다르다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign nonvmm_vector_ops = TOKENS*(HEADS+5);

    // elaboration/simulation 설정 검사. 양의 차원/head 나눗셈 조건이 깨진 회로는 오류를 알린다.
    // 매 token에서 모델 shape를 검사하는 동적 FPGA 기능은 아니다.
    initial begin
        if (HEADS < 1) $error("HEADS must be at least 1");
        if ((D_MODEL % HEADS) != 0) $error("D_MODEL must be divisible by HEADS");
        if (TOKENS < 1 || D_FF < 1) $error("TOKENS and D_FF must be positive");
    end
endmodule
