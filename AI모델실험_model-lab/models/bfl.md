# Black Forest Labs FLUX.1-schnell

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `black-forest-labs/FLUX.1-schnell` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 이미지 |
| 구조·설정 | 12B rectified-flow Transformer · 증류로 1~4 step 생성 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

적은 step은 한 번의 연산이 가볍다는 뜻이 아닙니다. 텍스트 인코더·본체·VAE의 로딩과 해상도별 연산이 함께 필요합니다. Schnell과 dev·pro는 배포물과 사용 조건이 다르므로 같은 이름으로 묶어 실행 조건을 대신할 수 없습니다.

## 재현 방법과 비교 항목

공식 Diffusers 예제의 FluxPipeline과 모델 카드를 사용합니다. 1·2·4 step을 같은 seed·해상도에서 비교하고 수량·텍스트 표기·공간 관계·세부 손상을 분리해 기록합니다. 첫 실행과 워밍업 후 실행도 구분합니다.

## 결과를 해석할 때

더 적은 step이 모든 prompt의 품질을 유지한다는 결론은 여러 입력 평가가 필요합니다. 이 문서에는 실제 이미지 생성 측정값을 넣지 않았습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/black-forest-labs/FLUX.1-schnell) · [공식 실행 코드 또는 참고 자료](https://github.com/black-forest-labs/flux)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Schnell trades sampling steps through distillation, but each step still executes a large model. Variant names, licenses, and hardware conditions should remain explicit. This is a source-based release analysis; model inference was not run locally.
