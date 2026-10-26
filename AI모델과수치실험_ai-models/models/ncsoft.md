# 계속 사전학습과 한국어 조정: Llama VARCO 8B | Continual pretraining and tuning

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `NCSOFT/Llama-VARCO-8B-Instruct` |
| 제공·입출력 | 공개 가중치 · 한국어·영어 텍스트 |
| 구조·설정 | Llama 3.1 8B 기반 명령 조정 |
| 사용 조건의 표기 | Llama 3.1 Community License |

## 구조와 용도

VARCO는 Meta Llama 3.1 8B를 기반으로 한국어·영어 계속 사전학습을 하고 한국어 SFT·DPO를 거친 배포물입니다. 구조를 물려받는 일과 뒤에 어떤 언어·목표로 학습했는지를 구분합니다. 따라서 개발 기관은 NCSOFT, 기반 모델의 개발 기관은 Meta로 적습니다.

[공식 About the Model](https://huggingface.co/NCSOFT/Llama-VARCO-8B-Instruct#about-the-model)은 이 순서를 명시합니다. 별도 문서의 자체 일정 문장은 학습 자료나 실제 응답이 아니라 평가 설계입니다. 공식 LogicKor도 지정 자동 평가자의 결과이므로, 모든 업무 문서를 사람이 검사한 정확도나 원래 Llama 구조의 독립 발명으로 소개하지 않습니다.

## 실행에 필요한 조건과 비교 항목

공식 카드의 Transformers 예제와 template을 사용합니다. 기본 Llama 계열과 한국어 표현·고유명사·문서 질의응답을 비교할 때 같은 입력과 출력 예산을 적용합니다. 추가 학습의 효과는 실제 응답과 오류 유형을 함께 남깁니다.

## 공개 범위와 한계

한국어 조정 모델이라고 모든 한국어 도메인에 적합한 것은 아닙니다. Llama 기반이라는 사실을 생략하고 독립 Apache 배포물로 소개하지 않습니다.

## 기반 모델과 한국어 조정 단계

공식 카드는 한국어·영어의 계속 사전학습과 한국어 SFT·DPO를 구분합니다. 계속 사전학습은 문서의 다음 토큰을 배우는 단계를 이어가는 것이고, SFT는 지시와 모범 답, DPO는 답 사이의 선호 관계를 이용하는 조정입니다. 모델 계보가 같아도 어떤 자료와 목표로 조정했는지에 따라 비교할 과제가 달라집니다. [About the Model](https://huggingface.co/NCSOFT/Llama-VARCO-8B-Instruct#about-the-model)

입력은 역할별 메시지에서 token ID로 변환됩니다. 공식 예제는 문장 종료와 대화 차례 종료에 해당하는 ID를 생성 중단 조건으로 함께 사용합니다. 출력이 끝나는 조건과 내용이 옳다는 조건은 다르며, 입력까지 포함한 decode 결과에서 정답 단어만 찾는 검사도 피해야 합니다. [Direct Use 예제](https://huggingface.co/NCSOFT/Llama-VARCO-8B-Instruct#direct-use)

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#ncsoft)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/NCSOFT/Llama-VARCO-8B-Instruct) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

The developer and base-model lineage answer different questions. This VARCO checkpoint inherits a Llama architecture and should retain the applicable base-model attribution and terms. This is a source-based release analysis; model inference was not run locally.
