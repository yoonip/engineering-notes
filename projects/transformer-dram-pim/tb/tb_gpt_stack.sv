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
// Multi-head·multi-layer GPT decoder core의 자체검증 테스트벤치.
// 이 bench는 weight bus를 직접 채우고, Python 정수 기준 모델과 결과를 비교한다.
// [테스트벤치 읽기] 이 파일은 FPGA에 내려갈 회로가 아니라 RTL 시뮬레이터를 구동하는 검사 프로그램입니다.
// Python run_tests.py가 iverilog로컴파일한 뒤 vvp로실행하고 출력값을 Python 정수 기준과비교합니다.
// initial은 시뮬레이션 0시점에한번실행합니다. #1은 1 ns 시뮬레이션대기이고물리딜레이소자가아닙니다.
// @(posedge/negedge clk)는시뮬레이션에서해당 edge까지기다립니다. always #5는 10 ns 테스트 클록을만듭니다.
// 이클록에서시뮬레이션통과해도 FPGA 배선 지연은별도로모델링되지 않으므로 Vivado timing 통과를뜻하지 않습니다.
// ===/!==는 0/1뿐아니라 X(미정)/Z(고임피던스)도비교해미초기화신호를검출합니다.
// $fatal은 실패하면즉시종료하는 assert 역할,$display/$write는 자동검증이읽는텍스트출력입니다.
// 정답출력이존재한다는확인과학습언어모델의문장 품질은다른검증입니다.이 bench는 기능/제어/산술규칙을 확인합니다.
module tb_gpt_stack;
    // T3,D4,H2,F8,L2,V8는 합성데모가아닌빠른 fixture입니다.HEAD_DIM=2,scale181은 round(256/sqrt(2)).
    // 3 bit token ID는 0~7을 표현하며 V8가 모든 ID에의미를부여합니다.
    localparam integer T = 3;
    localparam integer D = 4;
    localparam integer H = 2;
    localparam integer F = 8;
    localparam integer L = 2;
    localparam integer SCALE = 181;
    localparam integer V = 8;
    localparam integer TOKEN_BITS = 3;

    // 순차형 core는 하나의 MAC/PU를 여러 clock에 걸쳐 재사용한다.
    reg clk;
    reg reset_n;
    reg start;
    wire seq_busy;
    wire seq_done;
    wire [T*D*16-1:0] seq_embedding_sum_flat;
    wire [T*D*16-1:0] seq_hidden_flat;
    wire [T*V*16-1:0] seq_logits_flat;
    wire [31:0] seq_cycles;
    wire [31:0] seq_macs;

    // 새 token만 받아 과거 layer별 K/V를 보존하는 순차 streaming core.
    reg kvcache_reset_n;
    reg kvcache_start;
    reg kvcache_result_ready;
    reg [TOKEN_BITS-1:0] kvcache_token_id;
    wire [D*16-1:0] kvcache_hidden_flat;
    wire [V*16-1:0] kvcache_logits_flat;
    wire kvcache_input_ready, kvcache_busy, kvcache_done, kvcache_result_valid, kvcache_error;
    wire [31:0] kvcache_token_count, kvcache_cycles, kvcache_macs;

    // multi-layer weight bus는[layer,row,col]의 row-major 순서. bias와 gamma/beta bus도공급하지만
    // 이 fixture의 cache enable값기본 0이므로 full-ops affine/GELU 검증은별도 trained-checkpoint 경로가합니다.
    reg [T*D*16-1:0] x_flat;
    reg [L*D*D*16-1:0] wq_layers_flat;
    reg [L*D*D*16-1:0] wk_layers_flat;
    reg [L*D*D*16-1:0] wv_layers_flat;
    reg [L*D*D*16-1:0] wo_layers_flat;
    reg [L*D*F*16-1:0] w1_layers_flat;
    reg [L*F*D*16-1:0] w2_layers_flat;
    reg [L*D*16-1:0] wq_bias_flat, wk_bias_flat, wv_bias_flat, wo_bias_flat, w2_bias_flat;
    reg [L*F*16-1:0] w1_bias_flat;
    reg [V*16-1:0] lm_bias_flat;
    reg [L*D*16-1:0] ln1_gamma_flat, ln1_beta_flat, ln2_gamma_flat, ln2_beta_flat;
    wire [T*D*16-1:0] y_flat;
    wire [31:0] cpu_words;
    wire [31:0] pim_words;
    wire [31:0] macs;
    wire [31:0] pu_ops;
    reg [T*TOKEN_BITS-1:0] token_ids_flat;
    reg [V*D*16-1:0] token_embedding_flat;
    reg [T*D*16-1:0] position_embedding_flat;
    reg [D*V*16-1:0] lm_head_flat;
    wire [T*D*16-1:0] embedding_sum_flat;
    wire [T*D*16-1:0] language_hidden_flat;
    wire [T*V*16-1:0] logits_flat;
    wire [31:0] language_cpu_words;
    wire [31:0] language_pim_words;
    wire [31:0] language_macs;
    wire [31:0] language_pu_ops;

    reg [T*D*16-1:0] first_y;
    integer l;
    integer r;
    integer c;
    integer value;
    integer token;
    integer channel;
    integer seq_wait_cycles;
    integer vocab_index;
    integer first_seq_cycles;
    integer kvcache_wait_cycles;
    reg signed [15:0] held_logit;

    // 직접 hidden을 입력받는조합 2layer/2head DUT. Python gpt_core_reference.decoder_stack 기준입니다.
    transformer_gpt_decoder_stack_comb #(
        .TOKENS(T), .D_MODEL(D), .HEADS(H), .D_FF(F), .LAYERS(L),
        .SCORE_SCALE_Q8(SCALE)
    ) dut (
        .x_flat(x_flat),
        .wq_layers_flat(wq_layers_flat), .wk_layers_flat(wk_layers_flat),
        .wv_layers_flat(wv_layers_flat), .wo_layers_flat(wo_layers_flat),
        .w1_layers_flat(w1_layers_flat), .w2_layers_flat(w2_layers_flat),
        .y_flat(y_flat), .cpu_boundary_words(cpu_words),
        .pim_boundary_words(pim_words), .mac_count(macs),
        .nonvmm_vector_ops(pu_ops)
    );

    // Token ID -> learned token/position embeddings -> 2-layer decoder -> vocabulary logits.
    transformer_gpt_language_model_comb #(
        .TOKENS(T), .VOCAB_SIZE(V), .D_MODEL(D), .HEADS(H), .D_FF(F),
        .LAYERS(L), .SCORE_SCALE_Q8(SCALE), .TOKEN_BITS(TOKEN_BITS)
    ) language_model (
        .token_ids_flat(token_ids_flat),
        .token_embedding_flat(token_embedding_flat),
        .position_embedding_flat(position_embedding_flat),
        .wq_layers_flat(wq_layers_flat), .wk_layers_flat(wk_layers_flat),
        .wv_layers_flat(wv_layers_flat), .wo_layers_flat(wo_layers_flat),
        .w1_layers_flat(w1_layers_flat), .w2_layers_flat(w2_layers_flat),
        .lm_head_flat(lm_head_flat), .embedding_sum_flat(embedding_sum_flat),
        .hidden_flat(language_hidden_flat), .logits_flat(logits_flat),
        .cpu_boundary_words(language_cpu_words), .pim_boundary_words(language_pim_words),
        .mac_count(language_macs), .nonvmm_vector_ops(language_pu_ops)
    );

    // embedding→전체 context→LM head를 여러클록에공유 MAC으로 계산하는 DUT.
    // 같은토큰을넣는조합 language_model과 bit 단위로결과가동일해야합니다.
    transformer_gpt_language_model_seq #(
        .TOKENS(T), .VOCAB_SIZE(V), .D_MODEL(D), .HEADS(H), .D_FF(F),
        .LAYERS(L), .SCORE_SCALE_Q8(SCALE), .TOKEN_BITS(TOKEN_BITS)
    ) sequential_language_model (
        .clk(clk), .reset_n(reset_n), .start(start),
        .token_ids_flat(token_ids_flat),
        .token_embedding_flat(token_embedding_flat),
        .position_embedding_flat(position_embedding_flat),
        .wq_layers_flat(wq_layers_flat), .wk_layers_flat(wk_layers_flat),
        .wv_layers_flat(wv_layers_flat), .wo_layers_flat(wo_layers_flat),
        .w1_layers_flat(w1_layers_flat), .w2_layers_flat(w2_layers_flat),
        .lm_head_flat(lm_head_flat), .embedding_sum_flat(seq_embedding_sum_flat),
        .hidden_flat(seq_hidden_flat), .logits_flat(seq_logits_flat),
        .busy(seq_busy), .done(seq_done), .cycle_count(seq_cycles), .mac_count(seq_macs)
    );

    // 각 layer의 과거 K/V를 저장하고새 token만처리하는 DUT. Python gpt_q88.forward_q88_step에 대응합니다.
    // result_ready는 느린소비자를모사하고 error는 context 초과를 검증합니다.
    transformer_gpt_kvcache_seq #(
        .VOCAB_SIZE(V), .D_MODEL(D), .HEADS(H), .D_FF(F), .LAYERS(L),
        .MAX_TOKENS(T), .TOKEN_BITS(TOKEN_BITS), .SCORE_SCALE_Q8(SCALE)
    ) streaming_kvcache_model (
        .clk(clk), .reset_n(kvcache_reset_n), .start(kvcache_start),
        .result_ready(kvcache_result_ready), .input_ready(kvcache_input_ready),
        .token_id(kvcache_token_id),
        .token_embedding_flat(token_embedding_flat),
        .position_embedding_flat(position_embedding_flat),
        .wq_layers_flat(wq_layers_flat), .wk_layers_flat(wk_layers_flat),
        .wv_layers_flat(wv_layers_flat), .wo_layers_flat(wo_layers_flat),
        .w1_layers_flat(w1_layers_flat), .w2_layers_flat(w2_layers_flat),
        .wq_bias_flat(wq_bias_flat), .wk_bias_flat(wk_bias_flat),
        .wv_bias_flat(wv_bias_flat), .wo_bias_flat(wo_bias_flat),
        .w1_bias_flat(w1_bias_flat), .w2_bias_flat(w2_bias_flat),
        .lm_bias_flat(lm_bias_flat), .ln1_gamma_flat(ln1_gamma_flat),
        .ln1_beta_flat(ln1_beta_flat), .ln2_gamma_flat(ln2_gamma_flat),
        .ln2_beta_flat(ln2_beta_flat),
        .lm_head_flat(lm_head_flat), .hidden_flat(kvcache_hidden_flat),
        .logits_flat(kvcache_logits_flat), .busy(kvcache_busy),
        .done(kvcache_done), .result_valid(kvcache_result_valid),
        .error(kvcache_error), .token_count(kvcache_token_count),
        .cycle_count(kvcache_cycles), .mac_count(kvcache_macs)
    );

    // 10 ns 테스트 클록.순차연산의실제완료 clock 수를세지만 FPGA 물리 배선 지연은포함하지 않습니다.
    always #5 clk = ~clk;

    // 모든제어/가중치 bus 초기화 후 fixture 생성.랜덤실행마다다른 값이아니라수식으로정한값이므로
    // Python sample_weights/sample_tables와 완전히동일한데이터를재생할 수 있습니다.
    initial begin
        clk = 1'b0;
        reset_n = 1'b0;
        start = 1'b0;
        kvcache_reset_n = 1'b0;
        kvcache_start = 1'b0;
        kvcache_result_ready = 1'b1;
        kvcache_token_id = 0;
        x_flat = {T*D*16{1'b0}};
        wq_layers_flat = {L*D*D*16{1'b0}};
        wk_layers_flat = {L*D*D*16{1'b0}};
        wv_layers_flat = {L*D*D*16{1'b0}};
        wo_layers_flat = {L*D*D*16{1'b0}};
        w1_layers_flat = {L*D*F*16{1'b0}};
        w2_layers_flat = {L*F*D*16{1'b0}};
        wq_bias_flat = {L*D*16{1'b0}};
        wk_bias_flat = {L*D*16{1'b0}};
        wv_bias_flat = {L*D*16{1'b0}};
        wo_bias_flat = {L*D*16{1'b0}};
        w1_bias_flat = {L*F*16{1'b0}};
        w2_bias_flat = {L*D*16{1'b0}};
        lm_bias_flat = {V*16{1'b0}};
        ln1_gamma_flat = {L*D*16{1'b0}};
        ln1_beta_flat = {L*D*16{1'b0}};
        ln2_gamma_flat = {L*D*16{1'b0}};
        ln2_beta_flat = {L*D*16{1'b0}};
        token_ids_flat = {T*TOKEN_BITS{1'b0}};
        token_embedding_flat = {V*D*16{1'b0}};
        position_embedding_flat = {T*D*16{1'b0}};
        lm_head_flat = {D*V*16{1'b0}};
        // 교육용 ID열은[1,4,2]. 여기 V8 fixture는 실제 65문자 vocabulary의 문장 prompt와 다릅니다.
        token_ids_flat[0*TOKEN_BITS +: TOKEN_BITS] = 3'd1;
        token_ids_flat[1*TOKEN_BITS +: TOKEN_BITS] = 3'd4;
        token_ids_flat[2*TOKEN_BITS +: TOKEN_BITS] = 3'd2;

        for (r = 0; r < V; r = r + 1)
            for (c = 0; c < D; c = c + 1)
                token_embedding_flat[(r*D+c)*16 +: 16] = ((r*7+c*11) % 65) - 32;
        for (r = 0; r < T; r = r + 1)
            for (c = 0; c < D; c = c + 1)
                position_embedding_flat[(r*D+c)*16 +: 16] = ((r*5+c*3) % 21) - 10;
        for (r = 0; r < D; r = r + 1)
            for (c = 0; c < V; c = c + 1)
                lm_head_flat[(r*V+c)*16 +: 16] = ((r*3+c*7) % 31) - 15;

        // Layer마다 값이 다른 행렬을 공급한다. 모든 head와 layer가 같은 identity
        // weight를 공유하는 trivial 검증이 되지 않도록 작은 signed 교차항을 넣는다.
        for (l = 0; l < L; l = l + 1) begin
            for (r = 0; r < D; r = r + 1) begin
                ln1_gamma_flat[(l*D+r)*16 +:16] = 16'sd256;
                ln2_gamma_flat[(l*D+r)*16 +:16] = 16'sd256;
                for (c = 0; c < D; c = c + 1) begin
                    if (r == c) value = 240 + 4*l;
                    else value = ((r*13 + c*7 + l*3) % 17) - 8;
                    wq_layers_flat[((l*D*D+r*D+c)*16) +: 16] = value;

                    if (r == c) value = 200 - 3*l;
                    else value = ((r*5 + c*11 + l*2) % 13) - 6;
                    wk_layers_flat[((l*D*D+r*D+c)*16) +: 16] = value;

                    if (r == c) value = 256;
                    else value = ((r*7 + c*3 + l) % 11) - 5;
                    wv_layers_flat[((l*D*D+r*D+c)*16) +: 16] = value;

                    if (r == c) value = 224 + 2*l;
                    else value = ((r*9 + c*2 + l*5) % 15) - 7;
                    wo_layers_flat[((l*D*D+r*D+c)*16) +: 16] = value;
                end
                for (c = 0; c < F; c = c + 1) begin
                    if (r == c) value = 256;
                    else value = ((r*7 + c*5 + l) % 9) - 4;
                    w1_layers_flat[((l*D*F+r*F+c)*16) +: 16] = value;
                end
            end
            for (r = 0; r < F; r = r + 1) begin
                for (c = 0; c < D; c = c + 1) begin
                    if (r == c) value = 256;
                    else value = ((r*3 + c*11 + l) % 7) - 3;
                    w2_layers_flat[((l*F*D+r*D+c)*16) +: 16] = value;
                end
            end
        end

        x_flat[(0*D+0)*16 +: 16] = 16'sd64;
        x_flat[(0*D+1)*16 +: 16] = -16'sd32;
        x_flat[(0*D+2)*16 +: 16] = 16'sd96;
        x_flat[(0*D+3)*16 +: 16] = 16'sd128;
        x_flat[(1*D+0)*16 +: 16] = 16'sd128;
        x_flat[(1*D+1)*16 +: 16] = 16'sd64;
        x_flat[(1*D+2)*16 +: 16] = -16'sd64;
        x_flat[(1*D+3)*16 +: 16] = 16'sd32;
        x_flat[(2*D+0)*16 +: 16] = -16'sd32;
        x_flat[(2*D+1)*16 +: 16] = 16'sd128;
        x_flat[(2*D+2)*16 +: 16] = 16'sd64;
        x_flat[(2*D+3)*16 +: 16] = -16'sd64;

        #10;
        // 미정값을먼저검사해 RTL이 아예계산하지 않은경우를숫자오차와구분합니다.
        if ((^y_flat) === 1'bx) $fatal(1, "multi-head stack produced X/Z");
        if ((^logits_flat) === 1'bx) $fatal(1, "language model logits contain X/Z");
        // decoder 2layer의 activation 경계 모델 840→24 words,MAC912,비 VMM 벡터 42를 검사합니다.
        // 각 head Softmax의 vector 수를 더했으므로 single-head fixture보다 PU counter 해석이다릅니다.
        if (cpu_words !== 32'd840 || pim_words !== 32'd24 ||
            macs !== 32'd912 || pu_ops !== 32'd42)
            $fatal(1, "stack work counters incorrect cpu=%0d pim=%0d mac=%0d pu=%0d",
                   cpu_words, pim_words, macs, pu_ops);
        first_y = y_flat;

        // causal mask 확인: 마지막(미래) 토큰을 바꾸어도 앞선 토큰 두 개의 출력은
        // 두 decoder layer를 모두 통과한 뒤에도 바뀌지 않아야 한다.
        x_flat[(2*D+0)*16 +: 16] = 16'sd300;
        x_flat[(2*D+1)*16 +: 16] = -16'sd250;
        x_flat[(2*D+2)*16 +: 16] = 16'sd420;
        x_flat[(2*D+3)*16 +: 16] = -16'sd350;
        #10;
        for (token = 0; token < T-1; token = token + 1)
            for (channel = 0; channel < D; channel = channel + 1)
                if (first_y[(token*D+channel)*16 +: 16] !==
                    y_flat[(token*D+channel)*16 +: 16])
                    $fatal(1, "future token leaked to token=%0d channel=%0d", token, channel);

        if (language_cpu_words !== 32'd944 || language_pim_words !== 32'd25 ||
            language_macs !== 32'd1008 || language_pu_ops !== 32'd45)
            $fatal(1, "end-to-end GPT work counters incorrect cpu=%0d pim=%0d mac=%0d pu=%0d",
                   language_cpu_words, language_pim_words, language_macs, language_pu_ops);

        // OUTPUT은 decoder hidden4개,LOGITS는 각 위치별 vocab 8 개점수입니다.
        // 최종 검증 Python은 stdout를 parse해별도 reference와 비교합니다. 모든비교가이 bench 안에 있지는않습니다.
        for (token = 0; token < T; token = token + 1) begin
            $write("OUTPUT token=%0d", token);
            for (channel = 0; channel < D; channel = channel + 1)
                $write(" %0d", $signed(first_y[(token*D+channel)*16 +: 16]));
            $write("\n");
        end
        for (token = 0; token < T; token = token + 1) begin
            $write("LOGITS token=%0d", token);
            for (channel = 0; channel < V; channel = channel + 1)
                $write(" %0d", $signed(logits_flat[(token*V+channel)*16 +: 16]));
            $write("\n");
        end
        $display("RESULT gpt_layers=%0d heads=%0d cpu_words=%0d pim_words=%0d macs=%0d pu_ops=%0d",
                 L, H, cpu_words, pim_words, macs, pu_ops);
        $display("RESULT end_to_end_gpt_vocab=%0d cpu_words=%0d pim_words=%0d macs=%0d pu_ops=%0d",
                 V, language_cpu_words, language_pim_words, language_macs, language_pu_ops);

        // 동일한 packed 입력으로 순차 core를 실행한다. 기준 comb top과 모든 logits가
        // 같아야 하며, 실제 수행한 곱셈 항의 수가 MAC workload 식과 맞아야 한다.
        // 이하실제 seq DUT가 동작하도록 reset 해제.앞부분조합 DUT는 클록과무관하게출력을이미 계산했습니다.
        @(negedge clk); reset_n = 1'b1; kvcache_reset_n = 1'b1;
        @(negedge clk); start = 1'b1;
        @(negedge clk); start = 1'b0;
        seq_wait_cycles = 0;
        while ((seq_done !== 1'b1) && (seq_wait_cycles < 100000)) begin
            @(negedge clk);
            seq_wait_cycles = seq_wait_cycles + 1;
        end
        if (seq_done !== 1'b1)
            $fatal(1, "sequential Transformer timeout, state=%0d cycles=%0d",
                   sequential_language_model.state, seq_cycles);
        if (seq_busy !== 1'b0)
            $fatal(1, "sequential Transformer reported busy after done");
        if (seq_macs !== language_macs)
            $fatal(1, "sequential MAC count mismatch: sequential=%0d expected=%0d",
                   seq_macs, language_macs);
        // 두 번째거래와 latency를 비교할 snapshot.동일 입력은결과/연산수/완료 clock도같아야합니다.
        first_seq_cycles = seq_cycles;
        for (token = 0; token < T; token = token + 1)
            for (vocab_index = 0; vocab_index < V; vocab_index = vocab_index + 1)
                if (seq_logits_flat[(token*V+vocab_index)*16 +: 16] !==
                    logits_flat[(token*V+vocab_index)*16 +: 16])
                    $fatal(1, "sequential logits differ token=%0d vocab=%0d seq=%0d comb=%0d",
                           token, vocab_index,
                           $signed(seq_logits_flat[(token*V+vocab_index)*16 +: 16]),
                           $signed(logits_flat[(token*V+vocab_index)*16 +: 16]));
        for (token = 0; token < T; token = token + 1)
            for (channel = 0; channel < D; channel = channel + 1)
                if (seq_hidden_flat[(token*D+channel)*16 +: 16] !==
                    language_hidden_flat[(token*D+channel)*16 +: 16])
                    $fatal(1, "sequential hidden state differs token=%0d channel=%0d", token, channel);

        // 동일 core를 reset 없이 다시 호출해 2 회차에도 stale intermediate 값이 섞이지
        // 않는지 확인한다. start는 매 transaction마다 한 cycle pulse로 전달한다.
        @(negedge clk); start = 1'b1;
        @(negedge clk); start = 1'b0;
        seq_wait_cycles = 0;
        while ((seq_done !== 1'b1) && (seq_wait_cycles < 100000)) begin
            @(negedge clk);
            seq_wait_cycles = seq_wait_cycles + 1;
        end
        if (seq_done !== 1'b1)
            $fatal(1, "sequential Transformer second transaction timeout");
        if (seq_cycles !== first_seq_cycles || seq_macs !== language_macs)
            $fatal(1, "second transaction counters changed cycles=%0d macs=%0d",
                   seq_cycles, seq_macs);
        for (token = 0; token < T; token = token + 1)
            for (vocab_index = 0; vocab_index < V; vocab_index = vocab_index + 1)
                if (seq_logits_flat[(token*V+vocab_index)*16 +: 16] !==
                    logits_flat[(token*V+vocab_index)*16 +: 16])
                    $fatal(1, "second transaction retained stale logits");

        // Stream core 동작 중 active-low 동기식 reset을 상승 클록에 걸쳐 유지하면 연산을 취소하고
        // count를 0으로 되돌려야 한다. 아래 코드는 두 falling edge 사이에 reset을 유지하므로
        // 중간의 rising edge에서 core가 초기화된다. 다음 normal input이 stale state/cache 없이
        // 처음 token부터 시작하는지도 뒤의 전체 stream 비교가 확인한다.
        @(negedge clk); kvcache_token_id = token_ids_flat[0 +: TOKEN_BITS]; kvcache_start = 1'b1;
        @(negedge clk); kvcache_start = 1'b0;
        repeat (3) @(negedge clk);
        if (kvcache_busy !== 1'b1)
            $fatal(1, "KV-cache core did not enter a busy state before reset test");
        kvcache_reset_n = 1'b0;
        @(negedge clk);
        if (kvcache_busy !== 1'b0 || kvcache_token_count !== 0 || kvcache_done !== 1'b0)
            $fatal(1, "KV-cache asynchronous reset did not cancel and clear the stream state");
        kvcache_reset_n = 1'b1;
        @(negedge clk);

        // 느린 consumer를 흉내 내 result_ready를 낮게 유지한다. 결과가 준비되면
        // valid와 출력이 고정되고 busy가 유지되어야 하며, ready가 돌아온 뒤에만
        // 다음 입력을 받는 idle 상태로 복귀한다.
        kvcache_result_ready = 1'b0;
        @(negedge clk); kvcache_token_id = token_ids_flat[0 +: TOKEN_BITS]; kvcache_start = 1'b1;
        @(negedge clk); kvcache_start = 1'b0;
        kvcache_wait_cycles = 0;
        while ((kvcache_done !== 1'b1) && (kvcache_wait_cycles < 10000)) begin
            @(negedge clk); kvcache_wait_cycles = kvcache_wait_cycles + 1;
        end
        if (kvcache_done !== 1'b1 || kvcache_result_valid !== 1'b1)
            $fatal(1, "KV-cache result did not assert done/valid for backpressure test");
        // ready=0 동안출력값이 안바뀌는지첫 logit을 snapshot으로 확인합니다.
        // 검증은 handshake 유지의대표원소이며전체 word의 보존검증은별도 generated verification에도 있습니다.
        held_logit = $signed(kvcache_logits_flat[0 +: 16]);
        repeat (3) begin
            @(negedge clk);
            if (kvcache_busy !== 1'b1 || kvcache_result_valid !== 1'b1 ||
                $signed(kvcache_logits_flat[0 +: 16]) !== held_logit)
                $fatal(1, "KV-cache result was not held stable under backpressure");
        end
        kvcache_result_ready = 1'b1;
        kvcache_wait_cycles = 0;
        while ((kvcache_input_ready !== 1'b1) && (kvcache_wait_cycles < 5)) begin
            @(negedge clk); kvcache_wait_cycles = kvcache_wait_cycles + 1;
        end
        if (kvcache_input_ready !== 1'b1 || kvcache_result_valid !== 1'b0)
            $fatal(1, "KV-cache did not return to input-ready after result handshake");
        kvcache_reset_n = 1'b0;
        @(negedge clk); kvcache_reset_n = 1'b1;
        @(negedge clk);

        $display("RESULT sequential cycles=%0d macs=%0d", seq_cycles, seq_macs);

        // Stream core에 prompt token을 하나씩 보낸다. 각 token 완료 후 현재 위치의
        // logits가 전체 context 기준 Python 결과와 같아야 한다. 이때 과거 K/V는
        // RTL cache에 남고, 이전 token의 Q/K/V projection을 다시 수행하지 않는다.
        for (token = 0; token < T; token = token + 1) begin
            @(negedge clk);
            kvcache_token_id = token_ids_flat[token*TOKEN_BITS +: TOKEN_BITS];
            kvcache_start = 1'b1;
            @(negedge clk); kvcache_start = 1'b0;
            kvcache_wait_cycles = 0;
            while ((kvcache_done !== 1'b1) && (kvcache_wait_cycles < 10000)) begin
                @(negedge clk); kvcache_wait_cycles = kvcache_wait_cycles + 1;
            end
            if (kvcache_done !== 1'b1 || kvcache_error !== 1'b0)
                $fatal(1, "KV-cache stream timeout/error token=%0d", token);
            if (kvcache_token_count !== token+1)
                $fatal(1, "KV-cache token count mismatch token=%0d count=%0d", token, kvcache_token_count);
            // 완료한새 token의 vocab logits만출력합니다.과거위치 logits 전체가아닌한행 V개값입니다.
            // run_tests.py가 해당 token 위치의 Python 전체 context 결과와각 raw 값을 비교합니다.
            $write("KCACHE_LOGITS token=%0d", token);
            for (vocab_index = 0; vocab_index < V; vocab_index = vocab_index + 1)
                $write(" %0d", $signed(kvcache_logits_flat[vocab_index*16 +: 16]));
            $write("\n");
        end
        kvcache_wait_cycles = 0;
        while ((kvcache_input_ready !== 1'b1) && (kvcache_wait_cycles < 5)) begin
            @(negedge clk); kvcache_wait_cycles = kvcache_wait_cycles + 1;
        end
        if (kvcache_busy !== 1'b0 || kvcache_result_valid !== 1'b0 ||
            kvcache_token_count !== T || kvcache_input_ready !== 1'b1)
            $fatal(1, "KV-cache stream completion state is incorrect");

        // cache가 꽉 차면 메모리 밖에 쓰지 않고 명시적인 error/done을 돌려준다.
        @(negedge clk); kvcache_token_id = 0; kvcache_start = 1'b1;
        @(negedge clk); kvcache_start = 1'b0;
        if (kvcache_done !== 1'b1 || kvcache_error !== 1'b1 || kvcache_token_count !== T)
            $fatal(1, "KV-cache full condition did not reject an extra token");

        $display("RESULT kvcache tokens=%0d last_step_cycles=%0d last_step_macs=%0d", T, kvcache_cycles, kvcache_macs);
        $display("PASS: GPT embeddings, multi-head attention, multi-layer chain, LM logits, causal isolation, shared-MAC core, and true layer-wise KV-cache streaming");
        $finish;
    end
endmodule
