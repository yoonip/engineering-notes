# 이미 배치한 회로에 대해 다른 배선 전략을 비교한다.
# RTL·가중치·핀·5MHz 제약은 DCP에 들어 있는 그대로 사용한다.
# 기본 route가 혼잡 때문에 오래 걸릴 때 legal routing 후보를 먼저 만든다.
# Quick는 timing을 우선하지 않으므로 최종 STA가 통과하기 전 bit를 만들지 않는다.
# 공식 설명: AMD UG904 2024.1 / Using Directives.
foreach required {NEXYS_PLACED_DCP NEXYS_ROUTE_DIR} {
    if {![info exists ::env($required)]} { error "$required is required." }
}
set work [file normalize $::env(NEXYS_ROUTE_DIR)]
file mkdir $work
cd $work
set directive Quick
if {[info exists ::env(NEXYS_ROUTE_DIRECTIVE)]} { set directive $::env(NEXYS_ROUTE_DIRECTIVE) }
if {$directive ni {Quick Default RuntimeOptimized Explore}} { error "Unsupported route directive." }
set_param general.maxThreads 4
open_checkpoint $::env(NEXYS_PLACED_DCP)
route_design -directive $directive
report_route_status -file [file join $work route_status.rpt]
report_utilization -file [file join $work routed_utilization.rpt]
report_timing_summary -max_paths 20 -file [file join $work routed_timing.rpt]
report_drc -file [file join $work drc.rpt]
report_methodology -file [file join $work methodology.rpt]
write_checkpoint -force [file join $work routed.dcp]
set setup [get_property SLACK [get_timing_paths -delay_type max -max_paths 1]]
set hold [get_property SLACK [get_timing_paths -delay_type min -max_paths 1]]
puts "RESULT: route=$directive setup=$setup ns; hold=$hold ns"
if {$setup < 0 || $hold < 0} { error "Timing failed; no deployable bitstream is produced." }
write_bitstream -force [file join $work nexys4_ddr_gpt.bit]
puts "INFO: Physical board has not been programmed."
exit
