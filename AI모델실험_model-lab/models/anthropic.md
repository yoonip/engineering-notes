# Anthropic Claude Sonnet 5.5

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `claude-sonnet-5-5` |
| 제공·입출력 | Hosted API · 텍스트·이미지 → 텍스트 |
| 구조·설정 | 가중치 구조 대신 API 입출력 계약을 분석합니다. |
| 사용 조건의 표기 | 서비스 이용 조건 · 가중치 배포 라이선스가 아닙니다. |

## 구조와 용도

공식 문서는 1M 문맥과 최대 128k 출력을 안내합니다. 중요한 구현 차이는 응답이 단일 문자열이 아니라 thinking·text·도구 관련 블록으로 구성된다는 점입니다. 도구 사이의 출력 블록 처리가 잘못되면 실제 응답이 있어도 사용자 화면이 비어 보일 수 있습니다.

## 재현 방법과 비교 항목

공식 모델 ID를 고정하고 Messages 응답의 블록 유형·중단 이유·usage를 기록합니다. 문서 추출 과제에서는 정답 필드와 존재하지 않는 필드를 섞어 누락과 환각을 구분합니다. 호출 한도와 계정 접근은 실행 직전에 공식 설정에서 확인합니다.

## 결과를 해석할 때

현재 카드에는 temperature·top_p·top_k를 기본값과 다르게 주면 오류가 난다는 조건이 있습니다. 공개 모델의 공통 sampling 예제를 그대로 옮기면 안 됩니다. 유료 API를 호출하지 않았으므로 응답 품질·지연·비용 측정치는 없습니다.

[공식 모델 카드 또는 문서](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) · [공식 실행 코드 또는 참고 자료](https://platform.claude.com/docs/en/models/overview)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

This API analysis focuses on content blocks, limits, and supported parameters. No API calls, latency measurements, or quality comparisons were performed. This is a source-based release analysis; model inference was not run locally.
