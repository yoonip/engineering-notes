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

## 작은 모델에서도 차원 하나가 계산을 바꿉니다

이 배포물의 `hidden_size`는 1,024이고 Q 헤드는 16개입니다. 이를 나누면 64이지만 공식 `head_dim`은 128입니다. Q·K·V로 투영하는 크기가 단순한 hidden_size 분할이라는 가정을 넣으면 캐시를 절반으로 잘못 계산합니다. 모델 이름의 0.6B는 이 세부 차원을 대신하지 않습니다. [공식 config](https://huggingface.co/Qwen/Qwen3-0.6B/raw/main/config.json)

배치 1·28층·KV 헤드 8개·차원 128·원소 2바이트로 둔 K·V 본문은 토큰당 2×28×8×128×2=114,688바이트, 즉 112 KiB입니다. 4,096토큰은 469,762,048바이트이며 0.4375 GiB입니다. 앞의 2는 K와 V 두 묶음입니다. 가중치·중간값·실행기의 여유 할당은 뺀 계산이어서 이 수만큼의 장치 메모리로 실행된다는 뜻은 아닙니다.

## 직접 만든 소수 비교 예

자체 입력은 “소수로서 0.8과 0.75 중 큰 수를 적고 한국어 한 문장으로 설명해 주세요. 버전 번호가 아닙니다.”입니다. 기준은 0.8=0.80>0.75입니다. 실제 모델을 실행한 결과가 아닙니다.

| 항목 | 판정 기준 |
| --- | --- |
| 숫자 | 0.8을 골라야 합니다. |
| 근거 | 자릿수를 맞춘 0.80과 0.75의 크기를 비교할 수 있습니다. |
| 완료 | 사고 구간만 반복되고 답이 끝나지 않으면 미완료입니다. |
| 설정 | `enable_thinking`과 출력 예산을 함께 남깁니다. |

공식 카드의 thinking 모드는 template 단계의 선택이며 `<think>` 구간 뒤 최종 응답이 이어집니다. ‘설명을 길게 쓰세요’라는 자연어 지시와 같은 설정으로 취급하지 않습니다. 또한 이 모드에서 greedy decoding은 반복·성능 저하를 일으킬 수 있다는 공식 주의가 있으므로 다른 모델의 기본 생성 설정을 그대로 비교 조건으로 옮기지 않습니다. [모드 전환·생성 조건](https://huggingface.co/Qwen/Qwen3-0.6B#switching-between-thinking-and-non-thinking-mode)

두 모드를 비교하면 최종 숫자·설명 정확성·완료 여부를 따로 볼 수 있습니다. 사고 토큰이 많다는 사실은 정답을 대신하지 않으며, 단순 비교 한 사례를 맞혔다고 장문 추론이나 한국어 전체 능력을 확인한 것으로 쓰지 않습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/Qwen/Qwen3-0.6B) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/Qwen/Qwen3-0.6B/raw/main/config.json)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Thinking mode and generation budget are independent comparison settings. The offline cache calculation uses the explicit head dimension from the official configuration. This is a source-based release analysis; model inference was not run locally.
