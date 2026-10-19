// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// -----------------------------------------------------------------------------
// Vivado part-target용 token-stream GPT inference top
//
// 현재 검증 환경에서 찾은 Vivado part(xcau25p-ffvb676-2-e)에 RTL을 매핑하기
// 위한 합성 top입니다. 기본 parameter는 학습한 full-ops 모델의 크기와 맞춥니다.
// token/embedding/weight 표는 이 연구 RTL과 같이 외부의 안정된 bus로 입력합니다.
// 즉 이 top은 MAC·PU·cache datapath를 FPGA 자원에 매핑하지만, 직렬 weight loader,
// DDR controller, board pin assignment 또는 제품용 host interface는 포함하지 않습니다.
//
// FPGA top의 clock/reset/token 입력만 남기고 parameter를 고정한 실제 board shell을
// 만들려면 별도의 on-chip memory와 serial configuration protocol이 필요합니다.
// 여기서 거대한 packed input bus를 FPGA package pin에 직접 연결한다는 뜻은 아닙니다.
// Vivado out-of-context flow로 core 자체를 합성·배치·배선해 자원/내부 timing을 확인합니다.
// -----------------------------------------------------------------------------
// [학습용 상세 해설 2026-10-04]
// 위치: part 지정 Vivado에서 원본 KV core의 자원 매핑을 진단하는 parameter wrapper.
// Python 대응: model/gpt_q88.py:forward_q88_step. wrapper는 수학을 추가하지 않는다.
// 기본값은 V=65,D=16,H=4,F=32,L=2,cache=32이며 bias/affine/GELU를 켠 학습 설정이다.
// 전체 weight를 top port로 노출하면 논리 단자가 너무 많아 실제 place가 실패할 수 있다.
// 기존 OOC place/route 성공 증거는 gpt_kvcache_rom_board_top 기준이다.
// 이 파일의 존재 자체가 FPGA board 동작/전체 place 성공의 증거는 아니다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module gpt_kvcache_vivado_top #(
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
    parameter integer ENABLE_BIAS = 1,
    // 1이면 LayerNorm 뒤 gamma/beta를 적용한다. gamma=256,beta=0은 Q8.8 항등 affine이다.
    parameter integer ENABLE_NORM_AFFINE = 1,
    // 1은 GELU LUT/보간, 0은 ReLU max(0,x). 학습 checkpoint activation과 맞춘다.
    parameter integer ENABLE_GELU = 1
) (
    // 클록 입력. 순차 회로는 상승 에지에서 계산 결과를 register에 저장한다. comb wrapper에서는 비교용으로만 남는다.
    input  wire clk,
    // 0일 때 초기화하는 active-low reset. 상태/위치/완료 신호를 시작 값으로 만들고 KV 문맥을 새로 시작한다.
    input  wire reset_n,
    // 계산 요청. 순차 core는 idle에서만 수락하므로 ready/busy 확인 후 한 클록 펄스를 준다.
    input  wire start,
    // 결과 소비 확인. result_valid 이후 모든 logit을 읽은 host가 1을 주어 다음 토큰 수락을 허용한다.
    input  wire result_ready,
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
    // 마지막 decoder의 hidden 특징. raw/256으로 읽으며 개별 채널에 고정된 자연어 단어 뜻이 있지는 않다.
    output wire [D_MODEL*16-1:0] hidden_flat,
    // 다음 어휘 후보별 Q8.8 점수. 확률이 아니며 argmax/sampling으로 고른 ID를 vocab[id]로 문자로 바꾼다.
    output wire [VOCAB_SIZE*16-1:0] logits_flat,
    // 새 입력 수락 가능. 1인 idle에서 start/token_id를 제공한다.
    output wire input_ready,
    // 계산 중 또는 결과 소비 대기 상태. 1이면 새 start를 수락하지 않는다.
    output wire busy,
    // 계산 완료 한 클록 pulse. KV 결과를 지속해서 읽으려면 result_valid도 확인한다.
    output wire done,
    // hidden/logits가 유효함을 유지하는 신호. result_ready handshake까지 데이터가 고정된다.
    output wire result_valid,
    // 잘못된 어휘 ID/꽉 찬 문맥을 거절하는 한 클록 알림. 잘못된 입력을 정상 결과로 오해하지 않게 한다.
    output wire error,
    // 완료한 토큰 수. 다음 입력의 absolute position 및 layer별 KV cache 유효 길이이며 Q8.8 숫자가 아니다.
    output wire [31:0] token_count,
    // 최근 거래의 클록 수. 초 단위 시간=cycle_count*클록 주기다. KV의 output 대기 시간도 늘릴 수 있다.
    output wire [31:0] cycle_count,
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    output wire [31:0] mac_count
);
    // 코어는 layer별 K/V cache, shared MAC, Softmax/LayerNorm 및 선택형 GELU 경로를
    // 포함한 실제 추론 datapath입니다. parameter를 바꾸면 Vivado가 해당 크기로 펼칩니다.
    transformer_gpt_kvcache_seq #(
        .VOCAB_SIZE(VOCAB_SIZE), .D_MODEL(D_MODEL), .HEADS(HEADS),
        .D_FF(D_FF), .LAYERS(LAYERS), .MAX_TOKENS(MAX_TOKENS),
        .TOKEN_BITS(TOKEN_BITS), .SCORE_SCALE_Q8(SCORE_SCALE_Q8),
        .ENABLE_BIAS(ENABLE_BIAS), .ENABLE_NORM_AFFINE(ENABLE_NORM_AFFINE),
        .ENABLE_GELU(ENABLE_GELU)
    // Q/K/V/FFN/LM 연산은 하위 sequential KV core가 수행. shell의 weight/제어를 전달한다.
    ) transformer_core (
        .clk(clk), .reset_n(reset_n), .start(start), .input_ready(input_ready),
        .token_id(token_id), .token_embedding_flat(token_embedding_flat),
        .position_embedding_flat(position_embedding_flat),
        .wq_layers_flat(wq_layers_flat), .wk_layers_flat(wk_layers_flat),
        .wv_layers_flat(wv_layers_flat), .wo_layers_flat(wo_layers_flat),
        .w1_layers_flat(w1_layers_flat), .w2_layers_flat(w2_layers_flat),
        .lm_head_flat(lm_head_flat), .wq_bias_flat(wq_bias_flat),
        .wk_bias_flat(wk_bias_flat), .wv_bias_flat(wv_bias_flat),
        .wo_bias_flat(wo_bias_flat), .w1_bias_flat(w1_bias_flat),
        .w2_bias_flat(w2_bias_flat), .lm_bias_flat(lm_bias_flat),
        .ln1_gamma_flat(ln1_gamma_flat), .ln1_beta_flat(ln1_beta_flat),
        .ln2_gamma_flat(ln2_gamma_flat), .ln2_beta_flat(ln2_beta_flat),
        .result_ready(result_ready), .hidden_flat(hidden_flat),
        .logits_flat(logits_flat), .busy(busy), .done(done),
        .result_valid(result_valid), .error(error), .token_count(token_count),
        .cycle_count(cycle_count), .mac_count(mac_count)
    );
endmodule
