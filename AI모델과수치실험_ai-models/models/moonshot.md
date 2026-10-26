# 전문가 라우팅과 MLA: Kimi-K2-Instruct | Expert routing and latent attention

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `moonshotai/Kimi-K2-Instruct` |
| 제공·입출력 | 공개 가중치 · 텍스트·도구 사용 |
| 구조·설정 | MoE · 전체 1T / 활성 32B · MLA |
| 사용 조건의 표기 | Modified MIT |

## 구조와 용도

MLA(multi-head latent attention)는 K·V 관련 정보를 더 작은 잠재 표현으로 압축해 다루는 attention 설계입니다. 잠재 표현은 바로 읽을 수 있는 문장이 아니라 내부 수 배열입니다. 따라서 full-attention 모델의 KV 식을 수정 없이 대입해 실제 메모리를 확정하지 않습니다.

[공식 Model Introduction과 Summary](https://huggingface.co/moonshotai/Kimi-K2-Instruct#2-model-summary)는 Muon 계열 최적화와 Base·Instruct를 구분하며 원본 Instruct를 긴 사고가 없는 배포물로 설명합니다. 이 글은 원본 K2-Instruct를 대상으로 하므로 뒤에 나온 K2 Thinking의 긴 추론 방식을 대신 설명하지 않습니다. 전체·활성 파라미터와 외부 도구 실행 비용도 다른 수치입니다.

공식 카드는 전문가 384개 중 토큰마다 8개를 선택하고 공유 전문가 하나를 둔다고 설명합니다. 전체 1T를 BF16으로 단순 계산하면 약 2TB payload입니다. 활성 32B를 전체 모델 크기로 읽으면 배포 계획이 크게 달라집니다.

## 실행에 필요한 조건과 비교 항목

공식 chat template과 도구 schema를 함께 고정합니다. 도구 요청·도구 응답·후속 대화의 연결이 유지되는지 다중 단계 과제로 확인합니다. 배포 전에는 runtime의 MLA·MoE·양자화 지원을 확인합니다.

## 공개 범위와 한계

원본 K2-Instruct를 뒤에 나온 모든 Kimi 추론 모델과 같은 동작으로 취급하지 않습니다. Modified MIT의 추가 조건은 일반 MIT라는 이름으로 생략하면 안 됩니다.

## 전문가 선택과 도구 실행은 다른 선택입니다

MoE의 전문가는 모델 내부의 신경망 부분이며 외부 검색기·계산기 같은 도구가 아닙니다. 토큰마다 전문가 일부를 선택하는 연산과, 응답에서 함수를 요청하는 행동을 구분해야 합니다. MLA 역시 문맥 표현을 다루는 내부 attention 방식입니다. 활성 32B는 한 토큰의 계산에 참여하는 규모를 설명하며 모든 입력이 항상 같은 전문가만 쓰거나 전체 체크포인트가 32B라는 뜻은 아닙니다. [K2 원본 배포물의 구조 표](https://huggingface.co/moonshotai/Kimi-K2-Instruct#2-model-summary)

공식 도구 예제에서는 함수 인자를 JSON 문자열에서 객체로 읽고, 애플리케이션이 함수를 실행한 뒤 해당 `tool_call_id`에 결과를 연결합니다. 모델의 호출 요청, 실제 함수 실행, 결과를 반영한 최종 답이 한 번의 텍스트 생성과 동일하지 않은 이유입니다. [공식 도구 연결 예제](https://github.com/MoonshotAI/Kimi-K2#5-model-usage)

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#moonshot-ai)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/moonshotai/Kimi-K2-Instruct) · [공식 실행 코드 또는 참고 자료](https://github.com/MoonshotAI/Kimi-K2)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Total storage, active experts, and MLA state are separate deployment concerns. The original K2-Instruct release is the subject of this note. This is a source-based release analysis; model inference was not run locally.
