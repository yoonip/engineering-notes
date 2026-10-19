# 독립 실험 집계 지표

`archived_metrics.json`은 2026-10-04의 독립 구현 실험을 집계한 파일이다. smoke 검증 결과는 저장소 최상위 `VALIDATION_RESULTS.json`에 별도로 기록한다. 이 JSON의 정확도·공급전력은 2026-10-19 검사의 새 측정값과는 구분한다.

| 필드 | 의미 |
|---|---|
| `cnn_conditions` | 모델·분할·scale·rounding·학습·평가 조건 |
| `cnn_test_evaluations` | 전체10k test 평가38행; 반복 baseline을 포함 |
| `cifar10_training_seed_statistics` | 설정별 학습 seed 수·평균·표본 표준편차 |
| `qat` | INT6 k4, Conv1/FC k0, 5epoch STE 재학습; validation BEST는4epoch |
| `bn_only` | 가중치 갱신 없는 BN 통계 재보정 |
| `bias_compensation` | validation 평균 오차 보정과 동일 스케줄 대조군; 추가 저장·add 비용 |
| `saved_replay` | 과거 저장 모델 재평가의 label·prediction·logit 일치 여부 |
| `circuit_conditions` | 공급전력 경계·공정·전압·입력 수·제외한 비용 |
| `circuit_measurements` | Level1 28개와 SKY1308개 실행의 집계; idle 대조군 포함 |
| `signed_exhaustive` | 548,864개 signed 입력쌍·mask 조합의 비트 행렬 비교 |

`accuracy`는 퍼센트, `delta_pp`는 같은 bit의 k0 기준 퍼센트포인트다. 회로 전력의 단위는 µW, 에너지는 fJ/MAC이다. 공급전류 전체 적분값을 순수 dynamic power로 해석하지 않는다. clock-on idle도 순수 누설 전력만의 측정은 아니다.

전체 test 평가38행은 38개의 서로 다른 산술 설정이나38개 seed를 뜻하지 않는다. 주 실험, 보수적 k1 추가 평가, 다른 학습 seed, CIFAR100 평가를 합친 수다. 세 seed를 모두 실행한 설정은5개다. seed가1개인 설정의 표준편차는 null이다.

원자료·원본 주장 표·개인 경로·dataset·checkpoint·sample별 label/prediction·실제 입력 CSV·원시 파형·시뮬레이터 로그·공급사 모델은 이 파일에 포함하지 않는다. 원본 논문의 약35% 절감과 약0.4pp 정확도 손실을 동일 동작점에서 재현한 데이터로 사용할 수 없다.

## English

`archived_metrics.json` aggregates independent implementation experiments from October 4, 2026. Source smoke checks are recorded separately in the project's `VALIDATION_RESULTS.json`; the archived accuracy and supply-power values are not new measurements from the October 19 check.

| Field | Meaning |
| --- | --- |
| `cnn_conditions` | Model, split, scales, rounding, training and evaluation conditions |
| `cnn_test_evaluations` | Thirty-eight full 10k-image test evaluation rows, including repeated baselines |
| `cifar10_training_seed_statistics` | Number of seeds, mean and sample standard deviation per configuration |
| `qat` | INT6 k4, Conv1/FC k0, five-epoch STE fine-tuning; validation BEST at epoch 4 |
| `bn_only` | BN-statistic recalibration without weight updates |
| `bias_compensation` | Validation mean-error correction, same-schedule control and added storage/addition cost |
| `saved_replay` | Label, prediction and logit agreement when replaying stored models |
| `circuit_conditions` | Power boundary, process, voltage, input count and excluded costs |
| `circuit_measurements` | Aggregates of 28 Level1 and eight SKY130 runs, including idle controls |
| `signed_exhaustive` | Bit-matrix comparison across 548,864 signed-input/mask combinations |

`accuracy` is a percentage; `delta_pp` is the percentage-point difference from k0 at the same bit width. Circuit units are µW and fJ/MAC. Integrated total supply current is not pure dynamic power; clock-on idle is not a leakage-only measurement.

The 38 evaluation rows combine primary experiments, conservative k1 follow-ups, additional seeds and CIFAR100 evaluation. They are not 38 distinct arithmetic settings or seeds. Five settings have all three training seeds; single-seed standard deviations are `null`.

The file excludes raw data, original claim tables, personal paths, datasets, checkpoints, sample-level labels/predictions, stimuli, waveforms, simulator logs and vendor models. It does not establish reproduction of the original paper's approximately 35% savings and 0.4-percentage-point accuracy loss at a matched operating point.
