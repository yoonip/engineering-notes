`timescale 1ns/1ps
module tb_validation_top;
    reg clk = 0;
    reg reset = 0;
    reg [1:0] sw = 0;
    wire [3:0] led;
    integer checked = 0;
    integer errors = 0;
    integer before_pause;
    validation_top #(.TICK_CYCLES(10)) dut(clk, reset, sw, led);
    always #5 clk = ~clk;

    task do_reset;
        begin
            @(negedge clk); reset = 1;
            repeat (8) @(negedge clk);
            reset = 0;
            repeat (5) @(negedge clk);
        end
    endtask
    task check_samples(input integer n, input bit inject);
        integer count;
        reg [15:0] expected;
        begin
            count = 0;
            while (count < n) begin
                @(negedge clk);
                if (dut.sample_valid) begin
                    expected = dut.sample_seq ^ 16'h5A5A;
                    if (dut.expected_word !== expected) $fatal(1, "expected pattern incorrect");
                    if (dut.actual_word !== (expected ^ ((inject && dut.sample_seq[3:0] == 15) ? 16'h1 : 16'h0)))
                        $fatal(1, "actual pattern incorrect");
                    if (dut.mismatch !== (dut.actual_word != dut.expected_word))
                        $fatal(1, "mismatch flag incorrect");
                    if (dut.mismatch) errors = errors + 1;
                    count = count + 1;
                    checked = checked + 1;
                end
            end
        end
    endtask
    initial begin
        do_reset();
        sw = 2'b01;
        check_samples(32, 0);
        if (dut.error_count != 0) $fatal(1, "healthy run has errors");
        sw = 0;
        repeat (5) @(negedge clk);
        before_pause = dut.sample_count;
        repeat (30) @(negedge clk);
        if (dut.sample_count != before_pause) $fatal(1, "pause failed");
        do_reset();
        sw = 2'b11;
        check_samples(32, 1);
        if (dut.error_count != 2 || errors != 2) $fatal(1, "injection count incorrect");
        sw = 0;
        do_reset();
        if (dut.sample_count != 0 || dut.error_count != 0 || led[3] != 0)
            $fatal(1, "reset failed");
        $display("PASS: %0d samples, normal/injected errors, pause and reset checked", checked);
        $finish;
    end
    initial begin
        #100000;
        $fatal(1, "testbench timed out");
    end
endmodule
