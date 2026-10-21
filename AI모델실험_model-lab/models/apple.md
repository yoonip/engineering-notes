# 계산 그래프의 평가 시점: Apple MLX | Lazy array evaluation

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `MLX` |
| 제공·입출력 | 배열 연산·학습·추론 도구 · 모델 배포물이 아닙니다. |
| 구조·설정 | NumPy와 비슷한 API · 지연 계산 · 공유 메모리 |
| 사용 조건의 표기 | 개별 코드·모델의 조건을 각각 확인합니다. |

## 구조와 용도

MLX 자체에는 사전학습된 ‘정답 가중치’가 없습니다. 사용자가 배열과 신경망을 정의하고, 자동미분으로 손실의 기울기를 계산하고, optimizer로 매개변수를 갱신할 때 학습 도구로 쓰입니다. 이미 학습한 매개변수로 출력을 계산할 때는 추론 도구로 쓰입니다. 같은 framework를 썼다는 이유만으로 두 모델의 구조나 학습 자료가 같아지는 것은 아닙니다.

[공식 Lazy Evaluation](https://ml-explore.github.io/mlx/build/html/usage/lazy_evaluation.html)은 계산 그래프 구성과 `mx.eval`의 실제 평가를 구분합니다. 별도 평가 문서의 산술 기대값은 MLX 실행 결과가 아닙니다. Apple이 공개한 다른 모델이나 서비스 모델의 구조를 이 framework 설명으로 대신하지 않습니다.

MLX는 모델 이름이 아니라 연산 framework입니다. 배열 식을 만들었다고 계산이 끝난 것은 아닙니다. 지연 실행에서 평가를 강제하지 않고 시간을 재면 실제 연산 대신 계산 그래프를 만드는 시간만 측정할 수 있습니다.

## 실행에 필요한 조건과 비교 항목

지원 장치에서 공식 Quick Start를 실행하고 mx.eval로 결과를 실체화한 뒤 시간을 측정합니다. 워밍업·동기화·자료형을 고정합니다. 모델을 비교할 때는 원래 가중치와 MLX 변환본의 출처·변환 설정을 함께 남깁니다.

## 공개 범위와 한계

공유 메모리는 메모리 사용량이 무제한이라는 뜻이 아닙니다. 이 저장소의 Windows CPU 실험을 Apple 장치의 MLX 실험으로 표기하지 않았습니다.

## 배열의 값과 계산 계획을 나누어 보기

MLX의 배열에는 `shape`와 `dtype`이 있습니다. shape은 행·열 같은 축별 크기이고 dtype은 각 원소를 어떤 숫자 형식으로 저장할지 정합니다. `mx.eval`은 `model.eval()`처럼 신경망의 학습·평가 모드를 전환하는 이름과 구별해야 합니다. 여기서는 지연된 배열 계산의 평가를 뜻합니다. `print`, NumPy 변환, 스칼라의 `item()`도 평가를 일으킬 수 있어 출력문을 시간 구간에 넣느냐에 따라 측정 범위가 바뀝니다. [지연 실행의 평가 시점](https://ml-explore.github.io/mlx/build/html/usage/lazy_evaluation.html#when-to-evaluate)

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#apple)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

## 공유 메모리에서도 남는 크기 계산

직접 정한 백만 원소 배열의 본문은 float32라면 1,000,000×4=4,000,000바이트이고 float16이라면 2,000,000바이트입니다. 이는 형식별 원소 크기의 계산이며 MLX의 실측 최대 메모리가 아닙니다. 중간 배열·모델 가중치·런타임 부담은 포함하지 않았습니다. CPU와 GPU가 메모리를 공유한다고 해서 이런 저장량이 사라지지는 않습니다. MLX 변환 모델을 시험할 때 원래 모델의 정답과 변환본의 수치 오차를 먼저 비교해야 실행 시간의 차이도 의미 있게 읽을 수 있습니다.

[공식 framework 문서](https://ml-explore.github.io/mlx/build/html/index.html) · [공식 실행 코드 또는 참고 자료](https://ml-explore.github.io/mlx/build/html/usage/lazy_evaluation.html)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

MLX is a runtime, not a language model. Timing lazy expressions without materializing results does not measure complete execution. This note describes an array framework; MLX was not run on this Windows CPU experiment.
