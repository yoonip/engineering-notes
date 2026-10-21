# 적은 단계의 이미지 생성: FLUX.1-schnell | Distilled image generation

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `black-forest-labs/FLUX.1-schnell` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 이미지 |
| 구조·설정 | 12B rectified-flow Transformer · 증류로 1~4 step 생성 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

Rectified flow는 잡음에서 목표 자료 쪽으로 이동하는 흐름을 학습하는 생성 접근입니다. 추론의 step은 그 흐름을 따라 latent를 갱신하는 횟수이며 학습 횟수와 같은 단위가 아닙니다. 공식 카드는 latent adversarial diffusion distillation을 통해 1~4 step 생성을 가능하게 했다고 설명합니다.

[Schnell 개별 카드](https://huggingface.co/black-forest-labs/FLUX.1-schnell#key-features)의 설명을 대상으로 합니다. 저장소의 균등 4bit 예제는 이 증류 학습도 FLUX 실행도 아닙니다. Schnell의 공개 가중치·조건을 dev·pro 서비스에 대입하거나 짧은 step만으로 다른 이미지 모델보다 빠르고 정확하다고 결론 내리지 않습니다.

적은 step은 한 번의 연산이 가볍다는 뜻이 아닙니다. 텍스트 인코더·본체·VAE의 로딩과 해상도별 연산이 함께 필요합니다. Schnell과 dev·pro는 배포물과 사용 조건이 다르므로 같은 이름으로 묶어 실행 조건을 대신할 수 없습니다.

## 실행에 필요한 조건과 비교 항목

공식 Diffusers 예제의 FluxPipeline과 모델 카드를 사용합니다. 1·2·4 step을 같은 seed·해상도에서 비교하고 수량·텍스트 표기·공간 관계·세부 손상을 분리해 기록합니다. 첫 실행과 워밍업 후 실행도 구분합니다.

## 공개 범위와 한계

더 적은 step이 모든 prompt의 품질을 유지한다는 결론은 여러 입력 평가가 필요합니다. 이 문서에는 실제 이미지 생성 측정값을 넣지 않았습니다.

## 텍스트와 잡음에서 픽셀까지

입력 문장은 텍스트 표현으로 바뀌고, 샘플링은 이미지의 압축된 표현인 latent를 갱신합니다. VAE는 이 표현과 픽셀 공간을 연결하는 구성 요소입니다. 따라서 언어 모델처럼 다음 글자 ID를 나열하는 출력 흐름과 다릅니다. 공식 예제의 최종 결과는 `.images[0]`으로 꺼내는 이미지이며 생성 설명 문장이 아닙니다. Schnell 예제는 `guidance_scale=0.0`, 4 step, 고정 난수 생성기를 사용합니다. 다른 변형의 설정을 복사하기보다 해당 배포물의 예제를 기준으로 삼습니다. [공식 모델 카드의 Diffusers 예제](https://huggingface.co/black-forest-labs/FLUX.1-schnell#diffusers)

step은 샘플링 갱신의 횟수입니다. 전체 지연에는 가중치 로딩·텍스트 처리·픽셀 복원도 들어가므로 step을 4에서 2로 줄였다고 총시간이 반드시 절반이 되지는 않습니다. seed는 비교용 난수 조건이며 다른 라이브러리·장치까지 픽셀이 항상 같아진다는 증명도 아닙니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#black-forest-labs)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/black-forest-labs/FLUX.1-schnell) · [공식 실행 코드 또는 참고 자료](https://github.com/black-forest-labs/flux)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Schnell trades sampling steps through distillation, but each step still executes a large model. Variant names, licenses, and hardware conditions should remain explicit. This is a source-based release analysis; model inference was not run locally.
