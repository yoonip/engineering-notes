# KT Mi:dm 2.0 Mini Instruct

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `K-intelligence/Midm-2.0-Mini-Instruct` |
| 제공·입출력 | 공개 가중치 · 한국어·영어 텍스트 |
| 구조·설정 | Dense · 약 2.3B · Base에서 pruning·distillation |
| 사용 조건의 표기 | MIT |

## 구조와 용도

공식 카드는 11.5B Base와 2.3B Mini를 구분하고 Mini의 pruning·distillation을 설명합니다. Pruning은 구조나 가중치를 줄이고 distillation은 교사 정보를 학생에게 학습시키는 과정이므로 같은 조작이 아닙니다.

## 재현 방법과 비교 항목

공식 template과 실행 경로를 사용합니다. 한국어 존댓말·문맥에 맞는 표현·정확한 정보 추출을 구분하고 같은 질문의 표현을 바꿔 결과가 유지되는지 확인합니다. Base와 비교할 때는 메모리·속도·정답률을 함께 남깁니다.

## 결과를 해석할 때

한국어 문화 적합성이라는 목표가 개별 답변의 사실 정확도를 보장하지는 않습니다. 이 저장소의 작은 교사·학생 실험은 Mi:dm의 실제 압축 학습을 재현한 결과가 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/K-intelligence/Midm-2.0-Mini-Instruct) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/K-intelligence/Midm-2.0-Mini-Instruct)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Pruning changes model structure or weights; distillation changes the learning signal. The Mini release and the small educational experiment are not the same training run. This is a source-based release analysis; model inference was not run locally.
