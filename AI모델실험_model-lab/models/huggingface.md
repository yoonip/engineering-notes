# Hugging Face SmolLM2 135M Instruct

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `HuggingFaceTB/SmolLM2-135M-Instruct` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 약 135M Transformer decoder · SFT·DPO |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

Hugging Face는 배포 플랫폼이면서 자체 소형 모델도 제공합니다. Hub에 있다는 사실만으로 모델의 원저작자가 Hugging Face인 것은 아닙니다. SmolLM2 135M은 작은 모델의 데이터 구성과 명령 조정 과정을 읽기 좋은 구체적 사례입니다.

## 재현 방법과 비교 항목

공식 카드의 CPU Transformers 예제를 출발점으로 모델·tokenizer revision을 고정합니다. 짧은 영어 요약·형식 준수 과제를 먼저 확인하고 한국어는 별도 입력으로 평가합니다. 135M과 1.7B 모델의 기능 설명을 구분합니다.

## 결과를 해석할 때

공식 카드는 주로 영어를 이해·생성한다고 설명하며, 함수 호출 설명도 크기별 차이가 있습니다. 작은 크기가 모든 장치에서 빠른 실행을 보장하지는 않습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) · [공식 실행 코드 또는 참고 자료](https://arxiv.org/abs/2502.02737)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

SmolLM2 135M is a concrete Hugging Face model release, while the Hub hosts many independent authors. Size-specific language and tool capabilities still need checking. This is a source-based release analysis; model inference was not run locally.
