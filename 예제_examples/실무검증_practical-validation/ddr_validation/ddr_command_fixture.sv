`timescale 1ns/1ps
// 파일 구동·명령 출력·메모리 결함 대조를 위한 비합성 SV fixture입니다.
// 실제 DDR 핀/PHY/버스트/아날로그 셀 모델은 포함하지 않습니다.
module ddr_command_fixture;
    parameter integer FAULT = 0;
    parameter integer CYCLES = 256;
    reg clk = 0;
    always #5 clk = ~clk;
    reg [63:0] program_words [0:CYCLES-1];
    reg [15:0] memory [0:31];
    reg [15:0] response_data [0:CYCLES+1];
    reg [15:0] response_tag [0:CYCLES+1];
    reg response_valid [0:CYCLES+1];
    integer open_row [0:1];
    integer fd, cycle, i, op, bank, row, col, address;
    reg [15:0] tag, data, observed;
    initial begin
        $readmemh("program.hex", program_words);
        fd = $fopen("trace.csv", "w");
        if (!fd) $fatal(1, "cannot open trace.csv");
        $fdisplay(fd, "cycle,op,bank,row,col,tag,wdata,rvalid,rtag,rdata");
        open_row[0] = -1; open_row[1] = -1;
        for (i = 0; i < CYCLES+2; i = i+1) response_valid[i] = 0;
        // memory는 초기화하지 않습니다. 쓰지 않은 셀의 X를 그대로 관측합니다.
        for (cycle = 0; cycle < CYCLES; cycle = cycle+1) begin
            @(posedge clk);
            op = int'(program_words[cycle][39:37]);
            bank = int'(program_words[cycle][36]);
            row = int'(program_words[cycle][35:34]);
            col = int'(program_words[cycle][33:32]);
            tag = program_words[cycle][31:16]; data = program_words[cycle][15:0];
            if (FAULT == 5 && cycle == CYCLES/2) begin
                $fclose(fd); $finish;  // exit 0인 미완성 출력 대조입니다.
            end
            observed = (FAULT == 4) ? 16'hxxxx : response_data[cycle];
            $fdisplay(fd, "%0d,%0d,%0d,%0d,%0d,%0d,%04h,%0d,%0d,%04h",
                cycle, op, bank, row, col, tag, data,
                (FAULT == 3) ? 1'b0 : response_valid[cycle],
                response_valid[cycle] && FAULT != 3 ? response_tag[cycle] : 16'b0,
                response_valid[cycle] && FAULT != 3 ? observed : 16'b0);
            case (op)
                1: open_row[bank] = row;  // ACT: 해당 bank의 행을 선택합니다.
                2, 3: begin  // WR/RD: 선택된 행과 column으로 배열을 찾습니다.
                    address = bank*16 + open_row[bank]*4 + col;
                    if (FAULT == 2) address = address & ~2;  // column bit 1 alias입니다.
                    if (op == 2 && open_row[bank] >= 0)
                        memory[address] = (FAULT == 1) ? (data & 16'hfffe) : data;
                    if (op == 3) begin
                        response_valid[cycle+2] = 1;
                        response_tag[cycle+2] = tag;
                        response_data[cycle+2] = (open_row[bank] >= 0) ? memory[address] : 16'hxxxx;
                    end
                end
                4: open_row[bank] = -1;  // PRE: 행을 닫습니다.
                default: begin end  // NOP/REF는 이 배열의 값을 바꾸지 않습니다.
            endcase
        end
        $fclose(fd);
        $finish;
    end
endmodule
