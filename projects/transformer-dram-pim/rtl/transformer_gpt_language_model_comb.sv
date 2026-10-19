// [내부 신호 읽기 안내]
`timescale 1ns/1ps
// -----------------------------------------------------------------------------
// 토큰 ID에서 GPT next-token logits까지 계산하는 end-to-end RTL top
//
// 이 모듈은 소프트웨어 tokenizer가 만든 token ID를 받아 learned token embedding과
// learned absolute position embedding을 더한다. hidden vector가 multi-head·multi-layer
// decoder stack을 지나면, vocabulary projection이 각 위치의 다음 토큰 점수를 낸다.
// 따라서 text generation을 하기 위해 필요한 logits까지 SystemVerilog 경로로 잇는다.
//
// 토크나이저, sampling(top-k/top-p/temperature), 반복적인 KV-cache 기반 1-token
// decoding은 host software 기능으로 남긴다. 현재 RTL은 주어진 context 전체를 매번
// 계산하는 기능 모델이라 KV-cache cycle-accurate 성능을 주장하지 않는다.
// Embedding 및 weight bus는 Q8.8이며, 입력 표는 외부에서 학습한/양자화한 값을 준다.
// LM head와 token embedding을 같은 가중치로 연결하면 표준적인 weight tying이 된다.
// -----------------------------------------------------------------------------
// [학습용 상세 해설 2026-10-04]
// 위치: token ID -> embedding+position -> 여러 head/layer -> vocabulary logits 전체 경로.
// Python 대응: model/gpt_language_model_reference.py:language_model_logits의
// embedded, decoder_stack(embedded), qmat(hidden,lm_head). 일반 학습 모델은 gpt_q88:forward_q88다.
// 소형 테스트의 bias 없는 ReLU 모델이다. logits는 확률이 아닌 다음 문자 후보 점수다.
// host가 마지막 위치 argmax/sampling ID를 골라 vocab[id]로 문자로 바꾸고 다음 입력을 만든다.
// 거래마다 전체 context를 계산하며 이전 거래 K/V를 보존하는 KV-cache core와 다르다.
// 숫자 공통 규칙: signed Q8.8은 raw integer/256이다. raw 256=1.0, raw -128=-0.5.
// _flat bus는 표를 row-major로 묶는다. 원소 [r][c]는 [(r*columns+c)*16 +: 16]이고
// word 0이 최하위 [15:0]이다. layer 축은 layer*matrix_words를 앞에 더한다.
// SystemVerilog는 병렬 gate/register 연결을 기술한다. assign은 지속 조합 배선,
// always @*는 입력 변화에 반응하는 조합 회로, posedge always는 clock 저장 회로다.
// 조합/generate for가 여러 회로를 펼칠 수 있으므로 Python 반복의 CPU 실행과 구분한다.
// reg 문법 자체가 FF를 뜻하지 않는다. clock always의 저장은 FF, 모든 경로에 값을
// 주는 조합 always는 조합 신호다. function도 합성되면 연산 배선이 된다.
module transformer_gpt_language_model_comb #(
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
    // token t의 ID는 [t*TOKEN_BITS +: TOKEN_BITS]. Python token_ids[t]를 낮은 token 순서부터 묶는다.
    input wire [TOKENS*TOKEN_BITS-1:0] token_ids_flat,
    // [어휘 ID][hidden 채널] 학습 표. Python weights['token_embedding'][token_id][channel]을 row-major로 묶는다.
    input wire [VOCAB_SIZE*D_MODEL*16-1:0] token_embedding_flat,
    // [위치][hidden 채널] 학습 표. 순서를 나타내기 위해 embedding에 더하는 weights['position_embedding'][position][channel]이다.
    input wire [TOKENS*D_MODEL*16-1:0] position_embedding_flat,
    // [layer][입력 채널][출력 채널] Query 가중치. layer 0 원소가 낮은 bit에 놓이며 Python layer['wq'] 방향이다.
    input wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wq_layers_flat,
    // [layer][입력 채널][출력 채널] Key 가중치. 층마다 다른 학습 행렬로 검색 대상 특징을 만든다.
    input wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wk_layers_flat,
    // [layer][입력 채널][출력 채널] Value 가중치. 현재 층의 입력 hidden에서 꺼낼 내용을 만든다.
    input wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wv_layers_flat,
    // [layer][D_MODEL][D_MODEL] 출력 투영. head별 context를 연결한 뒤 전체 특징으로 섞는다.
    input wire [LAYERS*D_MODEL*D_MODEL*16-1:0] wo_layers_flat,
    // [layer][D_MODEL][D_FF] FFN 확장 행렬. Python layer['w1']와 row-major 방향이 같다.
    input wire [LAYERS*D_MODEL*D_FF*16-1:0] w1_layers_flat,
    // [layer][D_FF][D_MODEL] FFN 축소 행렬. Python layer['w2']와 row-major 방향이 같다.
    input wire [LAYERS*D_FF*D_MODEL*16-1:0] w2_layers_flat,
    // [hidden 채널][어휘 ID] 출력 행렬. 마지막 hidden을 다음 문자 후보별 logit 점수로 바꾼다.
    input wire [D_MODEL*VOCAB_SIZE*16-1:0] lm_head_flat,
    // embedding+position 중간 결과 [토큰][채널]. 문자열 ID가 처음 숫자 특징으로 변한 위치를 확인하는 출력이다.
    output reg [TOKENS*D_MODEL*16-1:0] embedding_sum_flat,
    // 마지막 decoder의 hidden 특징. raw/256으로 읽으며 개별 채널에 고정된 자연어 단어 뜻이 있지는 않다.
    output wire [TOKENS*D_MODEL*16-1:0] hidden_flat,
    // 다음 어휘 후보별 Q8.8 점수. 확률이 아니며 argmax/sampling으로 고른 ID를 vocab[id]로 문자로 바꾼다.
    output wire [TOKENS*VOCAB_SIZE*16-1:0] logits_flat,
    // 미융합 CPU 비교 가정의 경계 이동 단어 수. word=16bit=2byte이며 실측 DRAM 트래픽은 아니다.
    output wire [31:0] cpu_boundary_words,
    // 중간값을 메모리 가까이 유지한다는 PIM 비교 가정의 경계 이동 단어 수. 실제 칩 계측값은 아니다.
    output wire [31:0] pim_boundary_words,
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    output wire [31:0] mac_count,
    // Softmax/Residual/Norm/활성화의 vector 단계 수. 개별 산술 덧셈 개수와 다르다.
    output wire [31:0] nonvmm_vector_ops
);
    // Python 대응: model/reference.py 또는 model/gpt_q88.py:sat16 = max(-32768,min(32767,value)).
    // 범위 밖 숫자가 16비트에서 반대 부호로 뒤집히는 wrap-around를 막는 saturation(포화) 함수다.
    // raw -32768..32767은 /256하면 -128..127.99609375이다. 소수 비트 >>8 이동은 호출부가 수행한다.
    // automatic은 임시 지역값이 독립적인 SV 함수 선언이며 CPU가 Python 함수를 실행하는 회로는 아니다.
    function automatic signed [15:0] sat16(input signed [32:0] value);
        begin
            if (value > 33'sd32767) sat16 = 16'sd32767;
            else if (value < -33'sd32768) sat16 = -16'sd32768;
            else sat16 = value[15:0];
        end
    endfunction

    // 현재 embedding/Softmax/Norm 대상 token 위치. 한 vector PU를 여러 token에 재사용하는 주소다.
    integer token_index;
    integer channel_index;
    // packed ID에서 풀어낸 어휘 정수 주소. raw Q8.8로 해석하지 않는다.
    integer token_number;
    // 조합 embedding lookup의 현재 token/channel raw 값.
    reg signed [15:0] token_value;
    // 조합 position lookup의 현재 token 위치/channel raw 값.
    reg signed [15:0] position_value;
    // embedding/LM head 포함 전 decoder의 CPU 경계 이동 가정.
    wire [31:0] decoder_cpu_words;
    // decoder 내부 PIM 경계 이동 가정. top은 최종 token-to-logit 경계로 별도 계산한다.
    wire [31:0] decoder_pim_words;
    // decoder 층들의 MAC 항수. top에서는 LM head T*D*V를 추가한다.
    wire [31:0] decoder_macs;
    // decoder 층들의 non-VMM 단계 수. top은 embedding/position 덧셈을 추가한다.
    wire [31:0] decoder_pu_ops;

    // Python embedded[t][ch]=sat16(token_embedding[id][ch]+position_embedding[t][ch])의
    // 조합 lookup/덧셈이다. invalid ID는 이 검증 core에서 0 벡터이며 기본값은 latch를 방지한다.
    always @* begin
        embedding_sum_flat = {TOKENS*D_MODEL*16{1'b0}};
        token_number = 0;
        token_value = 0;
        position_value = 0;
        for (token_index = 0; token_index < TOKENS; token_index = token_index + 1) begin
            token_number = token_ids_flat[token_index*TOKEN_BITS +: TOKEN_BITS];
            for (channel_index = 0; channel_index < D_MODEL; channel_index = channel_index + 1) begin
                if (token_number < VOCAB_SIZE) begin
                    token_value = $signed(token_embedding_flat[(token_number*D_MODEL+channel_index)*16 +: 16]);
                    position_value = $signed(position_embedding_flat[(token_index*D_MODEL+channel_index)*16 +: 16]);
                    embedding_sum_flat[(token_index*D_MODEL+channel_index)*16 +: 16] =
                        sat16($signed(token_value) + $signed(position_value));
                end
            end
        end
    end

    transformer_gpt_decoder_stack_comb #(
        .TOKENS(TOKENS), .D_MODEL(D_MODEL), .HEADS(HEADS),
        .D_FF(D_FF), .LAYERS(LAYERS), .SCORE_SCALE_Q8(SCORE_SCALE_Q8)
    // Python hidden=decoder_stack(embedded). embedding 뒤 여러 층의 실제 직렬 연결.
    ) u_decoder_stack (
        .x_flat(embedding_sum_flat),
        .wq_layers_flat(wq_layers_flat), .wk_layers_flat(wk_layers_flat),
        .wv_layers_flat(wv_layers_flat), .wo_layers_flat(wo_layers_flat),
        .w1_layers_flat(w1_layers_flat), .w2_layers_flat(w2_layers_flat),
        .y_flat(hidden_flat), .cpu_boundary_words(decoder_cpu_words),
        .pim_boundary_words(decoder_pim_words), .mac_count(decoder_macs),
        .nonvmm_vector_ops(decoder_pu_ops)
    );

    // Language-model head: 마지막 hidden state [T,D]에 학습된 [D,V] 가중치를 곱해
    // 위치마다 어휘 전체의 점수 [T,V]를 출력한다. logits에 Softmax를 씌우는 것은
    // sampling 소프트웨어가 맡으며, argmax로 다음 토큰을 고를 수도 있다.
    // Python qmat(hidden,lm_head). 내부 hidden을 어휘 후보 logit으로 바꾸며 output 확률 변환은 host가 맡는다.
    dram_pim_vmm_bank #(.ROWS(TOKENS), .K(D_MODEL), .COLS(VOCAB_SIZE)) u_lm_head (
        .activation_flat(hidden_flat), .weight_flat(lm_head_flat), .result_flat(logits_flat)
    );

    // 최상위 통계는 token/position embedding과 vocabulary head도 포함한다. 한 word는
    // 16비트이다. PIM 쪽은 token ID를 받고 logits만 내보내며 embedding table과 중간
    // activation은 메모리 가까이에 상주한다고 가정한다. 가중치 최초 적재는 여전히
    // 별도 항목이며 이 간단한 카운터에는 포함하지 않는다.
    // 미융합 CPU 비교 가정의 경계 이동 단어 수. word=16bit=2byte이며 실측 DRAM 트래픽은 아니다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign cpu_boundary_words = decoder_cpu_words +
        3*TOKENS*D_MODEL + TOKENS*D_MODEL + D_MODEL*VOCAB_SIZE + TOKENS*VOCAB_SIZE;
    // 중간값을 메모리 가까이 유지한다는 PIM 비교 가정의 경계 이동 단어 수. 실제 칩 계측값은 아니다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign pim_boundary_words = ((TOKENS*TOKEN_BITS + 15) / 16) + TOKENS*VOCAB_SIZE;
    // a*b를 누산한 MAC 항수/수식. FLOPS 또는 처리 시간으로 직접 해석하지 않는다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign mac_count = decoder_macs + TOKENS*D_MODEL*VOCAB_SIZE;
    // Softmax/Residual/Norm/활성화의 vector 단계 수. 개별 산술 덧셈 개수와 다르다.
    // 고정 parameter 수식은 상수로 합성된다. 현재 DRAM 신호를 계측하는 동적 counter가 아니다.
    assign nonvmm_vector_ops = decoder_pu_ops + TOKENS; // token/position embedding residual add
endmodule
