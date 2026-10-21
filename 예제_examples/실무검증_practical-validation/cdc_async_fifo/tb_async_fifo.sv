`timescale 1ns/1ps
module tb_async_fifo;
    parameter integer BUG_MODE = 0;
    reg wclk = 0, rclk = 0;
    always #5 wclk = ~wclk;  // 10 ns write 주기입니다.
    always #7 rclk = ~rclk;  // 14 ns read 주기입니다.
    reg reset_all = 0, reset_write_request = 0;
    reg wen = 0, ren = 0;
    reg [31:0] wdata = 0;
    wire [31:0] rdata;
    wire full, empty, wfire, rfire, wr_reset, rd_reset;
    wire [2:0] wbin, rbin, wgray, rgray, rq1, rq2, wq1, wq2;
    async_fifo #(.BUG_MODE(BUG_MODE)) dut (.*);
    reg [32:0] writes [0:199];
    reg reads [0:149];
    integer wi, ri, fd;
    initial begin
        $readmemh("writes.hex", writes);
        $readmemb("reads.bin", reads);
        fd = $fopen("trace.csv", "w");
        if (!fd) $fatal(1, "cannot open trace.csv");
        $fdisplay(fd, "time,domain,reset_all,reset_write_request,local_reset,enable,flag,fire,data,bin,gray,sync1,sync2,remote_gray");
        #1 reset_all = 1;  // 초기값에 의존하지 않고 실제 reset 상승 전이를 만듭니다.
        #21 reset_all = 0;
        #980 reset_all = 1;  // 1002 ns: 어느 상승 edge에도 맞추지 않습니다.
        #30 reset_all = 0;
        #470 reset_write_request = 1;  // 1502 ns: 정상 설정은 양쪽을 flush합니다.
        #30 reset_write_request = 0;
        #668;
        $fclose(fd);
        $finish;
    end
    initial begin
        for (wi = 0; wi < 200; wi = wi + 1) begin
            @(negedge wclk); {wen, wdata} = writes[wi];
        end
        @(negedge wclk); wen = 0;
    end
    initial begin
        for (ri = 0; ri < 150; ri = ri + 1) begin
            @(negedge rclk); ren = reads[ri];
        end
        @(negedge rclk); ren = 0;
    end
    // Active 영역에서 기록하므로 포인터/플래그/읽기 값은 NBA 갱신 전 값입니다.
    always @(posedge wclk)
        $fdisplay(fd, "%0d,W,%0d,%0d,%0d,%0d,%0d,%0d,%08h,%0d,%0d,%0d,%0d,%0d",
                  $time, reset_all, reset_write_request, wr_reset, wen, full, wfire,
                  wdata, wbin, wgray, rq1, rq2, rgray);
    always @(posedge rclk)
        $fdisplay(fd, "%0d,R,%0d,%0d,%0d,%0d,%0d,%0d,%08h,%0d,%0d,%0d,%0d,%0d",
                  $time, reset_all, reset_write_request, rd_reset, ren, empty, rfire,
                  rfire ? rdata : 32'b0, rbin, rgray, wq1, wq2, wgray);
endmodule
