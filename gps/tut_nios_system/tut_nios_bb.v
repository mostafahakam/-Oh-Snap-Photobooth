
module tut_nios (
	clk_clk,
	leds_export,
	pushbutton_export,
	reset_reset,
	sdram_clk_clk,
	sdram_wire_addr,
	sdram_wire_ba,
	sdram_wire_cas_n,
	sdram_wire_cke,
	sdram_wire_cs_n,
	sdram_wire_dq,
	sdram_wire_dqm,
	sdram_wire_ras_n,
	sdram_wire_we_n,
	hex0_export,
	switches_export,
	uart_rxd,
	uart_txd,
	hex1_export,
	hex2_export,
	hex3_export,
	hex4_export,
	hex5_export);	

	input		clk_clk;
	output	[7:0]	leds_export;
	input		pushbutton_export;
	input		reset_reset;
	output		sdram_clk_clk;
	output	[12:0]	sdram_wire_addr;
	output	[1:0]	sdram_wire_ba;
	output		sdram_wire_cas_n;
	output		sdram_wire_cke;
	output		sdram_wire_cs_n;
	inout	[15:0]	sdram_wire_dq;
	output	[1:0]	sdram_wire_dqm;
	output		sdram_wire_ras_n;
	output		sdram_wire_we_n;
	output	[3:0]	hex0_export;
	input	[7:0]	switches_export;
	input		uart_rxd;
	output		uart_txd;
	output	[3:0]	hex1_export;
	output	[3:0]	hex2_export;
	output	[3:0]	hex3_export;
	output	[3:0]	hex4_export;
	output	[3:0]	hex5_export;
endmodule
