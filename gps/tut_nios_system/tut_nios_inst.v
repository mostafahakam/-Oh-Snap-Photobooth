	tut_nios u0 (
		.clk_clk           (<connected-to-clk_clk>),           //        clk.clk
		.leds_export       (<connected-to-leds_export>),       //       leds.export
		.pushbutton_export (<connected-to-pushbutton_export>), // pushbutton.export
		.reset_reset       (<connected-to-reset_reset>),       //      reset.reset
		.sdram_clk_clk     (<connected-to-sdram_clk_clk>),     //  sdram_clk.clk
		.sdram_wire_addr   (<connected-to-sdram_wire_addr>),   // sdram_wire.addr
		.sdram_wire_ba     (<connected-to-sdram_wire_ba>),     //           .ba
		.sdram_wire_cas_n  (<connected-to-sdram_wire_cas_n>),  //           .cas_n
		.sdram_wire_cke    (<connected-to-sdram_wire_cke>),    //           .cke
		.sdram_wire_cs_n   (<connected-to-sdram_wire_cs_n>),   //           .cs_n
		.sdram_wire_dq     (<connected-to-sdram_wire_dq>),     //           .dq
		.sdram_wire_dqm    (<connected-to-sdram_wire_dqm>),    //           .dqm
		.sdram_wire_ras_n  (<connected-to-sdram_wire_ras_n>),  //           .ras_n
		.sdram_wire_we_n   (<connected-to-sdram_wire_we_n>),   //           .we_n
		.hex0_export       (<connected-to-hex0_export>),       //       hex0.export
		.switches_export   (<connected-to-switches_export>),   //   switches.export
		.uart_rxd          (<connected-to-uart_rxd>),          //       uart.rxd
		.uart_txd          (<connected-to-uart_txd>),          //           .txd
		.hex1_export       (<connected-to-hex1_export>),       //       hex1.export
		.hex2_export       (<connected-to-hex2_export>),       //       hex2.export
		.hex3_export       (<connected-to-hex3_export>),       //       hex3.export
		.hex4_export       (<connected-to-hex4_export>),       //       hex4.export
		.hex5_export       (<connected-to-hex5_export>)        //       hex5.export
	);

