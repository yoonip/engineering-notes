create_clock -name core_clk -period 10.000 [get_ports clk] ; # 클록 주기의 입력 계약
set_clock_uncertainty 0.1 [get_clocks core_clk] ; # 클록 불확실성으로 따로 남긴 여유
set_input_delay -clock core_clk -max 2.0 [get_ports {rst in_valid in_data* out_ready}] ; # 가장 늦은 외부 입력 도착
set_input_delay -clock core_clk -min 0.2 [get_ports {rst in_valid in_data* out_ready}] ; # 가장 빠른 외부 입력 도착
set_output_delay -clock core_clk -max 2.0 [get_ports {in_ready out_valid out_data*}] ; # 외부 수신 회로의 최대 지연 조건
set_output_delay -clock core_clk -min 0.2 [get_ports {in_ready out_valid out_data*}] ; # 외부 수신 회로의 최소 지연 조건
