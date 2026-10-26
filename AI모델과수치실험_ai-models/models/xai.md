# 공개 전문가 모델의 범위: xAI Grok-1 | Public MoE checkpoint

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `xai-org/grok-1` |
| 제공·입출력 | 공개 가중치와 JAX 실행 예제 |
| 구조·설정 | 전체 314B · 전문가 8개 중 토큰마다 2개 선택 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

공개 사양은 64층, Q/KV 헤드 48/8, rotary embedding을 명시합니다. Rotary embedding(RoPE)은 토큰의 위치 관계를 Q·K 표현에 반영하는 방식이며 최신 뉴스 검색 기능이 아닙니다. 8개 전문가 중 2개를 선택하는 MoE는 모델 내부 계산 경로입니다.

[공식 Grok-1 저장소](https://github.com/xai-org/grok-1#model-specifications)는 JAX 참조 추론과 공개 체크포인트의 사양을 제공합니다. 이 자료만으로 서비스의 최신 Grok나 그 학습 전체를 설명하지 않습니다. 가중치가 공개되었다는 사실과 처음부터 동일한 모델을 재학습할 전체 데이터·인프라가 준비되었다는 사실은 다릅니다.

공개 Grok-1 저장소는 서비스의 현재 Grok API와 별개입니다. 전체 파라미터가 314B이므로 전문가 일부만 활성화되어도 가중치 저장량은 큽니다. 공식 저장소는 MoE 구현이 효율보다 정확성 확인에 초점을 둔다고 설명합니다.

## 실행에 필요한 조건과 비교 항목

공식 JAX 예제와 체크포인트 형식을 함께 사용합니다. 충분한 장치 메모리와 분산 구성을 확인한 뒤 공식 run.py 경로로 실행합니다. 성능을 재려면 단순 참조 구현과 최적화된 runtime을 구분해 기록합니다.

## 공개 범위와 한계

공개 참조 코드의 속도를 Grok API 지연으로 해석할 수 없습니다. 이 분석은 공개 1세대 배포물에 한정하며 서비스 모델의 구조·성능을 추정하지 않습니다.

## 공개 JAX 예제에서 무엇이 흘러갑니까

참조 실행 코드는 모델 구조·체크포인트 경로·추론 실행기를 구성하고 시험 입력에서 토큰을 샘플링합니다. SentencePiece tokenizer의 정수 ID와 JAX의 가중치 배열, 생성 결과를 글자로 되돌리는 단계는 서로 다른 자료입니다. 현재 서비스의 대화 API 요청 형식을 이 로컬 예제의 입력 계약으로 대신하지 않습니다. [공식 run.py](https://raw.githubusercontent.com/xai-org/grok-1/main/run.py)

## 저장 크기와 답변 품질의 분리

전체 314B를 모두 원소당 2바이트로 둔 자체 근사는 628,000,000,000바이트입니다. 이는 가중치 본문의 산술이며 실제 체크포인트 형식·최대 GPU 메모리 측정이 아닙니다. 전문가 2/8을 선택한다는 비율 1/4은 모든 저장량이나 연산이 무조건 1/4이라는 뜻도 아닙니다. 공유하는 부분과 모든 전문가의 보관 비용이 따로 있습니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#xai)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://github.com/xai-org/grok-1) · [공식 실행 코드 또는 참고 자료](https://github.com/xai-org/grok-1/blob/main/model.py)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

The public JAX reference implementation and hosted Grok services are different artifacts. Active experts reduce selected computation, not total checkpoint storage. This is a source-based release analysis; model inference was not run locally.
