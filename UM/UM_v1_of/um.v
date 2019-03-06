//
//  um module
//
//
//                                 UM
//                  _ _ _ _ _ _ _ _ | _ _ _ _ _ _ _ _ _
//                 |                |                  |
//       cdp --> parser ---------->lookup ----------> transmit --> cdp
//                 |    metadata            action     ^
//                 |                                   |
//                 +- - - - - - - - - - - - - - - - - -+
//                                packet
//
//  bv2.0_programmable
//
//  Created by LiJunnan on 16/9/15.
//  Copyright (c) 2016year LiJunnan. All rights reserved.
//


`timescale 1ns/1ps

module um(
clk,
reset,

//---localbus--//
localbus_cs_n,
localbus_rd_wr,
localbus_data,
localbus_ale, 
localbus_ack_n,  
localbus_data_out,		
//--cdp--//
um2cdp_path,					//if um2cdp_path=0, packets are routed to UM, else if um2cdp_path=1, packets are routed to CDP.
cdp2um_data_valid,
cdp2um_data,
um2cdp_tx_enable,
um2cdp_data_valid,
um2cdp_data,
cdp2um_tx_enable,				//change the name by mxl and ccz according to UM2.0;
um2cdp_rule,
um2cdp_rule_wrreq,
cdp2um_rule_usedw
);

parameter   width_meta  = 288;// packet_metadata(descriptor)
parameter   width_act   = 16; // rule_action


input         clk;
input         reset;
input         localbus_cs_n;
input         localbus_rd_wr;
input [31:0]  localbus_data;
input         localbus_ale;
output        localbus_ack_n;
output[31:0]  localbus_data_out;

output        um2cdp_path;
input         cdp2um_data_valid;
input [138:0] cdp2um_data;
output        um2cdp_tx_enable;
output        um2cdp_data_valid;
output[138:0] um2cdp_data;
input         cdp2um_tx_enable;
output        um2cdp_rule_wrreq;
output[29:0]  um2cdp_rule;
input [4:0]   cdp2um_rule_usedw; 


//----------------wire---------------//
wire            um2cdp_path;
wire            um2cdp_tx_enable;
wire            metadata_valid;
wire  [width_meta-1:0]    metadata;


wire            pkt_valid;            //  from parser to transmit
wire  [138:0]   pkt;

wire  [7:0]     transmit_usedw;       //  from transmit to parser

wire                      action_valid;//  from lookup to transmit
wire  [width_act-1:0]     action;

wire            localbus_ack_n;       //  from lookup to MM(localbus)
wire  [31:0]    localbus_data_out;

wire            um2cdp_rule_wrreq;    //  from transmit to cdp(pkt_out)
wire  [29:0]    um2cdp_rule;
wire            um2cdp_data_valid;
wire  [138:0]   um2cdp_data;

wire  countid_valid;
wire  [5:0] countid0, countid1, countid2, countid3;

//--temp--//
wire  localbus_ack_n_temp[0:1];
wire  [31:0]  localbus_data_out_temp[0:1];

assign  localbus_ack_n = (localbus_ack_n_temp[0] == 1'b0)? 1'b0:
                          (localbus_ack_n_temp[1]== 1'b0)? 1'b0:1'b1;
assign  localbus_data_out = (localbus_ack_n_temp[0] == 1'b0)? localbus_data_out_temp[0]:
                          localbus_data_out_temp[1];

parser parser(
.clk(clk),
.reset(reset),

.um2cdp_path(um2cdp_path),
.cdp2um_data_valid(cdp2um_data_valid),
.cdp2um_data(cdp2um_data),
.um2cdp_tx_enable(um2cdp_tx_enable),

.metadata_valid(metadata_valid),
.metadata(metadata),

.pkt_valid(pkt_valid),
.pkt(pkt),

.transmit_usedw(transmit_usedw)
);




lookup lookup(
.clk(clk),
.reset(reset),

.metadata_valid(metadata_valid),
.metadata(metadata),

.countid_valid(countid_valid),
.countid(countid0),

.localbus_cs_n(localbus_cs_n),
.localbus_rd_wr(localbus_rd_wr),
.localbus_data(localbus_data),
.localbus_ale(localbus_ale),
.localbus_ack_n(localbus_ack_n_temp[0]),
.localbus_data_out(localbus_data_out_temp[0])


);
//
//lookup lookup1(
//.clk(clk),
//.reset(reset),
//
//.metadata_valid(metadata_valid),
//.metadata(metadata),
//
//.countid_valid(),
//.countid(countid1),
//
//.localbus_cs_n(localbus_cs_n),
//.localbus_rd_wr(localbus_rd_wr),
//.localbus_data(localbus_data),
//.localbus_ale(localbus_ale),
//.localbus_ack_n(),
//.localbus_data_out()
//
//
//);
//
//lookup lookup2(
//.clk(clk),
//.reset(reset),
//
//.metadata_valid(metadata_valid),
//.metadata(metadata),
//
//.countid_valid(),
//.countid(countid2),
//
//.localbus_cs_n(localbus_cs_n),
//.localbus_rd_wr(localbus_rd_wr),
//.localbus_data(localbus_data),
//.localbus_ale(localbus_ale),
//.localbus_ack_n(),
//.localbus_data_out()
//
//
//);
//
//lookup lookup3(
//.clk(clk),
//.reset(reset),
//
//.metadata_valid(metadata_valid),
//.metadata(metadata),
//
//.countid_valid(),
//.countid(countid3),
//
//.localbus_cs_n(localbus_cs_n),
//.localbus_rd_wr(localbus_rd_wr),
//.localbus_data(localbus_data),
//.localbus_ale(localbus_ale),
//.localbus_ack_n(),
//.localbus_data_out()
//
//
//);

assign countid = countid0 & countid1 & countid2 & countid3;

lookup_rule looup_rule(
.clk(clk),
.reset(reset),

.localbus_cs_n(localbus_cs_n),
.localbus_rd_wr(localbus_rd_wr),
.localbus_data(localbus_data),
.localbus_ale(localbus_ale),
.localbus_ack_n(localbus_ack_n_temp[1]),
.localbus_data_out(localbus_data_out_temp[1]),

.countid_valid(countid_valid),
.countid(countid),

.action_valid(action_valid),
.action(action)
);




transmit transmit(
.clk(clk),
.reset(reset),
.action_valid(action_valid),
.action(action),
.pkt_valid(pkt_valid),
.pkt(pkt),
.um2cdp_rule_wrreq(um2cdp_rule_wrreq),
.um2cdp_rule(um2cdp_rule),
.um2cdp_data_valid(um2cdp_data_valid),
.um2cdp_data(um2cdp_data),
.cdp2um_rule_usedw(cdp2um_rule_usedw),
.cdp2um_tx_enable(cdp2um_tx_enable),
.transmit_fifo_usedw(transmit_usedw)


);














endmodule