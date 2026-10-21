# 합성 데이터와 지시 학습: Microsoft Phi-4-mini | Data and post-training

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `microsoft/Phi-4-mini-instruct` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 소형 자기회귀 언어 모델 · 128k 문맥 |
| 사용 조건의 표기 | MIT |

## 구조와 용도

공식 카드의 3.8B는 학습된 매개변수의 규모이며 128k는 문맥 길이입니다. 단위가 서로 달라 어느 하나로 다른 하나를 대신할 수 없습니다. 학습은 합성 자료와 선별한 웹 자료를 이용하고, SFT와 DPO로 이어집니다. SFT(supervised fine-tuning)는 질문과 모범 답을 맞추는 조정이고, DPO(direct preference optimization)는 선호한 답과 덜 선호한 답의 쌍을 이용하는 조정입니다.

[공식 Model Summary와 Model Quality](https://huggingface.co/microsoft/Phi-4-mini-instruct)는 이 배포물의 데이터·후속 학습을 설명합니다. 추론에서는 조정된 가중치를 불러 다음 토큰을 생성합니다. 짧은 정답표를 만든 일은 Phi를 학습하거나 평가한 일이 아니며, 합성 자료의 전체 생성 과정을 이 저장소에서 재현하지 않았습니다.

공식 카드는 합성 데이터와 선별한 공개 웹 데이터, SFT·DPO를 설명합니다. 작은 모델에서 데이터의 목적과 분포가 중요하다는 사례입니다. 문맥 한도가 길어도 필요한 정보를 끝까지 정확히 찾아낸다는 보장은 아닙니다.

## 실행에 필요한 조건과 비교 항목

공식 모델 카드의 Transformers 예제를 따라 tokenizer와 모델을 함께 고정합니다. 기본 attention 커널이 장치에서 동작하는지 확인하고, 지원되지 않는 장치에서는 카드가 안내한 eager 경로를 검토합니다. 근거 문장을 앞·중간·뒤에 둔 검색 과제로 길이별 정확도를 비교합니다.

## 공개 범위와 한계

공식 벤치마크의 수학·논리 점수를 한국어 문서 성능으로 옮기지 않습니다. 이 문서는 데이터·실행 조건 분석이며 실제 Phi 추론 결과를 포함하지 않습니다.

## 대화 역할과 생성 구간

Phi-4-mini-instruct는 질문·시스템 지시·응답의 경계를 대화 형식으로 표현합니다. tokenizer의 template을 적용한 정수 ID와 모델의 가중치 자료형은 역할이 다릅니다. `generate`의 결과를 decode할 때 질문을 포함한 전체와 새 응답을 구분해야 합니다. 함수 호출도 전용 입력 형식을 사용하는 별도 과제이므로 일반 대화 문자열만 바꿔 도구가 실행된 것으로 처리하지 않습니다. [공식 카드의 입력 형식](https://huggingface.co/microsoft/Phi-4-mini-instruct#input-formats)

합성 데이터는 사람이 직접 쓴 원문만이 아니라 생성·구성한 학습 사례를 포함한다는 뜻이고, 선별은 어떤 데이터를 남길지 정하는 일입니다. 이런 학습 설명이 사용자가 주는 자료의 사실을 항상 정확히 읽는다는 보증은 아닙니다. 모델 카드의 수학·논리 결과와 실제 문서 추출 과제를 따로 읽어야 하는 이유입니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#microsoft)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/microsoft/Phi-4-mini-instruct) · [공식 실행 코드 또는 참고 자료](https://github.com/microsoft/PhiCookBook)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Synthetic-data design and SFT/DPO are central to this release. Kernel compatibility and long-context retrieval quality require separate checks. This is a source-based release analysis; model inference was not run locally.
