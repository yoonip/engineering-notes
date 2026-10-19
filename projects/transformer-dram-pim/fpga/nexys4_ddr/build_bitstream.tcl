# Nexys 4 DDR 전용 학습 모델 UART top: 실제 pin/clock 포함 synthesis→route→bitstream.
# fullops V65/D16/H4/F32/L2 가중치를 유지한다. 기본 cache는8이고 환경변수로1..32를 선택한다.
# 실제 core clock은 기본5 MHz이며32-token distributed는2.5 MHz/57600 baud를자동선택한다.
# 느린clock은setup시간을확보하는설정이다. 새로운route/STA결과를실측하고처리성능과구분한다.
if {[info exists ::env(TRANSFORMER_REPO)]} {
    set repo_root $::env(TRANSFORMER_REPO)
} else {
    set repo_root [file normalize [file join [file dirname [info script]] ../..]]
}
set work_root [file join $repo_root build nexys4_ddr board]
set max_context 8
if {[info exists ::env(NEXYS_MAX_CONTEXT)]} { set max_context $::env(NEXYS_MAX_CONTEXT) }
if {![string is integer -strict $max_context] || $max_context < 1 || $max_context > 32} {
    error "NEXYS_MAX_CONTEXT must be in 1..32."
}
file mkdir $work_root
cd $work_root
set flat_cache 0
if {[info exists ::env(NEXYS_FLAT_CACHE)]} { set flat_cache $::env(NEXYS_FLAT_CACHE) }
if {$flat_cache != 0 && $flat_cache != 1} { error "NEXYS_FLAT_CACHE must be 0 or 1." }
# PowerShell을거치지않고Tcl을직접실행할때도같은자동설정을사용한다.
# CORE_CLOCK_HZ는실제MMCM분주/출력연결을바꾸고HOST_BAUD는UARTbit길이의계산기준이다.
set core_clock_hz [expr {$max_context == 32 && $flat_cache == 1 ? 2500000 : 5000000}]
if {[info exists ::env(NEXYS_CORE_CLOCK_HZ)]} { set core_clock_hz $::env(NEXYS_CORE_CLOCK_HZ) }
if {![string is integer -strict $core_clock_hz] || $core_clock_hz ni {2500000 5000000}} {
    error "NEXYS_CORE_CLOCK_HZ must be 2500000 or 5000000."
}
set host_baud [expr {$core_clock_hz == 2500000 ? 57600 : 115200}]
if {[info exists ::env(NEXYS_HOST_BAUD)]} { set host_baud $::env(NEXYS_HOST_BAUD) }
if {![string is integer -strict $host_baud] || $host_baud ni {57600 115200}} {
    error "NEXYS_HOST_BAUD must be 57600 or 115200."
}
puts "INFO: Build context=$max_context cache_flat=$flat_cache core_clock_hz=$core_clock_hz host_baud=$host_baud"
# CPU병렬실행의최대thread수를지정한다. FPGA하드웨어의head수나PU개수와무관하다.
set_param general.maxThreads 4
create_project -force nexys4_ddr_gpt [file join $work_root project] -part xc7a100tcsg324-1
foreach source {dram_pim_pu_synth.sv dram_pim_vmm_bank.sv transformer_gpt_kvcache_seq.sv gpt_kvcache_rom_board_top.sv nexys4_ddr_uart.sv nexys4_ddr_gpt_uart_bridge.sv nexys4_ddr_gpt_top.sv} {
    read_verilog -sv [file join $repo_root rtl $source]
}
read_xdc [file join $repo_root fpga nexys4_ddr nexys4_ddr_gpt.xdc]
synth_design -top nexys4_ddr_gpt_top -part xc7a100tcsg324-1 -generic "MAX_CONTEXT=$max_context FLAT_DISTRIBUTED_CACHE=$flat_cache CORE_CLOCK_HZ=$core_clock_hz HOST_BAUD=$host_baud"
report_utilization -file [file join $work_root synth_utilization.rpt]
report_timing_summary -max_paths 10 -file [file join $work_root synth_timing.rpt]
write_checkpoint -force [file join $work_root synthesized.dcp]
opt_design
place_design
write_checkpoint -force [file join $work_root placed.dcp]
# 저속32-token distributed는먼저Quick으로완전배선을시도한다.
# Quick후setup/hold중하나라도음수면Explore를추가해타이밍개선을시도한다.
# 기본8-token등의기존경로는Default router를사용한다. 어느전략도합격을보장하지않는다.
if {$max_context == 32 && $flat_cache == 1 && $core_clock_hz == 2500000} {
    route_design -directive Quick
    set quick_setup [get_property SLACK [get_timing_paths -delay_type max -max_paths 1]]
    set quick_hold [get_property SLACK [get_timing_paths -delay_type min -max_paths 1]]
    puts "RESULT: Quick worst_setup=$quick_setup ns; worst_hold=$quick_hold ns"
    if {$quick_setup < 0 || $quick_hold < 0} {
        puts "INFO: Quick timing failed; applying Explore before final STA."
        route_design -directive Explore
    }
} else {
    route_design
}
# 보드입력100 MHz는XDC에정의하고MMCM출력은실제분주속성에서자동도출한다.
# 요구설정만JSON에적지않고core BUFG출력에도달하는clock의실제주기를확인한다.
set routed_core_clock [get_clocks -of_objects [get_pins core_clock_buffer/O]]
if {[llength $routed_core_clock] != 1} { error "Exactly one clock must reach core_clock_buffer/O." }
set routed_core_period [get_property PERIOD $routed_core_clock]
set requested_core_period [expr {1000000000.0 / $core_clock_hz}]
if {abs($routed_core_period - $requested_core_period) > 0.001} {
    error "Physical core clock period does not match requested CORE_CLOCK_HZ."
}
puts "RESULT: actual core clock period=$routed_core_period ns; host_baud=$host_baud"
report_clocks -file [file join $work_root routed_clocks.rpt]
report_clock_networks -file [file join $work_root routed_clock_networks.rpt]
report_route_status -file [file join $work_root routed_route_status.rpt]
report_utilization -file [file join $work_root routed_utilization.rpt]
report_timing_summary -max_paths 20 -file [file join $work_root routed_timing.rpt]
report_drc -file [file join $work_root drc.rpt]
report_methodology -file [file join $work_root methodology.rpt]
write_checkpoint -force [file join $work_root routed.dcp]
# setup/hold 조건을 통과하지 못하면 실기기용 파일을 만들지 않고 RTL/clock을 수정한다.
set worst_setup [get_property SLACK [get_timing_paths -delay_type max -max_paths 1]]
set worst_hold [get_property SLACK [get_timing_paths -delay_type min -max_paths 1]]
puts "RESULT: routed worst_setup=$worst_setup ns; worst_hold=$worst_hold ns"
if {$worst_setup < 0 || $worst_hold < 0} {
    error "Timing does not pass; no deployable bitstream is produced."
}
write_bitstream -force [file join $work_root nexys4_ddr_gpt.bit]
puts "INFO: Bitstream built. Physical programming and measurements have not been performed."
exit
