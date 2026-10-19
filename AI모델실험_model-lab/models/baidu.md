# Baidu ERNIE 4.5 0.3B PT

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `baidu/ERNIE-4.5-0.3B-PT` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | Dense · 약 0.36B · 18층 · Q/KV 헤드 16/2 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

ERNIE 4.5 계열에 MoE와 멀티모달 모델이 있어도 이 작은 배포물은 텍스트 dense 모델입니다. 이름 끝의 PT는 Transformer 방식 PyTorch 가중치이며 Paddle 배포물과 파일 형식이 다릅니다.

## 재현 방법과 비교 항목

공식 카드의 Transformers 4.54.0 이상 조건과 템플릿을 확인합니다. 중국어·영어·한국어 문장을 같은 작업에 넣되 한국어는 별도 평가로 다룹니다. 형식 변환이 필요하다면 변환 전후 token ID와 출력 허용오차를 비교합니다.

## 결과를 해석할 때

계열 공통 설명의 heterogeneous MoE를 이 0.3B 모델의 구조로 옮기면 안 됩니다. 작은 가중치 크기만으로 사실 정확도나 한국어 품질을 단정할 수 없습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/baidu/ERNIE-4.5-0.3B-PT) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/baidu/ERNIE-4.5-0.3B-PT)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

This small ERNIE release is dense and text-only. The PT and Paddle variants use different weight formats. This is a source-based release analysis; model inference was not run locally.
