library ieee;  -- 표준 신호와 정수 변환의 라이브러리
use ieee.std_logic_1164.all;  -- 테스트 신호 자료형
use ieee.numeric_std.all;  -- unsigned 출력의 정수 비교
use std.env.all;  -- VHDL-2008의 정상 시뮬레이션 종료

entity tb_counter is  -- 외부 포트가 없는 독립 검증 회로
end entity;  -- 테스트벤치 경계 끝

architecture test of tb_counter is  -- 자극 생성과 독립 정수 기준
    signal clk : std_logic := '0';  -- 처음에는 낮은 클록
    signal clear : std_logic := '0';  -- 상승 에지에서 읽힐 초기화 입력
    signal enable : std_logic := '0';  -- 증가 허용 입력
    signal count : unsigned(3 downto 0);  -- 관찰할 실제 회로 출력
begin  -- 회로 인스턴스와 검증 프로세스 시작
    dut : entity work.mod10_counter  -- 검증 대상 원본 회로
        port map (clk => clk, clear => clear, enable => enable, count => count);  -- 이름으로 포트 연결
    stimulus : process  -- 시뮬레이션 전용 입력과 검사
        variable expected : natural := 0;  -- 정수 modulo 연산의 기준 상태
        variable checks : natural := 0;  -- 실제로 실행한 assert 수
        variable clearing : boolean;  -- 현재 클록의 초기화 조건
        variable enabled : boolean;  -- 현재 클록의 증가 조건
    begin  -- 고정된 80클록 시나리오
        for cycle in 0 to 79 loop  -- 정지·순환·중간 초기화를 반복
            clearing := cycle = 0 or cycle = 17 or cycle = 18 or cycle = 47 or cycle = 79;  -- 초기화 클록의 목록
            enabled := cycle mod 5 /= 2;  -- 매 다섯 클록 중 한 번 정지
            if clearing then clear <= '1'; else clear <= '0'; end if;  -- 에지 전에 초기화 입력 변경
            if enabled then enable <= '1'; else enable <= '0'; end if;  -- 에지 전에 증가 입력 변경
            wait for 4 ns;  -- 아직 상승 에지가 없는 구간
            assert to_integer(count) = expected report "changed before rising edge" severity failure;  -- 입력 변화만으로 상태가 바뀌지 않는지 검사
            checks := checks + 1;  -- 에지 전 유지 검사 집계
            if clearing then expected := 0; elsif enabled then expected := (expected + 1) mod 10; end if;  -- DUT의 if9 분기와 다른 정수 기준 계산
            wait for 1 ns;  -- 두 언어 모두 주기 시작 뒤 5ns에 상승
            clk <= '1';  -- 이번 클록의 상승 에지
            wait for 1 ns;  -- 신호 예약과 출력 연결의 델타 사이클 완료
            assert to_integer(count) = expected report "incorrect count after rising edge" severity failure;  -- 상승 에지 뒤 기능 비교
            checks := checks + 1;  -- 다음 상태 검사 집계
            assert to_integer(count) <= 9 report "count outside decimal range" severity failure;  -- 출력이 십진 범위인지 검사
            checks := checks + 1;  -- 범위 검사 집계
            wait for 4 ns;  -- 상승 뒤 5ns까지 높은 클록 유지
            clk <= '0';  -- 다음 주기 시작의 하강 에지
        end loop;  -- 80클록의 실제 검사 완료
        report "PASS mod10_counter cycles=80 checks=" & integer'image(checks) severity note;  -- 성공 표식과 실제 검사 수
        finish(0);  -- 실패 없이 시뮬레이션 종료
        wait;  -- 종료 함수 뒤 프로세스의 재시작 방지
    end process;  -- 독립 검증 프로세스 끝
end architecture;  -- 테스트벤치 구현 끝
