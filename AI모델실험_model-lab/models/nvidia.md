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

공식 지원 언어 목록에 한국어는 없습니다. NVIDIA GPU용 실행 도구의 속도 효과를 모델 자체의 정확도 효과와 구분해야 합니다.

[공식 모델 카드 또는 문서](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2) · [공식 실행 코드 또는 참고 자료](https://arxiv.org/abs/2508.14444)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

A Mamba2–Transformer hybrid needs a different state-memory model from full-attention Transformers. Runtime speed and model accuracy are separate measurements. This is a source-based release analysis; model inference was not run locally.
