# 프루닝과 증류의 역할: Mi:dm 2.0 Mini | Pruning and distillation

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `K-intelligence/Midm-2.0-Mini-Instruct` |
| 제공·입출력 | 공개 가중치 · 한국어·영어 텍스트 |
| 구조·설정 | Dense · 약 2.3B · Base에서 pruning·distillation |
| 사용 조건의 표기 | MIT |

## 구조와 용도

Dense 모델의 pruning은 선택한 부분을 제거해 구조나 가중치를 줄이는 과정이고, distillation은 교사의 응답·표현 등으로 학생을 학습시키는 접근입니다. 따라서 실행 파일을 단순 압축하는 일과 다릅니다. Base 자체의 DUS 확장과 Mini를 만드는 압축 과정도 별개 단계입니다.

[공식 Mi:dm 2.0 설명](https://huggingface.co/K-intelligence/Midm-2.0-Mini-Instruct#midm-20)은 11.5B Base와 2.3B Mini의 관계를 밝힙니다. 이 카드만으로 Mini에서 제거한 모든 구조나 교사 신호의 세부 항을 확정하지 않습니다. 로컬 확률 회귀 예의 100% 일치율을 Mi:dm 압축 학습의 성능 증거로 사용하지 않습니다.

## 실행에 필요한 조건과 비교 항목

공식 template과 실행 경로를 사용합니다. 한국어 존댓말·문맥에 맞는 표현·정확한 정보 추출을 구분하고 같은 질문의 표현을 바꿔 결과가 유지되는지 확인합니다. Base와 비교할 때는 메모리·속도·정답률을 함께 남깁니다.

## 공개 범위와 한계

한국어 문화 적합성이라는 목표가 개별 답변의 사실 정확도를 보장하지는 않습니다. 이 저장소의 작은 교사·학생 실험은 Mi:dm의 실제 압축 학습을 재현한 결과가 아닙니다.

## Mini의 크기와 지시 조정을 읽기

Base에서 Mini로 줄였다는 설명은 매개변수 수의 비교와 학습 방법을 함께 담습니다. 11.5B/2.3B는 산술로 5이지만, 이것만으로 실행 속도가 다섯 배이거나 정답률이 같다고 결론 내릴 수는 없습니다. 남은 구조·장치·자료형·입력 길이가 실제 비용에 영향을 줍니다. Pruning과 distillation 이후 instruct 단계까지 거친 배포물이라는 대상 구분도 필요합니다. [Mi:dm 2.0의 Base·Mini 설명](https://huggingface.co/K-intelligence/Midm-2.0-Mini-Instruct#midm-20)

공식 실행 경로는 모델과 tokenizer 외에 `GenerationConfig`도 읽습니다. 생성 설정은 출력 종료·길이·선택 규칙과 관련된 별도 자료입니다. 메시지를 template으로 만든 정수 ID와 BF16 같은 가중치의 숫자 형식을 같은 개념으로 취급하지 않습니다. 출력 전체를 decode한 문자열에는 질문도 포함될 수 있어 새 응답을 구분해야 합니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#kt)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/K-intelligence/Midm-2.0-Mini-Instruct) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/K-intelligence/Midm-2.0-Mini-Instruct)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Pruning changes model structure or weights; distillation changes the learning signal. The Mini release and the small educational experiment are not the same training run. This is a source-based release analysis; model inference was not run locally.
