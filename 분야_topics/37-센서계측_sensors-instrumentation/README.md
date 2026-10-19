# 센서와 계측 | Sensors, Instrumentation & Experiments

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

센서는 온도·압력·빛·가속도·전류 같은 물리량을 전기적 신호로 바꾼다. 측정 시스템은 센서뿐 아니라 구동·증폭·필터·변환기·시간 기준·보정 과정을 포함한다.

## 신호 경로와 오차

AFE는 센서 신호의 증폭·필터·변환 전 처리를 담당한다. Bridge 회로는 저항 변화를 전압 차이로 읽는 데 쓰인다. Offset·gain error·비선형성·잡음·drift는 서로 다른 오차 요인이다. 정확도는 기준값에 얼마나 가까운지, 정밀도는 반복 측정값이 얼마나 모이는지를 나타낸다. 분해능이 높다고 정확도가 자동으로 높아지는 것은 아니다.

## 장비와 자동 측정

DMM은 전압·전류·저항 등의 수치 측정, 오실로스코프는 시간 파형, VNA는 네트워크 특성, 로직애널라이저는 디지털 상태에 적합하다. Probe의 대역폭·입력 임피던스·접지 구조도 대상 회로를 바꿀 수 있다.

SCPI는 계측기 명령 체계다. VISA·PyVISA는 장비 통신에, LabVIEW·NI-DAQ은 계측과 데이터 수집에 쓰인다. 자동 측정에서는 장비 설정·대기 시간·단위·timestamp가 측정값을 해석하는 기준이 된다. Calibration과 측정 불확도는 값의 신뢰 범위를 설명한다.

## 관련 기술

SCPI, PyVISA, Sigrok, PulseView, LabVIEW, NI DAQ, Oscilloscope, VNA

## 참고 자료

- [PyVISA documentation](https://pyvisa.readthedocs.io/en/latest/)


## 개념·유도·모델·검증

[기초부터 읽기](../../문서_docs/공학기초_FOUNDATIONS.md)

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

[Foundations reading guide](../../문서_docs/공학기초_FOUNDATIONS.md#english)

- [Measurement, probe loading and uncertainty](해설_notes/계측_measurement-loading-uncertainty.md#english)
