# xAI Grok-1 공개 배포물

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `xai-org/grok-1` |
| 제공·입출력 | 공개 가중치와 JAX 실행 예제 |
| 구조·설정 | 전체 314B · 전문가 8개 중 토큰마다 2개 선택 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

공개 Grok-1 저장소는 서비스의 현재 Grok API와 별개입니다. 전체 파라미터가 314B이므로 전문가 일부만 활성화되어도 가중치 저장량은 큽니다. 공식 저장소는 MoE 구현이 효율보다 정확성 확인에 초점을 둔다고 설명합니다.

## 재현 방법과 비교 항목

공식 JAX 예제와 체크포인트 형식을 함께 사용합니다. 충분한 장치 메모리와 분산 구성을 확인한 뒤 공식 run.py 경로로 실행합니다. 성능을 재려면 단순 참조 구현과 최적화된 runtime을 구분해 기록합니다.

## 결과를 해석할 때

공개 참조 코드의 속도를 Grok API 지연으로 해석할 수 없습니다. 이 분석은 공개 1세대 배포물에 한정하며 서비스 모델의 구조·성능을 추정하지 않습니다.

[공식 모델 카드 또는 문서](https://github.com/xai-org/grok-1) · [공식 실행 코드 또는 참고 자료](https://github.com/xai-org/grok-1/blob/main/model.py)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

The public JAX reference implementation and hosted Grok services are different artifacts. Active experts reduce selected computation, not total checkpoint storage. This is a source-based release analysis; model inference was not run locally.
