# Meta Llama 3.2 1B Instruct

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `meta-llama/Llama-3.2-1B-Instruct` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 자기회귀 Transformer · 약 1.23B · GQA |
| 사용 조건의 표기 | Llama 3.2 Community License 및 사용 정책 |

## 구조와 용도

이 배포물은 1B·3B 텍스트 계열에 속합니다. GQA는 여러 Q 헤드가 K·V 헤드를 공유하여 캐시 저장량을 줄이는 구조입니다. 공식 지원 8개 언어 목록에 한국어는 없으므로 한국어 출력을 생성할 수 있다는 것과 공식 한국어 성능 보장을 구분해야 합니다.

## 재현 방법과 비교 항목

가중치 접근 조건을 확인하고 tokenizer의 템플릿을 사용합니다. 한국어 존댓말·숫자·고유명사 유지 과제를 별도로 준비합니다. 원본 텍스트 모델과 공식 양자화 배포물은 문맥 한도도 다를 수 있으므로 모델 ID와 설정 파일을 함께 남깁니다.

## 결과를 해석할 때

Llama 가중치의 사용 조건은 Apache 2.0과 같지 않습니다. 다른 Llama 기반 파생 모델에도 원래 모델의 출처와 적용 조건을 확인해야 합니다.

[공식 모델 카드 또는 문서](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct) · [공식 실행 코드 또는 참고 자료](https://github.com/meta-llama/llama-models)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

This note covers the 1B text model and GQA, not every Llama variant. Korean quality needs its own evaluation because Korean is outside the listed eight supported languages. This is a source-based release analysis; model inference was not run locally.
