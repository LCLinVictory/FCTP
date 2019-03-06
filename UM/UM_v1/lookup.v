`timescale 1ns/1ps

module lookup(
clk,
reset, 

localbus_cs_n,
localbus_rd_wr,
localbus_data,
localbus_ale,
localbus_ack_n,
localbus_data_out,

packethead_valid,
packethead,


countid_valid,
countid


);

parameter   width_packethead = 104;//- 5tuple_matchlength is 104, OpenFlow1.0_matchlength is 253
parameter	rule_num = 36;	// size of ruleset: 128, 256, 512, 1024
parameter	width_count		= 6;	// pow(2, width_count) = rule_num -> 7, 8, 9, 10

input           clk;
input           reset;

input           localbus_cs_n;
input           localbus_rd_wr;
input [31:0]    localbus_data;
input           localbus_ale;
output  wire    localbus_ack_n;
output  wire  [31:0]  localbus_data_out;

input           packethead_valid;
input [width_packethead-1:0]   packethead;

output  wire    countid_valid;
output  wire  [width_count-1:0]   countid;// rule num_max = 64;

//-------temp------//
wire            localbus_ale_temp[0:1];
wire            localbus_ack_n_temp[0:1];
wire  [31:0]    localbus_data_out_temp[0:1];
wire            bv_out_valid[0:1];
wire  [rule_num-1:0]    bv_out[0:1];
wire            bv_and_valid;
wire  [rule_num-1:0]    bv_and;

assign  localbus_ale_temp[0] = (localbus_data[18:16] == 3'd0)? localbus_ale:1'b0;
assign  localbus_ale_temp[1] = (localbus_data[18:16] == 3'd1)? localbus_ale:1'b0;

assign  localbus_ack_n  = (localbus_ack_n_temp[0] == 1'b0)? 1'b0:
                          (localbus_ack_n_temp[1] == 1'b0)? 1'b0:
                          1'b1;
                          
assign  localbus_data_out = (localbus_ack_n_temp[0] == 1'b0)? localbus_data_out_temp[0]:
                            (localbus_ack_n_temp[1] == 1'b0)? localbus_data_out_temp[1]:
                            32'b0;
                                                      
search_engine se(
.clk(clk),
.reset(reset),
.key_in_valid(packethead_valid),
.key_in(packethead[71:0]),
.bv_out_valid(bv_out_valid[0]),
.bv_out(bv_out[0]),
.localbus_cs_n(localbus_cs_n),
.localbus_rd_wr(localbus_rd_wr),
.localbus_data(localbus_data),
.localbus_ale(localbus_ale_temp[0]),
.localbus_ack_n(localbus_ack_n_temp[0]),
.localbus_data_out(localbus_data_out_temp[0])
);

search_engine_half se_half(
.clk(clk),
.reset(reset),
.key_in_valid(packethead_valid),
.key_in(packethead[width_packethead-1:72]),
.bv_out_valid(bv_out_valid[1]),
.bv_out(bv_out[1]),
.localbus_cs_n(localbus_cs_n),
.localbus_rd_wr(localbus_rd_wr),
.localbus_data(localbus_data),
.localbus_ale(localbus_ale_temp[1]),
.localbus_ack_n(localbus_ack_n_temp[1]),
.localbus_data_out(localbus_data_out_temp[1])
);

bv_and_2 bv_and_2(
.clk(clk),
.reset(reset),
.bv_in_valid(bv_out_valid[0]),
.bv_1(bv_out[0]),
.bv_2(bv_out[1]),
.bv_out_valid(bv_and_valid),
.bv_out(bv_and)
);

calculate_countid calculate_countid(
.clk(clk),
.reset(reset),
.bv_in_valid(bv_and_valid),
.bv_in(bv_and),
.countid_valid(countid_valid),
.countid(countid)
);


endmodule