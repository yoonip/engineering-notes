`timescale 1ns/1ps
// 깊이 4, 비동기 읽기 배열을 사용하는 교육용 dual-clock FIFO입니다.
module async_fifo #(parameter integer BUG_MODE = 0) (
    input wire wclk, rclk, reset_all, reset_write_request,
    input wire wen, ren,
    input wire [31:0] wdata,
    output wire [31:0] rdata,
    output reg full, empty,
    output wire wfire, rfire,
    output wire wr_reset, rd_reset,
    output reg [2:0] wbin, rbin, wgray, rgray,
    output reg [2:0] rq1, rq2, wq1, wq2
);
    reg [1:0] wr_release, rd_release;
    wire wr_request = reset_all | reset_write_request;
    // 변이 3: writer만 초기화하여 공유된 FIFO 세대를 어긋나게 합니다.
    wire rd_request = reset_all | ((BUG_MODE == 3) ? 1'b0 : reset_write_request);
    always @(posedge wclk or posedge wr_request)
        if (wr_request) wr_release <= 2'b11;
        else wr_release <= {wr_release[0], 1'b0};
    always @(posedge rclk or posedge rd_request)
        if (rd_request) rd_release <= 2'b11;
        else rd_release <= {rd_release[0], 1'b0};
    assign wr_reset = wr_release[1];
    assign rd_reset = rd_release[1];

    reg [31:0] memory [0:3];
    assign wfire = wen && !full && !wr_reset;
    // 변이 2는 빈 FIFO에서 읽기를 수락하는 기능 오류입니다.
    assign rfire = ren && ((BUG_MODE == 2) || !empty) && !rd_reset;
    assign rdata = memory[rbin[1:0]];
    wire [2:0] wn = wbin + {2'b00, wfire};
    wire [2:0] rn = rbin + {2'b00, rfire};
    wire [2:0] wg = (wn >> 1) ^ wn;
    wire [2:0] rg = (rn >> 1) ^ rn;
    // Gray 포인터의 full 판정은 상위 두 비트를 함께 반전합니다.
    wire [2:0] full_target = (BUG_MODE == 1) ? {~rq2[2], rq2[1:0]}
                                                   : {~rq2[2:1], rq2[0]};
    always @(posedge wclk or posedge wr_reset) begin
        if (wr_reset) begin
            wbin <= 3'b000; wgray <= 3'b000; full <= 1'b0;
            rq1 <= 3'b000; rq2 <= 3'b000;
        end else begin
            rq1 <= rgray; rq2 <= rq1;  // 읽기 포인터를 write 도메인에 2단 전달합니다.
            wbin <= wn; wgray <= wg; full <= (wg == full_target);
            if (wfire) memory[wbin[1:0]] <= wdata;
        end
    end
    always @(posedge rclk or posedge rd_reset) begin
        if (rd_reset) begin
            rbin <= 3'b000; rgray <= 3'b000; empty <= 1'b1;
            wq1 <= 3'b000; wq2 <= 3'b000;
        end else begin
            wq1 <= wgray; wq2 <= wq1;  // 쓰기 포인터를 read 도메인에 2단 전달합니다.
            rbin <= rn; rgray <= rg; empty <= (rg == wq2);
        end
    end
endmodule
