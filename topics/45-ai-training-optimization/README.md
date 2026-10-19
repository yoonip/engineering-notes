# AI Training & Optimization

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

학습은 모델·데이터·손실·optimizer·실행 환경이 함께 만드는 과정이다. 같은 구조라도 전처리, 학습률, batch size, 초기화, 정밀도 설정이 결과를 바꾼다.

## 학습을 구성하는 상태

SGD·Adam 계열은 gradient를 이용해 parameter를 갱신한다. Learning rate schedule은 갱신 크기를 시간에 따라 조절한다. Checkpoint에는 가중치뿐 아니라 optimizer·scheduler·random state 같은 상태가 포함될 수 있다. 학습 재개와 추론용 배포에 필요한 상태는 다르다.

## 자원 사용을 줄이는 방법

Mixed precision은 연산과 저장에 서로 다른 정밀도를 사용한다. DDP는 모델 복제와 gradient 동기화, FSDP는 상태 분할, DeepSpeed는 여러 분산 학습 최적화를 제공한다. Gradient accumulation은 여러 step의 gradient를 모아 갱신하지만 normalization·stochastic 동작까지 큰 batch와 항상 동일한 것은 아니다.

LoRA는 저랭크 adapter, QLoRA는 양자화된 기반 모델을 활용한 adapter 학습, distillation은 다른 모델의 출력을 이용한 지식 전달, pruning은 일부 연결·구조 제거다. PEFT·TRL·Accelerate·bitsandbytes는 관련 학습·경량화 도구다. MLflow·Weights & Biases·TensorBoard는 실험 기록, Optuna는 parameter 탐색에 쓰인다.

## 관련 기술

PEFT, TRL, Accelerate, DeepSpeed, FSDP, DDP, MLflow, W&B, TensorBoard, Optuna, bitsandbytes

## 참고 자료

- [PEFT documentation](https://huggingface.co/docs/peft/)
