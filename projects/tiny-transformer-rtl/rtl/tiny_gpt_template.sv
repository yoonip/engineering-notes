`timescale 1ns/1ps
`default_nettype none

// Tiny, trained decoder-only Transformer inference example.
//
// The Python/NumPy trainer exports learned parameters into the packed ROMs at
// GENERATED_WEIGHT_ROMS. This module itself performs inference in signed Q8.8
// fixed point and emits one vocabulary token per clock while in ST_GEN.
//
// Model: one causal self-attention head, D_MODEL=8, FFN=16, vocab=13,
// maximum context=8. Four curated weather examples train forecast-conditioned
// short answers. This is a real but intentionally tiny Transformer, not an
// unrestricted Korean language model.
module tiny_gpt (
    input  logic       clk,
    input  logic       rst_n,
    input  logic       in_valid,
    input  logic [3:0] in_token,
    input  logic       in_last,
    output logic       in_ready,
    output logic       out_valid,
    output logic [3:0] out_token,
    output logic       done
);
    localparam integer D = 8;
    localparam integer F = 16;
    localparam integer V = 13;
    localparam integer MAX_CONTEXT = 8;
    localparam integer ST_LOAD = 0;
    localparam integer ST_GEN = 1;

    // Token IDs are the model vocabulary, not UTF-8 characters.
    localparam integer TOK_PAD = 0;
    localparam integer TOK_BOS = 1;
    localparam integer TOK_ASK_RAIN = 2;
    localparam integer TOK_ASK_CLEAR = 3;
    localparam integer TOK_FORECAST_HIGH = 4;
    localparam integer TOK_FORECAST_LOW = 5;
    localparam integer TOK_BI = 6;
    localparam integer TOK_OL = 7;
    localparam integer TOK_CHANCE = 8;
    localparam integer TOK_HIGH = 9;
    localparam integer TOK_LOW = 10;
    localparam integer TOK_EOS = 11;
    localparam integer TOK_CLEAR = 12;

    // Q8.8 convention: 256 represents 1.0. Every learned parameter is signed
    // 16-bit Q8.8. Intermediate accumulators are 32-bit signed integers.
    // The ROMs are flattened in row-major order by train_numpy.py.
    // GENERATED_WEIGHT_ROMS

    logic state;
    logic [3:0] tokens [0:MAX_CONTEXT-1];
    integer token_count;

    // Public intermediate arrays are convenient for simulation waveforms and
    // testbench assertions. They describe the last combinational forward pass.
    integer signed x       [0:MAX_CONTEXT-1][0:D-1];
    integer signed ln1     [0:MAX_CONTEXT-1][0:D-1];
    integer signed q       [0:MAX_CONTEXT-1][0:D-1];
    integer signed key     [0:MAX_CONTEXT-1][0:D-1];
    integer signed value   [0:MAX_CONTEXT-1][0:D-1];
    integer signed attn    [0:MAX_CONTEXT-1][0:D-1];
    integer signed postattn[0:MAX_CONTEXT-1][0:D-1];
    integer signed ln2     [0:MAX_CONTEXT-1][0:D-1];
    integer signed ffn_act [0:MAX_CONTEXT-1][0:F-1];
    integer signed residual2[0:MAX_CONTEXT-1][0:D-1];
    integer signed hidden  [0:MAX_CONTEXT-1][0:D-1];
    integer signed scores  [0:MAX_CONTEXT-1][0:MAX_CONTEXT-1];
    integer signed probs   [0:MAX_CONTEXT-1][0:MAX_CONTEXT-1];
    integer signed logits  [0:V-1];
    logic [3:0] next_token;

    integer t, i, j, d, f, reset_idx;
    integer signed acc, mean_value, variance_value, sigma_value;
    integer signed centered, normalized, max_score, exp_sum, exp_value;
    integer signed best_logit, dot_acc, lut_index;

    // The packed tables allow a single self-contained RTL source in the
    // browser simulator. Variable part-selects make these function calls act
    // like asynchronous ROM reads.
    function automatic integer signed read16(input logic [15:0] word_value);
        begin read16 = $signed(word_value); end
    endfunction

    function automatic integer signed emb(input integer tok, input integer dim);
        integer index;
        begin index = (tok*D + dim)*16; emb = read16(EMB_ROM[index +: 16]); end
    endfunction
    function automatic integer signed pos_emb(input integer pos_id, input integer dim);
        integer index;
        begin index = (pos_id*D + dim)*16; pos_emb = read16(POS_ROM[index +: 16]); end
    endfunction
    function automatic integer signed gamma1(input integer dim);
        begin gamma1 = read16(GAMMA1_ROM[dim*16 +: 16]); end
    endfunction
    function automatic integer signed beta1(input integer dim);
        begin beta1 = read16(BETA1_ROM[dim*16 +: 16]); end
    endfunction
    function automatic integer signed gamma2(input integer dim);
        begin gamma2 = read16(GAMMA2_ROM[dim*16 +: 16]); end
    endfunction
    function automatic integer signed beta2(input integer dim);
        begin beta2 = read16(BETA2_ROM[dim*16 +: 16]); end
    endfunction
    function automatic integer signed gamma3(input integer dim);
        begin gamma3 = read16(GAMMA3_ROM[dim*16 +: 16]); end
    endfunction
    function automatic integer signed beta3(input integer dim);
        begin beta3 = read16(BETA3_ROM[dim*16 +: 16]); end
    endfunction
    function automatic integer signed wq(input integer row_id, input integer col_id);
        integer index;
        begin index = (row_id*D + col_id)*16; wq = read16(WQ_ROM[index +: 16]); end
    endfunction
    function automatic integer signed wk(input integer row_id, input integer col_id);
        integer index;
        begin index = (row_id*D + col_id)*16; wk = read16(WK_ROM[index +: 16]); end
    endfunction
    function automatic integer signed wv(input integer row_id, input integer col_id);
        integer index;
        begin index = (row_id*D + col_id)*16; wv = read16(WV_ROM[index +: 16]); end
    endfunction
    function automatic integer signed wo(input integer row_id, input integer col_id);
        integer index;
        begin index = (row_id*D + col_id)*16; wo = read16(WO_ROM[index +: 16]); end
    endfunction
    function automatic integer signed w1(input integer row_id, input integer col_id);
        integer index;
        begin index = (row_id*F + col_id)*16; w1 = read16(W1_ROM[index +: 16]); end
    endfunction
    function automatic integer signed b1(input integer col_id);
        begin b1 = read16(B1_ROM[col_id*16 +: 16]); end
    endfunction
    function automatic integer signed w2(input integer row_id, input integer col_id);
        integer index;
        begin index = (row_id*D + col_id)*16; w2 = read16(W2_ROM[index +: 16]); end
    endfunction
    function automatic integer signed b2(input integer col_id);
        begin b2 = read16(B2_ROM[col_id*16 +: 16]); end
    endfunction
    function automatic integer signed lm(input integer row_id, input integer col_id);
        integer index;
        begin index = (row_id*V + col_id)*16; lm = read16(LM_ROM[index +: 16]); end
    endfunction
    function automatic integer signed lmb(input integer col_id);
        begin lmb = read16(LMB_ROM[col_id*16 +: 16]); end
    endfunction

    // Restoring integer square-root circuit used by all three LayerNorms.
    function automatic integer signed isqrt(input integer signed number);
        integer signed n, bit_value, result_value;
        integer iteration;
        begin
            n = number; bit_value = 1 << 30; result_value = 0;
            for (iteration = 0; iteration < 16; iteration = iteration + 1) begin
                if (n >= result_value + bit_value) begin
                    n = n - (result_value + bit_value);
                    result_value = (result_value >> 1) + bit_value;
                end else result_value = result_value >> 1;
                bit_value = bit_value >> 2;
            end
            isqrt = result_value;
        end
    endfunction

    // exp(-delta) lookup every 0.25. Values are scaled by 4096. The stable
    // softmax subtracts the maximum score before looking up these exponentials.
    function automatic integer signed exp_lut(input integer index);
        begin
            case (index)
                0: exp_lut=4096; 1: exp_lut=3186; 2: exp_lut=2477; 3: exp_lut=1928;
                4: exp_lut=1500; 5: exp_lut=1167; 6: exp_lut=907; 7: exp_lut=705;
                8: exp_lut=549; 9: exp_lut=427; 10: exp_lut=332; 11: exp_lut=259;
                12: exp_lut=201; 13: exp_lut=157; 14: exp_lut=122; 15: exp_lut=95;
                16: exp_lut=74; 17: exp_lut=58; 18: exp_lut=45; 19: exp_lut=35;
                20: exp_lut=27; 21: exp_lut=21; 22: exp_lut=17; 23: exp_lut=13;
                24: exp_lut=10; 25: exp_lut=8; 26: exp_lut=6; 27: exp_lut=5;
                28: exp_lut=4; 29: exp_lut=3; 30: exp_lut=2; 31: exp_lut=2;
                default: exp_lut=1;
            endcase
        end
    endfunction

    // One complete forward pass over the occupied prefix. Causal masking is
    // implemented by evaluating only key positions j <= query position t.
    // Products are shifted right by 8 to return to Q8.8 after each multiply.
    always_comb begin
        // Explicit defaults keep every scratch value purely combinational,
        // including cycles with an empty context, so synthesis cannot infer a
        // storage latch for an intermediate accumulator.
        acc=0; mean_value=0; variance_value=0; sigma_value=0;
        centered=0; normalized=0; max_score=0; exp_sum=0; exp_value=0;
        best_logit=0; dot_acc=0; lut_index=0;
        for (t=0; t<MAX_CONTEXT; t=t+1) begin
            for (i=0; i<D; i=i+1) begin
                x[t][i]=0; ln1[t][i]=0; q[t][i]=0; key[t][i]=0;
                value[t][i]=0; attn[t][i]=0; postattn[t][i]=0;
                ln2[t][i]=0; residual2[t][i]=0; hidden[t][i]=0;
            end
            for (f=0; f<F; f=f+1) ffn_act[t][f]=0;
            for (j=0; j<MAX_CONTEXT; j=j+1) begin
                scores[t][j]=0; probs[t][j]=0;
            end
        end
        for (i=0; i<V; i=i+1) logits[i]=0;
        next_token = TOK_EOS;

        if ((token_count > 0) && (token_count <= MAX_CONTEXT)) begin
            // Token plus learned position embeddings.
            for (t=0; t<MAX_CONTEXT; t=t+1) if (t<token_count)
                for (i=0; i<D; i=i+1)
                    x[t][i] = emb(tokens[t], i) + pos_emb(t, i);

            // Pre-attention LayerNorm, with epsilon = 4/256 = 0.015625.
            for (t=0; t<MAX_CONTEXT; t=t+1) if (t<token_count) begin
                acc=0;
                for (i=0; i<D; i=i+1) acc=acc+x[t][i];
                mean_value=acc / D;
                variance_value=0;
                for (i=0; i<D; i=i+1) begin
                    centered=x[t][i]-mean_value;
                    variance_value=variance_value+((centered*centered) >>> 8);
                end
                variance_value=variance_value / D;
                sigma_value=isqrt((variance_value+4) <<< 8);
                for (i=0; i<D; i=i+1) begin
                    centered=x[t][i]-mean_value;
                    if (sigma_value != 0) normalized=(centered <<< 8)/sigma_value;
                    else normalized=0;
                    ln1[t][i]=((normalized*gamma1(i)) >>> 8)+beta1(i);
                end
            end

            // Learned query, key, and value projections.
            for (t=0; t<MAX_CONTEXT; t=t+1) if (t<token_count)
                for (i=0; i<D; i=i+1) begin
                    acc=0;
                    for (j=0; j<D; j=j+1) acc=acc+((ln1[t][j]*wq(j,i)) >>> 8);
                    q[t][i]=acc;
                    acc=0;
                    for (j=0; j<D; j=j+1) acc=acc+((ln1[t][j]*wk(j,i)) >>> 8);
                    key[t][i]=acc;
                    acc=0;
                    for (j=0; j<D; j=j+1) acc=acc+((ln1[t][j]*wv(j,i)) >>> 8);
                    value[t][i]=acc;
                end

            // Scaled dot-product causal attention. 90/256 approximates 1/sqrt(8).
            for (t=0; t<MAX_CONTEXT; t=t+1) if (t<token_count) begin
                max_score=-2147483647;
                for (j=0; j<MAX_CONTEXT; j=j+1) if (j<=t) begin
                    dot_acc=0;
                    for (i=0; i<D; i=i+1) dot_acc=dot_acc+((q[t][i]*key[j][i]) >>> 8);
                    scores[t][j]=(dot_acc*90) >>> 8;
                    if (scores[t][j]>max_score) max_score=scores[t][j];
                end
                exp_sum=0;
                for (j=0; j<MAX_CONTEXT; j=j+1) if (j<=t) begin
                    lut_index=(max_score-scores[t][j]) >>> 6;
                    if (lut_index>32) lut_index=32;
                    exp_value=exp_lut(lut_index);
                    probs[t][j]=exp_value;
                    exp_sum=exp_sum+exp_value;
                end
                for (j=0; j<MAX_CONTEXT; j=j+1) if (j<=t)
                    probs[t][j]=(probs[t][j]*256)/exp_sum;
                for (i=0; i<D; i=i+1) begin
                    acc=0;
                    for (j=0; j<MAX_CONTEXT; j=j+1)
                        if (j<=t) acc=acc+(probs[t][j]*value[j][i])/256;
                    attn[t][i]=acc;
                end
            end

            // Output projection and attention residual.
            for (t=0; t<MAX_CONTEXT; t=t+1) if (t<token_count)
                for (i=0; i<D; i=i+1) begin
                    acc=0;
                    for (j=0; j<D; j=j+1) acc=acc+((attn[t][j]*wo(j,i)) >>> 8);
                    postattn[t][i]=x[t][i]+acc;
                end

            // Second LayerNorm, learned two-layer FFN, ReLU, FFN residual.
            for (t=0; t<MAX_CONTEXT; t=t+1) if (t<token_count) begin
                acc=0;
                for (i=0; i<D; i=i+1) acc=acc+postattn[t][i];
                mean_value=acc / D;
                variance_value=0;
                for (i=0; i<D; i=i+1) begin
                    centered=postattn[t][i]-mean_value;
                    variance_value=variance_value+((centered*centered) >>> 8);
                end
                variance_value=variance_value / D;
                sigma_value=isqrt((variance_value+4) <<< 8);
                for (i=0; i<D; i=i+1) begin
                    centered=postattn[t][i]-mean_value;
                    if (sigma_value != 0) normalized=(centered <<< 8)/sigma_value;
                    else normalized=0;
                    ln2[t][i]=((normalized*gamma2(i)) >>> 8)+beta2(i);
                end
                for (f=0; f<F; f=f+1) begin
                    acc=b1(f);
                    for (i=0; i<D; i=i+1) acc=acc+((ln2[t][i]*w1(i,f)) >>> 8);
                    if (acc>0) ffn_act[t][f]=acc;
                    else ffn_act[t][f]=0;
                end
                // Temporary FFN vector has F entries; accumulate each D output.
                for (i=0; i<D; i=i+1) begin
                    acc=b2(i);
                    for (f=0; f<F; f=f+1) acc=acc+((ffn_act[t][f]*w2(f,i)) >>> 8);
                    residual2[t][i]=postattn[t][i]+acc;
                end
            end

            // Final LayerNorm and vocabulary projection for all positions.
            for (t=0; t<MAX_CONTEXT; t=t+1) if (t<token_count) begin
                acc=0;
                for (i=0; i<D; i=i+1) acc=acc+residual2[t][i];
                mean_value=acc / D;
                variance_value=0;
                for (i=0; i<D; i=i+1) begin
                    centered=residual2[t][i]-mean_value;
                    variance_value=variance_value+((centered*centered) >>> 8);
                end
                variance_value=variance_value / D;
                sigma_value=isqrt((variance_value+4) <<< 8);
                for (i=0; i<D; i=i+1) begin
                    centered=residual2[t][i]-mean_value;
                    if (sigma_value != 0) normalized=(centered <<< 8)/sigma_value;
                    else normalized=0;
                    hidden[t][i]=((normalized*gamma3(i)) >>> 8)+beta3(i);
                end
            end

            // GPT language-model head. Only the last context position predicts
            // the next ID; argmax is greedy autoregressive decoding.
            t=token_count-1;
            for (i=0; i<V; i=i+1) begin
                acc=lmb(i);
                for (j=0; j<D; j=j+1) acc=acc+((hidden[t][j]*lm(j,i)) >>> 8);
                logits[i]=acc;
            end
            best_logit=logits[0];
            next_token=0;
            for (i=1; i<V; i=i+1)
                if (logits[i]>best_logit) begin best_logit=logits[i]; next_token=i; end
        end
    end

    // Token-level autoregressive interface: accept prompt IDs, then emit one
    // predicted ID each cycle. EOS ends the response and resets the context.
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= ST_LOAD;
            token_count <= 0;
            out_valid <= 1'b0;
            out_token <= 0;
            done <= 1'b0;
            for (reset_idx=0; reset_idx<MAX_CONTEXT; reset_idx=reset_idx+1) tokens[reset_idx] <= 0;
        end else begin
            out_valid <= 1'b0;
            done <= 1'b0;
            if (state == ST_LOAD) begin
                if (in_valid && in_ready) begin
                    if ((in_token < V) && (token_count < MAX_CONTEXT)) begin
                        tokens[token_count] <= in_token;
                        token_count <= token_count + 1;
                        if (in_last) state <= ST_GEN;
                    end else begin
                        token_count <= 0;
                        done <= 1'b1;
                    end
                end
            end else begin
                if (next_token == TOK_EOS) begin
                    done <= 1'b1;
                    state <= ST_LOAD;
                    token_count <= 0;
                end else if (token_count < MAX_CONTEXT) begin
                    out_token <= next_token;
                    out_valid <= 1'b1;
                    tokens[token_count] <= next_token;
                    token_count <= token_count + 1;
                end else begin
                    done <= 1'b1;
                    state <= ST_LOAD;
                    token_count <= 0;
                end
            end
        end
    end

    always_comb in_ready = (state == ST_LOAD);
endmodule

`default_nettype wire
