# 응답 블록과 공개 범위: Claude Sonnet 5.5 | API content blocks

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `claude-sonnet-5-5` |
| 제공·입출력 | Hosted API · 텍스트·이미지 → 텍스트 |
| 구조·설정 | 가중치 구조 대신 API 입출력 계약을 분석합니다. |
| 사용 조건의 표기 | 서비스 이용 조건 · 가중치 배포 라이선스가 아닙니다. |

## 구조와 용도

이 문서는 공개 API의 입출력 계약을 분석합니다. 확인한 공식 문서만으로 Sonnet 5.5의 층 수·전문가 수·가중치·학습 데이터 전체를 확정할 수 없습니다. `thinking`이라는 응답 블록 이름도 내부가 특정 반복 신경망이라는 증거가 아닙니다. 이 한계를 공개 가중치 모델의 구조 분석과 구별합니다.

[공식 이전 안내](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide)는 블록을 `type`으로 구분하고, 반환받은 thinking 블록을 다음 요청에 보존하는 방법을 설명합니다. 추론 요청의 effort나 예산 변경과 학습 과정은 다릅니다. 자체 덧셈·표 추출 예로 Claude의 학습이나 다른 모델보다 높은 성능을 입증하지 않습니다.

공식 문서는 1M 문맥과 최대 128k 출력을 안내합니다. 중요한 구현 차이는 응답이 단일 문자열이 아니라 thinking·text·도구 관련 블록으로 구성된다는 점입니다. 도구 사이의 출력 블록 처리가 잘못되면 실제 응답이 있어도 사용자 화면이 비어 보일 수 있습니다.

## 실행에 필요한 조건과 비교 항목

공식 모델 ID를 고정하고 Messages 응답의 블록 유형·중단 이유·usage를 기록합니다. 문서 추출 과제에서는 정답 필드와 존재하지 않는 필드를 섞어 누락과 환각을 구분합니다. 호출 한도와 계정 접근은 실행 직전에 공식 설정에서 확인합니다.

## 공개 범위와 한계

현재 카드에는 temperature·top_p·top_k를 기본값과 다르게 주면 오류가 난다는 조건이 있습니다. 공개 모델의 공통 sampling 예제를 그대로 옮기면 안 됩니다. 유료 API를 호출하지 않았으므로 응답 품질·지연·비용 측정치는 없습니다.

## 문자열 대신 블록을 처리하는 이유

Messages의 `content`를 ‘첫 항목의 text’로만 읽으면 첫 블록이 `thinking`일 때 문제가 생깁니다. Sonnet 5.5의 기본 설정에서는 읽을 사고 요약이 생략될 수 있으며, 빈 사고 텍스트도 응답이 없다는 뜻은 아닙니다. 블록 유형을 확인한 뒤 최종 텍스트와 도구 관련 내용을 각각 처리해야 합니다. 도구를 쓰는 대화에서 반환된 thinking 블록은 다음 요청에 원형대로 보존하는 조건도 있습니다. [공식 이전 안내의 응답 처리](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide#handle-thinking-in-responses)

`max_tokens`는 thinking과 text에 함께 쓰이는 예산입니다. 출력 예산을 매우 작게 잡고 최종 답만 짧으니 충분하다고 생각하면, 그 앞의 처리 때문에 답이 잘릴 수 있습니다. 모델이 지원하는 출력 한도, 요청에서 정한 예산, 실제 중단 이유는 서로 다른 값입니다. 이 카드의 128k는 모든 요청에서 그만큼 생성한다는 뜻이 아닙니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#anthropic)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) · [공식 실행 코드 또는 참고 자료](https://platform.claude.com/docs/en/models/overview)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

This API analysis focuses on content blocks, limits, and supported parameters. No API calls, latency measurements, or quality comparisons were performed. The public API documentation does not establish its private weight architecture or complete training recipe.
