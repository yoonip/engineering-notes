# 근거 문서와 응답 구간: IBM Granite 3.3 2B | Grounding and response tags

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `ibm-granite/granite-3.3-2b-instruct` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 약 2B · 128k 문맥 · 구조화된 추론 출력 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

이 Instruct 배포물은 Granite-3.3-2B-Base를 바탕으로 추론과 지시 수행을 조정한 모델입니다. 공식 설명은 허용적인 라이선스의 자료와 구성한 합성 과제를 결합했다고 밝힙니다. 합성 과제는 학습용 자료를 생성·구성했다는 뜻이며, 사용자가 붙인 문서가 모두 옳다고 검증해 주는 기능을 뜻하지 않습니다.

[공식 Model Summary와 Training Data](https://huggingface.co/ibm-granite/granite-3.3-2b-instruct)는 이 계보와 자료 범위를 설명합니다. `<think>`와 `<response>`는 생성 텍스트의 구간 표식이며 별도 검색기나 사실 검증기의 실행 증거는 아닙니다. 학습된 가중치가 다음 토큰을 만들 때 근거 문서가 실제 입력에 있는지부터 구분해야 합니다.

공식 카드는 think와 response 태그로 추론 부분과 최종 응답을 구분합니다. RAG에 연결할 때는 문서가 실제 정답을 포함하는지와 모델이 그 근거를 사용했는지를 따로 평가해야 합니다. 한국어를 포함한 12개 언어가 지원 목록에 있습니다.

## 실행에 필요한 조건과 비교 항목

공식 chat template과 추론 설정을 사용합니다. 근거가 있는 질문·없는 질문·서로 충돌하는 문서를 준비하고, 인용 근거와 최종 답의 일치 여부를 기록합니다. 태그를 제거하기 전에 종료 조건과 출력이 잘리지 않았는지 확인합니다.

## 공개 범위와 한계

128k라는 입력 범위만으로 긴 문서의 사실 보존을 판단하지 않습니다. 검색기의 누락을 모델 오류로 세거나 정답이 없는 문서를 억지로 답하게 하면 비교 결과를 해석하기 어렵습니다.

## 근거 문서와 최종 답의 경로

RAG는 질문에 관련된 문서를 검색하고 그 문서를 모델 입력에 붙여 답하게 하는 방식입니다. 검색기가 원문을 가져오는 일과 모델이 그 원문을 읽는 일은 다릅니다. Granite의 `thinking=True` 입력 설정과 `<think>`·`<response>` 출력 구분을 사용하면, 최종 답 평가에 어떤 부분을 쓸지도 명시해야 합니다. 태그가 있는 출력이라는 사실이 그 내용의 사실성을 보장하지는 않습니다. [공식 생성 예제와 출력 형식](https://huggingface.co/ibm-granite/granite-3.3-2b-instruct)

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#ibm)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/ibm-granite/granite-3.3-2b-instruct) · [공식 실행 코드 또는 참고 자료](https://github.com/ibm-granite/granite-3.3-language-models)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Granite separates reasoning and final-response tags. A RAG evaluation should score retrieval coverage and evidence-grounded answers independently. This is a source-based release analysis; model inference was not run locally.
