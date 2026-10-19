# 모델 메모리·반복 계산·증류·양자화 실험 | Small numerical experiments

Python 표준 라이브러리만으로 네 가지 계산을 실행했습니다. 공식 모델의 가중치를 내려받거나 API를 호출하지 않았습니다. 따라서 아래 값은 모델의 정답률이나 실제 GPU 메모리 측정값이 아닙니다. 메모리 계산은 공개 설정에서 가져온 차원을 사용하며, 나머지 세 실험은 원리를 확인하는 작은 수치 예제입니다.

실행 환경은 CPython 3.12.14 / Windows이며, 실행일은 2026-10-19입니다. [실험 코드](cpu_lab.py), [수치 검사](test_cpu_lab.py), [계산 결과 JSON](results.json)을 함께 보실 수 있습니다. JSON은 다시 계산한 값과 비교하기 위한 기록이며, 본문 표에는 읽는 데 필요한 결과를 옮겼습니다.

## 다시 실행하기

저장소 루트에서 다음 명령을 실행하시면 됩니다. 외부 패키지와 네트워크 연결은 필요하지 않습니다.

```powershell
python AI모델실험_model-lab/experiments/cpu_lab.py
python -m unittest discover -s AI모델실험_model-lab/experiments -p "test_*.py" -v
```

## 1. 작은 모델의 KV 캐시가 더 클 수도 있습니다

Full attention에서 batch 하나의 K·V 저장량을 다음 식으로 계산했습니다. `L`은 층 수, `Hkv`는 K·V 헤드 수, `D`는 헤드 차원, `T`는 저장된 토큰 수, `s`는 값 하나의 byte 수입니다.

```text
KV byte = 2 × L × Hkv × D × T × batch × s
```

| 설정 | 층 / KV 헤드 / 헤드 차원 | 4,096 tokens | 16,384 tokens | 32,768 tokens |
|---|---|---:|---:|---:|
| DeepSeek-R1-Distill-Qwen-1.5B | 28 / 2 / 128 | 0.109375 GiB | 0.437500 GiB | 0.875000 GiB |
| Qwen3-0.6B | 28 / 8 / 128 | 0.437500 GiB | 1.750000 GiB | 3.500000 GiB |

두 모델은 이 계산에서 층 수와 헤드 차원이 같습니다. Qwen3-0.6B는 KV 헤드가 네 배이므로 같은 길이에서 캐시도 네 배입니다. 파라미터 수가 작다는 사실만으로 긴 문맥의 메모리를 판단할 수 없습니다.

파라미터 수를 이름의 근삿값으로 잡으면 BF16 가중치 저장량은 각각 약 2.794 GiB와 1.118 GiB입니다. 이는 실제 체크포인트 크기를 읽은 값이 아닙니다. INT4의 이상적인 payload는 각각 약 0.698 GiB와 0.279 GiB이며, scale·zero point·packing·일부 비양자화 층의 저장 공간을 제외합니다. 실행 시에는 activation·작업 공간·할당 여유도 추가됩니다.

계산에 사용한 차원은 [DeepSeek 설정](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B/raw/main/config.json)과 [Qwen 설정](https://huggingface.co/Qwen/Qwen3-0.6B/raw/main/config.json)에서 확인했습니다. Qwen의 `head_dim=128`은 `hidden_size / Q 헤드 수`로 추정하면 안 되는 명시적 설정입니다. 모델 카드의 권장 문맥 길이와 설정 파일의 위치 한도도 같은 뜻으로 취급하지 않았습니다.

## 2. 같은 계수를 반복해도 수렴이 보장되지는 않습니다

TRM의 입력 `x`, 답 상태 `y`, 잠재 상태 `z` 구분을 참고하여 다음 스칼라 갱신을 구성했습니다. TRM의 신경망·학습·중단 판정은 구현하지 않았습니다.

```text
x = 1, y = 0, z = 0
각 바깥 단계에서:
    z = a*z + 0.25*(x+y) 를 세 번 계산합니다.
    y = 0.5*y + 0.25*z 를 한 번 계산합니다.
```

| z의 이전 상태 계수 a | 1단계 y | 4단계 y | 8단계 y | 8단계까지 갱신 수 |
|---|---:|---:|---:|---:|
| 0.5 | 0.109375000 | 0.275126040 | 0.323801883 | 32 |
| 1.2 | 0.227500000 | 4.364192788 | 80.177049230 | 32 |

계수 네 자리는 단계마다 재사용합니다. 반복 횟수가 늘어도 저장하는 계수 수는 같습니다. 첫 번째 식의 고정점은 `y=1/3, z=2/3`이며 계산값이 가까워집니다. 두 번째 식은 값이 커집니다. 이 예제는 계산 깊이와 파라미터 저장량을 구분하고, 반복 자체가 정확도 향상을 보장하지 않는다는 점을 보여 줍니다. TRM이 발산한다는 실험 결과로 해석하시면 안 됩니다.

## 3. 확률을 배우는 학생과 정답 번호만 배우는 학생

입력 `x` 하나에 대한 교사의 세 logit을 `[-2x, 1, 2x]`로 정했습니다. Softmax는 logit을 합이 1인 확률로 바꿉니다. 학생은 클래스마다 기울기와 절편을 하나씩 갖는 선형 모델입니다. 학습 입력 7개, 학습에 쓰지 않은 입력 40개, 학습률 0.2, 경사하강법 1,200회로 조건을 맞췄습니다.

| 학습 목표 | 교사→학생 평균 KL 발산 | 평가 입력의 최상위 클래스 일치율 |
|---|---:|---:|
| 교사의 최상위 클래스 번호 | 0.379719331 | 90% |
| 교사의 전체 확률 분포 | 약 0.000000001 | 100% |

KL 발산은 두 분포의 차이를 나타내며 작을수록 가깝습니다. 이 예제에서는 학생이 교사의 식을 표현할 수 있으므로 분포를 직접 알려 주는 조건이 유리합니다. 교사가 더 크거나 학생이 더 작도록 구성하지 않았으므로 압축률을 비교하는 실험은 아닙니다. DeepSeek-R1-Distill의 실제 학습도 이 작은 확률 회귀와 같지 않습니다. R1이 만든 풀이 데이터를 다른 기반 모델에 학습시킨다는 원리와, 전통적인 확률 증류의 차이를 확인하는 용도입니다.

## 4. 적은 bit가 내적 오차에 미치는 영향

`sin(0.37*i)`로 만든 가중치 64개를 최솟값·최댓값 사이에 균등 양자화했습니다. 복원한 값과 `cos(0.19*i)` 입력의 내적을 원래 내적 `2.955841745`와 비교했습니다.

| bit 수 | 이상적인 가중치 payload | 최대 가중치 오차 | 내적의 절댓값 오차 |
|---|---:|---:|---:|
| 4 | 32 bytes | 0.066000616 | 0.263219193 |
| 8 | 64 bytes | 0.003722161 | 0.006814564 |

이 코드에서는 양자화 값을 다시 Python 실수로 복원합니다. 실제 메모리를 32 bytes로 줄이는 커널이 아닙니다. GPTQ·AWQ·MXFP4를 구현한 것도 아닙니다. 한 입력에서 내적 오차가 작다는 결과를 전체 언어 생성 품질의 보장으로 확대할 수 없습니다.

## 검사 범위

6개 검사는 KV 차원·batch·길이에 따른 비례 관계, 반복식의 수렴 사례와 반례, softmax의 큰 logit 처리, 학생의 분포 학습, 양자화 경계·오차 한계를 확인합니다. 공식 모델 추론과 공식 벤치마크 재현은 이 기록에 포함하지 않습니다.

## English

These four offline experiments use only the Python standard library. They calculate KV-cache storage from two official configurations, compare stable and unstable shared-state updates, fit a small student to teacher probabilities or hard labels, and measure uniform quantization error. No released weights, paid APIs, GPU runs, or official benchmarks were used. The tables distinguish calculated storage and educational numerical results from actual model performance.
