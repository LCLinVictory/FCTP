//
//  parser module
//  bv2.0_programmable
//
//  Created by LiJunnan on 16/9/15.
//  Copyright (c) 2016year LiJunnan. All rights reserved.
//

`timescale 1ns/1ps

module parser(
clk,
reset,
um2cdp_path,
cdp2um_data_valid,
cdp2um_data,
um2cdp_tx_enable,
metadata_valid,
metadata,
pkt_valid,
pkt,
transmit_usedw
);

parameter   width_meta = 288;// packet_metadata(descriptor)

input         clk;
input         reset;
output        um2cdp_path;
input         cdp2um_data_valid;
input [138:0] cdp2um_data;
output        um2cdp_tx_enable;

output        metadata_valid;
output[width_meta-1:0]  metadata;

output        pkt_valid;
output[138:0] pkt;
input [7:0]   transmit_usedw;

//------------------reg------------//
reg           um2cdp_path; //"0":packet from cdp to UM;
reg           um2cdp_tx_enable;
reg           metadata_valid;
reg   [width_meta-1:0]   metadata;


reg           pkt_valid;// from parser to transmit;
reg   [138:0] pkt;



//-----------------state------------------//
reg   [3:0]   parser_state;// parser state machine 

parameter     idle            = 4'd0,
              parser_eth_s    = 4'd1,
              parser_ip_1_s   = 4'd2,
              parser_ip_2_s   = 4'd3,
              parser_vlan_1_s = 4'd4,
              parser_vlan_2_s = 4'd5,
              pkt_trans_s     = 4'd6,
              
              discard_s       = 4'd7;


reg           cdp2um_state;// receive pkt from cdp 


//----------------------parser_state-------------------------//
always @ (posedge clk or negedge reset)
begin
    if(!reset)
      begin
			   metadata_valid  <= 1'b0;
			   metadata        <= {width_meta{1'b0}};
			   um2cdp_path	    <= 1'b0;
			   pkt_valid       <= 1'b0;
			   
			   parser_state    <= idle;
      end
    else
      begin
          case(parser_state)
            idle:
            begin
                if((cdp2um_data_valid == 1'b1) && (cdp2um_data[138:136] == 3'b101)) begin
                    metadata_valid <= 1'b1;
                    metadata  <= {cdp2um_data[127:80],{(width_meta-48){1'b1}}};
                    
                    pkt_valid <= 1'b1;
                    pkt <= cdp2um_data;
                    
                    parser_state <= pkt_trans_s;
                  end
                else begin
                    metadata_valid <= 1'b0;
                    pkt_valid <= 1'b0;
                  end
            end
            pkt_trans_s:
            begin
                pkt_valid <= 1'b1;
					 metadata_valid <= 1'b0;
                pkt <= cdp2um_data;
                if(cdp2um_data[138:136] == 3'b110)
                  begin
                      parser_state  <= idle;
                  end
            end
            default:
            begin
                parser_state <= idle;
            end
          endcase
      end
end

//-------------------cdp2um_state-------------------//
always @ (posedge clk or negedge reset)
begin
    if(!reset)
      begin
        um2cdp_tx_enable  <= 1'b0;
        cdp2um_state      <= 1'b0;
      end
    else
      begin
        case(cdp2um_state)
          1'b0:
          begin
              if(cdp2um_data_valid == 1'b0)
                begin
                    um2cdp_tx_enable  <= 1'b1;
                    cdp2um_state      <= 1'b1;
                end
          end
          1'b1:
          begin
              if(cdp2um_data_valid == 1'b1)
                begin
                    um2cdp_tx_enable  <= 1'b0;
                    cdp2um_state      <= 1'b0;
                end
          end
        endcase
      end
end





























endmodule


