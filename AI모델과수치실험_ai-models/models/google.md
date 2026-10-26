# 크기별 입력 범위: Google Gemma 3 1B IT | Text-only Gemma

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `google/gemma-3-1b-it` |
| 제공·입출력 | 공개 가중치 · 이 1B 배포물은 텍스트 → 텍스트 |
| 구조·설정 | 자기회귀 Transformer · 약 1B |
| 사용 조건의 표기 | Gemma 사용 조건 |

## 구조와 용도

자기회귀(autoregressive)는 이미 주어진 토큰을 조건으로 다음 토큰을 차례로 예측한다는 뜻입니다. IT는 instruction-tuned, 즉 지시에 맞는 응답을 하도록 조정된 배포물을 가리킵니다. 문서의 일부를 요약하게 하는 추론과 모델의 가중치를 바꾸는 학습은 다른 과정입니다.

[공식 모델 카드의 Model Data](https://ai.google.dev/gemma/docs/core/model_card_3#model_data)는 1B의 학습량을 2조 토큰으로 적고 웹 문서·코드·수학 자료를 설명합니다. 계열 설명에는 이미지도 있지만 여기서 선택한 1B는 텍스트 모델입니다. 큰 Gemma의 시각 입력이나 Gemini의 비공개 학습 구조를 1B의 확인된 특징으로 넣지 않습니다.

Gemma는 직접 내려받는 모델 계열이며 Gemini API와 별도 배포물입니다. Gemma 3의 큰 모델에 이미지 입력이 있다고 해서 1B 모델에도 같은 기능이 있다고 판단하면 안 됩니다. 1B의 문맥 한도는 32k이며 4B·12B·27B의 128k와 다릅니다.

## 실행에 필요한 조건과 비교 항목

공식 모델 카드에서 1B 예제를 선택하고 사용 조건에 동의한 뒤 tokenizer의 chat template을 적용합니다. 한국어 요약에서는 같은 문서의 핵심 사실 보존과 근거 없는 문장 추가를 따로 셉니다. 긴 문맥 실험에서는 입력 토큰과 생성 토큰의 합을 기록합니다.

## 공개 범위와 한계

모델 카드의 계열 설명과 개별 크기의 기능을 구분해야 합니다. 저장소에서는 가중치를 받지 않았으며 이미지 처리나 한국어 점수를 측정하지 않았습니다.

## 1B 텍스트 모델의 대화 흐름

대화 메시지는 template과 tokenizer를 거쳐 정수 ID가 되고, 1B 언어 모델은 앞선 ID를 조건으로 다음 ID를 생성합니다. 디코딩은 그 ID를 글자로 되돌리는 일입니다. 이 배포물의 입력에 이미지 블록을 붙이는 것은 모델을 더 크게 만드는 방법이 아닙니다. 해당 1B 텍스트 경로와 큰 멀티모달 모델의 처리기를 구별해야 합니다. [Gemma 3의 크기별 입력 범위](https://ai.google.dev/gemma/docs/core/model_card_3#inputs_and_outputs)

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#google)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/google/gemma-3-1b-it) · [공식 실행 코드 또는 참고 자료](https://ai.google.dev/gemma/docs/core/model_card_3)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Gemma 3 1B is the text-only member examined here. Its input range and context budget should not be inferred from the larger multimodal variants. This is a source-based release analysis; model inference was not run locally.
