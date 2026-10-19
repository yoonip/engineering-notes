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

// [테스트벤치 읽기] 이 파일은 FPGA에 내려갈 회로가 아니라 RTL 시뮬레이터를 구동하는 검사 프로그램입니다.
// Python run_tests.py가 iverilog로컴파일한 뒤 vvp로실행하고 출력값을 Python 정수 기준과비교합니다.
// initial은 시뮬레이션 0시점에한번실행합니다. #1은 1 ns 시뮬레이션대기이고물리딜레이소자가아닙니다.
// @(posedge/negedge clk)는시뮬레이션에서해당 edge까지기다립니다. always #5는 10 ns 테스트 클록을만듭니다.
// 이클록에서시뮬레이션통과해도 FPGA 배선 지연은별도로모델링되지 않으므로 Vivado timing 통과를뜻하지 않습니다.
// ===/!==는 0/1뿐아니라 X(미정)/Z(고임피던스)도비교해미초기화신호를검출합니다.
// $fatal은 실패하면즉시종료하는 assert 역할,$display/$write는 자동검증이읽는텍스트출력입니다.
// 정답출력이존재한다는확인과학습언어모델의문장 품질은다른검증입니다.이 bench는 기능/제어/산술규칙을 확인합니다.
module tb_transformer;
    // T=4 token,D=4 hidden 채널,F=8 FFN 확장채널의아주작은검증구성입니다.
    // 이 값을현재학습 체크포인트 V65,D16,H4,L2와 혼동하지마세요.
    localparam integer T = 4;
    localparam integer D = 4;
    localparam integer F = 8;

    // reg는 bench에서 값을대입하는변수,wire는 DUT(검사대상회로)의출력을받는연결선입니다.
    // x_flat은 embedding 이후 hidden을 직접주므로여기에는문자 tokenizer나 LM vocabulary logits가 없습니다.
    reg clk;
    reg rst_n;
    reg start;
    reg [T*D*16-1:0] x_flat;
    reg [D*D*16-1:0] wq_flat;
    reg [D*D*16-1:0] wk_flat;
    reg [D*D*16-1:0] wv_flat;
    reg [D*D*16-1:0] wo_flat;
    reg [D*F*16-1:0] w1_flat;
    reg [F*D*16-1:0] w2_flat;
    wire busy;
    wire done;
    wire [T*D*16-1:0] y_flat;
    wire [31:0] cpu_words;
    wire [31:0] pim_words;
    wire [31:0] macs;
    wire [31:0] pu_ops;
    wire [31:0] modeled_cycles;
    wire [3:0] scheduler_stage;

    // first_y/second_y는 미래 token 변경전후출력 snapshot. sm/ln/relu/add는 PU 단위검사용별도신호입니다.
    reg [T*D*16-1:0] first_y;
    reg [T*D*16-1:0] second_y;
    reg [T*16-1:0] sm_in;
    reg [T*16-1:0] sm_out;
    reg [T*16-1:0] ln_in;
    reg [T*16-1:0] ln_out;
    reg [T*16-1:0] relu_in;
    reg [T*16-1:0] relu_out;
    reg [T*16-1:0] add_a;
    reg [T*16-1:0] add_b;
    wire [T*16-1:0] add_out;
    wire [T*16-1:0] unused_b;
    integer i;
    integer r;
    integer c;
    integer output_sum;
    integer transaction_cycles;

    assign unused_b = {T*16{1'b0}};

    // DUT는 legacy one-head decoder와 모델 cycle scheduler입니다.
    // CPU/PIM words와 modeled_cycles는 가정의 counter이며외부 DDR에실제명령을내린횟수가아닙니다.
    transformer_decoder_pim #(.TOKENS(T), .D_MODEL(D), .D_FF(F)) dut (
        .clk(clk), .rst_n(rst_n), .start(start),
        .x_flat(x_flat), .wq_flat(wq_flat), .wk_flat(wk_flat),
        .wv_flat(wv_flat), .wo_flat(wo_flat),
        .w1_flat(w1_flat), .w2_flat(w2_flat),
        .busy(busy), .done(done), .y_flat(y_flat),
        .cpu_boundary_words(cpu_words), .pim_boundary_words(pim_words),
        .mac_count(macs), .nonvmm_vector_ops(pu_ops),
        .modeled_latency_cycles(modeled_cycles),
        .scheduler_stage(scheduler_stage)
    );

    dram_pim_nonvmm_pu #(.VEC_LEN(T)) softmax_test (
        .op(2'd2), .a_flat(sm_in), .b_flat(unused_b),
        .valid_mask(4'b0011), .y_flat(sm_out)
    );
    dram_pim_nonvmm_pu #(.VEC_LEN(T)) layernorm_test (
        .op(2'd3), .a_flat(ln_in), .b_flat(unused_b),
        .valid_mask(4'b1111), .y_flat(ln_out)
    );
    dram_pim_nonvmm_pu #(.VEC_LEN(T)) relu_test (
        .op(2'd0), .a_flat(relu_in), .b_flat(unused_b),
        .valid_mask(4'b1111), .y_flat(relu_out)
    );
    dram_pim_nonvmm_pu #(.VEC_LEN(T)) add_test (
        .op(2'd1), .a_flat(add_a), .b_flat(add_b),
        .valid_mask(4'b1111), .y_flat(add_out)
    );

    // 시뮬레이터 10 ns clock:5ns마다 반전. FPGA clock은 XDC의 create_clock와 보드 oscillator로따로정합니다.
    always #5 clk = ~clk;

    // Python교육표현: start_pulse(); wait_done_with_timeout(); assert cycles==expected.
    // negedge에서 start를 바꾸고 posedge에서 DUT가 읽어 bench/DUT 사이의동시대입 race를 피합니다.
    // #1은 posedge의 nonblocking 갱신이 끝난다음 done을 관찰하도록만든시뮬레이션여유입니다.
    task automatic run_transaction;
        begin
            @(negedge clk);
            start = 1'b1;
            @(negedge clk);
            start = 1'b0;
            transaction_cycles = 0;
            while (done !== 1'b1) begin
                @(posedge clk);
                #1;
                transaction_cycles = transaction_cycles + 1;
                if (transaction_cycles > 700)
                    $fatal(1, "scheduler did not finish within modeled latency");
            end
            if (transaction_cycles != modeled_cycles)
                $fatal(1, "scheduler latency mismatch: saw=%0d expected=%0d",
                       transaction_cycles, modeled_cycles);
        end
    endtask

    // 초기화→테스트데이터설정→reset 해제→거래실행→인과성/PU/모델 counter 검사순서입니다.
    initial begin
        clk = 0;
        rst_n = 0;
        start = 0;
        x_flat = 0;
        wq_flat = 0;
        wk_flat = 0;
        wv_flat = 0;
        wo_flat = 0;
        w1_flat = 0;
        w2_flat = 0;
        sm_in = 0;
        ln_in = 0;
        relu_in = 0;
        add_a = 0;
        add_b = 0;
        first_y = 0;
        second_y = 0;

        // 테스트 가중치를 항등행렬처럼 둔다. 따라서 Q/K/V와 출력 투영은 입력을
        // 크게 바꾸지 않고, FFN은 첫 네 채널을 여덟 채널 ReLU 층으로 전달한다.
        for (r = 0; r < D; r = r + 1) begin
            wq_flat[(r*D+r)*16 +: 16] = 16'sd256;
            wk_flat[(r*D+r)*16 +: 16] = 16'sd256;
            wv_flat[(r*D+r)*16 +: 16] = 16'sd256;
            wo_flat[(r*D+r)*16 +: 16] = 16'sd256;
            w1_flat[(r*F+r)*16 +: 16] = 16'sd256;
            w2_flat[(r*D+r)*16 +: 16] = 16'sd256;
        end

        // 토큰 네 개의 작은 signed Q8.8 입력 표현이다. 실제 토크나이저나
        // embedding lookup은 이 설계 바깥에서 끝났다고 가정한다.
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
        x_flat[(3*D+0)*16 +: 16] = 16'sd96;
        x_flat[(3*D+1)*16 +: 16] = -16'sd96;
        x_flat[(3*D+2)*16 +: 16] = 16'sd32;
        x_flat[(3*D+3)*16 +: 16] = 16'sd64;

        sm_in[0*16 +: 16] = 16'sd0;
        sm_in[1*16 +: 16] = 16'sd0;
        sm_in[2*16 +: 16] = 16'sd200;
        sm_in[3*16 +: 16] = -16'sd100;
        ln_in[0*16 +: 16] = 16'sd256;
        ln_in[1*16 +: 16] = 16'sd0;
        ln_in[2*16 +: 16] = -16'sd256;
        ln_in[3*16 +: 16] = 16'sd0;
        relu_in[0*16 +: 16] = -16'sd10;
        relu_in[1*16 +: 16] = 16'sd0;
        relu_in[2*16 +: 16] = 16'sd23;
        relu_in[3*16 +: 16] = -16'sd1;
        add_a[0*16 +: 16] = 16'sd32760;
        add_b[0*16 +: 16] = 16'sd100;
        add_a[1*16 +: 16] = -16'sd32760;
        add_b[1*16 +: 16] = -16'sd100;
        add_a[2*16 +: 16] = 16'sd100;
        add_b[2*16 +: 16] = -16'sd100;

        // reset을 처음두 clock 동안유지해모든제어 레지스터가초기 상태가되도록합니다.
        repeat (2) @(negedge clk);
        rst_n = 1;
        run_transaction();
        first_y = y_flat;

        // activation 이동량가정의 576→32 words를 검사합니다.1 word=16 bit이므로 1152→64bytes입니다.
        // 모델상감소율은 94.44%이고실제 보드 DDR 전력/속도절감측정이아닙니다.
        if (cpu_words !== 32'd576 || pim_words !== 32'd32)
            $fatal(1, "traffic model mismatch: cpu=%0d pim=%0d", cpu_words, pim_words);
        // 640은 가중치곱+QK+PV의 MAC 항수,24는 토큰당 6 개비 VMM 단계×4token입니다.
        // 688=640+6단계×8service cycle입니다.4 개 PU벡터병렬실행가정이므로 24×8을 더하지 않습니다.
        if (macs !== 32'd640 || pu_ops !== 32'd24 || modeled_cycles !== 32'd688)
            $fatal(1, "work model mismatch: macs=%0d pu=%0d cycles=%0d", macs, pu_ops, modeled_cycles);
        // reduction XOR는 어느 비트라도 X/Z면 X로퍼지므로 16 개출력전체의미정값을한번에검사합니다.
        if ((^first_y) === 1'bx)
            $fatal(1, "Transformer result contains X/Z");

        // 인과적 어텐션 검증: 마지막 토큰 3의 입력을 바꾸어도 과거 토큰 0~2의
        // 출력은 같아야 한다. 미래 정보가 과거 출력으로 역류하지 않는지 확인한다.
        x_flat[(3*D+0)*16 +: 16] = 16'sd200;
        x_flat[(3*D+1)*16 +: 16] = -16'sd200;
        x_flat[(3*D+2)*16 +: 16] = 16'sd160;
        x_flat[(3*D+3)*16 +: 16] = 16'sd240;
        run_transaction();
        second_y = y_flat;
        for (i = 0; i < 3*D; i = i + 1)
            if (first_y[i*16 +: 16] !== second_y[i*16 +: 16])
                $fatal(1, "causal-mask violation at token/channel index %0d", i);

        // PU 단위 동작 확인: Softmax mask/확률합, LayerNorm 평균, ReLU, 포화 덧셈을
        // Transformer 전체 결과와 분리해 각각 검사한다.
        output_sum = 0;
        for (i = 0; i < T; i = i + 1)
            output_sum = output_sum + $signed(sm_out[i*16 +: 16]);
        if (sm_out[2*16 +: 16] !== 16'sd0 || sm_out[3*16 +: 16] !== 16'sd0)
            $fatal(1, "softmax mask did not suppress invalid entries");
        if ($signed(sm_out[0*16 +: 16]) !== 16'sd128 ||
            $signed(sm_out[1*16 +: 16]) !== 16'sd128)
            $fatal(1, "equal softmax logits were not split evenly");
        if (output_sum < 254 || output_sum > 258)
            $fatal(1, "softmax probabilities do not sum to 1.0 Q8.8: %0d", output_sum);

        // LUT의 가장 작은 근사값은 index 10의 2다. 긴 context에서 큰 score
        // 차이가 나도 1로 바뀌지 않는지 확인한다(긴 prefix의 RTL/Python 차이 방지).
        sm_in[0*16 +: 16] = 16'sd0;
        sm_in[1*16 +: 16] = -16'sd3000;
        #1;
        if ($signed(sm_out[0*16 +: 16]) !== 16'sd254 ||
            $signed(sm_out[1*16 +: 16]) !== 16'sd1)
            $fatal(1, "softmax LUT lower saturation mismatch: %0d %0d",
                   $signed(sm_out[0*16 +: 16]), $signed(sm_out[1*16 +: 16]));

        output_sum = 0;
        for (i = 0; i < T; i = i + 1)
            output_sum = output_sum + $signed(ln_out[i*16 +: 16]);
        if (output_sum < -3 || output_sum > 3)
            $fatal(1, "LayerNorm output mean is not approximately zero: %0d", output_sum);

        if ($signed(relu_out[0*16 +: 16]) !== 16'sd0 ||
            $signed(relu_out[1*16 +: 16]) !== 16'sd0 ||
            $signed(relu_out[2*16 +: 16]) !== 16'sd23 ||
            $signed(relu_out[3*16 +: 16]) !== 16'sd0)
            $fatal(1, "ReLU PU check failed");
        if ($signed(add_out[0*16 +: 16]) !== 16'sd32767 ||
            $signed(add_out[1*16 +: 16]) !== -16'sd32768 ||
            $signed(add_out[2*16 +: 16]) !== 16'sd0)
            $fatal(1, "saturating-add PU check failed");

        // 아래숫자는 run_tests.py의 parser가 읽는재현출력입니다. $signed를 붙이지않으면음수비트패턴을
        // 큰 양수로출력할 수 있습니다.OUTPUT은 hidden raw 벡터이며각 값을 256으로 나누면실수입니다.
        $display("RESULT words_cpu=%0d words_pim=%0d activation_reduction_pct=%0d",
                 cpu_words, pim_words, ((cpu_words-pim_words)*100)/cpu_words);
        $display("RESULT macs=%0d nonvmm_vector_ops=%0d modeled_pim_cycles=%0d",
                 macs, pu_ops, modeled_cycles);
        for (r = 0; r < T; r = r + 1) begin
            $write("OUTPUT token=%0d", r);
            for (c = 0; c < D; c = c + 1)
                $write(" %0d", $signed(first_y[(r*D+c)*16 +: 16]));
            $write("\n");
        end
        $display("PASS: transformer datapath, causal mask, non-VMM PUs, and traffic assertions");
        $finish;
    end
endmodule
