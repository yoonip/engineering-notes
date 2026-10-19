# 32-token routed 회로의 실제 MMCM 전용 counter를 cascade하여 2.5MHz로 바꾼다.
# XDC의 숫자만 느리게 지정하는 방법이 아니다. CLKOUT6 /120과 CLKOUT4 /2를
# 직렬 연결하고 기존 BUFG의 입력을 실제 CLKOUT4 pin으로 옮긴다.
# UART divider43은 그대로이므로 PC baud도57600으로 함께 낮춘다.
# 모델/PU/MAC/cache 논리는 바꾸지 않는다. 원본 routed DCP는 보존한다.
# 공식 clock 구성: AMD 7-Series UG472의 CLKOUT4_CASCADE.
foreach required {NEXYS_CASCADE_INPUT_DCP NEXYS_CASCADE_DIR} {
    if {![info exists ::env($required)]} { error "$required is required." }
}
set work [file normalize $::env(NEXYS_CASCADE_DIR)]
file mkdir $work
cd $work
set_param general.maxThreads 4
open_checkpoint $::env(NEXYS_CASCADE_INPUT_DCP)
set mmcm [get_cells clock_generator]
if {[llength $mmcm] != 1} { error "Exactly one expected MMCM is required." }
set net [get_nets -of_objects [get_pins clock_generator/CLKOUT0]]
if {[llength $net] != 1} { error "Expected core clock net is missing." }
puts "CLOCK_ECO: before [get_property CLKOUT0_DIVIDE_F $mmcm], net=$net"
set_property CLKOUT4_CASCADE TRUE $mmcm
set_property CLKOUT6_DIVIDE 120 $mmcm
set_property CLKOUT4_DIVIDE 2 $mmcm
# 이 net의 전체 core clock fanout/BUFG를 그대로 두고 MMCM 출력 driver만 바꾼다.
disconnect_net -net $net -objects [get_pins clock_generator/CLKOUT0]
connect_net -net $net -objects [get_pins clock_generator/CLKOUT4]
puts "CLOCK_ECO: VCO600MHz /120 /2 = 2.5MHz; actual driver=CLKOUT4"
route_design -directive Quick
report_clocks -file [file join $work clocks.rpt]
report_route_status -file [file join $work route_status.rpt]
report_utilization -file [file join $work routed_utilization.rpt]
report_timing_summary -max_paths 20 -file [file join $work routed_timing.rpt]
report_drc -file [file join $work drc.rpt]
report_methodology -file [file join $work methodology.rpt]
write_checkpoint -force [file join $work routed.dcp]
set setup [get_property SLACK [get_timing_paths -delay_type max -max_paths 1]]
set hold [get_property SLACK [get_timing_paths -delay_type min -max_paths 1]]
puts "RESULT: MMCM cascade actual2.5MHz setup=$setup ns; hold=$hold ns"
if {$setup < 0 || $hold < 0} { error "Timing failed; no deployable bitstream is produced." }
write_bitstream -force [file join $work nexys4_ddr_gpt.bit]
puts "INFO: New bitstream generated; physical programming has not been performed."
exit
