library ieee;  -- 표준 논리와 숫자 패키지의 라이브러리
use ieee.std_logic_1164.all;  -- clk·enable·clear의 논리 신호
use ieee.numeric_std.all;  -- unsigned와 정수 변환

entity mod10_counter is  -- 입력과 출력으로 정의한 회로 경계
    port (  -- 외부에서 연결할 핀 목록
        clk : in std_logic;  -- 상태가 바뀌는 상승 에지
        clear : in std_logic;  -- enable보다 우선하는 동기 초기화
        enable : in std_logic;  -- 1인 클록에서만 증가
        count : out unsigned(3 downto 0)  -- 0부터 9를 표현할 네 비트
    );  -- 포트 선언 끝
end entity;  -- 회로 인터페이스 끝

architecture rtl of mod10_counter is  -- 레지스터와 다음 상태의 구현
    signal value : natural range 0 to 9 := 0;  -- 시뮬레이션의 정수 범위도 제한
begin  -- 동시 실행되는 회로 연결 시작
    count <= to_unsigned(value, count'length);  -- 내부 값을 네 비트 출력으로 연결
    process (clk)  -- 클록 이벤트에 반응하는 순차 회로
    begin  -- 클록 처리 시작
        if rising_edge(clk) then  -- 상승 에지에서만 상태 변경
            if clear = '1' then  -- 초기화가 증가보다 먼저
                value <= 0;  -- 다음 레지스터 값을 0으로 예약
            elsif enable = '1' then  -- 증가가 허용된 클록
                if value = 9 then  -- 네 비트의 15 대신 십진 경계 사용
                    value <= 0;  -- 9 다음에는 0으로 순환
                else  -- 0부터 8인 상태
                    value <= value + 1;  -- 한 번의 클록에서 1 증가
                end if;  -- 범위 경계 분기 끝
            end if;  -- 둘 다 0이면 값을 유지
        end if;  -- 상승 에지 처리 끝
    end process;  -- 레지스터의 다음 상태 정의 끝
end architecture;  -- 회로 구현 끝
