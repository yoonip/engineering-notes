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
    localparam logic [1663:0] EMB_ROM = {
        16'hFEE8, 16'hFF85, 16'hFFE8, 16'h00F6, 16'h005C, 16'h00A8, 16'h009F, 16'hFFC8,
        16'h002E, 16'h001E, 16'hFFCA, 16'h001B, 16'h003E, 16'hFFF3, 16'h0044, 16'h0001,
        16'hFF96, 16'h0063, 16'h00EF, 16'hFF15, 16'hFFAB, 16'h00DC, 16'h0095, 16'h00AE,
        16'hFF7E, 16'h0002, 16'h00DC, 16'hFEE9, 16'hFF66, 16'h004D, 16'h007E, 16'h0075,
        16'h007B, 16'h0074, 16'hFF64, 16'h00FB, 16'hFF32, 16'hFF38, 16'h0009, 16'h007A,
        16'hFF3C, 16'hFFB2, 16'h0059, 16'h0002, 16'h00D3, 16'h001C, 16'h00C6, 16'hFF4A,
        16'h00CA, 16'h0133, 16'h010B, 16'hFEFD, 16'hFF87, 16'hFF5E, 16'h007A, 16'hFFA3,
        16'h0012, 16'h005B, 16'h005B, 16'hFFF3, 16'h009F, 16'hFF8E, 16'hFF10, 16'hFF58,
        16'h0064, 16'hFFAD, 16'hFF6C, 16'hFFDC, 16'hFFE3, 16'h0051, 16'hFFE4, 16'hFF55,
        16'h000F, 16'h00C4, 16'hFFD9, 16'hFFDD, 16'h008C, 16'hFF51, 16'h0043, 16'h0007,
        16'hFFEB, 16'hFF55, 16'h0062, 16'h003C, 16'hFF54, 16'h009E, 16'h0069, 16'h0032,
        16'hFF8B, 16'hFFD6, 16'h0029, 16'h0081, 16'h003C, 16'hFFB4, 16'h007D, 16'hFF69,
        16'h0027, 16'hFFC3, 16'h0077, 16'h0023, 16'h0006, 16'h001E, 16'h0003, 16'hFFBE
    };

    localparam logic [1023:0] POS_ROM = {
        16'hFFFE, 16'hFFDF, 16'hFFD3, 16'h0007, 16'hFFEE, 16'h0054, 16'hFFEC, 16'h0014,
        16'h0072, 16'h000B, 16'h0021, 16'hFF6D, 16'hFF8E, 16'h00BA, 16'h0059, 16'hFFF9,
        16'hFF91, 16'h00D6, 16'hFFEC, 16'h0060, 16'hFF5C, 16'h0070, 16'h000E, 16'h002E,
        16'hFFFA, 16'h000C, 16'h0024, 16'h0030, 16'h0001, 16'h0018, 16'h005D, 16'hFFF0,
        16'hFFC6, 16'h001F, 16'h00FE, 16'hFF60, 16'h0002, 16'hFF82, 16'h0088, 16'hFF70,
        16'h00DD, 16'h0026, 16'hFFE1, 16'hFFF4, 16'h005E, 16'hFFFF, 16'hFF70, 16'hFF60,
        16'hFFC3, 16'h002A, 16'h0064, 16'h0058, 16'hFFCD, 16'hFFE0, 16'h0019, 16'hFFE7,
        16'hFFCD, 16'h0027, 16'h003D, 16'h00B9, 16'h0022, 16'hFFB1, 16'h008C, 16'hFFD7
    };

    localparam logic [127:0] GAMMA1_ROM = {
        16'h0072, 16'h00C8, 16'h0079, 16'h0036, 16'h00F2, 16'h010A, 16'h009C, 16'h005A
    };

    localparam logic [127:0] BETA1_ROM = {
        16'h0013, 16'hFFF1, 16'h0060, 16'h0051, 16'hFFDB, 16'h002B, 16'h0061, 16'h0010
    };

    localparam logic [127:0] GAMMA2_ROM = {
        16'h00B4, 16'h00D1, 16'h0135, 16'h014E, 16'h0163, 16'h00ED, 16'h00FC, 16'h00DE
    };

    localparam logic [127:0] BETA2_ROM = {
        16'h0019, 16'h0068, 16'hFFF2, 16'hFF92, 16'h003F, 16'h003C, 16'h0023, 16'hFF41
    };

    localparam logic [127:0] GAMMA3_ROM = {
        16'h030D, 16'h0240, 16'h01F4, 16'h01F7, 16'h0248, 16'h0321, 16'h0295, 16'h0300
    };

    localparam logic [127:0] BETA3_ROM = {
        16'hFFAB, 16'hFFD4, 16'hFF5A, 16'h009E, 16'hFFA3, 16'h0060, 16'h004D, 16'hFFE1
    };

    localparam logic [1023:0] WQ_ROM = {
        16'h0079, 16'h000D, 16'hFFC5, 16'hFF70, 16'h0089, 16'hFFC0, 16'hFF79, 16'h0014,
        16'hFFB2, 16'hFFAA, 16'hFF9E, 16'hFFAE, 16'h003B, 16'hFFD6, 16'hFF80, 16'h008A,
        16'h007B, 16'h0034, 16'hFFEB, 16'hFFE1, 16'hFFC2, 16'h0028, 16'h0010, 16'hFFC2,
        16'h0065, 16'h001B, 16'h0072, 16'hFFE3, 16'h0021, 16'h0099, 16'h0056, 16'h0019,
        16'h00A7, 16'hFFB8, 16'h0049, 16'hFF8E, 16'hFFFE, 16'hFFE5, 16'hFFC6, 16'h0046,
        16'hFFF7, 16'hFF91, 16'hFFA9, 16'hFFA0, 16'hFFE9, 16'h0033, 16'hFF95, 16'h00B9,
        16'h0046, 16'h000E, 16'h0097, 16'h00DB, 16'hFFAB, 16'hFF82, 16'h009E, 16'hFF99,
        16'hFF66, 16'h006C, 16'h0038, 16'h00AA, 16'h0042, 16'hFF87, 16'hFFED, 16'hFF53
    };

    localparam logic [1023:0] WK_ROM = {
        16'hFFFE, 16'h0048, 16'h0034, 16'h0047, 16'hFFA0, 16'hFFFD, 16'h0002, 16'hFFF5,
        16'h0011, 16'hFFF1, 16'hFF35, 16'hFF9B, 16'h0031, 16'h0050, 16'hFF8D, 16'h0058,
        16'h003A, 16'h001A, 16'hFFCA, 16'h0012, 16'h0047, 16'hFFFE, 16'hFFC9, 16'h006B,
        16'hFF21, 16'h001F, 16'hFFFE, 16'h0069, 16'h0042, 16'hFF8D, 16'hFFBD, 16'hFF94,
        16'h0010, 16'h0062, 16'h0003, 16'h00B5, 16'h0043, 16'hFF70, 16'h0056, 16'hFEF5,
        16'hFFE1, 16'hFF88, 16'h001E, 16'hFFA3, 16'h0015, 16'h0063, 16'h004C, 16'h0053,
        16'h0039, 16'hFFB3, 16'hFFDE, 16'hFFF7, 16'hFF60, 16'hFFE5, 16'h0052, 16'h000D,
        16'h0058, 16'hFFE7, 16'hFFF2, 16'hFF89, 16'h001C, 16'hFFCE, 16'hFF46, 16'h001D
    };

    localparam logic [1023:0] WV_ROM = {
        16'h0008, 16'h0008, 16'hFF9D, 16'hFFC9, 16'h0043, 16'h0051, 16'h0080, 16'h002F,
        16'h0027, 16'h004F, 16'hFF9C, 16'h008A, 16'h0004, 16'h005E, 16'hFF9B, 16'hFFE9,
        16'hFFCE, 16'hFF69, 16'hFFF0, 16'h006B, 16'hFFFE, 16'hFF90, 16'hFFD2, 16'hFFA0,
        16'h0057, 16'hFF99, 16'h004E, 16'h0033, 16'h003B, 16'hFF9F, 16'h0018, 16'h0018,
        16'h0023, 16'h00B4, 16'hFFBE, 16'h006F, 16'hFF9B, 16'h0004, 16'hFF7D, 16'hFF98,
        16'h0001, 16'hFF22, 16'h0065, 16'hFF2E, 16'h0067, 16'hFFE9, 16'h0078, 16'hFFB2,
        16'hFF92, 16'hFFB0, 16'h00A1, 16'hFFF9, 16'hFFF6, 16'h0000, 16'h0039, 16'hFF7C,
        16'h0027, 16'hFFF7, 16'hFFD6, 16'hFFF2, 16'h000E, 16'hFFDC, 16'hFF76, 16'hFFB3
    };

    localparam logic [1023:0] WO_ROM = {
        16'h000E, 16'h0004, 16'hFFE8, 16'h0008, 16'hFFEB, 16'hFFE9, 16'h0015, 16'h000E,
        16'h0065, 16'h0003, 16'hFFA7, 16'h0007, 16'hFFE0, 16'hFFB0, 16'h0112, 16'h0018,
        16'hFF84, 16'hFFBB, 16'h0058, 16'hFFD7, 16'h0071, 16'h0012, 16'hFF7A, 16'h005D,
        16'h0033, 16'hFFA8, 16'hFFB2, 16'hFFAB, 16'h00A4, 16'hFFF8, 16'h00A6, 16'hFFED,
        16'hFF86, 16'h002F, 16'hFFF1, 16'h0026, 16'hFFC7, 16'hFFF1, 16'hFFC1, 16'h0062,
        16'hFF8A, 16'hFFFC, 16'hFFDA, 16'hFFED, 16'hFFA9, 16'hFFDD, 16'h001E, 16'h00BD,
        16'hFF8B, 16'hFFFE, 16'h0074, 16'h006A, 16'hFFE2, 16'h0043, 16'hFF92, 16'h008C,
        16'h004D, 16'h0039, 16'hFF8F, 16'h0021, 16'hFF76, 16'hFFBB, 16'h001A, 16'hFFE3
    };

    localparam logic [2047:0] W1_ROM = {
        16'hFFA5, 16'hFFBA, 16'hFF98, 16'hFFA1, 16'hFF76, 16'h005D, 16'hFFC2, 16'hFF7C,
        16'h0058, 16'hFFFC, 16'h000C, 16'hFF53, 16'hFFD3, 16'h0048, 16'hFFF0, 16'h002D,
        16'h0009, 16'hFF96, 16'hFF34, 16'h0049, 16'hFFA1, 16'hFF9B, 16'h0046, 16'hFF99,
        16'hFFDC, 16'h00AD, 16'hFFAE, 16'hFFDF, 16'hFFE6, 16'hFFCE, 16'hFFF3, 16'hFF20,
        16'h0063, 16'hFFA6, 16'h008C, 16'h001E, 16'h001A, 16'h0021, 16'hFF87, 16'h000D,
        16'h003E, 16'h00E9, 16'hFF93, 16'h0030, 16'hFFD8, 16'h008F, 16'hFF51, 16'h00AE,
        16'hFFC1, 16'h00CF, 16'h0045, 16'h0017, 16'hFF39, 16'hFFEE, 16'h00C5, 16'h0033,
        16'h0015, 16'h00AE, 16'h00B6, 16'h007C, 16'h003D, 16'h002B, 16'h0055, 16'h0055,
        16'h0001, 16'hFF54, 16'h008F, 16'hFFB3, 16'hFEF6, 16'h001F, 16'hFEFC, 16'hFFE3,
        16'h0035, 16'hFFB8, 16'hFF6C, 16'h002C, 16'hFFFC, 16'h0075, 16'hFF36, 16'h0050,
        16'hFFE6, 16'hFFE5, 16'h006E, 16'h0008, 16'h00DD, 16'hFF9C, 16'hFFC2, 16'hFFE4,
        16'h0045, 16'h0040, 16'hFFBD, 16'hFFED, 16'h004B, 16'hFFA5, 16'hFF84, 16'hFFC3,
        16'h0050, 16'h002F, 16'h0012, 16'hFFA9, 16'hFFF9, 16'hFFFB, 16'hFFFA, 16'hFFB9,
        16'hFF98, 16'hFF03, 16'h001C, 16'hFFC0, 16'hFFAB, 16'hFFB3, 16'h0077, 16'h005F,
        16'hFFE9, 16'h005F, 16'hFFF2, 16'h002A, 16'h0047, 16'h00A3, 16'h0038, 16'h0040,
        16'hFFEE, 16'h0089, 16'h00A2, 16'h0070, 16'h004F, 16'h0018, 16'h0098, 16'h001D
    };

    localparam logic [255:0] B1_ROM = {
        16'hFFDD, 16'hFFC7, 16'hFFFE, 16'hFF8F, 16'hFFE2, 16'hFFD8, 16'h0059, 16'hFF8F,
        16'hFF7B, 16'hFFFF, 16'hFFA1, 16'hFF98, 16'hFF97, 16'hFFC1, 16'hFFCB, 16'hFFE0
    };

    localparam logic [2047:0] W2_ROM = {
        16'hFF71, 16'h0043, 16'h001D, 16'h007D, 16'hFFBC, 16'hFFD5, 16'h003F, 16'h0011,
        16'hFFA6, 16'hFF84, 16'hFFDB, 16'hFFDC, 16'h009F, 16'h0071, 16'h001E, 16'h00D5,
        16'hFF47, 16'hFFA5, 16'h0041, 16'h0052, 16'h00A4, 16'h0049, 16'h0006, 16'hFFD0,
        16'hFFAF, 16'hFFE0, 16'hFFE1, 16'h002D, 16'h001C, 16'hFFF1, 16'h0073, 16'h0013,
        16'h00A5, 16'hFF48, 16'h0027, 16'hFF66, 16'hFF33, 16'h008E, 16'h007E, 16'h001A,
        16'h0041, 16'hFFFD, 16'hFFDD, 16'hFFF5, 16'hFFBA, 16'hFF91, 16'hFF97, 16'h006C,
        16'hFF8D, 16'hFFFA, 16'h004B, 16'h0045, 16'h001F, 16'h0030, 16'h0018, 16'h011C,
        16'hFF6A, 16'hFFDB, 16'hFFF0, 16'hFFC8, 16'h004E, 16'h0030, 16'h0027, 16'h002F,
        16'h000C, 16'h0032, 16'hFFDE, 16'hFFED, 16'hFFDC, 16'h0054, 16'hFFCE, 16'hFFAA,
        16'h015F, 16'h00B3, 16'hFFDC, 16'h0087, 16'hFF9C, 16'hFF41, 16'h0021, 16'hFF46,
        16'hFFE8, 16'hFF8B, 16'hFF7E, 16'h0014, 16'h000F, 16'h0078, 16'hFFA2, 16'h0049,
        16'hFF67, 16'h0032, 16'hFFBD, 16'hFF86, 16'h00A8, 16'h0036, 16'h00AD, 16'hFFE3,
        16'h001C, 16'h000E, 16'h0014, 16'hFFF7, 16'hFFF2, 16'hFFB6, 16'hFFF8, 16'h0033,
        16'h0098, 16'h0053, 16'hFFF6, 16'h0002, 16'h005E, 16'h0024, 16'h0008, 16'hFF4A,
        16'hFFCA, 16'h0073, 16'hFFF1, 16'h0015, 16'hFFC3, 16'h0041, 16'hFF92, 16'h004E,
        16'h0003, 16'hFFCE, 16'h000C, 16'h0010, 16'hFFF7, 16'hFF91, 16'h005F, 16'hFFE8
    };

    localparam logic [127:0] B2_ROM = {
        16'h002E, 16'h003A, 16'h0044, 16'h003D, 16'hFFDF, 16'hFFDA, 16'hFFFA, 16'hFFD3
    };

    localparam logic [1663:0] LM_ROM = {
        16'h01A1, 16'h004C, 16'hFF15, 16'h003A, 16'hFECC, 16'hFF71, 16'h00D8, 16'h0061,
        16'h005D, 16'h004F, 16'h0056, 16'h007F, 16'h005E, 16'hFF3F, 16'hFF54, 16'hFF75,
        16'h009F, 16'hFF28, 16'h0142, 16'h009B, 16'h002A, 16'hFFFE, 16'h0051, 16'hFFFE,
        16'hFFD2, 16'hFFEA, 16'hFF53, 16'h00F6, 16'hFF71, 16'hFFA5, 16'h00DF, 16'h017A,
        16'h0057, 16'h00C5, 16'h00C6, 16'h00D8, 16'h00AF, 16'h00EE, 16'h008B, 16'hFF83,
        16'hFEE4, 16'h001C, 16'h00CC, 16'h0086, 16'hFE92, 16'h003C, 16'hFF1B, 16'hFF0D,
        16'hFF3E, 16'hFF10, 16'hFF4E, 16'hFF23, 16'h0135, 16'hFEE6, 16'hFFCF, 16'hFF66,
        16'h0162, 16'hFF64, 16'h0011, 16'h0098, 16'h00C3, 16'h00BC, 16'h0089, 16'h00D2,
        16'h007F, 16'h0039, 16'h0157, 16'h00C1, 16'hFEA8, 16'h0010, 16'hFEBD, 16'h00B6,
        16'hFFB1, 16'hFF91, 16'hFFBF, 16'hFF9C, 16'hFF8E, 16'hFFAD, 16'h009C, 16'h00B0,
        16'hFF8E, 16'h0042, 16'h00B9, 16'h0094, 16'hFE55, 16'hFFC5, 16'hFFB2, 16'hFFD4,
        16'hFFAF, 16'hFFB2, 16'hFFB3, 16'hFF3F, 16'h0033, 16'h00D9, 16'h0065, 16'hFF4F,
        16'hFF06, 16'hFF07, 16'h0072, 16'h0073, 16'h0073, 16'h0060, 16'h0080, 16'h0050
    };

    localparam logic [207:0] LMB_ROM = {
        16'h0027, 16'h0029, 16'h0019, 16'h002D, 16'h000C, 16'h0014, 16'h003D, 16'hFF63,
        16'hFF56, 16'hFF66, 16'hFF56, 16'hFF38, 16'hFF44
    };

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
