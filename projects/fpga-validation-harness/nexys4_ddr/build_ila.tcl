# Vivado 2024.1: educational Nexys4 DDR target with an ILA.
# Run in a fresh Vivado session. Builds files only; never connects to hardware.
# Example: vivado -mode batch -source build_ila.tcl -tclargs C:/my/build
set src [file dirname [file normalize [info script]]]
if {[info exists argv] && [llength $argv] > 0} {
    set build_dir [file normalize [lindex $argv 0]]
} else {
    set build_dir [file normalize [file join [pwd] nexys_validation_ila_build]]
}
file mkdir $build_dir
create_project -in_memory -part xc7a100tcsg324-1
read_verilog [file join $src validation_top.v]
read_xdc [file join $src nexys4_ddr.xdc]
synth_design -top validation_top -part xc7a100tcsg324-1

# Select the actual clock net driving sample_valid after synthesis.
set clock_net [get_nets -of_objects [get_pins sample_valid_reg/C]]
if {[llength $clock_net] != 1} { error "Cannot identify the sample clock" }
puts "ILA clock net: $clock_net"
create_debug_core u_ila_0 ila
set_property C_DATA_DEPTH 1024 [get_debug_cores u_ila_0]
set_property C_TRIGIN_EN false [get_debug_cores u_ila_0]
set_property C_TRIGOUT_EN false [get_debug_cores u_ila_0]
set_property C_ADV_TRIGGER false [get_debug_cores u_ila_0]
set_property C_INPUT_PIPE_STAGES 0 [get_debug_cores u_ila_0]
set_property C_EN_STRG_QUAL true [get_debug_cores u_ila_0]
set_property ALL_PROBE_SAME_MU true [get_debug_cores u_ila_0]
# Storage qualification needs at least two match units with Vivado 2024.1.
set_property ALL_PROBE_SAME_MU_CNT 2 [get_debug_cores u_ila_0]
set_property port_width 1 [get_debug_ports u_ila_0/clk]
connect_debug_port u_ila_0/clk $clock_net

# Append bus bits low-to-high so probe bit 0 is RTL bit 0.
set probe_index 0
foreach {signal_name width} {
    sample_valid 1
    sample_seq 16
    expected_word 16
    actual_word 16
    mismatch 1
    sample_count 32
    error_count 32
} {
    set signal_nets {}
    if {$width == 1} {
        set signal_nets [get_nets -quiet [list $signal_name]]
    } else {
        for {set bit_index 0} {$bit_index < $width} {incr bit_index} {
            set bit_name [format {%s[%d]} $signal_name $bit_index]
            set found [get_nets -quiet [list $bit_name]]
            if {[llength $found] != 1} { error "Missing debug net $bit_name" }
            lappend signal_nets [lindex $found 0]
        }
    }
    if {[llength $signal_nets] != $width} {
        error "Wrong net count for $signal_name: $signal_nets"
    }
    if {$probe_index > 0} { create_debug_port u_ila_0 probe }
    set port_name u_ila_0/probe$probe_index
    set_property port_width $width [get_debug_ports $port_name]
    set_property PROBE_TYPE DATA_AND_TRIGGER [get_debug_ports $port_name]
    connect_debug_port $port_name $signal_nets
    puts "Connected $port_name: $signal_name ($width bits)"
    incr probe_index
}

opt_design
place_design
route_design
report_timing_summary -file [file join $build_dir timing_summary.txt]
report_drc -file [file join $build_dir drc.txt]
report_utilization -file [file join $build_dir utilization.txt]
write_checkpoint -force [file join $build_dir validation_ila.dcp]
write_debug_probes -force [file join $build_dir validation_ila.ltx]
write_bitstream -force [file join $build_dir validation_ila.bit]
puts "Built ILA bitstream/probes in $build_dir. No board was programmed."
puts "Hardware Manager: BASIC capture qualification sample_valid == 1."
puts "Basic trigger: sample_valid == 1 AND mismatch == 1."
