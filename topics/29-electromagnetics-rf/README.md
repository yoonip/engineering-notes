# 전자기학 · RF · 안테나

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

전자기학은 전하·전류와 전기장·자기장의 관계를 다룬다. Maxwell 방정식은 전자기 현상의 기본 관계를 표현한다. 회로의 크기가 신호 파장에 비해 작을 때는 집중정수 모델이 유용하지만, 전파 지연이 무시되지 않으면 전송선과 분포 모델이 필요하다.

## 반사와 정합

전송선의 특성 임피던스와 부하 임피던스가 다르면 반사가 생긴다. Smith chart는 복소 임피던스·반사계수·정합 관계를 표현한다. S-parameter는 정해진 기준 임피던스에서 입사파와 반사파의 관계를 나타낸다. 기준면과 calibration 조건이 측정 해석에 영향을 준다.

## RF 회로와 안테나

LNA는 수신 신호를 낮은 잡음으로 증폭하고, mixer는 주파수를 변환하며, VCO·PLL은 주파수와 위상을 생성·제어한다. 안테나의 이득·방사 패턴·대역폭·효율은 서로 다른 특성이다. 잡음지수와 비선형성은 약한 신호와 큰 방해 신호가 공존할 때 중요하다.

HFSS·CST·Sonnet·openEMS는 전자기장 해석, ADS·AWR은 RF 회로·시스템 설계, scikit-rf는 Python 기반 RF 데이터 처리에 쓰인다. VNA는 네트워크의 S-parameter를, spectrum analyzer는 주파수별 신호 성분을 관찰한다.

## 관련 기술

HFSS, CST, ADS, AWR, Sonnet, openEMS, scikit-rf, VNA, Spectrum Analyzer

## 참고 자료

- [scikit-rf documentation](https://scikit-rf.readthedocs.io/en/latest/)
