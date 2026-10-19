# Transformer와 DRAM-PIM

문자 단위 Transformer를 SystemVerilog로 구현하고, Python 정수 기준 모델과 같은 입력·가중치로 계산 결과를 대조했습니다. 행렬 연산, attention, LayerNorm, GELU, residual, K/V cache를 연결한 추론 회로와 메모리 데이터 이동 분석을 담았습니다.

## 구현

- GPT decoder: vocabulary 65, hidden dimension 16, attention head 4개, FFN dimension 32, decoder layer 2개
- Signed Q8.8 연산, 학습된 bias와 LayerNorm gamma/beta, GELU LUT
- 전체 context 재계산과 token 단위 K/V cache 경로
- E8M7 MAX-EX 누산기, 일반 곱·덧셈 트리, max/average Pooling PU
- DRAM bank/row 전송량 모델과 FIFO·공유 버스·refresh 이벤트 시뮬레이터
- Nexys 4 DDR의 clock·UART·pin 제약과 Vivado 빌드 코드

`model/`은 정수 기준 모델과 CPU 학습·QAT 코드, `rtl/`은 회로, `tb/`는 testbench, `analysis/`는 메모리 모델입니다. `fpga/nexys4_ddr/`에 보드용 빌드·UART 도구를 두었습니다. 학습된 소형 모델은 `output/tiny_gpt_full_ops/`와 `output/tiny_gpt_full_ops_qat/`에 있습니다.

## 수치 검증

2026년 10월 19일에 Python 회귀 55개와 DRAM 이벤트 경계 시험 40개를 실행했습니다. 기본 RTL, 학습 checkpoint의 K/V cache 생성, Pooling, MAX-EX, 일반 E8M7 트리, 가중치 export도 다시 실행했습니다.

| 검사 | 결과 |
|---|---|
| QAT K/V cache 생성 | 7개 transaction, logits 455개·hidden 112개가 Python 기준과 일치 |
| 생성 시험 입력 | `ROMEO:` → 추가 문자 `\nA`, 38,465 simulation cycles·37,744 MAC |
| Python offline 입력 | `RO` → `RORI` |
| Pooling 표본 | WINDOW 1·3·16, 조합 200개·등록 출력 260개 일치 |
| MAX-EX 표본 | 3·16 lane, guard 16·32의 출력 248개가 정수 기준과 일치 |
| DRAM 이벤트 입력 | READ/WRITE 2,336개, FIFO·refresh 조건에서 baseline 12,246 / PIM 3,760 cycle |

이전 Vivado 2024.1 구현에서는 Nexys 4 DDR의 32-token distributed cache 구성을 2.5 MHz로 배치·배선했습니다. LUT 46,374개, FF 8,473개, DSP 194개, WNS +33.471 ns, WHS +0.047 ns였고 bitstream을 생성했습니다. 배선 지연 XSim은 Inertial100 정책의 context 8·32 × slow/max·fast/min 네 조건에서 각각 logits 130개가 일치했습니다. 기본 Transport0 실행은 중단된 기록으로 남아 있습니다. 해당 수치는 저장된 구현 기록이며 2026-10-19 검사에서 Vivado를 다시 실행한 값은 아닙니다.

실물 FPGA의 UART 출력·지연·전력과 DRAM-PIM 칩은 측정 범위에 포함하지 않습니다. 보드 이름의 DDR2를 Transformer의 외부 메모리로 연결한 설계도 아닙니다. 수치 일치는 회로 구현의 검증이고, 작은 문자 모델의 문장 품질 평가는 별개입니다.

## DRAM-PIM 분석

기본 전송량 모델은 prompt마다 가중치를 한 번 읽는 unfused baseline과, 가중치·중간 activation을 메모리 가까이에 유지하는 PIM 가정을 비교합니다. host-memory 경계 전송량은 114,688 byte와 34,816 byte로 계산됐습니다. 69.64%는 이 조건의 전송량 차이이며 처리속도나 소비전력의 측정값이 아닙니다.

캐시·반복 실행 분석에서는 가중치 재사용과 중간값 유지 조건을 바꿔 비교합니다. 같은 경계에서 같은 데이터를 유지하는 이상적 host 모델과 PIM의 전송량은 같아질 수 있습니다. 이벤트 모델은 유한 FIFO, bank timing, 공유 command/data bus, all-bank refresh를 별도로 계산합니다.

## 실행

Python 3.12 이상과 Icarus Verilog가 필요합니다. 정수 기준 모델·RTL 시험에는 PyTorch가 필요하지 않습니다. `iverilog`와 `vvp`를 PATH에서 찾습니다.

```powershell
python -m unittest analysis.test_dram_pim_model analysis.test_dram_pim_sensitivity model.test_gpt_q88 model.test_e8m7 model.test_e8m7_maxex model.test_config_metadata
python tools/test_dram_event_simulator.py
python run_tests.py
python verify_trained_generation.py --checkpoint output/tiny_gpt_full_ops_qat/tiny_gpt_qat_q88.json --prompt 'ROMEO:' --tokens 2 --kvcache-rtl
python fpga/nexys4_ddr/host.py --offline --prompt RO --tokens 2
```

메모리 분석과 가중치 export:

```powershell
python analysis/dram_pim_model.py --output-dir build/memory-run
python analysis/dram_pim_event_simulator.py --input-csv build/memory-run/dram_pim_command_trace.csv --output-dir build/event-run
python tools/export_vivado_weights.py --output build/vivado_weights
```

CPU 재학습은 `requirements-training.txt`, 보드 UART 연결은 `requirements-uart.txt`를 사용합니다. Vivado 빌드는 `fpga/nexys4_ddr/build.ps1`에서 실행 파일·임시 경로·context·cache 구성을 인수로 받습니다. `build/` 아래 결과는 실행할 때 생성합니다.

## 학습 데이터

문자 모델의 학습 원문은 [karpathy/char-rnn의 Tiny Shakespeare](https://github.com/karpathy/char-rnn/tree/master/data/tinyshakespeare)입니다. 학습 코드의 원문 SHA-256은 `86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed`이며, corpus 원문이나 외부 도구·라이브러리는 이 폴더에 포함하지 않았습니다.

## English

This character-level Transformer is implemented in SystemVerilog and compared with a Python integer reference using the same inputs and weights. The design connects matrix arithmetic, attention, LayerNorm, GELU, residuals and a K/V cache, alongside memory-traffic analysis.

### Implementation

- GPT decoder: 65 characters, hidden width 16, four attention heads, FFN width 32 and two decoder layers.
- Signed Q8.8, trained biases/LayerNorm gamma-beta and a GELU LUT.
- Full-context recomputation and token-stream K/V-cache paths.
- E8M7 MAX-EX accumulator, conventional multiply/add tree and max/average pooling units.
- DRAM bank/row traffic model and FIFO/shared-bus/refresh event simulation.
- Nexys 4 DDR clock/UART/pin constraints and Vivado build tools.

`model/` contains integer references and CPU training/QAT; `rtl/` contains circuits, `tb/` testbenches and `analysis/` memory models. Board build/UART tools are in `fpga/nexys4_ddr/`. Small trained checkpoints are in `output/tiny_gpt_full_ops/` and `output/tiny_gpt_full_ops_qat/`.

### Numerical checks and historical implementation

On October 19, 2026, 55 Python regressions and 40 DRAM-event boundary tests ran alongside basic RTL, checkpoint K/V generation, pooling, MAX-EX, conventional E8M7 trees and weight export.

| Check | Result |
| --- | --- |
| QAT K/V generation | Seven transactions; all 455 logits and 112 hidden values matched Python |
| Generation input | `ROMEO:` → extra `\nA`; 38,465 simulated cycles and 37,744 MACs |
| Offline Python | `RO` → `RORI` |
| Pooling | Windows 1/3/16; 200 combinational and 260 registered outputs matched |
| MAX-EX | Three/sixteen lanes, guards 16/32; 248 outputs matched the integer reference |
| DRAM events | 2,336 READ/WRITE commands with FIFO/refresh; baseline 12,246 versus PIM 3,760 cycles |

A historical Vivado 2024.1 run placed/routed the 32-token distributed-cache Nexys 4 DDR configuration at 2.5 MHz: 46,374 LUTs, 8,473 FFs, 194 DSPs, WNS +33.471 ns and WHS +0.047 ns, with a generated bitstream. Post-route XSim with Inertial100 matched 130 logits in each of four context-8/32 × slow/max/fast/min conditions. The default Transport0 run remains recorded as interrupted. These are archived implementation records, not a new Vivado run.

Physical UART latency/power and a DRAM-PIM chip were not measured. The design does not connect the board's external DDR2 as Transformer memory. Arithmetic agreement validates the implementation; language quality is a separate property of the small model.

### DRAM-PIM analysis

The basic traffic model compares an unfused baseline that reads weights once per prompt with a PIM assumption that keeps weights/intermediate activations near memory. Host-memory traffic is 114,688 versus 34,816 bytes. The resulting 69.64% difference is modeled traffic, not measured speed or power.

Cache/repetition analysis varies weight reuse and intermediate residency. An ideal host retaining the same data at the same boundary can have the same traffic as PIM. The event model separately handles finite FIFOs, bank timing, shared command/data buses and all-bank refresh.

### Execution and data

Use Python 3.12+ and Icarus Verilog, with `iverilog`/`vvp` on PATH. Integer references and RTL tests need no PyTorch. The commands above run Python/event/RTL checks, QAT generation and offline host inference, then generate traffic/event reports and Vivado weights. CPU retraining uses `requirements-training.txt`; board UART uses `requirements-uart.txt`. `fpga/nexys4_ddr/build.ps1` accepts tool, temporary-path, context and cache options. Runs create artifacts under `build/`.

Training text comes from [Tiny Shakespeare in karpathy/char-rnn](https://github.com/karpathy/char-rnn/tree/master/data/tinyshakespeare), with SHA-256 `86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed`. Corpus text, external tools and libraries are not bundled.
