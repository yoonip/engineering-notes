# MNIST weight mapping and circuit inference

학습한 신경망의 가중치를 저항 행렬로 옮기고, 입력 영상을 전압 파형으로 변환해 회로 출력을 비교합니다. 8×8 MNIST 입력, 64–50–10 MLP, 양·음 차동 conductance, 유한 이득 TIA의 계산을 Python과 ngspice로 연결했습니다.

## 모델과 회로

신경망은 ReLU 은닉층과 선형 출력층을 사용합니다. 가중치 하나는 양의 conductance 두 개의 차이로 표현하며, 각 소자는 1–100 µS 범위의 64개 상태를 가집니다. 논리 행렬 64×50과 50×10은 각각 물리 배열 64×100과 50×20에 대응합니다. 두 층의 가중치 저항은 총 7,400개입니다.

회로는 고정 저항, 유한 이득 VCVS 증폭기, 행동 모델의 bias·정규화·ReLU로 구성합니다. Python 참조식은 TIA의 입력 노드 전압과 열별 부하를 포함한 KCL로 계산합니다. 8 µs 시점의 출력 전압을 logit으로 환산하고 참조값과 비교합니다.

## 실행 결과

기존 NumPy 학습 기록은 seed 20261011, Adam, 20 epoch 조건이며 검증 정확도로 선택된 checkpoint는 19 epoch입니다. 시험 데이터 10,000장의 소프트웨어 정확도는 부동소수점 95.91%, 64상태 가중치 양자화 95.95%입니다.

SPICE에서는 정답이 5인 첫 두 시험 표본을 사용했습니다. 표본 선택에 예측 결과를 사용하지 않았습니다. 2026년 10월 19일 소스와 netlist로 두 회로를 다시 실행했고, 저장된 모델에서 netlist를 재생성했을 때도 원본과 byte 단위로 같았습니다.

| 시험 표본 인덱스 | 정답 | Python 참조 예측 | SPICE 예측 |
| --- | --- | --- | --- |
| 8 | 5 | 6 | 6 |
| 15 | 5 | 5 | 5 |

두 회로의 최대 logit 오차는 유한 이득 Python 참조식 대비 각각 약 1.22×10⁻¹⁰, 7.80×10⁻¹¹입니다. 첫 표본의 오분류도 그대로 남겼습니다. 회로가 모델 계산을 재현했는지와 모델이 정답을 맞혔는지는 별도로 평가합니다. 10,000장 정확도는 소프트웨어 평가값이며 SPICE 실행 범위는 위 두 표본입니다.

## 파일

| 파일 | 내용 |
| --- | --- |
| `prepare_demo.py` | MNIST 전처리, NumPy 학습, checkpoint와 평가 기록 저장 |
| `export_circuit.py` | 가중치 양자화, conductance·저항 매핑, KCL 참조식, 회로 생성 |
| `verify_run.py` | 두 회로 실행, 파형 파싱, 참조 logit·예측 비교 |
| `run_demo.ps1` | Windows 실행기 |
| `model.npz` | 이 실습에서 학습한 가중치·bias 네 배열 |
| `circuit_sample_00008.cir`, `circuit_sample_00015.cir` | 입력 PWL과 두 층을 포함한 자체 생성 netlist |
| `circuit_sample_*_results.json` | 각 표본의 Python 참조값 |
| `recorded_results.json` | 기존 학습 결과와 회로 실행 범위 |

데이터셋과 시뮬레이터 실행 파일은 포함하지 않습니다. `model.npz`에는 `w1`, `b1`, `w2`, `b2`의 숫자 배열만 들어 있습니다.

## 두 회로 재실행

Python 3, NumPy, Pillow와 별도로 설치한 ngspice를 사용합니다. 이 디렉터리에서 실행합니다.

```bash
python -m pip install -r requirements.txt
python verify_run.py --run-spice --ngspice /path/to/ngspice
```

ngspice가 PATH에 있거나 `NGSPICE` 환경변수로 지정돼 있으면 `--ngspice`는 생략할 수 있습니다. Windows에서는 `ngspice_con.exe` 경로를 사용합니다.

```powershell
.\run_demo.ps1 -PythonExe python -NgspiceExe 'C:\path\to\ngspice_con.exe'
```

실행한 파형·로그와 `verified_execution.json`은 현재 디렉터리에 생성됩니다. 기존 로그와 파형만 다시 검사할 때는 `python verify_run.py`를 실행합니다.

## 재학습과 회로 생성

```bash
python prepare_demo.py --epochs 20 --seed 20261011
python export_circuit.py
```

학습 스크립트는 공식 MNIST 배포 파일을 받고 checksum을 확인합니다. 학습 50,000장·검증 10,000장·시험 10,000장을 분리하며, 생성한 `inputs.npz`와 모델을 회로 내보내기에 사용합니다. 재학습한 모델의 결과는 새 평가 기록으로 확인합니다.

내보내기 스크립트는 ngspice와 Spectre 형식을 생성합니다. 저장된 실행 근거와 이 프로젝트의 재실행 검사는 ngspice 기준입니다. Spectre 형식과 Verilog-A 출력은 별도 Cadence 환경에서 확인할 대상입니다.


## 참고 자료

- [MNIST](https://yann.lecun.org/exdb/mnist/)
- [ngspice documentation](https://ngspice.sourceforge.io/docs.html)

## English

This project maps trained neural-network weights to resistor arrays and input images to voltage waveforms. Python and ngspice connect an 8×8 MNIST input, a 64–50–10 MLP, differential conductances and finite-gain TIAs.

### Model and circuit

The network has a ReLU hidden layer and a linear output layer. Each weight is the difference of two positive conductances, each quantized to 64 states from 1 to 100 µS. Logical matrices of 64×50 and 50×10 map to physical arrays of 64×100 and 50×20, totaling 7,400 weight resistors.

The circuit uses fixed resistors, finite-gain VCVS amplifiers and behavioral bias/normalization/ReLU. The Python KCL reference includes TIA input-node voltage and column loading. Output voltages sampled at 8 µs are converted to logits and compared with that reference.

### Recorded results

The NumPy run used seed 20261011, Adam and twenty epochs; validation accuracy selected epoch 19. On 10,000 test images, floating-point software accuracy was 95.91% and 64-state quantized-weight accuracy was 95.95%.

SPICE uses the first two test samples labeled 5, selected without consulting predictions. Both circuits were rerun from the source/netlists on October 19, 2026, and exporting from the stored model reproduced the netlists byte for byte.

| Test index | Label | Python reference | SPICE |
| --- | --- | --- | --- |
| 8 | 5 | 6 | 6 |
| 15 | 5 | 5 | 5 |

Maximum logit errors against the finite-gain reference were approximately 1.22×10⁻¹⁰ and 7.80×10⁻¹¹. The first sample's misclassification is retained: reproducing a model calculation and classifying correctly are separate checks. The 10,000-image accuracy is software evaluation; SPICE covers only these two samples.

### Files and execution

`prepare_demo.py` preprocesses MNIST, trains in NumPy and saves checkpoints/evaluation records. `export_circuit.py` quantizes/maps weights, computes the KCL reference and generates circuits. `verify_run.py` runs the two circuits, parses waveforms and compares logits/predictions; `run_demo.ps1` is the Windows runner. `model.npz` contains only four numeric arrays, `w1`, `b1`, `w2` and `b2`. The two `circuit_sample_*.cir` files contain input PWL and both layers; companion JSON records references, and `recorded_results.json` describes the training and simulation scope. Datasets and simulator binaries are not bundled.

Use Python 3, NumPy, Pillow and a separate ngspice installation. Run the listed commands from this directory. `--ngspice` can be omitted when ngspice is on PATH or set through `NGSPICE`; use `ngspice_con.exe` on Windows. Execution creates waveforms, logs and `verified_execution.json` locally. `python verify_run.py` rechecks existing logs/waveforms without a new simulation.

Retraining uses the official MNIST files with checksum verification and separates 50,000 training, 10,000 validation and 10,000 test images. The exporter reads the generated `inputs.npz` and model. Evaluate newly trained weights using their new records. The exporter supports ngspice and Spectre formats; recorded execution checks use ngspice. Spectre/Verilog-A outputs require verification in a Cadence environment. Official MNIST and ngspice references are linked above.
