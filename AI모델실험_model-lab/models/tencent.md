# 시간축을 함께 생성하는 구조: HunyuanVideo | Spatiotemporal video generation

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | 가중치 `tencent/HunyuanVideo` · 코드 `Tencent-Hunyuan/HunyuanVideo` |
| 제공·입출력 | 공개 코드·가중치 · 텍스트 조건의 영상 생성 |
| 구조·설정 | 영상 생성 모델 · 해상도·프레임 차원이 함께 증가합니다. |
| 사용 조건의 표기 | 공식 HunyuanVideo LICENSE 및 Notice |

## 구조와 용도

공식 HunyuanVideo는 텍스트 조건과 영상 latent를 처음에는 두 stream으로 처리한 뒤 하나의 stream에서 결합합니다. Stream은 여기서 표현을 처리하는 경로이고 동영상 네트워크 전송이라는 뜻이 아닙니다. Causal 3D VAE는 시간·공간을 압축한 표현과 영상 픽셀을 연결합니다.

[공식 구조·학습 설명](https://github.com/Tencent-Hunyuan/HunyuanVideo#hunyuanvideo-overall-architecture)은 이미지·영상 공동 학습과 텍스트 인코더를 구분합니다. 가중치 저장소 ID는 `tencent/HunyuanVideo`, 코드 저장소는 `Tencent-Hunyuan/HunyuanVideo`입니다. 공식 비교 표의 고품질 버전과 공개된 fast 버전이 다르다는 주의도 있으므로 발표된 평가를 로컬 공개 가중치의 실측으로 쓰지 않습니다.

공식 README는 batch 1의 720×1280·129프레임에 GPU peak memory 60GB, 544×960·129프레임에 45GB를 제시합니다. 이는 문서의 특정 조건이며 이 저장소의 측정값이 아닙니다. 텍스트 모델의 토큰 수만으로 영상 메모리를 설명할 수 없습니다.

## 실행에 필요한 조건과 비교 항목

공식 Linux·CUDA 설치 경로에서 가중치와 텍스트 인코더를 준비합니다. seed·해상도·프레임 수·step 수를 고정하고 장면 일치·움직임·시간적 일관성을 따로 봅니다. 저해상도와 고해상도 결과는 같은 비용 조건의 비교가 아닙니다.

## 공개 범위와 한계

정지 프레임 하나가 선명해도 시간에 따른 물체 형태가 유지된다는 뜻은 아닙니다. 코드를 공개했다는 사실만으로 다른 모델과 같은 라이선스라고 판단하지 않습니다.

## 영상에서는 시간도 배열의 축입니다

공식 구조는 텍스트 조건과 잡음에서 latent를 만들고 3D VAE로 영상·이미지를 복원하는 흐름입니다. VAE가 시간과 공간을 압축하기 때문에 최종 프레임의 픽셀 배열과 본체가 처리하는 latent 배열은 크기가 다릅니다. 공개 설명의 prompt 재작성도 입력의 표현을 바꾸는 별도 단계이며 원래 조건이 그대로 보존되는지 따로 봐야 합니다. [전체 구조·3D VAE·Prompt Rewrite](https://github.com/Tencent-Hunyuan/HunyuanVideo#hunyuanvideo-overall-architecture)

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#tencent)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://github.com/Tencent-Hunyuan/HunyuanVideo) · [공식 실행 코드 또는 참고 자료](https://github.com/Tencent-Hunyuan/HunyuanVideo/blob/main/LICENSE.txt)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Video comparisons must fix resolution, frame count, steps, and seed. Published peak-memory requirements are not measurements from this repository. This is a source-based release analysis; model inference was not run locally.
