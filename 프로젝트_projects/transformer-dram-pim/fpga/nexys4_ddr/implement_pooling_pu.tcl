# Pooling PU의 독립 등록 core를 Nexys FPGA part에 합성·배치·배선한다.
# 가상 I/O와 200ns clock을 사용하는 OOC이며 보드 pin/DDR/JTAG는 사용하지 않는다.
# 실제 GPT bitstream의 구성은 이 실행에서 변경하지 않는다.
if {![info exists ::env(POOLING_STAGE)]} { error "POOLING_STAGE is required." }
set taskRoot [file normalize $::env(POOLING_STAGE)]
set taskWindow $::env(POOLING_WINDOW)
if {$taskWindow < 1 || $taskWindow > 64} { error "WINDOW must be 1..64." }
set taskOut [file join $taskRoot output]
file mkdir $taskOut
cd $taskOut
# 대형 SDF 컴파일과 함께 실행해도 새 OOC 작업이 쓰는 병렬 수를 제한한다.
set_param general.maxThreads 1
create_project -force pooling_pu [file join $taskOut project] -part xc7a100tcsg324-1
read_verilog -sv [file join $taskRoot rtl dram_pim_pooling_pu.sv]
# helper가 module 선언의 이름 한 곳만 짧게 바꾼 가역 사본을 사용한다.
# 같은 회로인데 긴 top 이름의 내부 realtime Tcl을 못 찾은 최초 실패가 있었다.
# 보편적인 원인으로 단정하지 않으며 최초 로그와 원문 복원 SHA를 보존한다.
read_verilog -sv [file join $taskRoot rtl pool_top.sv]
synth_design -mode out_of_context -top pool_top -part xc7a100tcsg324-1 -generic "WINDOW=$taskWindow"
create_clock -name pooling_clk -period 200.000 [get_ports clk]
# reset/valid/data 입력과 결과/count/valid 출력도 실제 STA에 포함한다.
# false-path 또는 multicycle로 긴 평균 나눗셈 경로를 숨기지 않는다.
set_input_delay -clock pooling_clk 2.000 [get_ports -filter {DIRECTION==IN && NAME!=clk}]
set_output_delay -clock pooling_clk 2.000 [get_ports -filter {DIRECTION==OUT}]
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
puts "POOLING_RESULT: window=$taskWindow setup=$taskSetup hold=$taskHold"
if {$taskSetup < 0 || $taskHold < 0} { error "Pooling OOC timing failed; inspect reports." }
# 보드 package pin을 지정하지 않은 독립 core이므로 .bit를 만들지 않는다.
puts "POOLING_OOC_COMPLETE: independent core; no physical board or DRAM-PIM measurement."
exit
