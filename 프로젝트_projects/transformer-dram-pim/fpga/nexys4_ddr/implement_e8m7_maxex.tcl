# 원 제안 MAX-EX 누산기의 별도 OOC 물리 구현입니다.
# 실제 Transformer UART bitstream 및 외부 DDR/PIM 실험과 구분해야 합니다.
# 입력과 결과를 register로 감싼 core에 200ns(5MHz) clock을 적용합니다.
# 일반 입력/출력도 2ns delay로 검사하며 false-path 예외를 추가하지 않습니다.
if {![info exists ::env(MAXEX_STAGE)]} { error "MAXEX_STAGE is required." }
set taskRoot [file normalize $::env(MAXEX_STAGE)]
set taskGuard 16
if {[info exists ::env(MAXEX_GUARD_BITS)]} { set taskGuard $::env(MAXEX_GUARD_BITS) }
if {$taskGuard ni {16 32}} { error "Supported measured GUARD_BITS: 16 or 32." }
set taskOut [file join $taskRoot output]
file mkdir $taskOut
cd $taskOut
set_param general.maxThreads 4
create_project -force e8m7_maxex [file join $taskOut project] -part xc7a100tcsg324-1
read_verilog -sv [file join $taskRoot rtl dram_pim_e8m7_maxex_mac.sv]
read_verilog -sv [file join $taskRoot rtl e8m7_maxex_registered_top.sv]
synth_design -mode out_of_context -top e8m7_maxex_registered_top -part xc7a100tcsg324-1 -generic "LANES=16 GUARD_BITS=$taskGuard"
create_clock -name maxex_clk -period 200.000 [get_ports clk]
set_input_delay -clock maxex_clk 2.000 [get_ports -filter {DIRECTION==IN && NAME!=clk}]
set_output_delay -clock maxex_clk 2.000 [get_ports -filter {DIRECTION==OUT}]
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
puts "MAXEX_RESULT: guard=$taskGuard setup=$taskSetup hold=$taskHold"
if {$taskSetup < 0 || $taskHold < 0} { error "MAX-EX OOC timing failed; inspect reports." }
# OOC virtual ports에는 보드 package pin을 지정하지 않았으므로 .bit를 만들지 않습니다.
puts "MAXEX_OOC_COMPLETE: independent arithmetic core only; no physical board measurement."
exit
