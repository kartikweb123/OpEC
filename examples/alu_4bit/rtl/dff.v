module dff 
#(
	parameter WIDTH = 8,
	parameter TEST = 3 // does nothing
)
(
    clk,               
    rst_n,             
    d,
    q
);
	
	input wire clk;
	input wire rst_n;
	input wire [WIDTH-1:0] d;
	output reg [WIDTH-1:0] q;
	
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) q <= 0; 
        else q <= d;
    end
    
    // testing only...
    wire tclk;
    reg [2:0] hello;
    reg [TEST:1] world;
    reg [TEST-1:0] kartik;
    
    always @(*)
    		hello = {~tclk, tclk};
    
    always @(tclk) kartik <= world; // latch
    

endmodule
