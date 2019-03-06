
`timescale 1ns/1ps

module bv_and_2(
clk,
reset,

bv_in_valid,
bv_1,
bv_2,
bv_out_valid,
bv_out

);

parameter rule_num = 64; // size of ruleset: 128, 256, 512, 1024

input clk;
input reset;
input bv_in_valid;
input [rule_num-1:0]  bv_1;
input [rule_num-1:0]  bv_2;
output  reg         bv_out_valid;
output  reg [rule_num:0]  bv_out;

always @(posedge clk or negedge reset)
begin
    if(!reset)
      begin
          bv_out <= {rule_num{1'b0}};
          bv_out_valid <= 1'b0;
      end
    else
      begin
          if(bv_in_valid == 1'b1)
            begin
                bv_out <= {28'b0,bv_1 & bv_2};
                // bv_out <= {bv_1 & bv_2};
                bv_out_valid <= 1'b1;
            end
          else  bv_out_valid <= 1'b0;
      end
end













endmodule
