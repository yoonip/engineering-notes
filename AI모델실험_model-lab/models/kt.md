# KT Mi:dm 2.0 Mini Instruct

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `K-intelligence/Midm-2.0-Mini-Instruct` |
| 제공·입출력 | 공개 가중치 · 한국어·영어 텍스트 |
| 구조·설정 | Dense · 약 2.3B · Base에서 pruning·distillation |
| 사용 조건의 표기 | MIT |

## 구조와 용도

공식 카드는 11.5B Base와 2.3B Mini를 구분하고 Mini의 pruning·distillation을 설명합니다. Pruning은 구조나 가중치를 줄이고 distillation은 교사 정보를 학생에게 학습시키는 과정이므로 같은 조작이 아닙니다.

## 재현 방법과 비교 항목

공식 template과 실행 경로를 사용합니다. 한국어 존댓말·문맥에 맞는 표현·정확한 정보 추출을 구분하고 같은 질문의 표현을 바꿔 결과가 유지되는지 확인합니다. Base와 비교할 때는 메모리·속도·정답률을 함께 남깁니다.

## 결과를 해석할 때

한국어 문화 적합성이라는 목표가 개별 답변의 사실 정확도를 보장하지는 않습니다. 이 저장소의 작은 교사·학생 실험은 Mi:dm의 실제 압축 학습을 재현한 결과가 아닙니다.

## Mini의 크기와 지시 조정을 읽기

Base에서 Mini로 줄였다는 설명은 매개변수 수의 비교와 학습 방법을 함께 담습니다. 11.5B/2.3B는 산술로 5이지만, 이것만으로 실행 속도가 다섯 배이거나 정답률이 같다고 결론 내릴 수는 없습니다. 남은 구조·장치·자료형·입력 길이가 실제 비용에 영향을 줍니다. Pruning과 distillation 이후 instruct 단계까지 거친 배포물이라는 대상 구분도 필요합니다. [Mi:dm 2.0의 Base·Mini 설명](https://huggingface.co/K-intelligence/Midm-2.0-Mini-Instruct#midm-20)

공식 실행 경로는 모델과 tokenizer 외에 `GenerationConfig`도 읽습니다. 생성 설정은 출력 종료·길이·선택 규칙과 관련된 별도 자료입니다. 메시지를 template으로 만든 정수 ID와 BF16 같은 가중치의 숫자 형식을 같은 개념으로 취급하지 않습니다. 출력 전체를 decode한 문자열에는 질문도 포함될 수 있어 새 응답을 구분해야 합니다.

## 직접 만든 한국어 연락문 예

자체 입력은 “거래처 담당자께 보낼 문장을 두 문장으로 다듬어 주세요. 내일 오후 2시 회의가 오후 4시로 바뀌었습니다. 장소는 아직 정하지 않았습니다. 변경 전후 시간을 모두 적고, 장소는 미정이라고 남겨 주세요.”입니다. 실제 생성 결과가 아니라 한국어 사용을 살펴볼 평가 예입니다.

| 구분 | 정답 기준 | 실패 사례 |
| --- | --- | --- |
| 시간 | 오후 2시에서 오후 4시로 바뀌어야 합니다. | 변경 방향을 거꾸로 쓰면 사실 오류입니다. |
| 미정 정보 | 장소는 미정으로 남겨야 합니다. | 익숙한 회의실 이름을 붙이면 정보 추가입니다. |
| 문체 | 거래처에 맞는 존댓말이어야 합니다. | 공손함과 사실 보존은 별도로 판단합니다. |
| 형식 | 요구한 두 문장이어야 합니다. | 인사말을 더해 문장 수가 늘면 형식 위반입니다. |

한국어가 자연스럽더라도 시간 변경을 틀리면 업무 메시지로는 실패입니다. 반대로 사무적인 표현을 골랐다는 이유만으로 문화 이해가 낮다고 단정하지 않습니다. 무엇을 옮겨야 하는지와 누구에게 어떤 문체로 말하는지를 분리한 과제입니다.

Mini와 큰 모델을 비교한다면 이처럼 답 기준을 먼저 고정해야 합니다. 압축된 모델이 한 번 더 짧게 답했다는 관측만으로 연산이 더 적다고 추정하지 않고, 실제 생성 토큰 수와 장치 시간을 따로 기록합니다. 위 숫자 비율과 평가표는 그런 측정값이 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/K-intelligence/Midm-2.0-Mini-Instruct) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/K-intelligence/Midm-2.0-Mini-Instruct)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Pruning changes model structure or weights; distillation changes the learning signal. The Mini release and the small educational experiment are not the same training run. This is a source-based release analysis; model inference was not run locally.
