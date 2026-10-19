# 회로·디지털 하드웨어 기초 모델 | Circuit and digital hardware foundation models

저장소 루트에서 실행한다. Python 표준 라이브러리만 사용한다.

Run from the repository root. The Python examples use only the standard library.

```bash
python -m unittest discover -s examples/foundations/circuits_hardware -p "test_*.py" -v
```

| 모델 / Model | 확인하는 내용 / Checks |
|---|---|
| RC, series RLC | 해석해와 수치 적분, 시정수, 감쇠, 에너지 / Analytical versus numerical integration, time constant, damping, energy |
| NMOS square law | 채널 전하 적분, 영역 경계, 단조성 / Channel-charge integration, region boundary, monotonicity |
| Synchronous FIFO | 모든 길이 6 요청열과 무작위 순서·리셋 / All length-six request sequences plus randomized ordering and reset |
| Direct-mapped cache | 수작업 추적, 독립 블록 모델, 평균 지연 / Hand trace, independent block model, average latency |
| Lossless line | 반사 경계, 전력 보존, 직류 극한 / Reflection boundaries, power conservation, DC limit |
| Probe and uncertainty | 직류 분압, 극점, 상관 및 표본 검산 / DC divider, pole, correlation and sampling checks |

FIFO의 Python 모델과 RTL은 같은 명세를 구현하지만 서로 다른 프로그램이다. Python 테스트의 통과를 RTL 시뮬레이션 통과로 해석하지 않는다. `sync_fifo.sv`의 파라미터는 `WIDTH >= 1`, `DEPTH >= 1`이며 `PTR_W`, `COUNT_W`는 기본값을 사용한다. 동기식 active-high 리셋이며 메모리 내용 대신 유효 점유량을 초기화한다. 읽기 데이터는 수락한 상승 에지 뒤에 `rd_valid`와 함께 유효하다.

The Python FIFO and RTL implement the same contract as separate programs. Passing the Python tests does not establish RTL simulation success. `sync_fifo.sv` requires `WIDTH >= 1` and `DEPTH >= 1`; keep the default `PTR_W` and `COUNT_W`. It uses a synchronous active-high reset and resets occupancy rather than clearing the memory array. Read data becomes valid with `rd_valid` after the accepting rising edge.

Icarus Verilog가 설치된 환경에서는 다음과 같이 깊이 1과 3을 각각 검사한다. 산출물은 추적하지 않는 `build/`에 둔다.

With Icarus Verilog installed, exercise depths one and three separately. Keep generated files in the ignored `build/` directory.

```bash
mkdir -p build
iverilog -g2012 -s tb_sync_fifo -Ptb_sync_fifo.DEPTH=1 -o build/fifo1 examples/foundations/circuits_hardware/sync_fifo.sv examples/foundations/circuits_hardware/tb_sync_fifo.sv
vvp build/fifo1
iverilog -g2012 -s tb_sync_fifo -Ptb_sync_fifo.DEPTH=3 -o build/fifo3 examples/foundations/circuits_hardware/sync_fifo.sv examples/foundations/circuits_hardware/tb_sync_fifo.sv
vvp build/fifo3
```

수치 모델은 명시된 이상화 조건을 검사한다. 실제 부품의 공정 모델, FPGA 합성·타이밍 보고서, 계측기 교정 성적서나 실측 자료를 대신하지 않는다.

The numerical models check the stated idealizations. They do not substitute for process models, FPGA synthesis and timing reports, instrument calibration certificates, or physical measurements.
