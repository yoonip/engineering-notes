# 상태 공간과 어텐션의 혼합: Nemotron Nano 9B v2 | Hybrid state and attention

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `nvidia/NVIDIA-Nemotron-Nano-9B-v2` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | Mamba2·MLP 중심의 혼합 구조 · attention 4개 층 |
| 사용 조건의 표기 | NVIDIA Open Model License |

## 구조와 용도

Mamba-2는 입력을 읽으며 제한된 내부 상태를 갱신하는 상태 공간 계열이고, attention은 문맥의 표현을 직접 참조하는 계산입니다. 이 모델은 Mamba-2·MLP 중심에 attention 4개 층을 결합합니다. MLP는 각 위치의 표현을 변환하는 신경망이며, ‘attention이 적다’는 말은 모든 나머지 계산이 사라졌다는 뜻이 아닙니다.

[공식 Model Overview](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2#model-overview)는 NVIDIA의 처음부터 학습한 모델이며 Megatron-LM·NeMo-RL을 사용했다고 밝힙니다. 이 저장소의 스칼라 반복식은 Mamba 상태 갱신이나 해당 학습의 재현이 아닙니다. CUDA 실행 도구와 모델 구조, 후속 사고 예산 제어를 각각 구분합니다.

모든 층이 Transformer attention인 모델과 다릅니다. Mamba의 상태와 attention의 KV 캐시가 함께 있으므로 전체 층 수를 단순한 Transformer 캐시 식에 넣으면 메모리를 잘못 계산합니다. Thinking 예산은 출력 길이와 계산량에도 영향을 줍니다.

## 실행에 필요한 조건과 비교 항목

공식 카드가 안내한 runtime에서 해당 hybrid 구조의 지원을 확인합니다. 같은 문제를 추론 모드와 비추론 모드로 나누고 정답률·출력 길이·처리 시간을 함께 기록합니다. 일반 Transformer용 양자화 파일을 그대로 적용할 수 있는지도 확인합니다.

## 공개 범위와 한계

공식 카드의 언어 목록은 절마다 달라 한국어 지원 범위를 하나의 목록으로 단정하지 않습니다. NVIDIA GPU용 실행 도구의 속도 효과를 모델 자체의 정확도 효과와 구분해야 합니다.

## 혼합 상태와 사고 예산을 구분하기

Mamba 계열의 상태는 앞선 입력을 갱신하며 전달하는 내부 기억이고, attention의 KV 캐시는 앞 문맥의 키·값 표현을 저장합니다. 이 배포물은 두 종류를 함께 쓰므로 전체 상태 메모리를 ‘전체 층 수×KV 크기’ 하나로 계산하지 않습니다. 짧은 처리 시간을 목표로 한 runtime 설정과 모델의 정답도 별도로 비교합니다. [공식 구조 설명](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2#model-architecture)

사고 토큰 제한도 최종 답 공간과 구분해야 합니다. 공식 budget 제어 설명의 `max_thinking_tokens`는 다음 줄바꿈에서 사고를 끝내려는 문턱이며, 즉시 그 수에서 무조건 자르는 상한으로 설명하지 않습니다. 자체 예산을 전체 1,024·사고 구간 256으로 정하더라도 실제 종료·추가 표식 등을 확인하지 않고 항상 답 768토큰이 남는다고 보장할 수는 없습니다. [Budget 제어 조건](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2#using-budget-control-with-a-vllm-server)

## 공식 카드의 언어 범위

언어 범위에도 원문 대조가 필요합니다. 공식 카드의 개요와 Use Case는 영어·독일어·스페인어·프랑스어·이탈리아어·일본어를 적지만, Input 절에는 한국어·포르투갈어·러시아어·중국어도 포함됩니다. 두 목록의 차이를 해소하는 근거 없이 하나를 유일한 지원 범위로 단정하지 않습니다. [Use Case·Input](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2#input) 이번 분석에서는 한국어 품질을 측정하지 않았습니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#nvidia)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2) · [공식 실행 코드 또는 참고 자료](https://arxiv.org/abs/2508.14444)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

A Mamba2–Transformer hybrid needs a different state-memory model from full-attention Transformers. Runtime speed and model accuracy are separate measurements. This is a source-based release analysis; model inference was not run locally.
