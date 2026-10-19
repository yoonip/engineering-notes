# FPGA Validation Harness

입력 패턴 생성, 데이터 무결성 검사, 오류 주입, 실패 기록 저장을 다루는 검증 실습이다. Python에서는 가상 ADC와 8채널 binary frame을 검사하고, RTL에서는 순번과 기대값을 생성해 정상 동작과 오류 주입을 비교한다.

## Python

`validation_lab.py`는 12-bit signed ADC 코드를 생성한다. 샘플 개수와 순서, 전압 오차 등을 검사하고 CSV·JSON·이벤트 기록을 저장한다. 실패 상태를 reset 전에 보존한 뒤 장치 종료 처리를 수행한다.

```sh
python validation_lab.py --scenario healthy
python validation_lab.py --scenario offset
python validation_lab.py --scenario data-loss
python validation_lab.py --scenario timeout
python validation_lab.py --scenario healthy --decode unsigned
```

| 결과 | 종료 코드 |
| --- | --- |
| PASS | 0 |
| FAIL | 1 |
| TIMEOUT | 2 |
| ERROR | 3 |

`offline_fpga_measurement_lab.py`는 8채널 × uint16 little-endian frame을 검사한다. 정상 입력과 byte swap, channel swap, frame 누락, short read, zero fill, timeout을 비교한다.

```sh
python offline_fpga_measurement_lab.py --out lab_results
```

두 프로그램의 입력은 소프트웨어로 생성한다. 실제 ADC나 FPGA 전송 데이터를 읽는 인터페이스는 이 코드에 포함하지 않았다.

## RTL

`nexys4_ddr/validation_top.v`는 100 MHz 입력 클록에서 검증 패턴을 생성한다. `SW[0]`은 샘플 생성을 제어하고, `SW[1]`은 16번째 샘플마다 1-bit 오류를 주입한다. 기대값·실제값·오류 횟수는 ILA 관측용 신호로 지정했다.

```sh
iverilog -g2012 -s tb_validation_top -o validation.vvp nexys4_ddr/validation_top.v nexys4_ddr/tb_validation_top.sv
vvp validation.vvp
```

Testbench는 정상 32개와 오류 주입 32개의 패턴, pause, reset을 검사한다. `build.tcl`과 `build_ila.tcl`은 Nexys4 DDR의 Artix-7을 대상으로 한 Vivado 빌드 스크립트이며, `nexys4_ddr.xdc`는 해당 보드의 핀과 클록 제약이다. XDC에 핀맵의 원 출처를 표시했다.

2026-10-19에 Python 오류 시나리오 5개, binary frame 시나리오 7개, RTL의 64개 패턴을 실행해 판정과 실패 기록·종료 처리를 확인했다. 이번 검사는 PC 시뮬레이션으로 수행했다.

## English

This project studies pattern generation, integrity checks, fault injection and failure evidence. Python exercises simulate a signed ADC stream and eight-channel binary frames. The RTL generates reference patterns and injected mismatches for a Nexys4 DDR target.

Checks on 2026-10-19 covered five ADC scenarios, seven binary-frame scenarios and 64 RTL samples, including pause and reset. Failure snapshots and cleanup were verified. The current verification used PC simulation; board measurements and a new Vivado build were outside this run.
