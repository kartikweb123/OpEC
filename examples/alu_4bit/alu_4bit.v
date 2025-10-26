// Code your design here
module alu_4bit (
    input wire [3:0] A,             // 4-bit first operand
    input wire [3:0] B,             // 4-bit second operand
    input wire [1:0] ALU_Sel,       // 2-bit operation selector (Op-Code)
    output reg [3:0] Result,        // 4-bit result of the operation
    output wire Zero           // Flag: 1 if Result is zero, 0 otherwise
);

    // Internal wires for intermediate results
    wire [3:0] sum_result;
    wire [3:0] and_result;
    wire [3:0] or_result;
    wire [3:0] sub_result;
    wire carry_out;

    // --- Core Logic Operations ---

    // 1. Bitwise AND operation (4 gates)
    assign and_result = A & B;

    // 2. Bitwise OR operation (4 gates)
    assign or_result = A | B;

    // 3. Addition and Subtraction Logic (Using a Full Adder structure)
    // Subtraction B is achieved by adding (NOT B) + 1 (two's complement)
    wire [3:0] B_for_add_sub; // B or NOT B depending on the operation
    wire carry_in;            // 0 for Add, 1 for Sub

    // Selection logic for B and Carry-In based on ALU_Sel[0] (Add/Sub control)
    assign B_for_add_sub = (ALU_Sel[0] == 1'b1) ? ~B : B; // NOT B for sub, B for add
    assign carry_in      = ALU_Sel[0];                    // 1 for sub, 0 for add

    // 4-bit Ripple-Carry Adder for Sum/Difference
    // Note: This implements a full adder block 4 times (estimated ~18-24 gates)
    assign {carry_out, sum_result } = A + B_for_add_sub + carry_in;

    // --- Muxing (Selection) Logic ---

    // 4. Final Result Selection (8:1 Mux equivalent, roughly 12-16 gates)
    // A 4-bit, 4-to-1 multiplexer to choose the final output
    always @(*) begin
        case (ALU_Sel)
            2'b00: Result = sum_result;  // Add (or Subtraction when Sel[0] is 1'b1)
            2'b01: Result = sub_result;  // Not needed, but useful for expansion (e.g., A+1)
            2'b10: Result = and_result;  // AND
            2'b11: Result = or_result;   // OR
            default: Result = 4'bxxxx;   // Default for safety
        endcase
    end

    // --- Flag Logic ---

    // 5. Zero Flag calculation (Checks if all bits of Result are zero) (4-input NOR gate equivalent, ~3-4 gates)
    assign Zero = (Result == 4'b0000);

endmodule
