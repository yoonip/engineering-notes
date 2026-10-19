# Tencent HunyuanVideo의 생성 조건

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `Tencent-Hunyuan/HunyuanVideo` |
| 제공·입출력 | 공개 코드·가중치 · 텍스트 조건의 영상 생성 |
| 구조·설정 | 영상 생성 모델 · 해상도·프레임 차원이 함께 증가합니다. |
| 사용 조건의 표기 | 공식 HunyuanVideo LICENSE 및 Notice |

## 구조와 용도

공식 README는 batch 1의 720×1280·129프레임에 GPU peak memory 60GB, 544×960·129프레임에 45GB를 제시합니다. 이는 문서의 특정 조건이며 이 저장소의 측정값이 아닙니다. 텍스트 모델의 토큰 수만으로 영상 메모리를 설명할 수 없습니다.

## 재현 방법과 비교 항목

공식 Linux·CUDA 설치 경로에서 가중치와 텍스트 인코더를 준비합니다. seed·해상도·프레임 수·step 수를 고정하고 장면 일치·움직임·시간적 일관성을 따로 봅니다. 저해상도와 고해상도 결과는 같은 비용 조건의 비교가 아닙니다.

## 결과를 해석할 때

정지 프레임 하나가 선명해도 시간에 따른 물체 형태가 유지된다는 뜻은 아닙니다. 코드를 공개했다는 사실만으로 다른 모델과 같은 라이선스라고 판단하지 않습니다.

[공식 모델 카드 또는 문서](https://github.com/Tencent-Hunyuan/HunyuanVideo) · [공식 실행 코드 또는 참고 자료](https://github.com/Tencent-Hunyuan/HunyuanVideo/blob/main/LICENSE.txt)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Video comparisons must fix resolution, frame count, steps, and seed. Published peak-memory requirements are not measurements from this repository. This is a source-based release analysis; model inference was not run locally.
