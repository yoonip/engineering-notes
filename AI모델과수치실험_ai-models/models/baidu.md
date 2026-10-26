# 작은 밀집 모델과 배포 형식: ERNIE 4.5 0.3B PT | Dense model and weight format

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `baidu/ERNIE-4.5-0.3B-PT` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | Dense · 약 0.36B · 18층 · Q/KV 헤드 16/2 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

개별 Model Overview는 0.3B를 텍스트 dense post-trained 모델로 명시합니다. Post-training은 사전학습 뒤 지시·선호 등에 맞게 조정하는 단계입니다. 카드 앞부분의 대형 멀티모달 MoE 학습 기술은 계열 설명이므로 이 작은 모델의 전문가 배치나 시각 입력의 근거로 쓰지 않습니다.

[공식 개별 모델 표](https://huggingface.co/baidu/ERNIE-4.5-0.3B-PT#model-overview)의 18층·Q/KV 16/2를 대상으로 합니다. PT와 Paddle은 가중치 형식 구분이며 학습 단계의 이름이 아닙니다. 이 글은 작은 배포물에서 구체적으로 확인되지 않은 학습 손실·자료 비율을 계열 소개에서 추정해 채우지 않습니다.

ERNIE 4.5 계열에 MoE와 멀티모달 모델이 있어도 이 작은 배포물은 텍스트 dense 모델입니다. 이름 끝의 PT는 Transformer 방식 PyTorch 가중치이며 Paddle 배포물과 파일 형식이 다릅니다.

## 실행에 필요한 조건과 비교 항목

공식 카드의 Transformers 4.54.0 이상 조건과 템플릿을 확인합니다. 중국어·영어·한국어 문장을 같은 작업에 넣되 한국어는 별도 평가로 다룹니다. 형식 변환이 필요하다면 변환 전후 token ID와 출력 허용오차를 비교합니다.

## 공개 범위와 한계

계열 공통 설명의 heterogeneous MoE를 이 0.3B 모델의 구조로 옮기면 안 됩니다. 작은 가중치 크기만으로 사실 정확도나 한국어 품질을 단정할 수 없습니다.

## 텍스트가 생성 결과가 되는 과정

공식 예제의 입력은 `role`·`content`를 가진 메시지 목록입니다. `apply_chat_template`은 말한 주체와 차례를 표현하고 tokenizer는 이를 정수 token ID로 바꿉니다. `generate`가 돌려준 ID에서 입력 길이만큼 앞부분을 제외한 뒤 decode하는 이유는 새로 생성한 답과 원래 질문을 구분하기 위해서입니다. 질문까지 포함한 문자열을 정답으로 세면 입력에 이미 있던 숫자를 모델이 맞혔다고 오해할 수 있습니다. [공식 실행 예제](https://huggingface.co/baidu/ERNIE-4.5-0.3B-PT#using-transformers-library)

이 배포물의 Q/KV 헤드 수 16/2는 여덟 Q 헤드가 한 K·V 묶음을 공유하는 그룹 관계로 읽을 수 있습니다. Q는 앞 문맥에서 무엇을 찾을지, K·V는 그 문맥의 비교·내용 표현에 해당합니다. 그렇다고 계산 전체나 메모리 전체가 무조건 1/8이라는 뜻은 아닙니다. 이 비율은 K·V 헤드 수만 비교한 산술이며 측정한 속도 향상이 아닙니다. Dense라는 표기도 계열의 MoE 설명과 구별합니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#baidu)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/baidu/ERNIE-4.5-0.3B-PT) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/baidu/ERNIE-4.5-0.3B-PT)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

This small ERNIE release is dense and text-only. The PT and Paddle variants use different weight formats. This is a source-based release analysis; model inference was not run locally.
