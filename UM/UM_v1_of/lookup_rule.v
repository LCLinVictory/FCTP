`timescale 1ns/1ps


module lookup_rule(
clk,
reset,

countid_valid,
countid,

action_valid,
action,

localbus_cs_n,
localbus_rd_wr,
localbus_data,
localbus_ale,
localbus_ack_n,
localbus_data_out


);

input             clk;
input             reset;
input             countid_valid;
input [5:0]       countid;

output  wire      action_valid;
output  wire  [15:0]  action;

input             localbus_cs_n;
input             localbus_rd_wr;
input [31:0]      localbus_data;
input             localbus_ale;
output  reg       localbus_ack_n;
output  reg [31:0]  localbus_data_out;



//--reg--//
reg [31:0]  localbus_addr;
wire stage_enable;

//--ram--//
reg [5:0] address_a,address_b;
reg wren_a,wren_b;
reg rden_a,rden_b;
reg [31:0]  data_a,data_b;
wire  [31:0]  q_a,q_b;


//----------state------//
reg [3:0] set_state;


parameter     idle        = 4'd0,
              ram_set     = 4'd1,
              read_ram    = 4'd2,
              wait_1      = 4'd3,
              wait_2      = 4'd4,
              ram_read    = 4'd5,
              wait_back   = 4'd6;
         
assign action = q_a[15:0];


//-------set_state-------//
always @ (posedge clk or negedge reset)
begin
    if(!reset)
      begin
			    set_state <= idle;
			    
			    localbus_ack_n <= 1'b1;
      end
    else
      begin
          case(set_state)
            idle:
            begin
                if((localbus_ale == 1'b1) && (localbus_data[18]==1'b1))
                  begin
                      localbus_addr <= localbus_data;
                      if(localbus_rd_wr == 1'b0)
                        begin
                            set_state <= ram_set;
                        end
                      else
                        begin
                            set_state <= ram_read;
                        end
                  end
            end
            ram_set:
            begin
                if(localbus_cs_n == 1'b0)
                  begin
                      wren_b <= 1'b1;
                      address_b <= localbus_addr[5:0];
                      data_b <= localbus_data;
                      
                      localbus_ack_n <= 1'b0;
                      set_state <= wait_back;
                  end
            end
            ram_read:
            begin
                if(localbus_cs_n == 1'b0)
                  begin
                      rden_b <= 1'b1;
                      address_b <= localbus_addr[5:0];
                      
                      set_state <= wait_1;
                  end
            end
            wait_1:
            begin
                rden_b <= 1'b0;
                set_state <= wait_2;
            end
            wait_2:
            begin
                set_state <= read_ram;
            end
            read_ram:
            begin
                localbus_data_out <= q_b;
                localbus_ack_n <= 1'b0;
                set_state <= wait_back;
            end
            wait_back:
            begin
                wren_b <= 1'b0;
                if(localbus_cs_n == 1'b1)
                  begin
                      localbus_ack_n <= 1'b1;
                      set_state <= idle;
                  end
            end
            default:
            begin
                set_state <= idle;
            end
          endcase
      end
end


ram_32_64 rule_ram(
.address_a(countid),
.address_b(address_b),
.clock(clk),
.data_a(32'b0),
.data_b(data_b),
.rden_a(countid_valid),
.rden_b(rden_b),
.wren_a(1'b0),
.wren_b(wren_b),
.q_a(q_a),
.q_b(q_b)
);






//--stage_2--//
hold1clk h1c_1(
.clk(clk),
.reset(reset),
.stage_enable_in(countid_valid),
.stage_enable_out(stage_enable)
);
//--stage_3--//
hold1clk h1c_2(
.clk(clk),
.reset(reset),
.stage_enable_in(stage_enable),
.stage_enable_out(action_valid)
);




endmodule