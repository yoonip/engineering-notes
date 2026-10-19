# MAX-EX와 비교하는 일반 E8M7 pairwise floating tree의 별도 OOC 물리 구현입니다.
# 실제 Transformer UART bitstream 및 외부 DDR/PIM 실험과 구분해야 합니다.
# 입력과 결과를 register로 감싼 core에 200ns(5MHz) clock을 적용합니다.
# 일반 입력/출력도 2ns delay로 검사하며 false-path 예외를 추가하지 않습니다.
if {![info exists ::env(PAIRWISE_STAGE)]} { error "PAIRWISE_STAGE is required." }
set taskRoot [file normalize $::env(PAIRWISE_STAGE)]
set taskOut [file join $taskRoot output]
file mkdir $taskOut
cd $taskOut
set_param general.maxThreads 4
create_project -force e8m7_pairwise [file join $taskOut project] -part xc7a100tcsg324-1
read_verilog -sv [file join $taskRoot rtl e8m7_pairwise_tree_mac.sv]
read_verilog -sv [file join $taskRoot rtl e8m7_pairwise_registered_top.sv]
read_verilog -sv [file join $taskRoot rtl e8m7_pairwise_ooc_top.sv]
synth_design -mode out_of_context -top pw_top -part xc7a100tcsg324-1
create_clock -name pairwise_clk -period 200.000 [get_ports clk]
set_input_delay -clock pairwise_clk 2.000 [get_ports -filter {DIRECTION==IN && NAME!=clk}]
set_output_delay -clock pairwise_clk 2.000 [get_ports -filter {DIRECTION==OUT}]
report_utilization -file synth_utilization.rpt
write_checkpoint -force synthesized.dcp
opt_design
place_design
route_design
report_route_status -file route_status.rpt
report_timing_summary -max_paths 10 -file routed_timing.rpt
report_utilization -file routed_utilization.rpt
report_drc -file drc.rpt
report_methodology -file methodology.rpt
write_checkpoint -force routed.dcp
set taskSetup [get_property SLACK [get_timing_paths -delay_type max -max_paths 1]]
set taskHold [get_property SLACK [get_timing_paths -delay_type min -max_paths 1]]
puts "PAIRWISE_RESULT: setup=$taskSetup hold=$taskHold"
if {$taskSetup < 0 || $taskHold < 0} { error "Pairwise OOC timing failed; inspect reports." }
# OOC virtual ports에는 보드 package pin을 지정하지 않았으므로 .bit를 만들지 않습니다.
puts "PAIRWISE_OOC_COMPLETE: independent arithmetic core only; no physical board measurement."
exit
