# 센서와 계측

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

센서는 온도·압력·빛·가속도·전류 같은 물리량을 전기적 신호로 바꾼다. 측정 시스템은 센서뿐 아니라 구동·증폭·필터·변환기·시간 기준·보정 과정을 포함한다.

## 신호 경로와 오차

AFE는 센서 신호의 증폭·필터·변환 전 처리를 담당한다. Bridge 회로는 저항 변화를 전압 차이로 읽는 데 쓰인다. Offset·gain error·비선형성·잡음·drift는 서로 다른 오차 요인이다. 정확도는 참값과의 관계, 정밀도는 반복 측정의 분포와 관련된다. 분해능이 높다고 정확도가 자동으로 높아지는 것은 아니다.

## 장비와 자동 측정

DMM은 전압·전류·저항 등의 수치 측정, 오실로스코프는 시간 파형, VNA는 네트워크 특성, 로직애널라이저는 디지털 상태에 적합하다. Probe의 대역폭·입력 임피던스·접지 구조도 대상 회로를 바꿀 수 있다.

SCPI는 계측기 명령 체계, VISA·PyVISA는 장비 통신 접근, LabVIEW·NI-DAQ은 계측과 데이터 수집 생태계다. 자동 측정에서는 장비 설정·대기 시간·단위·timestamp가 숫자의 의미를 결정한다. Calibration과 측정 불확도는 값의 신뢰 범위를 설명한다.

## 관련 기술

SCPI, PyVISA, Sigrok, PulseView, LabVIEW, NI DAQ, Oscilloscope, VNA

## 참고 자료

- [PyVISA documentation](https://pyvisa.readthedocs.io/en/latest/)
