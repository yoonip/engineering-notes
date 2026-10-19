# NAVER HyperCLOVAX SEED Text 1.5B

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | Dense Transformer · 1.5B · 16k 문맥 |
| 사용 조건의 표기 | HyperCLOVAX SEED 라이선스 |

## 구조와 용도

한국어 언어·문화 지식에 초점을 둔 작은 텍스트 배포물입니다. HyperCLOVA X라는 서비스 계열의 멀티모달 기능을 이 체크포인트의 기능으로 옮기지 않습니다. 사실 지식과 자연스러운 한국어 문체는 별도 평가 항목입니다.

## 재현 방법과 비교 항목

모델 접근 조건과 공식 template을 확인합니다. 한국어 존댓말 변환·호칭 유지·수치 추출·모르는 질문 거절 과제를 준비합니다. 문맥이 길어질수록 입력의 근거 문장 위치를 바꾸어 정답 보존 여부를 기록합니다.

## 결과를 해석할 때

서비스 API와 이 공개 모델의 한도·라이선스는 서로 다를 수 있습니다. 한국 문화 벤치마크의 점수만으로 특정 분야 문서의 사실 정확도를 보장하지 않습니다.

## 지시·질문·종료 표식의 역할

공식 예제는 `tool_list`·`system`·`user` 차례를 구성하고 template으로 입력을 만듭니다. system에 적은 날짜는 실행 환경에서 제공한 조건이며 모델이 스스로 현재 날짜를 알아냈다는 증거가 아닙니다. 실제 글자를 정수 ID로 바꾸는 tokenizer와 답을 생성하는 모델도 구분합니다. [공식 사용 예제](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B#huggingface-usage-example)

해당 예제의 `max_length`는 입력을 포함한 전체 길이 제한이므로 새로 생성할 토큰 수와 혼동하지 않습니다. 입력이 길어진 상태에서 같은 값을 고정하면 답에 남는 공간이 줄 수 있습니다. 원문의 16k 문맥 범위와 예제에 적힌 작은 생성 길이는 모델 한도와 개별 호출 설정이라는 서로 다른 값입니다.

## 직접 만든 호칭·일정 변환 예

자체 입력은 “지훈 과장님이 고객에게 전달할 내용을 두 문장으로 다듬어 주세요. 지훈 과장님은 수요일에 보고서를 보낼 예정이지만, 검토가 늦어지면 목요일에 보낼 수 있습니다. 보낼 날짜가 확정되었다고 쓰지 마세요.”입니다. 실제 생성한 문장이 아니라 아래 조건을 보는 평가용 자료입니다.

| 항목 | 판정 기준 |
| --- | --- |
| 주체 | 보고서를 보내는 사람은 지훈 과장님입니다. |
| 기본 일정 | 수요일은 예정이며 확정이 아닙니다. |
| 조건 | 검토 지연 때 목요일이 가능하다는 관계를 남겨야 합니다. |
| 표현 | 호칭과 존댓말을 지키면서 두 문장으로 적어야 합니다. |

‘목요일에 보내 드립니다’처럼 단정하면 표현은 공손해도 가능성을 확정으로 바꾼 것입니다. ‘고객이 보고서를 보냅니다’처럼 주체가 바뀌는 오류도 따로 셉니다. 한국어의 높임 표현이 자연스럽다는 판단만으로 원문 사실까지 맞았다고 인정하지 않습니다.

같은 내용을 표로 추출한다면 발신자·예정일·지연 조건·대체 가능일을 각각 필드로 둘 수 있습니다. 네 필드 중 세 개만 맞으면 3/4이고 문서 전체 정답은 아닙니다. 수요일의 실제 날짜는 주어지지 않았으므로 연월일을 만들어 채우면 추가 정보입니다. 이처럼 문장 안에 정답 조건을 두면 한국 문화 지식의 평가와 문서 충실성 평가를 구분할 수 있습니다. 이 카드에서는 어느 입력도 실제 모델에 실행하지 않았습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

This 1.5B release is a text model with a 16k context, distinct from the full service ecosystem. Korean style and factual knowledge should be scored separately. This is a source-based release analysis; model inference was not run locally.
