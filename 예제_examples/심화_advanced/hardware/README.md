# Hardware 심화 실행 예제 / Advanced hardware examples

Python 3.11 이상 표준 라이브러리만으로 회로·통신·계측·상태전이 모델을 실행합니다. `models.py`는 참조모델, `demo.py`는 19개 주제의 CLI, `test_models.py`는 해석해·보존식·독립 구현·전수검사와 비교하는 검산입니다. 실행 위치는 이 폴더입니다.

```bash
python demo.py --case all
python demo.py --case mna
python -m unittest -v test_models
python run_rtl.py
```

`run_rtl.py`는 기존 Icarus Verilog와 vvp가 필요합니다. PATH에서 찾거나 `--iverilog /path/to/iverilog`로 지정합니다. Windows 기본 탐색 경로는 `C:/iverilog/bin/iverilog.exe`입니다. 실행 중 기대값 파일과 컴파일 결과는 임시 폴더에 만들고 종료 후 정리합니다.

| 분야 | CLI `--case` | 핵심 검산 |
|---|---|---|
| 09 MNA | mna | KCL·전력·floating source |
| 10 weak inversion | subthreshold | 미분·10배 current ratio |
| 11 feedback | feedback | 폐루프 해석식·0 dB |
| 12 PDN | pdn | admittance 상쇄·가지 KCL |
| 13 fixed point | fixedpoint | Fraction oracle·실제 RTL |
| 14 model checking | modelcheck | 7개 상태·56개 전이·mutation |
| 15 multicycle | multicycle | setup edge와 hold edge |
| 16 VIPT | vipt | offset 내 index·alias 반례 |
| 29 RF | rf | quarter/half-wave·수동성 |
| 30 QPSK | qpsk | 이론 BER/SER·Monte Carlo |
| 31 buck | buck | RK4와 해석해·에너지 |
| 32 ADC | adc | 전이값 DNL/INL·missing code |
| 33 SRAM | sram | divider KCL·RC ODE |
| 34 credit | credits | 자리 보존·순서·왕복 지연 |
| 35 equivalence | equivalence | 1024개 전이·실제 RTL |
| 36 thermal | thermal | 누적 열 보존·정상상태 |
| 37 calibration | calibration | normal equation·공분산 |
| 51 signature | signature | 다항식 나눗셈·alias 전수검사 |
| 54 PIM | pim | holdout affine 교정·비선형 반례 |

2026-10-19 검산에서 Python 39개 테스트가 통과했습니다. Icarus 12.0/vvp에서는 고정소수점 10121개 벡터와 카운터 10257 cycle이 통과했습니다. qmul의 `always_comb` constant-select 진단은 sensitivity의 모든 비트를 포함한다는 Icarus 안내입니다. 합성·STA·formal solver·실제 회로 측정은 이 실행 결과에 포함하지 않습니다. `validation.json`은 해당 실행의 요약이며 새로운 환경의 실행을 대신하지 않습니다.

## English

These reference models use only the Python 3.11+ standard library. `models.py` contains equations and state transitions, `demo.py` exposes 19 CLI cases, and `test_models.py` compares them with analytic limits, conservation laws, independent implementations and exhaustive state/input enumeration. Run the commands above from this directory. The case table maps each topic to its command and validation method.

`run_rtl.py` requires an existing Icarus compiler and vvp. It searches PATH, accepts `--iverilog /path/to/iverilog`, and includes `C:/iverilog/bin/iverilog.exe` as the Windows fallback. Golden vectors and compiled outputs live only in a temporary directory.

On 2026-10-19, 39 Python tests passed. Icarus 12.0/vvp also passed 10121 fixed-point vectors and 10257 counter cycles. The qmul constant-select diagnostic means that Icarus includes all bits in `always_comb` sensitivity. These results do not include synthesis, STA, a formal solver proof or circuit measurements. `validation.json` records this run and does not replace execution in another environment.
