# FPGA Validation Harness

입력 패턴 생성, 데이터 무결성 검사, 오류 주입, 실패 기록 저장을 다루는 검증 실습입니다. Python에서는 가상 ADC와 8채널 binary frame을 검사하고, RTL에서는 순번과 기대값을 생성해 정상 동작과 오류 주입을 비교합니다.

## Python

`validation_lab.py`는 12-bit signed ADC 코드를 생성합니다. 샘플 개수와 순서, 전압 오차 등을 검사하고 CSV·JSON·이벤트 기록을 저장합니다. 실패 상태를 reset 전에 보존한 뒤 장치 종료 처리를 수행합니다.

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

`offline_fpga_measurement_lab.py`는 8채널 × uint16 little-endian frame을 검사합니다. 정상 입력과 byte swap, channel swap, frame 누락, short read, zero fill, timeout을 비교합니다.

```sh
python offline_fpga_measurement_lab.py --out lab_results
```

두 프로그램의 입력은 소프트웨어로 생성합니다. 실제 ADC나 FPGA 전송 데이터를 읽는 인터페이스는 이 코드에 포함하지 않았습니다.

## RTL

`nexys4_ddr/validation_top.v`는 100 MHz 입력 클록에서 검증 패턴을 생성합니다. `SW[0]`은 샘플 생성을 제어하고, `SW[1]`은 16번째 샘플마다 1-bit 오류를 주입합니다. 기대값·실제값·오류 횟수는 ILA 관측용 신호로 지정했습니다.

```sh
iverilog -g2012 -s tb_validation_top -o validation.vvp nexys4_ddr/validation_top.v nexys4_ddr/tb_validation_top.sv
vvp validation.vvp
```

Testbench는 정상 32개와 오류 주입 32개의 패턴, pause, reset을 검사합니다. `build.tcl`과 `build_ila.tcl`은 Nexys4 DDR의 Artix-7을 대상으로 한 Vivado 빌드 스크립트이며, `nexys4_ddr.xdc`는 해당 보드의 핀과 클록 제약입니다. XDC에 핀맵의 원 출처를 표시했습니다.

2026-10-19에 Python 오류 시나리오 5개, binary frame 시나리오 7개, RTL의 64개 패턴을 실행해 판정과 실패 기록·종료 처리를 확인했습니다. 이번 검사는 PC 시뮬레이션으로 수행했습니다.

## English

This validation exercise covers pattern generation, integrity checks, fault injection and failure records. Python simulates an ADC stream and eight-channel binary frames; RTL generates sequence numbers and expected values for normal/fault-injected comparisons.

### Python paths

`validation_lab.py` generates 12-bit signed ADC codes and checks sample count, order and voltage error. It saves CSV, JSON and event records, preserving a failure snapshot before reset and cleanup. The scenarios listed above cover healthy, offset, data loss, timeout and an unsigned-decoding mismatch. Exit codes are PASS=0, FAIL=1, TIMEOUT=2 and ERROR=3.

`offline_fpga_measurement_lab.py` checks eight-channel uint16 little-endian frames against byte swap, channel swap, missing frame, short read, zero fill and timeout scenarios. Both programs use software-generated inputs; a physical ADC/FPGA acquisition interface is outside this code.

### RTL and verification

`nexys4_ddr/validation_top.v` generates patterns from a 100 MHz input clock. `SW[0]` enables samples; `SW[1]` injects one bit error every sixteenth sample. Expected values, observed values and error counts are marked for ILA observation. The commands above compile and run the Icarus testbench.

The testbench checks 32 normal and 32 fault-injected patterns, pause and reset. `build.tcl` and `build_ila.tcl` target the Nexys4 DDR Artix-7; `nexys4_ddr.xdc` supplies board pin/clock constraints with attribution to the pin-map source.

On October 19, 2026, five ADC scenarios, seven frame scenarios and 64 RTL patterns verified verdicts, failure snapshots and cleanup through PC simulation. Board measurements and a new Vivado build were outside that run.
