# NCSOFT Llama VARCO 8B Instruct

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `NCSOFT/Llama-VARCO-8B-Instruct` |
| 제공·입출력 | 공개 가중치 · 한국어·영어 텍스트 |
| 구조·설정 | Llama 3.1 8B 기반 명령 조정 |
| 사용 조건의 표기 | Llama 3.1 Community License |

## 구조와 용도

개발 기관은 NCSOFT이지만 기반 모델은 Meta Llama 3.1입니다. 모델의 개발자와 기반 계보를 함께 적어야 구조·tokenizer·사용 조건을 설명할 수 있습니다. 회사별 폴더가 모델의 원래 구조까지 독립적으로 발명했다는 의미는 아닙니다.

## 재현 방법과 비교 항목

공식 카드의 Transformers 예제와 template을 사용합니다. 기본 Llama 계열과 한국어 표현·고유명사·문서 질의응답을 비교할 때 같은 입력과 출력 예산을 적용합니다. 추가 학습의 효과는 실제 응답과 오류 유형을 함께 남깁니다.

## 결과를 해석할 때

한국어 조정 모델이라고 모든 한국어 도메인에 적합한 것은 아닙니다. Llama 기반이라는 사실을 생략하고 독립 Apache 배포물로 소개하지 않습니다.

## 기반 모델과 한국어 조정 단계

공식 카드는 한국어·영어의 계속 사전학습과 한국어 SFT·DPO를 구분합니다. 계속 사전학습은 문서의 다음 토큰을 배우는 단계를 이어가는 것이고, SFT는 지시와 모범 답, DPO는 답 사이의 선호 관계를 이용하는 조정입니다. 모델 계보가 같아도 어떤 자료와 목표로 조정했는지에 따라 비교할 과제가 달라집니다. [About the Model](https://huggingface.co/NCSOFT/Llama-VARCO-8B-Instruct#about-the-model)

입력은 역할별 메시지에서 token ID로 변환됩니다. 공식 예제는 문장 종료와 대화 차례 종료에 해당하는 ID를 생성 중단 조건으로 함께 사용합니다. 출력이 끝나는 조건과 내용이 옳다는 조건은 다르며, 입력까지 포함한 decode 결과에서 정답 단어만 찾는 검사도 피해야 합니다. [Direct Use 예제](https://huggingface.co/NCSOFT/Llama-VARCO-8B-Instruct#direct-use)

## 직접 만든 요청·확정 구분 예

자체 평가 문서를 “운영팀은 점검을 금요일 밤으로 옮기자고 요청했습니다. 개발팀은 아직 동의하지 않았습니다. 현재 확정된 일정은 목요일 밤입니다.”로 정하겠습니다. 질문은 “현재 확정 일정과 변경 요청을 구분해 두 항목으로 정리해 주세요.”입니다. 실제 모델 응답은 없습니다.

| 항목 | 정답 기준 | 피해야 할 판단 |
| --- | --- | --- |
| 확정 일정 | 목요일 밤입니다. | 요청된 금요일을 자동으로 최신 확정값으로 고르면 안 됩니다. |
| 변경 요청 | 운영팀이 금요일 밤으로 변경을 요청했습니다. | 요청자의 의사를 개발팀의 동의로 바꾸면 안 됩니다. |
| 근거 | 동의하지 않았다는 상태를 유지합니다. | 대화를 매끄럽게 만들려고 합의를 지어내면 안 됩니다. |

이 과제는 한국어 문장 유창성보다 주체·발화 행위·확정 상태의 보존을 봅니다. 답을 더 정중하게 바꿔도 확정과 제안이 섞이면 오답입니다. 기반 Llama와 비교할 때도 동일한 사실과 출력 요구를 주어야 추가 학습의 효과를 해석할 수 있습니다.

공식 LogicKor 결과에는 자동 평가자의 조건이 있으므로 그 점수를 사람이 모든 업무 메시지의 정확성을 확인한 수치로 읽지 않습니다. 위 세 문장을 읽는 자체 판정표 역시 그 벤치마크를 재현한 것이 아닙니다. 계보·학습 단계·생성 형식·업무 정답을 함께 적어야 ‘한국어에 맞췄습니다’라는 표현이 구체적인 분석이 됩니다.

[공식 모델 카드 또는 문서](https://huggingface.co/NCSOFT/Llama-VARCO-8B-Instruct) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

The developer and base-model lineage answer different questions. This VARCO checkpoint inherits a Llama architecture and should retain the applicable base-model attribution and terms. This is a source-based release analysis; model inference was not run locally.
