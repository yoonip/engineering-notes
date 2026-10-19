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

## 텍스트와 잡음에서 픽셀까지

입력 문장은 텍스트 표현으로 바뀌고, 샘플링은 이미지의 압축된 표현인 latent를 갱신합니다. VAE는 이 표현과 픽셀 공간을 연결하는 구성 요소입니다. 따라서 언어 모델처럼 다음 글자 ID를 나열하는 출력 흐름과 다릅니다. 공식 예제의 최종 결과는 `.images[0]`으로 꺼내는 이미지이며 생성 설명 문장이 아닙니다. Schnell 예제는 `guidance_scale=0.0`, 4 step, 고정 난수 생성기를 사용합니다. 다른 변형의 설정을 복사하기보다 해당 배포물의 예제를 기준으로 삼습니다. [공식 모델 카드의 Diffusers 예제](https://huggingface.co/black-forest-labs/FLUX.1-schnell#diffusers)

step은 샘플링 갱신의 횟수입니다. 전체 지연에는 가중치 로딩·텍스트 처리·픽셀 복원도 들어가므로 step을 4에서 2로 줄였다고 총시간이 반드시 절반이 되지는 않습니다. seed는 비교용 난수 조건이며 다른 라이브러리·장치까지 픽셀이 항상 같아진다는 증명도 아닙니다.

## 직접 만든 이미지 판정 예

자체 평가 문장을 “A blue square on the left and a yellow circle on the right, on a plain white background.”로 정하겠습니다. 생성하지 않은 평가 입력이며 아래 표도 관측 결과가 아닌 판정 기준입니다.

| 요소 | 확인할 내용 | 실패 사례 |
| --- | --- | --- |
| 대상 | 사각형과 원이 각각 있어야 합니다. | 둘 다 원으로 바뀌면 모양 오류입니다. |
| 색 | 사각형은 파랑, 원은 노랑이어야 합니다. | 색을 서로 바꾸면 속성 결합 오류입니다. |
| 관계 | 사각형이 원의 왼쪽에 있어야 합니다. | 대상은 맞아도 좌우가 바뀌면 관계 오류입니다. |
| 배경 | 단순한 흰색이어야 합니다. | 요구하지 않은 복잡한 장면을 넣으면 지시 이탈입니다. |

네 항목 중 세 개만 맞은 그림을 ‘prompt 전체 준수’라고 세지 않습니다. 예쁜 그림이라는 인상과 조건별 정답은 다르기 때문입니다. 같은 seed에서 step만 달리하여 비교할 수 있지만, 그 비교를 실제로 실행하기 전에는 어느 설정이 더 낫다고 기록하지 않습니다. 작은 글자나 로고를 추가하는 과제라면 모양과 별도로 철자까지 검사해야 합니다. 이 모델은 사실을 확인하는 시스템이 아니므로 그럴듯한 제품 그림을 실제 제품 사진의 증거로 취급하지 않습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/black-forest-labs/FLUX.1-schnell) · [공식 실행 코드 또는 참고 자료](https://github.com/black-forest-labs/flux)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Schnell trades sampling steps through distillation, but each step still executes a large model. Variant names, licenses, and hardware conditions should remain explicit. This is a source-based release analysis; model inference was not run locally.
