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

## 작은 가중치와 생성된 답을 나누어 보기

135M은 약 1억 3,500만 개의 파라미터를 가리킵니다. 직접 계산하면 모두 원소당 2바이트라고 가정한 가중치 본문은 약 270,000,000바이트입니다. 이는 크기를 이해하기 위한 근사 산술이며 실제 다운로드 용량이나 최대 RAM의 측정값이 아닙니다. 캐시·중간값·실행 라이브러리와 다른 자료형의 비용은 더해지거나 달라집니다.

SFT는 입력과 모범 답변으로 조정하는 단계이고 DPO는 선호되는 답과 덜 선호되는 답의 관계를 이용하는 조정입니다. 크기가 작다는 사실과 명령에 맞는 답을 배웠다는 사실은 다른 축입니다. 공식 카드가 함수 호출 대상을 1.7B로 한정한 설명을 135M의 확인된 기능으로 옮기지 않습니다. [크기별 설명과 학습 단계](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct#model-summary)

## 직접 만든 짧은 영어 독해 예

자체 입력을 “Lena packed three red notebooks and two blue notebooks. She gave away one red notebook. How many notebooks remain? Answer with one integer.”로 정하겠습니다. 실제 생성 결과가 아니라 정답 기준을 설계한 예입니다. 남은 수는 3+2−1=4입니다.

| 확인할 부분 | 판정 기준 |
| --- | --- |
| 계산 | 빨강만 세거나 준 물건을 더하지 않고 4를 답해야 합니다. |
| 형식 | 정수 하나라는 요구를 따로 확인합니다. |
| 생성 구간 | 질문을 제외한 새 답변만 판정합니다. |
| 언어 확장 | 같은 문제의 한국어 결과는 별도 항목으로 기록합니다. |

공식 CPU 예제처럼 전체 ID를 decode하면 입력 질문도 출력에 포함될 수 있습니다. 비교할 때는 입력과 새 생성 부분을 구별해야 합니다. 질문에 적힌 ‘three’나 ‘two’를 찾아 정답 근거로 삼는 문자열 검사는 계산 성공을 보여 주지 않습니다. 질문을 반복하기만 한 답도 생성은 했지만 문제를 해결한 답은 아닙니다.

135M에서 이런 짧은 입력의 형식·독해가 무너지는지 먼저 보면 장문 지식 질문의 오류를 더 분명히 해석할 수 있습니다. 그러나 한 사례가 맞았다고 수학 능력을 일반화하지 않습니다. 초소형 모델의 장점을 말하려면 실제 장치의 로딩 시간·생성 속도·정답 기준이 함께 필요하며, 위 270MB 계산을 그 측정의 대용품으로 쓰지 않습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) · [공식 실행 코드 또는 참고 자료](https://arxiv.org/abs/2502.02737)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

SmolLM2 135M is a concrete Hugging Face model release, while the Hub hosts many independent authors. Size-specific language and tool capabilities still need checking. This is a source-based release analysis; model inference was not run locally.
