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

## GQA와 캐시를 수로 이해하기

자기회귀 생성은 이미 읽은 문맥의 K·V를 캐시에 저장하여 다음 토큰 계산에 이용할 수 있습니다. GQA에서는 여러 Q 헤드가 더 적은 K·V 헤드를 공유합니다. 저장해야 할 K·V 헤드 수가 줄어드는 관계이며, 긴 문맥에서도 메모리가 고정된다는 뜻은 아닙니다. [공식 카드의 구조·크기별 문맥 표](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct#model-information)

실제 Llama 설정과 구별한 자체 모형으로, 2층·KV 헤드 2개·헤드 차원 4·문맥 3토큰·배치 1·원소당 2바이트를 정하겠습니다. K와 V를 합친 본문은 2×2×2×4×3×1×2=192바이트입니다. 같은 모형에서 문맥을 6으로 늘리면 384바이트입니다. 가중치·다른 중간값·할당 부담은 뺀 캐시 산술입니다. 이 작은 수를 Llama 1B의 실제 RAM 사용량으로 쓰지 않습니다.

## 직접 만든 지원 언어와 한국어 비교 예

자체 영어 입력은 “Mina ordered 4 sensors. Two arrived and one of the remaining sensors was canceled. How many are still pending? Answer with one number.”입니다. 비교 기준은 4−2−1=1입니다. 같은 사실을 “센서 4개 중 2개는 도착했고, 남은 것 중 1개를 취소했습니다. 아직 기다리는 수량은 몇 개입니까?”로도 적을 수 있습니다. 둘 다 실행 전의 평가 입력입니다.

| 구분 | 확인할 기준 |
| --- | --- |
| 의미 | 도착·취소·대기를 서로 다른 상태로 다루어야 합니다. |
| 숫자 | 대기 수량 1을 골라야 합니다. |
| 언어 | 한국어 성적은 공식 지원 언어의 성적과 별도로 남깁니다. |
| 배포물 | 원본과 양자화 모델의 문맥·설정을 섞어 기록하지 않습니다. |

한국어 문장이 나왔다고 공식 지원 범위가 바뀌는 것은 아닙니다. 또한 한 번의 영어·한국어 정답만으로 언어 전체의 차이를 추정할 수도 없습니다. 번역 쌍은 조건이 같은지 확인하는 출발점입니다.

공식 표에서 원본 텍스트 계열의 128k와 공식 양자화 계열의 8k는 구분되어 있습니다. 파일을 작게 만든 배포물이라도 허용 길이가 원본과 자동으로 같아지지는 않습니다. 캐시 산술, 모델 접근 조건, 실제 과제의 정답률을 각각 보아야 작은 모델을 고르는 이유가 구체적이 됩니다.

[공식 모델 카드 또는 문서](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct) · [공식 실행 코드 또는 참고 자료](https://github.com/meta-llama/llama-models)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

This note covers the 1B text model and GQA, not every Llama variant. Korean quality needs its own evaluation because Korean is outside the listed eight supported languages. This is a source-based release analysis; model inference was not run locally.
