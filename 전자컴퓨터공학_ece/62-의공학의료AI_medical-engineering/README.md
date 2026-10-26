# 의공학과 의료 AI / Biomedical engineering and medical AI

몸의 신호를 측정하고 해석하며, 의사소통·움직임을 돕거나 진단·치료에 연결하는 공학을 공부합니다. MRI를 복원하는 AI, 질환 후보를 찾는 AI, 신경 신호로 장치를 제어하는 기술, AI가 제안한 약물의 임상 평가를 구분합니다.

## 먼저 익힐 개념

[측정에서 진단과 치료까지](해설_notes/측정에서진단과치료까지_medical-ai-evidence.md)에서 공학이 개입하는 단계와 평가 지표를 계산합니다. 질환 비율이 1%인 자체 검사 사례, 영상별로 자료를 나눌 때 생기는 환자 중복, 촬영 시간과 전체 검사 시간의 차이를 다룹니다.

| 학습 경로 | 실제 본문에서 볼 내용 | 비교할 기준 |
|---|---|---|
| [의료영상과 진단](../../논문해설_papers/의료영상과진단_ai-medical-imaging/README.md) | MRI 복원·판독, OCT의 조직 분할·의뢰, 유방촬영 검진, 희귀질환 유사 사례 검색입니다. | 측정·영상·환자·임상 결정의 평가 단위 |
| [신경보철과 재활](../../논문해설_papers/신경보철과재활_neuroprosthetics-rehabilitation/README.md) | 뇌–척수 연결, 활동별 척수자극, 광전 망막보철과 폐회로 신경자극입니다. | 신호 해독·자극·실제 행동의 검증 범위 |
| [AI 신약 개발](../../논문해설_papers/AI신약개발_ai-drug-discovery/README.md) | AI가 관여한 후보와 사람 대상 무작위시험을 연결합니다. | 예측·실험·임상 결과의 대상과 분모 |

처음 읽으실 때에는 위 기초 해설에서 분모와 비교 기준을 익힌 뒤 관심 분야 논문으로 넘어가시면 좋습니다. 학습용 계산은 직접 만든 값으로 표시하고, 원논문의 수치에는 대상·기간·조건을 붙입니다.

## 기존 학습과 연결하기

| 배경 | 이어서 읽을 글 |
|---|---|
| 측정과 잡음 | [센서와 계측](../37-센서계측_sensors-instrumentation/README.md)에서 감도·보정·드리프트를, [신호처리와 제어](../21-신호처리제어_signals-control/README.md)에서 샘플링과 피드백을 읽습니다. |
| 신경 신호와 의사소통 | [기존 BCI 논문](../../논문해설_papers/뇌와신경공학_neuroengineering/README.md)에서 로봇 팔·손글씨·문자·음성의 출력을 비교합니다. |
| 영상 알고리즘 | [컴퓨터 비전](../43-컴퓨터비전_computer-vision/README.md)과 [U-Net](../../논문해설_papers/머신러닝과생성모델_machine-learning/픽셀분류와위치정보복원_unet2015.md)에서 영상 표현과 픽셀 분할의 원리를 읽습니다. |
| 생체분자와 실험 모델 | [AlphaFold 3](../../논문해설_papers/머신러닝과생성모델_machine-learning/생체분자복합체의구조예측_alphafold3_2024.md), [간 칩](../../논문해설_papers/생명과학과진단_life-science-diagnostics/간칩의약물독성예측_liverchip2022.md)에서 구조 예측과 실험 평가의 차이를 읽습니다. |
| 인과 효과 | [관측과 개입](../../논문해설_papers/인과추론_causal-inference/관측과개입을구별하는인과그림_pearl1995.md)과 [임상시험 평균의 질문](../../논문해설_papers/의약품과대사_metabolic-medicine/세마글루티드의체중감량시험_step1-2021.md)에서 비교 설계와 중단·결측을 읽습니다. |

## 연구와 제품의 차이

논문에서 한 참여자가 수행한 과제, 여러 기관의 검증, 제품의 허가 범위와 실제 장기 사용은 서로 다른 근거입니다. [BCI 장치 리뷰](../../제품기술분석_product-technology/진단과바이오제조_diagnostics-biomanufacturing/뇌컴퓨터인터페이스_bci-devices.md), [수술 로봇](../../제품기술분석_product-technology/진단과바이오제조_diagnostics-biomanufacturing/수술로봇의조작과임상근거_surgical-robots2026.md), [광자계수 CT](../../제품기술분석_product-technology/진단과바이오제조_diagnostics-biomanufacturing/광자계수CT의영상과선량_photon-counting-ct2026.md)는 실제 제품과 운용의 비교를 다룹니다.

## English

This learning path connects sensing, image reconstruction, diagnostic support, neural interfaces and AI-assisted drug discovery. The foundational lesson uses original calculations to distinguish denominators, patient-level data splits, workflow time and clinical effects. Paper studies separate engineering mechanisms from the populations, tasks and outcomes actually evaluated. Existing BCI, vision, control and molecular-modeling articles provide background without counting the same study twice.

[공학 분야별 목차](../README.md) · [논문 해설](../../논문해설_papers/README.md) · [전체 목차](../../분야별목차_CATALOG.md)
