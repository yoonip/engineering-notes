# VHDL 동기 카운터의 정지·증가·십진 순환

[하드웨어 학습목차](../../README.md) · [언어와 검증 도구](../../언어와검증도구_languages-and-verification.md)

## 회로의 계약

이 예제는 공식 문서의 언어·실행 방법을 참고하여 직접 작성한 카운터와 독립 테스트벤치입니다.
상승 에지에서 clear가 1이면 0으로 초기화하고, 그렇지 않고 enable이 1이면 증가합니다.
9 다음 값은 0이며, clear와 enable이 모두 0이면 현재 값을 유지합니다.
출력은 네 비트 unsigned이며 유효 상태는 0부터 9입니다.

| 입력·출력 | 의미 |
| --- | --- |
| clk | 상승 에지에서 상태를 저장하는 클록 |
| clear | enable보다 우선하는 동기 초기화 |
| enable | 증가 허용; 0이면 정지 |
| count[3:0] | 현재 십진 상태 |

비동기 초기화, 버튼 디바운스, 여러 클록 영역은 이 작은 회로의 입력 계약에 포함하지 않습니다.

## 원본 코드와 줄별 메모

[counter.vhd](counter.vhd)는 합성 대상 회로이며 [tb_counter.vhd](tb_counter.vhd)는 시뮬레이션 전용 검증 회로입니다.
두 파일의 의미 있는 각 줄에는 문법과 그 줄이 필요한 목적을 개인 복습 메모로 적었습니다.

| 문법 | 이 회로에서의 역할 |
| --- | --- |
| entity / port | 회로의 외부 연결 정의 |
| architecture | 레지스터와 출력 연결 구현 |
| natural range 0 to 9 | 정수 상태의 시뮬레이션 범위 명시 |
| process(clk), rising_edge(clk) | 상승 에지에서만 다음 상태 저장 |
| signal의 <= | 신호의 다음 값을 예약; 뒤의 출력 연결에도 델타 사이클 필요 |
| 테스트벤치 변수의 := | 기준 모델의 정수 값을 즉시 변경 |
| assert ... severity failure | 기대와 다른 값이면 실행을 실패로 종료 |
| wait / std.env.finish | 검증 시간 진행과 정상 종료; 테스트벤치의 역할 |

동시 할당 count <= ...는 소프트웨어의 순차 출력 함수가 아니라 항상 연결된 조합 회로입니다.
0..9를 나타내는 정보는 네 비트이며, 실제 장치의 레지스터·LUT 사용량은 합성 결과로 확인합니다.

## 같은 자극의 시간 흐름

VHDL과 [Amaranth 예제](../05-파이썬회로_amaranth-counter/README.md)는 같은 80클록의 입력을 사용합니다.
클록 주기는 10ns이며 주기 시작에 입력을 바꾸고, 4ns에 에지 전 유지, 5ns에 상승, 6ns에 다음 상태를 검사합니다.
clear는 주기 번호 0,17,18,47,79에서 1이고 enable은 주기 번호를 5로 나눈 나머지가 2일 때만 0입니다.
기준 모델은 정수 (expected+1) mod 10으로 계산하여 DUT의 명시적인 value=9 분기와 비교합니다.

| 주기 번호 | clear | enable | 상승 뒤 count | 확인할 조건 |
| ---: | ---: | ---: | ---: | --- |
| 0 | 1 | 1 | 0 | 초기화가 증가보다 우선 |
| 1 | 0 | 1 | 1 | 한 에지에서 한 번 증가 |
| 2 | 0 | 0 | 1 | enable이 0이면 유지 |
| 11 | 0 | 1 | 9 | 유효 범위의 마지막 값 도달 |
| 12 | 0 | 0 | 9 | 경계에서도 정지 가능 |
| 13 | 0 | 1 | 0 | 9에서 0으로 순환 |
| 18 | 1 | 1 | 0 | 중간 초기화의 우선순위 |
| 79 | 1 | 1 | 0 | 마지막 클록의 초기화 |

한 클록마다 에지 전 유지·에지 후 기대값·출력 범위의 세 조건을 검사하여 총 240개의 assert를 실행합니다.
검사한 이진 입력 시나리오에서의 기능 검증이며, 가능한 모든 입력 시퀀스를 전수 조사한 기록과는 범위가 다릅니다.

## 실행 방법과 확인한 결과

GHDL이 경로에 잡힌 환경에서 이 예제 디렉터리의 상대 파일명을 사용합니다.

```sh
ghdl -a --std=08 counter.vhd tb_counter.vhd  # 회로와 테스트벤치 분석
ghdl -e --std=08 tb_counter  # 독립 테스트벤치 구체화
ghdl -r --std=08 tb_counter --assert-level=error  # 오류를 실패로 처리하여 실행
```

GHDL 6.0.0 mcode, GNAT 15.2.0의 Windows 배포본으로 실행하여 다음 표식을 확인했습니다.

```text
PASS mod10_counter cycles=80 checks=240
simulation finished @800ns with status 0
```

실제 report 행에는 도구가 파일명·줄 번호·시각을 앞에 붙입니다.
한글 절대 소스 경로를 분석 데이터베이스에 기록하면 이 GHDL 배포본에서 문자 오류가 발생했습니다.
검사 때에는 두 소스를 바이트 그대로 임시 작업 디렉터리에 복사하고 counter.vhd와 tb_counter.vhd라는 상대 이름으로 실행했습니다.
도구 버전·공식 다운로드·실제 명령·파일 SHA256은 [example.json](example.json)에 기록합니다.

## 장치 사용과 검증 범위

value의 초기값 0은 시뮬레이션 시작 조건이며 실제 장치에서는 클록에 맞는 clear를 제공하는 초기화 절차를 설계합니다.
외부 버튼 같은 비동기 입력은 동기화와 필요한 디바운스를 거쳐야 합니다.
이번 확인 범위는 VHDL 분석·구체화·기능 시뮬레이션입니다.
합성·배치 배선·클록 제약·핀 전압·보드에서의 측정은 별도 단계입니다.

## 공식 참고와 라이선스 범위

[GHDL 공식 전가산기와 테스트벤치](https://ghdl.github.io/ghdl/quick_start/simulation/adder/index.html)에서 분석·구체화·실행과 assert 기반 검사 절차를 참고합니다.
회로와 검증 코드는 이 저장소용으로 직접 작성했으며 해당 전가산기 코드를 복사하지 않았습니다.
[GHDL 공식 릴리스](https://github.com/ghdl/ghdl/releases/tag/v6.0.0)의 실행 도구는 GPL로 배포되며, 이 예제는 도구의 원본 코드를 포함하지 않습니다.
참조 문서와 도구의 라이선스를 새 회로의 출처·허가 조건으로 혼용하지 않습니다.

## counter.vhd의 전체 코드

```vhdl
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
```

## tb_counter.vhd의 전체 코드

```vhdl
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
```
