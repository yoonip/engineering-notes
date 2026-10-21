# 크기별 구조와 정규화: EXAONE 4.0 1.2B | Variant-specific architecture

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `LGAI-EXAONE/EXAONE-4.0-1.2B` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 30층 · Q/KV 헤드 32/8 · 65,536 문맥 |
| 사용 조건의 표기 | EXAONE 개별 라이선스 |

## 구조와 용도

공식 설명의 QK-Reorder-Norm은 attention·MLP 출력 쪽의 정규화 배치와 Q·K 투영 뒤 RMS 정규화를 다룹니다. 정규화는 값의 크기 척도를 다루는 과정이며 ‘틀린 문장을 옳게 고치는 기능’이라는 뜻이 아닙니다. 모델 출력의 내용 정답은 별도 평가가 필요합니다.

[공식 Introduction과 Model Configuration](https://huggingface.co/LGAI-EXAONE/EXAONE-4.0-1.2B#introduction)은 두 크기와 구조 차이를 구분합니다. 32B에 명시된 local/global 3:1 구조를 1.2B의 확정 특징으로 쓰지 않습니다. `enable_thinking`은 생성 입력 형식 선택이고 학습 시 가중치를 갱신하는 optimizer와는 다른 설정입니다.

공식 카드는 한국어·영어·스페인어와 추론 모드 전환을 설명합니다. 32B의 3:1 local/global hybrid attention 설명을 1.2B에도 그대로 적용하면 안 됩니다. 이름이 같은 계열이라도 크기별 구조와 한도가 다릅니다.

## 실행에 필요한 조건과 비교 항목

공식 Transformers 4.54.0 이상 경로와 enable_thinking 설정을 확인합니다. 한국어 사실 추출·계산·형식 지시 과제를 추론 모드별로 나누어 비교합니다. 비임베딩 1.07B와 전체 파라미터 이름 1.2B도 구분합니다.

## 공개 범위와 한계

라이선스는 개별 배포물의 원문을 확인해야 하며 계열 이름만으로 사용 범위를 대신할 수 없습니다. 이 문서에는 실제 EXAONE 응답과 측정 결과를 넣지 않았습니다.

## 추론 모드를 켜는 위치

공식 예제의 `enable_thinking=True`는 tokenizer가 대화 입력을 만드는 단계의 인자입니다. 이미 만든 답에 생각 문장을 덧붙이는 후처리가 아닙니다. 생성에서는 `<think>`로 시작하는 구간과 최종 답을 구분해 읽어야 하며, 출력 길이 제한으로 사고 구간만 남으면 최종 정답을 얻은 것으로 세지 않습니다. [추론 모드 예제](https://huggingface.co/LGAI-EXAONE/EXAONE-4.0-1.2B#reasoning-mode)

32 Q 헤드와 8 KV 헤드는 네 Q 헤드가 K·V 정보를 공유하는 그룹 관계로 이해할 수 있습니다. 이 산술은 캐시 구조를 설명하며 모델 전체 메모리를 1/4로 만들었다는 실측은 아닙니다. 30층이라는 깊이도 30단계의 사람이 읽을 수 있는 논리 증명을 뜻하지 않습니다. 구조 수치와 출력 설명은 다른 대상입니다.

## 크기별 사용 안내

공식 사용 안내는 1.2B의 한국어 일반 대화에서 언어 전환을 줄이기 위한 설정도 따로 적습니다. 따라서 32B의 추천을 모든 1.2B 대화에 그대로 적용하지 않고 과제와 모드에 맞는 설정을 구분합니다. [사용 안내](https://huggingface.co/LGAI-EXAONE/EXAONE-4.0-1.2B#usage-guideline)

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#lg)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/LGAI-EXAONE/EXAONE-4.0-1.2B) · [공식 실행 코드 또는 참고 자료](https://github.com/LG-AI-EXAONE/EXAONE-4.0)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

The 1.2B and 32B variants differ in architecture and context conditions. Reasoning mode and non-embedding parameter counts need explicit labels. This is a source-based release analysis; model inference was not run locally.
