# Signed 부분곱 열 제거와 CNN 정확도 실험

INT6/INT8의 하위 부분곱 열을 제거하는 연산을 Python과 CMOS netlist로 구현하고, CNN의 양자화·누산값 절단·부분곱 제거를 비교한 프로젝트다. Baugh–Wooley signed 곱셈, 피드백 누산기, ngspice 입력 생성, CIFAR형 ResNet 학습·추론 코드를 포함한다.

연산 사양을 독립적으로 구현하고, 그 구현에서 얻은 정확도와 회로 공급전력을 정리했다. 코드·알고리즘·외부 의존성의 출처는 [NOTICE.md](NOTICE.md)에 있다.

## 연산 사양

두 피연산자는 signed two's-complement이며, INT6은 `k=0..5`, INT8은 `k=0..7`을 지원한다.

```text
T_k(a, w) = a*w - sum(a_i*w_j*2**(i+j), i+j < k)
```

부분곱 제거는 carry가 전파되기 전에 적용한다. 곱이나 전체 내적의 결과 비트를 나중에 지우는 연산과 다르다. 예를 들어 `a=w=3, k=2`에서 정확 곱은 9, 완성된 곱의 비트 절단은 8, 부분곱 제거는 4다.

CNN의 정수 내적은 절대합이 `2**24` 미만인 FP32 부분 내적으로 나눠 정확히 계산하고 INT64로 합한다. BN, residual add, dequantization 등은 FP32다. 전체 integer-only accelerator나 GPU 저전력 커널을 구현한 결과는 아니다.

## 구성

| 경로 | 내용 |
|---|---|
| `circuit/` | signed 산술, CMOS netlist 생성·실행, 선택적 SystemVerilog 참조 |
| `circuit/models/educational_level1.pm` | 공정 보정이 없는 자체 교육용 MOS 모델 |
| `circuit_open_pdk/` | 외부 SKY130 모델을 준비하고 사용하는 어댑터 |
| `cnn/` | ResNet18/50, 양자화 추론, STE 재학습, BN 및 평균 오차 보정 |
| `tests/` | 데이터가 필요 없는 산술·공개 파일 정책·집계 지표·해시 검증 |
| `metrics/` | 기존 독립 실험의 집계 지표 |
| `VALIDATION_RESULTS.json` | 이번 공개 소스 사본의 가벼운 검증 결과 |
| `MANIFEST_SHA256.json` | 배포 파일별 상대 경로·크기·SHA256 |

## 설치와 가벼운 검증

검증 환경은 Python3.12다. 아래 `python`은 선택한 가상환경의 Python을 가리킨다. 기본 산술 검증에는 NumPy만 필요하다.

```sh
python -m pip install -r requirements-core.txt
python -m unittest discover -s tests -v
python tools/manifest.py --verify
python circuit/run_circuit.py --exhaustive-only --output-dir results/arithmetic
```

CNN 검증에는 PyTorch와 torchvision이 필요하다. 아래 smoke 검증은 합성 입력을 사용하며 CIFAR 데이터를 내려받거나 전체 모델을 학습하지 않는다.

```sh
python -m pip install -r requirements.txt
python cnn/run_cifar.py microtests --out results/cnn_microtests
python cnn/thesis_recipe.py --smoke --output results/recipe_smoke.json
```

## 회로 생성과 시뮬레이션

netlist 생성에는 ngspice가 필요하지 않다.

```sh
python circuit/run_circuit.py --generate-only --bits 6 --masks 0 5 --samples 4 --output-dir results/netlists
```

실제 transient simulation에는 별도로 설치한 ngspice가 필요하다. 실행 파일은 `--ngspice`, `NGSPICE_EXECUTABLE`, PATH 순서로 찾는다. ngspice47에서 기존 실험을 수행했으며, 실행 파일과 배포 라이브러리는 이 저장소에 포함하지 않는다.

```sh
python circuit/run_circuit.py --bits 6 --masks 0 5 --samples 24 --skip-exhaustive --output-dir results/circuit
```

기본 MOS 모델은 1V 교육용 Level1이다. 형상에 적힌 45nm가 공정 보정을 뜻하지 않는다. 회로 전력은 곱셈기·누산기·register·내부 clock inverter의 공급전력이며, 이상적 외부 입력·클록·EN·비중첩 클록 발생기의 에너지는 제외한다. 추출 배선 기생과 PVT sweep은 포함하지 않는다.

SKY130 경로는 별도 로컬 모델이 필요하다. 공식 primitive 저장소의 TT nfet_01v8/pfet_01v8을 사용하며, 모델·계수·PDK vendor 파일을 배포하지 않는다. 준비와 실행 명령은 [공개 PDK 어댑터 설명](circuit_open_pdk/README.md)에 있다.

SystemVerilog 파일은 산술 참조다. 이번 공개 소스 검증에서는 합성·배치배선·타이밍·실제 보드 동작을 검증하지 않았다.

## CNN 학습과 평가

기본은 CIFAR형 ResNet18, 30epoch, SGD, crop/flip, label smoothing, cosine 학습률이다. 공식 train50k를 고정된 train45k/validation5k로 나누고, BEST와 scale은 validation에서 정한다. 최종 test는 별도 10k다. `--workers 0`을 기본으로 사용한다.

아래 명령은 선택적으로 새 학습·추론을 수행한다. 데이터·가중치는 포함하지 않으며, train 또는 infer 실행 시 torchvision이 누락된 CIFAR archive를 내려받을 수 있다.

```sh
python cnn/run_cifar.py train --data data --out results/baseline --seed 2026 --epochs 30
python cnn/run_cifar.py infer --data data --out results/inference --checkpoint results/baseline/best.pt --conservative
python cnn/run_cifar.py finetune --data data --out results/qat --checkpoint results/baseline/best.pt --bits 6 --k 4 --epochs 5 --lr 0.01 --batch 64
python cnn/run_cifar.py qat_eval --data data --out results/qat_replay --checkpoint results/qat/best_qat.pt
```

CIFAR100은 train/infer 양쪽에 `--dataset cifar100`, ResNet50은 `--arch resnet50`을 지정한다. checkpoint의 architecture·class 수와 일치해야 한다. `--recipe thesis`는 RandAugment, 반복 증강3회, Mixup/CutMix, SAM을 포함한 별도 독립 레시피다. `--epochs 300`만으로 이 레시피가 선택되지는 않는다. 300epoch 및 ResNet50 전체 학습의 정확도는 기존 측정 범위에 포함되지 않는다. `--resume`은 가중치만 불러오는 warm start이며 optimizer·scheduler·RNG를 복원하지 않는다.

## 기존 독립 측정

다음은 2026-10-04에 실행한 ResNet18 seed2026의 집계값이다. 이번 공개 사본 정리에서는 전체 학습·test 평가·트랜지스터 sweep을 다시 실행하지 않았다. 원시 예측·가중치·파형은 포함하지 않는다.

| 실험 | 정확도 또는 공급전력 |
|---|---|
| CIFAR10 FP32 / INT8 k0 / 부분곱 k1 | 93.45% / 93.46% / 93.49% |
| CIFAR100 FP32 / INT8 k0 / 부분곱 k1 | 74.33% / 74.21% / 74.42% |
| INT6 부분곱 k4, Conv1/FC k0, 5epoch 재학습 | 10.00% → 18.71% |
| SKY130, 동일한 CNN 입력12쌍, INT8 k0 / k1 | 14.703 / 14.347 µW |

INT8 k1의 정확도 차이에 대한 paired95% 구간은 CIFAR10에서 −0.15~+0.22pp, CIFAR100에서 −0.09~+0.51pp다. 성능 개선을 입증한 결과는 아니다. 이후 추가한 k1·오차 보정 실험은 탐색적 후속 평가다. 짧은 재학습의 낮은 정확도도 모든 학습 정책의 실패를 의미하지 않는다.

회로 표의 입력12쌍은 k1 네트워크에서 캡처한 동일한 짧은 부분 내적을 양쪽 회로에 넣은 비교다. 처음9개 activation이0이며, 해당 전력 차이를 전체 CNN 에너지 절감으로 환산하지 않았다. 교육용 Level1, SKY130130nm, 원문의45nm 공정은 서로 다른 조건이다.

38개 전체 test 평가의 집계, 3개 학습 seed 통계, 재학습·보정·회로 조건은 [metrics/README.md](metrics/README.md)와 [archived_metrics.json](metrics/archived_metrics.json)에 있다. 자체 소스의 오픈소스 라이선스는 지정하지 않았으며, 현재 상태는 [LICENSE](LICENSE)에 명시했다.

## English overview

An independent implementation of signed partial-product column removal, CMOS MAC netlist generation, and CIFAR ResNet quantization experiments. Dataset-free arithmetic and recipe smoke checks are included, with ngspice and optional SKY130 models as external dependencies. Archived aggregate measurements describe this implementation under the documented circuit and evaluation conditions. Datasets and checkpoints are managed separately.
