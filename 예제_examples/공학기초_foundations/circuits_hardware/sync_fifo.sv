module sync_fifo #(
    parameter integer WIDTH = 8,
    parameter integer DEPTH = 4,
    parameter integer PTR_W = (DEPTH <= 1) ? 1 : $clog2(DEPTH),
    parameter integer COUNT_W = $clog2(DEPTH + 1)
) (
    input  logic clk,
    input  logic rst,
    input  logic wr_en,
    input  logic rd_en,
    input  logic [WIDTH-1:0] wr_data,
    output logic [WIDTH-1:0] rd_data,
    output logic wr_ack,
    output logic rd_valid,
    output logic full,
    output logic empty,
    output logic [COUNT_W-1:0] count
);
    logic [WIDTH-1:0] memory [0:DEPTH-1];
    logic [PTR_W-1:0] read_pointer, write_pointer;
    logic take_write, take_read;

    assign full = (count == DEPTH);
    assign empty = (count == 0);
    // 클록 직전의 플래그로 각각 수락한다. 빈 상태의 직접 우회는 없다.
    assign take_write = wr_en && !full;
    assign take_read = rd_en && !empty;

    always_ff @(posedge clk) begin
        if (rst) begin
            read_pointer <= '0;
            write_pointer <= '0;
            count <= '0;
            rd_data <= '0;
            wr_ack <= 1'b0;
            rd_valid <= 1'b0;
        end else begin
            wr_ack <= take_write;
            rd_valid <= take_read;
            if (take_write) begin
                memory[write_pointer] <= wr_data;
                write_pointer <= (write_pointer == DEPTH-1) ? '0 : write_pointer + 1'b1;
            end
            if (take_read) begin
                rd_data <= memory[read_pointer];
                read_pointer <= (read_pointer == DEPTH-1) ? '0 : read_pointer + 1'b1;
            end
            case ({take_write, take_read})
                2'b10: count <= count + 1'b1;
                2'b01: count <= count - 1'b1;
                default: count <= count;
            endcase
        end
    end
endmodule
