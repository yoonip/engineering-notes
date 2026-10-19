# OpenOCD · GDB · Debugging

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

디버깅은 관찰한 현상과 원인을 연결하는 과정이다. 소프트웨어 디버거, 디버그 프로브, 칩의 디버그 인터페이스는 서로 다른 구성요소다. 회로 문제와 펌웨어 문제는 비슷한 증상을 만들기도 한다.

## 연결 구조

GDB는 실행 제어와 변수·메모리 조회를 맡는다. OpenOCD는 지원하는 프로브와 대상 장치를 연결하고 GDB 서버, flash 기록, 실행 제어 등을 제공한다. JTAG·SWD는 대상 칩과 통신하는 디버그 인터페이스다. ST-Link·J-Link는 프로브 제품군이며 pyOCD·probe-rs도 대상별 디버그 도구다.

## 관찰 도구의 차이

Breakpoint는 특정 위치에서 실행을 멈추고, watchpoint는 메모리 접근 조건에 반응한다. 정지 상태의 관찰은 타이밍을 바꿀 수 있다. HardFault 분석에는 원인 상태 레지스터, 예외 당시의 스택, PC·LR 같은 실행 정보가 연결된다. SWO·ETM은 지원 장치에서 trace와 실행 관찰에 사용된다.

오실로스코프는 전압의 시간 파형을, 로직애널라이저는 디지털 상태와 프로토콜을 관찰한다. Saleae·PulseView·sigrok은 디지털 신호 분석 생태계다. 소프트웨어 로그와 실제 핀 파형의 시간이 맞아야 통신 실패나 응답 지연을 해석할 수 있다.

## 관련 기술

OpenOCD, GDB, LLDB, J-Link, ST-Link, pyOCD, probe-rs, JTAG, SWD, SWO, ETM, Saleae, PulseView, Sigrok

## 참고 자료

- [About OpenOCD](https://openocd.org/doc/html/About.html)
- [GDB documentation](https://sourceware.org/gdb/documentation/)

## 디버거와 대상 연결

GDB는 ELF의 심볼과 디버그 정보를 읽어 소스, 변수와 CPU 상태를 연결한다. OpenOCD는 GDB의 요청을 대상의 디버그 기능으로 전달하는 서버다. 물리 보드에서는 ST-LINK 같은 프로브와 JTAG 또는 SWD를 통해 칩에 연결한다. USB, JTAG와 SWD는 연결 위치와 역할이 서로 다르다.

```text
GDB → OpenOCD → 디버그 프로브 → JTAG/SWD → 대상 칩
GDB → OpenOCD → remote_bitbang → Spike 가상 JTAG
GDB → Renode의 GDB 서버 → 가상 Cortex-M
```

OpenOCD가 C 코드를 컴파일하거나 CPU를 가상으로 실행하는 것은 아니다. GDB의 요청을 전달하고 CPU 정지·재개, 레지스터·메모리 접근 등의 디버그 동작을 제공한다. [OpenOCD 공식 문서](https://openocd.org/doc/html/GDB-and-OpenOCD.html)

| GDB 명령 | 의미 |
| --- | --- |
| `target extended-remote localhost:3334` | 이 실습의 OpenOCD GDB 서버에 연결 |
| `monitor halt` | 대상 정지 요청을 디버그 서버에 전달 |
| `load` | ELF의 적재 대상 코드·데이터를 메모리에 기록 |
| `break main` | `main` 진입 위치에 중단점 설정 |
| `stepi` | 기계 명령 하나 실행 |
| `info registers` | CPU 레지스터 조회 |
| `x/wx &result` | `result` 주소의 32비트 값 조회 |

`3334`는 현재 Spike 실습의 설정값이다. 기본값이나 모든 타깃의 공통 포트라는 뜻은 아니다. STM32의 Flash 기록과 리셋 절차는 대상의 메모리 맵과 OpenOCD 설정을 따른다.

## 메모리 검사와 오류 주입

패턴을 기록하고 다시 읽어 기대값과 비교한다. 결과에는 오류 수, 첫 오류 인덱스, 기대값과 관찰값을 남긴다. 정상·오류 주입·복원을 같은 절차로 실행해 판정 경로를 확인한다.

Spike+OpenOCD의 저장된 실행 기록에서는 정상 상태의 오류 수가 0이었고, 인덱스 17의 bit 0을 바꾼 뒤에는 오류 1개가 검출됐으며, 복원 뒤에는 다시 0이었다. Renode의 소프트웨어 메모리 회귀검사는 29개 사례를 포함한다. 모두 가상 대상의 소프트웨어 검사 결과다.
