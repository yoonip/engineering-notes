# 전자기학·RF·안테나 | Electromagnetics, RF & Antennas

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

전자기학은 전하·전류와 전기장·자기장의 관계를 다룹니다. Maxwell 방정식은 전자기 현상의 기본 관계를 표현합니다. 회로가 신호 파장에 비해 작으면 집중정수 모델로 다룰 수 있습니다. 전파 지연의 영향이 커지면 전송선과 분포 모델이 필요합니다.

## 반사와 정합

전송선의 특성 임피던스와 부하 임피던스가 다르면 반사가 생깁니다. Smith chart는 복소 임피던스·반사계수·정합 관계를 표현합니다. S-parameter는 정해진 기준 임피던스에서 입사파와 반사파의 관계를 나타냅니다. 기준면과 calibration 조건이 측정 해석에 영향을 줍니다.

## RF 회로와 안테나

LNA는 수신 신호를 낮은 잡음으로 증폭하고, mixer는 주파수를 변환하며, VCO·PLL은 주파수와 위상을 생성·제어합니다. 안테나의 이득·방사 패턴·대역폭·효율은 서로 다른 특성입니다. 잡음지수와 비선형성은 약한 수신 신호와 강한 방해 신호를 함께 다룰 때 중요합니다.

HFSS·CST·Sonnet·openEMS는 전자기장 해석, ADS·AWR은 RF 회로·시스템 설계, scikit-rf는 Python 기반 RF 데이터 처리에 쓰입니다. VNA는 네트워크의 S-parameter를, spectrum analyzer는 주파수별 신호 성분을 관찰합니다.

## 관련 기술

HFSS, CST, ADS, AWR, Sonnet, openEMS, scikit-rf, VNA, Spectrum Analyzer

## 참고 자료

- [scikit-rf documentation](https://scikit-rf.readthedocs.io/en/latest/)


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [전송선과 반사: 배선의 신호 저장과 전달](해설_notes/전송선과반사_transmission-lines-reflections.md)

## English

### Electromagnetics, RF, and antennas

Electromagnetics describes the relationship between charges, currents, and electric and magnetic fields. Maxwell's equations express the fundamental relationships behind these phenomena. A lumped-element circuit model works well when a circuit is small relative to the signal wavelength. When propagation delay matters, transmission-line and distributed models become necessary.

### Reflection and impedance matching

A mismatch between a transmission line's characteristic impedance and its load impedance causes reflections. A Smith chart shows the relationships among complex impedance, reflection coefficient, and matching. S-parameters describe incident and reflected waves at a specified reference impedance. The reference planes and calibration conditions affect how a measurement is interpreted.

### RF circuits and antennas

An LNA amplifies received signals while adding little noise. A mixer translates frequencies, and VCOs and PLLs generate and control frequency and phase. Antenna gain, radiation pattern, bandwidth, and efficiency describe different properties. Noise figure and linearity matter when weak signals coexist with strong interferers.

HFSS, CST, Sonnet, and openEMS support electromagnetic analysis. ADS and AWR support RF circuit and system design, while scikit-rf handles RF data in Python. A VNA measures network S-parameters; a spectrum analyzer shows signal components across frequency.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [Transmission lines and reflections](해설_notes/전송선과반사_transmission-lines-reflections.md#english)


## 심화 해설 | Advanced article

- [사분파장 정합: 선로 길이로 임피던스 바꾸기](해설_notes/사분파장정합_quarter-wave.md) · [English](해설_notes/사분파장정합_quarter-wave.md#english)
