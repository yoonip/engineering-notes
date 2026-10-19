# 생성된 bitstream을 사용자 확인된 Nexys4 DDR에 올릴 때만 직접 실행한다.
# hardware manager에서 실제 Artix-7 100T 한 대만 찾았을 때 진행한다.
if {[info exists ::env(TRANSFORMER_REPO)]} {
    set repo_root $::env(TRANSFORMER_REPO)
} else {
    set repo_root [file normalize [file join [file dirname [info script]] ../..]]
}
set bitfile [file join $repo_root build nexys4_ddr board nexys4_ddr_gpt.bit]
if {[info exists ::env(NEXYS_BITFILE)]} { set bitfile $::env(NEXYS_BITFILE) }
if {![file exists $bitfile]} { error "Build a timing-passing bitstream first: $bitfile" }
open_hw_manager
connect_hw_server
open_hw_target
set devices [get_hw_devices -filter {PART =~ xc7a100t*}]
if {[llength $devices] != 1} { error "Expected exactly one connected xc7a100t device." }
set device [lindex $devices 0]
current_hw_device $device
set_property PROGRAM.FILE $bitfile $device
program_hw_devices $device
refresh_hw_device $device
puts "INFO: programming command completed; run host.py for measured output comparison."
close_hw_manager
exit
