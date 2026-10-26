# 부분곱 열 제거 실험 읽기 | Reading a Partial-Product Experiment

[논문·코드·특허](../README.md) · [구현과 실험 기록](../../../프로젝트_projects/cnn-partial-product-reproduction/README.md) · [English](#english)

## 무엇을 재현했는지 먼저 정합니다

[ResNet 논문](https://arxiv.org/abs/1512.03385)은 입력을 참조하는 잔차 함수를 학습하는 구조를 제시합니다. 같은 ResNet 계열을 썼더라도 데이터, 학습 일정, 수치 정밀도와 회로 조건까지 같아야 같은 실험이라고 비교할 수 있습니다. 이 저장소의 부분곱 프로젝트는 곱셈의 일부를 생략했을 때의 산술, CNN 정확도와 회로 공급전력을 각각 다룹니다. ResNet 원문의 ImageNet 결과를 재현하는 프로젝트로 해석하지 않습니다.

이 글에서는 먼저 산술 사양을 확인하고, 어떤 관측이 어떤 주장을 지지하는지 살펴봅니다. 실험의 출처와 구현 범위는 프로젝트의 [NOTICE](../../../프로젝트_projects/cnn-partial-product-reproduction/NOTICE.md)에 있습니다.

## 같은 비트를 지워도 계산 위치가 다릅니다

`a=b=3`이면 이진수로 `11×11`입니다. 정확한 곱은 `1+2+2+4=9`입니다. 완성된 곱의 하위 두 비트를 지우면 `1001₂→1000₂`이므로 8입니다. 반면 자릿값이 4보다 작은 부분곱을 carry가 전파되기 전에 제거하면 `1+2+2`가 사라지고 4만 남습니다.

| 연산 | 처리하는 시점 | `3×3`의 결과 |
| --- | --- | --- |
| 정확한 곱 | 모든 부분곱을 합칩니다 | 9 |
| 완성된 곱의 비트 절단 | 곱을 구한 뒤 하위 비트를 지웁니다 | 8 |
| 부분곱 열 제거 | 합산하기 전에 하위 열을 지웁니다 | 4 |

양의 입력 예시만으로 signed 연산을 확인할 수는 없습니다. 구현의 입력은 n비트 2의 보수 정수이며, k는 `0≤k≤n−1`입니다. 제거하는 부분곱은 부호 비트에 닿지 않는 하위 열입니다. 이 범위에서 연산 사양은 다음과 같습니다.

```math
T_k(a,b)=ab-\sum_{i+j<k} a_i b_j2^{i+j}.
```

여기서 `a_i`, `b_j`는 해당 입력의 하위 비트입니다. 예를 들어 INT6에서 `a=b=−1`의 하위 비트는 모두 1입니다. k=2이면 정확 곱 1에서 `1+2+2=5`를 빼므로 결과는 −4입니다. 완성된 곱 1의 하위 두 비트를 지운 0과도 다릅니다. 이 차이를 놓치면 논문의 비트 연산을 다른 알고리즘으로 구현하고도 같은 이름을 붙일 수 있습니다.

## 식과 독립적인 비트 행렬을 대조합니다

[arithmetic.py](../../../프로젝트_projects/cnn-partial-product-reproduction/circuit/arithmetic.py)의 `column_mask_mul`은 위 식을 배열 연산으로 계산합니다. `baugh_wooley_mul`은 부호가 포함된 비트 행렬을 별도로 구성해 결과를 구합니다. 한 함수의 결과를 다른 함수가 그대로 호출하는 방식으로 비교하지 않습니다.

2026-10-19에 INT6의 모든 입력 쌍 4,096개를 k=2로 대조했으며 두 구현의 결과가 모두 같았습니다. 아래 값도 같은 실행에서 확인했습니다.

| a | b | 정확한 곱 | 완성된 곱의 하위 두 비트 제거 | 부분곱 열 제거 |
| --- | --- | --- | --- | --- |
| 3 | 3 | 9 | 8 | 4 |
| −3 | 3 | −9 | −12 | −12 |
| −32 | −32 | 1024 | 1024 | 1024 |
| −1 | −1 | 1 | 0 | −4 |

이 비교는 해당 입력 영역에서 두 산술 구현의 일치를 확인합니다. 회로 타이밍, 칩 전력 또는 CNN 정확도를 측정한 결과는 아닙니다. 더 큰 입력 폭이나 다른 k도 별도의 검사가 필요합니다. 프로젝트 루트에서 다음 명령으로 기존 산술 시험을 실행하실 수 있습니다.

```sh
python -m unittest discover -s tests -v
python circuit/run_circuit.py --exhaustive-only --output-dir results/arithmetic
```

## 정확도와 전력의 주장을 분리합니다

프로젝트의 기존 CIFAR10 기록은 FP32 93.45%, INT8 k1 93.49%입니다. 차이는 0.04퍼센트포인트입니다. 그러나 해당 차이의 쌍체 95% 구간은 −0.15~+0.22퍼센트포인트로 기록되어 있습니다. 점추정치가 높다는 이유만으로 정확도가 향상되었다고 결론내리지 않습니다. 이 값은 [기존 집계 기록](../../../프로젝트_projects/cnn-partial-product-reproduction/metrics/README.md)을 해석한 것이며 새 학습을 실행한 값이 아닙니다.

회로 비교는 같은 짧은 부분 내적 입력 12쌍을 사용했습니다. 이 입력에서 얻은 공급전력 차이를 CNN 전체 에너지로 환산하려면 연산 횟수, 입력 분포, 메모리 접근과 주변 회로까지 연결해야 합니다. 해당 기록은 그런 전체 시스템 환산을 수행한 결과가 아닙니다. 교육용 Level1과 SKY130 모델, 다른 공정의 결과도 같은 조건처럼 합치지 않습니다.

| 확인한 근거 | 말할 수 있는 범위 | 추가로 필요한 근거 |
| --- | --- | --- |
| 산술의 전수 비교 | 지정한 n·k·입력 범위의 수치 일치 | 다른 폭·모드와 실제 RTL·회로 검증 |
| 고정 평가 조건의 정확도 | 그 데이터와 모델 조건의 분류 결과 | 반복·쌍체 비교와 조건 변경 분석 |
| 같은 입력의 회로 공급전력 | 해당 파형·전압·모델 범위의 공급전력 | 배선·주변 회로·메모리·실제 작업량 |

재현 기록의 핵심은 수치 하나를 다시 얻는 일만이 아닙니다. 입력과 연산 사양, 비교 조건, 원시 관측과 결론을 연결해 다른 사람이 같은 범위에서 판단할 수 있게 하는 일입니다.

## English

The [ResNet paper](https://arxiv.org/abs/1512.03385) introduces learning residual functions with reference to the layer input. Reusing that architecture does not establish reproduction of its dataset, training procedure, precision or hardware results. This case examines the repository's independent partial-product implementation and its documented evidence.

### Arithmetic comes before a headline metric

For `3×3`, exact multiplication produces `1+2+2+4=9`. Clearing the bottom two bits of the completed product gives 8. Dropping the columns with place value below 4 before carry propagation removes `1+2+2` and gives 4. These operations cannot be interchanged.

The implementation accepts signed n-bit two's-complement operands and `0≤k≤n−1`. In that domain the removed terms do not reach the sign columns, yielding the equation above. For INT6 `−1×−1` with k=2, all relevant lower bits are one: subtracting `1+2+2` from the exact product 1 gives −4. Clearing the final product's bottom two bits instead gives 0.

`column_mask_mul` evaluates the specification through array operations. `baugh_wooley_mul` constructs a separate signed bit matrix. On 2026-10-19, all 4,096 INT6 operand pairs at k=2 matched between the two implementations. The four displayed examples came from that run. This check concerns arithmetic agreement in the stated domain, not timing, chip power or CNN accuracy. Existing test commands above run from the project directory.

### Match each claim to its evidence

The archived CIFAR10 values are 93.45% for FP32 and 93.49% for INT8 k1, a 0.04-percentage-point difference. The recorded paired 95% interval is −0.15 to +0.22 percentage points. A higher point estimate alone does not establish an accuracy gain. These are interpretations of the [archived measurements](../../../프로젝트_projects/cnn-partial-product-reproduction/metrics/README.md), not results of new training.

Circuit supply-power comparisons use the same twelve short partial dot-product inputs. Inferring whole-CNN energy would additionally require workload counts, input distributions, memory traffic and peripheral circuitry. Educational Level1, SKY130 and other process conditions must retain their own identities.

Arithmetic agreement, fixed-protocol classification results and circuit supply power therefore support different statements. A useful reproduction record preserves the connection between the input specification, comparison conditions, observations and conclusion, so another reader can assess the same scope.
