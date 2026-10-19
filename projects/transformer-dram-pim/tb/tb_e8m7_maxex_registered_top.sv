`timescale 1ns/1ps
// =============================================================================
// 독립 MAX-EX의 ‘입력 register → 조합 내적 → 출력 register’ 계약을 검사한다.
// 원 GPT/UART 회로와 별개이며, Icarus의 RTL 기능 시험이다. SDF/실물 측정이 아니다.
// 입력을 edge N에 수락하면 edge N+1 직후 output_valid와 결과가 나와야 한다.
// 연속 valid에서는 매 clock 결과가 하나씩 나온다. bubble은 valid=0인 빈 입력이다.
// reset_n은 비동기 reset이 아니다. falling edge에서 낮춰도 출력은 유지하고,
// 다음 rising edge에서만 register·result·valid를 지워 대기 중 거래를 취소한다.
// Python tools/verify_e8m7_maxex_registered.py가 schedule과 정답 mem을 생성한다.
// =============================================================================
module tb_e8m7_maxex_registered_top #(
    parameter integer LANES = 16,
    parameter integer GUARD_BITS = 16,
    parameter integer CYCLES = 64
);
    reg clk = 0;
    reg reset_n = 0;
    reg input_valid = 0;
    reg [LANES*16-1:0] a_packed = 0;
    reg [LANES*16-1:0] b_packed = 0;
    wire [15:0] result;
    wire output_valid;
    // controls[1]=reset_n, controls[0]=input_valid다. a/b mem 한 줄은 LANES*16bit다.
    // lane0은 packed bus의 최하위16bit, lane i는 [16*i+:16]에 있어야 한다.
    reg [1:0] controls [0:CYCLES-1];
    reg [LANES*16-1:0] a_values [0:CYCLES-1];
    reg [LANES*16-1:0] b_values [0:CYCLES-1];
    reg [15:0] input_expected [0:CYCLES-1];

    reg pending_valid = 0;
    reg [15:0] pending_word = 0;
    reg [15:0] before_result;
    reg before_valid;
    integer cycle;
    integer lane;
    integer exact_count = 0;
    integer accepted_count = 0;
    integer cancelled_count = 0;
    integer reset_count = 0;
    integer lane_checks = 0;
    integer valid_checks = 0;
    integer synchronous_checks = 0;
    integer burst_length = 0;
    integer maximum_burst = 0;

    e8m7_maxex_registered_top #(.LANES(LANES), .GUARD_BITS(GUARD_BITS)) dut (
        .clk(clk), .reset_n(reset_n), .input_valid(input_valid),
        .a_packed(a_packed), .b_packed(b_packed),
        .result(result), .output_valid(output_valid)
    );
    // OOC 제약과 같은200ns·5MHz clock이다. #1은 NBA 업데이트를 관찰하기 위한
    // testbench delay이며 조합 회로가 실제1ns에 계산된다는 주장은 아니다.
    always #100 clk = ~clk;

    initial begin
        $readmemh("controls.mem", controls);
        $readmemh("a.mem", a_values);
        $readmemh("b.mem", b_values);
        $readmemh("expected.mem", input_expected);
        for (cycle = 0; cycle < CYCLES; cycle = cycle + 1) begin
            // 입력은 sampling rising edge와 떨어진 falling edge에서 바꾼다.
            // reset을 낮춘 직후 즉시 지워지면 동기 reset 계약을 위반한 것이다.
            @(negedge clk);
            before_result = result;
            before_valid = output_valid;
            reset_n = controls[cycle][1];
            input_valid = controls[cycle][0];
            a_packed = a_values[cycle];
            b_packed = b_values[cycle];
            #1;
            if (result !== before_result || output_valid !== before_valid)
                $fatal(1, "output changed before rising edge cycle=%0d", cycle);
            synchronous_checks = synchronous_checks + 1;

            @(posedge clk); #1;
            // scoreboard는 직전 clock에 수락한 정답을 보관한다. 이번 입력의
            // 정답을 바로 비교하면 잘못된 zero-latency 회로도 통과할 수 있다.
            if (!reset_n) begin
                if (result !== 16'h0000 || output_valid !== 1'b0)
                    $fatal(1, "synchronous reset failed cycle=%0d", cycle);
                for (lane = 0; lane < LANES; lane = lane + 1)
                    if (dut.a_registered[lane] !== 16'h0000 ||
                        dut.b_registered[lane] !== 16'h0000)
                        $fatal(1, "reset did not clear input lane=%0d", lane);
                if (pending_valid) cancelled_count = cancelled_count + 1;
                pending_valid = 0;
                reset_count = reset_count + 1;
                burst_length = 0;
            end else begin
                if (output_valid !== pending_valid)
                    $fatal(1, "one-clock valid latency failed cycle=%0d got=%b expected=%b",
                           cycle, output_valid, pending_valid);
                if (pending_valid) begin
                    if (result !== pending_word)
                        $fatal(1, "registered result mismatch cycle=%0d got=%h expected=%h",
                               cycle, result, pending_word);
                    exact_count = exact_count + 1;
                end
                // 동시에 a/b의 모든 lane 순서도 검사한다. 내적에서 a와b를 같이
                // 뒤집으면 최종 합이 같을 수 있으므로 결과 비교만으로 endian을
                // 검증했다고 말할 수 없다. 실제 내부 register index를 확인한다.
                if (input_valid) begin
                    for (lane = 0; lane < LANES; lane = lane + 1) begin
                        if (dut.a_registered[lane] !== a_packed[16*lane +: 16] ||
                            dut.b_registered[lane] !== b_packed[16*lane +: 16])
                            $fatal(1, "packed lane/endian mismatch cycle=%0d lane=%0d", cycle, lane);
                        lane_checks = lane_checks + 2;
                    end
                    accepted_count = accepted_count + 1;
                    pending_word = input_expected[cycle];
                    burst_length = burst_length + 1;
                    if (burst_length > maximum_burst) maximum_burst = burst_length;
                end else begin
                    burst_length = 0;
                end
                // bubble에서는 계산 register 내용을 유지할 수 있다. 결과 값은
                // valid=0일 때 사용하지 않으며 valid가 정확히 내려가는지 검사한다.
                pending_valid = input_valid;
            end
            valid_checks = valid_checks + 1;
            $display("CHECK_REG cycle=%0d valid=%0d result=%h exact=%0d",
                     cycle, output_valid, result, exact_count);
        end
        // 마지막 schedule은 bubble이라 미검사 pending 입력을 남기지 않아야 한다.
        if (pending_valid) $fatal(1, "schedule did not flush final input");
        $display("PASS_REG lanes=%0d guard=%0d cycles=%0d exact=%0d accepted=%0d cancelled=%0d resets=%0d lane_checks=%0d valid_checks=%0d synchronous_checks=%0d maximum_burst=%0d",
                 LANES, GUARD_BITS, CYCLES, exact_count, accepted_count, cancelled_count,
                 reset_count, lane_checks, valid_checks, synchronous_checks, maximum_burst);
        $finish;
    end
    // 이 simulation은 수백clock만 필요하다. 무한 대기나 clock 정지를 명시적으로
    // 실패시킨다. real literal로 delay를 써32bit 정수 overflow도 피한다.
    initial begin #10000000.0; $fatal(1, "registered MAX-EX test timeout"); end
endmodule
