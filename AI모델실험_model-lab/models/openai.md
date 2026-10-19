# OpenAI gpt-oss-20b

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `openai/gpt-oss-20b` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | MoE · 전체 약 21B / 활성 약 3.6B |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

토큰마다 활성화되는 파라미터가 적어도 모든 전문가의 가중치를 저장해야 합니다. 활성 3.6B를 모델 전체 저장량으로 계산하면 메모리를 크게 잘못 추정하게 됩니다. 공식 실행 안내는 MXFP4를 이용한 20b 모델에 약 16GB VRAM을 제시하며, BF16 경로는 더 많은 메모리를 사용합니다.

## 재현 방법과 비교 항목

공식 Transformers 실행 안내에서 하드웨어의 MXFP4 지원과 설치 조건을 확인합니다. 대화는 Harmony 형식으로 구성하며, reasoning effort와 출력 토큰 수를 고정해 비교합니다. 모델이 도구 호출 형식을 생성하는 일과 실제 프로그램을 실행하는 일은 구분합니다.

## 결과를 해석할 때

이 수치는 공식 안내의 조건이며 이 저장소에서 측정한 값이 아닙니다. 같은 이름의 hosted API 설정을 로컬 실행 설정에 그대로 적용할 수는 없습니다.

[공식 모델 카드 또는 문서](https://developers.openai.com/api/docs/models/gpt-oss-20b) · [공식 실행 코드 또는 참고 자료](https://developers.openai.com/cookbook/articles/gpt-oss/run-transformers)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

The total and active parameter counts describe different resource costs. Harmony formatting and MXFP4 hardware support matter when reproducing local inference. This is a source-based release analysis; model inference was not run locally.
