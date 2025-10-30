
`include "dff.v"

module alu_4bit (
	input wire clk,
	input wire rst,
    input wire [3:0] A,             // 4-bit first operand
    input wire [3:0] B,             // 4-bit second operand
    input wire [1:0] ALU_Sel,       // 2-bit operation selector (Op-Code)
    output wire [3:0] Result,        // 4-bit result of the operation
    output wire Zero           // Flag: 1 if Result is zero, 0 otherwise
);

    (* keep *) wire [3:0] sum_result;
    (* keep *) wire [3:0] and_result;
    (* keep *) wire [3:0] or_result;
    (* keep *) wire [3:0] sub_result;
    (* keep *) wire carry_out_sum;
    (* keep *) wire carry_out_sub;
    
    (* keep *) wire [3:0] A_ff, B_ff, Result_ff;
    (* keep *) wire [1:0] ALU_Sel_ff;
    (* keep *) wire Zero_ff;
    (* keep *) wire [3:0] B_for_add_sub; // B or NOT B depending on the operation
    (* keep *) wire carry_in;            // 0 for Add, 1 for Sub

    wire rst_n;
    notgate #(.WIDTH(1)) notgate0 (.a(rst), .y(rst_n));

    
	dff #(.WIDTH(4)) dff_A (.clk(clk), .rst_n(rst_n), .d(A), .q(A_ff));
	dff #(.WIDTH(4)) dff_B (.clk(clk), .rst_n(rst_n), .d(B), .q(B_ff));
	dff #(.WIDTH(2)) dff_ALU_Sel (.clk(clk), .rst_n(rst_n), .d(ALU_Sel), .q(ALU_Sel_ff));
	
    assign and_result = A_ff & B_ff;
    assign or_result = A_ff | B_ff;
    assign B_for_add_sub = (ALU_Sel_ff[0] == 1'b1) ? ~B_ff : B_ff;
    assign carry_in = ALU_Sel_ff[0];
    assign {carry_out, sum_result} = A_ff + B_for_add_sub + {3'b000, carry_in};
    assign {carry_out, sub_result} = A_ff + B_for_add_sub + {3'b000, carry_in};
    assign Result_ff = 
    		(ALU_Sel_ff == 2'b00) ? sum_result :
    		(ALU_Sel_ff == 2'b01) ? sub_result :
    		(ALU_Sel_ff == 2'b10) ? and_result :
    		(ALU_Sel_ff == 2'b11) ? or_result : 4'bxxxx;
    assign Zero_ff = (Result_ff == 4'b0000);
    
    dff #(.WIDTH(4)) dff_Result (.clk(clk), .rst_n(rst_n), .d(Result_ff), .q(Result));
    dff #(.WIDTH(1)) dff_Zero (.clk(clk), .rst_n(rst_n), .d(Zero_ff), .q(Zero));

endmodule

module notgate #(parameter WIDTH = 1) (
    input wire [WIDTH-1:0] a,
    output wire [WIDTH-1:0] y
);

assign y = ~a;

endmodule
