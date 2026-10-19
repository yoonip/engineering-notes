# Stability AI Stable Diffusion 3.5 Medium

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `stabilityai/stable-diffusion-3.5-medium` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 이미지 |
| 구조·설정 | MMDiT-X · 텍스트 인코더 3개와 latent 이미지 처리 |
| 사용 조건의 표기 | Stability Community License |

## 구조와 용도

이미지 생성에는 본체 외에 텍스트 인코더와 VAE가 함께 작동합니다. 본체 파라미터만 세면 로딩 메모리를 설명하지 못합니다. Prompt의 글자·수량·공간 관계를 나누어 평가하면 보기 좋은 그림과 지시 준수를 구분할 수 있습니다.

## 재현 방법과 비교 항목

공식 Diffusers 또는 ComfyUI 경로에서 구성 요소와 자료형을 기록합니다. seed·step·guidance·해상도를 고정하고 동일 prompt 여러 개를 비교합니다. 인코더 offload를 썼다면 전송에 드는 시간도 기록합니다.

## 결과를 해석할 때

공식 가중치 사용 조건은 Apache 2.0과 다릅니다. 한 seed의 결과를 대표 품질로 제시하거나 이미지 생성물을 실제 사진의 사실 근거로 다루지 않습니다.

## 세 텍스트 인코더와 이미지 복원

이 배포물은 CLIP 계열 둘과 T5 계열 텍스트 인코더를 사용합니다. 문장의 조건 표현과 이미지 latent를 처리하는 본체, 픽셀로 복원하는 VAE는 역할이 다릅니다. 본체만 양자화했다고 나머지 인코더까지 같은 비트 수가 되는 것은 아닙니다. 공식 예제의 `.images[0]`은 첫 이미지 결과이며 답변 문자열을 꺼내는 표현이 아닙니다. [구성 요소와 실행 예제](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium#implementation-details)

step은 갱신 횟수이고 guidance는 조건을 반영하는 생성 설정이므로 서로 대신할 수 없습니다. 해상도의 가로·세로를 모두 두 배로 정하면 픽셀 수는 네 배입니다. 이 산술만으로 실제 메모리·처리 시간이 정확히 네 배라고 확정하지는 않습니다. latent 크기, attention과 구성 요소의 배치도 영향을 줍니다.

## 직접 만든 글자·배치 판정 예

자체 입력을 “A white rectangular sign with exactly the text LAB 17 in black, above a small green arrow pointing right, plain background.”로 정하겠습니다. 실제로 이미지를 생성하지 않았으며 아래는 관측 결과가 아닌 판정 기준입니다.

| 항목 | 확인할 내용 |
| --- | --- |
| 글자 | LAB의 순서와 숫자 17을 유지해야 합니다. |
| 추가 글자 | 요구하지 않은 표지 문구를 넣지 않아야 합니다. |
| 공간 관계 | 표지 아래에 화살표가 있어야 합니다. |
| 방향·색 | 화살표가 오른쪽을 가리키고 초록색이어야 합니다. |

LAB 71은 문자가 선명해도 숫자 순서가 틀린 그림입니다. 화살표가 왼쪽을 가리키는 그림도 예쁘다는 인상과 별개로 조건 오류입니다. 철자·관계·색을 분리하면 어느 지시를 놓쳤는지 기록할 수 있습니다. 한 seed의 성공만 골라 전체 지시 준수라고 보고하지 않습니다.

이 모델에는 긴 T5 입력에 관한 구체적인 주의도 있습니다. 공식 카드는 256토큰을 넘으면 생성물 가장자리에 artifact가 나타날 수 있다고 설명합니다. 이는 한국어 256글자의 절대 한도라는 뜻도, 더 긴 입력이 언제나 실패한다는 뜻도 아닙니다. [Usage & Limitations](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium#usage--limitations) 위 짧은 문장의 성공 여부와 장문 prompt의 가장자리 손상을 별도로 시험할 수 있지만 이 카드에서는 실제 생성·비교를 하지 않았습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium) · [공식 실행 코드 또는 참고 자료](https://github.com/Stability-AI/sd3.5)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Text encoders and the VAE contribute to deployment memory. Fixed seeds and image quality alone do not establish prompt adherence across a test set. This is a source-based release analysis; model inference was not run locally.
