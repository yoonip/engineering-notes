# Moonshot Kimi-K2-Instruct

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `moonshotai/Kimi-K2-Instruct` |
| 제공·입출력 | 공개 가중치 · 텍스트·도구 사용 |
| 구조·설정 | MoE · 전체 1T / 활성 32B · MLA |
| 사용 조건의 표기 | Modified MIT |

## 구조와 용도

공식 카드는 전문가 384개 중 토큰마다 8개를 선택하고 공유 전문가 하나를 둔다고 설명합니다. 전체 1T를 BF16으로 단순 계산하면 약 2TB payload입니다. 활성 32B를 전체 모델 크기로 읽으면 배포 계획이 크게 달라집니다.

## 재현 방법과 비교 항목

공식 chat template과 도구 schema를 함께 고정합니다. 도구 요청·도구 응답·후속 대화의 연결이 유지되는지 다중 단계 과제로 확인합니다. 배포 전에는 runtime의 MLA·MoE·양자화 지원을 확인합니다.

## 결과를 해석할 때

원본 K2-Instruct를 뒤에 나온 모든 Kimi 추론 모델과 같은 동작으로 취급하지 않습니다. Modified MIT의 추가 조건은 일반 MIT라는 이름으로 생략하면 안 됩니다.

## 전문가 선택과 도구 실행은 다른 선택입니다

MoE의 전문가는 모델 내부의 신경망 부분이며 외부 검색기·계산기 같은 도구가 아닙니다. 토큰마다 전문가 일부를 선택하는 연산과, 응답에서 함수를 요청하는 행동을 구분해야 합니다. MLA 역시 문맥 표현을 다루는 내부 attention 방식입니다. 활성 32B는 한 토큰의 계산에 참여하는 규모를 설명하며 모든 입력이 항상 같은 전문가만 쓰거나 전체 체크포인트가 32B라는 뜻은 아닙니다. [K2 원본 배포물의 구조 표](https://huggingface.co/moonshotai/Kimi-K2-Instruct#2-model-summary)

공식 도구 예제에서는 함수 인자를 JSON 문자열에서 객체로 읽고, 애플리케이션이 함수를 실행한 뒤 해당 `tool_call_id`에 결과를 연결합니다. 모델의 호출 요청, 실제 함수 실행, 결과를 반영한 최종 답이 한 번의 텍스트 생성과 동일하지 않은 이유입니다. [공식 도구 연결 예제](https://github.com/MoonshotAI/Kimi-K2#5-model-usage)

## 직접 만든 조회·계산의 연결 예

자체 시험은 “품목 P07을 세 개 살 때의 금액과 재고 충족 여부를 알려 주세요.”입니다. 평가지의 가정 자료는 단가 1,200원, 재고 2개라고 정합니다. 이는 실제 API 응답이 아니라 도구 결과가 주어졌을 때의 후속 판단을 검사하기 위한 고정 자료입니다.

| 단계 | 정답 기준 | 실패 사례 |
| --- | --- | --- |
| 조회 인자 | 품목 코드 P07을 그대로 사용합니다. | 이름이 비슷한 다른 품목을 조회하면 안 됩니다. |
| 결과 연결 | 단가와 재고의 필드를 구분합니다. | 재고 2를 단가로 읽으면 의미 오류입니다. |
| 금액 | 요청 수량 기준 1,200×3=3,600원입니다. | 재고 수량 2를 곱하면 질문을 바꿉니다. |
| 충족 여부 | 필요한 3개보다 재고가 1개 부족합니다. | 금액 계산만 맞고 구매 가능하다고 답하면 오답입니다. |

조회에 실패했다면 가격을 0으로 간주하는 대신 확인할 수 없는 값으로 남겨야 합니다. 같은 형식의 JSON이라도 요청한 품목과 연결되지 않으면 정답의 근거가 아닙니다. 이 시험은 대화 템플릿과 호출 ID의 보존을 보려는 구성으로, 거대한 가중치를 실제로 올렸거나 도구를 실행한 기록이 아닙니다. 원본 K2-Instruct의 동작과 후속 장기 추론 배포물도 분리해서 봅니다.

[공식 모델 카드 또는 문서](https://huggingface.co/moonshotai/Kimi-K2-Instruct) · [공식 실행 코드 또는 참고 자료](https://github.com/MoonshotAI/Kimi-K2)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Total storage, active experts, and MLA state are separate deployment concerns. The original K2-Instruct release is the subject of this note. This is a source-based release analysis; model inference was not run locally.
