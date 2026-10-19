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
