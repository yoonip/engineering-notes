# Z.ai GLM-4.5-Air

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `zai-org/GLM-4.5-Air` |
| 제공·입출력 | 공개 가중치 · 텍스트·도구 사용 |
| 구조·설정 | MoE · 전체 106B / 활성 12B · 추론 모드 전환 |
| 사용 조건의 표기 | MIT |

## 구조와 용도

Air라는 이름이어도 전체 가중치는 106B입니다. BF16의 단순 payload는 약 212GB가 되므로 활성 12B만 보고 소형 GPU에 모두 들어간다고 판단하면 안 됩니다. 실제 배포에는 양자화·분산·전송량의 조건이 추가됩니다.

## 재현 방법과 비교 항목

공식 배포 지침에서 runtime·모델 revision·FP8 여부를 고정합니다. 도구 선택이 맞는지, 인자 형식이 맞는지, 도구 결과를 반영했는지를 분리해 셉니다. Thinking 모드의 출력 토큰도 예산에 포함합니다.

## 결과를 해석할 때

활성 파라미터 수는 모델 전체 저장량이 아닙니다. 공개 가중치와 서비스 API의 처리 속도를 직접 비교하려면 장치·동시 요청·네트워크 조건이 필요합니다.

[공식 모델 카드 또는 문서](https://huggingface.co/zai-org/GLM-4.5-Air) · [공식 실행 코드 또는 참고 자료](https://github.com/zai-org/GLM-4.5)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Air still denotes 106B total parameters. Tool choice, argument validity, and use of tool results should be scored independently. This is a source-based release analysis; model inference was not run locally.
