# 전문가 구조와 사고 모드: GLM-4.5-Air | MoE and reasoning modes

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `zai-org/GLM-4.5-Air` |
| 제공·입출력 | 공개 가중치 · 텍스트·도구 사용 |
| 구조·설정 | MoE · 전체 106B / 활성 12B · 추론 모드 전환 |
| 사용 조건의 표기 | MIT |

## 구조와 용도

GLM-4.5-Air의 두 구분을 나누어 읽어야 합니다. MoE는 내부 전문가 망을 일부 선택하는 구조이고, hybrid reasoning은 사고 구간을 사용하는 모드와 즉시 응답 모드를 선택하는 동작입니다. 도구 호출은 모델 밖 프로그램에 전달할 요청이므로 내부 전문가 선택과도 다릅니다.

[개별 공식 카드](https://huggingface.co/zai-org/GLM-4.5-Air#model-introduction)는 base·hybrid reasoning·FP8 배포물과 실행기의 parser 연결을 안내합니다. Base와 후속 조정 모델을 같은 체크포인트로 취급하지 않습니다. 이 글에서는 전체 학습을 다시 수행하지 않았으며, 뒤 버전의 parser·추론 특징을 4.5-Air의 확인된 동작으로 추가하지 않습니다.

Air라는 이름이어도 전체 가중치는 106B입니다. BF16의 단순 payload는 약 212GB가 되므로 활성 12B만 보고 소형 GPU에 모두 들어간다고 판단하면 안 됩니다. 실제 배포에는 양자화·분산·전송량의 조건이 추가됩니다.

## 실행에 필요한 조건과 비교 항목

공식 배포 지침에서 runtime·모델 revision·FP8 여부를 고정합니다. 도구 선택이 맞는지, 인자 형식이 맞는지, 도구 결과를 반영했는지를 분리해 셉니다. Thinking 모드의 출력 토큰도 예산에 포함합니다.

## 공개 범위와 한계

활성 파라미터 수는 모델 전체 저장량이 아닙니다. 공개 가중치와 서비스 API의 처리 속도를 직접 비교하려면 장치·동시 요청·네트워크 조건이 필요합니다.

## hybrid reasoning은 구조 혼합과 다른 표현입니다

여기서 hybrid reasoning은 thinking과 non-thinking 모드를 선택하는 동작을 가리킵니다. Mamba와 attention을 섞은 네트워크라는 뜻으로 바꾸어 읽지 않습니다. Air의 MoE 구조, 출력 사고 모드, 도구 호출 형식은 서로 다른 구분입니다. [GLM-4.5-Air 개별 카드](https://huggingface.co/zai-org/GLM-4.5-Air#model-introduction)

공식 GitHub 저장소는 현재 4.5뿐 아니라 4.6·4.7도 함께 설명합니다. 4.7의 Preserved Thinking·전용 parser 안내를 제목이 같은 저장소라는 이유만으로 4.5-Air에 적용하지 않습니다. 설치한 runtime과 해당 모델의 parser가 맞아야 사고 텍스트·함수 요청·최종 답을 올바르게 구분할 수 있습니다. [버전별 설명](https://github.com/zai-org/GLM-4.5#model-introduction)

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#zai)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/zai-org/GLM-4.5-Air) · [공식 실행 코드 또는 참고 자료](https://github.com/zai-org/GLM-4.5)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Air still denotes 106B total parameters. Tool choice, argument validity, and use of tool results should be scored independently. This is a source-based release analysis; model inference was not run locally.
