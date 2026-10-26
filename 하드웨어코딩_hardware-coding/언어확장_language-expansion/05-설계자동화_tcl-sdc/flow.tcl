set config [dict create top elastic_buffer source elastic_buffer.sv period_ns 10.0] ; # 이번 합성 작업의 이름·소스·클록 조건
if {[info exists ::env(PERIOD_NS)]} { dict set config period_ns $::env(PERIOD_NS) } ; # 실행 환경이 넘긴 클록 주기를 선택
set period [dict get $config period_ns] ; # 사전에서 사용할 주기를 한 번 꺼내기
if {![string is double -strict $period]} { error "period_ns must be a positive finite number" } ; # 숫자가 아닌 설정을 합성 전에 거절
if {$period < 0.001 || $period > 1000000 || $period != $period} { error "period_ns must be a number in 0.001..1000000" } ; # 1ps 이상 범위와 자기 비교가 다른 NaN을 함께 검사
set source [dict get $config source] ; # 공백을 쪼개지 않는 Tcl 단어로 소스 이름 전달
if {![file isfile $source]} { error "source RTL is missing" } ; # 입력 파일 부재를 먼저 알리기
set sdc [open constraints.sdc w] ; # 새 작업 폴더 안에만 제약 파일 작성
fconfigure $sdc -encoding utf-8 -translation lf ; # 한글 메모와 줄바꿈을 파일에 그대로 유지
puts $sdc [format {create_clock -name core_clk -period %.3f [get_ports clk] ; # 클록 주기의 입력 계약} $period] ; # 중괄호로 감싼 명령은 이 단계에서 실행하지 않기
puts $sdc {set_clock_uncertainty 0.1 [get_clocks core_clk] ; # 클록 불확실성으로 따로 남긴 여유} ; # STA 도구가 나중에 해석할 SDC 줄
puts $sdc {set_input_delay -clock core_clk -max 2.0 [get_ports {rst in_valid in_data* out_ready}] ; # 가장 늦은 외부 입력 도착} ; # 클록 포트는 데이터 입력 목록에서 제외
puts $sdc {set_input_delay -clock core_clk -min 0.2 [get_ports {rst in_valid in_data* out_ready}] ; # 가장 빠른 외부 입력 도착} ; # hold 검토에 필요한 최소 조건도 함께 기록
puts $sdc {set_output_delay -clock core_clk -max 2.0 [get_ports {in_ready out_valid out_data*}] ; # 외부 수신 회로의 최대 지연 조건} ; # 출력 사용처와 연결할 계약
puts $sdc {set_output_delay -clock core_clk -min 0.2 [get_ports {in_ready out_valid out_data*}] ; # 외부 수신 회로의 최소 지연 조건} ; # 최대 조건 하나로 모든 검사를 대신하지 않기
close $sdc ; # 파일 내용을 실제로 저장
set top [dict get $config top] ; # 합성 최상위 회로 이름
yosys read_verilog -sv $source ; # Yosys의 HDL 읽기 명령을 Tcl에서 호출
yosys hierarchy -check -top $top ; # 모듈 연결과 최상위 이름 확인
yosys proc ; # 순차·조합 절차를 내부 회로 셀로 변환
yosys opt ; # 상수와 불필요한 연결을 정리한 일반 회로 구조
yosys check -assert ; # 구조 검사 오류가 있으면 작업을 실패로 종료
yosys write_json design.json ; # 외부 검사기가 읽을 일반 셀·포트 정보
yosys stat ; # 도구가 실제 만든 구조의 통계 출력
puts "PASS tcl_flow top=$top period_ns=$period sdc_commands=6" ; # 성공한 Tcl 실행과 생성한 제약 명령 수 기록
