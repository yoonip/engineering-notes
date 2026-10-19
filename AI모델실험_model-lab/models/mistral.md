# Mistral Ministral 8B Instruct 2410

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `mistralai/Ministral-8B-Instruct-2410` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | Dense Transformer · 36층 · GQA · interleaved sliding-window attention |
| 사용 조건의 표기 | Mistral Research License |

## 구조와 용도

긴 문맥을 처리하는 층과 sliding-window 층을 섞습니다. 공식 카드의 attention pattern은 128k·32k·32k·32k입니다. 이를 모든 층이 같은 길이의 KV 캐시를 보관하는 모델로 계산하면 실제 구조를 반영하지 못합니다.

## 재현 방법과 비교 항목

V3-Tekken tokenizer와 공식 mistral-common·mistral-inference 경로를 확인합니다. 모델 카드에는 runtime별 attention 지원 범위 차이가 기록되어 있으므로 설치한 버전에서 가능한 문맥을 다시 확인합니다. 같은 문서 검색 과제를 길이별로 나누어 평가합니다.

## 결과를 해석할 때

이 2410 배포물의 Research License를 Mistral의 다른 Apache 배포물과 혼동하면 안 됩니다. 128k 학습 한도가 모든 runtime의 128k 지원을 뜻하지 않습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/mistralai/Ministral-8B-Instruct-2410) · [공식 실행 코드 또는 참고 자료](https://github.com/mistralai/mistral-inference)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Interleaved attention changes cache behavior. The selected 2410 release has its own research license and runtime-dependent context support. This is a source-based release analysis; model inference was not run locally.
