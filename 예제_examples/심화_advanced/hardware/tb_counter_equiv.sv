module tb_counter_equiv;
    logic clk=0, reset=1, enable=0;
    logic [7:0] qb, qs, expected=0;
    logic [31:0] rng=32'h55aacc17;
    integer k;
    counter_behavioral reference_dut(clk,reset,enable,qb);
    counter_structural structural_dut(clk,reset,enable,qs);
    task tick;
        begin
            #1; clk=1;
            if (reset) expected=0;
            else if (enable) expected=expected+8'd1;
            #1;
            if (qb !== expected || qs !== expected)
                $fatal(1,"counter mismatch qb=%0d qs=%0d expected=%0d",qb,qs,expected);
            clk=0; #1;
        end
    endtask
    initial begin
        tick();
        reset=0; enable=1;
        for(k=0;k<256;k=k+1) tick();
        for(k=0;k<10000;k=k+1) begin
            rng={rng[30:0],rng[31]^rng[21]^rng[1]^rng[0]};
            enable=rng[0]; reset=(rng[5:1]==0);
            tick();
        end
        $display("PASS counter cycles=10257");
        $finish;
    end
endmodule
