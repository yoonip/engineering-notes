# 공유 KV 헤드와 지시 조정: Meta Llama 3.2 1B | GQA and instruction tuning

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `meta-llama/Llama-3.2-1B-Instruct` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 자기회귀 Transformer · 약 1.23B · GQA |
| 사용 조건의 표기 | Llama 3.2 Community License 및 사용 정책 |

## 구조와 용도

공식 모델 카드는 자기회귀 Transformer와 SFT·RLHF를 구분해 설명합니다. RLHF는 human feedback, 즉 사람의 선호 정보를 반영하는 강화학습 계열의 조정입니다. 지시 조정은 ‘다음 토큰을 생성하는 구조’를 없애는 일이 아니라 어떤 응답을 더 잘 내도록 가중치를 바꾸는 과정입니다.

[Model Information](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct#model-information)의 GQA와 공유 임베딩은 저장·계산의 구조 정보이고, 지원 언어 목록은 평가·사용 범위 정보입니다. 언어 모델이 한국어 토큰을 생성했다는 사실만으로 해당 언어가 공식 지원 목록에 들어간다고 해석하지 않습니다. Llama 3.1 기반 VARCO와도 판본을 구분합니다.

이 배포물은 1B·3B 텍스트 계열에 속합니다. GQA는 여러 Q 헤드가 K·V 헤드를 공유하여 캐시 저장량을 줄이는 구조입니다. 공식 지원 8개 언어 목록에 한국어는 없으므로 한국어 출력을 생성할 수 있다는 것과 공식 한국어 성능 보장을 구분해야 합니다.

## 실행에 필요한 조건과 비교 항목

가중치 접근 조건을 확인하고 tokenizer의 템플릿을 사용합니다. 한국어 존댓말·숫자·고유명사 유지 과제를 별도로 준비합니다. 원본 텍스트 모델과 공식 양자화 배포물은 문맥 한도도 다를 수 있으므로 모델 ID와 설정 파일을 함께 남깁니다.

## 공개 범위와 한계

Llama 가중치의 사용 조건은 Apache 2.0과 같지 않습니다. 다른 Llama 기반 파생 모델에도 원래 모델의 출처와 적용 조건을 확인해야 합니다.

## GQA와 캐시를 수로 이해하기

자기회귀 생성은 이미 읽은 문맥의 K·V를 캐시에 저장하여 다음 토큰 계산에 이용할 수 있습니다. GQA에서는 여러 Q 헤드가 더 적은 K·V 헤드를 공유합니다. 저장해야 할 K·V 헤드 수가 줄어드는 관계이며, 긴 문맥에서도 메모리가 고정된다는 뜻은 아닙니다. [공식 카드의 구조·크기별 문맥 표](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct#model-information)

## 배포물별 문맥

공식 표에서 원본 텍스트 계열의 128k와 공식 양자화 계열의 8k는 구분되어 있습니다. 파일을 작게 만든 배포물이라도 허용 길이가 원본과 자동으로 같아지지는 않습니다. 캐시 산술, 모델 접근 조건, 실제 과제의 정답률을 각각 보아야 작은 모델을 고르는 이유가 구체적이 됩니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#meta)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct) · [공식 실행 코드 또는 참고 자료](https://github.com/meta-llama/llama-models)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

This note covers the 1B text model and GQA, not every Llama variant. Korean quality needs its own evaluation because Korean is outside the listed eight supported languages. This is a source-based release analysis; model inference was not run locally.
