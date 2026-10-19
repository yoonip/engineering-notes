# LG EXAONE 4.0 1.2B

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `LGAI-EXAONE/EXAONE-4.0-1.2B` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 30층 · Q/KV 헤드 32/8 · 65,536 문맥 |
| 사용 조건의 표기 | EXAONE 개별 라이선스 |

## 구조와 용도

공식 카드는 한국어·영어·스페인어와 추론 모드 전환을 설명합니다. 32B의 3:1 local/global hybrid attention 설명을 1.2B에도 그대로 적용하면 안 됩니다. 이름이 같은 계열이라도 크기별 구조와 한도가 다릅니다.

## 재현 방법과 비교 항목

공식 Transformers 4.54.0 이상 경로와 enable_thinking 설정을 확인합니다. 한국어 사실 추출·계산·형식 지시 과제를 추론 모드별로 나누어 비교합니다. 비임베딩 1.07B와 전체 파라미터 이름 1.2B도 구분합니다.

## 결과를 해석할 때

라이선스는 개별 배포물의 원문을 확인해야 하며 계열 이름만으로 사용 범위를 대신할 수 없습니다. 이 문서에는 실제 EXAONE 응답과 측정 결과를 넣지 않았습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/LGAI-EXAONE/EXAONE-4.0-1.2B) · [공식 실행 코드 또는 참고 자료](https://github.com/LG-AI-EXAONE/EXAONE-4.0)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

The 1.2B and 32B variants differ in architecture and context conditions. Reasoning mode and non-embedding parameter counts need explicit labels. This is a source-based release analysis; model inference was not run locally.
