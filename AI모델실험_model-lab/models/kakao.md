# Kakao Kanana 1.5 2.1B Instruct

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `kakaocorp/kanana-1.5-2.1b-instruct-2505` |
| 제공·입출력 | 공개 가중치 · 한국어·영어 텍스트 |
| 구조·설정 | Dense 언어 모델 · 기본 32k / YaRN 확장 안내 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

모델 카드는 기본 32k와 YaRN을 통한 최대 128k 확장을 구분합니다. 위치 인코딩을 확장하는 설정은 긴 입력의 모든 정보를 정확히 활용한다는 증명과 다릅니다. 기능 호출도 형식이 맞는지와 실제 의도가 맞는지를 나누어 봐야 합니다.

## 재현 방법과 비교 항목

공식 template과 확장 여부를 명시합니다. 기본 길이 이내의 문서와 길이 확장 문서를 따로 비교하고 근거 회수율을 기록합니다. 한국어 도구 설명을 영어로 바꿨을 때 선택과 인자가 유지되는지도 확인할 수 있습니다.

## 결과를 해석할 때

외부 도구의 설명·schema·결과 포맷이 바뀌면 모델이 같아도 결과가 달라질 수 있습니다. 이 문서에서는 도구 실행이나 장문 성능을 측정하지 않았습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/kakaocorp/kanana-1.5-2.1b-instruct-2505) · [공식 실행 코드 또는 참고 자료](https://arxiv.org/abs/2502.18934)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Native context and YaRN extension are different settings. Tool selection accuracy and schema validity should not be merged into one impressionistic score. This is a source-based release analysis; model inference was not run locally.
