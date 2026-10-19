// RV32I, 32bit, little-endian, 순차 다중사이클 CPU. 캐시/CSR/인터럽트는 없음.
// 외부 bus: valid && ready인 clock에서 1회 완료. ready 전에는 요청을 유지한다.
module rv32_cpu #(
    parameter logic [31:0] RESET_PC = 32'h0000_0000
)(
    input  logic clk, rst_n,
    output logic mem_valid, mem_write,
    output logic [31:0] mem_addr, mem_wdata,
    output logic [3:0] mem_wstrb,
    input  logic mem_ready, mem_error,
    input  logic [31:0] mem_rdata,
    output logic halted,
    output logic [31:0] trap_cause, trap_pc,
    output logic commit_valid,
    output logic [31:0] commit_pc, commit_instr, commit_data,
    output logic [4:0] commit_rd
);
    typedef enum logic [2:0] {FETCH, DECODE, EXECUTE, MEMORY, WRITEBACK, STOP} state_t;
    state_t state;
    logic [31:0] regs [0:31];
    logic [31:0] pc, ir, a, b, result, next_pc;
    logic [31:0] address, store_value;
    logic [4:0] destination;
    logic write_reg, load_op, store_op;
    logic [2:0] size_code;
    wire [6:0] opcode = ir[6:0];
    wire [2:0] f3 = ir[14:12];
    wire [6:0] f7 = ir[31:25];
    // signed immediate를 32bit로 sign-extension; branch/jump bit는 흩어져 있음.
    wire [31:0] imm_i = {{20{ir[31]}}, ir[31:20]};
    wire [31:0] imm_s = {{20{ir[31]}}, ir[31:25], ir[11:7]};
    wire [31:0] imm_b = {{19{ir[31]}}, ir[31], ir[7], ir[30:25], ir[11:8], 1'b0};
    wire [31:0] imm_u = {ir[31:12], 12'b0};
    wire [31:0] imm_j = {{11{ir[31]}}, ir[31], ir[19:12], ir[20], ir[30:21], 1'b0};
    logic [31:0] ex_value, ex_pc, ex_address;
    logic ex_write, ex_load, ex_store, ex_trap, taken;
    logic [31:0] ex_cause;
    logic [31:0] shifted_read;

    always_comb begin
        ex_value = 0; ex_pc = pc + 4; ex_address = 0;
        ex_write = 1; ex_load = 0; ex_store = 0;
        ex_trap = 0; ex_cause = 2; taken = 0;
        case (opcode)
            7'h37: ex_value = imm_u;       // LUI
            7'h17: ex_value = pc + imm_u;  // AUIPC
            7'h6f: begin                  // JAL: 복귀 주소 pc+4와 jump 목적지는 별도 값.
                ex_value = pc + 4; ex_pc = pc + imm_j;
            end
            7'h67: begin                  // JALR: ISA에 따라 목적지 bit0를 0으로 만든다.
                ex_value = pc + 4; ex_pc = (a + imm_i) & 32'hffff_fffe;
                if (f3 != 0) ex_trap = 1;
            end
            7'h63: begin
                ex_write = 0;
                case (f3)
                    3'h0: taken = (a == b);                   // BEQ
                    3'h1: taken = (a != b);                   // BNE
                    3'h4: taken = ($signed(a) < $signed(b));   // BLT
                    3'h5: taken = ($signed(a) >= $signed(b));  // BGE
                    3'h6: taken = (a < b);                    // BLTU
                    3'h7: taken = (a >= b);                   // BGEU
                    default: ex_trap = 1;
                endcase
                if (taken) ex_pc = pc + imm_b;
            end
            7'h13: begin
                case (f3)
                    3'h0: ex_value = a + imm_i;                       // ADDI
                    3'h2: ex_value = {31'b0, $signed(a)<$signed(imm_i)};
                    3'h3: ex_value = {31'b0, a<imm_i};                 // SLTIU
                    3'h4: ex_value = a ^ imm_i;
                    3'h6: ex_value = a | imm_i;
                    3'h7: ex_value = a & imm_i;
                    3'h1: begin
                        ex_value = a << ir[24:20];
                        if (f7 != 0) ex_trap = 1;                     // SLLI
                    end
                    3'h5: begin
                        if (f7 == 0) ex_value = a >> ir[24:20];       // SRLI
                        else if (f7 == 7'h20)
                            ex_value = $signed(a) >>> ir[24:20];      // SRAI
                        else ex_trap = 1;
                    end
                endcase
            end
            7'h33: begin
                case (f3)
                    3'h0: begin
                        if (f7 == 0) ex_value = a + b;
                        else if (f7 == 7'h20) ex_value = a - b;
                        else ex_trap = 1;
                    end
                    3'h1: ex_value = a << b[4:0];
                    3'h2: ex_value = {31'b0, $signed(a)<$signed(b)};
                    3'h3: ex_value = {31'b0, a<b};
                    3'h4: ex_value = a ^ b;
                    3'h5: begin
                        if (f7 == 0) ex_value = a >> b[4:0];
                        else if (f7 == 7'h20) ex_value = $signed(a) >>> b[4:0];
                        else ex_trap = 1;
                    end
                    3'h6: ex_value = a | b;
                    3'h7: ex_value = a & b;
                endcase
                if (f3 != 0 && f3 != 5 && f7 != 0) ex_trap = 1;
            end
            7'h03: begin
                ex_load = 1; ex_address = a + imm_i;
                if (!(f3 == 0 || f3 == 1 || f3 == 2 || f3 == 4 || f3 == 5)) ex_trap = 1;
            end
            7'h23: begin
                ex_write = 0; ex_store = 1; ex_address = a + imm_s;
                if (!(f3 == 0 || f3 == 1 || f3 == 2)) ex_trap = 1;
            end
            7'h0f: begin
                // 순차 완료 bus에는 outstanding access가 없어 FENCE가 추가 동작 불필요.
                ex_write = 0; if (f3 != 0) ex_trap = 1;
            end
            7'h73: begin
                ex_write = 0; ex_trap = 1;
                if (ir == 32'h0010_0073) ex_cause = 3;       // EBREAK
                else if (ir == 32'h0000_0073) ex_cause = 11; // ECALL: 본 EEI의 fatal trap.
            end
            default: ex_trap = 1;
        endcase
        if (!ex_trap && ex_pc[1:0] != 0) begin
            ex_trap = 1; ex_cause = 0; // RV32I는 4byte instruction alignment.
        end
        if (!ex_trap && (ex_load || ex_store) &&
            (((f3 == 1 || f3 == 5) && ex_address[0]) ||
             (f3 == 2 && ex_address[1:0] != 0))) begin
            ex_trap = 1; ex_cause = ex_store ? 6 : 4;
        end
    end

    always_comb begin
        mem_valid = 0; mem_write = 0; mem_addr = 0;
        mem_wdata = 0; mem_wstrb = 0;
        if (state == FETCH) begin mem_valid = 1; mem_addr = pc; end
        if (state == MEMORY) begin
            mem_valid = 1; mem_write = store_op;
            mem_addr = {address[31:2], 2'b00}; // bus는 aligned 32bit word를 접근.
            mem_wdata = store_value << (8 * address[1:0]);
            if (store_op) case (size_code)
                3'h0: mem_wstrb = 4'b0001 << address[1:0]; // SB
                3'h1: mem_wstrb = 4'b0011 << address[1:0]; // SH
                3'h2: mem_wstrb = 4'b1111;                 // SW
                default: mem_wstrb = 0;
            endcase
        end
        shifted_read = mem_rdata >> (8 * address[1:0]);
        halted = (state == STOP);
    end

    always_ff @(posedge clk) begin
        if (!rst_n) begin
            state <= FETCH; pc <= RESET_PC; ir <= 0; a <= 0; b <= 0;
            result <= 0; next_pc <= 0; address <= 0; store_value <= 0;
            destination <= 0; write_reg <= 0; load_op <= 0; store_op <= 0;
            size_code <= 0; trap_cause <= 0; trap_pc <= 0;
            commit_valid <= 0; commit_pc <= 0; commit_instr <= 0;
            commit_rd <= 0; commit_data <= 0;
            for (int i=0; i<32; i++) regs[i] <= 0;
        end else begin
            commit_valid <= 0;
            regs[0] <= 0;  // x0는 항상 0. rd=0인 쓰기로도 바뀌지 않는다.
            case (state)
                FETCH: if (mem_ready) begin
                    if (mem_error) begin state <= STOP; trap_cause <= 1; trap_pc <= pc; end
                    else begin ir <= mem_rdata; state <= DECODE; end
                end
                DECODE: begin
                    a <= regs[ir[19:15]]; b <= regs[ir[24:20]]; state <= EXECUTE;
                end
                EXECUTE: begin
                    if (ex_trap) begin state <= STOP; trap_cause <= ex_cause; trap_pc <= pc; end
                    else begin
                        result <= ex_value; next_pc <= ex_pc;
                        destination <= ir[11:7]; write_reg <= ex_write;
                        load_op <= ex_load; store_op <= ex_store;
                        address <= ex_address; store_value <= b; size_code <= f3;
                        if (ex_load || ex_store) state <= MEMORY;
                        else state <= WRITEBACK;
                    end
                end
                MEMORY: if (mem_ready) begin
                    if (mem_error) begin
                        state <= STOP; trap_cause <= store_op ? 7 : 5; trap_pc <= pc;
                    end else begin
                        if (load_op) case (size_code)
                            3'h0: result <= {{24{shifted_read[7]}}, shifted_read[7:0]};
                            3'h1: result <= {{16{shifted_read[15]}}, shifted_read[15:0]};
                            3'h2: result <= shifted_read;
                            3'h4: result <= {24'b0, shifted_read[7:0]};
                            3'h5: result <= {16'b0, shifted_read[15:0]};
                            default: result <= 0;
                        endcase
                        state <= WRITEBACK;
                    end
                end
                WRITEBACK: begin
                    if (write_reg && destination != 0) regs[destination] <= result;
                    commit_valid <= 1; commit_pc <= pc; commit_instr <= ir;
                    commit_rd <= write_reg ? destination : 0; commit_data <= result;
                    pc <= next_pc; state <= FETCH;
                end
                STOP: state <= STOP;
                default: state <= STOP;
            endcase
        end
    end
endmodule
