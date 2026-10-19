// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// -----------------------------------------------------------------------------
// 학습 완료 Q8.8 가중치를 포함한 좁은 입출력 FPGA 합성 shell
//
// 이 top은 검증한 full-ops checkpoint(V=65, D=16, H=4, FF=32, layer=2)를
// 고정 구성으로 사용합니다. 가중치는 FPGA 구성 시 함께 합성되는 초기화 이미지로
// 제공하고, 외부에는 token 입력과 결과 logit 읽기만 노출합니다. 따라서 앞선
// 진단 top처럼 수십만 weight bit를 package pin으로 빼지 않습니다.
//
// gpt_q88_rom_flat은 $readmemh로 각 Q8.8 단어를 읽은 뒤 모든 단어를 평탄화된
// 상수 bus에 연결합니다. 현재 코어가 matrix 전체 bus를 받아 내부 주소로 고르기
// 때문입니다. 이는 합성 가능한 저장/배선 shell이지, 동작 중 외부 DRAM을 읽는
// controller나 실제 DRAM-PIM 칩의 구현이 아닙니다. K/V cache도 현 코어 구조상
// FPGA register bank로 매핑될 수 있으며, Vivado 보고서에서 확인합니다.
//
// 인터페이스: start를 1 cycle 올리면 token_id를 입력합니다. logit_index를 바꾸어
// result_valid가 유지되는 동안 0..64의 logit을 한 단어씩 읽습니다. 읽기를 마친
// 뒤 result_ready를 1 cycle 올려 다음 token을 받을 수 있습니다.
// -----------------------------------------------------------------------------
// [학습용 상세 해설 2026-10-04]
// 위치: full-ops 학습 checkpoint를 합성 구성 이미지에 고정한 좁은 제어/logit shell.
// Python 대응: model/gpt_q88.py:write_mem_files의 표를 ROM adapter가 읽고
// forward_q88_step 연산은 하위 transformer_core가 수행한다.
// 문자 -> Python vocab lookup -> token_id/start -> KV core -> result_valid ->
// logit_index 0..64 읽기 -> host argmax -> vocab[id] -> 다음 문자를 다시 입력하는 흐름이다.
// board_top 이름은 UART/clock/pin 제약 완료라는 증거가 아니다. 기존 검증은 xcau25p
// OOC 배선이고 10ns timing은 미달이다. Nexys 4 DDR는 다른 part/제약을 사용한다.
// 전체 ROM word를 상수 bus로 펼치며 BRAM 주소 port가 아니다. 합성시 상수/배선이
// 될 수 있고 이 shell은 보드 외장 DDR를 읽는 controller를 포함하지 않는다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module gpt_kvcache_rom_board_top #(
    // 학습 context32 이하에서 cache 길이만 줄일 수 있다. head/layer/weight는 같다.
    // Nexys용8은 짧은 prompt의 동일 연산을 적은 register/Softmax 회로로 구현한다.
    parameter integer MAX_TOKENS = 32,
    // 1이면 하위 core의 K/V를 flat single-write/asynchronous-read distributed RAM으로
    // 표현한다. 학습 checkpoint/정수 수식/거래 cycle은 동일하며 기본0은 기존 저장 경로다.
    parameter integer FLAT_DISTRIBUTED_CACHE = 0
) (
    // 클록 입력. 순차 회로는 상승 에지에서 계산 결과를 register에 저장한다. comb wrapper에서는 비교용으로만 남는다.
    input  wire       clk,
    // 0일 때 초기화하는 active-low reset. 상태/위치/완료 신호를 시작 값으로 만들고 KV 문맥을 새로 시작한다.
    input  wire       reset_n,
    // 계산 요청. 순차 core는 idle에서만 수락하므로 ready/busy 확인 후 한 클록 펄스를 준다.
    input  wire       start,
    // 결과 소비 확인. result_valid 이후 모든 logit을 읽은 host가 1을 주어 다음 토큰 수락을 허용한다.
    input  wire       result_ready,
    // 문자 자체가 아닌 어휘표 정수 번호. Python encode[char]로 만든 ID이고 Q8.8 실수가 아니다.
    input  wire [6:0] token_id,
    // 현재 읽을 출력 어휘 번호 0..64. token_id는 입력 번호이고 이 신호는 출력 점수 주소다.
    input  wire [6:0] logit_index,
    // 새 입력 수락 가능. 1인 idle에서 start/token_id를 제공한다.
    output wire       input_ready,
    // 계산 중 또는 결과 소비 대기 상태. 1이면 새 start를 수락하지 않는다.
    output wire       busy,
    // 계산 완료 한 클록 pulse. KV 결과를 지속해서 읽으려면 result_valid도 확인한다.
    output wire       done,
    // hidden/logits가 유효함을 유지하는 신호. result_ready handshake까지 데이터가 고정된다.
    output wire       result_valid,
    // 잘못된 어휘 ID/꽉 찬 문맥을 거절하는 한 클록 알림. 잘못된 입력을 정상 결과로 오해하지 않게 한다.
    output wire       error,
    // 완료한 토큰 수. 다음 입력의 absolute position 및 layer별 KV cache 유효 길이이며 Q8.8 숫자가 아니다.
    output wire [5:0] token_count,
    // 선택 후보의 signed Q8.8 raw 점수. host는 부호 변환 후 /256으로 읽으며 잘못된 index는 0을 반환한다.
    output wire [15:0] logit_data
);
    // 어휘 후보 수 V. V=65는 logit 65개를 뜻하며 65개 지식을 학습했다는 뜻이 아니다.
    localparam integer VOCAB_SIZE = 65;
    // 토큰마다 hidden 숫자 수 D. embedding/residual 폭이며 모든 head 채널 수 합이 D다.
    localparam integer D_MODEL = 16;
    // attention 관점 수 H. head_dim=D_MODEL/HEADS이며 서로 다른 채널로 독립 점수/확률을 만든다.
    localparam integer HEADS = 4;
    // FFN 중간 채널 수 F. W1=D*F, W2=F*D이고 폭을 키우면 연산/저장 비용도 커진다.
    localparam integer D_FF = 32;
    // decoder block 반복 층 수 L. 앞 층 출력이 다음 층 입력이며 층마다 별도 weight다.
    localparam integer LAYERS = 2;
    // KV cache 최대 길이. 0..MAX_TOKENS-1 위치를 쓰며 꽉 차면 새 창의 reset/prefill이 필요하다.
    // ID 비트 폭. V=65일 때 7비트(0..127)를 표현하지만 유효 번호는 0..64다.
    localparam integer TOKEN_BITS = 7;

    // 각 메모리 출력은 단어 0이 가장 낮은 비트에 놓입니다. 코어의 주소 계산도
    // 이 row-major 순서(Q8.8 원소 1개 = 16-bit 한 단어)를 기준으로 합니다.
    // [어휘 ID][hidden 채널] 학습 표. Python weights['token_embedding'][token_id][channel]을 row-major로 묶는다.
    wire [VOCAB_SIZE*D_MODEL*16-1:0] token_embedding_flat;
    // [위치][hidden 채널] 학습 표. 순서를 나타내기 위해 embedding에 더하는 weights['position_embedding'][position][channel]이다.
    wire [MAX_TOKENS*D_MODEL*16-1:0] position_embedding_flat;
    wire [32*D_MODEL*16-1:0] checkpoint_position_embedding_full;
    // checkpoint 파일의32개 위치를 항상 모두 읽고, 이 core가 허용한 초기위치만 연결한다.
    // .mem 파일을 잘라 새 가중치를 만들지 않으며 position0..MAX_TOKENS-1 값은 동일하다.
    assign position_embedding_flat = checkpoint_position_embedding_full[MAX_TOKENS*D_MODEL*16-1:0];
    // [hidden 채널][어휘 ID] 출력 행렬. 마지막 hidden을 다음 문자 후보별 logit 점수로 바꾼다.
    wire [D_MODEL*VOCAB_SIZE*16-1:0] lm_head_flat;
    // [어휘 ID] LM head bias. Python weights.get('lm_bias')이며 문자 후보 점수 각각에 더한다.
    wire [VOCAB_SIZE*16-1:0] lm_bias_flat;
    // [layer][입력 채널][출력 채널] Query 가중치. layer 0 원소가 낮은 bit에 놓이며 Python layer['wq'] 방향이다.
    wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wq_layers_flat;
    // [layer][입력 채널][출력 채널] Key 가중치. 층마다 다른 학습 행렬로 검색 대상 특징을 만든다.
    wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wk_layers_flat;
    // [layer][입력 채널][출력 채널] Value 가중치. 현재 층의 입력 hidden에서 꺼낼 내용을 만든다.
    wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wv_layers_flat;
    // [layer][D_MODEL][D_MODEL] 출력 투영. head별 context를 연결한 뒤 전체 특징으로 섞는다.
    wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wo_layers_flat;
    // [layer][D_MODEL][D_FF] FFN 확장 행렬. Python layer['w1']와 row-major 방향이 같다.
    wire [LAYERS*D_MODEL*D_FF*16-1:0] w1_layers_flat;
    // [layer][D_FF][D_MODEL] FFN 축소 행렬. Python layer['w2']와 row-major 방향이 같다.
    wire [LAYERS*D_FF*D_MODEL*16-1:0] w2_layers_flat;
    // [layer][D_MODEL] Q linear bias. 내적 >>8/포화 후 더하는 Python layer.get('bq')이다.
    wire [LAYERS*D_MODEL*16-1:0] wq_bias_flat;
    // [layer][D_MODEL] K linear bias. ENABLE_BIAS=1일 때 선택하며 Python layer.get('bk')와 같다.
    wire [LAYERS*D_MODEL*16-1:0] wk_bias_flat;
    // [layer][D_MODEL] V linear bias. Python qmat_bias([state],layer['wv'],layer.get('bv'))의 bv다.
    wire [LAYERS*D_MODEL*16-1:0] wv_bias_flat;
    // [layer][D_MODEL] attention output bias. Python layer.get('bo')와 같다.
    wire [LAYERS*D_MODEL*16-1:0] wo_bias_flat;
    // [layer][D_FF] FFN 확장 bias. 길이는 D_MODEL이 아니라 확장 폭 D_FF다.
    wire [LAYERS*D_FF*16-1:0] w1_bias_flat;
    // [layer][D_MODEL] FFN 축소 bias. Python layer.get('b2')를 linear 포화 후 더한다.
    wire [LAYERS*D_MODEL*16-1:0] w2_bias_flat;
    // [layer][D_MODEL] 첫 LayerNorm 학습 scale gamma. Q8.8 256=배율 1.0이다.
    wire [LAYERS*D_MODEL*16-1:0] ln1_gamma_flat;
    // [layer][D_MODEL] 첫 LayerNorm 학습 이동량 beta. gamma 곱셈 >>8/포화 후 더한다.
    wire [LAYERS*D_MODEL*16-1:0] ln1_beta_flat;
    // [layer][D_MODEL] 두 번째 LayerNorm gamma. Python layernorm_q8_affine(...,ln2_gamma,...)이다.
    wire [LAYERS*D_MODEL*16-1:0] ln2_gamma_flat;
    // [layer][D_MODEL] 두 번째 LayerNorm beta. ENABLE_NORM_AFFINE=0이면 gamma/beta를 쓰지 않는다.
    wire [LAYERS*D_MODEL*16-1:0] ln2_beta_flat;

    // 임베딩과 language-model head는 모든 layer가 공유하는 checkpoint tensor입니다.
    // 학습 tensor token_embedding의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(VOCAB_SIZE*D_MODEL), .INIT_FILE("weights/token_embedding.mem"))
        rom_token_embedding (.data_flat(token_embedding_flat));
    // 학습 tensor position_embedding의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(32*D_MODEL), .INIT_FILE("weights/position_embedding.mem"))
        rom_position_embedding (.data_flat(checkpoint_position_embedding_full));
    // 학습 tensor lm_head의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL*VOCAB_SIZE), .INIT_FILE("weights/lm_head.mem"))
        rom_lm_head (.data_flat(lm_head_flat));
    // 학습 tensor lm_bias의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(VOCAB_SIZE), .INIT_FILE("weights/lm_bias.mem"))
        rom_lm_bias (.data_flat(lm_bias_flat));

    // layer 0 원소가 각 bus의 하위 주소가 되도록 {layer1, layer0} 순으로 묶습니다.
    // 이는 core의 layer_index*matrix_words + row*columns + column 주소와 일치합니다.
    wire [D_MODEL*D_MODEL*16-1:0] wq0, wq1, wk0, wk1, wv0, wv1, wo0, wo1;
    wire [D_MODEL*D_FF*16-1:0] w10;
    wire [D_MODEL*D_FF*16-1:0] w11;
    wire [D_FF*D_MODEL*16-1:0] w20;
    wire [D_FF*D_MODEL*16-1:0] w21;
    // 학습 tensor layer_0_wq의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL*D_MODEL), .INIT_FILE("weights/layer_0_wq.mem")) rom_wq0 (.data_flat(wq0));
    // 학습 tensor layer_1_wq의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL*D_MODEL), .INIT_FILE("weights/layer_1_wq.mem")) rom_wq1 (.data_flat(wq1));
    // 학습 tensor layer_0_wk의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL*D_MODEL), .INIT_FILE("weights/layer_0_wk.mem")) rom_wk0 (.data_flat(wk0));
    // 학습 tensor layer_1_wk의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL*D_MODEL), .INIT_FILE("weights/layer_1_wk.mem")) rom_wk1 (.data_flat(wk1));
    // 학습 tensor layer_0_wv의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL*D_MODEL), .INIT_FILE("weights/layer_0_wv.mem")) rom_wv0 (.data_flat(wv0));
    // 학습 tensor layer_1_wv의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL*D_MODEL), .INIT_FILE("weights/layer_1_wv.mem")) rom_wv1 (.data_flat(wv1));
    // 학습 tensor layer_0_wo의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL*D_MODEL), .INIT_FILE("weights/layer_0_wo.mem")) rom_wo0 (.data_flat(wo0));
    // 학습 tensor layer_1_wo의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL*D_MODEL), .INIT_FILE("weights/layer_1_wo.mem")) rom_wo1 (.data_flat(wo1));
    // 학습 tensor layer_0_w1의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL*D_FF), .INIT_FILE("weights/layer_0_w1.mem")) rom_w10 (.data_flat(w10));
    // 학습 tensor layer_1_w1의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL*D_FF), .INIT_FILE("weights/layer_1_w1.mem")) rom_w11 (.data_flat(w11));
    // 학습 tensor layer_0_w2의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_FF*D_MODEL), .INIT_FILE("weights/layer_0_w2.mem")) rom_w20 (.data_flat(w20));
    // 학습 tensor layer_1_w2의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_FF*D_MODEL), .INIT_FILE("weights/layer_1_w2.mem")) rom_w21 (.data_flat(w21));
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign wq_layers_flat = {wq1, wq0};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign wk_layers_flat = {wk1, wk0};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign wv_layers_flat = {wv1, wv0};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign wo_layers_flat = {wo1, wo0};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign w1_layers_flat = {w11, w10};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign w2_layers_flat = {w21, w20};

    // 학습 시 활성화했던 linear bias와 LayerNorm affine 계수도 각 layer별로 내장합니다.
    wire [D_MODEL*16-1:0] bq0, bq1, bk0, bk1, bv0, bv1, bo0, bo1, b20, b21;
    wire [D_FF*16-1:0] b10, b11;
    wire [D_MODEL*16-1:0] ln1g0, ln1g1, ln1b0, ln1b1, ln2g0, ln2g1, ln2b0, ln2b1;
    // 학습 tensor layer_0_bq의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_0_bq.mem")) rom_bq0 (.data_flat(bq0));
    // 학습 tensor layer_1_bq의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_1_bq.mem")) rom_bq1 (.data_flat(bq1));
    // 학습 tensor layer_0_bk의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_0_bk.mem")) rom_bk0 (.data_flat(bk0));
    // 학습 tensor layer_1_bk의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_1_bk.mem")) rom_bk1 (.data_flat(bk1));
    // 학습 tensor layer_0_bv의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_0_bv.mem")) rom_bv0 (.data_flat(bv0));
    // 학습 tensor layer_1_bv의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_1_bv.mem")) rom_bv1 (.data_flat(bv1));
    // 학습 tensor layer_0_bo의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_0_bo.mem")) rom_bo0 (.data_flat(bo0));
    // 학습 tensor layer_1_bo의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_1_bo.mem")) rom_bo1 (.data_flat(bo1));
    // 학습 tensor layer_0_b1의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_FF), .INIT_FILE("weights/layer_0_b1.mem")) rom_b10 (.data_flat(b10));
    // 학습 tensor layer_1_b1의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_FF), .INIT_FILE("weights/layer_1_b1.mem")) rom_b11 (.data_flat(b11));
    // 학습 tensor layer_0_b2의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_0_b2.mem")) rom_b20 (.data_flat(b20));
    // 학습 tensor layer_1_b2의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_1_b2.mem")) rom_b21 (.data_flat(b21));
    // 학습 tensor layer_0_ln1_gamma의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_0_ln1_gamma.mem")) rom_ln1g0 (.data_flat(ln1g0));
    // 학습 tensor layer_1_ln1_gamma의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_1_ln1_gamma.mem")) rom_ln1g1 (.data_flat(ln1g1));
    // 학습 tensor layer_0_ln1_beta의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_0_ln1_beta.mem")) rom_ln1b0 (.data_flat(ln1b0));
    // 학습 tensor layer_1_ln1_beta의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_1_ln1_beta.mem")) rom_ln1b1 (.data_flat(ln1b1));
    // 학습 tensor layer_0_ln2_gamma의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_0_ln2_gamma.mem")) rom_ln2g0 (.data_flat(ln2g0));
    // 학습 tensor layer_1_ln2_gamma의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_1_ln2_gamma.mem")) rom_ln2g1 (.data_flat(ln2g1));
    // 학습 tensor layer_0_ln2_beta의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_0_ln2_beta.mem")) rom_ln2b0 (.data_flat(ln2b0));
    // 학습 tensor layer_1_ln2_beta의 raw Q8.8 이미지를 읽는 ROM adapter. Python checkpoint의 같은 이름 표에서 export했다.
    gpt_q88_rom_flat #(.WORDS(D_MODEL), .INIT_FILE("weights/layer_1_ln2_beta.mem")) rom_ln2b1 (.data_flat(ln2b1));
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign wq_bias_flat = {bq1, bq0};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign wk_bias_flat = {bk1, bk0};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign wv_bias_flat = {bv1, bv0};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign wo_bias_flat = {bo1, bo0};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign w1_bias_flat = {b11, b10};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign w2_bias_flat = {b21, b20};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign ln1_gamma_flat = {ln1g1, ln1g0};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign ln1_beta_flat = {ln1b1, ln1b0};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign ln2_gamma_flat = {ln2g1, ln2g0};
    // {layer1,layer0} 오른쪽 layer0가 낮은 bit에 놓여 Python layer 순서/core 주소 계산과 일치한다.
    assign ln2_beta_flat = {ln2b1, ln2b0};

    // 마지막 decoder의 hidden 특징. raw/256으로 읽으며 개별 채널에 고정된 자연어 단어 뜻이 있지는 않다.
    wire [D_MODEL*16-1:0] hidden_flat;
    // 다음 어휘 후보별 Q8.8 점수. 확률이 아니며 argmax/sampling으로 고른 ID를 vocab[id]로 문자로 바꾼다.
    wire [VOCAB_SIZE*16-1:0] logits_flat;
    // 하위 core의 32bit 완료 token 수. shell 외부에는 작은 model 범위에 충분한 하위 6bit를 연결한다.
    wire [31:0] token_count_full, cycle_count, mac_count;

    // full-ops 설정은 학습 checkpoint의 정의와 맞춥니다: bias, affine LayerNorm,
    // GELU 활성화를 모두 켠 4-head, 2-layer GPT-style decoder입니다.
    transformer_gpt_kvcache_seq #(
        .VOCAB_SIZE(VOCAB_SIZE), .D_MODEL(D_MODEL), .HEADS(HEADS),
        .D_FF(D_FF), .LAYERS(LAYERS), .MAX_TOKENS(MAX_TOKENS),
        .TOKEN_BITS(TOKEN_BITS), .SCORE_SCALE_Q8(128),
        .ENABLE_BIAS(1), .ENABLE_NORM_AFFINE(1), .ENABLE_GELU(1),
        .FLAT_DISTRIBUTED_CACHE(FLAT_DISTRIBUTED_CACHE)
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
        .result_valid(result_valid), .error(error), .token_count(token_count_full),
        .cycle_count(cycle_count), .mac_count(mac_count)
    );

    // 이 작은 read mux로 vocab 65개의 logit을 한 번에 내보낼 필요를 없앱니다.
    // 유효하지 않은 index는 X를 전파하지 않고 0을 반환해 보드 디버깅을 단순하게 합니다.
    assign token_count = token_count_full[5:0];
    // 주소로 후보 score 하나를 고르는 조합 mux. 읽는 순서가 값 자체를 바꾸지는 않는다.
    assign logit_data = (logit_index < VOCAB_SIZE)
        ? logits_flat[logit_index*16 +: 16] : 16'sd0;
endmodule

// Q8.8 초기화 파일을 읽어 matrix row-major 순서의 packed bus를 제공하는 합성 ROM
// 이미지입니다. 주소 핀을 가진 별도 RAM이 아니라, 현재 가중치 입력 bus 인터페이스에
// 맞춰 상수 tensor를 고정하는 adapter입니다. readmemh 파일들은 Vivado 실행 시
// 작업 디렉터리 아래 weights/에 두어야 합니다.
// [학습용 상세 해설 2026-10-04]
// 위치: weight 이미지 -> 고정 packed bus adapter. 추론 알고리즘을 실행하는 함수는 아니다.
// Python 대응: model/gpt_q88.py:write_mem_files 내부 flatten/value & 0xffff 출력 규칙.
// 예: raw -256은 .mem에서 ff00, $signed(16'hff00)는 -256이며 /256하면 -1.0이다.
// initial $readmemh는 합성 도구가 구성 이미지 초기값을 읽는 기술 방식이다. FPGA가
// 전원 켜짐 후 운영체제 파일 경로를 열어 Python 파일을 읽는 동작이 아니다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module gpt_q88_rom_flat #(
    // ROM 이미지 16비트 원소 수. matrix=rows*columns, vector=길이만큼이다.
    parameter integer WORDS = 1,
    // 실행 작업 폴더 기준 .mem 경로. Python write_mem_files의 16진수 이미지를 구성 초기값에 포함한다.
    parameter INIT_FILE = ""
) (
    // INIT_FILE의 row-major Q8.8 상수 word bus. word 0은 [15:0]이며 주소형 RAM 포트가 아니다.
    output wire [WORDS*16-1:0] data_flat
);
    // INIT_FILE에서 읽은 16bit raw word 배열. 전체 bus에 고정 연결하므로 주소형 BRAM read port와 다르다.
    reg [15:0] words [0:WORDS-1];

    // $readmemh 각 줄은 signed Q8.8 한 단어의 raw 16-bit 16진수입니다.
    // 비트 패턴을 변환하지 않으므로 Python checkpoint와 RTL의 부호/scale이 같습니다.
    // .mem의 16진수 bit pattern을 words에 넣어 simulation/구성 초기값 이미지로 반영한다.
    // FPGA 동작 중 운영체제 파일을 읽는 프로세스가 아니라 합성 도구의 초기화 정보다.
    initial begin
        $readmemh(INIT_FILE, words);
    end

    // 단어 번호를 bus bit 위치로 고정 연결합니다. core는 낮은 주소가 낮은 bit에서
    // 시작하는 indexed part-select를 쓰므로 여기서도 word 0을 최하위 16-bit로 둡니다.
    // word i -> bit i*16의 고정 연결. Python flatten()[i]와 같은 row-major 순서이며 word 0이 최하위다.
    for (genvar word_index = 0; word_index < WORDS; word_index = word_index + 1) begin : g_flatten_words
        assign data_flat[word_index*16 +: 16] = words[word_index];
    end
endmodule
