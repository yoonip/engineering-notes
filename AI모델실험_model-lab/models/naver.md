# 자료 학습과 지시 조정의 단계: HyperCLOVAX SEED 1.5B | Training stages

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | Dense Transformer · 1.5B · 16k 문맥 |
| 사용 조건의 표기 | HyperCLOVAX SEED 라이선스 |

## 구조와 용도

공식 카드는 문서로 배우는 사전학습 1단계, 높은 품질 자료의 2단계, RFT, SFT를 구분합니다. 여기서 RFT는 rejection sampling fine-tuning입니다. 생성한 후보 중 조건에 맞는 것을 골라 조정 자료로 삼는 접근이며, 문서에서 reinforcement learning이라는 말로 바꾸어 쓰면 안 됩니다.

[공식 Training and Data](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B#training-and-data)는 작은 모델의 긴 문맥 처리를 사전학습부터 SFT까지 다뤘다고 설명합니다. 이 과정의 설명과 16k 설정, 실제 장문 회수 정답률은 별개입니다. 공개 모델의 학습 단계만 다루며 CLOVA X 서비스 전체의 비공개 구조를 추정하지 않습니다.

한국어 언어·문화 지식에 초점을 둔 작은 텍스트 배포물입니다. HyperCLOVA X라는 서비스 계열의 멀티모달 기능을 이 체크포인트의 기능으로 옮기지 않습니다. 사실 지식과 자연스러운 한국어 문체는 별도 평가 항목입니다.

## 실행에 필요한 조건과 비교 항목

모델 접근 조건과 공식 template을 확인합니다. 한국어 존댓말 변환·호칭 유지·수치 추출·모르는 질문 거절 과제를 준비합니다. 문맥이 길어질수록 입력의 근거 문장 위치를 바꾸어 정답 보존 여부를 기록합니다.

## 공개 범위와 한계

서비스 API와 이 공개 모델의 한도·라이선스는 서로 다를 수 있습니다. 한국 문화 벤치마크의 점수만으로 특정 분야 문서의 사실 정확도를 보장하지 않습니다.

## 지시·질문·종료 표식의 역할

공식 예제는 `tool_list`·`system`·`user` 차례를 구성하고 template으로 입력을 만듭니다. system에 적은 날짜는 실행 환경에서 제공한 조건이며 모델이 스스로 현재 날짜를 알아냈다는 증거가 아닙니다. 실제 글자를 정수 ID로 바꾸는 tokenizer와 답을 생성하는 모델도 구분합니다. [공식 사용 예제](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B#huggingface-usage-example)

해당 예제의 `max_length`는 입력을 포함한 전체 길이 제한이므로 새로 생성할 토큰 수와 혼동하지 않습니다. 입력이 길어진 상태에서 같은 값을 고정하면 답에 남는 공간이 줄 수 있습니다. 원문의 16k 문맥 범위와 예제에 적힌 작은 생성 길이는 모델 한도와 개별 호출 설정이라는 서로 다른 값입니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#naver)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

This 1.5B release is a text model with a 16k context, distinct from the full service ecosystem. Korean style and factual knowledge should be scored separately. This is a source-based release analysis; model inference was not run locally.
