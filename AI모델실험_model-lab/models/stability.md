# 텍스트 조건과 이미지 잠재 표현: SD 3.5 Medium | Text conditioning and image latents

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `stabilityai/stable-diffusion-3.5-medium` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 이미지 |
| 구조·설정 | MMDiT-X · 텍스트 인코더 3개와 latent 이미지 처리 |
| 사용 조건의 표기 | Stability Community License |

## 구조와 용도

MMDiT는 텍스트 조건과 이미지 표현을 함께 다루는 diffusion Transformer 계열입니다. VAE의 latent는 이미지를 압축한 내부 배열이며 token ID로 문장을 이어 쓰는 출력과 다릅니다. QK normalization은 attention 비교에 쓰는 수의 크기를 조절하는 정규화입니다. 예를 들어 큰 수가 내적을 압도하지 않도록 표현의 척도를 다루지만 이것만으로 학습 안정성을 증명하지는 않습니다.

[공식 Model Description·Implementation Details](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium#implementation-details)는 세 고정 텍스트 인코더와 혼합 해상도 학습을 설명합니다. 카드에 추가 attention 범위를 12층과 13층으로 서로 다르게 적은 부분이 있어 이 글에서는 그 수를 단일 확정값으로 인용하지 않습니다. 실제 가중치 생성과 학습 재현은 수행하지 않았습니다.

이미지 생성에는 본체 외에 텍스트 인코더와 VAE가 함께 작동합니다. 본체 파라미터만 세면 로딩 메모리를 설명하지 못합니다. Prompt의 글자·수량·공간 관계를 나누어 평가하면 보기 좋은 그림과 지시 준수를 구분할 수 있습니다.

## 실행에 필요한 조건과 비교 항목

공식 Diffusers 또는 ComfyUI 경로에서 구성 요소와 자료형을 기록합니다. seed·step·guidance·해상도를 고정하고 동일 prompt 여러 개를 비교합니다. 인코더 offload를 썼다면 전송에 드는 시간도 기록합니다.

## 공개 범위와 한계

공식 가중치 사용 조건은 Apache 2.0과 다릅니다. 한 seed의 결과를 대표 품질로 제시하거나 이미지 생성물을 실제 사진의 사실 근거로 다루지 않습니다.

## 세 텍스트 인코더와 이미지 복원

이 배포물은 CLIP 계열 둘과 T5 계열 텍스트 인코더를 사용합니다. 문장의 조건 표현과 이미지 latent를 처리하는 본체, 픽셀로 복원하는 VAE는 역할이 다릅니다. 본체만 양자화했다고 나머지 인코더까지 같은 비트 수가 되는 것은 아닙니다. 공식 예제의 `.images[0]`은 첫 이미지 결과이며 답변 문자열을 꺼내는 표현이 아닙니다. [구성 요소와 실행 예제](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium#implementation-details)

step은 갱신 횟수이고 guidance는 조건을 반영하는 생성 설정이므로 서로 대신할 수 없습니다. 해상도의 가로·세로를 모두 두 배로 정하면 픽셀 수는 네 배입니다. 이 산술만으로 실제 메모리·처리 시간이 정확히 네 배라고 확정하지는 않습니다. latent 크기, attention과 구성 요소의 배치도 영향을 줍니다.

## T5 입력 길이의 주의점

이 모델에는 긴 T5 입력에 관한 구체적인 주의도 있습니다. 공식 카드는 256토큰을 넘으면 생성물 가장자리에 artifact가 나타날 수 있다고 설명합니다. 이는 한국어 256글자의 절대 한도라는 뜻도, 더 긴 입력이 언제나 실패한다는 뜻도 아닙니다. [Usage & Limitations](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium#usage--limitations) 짧은 입력의 지시 준수와 장문 prompt의 가장자리 손상은 별도 항목이며, 이 글에서는 실제 생성·비교를 하지 않았습니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#stability-ai)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium) · [공식 실행 코드 또는 참고 자료](https://github.com/Stability-AI/sd3.5)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Text encoders and the VAE contribute to deployment memory. Fixed seeds and image quality alone do not establish prompt adherence across a test set. This is a source-based release analysis; model inference was not run locally.
