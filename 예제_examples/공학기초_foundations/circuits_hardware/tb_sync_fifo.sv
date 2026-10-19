`timescale 1ns/1ps
module tb_sync_fifo;
    parameter integer DEPTH = 3;
    localparam integer COUNT_W = $clog2(DEPTH + 1);
    logic clk = 0;
    always #5 clk = ~clk;
    logic rst = 1, wr_en = 0, rd_en = 0;
    logic [7:0] wr_data = 0;
    wire [7:0] rd_data;
    wire wr_ack, rd_valid, full, empty;
    wire [COUNT_W-1:0] count;
    sync_fifo #(.WIDTH(8), .DEPTH(DEPTH)) dut (.*);
    integer q [0:DEPTH-1];
    integer n = 0;
    integer index;
    reg [31:0] seed = 32'h137;

    task automatic step(input bit w, input bit r, input logic [7:0] d, input bit reset);
        bit aw, ar;
        integer expected, j;
        begin
            @(negedge clk);
            rst = reset;
            wr_en = w;
            rd_en = r;
            wr_data = d;
            aw = w && n < DEPTH && !reset;
            ar = r && n > 0 && !reset;
            if (reset) begin
                n = 0;
            end else begin
                if (ar) begin
                    expected = q[0];
                    for (j = 1; j < n; j = j + 1) q[j-1] = q[j];
                    n = n - 1;
                end
                if (aw) begin
                    q[n] = d;
                    n = n + 1;
                end
            end
            @(posedge clk);
            #1;
            if (count !== n || full !== (n == DEPTH) || empty !== (n == 0))
                $fatal(1, "FIFO 상태 불일치");
            if (wr_ack !== aw || rd_valid !== ar) $fatal(1, "수락 플래그 불일치");
            if (ar && rd_data !== expected[7:0]) $fatal(1, "FIFO 순서 불일치");
        end
    endtask

    initial begin
        step(0, 0, 0, 1);
        step(1, 1, 8'h42, 0);
        for (index = 0; index < DEPTH+2; index = index + 1) step(1, 0, index[7:0], 0);
        step(1, 1, 8'h99, 0);
        for (index = 0; index < DEPTH+2; index = index + 1) step(0, 1, 0, 0);
        for (index = 0; index < 5000; index = index + 1) begin
            seed = seed * 32'd1664525 + 32'd1013904223;
            step(seed[30], seed[29], seed[23:16], index % 997 == 0);
        end
        $display("PASS DEPTH=%0d", DEPTH);
        $finish;
    end
endmodule
