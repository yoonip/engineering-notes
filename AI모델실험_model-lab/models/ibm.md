# IBM Granite 3.3 2B Instruct

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `ibm-granite/granite-3.3-2b-instruct` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 약 2B · 128k 문맥 · 구조화된 추론 출력 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

공식 카드는 think와 response 태그로 추론 부분과 최종 응답을 구분합니다. RAG에 연결할 때는 문서가 실제 정답을 포함하는지와 모델이 그 근거를 사용했는지를 따로 평가해야 합니다. 한국어를 포함한 12개 언어가 지원 목록에 있습니다.

## 재현 방법과 비교 항목

공식 chat template과 추론 설정을 사용합니다. 근거가 있는 질문·없는 질문·서로 충돌하는 문서를 준비하고, 인용 근거와 최종 답의 일치 여부를 기록합니다. 태그를 제거하기 전에 종료 조건과 출력이 잘리지 않았는지 확인합니다.

## 결과를 해석할 때

128k라는 입력 범위만으로 긴 문서의 사실 보존을 판단하지 않습니다. 검색기의 누락을 모델 오류로 세거나 정답이 없는 문서를 억지로 답하게 하면 비교 결과를 해석하기 어렵습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/ibm-granite/granite-3.3-2b-instruct) · [공식 실행 코드 또는 참고 자료](https://github.com/ibm-granite/granite-3.3-language-models)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Granite separates reasoning and final-response tags. A RAG evaluation should score retrieval coverage and evidence-grounded answers independently. This is a source-based release analysis; model inference was not run locally.
