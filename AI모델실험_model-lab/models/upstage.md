# 깊이 확장과 후속 학습: SOLAR 10.7B | Depth Up-Scaling and post-training

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `upstage/SOLAR-10.7B-Instruct-v1.0` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | Depth Up-Scaling · 약 10.7B · 단일 턴 대화 조정 |
| 사용 조건의 표기 | 이 Instruct 배포물은 CC-BY-NC 4.0 |

## 구조와 용도

이 배포물은 SOLAR-10.7B-v1.0을 SFT와 반복 DPO로 조정한 Instruct입니다. 공식 설명은 Mistral 7B 가중치를 확장된 층에 넣고 계속 사전학습하는 DUS와, 그 뒤 지시 조정의 자료·목표를 나눕니다. 모델의 기반 구성, 학습 단계, 최종 사용 조건이 서로 연결되어도 같은 항목은 아닙니다.

[공식 Instruction Fine-Tuning Strategy](https://huggingface.co/upstage/SOLAR-10.7B-Instruct-v1.0#instruction-fine-tuning-strategy)는 사용한 자료와 평가 오염 방지 조치를 설명합니다. 개발자가 보고한 오염 검사는 모든 외부 입력·모든 후속 평가에서 오염이 없다는 증명으로 확대하지 않습니다. 함수로 구성한 자체 비교 예는 별도 평가 설계 문서에 있습니다.

Depth Up-Scaling은 층 구성을 늘리고 이어서 사전학습하는 접근입니다. TRM처럼 같은 작은 네트워크를 반복하는 방식과 파라미터 공유가 다릅니다. 공식 카드는 이 Instruct 버전이 주로 단일 턴 대화에 맞춰져 있다고 설명합니다.

## 실행에 필요한 조건과 비교 항목

공식 모델 ID와 chat template으로 독립 질문을 평가합니다. 다중 턴 성능을 확인하려면 앞 대화의 사실을 이어받는 과제를 별도로 둡니다. 원본 SOLAR base와 Instruct를 비교할 때 학습 단계·사용 조건도 함께 기록합니다.

## 공개 범위와 한계

Base의 Apache 2.0 조건을 Instruct에 그대로 옮기면 안 됩니다. 공식 카드에서 Instruct는 비상업 데이터를 이용한 조정 때문에 CC-BY-NC로 구분합니다.

## 층을 복사한 뒤에도 학습이 필요합니다

논문의 DUS는 32층 모형을 복제한 뒤 한쪽의 마지막 8층, 다른 쪽의 첫 8층을 제외하고 연결해 2×(32−8)=48층을 만듭니다. 이어 계속 사전학습을 수행합니다. 연결만으로 끝난 기법으로 읽으면 학습 단계를 빠뜨립니다. 이 관계는 원 논문 §2·그림1에서 확인할 수 있습니다. [DUS 원문](https://arxiv.org/html/2312.15166v3#S2)

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#upstage)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/upstage/SOLAR-10.7B-Instruct-v1.0) · [공식 실행 코드 또는 참고 자료](https://arxiv.org/abs/2312.15166)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Depth Up-Scaling grows the stored network, unlike shared-weight recursion. This Instruct release is primarily single-turn and has different terms from the base model. This is a source-based release analysis; model inference was not run locally.
