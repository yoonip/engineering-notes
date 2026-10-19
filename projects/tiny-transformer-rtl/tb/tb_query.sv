`timescale 1ns/1ps
`default_nettype none

// Single live query bench. run.ps1 geocodes a location, retrieves forecast
// precipitation probability, and passes QUERY_ID and FORECAST_ID as plusargs.
// Only the compact IDs enter the DUT; API/text processing stays on the host.
module tb_tiny_gpt;
    localparam logic [3:0] TOK_BOS = 4'd1;
    localparam logic [3:0] TOK_ASK_RAIN = 4'd2;
    localparam logic [3:0] TOK_ASK_CLEAR = 4'd3;
    localparam logic [3:0] TOK_FORECAST_HIGH = 4'd4;
    localparam logic [3:0] TOK_FORECAST_LOW = 4'd5;
    localparam logic [3:0] TOK_BI_GA = 4'd6;
    localparam logic [3:0] TOK_OL = 4'd7;
    localparam logic [3:0] TOK_CHANCE = 4'd8;
    localparam logic [3:0] TOK_HIGH = 4'd9;
    localparam logic [3:0] TOK_LOW = 4'd10;
    localparam logic [3:0] TOK_CLEAR = 4'd12;

    logic clk = 1'b0;
    logic rst_n = 1'b0;
    logic in_valid = 1'b0;
    logic [3:0] in_token = 0;
    logic in_last = 1'b0;
    logic in_ready, out_valid, done;
    logic [3:0] out_token;
    integer query_id = 2;
    integer forecast_id = 4;
    integer expected_count;
    integer cycles, index;
    integer future_nonzero;
    integer generated_count = 0;
    logic [3:0] generated [0:7];

    always #5 clk = ~clk;

    tiny_gpt dut (
        .clk(clk), .rst_n(rst_n), .in_valid(in_valid), .in_token(in_token),
        .in_last(in_last), .in_ready(in_ready), .out_valid(out_valid),
        .out_token(out_token), .done(done)
    );

    task automatic send_token(input logic [3:0] id, input logic last_token);
        begin
            @(negedge clk);
            while (!in_ready) @(negedge clk);
            in_valid = 1'b1;
            in_token = id;
            in_last = last_token;
            @(negedge clk);
            in_valid = 1'b0;
            in_last = 1'b0;
        end
    endtask

    task automatic print_token(input logic [3:0] id);
        begin
            case (id)
                TOK_BI_GA: $write("비가 ");
                TOK_OL: $write("올 ");
                TOK_CHANCE: $write("가능성이 ");
                TOK_HIGH: $write("높습니다.");
                TOK_LOW: $write("낮습니다.");
                TOK_CLEAR: $write("맑을 ");
                default: $write("<ID:%0d>", id);
            endcase
        end
    endtask

    initial begin
        if (!$value$plusargs("QUERY_ID=%d", query_id)) query_id = 2;
        if (!$value$plusargs("FORECAST_ID=%d", forecast_id)) forecast_id = 4;
        if ((query_id != 2) && (query_id != 3)) $fatal(1, "QUERY_ID must be 2 or 3");
        if ((forecast_id != 4) && (forecast_id != 5)) $fatal(1, "FORECAST_ID must be 4 or 5");
        if (query_id == 2) expected_count = 4;
        else expected_count = 3;

        repeat (3) @(negedge clk);
        rst_n = 1'b1;
        repeat (2) @(negedge clk);

        if (query_id == 2) $display("TOKENIZER: ASK_RAIN (ID=2)");
        else $display("TOKENIZER: ASK_CLEAR (ID=3)");
        if (forecast_id == 4) $display("FORECAST TOKEN: HIGH precipitation probability (ID=4)");
        else $display("FORECAST TOKEN: LOW precipitation probability (ID=5)");
        send_token(TOK_BOS, 1'b0);
        send_token(query_id, 1'b0);
        send_token(forecast_id, 1'b1);

        future_nonzero = 0;
        for (index=3; index<8; index=index+1)
            if (dut.probs[2][index] != 0) future_nonzero = 1;
        if ((dut.probs[2][0] + dut.probs[2][1] + dut.probs[2][2] < 250) ||
            (dut.probs[2][0] + dut.probs[2][1] + dut.probs[2][2] > 258) ||
            (future_nonzero != 0))
            $fatal(1, "causal softmax assertion failed");
        $display("ATTN Q8: scores=(%0d,%0d,%0d), probabilities=(%0d,%0d,%0d)",
                 dut.scores[2][0], dut.scores[2][1], dut.scores[2][2],
                 dut.probs[2][0], dut.probs[2][1], dut.probs[2][2]);

        cycles = 0;
        while ((cycles < 16) && !done) begin
            @(posedge clk);
            #1;
            if (out_valid) begin
                if (generated_count < 8) generated[generated_count] = out_token;
                generated_count = generated_count + 1;
            end
            cycles = cycles + 1;
        end
        if (!done) $fatal(1, "timed out waiting for EOS");
        if (generated_count != expected_count)
            $fatal(1, "expected %0d tokens, received %0d", expected_count, generated_count);

        if (query_id == 2) begin
            if ((generated[0] != TOK_BI_GA) || (generated[1] != TOK_OL) ||
                (generated[2] != TOK_CHANCE) ||
                ((forecast_id == 4) && (generated[3] != TOK_HIGH)) ||
                ((forecast_id == 5) && (generated[3] != TOK_LOW)))
                $fatal(1, "rain answer tokens do not match forecast token");
        end else begin
            if ((generated[0] != TOK_CLEAR) || (generated[1] != TOK_CHANCE) ||
                ((forecast_id == 4) && (generated[2] != TOK_LOW)) ||
                ((forecast_id == 5) && (generated[2] != TOK_HIGH)))
                $fatal(1, "clear answer tokens do not match forecast token");
        end

        $write("OUTPUT: ");
        for (index=0; index<generated_count; index=index+1) print_token(generated[index]);
        $write("\nIDS:");
        for (index=0; index<generated_count; index=index+1) $write(" %0d", generated[index]);
        $display("\nPASS: forecast-conditioned token generation, causal attention, and EOS verified.");
        $finish;
    end
endmodule

`default_nettype wire
