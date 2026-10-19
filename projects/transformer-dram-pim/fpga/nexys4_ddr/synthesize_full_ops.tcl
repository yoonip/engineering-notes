# Nexys 4 DDR 실기기의 Artix-7 part에 기존 full-ops 설계를 직접 합성한다.
# 이 파일은 실물 실행 전에 용량/내부 경로를 확인하는 OOC 검사이며 bitstream은 만들지 않는다.
if {[info exists ::env(TRANSFORMER_REPO)]} {
    set repo_root $::env(TRANSFORMER_REPO)
} else {
    set repo_root [file normalize [file join [file dirname [info script]] ../..]]
}
set work_root [file join $repo_root build nexys4_ddr full_ops]
puts "INFO: cwd=[pwd]; script=[info script]; repo=$repo_root; output=$work_root"
file mkdir $work_root
cd $work_root
set part_name xc7a100tcsg324-1
set_param general.maxThreads 1
puts "INFO: Nexys 4 DDR target=$part_name; original trained V65/D16/H4/F32/L2/T32 core"
read_verilog -sv [file join $repo_root rtl dram_pim_pu_synth.sv]
read_verilog -sv [file join $repo_root rtl dram_pim_vmm_bank.sv]
read_verilog -sv [file join $repo_root rtl transformer_gpt_kvcache_seq.sv]
read_verilog -sv [file join $repo_root rtl gpt_kvcache_rom_board_top.sv]
synth_design -top gpt_kvcache_rom_board_top -part $part_name -mode out_of_context
# 100 MHz board oscillator와는 별개의 내부 core 검사 조건이다.
# 실제 board flow는 MMCM/clock tree와 pin constraint까지 추가해야 한다.
create_clock -name candidate_core_clk -period 200.000 [get_ports clk]
report_utilization -file [file join $work_root utilization.rpt]
report_timing_summary -delay_type max -max_paths 10 -file [file join $work_root timing.rpt]
report_drc -file [file join $work_root drc.rpt]
write_checkpoint -force [file join $work_root synthesized.dcp]
puts "INFO: Nexys target synthesis complete; physical board operation has not been measured."
exit
