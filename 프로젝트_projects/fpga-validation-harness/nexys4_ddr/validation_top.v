`timescale 1ns/1ps
// Educational digital validation target. No ADC, DDR, UART or CPU is instantiated.
// CLK_HZ=100 MHz on Nexys4 DDR. TICK_CYCLES may be reduced in simulation only.
module validation_top #(
    parameter integer TICK_CYCLES = 100000
) (
    input wire CLK100MHZ,
    input wire BTNC,
    input wire [1:0] SW,
    output wire [3:0] LED
);
    (* ASYNC_REG = "TRUE" *) reg [1:0] sw_meta = 0, sw_sync = 0;
    (* ASYNC_REG = "TRUE" *) reg rst_meta = 0, rst_sync = 0;
    reg [25:0] heartbeat = 0;
    reg [31:0] divider = 0;
    reg [15:0] next_seq = 0;
    (* MARK_DEBUG = "TRUE" *) reg sample_valid = 0;
    (* MARK_DEBUG = "TRUE" *) reg [15:0] sample_seq = 0;
    (* MARK_DEBUG = "TRUE" *) reg [15:0] expected_word = 0;
    (* MARK_DEBUG = "TRUE" *) reg [15:0] actual_word = 0;
    (* MARK_DEBUG = "TRUE" *) reg mismatch = 0;
    (* MARK_DEBUG = "TRUE" *) reg [31:0] sample_count = 0;
    (* MARK_DEBUG = "TRUE" *) reg [31:0] error_count = 0;

    wire [15:0] expected_next = next_seq ^ 16'h5A5A;
    wire inject_now = sw_sync[1] && (next_seq[3:0] == 4'hF);
    wire [15:0] actual_next = expected_next ^ (inject_now ? 16'h0001 : 16'h0000);

    always @(posedge CLK100MHZ) begin
        sw_meta <= SW;
        sw_sync <= sw_meta;
        rst_meta <= BTNC;
        rst_sync <= rst_meta;
        heartbeat <= heartbeat + 1'b1;
        sample_valid <= 1'b0;
        if (rst_sync) begin
            divider <= 0;
            next_seq <= 0;
            sample_seq <= 0;
            expected_word <= 0;
            actual_word <= 0;
            mismatch <= 0;
            sample_count <= 0;
            error_count <= 0;
        end else if (!sw_sync[0]) begin
            divider <= 0;
        end else if (divider == TICK_CYCLES - 1) begin
            divider <= 0;
            sample_valid <= 1'b1;
            sample_seq <= next_seq;
            expected_word <= expected_next;
            actual_word <= actual_next;
            mismatch <= (actual_next != expected_next);
            sample_count <= sample_count + 1'b1;
            if (actual_next != expected_next)
                error_count <= error_count + 1'b1;
            next_seq <= next_seq + 1'b1;
        end else begin
            divider <= divider + 1'b1;
        end
    end
    assign LED[0] = heartbeat[25];
    assign LED[1] = sw_sync[0];
    assign LED[2] = mismatch;
    assign LED[3] = (error_count != 0);
endmodule
