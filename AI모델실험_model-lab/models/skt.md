# SK Telecom A.X 4.0 Light

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `skt/A.X-4.0-Light` |
| 제공·입출력 | 공개 가중치 · 한국어 중심 텍스트 |
| 구조·설정 | Qwen2.5 기반 추가 학습 · 약 7B · 16,384 문맥 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

한국어 데이터를 추가 학습한 배포물입니다. 공식 카드의 계열 설명에는 72B 모델도 있지만 Light의 문맥은 16,384로 별도 표기합니다. 같은 A.X 4.0 이름만 보고 72B의 131,072 한도를 적용하면 안 됩니다.

## 재현 방법과 비교 항목

Light의 model ID·tokenizer·template을 함께 고정합니다. 한국어 기업 문서의 수치·약어·표현을 추출하고 기본 Qwen 계열과 비교하려면 입력과 채점 기준을 같게 둡니다. tokenizer 차이는 동일 문장의 token 수로 따로 기록합니다.

## 결과를 해석할 때

한국어 추가 학습이 모든 수학·코드 능력을 같은 방향으로 바꾼다고 단정하지 않습니다. 계열 전체의 홍보 점수를 Light의 직접 측정값처럼 옮기지 않습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/skt/A.X-4.0-Light) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/skt/A.X-4.0-Light)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

The Light variant has its own 16,384-token limit. Family-level benchmark descriptions should not be relabeled as measurements of this smaller checkpoint. This is a source-based release analysis; model inference was not run locally.
