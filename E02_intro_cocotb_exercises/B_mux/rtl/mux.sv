
`timescale 1ns/1ps

module mux(
    input                       clk,
    input logic unsigned [3:0]  A,
    input logic unsigned [1:0]  sel,
    output logic unsigned       out
);

    always @(posedge clk)
        out <= A[sel];

    initial begin
        $dumpfile ("sim_build/mux.vcd");
        $dumpvars (0, mux);
      end

endmodule