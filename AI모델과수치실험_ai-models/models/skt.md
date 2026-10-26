# 기반 모델과 한국어 추가 학습: A.X 4.0 Light | Qwen lineage and adaptation

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `skt/A.X-4.0-Light` |
| 제공·입출력 | 공개 가중치 · 한국어 중심 텍스트 |
| 구조·설정 | Qwen2.5 기반 추가 학습 · 약 7B · 16,384 문맥 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

A.X 4.0 Light는 Qwen2.5 계열에 한국어 자료를 추가 학습한 배포물입니다. 모델을 다른 회사가 배포해도 기반 구조와 가중치 계보를 함께 적어야 하는 이유입니다. 한국어 지식과 문체를 학습시키는 일은 입력 문서의 숫자를 응용 프로그램이 검산하는 일과 다릅니다.

[공식 Family Highlights와 Light 표](https://huggingface.co/skt/A.X-4.0-Light#ax-40-family-highlights)는 72B와 7B를 함께 설명하므로 문맥·정답률의 대상부터 구분합니다. 카드가 밝힌 추가 학습 범위를 넘어서 전체 데이터·세부 손실·서비스 A.X의 내부 구성을 추정하지 않습니다. 같은 문제를 직접 실행하기 전에는 추가 학습이 특정 업무를 더 잘 풀었다고 쓰지 않습니다.

한국어 데이터를 추가 학습한 배포물입니다. 공식 카드의 계열 설명에는 72B 모델도 있지만 Light의 문맥은 16,384로 별도 표기합니다. 같은 A.X 4.0 이름만 보고 72B의 131,072 한도를 적용하면 안 됩니다.

## 실행에 필요한 조건과 비교 항목

Light의 model ID·tokenizer·template을 함께 고정합니다. 한국어 기업 문서의 수치·약어·표현을 추출하고 기본 Qwen 계열과 비교하려면 입력과 채점 기준을 같게 둡니다. tokenizer 차이는 동일 문장의 token 수로 따로 기록합니다.

## 공개 범위와 한계

한국어 추가 학습이 모든 수학·코드 능력을 같은 방향으로 바꾼다고 단정하지 않습니다. 계열 전체의 홍보 점수를 Light의 직접 측정값처럼 옮기지 않습니다.

## 기업 문서의 글자와 숫자가 답이 되는 과정

메시지 목록은 Light의 template을 거쳐 token ID로 바뀌고 모델은 다음 ID를 생성합니다. 한국어 추가 학습은 입력을 이해하는 데 영향을 줄 수 있지만, 숫자의 단위까지 응용 프로그램이 자동으로 검산해 준다는 뜻은 아닙니다. 일반 A.X 4.0 표와 Lightweight Model Performance 표의 대상도 구분해야 합니다. [Light 전용 평가 표](https://huggingface.co/skt/A.X-4.0-Light#lightweight-model-performance)

한국어 token 수가 적다는 계열 설명을 모든 문서의 고정 절약률로 대입하지 않습니다. 문서 안의 숫자·코드·영어 약어 구성에 따라 길이는 달라질 수 있습니다. 실제 비교에서는 글자가 같은 문서를 각 tokenizer로 변환한 길이와, 생성 답의 의미를 별도로 보아야 합니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#sk-telecom)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/skt/A.X-4.0-Light) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/skt/A.X-4.0-Light)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

The Light variant has its own 16,384-token limit. Family-level benchmark descriptions should not be relabeled as measurements of this smaller checkpoint. This is a source-based release analysis; model inference was not run locally.
