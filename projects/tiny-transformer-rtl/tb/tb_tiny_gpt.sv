`timescale 1ns/1ps
`default_nettype none

// Four self-checking forecast-conditioned examples. Forecast category IDs are
// normally produced by run.ps1 from a live API; these test values make the
// default simulation reproducible without Internet access.
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
    integer failures = 0;
    integer generated_count;
    logic [3:0] generated [0:7];

    always #5 clk = ~clk;

    tiny_gpt dut (
        .clk(clk), .rst_n(rst_n), .in_valid(in_valid), .in_token(in_token),
        .in_last(in_last), .in_ready(in_ready), .out_valid(out_valid),
        .out_token(out_token), .done(done)
    );

    // The input adapter is intentionally outside the neural RTL. This task
    // sends a three-token prefix: BOS, question intent, and forecast category.
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

    task automatic run_case(
        input string prompt_label,
        input logic [3:0] query_id,
        input logic [3:0] forecast_id,
        input integer expected_count,
        input logic [3:0] expected0,
        input logic [3:0] expected1,
        input logic [3:0] expected2,
        input logic [3:0] expected3
    );
        integer cycles, index, future_nonzero;
        begin
            generated_count = 0;
            $display("INPUT : %s", prompt_label);
            send_token(TOK_BOS, 1'b0);
            send_token(query_id, 1'b0);
            send_token(forecast_id, 1'b1);

            // The final prompt token is position 2. Its causal attention row
            // may see positions 0..2, but never position 3 or later.
            // Integer softmax division can leave a few Q8 units unassigned.
            future_nonzero = 0;
            for (index=3; index<8; index=index+1)
                if (dut.probs[2][index] != 0) future_nonzero = 1;
            if ((dut.probs[2][0] + dut.probs[2][1] + dut.probs[2][2] < 250) ||
                (dut.probs[2][0] + dut.probs[2][1] + dut.probs[2][2] > 258) ||
                (future_nonzero != 0)) begin
                $display("FAIL: causal softmax row = (%0d,%0d,%0d,%0d)",
                         dut.probs[2][0], dut.probs[2][1], dut.probs[2][2], dut.probs[2][3]);
                failures = failures + 1;
            end else begin
                $display("ATTN : score_Q8=(%0d,%0d,%0d), probability_Q8=(%0d,%0d,%0d)",
                         dut.scores[2][0], dut.scores[2][1], dut.scores[2][2],
                         dut.probs[2][0], dut.probs[2][1], dut.probs[2][2]);
            end

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

            if (!done) begin
                $display("FAIL: timed out waiting for EOS");
                failures = failures + 1;
            end else if (generated_count != expected_count) begin
                $display("FAIL: expected %0d tokens, received %0d", expected_count, generated_count);
                failures = failures + 1;
            end else if ((generated[0] != expected0) ||
                         ((expected_count > 1) && (generated[1] != expected1)) ||
                         ((expected_count > 2) && (generated[2] != expected2)) ||
                         ((expected_count > 3) && (generated[3] != expected3))) begin
                $display("FAIL: generated token IDs differ from expected sequence");
                failures = failures + 1;
            end else begin
                $write("OUTPUT: ");
                for (index=0; index<generated_count; index=index+1) print_token(generated[index]);
                $write("\nIDS   :");
                for (index=0; index<generated_count; index=index+1) $write(" %0d", generated[index]);
                $write("\n");
            end
        end
    endtask

    initial begin
        repeat (3) @(negedge clk);
        rst_n = 1'b1;
        repeat (2) @(negedge clk);

        // Deterministic mock forecast bins test every model response path.
        run_case("rain intent, precipitation probability 75%", TOK_ASK_RAIN, TOK_FORECAST_HIGH,
                 4, TOK_BI_GA, TOK_OL, TOK_CHANCE, TOK_HIGH);
        run_case("rain intent, precipitation probability 10%", TOK_ASK_RAIN, TOK_FORECAST_LOW,
                 4, TOK_BI_GA, TOK_OL, TOK_CHANCE, TOK_LOW);
        run_case("clear intent, precipitation probability 75%", TOK_ASK_CLEAR, TOK_FORECAST_HIGH,
                 3, TOK_CLEAR, TOK_CHANCE, TOK_LOW, 0);
        run_case("clear intent, precipitation probability 10%", TOK_ASK_CLEAR, TOK_FORECAST_LOW,
                 3, TOK_CLEAR, TOK_CHANCE, TOK_HIGH, 0);

        if (failures == 0)
            $display("PASS: all four forecast-conditioned token sequences, causal masks, and EOS checks passed.");
        else
            $fatal(1, "FAIL: %0d check(s) failed.", failures);
        $finish;
    end
endmodule

`default_nettype wire
