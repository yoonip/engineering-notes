# NCSOFT Llama VARCO 8B Instruct

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `NCSOFT/Llama-VARCO-8B-Instruct` |
| 제공·입출력 | 공개 가중치 · 한국어·영어 텍스트 |
| 구조·설정 | Llama 3.1 8B 기반 명령 조정 |
| 사용 조건의 표기 | Llama 3.1 Community License |

## 구조와 용도

개발 기관은 NCSOFT이지만 기반 모델은 Meta Llama 3.1입니다. 모델의 개발자와 기반 계보를 함께 적어야 구조·tokenizer·사용 조건을 설명할 수 있습니다. 회사별 폴더가 모델의 원래 구조까지 독립적으로 발명했다는 의미는 아닙니다.

## 재현 방법과 비교 항목

공식 카드의 Transformers 예제와 template을 사용합니다. 기본 Llama 계열과 한국어 표현·고유명사·문서 질의응답을 비교할 때 같은 입력과 출력 예산을 적용합니다. 추가 학습의 효과는 실제 응답과 오류 유형을 함께 남깁니다.

## 결과를 해석할 때

한국어 조정 모델이라고 모든 한국어 도메인에 적합한 것은 아닙니다. Llama 기반이라는 사실을 생략하고 독립 Apache 배포물로 소개하지 않습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/NCSOFT/Llama-VARCO-8B-Instruct) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

The developer and base-model lineage answer different questions. This VARCO checkpoint inherits a Llama architecture and should retain the applicable base-model attribution and terms. This is a source-based release analysis; model inference was not run locally.
