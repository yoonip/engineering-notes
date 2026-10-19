// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// -----------------------------------------------------------------------------
// 자원 공유형, 순차 동작 GPT-style Transformer 언어 모델
//
// comb 버전은 기능 확인에 편하지만 토큰·head·layer·행렬 원소마다 연산 회로를
// 한꺼번에 펼친다. 이 모듈은 하나의 signed Q8.8 MAC을 시간에 따라 재사용한다.
// 한 출력 원소의 내적을 k=0부터 한 항씩 누산하고, 마지막 항에서만 Q8.8로
// 이동·포화한다. 따라서 연산 사이클은 늘지만 복제 MAC 수를 크게 줄이는 구조다.
//
// 동작 순서:
// token/position embedding → 각 layer의 Q,K,V → head별 QK^T → causal Softmax
// → head별 probability×V → head 연결 → Wo → residual/LayerNorm → W1/ReLU/W2
// → residual/LayerNorm → 다음 layer 또는 vocabulary LM head
//
// 주의: 입력 weight/embedding/token bus는 start가 받아들여진 뒤 done이 나올 때까지
// 바뀌지 않아야 한다. 토크나이저와 다음 토큰 sampling은 host software가 맡는다.
// 이 RTL은 기능적으로 완성된 context-to-logits 경로이며, 실제 DRAM PHY나 vendor
// FPGA timing closure는 별도의 메모리·part·clock 제약과 도구로 검증해야 한다.
// -----------------------------------------------------------------------------
// [학습용 상세 해설 2026-10-04]
// 위치: 전체 context를 단일 MAC/Softmax/LayerNorm의 시간 분할로 처리하는 core.
// Python 대응: model/gpt_language_model_reference.py:language_model_logits 및
// model/gpt_core_reference.py:decoder_block/decoder_stack의 중첩 for를 FSM으로 바꾼다.
// qmat의 for row/column/k가 mac_row/mac_col/mac_k에 대응한다. S_MAC_RUN 한 클록은
// a*b 한 항을 처리한다. 중간값/register/누산기/다음 상태가 물리적으로 명시되어 있다.
// 제어/PU/복사 상태도 별도 클록을 사용한다. 거래마다 전체 context를 다시 계산한다.
// bias/GELU/affine/KV cache는 이 버전에 없고 transformer_gpt_kvcache_seq가 제공한다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module transformer_gpt_language_model_seq #(
    // context 토큰 수 T. attention 점수는 T*T개이며 문자열 byte 수와 항상 같지는 않다.
    parameter integer TOKENS = 4,
    // 어휘 후보 수 V. V=65는 logit 65개를 뜻하며 65개 지식을 학습했다는 뜻이 아니다.
    parameter integer VOCAB_SIZE = 16,
    // 토큰마다 hidden 숫자 수 D. embedding/residual 폭이며 모든 head 채널 수 합이 D다.
    parameter integer D_MODEL = 8,
    // attention 관점 수 H. head_dim=D_MODEL/HEADS이며 서로 다른 채널로 독립 점수/확률을 만든다.
    parameter integer HEADS = 2,
    // FFN 중간 채널 수 F. W1=D*F, W2=F*D이고 폭을 키우면 연산/저장 비용도 커진다.
    parameter integer D_FF = 16,
    // decoder block 반복 층 수 L. 앞 층 출력이 다음 층 입력이며 층마다 별도 weight다.
    parameter integer LAYERS = 2,
    // round(256/sqrt(head_dim)) 정수. QK의 차원 효과를 완화하며 head_dim=4일 때 128=0.5다.
    parameter integer SCORE_SCALE_Q8 = 128,
    // ID 비트 폭. V=65일 때 7비트(0..127)를 표현하지만 유효 번호는 0..64다.
    parameter integer TOKEN_BITS = (VOCAB_SIZE <= 1) ? 1 : $clog2(VOCAB_SIZE)
) (
    // 클록 입력. 순차 회로는 상승 에지에서 계산 결과를 register에 저장한다. comb wrapper에서는 비교용으로만 남는다.
    input  wire clk,
    // 0일 때 초기화하는 active-low reset. 상태/위치/완료 신호를 시작 값으로 만들고 KV 문맥을 새로 시작한다.
    input  wire reset_n,
    // 계산 요청. 순차 core는 idle에서만 수락하므로 ready/busy 확인 후 한 클록 펄스를 준다.
    input  wire start,
    // token t의 ID는 [t*TOKEN_BITS +: TOKEN_BITS]. Python token_ids[t]를 낮은 token 순서부터 묶는다.
    input  wire [TOKENS*TOKEN_BITS-1:0] token_ids_flat,
    // [어휘 ID][hidden 채널] 학습 표. Python weights['token_embedding'][token_id][channel]을 row-major로 묶는다.
    input  wire [VOCAB_SIZE*D_MODEL*16-1:0] token_embedding_flat,
    // [위치][hidden 채널] 학습 표. 순서를 나타내기 위해 embedding에 더하는 weights['position_embedding'][position][channel]이다.
    input  wire [TOKENS*D_MODEL*16-1:0] position_embedding_flat,
    // [layer][입력 채널][출력 채널] Query 가중치. layer 0 원소가 낮은 bit에 놓이며 Python layer['wq'] 방향이다.
    input  wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wq_layers_flat,
    // [layer][입력 채널][출력 채널] Key 가중치. 층마다 다른 학습 행렬로 검색 대상 특징을 만든다.
    input  wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wk_layers_flat,
    // [layer][입력 채널][출력 채널] Value 가중치. 현재 층의 입력 hidden에서 꺼낼 내용을 만든다.
    input  wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wv_layers_flat,
    // [layer][D_MODEL][D_MODEL] 출력 투영. head별 context를 연결한 뒤 전체 특징으로 섞는다.
    input  wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wo_layers_flat,
    // [layer][D_MODEL][D_FF] FFN 확장 행렬. Python layer['w1']와 row-major 방향이 같다.
    input  wire [LAYERS*D_MODEL*D_FF*16-1:0] w1_layers_flat,
    // [layer][D_FF][D_MODEL] FFN 축소 행렬. Python layer['w2']와 row-major 방향이 같다.
    input  wire [LAYERS*D_FF*D_MODEL*16-1:0] w2_layers_flat,
    // [hidden 채널][어휘 ID] 출력 행렬. 마지막 hidden을 다음 문자 후보별 logit 점수로 바꾼다.
    input  wire [D_MODEL*VOCAB_SIZE*16-1:0] lm_head_flat,
    // embedding+position 중간 결과 [토큰][채널]. 문자열 ID가 처음 숫자 특징으로 변한 위치를 확인하는 출력이다.
    output reg  [TOKENS*D_MODEL*16-1:0] embedding_sum_flat,
    // 마지막 decoder의 hidden 특징. raw/256으로 읽으며 개별 채널에 고정된 자연어 단어 뜻이 있지는 않다.
    output reg  [TOKENS*D_MODEL*16-1:0] hidden_flat,
    // 다음 어휘 후보별 Q8.8 점수. 확률이 아니며 argmax/sampling으로 고른 ID를 vocab[id]로 문자로 바꾼다.
    output reg  [TOKENS*VOCAB_SIZE*16-1:0] logits_flat,
    // 계산 중 또는 결과 소비 대기 상태. 1이면 새 start를 수락하지 않는다.
    output wire busy,
    // 계산 완료 한 클록 pulse. KV 결과를 지속해서 읽으려면 result_valid도 확인한다.
    output reg done,
    // 최근 거래의 클록 수. 초 단위 시간=cycle_count*클록 주기다. KV의 output 대기 시간도 늘릴 수 있다.
    output reg [31:0] cycle_count,
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    output reg [31:0] mac_count
);
    // 한 head의 채널 수 D/H. QK 내적 길이이자 연결 전 context 폭이다.
    localparam integer HEAD_DIM = D_MODEL / HEADS;

    // 상태 레지스터. 모든 연산 단계가 한 번에 한 종류만 활성화되므로
    // Q/K/V, attention, FFN용 전체 MAC 배열을 동시에 복제하지 않는다.
    localparam [4:0] S_IDLE          = 5'd0;
    localparam [4:0] S_EMBED         = 5'd1;
    localparam [4:0] S_Q_START       = 5'd2;
    localparam [4:0] S_K_START       = 5'd3;
    localparam [4:0] S_V_START       = 5'd4;
    localparam [4:0] S_QK_START      = 5'd5;
    localparam [4:0] S_QK_NEXT       = 5'd6;
    localparam [4:0] S_SOFTMAX       = 5'd7;
    localparam [4:0] S_CTX_START     = 5'd8;
    localparam [4:0] S_CTX_NEXT      = 5'd9;
    localparam [4:0] S_WO_START      = 5'd10;
    localparam [4:0] S_RESID1        = 5'd11;
    localparam [4:0] S_NORM1         = 5'd12;
    localparam [4:0] S_W1_START      = 5'd13;
    localparam [4:0] S_W2_START      = 5'd14;
    localparam [4:0] S_RESID2        = 5'd15;
    localparam [4:0] S_NORM2         = 5'd16;
    localparam [4:0] S_LM_START      = 5'd17;
    localparam [4:0] S_MAC_START     = 5'd18;
    localparam [4:0] S_MAC_RUN       = 5'd19;
    localparam [4:0] S_FINISH        = 5'd20;
    localparam [4:0] S_NEXT_LAYER    = 5'd21;

    // matrix-operation selector for the one shared MAC datapath.
    // shared MAC selector의 번호. 물리 multiplier를 새로 만들지 않고 입력/출력 mux와 dimension을 선택한다.
    localparam [3:0] OP_Q   = 4'd0;
    // shared MAC selector의 번호. 물리 multiplier를 새로 만들지 않고 입력/출력 mux와 dimension을 선택한다.
    localparam [3:0] OP_K   = 4'd1;
    // shared MAC selector의 번호. 물리 multiplier를 새로 만들지 않고 입력/출력 mux와 dimension을 선택한다.
    localparam [3:0] OP_V   = 4'd2;
    // shared MAC selector의 번호. 물리 multiplier를 새로 만들지 않고 입력/출력 mux와 dimension을 선택한다.
    localparam [3:0] OP_QK  = 4'd3;
    // shared MAC selector의 번호. 물리 multiplier를 새로 만들지 않고 입력/출력 mux와 dimension을 선택한다.
    localparam [3:0] OP_CTX = 4'd4;
    // shared MAC selector의 번호. 물리 multiplier를 새로 만들지 않고 입력/출력 mux와 dimension을 선택한다.
    localparam [3:0] OP_WO  = 4'd5;
    // shared MAC selector의 번호. 물리 multiplier를 새로 만들지 않고 입력/출력 mux와 dimension을 선택한다.
    localparam [3:0] OP_W1  = 4'd6;
    // shared MAC selector의 번호. 물리 multiplier를 새로 만들지 않고 입력/출력 mux와 dimension을 선택한다.
    localparam [3:0] OP_W2  = 4'd7;
    // shared MAC selector의 번호. 물리 multiplier를 새로 만들지 않고 입력/출력 mux와 dimension을 선택한다.
    localparam [3:0] OP_LM  = 4'd8;

    // 순차 FSM 현재 단계 번호. decoder-stack의 wire state 배열은 층 연결 배선이므로 별도 의미다.
    reg [4:0] state;
    // shared MAC이 현재 행렬을 끝낸 뒤 돌아갈 단계. Python 함수 호출 뒤 다음 연산으로 이어지는 제어와 같다.
    reg [4:0] return_state;
    // shared MAC의 행렬 종류 selector. Q/K/V/QK/context/Wo/W1/W2/LM마다 input/output mux를 바꾼다.
    reg [3:0] mac_operation;
    // 한 거래에서 쓸 context ID들을 수락 순간 저장한 배열. Python token_ids list와 대응한다.
    reg [31:0] token_id_mem [0:TOKENS-1];
    // 현재 decoder 층 번호. packed layer weight의 시작 주소와 KV cache layer 주소를 결정한다.
    reg [31:0] layer_index;
    // 현재 embedding/Softmax/Norm 대상 token 위치. 한 vector PU를 여러 token에 재사용하는 주소다.
    reg [31:0] token_index;
    // 현재 attention head 번호. hidden 채널 offset=head_index*HEAD_DIM이다.
    reg [31:0] head_index;

    // Transformer의 중간 텐서들은 작은 SRAM/register-file처럼 저장한다.
    // 배열 하나를 모든 단계가 공유해 full-unroll comb 구조보다 저장 자원이 명시적이다.
    // 현재 층 입력 hidden 표현. 첫 층은 embedding+position, 다음 층은 이전 norm2다.
    reg signed [15:0] x_mem       [0:TOKENS-1][0:D_MODEL-1];
    // Q=X*Wq 결과. 현재 query가 찾을 특징이며 Python q다.
    reg signed [15:0] q_mem       [0:TOKENS-1][0:D_MODEL-1];
    // K=X*Wk 결과. 다른 query가 비교할 대상 특징이며 Python k다.
    reg signed [15:0] k_mem       [0:TOKENS-1][0:D_MODEL-1];
    // V=X*Wv 결과. 관련성 비중으로 합칠 token 내용이며 Python v다.
    reg signed [15:0] v_mem       [0:TOKENS-1][0:D_MODEL-1];
    // [head][query token][key token] 전체 context attention 점수. causal mask는 Softmax 입력에 따로 적용한다.
    reg signed [15:0] score_mem   [0:HEADS-1][0:TOKENS-1][0:TOKENS-1];
    // [head][query token][key token] 전체 context 확률 근사. 미래 위치는 mask로 0이다.
    reg signed [15:0] prob_mem    [0:HEADS-1][0:TOKENS-1][0:TOKENS-1];
    // probability*V 결과. 각 token/head가 관련된 과거 내용을 모은 vector다.
    reg signed [15:0] context_mem [0:TOKENS-1][0:D_MODEL-1];
    // context*Wo 결과. residual에 더하기 전 attention 출력.
    reg signed [15:0] attn_mem    [0:TOKENS-1][0:D_MODEL-1];
    // x+attention의 첫 포화 residual. LayerNorm 입력이다.
    reg signed [15:0] resid1_mem  [0:TOKENS-1][0:D_MODEL-1];
    // 첫 residual의 LayerNorm 결과. FFN 입력이자 두 번째 residual 경로다.
    reg signed [15:0] norm1_mem   [0:TOKENS-1][0:D_MODEL-1];
    // W1 확장 후 활성화한 FFN 중간 특징. seq 버전은 ReLU 결과를 저장한다.
    reg signed [15:0] ff1_mem     [0:TOKENS-1][0:D_FF-1];
    // 활성화한 FFN 특징*W2의 축소 출력. norm1과 residual 덧셈한다.
    reg signed [15:0] ff2_mem     [0:TOKENS-1][0:D_MODEL-1];
    // norm1+FFN의 두 번째 포화 residual.
    reg signed [15:0] resid2_mem  [0:TOKENS-1][0:D_MODEL-1];
    // 두 번째 residual의 LayerNorm. 다음 층 입력 또는 최종 hidden이다.
    reg signed [15:0] norm2_mem   [0:TOKENS-1][0:D_MODEL-1];

    // 현재 MAC 내적의 행·열·축 카운터와 Q16.16 넓은 누산기.
    // Q8.8로의 절삭/포화는 한 dot product가 끝나는 순간 단 한 번만 한다.
    // qmat output 행 번호. context 전체 처리 core에서 token 행을 선택한다.
    integer mac_row;
    // qmat output 열 번호. projection에서는 출력 channel, QK에서는 key token, LM에서는 어휘 ID다.
    integer mac_col;
    // 현재 내적 항 번호. Python sum(a[r][k]*b[k][c] for k ...)의 k를 클록마다 증가시킨다.
    integer mac_k;
    // 현재 MAC 행렬의 출력 행 수. 전체 context core는 주로 TOKENS이고 cache core는 한 token 행이다.
    integer op_rows;
    // 현재 내적 길이. QKV/LM는 D, QK는 head_dim, context는 유효 token 수, W2는 F다.
    integer op_inner;
    // 현재 MAC 출력 열 수. projection은 D/F, context는 head_dim, LM는 V다.
    integer op_cols;
    // 내적 중간 signed 64bit 누산기. Q16.16 항을 더해 overflow/중간 절삭을 줄인다.
    reg signed [63:0] mac_acc;
    // 현재 내적의 activation 쪽 Q8.8 입력. mac_operation에 따라 x/q/prob/context/norm/FFN에서 선택한다.
    reg signed [15:0] operand_a;
    // 현재 내적의 weight/key/value 쪽 Q8.8 입력. packed 가중치 또는 cache 배열의 주소 mux다.
    reg signed [15:0] operand_b;
    // signed 16bit*16bit 한 항의 32bit 곱. 아직 >>8하지 않은 Q16.16 raw다.
    reg signed [31:0] product_value;
    // mac_acc+현재 곱 항의 조합 결과. 마지막 항일 때 이 값을 저장/포화해야 해당 항이 빠지지 않는다.
    reg signed [63:0] accumulated_next;
    // 내적 끝의 >>8/포화 및 선택 bias/scale 결과. 각 중간 tensor에 저장하는 16bit word다.
    reg signed [15:0] q88_result;
    // QK 내적의 scale 곱 중간값. 다른 linear output에는 attention scale을 적용하지 않는다.
    reg signed [63:0] scaled_result_wide;

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

    // residual와 embedding은 16비트 합계가 wrap되기 전에 17비트로 계산해 포화한다.
    // Python 대응: sat16(left_value+right_value). embedding/residual/bias/beta에서 사용한다.
    // 16비트 두 수의 합을 17비트로 계산해 carry/부호를 보존한 뒤 포화한다.
    // 같은 Q8.8 덧셈에는 >>8이 필요 없다. 256+128=384는 1.0+0.5=1.5다.
    function automatic signed [15:0] sat_add16(
        input signed [15:0] left_value,
        input signed [15:0] right_value
    );
        reg signed [16:0] sum_wide;
        begin
            sum_wide = $signed(left_value) + $signed(right_value);
            if (sum_wide > 17'sd32767) sat_add16 = 16'sd32767;
            else if (sum_wide < -17'sd32768) sat_add16 = -16'sd32768;
            else sat_add16 = sum_wide[15:0];
        end
    endfunction

    // 계산/결과 대기를 상태 비교로 표시. comb top의 상수 0은 transaction FSM이 없는 비교 표현이다.
    assign busy = (state != S_IDLE);

    // 현재 operation의 행렬 크기와 한 MAC cycle의 피연산자를 선택한다.
    // 각 행렬 출력은 순차적으로 계산하며, head 수나 vocabulary 폭만큼 MAC을 복제하지 않는다.
    // 공유 MAC input mux/차원/결과 조합 블록. mac_operation이 Python qmat의 어느 행렬을 실행할지 선택한다.
    // 처음 기본값을 주고 필요한 조건에서 덮어써 latch(이전 값 유지 회로)를 방지한다.
    // 이 블록은 clock을 기다리지 않는다. 깊이가 크면 출력 저장까지 한 clock timing을 넘을 수 있다.
    always @* begin
        op_rows = TOKENS;
        op_inner = D_MODEL;
        op_cols = D_MODEL;
        operand_a = 16'sd0;
        operand_b = 16'sd0;

        // operation마다 서로 다른 tensor/weight/cache를 읽고 쓰는 mux 선택. Python의 qmat 인자 선택을 물리 배선으로 바꾼다.
        case (mac_operation)
            OP_Q, OP_K, OP_V, OP_WO: begin
                op_rows = TOKENS; op_inner = D_MODEL; op_cols = D_MODEL;
            end
            OP_QK: begin
                op_rows = TOKENS; op_inner = HEAD_DIM; op_cols = TOKENS;
            end
            OP_CTX: begin
                op_rows = TOKENS; op_inner = TOKENS; op_cols = HEAD_DIM;
            end
            OP_W1: begin
                op_rows = TOKENS; op_inner = D_MODEL; op_cols = D_FF;
            end
            OP_W2: begin
                op_rows = TOKENS; op_inner = D_FF; op_cols = D_MODEL;
            end
            OP_LM: begin
                op_rows = TOKENS; op_inner = D_MODEL; op_cols = VOCAB_SIZE;
            end
            default: begin
                op_rows = TOKENS; op_inner = D_MODEL; op_cols = D_MODEL;
            end
        endcase

        // activation 쪽 선택: Q/K/V·QK는 hidden/Q, 문맥·FFN·LM head는
        // 해당 단계의 저장 배열을 읽는다.
        // operation마다 서로 다른 tensor/weight/cache를 읽고 쓰는 mux 선택. Python의 qmat 인자 선택을 물리 배선으로 바꾼다.
        case (mac_operation)
            OP_Q, OP_K, OP_V: operand_a = x_mem[mac_row][mac_k];
            OP_QK: operand_a = q_mem[mac_row][head_index*HEAD_DIM+mac_k];
            OP_CTX: operand_a = prob_mem[head_index][mac_row][mac_k];
            OP_WO: operand_a = context_mem[mac_row][mac_k];
            OP_W1: operand_a = norm1_mem[mac_row][mac_k];
            OP_W2: operand_a = ff1_mem[mac_row][mac_k];
            OP_LM: operand_a = norm2_mem[mac_row][mac_k];
            default: operand_a = 16'sd0;
        endcase

        // weight 쪽 선택. Q/K/V·Wo·FFN 가중치는 현재 layer 부분을 외부의
        // 안정된 packed bus에서 읽고, QK/context는 저장된 key/value에서 읽는다.
        // operation마다 서로 다른 tensor/weight/cache를 읽고 쓰는 mux 선택. Python의 qmat 인자 선택을 물리 배선으로 바꾼다.
        case (mac_operation)
            OP_Q: operand_b = $signed(wq_layers_flat[
                ((layer_index*D_MODEL*D_MODEL + mac_k*D_MODEL + mac_col)*16) +: 16]);
            OP_K: operand_b = $signed(wk_layers_flat[
                ((layer_index*D_MODEL*D_MODEL + mac_k*D_MODEL + mac_col)*16) +: 16]);
            OP_V: operand_b = $signed(wv_layers_flat[
                ((layer_index*D_MODEL*D_MODEL + mac_k*D_MODEL + mac_col)*16) +: 16]);
            OP_QK: operand_b = k_mem[mac_col][head_index*HEAD_DIM+mac_k];
            OP_CTX: operand_b = v_mem[mac_k][head_index*HEAD_DIM+mac_col];
            OP_WO: operand_b = $signed(wo_layers_flat[
                ((layer_index*D_MODEL*D_MODEL + mac_k*D_MODEL + mac_col)*16) +: 16]);
            OP_W1: operand_b = $signed(w1_layers_flat[
                ((layer_index*D_MODEL*D_FF + mac_k*D_FF + mac_col)*16) +: 16]);
            OP_W2: operand_b = $signed(w2_layers_flat[
                ((layer_index*D_FF*D_MODEL + mac_k*D_MODEL + mac_col)*16) +: 16]);
            OP_LM: operand_b = $signed(lm_head_flat[
                ((mac_k*VOCAB_SIZE + mac_col)*16) +: 16]);
            default: operand_b = 16'sd0;
        endcase

        // Python term=int(a)*int(b). signed 16bit 곱은 32bit이고 Q8.8*Q8.8=Q16.16 raw다.
        // 누산할 때 중간 항마다 >>8하지 않는다. 전체 내적 마지막에만 자르는 수치 정의를 보존한다.
        product_value = $signed(operand_a) * $signed(operand_b);
        // {{32{product_value[31]}},product_value}는 sign bit를 늘리는 sign extension. 음수 항을 유지한다.
        accumulated_next = mac_acc + {{32{product_value[31]}}, product_value};
        // Python sat16(sum(products)>>8). 소수 8bit 제거 후 포화하여 다음 연산의 Q8.8로 맞춘다.
        q88_result = sat16(accumulated_next >>> 8);
        scaled_result_wide = $signed(q88_result) * SCORE_SCALE_Q8;
        if (mac_operation == OP_QK)
            q88_result = sat16(scaled_result_wide >>> 8);
    end

    // 한 query/head의 causal Softmax만 처리하는 단일 PU. 조합식 기능 PU를 head×token
    // 수만큼 복제하는 대신 FSM이 한 행씩 공급해 결과를 probability RAM에 저장한다.
    // 현재 query/head의 점수 vector를 낮은 word부터 묶은 PU 입력 배선.
    reg [TOKENS*16-1:0] softmax_input_flat;
    // bit j=1이면 key 위치 j를 attention에 포함. 0이면 padding/미래 정보로 제외한다.
    reg [TOKENS-1:0] softmax_valid_mask;
    // Softmax PU의 Q8.8 확률 근사 vector. 정수 나눗셈 절삭으로 합이 정확히 256보다 작을 수 있다.
    wire [TOKENS*16-1:0] softmax_output_flat;
    // 현재 score vector를 packed bit 주소로 연결할 조합 반복 인덱스.
    integer softmax_index;
    // Softmax 입력 packing/valid mask 블록. Python scores/valid를 PU의 packed port로 전달한다.
    // 처음 기본값을 주고 필요한 조건에서 덮어써 latch(이전 값 유지 회로)를 방지한다.
    // 이 블록은 clock을 기다리지 않는다. 깊이가 크면 출력 저장까지 한 clock timing을 넘을 수 있다.
    always @* begin
        softmax_input_flat = {TOKENS*16{1'b0}};
        softmax_valid_mask = {TOKENS{1'b0}};
        for (softmax_index = 0; softmax_index < TOKENS; softmax_index = softmax_index + 1) begin
            softmax_input_flat[softmax_index*16 +: 16] =
                score_mem[head_index][token_index][softmax_index];
            softmax_valid_mask[softmax_index] = (softmax_index <= token_index);
        end
    end
    // 하나의 Softmax를 head/token 순서대로 재사용하여 회로 복제를 줄인다.
    dram_pim_softmax_pu #(.VEC_LEN(TOKENS)) u_one_softmax_pu (
        .a_flat(softmax_input_flat),
        .valid_mask(softmax_valid_mask),
        .y_flat(softmax_output_flat)
    );

    // 단일 LayerNorm PU. 먼저 residual 벡터를 저장하고, 다음 cycle에서 그 벡터를
    // PU에 넣는다. 이렇게 해야 nonblocking register 갱신 전 이전 token이 섞이지 않는다.
    // 현재 residual vector를 LayerNorm PU에 연결하는 packing signal.
    reg [D_MODEL*16-1:0] layernorm_input_flat;
    // LayerNorm PU의 정규화 Q8.8 vector. 학습 affine 사용 시 이 뒤 gamma/beta를 적용한다.
    wire [D_MODEL*16-1:0] layernorm_output_flat;
    // LayerNorm packed vector의 channel 배선 인덱스. 한 반복이 한 클록을 뜻하지 않는다.
    integer norm_index;
    // LayerNorm 입력 선택 블록. S_NORM1/2가 첫/두 번째 residual을 같은 PU에 연결한다.
    // 처음 기본값을 주고 필요한 조건에서 덮어써 latch(이전 값 유지 회로)를 방지한다.
    // 이 블록은 clock을 기다리지 않는다. 깊이가 크면 출력 저장까지 한 clock timing을 넘을 수 있다.
    always @* begin
        layernorm_input_flat = {D_MODEL*16{1'b0}};
        for (norm_index = 0; norm_index < D_MODEL; norm_index = norm_index + 1) begin
            if (state == S_NORM1)
                layernorm_input_flat[norm_index*16 +: 16] = resid1_mem[token_index][norm_index];
            else if (state == S_NORM2)
                layernorm_input_flat[norm_index*16 +: 16] = resid2_mem[token_index][norm_index];
        end
    end
    // 하나의 LayerNorm을 token/layer별 재사용. 원본 내부는 조합식이므로 timing을 따로 만족해야 한다.
    dram_pim_layernorm_pu #(.VEC_LEN(D_MODEL)) u_one_layernorm_pu (
        .a_flat(layernorm_input_flat),
        .y_flat(layernorm_output_flat)
    );

    integer copy_index;
    integer channel_index;
    integer vocab_index;
    // embedding lookup 중 현재 token/channel 학습 raw 값.
    reg signed [15:0] token_embedding_value;
    // position lookup 중 현재 token 위치/channel 학습 raw 값.
    reg signed [15:0] position_embedding_value;

    // posedge clk에서 RHS를 이전 register 값으로 계산하고 <= nonblocking으로 동시에 갱신한다.
    // negedge reset_n/rst_n은 비동기 reset이다. 물리 board에서는 reset 해제를 동기화해야 한다.
    // Python 대입과 달리 <= 새 값은 같은 always의 아래 줄에서 즉시 읽히지 않는다.
    // 그래서 residual 저장/Norm 계산, 마지막 layer 저장/다음 layer 복사를 상태로 나눈다.
    always @(posedge clk or negedge reset_n) begin
        if (!reset_n) begin
            state <= S_IDLE;
            return_state <= S_IDLE;
            mac_operation <= OP_Q;
            layer_index <= 0;
            token_index <= 0;
            head_index <= 0;
            mac_row <= 0;
            mac_col <= 0;
            mac_k <= 0;
            mac_acc <= 0;
            done <= 1'b0;
            cycle_count <= 0;
            mac_count <= 0;
            embedding_sum_flat <= {TOKENS*D_MODEL*16{1'b0}};
            hidden_flat <= {TOKENS*D_MODEL*16{1'b0}};
            logits_flat <= {TOKENS*VOCAB_SIZE*16{1'b0}};
        end else begin
            done <= 1'b0;
            // 전체 busy clock에는 control/PU/복사/결과 대기가 포함될 수 있어 MAC 항수와 cycle 수는 다르다.
            if (state != S_IDLE)
                cycle_count <= cycle_count + 1'b1;

            // FSM 단계 switch. 이 clock에 어떤 register를 갱신하고 다음 clock은 무엇을 계산할지 결정한다.
            case (state)
                // 요청 대기/수락. 거래의 인덱스와 cycle/MAC 카운터를 초기화하여 이전 제어 상태가 섞이지 않게 한다.
                S_IDLE: begin
                    // start는 1 cycle pulse다. 입력 bus는 transaction 전체 동안 안정돼야 한다.
                    if (start) begin
                        for (copy_index = 0; copy_index < TOKENS; copy_index = copy_index + 1)
                            token_id_mem[copy_index] <= token_ids_flat[copy_index*TOKEN_BITS +: TOKEN_BITS];
                        layer_index <= 0;
                        token_index <= 0;
                        head_index <= 0;
                        cycle_count <= 0;
                        mac_count <= 0;
                        state <= S_EMBED;
                    end
                end

                // Python state=[sat16(token_embedding[id][ch]+position_embedding[pos][ch]) ...]를 lookup/포화 덧셈으로 수행한다.
                S_EMBED: begin
                    // 매 cycle 한 위치의 embedding 벡터를 읽는다. token id가 어휘 범위를
                    // 벗어나면 기능 comb top과 같이 0 벡터를 만든다.
                    for (channel_index = 0; channel_index < D_MODEL; channel_index = channel_index + 1) begin
                        if (token_id_mem[token_index] < VOCAB_SIZE) begin
                            token_embedding_value = $signed(token_embedding_flat[
                                ((token_id_mem[token_index]*D_MODEL + channel_index)*16) +: 16]);
                            position_embedding_value = $signed(position_embedding_flat[
                                ((token_index*D_MODEL + channel_index)*16) +: 16]);
                            x_mem[token_index][channel_index] <=
                                sat_add16(token_embedding_value, position_embedding_value);
                            embedding_sum_flat[(token_index*D_MODEL+channel_index)*16 +: 16] <=
                                sat_add16(token_embedding_value, position_embedding_value);
                        end else begin
                            x_mem[token_index][channel_index] <= 16'sd0;
                            embedding_sum_flat[(token_index*D_MODEL+channel_index)*16 +: 16] <= 16'sd0;
                        end
                    end
                    if (token_index == TOKENS-1) begin
                        token_index <= 0;
                        state <= S_Q_START;
                    end else token_index <= token_index + 1'b1;
                end

                // MAC 종류를 Q projection으로 정하고 끝나면 K 단계로 돌아오도록 return_state를 설정한다.
                S_Q_START: begin
                    mac_operation <= OP_Q; return_state <= S_K_START; state <= S_MAC_START;
                end
                // 같은 MAC으로 K projection 수행. KV core는 현재 cache 위치에 써서 다음 token에서 재사용한다.
                S_K_START: begin
                    mac_operation <= OP_K; return_state <= S_V_START; state <= S_MAC_START;
                end
                // 같은 MAC으로 V projection 수행. Q/K/V는 수학이 같고 weight/결과 저장 위치가 다르다.
                S_V_START: begin
                    mac_operation <= OP_V; return_state <= S_QK_START;
                    head_index <= 0; state <= S_MAC_START;
                end
                // 한 head의 Q와 K 내적 시작. Python scores의 sum(q[dim]*key[dim])에 대응한다.
                S_QK_START: begin
                    mac_operation <= OP_QK; return_state <= S_QK_NEXT; state <= S_MAC_START;
                end
                // 다음 head로 점수 계산을 넘긴다. 모든 head가 끝나면 Softmax로 가므로 multi-head를 실제 실행한다.
                S_QK_NEXT: begin
                    // QK^T 결과는 한 head의 점수 행렬이다. 다음 head도 같은 MAC을 쓴다.
                    if (head_index == HEADS-1) begin
                        head_index <= 0; token_index <= 0; state <= S_SOFTMAX;
                    end else begin
                        head_index <= head_index + 1'b1; state <= S_QK_START;
                    end
                end
                // 유효 과거 점수를 LUT Softmax 확률 근사로 바꾸어 저장. Python softmax_q8(scores,valid)에 대응한다.
                S_SOFTMAX: begin
                    // 현재 query의 미래 위치는 마스크되며, 계산된 확률을 모두 저장한다.
                    for (copy_index = 0; copy_index < TOKENS; copy_index = copy_index + 1)
                        prob_mem[head_index][token_index][copy_index] <=
                            $signed(softmax_output_flat[copy_index*16 +: 16]);
                    if (token_index == TOKENS-1) begin
                        token_index <= 0;
                        if (head_index == HEADS-1) begin
                            head_index <= 0; state <= S_CTX_START;
                        end else head_index <= head_index + 1'b1;
                    end else token_index <= token_index + 1'b1;
                end
                // probability*V 내적 시작. Python qmat(probabilities,value_head)는 관련성 비중으로 내용을 합친다.
                S_CTX_START: begin
                    mac_operation <= OP_CTX; return_state <= S_CTX_NEXT; state <= S_MAC_START;
                end
                // 한 head 문맥을 해당 hidden 채널에 저장 후 다음 head로 간다. 모두 완료되어야 Wo로 넘어간다.
                S_CTX_NEXT: begin
                    if (head_index == HEADS-1) begin
                        head_index <= 0; state <= S_WO_START;
                    end else begin
                        head_index <= head_index + 1'b1; state <= S_CTX_START;
                    end
                end
                // 연결한 head context에 Wo를 곱해 여러 head의 정보를 hidden 전체로 섞는다.
                S_WO_START: begin
                    mac_operation <= OP_WO; return_state <= S_RESID1;
                    token_index <= 0; state <= S_MAC_START;
                end
                // Python residual1=[sat16(state[ch]+attention[ch]) ...]. 입력과 attention의 첫 포화 residual 덧셈이다.
                S_RESID1: begin
                    // attention 출력에 원래 입력을 더하는 첫 residual connection.
                    for (channel_index = 0; channel_index < D_MODEL; channel_index = channel_index + 1)
                        resid1_mem[token_index][channel_index] <=
                            sat_add16(x_mem[token_index][channel_index], attn_mem[token_index][channel_index]);
                    if (token_index == TOKENS-1) begin
                        token_index <= 0; state <= S_NORM1;
                    end else token_index <= token_index + 1'b1;
                end
                // 첫 residual을 LayerNorm하고 지원 설정에 따라 gamma/beta 적용. FFN에 줄 채널 분포를 조절한다.
                S_NORM1: begin
                    for (channel_index = 0; channel_index < D_MODEL; channel_index = channel_index + 1)
                        norm1_mem[token_index][channel_index] <=
                            $signed(layernorm_output_flat[channel_index*16 +: 16]);
                    if (token_index == TOKENS-1) begin
                        token_index <= 0; state <= S_W1_START;
                    end else token_index <= token_index + 1'b1;
                end
                // FFN D_MODEL -> D_FF 확장 내적. 선형 변환 후 ReLU/GELU가 비선형 특징을 추가한다.
                S_W1_START: begin
                    mac_operation <= OP_W1; return_state <= S_W2_START; state <= S_MAC_START;
                end
                // FFN D_FF -> D_MODEL 축소 내적. 활성화한 특징을 residual 덧셈 가능한 원래 폭으로 돌린다.
                S_W2_START: begin
                    mac_operation <= OP_W2; return_state <= S_RESID2;
                    token_index <= 0; state <= S_MAC_START;
                end
                // Python residual2=[sat16(norm1[ch]+ff2[ch]) ...]. FFN 출력과 첫 norm 특징을 더한다.
                S_RESID2: begin
                    // 두 번째 residual: LayerNorm(첫 norm + FFN 출력).
                    for (channel_index = 0; channel_index < D_MODEL; channel_index = channel_index + 1)
                        resid2_mem[token_index][channel_index] <=
                            sat_add16(norm1_mem[token_index][channel_index], ff2_mem[token_index][channel_index]);
                    if (token_index == TOKENS-1) begin
                        token_index <= 0; state <= S_NORM2;
                    end else token_index <= token_index + 1'b1;
                end
                // 두 번째 post-norm 완료. 마지막 layer이면 LM head, 층이 남으면 다음 layer 입력 복사로 간다.
                S_NORM2: begin
                    for (channel_index = 0; channel_index < D_MODEL; channel_index = channel_index + 1)
                        norm2_mem[token_index][channel_index] <=
                            $signed(layernorm_output_flat[channel_index*16 +: 16]);
                    if (token_index == TOKENS-1) begin
                        token_index <= 0;
                        if (layer_index == LAYERS-1) begin
                            state <= S_LM_START;
                        end else begin
                            // 마지막 norm2 token은 직전 cycle에서 저장됐으므로, 별도 cycle에 넘긴다.
                            state <= S_NEXT_LAYER;
                        end
                    end else token_index <= token_index + 1'b1;
                end
                // norm2를 다음 층 x로 복사하고 layer_index 증가. Python state=layernorm_q8_affine(residual2)다.
                S_NEXT_LAYER: begin
                    for (copy_index = 0; copy_index < TOKENS; copy_index = copy_index + 1)
                        for (channel_index = 0; channel_index < D_MODEL; channel_index = channel_index + 1)
                            x_mem[copy_index][channel_index] <= norm2_mem[copy_index][channel_index];
                    layer_index <= layer_index + 1'b1;
                    state <= S_Q_START;
                end
                // hidden*[D_MODEL,VOCAB_SIZE] LM head로 후보 점수를 만든다. 다음 ID argmax/sampling은 host 역할이다.
                S_LM_START: begin
                    mac_operation <= OP_LM; return_state <= S_FINISH; state <= S_MAC_START;
                end

                // row/col/k 및 accumulator를 0으로 맞추어 새 행렬 연산을 시작한다. qmat 중첩 for 시작점이다.
                S_MAC_START: begin
                    mac_row <= 0; mac_col <= 0; mac_k <= 0; mac_acc <= 0;
                    state <= S_MAC_RUN;
                end
                // 한 clock에 a*b 한 항 누산. 마지막 k에서 >>8/포화 후 결과 저장하고 다음 column/row로 진행한다.
                S_MAC_RUN: begin
                    mac_count <= mac_count + 1'b1;
                    // 마지막 항은 accumulated_next에 이미 포함된다. 저장 후 다음 output accumulator를 0으로 시작한다.
                    if (mac_k == op_inner-1) begin
                        // 출력 한 원소의 내적을 마무리해 해당 중간 텐서의 SRAM 위치에 저장.
                        // operation마다 서로 다른 tensor/weight/cache를 읽고 쓰는 mux 선택. Python의 qmat 인자 선택을 물리 배선으로 바꾼다.
                        case (mac_operation)
                            OP_Q: q_mem[mac_row][mac_col] <= q88_result;
                            OP_K: k_mem[mac_row][mac_col] <= q88_result;
                            OP_V: v_mem[mac_row][mac_col] <= q88_result;
                            OP_QK: score_mem[head_index][mac_row][mac_col] <= q88_result;
                            OP_CTX: context_mem[mac_row][head_index*HEAD_DIM+mac_col] <= q88_result;
                            OP_WO: attn_mem[mac_row][mac_col] <= q88_result;
                            OP_W1: ff1_mem[mac_row][mac_col] <=
                                ($signed(q88_result) < 0) ? 16'sd0 : q88_result;
                            OP_W2: ff2_mem[mac_row][mac_col] <= q88_result;
                            OP_LM: logits_flat[(mac_row*VOCAB_SIZE+mac_col)*16 +: 16] <= q88_result;
                            default: begin end
                        endcase

                        mac_acc <= 0;
                        mac_k <= 0;
                        if (mac_col == op_cols-1) begin
                            mac_col <= 0;
                            if (mac_row == op_rows-1) begin
                                mac_row <= 0;
                                state <= return_state;
                            end else begin
                                mac_row <= mac_row + 1;
                            end
                        end else mac_col <= mac_col + 1;
                    end else begin
                        // 같은 dot product의 다음 항. signed 64-bit 누산으로 carry 보존.
                        mac_acc <= accumulated_next;
                        mac_k <= mac_k + 1;
                    end
                end

                // 최종 hidden을 output bus로 복사하고 완료 pulse. KV core는 token_count 증가 후 결과 소비를 기다린다.
                S_FINISH: begin
                    // 마지막 decoder layer의 norm2를 외부 hidden bus로 내보내고 완료 pulse.
                    for (copy_index = 0; copy_index < TOKENS; copy_index = copy_index + 1)
                        for (channel_index = 0; channel_index < D_MODEL; channel_index = channel_index + 1)
                            hidden_flat[(copy_index*D_MODEL+channel_index)*16 +: 16] <=
                                norm2_mem[copy_index][channel_index];
                    done <= 1'b1;
                    state <= S_IDLE;
                end
                default: state <= S_IDLE;
            endcase
        end
    end

    // elaboration/simulation 설정 검사. 양의 차원/head 나눗셈 조건이 깨진 회로는 오류를 알린다.
    // 매 token에서 모델 shape를 검사하는 동적 FPGA 기능은 아니다.
    initial begin
        if (TOKENS < 1 || VOCAB_SIZE < 1 || D_MODEL < 1 || D_FF < 1 || LAYERS < 1)
            $error("All Transformer dimensions must be positive");
        if (HEADS < 1 || (D_MODEL % HEADS) != 0)
            $error("D_MODEL must be divisible by HEADS");
    end
endmodule
