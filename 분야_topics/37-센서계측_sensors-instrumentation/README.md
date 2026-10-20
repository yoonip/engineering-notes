# 센서와 계측 | Sensors, Instrumentation & Experiments

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

센서는 온도·압력·빛·가속도·전류 같은 물리량을 전기적 신호로 바꿉니다. 측정 시스템은 센서뿐 아니라 구동·증폭·필터·변환기·시간 기준·보정 과정을 포함합니다.

## 신호 경로와 오차

AFE는 센서 신호의 증폭·필터·변환 전 처리를 담당합니다. Bridge 회로는 저항 변화를 전압 차이로 읽는 데 쓰입니다. Offset·gain error·비선형성·잡음·drift는 서로 다른 오차 요인입니다. 정확도는 기준값에 얼마나 가까운지, 정밀도는 반복 측정값이 얼마나 모이는지를 나타냅니다. 분해능이 높다고 정확도가 자동으로 높아지는 것은 아닙니다.

## 장비와 자동 측정

DMM은 전압·전류·저항 등의 수치 측정, 오실로스코프는 시간 파형, VNA는 네트워크 특성, 로직애널라이저는 디지털 상태에 적합합니다. Probe의 대역폭·입력 임피던스·접지 구조도 대상 회로를 바꿀 수 있습니다.

SCPI는 계측기 명령 체계입니다. VISA·PyVISA는 장비 통신에, LabVIEW·NI-DAQ은 계측과 데이터 수집에 쓰입니다. 자동 측정에서는 장비 설정·대기 시간·단위·timestamp가 측정값을 해석하는 기준이 됩니다. Calibration과 측정 불확도는 값의 신뢰 범위를 설명합니다.

## 두 기준점으로 센서 출력을 읽는 예

다음은 실제 센서 성능을 측정한 결과가 아닌 직접 만든 교정 예입니다. 알려진 기준량 `x`를 가했을 때 전압 `V`를 읽는 장치가 있다고 하겠습니다. 기준량 0에서 0.20 V, 기준량 10에서 2.20 V를 읽었다면, 이 범위에서 직선 관계라고 가정하여 다음과 같이 나타낼 수 있습니다.

```math
V=ax+b,\qquad a=(2.20-0.20)/(10-0)=0.20\text{ V/단위},\qquad b=0.20\text{ V}
```

`a`는 입력 한 단위가 바뀔 때 출력이 얼마나 바뀌는지 나타내는 감도이고, `b`는 입력이 0일 때의 출력인 영점 오프셋입니다. 새 측정이 1.40 V이면 입력 추정값은 `(1.40−0.20)/0.20=6`입니다. 1.40을 감도로 나누기만 하면 7이 되어 영점의 영향을 놓칩니다. 출력 숫자를 읽는 일과 물리량으로 바꾸는 일이 다른 이유입니다.

두 점은 직선을 하나 정하기에 충분하지만 센서가 정말 직선인지 확인하기에는 부족합니다. 별도의 기준량 5에서 1.20 V에 가까운지 관측하면 중간 구간의 일치 여부를 살필 수 있습니다. 교정에 쓴 점의 오차만 작다는 사실을 독립적인 확인 결과처럼 사용하면 안 됩니다. 기준점 자체의 불확도와 온도·시간 변화도 남습니다. 이 예는 단순 산술이며 실제 교정의 전체 불확도 예산을 계산한 것은 아닙니다.

## 잡음을 줄이는 것과 편향을 없애는 것은 다릅니다

같은 입력을 여러 번 측정하면 값이 조금씩 흩어질 수 있습니다. 서로 독립이고 평균이 0인 잡음만 있다고 가정하면, `n`번 평균의 표준편차는 한 번 측정한 표준편차를 `√n`으로 나눈 값입니다. 이 단순 모형에서 한 번의 표준편차가 0.04 V이면 16번 평균은 0.01 V가 됩니다. 앞의 감도 0.20 V/단위를 적용하면 입력의 무작위 변동은 약 0.05단위에 해당합니다.

하지만 모든 값에 0.10 V의 편향이 더해져 있으면 평균을 내어도 그 편향은 그대로 남습니다. 주변 온도가 느리게 변하거나 같은 전원 잡음을 공유하면 측정 간 독립성도 성립하지 않을 수 있습니다. 많이 측정했다는 사실만으로 정확해졌다고 말하지 않고, 무엇이 흩어짐이고 무엇이 공통된 오차인지 나눠 봅니다.

분해능은 이와 또 다른 개념입니다. 가상의 0–4.096 V 범위를 12비트로 나눈 변환기는 코드 한 칸이 약 1 mV입니다. 소수점 셋째 자리까지 표시할 수 있다고 실제 전압이 그 수준으로 정확하다는 뜻은 아닙니다. 증폭기의 오프셋, 기준 전압, 센서의 비선형성, 접촉 저항과 환경 영향이 더 클 수 있습니다. 또한 한 칸 이하의 물리량 변화가 중요하다면 센서 감도와 증폭 배율을 포함해 신호 경로 전체를 설계해야 합니다.

## 검출한계와 반복 관측을 연결합니다

검출한계는 신호를 배경과 구별할 수 있는 수준에 관한 개념입니다. 바탕 신호가 흔들리면 매우 작은 양의 표적이 있어도 ‘없을 때’와 관측이 겹칩니다. 경고 임계값을 낮추면 약한 표적을 더 잡을 수 있지만 거짓 경고도 늘 수 있습니다. 전자 센서와 분자 진단에서 공통으로 등장하는 문제이며, 특정 제품의 검출한계를 임의의 잡음 배수 하나로 확정하지 않습니다.

실제 기록에는 원시 출력과 환산값을 함께 남기면 유용합니다. 예컨대 시간·시료 ID·전압 단위·교정식 버전·환경 온도·판정 결과를 구분합니다. 나중에 교정식을 바꿨을 때 원시 출력이 없으면 환산값을 다시 계산하기 어렵습니다. 같은 숫자라도 센서와 교정 조건이 다르면 직접 비교할 수 없으므로 메타데이터가 측정의 일부가 됩니다. [진단 기술 비교](../../제품리뷰_reviews/진단과바이오제조_diagnostics-biomanufacturing/현장진단의측정대상_point-of-care2026.md)에는 임계값과 분모의 차이를 적용한 사례가 있습니다.

## 확인 문제

1. 직선 교정의 영점이 0.20 V인데 측정 전압을 감도로만 나누면 무엇을 놓칠까요?
2. 독립적인 무작위 잡음을 평균으로 줄이면 일정한 편향도 같은 비율로 줄어들까요?
3. 표시 자릿수가 많으면 별도 기준과 비교할 필요가 없어질까요?

<details>
<summary>해설 보기</summary>

1. 영점 오프셋을 놓칩니다. 먼저 오프셋을 빼고 감도로 나눠야 합니다.
2. 아닙니다. 평균이 줄이는 것은 가정에 맞는 무작위 변동입니다. 공통 편향과 느린 드리프트는 별도로 확인해야 합니다.
3. 아닙니다. 분해능·정밀도·정확도는 다른 성질입니다. 기준과 환경 조건을 포함해 검토해야 합니다.

</details>

## 관련 기술

SCPI, PyVISA, Sigrok, PulseView, LabVIEW, NI DAQ, Oscilloscope, VNA

## 참고 자료

- [PyVISA documentation](https://pyvisa.readthedocs.io/en/latest/)


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [계측: 숫자를 읽는 것에서 믿을 수 있는 결과로](해설_notes/계측_measurement-loading-uncertainty.md)

## English

### Sensors and instrumentation

Sensors convert physical quantities such as temperature, pressure, light, acceleration, and current into electrical signals. A measurement system also includes excitation, amplification, filters, converters, a time reference, and calibration.

### Signal paths and errors

An analog front end amplifies and filters a sensor signal before conversion. Bridge circuits turn resistance changes into differential voltages. Offset, gain error, nonlinearity, noise, and drift are distinct sources of error. Accuracy describes agreement with a reference value; precision describes the distribution of repeated measurements. Higher resolution alone does not guarantee higher accuracy.

### Instruments and automated measurements

A DMM measures quantities such as voltage, current, and resistance. An oscilloscope shows waveforms over time, a VNA measures network behavior, and a logic analyzer captures digital states. A probe's bandwidth, input impedance, and grounding arrangement can affect the circuit being measured.

SCPI defines instrument commands. VISA and PyVISA provide instrument communication, while LabVIEW and NI-DAQ support measurement and data acquisition. Instrument settings, settling time, units, and timestamps give automated measurements their meaning. Calibration and measurement uncertainty describe the confidence associated with a value.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [Measurement, probe loading and uncertainty](해설_notes/계측_measurement-loading-uncertainty.md#english)


## 심화 해설 | Advanced article

- [직선 교정의 불확도: 기울기와 절편을 함께 다루기](해설_notes/직선교정의불확도_linear-calibration.md) · [English](해설_notes/직선교정의불확도_linear-calibration.md#english)
