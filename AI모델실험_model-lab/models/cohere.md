# Cohere Labs Aya Expanse 8B

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `CohereLabs/aya-expanse-8b` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 다국어 연구 모델 · 약 8B · 8k 문맥 |
| 사용 조건의 표기 | CC-BY-NC 4.0 및 관련 사용 정책 |

## 구조와 용도

한국어를 포함한 다국어 평가가 목적에 들어 있습니다. 같은 질문을 단순 번역하면 언어마다 정답 난도나 문화적 전제가 달라질 수 있으므로 공통 사실 과제와 언어별 표현 과제를 나누는 편이 해석에 도움이 됩니다.

## 재현 방법과 비교 항목

공식 chat template을 사용하고 한국어·영어의 같은 사실 추출 문제를 쌍으로 준비합니다. 의미 보존·존댓말·고유명사·숫자 정확성을 구분해 셉니다. 출력 길이와 모델별 tokenizer 차이도 기록합니다.

## 결과를 해석할 때

연구용 공개 가중치와 Cohere의 상용 API를 같은 사용 조건으로 취급하면 안 됩니다. 이 배포물은 비상업 라이선스이며 다른 Command·Aya 배포물의 조건도 따로 확인해야 합니다.

[공식 모델 카드 또는 문서](https://huggingface.co/CohereLabs/aya-expanse-8b) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/CohereLabs/aya-expanse-8b)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Aya Expanse offers multilingual research weights. Parallel factual tests and language-specific style tests answer different questions. This is a source-based release analysis; model inference was not run locally.
