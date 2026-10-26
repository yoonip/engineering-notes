# 하드웨어 코딩 실행·채점 확인 — 2026-10-26

[학습 목차](README.md) · [사이트 채점 화면](HDLBits/확인기록_online-grading.md)

## 확인한 결과

| 구분 | 이 실행의 범위 | 결과 |
| --- | --- | --- |
| HDLBits 사이트 제출 | 서로 다른 문제 12개, 최종 solution.v와 제출 소스 해시 대조 | 모두 Success! 확인 |
| 로컬 기능 시뮬레이션 | 자료 17개, 정상 설정 20개 | 모두 통과 |
| 테스트벤치 비교 | 정상 설정에서 집계한 비교 282,474회 | 모두 일치 |
| 의도적 결함 대조 | 버퍼 유실·UART 비트 순서·상태기계 겹침 오류 3설정 | 컴파일 후 예상 기능 불일치 검출 |
| Amaranth 회로 출력 | 모델 시뮬레이션과 별도로 RTLIL 생성 1회 | 출력 구조와 기록된 해시 일치 |

로컬의 실제 명령·표준 출력·오류·종료 코드는 [validation.json](validation.json)에 있습니다. 사이트의 판정과 횟수는 별도의 온라인 기록에서 확인합니다. 결함 대조는 컴파일 오류나 시간 초과가 아니라 지정한 DUT 불일치로 실패했는지 확인했습니다.

## 자료별 로컬 실행

| 자료 | 정상 설정 통과 | 예상 결함 검출 | 결과 |
| --- | --- | --- | --- |
| [예제_examples/01-전송대기_elastic-buffer](예제_examples/01-전송대기_elastic-buffer/README.md) | 1 | 1 | 통과 |
| [예제_examples/02-직렬송신_uart-tx](예제_examples/02-직렬송신_uart-tx/README.md) | 4 | 1 | 통과 |
| [예제_examples/03-순서검출_sequence-detector](예제_examples/03-순서검출_sequence-detector/README.md) | 1 | 1 | 통과 |
| [예제_examples/04-카운터와범위_vhdl-counter](예제_examples/04-카운터와범위_vhdl-counter/README.md) | 1 | 0 | 통과 |
| [예제_examples/05-파이썬회로_amaranth-counter](예제_examples/05-파이썬회로_amaranth-counter/README.md) | 1 | 0 | 통과 |
| [HDLBits/always_case2](HDLBits/always_case2/README.md) | 1 | 0 | 통과 |
| [HDLBits/count10](HDLBits/count10/README.md) | 1 | 0 | 통과 |
| [HDLBits/dff8r](HDLBits/dff8r/README.md) | 1 | 0 | 통과 |
| [HDLBits/edgedetect](HDLBits/edgedetect/README.md) | 1 | 0 | 통과 |
| [HDLBits/fadd](HDLBits/fadd/README.md) | 1 | 0 | 통과 |
| [HDLBits/fsm1s](HDLBits/fsm1s/README.md) | 1 | 0 | 통과 |
| [HDLBits/mux2to1v](HDLBits/mux2to1v/README.md) | 1 | 0 | 통과 |
| [HDLBits/popcount3](HDLBits/popcount3/README.md) | 1 | 0 | 통과 |
| [HDLBits/shift4](HDLBits/shift4/README.md) | 1 | 0 | 통과 |
| [HDLBits/step_one](HDLBits/step_one/README.md) | 1 | 0 | 통과 |
| [HDLBits/vector2](HDLBits/vector2/README.md) | 1 | 0 | 통과 |
| [HDLBits/vectorr](HDLBits/vectorr/README.md) | 1 | 0 | 통과 |

HDLBits 로컬 풀이의 비교는 274,001회, SystemVerilog 전송·UART·순서 검출의 정상 설정 비교는 7,993회, VHDL·Amaranth 카운터 비교는 각각 240회입니다. 이 수는 테스트벤치 검사식의 실행 횟수이며, 서로 다른 실제 하드웨어 조건의 수나 수학적 완전성을 뜻하지 않습니다.

## 도구와 재현 명령

| 도구 | 실제 판본 | 용도 |
| --- | --- | --- |
| Icarus Verilog·VVP | 12.0 devel, s20150603-1539-g2693dd32b | Verilog·SystemVerilog 분석과 디지털 시뮬레이션 |
| GHDL | 6.0.0, mcode | VHDL-2008 분석·전개·실행 |
| Python | 3.12.14 | 실행기·Amaranth 테스트 |
| Amaranth | 0.5.8 | 회로 모델 시뮬레이션·RTLIL 출력 |

도구 경로는 환경에 맞게 지정합니다. 실행기는 기존 소스를 새 임시 작업 폴더에 같은 바이트로 복사하여 컴파일하고, 그 복사본의 해시도 확인합니다. 아래 명령의 build 폴더와 JSON 보고서는 실행할 때 새로 기록할 위치입니다.

```bash
python -B 하드웨어코딩_hardware-coding/check_hardware.py --iverilog /path/to/iverilog --vvp /path/to/vvp --ghdl /path/to/ghdl --python-deps /path/to/amaranth-dependencies --build-dir /path/to/new-build-parent --out /path/to/new-report.json
```

실행 시각은 2026-10-26T07:30:26.471084+00:00입니다. 전체 정상·음성 대조·생성 결과는 실행기의 종료 코드 0과 함께 확인했습니다. RTL 시간 단위가 없는 HDLBits 회로에 대한 Icarus 경고는 원로그에 보존했습니다. 이 회로에는 지연문이 없고 테스트벤치에는 시간 단위가 명시되어 있습니다.

## 소스와 기존 파일 대조

실행한 예제·풀이 소스 34개의 해시와 README에 실은 소스 전체를 대조했습니다. 각 의미 있는 줄에는 문법과 목적을 짧은 복습용 주석으로 적었습니다. 작업 시작 시 Git에서 추적하던 기존 소스 3,052개를 바이트 해시로 대조했으며, 그중 기존 Python 파일 1,795개를 포함해 내용이 유지됐습니다. 새로운 Amaranth 예제와 실행기는 별도의 새 파일입니다.

## 확인하지 않은 하드웨어 조건

로컬 실행은 기능 시뮬레이션과 RTLIL 생성 범위입니다. 로컬 합성, 형식 증명, 정적 타이밍 분석, 실물 보드 측정은 수행하지 않았습니다. Amaranth에서 생성한 RTLIL을 별도 시뮬레이터로 다시 검증한 결과도 아닙니다. 온라인 문제 전체나 외부 프로젝트 전체를 완료한 기록으로 확장하지 않습니다.
