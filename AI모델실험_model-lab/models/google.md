# Google Gemma 3 1B IT

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `google/gemma-3-1b-it` |
| 제공·입출력 | 공개 가중치 · 이 1B 배포물은 텍스트 → 텍스트 |
| 구조·설정 | 자기회귀 Transformer · 약 1B |
| 사용 조건의 표기 | Gemma 사용 조건 |

## 구조와 용도

Gemma는 직접 내려받는 모델 계열이며 Gemini API와 별도 배포물입니다. Gemma 3의 큰 모델에 이미지 입력이 있다고 해서 1B 모델에도 같은 기능이 있다고 판단하면 안 됩니다. 1B의 문맥 한도는 32k이며 4B·12B·27B의 128k와 다릅니다.

## 재현 방법과 비교 항목

공식 모델 카드에서 1B 예제를 선택하고 사용 조건에 동의한 뒤 tokenizer의 chat template을 적용합니다. 한국어 요약에서는 같은 문서의 핵심 사실 보존과 근거 없는 문장 추가를 따로 셉니다. 긴 문맥 실험에서는 입력 토큰과 생성 토큰의 합을 기록합니다.

## 결과를 해석할 때

모델 카드의 계열 설명과 개별 크기의 기능을 구분해야 합니다. 저장소에서는 가중치를 받지 않았으며 이미지 처리나 한국어 점수를 측정하지 않았습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/google/gemma-3-1b-it) · [공식 실행 코드 또는 참고 자료](https://ai.google.dev/gemma/docs/core/model_card_3)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Gemma 3 1B is the text-only member examined here. Its input range and context budget should not be inferred from the larger multimodal variants. This is a source-based release analysis; model inference was not run locally.
