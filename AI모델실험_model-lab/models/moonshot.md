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

[공식 모델 카드 또는 문서](https://huggingface.co/moonshotai/Kimi-K2-Instruct) · [공식 실행 코드 또는 참고 자료](https://github.com/MoonshotAI/Kimi-K2)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Total storage, active experts, and MLA state are separate deployment concerns. The original K2-Instruct release is the subject of this note. This is a source-based release analysis; model inference was not run locally.
