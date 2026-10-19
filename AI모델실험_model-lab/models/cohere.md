# Cohere Labs Aya Expanse 8B

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `CohereLabs/aya-expanse-8b` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 다국어 연구 모델 · 약 8B · 8k 문맥 |
| 사용 조건의 표기 | CC-BY-NC 4.0 및 관련 사용 정책 |

## 구조와 용도

한국어를 포함한 다국어 평가가 목적에 들어 있습니다. 같은 질문을 단순 번역하면 언어마다 정답 난도나 문화적 전제가 달라질 수 있으므로 공통 사실 과제와 언어별 표현 과제를 나누는 편이 해석에 도움이 됩니다.

## 재현 방법과 비교 항목

공식 chat template을 사용하고 한국어·영어의 같은 사실 추출 문제를 쌍으로 준비합니다. 의미 보존·존댓말·고유명사·숫자 정확성을 구분해 셉니다. 출력 길이와 모델별 tokenizer 차이도 기록합니다.

## 결과를 해석할 때

연구용 공개 가중치와 Cohere의 상용 API를 같은 사용 조건으로 취급하면 안 됩니다. 이 배포물은 비상업 라이선스이며 다른 Command·Aya 배포물의 조건도 따로 확인해야 합니다.

## 다국어 대화의 입력 형식

Aya의 chat template은 질문 글자만 이어 붙이는 대신 차례 시작·끝과 사용자·응답자 역할을 표현합니다. 메시지 목록이 token ID로 바뀌고 생성된 ID가 다시 텍스트가 되는 흐름입니다. 역할 표식을 다른 모델의 것으로 바꾸면 같은 자연어 질문도 다른 형식의 입력이 됩니다. 공식 카드의 8k는 문맥 토큰 범위이므로 ‘한국어 8천 글자’와 같다고 가정하지 않습니다. [Aya Expanse 실행 예와 모델 상세](https://huggingface.co/CohereLabs/aya-expanse-8b#how-to-use-aya-expanse)

다국어 모델은 같은 의미를 여러 언어로 다루는 대상을 제공합니다. 그러나 지원 언어 목록만으로 부정·예외·존댓말이 모든 상황에서 보존된다고 판단할 수는 없습니다. 문법이 매끄러운 답과 입력의 조건을 정확히 유지한 답은 따로 볼 필요가 있습니다.

## 직접 만든 한국어·영어 조건 쌍

자체 한국어 입력은 “이 도서관은 화요일에 닫습니다. 다만 매달 첫째 화요일에는 엽니다. 첫째 화요일과 둘째 화요일의 운영 여부를 각각 한 문장으로 답해 주세요.”입니다. 영어 입력은 “The library is closed on Tuesdays, except the first Tuesday of each month. Is it open on the first and the second Tuesday? Answer each separately.”로 정합니다. 실제 추론 결과가 아닌 평가용 문장입니다.

| 판단 대상 | 두 입력에서 공통으로 맞아야 할 내용 |
| --- | --- |
| 첫째 화요일 | 예외가 적용되어 엽니다. |
| 둘째 화요일 | 일반 조건이 적용되어 닫습니다. |
| 범위 | 첫째 화요일의 예외를 모든 화요일로 넓히면 안 됩니다. |
| 한국어 표현 | 독자에게 요청한 존댓말을 유지하는지도 별도로 봅니다. |

내용 두 개 중 하나를 맞혔으면 1/2이며, 말투가 공손하다는 이유로 내용 점수를 올리지 않습니다. 반대로 두 사실이 같다면 영어와 한국어의 문장 길이 차이를 내용 오류로 세지 않습니다. 월의 실제 날짜를 묻지 않았으므로 달력을 임의로 만들어 붙이는 것도 불필요한 정보 추가입니다.

언어별 차이를 보고 싶다면 질문의 사실·예외 수를 유지하고 언어만 바꾸는 방식이 도움이 됩니다. 한 언어에만 어려운 관용구를 넣은 비교는 번역 난도까지 바뀝니다. 이 예의 기준은 문장 안에 닫혀 있어 외부 상식의 영향을 줄이지만, 두 짧은 질문의 결과만으로 23개 언어 전체의 성능을 대표하지는 않습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/CohereLabs/aya-expanse-8b) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/CohereLabs/aya-expanse-8b)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Aya Expanse offers multilingual research weights. Parallel factual tests and language-specific style tests answer different questions. This is a source-based release analysis; model inference was not run locally.
