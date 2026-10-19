# Run from Vivado Tcl console: source path/to/build.tcl
# Builds an LED-only target. Add ILA with Set Up Debug for the ILA exercise.
# Never connects to or programs a board.
set src [file dirname [file normalize [info script]]]
set build_dir [file normalize [file join [pwd] nexys_validation_build]]
file mkdir $build_dir
create_project -in_memory -part xc7a100tcsg324-1
read_verilog [file join $src validation_top.v]
read_xdc [file join $src nexys4_ddr.xdc]
synth_design -top validation_top -part xc7a100tcsg324-1
opt_design
place_design
route_design
report_timing_summary -file [file join $build_dir timing_summary.txt]
report_drc -file [file join $build_dir drc.txt]
write_checkpoint -force [file join $build_dir validation_top.dcp]
write_bitstream -force [file join $build_dir validation_top.bit]
puts "Built in $build_dir. No board was programmed."
