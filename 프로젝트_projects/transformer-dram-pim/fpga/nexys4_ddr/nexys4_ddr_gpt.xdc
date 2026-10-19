# Digilent 공식 Nexys-4-DDR-Master.xdc에서 실제사용핀만선택했다.
# 원본: https://github.com/Digilent/digilent-xdc/blob/master/Nexys-4-DDR-Master.xdc
# Nexys4(DDR가없는구형), NexysA7-50T나다른보드에는이핀표를그대로적용하지않는다.
set_property -dict {PACKAGE_PIN E3 IOSTANDARD LVCMOS33} [get_ports CLK100MHZ]
create_clock -name board_clk100 -period 10.000 [get_ports CLK100MHZ]
set_property -dict {PACKAGE_PIN C12 IOSTANDARD LVCMOS33} [get_ports CPU_RESETN]
set_property -dict {PACKAGE_PIN C4 IOSTANDARD LVCMOS33} [get_ports UART_TXD_IN]
set_property -dict {PACKAGE_PIN D4 IOSTANDARD LVCMOS33} [get_ports UART_RXD_OUT]
set_property -dict {PACKAGE_PIN H17 IOSTANDARD LVCMOS33} [get_ports {LED[0]}]
set_property -dict {PACKAGE_PIN K15 IOSTANDARD LVCMOS33} [get_ports {LED[1]}]
set_property -dict {PACKAGE_PIN J13 IOSTANDARD LVCMOS33} [get_ports {LED[2]}]
set_property -dict {PACKAGE_PIN N14 IOSTANDARD LVCMOS33} [get_ports {LED[3]}]
# CPU reset과UART RX는내부clock과비동기이며RTL에서release/RX동기화한다.
# 아래예외는비동기외부핀경로만대상으로하며core내부setup경로를가리지않는다.
set_false_path -from [get_ports {CPU_RESETN UART_TXD_IN}]
# UART수신PC는비동기8N1 bit중간을샘플하고LED는clock동기수신기가없는상태표시핀이다.
# clockedge간보드외부data입출력관계가없으므로외부포트에동기I/O지연가정을넣지않는다.
set_false_path -to [get_ports {UART_RXD_OUT LED[*]}]
set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
