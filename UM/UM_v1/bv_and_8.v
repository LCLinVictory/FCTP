
`timescale 1ns/1ps

module bv_and_8(
clk,
reset,

bv_in_valid,
bv_1,
bv_2,
bv_3,
bv_4,
bv_5,
bv_6,
bv_7,
bv_8,
bv_out_valid,
bv_out

);

parameter rule_num = 36; // size of ruleset: 128, 256, 512, 1024
parameter rule_num_half = 18;
parameter cluster_n = 36; // two m9K -> 36*512

input clk;
input reset;
input bv_in_valid;
input [cluster_n-1:0]  bv_1;
input [cluster_n-1:0]  bv_2;
input [cluster_n-1:0]  bv_3;
input [cluster_n-1:0]  bv_4;
input [cluster_n-1:0]  bv_5;
input [cluster_n-1:0]  bv_6;
input [cluster_n-1:0]  bv_7;
input [cluster_n-1:0]  bv_8;
output  reg         bv_out_valid;
output  reg [rule_num-1:0]  bv_out;

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
            if(bv_5 == {cluster_n{1'b1}})
              begin
                case(rule_num)
                  36:     bv_out <= {bv_1 & bv_2 & bv_3 & bv_4};
                  //128:    bv_out <= {bv_1, bv_2, bv_3, bv_4[19:0]};
                  //256:    bv_out <= {bv_1, bv_2, bv_3, bv_4, bv_5, bv_6, bv_7, bv_8[3:0]};
                  //512:    bv_out <= {224'b0, bv_1, bv_2, bv_3, bv_4, bv_5, bv_6, bv_7, bv_8};
                  //1024:   bv_out <= {736'b0,bv_1, bv_2, bv_3, bv_4, bv_5, bv_6, bv_7, bv_8};
                  default: ;
                endcase
                bv_out_valid <= 1'b1;
              end
            else 
              begin
                case(rule_num)
                  36:     bv_out <= {bv_1 & bv_2 & bv_3 & bv_4 & bv_5 & bv_6 & bv_7 & bv_8};
                  //128:    bv_out <= {bv_1, bv_2, bv_3, bv_4[19:0]};
                  //256:    bv_out <= {bv_1, bv_2, bv_3, bv_4, bv_5, bv_6, bv_7, bv_8[3:0]};
                  //512:    bv_out <= {224'b0, bv_1, bv_2, bv_3, bv_4, bv_5, bv_6, bv_7, bv_8};
                  //1024:   bv_out <= {736'b0,bv_1, bv_2, bv_3, bv_4, bv_5, bv_6, bv_7, bv_8};
                  default: ;
                endcase
                bv_out_valid <= 1'b1;
              end
          else  bv_out_valid <= 1'b0;
      end
end













endmodule

