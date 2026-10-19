`timescale 1ns/1ps
module tb_cpu;
    localparam logic [31:0] EXPECTED_SIGNATURE = `EXPECTED_SIGNATURE;
    logic clk=0, rst_n=0;
    always #5 clk=~clk; // 설명용 100MHz clock. 실제 FPGA timing closure 결과가 아님.
    wire valid, write_en, ready, bus_error, halted, commit;
    wire [31:0] addr, wdata, rdata, cause, fault_pc, cpc, cir, cdata;
    wire [3:0] strobe;
    wire [4:0] crd;
    logic [31:0] ram[0:16383];
    logic [31:0] mailbox[0:3];
    integer waits=0, cycles=0, retired=0, ef, rc;
    logic [31:0] random_state=1;
    logic last_wait=0;
    logic [68:0] previous_request;
    logic [31:0] expected_pc, expected_ir, expected_data;
    logic [31:0] expected_fault_pc;
    logic [4:0] expected_rd;
    integer expected_cause=3, seed=1;
    string image, golden;
    assign ready = valid && (waits == int'(random_state[1:0]));
    // RAM은 64KiB. mailbox는 store만 받는 별도 MMIO 영역이다.
    assign bus_error = addr >= 32'h10000 &&
                      !(write_en && addr >= 32'h10000 && addr < 32'h10010);
    assign rdata = addr < 32'h10000 ? ram[addr[15:2]] : 0;
    rv32_cpu dut(clk, rst_n, valid, write_en, addr, wdata, strobe,
                 ready, bus_error, rdata, halted, cause, fault_pc,
                 commit, cpc, cir, cdata, crd);

    initial begin
        if (!$value$plusargs("IMAGE=%s", image)) $fatal(1,"IMAGE missing");
        if (!$value$plusargs("GOLDEN=%s", golden)) $fatal(1,"GOLDEN missing");
        rc=$value$plusargs("CAUSE=%d", expected_cause);
        if (!$value$plusargs("TRAP_PC=%h", expected_fault_pc)) $fatal(1,"TRAP_PC missing");
        rc=$value$plusargs("SEED=%d", seed); random_state=seed;
        for (int i=0;i<16384;i++) ram[i]=0;
        for (int i=0;i<4;i++) mailbox[i]=0;
        $readmemh(image,ram);
        ef=$fopen(golden,"r"); if (!ef) $fatal(1,"golden not opened");
        if ($test$plusargs("VCD")) begin $dumpfile("cpu.vcd"); $dumpvars(0,tb_cpu); end
        repeat(4) @(negedge clk); rst_n=1;
    end

    always @(posedge clk) begin
        if (!rst_n) begin waits<=0; last_wait<=0; end
        else begin
            cycles<=cycles+1;
            if (cycles>2000000) $fatal(1,"timeout: no completion");
            // backpressure 중 address/data/strobe가 바뀌면 실제 장치에서 데이터 손상 가능.
            if (last_wait && (!valid || previous_request != {write_en,addr,wdata,strobe}))
                $fatal(1,"bus request changed while waiting");
            last_wait <= valid && !ready;
            previous_request <= {write_en,addr,wdata,strobe};
            if (valid && ready) begin
                waits<=0;
                random_state <= {random_state[30:0],
                                 random_state[31]^random_state[21]^random_state[1]^random_state[0]};
                if (write_en && !bus_error) begin
                    if (addr < 32'h10000) begin
                        for (int lane=0;lane<4;lane++)
                            if (strobe[lane]) ram[addr[15:2]][lane*8+:8] <= wdata[lane*8+:8];
                    end else mailbox[addr[3:2]] <= wdata;
                end
            end else if (valid) waits<=waits+1;
            if (dut.regs[0] !== 0) $fatal(1,"x0 corrupted");
        end
    end

    // NBA 갱신 뒤 negedge에서 retire trace를 읽는다. golden은 독립 Python ISA 결과.
    always @(negedge clk) if (rst_n) begin
        if (commit) begin
            rc=$fscanf(ef,"%h %h %h %h\n",expected_pc,expected_ir,expected_rd,expected_data);
            if (rc != 4) $fatal(1,"unexpected extra commit");
            if (cpc!==expected_pc || cir!==expected_ir || crd!==expected_rd ||
                (crd!=0 && cdata!==expected_data))
                $fatal(1,"trace mismatch pc=%h instr=%h rd=%d data=%h expected=%h",
                       cpc,cir,crd,cdata,expected_data);
            retired=retired+1;
        end
        if (halted) begin
            if (cause != expected_cause) $fatal(1,"wrong trap cause=%d",cause);
            if (fault_pc !== expected_fault_pc) $fatal(1,"wrong trap pc=%h",fault_pc);
            rc=$fscanf(ef,"%h %h %h %h\n",expected_pc,expected_ir,expected_rd,expected_data);
            if (rc==4) $fatal(1,"missing commits before halt");
            if ($test$plusargs("MAILBOX") &&
                (mailbox[0]!==32'hcafebabe || mailbox[1]!==0 ||
                 mailbox[2]!==EXPECTED_SIGNATURE || mailbox[3]!==1024))
                $fatal(1,"mailbox validation failed");
            $display("PASS seed=%0d cause=%0d retired=%0d cycles=%0d",seed,cause,retired,cycles);
            $fclose(ef); $finish;
        end
    end
endmodule
