# Upstage SOLAR 10.7B Instruct v1

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `upstage/SOLAR-10.7B-Instruct-v1.0` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | Depth Up-Scaling · 약 10.7B · 단일 턴 대화 조정 |
| 사용 조건의 표기 | 이 Instruct 배포물은 CC-BY-NC 4.0 |

## 구조와 용도

Depth Up-Scaling은 층 구성을 늘리고 이어서 사전학습하는 접근입니다. TRM처럼 같은 작은 네트워크를 반복하는 방식과 파라미터 공유가 다릅니다. 공식 카드는 이 Instruct 버전이 주로 단일 턴 대화에 맞춰져 있다고 설명합니다.

## 재현 방법과 비교 항목

공식 모델 ID와 chat template으로 독립 질문을 평가합니다. 다중 턴 성능을 확인하려면 앞 대화의 사실을 이어받는 과제를 별도로 둡니다. 원본 SOLAR base와 Instruct를 비교할 때 학습 단계·사용 조건도 함께 기록합니다.

## 결과를 해석할 때

Base의 Apache 2.0 조건을 Instruct에 그대로 옮기면 안 됩니다. 공식 카드에서 Instruct는 비상업 데이터를 이용한 조정 때문에 CC-BY-NC로 구분합니다.

[공식 모델 카드 또는 문서](https://huggingface.co/upstage/SOLAR-10.7B-Instruct-v1.0) · [공식 실행 코드 또는 참고 자료](https://arxiv.org/abs/2312.15166)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Depth Up-Scaling grows the stored network, unlike shared-weight recursion. This Instruct release is primarily single-turn and has different terms from the base model. This is a source-based release analysis; model inference was not run locally.
