# 배포 플랫폼과 자체 소형 모델: SmolLM2 135M | Hub and model authorship

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `HuggingFaceTB/SmolLM2-135M-Instruct` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 약 135M Transformer decoder · SFT·DPO |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

Hugging Face Hub는 여러 개발자의 모델·자료를 보관하는 플랫폼입니다. Transformers는 모델 실행 라이브러리이고, 여기서 선택한 SmolLM2는 HuggingFaceTB가 공개한 모델 계열입니다. Hub에 있는 Meta·Google·NAVER의 가중치를 Hugging Face가 직접 학습한 것으로 분류하지 않습니다.

[SmolLM2 공식 카드의 Model Summary·Training](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct#training)은 Transformer decoder, 2조 토큰 사전학습, SFT와 UltraFeedback 기반 DPO를 밝힙니다. 같은 framework로 불러오는 일과 같은 학습법·자료를 썼다는 판단은 다릅니다. 이 저장소의 표준 라이브러리 실험도 Transformers로 SmolLM2를 실행한 기록이 아닙니다.

Hugging Face는 배포 플랫폼이면서 자체 소형 모델도 제공합니다. Hub에 있다는 사실만으로 모델의 원저작자가 Hugging Face인 것은 아닙니다. SmolLM2 135M은 작은 모델의 데이터 구성과 명령 조정 과정을 읽기 좋은 구체적 사례입니다.

## 실행에 필요한 조건과 비교 항목

공식 카드의 CPU Transformers 예제를 출발점으로 모델·tokenizer revision을 고정합니다. 짧은 영어 요약·형식 준수 과제를 먼저 확인하고 한국어는 별도 입력으로 평가합니다. 135M과 1.7B 모델의 기능 설명을 구분합니다.

## 공개 범위와 한계

공식 카드는 주로 영어를 이해·생성한다고 설명하며, 함수 호출 설명도 크기별 차이가 있습니다. 작은 크기가 모든 장치에서 빠른 실행을 보장하지는 않습니다.

## 작은 가중치와 생성된 답을 나누어 보기

135M은 약 1억 3,500만 개의 파라미터를 가리킵니다. 직접 계산하면 모두 원소당 2바이트라고 가정한 가중치 본문은 약 270,000,000바이트입니다. 이는 크기를 이해하기 위한 근사 산술이며 실제 다운로드 용량이나 최대 RAM의 측정값이 아닙니다. 캐시·중간값·실행 라이브러리와 다른 자료형의 비용은 더해지거나 달라집니다.

SFT는 입력과 모범 답변으로 조정하는 단계이고 DPO는 선호되는 답과 덜 선호되는 답의 관계를 이용하는 조정입니다. 크기가 작다는 사실과 명령에 맞는 답을 배웠다는 사실은 다른 축입니다. 공식 카드가 함수 호출 대상을 1.7B로 한정한 설명을 135M의 확인된 기능으로 옮기지 않습니다. [크기별 설명과 학습 단계](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct#model-summary)

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#hugging-face)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) · [공식 실행 코드 또는 참고 자료](https://arxiv.org/abs/2502.02737)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

SmolLM2 135M is a concrete Hugging Face model release, while the Hub hosts many independent authors. Size-specific language and tool capabilities still need checking. This is a source-based release analysis; model inference was not run locally.
