# 조건별 오동작과 수율의 경계 / PVT, shmoo plots and characterization

칩이 한 번 동작했다는 기록에는 어느 전압·온도·입력·판정 기준에서 시험했는지가 함께 있어야 합니다. 다른 조건에서도 같은 결과인지, 양산 검사에서 무엇을 선별하는지, 측정 오차를 어떻게 다루는지는 별도 질문입니다. 기준일은 2026-10-21이며 아래 시험표·수치는 직접 구성한 교육용 자료입니다. 실제 칩·생산 설비를 시험한 결과가 아닙니다.

## 시험의 목적부터 구별합니다

Characterization은 소자의 특성과 동작 범위를 여러 조건에서 조사하는 일입니다. 전압·온도·주파수에 따른 경계와 분포, 설계 모형과 실측의 차이를 살핍니다. Production test는 생산품을 정해진 시험·한계값으로 선별하는 검사입니다. Validation은 실제 사용 요구와 시스템 조건에서 기능·성능이 적합한지 확인하는 활동입니다. 조직마다 명칭과 담당 경계가 다를 수 있으므로 보고서에는 실제 확인한 요구와 조건을 적습니다.

[TI의 Amplifier fundamentals and specifications](https://www.ti.com/lit/pdf/slypa73) 6쪽은 양산 probe/final test, 표본의 특성 조사, process corner에서의 설계 모형을 나눕니다. 넓은 조건에서 조사한 표본의 결과와 출하품마다 실행한 검사를 같은 실적으로 세지 않습니다. 설계 시뮬레이션 역시 실제 표본의 측정과 구별합니다.

CP는 보통 wafer 상태에서 수행하는 chip probing을, FT는 보통 패키지 이후의 final test를 가리킵니다. Probe card·socket·handler·배선·열 제어가 다르면 같은 항목의 측정도 달라질 수 있습니다. wafer 좌표와 die 식별자, 패키지 이후 식별자를 연결해야 전후 결과를 추적할 수 있습니다. 시험기 이름이 같다는 사실만으로 두 단계의 조건이 같아지지는 않습니다.

## PVT는 세 가지 조건의 묶음입니다

P는 fabrication process의 변동, V는 공급 전압, T는 온도입니다. Process corner는 소자 특성 변동을 대표하는 모형 조건입니다. 이미 만들어진 같은 칩에서 전원 설정처럼 P를 자유롭게 바꾸는 것은 아닙니다. 다른 표본·lot와 설계 모형을 어떤 근거로 대응시켰는지 남겨야 합니다.

전압은 전원 장비의 설정값·출력 단자값·DUT 핀 근처 값 중 무엇인지 구별합니다. 온도도 챔버 공기·보드·패키지·접합 온도가 같지 않습니다. 소비 전력과 안정화 시간에 따라 차이가 생깁니다. 온도 설정을 적었다고 칩 내부 온도를 직접 측정했다고 쓸 수는 없습니다.

PVT 조합은 제품의 지원 범위와 모형에 맞게 정합니다. 가장 높은 온도 하나만 확인했다고 모든 최악 조건을 찾았다는 뜻은 아닙니다. 앞의 TI 자료도 process corner에서의 설계 모형과 실제 측정을 구분합니다.

## Shmoo는 시험 조건과 판정의 지도입니다

Shmoo plot은 두 조건을 축으로 놓고 각 조합의 결과를 표시하는 그림입니다. 예를 들어 x축은 clock 주파수, y축은 DUT 전압이며 온도·표본·입력 pattern은 고정합니다. 다른 온도는 같은 축·단위의 별도 그림으로 비교할 수 있습니다. [Marvin Test Solutions의 shmoo 설명](https://www.marvintest.com/KB/Q200244/Using-ICEasy-s-Shmoo-Plot-Tool-with-ATEasy)은 축의 범위·간격과 각 조건의 Boolean 판정을 연결합니다.

다음은 가상 디지털 DUT 한 개, 가상의 고정 온도·pattern에서 한 번씩 시험했다고 정한 표입니다. TI의 증폭기 사양이나 실제 부품의 권장 전압·주파수가 아닙니다.

| 가상 DUT 전압 / 주파수 | 80MHz | 100MHz | 120MHz | 140MHz |
|---|---|---|---|---|
| 0.90V | P | P | F | F |
| 0.95V | P | P | P | F |
| 1.00V | P | P | P | P |

P는 지정한 비교가 일치한 조건, F는 불일치한 조건입니다. 총 12점 중 9점 통과로 시험점 통과 비율은 `9/12=75%`입니다. 이것은 칩 12개의 양산 수율이 아닙니다. 같은 DUT를 조건만 바꾸어 재시험했기 때문입니다. 1.00V·140MHz의 P도 그 위 주파수의 동작이나 다른 pattern·온도의 통과를 입증하지 않습니다.

실제 표에는 미시험·통신 오류·측정 불가도 구별합니다. Timeout을 기능 불일치와 합치면 원인이 섞입니다. 재시험할 때에도 실패점과 시험 순서·반복 횟수를 보존합니다. 높은 전압이 늘 모든 동작을 좋게 만든다고 일반화하지 않습니다.

## 판정 설정은 전압과 주파수보다 넓습니다

시험표에는 pattern·firmware·test program의 버전과 checksum, reset·초기화 조건, 기대값과 허용 오차를 연결합니다. 부하·종단·clock source, 입력과 비교 시각, tester site, fixture·socket, 전류 제한 상태, 실제 측정 위치도 포함합니다. 같은 clock 주파수라도 입력이 도착하는 시각과 출력을 읽는 시각이 다르면 다른 시험입니다.

접촉 불량이나 전압 강하가 있으면 시험 경로가 경계를 만들 수 있습니다. site마다 경계가 다르다면 소자 분포와 접촉 경로의 효과를 나눌 자료가 필요합니다. 원시 측정·판정 코드·설정·표본 ID를 함께 보존합니다.

## 전원 설정과 DUT 전압을 따로 기록합니다

자체 DC 모형에서 전원 단자는 1.00V, 부하 전류는 0.40A, 왕복 배선·접점 저항 합계는 0.10Ω이라고 가정합니다. 배선 전압 강하는 `IR=0.04V`, DUT 쪽 전압은 0.96V입니다. 설정값 대비 4% 차이입니다. 실제 fixture를 측정한 값이 아니며 순간 부하·배선 인덕턴스·전원 제어의 동적 변화는 이 모형에 포함하지 않았습니다.

[Keysight의 remote sense 설명](https://www.keysight.com/zz/en/assets/7018-06397/white-papers/5992-3458.pdf)은 전류를 보내는 선과 부하 전압을 감지하는 선을 나누는 4선 감지를 설명합니다. 감지 지점의 전압을 제어에 반영하는 방식이며 모든 핀의 전압·접촉·고속 과도응답을 자동 보장하는 기능은 아닙니다. 실제 사용에서는 해당 모델의 감지 범위·보상 한계와 연결 조건을 확인합니다.

장비 모델·교정 상태·range·분해능·대역폭·측정 위치를 남깁니다. 표시 자릿수가 많거나 반복 산포가 작아도 offset이나 접촉 경로의 편향은 남을 수 있습니다.

## 한 번의 통과와 guardband를 구별합니다

Guardband는 측정 불확실성 등의 조건을 고려하여 규격 한계와 판정 한계 사이에 두는 간격입니다. [Keysight의 Guardbanding Explained](https://www.keysight.com/sg/en/assets/7018-02998/technical-overviews/5990-8121.pdf)는 규격에서 합격 한계를 정하는 offset으로 설명합니다. 측정 불확실성, 장비 간 상관, drift와 허용할 오판 위험에 맞는 판정 규칙이 필요합니다.

자체 예로 어떤 DC 전압의 규격을 0.95~1.05V, 평가한 확장불확실성 U를 0.02V라고 놓겠습니다. `측정값±U` 전체를 규격 안에 두는 규칙을 택하면 측정값의 합격 구간은 0.97~1.03V입니다. 0.96V는 규격 숫자만 보면 안쪽이지만 이 규칙으로는 합격하지 않습니다. U를 절대적인 최대 오차나 불량 확률 0의 보증으로 읽지는 않습니다. 이는 직접 구성한 판정 예이며 제조사의 출하 기준이 아닙니다.

PVT 설계 여유와 계측 불확실성에 따른 판정 여유도 같은 숫자가 아닙니다. 동작 경계에서 얼마나 떨어져 있는지, 시험 장비가 그 값을 얼마나 불확실하게 측정하는지 각각 설명해야 합니다. 한 번 P가 나왔다고 시간 경과·표본 변동·반복성을 모두 만족했다고 기록할 수는 없습니다.

## Binning·coverage·수율에는 분모가 필요합니다

Bin은 시험 결과로 분류한 집합입니다. 합격·실패 원인·속도 등급 등을 나눌 수 있으며 bin 번호의 뜻은 test program과 규칙에 달려 있습니다. [NI의 wafer test 설명](https://www.ni.com/en/solutions/semiconductor/enterprise-data-management-analytics/reducing-quality-escapes-manufacturing.html)은 잘못 폐기한 양품과 잘못 출하한 불량품의 두 손실을 함께 설명합니다. 분류 결과는 시험 기준에 따른 판정이지 모든 고장이 없다는 증명은 아닙니다.

Coverage는 정한 요구·fault model·입력·상태 중 무엇을 시험했는지의 범위입니다. Code coverage, scan fault coverage, 기능·환경 조합 coverage는 분모가 다릅니다. ‘coverage 99%’에는 대상 집합과 계산법이 있어야 하며 field 고장 99%를 잡는다는 뜻으로 바꿀 수 없습니다.

별도 자체 batch에서 고유 제품 30개 중 첫 검사 합격이 27개면 first-pass 비율은 90%입니다. 실패 3개를 정해진 재검사 규칙으로 확인해 1개를 합격 처리했다면 최종 고유 합격은 `28/30≈93.3%`입니다. 재검사 통과 비율 `1/3≈33.3%`와도 다릅니다. 재검사 이유·이전 실패·접촉 조치 등을 보존해야 하며 이 숫자만으로 제조 공정의 품질이 좋아졌다고 결론 내릴 수 없습니다.

## 확인 문제

1. Shmoo의 9/12와 batch의 27/30은 같은 수율입니까?
2. 왕복 0.10Ω·0.40A 모형에서 설정 1.00V를 DUT의 실측 전압으로 적어도 됩니까?
3. 자체 규격·U·판정 규칙에서 측정값 0.96V는 합격입니까?

<details>
<summary>답과 이유</summary>

1. 아닙니다. 앞의 분모는 한 DUT의 시험점 12개이고 뒤는 고유 제품 30개입니다.
2. 안 됩니다. 모형의 DUT 전압은 0.96V이며 실제 시험에서는 측정 위치와 동적 조건까지 확인해야 합니다.
3. 아닙니다. 이 예의 합격 구간은 0.97~1.03V입니다. 다른 판정 규칙에서는 결과가 달라질 수 있으므로 규칙을 함께 기록합니다.

</details>

## English summary

Separate characterization, production screening and system validation. Record the voltage at the DUT, test conditions and decision rule; shmoo-point pass ratios, first-pass yield and retest outcomes have different denominators. The tables and uncertainty calculation here are synthetic examples.

## 원자료와 읽은 범위

2026-10-21에 TI SLYPA73 교육자료 6~7쪽과 OPAx314 데이터시트 SBOS563G, Rev. G(2015-06)의 §6.7·각주를 확인했습니다. [해당 데이터시트](https://www.ti.com/lit/ds/symlink/opa314.pdf)는 25°C 양산 검사와 온도 범위의 characterization·통계 근거를 구별합니다. 제품마다 모든 온도·모든 항목을 전수 측정한다고 일반화하지 않습니다.

Marvin의 2013-04/06 ATEasy 9 사전판 문서는 축·간격·판정 원리에 사용했습니다. Keysight 두 자료는 자산 소개 페이지의 remote sense·guardband 본문을 읽었으며 첨부 PDF 전체 열람으로 표시하지 않습니다. NI의 bin 설명도 대조했습니다. 실제 장비 실행과 생산 수율 관측은 하지 않았습니다.

[함께 읽기: 통신의 고장 분리](차량과설비통신의고장분리_can-ethercat-modbus.md)
