# NVIDIA Nemotron Nano 9B v2

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `nvidia/NVIDIA-Nemotron-Nano-9B-v2` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | Mamba2·MLP 중심의 혼합 구조 · attention 4개 층 |
| 사용 조건의 표기 | NVIDIA Open Model License |

## 구조와 용도

모든 층이 Transformer attention인 모델과 다릅니다. Mamba의 상태와 attention의 KV 캐시가 함께 있으므로 전체 층 수를 단순한 Transformer 캐시 식에 넣으면 메모리를 잘못 계산합니다. Thinking 예산은 출력 길이와 계산량에도 영향을 줍니다.

## 재현 방법과 비교 항목

공식 카드가 안내한 runtime에서 해당 hybrid 구조의 지원을 확인합니다. 같은 문제를 추론 모드와 비추론 모드로 나누고 정답률·출력 길이·처리 시간을 함께 기록합니다. 일반 Transformer용 양자화 파일을 그대로 적용할 수 있는지도 확인합니다.

## 결과를 해석할 때

공식 카드의 언어 목록은 절마다 달라 한국어 지원 범위를 하나의 목록으로 단정하지 않습니다. NVIDIA GPU용 실행 도구의 속도 효과를 모델 자체의 정확도 효과와 구분해야 합니다.

## 혼합 상태와 사고 예산을 구분하기

Mamba 계열의 상태는 앞선 입력을 갱신하며 전달하는 내부 기억이고, attention의 KV 캐시는 앞 문맥의 키·값 표현을 저장합니다. 이 배포물은 두 종류를 함께 쓰므로 전체 상태 메모리를 ‘전체 층 수×KV 크기’ 하나로 계산하지 않습니다. 짧은 처리 시간을 목표로 한 runtime 설정과 모델의 정답도 별도로 비교합니다. [공식 구조 설명](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2#model-architecture)

사고 토큰 제한도 최종 답 공간과 구분해야 합니다. 공식 budget 제어 설명의 `max_thinking_tokens`는 다음 줄바꿈에서 사고를 끝내려는 문턱이며, 즉시 그 수에서 무조건 자르는 상한으로 설명하지 않습니다. 자체 예산을 전체 1,024·사고 구간 256으로 정하더라도 실제 종료·추가 표식 등을 확인하지 않고 항상 답 768토큰이 남는다고 보장할 수는 없습니다. [Budget 제어 조건](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2#using-budget-control-with-a-vllm-server)

## 직접 만든 추론 완료 판정

자체 입력은 “세 상자에는 합계 18개의 나사가 있습니다. 두 번째에는 첫 번째보다 2개 더 있고, 세 번째에는 첫 번째보다 4개 더 있습니다. 각 상자의 수량을 순서대로 적어 주세요.”입니다. 첫 수량을 x로 두면 x+(x+2)+(x+4)=18이고 기준 답은 4·6·8입니다. 이는 손으로 구성한 정답이며 실제 응답이 아닙니다.

| 확인할 부분 | 정답 기준 |
| --- | --- |
| 합계 | 세 수를 더하면 18이어야 합니다. |
| 관계 | 두 번째·세 번째는 첫 번째보다 각각 2·4 커야 합니다. |
| 완료 | 사고 문장만 남고 최종 수량이 없으면 미완료입니다. |
| 모드 비교 | 사고 예산·새 생성 길이·정답을 함께 기록합니다. |

6·6·6은 합계만 맞으므로 관계 오답입니다. 4·8·6은 원소가 같아도 상자 순서가 틀립니다. 더 긴 설명이 나왔다는 사실만으로 정답을 인정하지 않습니다.

언어 범위에도 원문 대조가 필요합니다. 공식 카드의 개요와 Use Case는 영어·독일어·스페인어·프랑스어·이탈리아어·일본어를 적지만, Input 절에는 한국어·포르투갈어·러시아어·중국어도 포함됩니다. 두 목록의 차이를 해소하는 근거 없이 하나를 유일한 지원 범위로 단정하지 않습니다. [Use Case·Input](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2#input) 이번 분석에서는 한국어 품질을 측정하지 않았습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2) · [공식 실행 코드 또는 참고 자료](https://arxiv.org/abs/2508.14444)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

A Mamba2–Transformer hybrid needs a different state-memory model from full-attention Transformers. Runtime speed and model accuracy are separate measurements. This is a source-based release analysis; model inference was not run locally.
