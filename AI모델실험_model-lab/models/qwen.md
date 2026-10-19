# Alibaba Qwen3-0.6B

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `Qwen/Qwen3-0.6B` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | Dense · 28층 · Q 헤드 16개 / KV 헤드 8개 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

같은 모델에서 thinking과 non-thinking 형식을 선택할 수 있습니다. 모델 크기가 0.6B여도 캐시는 KV 헤드 수와 문맥 길이에 좌우됩니다. 공식 설정의 head_dim은 128이므로 hidden_size를 Q 헤드 수로 나눈 값으로 대신하면 계산이 틀립니다.

## 재현 방법과 비교 항목

공식 카드의 enable_thinking 설정을 명시하고 출력 토큰 예산을 함께 고정합니다. 이 저장소의 메모리 실험은 28층·KV 8개·차원 128을 사용했습니다. BF16 캐시는 4,096토큰에서 0.4375 GiB, 32,768토큰에서 3.5 GiB로 계산되었습니다.

## 결과를 해석할 때

카드의 문맥 안내와 config의 max_position_embeddings는 같은 의미로 합치지 않았습니다. 계산한 캐시 크기는 실제 장치 할당량이나 생성 속도가 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/Qwen/Qwen3-0.6B) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/Qwen/Qwen3-0.6B/raw/main/config.json)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Thinking mode and generation budget are independent comparison settings. The offline cache calculation uses the explicit head dimension from the official configuration. This is a source-based release analysis; model inference was not run locally.
