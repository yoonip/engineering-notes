# Microsoft Phi-4-mini-instruct

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `microsoft/Phi-4-mini-instruct` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 소형 자기회귀 언어 모델 · 128k 문맥 |
| 사용 조건의 표기 | MIT |

## 구조와 용도

공식 카드는 합성 데이터와 선별한 공개 웹 데이터, SFT·DPO를 설명합니다. 작은 모델에서 데이터의 목적과 분포가 중요하다는 사례입니다. 문맥 한도가 길어도 필요한 정보를 끝까지 정확히 찾아낸다는 보장은 아닙니다.

## 재현 방법과 비교 항목

공식 모델 카드의 Transformers 예제를 따라 tokenizer와 모델을 함께 고정합니다. 기본 attention 커널이 장치에서 동작하는지 확인하고, 지원되지 않는 장치에서는 카드가 안내한 eager 경로를 검토합니다. 근거 문장을 앞·중간·뒤에 둔 검색 과제로 길이별 정확도를 비교합니다.

## 결과를 해석할 때

공식 벤치마크의 수학·논리 점수를 한국어 문서 성능으로 옮기지 않습니다. 이 문서는 데이터·실행 조건 분석이며 실제 Phi 추론 결과를 포함하지 않습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/microsoft/Phi-4-mini-instruct) · [공식 실행 코드 또는 참고 자료](https://github.com/microsoft/PhiCookBook)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Synthetic-data design and SFT/DPO are central to this release. Kernel compatibility and long-context retrieval quality require separate checks. This is a source-based release analysis; model inference was not run locally.
