# 다국어 선호 학습: Cohere Aya Expanse 8B | Multilingual post-training

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `CohereLabs/aya-expanse-8b` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | 다국어 연구 모델 · 약 8B · 8k 문맥 |
| 사용 조건의 표기 | CC-BY-NC 4.0 및 관련 사용 정책 |

## 구조와 용도

공식 Model Details는 자기회귀 Transformer와 SFT·선호 학습·model merging을 설명합니다. 선호 학습은 여러 답 중 더 적절한 답의 관계를 반영하는 과정이고, merging은 학습된 모델 매개변수를 결합하는 접근입니다. 요청마다 여러 상용 서비스를 합쳐 답한다는 뜻과는 다릅니다.

[Aya Expanse 8B 카드](https://huggingface.co/CohereLabs/aya-expanse-8b#model-details)는 Command 계열의 사전학습 모델과 다국어 후속 연구의 관계를 밝힙니다. Cohere라는 회사, Command 제품군, 연구용 Aya 공개 가중치의 범위를 구분합니다. 별도 문서의 언어 쌍 정답표는 자체 평가 설계이며 카드의 자동 평가자 결과를 재현한 수치가 아닙니다.

한국어를 포함한 다국어 평가가 목적에 들어 있습니다. 같은 질문을 단순 번역하면 언어마다 정답 난도나 문화적 전제가 달라질 수 있으므로 공통 사실 과제와 언어별 표현 과제를 나누는 편이 해석에 도움이 됩니다.

## 실행에 필요한 조건과 비교 항목

공식 chat template을 사용하고 한국어·영어의 같은 사실 추출 문제를 쌍으로 준비합니다. 의미 보존·존댓말·고유명사·숫자 정확성을 구분해 셉니다. 출력 길이와 모델별 tokenizer 차이도 기록합니다.

## 공개 범위와 한계

연구용 공개 가중치와 Cohere의 상용 API를 같은 사용 조건으로 취급하면 안 됩니다. 이 배포물은 비상업 라이선스이며 다른 Command·Aya 배포물의 조건도 따로 확인해야 합니다.

## 다국어 대화의 입력 형식

Aya의 chat template은 질문 글자만 이어 붙이는 대신 차례 시작·끝과 사용자·응답자 역할을 표현합니다. 메시지 목록이 token ID로 바뀌고 생성된 ID가 다시 텍스트가 되는 흐름입니다. 역할 표식을 다른 모델의 것으로 바꾸면 같은 자연어 질문도 다른 형식의 입력이 됩니다. 공식 카드의 8k는 문맥 토큰 범위이므로 ‘한국어 8천 글자’와 같다고 가정하지 않습니다. [Aya Expanse 실행 예와 모델 상세](https://huggingface.co/CohereLabs/aya-expanse-8b#how-to-use-aya-expanse)

다국어 모델은 같은 의미를 여러 언어로 다루는 대상을 제공합니다. 그러나 지원 언어 목록만으로 부정·예외·존댓말이 모든 상황에서 보존된다고 판단할 수는 없습니다. 문법이 매끄러운 답과 입력의 조건을 정확히 유지한 답은 따로 볼 필요가 있습니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#cohere)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/CohereLabs/aya-expanse-8b) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/CohereLabs/aya-expanse-8b)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Aya Expanse offers multilingual research weights. Parallel factual tests and language-specific style tests answer different questions. This is a source-based release analysis; model inference was not run locally.
