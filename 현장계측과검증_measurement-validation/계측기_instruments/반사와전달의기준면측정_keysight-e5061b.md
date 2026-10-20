# 반사와 전달의 기준면 측정 / S11, S21, and calibration planes with the E5061B

케이블 끝에 연결한 필터의 손실을 읽었는데 케이블을 바꾸자 결과가 달라지면, 필터와 측정 경로를 나누어 살펴야 합니다. VNA(Vector Network Analyzer)는 알려진 시험 신호를 가하고 반사·전달 성분의 크기와 위상을 비교하는 장비입니다. E5061B의 50 Ω·2포트 S-parameter 구성으로 수동 필터·감쇠기·케이블의 측정을 설계합니다. 공식 도움말 기반 절차와 자체 계산이며 실물 RF 부품의 측정 결과는 없습니다.

## 모델명 뒤의 옵션과 측정 포트를 확인합니다

이 글의 기준 구성은 E5061B-235로, 100 kHz~3 GHz·50 Ω S-parameter 시험 세트입니다. 3L3/3L4/3L5의 저주파·Gain-Phase 포트나 옵션 005의 임피던스 기능을 이 구성의 기본 기능으로 다루지 않습니다. 포트 1·2의 S-parameter와 별도 LF Out·R·T 포트를 섞으면 입력 범위·교정·연결법을 잘못 적용할 수 있습니다. [공식 옵션 표](https://helpfiles.keysight.com/csg/e5061b/product_information/options.htm), [전면 포트 설명](https://helpfiles.keysight.com/csg/e5061b/overview/front_panel.htm)

VNA를 주파수별 전압계 두 개로만 생각하면 반사와 기준면을 놓치기 쉽습니다. 고주파에서는 신호가 선을 따라 진행하고, 임피던스가 바뀌는 곳에서 일부가 되돌아옵니다. 종단에 가해진 합성 전압과 “그 지점을 향해 진행하는 파”는 서로 다른 양입니다.

## S11과 S21의 아래첨자는 출발점과 관측점을 나타냅니다

S-parameter는 산란 계수로, 기준 임피던스와 다른 포트의 정합 조건 아래 진행파의 비를 표현합니다. 복소수이므로 크기와 위상을 함께 가집니다. S21은 포트 1에서 입사한 파에 대한 포트 2의 출력파, S11은 포트 1의 입사파에 대한 같은 포트의 반사파입니다. S12·S22는 반대 방향의 전달·출력측 반사를 다룹니다. [측정 파라미터 설명](https://helpfiles.keysight.com/csg/e5061b/measurement/setting_measurement_conditions/selecting_measurement_parameters.htm)

자체 예제로 기준 Z0=50 Ω인 이상적인 선 끝에 순수 저항 75 Ω을 연결합니다. 반사계수 Γ는 다음과 같습니다.

```math
\Gamma=\frac{Z_L-Z_0}{Z_L+Z_0}=\frac{75-50}{75+50}=0.2
```

입사 전력 중 반사 비율은 |Γ|²=0.04, 즉 4%입니다. `S11 Log Mag`는 20log10|Γ|≈-13.979 dB이고, return loss를 양의 값으로 정의하면 13.979 dB입니다. “반사 손실이 크다”와 “반사 전력이 크다”는 같은 방향의 표현이 아닙니다. return loss가 클수록 돌아오는 비율은 작습니다. VSWR, 정재파비는 (1+|Γ|)/(1-|Γ|)=1.5입니다.

| 표시량 | 자체 75 Ω 예제 | 의미 |
| --- | --- | --- |
| S11 Log Mag | 약 -13.979 dB | 반사파 크기의 로그 비입니다. |
| Return loss | 약 +13.979 dB | 같은 반사를 양의 손실 값으로 표현합니다. |
| 반사 전력비 | 4% | 입사 전력 중 되돌아오는 몫입니다. |
| VSWR | 1.5 | 정재파 전압의 최대/최소 비입니다. |

S21=-6 dB라는 별도 예제에서는 파의 크기 비가 약 0.501187이고, 동일한 실수 기준 임피던스·정합 조건의 전력비는 약 0.251189입니다. 전압·파 크기에 10log를 쓰거나 dB 값을 그대로 백분율로 읽으면 달라집니다. S21만으로 반사와 소자 내부 소모의 몫을 모두 나눌 수는 없습니다.

## 교정은 측정 경로의 반복 가능한 오차를 다룹니다

SOLT는 Short·Open·Load·Thru 표준을 사용하는 교정 방식입니다. 알려진 반응을 가진 표준들을 측정해 직접파 누설, 정합, 주파수 응답 등 반복 가능한 계통 오차를 추정합니다. 모든 잡음·온도 변화·접점 마모를 없애거나 고장 난 표준을 정상으로 만드는 절차는 아닙니다.

표준의 Open은 단순히 공중에 비어 있는 완전 이상 회로가 아닙니다. 커넥터와 길이·기생 성분의 정의를 가진 실제 표준입니다. 사용한 키트 모델·커넥터·표준 정의를 맞춥니다. 장비에 저장된 다른 키트 이름을 골라 놓고 물리적인 모양만 비슷한 표준을 연결하지 않습니다. E5061B의 키트 표시 (m)/(f)는 장비 쪽 커넥터 기준이므로 표준 이름을 눈짐작으로 고르지 않습니다. [Selecting Calibration Kit](https://helpfiles.keysight.com/csg/e5061b/measurement/calibration/basic_calibrations/selecting_calibration_kit.htm)

```text
VNA P1 ── 케이블 A ── |기준면 1| ── [DUT] ── |기준면 2| ── 케이블 B ── VNA P2
                          ↑ 표준을 연결하는 위치 ↑
```

기준면은 보정한 결과가 어느 물리적 경계의 특성인지 정하는 위치입니다. 케이블 A/B를 연결한 끝에서 교정하면 그 경로를 포함해 오차를 추정합니다. 교정 후 DUT를 연결하려고 새로운 어댑터를 더하면 그 어댑터는 원래 기준면 바깥입니다. 장비 전면에서 교정하고 긴 케이블을 붙인 결과를 DUT 단자 기준으로 부르면 안 됩니다.

## 연결 → 설정 → 관측 → 판정 → 기록

1. 준비·연결: 무전원 수동 소자와 50 Ω 경로를 사용합니다. 외부 전원·DC bias·능동 증폭기를 연결하지 않습니다. 커넥터 상태와 규정 체결 방법을 확인하고, 교정 후 움직임이 작도록 케이블을 고정합니다.
2. 측정 조건: 예제 필터의 관심 구간을 10~100 MHz·201점으로 정합니다. 소자와 장비의 허용 범위 안에서 시험 전력·IF bandwidth를 정하고 S11·S21을 표시합니다. IF bandwidth는 수신 잡음과 측정 시간에 영향을 주는 필터 대역폭입니다.
3. 교정: 실제 키트를 선택한 뒤 케이블 끝 두 곳에서 Full 2-Port를 수행합니다. 각 포트의 Open·Short·Load와 두 기준면 사이 Thru를 측정하고, 절차를 끝내 보정 상태를 확인합니다. 반사만 교정한 1-port와 full 2-port를 같은 것으로 기록하지 않습니다.
4. 검증·관측: 교정에 쓴 표준을 다시 읽는 확인 외에 별도의 알려진 감쇠기 등 검증 소자를 비교합니다. DUT를 연결하고 통과 대역·차단 대역·반사와 반복 연결 결과를 확인합니다. 검증 소자의 값도 주파수·불확실성 조건과 비교합니다.
5. 판정·저장: 합격 주파수·지표·한계를 미리 정의합니다. 스크린샷뿐 아니라 복소 S-parameter 데이터, 기준 임피던스, 주파수점, 장비 상태·교정 계수 포함 여부와 검증 기록을 보관합니다.

교정 버튼 순서와 필요한 표준 조합은 [Full 2-Port Calibration](https://helpfiles.keysight.com/csg/e5061b/measurement/calibration/basic_calibrations/full_2_port_calibration.htm)에서 대조했습니다. 위 주파수점·검증 소자는 자체 시험 계획입니다. 별도의 독립 검증 소자가 없다면 “교정 표준 재확인”의 범위로 기록합니다.

## 자체 계산: 케이블이 반사를 좋아 보이게 만들 수도 있습니다

편도 손실이 1 dB인 이상적인 정합 케이블이 있고 DUT의 반사계수 크기가 0.2라고 가정합니다. 케이블을 보정하지 않은 전면 기준에서는 반사파가 왕복하며 2 dB의 추가 손실을 받습니다. 이때 보이는 크기는 약 0.158866이고 return loss는 약 15.979 dB입니다. DUT의 실제 13.979 dB보다 좋아 보이지만 DUT를 바꾼 것은 아닙니다.

같은 가정에서 S21=-6 dB인 소자 앞뒤에 1 dB 케이블을 하나씩 더하면 총 전달은 -8 dB입니다. 이 단순 합은 모두 정합된 이상 경로의 예제입니다. 실제로는 다중 반사가 있어 dB 두 개를 빼는 것만으로 모든 경로 오차를 제거할 수 없습니다. 케이블 끝의 full 2-port 교정과 임의 상수 빼기를 구분합니다.

```python
from math import log10              # math에서 상용로그 함수를 가져옵니다.
gamma = (75 - 50) / (75 + 50)        # 임피던스로 자체 반사계수를 계산합니다.
rl_db = -20 * log10(abs(gamma))      # abs는 크기이며 양의 return loss를 구합니다.
seen = gamma * 10 ** (-2 / 20)      # 왕복 2 dB의 파 크기 감소를 적용합니다.
print(rl_db, -20 * log10(abs(seen))) # 약 13.979 dB와 15.979 dB를 출력합니다.
```

## 지연 보정과 완전한 경로 제거는 다릅니다

전파 속도를 2×10⁸ m/s로 둔 자체 모형에서 1 m 케이블의 편도 지연은 5 ns입니다. 전달 위상은 10 MHz에서 -18°, 50 MHz에서 -90°입니다. 반사는 왕복하므로 각각 -36°·-180°입니다. 100 MHz 반사는 -360°여서 위상 감싸기 화면에서 0°처럼 보일 수 있습니다. 한 주파수의 평평한 숫자만 보고 케이블 지연이 없다고 판단하지 않습니다.

E5061B의 port extension은 전기적 지연으로 기준면을 옮깁니다. 지연만 지정하면 임피던스 부정합과 모든 손실까지 사라지지 않습니다. 별도의 손실 설정도 있지만 복잡한 치구의 주파수별 반사를 완전한 S-parameter 모형으로 제거하는 것과는 다릅니다. 장비가 제공하는 단순 지연·손실 기능의 범위와 별도 fixture de-embedding의 범위를 구분합니다. [Port Extensions and Loss Values](https://helpfiles.keysight.com/csg/e5061b/measurement/optimizing_measurements/improving_phase_measurement_accuracy.htm)

| 가정한 관측 | 원인 후보 | 분리·조치 |
| --- | --- | --- |
| 케이블을 굽히자 좁은 파형의 위치·위상이 바뀜 | 케이블 상태·접속의 변화 | 고정 후 기준 소자를 다시 읽고 필요하면 교정합니다. |
| S21은 그럴듯하지만 S11이 크게 다름 | 1-port/response만 적용·기준면 불일치 | 적용 교정 종류와 포트·표준 연결을 대조합니다. |
| 어댑터 추가 후 리플이 생김 | 새 경로의 지연·부정합 | 가능한 DUT 경계에서 다시 교정하거나 검증된 경로 모형을 사용합니다. |

원본을 남기지 않고 port extension 숫자를 바꿔 “예쁜 곡선”을 만드는 방법은 원인 분석이 아닙니다. 추가 경로의 길이·표준·보정 전후 데이터와 독립 검증 결과가 있어야 변경 근거를 설명할 수 있습니다.

## 확인 문제

1. 50 Ω 기준에 75 Ω 순수 저항을 연결하면 반사 전력 비율은 얼마일까요?
2. S21=-6 dB를 전력 50% 전달로 읽어도 될까요?
3. 지연만 보정하는 port extension이 어댑터의 부정합까지 제거할까요?

<details>
<summary>해설</summary>

1. Γ=0.2이고 |Γ|²=0.04이므로 4%입니다.
2. 아닙니다. 파 크기는 약 0.5012배, 같은 실수 기준 임피던스의 전력비는 약 0.2512입니다.
3. 아닙니다. 지연·손실 근사와 다중 반사를 포함한 경로 특성 제거를 구분합니다.

</details>

## 판본과 실제 열람 범위

2026-10-21 확인했습니다. [E5061B 공식 Help](https://helpfiles.keysight.com/csg/e5061b/home.htm)의 표시 판본은 Edition 9.01, 2023-06-07, 펌웨어 B.05.8x입니다. Options·Front Panel·Selecting Measurement Parameters·Selecting Calibration Kit·Full 2-Port Calibration·Port Extensions and Loss Values를 읽었습니다. 도움말의 날짜를 현재 판매·지원 여부의 확인으로 대신하지 않았으며, 실물 교정·Touchstone 파일 취득은 수행하지 않았습니다.

## English summary

This passive two-port study distinguishes S11/S21, reflection power, return loss, and the physical calibration plane. The examples show how an uncorrected cable can hide a mismatch and add phase delay. SOLT calibration, independent verification, delay-only port extension, and full fixture de-embedding answer different questions. No physical RF measurements are claimed.
