# 이미 합성한 DCP에서 배치·배선을 재시도하는 면적 최적화 경로다.
# 원본 실패 로그를 보존하면서 별도 NEXYS_IMPL_DIR에 결과를 저장한다.
# RTL/학습 가중치/보드 clock은 바꾸지 않는다. netlist 논리 최적화와
# 배치 전략만 바꾸며, 결과값의 기능 검증은 별도의 xsim 시험에서 수행한다.
# UG904 2024.1: ExploreSequentialArea는 순차 회로 면적을 줄이는 opt 전략이다.
foreach required {NEXYS_INPUT_DCP NEXYS_IMPL_DIR} {
    if {![info exists ::env($required)]} { error "$required is required." }
}
set work [file normalize $::env(NEXYS_IMPL_DIR)]
file mkdir $work
cd $work
set_param general.maxThreads 1
open_checkpoint $::env(NEXYS_INPUT_DCP)
opt_design -directive ExploreSequentialArea
report_utilization -file [file join $work optimized_utilization.rpt]
report_control_sets -verbose -file [file join $work control_sets.rpt]
write_checkpoint -force [file join $work optimized.dcp]
# Quick는 timing 중심의 추가 논리 확장을 피하고 legal packing을 먼저 시도한다.
# 실제 setup/hold 판정은 아래 route STA에서 한다. 실패하면 bitstream을 만들지 않는다.
place_design -directive Quick
write_checkpoint -force [file join $work placed.dcp]
route_design
report_utilization -file [file join $work routed_utilization.rpt]
report_timing_summary -max_paths 20 -file [file join $work routed_timing.rpt]
report_drc -file [file join $work drc.rpt]
report_methodology -file [file join $work methodology.rpt]
write_checkpoint -force [file join $work routed.dcp]
set setup [get_property SLACK [get_timing_paths -delay_type max -max_paths 1]]
set hold [get_property SLACK [get_timing_paths -delay_type min -max_paths 1]]
puts "RESULT: area flow setup=$setup ns; hold=$hold ns"
if {$setup < 0 || $hold < 0} { error "Timing failed; no deployable bitstream is produced." }
write_bitstream -force [file join $work nexys4_ddr_gpt.bit]
exit
