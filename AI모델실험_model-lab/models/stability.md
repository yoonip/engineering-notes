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

[공식 모델 카드 또는 문서](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium) · [공식 실행 코드 또는 참고 자료](https://github.com/Stability-AI/sd3.5)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Text encoders and the VAE contribute to deployment memory. Fixed seeds and image quality alone do not establish prompt adherence across a test set. This is a source-based release analysis; model inference was not run locally.
