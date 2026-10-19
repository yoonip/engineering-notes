// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// -----------------------------------------------------------------------------
// 한 token씩 받아 layer별 Key/Value를 보존하는 GPT-style 순차 decoder
//
// transformer_gpt_language_model_seq.sv는 한 번의 start에서 입력 context 전체를
// 다시 계산한다. 이 모듈은 그 결과를 바꾸지 않으면서 생성에 필요한 과거 K/V만
// MAX_TOKENS 위치까지 저장하고, 새 token의 query만 과거 K/V에 대조한다.
// 따라서 이미 처리한 token의 Q/K/V projection과 과거 query attention을 반복하지
// 않는다. MAC 하나, Softmax PU 하나, LayerNorm PU 하나를 모든 head/layer가 공유한다.
//
// 수치/모델 규칙: signed Q8.8, causal multi-head attention, post-norm. 기본값은
// ReLU/bias 없는/affine 없는 정의이며 ENABLE_*로 bias·affine·GELU를 켤 수 있다.
// wrapper는 사용한 학습 checkpoint의 연산 설정과 일치하도록 값을 지정한다.
// Layer마다 K/V를 따로 저장한다. layer N의 K/V는 layer N 입력 hidden에서 나온다.
//
// 제어: input_ready가 1일 때 start를 1-cycle pulse로 올리면 token_id를 받아들인다.
// weight와 embedding bus는 입력 token을 받을 때부터 결과 handshake까지 안정돼야 한다.
// done은 결과가 처음 준비된 때의 pulse이고, result_valid는 result_ready가 1이 될
// 때까지 유지된다. 이 기간에는 busy가 계속 1이며 hidden/logits도 유지된다.
// context가 가득 찬 상태에서 start하면 error와 done이 뜨며 cache는 유지된다.
// learned absolute position을 다시 매겨 sliding하는 기능은 없다; 새 창이 필요하면
// reset_n을 낮추고 새 context를 다시 넣어야 한다.
// -----------------------------------------------------------------------------
// [학습용 상세 해설 2026-10-04]
// 위치: 새 토큰 하나를 받아 layer별 과거 K/V를 재사용하는 순차 full-ops 추론 core.
// Python 대응: model/gpt_q88.py:forward_q88_step. reset은 new_kv_cache, prompt 연속
// 입력은 prefill_q88 반복, 문자를 선택해 재입력하는 host 동작은 generate_q88_cached다.
// embedding -> qmat_bias Q/K/V -> cache.append -> head별 QK/Softmax/context -> Wo
// -> residual/affine LN -> W1 -> GELU/ReLU -> W2 -> residual/affine LN -> LM head다.
// Python은 호출 안에서 끝내지만 RTL은 클록마다 MAC 한 항을 실행하며 값을 저장한다.
// ENABLE_*를 checkpoint와 맞춰야 같은 모델이다. cache 선언만으로 BRAM이 보장되지
// 않는다. 여러 주소/전체 vector 접근은 mux/FF로 합성될 수 있어 주소형 동기 RAM이 필요하다.
// 원본 PU는 한 상태에 조합 division/정규화를 수행하므로 timing 문제가 생길 수 있다.
// MAC을 공유했다는 사실과 전체 core의 clock timing 만족은 각각 따로 검증해야 한다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module transformer_gpt_kvcache_seq #(
    // 어휘 후보 수 V. V=65는 logit 65개를 뜻하며 65개 지식을 학습했다는 뜻이 아니다.
    parameter integer VOCAB_SIZE = 65,
    // 토큰마다 hidden 숫자 수 D. embedding/residual 폭이며 모든 head 채널 수 합이 D다.
    parameter integer D_MODEL = 16,
    // attention 관점 수 H. head_dim=D_MODEL/HEADS이며 서로 다른 채널로 독립 점수/확률을 만든다.
    parameter integer HEADS = 4,
    // FFN 중간 채널 수 F. W1=D*F, W2=F*D이고 폭을 키우면 연산/저장 비용도 커진다.
    parameter integer D_FF = 32,
    // decoder block 반복 층 수 L. 앞 층 출력이 다음 층 입력이며 층마다 별도 weight다.
    parameter integer LAYERS = 2,
    // KV cache 최대 길이. 0..MAX_TOKENS-1 위치를 쓰며 꽉 차면 새 창의 reset/prefill이 필요하다.
    parameter integer MAX_TOKENS = 32,
    // ID 비트 폭. V=65일 때 7비트(0..127)를 표현하지만 유효 번호는 0..64다.
    parameter integer TOKEN_BITS = 7,
    // round(256/sqrt(head_dim)) 정수. QK의 차원 효과를 완화하며 head_dim=4일 때 128=0.5다.
    parameter integer SCORE_SCALE_Q8 = 128,
    // 1이면 linear에 학습 bias를 더한다. checkpoint와 다르면 같은 모델 결과가 아니다.
    parameter integer ENABLE_BIAS = 0,
    // 1이면 LayerNorm 뒤 gamma/beta를 적용한다. gamma=256,beta=0은 Q8.8 항등 affine이다.
    parameter integer ENABLE_NORM_AFFINE = 0,
    // 1은 GELU LUT/보간, 0은 ReLU max(0,x). 학습 checkpoint activation과 맞춘다.
    parameter integer ENABLE_GELU = 0,
    // 0은 기존 [layer][token][channel] 저장 경로를 그대로 사용한다.
    // 1은 같은 K/V 값을 1차원 메모리에 저장해 FPGA distributed RAM 추론을 유도한다.
    // 수치·MAC 순서·FSM의 cycle 수를 바꾸는 옵션이 아니며, BRAM 사용을 의미하지 않는다.
    parameter integer FLAT_DISTRIBUTED_CACHE = 0
) (
    // 클록 입력. 순차 회로는 상승 에지에서 계산 결과를 register에 저장한다. comb wrapper에서는 비교용으로만 남는다.
    input  wire clk,
    // 0일 때 초기화하는 active-low reset. 상태/위치/완료 신호를 시작 값으로 만들고 KV 문맥을 새로 시작한다.
    input  wire reset_n,
    // 계산 요청. 순차 core는 idle에서만 수락하므로 ready/busy 확인 후 한 클록 펄스를 준다.
    input  wire start,
    // 새 입력 수락 가능. 1인 idle에서 start/token_id를 제공한다.
    output wire input_ready,
    // 문자 자체가 아닌 어휘표 정수 번호. Python encode[char]로 만든 ID이고 Q8.8 실수가 아니다.
    input  wire [TOKEN_BITS-1:0] token_id,
    // [어휘 ID][hidden 채널] 학습 표. Python weights['token_embedding'][token_id][channel]을 row-major로 묶는다.
    input  wire [VOCAB_SIZE*D_MODEL*16-1:0] token_embedding_flat,
    // [위치][hidden 채널] 학습 표. 순서를 나타내기 위해 embedding에 더하는 weights['position_embedding'][position][channel]이다.
    input  wire [MAX_TOKENS*D_MODEL*16-1:0] position_embedding_flat,
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
    // [layer][D_MODEL] Q linear bias. 내적 >>8/포화 후 더하는 Python layer.get('bq')이다.
    input  wire [LAYERS*D_MODEL*16-1:0] wq_bias_flat,
    // [layer][D_MODEL] K linear bias. ENABLE_BIAS=1일 때 선택하며 Python layer.get('bk')와 같다.
    input  wire [LAYERS*D_MODEL*16-1:0] wk_bias_flat,
    // [layer][D_MODEL] V linear bias. Python qmat_bias([state],layer['wv'],layer.get('bv'))의 bv다.
    input  wire [LAYERS*D_MODEL*16-1:0] wv_bias_flat,
    // [layer][D_MODEL] attention output bias. Python layer.get('bo')와 같다.
    input  wire [LAYERS*D_MODEL*16-1:0] wo_bias_flat,
    // [layer][D_FF] FFN 확장 bias. 길이는 D_MODEL이 아니라 확장 폭 D_FF다.
    input  wire [LAYERS*D_FF*16-1:0] w1_bias_flat,
    // [layer][D_MODEL] FFN 축소 bias. Python layer.get('b2')를 linear 포화 후 더한다.
    input  wire [LAYERS*D_MODEL*16-1:0] w2_bias_flat,
    // [어휘 ID] LM head bias. Python weights.get('lm_bias')이며 문자 후보 점수 각각에 더한다.
    input  wire [VOCAB_SIZE*16-1:0] lm_bias_flat,
    // [layer][D_MODEL] 첫 LayerNorm 학습 scale gamma. Q8.8 256=배율 1.0이다.
    input  wire [LAYERS*D_MODEL*16-1:0] ln1_gamma_flat,
    // [layer][D_MODEL] 첫 LayerNorm 학습 이동량 beta. gamma 곱셈 >>8/포화 후 더한다.
    input  wire [LAYERS*D_MODEL*16-1:0] ln1_beta_flat,
    // [layer][D_MODEL] 두 번째 LayerNorm gamma. Python layernorm_q8_affine(...,ln2_gamma,...)이다.
    input  wire [LAYERS*D_MODEL*16-1:0] ln2_gamma_flat,
    // [layer][D_MODEL] 두 번째 LayerNorm beta. ENABLE_NORM_AFFINE=0이면 gamma/beta를 쓰지 않는다.
    input  wire [LAYERS*D_MODEL*16-1:0] ln2_beta_flat,
    // 결과 소비 확인. result_valid 이후 모든 logit을 읽은 host가 1을 주어 다음 토큰 수락을 허용한다.
    input  wire result_ready,
    // 마지막 decoder의 hidden 특징. raw/256으로 읽으며 개별 채널에 고정된 자연어 단어 뜻이 있지는 않다.
    output reg  [D_MODEL*16-1:0] hidden_flat,
    // 다음 어휘 후보별 Q8.8 점수. 확률이 아니며 argmax/sampling으로 고른 ID를 vocab[id]로 문자로 바꾼다.
    output reg  [VOCAB_SIZE*16-1:0] logits_flat,
    // 계산 중 또는 결과 소비 대기 상태. 1이면 새 start를 수락하지 않는다.
    output wire busy,
    // 계산 완료 한 클록 pulse. KV 결과를 지속해서 읽으려면 result_valid도 확인한다.
    output reg  done,
    // hidden/logits가 유효함을 유지하는 신호. result_ready handshake까지 데이터가 고정된다.
    output reg  result_valid,
    // 잘못된 어휘 ID/꽉 찬 문맥을 거절하는 한 클록 알림. 잘못된 입력을 정상 결과로 오해하지 않게 한다.
    output reg  error,
    // 완료한 토큰 수. 다음 입력의 absolute position 및 layer별 KV cache 유효 길이이며 Q8.8 숫자가 아니다.
    output reg  [31:0] token_count,
    // 최근 거래의 클록 수. 초 단위 시간=cycle_count*클록 주기다. KV의 output 대기 시간도 늘릴 수 있다.
    output reg  [31:0] cycle_count,
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    output reg  [31:0] mac_count
);
    // 한 head의 채널 수 D/H. QK 내적 길이이자 연결 전 context 폭이다.
    localparam integer HEAD_DIM = D_MODEL / HEADS;

    localparam [4:0]
        S_IDLE       = 5'd0,
        S_EMBED      = 5'd1,
        S_Q_START    = 5'd2,
        S_K_START    = 5'd3,
        S_V_START    = 5'd4,
        S_QK_START   = 5'd5,
        S_QK_NEXT    = 5'd6,
        S_SOFTMAX    = 5'd7,
        S_CTX_START  = 5'd8,
        S_CTX_NEXT   = 5'd9,
        S_WO_START   = 5'd10,
        S_RESID1     = 5'd11,
        S_NORM1      = 5'd12,
        S_W1_START   = 5'd13,
        S_W2_START   = 5'd14,
        S_RESID2     = 5'd15,
        S_NORM2      = 5'd16,
        S_NEXT_LAYER = 5'd17,
        S_LM_START   = 5'd18,
        S_MAC_START  = 5'd19,
        S_MAC_RUN    = 5'd20,
        S_FINISH     = 5'd21,
        S_SOFTMAX_NEXT = 5'd22,
        S_GELU_START = 5'd23,
        S_GELU = 5'd24,
        S_OUTPUT_WAIT = 5'd25;

    localparam [3:0]
        OP_Q  = 4'd0, OP_K  = 4'd1, OP_V  = 4'd2, OP_QK = 4'd3,
        OP_CTX= 4'd4, OP_WO = 4'd5, OP_W1 = 4'd6, OP_W2 = 4'd7,
        OP_LM = 4'd8;

    // 순차 FSM 현재 단계 번호. decoder-stack의 wire state 배열은 층 연결 배선이므로 별도 의미다.
    reg [4:0] state;
    // shared MAC이 현재 행렬을 끝낸 뒤 돌아갈 단계. Python 함수 호출 뒤 다음 연산으로 이어지는 제어와 같다.
    reg [4:0] return_state;
    // shared MAC의 행렬 종류 selector. Q/K/V/QK/context/Wo/W1/W2/LM마다 input/output mux를 바꾼다.
    reg [3:0] mac_operation;
    // 요청 수락 순간 복사한 입력 ID. host가 이후 token_id pin을 바꾸어도 현재 거래 ID는 유지된다.
    reg [TOKEN_BITS-1:0] token_id_latched;
    // 현재 decoder 층 번호. packed layer weight의 시작 주소와 KV cache layer 주소를 결정한다.
    integer layer_index;
    // 현재 attention head 번호. hidden 채널 offset=head_index*HEAD_DIM이다.
    integer head_index;
    // qmat output 열 번호. projection에서는 출력 channel, QK에서는 key token, LM에서는 어휘 ID다.
    integer mac_col;
    // 현재 내적 항 번호. Python sum(a[r][k]*b[k][c] for k ...)의 k를 클록마다 증가시킨다.
    integer mac_k;
    // 현재 내적 길이. QKV/LM는 D, QK는 head_dim, context는 유효 token 수, W2는 F다.
    integer op_inner;
    // 현재 MAC 출력 열 수. projection은 D/F, context는 head_dim, LM는 V다.
    integer op_cols;

    // 현재 token만 보유하는 활성 벡터들. 차례로 재사용되는 동일 MAC이 이 배열을
    // 읽고 씁니다. signed Q8.8 raw 정수이므로 16'sd256은 실수 1.0입니다.
    // 현재 층 입력 hidden 표현. 첫 층은 embedding+position, 다음 층은 이전 norm2다.
    reg signed [15:0] x_vec       [0:D_MODEL-1];
    // Q=X*Wq 결과. 현재 query가 찾을 특징이며 Python q다.
    reg signed [15:0] q_vec       [0:D_MODEL-1];
    // context*Wo 결과. residual에 더하기 전 attention 출력.
    reg signed [15:0] attn_vec    [0:D_MODEL-1];
    // x+attention의 첫 포화 residual. LayerNorm 입력이다.
    reg signed [15:0] resid1_vec  [0:D_MODEL-1];
    // 첫 residual의 LayerNorm 결과. FFN 입력이자 두 번째 residual 경로다.
    reg signed [15:0] norm1_vec   [0:D_MODEL-1];
    // W1 확장 후 활성화한 FFN 중간 특징. ENABLE_GELU에 따라 GELU 또는 ReLU 결과를 저장한다.
    reg signed [15:0] ff1_vec     [0:D_FF-1];
    // W1 linear 결과를 비선형 전에 보존. GELU와 ReLU 선택을 위한 저장점이다.
    reg signed [15:0] ff1_pre_vec [0:D_FF-1];
    // 활성화한 FFN 특징*W2의 축소 출력. norm1과 residual 덧셈한다.
    reg signed [15:0] ff2_vec     [0:D_MODEL-1];
    // norm1+FFN의 두 번째 포화 residual.
    reg signed [15:0] resid2_vec  [0:D_MODEL-1];
    // 두 번째 residual의 LayerNorm. 다음 층 입력 또는 최종 hidden이다.
    reg signed [15:0] norm2_vec   [0:D_MODEL-1];
    // probability*V 결과. 각 token/head가 관련된 과거 내용을 모은 vector다.
    reg signed [15:0] context_vec [0:D_MODEL-1];

    // Cache layout [layer][token position][hidden channel]. K와 V를 layer별로
    // 보관해야 현재 token이 해당 layer를 통과할 때 과거 layer 입력과 같은 기준의
    // attention key/value를 사용할 수 있습니다. 대기 상태에서는 token_count 이전의 과거 항목이 유효합니다.
    // 현재 token의 K/V projection이 모두 끝난 뒤 QK/CTX에서는 현재 위치token_count도 포함해 읽습니다.
    // [layer][token position][channel] 과거 K 저장. Python cache['layers'][layer]['keys']와 대응한다.
    reg signed [15:0] key_cache   [0:LAYERS-1][0:MAX_TOKENS-1][0:D_MODEL-1];
    // [layer][token position][channel] 과거 V 저장. Python cache['layers'][layer]['values']와 대응한다.
    reg signed [15:0] value_cache [0:LAYERS-1][0:MAX_TOKENS-1][0:D_MODEL-1];

    // [분산 메모리 선택 경로]
    // Transformer의 K/V는 '학습 가중치'가 아니라 지금 입력한 문맥에서 얻은 일시적인 값이다.
    // Python cache['layers'][layer]['keys'][token][channel]과 동일한 16bit signed Q8.8 값을
    // address=(layer*MAX_TOKENS+token)*D_MODEL+channel 순서로 한 줄에 펼친다.
    // 예: L=2,T=32,D=16이면 K 1024word, V 1024word이고 합계 32768bit=4096byte다.
    // 1차원·단일 쓰기 포트·비동기 읽기를 명확하게 표현하면 LUT 안의 분산 RAM을 사용할
    // 가능성이 생긴다. FF 32768개와 큰 선택기로 저장할 필요를 줄이는 것이 목표이며,
    // 실제 RAM primitive/LUT/FF 사용량은 새 Vivado 합성 보고서로 확인해야 한다.
    localparam integer CACHE_WORDS = LAYERS*MAX_TOKENS*D_MODEL;
    localparam integer CACHE_ADDR_BITS = (CACHE_WORDS > 1) ? $clog2(CACHE_WORDS) : 1;
    // 주소는 유효 범위 0..CACHE_WORDS-1만 표현하면 된다. FSM은 ID/context 범위를 검사하고
    // layer/channel도 정의된 반복 범위 안에서 사용하므로 유효 연산 주소는 잘리지 않는다.
    wire [CACHE_ADDR_BITS-1:0] flat_cache_write_address =
        (layer_index*MAX_TOKENS+token_count)*D_MODEL+mac_col;
    // QK: 현재 query 채널과 과거 key token을 내적한다. mac_col은 key 위치, mac_k는 head 채널이다.
    wire [CACHE_ADDR_BITS-1:0] flat_key_read_address =
        (layer_index*MAX_TOKENS+mac_col)*D_MODEL+head_index*HEAD_DIM+mac_k;
    // P*V: mac_k는 과거 token 위치, mac_col은 현재 head의 출력 채널이다.
    wire [CACHE_ADDR_BITS-1:0] flat_value_read_address =
        (layer_index*MAX_TOKENS+mac_k)*D_MODEL+head_index*HEAD_DIM+mac_col;
    wire signed [15:0] flat_key_read_value;
    wire signed [15:0] flat_value_read_value;
    generate
        if (FLAT_DISTRIBUTED_CACHE != 0) begin : g_flat_distributed_cache
            // ram_style은 합성 의도를 알려 주는 속성이다. 물리 mapping의 성공 증명은 아니다.
            // 각 메모리는 clock당 한 주소만 쓰고 한 주소를 비동기로 읽는다.
            (* ram_style = "distributed" *) reg signed [15:0] key_memory [0:CACHE_WORDS-1];
            (* ram_style = "distributed" *) reg signed [15:0] value_memory [0:CACHE_WORDS-1];
            assign flat_key_read_value = key_memory[flat_key_read_address];
            assign flat_value_read_value = value_memory[flat_value_read_address];

            // K projection의 마지막 내적 항을 더한 바로 그 상승 edge에 q88_result를 저장한다.
            // 기존 FSM의 OP_K 대입과 같은 edge·주소·bias/포화 결과다. RAM은 별도 순수
            // write block으로 표현하여 state/reset 분기 전체가 각 word의 FF 제어로 복제되지
            // 않게 한다. reset_n은 쓰기를 금지할 뿐 메모리 내용 자체를 0으로 덮어쓰지 않는다.
            always @(posedge clk) begin
                if (reset_n && state == S_MAC_RUN && mac_k == op_inner-1 && mac_operation == OP_K)
                    key_memory[flat_cache_write_address] <= q88_result;
            end
            // V도 독립적인 한 쓰기 포트다. OP_K/OP_V는 차례로 실행되므로 각각 해당 결과만 쓴다.
            always @(posedge clk) begin
                if (reset_n && state == S_MAC_RUN && mac_k == op_inner-1 && mac_operation == OP_V)
                    value_memory[flat_cache_write_address] <= q88_result;
            end
            // reset 뒤 과거 비트가 남아 있어도 token_count=0이면 과거 문맥은 유효하지 않다.
            // 새 token의 K/V를 먼저 전 채널에 기록한 뒤 QK/P*V를 수행하며 token_count 이하만
            // 읽는다. 따라서 미작성 word를 attention에 포함하지 않고 재시작 결과도 동일하다.
            // 비동기 read는 현재 MAC operand를 같은 cycle에 공급한다. synchronous BRAM처럼
            // read 대기 state를 추가하지 않으므로 기존 cycle_count/mac_count를 유지한다.
        end else begin : g_legacy_cache_read
            // 기본0에서는 flat 메모리를 생성하지 않는다. 기존 testbench/보드 경로를 보존한다.
            assign flat_key_read_value = 16'sd0;
            assign flat_value_read_value = 16'sd0;
        end
    endgenerate
    // [head][유효 key 위치] 현재 query 점수. 다른 head/과거 query 계산 결과를 덮어쓰지 않게 구분한다.
    reg signed [15:0] score_vec   [0:HEADS-1][0:MAX_TOKENS-1];
    // [head][유효 key 위치] 현재 query 확률 근사. raw 128은 약 0.5, raw 256은 1.0이다.
    reg signed [15:0] prob_vec    [0:HEADS-1][0:MAX_TOKENS-1];

    // 한 번에 한 곱셈 항만 계산하고 64-bit 누산기에 쌓습니다. Q8.8 절삭은
    // dot-product가 모두 끝난 때 적용해 중간 carry를 보존합니다.
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
    // QK 점수와 SCORE_SCALE_Q8 곱을 넓은 폭에 보관하여 다음 >>8/포화에서 부호를 유지한다.
    reg signed [63:0] score_scale_wide;
    // 현재 output column에 대응하는 bias. ENABLE_BIAS=0/QK/context에서는 0이다.
    reg signed [15:0] linear_bias_value;
    // 정규화 결과*학습 gamma의 넓은 곱. >>8 후 16bit 포화하고 beta를 더한다.
    reg signed [63:0] norm_product_wide;
    // gamma scale과 beta shift를 적용한 LayerNorm 최종 16bit 임시 값.
    reg signed [15:0] norm_affine_value;

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

    // 상태 비교기를 지속 배선으로 연결해 IDLE에서만 host의 새 입력을 허용한다.
    assign input_ready = (state == S_IDLE);
    // 계산/결과 대기를 상태 비교로 표시. comb top의 상수 0은 transaction FSM이 없는 비교 표현이다.
    assign busy = (state != S_IDLE);

    // 현재 MAC이 어떤 행렬/vector 내적을 수행하는지 정합니다. 한 query의 QK^T는
    // 과거 token 수(token_count) + 방금 쓴 자기 자신 한 항까지만 계산합니다.
    // 공유 MAC input mux/차원/결과 조합 블록. mac_operation이 Python qmat의 어느 행렬을 실행할지 선택한다.
    // 처음 기본값을 주고 필요한 조건에서 덮어써 latch(이전 값 유지 회로)를 방지한다.
    // 이 블록은 clock을 기다리지 않는다. 깊이가 크면 출력 저장까지 한 clock timing을 넘을 수 있다.
    always @* begin
        op_inner = D_MODEL;
        op_cols = D_MODEL;
        operand_a = 16'sd0;
        operand_b = 16'sd0;
        linear_bias_value = 16'sd0;
        // operation마다 서로 다른 tensor/weight/cache를 읽고 쓰는 mux 선택. Python의 qmat 인자 선택을 물리 배선으로 바꾼다.
        case (mac_operation)
            OP_Q, OP_K, OP_V, OP_WO: begin op_inner = D_MODEL; op_cols = D_MODEL; end
            OP_QK: begin op_inner = HEAD_DIM; op_cols = token_count + 1; end
            OP_CTX: begin op_inner = token_count + 1; op_cols = HEAD_DIM; end
            OP_W1: begin op_inner = D_MODEL; op_cols = D_FF; end
            OP_W2: begin op_inner = D_FF; op_cols = D_MODEL; end
            OP_LM: begin op_inner = D_MODEL; op_cols = VOCAB_SIZE; end
            default: begin op_inner = D_MODEL; op_cols = D_MODEL; end
        endcase

        // operation마다 서로 다른 tensor/weight/cache를 읽고 쓰는 mux 선택. Python의 qmat 인자 선택을 물리 배선으로 바꾼다.
        case (mac_operation)
            OP_Q, OP_K, OP_V: operand_a = x_vec[mac_k];
            OP_QK: operand_a = q_vec[head_index*HEAD_DIM + mac_k];
            OP_CTX: operand_a = prob_vec[head_index][mac_k];
            OP_WO: operand_a = context_vec[mac_k];
            OP_W1: operand_a = norm1_vec[mac_k];
            OP_W2: operand_a = ff1_vec[mac_k];
            OP_LM: operand_a = norm2_vec[mac_k];
            default: operand_a = 16'sd0;
        endcase

        // operation마다 서로 다른 tensor/weight/cache를 읽고 쓰는 mux 선택. Python의 qmat 인자 선택을 물리 배선으로 바꾼다.
        case (mac_operation)
            OP_Q: operand_b = $signed(wq_layers_flat[
                ((layer_index*D_MODEL*D_MODEL + mac_k*D_MODEL + mac_col)*16) +: 16]);
            OP_K: operand_b = $signed(wk_layers_flat[
                ((layer_index*D_MODEL*D_MODEL + mac_k*D_MODEL + mac_col)*16) +: 16]);
            OP_V: operand_b = $signed(wv_layers_flat[
                ((layer_index*D_MODEL*D_MODEL + mac_k*D_MODEL + mac_col)*16) +: 16]);
            OP_QK: begin
                // 두 경로는 같은 [layer][key token][head channel] word를 읽는다.
                if (FLAT_DISTRIBUTED_CACHE != 0) operand_b = flat_key_read_value;
                else operand_b = key_cache[layer_index][mac_col][head_index*HEAD_DIM + mac_k];
            end
            OP_CTX: begin
                if (FLAT_DISTRIBUTED_CACHE != 0) operand_b = flat_value_read_value;
                else operand_b = value_cache[layer_index][mac_k][head_index*HEAD_DIM + mac_col];
            end
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

        // Linear의 bias는 dot product를 Q8.8로 자른 뒤 포화 덧셈한다. 이는
        // PyTorch affine 변환과 같은 경계 순서이며, dot-product 누산기 폭을
        // bias 때문에 늘리지는 않는다.
        // bias는 학습 linear OP_Q/K/V/WO/W1/W2/LM에만 있고 QK/probability*V에는 적용하지 않는다.
        if (ENABLE_BIAS != 0) begin
            // operation마다 서로 다른 tensor/weight/cache를 읽고 쓰는 mux 선택. Python의 qmat 인자 선택을 물리 배선으로 바꾼다.
            case (mac_operation)
                OP_Q: linear_bias_value = $signed(wq_bias_flat[((layer_index*D_MODEL+mac_col)*16) +: 16]);
                OP_K: linear_bias_value = $signed(wk_bias_flat[((layer_index*D_MODEL+mac_col)*16) +: 16]);
                OP_V: linear_bias_value = $signed(wv_bias_flat[((layer_index*D_MODEL+mac_col)*16) +: 16]);
                OP_WO: linear_bias_value = $signed(wo_bias_flat[((layer_index*D_MODEL+mac_col)*16) +: 16]);
                OP_W1: linear_bias_value = $signed(w1_bias_flat[((layer_index*D_FF+mac_col)*16) +: 16]);
                OP_W2: linear_bias_value = $signed(w2_bias_flat[((layer_index*D_MODEL+mac_col)*16) +: 16]);
                OP_LM: linear_bias_value = $signed(lm_bias_flat[mac_col*16 +: 16]);
                default: linear_bias_value = 16'sd0;
            endcase
        end

        // Python term=int(a)*int(b). signed 16bit 곱은 32bit이고 Q8.8*Q8.8=Q16.16 raw다.
        // 누산할 때 중간 항마다 >>8하지 않는다. 전체 내적 마지막에만 자르는 수치 정의를 보존한다.
        product_value = $signed(operand_a) * $signed(operand_b);
        // {{32{product_value[31]}},product_value}는 sign bit를 늘리는 sign extension. 음수 항을 유지한다.
        accumulated_next = mac_acc + {{32{product_value[31]}}, product_value};
        // Python sat16(sum(products)>>8). 소수 8bit 제거 후 포화하여 다음 연산의 Q8.8로 맞춘다.
        q88_result = sat16(accumulated_next >>> 8);
        score_scale_wide = $signed(q88_result) * SCORE_SCALE_Q8;
        if (mac_operation == OP_QK)
            q88_result = sat16(score_scale_wide >>> 8);
        else if (mac_operation != OP_CTX)
            q88_result = sat_add16(q88_result, linear_bias_value);
    end

    // Softmax PU 하나를 각 head의 새 query가 돌아가며 사용합니다. valid mask에는
    // cache의 현재 유효 길이만 표시합니다. 아직 채우지 않은 cache word는 읽지 않습니다.
    // 현재 query/head의 점수 vector를 낮은 word부터 묶은 PU 입력 배선.
    reg [MAX_TOKENS*16-1:0] softmax_input_flat;
    // bit j=1이면 key 위치 j를 attention에 포함. 0이면 padding/미래 정보로 제외한다.
    reg [MAX_TOKENS-1:0] softmax_valid_mask;
    // Softmax PU의 Q8.8 확률 근사 vector. 정수 나눗셈 절삭으로 합이 정확히 256보다 작을 수 있다.
    wire [MAX_TOKENS*16-1:0] softmax_output_flat;
    // 현재 score vector를 packed bit 주소로 연결할 조합 반복 인덱스.
    integer softmax_index;
    // Softmax 입력 packing/valid mask 블록. Python scores/valid를 PU의 packed port로 전달한다.
    // 처음 기본값을 주고 필요한 조건에서 덮어써 latch(이전 값 유지 회로)를 방지한다.
    // 이 블록은 clock을 기다리지 않는다. 깊이가 크면 출력 저장까지 한 clock timing을 넘을 수 있다.
    always @* begin
        softmax_input_flat = {MAX_TOKENS*16{1'b0}};
        softmax_valid_mask = {MAX_TOKENS{1'b0}};
        for (softmax_index = 0; softmax_index < MAX_TOKENS; softmax_index = softmax_index + 1) begin
            softmax_input_flat[softmax_index*16 +: 16] = score_vec[head_index][softmax_index];
            softmax_valid_mask[softmax_index] = (softmax_index <= token_count);
        end
    end
    // head들이 재사용하는 Softmax PU. cache의 채워진 과거 위치와 현재 위치만 유효하다.
    dram_pim_softmax_pu #(.VEC_LEN(MAX_TOKENS)) u_cached_softmax (
        .a_flat(softmax_input_flat), .valid_mask(softmax_valid_mask),
        .y_flat(softmax_output_flat)
    );

    // LayerNorm 역시 한 vector PU를 모든 layer에서 공유합니다. 먼저 residual을
    // register에 저장하고 다음 state에서 PU 출력으로 norm vector를 갱신합니다.
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
                layernorm_input_flat[norm_index*16 +: 16] = resid1_vec[norm_index];
            else if (state == S_NORM2)
                layernorm_input_flat[norm_index*16 +: 16] = resid2_vec[norm_index];
        end
    end
    // layer들이 재사용하는 LayerNorm PU. S_NORM1/2가 첫/두 번째 residual을 선택한다.
    dram_pim_layernorm_pu #(.VEC_LEN(D_MODEL)) u_cached_layernorm (
        .a_flat(layernorm_input_flat), .y_flat(layernorm_output_flat)
    );

    // FFN 활성값은 가중치 곱셈 결과를 register에 쓴 다음 GELU PU가 처리합니다.
    // ReLU 사용 시 ENABLE_GELU=0이므로 이 PU는 결과 경로에서 선택되지 않습니다.
    // W1 선형 출력 ff1_pre_vec를 GELU PU에 연결하는 packed vector.
    reg [D_FF*16-1:0] gelu_input_flat;
    // GELU LUT/보간의 activated FFN vector. W2의 입력으로 저장한다.
    wire [D_FF*16-1:0] gelu_output_flat;
    // GELU vector의 channel packing 인덱스. 모든 원소를 같은 순서로 연결한다.
    integer gelu_index;
    // GELU 입력 packing 블록. W1 저장값을 FFN 활성화 PU에 word 순서대로 연결한다.
    // 처음 기본값을 주고 필요한 조건에서 덮어써 latch(이전 값 유지 회로)를 방지한다.
    // 이 블록은 clock을 기다리지 않는다. 깊이가 크면 출력 저장까지 한 clock timing을 넘을 수 있다.
    always @* begin
        gelu_input_flat = {D_FF*16{1'b0}};
        for (gelu_index = 0; gelu_index < D_FF; gelu_index = gelu_index + 1)
            gelu_input_flat[gelu_index*16 +: 16] = ff1_pre_vec[gelu_index];
    end
    // Q8.8 GELU LUT/보간 PU. ENABLE_GELU=0이면 추론 결과에 이 경로가 선택되지 않는다.
    dram_pim_gelu_pu #(.VEC_LEN(D_FF)) u_cached_gelu (
        .a_flat(gelu_input_flat), .y_flat(gelu_output_flat)
    );

    integer i;
    integer channel;
    // 입력 token ID가 가리킨 현재 channel의 embedding raw 값.
    reg signed [15:0] emb_value;
    // 현재 absolute position의 동일 channel 위치 특징 raw 값.
    reg signed [15:0] pos_value;
    // posedge clk에서 RHS를 이전 register 값으로 계산하고 <= nonblocking으로 동시에 갱신한다.
    // 이 KV core의 reset은 아래 posedge에서만 반영되는 동기식이다. UART/top의 비동기 reset과 구분한다.
    // Python 대입과 달리 <= 새 값은 같은 always의 아래 줄에서 즉시 읽히지 않는다.
    // 그래서 residual 저장/Norm 계산, 마지막 layer 저장/다음 layer 복사를 상태로 나눈다.
    // FPGA 호환성을 위해 이 KV core는 동기식 reset을 사용한다. reset_n=0을
    // 적어도 하나의 상승 에지 동안 유지해야 한다. 여러 배열을 비동기로 초기화하는
    // 원래 비동기 형식에서 나타난 set/reset 경고를 줄이고 reset 계약을 단순하게 한다.
    // 관찰된 Vivado 내부 종료는 동일 소스의 영문 경로 실행에서 해소되어,
    // reset 형식이 내부 종료의 원인이라고 단정하지 않는다.
    // 보드 wrapper는 reset을 여러 clock 유지하고 해제를 동기화한다. 수치 연산은 같다.
    always @(posedge clk) begin
        if (!reset_n) begin
            state <= S_IDLE;
            return_state <= S_IDLE;
            mac_operation <= OP_Q;
            token_id_latched <= {TOKEN_BITS{1'b0}};
            token_count <= 0;
            layer_index <= 0;
            head_index <= 0;
            mac_col <= 0;
            mac_k <= 0;
            mac_acc <= 0;
            done <= 1'b0;
            result_valid <= 1'b0;
            error <= 1'b0;
            cycle_count <= 0;
            mac_count <= 0;
            hidden_flat <= {D_MODEL*16{1'b0}};
            logits_flat <= {VOCAB_SIZE*16{1'b0}};
        end else begin
            done <= 1'b0;
            error <= 1'b0;
            // 전체 busy clock에는 control/PU/복사/결과 대기가 포함될 수 있어 MAC 항수와 cycle 수는 다르다.
            if (state != S_IDLE) cycle_count <= cycle_count + 1'b1;

            // FSM 단계 switch. 이 clock에 어떤 register를 갱신하고 다음 clock은 무엇을 계산할지 결정한다.
            case (state)
                // 요청 대기/수락. 거래의 인덱스와 cycle/MAC 카운터를 초기화하여 이전 제어 상태가 섞이지 않게 한다.
                S_IDLE: begin
                    if (start) begin
                        if (token_count >= MAX_TOKENS || token_id >= VOCAB_SIZE) begin
                            // cache를 넘기거나 어휘에 없는 ID는 계산하지 않고 명시적으로 알린다.
                            error <= 1'b1;
                            done <= 1'b1;
                        end else begin
                            token_id_latched <= token_id;
                            layer_index <= 0;
                            head_index <= 0;
                            cycle_count <= 0;
                            mac_count <= 0;
                            state <= S_EMBED;
                        end
                    end
                end

                // Python state=[sat16(token_embedding[id][ch]+position_embedding[pos][ch]) ...]를 lookup/포화 덧셈으로 수행한다.
                S_EMBED: begin
                    for (channel = 0; channel < D_MODEL; channel = channel + 1) begin
                        emb_value = $signed(token_embedding_flat[
                            ((token_id_latched*D_MODEL + channel)*16) +: 16]);
                        pos_value = $signed(position_embedding_flat[
                            ((token_count*D_MODEL + channel)*16) +: 16]);
                        x_vec[channel] <= sat_add16(emb_value, pos_value);
                    end
                    state <= S_Q_START;
                end

                // MAC 종류를 Q projection으로 정하고 끝나면 K 단계로 돌아오도록 return_state를 설정한다.
                S_Q_START: begin mac_operation <= OP_Q; return_state <= S_K_START; state <= S_MAC_START; end
                // 같은 MAC으로 K projection 수행. KV core는 현재 cache 위치에 써서 다음 token에서 재사용한다.
                S_K_START: begin mac_operation <= OP_K; return_state <= S_V_START; state <= S_MAC_START; end
                // 같은 MAC으로 V projection 수행. Q/K/V는 수학이 같고 weight/결과 저장 위치가 다르다.
                S_V_START: begin
                    mac_operation <= OP_V; return_state <= S_QK_START;
                    head_index <= 0; state <= S_MAC_START;
                end
                // 한 head의 Q와 K 내적 시작. Python scores의 sum(q[dim]*key[dim])에 대응한다.
                S_QK_START: begin mac_operation <= OP_QK; return_state <= S_QK_NEXT; state <= S_MAC_START; end
                // 다음 head로 점수 계산을 넘긴다. 모든 head가 끝나면 Softmax로 가므로 multi-head를 실제 실행한다.
                S_QK_NEXT: begin
                    if (head_index == HEADS-1) begin
                        head_index <= 0; state <= S_SOFTMAX;
                    end else begin
                        head_index <= head_index + 1; state <= S_QK_START;
                    end
                end
                // 유효 과거 점수를 LUT Softmax 확률 근사로 바꾸어 저장. Python softmax_q8(scores,valid)에 대응한다.
                S_SOFTMAX: begin
                    for (i = 0; i < MAX_TOKENS; i = i + 1)
                        prob_vec[head_index][i] <= $signed(softmax_output_flat[i*16 +: 16]);
                    if (head_index == HEADS-1) begin
                        head_index <= 0;
                        state <= S_CTX_START;
                    end else begin
                        head_index <= head_index + 1;
                        state <= S_SOFTMAX_NEXT;
                    end
                end
                // head 주소 갱신 후 조합 PU 입력을 다음 head로 바꾸는 별도 상태. 주소 전환과 저장을 분리한다.
                S_SOFTMAX_NEXT: state <= S_SOFTMAX;
                // probability*V 내적 시작. Python qmat(probabilities,value_head)는 관련성 비중으로 내용을 합친다.
                S_CTX_START: begin mac_operation <= OP_CTX; return_state <= S_CTX_NEXT; state <= S_MAC_START; end
                // 한 head 문맥을 해당 hidden 채널에 저장 후 다음 head로 간다. 모두 완료되어야 Wo로 넘어간다.
                S_CTX_NEXT: begin
                    if (head_index == HEADS-1) begin
                        head_index <= 0; state <= S_WO_START;
                    end else begin
                        head_index <= head_index + 1; state <= S_CTX_START;
                    end
                end
                // 연결한 head context에 Wo를 곱해 여러 head의 정보를 hidden 전체로 섞는다.
                S_WO_START: begin mac_operation <= OP_WO; return_state <= S_RESID1; state <= S_MAC_START; end
                // Python residual1=[sat16(state[ch]+attention[ch]) ...]. 입력과 attention의 첫 포화 residual 덧셈이다.
                S_RESID1: begin
                    for (channel = 0; channel < D_MODEL; channel = channel + 1)
                        resid1_vec[channel] <= sat_add16(x_vec[channel], attn_vec[channel]);
                    state <= S_NORM1;
                end
                // 첫 residual을 LayerNorm하고 지원 설정에 따라 gamma/beta 적용. FFN에 줄 채널 분포를 조절한다.
                S_NORM1: begin
                    for (channel = 0; channel < D_MODEL; channel = channel + 1) begin
                        // Python sat16(sat16((normalized*gamma)>>8)+beta). 곱 뒤 포화/덧셈 뒤 포화 순서를 보존한다.
                        if (ENABLE_NORM_AFFINE != 0) begin
                            norm_product_wide = $signed(layernorm_output_flat[channel*16 +: 16]) *
                                $signed(ln1_gamma_flat[((layer_index*D_MODEL+channel)*16) +: 16]);
                            norm_affine_value = sat16(norm_product_wide >>> 8);
                            norm_affine_value = sat_add16(norm_affine_value,
                                $signed(ln1_beta_flat[((layer_index*D_MODEL+channel)*16) +: 16]));
                            norm1_vec[channel] <= norm_affine_value;
                        end else norm1_vec[channel] <= $signed(layernorm_output_flat[channel*16 +: 16]);
                    end
                    state <= S_W1_START;
                end
                // FFN D_MODEL -> D_FF 확장 내적. 선형 변환 후 ReLU/GELU가 비선형 특징을 추가한다.
                S_W1_START: begin
                    mac_operation <= OP_W1;
                    if (ENABLE_GELU != 0) return_state <= S_GELU_START;
                    else return_state <= S_W2_START;
                    state <= S_MAC_START;
                end
                // W1 ff1_pre_vec가 저장된 뒤 GELU PU가 읽도록 계산 상태로 넘어가는 준비 단계다.
                S_GELU_START: state <= S_GELU;
                // Python [gelu_q8(v) for v in ff1]의 Q8.8 LUT/보간을 FFN 특징에 적용한다.
                S_GELU: begin
                    for (i = 0; i < D_FF; i = i + 1)
                        ff1_vec[i] <= $signed(gelu_output_flat[i*16 +: 16]);
                    state <= S_W2_START;
                end
                // FFN D_FF -> D_MODEL 축소 내적. 활성화한 특징을 residual 덧셈 가능한 원래 폭으로 돌린다.
                S_W2_START: begin mac_operation <= OP_W2; return_state <= S_RESID2; state <= S_MAC_START; end
                // Python residual2=[sat16(norm1[ch]+ff2[ch]) ...]. FFN 출력과 첫 norm 특징을 더한다.
                S_RESID2: begin
                    for (channel = 0; channel < D_MODEL; channel = channel + 1)
                        resid2_vec[channel] <= sat_add16(norm1_vec[channel], ff2_vec[channel]);
                    state <= S_NORM2;
                end
                // 두 번째 post-norm 완료. 마지막 layer이면 LM head, 층이 남으면 다음 layer 입력 복사로 간다.
                S_NORM2: begin
                    for (channel = 0; channel < D_MODEL; channel = channel + 1) begin
                        // Python sat16(sat16((normalized*gamma)>>8)+beta). 곱 뒤 포화/덧셈 뒤 포화 순서를 보존한다.
                        if (ENABLE_NORM_AFFINE != 0) begin
                            norm_product_wide = $signed(layernorm_output_flat[channel*16 +: 16]) *
                                $signed(ln2_gamma_flat[((layer_index*D_MODEL+channel)*16) +: 16]);
                            norm_affine_value = sat16(norm_product_wide >>> 8);
                            norm_affine_value = sat_add16(norm_affine_value,
                                $signed(ln2_beta_flat[((layer_index*D_MODEL+channel)*16) +: 16]));
                            norm2_vec[channel] <= norm_affine_value;
                        end else norm2_vec[channel] <= $signed(layernorm_output_flat[channel*16 +: 16]);
                    end
                    if (layer_index == LAYERS-1) state <= S_LM_START;
                    else state <= S_NEXT_LAYER;
                end
                // norm2를 다음 층 x로 복사하고 layer_index 증가. Python state=layernorm_q8_affine(residual2)다.
                S_NEXT_LAYER: begin
                    for (channel = 0; channel < D_MODEL; channel = channel + 1)
                        x_vec[channel] <= norm2_vec[channel];
                    layer_index <= layer_index + 1;
                    state <= S_Q_START;
                end
                // hidden*[D_MODEL,VOCAB_SIZE] LM head로 후보 점수를 만든다. 다음 ID argmax/sampling은 host 역할이다.
                S_LM_START: begin mac_operation <= OP_LM; return_state <= S_FINISH; state <= S_MAC_START; end

                // row/col/k 및 accumulator를 0으로 맞추어 새 행렬 연산을 시작한다. qmat 중첩 for 시작점이다.
                S_MAC_START: begin
                    mac_col <= 0;
                    mac_k <= 0;
                    mac_acc <= 0;
                    state <= S_MAC_RUN;
                end
                // 한 clock에 a*b 한 항 누산. 마지막 k에서 >>8/포화 후 결과 저장하고 다음 column/row로 진행한다.
                S_MAC_RUN: begin
                    mac_count <= mac_count + 1'b1;
                    // 마지막 항은 accumulated_next에 이미 포함된다. 저장 후 다음 output accumulator를 0으로 시작한다.
                    if (mac_k == op_inner-1) begin
                        // operation마다 서로 다른 tensor/weight/cache를 읽고 쓰는 mux 선택. Python의 qmat 인자 선택을 물리 배선으로 바꾼다.
                        case (mac_operation)
                            OP_Q: q_vec[mac_col] <= q88_result;
                            // flag1은 위의 RAM 전용 always가 같은 edge에 쓴다. 이 FSM에서
                            // 또 쓰면 한 RAM에 두 쓰기 프로세스가 생겨 inference를 방해한다.
                            OP_K: if (FLAT_DISTRIBUTED_CACHE == 0)
                                key_cache[layer_index][token_count][mac_col] <= q88_result;
                            OP_V: if (FLAT_DISTRIBUTED_CACHE == 0)
                                value_cache[layer_index][token_count][mac_col] <= q88_result;
                            OP_QK: score_vec[head_index][mac_col] <= q88_result;
                            OP_CTX: context_vec[head_index*HEAD_DIM + mac_col] <= q88_result;
                            OP_WO: attn_vec[mac_col] <= q88_result;
                            OP_W1: begin
                                ff1_pre_vec[mac_col] <= q88_result;
                                if (ENABLE_GELU == 0)
                                    ff1_vec[mac_col] <= (q88_result < 0) ? 16'sd0 : q88_result;
                            end
                            OP_W2: ff2_vec[mac_col] <= q88_result;
                            OP_LM: logits_flat[mac_col*16 +: 16] <= q88_result;
                            default: begin end
                        endcase
                        mac_acc <= 0;
                        mac_k <= 0;
                        if (mac_col == op_cols-1) begin
                            mac_col <= 0;
                            state <= return_state;
                        end else mac_col <= mac_col + 1;
                    end else begin
                        mac_acc <= accumulated_next;
                        mac_k <= mac_k + 1;
                    end
                end
                // 최종 hidden을 output bus로 복사하고 완료 pulse. KV core는 token_count 증가 후 결과 소비를 기다린다.
                S_FINISH: begin
                    for (channel = 0; channel < D_MODEL; channel = channel + 1)
                        hidden_flat[channel*16 +: 16] <= norm2_vec[channel];
                    token_count <= token_count + 1'b1;
                    done <= 1'b1;
                    result_valid <= 1'b1;
                    state <= S_OUTPUT_WAIT;
                end
                // host가 모든 점수를 읽을 때까지 결과/result_valid 유지. result_ready 후 새 token을 수락한다.
                S_OUTPUT_WAIT: begin
                    // 소비자가 ready를 줄 때까지 계산 결과를 고정해 둡니다.
                    // 따라서 느린 host가 결과를 놓치지 않으며 다음 입력도 받지 않습니다.
                    if (result_ready) begin
                        result_valid <= 1'b0;
                        state <= S_IDLE;
                    end
                end
                default: state <= S_IDLE;
            endcase
        end
    end

    // elaboration/simulation 설정 검사. 양의 차원/head 나눗셈 조건이 깨진 회로는 오류를 알린다.
    // 매 token에서 모델 shape를 검사하는 동적 FPGA 기능은 아니다.
    initial begin
        if (VOCAB_SIZE < 1 || D_MODEL < 1 || D_FF < 1 || LAYERS < 1 || MAX_TOKENS < 1)
            $error("Transformer dimensions must be positive");
        if (HEADS < 1 || (D_MODEL % HEADS) != 0)
            $error("D_MODEL must be divisible by HEADS");
    end
endmodule
