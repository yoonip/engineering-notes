# Samsung TRM의 반복 구조와 계산량 | TRM recursion and compute

Samsung SAIL Montréal의 Tiny Recursive Models(TRM)는 작은 네트워크를 재사용해 퍼즐의 답 상태를 갱신하는 연구입니다. 일반 대화형 LLM의 축소판과는 과제·입출력·학습 방식이 다릅니다. 공식 자료 확인일은 2026-10-19입니다. 공식 코드는 MIT 라이선스이며, 저장소는 2026-04-01부터 읽기 전용 상태입니다. [공식 저장소](https://github.com/SamsungSAILMontreal/TinyRecursiveModels)

## 입력과 두 상태의 역할

설명의 `x`는 입력 임베딩, `y`는 답의 표현, `z`는 잠재 상태입니다. 코드에서는 답 쪽 상태를 `z_H`, 잠재 상태를 `z_L`로 보관합니다. `L_level`이라는 같은 네트워크를 두 상태 갱신에 재사용합니다. Attention 버전의 블록은 causal=False이므로 앞 토큰만 보는 일반적인 자기회귀 생성과도 다릅니다.

| 설명의 역할 | 코드에서 확인할 곳 | 읽을 내용 |
|---|---|---|
| 입력 표현 x | `_input_embeddings` | 입력·퍼즐 식별자·위치 표현을 구성합니다. |
| 잠재 상태 z | `z_L` 갱신 | 현재 상태에 `z_H + input_embeddings`를 주입합니다. |
| 답 상태 y | `z_H` 갱신 | 갱신한 잠재 상태를 같은 `L_level`에 넣습니다. |
| 답 출력 | `lm_head(z_H)` | 답 상태에서 위치별 출력 점수를 만듭니다. |
| 다음 단계로 상태 전달 | `new_carry` | `detach()`로 이전 계산의 gradient 연결을 끊습니다. |

[공식 모델 코드](https://github.com/SamsungSAILMontreal/TinyRecursiveModels/blob/main/models/recursive_reasoning/trm.py)에서 위 흐름을 확인했습니다. 앞의 `H_cycles-1` 반복은 `torch.no_grad()` 안에서 진행하며 마지막 반복은 gradient를 계산합니다. 학습용 중단 판정과 달리 평가에서는 batch 처리를 위해 최대 단계까지 진행하도록 구현되어 있습니다.

## 작은 파라미터 수와 짧은 실행 시간은 다른 문제입니다

[기본 설정](https://github.com/SamsungSAILMontreal/TinyRecursiveModels/blob/main/config/arch/trm.yaml)의 `H_cycles=3`, `L_cycles=6`, `L_layers=2`, `halt_max_steps=16`을 세면 다음과 같습니다. 과제별 실행 명령에서는 이 설정을 덮어쓸 수 있습니다.

| 계산 단위 | 기본 설정으로 센 값 |
|---|---:|
| inner forward 한 번의 잠재 상태 갱신 | 3×6 = 18회 |
| inner forward 한 번의 답 상태 갱신 | 3회 |
| 같은 `L_level` 호출 수 | 3×(6+1) = 21회 |
| `L_level`의 블록 실행 수 | 21×2 = 42회 |
| 16단계 평가의 블록 실행 수 | 16×42 = 672회 |

가중치를 공유하므로 블록을 672개 저장하는 것은 아닙니다. 그러나 연산을 672번 수행하는 비용은 남습니다. 임베딩·출력·중단 head 등의 연산은 이 표에서 제외했으므로 전체 FLOP 수나 시간 측정값으로 해석하면 안 됩니다. 과제의 입력 길이와 batch도 계산량을 바꿉니다.

## 실제로 실행한 작은 반복식

[CPU 실험 2](../experiments/README.md#2-같은-계수를-반복해도-수렴이-보장되지는-않습니다)에서 x·y·z를 구분한 스칼라 갱신을 실행했습니다. 같은 계수 네 자리를 재사용하며 8단계, 총 32회 갱신했습니다.

| 잠재 상태의 이전 값 계수 | 1단계 답 상태 | 8단계 답 상태 | 해석 |
|---|---:|---:|---|
| 0.5 | 0.109375 | 0.323802 | 이 식의 고정점 1/3에 가까워집니다. |
| 1.2 | 0.227500 | 80.177049 | 반복할수록 값이 커지는 반례입니다. |

이 결과는 파라미터 저장과 반복 계산을 구분하는 교육용 실험입니다. TRM 신경망을 학습하거나 Sudoku·ARC 정답률을 재현한 결과가 아닙니다. 반복한다는 사실만으로 정확도가 올라간다는 결론을 내릴 수 없다는 점을 확인했습니다.

## 공식 과제를 재현하려면

공식 저장소에서 과제별 데이터 생성과 학습 명령을 선택하고 코드 revision·데이터 분할·증강·seed·전체 batch·반복 설정을 남겨야 합니다. ARC 계열의 학습·평가 데이터 중복 가능성을 먼저 확인하고, 문제 전체가 맞는 exact accuracy와 칸 단위 정확도를 구분합니다. 공식 학습은 GPU 조건을 전제로 안내되어 있어 이 저장소에서는 실행하지 않았습니다.

[다른 기관의 모델 분석](../models/README.md) · [실험 코드와 결과](../experiments/README.md)

## English

TRM reuses one small network to update latent and answer states. The default configuration gives 21 reasoning-module calls, or 42 two-block evaluations, per inner forward; 16 evaluation steps give 672 block executions, excluding other operations. These are code-derived counts, not measured FLOPs or latency. The scalar state experiment demonstrates parameter sharing and a stability counterexample, not official TRM training or benchmark reproduction.
